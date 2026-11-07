"""Contributors, their assignments, invitations, and consent records (plan §2.2; D-042, D-044).

Each contributor has one personal link at a time. It opens one paper: the contributor's
current assignment, which the contributor chooses from the papers offered to them (their own
assignments, and the papers the team opens to all contributors) and can change at any time.
"""
import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

from papers.models import Paper, log_event


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
    current_assignment = models.ForeignKey(
        "Assignment", null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
        verbose_name="current paper", help_text="The paper the contributor's link opens (D-044).")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.display_name} ({self.public_id})"

    def current(self):
        """The current assignment, if it is really this contributor's."""
        a = self.current_assignment
        return a if a is not None and a.contributor_id == self.pk else None

    def choosable_papers(self):
        """Papers offered to this contributor: their assignments, and papers open to all."""
        return Paper.objects.filter(Q(in_pool=True) | Q(assignments__contributor=self)).distinct()

    @transaction.atomic
    def choose(self, paper):
        """Make `paper` the one the link opens; returns (assignment, previous assignment, created)."""
        previous = self.current()
        assignment, created = Assignment.objects.get_or_create(
            contributor=self, paper=paper,
            defaults={"relationship_to_paper": "invited_expert", "added_by": Assignment.BY_CONTRIBUTOR})
        self.current_assignment = assignment
        self.save(update_fields=["current_assignment"])
        return assignment, previous, created


class Assignment(models.Model):
    RELATIONSHIP_CHOICES = [("author", "Author of the paper"), ("invited_expert", "Invited expert")]
    BY_TEAM, BY_CONTRIBUTOR = "team", "contributor"
    ADDED_BY_CHOICES = [(BY_TEAM, "Offered by the team"), (BY_CONTRIBUTOR, "Chosen by the contributor from the papers open to all")]

    public_id = models.CharField(max_length=32, unique=True, default=assignment_public_id,
                                 help_text="Pseudonymous ID used in exports (assignment_id).")
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name="assignments")
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT, related_name="assignments")
    relationship_to_paper = models.CharField(max_length=32, choices=RELATIONSHIP_CHOICES,
                                             help_text="Only the team records authorship.")
    added_by = models.CharField(max_length=16, choices=ADDED_BY_CHOICES, default=BY_TEAM)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("contributor", "paper")]

    def __str__(self):
        return f"{self.public_id}: {self.contributor.public_id} on {self.paper.paper_id}"

    def latest_consent(self):
        return self.consents.order_by("-recorded_at", "-pk").first()


class Invitation(models.Model):
    """A contributor's personal link. Only the token's SHA-256 is stored.

    The link opens the contributor's current paper. Its expiry stops new sign-ins only; a
    session already opened with it lasts until the link is revoked, or until it has not been
    used for SESSION_COOKIE_AGE (a year; D-044, P-060).
    """

    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name="invitations")
    token_hash = models.CharField(max_length=64, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)
    first_used_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"invitation for {self.contributor.public_id} (expires {self.expires_at:%Y-%m-%d})"

    @classmethod
    def issue(cls, contributor, days=None):
        """Create an invitation; returns (invitation, raw token). The raw token is not stored.

        Use issue_invitation() outside tests: it also revokes the contributor's earlier links.
        """
        raw = secrets.token_urlsafe(32)
        days = settings.INVITATION_DAYS if days is None else days
        inv = cls.objects.create(contributor=contributor, token_hash=hash_token(raw),
                                 expires_at=timezone.now() + timedelta(days=days))
        return inv, raw

    @classmethod
    def find_active(cls, raw):
        """The invitation a raw token opens, if it is neither revoked nor expired."""
        if not raw or len(raw) > 128:
            return None
        inv = cls.objects.select_related("contributor").filter(token_hash=hash_token(raw)).first()
        return inv if inv and inv.is_active else None

    @property
    def is_active(self):
        """Whether the link can still be opened."""
        return self.revoked_at is None and self.expires_at > timezone.now()

    def link(self, raw):
        return f"{settings.SITE_BASE_URL.rstrip('/')}/i/{raw}/"


def set_first_paper(contributor, assignment, actor):
    """Make `assignment` the contributor's current paper if they have none (D-044).

    The link stays on a paper the contributor chose until they change it, so the team does
    not move it. Returns a note for the team when the contributor's own choice was kept.
    """
    current = contributor.current()
    if current is None:
        contributor.current_assignment = assignment
        contributor.save(update_fields=["current_assignment"])
        log_event(actor, "current_paper_set", assignment, by="team")
        return ""
    if current.pk != assignment.pk:
        return f"kept the contributor's current paper, {current.paper.paper_id}; they can change it themselves"
    return ""


@transaction.atomic
def issue_invitation(contributor, actor, days=None):
    """Issue the contributor's personal link and revoke their earlier ones: one link at a time."""
    earlier = list(contributor.invitations.filter(revoked_at__isnull=True).values_list("pk", flat=True))
    contributor.invitations.filter(pk__in=earlier).update(revoked_at=timezone.now())
    invitation, raw = Invitation.issue(contributor, days)
    log_event(actor, "invitation_issued", invitation, contributor_id=contributor.public_id,
              expires_at=invitation.expires_at.isoformat(), revoked_earlier=earlier)
    return invitation, raw


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
