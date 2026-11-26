"""Selection screens (M2; MVP §3 steps 3–6, §4): the review, the matrix, proposals,
"Ask the team", confirmation, and the contributor's own download.

Every screen works without JavaScript. static/review.js adds autosave (the same form,
posted with X-Requested-With: fetch, answered in JSON) and keyboard shortcuts.
"""
from django.contrib import messages
from django.db import transaction
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone, translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from papers.importers import rubric_checks
from papers.models import log_event

from . import review as selection
from .access import assignment_for, contributor_required
from .forms import REJECT_REASONS, TRI_STATE, VARIANTS, VERDICTS, ProposalForm, QuestionForm, ReviewForm
from .models import Proposal, Question

PROPOSAL_FIELDS = ["category", "location", "description", "why_it_matters", "suggested_repair",
                   "ai_used", "ai_tool", "ai_account_kind", "ai_entered_items"]
REVIEW_FIELDS = ["verdict", "reject_reason", "variant_choice", "check_realistic", "check_consequential",
                 "check_repair_correct", "suggested_title", "suggested_description", "other_valid_repairs", "comment",
                 "ai_used", "ai_tool", "ai_account_kind", "ai_entered_items"]


def _language():
    return selection.interface_tag(translation.get_language())


def _assignment_with_consent(request, paper_id):
    """(assignment, None) or (None, redirect to the notice) when consent is missing."""
    assignment = assignment_for(request, paper_id)
    if assignment.latest_consent() is None:
        return None, redirect("contributors:notice", paper_id=paper_id)
    return assignment, None


def _is_fetch(request):
    return request.headers.get("X-Requested-With") == "fetch"


def _initial(review):
    if review is None:
        return {"version": 0}
    data = {f: getattr(review, f) for f in REVIEW_FIELDS}
    data["version"] = review.version
    return data


def _categories(paper):
    rc = rubric_checks()
    return [(c["id"], rc.localize(c["label"], _language())) for c in paper.config["categories"]]


@require_GET
@contributor_required
def review_start(request, paper_id):
    assignment, gate = _assignment_with_consent(request, paper_id)
    if gate:
        return gate
    items = selection.paper_items(assignment.paper)
    if not items:
        raise Http404("No items yet.")
    answered = set(selection.reviews_by_item(assignment))
    first = next((it for it in items if it.item_id not in answered), items[0])
    return redirect("contributors:review_item", paper_id=paper_id, item_id=first.item_id)


@require_http_methods(["GET", "POST"])
@contributor_required
def review_item(request, paper_id, item_id):
    assignment, gate = _assignment_with_consent(request, paper_id)
    if gate:
        return gate
    paper = assignment.paper
    items = selection.paper_items(paper)
    item = next((it for it in items if it.item_id == item_id), None)
    if item is None:
        raise Http404("No such item.")
    views = selection.item_views(paper, _language())
    view = views[item_id]
    partner = views.get(view.get("paired_with"))
    reviews = selection.reviews_by_item(assignment)
    review = reviews.get(item_id)
    if request.method == "GET" and _is_fetch(request):
        # review.js asks this when a page may have been built before a save arrived.
        return JsonResponse({"version": review.version if review else 0})
    prev_id, next_id = selection.neighbours(items, item_id)
    conflict = False
    pair_cards = []
    if partner:
        # The pair is shown in rubric order on both items' pages, so "the first" and "the
        # second" mean the same thing wherever the contributor answers (contributors/review.py).
        position = {it.item_id: it.position for it in items}
        ordered = sorted([view, partner], key=lambda v: position.get(v["id"], 0))
        pair_cards = [{"card": c, "label": label, "current": c["id"] == item_id}
                      for c, label in zip(ordered, (_("First version"), _("Second version")))]

    def current_mate():
        return assignment.reviews.filter(item__rubric=item.rubric, item__item_id=partner["id"]).first() if partner else None

    def initial(review):
        # The pair's choice is one answer: show the most recent one given on either item's page.
        data = _initial(review)
        mate = current_mate()
        if mate and mate.variant_choice and (not data.get("variant_choice") or (review and mate.updated_at > review.updated_at)):
            data["variant_choice"] = mate.variant_choice
        return data

    if request.method == "POST":
        if assignment.is_frozen:
            if _is_fetch(request):
                return JsonResponse({"ok": False, "frozen": True}, status=423)
            messages.error(request, _("The team has frozen your review; it can no longer be changed."))
            return redirect("contributors:review_item", paper_id=paper_id, item_id=item_id)
        data = request.POST.copy()
        if data.get("set_verdict"):
            data["verdict"] = data["set_verdict"]
        form = ReviewForm(data, paired=partner is not None)
        if form.is_valid():
            try:
                try:
                    partner_version = int(request.POST.get("partner_version", "")) if partner else None
                except ValueError:
                    partner_version = None
                saved = selection.save_review(assignment, item, form.review_data(), form.cleaned_data["version"],
                                              partner_version=partner_version)
            except selection.Conflict as clash:
                if _is_fetch(request):
                    return JsonResponse({"ok": False, "conflict": True,
                                         "version": clash.review.version if clash.review else 0}, status=409)
                conflict, review = True, clash.review
                form = ReviewForm(initial=initial(review), paired=partner is not None)
            except selection.Frozen:
                return JsonResponse({"ok": False, "frozen": True}, status=423) if _is_fetch(request) else \
                    redirect("contributors:review_item", paper_id=paper_id, item_id=item_id)
            else:
                if _is_fetch(request):
                    return JsonResponse({"ok": True, "version": saved.version, "partner_version": saved.partner_version,
                                         "saved_at": timezone.localtime(saved.updated_at).strftime("%H:%M")})
                # A one-tap answer moves on, except Reject, whose optional reasons appear next (MVP §4.2).
                # After the last item it moves on to "Review and confirm" (step 6).
                if data.get("set_verdict") and saved.verdict != "reject":
                    if next_id:
                        return redirect("contributors:review_item", paper_id=paper_id, item_id=next_id)
                    return redirect("contributors:confirm", paper_id=paper_id)
                return redirect("contributors:review_item", paper_id=paper_id, item_id=item_id)
        elif _is_fetch(request):
            return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)
    else:
        form = ReviewForm(initial=initial(review), paired=partner is not None)

    earlier = selection.earlier_review(assignment, item_id) if review is None else None
    mate = current_mate()
    return render(request, "contributors/review_item.html", {
        "assignment": assignment, "paper": paper, "item": view, "partner": partner, "pair_cards": pair_cards,
        "form": form, "review": review, "conflict": conflict, "prev_id": prev_id, "next_id": next_id,
        "verdicts": VERDICTS, "map": selection.map_for(assignment, _language(), result=request.GET.get("result")),
        "progress": selection.progress(assignment), "questions": assignment.questions.filter(item=item),
        "question_form": QuestionForm(), "frozen": assignment.is_frozen,
        "earlier": earlier, "earlier_verdict": dict(VERDICTS).get(earlier.verdict) if earlier else None,
        # After an invalid post the page shows the posted (possibly stale) choice again, so it keeps
        # the partner's version it was loaded with; otherwise the page shows the stored answers.
        "partner_version": (request.POST.get("partner_version", "0") if request.method == "POST" and not conflict
                            else (mate.version if mate else 0)),
    })


@require_GET
@contributor_required
def review_matrix(request, paper_id):
    """Results × items, the same information as the map, as a grid (MVP §4.1)."""
    assignment, gate = _assignment_with_consent(request, paper_id)
    if gate:
        return gate
    the_map = selection.map_for(assignment, _language())
    if the_map is None:
        raise Http404("No item map yet.")
    items = selection.paper_items(assignment.paper)
    reviews = selection.reviews_by_item(assignment)
    rows = []
    for node in the_map["nodes"]:
        if node["affected_by"]:
            affecting = {m["item_id"] for m in node["affected_by"]}
            rows.append({"label": node["label_text"], "cells": [it.item_id in affecting for it in items]})
    palette = selection.colours(assignment.paper)
    columns = [{"id": it.item_id, "colour": palette.get(it.category, 0), "reviewed": it.item_id in reviews} for it in items]
    return render(request, "contributors/review_matrix.html", {
        "assignment": assignment, "paper": assignment.paper, "rows": rows, "columns": columns,
        "progress": selection.progress(assignment)})


@require_http_methods(["GET", "POST"])
@contributor_required
def propose(request, paper_id, proposal_id=None):
    """Propose an addition (MVP §3 step 5); edit or delete one's own proposals until frozen."""
    assignment, gate = _assignment_with_consent(request, paper_id)
    if gate:
        return gate
    proposal = get_object_or_404(Proposal, public_id=proposal_id, assignment=assignment) if proposal_id else None
    categories = _categories(assignment.paper)
    frozen_message = _("The team has frozen your review; it can no longer be changed.")
    if request.method == "POST":
        form = ProposalForm(request.POST, categories=categories)
        try:
            with transaction.atomic():
                selection.check_not_frozen(assignment)
                current = Proposal.objects.select_for_update().get(pk=proposal.pk) if proposal else None
                values = ({f: (v.strip() if isinstance(v, str) else v)
                           for f, v in ((f, form.cleaned_data.get(f)) for f in PROPOSAL_FIELDS)}
                          if form.is_valid() else None)
                if (current is not None and values is not None and not request.POST.get("delete")
                        and all(getattr(current, f) == v for f, v in values.items())):
                    # Nothing to change, e.g. "Save" pressed twice: the first press saved it.
                    messages.success(request, _("Your proposal was saved."))
                    return redirect("contributors:propose", paper_id=paper_id)
                if current is not None and request.POST.get("version") != str(current.version):
                    # Saved from another tab since this page was opened: show the saved text instead.
                    messages.error(request, _("This proposal was changed in another tab after you opened this page. "
                                              "The saved text is shown below; please make your change again."))
                    return redirect("contributors:proposal_edit", paper_id=paper_id, proposal_id=current.public_id)
                if current is not None and request.POST.get("delete"):
                    current.delete()
                    log_event(assignment.public_id, "proposal_deleted", assignment, proposal_id=current.public_id)
                    messages.success(request, _("The proposal was deleted."))
                    return redirect("contributors:propose", paper_id=paper_id)
                if values is not None:
                    if current is None:
                        duplicate = assignment.proposals.filter(**values).first()
                        if duplicate:          # every field the same: "Save" pressed twice
                            messages.success(request, _("Your proposal was saved."))
                            return redirect("contributors:propose", paper_id=paper_id)
                    target = current or Proposal(assignment=assignment)
                    for field, value in values.items():
                        setattr(target, field, value)
                    if current is not None:
                        target.version = current.version + 1
                    target.save()
                    log_event(assignment.public_id, "proposal_added" if current is None else "proposal_edited",
                              assignment, proposal_id=target.public_id)
                    messages.success(request, _("Your proposal was saved."))
                    return redirect("contributors:propose", paper_id=paper_id)
        except selection.Frozen:
            messages.error(request, frozen_message)
            return redirect("contributors:propose", paper_id=paper_id)
    else:
        initial = {f: getattr(proposal, f) for f in PROPOSAL_FIELDS} if proposal else {}
        form = ProposalForm(initial=initial, categories=categories)
    return render(request, "contributors/propose.html", {
        "assignment": assignment, "paper": assignment.paper, "form": form, "editing": proposal,
        "proposals": assignment.proposals.all(), "labels": dict(categories), "frozen": assignment.is_frozen})


@require_POST
@contributor_required
def ask(request, paper_id):
    """'Ask the team' (MVP §4.2): stored on the site and answered in the admin; no AI, no e-mail."""
    assignment, gate = _assignment_with_consent(request, paper_id)
    if gate:
        return gate
    item_id = request.POST.get("item_id") or None
    item = next((it for it in selection.paper_items(assignment.paper) if it.item_id == item_id), None) if item_id else None
    if item_id and item is None:
        raise Http404("No such item.")
    form = QuestionForm(request.POST)
    if form.is_valid():
        question = Question.objects.create(assignment=assignment, item=item, text=form.cleaned_data["text"].strip())
        log_event(assignment.public_id, "question_asked", assignment, question_id=question.public_id)
        messages.success(request, _("Your question was sent to the team. Their answer will appear here."))
    else:
        messages.error(request, _("Please write your question first."))
    if item:
        return redirect("contributors:review_item", paper_id=paper_id, item_id=item.item_id)
    return redirect("contributors:my_paper", paper_id=paper_id)


@require_http_methods(["GET", "POST"])
@contributor_required
def confirm(request, paper_id):
    """Review and confirm (MVP §3 step 6): all answers in the contributor's own words; each
    confirmation is a numbered version, revisable until the team freezes the review."""
    assignment, gate = _assignment_with_consent(request, paper_id)
    if gate:
        return gate
    if request.method == "POST":
        try:
            version = selection.confirm(assignment, language=_language())
        except selection.Frozen:
            messages.error(request, _("The team has frozen your review; it can no longer be changed."))
        else:
            log_event(assignment.public_id, "review_confirmed", assignment, version=version.version,
                      content_sha256=version.content_sha256)
            messages.success(request, _("Version %(n)s confirmed. You can still revise it until the team freezes your review.")
                             % {"n": version.version})
        return redirect("contributors:confirm", paper_id=paper_id)
    paper = assignment.paper
    views = selection.item_views(paper, _language())
    reviews = selection.reviews_by_item(assignment)
    labels, reasons, variants = dict(VERDICTS), dict(REJECT_REASONS), dict(VARIANTS)
    rows = []
    for it in selection.paper_items(paper):
        r = reviews.get(it.item_id)
        rows.append({"item": views[it.item_id], "review": r,
                     "verdict_label": labels.get(r.verdict) if r else None,
                     "reason_label": reasons.get(r.reject_reason) if r and r.verdict == "reject" else None,
                     "variant_label": variants.get(r.variant_choice) if r else None})
    return render(request, "contributors/confirm.html", {
        "assignment": assignment, "paper": paper, "rows": rows, "proposals": assignment.proposals.all(),
        "confirmations": assignment.confirmations.order_by("-version"), "progress": selection.progress(assignment),
        "frozen": assignment.is_frozen, "category_labels": dict(_categories(paper))})


@require_GET
@contributor_required
def my_review_download(request, paper_id):
    """The contributor's latest confirmed version as Markdown, for their records (MVP §4.2)."""
    assignment, gate = _assignment_with_consent(request, paper_id)
    if gate:
        return gate
    latest = assignment.confirmations.order_by("-version").first()
    if latest is None:
        raise Http404("Nothing confirmed yet.")
    labels, reasons, variants, ticks = dict(VERDICTS), dict(REJECT_REASONS), dict(VARIANTS), dict(TRI_STATE)
    categories = dict(_categories(assignment.paper))
    categories["unsure"] = _("Not sure")
    fields = ReviewForm.base_fields
    check_labels = {"realistic": fields["check_realistic"].label, "consequential": fields["check_consequential"].label,
                    "repair_correct": fields["check_repair_correct"].label}
    lines = [f"# {assignment.paper.title}", "",
             "> " + _("Confidential: these items are the benchmark's answers. Please do not publish or share them."), "",
             _("Version %(n)s, confirmed %(date)s UTC") % {"n": latest.version,
                                                          "date": latest.confirmed_at.strftime("%Y-%m-%d %H:%M")},
             f"SHA-256 {latest.content_sha256}", ""]
    for r in latest.content["reviews"]:
        lines.append(f"## {r['item_id']} ({categories.get(r['category'], r['category'])}): "
                     f"{labels.get(r['verdict'], r['verdict'])}")
        if r.get("reject_reason"):
            lines.append(f"- {fields['reject_reason'].label}: {reasons.get(r['reject_reason'], r['reject_reason'])}")
        if r.get("variant_choice"):
            lines.append(f"- {fields['variant_choice'].label} {variants.get(r['variant_choice'], r['variant_choice'])}")
        for key, value in r.get("checks", {}).items():
            lines.append(f"- {check_labels.get(key, key)}: {ticks.get(value, value)}")
        for key in ("suggested_title", "suggested_description", "other_valid_repairs", "comment"):
            if r.get(key):
                lines.append(f"- {fields[key].label}: {r[key]}")
        if r.get("ai_help", {}).get("used"):
            lines.append(f"- {fields['ai_used'].label}: {r['ai_help'].get('tool', '')}")
        lines.append("")
    if latest.content["proposals"]:
        lines.append("## " + _("Proposed additions"))
        for p in latest.content["proposals"]:
            lines.append(f"- [{categories.get(p['category'], p['category'])}] {p['description']}")
    response = HttpResponse("\n".join(lines) + "\n", content_type="text/markdown; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{assignment.paper.paper_id}-my-review-v{latest.version}.md"'
    log_event(assignment.public_id, "own_review_downloaded", assignment, version=latest.version)
    return response
