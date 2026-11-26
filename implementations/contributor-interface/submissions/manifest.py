"""The submission manifest (submission-manifest.schema.json 0.3.0), what a submission still
lacks, and numbered submitted versions."""
import hashlib
import json

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from papers.importers import _validator
from papers.models import log_event

from .models import Submission, SubmissionVersion, Upload, accepted_channels, runnable_required

SCHEMA_VERSION = "0.3.0"


def submission_for(assignment):
    submission, _created = Submission.objects.get_or_create(assignment=assignment)
    return submission


def checklist(paper):
    return list(paper.config.get("materials_checklist") or [])


def received_uploads(assignment):
    return list(assignment.uploads.filter(status=Upload.RECEIVED).order_by("created_at", "pk"))


def _iso(moment):
    return moment.isoformat().replace("+00:00", "Z")


def build(assignment, submitted_version=None):
    """The manifest as the submission stands (not validated)."""
    paper = assignment.paper
    sub = submission_for(assignment)
    answers = {a.checklist_id: a for a in sub.checklist.all()}
    data = {
        "schema_version": SCHEMA_VERSION,
        "paper_id": paper.paper_id,
        "assignment_id": assignment.public_id,
        "channel": sub.channel or None,
        "datasets": [d.export() for d in sub.datasets.all()],
        "checklist_coverage": [
            {"checklist_id": c["id"], "status": answers[c["id"]].status,
             **({"note": answers[c["id"]].note.strip()} if answers[c["id"]].note.strip() else {})}
            for c in checklist(paper) if c["id"] in answers and answers[c["id"]].status],
        "declarations": {"no_restricted_or_confidential_data_included": sub.no_restricted_included},
        "created_at": _iso(timezone.now()),
    }
    if sub.permission_to_share:
        data["declarations"]["permission_to_share_included_data"] = True
    files = [{"path": u.original_name, "size_bytes": u.size_bytes, "sha256": u.sha256} for u in received_uploads(assignment)]
    if files:
        data["files"] = files
    if sub.channel == "public_reference":
        ref = {"repository": sub.pub_repository.strip(), "identifier": sub.pub_identifier.strip(),
               "version": sub.pub_version.strip()}
        if sub.pub_url.strip():
            ref["url"] = sub.pub_url.strip()
        if sub.pub_doi.strip():
            ref["doi"] = sub.pub_doi.strip()
        data["public_reference"] = ref
    if sub.channel == "other_agreed":
        data["other_channel_note"] = sub.other_channel_note.strip()
    package_given = any([sub.master_script.strip(), sub.readme.strip(), sub.software])
    if runnable_required(paper) or package_given:
        package = {"master_script": sub.master_script.strip(), "readme": sub.readme.strip(), "software": sub.software}
        for field in ("dependencies_included", "author_run_log_included", "expected_outputs_included"):
            if getattr(sub, field) is not None:
                package[field] = getattr(sub, field)
        if sub.run_time:
            package["run_time"] = sub.run_time
        if sub.hardware_note.strip():
            package["hardware_note"] = sub.hardware_note.strip()
        data["package"] = package
    if submitted_version is not None:
        data["submitted_version"] = submitted_version
    return data


def schema_problems(data):
    errors = sorted(_validator("submission-manifest").iter_errors(data), key=lambda e: list(e.absolute_path))
    return ["/".join(str(p) for p in e.absolute_path) or "(top level)" for e in errors]


def problems(assignment):
    """What must be done before the contributor can submit, in their interface language."""
    paper = assignment.paper
    sub = submission_for(assignment)
    out = []
    channels = accepted_channels(paper)
    if sub.channel not in channels:
        out.append(_("Choose how the materials reach us."))
    elif sub.channel == "upload" and not received_uploads(assignment):
        out.append(_("Upload your package (a ZIP file), or choose another way to send it."))
    elif sub.channel == "public_reference" and not all([sub.pub_repository.strip(), sub.pub_identifier.strip(),
                                                        sub.pub_version.strip()]):
        out.append(_("Give the public package's repository, identifier, and version."))
    elif sub.channel == "other_agreed" and not sub.other_channel_note.strip():
        out.append(_("Say which channel you agreed with the team."))
    if assignment.uploads.filter(status__in=[Upload.RECEIVING, Upload.CHECKING]).exists():
        out.append(_("An upload is not finished. Finish it, or remove it."))
    if runnable_required(paper):
        if not sub.master_script.strip() or not sub.readme.strip() or not sub.software:
            out.append(_("Name the master script, the README, and the software with its version."))
    answers = {a.checklist_id: a.status for a in sub.checklist.all()}
    missing = [c["id"] for c in checklist(paper)
               if c.get("requirement") in ("required", "confirm_existing") and not answers.get(c["id"])]
    if missing:
        out.append(_("Answer every required entry of the checklist."))
    if not sub.no_restricted_included:
        out.append(_("Confirm that nothing restricted or confidential is included."))
    if sub.datasets.filter(availability="included").exists() and not sub.permission_to_share:
        out.append(_("Confirm that you may share the data you include with the project."))
    if not out and schema_problems(build(assignment)):
        out.append(_("Some answers are incomplete; please check the form."))
    return out


def canonical_sha256(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


@transaction.atomic
def submit(assignment, language=""):
    """Create the next numbered version. Returns (version, problems); version is None if not ready."""
    found = problems(assignment)
    if found:
        return None, found
    last = assignment.submission_versions.select_for_update().order_by("-version").first()
    number = (last.version + 1) if last else 1
    data = build(assignment, submitted_version=number)
    bad = schema_problems(data)
    if bad:
        raise ValueError(f"manifest fails submission-manifest.schema.json at: {', '.join(bad[:10])}")
    version = SubmissionVersion.objects.create(assignment=assignment, version=number, manifest=data,
                                               manifest_sha256=canonical_sha256(data), language=language)
    version.uploads.set(received_uploads(assignment))
    log_event(assignment.public_id, "submission_submitted", assignment, version=number, channel=data["channel"],
              manifest_sha256=version.manifest_sha256, files=len(data.get("files", [])))
    return version, []


def export(version):
    """The stored manifest with the team's receipt and verification, validated."""
    data = dict(version.manifest)
    if version.received_at:
        data["received_at"] = _iso(version.received_at)
    data["verification_status"] = version.verification_status
    if version.verified_by:
        data["verified_by"] = version.verified_by
    bad = schema_problems(data)
    if bad:
        raise ValueError(f"manifest fails submission-manifest.schema.json at: {', '.join(bad[:10])}")
    return data
