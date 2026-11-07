# Contributor-Interface Schemas

| | |
|---|---|
| **Status** | Draft 0.3.0 (2026-11-07), used by the contributor site from milestone M1 ([implementation](../../implementations/contributor-interface/README.md); plan approved, D-043). 0.3.0 adds the fields the [AI use and integrity rules](../../docs/architecture/llm-use-policy.md) need: per-item AI help and consent in the contributor review (0.3.0), item origin in the item map (0.2.0), and publication status in the paper configuration (0.3.0). 0.2.0 (2026-11-06) made item categories configurable per field (D-025), added the item map and runnable-package submissions with data routes (D-027), and localized interface text by BCP 47 language tag; item text is not translated (D-030). |
| **Replaces** | The earlier contribution schema 0.3.0 (`../deepecon-contribution.schema.json`), which assumed an AI interview; kept as a record. |
| **Tests** | `python3 tests/schema/test_contributor_interface.py` (16 tests). All examples are fictional: an [empirical paper](examples/empirical/) with V5-style categories and a [theory paper](examples/theory/) with different ones. |

## The five files

| Schema | Purpose | Notes |
|---|---|---|
| [`rubric-import.schema.json`](rubric-import.schema.json) | The team's own rubric file, imported as it is | Deliberately minimal: categories and points differ by field. The paper configuration declares which arrays hold items and which fields fill each role; `validation/rubric_checks.py` checks the file against that. **Checked on 2026-11-06:** the real V5 rubric imports through this path with a V5-style profile, and its scoring fields never reach the contributor view (only pass/fail printed). |
| [`paper-config.schema.json`](paper-config.schema.json) | One configured paper | Field label; citation; versions; **categories** (localized label and one-line meaning, source array, field roles, visible roles, target); interface languages (BCP 47 tags; English required); original-file-name map; checklist; submission settings. |
| [`item-map.schema.json`](item-map.schema.json) | The map for the review screen (expert-only) | Nodes (stages, files, results, or for theory papers sections, derivations, propositions) and edges; per item: anchors, affected results, original and modified excerpts, summary, consequence, pairing with a variant. |
| [`contributor-review.schema.json`](contributor-review.schema.json) | Export of one contributor's answers | Pseudonymous contributor ID; one answer per item with the configured category; proposals; "Ask the team" messages; numbered confirmations. Unknown fields are rejected, so credentials cannot leak into exports. |
| [`submission-manifest.schema.json`](submission-manifest.schema.json) | What the contributor provided | Channel; files with SHA-256; package information (master script, README, software, run log, expected outputs, run time in the template README's bands); every dataset's availability and, if restricted or confidential, its route; declarations. |

## Rules enforced in code

[`validation/rubric_checks.py`](../../validation/rubric_checks.py) (standard library only):
- `normalize` and `check_rubric`: categories' source arrays exist; role fields are present; unique item IDs; points equal the largest allowed score; tiers match allowed scores; points sum to the maximum; the configuration's rubric version matches. Messages contain IDs and field names only.
- `check_item_map`: unique nodes; edges, parents, anchors, and affected results refer to existing nodes; every item is placed on the map; pairings are mutual.
- `contributor_view`: only configured roles appear; locations and excerpts show original file names; item text stays in its original language.
- `localize`: interface text in the requested language, falling back to the base language and then English.
- `map_view`: every node with markers for the items anchored to it and the items that affect it; markers carry only ID, category, and status.

## Changes in 0.3.0 (2026-11-07)

Fields that the [AI use and integrity rules](../../docs/architecture/llm-use-policy.md) (D-039, D-040, D-042) need, each with an example and a test:
- **Contributor review (0.3.0):** per item and per proposal, `ai_help` (used; tool; account kind: work, personal, API, or unknown; whether the items or the package were entered; tool and entry are required when AI was used). At the top level, `consent` (acknowledgement that evaluation sends the finished task through AI companies' APIs, which must be true; whether the team may use AI services with the contributor's unpublished materials and responses; notice version; date recorded).
- **Item map (0.2.0):** per item, `origin` (drafted by the team, the contributor, or an AI service, with the model family required for an AI service; whether AI helped review it). It is team-side and never appears in the contributor view.
- **Paper configuration (0.3.0):** `publication_status` (scored, or demo or development with its designation date). Without it, the site treats the task as scored. `candidate_version` is limited to letters, digits, `.`, `_` and `-`, because it becomes part of a file name in private storage.
- **Exposure log:** a team-side record kept in the site's team administration (not a contributor-facing schema), with the fields of Rule 10: task, AI service, developer and API host, what was received, route, date, account kind, and, for evaluation runs, the model version and release date.
