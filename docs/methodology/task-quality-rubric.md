# Task-Quality Rubric for Economics Benchmark Tasks

| | |
|---|---|
| **Status** | **Proposed** v0.1.0 (2026-11-05). Part of Deliverable 2. Not yet reviewed by the research lead. |
| **Primary basis** | Bercovich (2026), *Good Benchmarks* — [reading notes](../research/reading-notes/good-benchmarks-bercovich-2026.md) (§ numbers below refer to the paper) |
| **Also informed by** | Terminal-Bench-Science (TBS) proposal, implementation (39 criteria), trial-analysis, and cheat-analysis rubrics, Apache-2.0 ([evidence note R1](../research/evidence/R1-terminal-bench-science.md)); the research lead's brief §4 and §10. Criteria adapted from TBS name their TBS counterpart in brackets. |
| **Used by** | Contributors (self-assessment), shepherds, independent reviewers, automated checks; recorded as `rubricAssessment` in the [schema](../../schemas/README.md) |

## How to use this rubric

*Good Benchmarks* defines seven properties of a good task. A checklist that asks "Is the task verifiable? yes/no" invites generic answers, which the research lead explicitly ruled out (brief §4). Each criterion below therefore names **the evidence that settles it**, gives **economics-specific anchors** for pass, concern, and fail, and says **who assesses it, and when**.

- **Ratings:** `pass` · `concern` (acceptable only with a written resolution) · `fail` · `not_applicable`.
- **Gates.** Criteria marked **[G]** are gates: one `fail` blocks progression to the next stage. Other criteria accumulate; a reviewer may still reject a task with several unresolved concerns.
- **Stages.** **C** = candidate (end of the interview, before task engineering) · **T** = task (after the shepherd builds the task and verifier) · **A** = admission (independent review before release).
- **No numeric total.** Summing criteria hides the failure that matters. Decisions cite the specific criteria.
- **Standard of evidence (§9).** "This is standard in our field" is not evidence. A disputed methodological claim is settled by an authoritative citation, a simulation, or an independent reviewer's demonstration.

---

## 1. Scientific relevance and realism

*Good Benchmarks #5 "Realistic and valuable", §2 "Start from real work".*

| ID | Criterion | Evidence that settles it | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **RV-1** [G] | The task mirrors work economists or research assistants are actually paid to do. | Mapping from the task to a real activity (implementing a design, replicating a result, auditing code, refereeing an empirical analysis); grounding in a published target analysis. | "Re-estimate Table 2's main effect from the provided panel" or "find and fix the problem in this estimation script." | Realistic activity but an unusual framing that needs justification. | A quiz, a puzzle, or trivia ("Which estimator did Callaway and Sant'Anna propose?"). | Contributor, shepherd · C |
| **RV-2** [G] | The decision under test is **consequential**: getting it wrong changes a scientifically meaningful quantity. | Consequence evidence under a pre-registered materiality rule (e.g., shift > 1 reference SE, sign change, significance-decision change, a contributor-justified change in interpretation). | Wrong clustering halves the SE and flips significance. | Material only on some outputs or in some samples. | Changes only labels, formatting, or a third decimal place (brief X-002). | Shepherd · T |
| **RV-3** [G] | The failure mode is **realistic**: competent researchers plausibly make it. | Realism warrant with at least one type: the contributor's own research, refereeing, or supervising experience; a published comment or replication; methodological literature documenting the pitfall; observed AI-agent behaviour. | Documented in the literature and seen in RA code. | Plausible by argument only, no documented instance. | An artificial code mutation nobody would write (brief §10G, X-005). | Contributor · C; domain reviewer · A |
| **RV-4** [G] | The **target capability** is stated precisely, and the verifier measures that capability rather than a proxy. | One-sentence capability statement; reviewer check that an agent lacking the capability cannot pass by another route (see SH-1 to SH-4). | Capability: "recognize that staggered adoption with dynamic effects invalidates static TWFE, and recover the estimand." Verifier checks the recovered estimand on hidden variants. | Capability broader than what the verifier checks. | The task claims to test identification reasoning but grades a number reachable mechanically (brief §10B). | Shepherd · T; benchmark reviewer · A |

## 2. Ground truth and scientific defensibility

*Good Benchmarks #1 "Verifiable" and §5; the brief's distinction among computational, statistical, and identification validity (§4, D-013).*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **GT-1** [G] | The **reference implementation** is validated. | Reproduction status versus the published result (exact, within tolerance, or discrepancy explained) **and** an independent check: a cross-language re-implementation, a line-by-line review by someone other than its author, or a simulation check. | Original Stata package and independent R re-implementation agree within tolerance; discrepancies with the paper are explained. | Reproduces the paper but has no independent check yet. | Matches published coefficients with no independent check, while the task depends on details the published numbers do not pin down (brief §3.2: "matching published coefficients does not automatically establish scientific correctness"). | Shepherd · T; domain reviewer · A |
| **GT-2** [G] | The failure mode is **genuinely wrong**, not an alternative valid approach. | Status: `established` (consensus; cite), or `conditional` (wrong under stated assumptions shown to hold here; cite and justify). | Established pitfall with citations; contributor and reviewer agree. | Conditional status whose conditions are argued but not demonstrated. | `contested` status used for a binary-keyed task (D-013, X-003). | Contributor · C; domain reviewer · A |
| **GT-3** | The **validity layer** is identified, and the verifiability tier fits it. | Layer: computational, statistical, identification, or interpretation. Tier: V1 deterministic computational; V2 statistical with known truth; V3 structured judgment with an expert-consensus key; V4 open-ended judgment. | Statistical-validity error verified at V2 with semi-synthetic known truth. | Identification-layer task at V3 without an agreement study yet. | Identification claim graded as if it were V1 (an untestable assumption treated as a number). | Shepherd · T |
| **GT-4** | **Alternative valid implementations** are identified and credited. | List of look-alike valid approaches; each validated alternative is run and accepted by the verifier. | Callaway–Sant'Anna, Sun–Abraham, and imputation estimators all accepted for an ATT estimand they share. | Alternatives listed but not all run. | Verifier accepts only the contributor's estimator when others identify the same estimand (§7: verifier "co-designed with the author's own solution"). | Shepherd · T; benchmark reviewer · A |

## 3. Specification

*Good Benchmarks #2 "Well-specified", §4 "Focus on the outcome", §9 on authorship.*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **SP-1** [G] | The instruction states the **required outcome** precisely enough that meeting it implies passing the verifier. [TBS `well_specified`, `test_instruction_alignment`] | **Dual-verifier test** (§1): two economists independently write acceptance criteria from the agent-facing instruction alone; their criteria agree on every reference, alternative, and flawed output. Every verifier assertion maps to a stated requirement, and vice versa. Where conventions legitimately differ (small-sample corrections, singleton handling, degrees of freedom), the instruction states the convention or the verifier accepts every defensible one. | Both accept the same answers. | Agreement only after a clarification that is then written into the instruction. | Disagreement on what counts as correct. | Shepherd + one independent economist · T |
| **SP-2** | The instruction is **short, in practitioner language, and human-written or substantially human-edited.** | Authorship record; instruction length; reviewer reading. | Two paragraphs a referee would write; goal stated first. | Longer than necessary; some LLM-style scaffolding. | LLM-drafted and unedited; enumerates steps instead of the goal (§4, §9). | Shepherd · T; benchmark reviewer · A |
| **SP-3** [G] | Difficulty does **not** come from a hidden fact, an unstated convention, or ambiguity. | **One-sentence-fact probe** (§9): state the disputed or key fact in a temporary instruction; record how difficulty changes. Disclosure of *the design's structure* (data, timing, assignment level) must already be in the instruction. | Disclosing the method makes the task easy, but recognizing the method from the disclosed design *is* the capability under test (record why). | Collapse to trivial on disclosure and no argument that recognition is the capability. | The task is hard only because the data's structure or the estimand is not described. | Shepherd · T |
| **SP-4** | The **output contract** is minimal and self-checkable. | Results-file schema provided in the agent environment; format validator available to the agent. | One small JSON file plus a code entry point; the agent can validate its format. | A complex structure without a validator. | Failures dominated by formatting (§3: "measuring format compliance"). | Shepherd · T |

## 4. Solvability

*Good Benchmarks #3 "Solvable", §5 "Prove the task is solvable", §7 fairness check.*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **SO-1** [G] | A **reference solution works from the agent-facing materials only** and follows the path a researcher or agent would take. | Oracle run in the task environment with no privileged files; for diagnostic tasks, the oracle investigates (runs diagnostics) before fixing (§5). | Oracle reproduces the target outputs from the provided data and instruction. | Oracle uses a documented heuristic an expert would use but the instruction does not mention. | Oracle hard-codes the answer or reads hidden files. | Shepherd · T |
| **SO-2** | The task is feasible within stated time and compute limits. | Measured oracle runtime, memory, and agent-trial durations. | Comfortably within limits on the reference hardware. | Close to the limit. | Exceeds the limit or depends on unavailable software. | Automated · T |
| **SO-3** | **Guided-agent fairness check** (§7): with the method temporarily named, a strong agent passes. | Agent trials on an over-specified variant of the instruction. | Guided agents pass, so the remaining difficulty lies in choosing or recognizing the method. | Guided agents pass inconsistently. | Guided agents fail — look at the verifier or the environment. | Shepherd · T |

## 5. Verification

*Good Benchmarks #1 "Verifiable", #6 "Outcome-verified", §7 "Make the verifier mean something".*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **VE-1** [G] | The verifier **accepts every correct solution**: the reference and all validated alternatives, on the main data and all hidden variants. | Validation runs of kind `oracle`, `alternative_solution`, `hidden_variant`. | 100% acceptance. | Rare rejections explained by numerical tolerance, with tolerance widened. | Any validated correct solution is rejected. | Automated + shepherd · T |
| **VE-2** [G] | The verifier **rejects every validated flawed variant**, with margin, robustly. [TBS `verification_explanation_quality`] | Negative-control runs; separation margin; share of hidden variants on which the flawed output is rejected. The flagship flawed variant must not be an "equivalent mutant" (numerically indistinguishable on the evaluation data). Separation is measured against a structurally independent correct implementation (a "witness"), and any comparator that "failed to fail" is reported, not hidden. | All flawed variants rejected on ≥ 95% of hidden variants; margin several tolerance widths. | Rejected on the main data only. | Some validated flawed variant passes. | Automated + shepherd · T |
| **VE-3** | The verifier grades **outcomes**, and tests **procedure** through outcomes. | Verifier design: re-execution of the agent's code on hidden variants and metamorphic relations, rather than inspection of code or libraries (§7: "tests should verify outcomes, not implementations"). | Agent's code re-run on hidden semi-synthetic variants; outputs compared to the reference on the same inputs. | Single-dataset numeric check only (vulnerable to memorization). | Verifier checks which package or function was used. | Shepherd · T |
| **VE-4** [G] | **Shortcut resistance.** | Attack runs: (a) published coefficients hard-coded; (b) no-op or empty output, and trivial nulls (constant, mean, zero effect, identity) on every hidden instance [TBS `graded_instances_discriminate`]; (c) answer copied from any file in the environment; (d) generic "flag everything" answer for detection tasks; (e) diff against the public source package where applicable; (f) an adversarial agent briefed to obtain the reward without doing the work, including by locating the original package online [TBS cheat trials]. | All attacks fail. | An attack fails only because of an incidental detail. | Any attack passes. | Automated + benchmark reviewer · T, A |
| **VE-5** | **Verifier stability and boundary fairness.** [TBS `deterministic_reproducible`, trial-analysis `boundary_fairness`] | Repeat runs (target: hundreds, §1; TBS asks for 100+ for stochastic tasks) with fixed seeds; tolerance justified by the dispersion of valid solutions; outcomes near the acceptance boundary reflect real quality differences, not seeds or conventions. | Zero spurious failures; no knife-edge decisions. | Rare flakes, root cause known and fixed. | Flaky outcomes, or pass/fail decided by noise near a threshold. | Automated · T |

## 6. Difficulty

*Good Benchmarks #4 "Difficult", §3 "What difficulty actually means", §8 "Run the task and watch it fail".*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **DF-1** | Difficulty is **intrinsic** to the economics, confirmed by **crux alignment**: agents that fail, fail at the stated crux. | Agent trials (batches of five per configuration, §8) with failure analysis. | Failing trajectories use static TWFE or the wrong clustering level — the stated crux. | Mixed failure causes. | Failures come from environment problems, formatting, or misread instructions. | Shepherd · T |
| **DF-2** | The task is **one coherent problem**, not a concatenation, not "too wide", not a trick. | Instruction review; count of deliverables. | One estimand, one decision at stake. | Two related decisions. | Many small deliverables, or a misleading hint (§3). | Benchmark reviewer · A |
| **DF-3** | Difficulty is **calibrated** and recorded. | Pass rates of several frontier agent configurations. | Recorded; neither trivially solved nor universally failed for non-crux reasons. | Universally failed but crux-aligned (keep, flag as frontier). | Trivially solved by all configurations. | Shepherd · T |

## 7. Environment robustness

*Good Benchmarks #7 "Robust", §6 "Build a controlled environment".*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **EN-1** [G] | **Pinned, offline, reproducible** environment. | Pinned container image and package versions (lockfiles for R and Python); no internet in the agent phase (a deliberate departure from TBS, whose agents have open internet, because DeepEcon's source packages are public); no live data downloads; open-source software, or explicitly marked licensed track. The set of pre-installed econometrics packages is documented, because it can change difficulty (*Good Benchmarks* §8 red flag). | R or Python with pinned packages, data baked in. | Requires Stata (licensed track only). | Downloads data at run time; unpinned packages. | Automated · T |
| **EN-2** | **Hackability reviewed** (§6). | Adversarial "cheat" trials; root-cause explanation for any hack; oracle re-run after fixes. | No hack found. | Hack found and fixed at its root. | Known hack unfixed. | Benchmark reviewer · A |
| **EN-3** [G] | **Licensing** permits distributing the data and code for evaluation. | Licence records per asset. | Redistributable (perhaps evaluation-only). | Permission pending. | Not redistributable and no substitute (synthetic or semi-synthetic) data. | Shepherd · T |
| **EN-4** [G] | **Verifier isolation and task security.** Agent code that the verifier re-executes runs unprivileged, in a separate container, without network access, and cannot write the reward. Every "do not modify" in the instruction is enforced. [TBS `verifier_execution_isolation`, `task_security`, `do_not_modify_enforced`] | Verifier configuration review; an attack run in which agent code tries to write the reward file or read hidden data. | Isolated and enforced. | — | Agent code can influence its own grade. | Benchmark reviewer · T, A |

## 8. Leakage and contamination

*The brief's Safeguard F; economics-specific because the source papers and many packages are public.*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **LK-1** [G] | **Tier separation.** Nothing from the hidden tier is in the agent's environment. | Automated leakage scan of agent-tier files (hidden IDs, flawed code fragments, key values, target outputs). | Clean scan. | — | Any hit. | Automated · T, A |
| **LK-2** | **Contamination resistance.** Memorizing the published paper or package does not solve the task. | Perturbed or semi-synthetic data; hidden-variant re-execution; a test that the published coefficients fail. | Published numbers fail the verifier. | Published numbers fail only on hidden variants. | Published numbers pass. | Shepherd · T |
| **LK-3** | **Natural presentation.** The flawed package carries no tell-tale signs. | Naturalness review: no comments, names, formatting changes, or diff artifacts that mark the planted change; where memorization of the public package would be a shortcut, the code is restructured or re-implemented. | Reviewer cannot spot the change without methodological reasoning. | Minor stylistic asymmetry. | The change is visible from style alone. | Benchmark reviewer · A |

## 9. Provenance and human authority

*Brief §5.5 (D-008); Good Benchmarks §9 "Keep authorship and review human".*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **PR-1** [G] | **Complete provenance.** Every scientific assertion records its origin and the contributor's disposition; LLM-originated items were endorsed with the contributor's own reasoning. | Provenance fields; interview record; share of LLM-originated items. | Contributor-originated core, LLM suggestions explicitly endorsed or rejected. | Majority of items LLM-originated (triggers deeper review, §9 "hill climbing toward a task that is too artificial"). | Unendorsed LLM content presented as the contributor's. | Automated + shepherd · C, T |
| **PR-2** [G] | **Independent review.** At least one domain economist not involved in the contribution, who could solve the task, and one benchmark reviewer who has built tasks before (§9). | Review records with conflict-of-interest statements. | Both reviews complete; concerns resolved. | Reviews converge only after more than three rounds (§8 red flag). | No independent review. | Release editor · A |

## 10. Documentation

*TBS README and metadata criteria [`difficulty_explanation_quality`, `solution_explanation_quality`, `verification_explanation_quality`, `expert_time_estimate`].*

| ID | Criterion | Evidence | Pass | Concern | Fail | Who / when |
|---|---|---|---|---|---|---|
| **DC-1** | The task README explains, for reviewers: why the task is hard for humans and agents, and who does this work in practice (without citing pass rates); the reference solution's strategy and key insight; what the verifier checks, why that suffices, and how each tolerance was calibrated. | README review. | Complete and consistent with the code. | Gaps. | Missing or inconsistent with the code. | Shepherd · T; benchmark reviewer · A |
| **DC-2** | Metadata: design type, validity layer, verifiability tier, JEL codes, a plausible expert time estimate, data licences. | Schema validation; reviewer check. | Complete. | Partial. | Missing. | Automated + shepherd · T |

---

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

The rubric is versioned (`rubric_version`); each assessment records the version used. Changes follow the [decision log](../decisions/decision-log.md): wording clarifications are patch versions; new or removed gates are minor versions and require re-assessment only of tasks not yet admitted.
