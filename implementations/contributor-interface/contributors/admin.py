"""Team administration for contributors, assignments, invitations, and consent (plan §2.2; D-044).

A contributor has one personal link at a time; it opens their current paper. Creating a link
from an assignment also makes that assignment the current paper; creating one from a
contributor leaves the current paper as it is (a contributor with none chooses one).
"""
from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.utils import timezone

from papers.models import log_event

from .models import Assignment, Consent, Contributor, Invitation, issue_invitation


class InviteActionMixin:
    def has_invite_permission(self, request):
        return request.user.has_perm("contributors.add_invitation")

    def _links_page(self, request, created):
        # The links are rendered in this response only: they are never stored in messages,
        # sessions, or logs, and the response is not cached (Cache-Control: no-store).
        return TemplateResponse(request, "admin/contributors/invitations_created.html",
                                {**self.admin_site.each_context(request), "title": "Invitation links", "created": created})

    def _issue(self, request, contributor):
        invitation, raw = issue_invitation(contributor, request.user.get_username())
        current = contributor.current()
        return {"contributor": contributor, "opens": current.paper.paper_id if current else None,
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

    @admin.action(description="Create a personal link that opens this paper (shown once; earlier links are revoked)",
                  permissions=["invite"])
    def create_invitation(self, request, queryset):
        assignments = list(queryset.select_related("contributor", "paper"))
        contributors = [a.contributor_id for a in assignments]
        if len(contributors) != len(set(contributors)):
            self.message_user(request, "A link opens one paper: select at most one assignment per contributor.", messages.ERROR)
            return None
        created = []
        for assignment in assignments:
            contributor = assignment.contributor
            contributor.current_assignment = assignment
            contributor.save(update_fields=["current_assignment"])
            log_event(request.user.get_username(), "current_paper_set", assignment, by="team")
            created.append(self._issue(request, contributor))
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
