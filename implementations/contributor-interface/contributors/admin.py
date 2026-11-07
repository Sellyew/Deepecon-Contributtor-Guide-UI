"""Team administration for contributors, assignments, invitations, and consent (plan §2.2)."""
from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils import timezone

from papers.models import log_event

from .models import Assignment, Consent, Contributor, Invitation


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ("display_name", "public_id", "preferred_language", "created_at")
    readonly_fields = ("public_id", "created_at")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("public_id", "contributor", "paper", "relationship_to_paper", "created_at")
    list_filter = ("paper", "relationship_to_paper")
    readonly_fields = ("public_id", "created_at")
    actions = ["create_invitation"]

    @admin.action(description="Create an invitation link (shown once)")
    def create_invitation(self, request, queryset):
        # The links are rendered in this response only: they are never stored in messages,
        # sessions, or logs, and the response is not cached (Cache-Control: no-store).
        created = []
        for assignment in queryset.select_related("contributor", "paper"):
            invitation, raw = Invitation.issue(assignment)
            log_event(request.user.get_username(), "invitation_issued", assignment, invitation_id=invitation.pk,
                      expires_at=invitation.expires_at.isoformat())
            created.append({"assignment": assignment, "link": invitation.link(raw), "expires_at": invitation.expires_at})
        return TemplateResponse(request, "admin/contributors/invitations_created.html",
                                {**self.admin_site.each_context(request), "title": "Invitation links", "created": created})


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("assignment", "created_at", "expires_at", "revoked_at", "first_used_at", "last_used_at")
    readonly_fields = ("assignment", "token_hash", "created_at", "expires_at", "revoked_at", "first_used_at", "last_used_at")
    actions = ["revoke"]

    def has_add_permission(self, request):
        return False        # use the action on assignments, so the token is generated and shown once

    @admin.action(description="Revoke the selected invitations")
    def revoke(self, request, queryset):
        now = timezone.now()
        for invitation in queryset.filter(revoked_at__isnull=True):
            invitation.revoked_at = now
            invitation.save(update_fields=["revoked_at"])
            log_event(request.user.get_username(), "invitation_revoked", invitation.assignment, invitation_id=invitation.pk)


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ("assignment", "evaluation_through_apis_acknowledged", "team_ai_use_of_unpublished_material", "notice_version", "recorded_at")
    readonly_fields = list_display

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
