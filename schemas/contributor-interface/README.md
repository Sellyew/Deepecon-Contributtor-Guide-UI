# Contributor-Interface Schemas

| | |
|---|---|
| **Status** | **Proposed** draft 0.2.0 (2026-11-06) for the [MVP contributor interface](../../docs/architecture/mvp-contributor-interface.md) v0.3. 0.2.0 makes item categories configurable per field (D-025), adds the item map for the map-and-panel review screen, translations with provenance (D-029), and runnable-package submissions with data routes (D-027). |
| **Replaces** | The earlier contribution schema 0.3.0 (`../deepecon-contribution.schema.json`), which assumed an AI interview; kept as a record. |
| **Tests** | `python3 tests/schema/test_contributor_interface.py` (15 tests). All examples are fictional: an [empirical paper](examples/empirical/) with V5-style categories and a [theory paper](examples/theory/) with different ones. |

## The five files

| Schema | Purpose | Notes |
|---|---|---|
| [`rubric-import.schema.json`](rubric-import.schema.json) | The team's own rubric file, imported as it is | Deliberately minimal: categories and points differ by field. The paper configuration declares which arrays hold items and which fields fill each role; `validation/rubric_checks.py` checks the file against that. **Checked on 2026-11-06:** the real V5 rubric imports through this path with a V5-style profile, and its scoring fields never reach the contributor view (only pass/fail printed). |
| [`paper-config.schema.json`](paper-config.schema.json) | One configured paper | Field label; citation; versions; **categories** (label, one-line meaning, source array, field roles, visible roles, target); translations with method, model, mode (local or external API), and reviewer; original-file-name map; checklist; submission settings. |
| [`item-map.schema.json`](item-map.schema.json) | The map for the review screen (expert-only) | Nodes (stages, files, results, or for theory papers sections, derivations, propositions) and edges; per item: anchors, affected results, original and modified excerpts, summary, consequence, pairing with a variant. |
| [`contributor-review.schema.json`](contributor-review.schema.json) | Export of one contributor's answers | Pseudonymous contributor ID; one answer per item with the configured category; proposals; "Ask the team" messages; numbered confirmations. Unknown fields are rejected, so credentials cannot leak into exports. |
| [`submission-manifest.schema.json`](submission-manifest.schema.json) | What the contributor provided | Channel; files with SHA-256; package information (master script, README, software, run log, expected outputs, run time in the template README's bands); every dataset's availability and, if restricted or confidential, its route; declarations. |

## Rules enforced in code

[`validation/rubric_checks.py`](../../validation/rubric_checks.py) (standard library only):
- `normalize` and `check_rubric`: categories' source arrays exist; role fields are present; unique item IDs; points equal the largest allowed score; tiers match allowed scores; points sum to the maximum; the configuration's rubric version matches. Messages contain IDs and field names only.
- `check_item_map`: unique nodes; edges, parents, anchors, and affected results refer to existing nodes; every item is placed on the map; pairings are mutual.
- `contributor_view`: only configured roles appear; locations and excerpts show original file names; only reviewed translations appear, with their method.
- `map_view`: every node with markers for the items anchored to it and the items that affect it; markers carry only ID, category, and status.
