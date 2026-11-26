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
    frozen_at = models.DateTimeField(null=True, blank=True,
                                     help_text="When the team froze this review; the contributor can no longer change it.")
    frozen_by = models.CharField(max_length=150, blank=True)

    class Meta:
        unique_together = [("contributor", "paper")]

    def __str__(self):
        return f"{self.public_id}: {self.contributor.public_id} on {self.paper.paper_id}"

    def latest_consent(self):
        return self.consents.order_by("-recorded_at", "-pk").first()

    @property
    def is_frozen(self):
        return self.frozen_at is not None


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


# --- M2: Selection (plan §2.3–2.7; MVP §3–4; contributor-review schema 0.3.0) ---------------

def _short_id(prefix):
    return f"{prefix}-{secrets.token_hex(6)}"


def proposal_public_id():
    return _short_id("p")


def question_public_id():
    return _short_id("m")


TRI_STATE = [("yes", "Yes"), ("no", "No"), ("unsure", "Unsure")]
ACCOUNT_KINDS = [("work", "Work or business"), ("personal", "Personal"), ("api", "API"), ("unknown", "Unknown")]


class AIHelpFields(models.Model):
    """The contributor's own report that AI helped with an answer or proposal (D-039)."""

    ai_used = models.BooleanField(default=False)
    ai_tool = models.CharField(max_length=200, blank=True)
    ai_account_kind = models.CharField(max_length=16, choices=ACCOUNT_KINDS, blank=True)
    ai_entered_items = models.BooleanField(null=True, blank=True,
                                           help_text="Whether the items or the task package were put into the AI tool.")

    class Meta:
        abstract = True

    def ai_help(self):
        if not self.ai_used:
            return {"used": False}
        help_ = {"used": True, "tool": self.ai_tool or "not named", "entered_items_or_package": bool(self.ai_entered_items)}
        if self.ai_account_kind:
            help_["account_kind"] = self.ai_account_kind
        return help_


class ItemReview(AIHelpFields):
    """A contributor's answer on one prepared item. `version` rises with every save, so a
    save made from an outdated page is refused instead of silently overwriting (plan §2.4)."""

    VERDICTS = [("keep", "Keep"), ("keep_with_changes", "Keep with changes"), ("reject", "Reject"), ("unsure", "Unsure")]
    REJECT_REASONS = [("not_realistic", "Not realistic"), ("not_consequential", "Not consequential"),
                      ("repair_or_acceptable_work_wrong", "Repair or acceptable work wrong"), ("other", "Other")]
    VARIANT_CHOICES = [("first", "First"), ("second", "Second"), ("both", "Both"), ("neither", "Neither")]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="reviews")
    item = models.ForeignKey("papers.Item", on_delete=models.PROTECT, related_name="reviews")
    verdict = models.CharField(max_length=32, choices=VERDICTS)
    reject_reason = models.CharField(max_length=40, choices=REJECT_REASONS, blank=True)
    variant_choice = models.CharField(max_length=16, choices=VARIANT_CHOICES, blank=True)
    check_realistic = models.CharField(max_length=8, choices=TRI_STATE, blank=True)
    check_consequential = models.CharField(max_length=8, choices=TRI_STATE, blank=True)
    check_repair_correct = models.CharField(max_length=8, choices=TRI_STATE, blank=True)
    suggested_title = models.TextField(blank=True)
    suggested_description = models.TextField(blank=True)
    other_valid_repairs = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    version = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("assignment", "item")]
        ordering = ["assignment", "item__position"]

    def __str__(self):
        return f"{self.assignment.public_id} {self.item.item_id}: {self.verdict}"

    def export(self):
        out = {"item_id": self.item.item_id, "category": self.item.category, "verdict": self.verdict,
               "updated_at": self.updated_at.isoformat().replace("+00:00", "Z"), "ai_help": self.ai_help()}
        checks = {k: v for k, v in (("realistic", self.check_realistic), ("consequential", self.check_consequential),
                                    ("repair_correct", self.check_repair_correct)) if v}
        if checks:
            out["checks"] = checks
        if self.verdict == "reject" and self.reject_reason:
            out["reject_reason"] = self.reject_reason
        if self.variant_choice:
            out["variant_choice"] = self.variant_choice
        for field in ("suggested_title", "suggested_description", "other_valid_repairs", "comment"):
            if getattr(self, field).strip():
                out[field] = getattr(self, field).strip()
        return out


class Proposal(AIHelpFields):
    """An additional item proposed by the contributor (MVP §3 step 5)."""

    public_id = models.CharField(max_length=32, unique=True, default=proposal_public_id)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="proposals")
    category = models.CharField(max_length=64, help_text="A category ID from the paper configuration, or 'unsure'.")
    location = models.CharField(max_length=500, blank=True)
    description = models.TextField()
    why_it_matters = models.TextField(blank=True)
    suggested_repair = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["assignment", "created_at", "pk"]

    def __str__(self):
        return f"{self.public_id} on {self.assignment.public_id}"

    def export(self):
        out = {"proposal_id": self.public_id, "category": self.category, "description": self.description.strip(),
               "created_at": self.created_at.isoformat().replace("+00:00", "Z"), "ai_help": self.ai_help()}
        for field in ("location", "why_it_matters", "suggested_repair"):
            if getattr(self, field).strip():
                out[field] = getattr(self, field).strip()
        return out


class Question(models.Model):
    """'Ask the team' (MVP §4.2): a question stored on the site and answered in the admin. No AI, no e-mail."""

    public_id = models.CharField(max_length=32, unique=True, default=question_public_id)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="questions")
    item = models.ForeignKey("papers.Item", null=True, blank=True, on_delete=models.PROTECT, related_name="questions")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    answered_by = models.CharField(max_length=150, blank=True)

    class Meta:
        # Unanswered first, oldest first (D-049).
        ordering = [models.F("answered_at").asc(nulls_first=True), "created_at"]

    def __str__(self):
        return f"{self.public_id} on {self.assignment.public_id}"

    def export(self):
        base = {"item_id": self.item.item_id} if self.item_id else {}
        out = [{"message_id": self.public_id, "author": "contributor", "text": self.text,
                "created_at": self.created_at.isoformat().replace("+00:00", "Z"), **base}]
        if self.answer.strip() and self.answered_at:
            out.append({"message_id": f"{self.public_id}-a", "author": "team", "text": self.answer.strip(),
                        "created_at": self.answered_at.isoformat().replace("+00:00", "Z"), **base})
        return out


class Confirmation(models.Model):
    """A numbered version of the contributor's review (MVP §3 step 6): the reviews and proposals
    exactly as confirmed, and their SHA-256."""

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="confirmations")
    version = models.PositiveIntegerField()
    confirmed_at = models.DateTimeField(auto_now_add=True)
    content = models.JSONField()
    content_sha256 = models.CharField(max_length=64)

    class Meta:
        unique_together = [("assignment", "version")]
        ordering = ["assignment", "version"]

    def __str__(self):
        return f"{self.assignment.public_id} version {self.version}"
