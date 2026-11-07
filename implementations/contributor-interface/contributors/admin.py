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
from django import forms
from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone

from papers.models import log_event

from .models import Assignment, Consent, Contributor, Invitation, issue_invitation, set_first_paper


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
    list_display = ("public_id", "contributor", "paper", "relationship_to_paper", "added_by", "created_at")
    list_filter = ("paper", "relationship_to_paper", "added_by")
    readonly_fields = ("public_id", "added_by", "created_at")
    actions = ["create_invitation"]

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
    list_display = ("assignment", "evaluation_through_apis_acknowledged", "team_ai_use_of_unpublished_material", "notice_version", "recorded_at")
    readonly_fields = list_display

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
