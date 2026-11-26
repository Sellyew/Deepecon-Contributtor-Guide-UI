"""Team pages for submissions (M3). The team reads the contributor's answers and uploads, exports
the manifest, and records receipt and verification; it neither edits nor deletes them (withdrawal
at the contributor's request is the one logged step that does, contributors/admin.py).

Uploaded archives cannot be downloaded here yet: the data steward's check, which must come
before anyone opens uploaded data, is built in M4 (plan §3, MVP §5.5). The team sees each
archive's size, SHA-256, and list of file names and sizes.
"""
import json

from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html_join

from papers.models import log_event

from . import manifest
from .models import ChecklistAnswer, DatasetDeclaration, Submission, SubmissionVersion, Upload


class ReadOnly(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ChecklistInline(admin.TabularInline):
    model = ChecklistAnswer
    fields = ("checklist_id", "status", "note")
    readonly_fields = fields
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class DatasetInline(ChecklistInline):
    model = DatasetDeclaration
    fields = ("name", "availability", "access_route", "source", "terms", "where", "notes")
    readonly_fields = fields


@admin.register(Submission)
class SubmissionAdmin(ReadOnly):
    list_display = ("assignment", "channel", "updated_at")
    list_filter = ("assignment__paper", "channel")
    inlines = [DatasetInline, ChecklistInline]


@admin.register(Upload)
class UploadAdmin(ReadOnly):
    list_display = ("public_id", "assignment", "original_name", "size_bytes", "status", "sha256", "completed_at")
    list_filter = ("assignment__paper", "status")
    exclude = ("entries", "storage_name")
    readonly_fields = ("listing",)

    @admin.display(description="Files in the archive (names and sizes only; nothing is extracted)")
    def listing(self, obj):
        rows = format_html_join("\n", "<li>{} ({} bytes)</li>", ((name, size) for name, size in obj.entries))
        more = " …and more (list truncated)" if obj.entries_truncated else ""
        return format_html_join("", "<ul>{}</ul>{}", [(rows, more)])


@admin.register(SubmissionVersion)
class SubmissionVersionAdmin(ReadOnly):
    list_display = ("assignment", "version", "submitted_at", "received_at", "verification_status", "verified_by")
    list_filter = ("assignment__paper", "verification_status")
    exclude = ("manifest", "uploads")
    readonly_fields = ("manifest_pretty",)
    actions = ["mark_received", "mark_verified", "mark_mismatch", "export_manifest"]

    @admin.display(description="Manifest")
    def manifest_pretty(self, obj):
        return format_html_join("", "<pre>{}</pre>", [(json.dumps(obj.manifest, indent=2, ensure_ascii=False),)])

    def has_record_permission(self, request):
        # Recording receipt and verification changes the team's record, not the contributor's answers.
        return request.user.has_perm("submissions.change_submissionversion")

    def _set(self, request, queryset, operation, **fields):
        for version in queryset:
            for field, value in fields.items():
                setattr(version, field, value)
            version.save(update_fields=list(fields))
            log_event(request.user.get_username(), operation, version.assignment, version=version.version)
        self.message_user(request, f"{queryset.count()} version(s) updated.", messages.SUCCESS)

    @admin.action(description="Record that the team received the materials", permissions=["record"])
    def mark_received(self, request, queryset):
        self._set(request, queryset.filter(received_at__isnull=True), "submission_received", received_at=timezone.now())

    @admin.action(description="Record that the materials match the manifest (verified)", permissions=["record"])
    def mark_verified(self, request, queryset):
        self._set(request, queryset, "submission_verified", verification_status="verified",
                  verified_by=request.user.get_username())

    @admin.action(description="Record that the materials do not match the manifest", permissions=["record"])
    def mark_mismatch(self, request, queryset):
        self._set(request, queryset, "submission_mismatch", verification_status="mismatch",
                  verified_by=request.user.get_username())

    def has_export_permission(self, request):
        return all(request.user.has_perm(f"submissions.view_{model}") for model in
                   ("submissionversion", "submission", "upload", "datasetdeclaration", "checklistanswer"))

    @admin.action(description="Export the selected version's manifest as JSON (submission-manifest schema)",
                  permissions=["export"])
    def export_manifest(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Export one version at a time.", messages.ERROR)
            return None
        version = queryset.select_related("assignment__paper").get()
        data = manifest.export(version)
        log_event(request.user.get_username(), "manifest_exported", version.assignment, version=version.version)
        response = HttpResponse(json.dumps(data, ensure_ascii=False, indent=2), content_type="application/json; charset=utf-8")
        response["Content-Disposition"] = (f'attachment; filename="{version.assignment.paper.paper_id}-'
                                           f'{version.assignment.public_id}-submission-v{version.version}.json"')
        return response
