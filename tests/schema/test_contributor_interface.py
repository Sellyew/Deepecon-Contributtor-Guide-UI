"""Tests for the contributor-interface schemas and checks (MVP proposal v0.3).

Run from the repository root:  python3 tests/schema/test_contributor_interface.py
Requires: jsonschema>=4.18. All examples are synthetic and marked fictional; no example-package
content is used. Two fields are covered: an empirical paper (V5-style categories) and a theory
paper (different categories), because item categories and points differ by field.
"""
import copy
import json
import pathlib
import sys

from jsonschema import Draft202012Validator, FormatChecker

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas" / "contributor-interface"
EX = SCHEMAS / "examples"
sys.path.insert(0, str(ROOT / "validation"))
import rubric_checks as rc  # noqa: E402

SCHEMA_FOR = {"rubric": "rubric-import", "paper-config": "paper-config", "item-map": "item-map",
              "contributor-review": "contributor-review", "submission-manifest": "submission-manifest"}


def schema(name):
    return json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))


def ex(field, name):
    return json.loads((EX / field / f"{name}.json").read_text(encoding="utf-8"))


def valid(name, inst):
    return Draft202012Validator(schema(name), format_checker=FormatChecker()).is_valid(inst)


def bundle(field):
    r, c, m = ex(field, "rubric"), ex(field, "paper-config"), ex(field, "item-map")
    items, problems = rc.normalize(r, c)
    assert problems == [], problems
    return r, c, m, items


def test_schemas_are_valid_draft_2020_12():
    for name in set(SCHEMA_FOR.values()):
        Draft202012Validator.check_schema(schema(name))


def test_examples_validate():
    for field in ("empirical", "theory"):
        for f in sorted((EX / field).glob("*.json")):
            name = SCHEMA_FOR[f.stem]
            errors = list(Draft202012Validator(schema(name), format_checker=FormatChecker()).iter_errors(json.loads(f.read_text(encoding="utf-8"))))
            assert not errors, (f.name, [e.message for e in errors])


def test_examples_are_consistent():
    for field in ("empirical", "theory"):
        r, c, m, items = bundle(field)
        assert rc.check_rubric(r, c) == [], field
        assert rc.check_item_map(m, items) == [], field


def test_categories_are_configurable_per_field():
    _, _, _, emp = bundle("empirical")
    _, _, _, th = bundle("theory")
    assert {i["category"] for i in emp} == {"conceptual", "missing", "technical"}
    assert {i["category"] for i in th} == {"derivation", "assumption", "proof-gap"}


def test_normalize_reports_missing_arrays_and_fields():
    r, c = ex("theory", "rubric"), ex("theory", "paper-config")
    del r["proof_gaps"]
    assert any("no item array 'proof_gaps'" in p for p in rc.normalize(r, c)[1])
    r = ex("empirical", "rubric")
    del r["technical"][0]["repair"]
    assert any("T01: none of the description fields" in p for p in rc.normalize(r, ex("empirical", "paper-config"))[1])


def test_rubric_consistency_checks_catch_errors():
    c = ex("empirical", "paper-config")
    r = ex("empirical", "rubric")
    r["conceptual"][0]["points"] = 7
    msgs = rc.check_rubric(r, c)
    assert any("largest allowed score" in m for m in msgs) and any("sum to" in m for m in msgs)
    r = ex("empirical", "rubric")
    r["technical"][0]["id"] = "A"
    assert any("duplicate item id" in m for m in rc.check_rubric(r, c))
    r = ex("empirical", "rubric")
    del r["missing"][0]["tiers"]["6"]
    assert any("tier keys" in m for m in rc.check_rubric(r, c))
    c2 = copy.deepcopy(c)
    c2["rubric_version"] = "other"
    assert any("rubric_version" in m for m in rc.check_rubric(ex("empirical", "rubric"), c2))


def test_messages_never_contain_item_text():
    r, c = ex("empirical", "rubric"), ex("empirical", "paper-config")
    for g in ("conceptual", "missing", "technical"):
        r[g][0]["points"] += 1
    texts = [v for g in ("conceptual", "missing", "technical") for it in r[g] for k, v in it.items() if isinstance(v, str) and k != "id" and len(v) > 3]
    for msg in rc.check_rubric(r, c):
        assert not any(t in msg for t in texts), msg


def test_item_map_checks():
    _, _, m, items = bundle("empirical")
    bad = copy.deepcopy(m)
    bad["items"]["A"]["anchors"] = ["nowhere"]
    assert any("unknown node nowhere" in p for p in rc.check_item_map(bad, items))
    bad = copy.deepcopy(m)
    del bad["items"]["T01"]
    assert any("T01 is not placed on the map" in p for p in rc.check_item_map(bad, items))
    bad = copy.deepcopy(m)
    bad["items"]["A"]["paired_with"] = "M1"
    assert any("not mutual" in p for p in rc.check_item_map(bad, items))
    bad["items"]["M1"]["paired_with"] = "A"
    assert not any("not mutual" in p for p in rc.check_item_map(bad, items))


def test_contributor_view_shows_only_configured_roles():
    r, c, m, items = bundle("empirical")
    r["technical"][0]["secret_note"] = "must never show"
    items, _ = rc.normalize(r, c)
    view = rc.contributor_view(items, c, m)
    allowed = {"id", "category", "paired_with"} | set(rc.ROLE_FROM_MAP) | {
        "title", "weight", "locations", "description", "acceptable_answer", "critical_requirements"}
    flat = json.dumps(view, ensure_ascii=False)
    for word in ("tiers", "allowed_scores", "scoring_method", "evidence_record_required", "must never show", "Fictional example; not calibrated"):
        assert word not in flat, word
    for cat, entries in view.items():
        for v in entries:
            assert set(v) <= allowed, set(v) - allowed
            assert "weight" not in v          # weight is not in the default visible roles
    c2 = copy.deepcopy(c)
    c2["categories"][0]["visible_roles"].append("weight")
    assert rc.contributor_view(items, c2, m)["conceptual"][0]["weight"] == 8


def test_whole_picture_and_local_change():
    _, c, m, items = bundle("empirical")
    v = rc.contributor_view(items, c, m)["conceptual"][0]
    assert v["change"]["original"]["path"] == "code/build/panel.do (02_code/example_build_panel.do)"
    assert v["affected_results"] == ["r-table2"]
    mv = rc.map_view(m, items, {"A": "keep"})
    node = {n["id"]: n for n in mv["nodes"]}
    assert [x["item_id"] for x in node["f-panel"]["items_here"]] == ["A"]
    assert node["f-panel"]["items_here"][0]["status"] == "keep"
    assert {x["item_id"] for x in node["r-table2"]["affected_by"]} == {"A", "T01"}
    for n in mv["nodes"]:
        for mk in n["items_here"] + n["affected_by"]:
            assert set(mk) == {"item_id", "category", "status"}


def test_original_file_names_are_shown():
    _, c, m, items = bundle("empirical")
    v = rc.contributor_view(items, c, m)["technical"][0]
    assert v["locations"] == ["code/build/registry_merge.do (02_code/example_merge_registry.do)"]


def test_item_text_stays_in_original_language():
    _, c, m, items = bundle("empirical")
    view = rc.contributor_view(items, c, m)
    assert view["conceptual"][0]["title"].startswith("FICTIONAL")
    assert "translation" not in json.dumps(view)
    bad = copy.deepcopy(c)
    bad["translations"] = {"A": {"zh-Hans": {"title": "x"}}}
    assert not valid("paper-config", bad)              # no item-translation channel exists


def test_interface_text_supports_more_languages():
    c = ex("empirical", "paper-config")
    c["languages"] = ["zh-Hans", "en", "es"]
    c["categories"][0]["label"]["es"] = "Error conceptual (ejemplo)"
    assert valid("paper-config", c)
    label = c["categories"][0]["label"]
    assert rc.localize(label, "es") == "Error conceptual (ejemplo)"
    assert rc.localize(label, "zh-Hans") == "学理错误"
    assert rc.localize(label, "zh") == "学理错误"      # base-language fallback
    assert rc.localize(label, "fr") == "Conceptual error"
    bad = copy.deepcopy(c)
    bad["languages"] = ["Chinese"]
    assert not valid("paper-config", bad)


def test_config_rejects_unknown_roles_and_fields():
    c = ex("empirical", "paper-config")
    c["categories"][0]["visible_roles"].append("tiers")
    assert not valid("paper-config", c)
    c = ex("empirical", "paper-config")
    c["categories"][0]["field_roles"]["answer_key"] = "tiers"
    assert not valid("paper-config", c)
    c = ex("empirical", "paper-config")
    c["categories"][0]["target"] = -1
    assert not valid("paper-config", c)


def test_review_rules():
    base = ex("empirical", "contributor-review")
    bad = copy.deepcopy(base)
    bad["reviews"][2]["reject_reason"] = "other"
    assert not valid("contributor-review", bad)
    bad = copy.deepcopy(base)
    bad["reviews"][0] = {"item_id": "A", "category": "conceptual", "verdict": "keep_with_changes", "updated_at": "2026-11-10T09:00:00Z"}
    assert not valid("contributor-review", bad)
    bad = copy.deepcopy(base)
    bad["invitation_token"] = "abc"
    assert not valid("contributor-review", bad)
    ok = copy.deepcopy(base)
    ok["reviews"][1].pop("reject_reason")
    ok["reviews"][1]["category"] = "proof-gap"            # categories are not fixed
    assert valid("contributor-review", ok)


def test_submission_requires_a_runnable_description_and_data_routes():
    base = ex("empirical", "submission-manifest")
    bad = copy.deepcopy(base)
    del bad["package"]["master_script"]
    assert not valid("submission-manifest", bad)
    bad = copy.deepcopy(base)
    del bad["datasets"][1]["access_route"]               # restricted data need a route
    assert not valid("submission-manifest", bad)
    bad = copy.deepcopy(base)
    del bad["declarations"]["permission_to_share_included_data"]   # included data need permission
    assert not valid("submission-manifest", bad)
    bad = copy.deepcopy(base)
    bad["declarations"]["no_restricted_or_confidential_data_included"] = False
    assert not valid("submission-manifest", bad)
    ok = copy.deepcopy(base)
    ok["datasets"] = [ok["datasets"][1]]
    del ok["declarations"]["permission_to_share_included_data"]    # nothing included, nothing to permit
    assert valid("submission-manifest", ok)
    pub = copy.deepcopy(base)
    pub["channel"] = "public_reference"
    del pub["files"]
    assert not valid("submission-manifest", pub)
    pub["public_reference"] = {"repository": "example-archive", "identifier": "000000", "version": "V1"}
    assert valid("submission-manifest", pub)
    bad = copy.deepcopy(base)
    bad["datasets"][0]["availability"] = "public_elsewhere"
    assert not valid("submission-manifest", bad)         # needs where


if __name__ == "__main__":
    tests = [f for name, f in sorted(globals().items()) if name.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print(f"{len(tests)} tests passed")
