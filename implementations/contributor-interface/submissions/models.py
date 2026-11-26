"""Guidance and submission (M3; MVP §5; plan §2.5).

A contributor tells the team how the full runnable package reaches it (D-027): uploaded
archives, a public reference, or another agreed channel; the package's master script, README,
and software; each dataset's availability and, for data that cannot be shared, the route by
which the team can still run the code; which checklist entries are covered; and two
declarations. Submitting creates a numbered version holding the manifest and its SHA-256.

Uploads are stored in private storage under generated names. They are never extracted or run:
the site reads only each archive's list of file names and sizes (plan §2.5). The data
steward's check before anyone opens uploaded data comes in M4 (plan §3, MVP §5.5).

Contributors' records are never deleted as a side effect (PROTECT); withdrawal at the
contributor's request deletes them, files included, as one logged step (plan §3).
"""
import secrets

from django.conf import settings
from django.db import models

from contributors.models import AIHelpFields, Assignment


def upload_public_id():
    return f"u-{secrets.token_hex(6)}"


class Submission(AIHelpFields):
    """The contributor's current answers about their materials; a draft until submitted. The team
    can read drafts; submitting tells it that the materials are complete and creates a version.
    The AI disclosure covers what the contributor wrote here, such as README text (D-039)."""

    CHANNELS = [("upload", "Upload"), ("public_reference", "Public reference"), ("other_agreed", "Another agreed channel")]
    RUN_TIMES = [(band, band) for band in ("<10 minutes", "10-60 minutes", "1-2 hours", "2-8 hours", "8-24 hours",
                                           "1-3 days", "3-14 days", ">14 days")]          # the template README's bands

    assignment = models.OneToOneField(Assignment, on_delete=models.PROTECT, related_name="submission")
    channel = models.CharField(max_length=20, choices=CHANNELS, blank=True)
    pub_repository = models.CharField("repository", max_length=200, blank=True)
    pub_identifier = models.CharField("identifier", max_length=200, blank=True)
    pub_version = models.CharField("version", max_length=100, blank=True)
    pub_url = models.URLField("URL", max_length=500, blank=True)
    pub_doi = models.CharField("DOI", max_length=200, blank=True)
    other_channel_note = models.TextField(blank=True)
    master_script = models.CharField(max_length=500, blank=True)
    readme = models.CharField(max_length=500, blank=True)
    software = models.JSONField(default=list, blank=True, help_text='[{"name": ..., "version": ...}]')
    dependencies_included = models.BooleanField(null=True)
    author_run_log_included = models.BooleanField(null=True)
    expected_outputs_included = models.BooleanField(null=True)
    run_time = models.CharField(max_length=16, choices=RUN_TIMES, blank=True)
    hardware_note = models.TextField(blank=True)
    no_restricted_included = models.BooleanField(default=False)
    permission_to_share = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=0)        # optimistic: a page out of date never overwrites
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Submission for {self.assignment.public_id}"


class ChecklistAnswer(models.Model):
    STATUSES = [("provided", "Provided"), ("in_public_package", "In the public package"),
                ("not_available", "Not available"), ("not_applicable", "Not applicable")]

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="checklist")
    checklist_id = models.CharField(max_length=64)
    status = models.CharField(max_length=20, choices=STATUSES, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = [("submission", "checklist_id")]


class DatasetDeclaration(models.Model):
    AVAILABILITY = [("included", "Included in the upload"), ("public_elsewhere", "Public elsewhere"),
                    ("restricted_not_included", "Restricted, not included"),
                    ("confidential_not_included", "Confidential, not included"),
                    ("not_decided", "Not yet decided")]
    ROUTES = [("author_runs_and_returns_outputs", "The author or their RA runs the team's versions and returns outputs"),
              ("team_applies_for_access", "The team applies for access"),
              ("secure_environment", "A secure environment"),
              ("fully_synthetic_substitute", "A fully synthetic substitute"),
              ("to_be_decided", "To be decided")]

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="datasets")
    position = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=300)
    source = models.CharField(max_length=500, blank=True)
    terms = models.CharField(max_length=500, blank=True)
    availability = models.CharField(max_length=32, choices=AVAILABILITY)
    where = models.CharField(max_length=500, blank=True)
    access_route = models.CharField(max_length=40, choices=ROUTES, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["submission", "position", "pk"]

    def export(self):
        out = {"name": self.name, "availability": self.availability}
        for field in ("source", "terms", "where", "access_route", "notes"):
            if getattr(self, field).strip():
                out[field] = getattr(self, field).strip()
        return out


class Upload(models.Model):
    """One archive the contributor sent, received in chunks so that it can be resumed."""

    RECEIVING, CHECKING, RECEIVED, REFUSED = "receiving", "checking", "received", "refused"
    STATUSES = [(RECEIVING, "Receiving"), (CHECKING, "Computing its SHA-256"), (RECEIVED, "Received"), (REFUSED, "Refused")]

    public_id = models.CharField(max_length=32, unique=True, default=upload_public_id)
    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT, related_name="uploads")
    original_name = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField()
    received_bytes = models.BigIntegerField(default=0)
    status = models.CharField(max_length=12, choices=STATUSES, default=RECEIVING)
    refusal = models.CharField(max_length=300, blank=True)
    sha256 = models.CharField(max_length=64, blank=True)
    storage_name = models.CharField(max_length=300)
    entries = models.JSONField(default=list, blank=True, help_text="[[name, size], ...] read from the archive's directory")
    entries_truncated = models.BooleanField(default=False)
    entry_count = models.PositiveIntegerField(default=0, help_text="Files in the archive, from its directory.")
    client_modified = models.BigIntegerField(null=True, blank=True, help_text="The file's last-modified time in the "
                                             "contributor's browser; a resume must match it, as well as name and size.")
    head_sha256 = models.CharField(max_length=64, blank=True, help_text="SHA-256 of the file's first MiB, from the browser.")
    included = models.BooleanField(default=True, help_text="Part of the next submitted version. The contributor can leave "
                                   "out an archive they replaced; earlier versions keep it.")
    checking_since = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["assignment", "created_at", "pk"]

    def __str__(self):
        return f"{self.public_id} {self.original_name}"


class SubmissionVersion(models.Model):
    """What the contributor submitted: the manifest as it stood, and its SHA-256."""

    VERIFICATION = [("pending", "Pending"), ("verified", "Verified"), ("mismatch", "Mismatch")]

    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT, related_name="submission_versions")
    version = models.PositiveIntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    manifest = models.JSONField()
    manifest_sha256 = models.CharField(max_length=64)
    language = models.CharField(max_length=16, blank=True)
    uploads = models.ManyToManyField(Upload, blank=True, related_name="versions")
    received_at = models.DateTimeField(null=True, blank=True, help_text="When the team received the materials.")
    verification_status = models.CharField(max_length=12, choices=VERIFICATION, default="pending")
    verified_by = models.CharField(max_length=150, blank=True)

    class Meta:
        unique_together = [("assignment", "version")]
        ordering = ["assignment", "version"]

    def __str__(self):
        return f"{self.assignment.public_id} submission {self.version}"


def max_upload_bytes(paper):
    return int((paper.config.get("submission") or {}).get("max_upload_bytes") or settings.DEFAULT_MAX_UPLOAD_BYTES)


def accepted_channels(paper):
    return list((paper.config.get("submission") or {}).get("accepted_channels") or ["upload", "public_reference", "other_agreed"])


def runnable_required(paper):
    return bool((paper.config.get("submission") or {}).get("runnable_package_required", True))
