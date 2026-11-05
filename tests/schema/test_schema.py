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



def test_rejects_failure_mode_without_observed_in_practice():
    """Protocol v0.2.0 makes the realism warrant's observed/hypothetical field mandatory (probe P-SEEN)."""
    inst = _example()
    inst["failure_modes"][0]["realism_warrant"].pop("observed_in_practice")
    assert not _validator().is_valid(inst)


def test_rejects_unknown_validity_layer():
    inst = _example()
    inst["failure_modes"][0]["validity_layer"] = "vibes"
    assert not _validator().is_valid(inst)


# --- 0.3.0 constraints -------------------------------------------------------------------

NON_REDISTRIBUTABLE = ["public_not_redistributable", "restricted_access", "confidential"]


def _valid(inst):
    return _validator().is_valid(inst)


def _task(inst):
    return inst["task_candidates"][0]


def _graded(inst):
    return _task(inst)["hidden"]["verifier"]["graded_outputs"]


def _decision_space(inst):
    return _task(inst)["hidden"]["decision_space"]


def _data_file(tier, source_access, data_route):
    return {"path": f"{tier}/data/extra.csv", "visibility": tier, "role": "data",
            "source_access": source_access, "data_route": data_route}


def _run(kind, **fields):
    run = {"run_id": "vr-test", "task_id": "task-ec-01", "kind": kind, "subject": "subject-01",
           "executed_at": "2026-11-05T12:00:00Z", "expected_verdict": "accept",
           "observed": {"n_accept": 1, "n_reject": 0, "n_error": 0}, "visibility": "hidden"}
    run.update(fields)
    return run


def _exposure(**fields):
    entry = {"entry_id": "exp-test", "exposed_at": "2026-11-05T12:00:00Z",
             "material_description": "Answer key of task-ec-01", "material_refs": ["task-ec-01"],
             "service": "API account", "terms": "commercial_no_training_zdr", "visibility": "internal"}
    entry.update(fields)
    return entry


def _interview_record(**fields):
    record = {"session_id": "sess-01", "started_at": "2026-11-05T09:00:00Z", "interface": "human_interviewer",
              "protocol_version": "0.2.1", "model": {"provider": "anthropic", "model_id": "claude-opus-5-5"},
              "language": "en", "turns": [], "visibility": "internal"}
    record.update(fields)
    return record


def _ledger_entry(**fields):
    entry = {"suggestion_id": "sg-01", "offered_at": "2026-11-05T09:30:00Z", "source_entry": "P1",
             "is_known_valid_control": True, "disposition": "endorsed"}
    entry.update(fields)
    return entry


def test_schema_id_and_example_versions_agree():
    version = SCHEMA["$id"].rsplit("/", 1)[-1]
    assert f"draft {version}" in SCHEMA["description"]
    for path in EXAMPLES:
        assert str(yaml.safe_load(path.read_text())["schema_version"]) == version, path.name


def test_accepts_each_verifiability_tier():
    for tier in ["V1", "V2a", "V2b", "V3", "V4"]:
        inst = _example()
        _graded(inst)[0]["verifiability_tier"] = tier
        assert _valid(inst), tier


def test_rejects_undivided_tier_v2():
    """V2 was split into V2a (exact relation) and V2b (stochastic check)."""
    inst = _example()
    _graded(inst)[0]["verifiability_tier"] = "V2"
    assert not _valid(inst)


def test_rejects_task_level_tier_and_requires_graded_outputs():
    """Tiers live on graded outputs; the 0.2.0 task-level field is gone."""
    inst = _example()
    _task(inst)["verifiability_tier"] = "V1"
    assert not _valid(inst)
    inst = _example()
    del _task(inst)["hidden"]["verifier"]["graded_outputs"]
    assert not _valid(inst)
    inst = _example()
    _task(inst)["hidden"]["verifier"]["graded_outputs"] = []
    assert not _valid(inst)


def test_rejects_unknown_graded_quantity():
    inst = _example()
    _graded(inst)[0]["quantity"] = "vibes"
    assert not _valid(inst)


def test_accepts_secondary_layers_and_rejects_unknown_ones():
    inst = _example()
    inst["failure_modes"][0]["secondary_validity_layers"] = ["measurement", "identification"]
    assert _valid(inst)
    inst["failure_modes"][0]["secondary_validity_layers"] = ["vibes"]
    assert not _valid(inst)
    inst["failure_modes"][0]["secondary_validity_layers"] = ["interpretation", "interpretation"]
    assert not _valid(inst)


def test_accepts_changes_inference_only_prediction():
    inst = _example()
    inst["failure_modes"][0]["predicted_consequence"]["category"] = "changes_inference_only"
    assert _valid(inst)
    inst["failure_modes"][0]["predicted_consequence"]["category"] = "vibes"
    assert not _valid(inst)


def test_accepts_standard_error_comparison():
    inst = _example()
    inst["flawed_variants"][0]["consequence"]["comparisons"][0]["quantity"] = "std_error"
    assert _valid(inst)


def test_decision_space_reference_format():
    """References are <decision_id>/<option_id>; whether they resolve is a validator rule (README §5)."""
    for field in ["requires", "excludes"]:
        inst = _example()
        _decision_space(inst)[2][field] = ["cd-parallel-trends/all-years", "cd-other.v2/option_1"]
        assert _valid(inst), field
        for bad in ["none", "cd-anticipation/", "/none", "CD-Anticipation/none", "cd anticipation/none",
                    "cd-anticipation/none/extra", ""]:
            inst = _example()
            _decision_space(inst)[2][field] = [bad]
            assert not _valid(inst), (field, bad)
        inst = _example()
        _decision_space(inst)[2][field] = ["cd-anticipation/none", "cd-anticipation/none"]
        assert not _valid(inst), (field, "duplicate")


def test_rejects_decision_space_option_without_option_id():
    inst = _example()
    del _decision_space(inst)[0]["option_id"]
    assert not _valid(inst)


def test_rejects_non_redistributable_source_in_agent_tier_unless_fully_synthetic():
    for access in NON_REDISTRIBUTABLE:
        for route in ["redistributable_original", "derived_from_redistributable"]:
            inst = _example()
            _task(inst)["agent_facing"]["provided_materials"].append(_data_file("agent", access, route))
            assert not _valid(inst), (access, route)
        inst = _example()
        _task(inst)["agent_facing"]["provided_materials"].append(_data_file("agent", access, "fully_synthetic"))
        assert _valid(inst), access


def test_rejects_derived_hidden_variant_of_restricted_source():
    """Effect-injected or perturbed variants are for redistributable data only (verifier protocol §6)."""
    inst = _example()
    _task(inst)["hidden"]["verifier"]["hidden_datasets"].append(
        _data_file("hidden", "restricted_access", "derived_from_redistributable"))
    assert not _valid(inst)


def test_rejects_data_file_without_route_or_source():
    for missing in ["data_route", "source_access"]:
        inst = _example()
        del _task(inst)["agent_facing"]["provided_materials"][0][missing]
        assert not _valid(inst), missing
    inst = _example()
    _task(inst)["agent_facing"]["provided_materials"][0]["data_route"] = "semi_synthetic_restricted"
    assert not _valid(inst)


def test_accepts_new_validation_run_kinds():
    runs = [
        _run("expert_solve", blind=True, duration_minutes=95),
        _run("recognition_probe", expected_verdict="not_applicable", n_correct_answers=0),
        _run("knowledge_probe", expected_verdict="not_applicable", n_correct_answers=3),
        _run("hint_ladder", hint_level="H2"),
        _run("full_harness_replay", n_runs=300),
        _run("mutation_analysis", expected_verdict="reject"),
    ]
    for run in runs:
        inst = _example()
        inst["validation_runs"] = [run]
        assert _valid(inst), run["kind"]


def test_rejects_unknown_validation_run_kind():
    inst = _example()
    inst["validation_runs"] = [_run("vibe_check")]
    assert not _valid(inst)


def test_validation_run_kind_specific_fields():
    probe = _run("recognition_probe", expected_verdict="not_applicable")
    del probe["observed"]
    no_observed = _run("agent_trial")
    del no_observed["observed"]
    cases = [
        probe,                                  # probes need n_correct_answers
        _run("hint_ladder"),                    # hint ladder needs hint_level
        _run("hint_ladder", hint_level="H4"),   # only H1-H3 exist
        _run("expert_solve"),                   # expert solves record blindness
        no_observed,                            # every other kind needs observed verdicts
    ]
    for run in cases:
        inst = _example()
        inst["validation_runs"] = [run]
        assert not _valid(inst), run


def test_accepts_recognition_task_tag_only():
    inst = _example()
    _task(inst)["tags"] = ["recognition_task"]
    assert _valid(inst)
    _task(inst)["tags"] = ["easy_task"]
    assert not _valid(inst)


def test_exposure_log_entry():
    inst = _example()
    inst["exposure_log"].append(_exposure())
    assert _valid(inst)
    for change in [{"visibility": "hidden"}, {"terms": "vibes"}]:
        inst = _example()
        inst["exposure_log"].append(_exposure(**change))
        assert not _valid(inst), change
    for missing in ["terms", "exposed_at", "material_description"]:
        inst = _example()
        entry = _exposure()
        del entry[missing]
        inst["exposure_log"].append(entry)
        assert not _valid(inst), missing
    inst = _example()
    entry = _exposure()
    del entry["service"]                        # neither a model nor a service
    inst["exposure_log"].append(entry)
    assert not _valid(inst)


def test_exposure_log_can_record_a_breach():
    """Consumer-account exposures must be recordable, so that LK-5 breaches are logged rather than hidden."""
    inst = _example()
    inst["exposure_log"].append(_exposure(terms="consumer_training_opt_out"))
    assert _valid(inst)


def test_interview_record_adjudication_and_suggestion_assignments():
    adjudicated = _ledger_entry(adjudication={"adjudicator_id": "econ-ext-02", "verdict": "valid_objection",
                                              "adjudicated_at": "2026-11-06T10:00:00Z"})
    inst = _example()
    inst["interview_records"] = [_interview_record(
        suggestion_ledger=[adjudicated],
        suggestion_assignments=[{"decision_id": "dm-estimator", "suggestions_on": True},
                                {"decision_id": "dm-clustering", "suggestions_on": False}])]
    assert _valid(inst)
    bad_verdict = _ledger_entry(adjudication={"adjudicator_id": "econ-ext-02", "verdict": "probably_fine",
                                              "adjudicated_at": "2026-11-06T10:00:00Z"})
    no_adjudicator = _ledger_entry(adjudication={"verdict": "false_endorsement",
                                                 "adjudicated_at": "2026-11-06T10:00:00Z"})
    for entry in [bad_verdict, no_adjudicator]:
        inst = _example()
        inst["interview_records"] = [_interview_record(suggestion_ledger=[entry])]
        assert not _valid(inst), entry
    inst = _example()
    inst["interview_records"] = [_interview_record(suggestion_assignments=[{"decision_id": "dm-estimator"}])]
    assert not _valid(inst)


def test_accepts_clean_room_independent_check():
    inst = _example()
    check = inst["reference_implementations"][0]["validation"]["independent_check"]
    for method in ["clean_room_reimplementation", "blind_expert_solve"]:
        check["method"] = method
        assert _valid(inst), method



def test_rubric_assessment_roles_and_stage():
    def assessment(**over):
        a = {"rubric_version": "0.2.0", "assessor_role": "blind_outside_economist",
             "assessed_at": "2026-11-06T10:00:00Z", "stage": 5,
             "items": [{"criterion_id": "SP-1", "rating": "pass"}], "overall": "ready_for_next_stage"}
        a.update(over)
        return a
    for role in ["blind_outside_economist", "status_classifier", "release_editor", "shepherd"]:
        inst = _example()
        inst["task_candidates"][0]["quality_assessments"] = [assessment(assessor_role=role)]
        assert _valid(inst), role
    for bad in [assessment(stage=9), assessment(stage=-1), assessment(assessor_role="journal_editor")]:
        inst = _example()
        inst["task_candidates"][0]["quality_assessments"] = [bad]
        assert not _valid(inst), bad

if __name__ == "__main__":
    tests = [f for name, f in sorted(globals().items()) if name.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print(f"{len(tests)} tests passed")
