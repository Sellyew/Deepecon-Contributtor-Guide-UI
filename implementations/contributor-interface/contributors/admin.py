"""Team administration for contributors, assignments, invitations, and consent (plan §2.2; D-044).

A contributor has one personal link at a time; it opens their current paper. Creating a link
from an assignment makes that assignment the current paper only if the contributor has none:
the link stays on the paper a contributor chose until they change it (D-044). Creating one
from a contributor leaves the current paper as it is (a contributor with none chooses one).
An assignment's contributor and paper cannot be changed once it exists, because consent and
reviews belong to it; a mistake is corrected by creating a new assignment.
"""
from django.contrib import admin, messages
from django.template.response import TemplateResponse
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


@admin.register(Contributor)
class ContributorAdmin(InviteActionMixin, admin.ModelAdmin):
    list_display = ("display_name", "public_id", "current_assignment", "preferred_language", "created_at")
    readonly_fields = ("public_id", "current_assignment", "created_at")
    actions = ["create_invitation"]

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
