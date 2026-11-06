"""Tests for the contributor-interface schemas and checks (MVP proposal v0.2).

Run from the repository root:  python3 tests/schema/test_contributor_interface.py
Requires: jsonschema>=4.18. Examples are synthetic; no example-package content is used.
"""
import copy
import json
import pathlib
import sys

from jsonschema import Draft202012Validator, FormatChecker

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas" / "contributor-interface"
sys.path.insert(0, str(ROOT / "validation"))
import rubric_checks as rc  # noqa: E402

NAMES = ["rubric-import", "paper-config", "contributor-review", "submission-manifest"]


def load(name):
    return json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))


def example(name):
    return json.loads((SCHEMAS / "examples" / f"{name}.example.json").read_text(encoding="utf-8"))


def valid(name, inst):
    return Draft202012Validator(load(name), format_checker=FormatChecker()).is_valid(inst)


def test_schemas_are_valid_draft_2020_12():
    for n in NAMES:
        Draft202012Validator.check_schema(load(n))


def test_examples_validate():
    for n in NAMES:
        errors = list(Draft202012Validator(load(n), format_checker=FormatChecker()).iter_errors(example(n)))
        assert not errors, (n, [e.message for e in errors])


def test_example_rubric_is_consistent_and_matches_config():
    r, c = example("rubric-import"), example("paper-config")
    assert rc.check_rubric(r) == []
    assert rc.check_config_against_rubric(c, r) == []


def test_rubric_import_preserves_unknown_fields_and_requires_groups():
    r = example("rubric-import")
    r["some_future_section"] = {"anything": 1}
    r["conceptual"][0]["previous_component_weights_for_history"] = {"x": 2}
    assert valid("rubric-import", r)
    for group in rc.GROUPS:
        bad = example("rubric-import")
        del bad[group]
        assert not valid("rubric-import", bad), group


def test_rubric_items_need_group_specific_description():
    for group, field in [("conceptual", "criterion"), ("missing", "acceptable_work"), ("technical", "repair")]:
        bad = example("rubric-import")
        del bad[group][0][field]
        assert not valid("rubric-import", bad), group
    bad = example("rubric-import")
    del bad["technical"][0]["title"]
    assert not valid("rubric-import", bad)


def test_rubric_consistency_checks_catch_errors():
    r = example("rubric-import")
    r["conceptual"][0]["points"] = 7
    msgs = rc.check_rubric(r)
    assert any("largest allowed score" in m for m in msgs) and any("sum to" in m for m in msgs)
    r = example("rubric-import")
    r["technical"][0]["id"] = "A"
    assert any("duplicate item id" in m for m in rc.check_rubric(r))
    r = example("rubric-import")
    del r["missing"][0]["tiers"]["6"]
    assert any("tier keys" in m for m in rc.check_rubric(r))
    r = example("rubric-import")
    r["technical"][0]["allowed_scores"] = [1, 3]
    assert any("start at 0" in m for m in rc.check_rubric(r))


def test_consistency_messages_never_contain_item_text():
    r = example("rubric-import")
    for g in rc.GROUPS:
        r[g][0]["points"] += 1
    texts = [str(v) for g in rc.GROUPS for it in r[g] for k, v in it.items() if k not in ("id", "points")]
    for m in rc.check_rubric(r):
        assert not any(t in m for t in texts if len(t) > 3), m


def test_contributor_view_shows_only_configured_fields():
    r, c = example("rubric-import"), example("paper-config")
    view = rc.contributor_view(r, c)
    for group in rc.GROUPS:
        allowed = set(c["visible_item_fields"][group]) | {"id", "group", "display_title", "display_description"}
        for item in view[group]:
            assert set(item) <= allowed, (group, set(item) - allowed)
            for hidden in ("points", "tiers", "allowed_scores", "scoring_method", "evidence_record_required"):
                assert hidden not in item
    r["technical"][0]["secret_note"] = "must never show"
    assert "secret_note" not in rc.contributor_view(r, c)["technical"][0]


def test_contributor_view_maps_original_file_names_and_language():
    r, c = example("rubric-import"), example("paper-config")
    en = rc.contributor_view(r, c, "en")
    assert "code/build/panel.do (02_code/example_build_panel.do)" in en["conceptual"][0]["files"]
    assert "display_title" not in en["conceptual"][0]
    zh = rc.contributor_view(r, c, "zh-Hans")
    assert zh["conceptual"][0]["display_title"].startswith("虚构示例")


def test_config_rejects_unknown_fields_and_negative_targets():
    c = example("paper-config")
    c["visible_item_fields"]["technical"].append("secret_answer")
    assert not valid("paper-config", c)
    c = example("paper-config")
    c["group_targets"]["missing"] = -1
    assert not valid("paper-config", c)
    c = example("paper-config")
    c["item_display_text"]["A"]["zh-Hans"]["machine_translated"] = True
    assert not valid("paper-config", c)
    c = example("paper-config")
    c["materials_checklist"][0]["requirement"] = "must"
    assert not valid("paper-config", c)


def test_config_version_must_match_rubric():
    r, c = example("rubric-import"), example("paper-config")
    c["rubric_version"] = "other"
    assert rc.check_config_against_rubric(c, r)
    c = example("paper-config")
    c["paired_variants"] = [{"key_point_id": "kp-1", "item_ids": ["A", "ZZ"]}]
    assert any("unknown item ZZ" in m for m in rc.check_config_against_rubric(c, r))


def test_review_rules():
    base = example("contributor-review")
    bad = copy.deepcopy(base)
    bad["reviews"][2]["reject_reason"] = "other"          # reason only with a rejection
    assert not valid("contributor-review", bad)
    bad = copy.deepcopy(base)
    bad["reviews"][0] = {"item_id": "A", "group": "conceptual", "verdict": "keep_with_changes", "updated_at": "2026-11-10T09:00:00Z"}
    assert not valid("contributor-review", bad)            # changes need some text
    bad = copy.deepcopy(base)
    bad["reviews"][0]["verdict"] = "approve"
    assert not valid("contributor-review", bad)
    bad = copy.deepcopy(base)
    bad["invitation_token"] = "abc"
    assert not valid("contributor-review", bad)            # no credentials in exports
    ok = copy.deepcopy(base)
    ok["reviews"][1].pop("reject_reason")
    assert valid("contributor-review", ok)                 # a rejection reason is optional


def test_submission_rules():
    base = example("submission-manifest")
    bad = copy.deepcopy(base)
    bad["files"] = []
    assert not valid("submission-manifest", bad)
    bad = copy.deepcopy(base)
    bad["files"][0]["sha256"] = "XYZ"
    assert not valid("submission-manifest", bad)
    bad = copy.deepcopy(base)
    bad["no_data_declaration"] = False
    assert not valid("submission-manifest", bad)
    pub = copy.deepcopy(base)
    pub["channel"] = "public_reference"
    del pub["files"]
    assert not valid("submission-manifest", pub)
    pub["public_reference"] = {"repository": "example-archive", "identifier": "000000", "version": "V1"}
    assert valid("submission-manifest", pub)
    other = copy.deepcopy(base)
    other["channel"] = "other_agreed"
    del other["files"]
    assert not valid("submission-manifest", other)
    other["other_channel_note"] = "Delivered on an institutional drive; checksums recorded by the team."
    assert valid("submission-manifest", other)


if __name__ == "__main__":
    tests = [f for name, f in sorted(globals().items()) if name.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print(f"{len(tests)} tests passed")
