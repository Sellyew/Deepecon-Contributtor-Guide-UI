# Contributor-Interface Schemas

| | |
|---|---|
| **Status** | **Proposed** draft 0.1.0 (2026-11-06), derived from the [example contribution package V5](../../docs/requirements/2026-11-06-example-package-v5-review.md) for the [MVP contributor interface](../../docs/architecture/mvp-contributor-interface.md). Questions Q1–Q6 in the MVP proposal (§9) may change details. |
| **Replaces** | The earlier contribution schema 0.3.0 (`../deepecon-contribution.schema.json`), which assumed an AI interview; it is kept as a record. |
| **Tests** | `python3 tests/schema/test_contributor_interface.py` (13 tests). All examples are synthetic and marked fictional. |

## The four files

| Schema | Purpose | Notes |
|---|---|---|
| [`rubric-import.schema.json`](rubric-import.schema.json) | The team's rubric in the V5 `Rubric.json` format, imported as it is | Three item groups (`conceptual`, `missing`, `technical`). Each item needs `id`, `points`, and `title`, plus its group's description field(s): `files` and `criterion`; `acceptable_work` (and optionally `available_evidence_and_boundary`); `file` and `repair`. Every other field is preserved and hidden unless configured. **Checked on 2026-11-06:** the real V5 rubric passes this schema and the consistency checks (validation output only; no content was printed). |
| [`paper-config.schema.json`](paper-config.schema.json) | One configured paper and task version | Citation; the public replication package; versions; candidate-package hash; group targets; **which item fields contributors see**; optional human-written Chinese display text (`machine_translated` must be false); optional map from original to candidate file names; optional paired error/missing key points; the materials checklist. |
| [`contributor-review.schema.json`](contributor-review.schema.json) | Export of one contributor's answers | Pseudonymous contributor ID only; verdict per item (keep, keep with changes, reject, unsure, not reviewed); optional ticks and reasons; suggested wording; proposals; numbered confirmations with hashes. Unknown fields are rejected, so credentials cannot leak into exports. |
| [`submission-manifest.schema.json`](submission-manifest.schema.json) | What the contributor provided | Upload (files with SHA-256), public reference, or another agreed channel; checklist coverage; a required declaration that no data are included. |

## Rules enforced in code

[`validation/rubric_checks.py`](../../validation/rubric_checks.py) (standard library only):
- `check_rubric`: unique item IDs; points equal the largest allowed score; allowed scores start at 0 and increase; tier keys equal the allowed scores; item points sum to the maximum. Messages contain item IDs and field names only, never item text.
- `check_config_against_rubric`: the rubric versions match; display text and paired variants refer to existing items.
- `contributor_view`: builds what a contributor may see. Fields not listed in the configuration never appear, whatever the rubric contains. Original file names are shown when a map is configured.
