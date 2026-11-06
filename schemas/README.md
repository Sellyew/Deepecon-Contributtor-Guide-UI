# Deliverable 4 — Contribution Data Schema

> **To be redesigned (2026-11-06).** The contribution schema will be rebuilt from the coauthor's example contribution package (D-023; [MVP proposal](../docs/architecture/mvp-contributor-interface.md) §6). This 0.3.0 draft and its tests are kept as a record of the earlier design, which assumed an AI interview.

| | |
|---|---|
| **Status** | **Proposed** draft 0.3.0 (2026-11-05). Not yet reviewed by the research lead. 0.3.0 integrates two independent reviews of 2026-11-05 (econometric; benchmark methodology): decision-space constraints, tiers per graded output, secondary validity layers, inference-only predictions, data routes, new validation-run kinds, a recognition-task tag, and an exposure log of hidden material (see §8). It is **not backward compatible** with 0.2.0 (§6). |
| **Machine-readable schema** | [`deepecon-contribution.schema.json`](deepecon-contribution.schema.json) (JSON Schema, draft 2020-12) |
| **Illustrative instance** | [`examples/illustrative-staggered-did.contribution.yaml`](examples/illustrative-staggered-did.contribution.yaml) — fictional paper and numbers |
| **Tests** | [`../tests/schema/test_schema.py`](../tests/schema/test_schema.py) |
| **Depends on** | [Decision log](../docs/decisions/decision-log.md) D-007 to D-011, P-013, P-015, P-026, P-027; [verifier validation protocol](../docs/methodology/verifier-validation-protocol.md) v0.3.0 ("VVP" below); [construction protocol](../docs/methodology/benchmark-construction-protocol.md); [task-quality rubric](../docs/methodology/task-quality-rubric.md); [interview protocol](../docs/interview/expert-interview-protocol.md) v0.2.1 |

## 1. What the schema is for

One contribution — one paper, one contributor team — produces a **contribution package**: a directory (or ZIP archive) with a manifest that conforms to this schema. The schema is the contract between three otherwise independent parts of the project:

1. **Whatever interface the contributor uses** (hosted platform, Claude Code plugin, or a human interviewer). The schema knows nothing about frontends (requirement from Deliverable 4: "avoid coupling the schema to either frontend architecture").
2. **The internal construction pipeline**, where shepherds turn candidate material into tasks and validate verifiers.
3. **The benchmark release**, which may only ever receive material marked as agent-facing, plus hidden evaluation material kept outside agents' reach.

## 2. Design principles

| Principle | How the schema implements it | Brief / log reference |
|---|---|---|
| Language independence | All enumerations are language-neutral codes. Free text is a `localizedText`: exactly one original plus any number of labelled translations (`machine_translated`, `translation_of`, `translator`). | §9; D-007 |
| Preserve the contributor's own words | The original version is mandatory and can never be replaced by a translation; the schema rejects records with zero or two originals. | §9 |
| Human authority and provenance | Every substantive assertion is a `statement` with `provenance`: who originated it (contributor, RA, LLM-suggested, LLM-summarized, LLM-extracted, shepherd, reviewer, automated check), the contributor's disposition (pending, endorsed, edited-then-endorsed, rejected, withdrawn), and independent validation status. LLM-originated content must name the model. | §5.5; D-008 |
| Four information tiers | Every entity and file carries `visibility`: `contributor`, `internal`, `agent`, `hidden`. Several entities fix their tier with `const` (e.g., failure modes and flawed variants are always `hidden`), so a mislabelled record fails validation. | §5.4; D-009 |
| Candidate, not benchmark content | Lifecycle fields (`status`, `review_status`, `lifecycle`) separate contributor approval from independent review and admission. | §10D; D-010 |
| Originals are never modified | Flawed variants are stored as a patch plus separate files referencing a base implementation. | §6; D-011 |
| Validity layers | Critical decisions carry `validity_layer`. Failure modes carry a primary `validity_layer` plus optional `secondary_validity_layers`, with the same five values: computational (implementation fidelity), measurement, statistical, identification, interpretation — the lead's three layers plus two. | §4; D-013; P-003; VVP §9 |
| Estimand, assumptions, and estimator kept apart | `target_analyses[].estimand` states the estimand in potential-outcome terms, with `weights`, `window`, and `population`, plus its `identifying_assumptions`; it never names the estimator. Valid alternatives sit in the hidden `decision_space`, whose options can `require` or `exclude` options of other decisions. | §4; P-022; VVP §4 |
| No artificial binary keys | Failure-mode `status` (established, conditional, contested; default needs_review) comes from independent blind classifications (`status_classifications`); the contributor's view is kept separately as a claim. Each **graded output** carries a verifiability tier: V1 deterministic comparison, V2a exact relation, V2b stochastic check with stated error rates, V3 expert-consensus key, V4 open-ended (unscored). The tier does not follow from the layer. | §4; D-013; X-003; P-004; VVP §9 |
| No restricted microdata, no derived works of them | `submission.contains_restricted_microdata` must be `false`. Data files record `source_access` and `data_route`; data from a non-redistributable source may appear, in any tier, only as `fully_synthetic` data. | §10E; P-015; P-027; VVP §6 |
| Exposure of hidden material is logged | `exposure_log[]` (internal tier) records what hidden-tier material a model or service saw, under which terms, and when. | P-026; rubric LK-5; VVP §10 |
| Versioned everything | `schema_version`, `protocol_version`, `rubric_version` (semantic versioning) on every package. | §7 (version management) |

## 3. Entity overview

```
Contribution (manifest)
├── contributors[]            role, relationship to paper, ORCID (optional)
├── consent                   data-flow disclosure version, model providers, account terms, disclosure embargo,
│                             credit preference
├── paper                     bibliographic metadata (PDF only if licensed)
├── source_package            where the original replication package lives, licence, data availability
├── target_analyses[]         bounded results (e.g., Table 2 col. 1): estimand in potential-outcome terms
│                             (weights, window, population) and identifying assumptions; never the estimator
├── reference_implementations[]   validated correct code, environment, expected + intermediate outputs,
│                                 reproduction status, independent check     (internal)
├── critical_decisions[]      decisions that determine validity, with alternatives and rationale (internal)
├── failure_modes[]           plausible wrong alternatives: why wrong, realism warrant, primary and secondary
│                             layers, status, predicted consequence, detection procedure     (hidden)
├── flawed_variants[]         patch + files + observed outputs + consequence evidence (hidden)
├── task_candidates[]         agent_facing part (agent tier) | hidden part: verifier with graded outputs and
│                             their tiers, decision space with requires/excludes, keys, controls; tags
├── interview_records[]       turns, stages, model, free-recall locks, suggestion ledger and assignments,
│                             influence metrics (internal)
├── validation_runs[]         one record per ladder run: oracle … agent trials, expert solves, probes,
│                             hint ladder, full-harness replays (hidden)
├── exposure_log[]            hidden material seen by a model or service: what, by whom, terms, when (internal)
├── reviews[]                 independent review decisions (internal)
├── submission                channel, checksum, licence confirmation
├── licenses[]                per-asset redistribution status
└── files[]                   inventory: path, tier, checksum, role; data files also source access and route
```

## 4. Mapping to the research lead's requested fields

**The ten elements per mistake (brief §3.3):**

| # | Requested element | Schema location |
|---|---|---|
| 1 | Description of the mistake | `failure_modes[].description` |
| 2 | Why it is incorrect | `failure_modes[].why_incorrect.statement` (+ `citations`) |
| 3 | Why it is realistic and easy to overlook | `failure_modes[].realism_warrant` (with warrant types) |
| 4 | The implementation change | `flawed_variants[].patch` (unified diff) |
| 5 | The incorrect code | `flawed_variants[].files` |
| 6 | Results of the incorrect implementation | `flawed_variants[].observed_outputs` |
| 7 | Difference between correct and incorrect outputs | `flawed_variants[].consequence.comparisons` (estimate or standard error, + robustness) |
| 8 | Scientific consequences | `failure_modes[].scientific_consequence` |
| 9 | Detection or verification procedure | `failure_modes[].detection_procedure`; `task_candidates[].hidden.verifier` (with `graded_outputs`) |
| 10 | Evidence it is wrong, not an alternative valid approach | `failure_modes[].status`, `status_justification`, `conditions`, `why_incorrect.citations`, `similar_but_valid_approaches`; `hidden.decision_space` |

**The structured-output fields (brief §5.4):** paper metadata → `paper`; contributor metadata and relationship → `contributors[]`; research objective and empirical design → `target_analyses[].estimand`; target AI capability → `task_candidates[].target_capability`; critical scientific decision → `critical_decisions[]`; plausible mistake → `failure_modes[]`; correct and incorrect implementation → `reference_implementations[]`, `flawed_variants[]`; expected and observed outputs → `expected_outputs`, `observed_outputs`; ground-truth evidence → `why_incorrect`, `validation_runs[]`, `reference_implementations[].validation`; verification strategy → `task_candidates[].hidden.verifier` (graded outputs and their tiers); alternative valid solutions → `hidden.decision_space`, `hidden.alternative_solution_impl_ids`, `similar_but_valid_approaches`; task-quality assessment → `task_candidates[].quality_assessments[]`; data and software requirements → `softwareEnv`, `source_package.data_availability`, `fileRef.source_access` and `data_route`; unresolved concerns → `task_candidates[].unresolved_concerns`; expert review status → `reviews[]`, `review_status`.

## 5. Physical package layout and tier enforcement

```
<contribution-id>/
├── manifest.yaml        # the schema instance (tier: internal); hidden fields may be split out, see below
├── contributor/         # what the contributor saw and approved: dossier summary, consent text
├── internal/            # reference implementations, decisions, interview records, reviews, exposure log
├── agent/               # ONLY material that may enter an evaluated agent's environment
├── hidden/              # failure modes, flawed variants, verifiers, keys, hidden datasets, validation logs
└── checksums.sha256
```

**Enforced by the JSON Schema** (and covered by the tests): tier constants; one original per text; LLM-originated content names its model; tier enum V1, V2a, V2b, V3, V4 on every graded output, and at least one graded output per task; `<decision_id>/<option_id>` reference format; data files carry `source_access` and `data_route`, and a non-redistributable source (`public_not_redistributable`, `restricted_access`, `confidential`) forces `fully_synthetic` in every tier, which covers agent-facing material and hidden variants; probe runs carry `n_correct_answers`, hint-ladder runs a `hint_level`, expert solves a `blind` flag, and every other run its verifier verdicts; exposure-log entries name a model or a service and the terms.

**Validation rules beyond what JSON Schema can express** (to be implemented as part of `validation/`, Phase 5):

1. Every `fileRef.path` sits under the directory matching its `visibility`.
2. **Leakage scan:** no file under `agent/` contains hidden identifiers, failure-mode text, patch annotations, answer-key values, or the outputs a task asks the agent to produce. In correction and detection tasks, where the presented package itself carries the planted change, that package is checked for tell-tales under rubric LK-3 instead (rubric LK-1).
3. Every `failure_mode_id`, `variant_id`, and `impl_id` reference resolves, and so does every decision-space reference (`requires`, `excludes`) within its task; `decision_id`/`option_id` pairs are unique within a task.
4. A task with `task_type` in {research_execution, error_correction} and any graded output at tier V1, V2a, or V2b lists at least one negative control with `expected_verdict: reject`, and every listed negative control has a validation run with the expected verdict.
5. `instruction_authorship: llm_drafted_unedited` blocks admission.
6. A failure mode with `status: contested` cannot back a graded output at tier V1, V2a, or V2b.
7. Checksums match.
8. **Decision space.** For each decision named in an option's `requires`, a valid combination selects one of the listed options of that decision; it selects none of the options in `excludes`. No option both requires and excludes the same option. At most two decisions per task have more than one `reference` or `accepted` option, and every selectable combination has a conditional reference checked against a second implementation (VVP §4 items 3–4; rubric GT-1). An identifying assumption that the instruction fixes may be recorded as a decision with a single `reference` option, so that other options can require it.
9. **Graded outputs.** Each `(output_id, quantity)` pair appears once and names an output of the output contract or the benchmark-wide results schema. When several checks grade one quantity, its tier is the least verifiable of them; where a document needs a single tier for a task, it is that of the task's least verifiable graded output. A V3 graded output needs the agreement evidence of VVP §9.
10. **Layers.** `secondary_validity_layers` does not repeat the primary `validity_layer`.
11. **Data.** A fully synthetic file built for a non-redistributable source has a `license_ref` to a licence record documenting the disclosure review and, where required, the provider's permission; GT-1 and RV-2 are re-run on these data (VVP §6). `source_access: unknown` blocks admission (rubric EN-3).
12. **Exposure (rubric LK-5).** Every session, trial, or model call that saw hidden-tier material has an `exposure_log` entry. LK-5 fails on any entry whose `terms` are not commercial no-training terms, a locally hosted open-weight model, or a vetted evaluator's agreement. The schema accepts such entries on purpose, so that breaches are recorded rather than hidden.
13. **Interview records.** Every free-recall lock precedes the contribution's first suggestion, and `false_endorsement_rate` counts only endorsements adjudicated as `false_endorsement` (protocol §4, §7).

**Reporting.** Task counts are reported by failure-mode category (the `category` of the failure mode's critical decision) × data route (the routes of the task's agent-tier data files), so that a bias toward estimator-choice flaws on fully synthetic data is visible (VVP §6).

## 6. Versioning policy (proposed)

- **Patch** (0.1.x): clarifications and new optional fields. Old packages remain valid.
- **Minor** (0.x.0): new optional entities or enumerations. Old packages remain valid; tools must ignore unknown `x-` fields.
- **Major** (x.0.0): breaking change, accompanied by a migration script and a note in the decision log.
- **Before 1.0.0**, while the schema is a draft, a minor version may also make breaking changes; each is listed with a migration note. 0.3.0 is the first version to list its breaking changes with migration notes (§8); 0.2.0 had already made `realism_warrant.observed_in_practice` required, without a migration note. No contribution packages existed when either was drafted.
- Packages are never rewritten in place by a schema upgrade; a migration produces a new package version with provenance.

## 7. Measuring AI influence

The interview protocol (v0.2.1, §4 and §7) treats AI influence on contributors as a measured quantity. The schema records:
- `provenance.exposure` and `preceding_suggestion_ids` on every statement;
- `interview_records[].free_recall_lists`: unaided lists, all recorded before the contribution's first suggestion;
- a `suggestion_ledger` that includes known-valid controls, with an independent `adjudication` of each endorsed control;
- `suggestion_assignments`: the pre-registered, balanced randomization of suggestions over design-map decisions;
- the metrics `llm_originated_share`, `post_exposure_share`, `llm_influenced_share`, and `false_endorsement_rate`.

Recall of a known-issues key is computed on pre-exposure items only. The similarity threshold behind `llm_influenced_share` is validated against blinded double human coding, with suggestion-off decisions as the baseline. Thresholds that judge the protocol or a workflow are applied to counts pooled across participants, with exact confidence intervals.

`provenance.exposure` concerns a contributor's exposure to AI content. It is unrelated to `exposure_log`, which records which models and services saw hidden material (§2).

## 8. Changes

### 0.3.0 (independent reviews, 2026-11-05)

**Breaking changes, with migration notes:**
- The task-level `verifiability_tier` is removed. Each task lists `hidden.verifier.graded_outputs[]`, each with its own `verifiability_tier`. Migrate V2 to V2a (exact relation) or V2b (stochastic check) for each graded output.
- Decision-space options need an `option_id`, and their `decision_id` must be a valid ID.
- Probe runs (`recognition_probe`, `knowledge_probe`) carry `n_correct_answers` instead of `observed`; `hint_ladder` runs need `hint_level`; `expert_solve` runs need `blind`.
- Data files (`role: data`) need `source_access` and `data_route`.

**Additions:**
- **Decision space** (`$defs/decisionSpaceOption`): `option_id`, `requires`, `excludes`, with references written `<decision_id>/<option_id>` (VVP §4 item 3).
- **Graded outputs** (`$defs/gradedOutput`): output, quantity, tier (`$defs/verifiabilityTier`: V1, V2a, V2b, V3, V4), methods, and a noise-only tolerance (VVP §4 item 6, §9).
- **Layers:** `failure_modes[].secondary_validity_layers`, sharing `$defs/validityLayer` with the primary layer.
- **Consequences:** `predicted_consequence.category` adds `changes_inference_only` (probe P-PRED); `consequence.comparisons[].quantity` lets a standard-error comparison be recorded (the SE-ratio criterion of rubric RV-2).
- **Estimand:** `weights` and `window`; descriptions separate the estimand, the identifying assumptions, and the estimator (VVP §4 item 1).
- **Data routes:** `fileRef.source_access` and `fileRef.data_route` (`redistributable_original`, `derived_from_redistributable`, `fully_synthetic`) (VVP §6).
- **Validation runs:** kinds `expert_solve`, `recognition_probe`, `knowledge_probe`, `hint_ladder`, `full_harness_replay`, and `mutation_analysis` (VVP L5 had no kind); fields `blind`, `duration_minutes`, `hint_level`, `n_correct_answers`. The `kind` description maps kinds to ladder rungs; `repeat_stability` does not satisfy L9, and `guided_agent_fairness` is superseded by `hint_ladder`.
- **Task `tags`:** `recognition_task` (rubric SP-3).
- **Exposure:** `exposure_log[]` (`$defs/exposureLogEntry`, internal tier; VVP §10, rubric LK-5); `consent.disclosure_embargo_accepted`.
- **Independent check:** methods `clean_room_reimplementation` and `blind_expert_solve` (rubric GT-1); a port or a code review does not qualify.
- **Output contract:** declarations limited to non-crux conventions from a benchmark-wide `convention_vocabulary`; a benchmark-wide results schema; intermediate outputs taken from re-execution (VVP §4 items 4–5).
- **Interview records:** `suggestion_assignments` and `suggestion_ledger[].adjudication` (protocol v0.2.1).
- **Rubric assessments:** `assessor_role` adds `blind_outside_economist`, `status_classifier`, and `release_editor`; an optional `stage` (0–8) records the construction stage of each assessment, per the rubric's stage map.
- **Descriptions** aligned with VVP v0.3.0 and rubric v0.2.0: noise-only tolerances, the RV-2 materiality rule, the L7 separation bound, and status classification after RV-2 and L4/L7 by one or two classifiers.
- **Example:** estimand in potential-outcome terms, with the comparison group moved to the identifying assumptions; a noise-only tolerance; a decision space with `requires`; tiers V2a (injection-checked estimate) and V1 (deterministic comparisons); data routes; a blind expert solve, a recognition probe, and an exposure-log entry.
- **Tests** for each new constraint.

### 0.2.0

- `validity_layer` gains `measurement`.
- `provenance.exposure` and `preceding_suggestion_ids` added.
- `realism_warrant.observed_in_practice` added and required.
- Failure-mode status: default `needs_review`; `status_claimed_by_contributor` and `status_classifications` added.
- `predicted_consequence.category` and optional `quantiles` added.
- Task candidates: `hidden.decision_space`, `hidden.verifier_version`, `hidden.verifier_frozen_at`, plus output-contract fields `declared_choices_required` and `intermediate_outputs_required`.
- Interview records: `free_recall_lists`, `suggestion_ledger`, influence metrics, and `summary_accuracy_ratings`.
- Validation runs: `tolerance_calibration` and `expert_calibration` kinds.

## 9. Open points for review

- Whether to split `manifest.yaml` into a non-hidden manifest plus a `hidden/manifest.hidden.yaml`, so that the internal tier never carries hidden fields (stronger separation, more files).
- Whether contributor identity fields (e-mail, ORCID) should live outside the package in a separate registry (data minimization).
- Whether `numericResult` needs vector/matrix outputs (event-study coefficient paths), or a file reference suffices.
- Where the exposure log should live: in each contribution package, or in a benchmark-wide registry, since external evaluations happen long after submission.
- A `split` field (public or held-out) once O-001 is decided; all tasks and twins from one paper, across contributions, would share it (VVP §10 item 3).
