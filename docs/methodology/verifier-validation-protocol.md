# Verifier Validation Protocol

| | |
|---|---|
| **Status** | **Proposed** v0.1.0 (2026-11-05). Part of Deliverable 2. Not yet reviewed by the research lead. |
| **Purpose** | Establish, with recorded evidence, that a task's verifier accepts correct work and rejects scientifically consequential mistakes, so that the benchmark score means what it claims. |
| **Inputs** | A task candidate with a reference implementation, at least one validated flawed variant, and a draft verifier (see the [construction protocol](benchmark-construction-protocol.md)). |
| **Outputs** | `validationRun` records (see the [schema](../../schemas/README.md)) and a pass/fail decision on rubric criteria VE-1 to VE-5, SO-1 to SO-3, DF-1, EN-2, LK-1 and LK-2 ([rubric](task-quality-rubric.md)). |
| **Evidence labels** | Literature claims are labelled per project convention; method references marked [U] are pending verification in [evidence note R6](../research/evidence/R6-error-detection-and-verifier-methodology.md). |

## 1. Why a flawed implementation is not enough

The research lead's brief (§4) states the core difficulty: "A deliberately flawed implementation is not sufficient by itself to establish that a task is good." Three distinct failures can hide behind a verifier that "rejects the flawed version":

1. **Over-fitting to one wrong answer.** The verifier rejects the specific flawed output but accepts other wrong answers. This is the negative-side version of the verifier "co-designed with the author's own solution" (*Good Benchmarks* §7).
2. **Rejecting valid alternatives.** The verifier rejects a different estimator that identifies the same estimand (many-analysts dispersion).
3. **Coincidence (the equivalent-mutant problem).** On the evaluation data, the flawed procedure gives the same answer as the correct one, so no outcome check can separate them. Mutation testing calls such variants *equivalent mutants*. Here the equivalence may be data-specific: two-way fixed effects matches heterogeneity-robust estimators when effects happen to be homogeneous.

The protocol below attacks each failure with a different kind of evidence.

## 2. Definitions

- **Acceptance region.** The set of outputs the verifier accepts for a given input dataset (e.g., an interval around the reference estimate whose width is justified by the dispersion of valid implementations and numerical noise).
- **Correct-acceptance rate.** Share of validated correct solutions (reference plus alternatives) accepted across all inputs. Target: 100%.
- **Flaw-rejection rate.** Share of validated flawed variants rejected across all inputs. Target: 100% on the main data, at least 95% per variant across hidden variants.
- **Separation margin.** Distance from a flawed output to the acceptance region, in units of the region's half-width.
- **Hidden variants.** Datasets the agent never sees, on which the verifier re-runs the agent's code: resamples, semi-synthetic outcomes with known effects, and metamorphic transformations.
- **Kill.** A flawed variant is killed when some verifier check rejects it (mutation-testing terminology).

## 3. The validation ladder

Run the rungs in order; a failure sends the task back to the shepherd. Each run is stored as a `validationRun`.

| Rung | Run kind | What it establishes | Pass condition | Automatable? |
|---|---|---|---|---|
| L0 | Static checks | Package integrity | Schema valid; tiers correct; leakage scan clean (LK-1); environment pinned and offline (EN-1). | Yes |
| L1 | **Oracle** | Solvability from agent-facing materials (SO-1); verifier accepts correct work | Reference solution, run inside the task environment with no privileged files, is accepted. | Yes |
| L2 | **No-op / null** | Verifier is not trivially satisfied | Empty, missing, or default outputs rejected. | Yes |
| L3 | **Alternative valid implementations** | Verifier credits other correct paths (GT-4, VE-1) | Every validated alternative accepted on main data and all hidden variants. | Run: yes; choosing alternatives: human |
| L4 | **Negative controls (expert flawed variants)** | Verifier rejects consequential mistakes (VE-2) | Every validated flawed variant rejected; separation margin recorded; flagship variant killed on main data. | Run: yes; designing variants: human |
| L5 | **Mutation analysis (artificial mutants)** | Verifier sensitivity beyond the expert variants | Report a mutation score over automatically generated mutants (drop a fixed effect, change the cluster variable, shift treatment timing by one period, alter a sample filter, flip a sign). Investigate survivors; classify each as an equivalent mutant (ignore), a verifier gap (fix), or a valid alternative (add to L3). | Yes, with human triage |
| L6 | **Metamorphic relations** | Procedure-level correctness without exact keys (VE-3) | Relations in §5 hold for the reference and all alternatives; relevant relations are violated by the flawed variants they target. | Yes |
| L7 | **Hidden-variant separation** | The flaw is not an equivalent mutant for the evaluation (DP-05) | Each flawed variant rejected on ≥ 95% of hidden variants; each correct solution accepted on 100%. | Yes |
| L8 | **Shortcut and adversarial attacks** | Score cannot be obtained without the capability (VE-4, EN-2) | All fail: hard-coded published coefficients; memorized values; null outputs; copying any file in the environment; "flag everything" answers for detection tasks; diffing against the public source package; an adversarial agent instructed to obtain the reward without doing the work (cheat trial). | Mostly yes |
| L9 | **Repeat stability** | No flakiness (VE-5) | Hundreds of repeated verifier runs (*Good Benchmarks* §1) with zero spurious failures. | Yes |
| L10 | **Guided-agent fairness** | Verifier is fair conditional on the method (SO-3; *Good Benchmarks* §7) | With the method named in a temporary instruction, strong agents pass. | Yes, with human reading of failures |
| L11 | **Agent trials and crux alignment** | Difficulty is intrinsic and located where claimed (DF-1, DF-3) | Batches of five trials per configuration across several models; failures read by the shepherd; failures occur at the stated crux. | Runs: yes; analysis: human |
| L12 | **Independent review** | Domain correctness and benchmark correctness (PR-2, SP-1) | Domain reviewer and benchmark reviewer sign off; dual-verifier specification test passes. | No |
| L13 | **Post-admission monitoring** | Validity over time | Issue reports and task repairs (as in Terminal-Bench-Science); re-run L1–L9 when the environment changes. | Partly |

## 4. Designing the acceptance region

1. **Start from the estimand, not the estimator.** The instruction defines the target quantity precisely (*Good Benchmarks* §4: "tightening the instruction is usually the simpler fix").
2. **Measure legitimate dispersion.** Run every validated alternative implementation, plus reference runs with different seeds for stochastic procedures. The region must contain all of them.
3. **Add a justified numerical tolerance** (expressed in reference standard-error units or relative terms), recorded with its justification.
4. **Check discrimination.** If the region now contains a flawed variant's output, the task is not discriminating on this data: tighten the estimand, choose a different target analysis, rely on hidden variants that separate them (L7), or demote the task to a structured-judgment tier.
5. **Avoid knife-edge decisions.** Never key a task on a significance decision when the reference p-value is near the threshold; small legitimate differences would flip it.
6. **Inference outputs.** Compare standard errors with relative tolerances; compare confidence intervals by endpoints. Inference errors (e.g., wrong clustering level) are often better verified through metamorphic relations (§5) than through a single standard error.

## 5. Econometric metamorphic relations

A metamorphic relation states how the output must change when the input is transformed. It verifies procedure without an exact answer key. Each relation must first be checked on the reference and on all alternatives.

| Transformation of the input | Required behaviour of a correct procedure | Typical flaw it exposes |
|---|---|---|
| Multiply the outcome by a constant *c* | Coefficients and standard errors scale by *c*; t-statistics unchanged | Hard-coded values; ad hoc transformations |
| Add a constant to the outcome | Slope coefficients unchanged (model with intercept or fixed effects) | Mis-specified normalization |
| Permute the row order | All outputs unchanged | Order-dependent data manipulation, unstable sorting in panel construction |
| Relabel unit identifiers consistently | All outputs unchanged | Identifier-dependent merges or clustering mistakes |
| Shift every calendar date by a constant | Event-time effects unchanged | Treatment timing tied to calendar values instead of adoption dates |
| Duplicate the panel with fresh cluster identifiers | Point estimates unchanged; cluster-robust standard errors shrink by about 1/√2 | Clustering on the wrong variable; non-clustered errors |
| Randomly reassign treatment (placebo) | Estimates centred on zero across draws | Mechanical correlation introduced by the procedure |
| Inject known heterogeneous effects into semi-synthetic outcomes | A heterogeneity-robust estimator recovers the injected aggregate effect | Static two-way fixed effects under staggered adoption |
| Add never-treated units whose outcomes are generated with zero effect | Robust estimators stable; contaminated comparisons move | Forbidden comparisons in staggered designs |

## 6. Semi-synthetic data: uses and dangers

Semi-synthetic datasets keep the real design (covariates, treatment timing, cluster structure) and simulate outcomes with a known effect and realistic noise. Data-analysis competitions in causal inference have used this approach [U: e.g., the ACIC data challenge, Dorie et al. 2019 — verify in R6]. It supplies known ground truth for statistical-validity tasks (tier V2) and defeats memorized published results.

*Good Benchmarks* §7 names the danger directly: "When you generate the data from a hypothesis, the verifier can quietly encode an assumption only you hold." Safeguards:

- The data-generating process is documented in the hidden tier and reviewed by an independent economist.
- Every validated alternative estimator must recover the truth on the semi-synthetic data (L3); if only the contributor's estimator does, the generating process encodes that estimator's assumptions.
- Calibrate realism: noise and heterogeneity magnitudes are plausible for the setting, not tuned to maximize the gap between the correct and flawed procedures.
- Record coverage of the reference procedure's confidence intervals across simulations (a simulation-based calibration check).

## 7. Verification by validity layer

| Validity layer | What can be verified objectively | Recommended tier and methods | What cannot be verified objectively |
|---|---|---|---|
| Computational correctness | The code implements the stated design | V1: numeric tolerance, intermediate outputs (sample size, number of clusters), hidden-variant re-execution | — |
| Statistical validity | The procedure is appropriate for the estimand and design | V2: semi-synthetic known truth, metamorphic relations, established statistical results | Choices among valid procedures with different finite-sample trade-offs |
| Identification validity | Whether stated falsification tests were run correctly, and how their results come out | V2 for the computational part of tests; V3 for recognizing threats (structured key validated by inter-expert agreement) | Whether untestable assumptions hold |
| Interpretation validity | Whether specific claims follow from given results | V3: claim classification with an expert-consensus key; contested claims excluded or keyed as an acceptable set | Nuanced judgments where credible experts disagree |

**Agreement standard for V3 keys (proposed).** At least three independent economists label each item without seeing one another's labels. An item enters the scored set only if all three agree (or a pre-registered agreement statistic clears a pre-registered threshold), with written rationales and citations. Disagreement is evidence that the item is contested; such items go to the experimental track.

**LLM-as-judge (V4).** Useful for triage and review assistance; never the sole grader of a scored task. *Good Benchmarks* §7: an LLM judge "will find some issues, but not everything." Any LLM-judged track reports agreement with human graders.

## 8. Division of labour

| Activity | Automated | Shepherd | Contributor | Independent reviewers |
|---|---|---|---|---|
| Static checks, leakage scan | ✔ | reviews hits | — | — |
| Oracle, null, repeat stability, metamorphic runs | ✔ | interprets | — | — |
| Designing flawed variants | — | assists | ✔ (scientific content) | domain reviewer checks |
| Selecting alternative valid implementations | — | ✔ | ✔ | domain reviewer checks |
| Mutation analysis | generates and runs | triages survivors | — | — |
| Designing hidden variants and semi-synthetic data | runs | ✔ | consulted | domain reviewer checks |
| Shortcut and cheat trials | ✔ | designs attacks | — | benchmark reviewer checks |
| Agent trials and crux alignment | runs | ✔ (reads trajectories) | consulted on surprising failures | — |
| Dual-verifier specification test | — | organizes | — | ✔ |
| Admission decision | — | recommends | — | ✔ (release editor decides) |

## 9. References (to be verified)

Pending verification in evidence note R6 ([U] until then): DeMillo, Lipton & Sayward (1978) on mutation testing; Chen, Cheung & Yiu (1998) on metamorphic testing; Barr et al. (2015) on the test-oracle problem; Knight & Leveson (1986) on correlated failures in independently developed program versions (relevant to independent reference implementations); Dorie et al. (2019) on the ACIC causal-inference data challenge. Primary: Bercovich (2026), *Good Benchmarks* [P-full].
