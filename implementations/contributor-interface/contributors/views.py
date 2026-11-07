"""Contributor views for M1: invitation landing, notice and consent, my paper, package download.

The overview, the review screen, proposals, "Ask the team", guidance, and submission come in
M2 and M3 (plan §4).
"""
from django import forms
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_http_methods

from papers.importers import package_path, rubric_checks
from papers.models import log_event

from .access import assignment_for, contributor_required, current_contributor, sign_in
from .models import Consent, Invitation


class NoticeForm(forms.Form):
    acknowledge_evaluation = forms.BooleanField(
        required=True,
        label=_("I understand that the finished task, built from my package, will be sent through their APIs to each AI company whose models are evaluated, which receives it and may keep it."),
        error_messages={"required": _("Taking part requires this acknowledgement.")},
    )
    team_ai_use = forms.ChoiceField(
        label=_("May the team use AI services with my unpublished materials and my responses?"),
        choices=[("no", _("No")), ("yes", _("Yes"))],
        widget=forms.RadioSelect,
        initial="no",
    )


def _interface_tag():
    """The current interface language as a configuration language tag (zh-hans -> zh-Hans)."""
    code = translation.get_language() or settings.LANGUAGE_CODE
    return "zh-Hans" if code.lower() == "zh-hans" else code


@require_GET
def home(request):
    contributor = current_contributor(request)
    if contributor is None:
        return render(request, "contributors/not_signed_in.html", status=403)
    first = contributor.assignments.select_related("paper").order_by("created_at").first()
    if first is None:
        return render(request, "contributors/not_signed_in.html", status=403)
    return redirect("contributors:my_paper", paper_id=first.paper.paper_id)


@require_GET
def invitation_landing(request, token):
    invitation = Invitation.find_active(token)
    if invitation is None:
        return render(request, "contributors/link_invalid.html", status=404)
    now = timezone.now()
    invitation.first_used_at = invitation.first_used_at or now
    invitation.last_used_at = now
    invitation.save(update_fields=["first_used_at", "last_used_at"])
    assignment = invitation.assignment
    sign_in(request, assignment.contributor)
    log_event(assignment.public_id, "invitation_used", invitation.assignment, invitation_id=invitation.pk)
    response = redirect("contributors:notice", paper_id=assignment.paper.paper_id)   # the token never appears again
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, assignment.contributor.preferred_language,
                        max_age=settings.SESSION_COOKIE_AGE, samesite=settings.LANGUAGE_COOKIE_SAMESITE,
                        secure=settings.LANGUAGE_COOKIE_SECURE, httponly=settings.LANGUAGE_COOKIE_HTTPONLY)
    return response


@require_http_methods(["GET", "POST"])
@contributor_required
def notice(request, paper_id):
    assignment = assignment_for(request, paper_id)
    latest = assignment.latest_consent()
    initial = {"team_ai_use": "yes" if latest and latest.team_ai_use_of_unpublished_material else "no",
               "acknowledge_evaluation": bool(latest)}
    form = NoticeForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        consent = Consent.objects.create(
            assignment=assignment,
            evaluation_through_apis_acknowledged=True,
            team_ai_use_of_unpublished_material=form.cleaned_data["team_ai_use"] == "yes",
            notice_version=settings.NOTICE_VERSION,
        )
        log_event(assignment.public_id, "consent_recorded", assignment, consent_id=consent.pk,
                  team_ai_use=consent.team_ai_use_of_unpublished_material, notice_version=consent.notice_version)
        return redirect("contributors:my_paper", paper_id=paper_id)
    return render(request, "contributors/notice.html", {"assignment": assignment, "paper": assignment.paper,
                                                         "form": form, "latest": latest})


@require_GET
@contributor_required
def my_paper(request, paper_id):
    assignment = assignment_for(request, paper_id)
    if assignment.latest_consent() is None:
        return redirect("contributors:notice", paper_id=paper_id)
    paper = assignment.paper
    rc = rubric_checks()
    lang = _interface_tag()
    rubric = paper.current_rubric()
    counts = {}
    if rubric:
        for category in rubric.items.values_list("category", flat=True):
            counts[category] = counts.get(category, 0) + 1
    categories = [
        {"label": rc.localize(c["label"], lang), "summary": rc.localize(c["summary"], lang) if c.get("summary") else "",
         "count": counts.get(c["id"], 0)}
        for c in paper.config["categories"]
    ]
    package = paper.current_package() if paper.config.get("candidate_package_visible_to_contributors") else None
    return render(request, "contributors/my_paper.html", {
        "assignment": assignment, "paper": paper, "citation": paper.config["citation"],
        "task_version": paper.config["task_version"], "categories": categories, "package": package,
    })


@require_GET
@contributor_required
def package_download(request, paper_id):
    assignment = assignment_for(request, paper_id)
    paper = assignment.paper
    package = paper.current_package()
    if (assignment.latest_consent() is None or package is None
            or not paper.config.get("candidate_package_visible_to_contributors")):
        raise Http404("No package.")
    log_event(assignment.public_id, "package_downloaded", package, sha256=package.sha256)
    return FileResponse(open(package_path(package), "rb"), as_attachment=True,
                        filename=f"{paper.paper_id}-{package.candidate_version}.zip", content_type="application/zip")
