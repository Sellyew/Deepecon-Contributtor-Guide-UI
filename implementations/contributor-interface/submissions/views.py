"""Guidance and Submit (M3; MVP §3 steps 7-8, §5; plan §2.3, §2.5).

Every screen works without JavaScript: the upload form then posts the whole file at once.
static/upload.js sends it in chunks instead, so an interrupted upload resumes where it stopped.
"""
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from contributors.access import contributor_required
from contributors.selection_views import _assignment_with_consent, _language
from papers.importers import rubric_checks
from . import manifest
from . import storage
from .forms import ChecklistForm, DatasetFormSet, SubmissionForm, software_text, tri_initial
from .models import ChecklistAnswer, DatasetDeclaration, Submission, Upload, accepted_channels, max_upload_bytes, runnable_required


def refusal_text(code, params):
    texts = {
        "not_zip_name": _("Please upload one ZIP file (a name ending in .zip)."),
        "not_zip": _("This file is not a ZIP archive, so it was not kept."),
        "empty": _("The file is empty."),
        "too_large": _("The file is larger than %(limit)s. Please send it through another channel agreed with the team."),
        "too_many": _("There are already many uploads for this paper. Please remove one you no longer need."),
        "resume_with_script": _("An unfinished upload of this file exists. Finish it with the upload button (with JavaScript on), or remove it."),
        "in_a_version": _("This file belongs to a submitted version and stays with the team."),
        "checking": _("This file is still being checked. Please wait a moment."),
    }
    text = texts.get(code, _("The upload could not continue. Please try again."))
    if code == "too_large":
        text = text % {"limit": filesizeformat(params.get("limit", 0))}
    return text


def _upload_json(upload):
    out = {"id": upload.public_id, "offset": upload.received_bytes, "size": upload.size_bytes, "status": upload.status,
           "chunk_bytes": settings.UPLOAD_CHUNK_BYTES}
    if upload.status in (Upload.RECEIVED, Upload.REFUSED):
        out["sha256"] = upload.sha256
    if upload.status == Upload.REFUSED:
        out["message"] = refusal_text(upload.refusal, {})
    if upload.status == Upload.RECEIVED:
        out["files"] = len(upload.entries)
    return out


@require_GET
@contributor_required
def guidance(request, paper_id):
    assignment, gate = _assignment_with_consent(request, paper_id)
    if gate:
        return gate
    paper = assignment.paper
    rc = rubric_checks()
    entries = [{"label": rc.localize(c["label"], _language()), "help": rc.localize(c["help"], _language()) if c.get("help") else "",
                "requirement": c.get("requirement")}
               for c in manifest.checklist(paper) if c.get("requirement") != "not_needed"]
    return render(request, "submissions/guidance.html", {
        "assignment": assignment, "paper": paper, "entries": entries, "channels": accepted_channels(paper),
        "runnable": runnable_required(paper), "max_upload": max_upload_bytes(paper),
        "public_package": paper.config.get("replication_package")})


def _initial(sub, paper):
    data = {f: getattr(sub, f) for f in ("channel", "pub_repository", "pub_identifier", "pub_version", "pub_url", "pub_doi",
                                          "other_channel_note", "master_script", "readme", "run_time", "hardware_note",
                                          "no_restricted_included", "permission_to_share")}
    data["software"] = software_text(sub.software)
    for field in ("dependencies_included", "author_run_log_included", "expected_outputs_included"):
        data[field] = tri_initial(getattr(sub, field))
    data["version"] = sub.version
    ref = paper.config.get("replication_package") or {}
    if not (sub.pub_repository or sub.pub_identifier or sub.pub_version) and ref:   # the team knows the public package
        data.update(pub_repository=ref.get("repository", ""), pub_identifier=ref.get("identifier", ""),
                    pub_version=ref.get("version", ""), pub_url=ref.get("url", ""), pub_doi=ref.get("doi", ""))
    return data


@require_http_methods(["GET", "POST"])
@contributor_required
def submit(request, paper_id):
    assignment, gate = _assignment_with_consent(request, paper_id)
    if gate:
        return gate
    paper = assignment.paper
    rc = rubric_checks()
    sub = manifest.submission_for(assignment)
    channels = accepted_channels(paper)
    entries = manifest.checklist(paper)
    answers = {a.checklist_id: a for a in sub.checklist.all()}
    problems = []
    if request.method == "POST":
        form = SubmissionForm(request.POST, channels=channels)
        checklist_form = ChecklistForm(request.POST, entries=entries, language=_language(), localize=rc.localize)
        datasets = DatasetFormSet(request.POST, prefix="datasets")
        if form.is_valid() and checklist_form.is_valid() and datasets.is_valid():
            with transaction.atomic():
                current = Submission.objects.select_for_update().get(pk=sub.pk)
                if form.cleaned_data["version"] != current.version:
                    messages.error(request, _("These answers were saved from another tab after you opened this page. "
                                              "The saved answers are shown below; please make your change again."))
                    return redirect("submissions:submit", paper_id=paper_id)
                for field, value in form.values().items():
                    setattr(current, field, value)
                current.version += 1
                current.save()
                for checklist_id, (status, note) in checklist_form.answers().items():
                    ChecklistAnswer.objects.update_or_create(submission=current, checklist_id=checklist_id,
                                                             defaults={"status": status, "note": note})
                current.datasets.all().delete()
                position = 0
                for row in datasets.cleaned_data:
                    if not row or row.get("DELETE"):
                        continue
                    DatasetDeclaration.objects.create(
                        submission=current, position=position, name=row["name"].strip(), source=row["source"].strip(),
                        terms=row["terms"].strip(), availability=row["availability"], where=row["where"].strip(),
                        access_route=row["access_route"], notes=row["notes"].strip())
                    position += 1
            if request.POST.get("submit"):
                version, problems = manifest.submit(assignment, language=_language())
                if version is not None:
                    messages.success(request, _("Submitted: version %(n)s. Thank you. You can still change your answers and submit again.")
                                     % {"n": version.version})
                    return redirect("submissions:submit", paper_id=paper_id)
            else:
                messages.success(request, _("Saved. Nothing is sent to the team until you submit."))
                return redirect("submissions:submit", paper_id=paper_id)
            sub.refresh_from_db()
            form = SubmissionForm(initial=_initial(sub, paper), channels=channels)
            checklist_form = _checklist_form(sub, entries, rc)
            datasets = _dataset_formset(sub)
    else:
        form = SubmissionForm(initial=_initial(sub, paper), channels=channels)
        checklist_form = _checklist_form(sub, entries, rc, answers)
        datasets = _dataset_formset(sub)
    uploads = list(assignment.uploads.exclude(status=Upload.REFUSED).prefetch_related("versions"))
    return render(request, "submissions/submit.html", {
        "assignment": assignment, "paper": paper, "form": form, "checklist": checklist_form.bound_entries(),
        "checklist_errors": checklist_form.errors, "datasets": datasets, "problems": problems, "uploads": uploads,
        "versions": assignment.submission_versions.order_by("-version"), "runnable": runnable_required(paper),
        "channels": channels, "max_upload": max_upload_bytes(paper), "chunk_bytes": settings.UPLOAD_CHUNK_BYTES,
        "requirement_labels": {"required": _("required"), "confirm_existing": _("confirm if already in your public package"),
                               "optional": _("optional")}})


def _checklist_form(sub, entries, rc, answers=None):
    answers = answers if answers is not None else {a.checklist_id: a for a in sub.checklist.all()}
    initial = {}
    for checklist_id, answer in answers.items():
        initial[f"status_{checklist_id}"], initial[f"note_{checklist_id}"] = answer.status, answer.note
    return ChecklistForm(initial=initial, entries=entries, language=_language(), localize=rc.localize)


def _dataset_formset(sub):
    return DatasetFormSet(prefix="datasets", initial=[
        {"name": d.name, "source": d.source, "terms": d.terms, "availability": d.availability, "where": d.where,
         "access_route": d.access_route, "notes": d.notes} for d in sub.datasets.all()])


# ---- Uploads (JSON for static/upload.js; one plain form for pages without JavaScript) ----

def _upload_gate(request, paper_id):
    assignment, gate = _assignment_with_consent(request, paper_id)
    if gate:
        return None, gate
    if "upload" not in accepted_channels(assignment.paper):
        raise Http404("Uploads are not accepted for this paper.")
    return assignment, None


def _refused(exc, status=400):
    body = {"error": exc.code, "message": refusal_text(exc.code, exc.params)}
    if exc.code == "wrong_offset":
        body["offset"] = exc.params.get("offset")
        status = 409
    return JsonResponse(body, status=status)


@require_POST
@contributor_required
def upload_start(request, paper_id):
    assignment, gate = _upload_gate(request, paper_id)
    if gate:
        return gate
    try:
        size = int(request.POST.get("size", ""))
    except ValueError:
        size = None
    try:
        upload = storage.start(assignment, request.POST.get("name", ""), size)
    except storage.UploadRefused as exc:
        return _refused(exc)
    return JsonResponse(_upload_json(upload), status=201)


def _own_upload(assignment, upload_id):
    return get_object_or_404(Upload, public_id=upload_id, assignment=assignment)


@require_GET
@contributor_required
def upload_status(request, paper_id, upload_id):
    assignment, gate = _upload_gate(request, paper_id)
    if gate:
        return gate
    return JsonResponse(_upload_json(_own_upload(assignment, upload_id)))


@require_POST
@contributor_required
def upload_chunk(request, paper_id, upload_id):
    assignment, gate = _upload_gate(request, paper_id)
    if gate:
        return gate
    upload = _own_upload(assignment, upload_id)
    try:
        offset = int(request.GET.get("offset", ""))
    except ValueError:
        return JsonResponse({"error": "offset", "message": refusal_text("offset", {})}, status=400)
    try:
        upload = storage.append(upload, offset, request)
    except storage.UploadRefused as exc:
        return _refused(exc)
    return JsonResponse(_upload_json(upload))


@require_POST
@contributor_required
def upload_plain(request, paper_id):
    assignment, gate = _upload_gate(request, paper_id)
    if gate:
        return gate
    uploaded = request.FILES.get("package")
    if uploaded is None:
        messages.error(request, _("Please choose a file first."))
        return redirect("submissions:submit", paper_id=paper_id)
    try:
        upload = storage.store_whole(assignment, uploaded)
    except storage.UploadRefused as exc:
        messages.error(request, refusal_text(exc.code, exc.params))
        return redirect("submissions:submit", paper_id=paper_id)
    if upload.status == Upload.RECEIVED:
        messages.success(request, _("Received %(name)s. SHA-256: %(sha)s") % {"name": upload.original_name, "sha": upload.sha256})
    else:
        messages.error(request, refusal_text(upload.refusal, {}))
    return redirect("submissions:submit", paper_id=paper_id)


@require_POST
@contributor_required
def upload_remove(request, paper_id, upload_id):
    assignment, gate = _upload_gate(request, paper_id)
    if gate:
        return gate
    upload = _own_upload(assignment, upload_id)
    try:
        storage.remove(upload, assignment.public_id)
    except storage.UploadRefused as exc:
        messages.error(request, refusal_text(exc.code, exc.params))
    else:
        messages.success(request, _("Removed %(name)s.") % {"name": upload.original_name})
    return redirect("submissions:submit", paper_id=paper_id)
