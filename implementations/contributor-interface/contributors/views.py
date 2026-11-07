"""Contributor views for M1: invitation landing, choosing a paper, notice and consent, my paper,
package download (D-044: the personal link opens one paper at a time, chosen by the contributor).

The overview, the review screen, proposals, "Ask the team", guidance, and submission come in
M2 and M3 (plan §4).
"""
from django import forms
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_http_methods

from papers.importers import package_path, rubric_checks
from papers.models import log_event

from .access import assignment_for, contributor_required, current_invitation, sign_in
from .models import Consent, Invitation


class NoticeForm(forms.Form):
    acknowledge_evaluation = forms.BooleanField(
        required=True,
        label=_("I understand that the finished task, built from my package, will be sent through their APIs to each AI company whose models are evaluated, which receives it and may keep it."),
        error_messages={"required": _("Taking part requires this acknowledgement.")},
    )
    EXPERT_LABEL = _("I understand that the finished task, built from this paper's package and the reviews, will be sent through their APIs to each AI company whose models are evaluated, which receives it and may keep it.")
    team_ai_use = forms.ChoiceField(
        label=_("May the team use AI services with my unpublished materials and my responses?"),
        choices=[("no", _("No")), ("yes", _("Yes"))],
        widget=forms.RadioSelect,
        initial="no",
    )

    def __init__(self, *args, author=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not author:
            self.fields["acknowledge_evaluation"].label = self.EXPERT_LABEL


def _is_author(assignment):
    return assignment.relationship_to_paper == "author"


def _notice_version(assignment):
    # The notice has two wordings: for the paper's authors and for invited experts.
    return f"{settings.NOTICE_VERSION}/{'author' if _is_author(assignment) else 'expert'}"


def _package_visible(paper):
    # The schema's default is true: contributors may see the agent-facing package (D-028).
    return paper.config.get("candidate_package_visible_to_contributors", True)


def _interface_tag():
    """The current interface language as a configuration language tag (zh-hans -> zh-Hans)."""
    code = translation.get_language() or settings.LANGUAGE_CODE
    return "zh-Hans" if code.lower() == "zh-hans" else code


def _start_page(contributor):
    current = contributor.current()
    return redirect("contributors:my_paper", paper_id=current.paper.paper_id) if current else redirect("contributors:papers")


@require_GET
def home(request):
    invitation = current_invitation(request)
    if invitation is None:
        return render(request, "contributors/not_signed_in.html", status=403)
    return _start_page(invitation.contributor)


@require_GET
def invitation_landing(request, token):
    invitation = Invitation.find_active(token)
    if invitation is None:
        return render(request, "contributors/link_invalid.html", status=404)
    now = timezone.now()
    invitation.first_used_at = invitation.first_used_at or now
    invitation.last_used_at = now
    invitation.save(update_fields=["first_used_at", "last_used_at"])
    contributor = invitation.contributor
    sign_in(request, invitation)
    log_event(contributor.public_id, "invitation_used", invitation, invitation_id=invitation.pk)
    current = contributor.current()
    # The token never appears again: the link leads to the current paper's notice, or to the
    # page for choosing a paper.
    response = (redirect("contributors:notice", paper_id=current.paper.paper_id) if current
                else redirect("contributors:papers"))
    if settings.LANGUAGE_COOKIE_NAME not in request.COOKIES:
        # The team's preset applies at the first visit only; afterwards the contributor's own choice stays.
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, contributor.preferred_language,
                            max_age=settings.LANGUAGE_COOKIE_AGE, samesite=settings.LANGUAGE_COOKIE_SAMESITE,
                            secure=settings.LANGUAGE_COOKIE_SECURE, httponly=settings.LANGUAGE_COOKIE_HTTPONLY)
    return response


def _citation_view(paper):
    citation = paper.config.get("citation", {})
    return {"paper_id": paper.paper_id, "title": citation.get("title", paper.title),
            "authors": citation.get("authors", []), "journal": citation.get("journal", ""), "year": citation.get("year", "")}


@require_GET
@contributor_required
def papers(request):
    """The papers offered to the contributor; the link opens the one they choose."""
    contributor = request.contributor
    current = contributor.current()
    worked_on = set(contributor.assignments.filter(consents__isnull=False).values_list("paper_id", flat=True))
    others = []
    for paper in contributor.choosable_papers().exclude(pk=current.paper_id if current else None).order_by("title"):
        others.append({**_citation_view(paper), "worked_on": paper.pk in worked_on})
    return render(request, "contributors/papers.html", {
        "current": _citation_view(current.paper) if current else None, "others": others,
    })


@require_http_methods(["GET", "POST"])
@contributor_required
def choose(request, paper_id):
    """Asks whether to switch the link to another paper, and switches on confirmation."""
    contributor = request.contributor
    paper = get_object_or_404(contributor.choosable_papers(), paper_id=paper_id)
    current = contributor.current()
    if current is not None and current.paper_id == paper.pk:
        return redirect("contributors:my_paper", paper_id=paper_id)
    if request.method == "POST":
        assignment, previous, created = contributor.choose(paper)
        log_event(contributor.public_id, "paper_chosen", assignment, by="contributor", new_assignment=created,
                  previous_assignment=previous.public_id if previous else None)
        return redirect("contributors:my_paper", paper_id=paper_id)
    return render(request, "contributors/choose.html", {
        "paper": _citation_view(paper), "current": _citation_view(current.paper) if current else None,
    })


@require_http_methods(["GET", "POST"])
@contributor_required
def notice(request, paper_id):
    assignment = assignment_for(request, paper_id)
    latest = assignment.latest_consent()
    initial = {"team_ai_use": "yes" if latest and latest.team_ai_use_of_unpublished_material else "no",
               "acknowledge_evaluation": bool(latest)}
    author = _is_author(assignment)
    form = NoticeForm(request.POST or None, initial=initial, author=author)
    if request.method == "POST" and form.is_valid():
        consent = Consent.objects.create(
            assignment=assignment,
            evaluation_through_apis_acknowledged=True,
            team_ai_use_of_unpublished_material=form.cleaned_data["team_ai_use"] == "yes",
            notice_version=_notice_version(assignment),
        )
        log_event(assignment.public_id, "consent_recorded", assignment, consent_id=consent.pk,
                  team_ai_use=consent.team_ai_use_of_unpublished_material, notice_version=consent.notice_version)
        return redirect("contributors:my_paper", paper_id=paper_id)
    return render(request, "contributors/notice.html", {"assignment": assignment, "paper": assignment.paper,
                                                         "form": form, "latest": latest, "author": author})


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
    package = paper.current_package() if _package_visible(paper) else None
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
            or not _package_visible(paper)):
        raise Http404("No package.")
    log_event(assignment.public_id, "package_downloaded", package, sha256=package.sha256)
    return FileResponse(open(package_path(package), "rb"), as_attachment=True,
                        filename=f"{paper.paper_id}-{package.candidate_version}.zip", content_type="application/zip")
