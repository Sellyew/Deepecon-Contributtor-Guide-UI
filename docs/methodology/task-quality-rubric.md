# Task-Quality Rubric for Economics Benchmark Tasks

| | |
|---|---|
| **Status** | **Proposed** v0.2.0 (2026-11-05). Part of Deliverable 2. Not yet reviewed by the research lead. **36 criteria in 10 groups, 20 of them gates.** v0.2.0 integrates two independent reviews ([Changes](#changes)). |
| **Primary basis** | Bercovich (2026), *Good Benchmarks* — [reading notes](../research/reading-notes/good-benchmarks-bercovich-2026.md) (bare § numbers below refer to the paper) |
| **Also informed by** | Terminal-Bench-Science (TBS) proposal, implementation (39 criteria), trial-analysis, and cheat-analysis rubrics, Apache-2.0 ([evidence note R1](../research/evidence/R1-terminal-bench-science.md)); the research lead's brief §4 and §10; independent benchmark-methodology and econometric reviews (2026-11-05). Criteria adapted from TBS name their TBS counterpart in brackets. |
| **Used by** | Contributors (self-assessment), shepherds, outside economists, independent reviewers, automated checks; recorded as `rubricAssessment` in the [schema](../../schemas/README.md). Stages are those of the [construction protocol](benchmark-construction-protocol.md); rungs L0–L13 are those of the [verifier validation protocol](verifier-validation-protocol.md) (**VVP**). |

## How to use this rubric

*Good Benchmarks* defines seven properties of a good task. A checklist that asks "Is the task verifiable? yes/no" invites generic answers, which the research lead explicitly ruled out (brief §4). Each criterion below therefore names **the evidence that settles it**, gives **economics-specific anchors** for pass, concern, and fail, and says **who assesses it, and when**.

- **Ratings:** `pass` · `concern` (acceptable only with a written resolution) · `fail` · `not_applicable`.
- **Gates.** Criteria marked **[G]** are gates: one `fail` blocks progression to the next stage. Other criteria accumulate; a reviewer may still reject a task with several unresolved concerns.
- **Stages and thresholds.** *Who / when* gives the assessor, the construction stage (0–8), and any VVP rung. It is the **single map from criteria to stages**, from which the [summary by stage](#criteria-by-construction-stage) and the protocol's gate lines derive; a criterion listed at several stages is re-assessed at each. Thresholds are proposals for the research lead, fixed in the rubric version before the outputs they judge exist.
- **No numeric total.** Summing criteria hides the failure that matters. Decisions cite the specific criteria.
- **Standard of evidence (§9).** "This is standard in our field" is not evidence. A disputed methodological claim is settled by an authoritative citation, a simulation, or an independent reviewer's demonstration.

---

## 1. Scientific relevance and realism

*Good Benchmarks #5 "Realistic and valuable", §2 "Start from real work".*

| ID | Criterion | Evidence that settles it | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **RV-1** [G] | The task mirrors work economists or research assistants are actually paid to do. | Mapping from the task to a real activity (implementing a design, replicating a result, auditing code, refereeing an empirical analysis); grounding in a published target analysis. | "Re-estimate Table 2's main effect from the provided panel" or "find and fix the problem in this estimation script." | Realistic activity but an unusual framing that needs justification. | A quiz, a puzzle, or trivia ("Which estimator did Callaway and Sant'Anna propose?"). | Contributor, shepherd · Stage 2 |
| **RV-2** [G] | The decision under test is **consequential**: getting it wrong changes a scientifically meaningful quantity. | Consequence under the **materiality rule** below; for restricted sources, re-demonstrated on fully synthetic data (EN-3). | Wrong clustering halves the SE; static TWFE shifts the ATT by over one reference SE. | Material only on some outputs or samples; or interpretation-only (V3; see the rule). | Only labels, formatting, or a third decimal place change (brief X-002), or only a knife-edge significance change. | Shepherd · Stage 4 |
| **RV-3** [G] | The failure mode is **realistic**: competent researchers plausibly make it. | Realism warrant with at least one type: the contributor's own research, refereeing, or supervising experience; a published comment or replication; methodological literature documenting the pitfall; observed AI-agent behaviour. Re-checked in the port's language (a Stata-default pitfall may not be realistic in R). | Documented in the literature and seen in RA code. | Plausible by argument only; or realistic only in the original software. | An artificial code mutation nobody would write (brief §10G, X-005). | Contributor · Stage 3; shepherd (port's language) · Stage 4; domain reviewer · Stage 7 |
| **RV-4** [G] | The **target capability** is stated precisely, and the verifier measures that capability rather than a proxy. | One-sentence capability statement; reviewer check that an agent lacking the capability cannot pass by another route (VE-4, LK-2, LK-4). | Capability: "recognize that staggered adoption with dynamic effects invalidates static TWFE, and recover the estimand." Verifier checks the recovered estimand on hidden variants. | Capability broader than what the verifier checks. | The task claims to test identification reasoning but grades a number reachable mechanically (brief §10B). | Shepherd · Stage 5; benchmark reviewer · Stage 7 |

**Materiality rule for RV-2** (benchmark-wide default; proposed thresholds), fixed in the rubric version and applied before the variant is run; task-specific deviations need the release editor's prior approval. With P the correct and F the flawed procedure, a consequence is material if any of these holds:

1. |θ_F − θ_P| ≥ SE_P;
2. SE_F/SE_P lies outside [0.75, 1.33], or coverage of the known truth falls below 85% at nominal 95% in a design-preserving simulation;
3. the sign changes, with |t| ≥ 1 under both;
4. significance changes, but only if both p-values lie outside [0.02, 0.10].

An interpretation-only consequence needs an independent reviewer's written concurrence and puts the task at tier V3.

## 2. Ground truth and scientific defensibility

*Good Benchmarks #1 "Verifiable" and §5; the brief's distinction among computational, statistical, and identification validity (§4, D-013).*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **GT-1** [G] | The **reference implementation** is validated. | Reproduction status versus the published result **and** an independent check: a **clean-room re-implementation** (from the paper, estimand statement, and codebook, by someone other than the shepherd who has not read the original code) or a **correct blind solve** (SP-1). The task environment's port is a separate artifact, checked for numerical equivalence; it inherits the original's logic, so it is not the check. Conditional references get a second implementation (VVP §4 item 4). | Original Stata code and a clean-room R implementation agree within numerical noise; discrepancies with the paper are explained. | Independent check pending (it may wait for the Stage 5 blind solve). | Unexplained discrepancy; or no clean-room or blind-solve check by Stage 7 (brief §3.2: "matching published coefficients does not automatically establish scientific correctness"). | Shepherd · Stage 1, and Stage 5 if a blind solve is the check; domain reviewer · Stage 7 |
| **GT-2** [G] | The failure mode is **genuinely wrong**, not an alternative valid approach. | Blind classification by outside economists after RV-2 and L4/L7: **one** for a vetted-taxonomy item with a canonical citation, **two** (blind to each other) for a novel item. `established` (consensus; cite) or `conditional`, each condition shown by a recorded diagnostic (event-study heterogeneity, Goodman-Bacon weights, first-stage F, treated clusters) **on the evaluation data and every hidden-variant family used for grading**. The contributor's view is a claim. | Established or conditional, with citations; every diagnostic holds on all grading data. | Conditions argued but not demonstrated on every grading family. | `contested` status behind a binary key (D-013, X-003); or a conditional flaw keyed where its conditions fail (e.g., static TWFE on constant-effect variants). | Outside classifiers · Stage 6 (after L7, before L8); domain reviewer · Stage 7 |
| **GT-3** | The failure mode's **validity layers** are identified, and each graded output's **tier** fits what it can establish. | One primary layer of five (computational, measurement, statistical, identification, interpretation) plus optional secondary layers; agreement reported. A tier per graded output (VVP §9): V1 deterministic, V2a exact relation, V2b stochastic with stated error rates, V3 expert key, V4 unscored. The tier does not follow from the layer. | Static TWFE under staggered adoption: primary layer statistical; main estimate at V2a, sample counts at V1. | One tier for differing outputs; or V3 before its item type passes the agreement study. | Identification claim graded as if it were V1 (an untestable assumption treated as a number). | Shepherd · Stage 5 |
| **GT-4** | **Alternative valid implementations** are identified and credited. | A hidden **decision space** (reference, accepted, unjustifiable, contested) with provenance and `requires`/`excludes` constraints; every accepted alternative accepted on all data (L3). Crux decisions are graded only through outcomes on separating hidden variants; declarations cover only non-crux conventions (VVP §4 items 3–4). | Each estimator (e.g., Callaway–Sant'Anna, imputation) is accepted after showing that it targets the stated weighted ATT under the stated assumption, and each is graded against its own conditional reference. | Alternatives listed but not all run. | Verifier accepts only the contributor's estimator when others target the same estimand under the stated assumptions (§7: "co-designed with the author's own solution"). | Shepherd · Stage 6 (L3); benchmark reviewer · Stage 7 |

## 3. Specification

*Good Benchmarks #2 "Well-specified", §4 "Focus on the outcome", §9 on authorship.*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **SP-1** [G] | The instruction states the **required outcome** precisely enough that meeting it implies passing the verifier. [TBS `well_specified`, `test_instruction_alignment`] | **Blind dual-verifier test** (§1, §7), before verifier engineering: two economists outside the contribution who have seen only the agent tier write acceptance criteria from the instruction and attempt the task within its limits (`expert_solve`: time, outcome, sticking points). The acceptance region must accept every correct blind solution; disagreements tighten the instruction (§4). They are then unblinded. Each verifier assertion maps to a stated requirement, and vice versa. Fallback: one blind solve per task, two on a random quarter of each task type. | Both sets of criteria accept the same answers; every correct blind solve passes. | Agreement only after a clarification then written into the instruction. | Disagreement on what counts as correct; or a correct blind solve rejected. | Two blind outside economists · Stage 5; re-checked against L11 outputs · Stage 7 (L12) |
| **SP-2** | The instruction is **short, in practitioner language, and human-written or substantially human-edited.** | Authorship record; instruction length; reviewer reading. | Two paragraphs a referee would write; goal stated first. | Longer than necessary; some LLM-style scaffolding. | LLM-drafted and unedited; enumerates steps instead of the goal (§4, §9). | Shepherd · Stage 5; benchmark reviewer · Stage 7 |
| **SP-3** [G] | Difficulty does **not** come from a hidden fact, an unstated convention, or ambiguity (§9's one-sentence-fact test). | Pre-declared **hint ladder** in agent trials (L10): H1 a design fact the instruction should carry; H2 the pitfall; H3 the method. A **knowledge probe** asks the key fact outside the task. The output contract and environment count as instruction; method-disclosing estimand phrases are recorded (VVP §4 item 1). The contributor's P-1FACT answer is only a prediction. | H1's content already in the instruction; unguided failures crux-aligned; agents that answer the knowledge probe still fail unguided; H3 trials pass (SO-3). | Failure disappears at H2: tagged `recognition_task` and reported separately until O-004 (Open) is decided. | Agents fail the knowledge probe (a fact test; see RV-1), or the failure disappears at H1 (underspecified). | Shepherd · Stage 6 (L10) |
| **SP-4** | The **output contract** is minimal, self-checkable, and **benchmark-wide**. | Results schema, declaration vocabulary, and installed software identical for all tasks of a type; nothing agent-facing is task-specific. Each task of a type reports the same superset: estimate, SE, CI, N, clusters, cluster variable, estimation-sample hash; estimator family as ungraded free text. A format validator is provided. | The type's standard results file plus a code entry point; the agent can validate its format. | A complex structure without a validator. | A task-specific field naming the crux (e.g., `cluster_level`); or failures dominated by formatting (§3: "measuring format compliance"). | Shepherd · Stage 5; automated · Stage 6 (L0) |

## 4. Solvability

*Good Benchmarks #3 "Solvable", §5 "Prove the task is solvable", §7 fairness check.*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **SO-1** [G] | A **reference solution works from the agent-facing materials only** and follows the path a researcher or agent would take. | Oracle run in the task environment with no privileged files; for diagnostic tasks, the oracle investigates (runs diagnostics) before fixing (§5). | Oracle reproduces the target outputs from the provided data and instruction. | Oracle uses a documented heuristic an expert would use but the instruction does not mention. | Oracle hard-codes the answer or reads hidden files. | Shepherd · Stage 6 (L1) |
| **SO-2** | The task is feasible within stated time and compute limits. | Measured oracle runtime and memory, agent-trial durations, and verifier re-execution time over all hidden instances. | Comfortably within limits on the reference hardware. | Close to the limit. | Exceeds the limit or depends on unavailable software. | Automated · Stage 6 (L1, L11) |
| **SO-3** | **Guided-agent fairness** (§7): with the method named, a strong agent passes. | H3 trials of the hint ladder (L10), at least 5 per configuration. | At least 4 of 5 H3 trials pass for at least one configuration: the remaining difficulty is choosing or recognizing the method. | Some H3 trials pass, but fewer than 4 of 5 for every configuration. | No H3 trial passes: look at the verifier or the environment. | Shepherd · Stage 6 (L10) |

## 5. Verification

*Good Benchmarks #1 "Verifiable", #6 "Outcome-verified", §7 "Make the verifier mean something".*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **VE-1** [G] | The verifier **accepts every correct solution** (reference, validated alternatives, correct blind solves) on the main data and all hidden variants. | Runs of kind `oracle`, `alternative_solution`, `expert_solve`, `hidden_variant` (L1, L3, L7). | Deterministic families: 100%; stochastic families: false rejection below 10⁻³ by simulation; familywise at most 1% (VVP §4 item 8). | Rare noise rejections; band re-derived with an expert's written justification, all controls re-run (VVP §4 item 9). | Any validated correct solution is rejected. | Automated + shepherd · Stage 6 (L1, L3, L7) |
| **VE-2** [G] | The verifier **rejects every validated flawed variant**, with margin, robustly. [TBS `verification_explanation_quality`] | Negative controls (L4), mutation analysis (L5), and hidden-variant separation (L7), in the kill matrix. The flagship variant must not be **data-equivalent** (VVP §2, type 2). Separation is measured against an independent witness (GT-1, L3); comparators that "failed to fail" are reported. | Each variant rejected where its conditions hold, one-sided 95% lower bound ≥ 0.90 (194 of 200 gives 0.936); margins of several noise bands; no mutant survivor reveals a verifier gap (L5). | Rejected on the main data only. | Some validated flawed variant passes. | Automated + shepherd · Stage 6 (L4, L5, L7) |
| **VE-3** | The verifier grades **outcomes**, and tests **procedure** through outcomes. | **Every graded quantity**, intermediate outputs included, comes from re-executing the agent's code in the verifier sandbox; self-reports must match and are never graded alone; inference is graded deterministically (VVP §4 items 5, 7). Hidden variants use bases the agent never sees; counterfactual-side invariances test how Y(0) is built (VVP §5). | Agent code re-run on answer-changing and invariance instances; outputs compared with conditional references on the same inputs. | Single-dataset numeric check (vulnerable to memorization); or injection without a counterfactual-side invariance. | Verifier checks which package or function was used (§7: "tests should verify outcomes, not implementations"), or grades a self-reported value. | Shepherd · Stage 6 (L6, L7) |
| **VE-4** [G] | **Shortcut resistance.** | Every VVP L8 attack fails: (a) published coefficients; (b) trivial nulls (L2) [TBS `graded_instances_discriminate`]; (c) file copying; (d) flag-everything; (e) recall (LK-4); (f) cheat trials [TBS], offline (the official configuration) and once online to measure what the offline rule protects; (g) the differential attack; (h) invariance constants; (i) change-nothing and newest-estimator policies; (j) reward writing or hidden-data reads (EN-4). Offline execution is a validity condition for any reported score. | All attacks fail. | An attack fails only because of an incidental detail. | Any attack passes in the official, offline configuration. | Automated + shepherd · Stage 6 (L2, L8); benchmark reviewer · Stage 7 |
| **VE-5** | **Verifier stability, boundary fairness, and freezing.** [TBS `deterministic_reproducible`, trial-analysis `boundary_fairness`] | **Full-harness replay** (L9): ≥ 300 replays of the oracle and each accepted alternative through sandbox and verifier, varying unfixed seeds, threads, and ≥ 2 platforms (fixed-seed re-runs of stored outputs do not count). Bands separate noise, conventions, and alternatives and are calibrated with blind expert solves (VVP §4 items 6, 10). The verifier is **frozen** before evaluation; changes create a new task version. | Zero spurious failures in at least 300 replays (one-sided 95% upper bound about 1%); no knife-edge keys (VVP §4 item 12). | Rare flakes, root cause known and fixed, replay repeated. | Flaky outcomes, or pass/fail decided by noise near a threshold. | Automated · Stage 6 (L9) |

## 6. Difficulty

*Good Benchmarks #4 "Difficult", §3 "What difficulty actually means", §8 "Run the task and watch it fail".*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **DF-1** | Difficulty is **intrinsic** to the economics, confirmed by **crux alignment**: agents that fail, fail at the stated crux. | Agent trials (L11) with failure analysis. | At least 4 of 5 failing trials fail at the stated crux (e.g., static TWFE, wrong clustering level). | Fewer than 4 of 5 fail at the crux; other causes diagnosed. | Failures come mainly from environment problems, formatting, or misread instructions. | Shepherd · Stage 6 (L11) |
| **DF-2** | The task is **one coherent problem**, not a concatenation, not "too wide", not a trick. | Instruction review; count of deliverables. | One estimand, one decision at stake. | Two related decisions. | Many small deliverables, or a misleading hint (§3). | Benchmark reviewer · Stage 7 |
| **DF-3** | Difficulty is **calibrated** without tuning against the evaluated models, and recorded. | L11: ≥ 5 trials × ≥ 3 configurations × ≥ 2 model families on the frozen task, with model IDs and dates. Each release pre-declares a target band (TBS: "10–20%" at release [P-full, R1]). No edit is justified only by an agent's success; hardening is logged with its trial (VVP §3.1). Calibration models are listed, their scores *calibration-exposed*. | Within the target band for at least one configuration, failures crux-aligned (DF-1). | Universally failed but crux-aligned (keep, flag as frontier). | At least 4 of 5 trials pass for every configuration. | Shepherd · Stage 6 (L11) |

## 7. Environment robustness

*Good Benchmarks #7 "Robust", §6 "Build a controlled environment".*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **EN-1** [G] | **Pinned, offline, reproducible, standard** environment. | **One standard image, or a dated offline CRAN/PyPI snapshot, per task type** (task-specific packages would be a menu of methods); lockfiles; no internet in the agent phase (unlike TBS, because DeepEcon's source packages are public); no live downloads; open-source software, or the licensed track. | The type's standard R or Python image, data baked in. | Requires Stata (licensed track only). | Task-specific packages; run-time downloads; unpinned packages. | Shepherd · Stage 5; automated · Stage 6 (L0) |
| **EN-2** | **Hackability reviewed** (§6). | Cheat trials (L8 f); root-cause explanation for any hack; oracle and alternatives re-run after fixes (§6: "a fixer can make the task impossible too"). | No hack found. | Hack found and fixed at its root. | Known hack unfixed. | Shepherd · Stage 6 (L8); benchmark reviewer · Stage 7 |
| **EN-3** [G] | **Licensing** permits distributing the data and code for evaluation. | Licence records per asset; the **data route** (VVP §6). Derived data (effect-injected, perturbed, semi-synthetic on real covariates) inherit the licence. Restricted sources: **fully synthetic data only** (disclosure review; provider permission where required), with GT-1 and RV-2 re-run and the consequence re-demonstrated on them. | Redistributable (perhaps evaluation-only), or fully synthetic with those checks re-run. | Permission pending. | Restricted microdata, or data derived from them, in any task material. | Shepherd · Stage 0 (screen), Stage 5 (data built) |
| **EN-4** [G] | **Verifier isolation and task security.** Agent code that the verifier re-executes runs unprivileged, in a separate container, without network access, and cannot write the reward. Every "do not modify" in the instruction is enforced. [TBS `verifier_execution_isolation`, `task_security`, `do_not_modify_enforced`] | Verifier configuration review; attack L8 (j), in which agent code tries to write the reward file or read hidden data. | Isolated and enforced. | — | Agent code can influence its own grade. | Benchmark reviewer · Stage 6 (L8), Stage 7 |

## 8. Leakage and contamination

*The brief's Safeguard F; economics-specific because the source papers and many packages are public. Exposure rules: VVP §10.*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **LK-1** [G] | **Tier separation.** Nothing from the hidden tier is in the agent's environment. | Automated scan of agent-tier files for hidden IDs, failure-mode text, patch annotations, key values, target outputs, and flawed code. In correction and detection tasks the presented package is flawed by design; LK-3 covers it. | Clean scan. | — | Any hit. | Automated · Stage 5 (before the blind solves), Stage 6 (L0), Stage 8 |
| **LK-2** | **Contamination resistance (numbers).** Memorized published numbers do not solve the task. | Perturbed or fully synthetic data, per the data route; answer-changing hidden variants on bases the agent never sees (VVP §5.1); attacks L8 (a) and (g). | Published numbers fail the verifier on the main data. | Published numbers fail only on hidden variants (the main-data answer is the published one). | Published numbers pass, or the differential attack passes. | Shepherd · Stage 6 (L8) |
| **LK-3** | **Natural presentation.** The flawed package carries no tell-tale signs. | Naturalness review: no comments, names, formatting changes, or diff artifacts marking the change. Variant and clean twin share one restructured presentation, so neither a diff against the public package nor a style difference reveals the change. | Reviewer cannot spot the change without methodological reasoning. | Minor stylistic asymmetry. | The change is visible from style alone. | Shepherd · Stage 4; benchmark reviewer · Stage 7 |
| **LK-4** [G] | **Recognition probe.** Memory of the paper or package does not solve the task. | Each calibration model, given only the agent tier, is asked to name the paper and the original choice at the crux (`recognition_probe` runs; L8 e). | None can. | Recognized but disguised (variables, files, setting, and identifiers re-keyed; both twins restructured identically), with recognized and unrecognized scores reported separately. | Recognized and undisguised in the held-out split. | Shepherd · Stage 6 (L8) |
| **LK-5** [G] | **Exposure log** complete; no hidden-tier exposure outside no-training terms. | Log (internal tier) of every session, trial, and LLM call that saw hidden-tier material, with its terms (VVP §10); held-out tasks count external evaluations toward the refresh limit. | Complete; all exposures under commercial no-training terms (zero data retention where available). | — | A gap, or hidden-tier material seen under consumer terms, even after an opt-out. | Shepherd · Stage 2; benchmark reviewer · Stage 8, and before each release |

## 9. Provenance and human authority

*Brief §5.5 (D-008); Good Benchmarks §9 "Keep authorship and review human".*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **PR-1** [G] | **Complete provenance and measured AI influence.** Every scientific assertion records its origin, exposure (pre- or post-suggestion), and the contributor's disposition; influence is measured, not self-reported (experts adopt and restate AI arguments without crediting them: [R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) §3.4). | Provenance and exposure fields; free-recall lists; suggestion ledger; LLM-originated, post-exposure, and LLM-influenced shares; false-endorsement rate on known-valid controls. | Core items pre-exposure; suggestions explicitly endorsed with an evidence bundle or rejected. | LLM-influenced share above 50% of endorsed items, or adjudicated false endorsement of over 25% of known-valid controls (provisional; [pilot plan](../pilot/pilot-evaluation-plan.md) §7): deeper review (§9: "hill climbing toward a hard task that is too artificial"). | Unendorsed LLM content presented as the contributor's. | Automated + shepherd · Stage 2 |
| **PR-2** [G] | **Independent review.** At least one domain economist outside the contribution **who has attempted the task blind, with the attempt recorded** (SP-1), and one benchmark reviewer who has built tasks before (§9), qualified under VVP §11. | Review records with conflict-of-interest statements; the domain reviewer's `expert_solve` run. | Both reviews complete; concerns resolved. | Reviews converge only after more than three rounds (§8 red flag). | No independent review, or no recorded blind attempt. | Release editor · Stage 7 |

## 10. Documentation

*TBS README and metadata criteria [`difficulty_explanation_quality`, `solution_explanation_quality`, `verification_explanation_quality`, `expert_time_estimate`].*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **DC-1** | The task README explains, for reviewers: why the task is hard for humans and agents, and who does this work in practice (without citing pass rates); the reference solution's strategy and key insight; what the verifier checks, why that suffices, and how each band was set (VVP §4 item 6). | README review. | Complete and consistent with the code. | Gaps. | Missing or inconsistent with the code. | Shepherd · Stage 6; benchmark reviewer · Stage 7 |
| **DC-2** | Metadata: design type, primary and secondary layers, tier per graded output, data route, licences, JEL codes, an expert time estimate from the blind solves (SP-1), and any `recognition_task` tag (SP-3). | Schema validation; reviewer check. | Complete. | Partial. | Missing. | Automated + shepherd · Stage 6 |

---

## Criteria by construction stage

Derived from *Who / when*; each row is that stage's gate line in the [construction protocol](benchmark-construction-protocol.md). Stage 7 reviewers also re-check the full rubric (PR-2).

| Stage | Gates [G] | Also assessed |
|---|---|---|
| 0 Selection | EN-3 | — |
| 1 Replication | GT-1 | — |
| 2 Interview | RV-1, LK-5, PR-1 | — |
| 3 Error identification | RV-3 | — |
| 4 Flawed implementation | RV-2, RV-3 | LK-3 |
| 5 Task construction | RV-4, GT-1 (if a blind solve is the check), SP-1, EN-1, EN-3, LK-1 | GT-3, SP-2, SP-4 |
| 6 Verification | GT-2 (after L7), SP-3, SO-1, VE-1, VE-2, VE-4, EN-1, EN-4, LK-1, LK-4 | GT-4, SP-4, SO-2, SO-3, VE-3, VE-5, DF-1, DF-3, EN-2, LK-2, DC-1, DC-2 |
| 7 Review | RV-3, RV-4, GT-1, GT-2, SP-1, VE-4, EN-4, PR-2 | GT-4, SP-2, DF-2, EN-2, LK-3, DC-1 |
| 8 Admission | LK-1, LK-5 | — |

## Red flags (from §8, adapted to economics)

None is disqualifying alone; each is a reason to look closer.

- The pass rate swings with a tiny change — a package version (e.g., an estimator library update), a pre-installed package, or a small hint.
- Several agents converge on the **same wrong answer**. In economics, first check whether that answer is a valid alternative the verifier wrongly rejects. (TBS: "Recurring 'misunderstandings' by independent agents are evidence of ambiguity.")
- Review keeps returning critical concerns after two or three rounds.
- The instruction has a large surface (many files to read, many deliverables).
- The reference solution states the answer instead of deriving it, or uses information the agent does not have.
- The task is too synthetic to correspond to real research.
- Run-to-run variance in pass rate or cost is high.

## Change control

The rubric is versioned (`rubric_version`); each assessment records the version used. Changes follow the [decision log](../decisions/decision-log.md): wording clarifications are patch versions; new or removed gates and changed thresholds are minor versions. **New gates apply to already admitted tasks before the next release**: a task that fails one is repaired or withdrawn at that release, since a release's contents are frozen (VVP §8).

## Changes

**v0.2.0** (independent reviews, 2026-11-05):
- *Who / when* is the single map from criteria to construction stages and VVP rungs, summarized by stage (C/T/A codes retired). New gates LK-4 and LK-5: 36 criteria, 20 gates.
- Aligned with VVP v0.3.0: RV-2 (materiality rule), GT-1 to GT-4, SP-1 (blind solves), SP-3 (hint ladder; O-004 stays Open), SP-4, VE-1 to VE-5, EN-1, EN-3 (data routes), LK-1 to LK-3.
- Numeric anchors for SO-3, DF-1, DF-3, and PR-1; PR-2 and DC-2 tied to blind solves; stricter change control; a §9 quotation (PR-1) and a cross-reference (RV-4) corrected.

**v0.1.0** (2026-11-05): first version (34 criteria, 18 gates, stages C/T/A).
