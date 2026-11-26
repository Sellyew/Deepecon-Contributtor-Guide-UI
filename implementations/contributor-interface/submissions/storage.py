"""Receiving uploads (plan §2.5): in chunks, resumable, with a SHA-256 receipt.

An upload is created with its name and size, then receives chunks in order; the client asks
for the current offset to resume after an interruption. When the last byte arrives, the server
computes the SHA-256 of the whole file (the receipt the contributor compares with their own),
checks that it is a ZIP archive, and reads the archive's directory: file names and sizes only.
Nothing is extracted, opened, or run. Files live in private storage under generated names.
"""
import hashlib
import os
import zipfile
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from papers.models import log_event

from .models import Upload, max_upload_bytes


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


def start(assignment, name, size):
    """A new upload, or the unfinished one with the same name and size (to resume it)."""
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
        if existing is not None:
            return existing
        if assignment.uploads.exclude(status=Upload.REFUSED).count() >= settings.MAX_UPLOADS_PER_ASSIGNMENT:
            raise UploadRefused("too_many")
        upload = Upload(assignment=assignment, original_name=name, size_bytes=size)
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
            current.status = Upload.CHECKING        # one request finishes it; others see "checking"
        current.save(update_fields=["received_bytes", "status"])
    return finish(current) if complete else current


def finish(upload):
    """SHA-256 of the whole file, the ZIP check, and the archive's names and sizes.
    Runs outside any database transaction, because hashing a large file takes a while."""
    part = path_of(upload, part=True)
    digest = hashlib.sha256()
    with open(part, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    sha = digest.hexdigest()
    entries, truncated, refusal = [], False, ""
    if not zipfile.is_zipfile(part):
        refusal = "not_zip"
    else:
        try:
            with zipfile.ZipFile(part) as archive:          # the directory only: nothing is extracted
                for info in archive.infolist():
                    if info.is_dir():
                        continue
                    if len(entries) >= settings.UPLOAD_LIST_LIMIT:
                        truncated = True
                        break
                    entries.append([info.filename, info.file_size])
        except (zipfile.BadZipFile, OSError, ValueError):
            refusal = "not_zip"
    with transaction.atomic():
        current = Upload.objects.select_for_update().get(pk=upload.pk)
        current.sha256, current.completed_at = sha, timezone.now()
        if refusal:
            current.status, current.refusal, current.entries = Upload.REFUSED, refusal, []
            part.unlink(missing_ok=True)
        else:
            final = path_of(current)
            os.replace(part, final)
            os.chmod(final, 0o600)
            current.status, current.entries, current.entries_truncated = Upload.RECEIVED, entries, truncated
        current.save()
    log_event(current.assignment.public_id, "upload_received" if not refusal else "upload_refused", current.assignment,
              upload_id=current.public_id, size_bytes=current.size_bytes, sha256=sha, files=len(entries),
              **({"reason": refusal} if refusal else {}))
    return current


def store_whole(assignment, uploaded):
    """The form without JavaScript posts the whole file at once (Django has already written
    it to a temporary file); it is stored through the same steps as chunks."""
    upload = start(assignment, uploaded.name, uploaded.size)
    if upload.received_bytes:
        raise UploadRefused("resume_with_script")
    with transaction.atomic():
        current = Upload.objects.select_for_update().get(pk=upload.pk)
        with open(path_of(current, part=True), "wb") as out:
            for chunk in uploaded.chunks(1024 * 1024):
                out.write(chunk)
        current.received_bytes, current.status = current.size_bytes, Upload.CHECKING
        current.save(update_fields=["received_bytes", "status"])
    return finish(current)


def remove(upload, actor):
    """The contributor removes an archive no submitted version includes (e.g. the wrong file)."""
    with transaction.atomic():
        current = Upload.objects.select_for_update().get(pk=upload.pk)
        if current.versions.exists():
            raise UploadRefused("in_a_version")
        if current.status == Upload.CHECKING:
            raise UploadRefused("checking")
        delete_files(current)
        current.delete()
    log_event(actor, "upload_removed", upload.assignment, upload_id=upload.public_id)


def delete_files(upload):
    for path in (path_of(upload, part=True), path_of(upload)):
        path.unlink(missing_ok=True)
