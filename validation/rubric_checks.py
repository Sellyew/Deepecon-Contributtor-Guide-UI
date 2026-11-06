"""Checks and views for the contributor interface (MVP proposal v0.2, §5 and §7).

check_rubric(rubric)              -> list of problems (item IDs and field names only, never item text)
check_config_against_rubric(c, r) -> list of problems
contributor_view(rubric, config, language="en") -> what a contributor may see, per group

Standard library only. The rubric is the team's V5-format file; see
schemas/contributor-interface/rubric-import.schema.json.
"""
GROUPS = ("conceptual", "missing", "technical")
# Description fields per group (V5 format); shown only if the configuration lists them.
DESCRIPTION_FIELDS = {
    "conceptual": ("criterion",),
    "missing": ("available_evidence_and_boundary", "acceptable_work"),
    "technical": ("repair",),
}
LOCATION_FIELDS = ("files", "file")


def check_rubric(rubric):
    problems = []
    seen = set()
    total = 0
    for group in GROUPS:
        for item in rubric.get(group, []):
            iid = item.get("id", "?")
            if iid in seen:
                problems.append(f"duplicate item id {iid}")
            seen.add(iid)
            points = item.get("points", 0)
            total += points
            scores = item.get("allowed_scores")
            if scores:
                if max(scores) != points:
                    problems.append(f"{group} {iid}: points differ from the largest allowed score")
                if min(scores) != 0:
                    problems.append(f"{group} {iid}: allowed scores do not start at 0")
                if scores != sorted(set(scores)):
                    problems.append(f"{group} {iid}: allowed scores are not strictly increasing")
                tiers = item.get("tiers")
                if tiers is not None and sorted(int(k) for k in tiers) != sorted(scores):
                    problems.append(f"{group} {iid}: tier keys differ from the allowed scores")
    if "maximum" in rubric and total != rubric["maximum"]:
        problems.append(f"item points sum to {total}, not the maximum {rubric['maximum']}")
    return problems


def check_config_against_rubric(config, rubric):
    problems = []
    if config.get("rubric_version") != rubric.get("version"):
        problems.append("configuration rubric_version differs from the imported rubric version")
    ids = {item.get("id") for g in GROUPS for item in rubric.get(g, [])}
    for iid in config.get("item_display_text", {}):
        if iid not in ids:
            problems.append(f"display text for unknown item {iid}")
    for pair in config.get("paired_variants", []):
        for iid in pair["item_ids"]:
            if iid not in ids:
                problems.append(f"paired variant refers to unknown item {iid}")
    return problems


def _map_location(value, file_map):
    if not value or not file_map:
        return value
    out = value
    for cand, orig in file_map.items():
        out = out.replace(cand, f"{orig} ({cand})")
    return out


def contributor_view(rubric, config, language="en"):
    """Return {group: [item views]} with only the configured fields.

    Fields not listed in config['visible_item_fields'][group] never appear, whatever the
    rubric contains (points, tiers, scoring methods, unknown fields)."""
    file_map = {m["candidate_path"]: m["original_path"] for m in config.get("file_name_map", [])}
    display = config.get("item_display_text", {})
    view = {}
    for group in GROUPS:
        visible = set(config["visible_item_fields"][group])
        items = []
        for item in rubric.get(group, []):
            v = {"id": item["id"], "group": group}
            for field in visible:
                if field in item and field != "id":
                    value = item[field]
                    if field in LOCATION_FIELDS:
                        value = _map_location(value, file_map)
                    v[field] = value
            text = display.get(item["id"], {}).get(language)
            if text:
                v["display_title"] = text["title"]
                if "description" in text:
                    v["display_description"] = text["description"]
            items.append(v)
        view[group] = items
    return view
