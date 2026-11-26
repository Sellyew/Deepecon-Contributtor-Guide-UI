"""Receiving uploads (plan §2.5): in chunks, resumable, with a SHA-256 receipt.

An upload is created with its name, size, and the browser's last-modified time, then receives
chunks in order; the client asks for the current offset to resume after an interruption, and a
resume must be the same file (name, size, last-modified time, and the SHA-256 of its first MiB).
When the last byte arrives, the server computes the SHA-256 of the whole file (the receipt the
contributor compares with their own), checks that it is a ZIP archive, and reads the archive's
directory: file names and sizes only. Nothing is extracted, opened, or run. Files live in private
storage under generated names.

Limits keep one contributor from filling the disk: a byte budget per assignment, a reserve of
free space, and the deletion of unfinished uploads left untouched (expire_uploads). A check that
fails for any reason refuses the file; it never leaves the upload stuck.
"""
import hashlib
import os
import shutil
import zipfile
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from papers.models import log_event

from .models import Upload, max_upload_bytes

HEAD_BYTES = 1024 * 1024        # the first MiB identifies the file when an upload is resumed
NAME_LIMIT = 1024               # characters kept of each name read from an archive's directory


class UploadRefused(Exception):
    """A request the upload cannot take. `code` is translated by the view."""

    def __init__(self, code, **params):
        super().__init__(code)
        self.code, self.params = code, params


def _root():
    return Path(settings.PRIVATE_STORAGE_ROOT).resolve()


def path_of(upload, part=False):
    path = (_root() / upload.storage_name).resolve()
    if not path.is_relative_to(_root()):
        raise UploadRefused("outside_storage")
    return path.with_suffix(".part") if part else path


def _free_bytes():
    _root().mkdir(parents=True, exist_ok=True)
    return shutil.disk_usage(_root()).free


def is_stale(upload):
    return (upload.status == Upload.CHECKING and upload.checking_since is not None
            and timezone.now() - upload.checking_since > timedelta(seconds=settings.UPLOAD_CHECK_STALE_SECONDS))


def _head_sha256(path, length):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        digest.update(stream.read(length))
    return digest.hexdigest()


def start(assignment, name, size, client_modified=None, head_sha256=""):
    """A new upload, or the unfinished one of the same file (to resume it)."""
    name = (name or "").replace("\\", "/").rsplit("/", 1)[-1].strip()[:255]
    if not name.lower().endswith(".zip"):
        raise UploadRefused("not_zip_name")
    limit = max_upload_bytes(assignment.paper)
    if not isinstance(size, int) or size <= 0:
        raise UploadRefused("empty")
    if size > limit:
        raise UploadRefused("too_large", limit=limit)
    with transaction.atomic():
        existing = (assignment.uploads.select_for_update()
                    .filter(original_name=name, size_bytes=size, status=Upload.RECEIVING).order_by("-created_at").first())
        if existing is not None and client_modified is not None and existing.client_modified == client_modified:
            head = min(HEAD_BYTES, size)
            if existing.received_bytes < head:
                # Too little arrived to tell the files apart: start this upload again from the beginning.
                os.truncate(path_of(existing, part=True), 0)
                existing.received_bytes, existing.head_sha256 = 0, head_sha256 or ""
                existing.save(update_fields=["received_bytes", "head_sha256", "updated_at"])
                return existing
            if head_sha256 and existing.head_sha256 == head_sha256:
                return existing
        if existing is not None and client_modified is None:
            raise UploadRefused("resume_with_script")      # the plain form cannot resume; never join two files
        stored = assignment.uploads.exclude(status=Upload.REFUSED)
        if stored.filter(included=True).count() >= settings.MAX_UPLOADS_PER_ASSIGNMENT:
            raise UploadRefused("too_many")
        budget = limit * settings.UPLOAD_BUDGET_FACTOR
        if sum(stored.values_list("size_bytes", flat=True)) + size > budget:
            raise UploadRefused("over_budget", limit=budget)
        if _free_bytes() < size + settings.UPLOAD_DISK_RESERVE_BYTES:
            raise UploadRefused("disk_full")
        upload = Upload(assignment=assignment, original_name=name, size_bytes=size,
                        client_modified=client_modified, head_sha256=head_sha256 or "")
        upload.storage_name = f"uploads/{assignment.public_id}/{upload.public_id}.zip"
        part = path_of(upload, part=True)
        part.parent.mkdir(parents=True, exist_ok=True)
        part.touch(exist_ok=False)
        os.chmod(part, 0o600)
        upload.save()
    log_event(assignment.public_id, "upload_started", assignment, upload_id=upload.public_id, size_bytes=size)
    return upload


def append(upload, offset, stream):
    """Write the next chunk. `offset` must equal the bytes received so far, so a repeated or
    out-of-order chunk is refused, never written twice. Returns the upload, finished if complete."""
    limit = settings.UPLOAD_CHUNK_BYTES
    data = stream.read(limit + 1)
    if len(data) > limit:
        raise UploadRefused("chunk_too_large", limit=limit)
    if not data:
        raise UploadRefused("empty_chunk")
    if _free_bytes() < len(data) + settings.UPLOAD_DISK_RESERVE_BYTES:
        raise UploadRefused("disk_full")
    with transaction.atomic():
        current = Upload.objects.select_for_update().get(pk=upload.pk)
        if current.status != Upload.RECEIVING:
            raise UploadRefused("not_receiving", status=current.status)
        if offset != current.received_bytes:
            raise UploadRefused("wrong_offset", offset=current.received_bytes)
        if current.received_bytes + len(data) > current.size_bytes:
            raise UploadRefused("beyond_size")
        part = path_of(current, part=True)
        on_disk = part.stat().st_size
        if on_disk < current.received_bytes:
            raise UploadRefused("storage_mismatch")
        if on_disk > current.received_bytes:          # a chunk written before its record failed to save
            os.truncate(part, current.received_bytes)
        with open(part, "ab") as out:
            out.write(data)
        current.received_bytes += len(data)
        complete = current.received_bytes == current.size_bytes
        if complete:
            current.status, current.checking_since = Upload.CHECKING, timezone.now()
        current.save(update_fields=["received_bytes", "status", "checking_since", "updated_at"])
    return finish(current) if complete else current


def _directory(path):
    """(entries, count, truncated) from the archive's directory, read without loading a huge one.
    Raises for anything that is not a readable ZIP archive."""
    with open(path, "rb") as stream:
        end = zipfile._EndRecData(stream)              # the end record, ZIP64-aware (standard library)
    if end is None:
        raise zipfile.BadZipFile("no end record")
    count, directory_size = end[zipfile._ECD_ENTRIES_TOTAL], end[zipfile._ECD_SIZE]
    if count > settings.UPLOAD_LIST_LIMIT * 10 or directory_size > settings.UPLOAD_DIRECTORY_MAX_BYTES:
        return [], count, True                         # too large to list safely; the count is still known
    entries, files = [], 0
    with zipfile.ZipFile(path) as archive:             # the directory only: nothing is extracted
        for info in archive.infolist():
            if info.is_dir():
                continue
            files += 1
            if len(entries) < settings.UPLOAD_LIST_LIMIT:
                entries.append([info.filename[:NAME_LIMIT], info.file_size])
    return entries, files, files > len(entries)


def finish(upload):
    """SHA-256 of the whole file, the ZIP check, and the archive's names and sizes. Runs outside
    any database transaction, because hashing a large file takes a while. Any failure refuses the
    file: an upload never stays "checking"."""
    part = path_of(upload, part=True)
    refusal, sha, entries, count, truncated = "", "", [], 0, False
    try:
        digest = hashlib.sha256()
        with open(part, "rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        sha = digest.hexdigest()
        try:
            entries, count, truncated = _directory(part)
        except Exception:                               # not a ZIP, a damaged one, or one Python cannot read
            refusal = "not_zip"
    except Exception:
        refusal = "check_failed"
    with transaction.atomic():
        current = Upload.objects.select_for_update().get(pk=upload.pk)
        current.sha256, current.completed_at = sha, timezone.now()
        if refusal:
            current.status, current.refusal, current.entries = Upload.REFUSED, refusal, []
        else:
            current.status, current.entries, current.entry_count = Upload.RECEIVED, entries, count
            current.entries_truncated = truncated
        current.save()
        if refusal:
            part.unlink(missing_ok=True)
        else:
            final = path_of(current)
            os.replace(part, final)                    # inside the transaction: the record and the file agree
            os.chmod(final, 0o600)
    log_event(current.assignment.public_id, "upload_received" if not refusal else "upload_refused", current.assignment,
              upload_id=current.public_id, size_bytes=current.size_bytes, sha256=sha, files=count,
              **({"reason": refusal} if refusal else {}))
    return current


def store_whole(assignment, uploaded):
    """The form without JavaScript posts the whole file at once; the handler has written it to
    private storage. It is moved into place outside any transaction, then checked like chunks."""
    upload = start(assignment, uploaded.name, uploaded.size)
    part = path_of(upload, part=True)
    try:
        os.replace(uploaded.temporary_file_path(), part)
    except (AttributeError, OSError):
        with open(part, "wb") as out:                   # a small file kept in memory, or another file system
            for chunk in uploaded.chunks(1024 * 1024):
                out.write(chunk)
    os.chmod(part, 0o600)
    with transaction.atomic():
        current = Upload.objects.select_for_update().get(pk=upload.pk)
        if current.status != Upload.RECEIVING or current.received_bytes != 0:
            raise UploadRefused("not_receiving", status=current.status)
        current.received_bytes, current.status, current.checking_since = current.size_bytes, Upload.CHECKING, timezone.now()
        current.save(update_fields=["received_bytes", "status", "checking_since", "updated_at"])
    return finish(current)


def recheck(upload):
    """For a check that never finished (the server stopped while hashing): run it again."""
    with transaction.atomic():
        current = Upload.objects.select_for_update().get(pk=upload.pk)
        if current.status != Upload.CHECKING:
            return current
        current.checking_since = timezone.now()
        current.save(update_fields=["checking_since", "updated_at"])
    return finish(current)


def remove(upload, actor):
    """The contributor removes an archive no submitted version includes (e.g. the wrong file).
    A submitted one can instead be left out of later versions (set_included)."""
    with transaction.atomic():
        current = Upload.objects.select_for_update().get(pk=upload.pk)
        if current.versions.exists():
            raise UploadRefused("in_a_version")
        if current.status == Upload.CHECKING and not is_stale(current):
            raise UploadRefused("checking")
        delete_files(current)
        current.delete()
    log_event(actor, "upload_removed", upload.assignment, upload_id=upload.public_id)


def set_included(upload, included, actor):
    with transaction.atomic():
        current = Upload.objects.select_for_update().get(pk=upload.pk)
        if current.status != Upload.RECEIVED:
            raise UploadRefused("not_received")
        if included and not current.included and current.assignment.uploads.filter(
                included=True).exclude(status=Upload.REFUSED).count() >= settings.MAX_UPLOADS_PER_ASSIGNMENT:
            raise UploadRefused("too_many")
        current.included = included
        current.save(update_fields=["included", "updated_at"])
    log_event(actor, "upload_included" if included else "upload_left_out", upload.assignment, upload_id=upload.public_id)
    return current


def delete_files(upload):
    for path in (path_of(upload, part=True), path_of(upload)):
        path.unlink(missing_ok=True)


def expire_unfinished(days, actor="expire_uploads"):
    """Delete unfinished uploads left untouched for `days` days. Returns how many."""
    cutoff = timezone.now() - timedelta(days=days)
    stale = list(Upload.objects.filter(status=Upload.RECEIVING, updated_at__lt=cutoff).select_related("assignment"))
    for upload in stale:
        delete_files(upload)
        upload.delete()
        log_event(actor, "upload_expired", upload.assignment, upload_id=upload.public_id,
                  received_bytes=upload.received_bytes)
    return len(stale)
