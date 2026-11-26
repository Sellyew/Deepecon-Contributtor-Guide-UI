"""Team administration for contributors, assignments, invitations, and consent (plan §2.2; D-044).

A contributor has one personal link at a time; it opens their current paper. Creating a link
from an assignment makes that assignment the current paper only if the contributor has none:
the link stays on the paper a contributor chose until they change it (D-044). Creating one
from a contributor leaves the current paper as it is (a contributor with none chooses one).
An assignment's contributor and paper cannot be changed once it exists, because consent and
reviews belong to it; a mistake is corrected by creating a new assignment.

The team moves a contributor's link only when the contributor asks (D-045). The contributor's
page has a "danger zone" for this, with GitHub's confirmation steps for deleting a
repository: what will happen, "I have read and understand these effects", then typing the
contributor's ID. "Rewind" sends the link back to the start: the list of papers.
"""
import json

from django import forms
from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone

from papers.models import log_event

from . import review as selection
from .models import (Assignment, Confirmation, Consent, Contributor, Invitation, ItemReview, Proposal, Question,
                     issue_invitation, set_first_paper)


class InviteActionMixin:
    def has_invite_permission(self, request):
        return request.user.has_perm("contributors.add_invitation")

    def _links_page(self, request, created):
        # The links are rendered in this response only: they are never stored in messages,
        # sessions, or logs, and the response is not cached (Cache-Control: no-store).
        return TemplateResponse(request, "admin/contributors/invitations_created.html",
                                {**self.admin_site.each_context(request), "title": "Invitation links", "created": created})

    def _issue(self, request, contributor, note=""):
        invitation, raw = issue_invitation(contributor, request.user.get_username())
        current = contributor.current()
        if current is not None:
            opens = current.paper.paper_id
        elif contributor.choosable_papers().exists():
            opens = "(the contributor chooses a paper)"
        else:
            opens = "(nothing to choose yet: assign or open a paper first)"
        return {"contributor": contributor, "opens": opens, "note": note,
                "link": invitation.link(raw), "expires_at": invitation.expires_at}


REWIND = "rewind"


class MoveLinkForm(forms.Form):
    """Step 3 of moving a contributor's link: target, the contributor's request, typed confirmation."""

    CHANNELS = [("email", "E-mail"), ("wechat", "WeChat"), ("in_person", "In person or by phone"), ("other", "Other")]
    target = forms.ChoiceField(label="Where their link should go")
    requested_on = forms.DateField(label="Date of the contributor's request", widget=forms.DateInput(attrs={"type": "date"}))
    request_channel = forms.ChoiceField(label="How they asked", choices=CHANNELS)
    confirmation = forms.CharField(label="Confirmation", max_length=64, strip=False)   # exact, as on GitHub

    def __init__(self, *args, contributor, **kwargs):
        super().__init__(*args, **kwargs)
        self.contributor = contributor
        current = contributor.current()
        choices = [(paper.paper_id, f"{paper.paper_id}: {paper.title}")
                   for paper in contributor.choosable_papers().order_by("paper_id")
                   if current is None or paper.pk != current.paper_id]
        if current is not None:
            choices.append((REWIND, "Rewind: no paper; their link opens the list of papers and they choose again"))
        self.fields["target"].choices = choices

    def clean_requested_on(self):
        day = self.cleaned_data["requested_on"]
        if day > timezone.localdate():
            raise forms.ValidationError("The request cannot be in the future.")
        return day

    def clean_confirmation(self):
        typed = self.cleaned_data["confirmation"]
        if typed != self.contributor.public_id:
            raise forms.ValidationError(f"Type {self.contributor.public_id} exactly to confirm.")
        return typed


class WithdrawForm(forms.Form):
    """Step 3 of a withdrawal at the contributor's request: their request, typed confirmation."""

    requested_on = forms.DateField(label="Date of the contributor's request", widget=forms.DateInput(attrs={"type": "date"}))
    request_channel = forms.ChoiceField(label="How they asked", choices=MoveLinkForm.CHANNELS)
    confirmation = forms.CharField(label="Confirmation", max_length=64, strip=False)

    def __init__(self, *args, assignment, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignment = assignment

    def clean_requested_on(self):
        day = self.cleaned_data["requested_on"]
        if day > timezone.localdate():
            raise forms.ValidationError("The request cannot be in the future.")
        return day

    def clean_confirmation(self):
        typed = self.cleaned_data["confirmation"]
        if typed != self.assignment.public_id:
            raise forms.ValidationError(f"Type {self.assignment.public_id} exactly to confirm.")
        return typed


@admin.register(Contributor)
class ContributorAdmin(InviteActionMixin, admin.ModelAdmin):
    list_display = ("display_name", "public_id", "current_assignment", "preferred_language", "created_at")
    readonly_fields = ("public_id", "current_assignment", "created_at")
    actions = ["create_invitation"]
    change_form_template = "admin/contributors/contributor_change_form.html"

    def get_urls(self):
        move = path("<int:pk>/move-link/", self.admin_site.admin_view(self.move_link_view),
                    name="contributors_contributor_move_link")
        return [move] + super().get_urls()

    def move_link_view(self, request, pk):
        """Moves a contributor's link on their request, in GitHub's three confirmation steps."""
        contributor = get_object_or_404(Contributor, pk=pk)
        if not self.has_change_permission(request, contributor):
            raise PermissionDenied
        step = request.POST.get("step") or request.GET.get("step") or "1"
        form = None
        if step == "3":
            form = MoveLinkForm(request.POST or None, contributor=contributor)
            if not form.fields["target"].choices:
                messages.error(request, "This contributor has no other paper their link could open.")
                return redirect("admin:contributors_contributor_change", contributor.pk)
            if request.method == "POST" and form.is_valid():
                self._move_link(request, contributor, form.cleaned_data)
                return redirect("admin:contributors_contributor_change", contributor.pk)
        current = contributor.current()
        return TemplateResponse(request, "admin/contributors/move_link.html", {
            **self.admin_site.each_context(request), "opts": self.model._meta, "original": contributor,
            "title": f"Move or rewind the link of {contributor.public_id}", "contributor": contributor,
            "current": current, "step": step if step in ("1", "2", "3") else "1", "form": form,
            "change_url": reverse("admin:contributors_contributor_change", args=[contributor.pk]),
        })

    def _move_link(self, request, contributor, data):
        actor = request.user.get_username()
        previous = contributor.current()
        details = {"contributor_id": contributor.public_id, "requested_on": data["requested_on"].isoformat(),
                   "request_channel": data["request_channel"],
                   "previous_assignment": previous.public_id if previous else None}
        if data["target"] == REWIND:
            contributor.current_assignment = None
            contributor.save(update_fields=["current_assignment"])
            log_event(actor, "link_rewound_on_request", previous or contributor, **details)
            messages.success(request, f"Done: the link of {contributor.public_id} now opens the list of papers.")
            return
        paper = contributor.choosable_papers().get(paper_id=data["target"])
        assignment, _, created = contributor.choose(paper)
        log_event(actor, "link_moved_on_request", assignment, new_assignment=created, **details)
        messages.success(request, f"Done: the link of {contributor.public_id} now opens {paper.paper_id}.")

    @admin.action(description="Create the personal link (shown once; earlier links are revoked)", permissions=["invite"])
    def create_invitation(self, request, queryset):
        return self._links_page(request, [self._issue(request, c) for c in queryset])


@admin.register(Assignment)
class AssignmentAdmin(InviteActionMixin, admin.ModelAdmin):
    list_display = ("public_id", "contributor", "paper", "relationship_to_paper", "added_by", "progress", "frozen_at", "created_at")
    list_filter = ("paper", "relationship_to_paper", "added_by")
    readonly_fields = ("public_id", "added_by", "created_at", "frozen_at", "frozen_by")
    actions = ["create_invitation", "freeze", "unfreeze", "export_review"]
    change_form_template = "admin/contributors/assignment_change_form.html"

    def get_urls(self):
        withdraw = path("<int:pk>/withdraw/", self.admin_site.admin_view(self.withdraw_view),
                        name="contributors_assignment_withdraw")
        return [withdraw] + super().get_urls()

    def withdraw_view(self, request, pk):
        """Withdrawal at the contributor's request (the notice; plan §3): deletes their work on this
        paper and the assignment, in GitHub's three confirmation steps, and logs counts, not content."""
        assignment = get_object_or_404(Assignment.objects.select_related("contributor", "paper"), pk=pk)
        if not self.has_delete_permission(request, assignment):
            raise PermissionDenied
        step = request.POST.get("step") or request.GET.get("step") or "1"
        form = None
        if step == "3":
            form = WithdrawForm(request.POST or None, assignment=assignment)
            if request.method == "POST" and form.is_valid():
                self._withdraw(request, assignment, form.cleaned_data)
                return redirect("admin:contributors_contributor_change", assignment.contributor.pk)
        counts = {"answers": assignment.reviews.count(), "proposals": assignment.proposals.count(),
                  "questions": assignment.questions.count(), "confirmed versions": assignment.confirmations.count()}
        return TemplateResponse(request, "admin/contributors/withdraw.html", {
            **self.admin_site.each_context(request), "opts": self.model._meta, "original": assignment,
            "title": f"Withdraw {assignment.public_id}", "assignment": assignment, "counts": counts,
            "step": step if step in ("1", "2", "3") else "1", "form": form,
            "change_url": reverse("admin:contributors_assignment_change", args=[assignment.pk]),
        })

    @transaction.atomic
    def _withdraw(self, request, assignment, data):
        contributor = assignment.contributor
        details = {"assignment_id": assignment.public_id, "paper_id": assignment.paper.paper_id,
                   "requested_on": data["requested_on"].isoformat(), "request_channel": data["request_channel"],
                   "was_frozen": assignment.is_frozen}
        for name in ("reviews", "proposals", "questions", "confirmations", "consents"):
            related = getattr(assignment, name)
            details[f"{name}_deleted"] = related.count()
            related.all().delete()
        assignment.delete()             # the contributor's link falls back to the list of papers if it was current
        log_event(request.user.get_username(), "withdrawn_on_request", contributor, **details)
        messages.success(request, f"Done: {details['assignment_id']} and the contributor's work on "
                                  f"{details['paper_id']} were deleted, as they asked.")

    @admin.display(description="Reviewed")
    def progress(self, obj):
        p = selection.progress(obj)
        return f"{p['reviewed']} of {p['total']}"

    @admin.action(description="Freeze the selected reviews (contributors can no longer change them)", permissions=["change"])
    def freeze(self, request, queryset):
        for assignment in queryset.select_related("paper", "contributor"):
            if assignment.is_frozen:
                continue
            blocking, warnings = selection.freeze_problems(assignment)
            if blocking:
                self.message_user(request, f"{assignment.public_id} not frozen: {'; '.join(blocking)}.", messages.ERROR)
                continue
            assignment.frozen_at, assignment.frozen_by = timezone.now(), request.user.get_username()
            assignment.save(update_fields=["frozen_at", "frozen_by"])
            # What was frozen (plan §2.7): the hash of the answers, and the confirmed version they match, if any.
            log_event(request.user.get_username(), "review_frozen", assignment, warnings=warnings,
                      **selection.freeze_record(assignment))
            note = f" Note: {'; '.join(warnings)}." if warnings else ""
            self.message_user(request, f"{assignment.public_id} frozen.{note}", messages.WARNING if warnings else messages.SUCCESS)

    @admin.action(description="Unfreeze the selected reviews", permissions=["change"])
    def unfreeze(self, request, queryset):
        for assignment in queryset.filter(frozen_at__isnull=False):
            record = selection.freeze_record(assignment)
            assignment.frozen_at, assignment.frozen_by = None, ""
            assignment.save(update_fields=["frozen_at", "frozen_by"])
            log_event(request.user.get_username(), "review_unfrozen", assignment, **record)
            self.message_user(request, f"{assignment.public_id} unfrozen; the contributor can edit again.", messages.SUCCESS)

    def has_export_permission(self, request):
        """The export holds the contributor's answers, proposals, messages, and consent, so it needs
        the permission to view each of them, not only the assignment."""
        return all(request.user.has_perm(f"contributors.view_{model}")
                   for model in ("assignment", "itemreview", "proposal", "question", "consent", "confirmation"))

    @admin.action(description="Export the selected review as JSON (contributor-review schema)", permissions=["export"])
    def export_review(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Export one review at a time.", messages.ERROR)
            return None
        assignment = queryset.select_related("paper", "contributor").get()
        data = selection.export(assignment)
        log_event(request.user.get_username(), "review_exported", assignment,
                  reviews=len(data["reviews"]), proposals=len(data["proposals"]))
        response = HttpResponse(json.dumps(data, ensure_ascii=False, indent=2), content_type="application/json; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="{assignment.paper.paper_id}-{assignment.public_id}-review.json"'
        return response

    def get_readonly_fields(self, request, obj=None):
        # Consent (and, from M2, reviews) belong to the assignment: they never move to another
        # person or paper. Correct a mistake by creating a new assignment.
        return self.readonly_fields + (("contributor", "paper") if obj is not None else ())

    @admin.action(description="Create a personal link, opening this paper unless the contributor has chosen one "
                              "(shown once; earlier links are revoked)", permissions=["invite"])
    def create_invitation(self, request, queryset):
        assignments = list(queryset.select_related("contributor", "paper"))
        contributors = [a.contributor_id for a in assignments]
        if len(contributors) != len(set(contributors)):
            self.message_user(request, "A link opens one paper: select at most one assignment per contributor.", messages.ERROR)
            return None
        created = []
        for assignment in assignments:
            contributor = assignment.contributor
            created.append(self._issue(request, contributor, note=set_first_paper(contributor, assignment, request.user.get_username())))
        return self._links_page(request, created)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("contributor", "created_at", "expires_at", "revoked_at", "first_used_at", "last_used_at")
    readonly_fields = ("contributor", "token_hash", "created_at", "expires_at", "revoked_at", "first_used_at", "last_used_at")
    actions = ["revoke"]

    def has_add_permission(self, request):
        return False        # use the actions on contributors or assignments, so the token is generated and shown once

    @admin.action(description="Revoke the selected links (this also ends sessions opened with them)", permissions=["change"])
    def revoke(self, request, queryset):
        now = timezone.now()
        for invitation in queryset.filter(revoked_at__isnull=True):
            invitation.revoked_at = now
            invitation.save(update_fields=["revoked_at"])
            log_event(request.user.get_username(), "invitation_revoked", invitation, invitation_id=invitation.pk)


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    """Consent is never deleted on its own. It goes with its assignment: when a work-free assignment
    is deleted, or in a withdrawal. (Django checks the delete permission of every record a deletion
    cascades to, so this keeps the permission and closes the direct ways instead.)"""

    list_display = ("assignment", "evaluation_through_apis_acknowledged", "team_ai_use_of_unpublished_material", "notice_version", "recorded_at")
    readonly_fields = list_display

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def delete_view(self, request, object_id, extra_context=None):
        raise PermissionDenied


class ReadOnlyRecordAdmin(admin.ModelAdmin):
    """Contributors' own records: the team reads them here and exports them; it neither edits nor
    deletes them (deleting would silently change a frozen review, and a confirmed version number
    could be given again). Withdrawal at a contributor's request is its own, logged step (plan §3)."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ItemReview)
class ItemReviewAdmin(ReadOnlyRecordAdmin):
    list_display = ("assignment", "item", "verdict", "ai_used", "version", "updated_at")
    list_filter = ("assignment__paper", "verdict", "ai_used")


@admin.register(Proposal)
class ProposalAdmin(ReadOnlyRecordAdmin):
    list_display = ("public_id", "assignment", "category", "ai_used", "created_at")
    list_filter = ("assignment__paper", "category")


@admin.register(Confirmation)
class ConfirmationAdmin(ReadOnlyRecordAdmin):
    list_display = ("assignment", "version", "confirmed_at", "content_sha256")


class QuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["answer"]
        widgets = {"answer": forms.Textarea(attrs={"rows": 6})}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """'Ask the team' queue (D-049): unanswered first, oldest first, with each question's age and owner."""

    form = QuestionAnswerForm
    list_display = ("public_id", "paper", "item", "age", "answered", "owner", "created_at")
    list_filter = ("assignment__paper", "assignment__paper__team_owner", ("answered_at", admin.EmptyFieldListFilter))
    readonly_fields = ("public_id", "assignment", "item", "text", "created_at", "answered_at", "answered_by")
    fields = ("public_id", "assignment", "item", "created_at", "text", "answer", "answered_at", "answered_by")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False        # a contributor's question is part of their record

    @admin.display(description="Paper")
    def paper(self, obj):
        return obj.assignment.paper.paper_id

    @admin.display(description="Owner")
    def owner(self, obj):
        return obj.assignment.paper.team_owner or "—"

    @admin.display(boolean=True, description="Answered")
    def answered(self, obj):
        return obj.answered_at is not None

    @admin.display(description="Waiting")
    def age(self, obj):
        if obj.answered_at:
            return "—"
        days = (timezone.now() - obj.created_at).days
        return "today" if days == 0 else f"{days} day(s)"

    def save_model(self, request, obj, form, change):
        operation = None
        if "answer" in form.changed_data:
            if obj.answer.strip():
                obj.answered_at, obj.answered_by, operation = timezone.now(), request.user.get_username(), "question_answered"
            else:           # an answer removed: the question is waiting again
                obj.answer, obj.answered_at, obj.answered_by, operation = "", None, "", "question_answer_removed"
        super().save_model(request, obj, form, change)
        if operation:
            log_event(request.user.get_username(), operation, obj.assignment, question_id=obj.public_id)
