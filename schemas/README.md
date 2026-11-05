# Deliverable 4 — Contribution Data Schema

| | |
|---|---|
| **Status** | **Proposed** draft 0.1.0 (2026-11-05). Not yet reviewed by the research lead. |
| **Machine-readable schema** | [`deepecon-contribution.schema.json`](deepecon-contribution.schema.json) (JSON Schema, draft 2020-12) |
| **Illustrative instance** | [`examples/illustrative-staggered-did.contribution.yaml`](examples/illustrative-staggered-did.contribution.yaml) — fictional paper and numbers |
| **Tests** | [`../tests/schema/test_schema.py`](../tests/schema/test_schema.py) |
| **Depends on** | [Decision log](../docs/decisions/decision-log.md) D-007 to D-011; [construction protocol](../docs/methodology/benchmark-construction-protocol.md); [interview protocol](../docs/interview/expert-interview-protocol.md) |

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
| Three (plus one) validity layers | Critical decisions and failure modes carry `validity_layer`: computational, statistical, identification, interpretation. | §4; D-013 |
| No artificial binary keys | Failure modes carry `status`: established, conditional, or contested; tasks carry a verifiability tier (V1–V4). | §4; D-013; X-003 |
| No restricted microdata | `submission.contains_restricted_microdata` must be `false`. | §10E |
| Versioned everything | `schema_version`, `protocol_version`, `rubric_version` (semantic versioning) on every package. | §7 (version management) |

## 3. Entity overview

```
Contribution (manifest)
├── contributors[]            role, relationship to paper, ORCID (optional)
├── consent                   data-flow disclosure version, model providers, account terms, credit preference
├── paper                     bibliographic metadata (PDF only if licensed)
├── source_package            where the original replication package lives, licence, data availability
├── target_analyses[]         bounded results (e.g., Table 2 col. 1) with a precise estimand
├── reference_implementations[]   validated correct code, environment, expected + intermediate outputs,
│                                 reproduction status, independent check     (internal)
├── critical_decisions[]      decisions that determine validity, with alternatives and rationale (internal)
├── failure_modes[]           plausible wrong alternatives: why wrong, realism warrant, status,
│                             predicted consequence, detection procedure     (hidden)
├── flawed_variants[]         patch + files + observed outputs + consequence evidence (hidden)
├── task_candidates[]         agent_facing part (agent tier) | hidden part (verifier, keys, controls)
├── interview_records[]       turns, stages, model, metrics incl. LLM-suggestion acceptance (internal)
├── validation_runs[]         oracle, negative-control, metamorphic, hidden-variant, shortcut, agent trials (hidden)
├── reviews[]                 independent review decisions (internal)
├── submission                channel, checksum, licence confirmation
├── licenses[]                per-asset redistribution status
└── files[]                   inventory: path, tier, checksum, role
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
| 7 | Difference between correct and incorrect outputs | `flawed_variants[].consequence.comparisons` (+ robustness) |
| 8 | Scientific consequences | `failure_modes[].scientific_consequence` |
| 9 | Detection or verification procedure | `failure_modes[].detection_procedure`; `task_candidates[].hidden.verifier` |
| 10 | Evidence it is wrong, not an alternative valid approach | `failure_modes[].status`, `status_justification`, `conditions`, `why_incorrect.citations`, `similar_but_valid_approaches` |

**The structured-output fields (brief §5.4):** paper metadata → `paper`; contributor metadata and relationship → `contributors[]`; research objective and empirical design → `target_analyses[].estimand`; target AI capability → `task_candidates[].target_capability`; critical scientific decision → `critical_decisions[]`; plausible mistake → `failure_modes[]`; correct and incorrect implementation → `reference_implementations[]`, `flawed_variants[]`; expected and observed outputs → `expected_outputs`, `observed_outputs`; ground-truth evidence → `why_incorrect`, `validation_runs[]`, `reference_implementations[].validation`; verification strategy → `task_candidates[].hidden.verifier`; alternative valid solutions → `hidden.alternative_solution_impl_ids`, `similar_but_valid_approaches`; task-quality assessment → `task_candidates[].quality_assessments[]`; data and software requirements → `softwareEnv`, `source_package.data_availability`; unresolved concerns → `task_candidates[].unresolved_concerns`; expert review status → `reviews[]`, `review_status`.

## 5. Physical package layout and tier enforcement

```
<contribution-id>/
├── manifest.yaml        # the schema instance (tier: internal); hidden fields may be split out, see below
├── contributor/         # what the contributor saw and approved: dossier summary, consent text
├── internal/            # reference implementations, decisions, interview records, reviews
├── agent/               # ONLY material that may enter an evaluated agent's environment
├── hidden/              # failure modes, flawed variants, verifiers, keys, hidden datasets, validation logs
└── checksums.sha256
```

Validation rules beyond what JSON Schema can express (to be implemented as part of `validation/`, Phase 5):

1. Every `fileRef.path` sits under the directory matching its `visibility`.
2. **Leakage scan:** no file under `agent/` contains hidden identifiers, flawed-variant code fragments, answer-key values, or the reference outputs that a task asks the agent to produce.
3. Every `failure_mode_id`, `variant_id`, and `impl_id` reference resolves.
4. A task with `task_type` in {research_execution, error_correction} at tier V1/V2 lists at least one negative control with `expected_verdict: reject`, and every listed negative control has a validation run with the expected verdict.
5. `instruction_authorship: llm_drafted_unedited` blocks admission.
6. A failure mode with `status: contested` cannot back a task at tier V1 or V2.
7. Checksums match.

## 6. Versioning policy (proposed)

- **Patch** (0.1.x): clarifications and new optional fields. Old packages remain valid.
- **Minor** (0.x.0): new optional entities or enumerations. Old packages remain valid; tools must ignore unknown `x-` fields.
- **Major** (x.0.0): breaking change, accompanied by a migration script and a note in the decision log.
- Packages are never rewritten in place by a schema upgrade; a migration produces a new package version with provenance.

## 7. Open points for review

- Whether to split `manifest.yaml` into a non-hidden manifest plus a `hidden/manifest.hidden.yaml`, so that the internal tier never carries hidden fields (stronger separation, more files).
- Whether contributor identity fields (e-mail, ORCID) should live outside the package in a separate registry (data minimization).
- Whether `numericResult` needs vector/matrix outputs (event-study coefficient paths) in 0.1, or a file reference suffices.
