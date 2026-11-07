"""Papers, the team's rubric files, item maps, candidate packages, and the team's records.

The team's files are stored as they are (P-041) and normalized through the paper's
configured categories (D-025). Nothing here is sent to any AI service (D-042).
"""
from django.core.exceptions import ValidationError
from django.db import models


class Paper(models.Model):
    SCORED = "scored"
    DEMO = "demo_or_development"
    PUBLICATION_CHOICES = [
        (SCORED, "Scored: answers stay unpublished until retired"),
        (DEMO, "Demo or development: may be published, not scored"),
    ]

    paper_id = models.SlugField(max_length=64, unique=True)
    field = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=500)
    config = models.JSONField(help_text="The imported paper configuration, as validated.")
    config_sha256 = models.CharField(max_length=64)
    publication_status = models.CharField(max_length=32, choices=PUBLICATION_CHOICES, default=SCORED)
    designated_on = models.DateField(null=True, blank=True, help_text="Date of the demo or development designation (Rule 8).")
    imported_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["paper_id"]

    def __str__(self):
        return self.paper_id

    def current_rubric(self):
        return self.rubrics.filter(version=self.config.get("rubric_version")).first()

    def current_package(self):
        # Only the package whose hash the current configuration names (the importer's own rules).
        return self.packages.filter(candidate_version=self.config.get("candidate_version") or "unversioned",
                                    sha256=self.config.get("candidate_package_sha256", "")).first()


class RubricVersion(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="rubrics")
    version = models.CharField(max_length=100)
    raw = models.JSONField(help_text="The team's rubric file, stored as it is (P-041). Expert-only.")
    sha256 = models.CharField(max_length=64)
    imported_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("paper", "version")]
        ordering = ["paper", "version"]

    def __str__(self):
        return f"{self.paper.paper_id} {self.version}"


class Item(models.Model):
    """One prepared item, normalized through the paper's category profile."""

    rubric = models.ForeignKey(RubricVersion, on_delete=models.CASCADE, related_name="items")
    item_id = models.CharField(max_length=16)
    category = models.CharField(max_length=64)
    position = models.PositiveIntegerField()
    normalized = models.JSONField(help_text="Display roles from validation/rubric_checks.normalize, without the raw rubric entry.")
    origin = models.JSONField(null=True, blank=True, help_text="Who drafted the item and whether AI helped review it (D-039). Never shown to contributors.")

    class Meta:
        unique_together = [("rubric", "item_id")]
        ordering = ["rubric", "position"]

    def __str__(self):
        return f"{self.rubric} {self.item_id}"


class ItemMap(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="item_maps")
    rubric = models.ForeignKey(RubricVersion, on_delete=models.CASCADE, related_name="item_maps")
    raw = models.JSONField()
    sha256 = models.CharField(max_length=64)
    imported_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("paper", "rubric")]

    def __str__(self):
        return f"item map for {self.rubric}"


class CandidatePackage(models.Model):
    """The agent-facing ZIP that contributors may download (D-028), kept in private storage."""

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="packages")
    candidate_version = models.CharField(max_length=100)
    sha256 = models.CharField(max_length=64)
    size_bytes = models.PositiveBigIntegerField()
    storage_name = models.CharField(max_length=300, help_text="Path relative to the private storage root.")
    imported_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("paper", "candidate_version")]

    def __str__(self):
        return f"{self.paper.paper_id} {self.candidate_version}"


class ExposureLogEntry(models.Model):
    """Rule 10 (D-040): which AI services received a task's answer-key material or package."""

    MATERIAL_CHOICES = [
        ("answer_key", "Answer-key material (items, rubric, item map, flawed code)"),
        ("package", "Agent-facing package"),
        ("package_and_trajectory", "Package and an agent's work (evaluation run)"),
    ]
    ROUTE_CHOICES = [
        ("construction", "While building the task"),
        ("contributor_review", "Reported by a contributor"),
        ("calibration", "Calibration trial"),
        ("evaluation_run", "Evaluation run"),
        ("other", "Other"),
    ]
    ACCOUNT_CHOICES = [("work", "Work or business"), ("personal", "Personal"), ("api", "API"), ("unknown", "Unknown")]

    paper = models.ForeignKey(Paper, on_delete=models.PROTECT, related_name="exposures")
    occurred_on = models.DateField()
    ai_service = models.CharField(max_length=200, help_text="The tool or API used, including AI coding assistants that opened the files.")
    developer = models.CharField(max_length=200, help_text="The model's developer.")
    api_host = models.CharField(max_length=200, blank=True, help_text="The API host, if different from the developer.")
    material = models.CharField(max_length=32, choices=MATERIAL_CHOICES)
    route = models.CharField(max_length=32, choices=ROUTE_CHOICES)
    account_kind = models.CharField(max_length=16, choices=ACCOUNT_CHOICES)
    model_version = models.CharField(max_length=200, blank=True, help_text="Pinned model snapshot, for evaluation runs.")
    model_release_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.CharField(max_length=200)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["paper", "occurred_on"]
        verbose_name = "exposure log entry"
        verbose_name_plural = "exposure log"

    def __str__(self):
        return f"{self.paper.paper_id} {self.occurred_on} {self.developer} ({self.material})"

    def clean(self):
        if self.route == "evaluation_run" and (not self.model_version or not self.model_release_date):
            raise ValidationError("An evaluation run needs the pinned model version and its release date (Rule 10).")


class EventLog(models.Model):
    """Actor, operation, object, and time for imports, invitations, consents, and downloads.

    Details hold IDs, counts, and hashes only, never item text or contributor text.
    """

    at = models.DateTimeField(auto_now_add=True)
    actor = models.CharField(max_length=200)
    operation = models.CharField(max_length=64)
    object_type = models.CharField(max_length=64)
    object_id = models.CharField(max_length=200)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-at"]

    def __str__(self):
        return f"{self.at:%Y-%m-%d %H:%M} {self.actor} {self.operation} {self.object_type} {self.object_id}"


def log_event(actor, operation, obj, **details):
    return EventLog.objects.create(
        actor=str(actor), operation=operation, object_type=type(obj).__name__, object_id=str(obj), details=details
    )
