"""Contributors, their assignments, invitations, and consent records (plan §2.2; D-042)."""
import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from papers.models import Paper


def _public_id(prefix):
    return f"{prefix}-{secrets.token_hex(6)}"


def contributor_public_id():
    return _public_id("c")


def assignment_public_id():
    return _public_id("a")


def hash_token(raw):
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class Contributor(models.Model):
    public_id = models.CharField(max_length=32, unique=True, default=contributor_public_id,
                                 help_text="Pseudonymous ID used in exports (contributor_id).")
    display_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, help_text="Optional. The team delivers invitations itself; the site sends no e-mail.")
    preferred_language = models.CharField(max_length=16, choices=settings.LANGUAGES, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.display_name} ({self.public_id})"


class Assignment(models.Model):
    RELATIONSHIP_CHOICES = [("author", "Author of the paper"), ("invited_expert", "Invited expert")]

    public_id = models.CharField(max_length=32, unique=True, default=assignment_public_id,
                                 help_text="Pseudonymous ID used in exports (assignment_id).")
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name="assignments")
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT, related_name="assignments")
    relationship_to_paper = models.CharField(max_length=32, choices=RELATIONSHIP_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("contributor", "paper")]

    def __str__(self):
        return f"{self.public_id}: {self.contributor.public_id} on {self.paper.paper_id}"

    def latest_consent(self):
        return self.consents.order_by("-recorded_at", "-pk").first()


class Invitation(models.Model):
    """An invitation link for one assignment. Only the token's SHA-256 is stored."""

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="invitations")
    token_hash = models.CharField(max_length=64, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)
    first_used_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"invitation for {self.assignment.public_id} (expires {self.expires_at:%Y-%m-%d})"

    @classmethod
    def issue(cls, assignment, days=None):
        """Create an invitation; returns (invitation, raw token). The raw token is not stored."""
        raw = secrets.token_urlsafe(32)
        days = settings.INVITATION_DAYS if days is None else days
        inv = cls.objects.create(assignment=assignment, token_hash=hash_token(raw),
                                 expires_at=timezone.now() + timedelta(days=days))
        return inv, raw

    @classmethod
    def find_active(cls, raw):
        if not raw or len(raw) > 128:
            return None
        inv = cls.objects.select_related("assignment__contributor", "assignment__paper").filter(token_hash=hash_token(raw)).first()
        return inv if inv and inv.is_active else None

    @property
    def is_active(self):
        return self.revoked_at is None and self.expires_at > timezone.now()

    def link(self, raw):
        return f"{settings.SITE_BASE_URL.rstrip('/')}/i/{raw}/"


class Consent(models.Model):
    """The contributor's choices on the notice screen (D-042), one record per change."""

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="consents")
    evaluation_through_apis_acknowledged = models.BooleanField()
    team_ai_use_of_unpublished_material = models.BooleanField()
    notice_version = models.CharField(max_length=32)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"consent of {self.assignment.public_id} at {self.recorded_at:%Y-%m-%d %H:%M}"
