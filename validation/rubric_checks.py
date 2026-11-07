"""Checks and views for the contributor interface (MVP proposal v0.3).

The team's rubric is imported as it is. Its item categories differ by field (V5 has
conceptual / missing / technical; a theory paper may have derivation errors), so the paper
configuration declares, per category, which rubric array holds the items and which item
fields fill each display role.

normalize(rubric, config)            -> (items, problems)
check_rubric(rubric, config)         -> problems  (structure, IDs, scores, total)
check_item_map(item_map, items)      -> problems  (nodes, edges, anchors, pairs)
contributor_view(items, config, item_map) -> {category_id: [item views]}
map_view(item_map, items, statuses)  -> nodes with item markers (the "whole picture")
localize(text, language)             -> interface text in a language, falling back to English

Item text is shown in its original language and never translated (D-030); only interface
text (category labels, checklist entries, node labels) is localized.

Problem messages contain category IDs, item IDs, node IDs and field names only, never item
text. Standard library only.
"""
import re

# Item IDs as the item-map and contributor-review schemas accept them.
ITEM_ID = re.compile(r"[A-Za-z0-9_.-]{1,16}")

ROLE_FROM_MAP = ("summary", "change", "affected_results", "consequence")


def _as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def normalize(rubric, config):
    """Build the site's internal item list from the team's rubric and the category profile."""
    items, problems = [], []
    for cat in config["categories"]:
        arr = rubric.get(cat["source_array"])
        if not isinstance(arr, list):
            problems.append(f"category {cat['id']}: rubric has no item array '{cat['source_array']}'")
            continue
        roles = cat["field_roles"]
        for raw in arr:
            if not isinstance(raw, dict):
                problems.append(f"category {cat['id']}: an item is not an object")
                continue
            iid = raw.get("id")
            if not iid:
                problems.append(f"category {cat['id']}: an item has no id")
                continue
            if not isinstance(iid, str) or not ITEM_ID.fullmatch(iid):
                problems.append(f"category {cat['id']}: item id {iid!r} must be 1-16 letters, digits, '.', '_' or '-'")
                continue
            item = {"id": iid, "category": cat["id"], "raw": raw}
            if roles["title"] not in raw:
                problems.append(f"{cat['id']} {iid}: missing title field '{roles['title']}'")
            item["title"] = raw.get(roles["title"])
            if "points" in roles:
                pts = raw.get(roles["points"])
                if isinstance(pts, bool) or not isinstance(pts, (int, float)):
                    problems.append(f"{cat['id']} {iid}: points field '{roles['points']}' is missing or not a number")
                    pts = None
                item["points"] = pts
            for role in ("locations", "description", "acceptable_answer"):
                fields = roles.get(role, [])
                present = [f for f in fields if f in raw]
                if fields and not present:
                    problems.append(f"{cat['id']} {iid}: none of the {role} fields {fields} present")
                item[role] = [{"field": f, "value": raw[f]} for f in present]
            if "critical_requirements" in roles:
                item["critical_requirements"] = _as_list(raw.get(roles["critical_requirements"]))
            items.append(item)
    return items, problems


def check_rubric(rubric, config):
    items, problems = normalize(rubric, config)
    seen = set()
    # The sum is checked only when every category declares a points field.
    total, have_points = 0, all("points" in c["field_roles"] for c in config["categories"])
    for it in items:
        cat, iid, raw = it["category"], it["id"], it["raw"]
        if iid in seen:
            problems.append(f"duplicate item id {iid}")
        seen.add(iid)
        pts = it.get("points")
        if pts is not None:
            total += pts
        scores = raw.get("allowed_scores")
        if scores and pts is not None:
            if max(scores) != pts:
                problems.append(f"{cat} {iid}: points differ from the largest allowed score")
            if min(scores) != 0:
                problems.append(f"{cat} {iid}: allowed scores do not start at 0")
            if scores != sorted(set(scores)):
                problems.append(f"{cat} {iid}: allowed scores are not strictly increasing")
            tiers = raw.get("tiers")
            if isinstance(tiers, dict) and sorted(int(k) for k in tiers) != sorted(scores):
                problems.append(f"{cat} {iid}: tier keys differ from the allowed scores")
    if have_points and "maximum" in rubric and total != rubric["maximum"]:
        problems.append(f"item points sum to {total}, not the maximum {rubric['maximum']}")
    if config.get("rubric_version") != rubric.get("version"):
        problems.append("configuration rubric_version differs from the rubric version")
    return problems


def check_item_map(item_map, items):
    problems = []
    nodes = [n["id"] for n in item_map["nodes"]]
    node_set = set(nodes)
    if len(nodes) != len(node_set):
        problems.append("duplicate node id")
    for n in item_map["nodes"]:
        if n.get("parent") and n["parent"] not in node_set:
            problems.append(f"node {n['id']}: unknown parent {n['parent']}")
    for e in item_map.get("edges", []):
        for end in (e["from"], e["to"]):
            if end not in node_set:
                problems.append(f"edge refers to unknown node {end}")
    ids = {it["id"] for it in items}
    for iid, ov in item_map["items"].items():
        if iid not in ids:
            problems.append(f"item map entry for unknown item {iid}")
        for nid in ov.get("anchors", []) + ov.get("affected_results", []):
            if nid not in node_set:
                problems.append(f"item {iid}: unknown node {nid}")
        pw = ov.get("paired_with")
        if pw and (pw not in ids or item_map["items"].get(pw, {}).get("paired_with") != iid):
            problems.append(f"item {iid}: pairing with {pw} is not mutual")
    for it in items:
        if it["id"] not in item_map["items"]:
            problems.append(f"item {it['id']} is not placed on the map")
    return problems


def _map_path(text, file_map):
    if not isinstance(text, str) or not file_map:
        return text
    for cand, orig in file_map.items():
        text = text.replace(cand, f"{orig} ({cand})")
    return text


def localize(text, language):
    """Interface text (a {language tag: string} object) in the requested language,
    falling back to the base language and then to English."""
    if language in text:
        return text[language]
    base = language.split("-")[0]
    for tag, value in text.items():
        if tag.split("-")[0] == base:
            return value
    return text["en"]


def contributor_view(items, config, item_map=None):
    """What a contributor may see, per category. Only configured roles appear; rubric
    fields not mapped to a visible role never appear. Item text stays in its original
    language (D-030)."""
    file_map = {m["candidate_path"]: m["original_path"] for m in config.get("file_name_map", [])}
    overlays = (item_map or {}).get("items", {})
    cats = {c["id"]: c for c in config["categories"]}
    view = {cid: [] for cid in cats}
    for it in items:
        cat = cats[it["category"]]
        visible = set(cat["visible_roles"])
        v = {"id": it["id"], "category": it["category"]}
        if "title" in visible:
            v["title"] = it["title"]
        if "weight" in visible and it.get("points") is not None:
            v["weight"] = it["points"]
        if "locations" in visible:
            v["locations"] = [_map_path(x["value"], file_map) for x in it["locations"]]
        for role in ("description", "acceptable_answer"):
            if role in visible and it[role]:
                v[role] = [x["value"] for x in it[role]]
        if "critical_requirements" in visible and it.get("critical_requirements"):
            v["critical_requirements"] = it["critical_requirements"]
        ov = overlays.get(it["id"], {})
        for role in ROLE_FROM_MAP:
            if role in visible and role in ov:
                v[role] = ov[role]
        if "change" in v:
            ch = v["change"]
            v["change"] = {**ch, "original": {**ch["original"], "path": _map_path(ch["original"].get("path"), file_map)}}
        if ov.get("paired_with"):
            v["paired_with"] = ov["paired_with"]
        view[it["category"]].append(v)
    return view


def map_view(item_map, items, statuses=None):
    """The whole-picture pane: every node with markers for the items anchored to it and
    for the items that affect it (results). Markers carry only ID, category and status."""
    statuses = statuses or {}
    cat_of = {it["id"]: it["category"] for it in items}
    nodes = []
    for n in sorted(item_map["nodes"], key=lambda n: (n.get("order", 0), n["id"])):
        here, affecting = [], []
        for iid, ov in item_map["items"].items():
            if iid not in cat_of:
                continue
            marker = {"item_id": iid, "category": cat_of[iid], "status": statuses.get(iid, "not_reviewed")}
            if n["id"] in ov.get("anchors", []):
                here.append(marker)
            if n["id"] in ov.get("affected_results", []):
                affecting.append(marker)
        nodes.append({"id": n["id"], "kind": n["kind"], "label": n["label"], "parent": n.get("parent"),
                      "items_here": here, "affected_by": affecting})
    return {"nodes": nodes, "edges": item_map.get("edges", [])}
