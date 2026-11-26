"""Selection (M2): the review of one assignment's prepared items.

Kept apart from the views so the rules are tested once:
- what a contributor may see of each item (the paper's configured roles only);
- saving an answer with an optimistic version, so a stale page never overwrites silently;
- confirmations as numbered versions with the SHA-256 of what was confirmed;
- the export, validated against contributor-review.schema.json;
- the checks that must pass before the team freezes a review (D-049).
"""
import hashlib
import json

from django.db import transaction
from django.utils import timezone

from papers.importers import _validator, rubric_checks

from .models import Confirmation, ItemReview

MINUTES_PER_ITEM = 2.5      # MVP §3 step 3: "about 2–3 minutes per item" [U: to be measured]


class Conflict(Exception):
    """The page was out of date: someone (another tab) saved this item since it was loaded."""

    def __init__(self, review):
        super().__init__(review.version)
        self.review = review


class Frozen(Exception):
    """The team has frozen this review; nothing can change until it is unfrozen."""


def interface_tag(language_code):
    return "zh-Hans" if (language_code or "").lower() == "zh-hans" else (language_code or "en")


def paper_items(paper):
    """The current rubric's items in rubric order, or [] if no rubric is imported."""
    rubric = paper.current_rubric()
    return list(rubric.items.order_by("position")) if rubric else []


def item_map_for(paper):
    rubric = paper.current_rubric()
    item_map = rubric.item_maps.first() if rubric else None
    return item_map.raw if item_map else None


def colours(paper):
    """A colour slot (0 to 5) per category, by its order in the paper configuration (D-025)."""
    return {c["id"]: i % 6 for i, c in enumerate(paper.config["categories"])}


def item_views(paper, language="en"):
    """{item_id: what the contributor may see}, using only the configured visible roles."""
    rc = rubric_checks()
    items = paper_items(paper)
    normalized = [it.normalized for it in items]
    grouped = rc.contributor_view(normalized, paper.config, item_map_for(paper))
    labels = {c["id"]: rc.localize(c["label"], language) for c in paper.config["categories"]}
    nodes = {n["id"]: rc.localize(n["label"], language) for n in (item_map_for(paper) or {}).get("nodes", [])}
    palette = colours(paper)
    views = {}
    for category_items in grouped.values():
        for v in category_items:
            v["colour"] = palette.get(v["category"], 0)
            v["category_label"] = labels.get(v["category"], v["category"])
            v["affected_result_labels"] = [nodes.get(r, r) for r in v.get("affected_results", [])]
            views[v["id"]] = v
    return views


def reviews_by_item(assignment):
    return {r.item.item_id: r for r in assignment.reviews.select_related("item")}


def progress(assignment):
    items = paper_items(assignment.paper)
    done = assignment.reviews.filter(item__in=items).count()
    left = len(items) - done
    return {"reviewed": done, "total": len(items), "minutes_left": round(left * MINUTES_PER_ITEM)}


def map_for(assignment, language="en"):
    """The whole-picture pane, with each marker's review status, or None without an item map."""
    item_map = item_map_for(assignment.paper)
    if item_map is None:
        return None
    rc = rubric_checks()
    statuses = {iid: r.verdict for iid, r in reviews_by_item(assignment).items()}
    view = rc.map_view(item_map, [it.normalized for it in paper_items(assignment.paper)], statuses)
    palette = colours(assignment.paper)
    for node in view["nodes"]:
        node["label_text"] = rc.localize(node["label"], language)
        for marker in node["items_here"] + node["affected_by"]:
            marker["colour"] = palette.get(marker["category"], 0)
            marker["done"] = marker["status"] != "not_reviewed"
    # A stage whose children are all results (e.g. "Results in the paper") names the results
    # column instead of appearing as an empty stage in the workflow.
    children = {}
    for node in view["nodes"]:
        if node["parent"]:
            children.setdefault(node["parent"], []).append(node)
    view["results_heading"] = None
    for node in view["nodes"]:
        kids = children.get(node["id"], [])
        node["hidden"] = bool(node["affected_by"]) or (bool(kids) and all(k["affected_by"] for k in kids))
        if kids and all(k["affected_by"] for k in kids) and view["results_heading"] is None:
            view["results_heading"] = node["label_text"]
    return view


def neighbours(items, item_id):
    ids = [it.item_id for it in items]
    i = ids.index(item_id)
    return (ids[i - 1] if i > 0 else None), (ids[i + 1] if i + 1 < len(ids) else None)


@transaction.atomic
def save_review(assignment, item, data, expected_version):
    """Create or update one answer. `expected_version` is the version the page was loaded with
    (0 for an item never answered). Raises Conflict if it is out of date, Frozen if frozen."""
    if assignment.is_frozen:
        raise Frozen()
    review = ItemReview.objects.select_for_update().filter(assignment=assignment, item=item).first()
    current = review.version if review else 0
    if expected_version != current:
        raise Conflict(review)
    if review is None:
        review = ItemReview(assignment=assignment, item=item, version=0)
    for field, value in data.items():
        setattr(review, field, value)
    if review.verdict != "reject":
        review.reject_reason = ""
    if not review.ai_used:
        review.ai_tool, review.ai_account_kind, review.ai_entered_items = "", "", None
    review.version = current + 1
    review.save()
    return review


def snapshot(assignment):
    """The reviews and proposals as they stand, in the export's form."""
    return {
        "reviews": [r.export() for r in assignment.reviews.select_related("item").order_by("item__position")],
        "proposals": [p.export() for p in assignment.proposals.all()],
    }


def content_sha256(content):
    canonical = json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@transaction.atomic
def confirm(assignment):
    """Create the next numbered version. Raises Frozen if the team has frozen the review."""
    if assignment.is_frozen:
        raise Frozen()
    content = snapshot(assignment)
    last = assignment.confirmations.select_for_update().order_by("-version").first()
    return Confirmation.objects.create(assignment=assignment, version=(last.version + 1) if last else 1,
                                       content=content, content_sha256=content_sha256(content))


def export(assignment):
    """The contributor review in contributor-review.schema.json form, validated before it is returned."""
    paper = assignment.paper
    content = snapshot(assignment)
    reviewed = {r["item_id"] for r in content["reviews"]}
    for item in paper_items(paper):
        if item.item_id not in reviewed:
            content["reviews"].append({"item_id": item.item_id, "category": item.category, "verdict": "not_reviewed",
                                       "updated_at": timezone.now().isoformat().replace("+00:00", "Z")})
    consent = assignment.latest_consent()
    data = {
        "schema_version": "0.3.0",
        "paper_id": paper.paper_id,
        "assignment_id": assignment.public_id,
        "contributor_id": assignment.contributor.public_id,
        "relationship_to_paper": assignment.relationship_to_paper,
        "language": interface_tag(assignment.contributor.preferred_language),
        "rubric_version": paper.config["rubric_version"],
        "reviews": content["reviews"],
        "proposals": content["proposals"],
        "confirmations": [{"version": c.version, "confirmed_at": c.confirmed_at.isoformat().replace("+00:00", "Z"),
                           "content_sha256": c.content_sha256} for c in assignment.confirmations.all()],
        "frozen": assignment.is_frozen,
        "messages": [m for q in assignment.questions.select_related("item") for m in q.export()],
    }
    if paper.config.get("candidate_version"):
        data["candidate_version"] = paper.config["candidate_version"]
    if assignment.frozen_at:
        data["frozen_at"] = assignment.frozen_at.isoformat().replace("+00:00", "Z")
    if consent:
        data["consent"] = {"evaluation_through_apis_acknowledged": True,
                           "team_ai_use_of_unpublished_material": consent.team_ai_use_of_unpublished_material,
                           "notice_version": consent.notice_version,
                           "recorded_at": consent.recorded_at.isoformat().replace("+00:00", "Z")}
    errors = sorted(_validator("contributor-review").iter_errors(data), key=lambda e: list(e.absolute_path))
    if errors:
        where = ["/".join(str(p) for p in e.absolute_path) or "(top level)" for e in errors[:10]]
        raise ValueError(f"export fails contributor-review.schema.json at: {', '.join(where)}")
    return data


def freeze_problems(assignment):
    """(blocking, warnings) before the team freezes a review (D-049)."""
    paper = assignment.paper
    blocking, warnings = [], []
    if paper.built_on is None:
        blocking.append("the paper has no task build date (Rule 10)")
    missing = [it.item_id for it in paper_items(paper) if not it.origin]
    if missing:
        blocking.append(f"items without provenance (import the item map): {', '.join(missing)}")
    prog = progress(assignment)
    if prog["reviewed"] < prog["total"]:
        warnings.append(f"{prog['total'] - prog['reviewed']} of {prog['total']} items are not answered")
    if not assignment.confirmations.exists():
        warnings.append("the contributor has not confirmed a version")
    return blocking, warnings
