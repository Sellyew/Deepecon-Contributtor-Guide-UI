"""Team administration for papers and their records (plan §2.1, §2.7)."""
from django import forms
from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import path

from . import importers
from .models import CandidatePackage, EventLog, ExposureLogEntry, Item, ItemMap, Paper, RubricVersion, log_event


class ImportForm(forms.Form):
    KIND_CHOICES = [
        ("paper_config", "Paper configuration (paper-config.json)"),
        ("rubric", "The team's rubric file"),
        ("item_map", "Item map (item-map.json)"),
        ("candidate_package", "Agent-facing candidate package (ZIP)"),
    ]
    kind = forms.ChoiceField(choices=KIND_CHOICES)
    paper = forms.ModelChoiceField(queryset=Paper.objects.all(), required=False,
                                   help_text="Required for everything except a paper configuration.")
    file = forms.FileField()

    def clean(self):
        data = super().clean()
        if data.get("kind") != "paper_config" and not data.get("paper"):
            raise forms.ValidationError("Choose the paper this file belongs to.")
        return data


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ("paper_id", "title", "field", "publication_status", "designated_on", "in_pool", "imported_at")
    list_filter = ("in_pool", "publication_status")
    # Everything comes from the imported configuration except whether the paper is open to all
    # contributors (D-044), which the team switches here.
    fields = ("paper_id", "title", "field", "publication_status", "designated_on", "in_pool", "config", "config_sha256", "imported_at")
    readonly_fields = ("paper_id", "field", "title", "config", "config_sha256", "publication_status", "designated_on", "imported_at")
    change_list_template = "admin/papers/paper_change_list.html"

    def has_add_permission(self, request):
        return False        # papers are created by importing their configuration

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if "in_pool" in form.changed_data:
            log_event(request.user.get_username(), "pool_changed", obj, in_pool=obj.in_pool)
            chosen = obj.assignments.filter(added_by="contributor").count()
            if not obj.in_pool and chosen:
                self.message_user(request, f"{obj.paper_id} is no longer open to all contributors, but {chosen} "
                                  "contributor(s) who chose it keep access. To withdraw it, delete their assignments "
                                  "(Assignments, filtered by this paper and 'Chosen by the contributor').", messages.WARNING)

    def get_urls(self):
        return [path("import/", self.admin_site.admin_view(self.import_view), name="papers_import")] + super().get_urls()

    def import_view(self, request):
        if not self.has_change_permission(request):
            raise PermissionDenied          # being staff is not enough to import or overwrite files
        form = ImportForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            kind, paper, upload = form.cleaned_data["kind"], form.cleaned_data["paper"], form.cleaned_data["file"]
            actor = request.user.get_username()
            try:
                if kind == "paper_config":
                    result = importers.import_paper_config(upload.read(), actor)
                elif kind == "rubric":
                    result = importers.import_rubric(paper, upload.read(), actor)
                elif kind == "item_map":
                    result = importers.import_item_map(paper, upload.read(), actor)
                else:
                    result = importers.import_candidate_package(paper, upload, actor)
            except importers.ImportRefused as refused:
                for problem in refused.problems:
                    messages.error(request, problem)
            else:
                messages.success(request, f"Imported {result}.")
                return redirect("admin:papers_paper_changelist")
        context = {**self.admin_site.each_context(request), "form": form, "title": "Import the team's files", "opts": self.model._meta}
        return render(request, "admin/papers/import_form.html", context)


@admin.register(RubricVersion)
class RubricVersionAdmin(ReadOnlyAdmin):
    list_display = ("paper", "version", "sha256", "imported_at")


@admin.register(Item)
class ItemAdmin(ReadOnlyAdmin):
    list_display = ("rubric", "item_id", "category", "position", "origin")
    list_filter = ("rubric__paper", "category")


@admin.register(ItemMap)
class ItemMapAdmin(ReadOnlyAdmin):
    list_display = ("paper", "rubric", "sha256", "imported_at")


@admin.register(CandidatePackage)
class CandidatePackageAdmin(ReadOnlyAdmin):
    list_display = ("paper", "candidate_version", "sha256", "size_bytes", "imported_at")


@admin.register(ExposureLogEntry)
class ExposureLogEntryAdmin(admin.ModelAdmin):
    list_display = ("paper", "occurred_on", "material", "route", "developer", "api_host", "account_kind", "model_version", "model_release_date")
    list_filter = ("paper", "material", "route", "developer")
    readonly_fields = ("recorded_by", "recorded_at")

    # The log is append-only (Rule 10): entries are added and viewed, never edited or deleted;
    # corrections are new entries with a note.
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.recorded_by = request.user.get_username()
        super().save_model(request, obj, form, change)
        log_event(obj.recorded_by, "exposure_recorded", obj.paper, exposure_id=obj.pk, route=obj.route,
                  occurred_on=obj.occurred_on.isoformat())


@admin.register(EventLog)
class EventLogAdmin(ReadOnlyAdmin):
    list_display = ("at", "actor", "operation", "object_type", "object_id")
    list_filter = ("operation",)

    def has_delete_permission(self, request, obj=None):
        return False
