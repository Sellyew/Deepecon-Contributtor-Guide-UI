"""Schema tests for the DeepEcon contribution package (Deliverable 4).

Run from the repository root:  python3 -m pytest tests/schema  (or)  python3 tests/schema/test_schema.py
Requires: jsonschema>=4.18, PyYAML.
"""
import copy
import datetime
import json
import pathlib

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "schemas" / "deepecon-contribution.schema.json").read_text())
EXAMPLES = sorted((ROOT / "schemas" / "examples").glob("*.yaml"))


def _normalize(obj):
    """YAML parses timestamps into datetime objects; JSON carries them as strings."""
    if isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_normalize(v) for v in obj]
    if isinstance(obj, datetime.datetime):
        return obj.isoformat().replace("+00:00", "Z")
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    return obj


def _validator():
    return Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def _example():
    return _normalize(yaml.safe_load(EXAMPLES[0].read_text()))


def test_schema_is_valid_draft_2020_12():
    Draft202012Validator.check_schema(SCHEMA)


def test_examples_validate():
    assert EXAMPLES, "no example instances found"
    v = _validator()
    for path in EXAMPLES:
        errors = list(v.iter_errors(_normalize(yaml.safe_load(path.read_text()))))
        assert not errors, f"{path.name}: {[e.message for e in errors]}"


def test_rejects_restricted_microdata_in_submission():
    inst = _example()
    inst["submission"] = {
        "submission_id": "s1", "channel": "email", "submitted_at": "2026-11-05T12:00:00Z",
        "package_sha256": "a" * 64, "contains_restricted_microdata": True, "licenses_confirmed": True,
    }
    assert not _validator().is_valid(inst)


def test_rejects_llm_origin_without_model():
    inst = _example()
    inst["failure_modes"][0]["description"]["provenance"].pop("model")
    assert not _validator().is_valid(inst)


def test_rejects_two_original_texts():
    inst = _example()
    inst["target_analyses"][0]["description"][1]["is_original"] = True
    assert not _validator().is_valid(inst)


def test_rejects_mislabelled_agent_tier():
    inst = _example()
    inst["task_candidates"][0]["agent_facing"]["visibility"] = "hidden"
    assert not _validator().is_valid(inst)


def test_rejects_failure_mode_outside_hidden_tier():
    inst = _example()
    inst["failure_modes"][0]["visibility"] = "agent"
    assert not _validator().is_valid(inst)


if __name__ == "__main__":
    tests = [f for name, f in sorted(globals().items()) if name.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
