# Verifier Validation Protocol

> **Note (2026-11-06).** The contributor workflow changed: the team prepares candidate errors and contributors review them in a self-hosted interface, with no AI interview; AI use follows the [AI use and integrity rules](../architecture/llm-use-policy.md) (2026-11-07) ([revised requirements](../requirements/2026-11-06-research-lead-revision.md); [MVP proposal](../architecture/mvp-contributor-interface.md)). This document remains the team's internal methodology for turning confirmed candidates into verified tasks, to be aligned with the three verification rounds of the [team's plan](../requirements/2026-11-05-team-handover-plan.md). Passages that assume the AI interview, Options A and B, or Claude-based sessions are superseded.

| | |
|---|---|
| **Status** | **Proposed** v0.3.0 (2026-11-05). Part of Deliverable 2. Not yet reviewed by the research lead. v0.3.0 integrates two review passes by Claude agents, one prompted as an applied econometrician and one on benchmark methodology (AI, not human reviewers; §16). |
| **Purpose** | Establish, with recorded evidence, that a task's verifier accepts correct work and rejects scientifically consequential mistakes, so that the benchmark score means what it claims. |
| **Inputs** | A task candidate with a reference implementation, at least one validated flawed variant, and a draft verifier (see the [construction protocol](benchmark-construction-protocol.md)). |
| **Outputs** | `validationRun` records (see the [schema](../../schemas/README.md)), a **kill matrix**, an exposure log, and a pass/fail decision on the verification and leakage criteria of the [rubric](task-quality-rubric.md). |
| **Evidence** | [R1](../research/evidence/R1-terminal-bench-science.md) (Terminal-Bench-Science practice), [R5](../research/evidence/R5-analysis-causal-econ-benchmarks.md) (analytic dispersion, causal benchmarks), [R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) (testing techniques, numerical checks); review passes by Claude agents of 2026-11-05 (§16) |

---

## 1. Why a flawed implementation is not enough

The research lead's brief (§4) states the core difficulty: "A deliberately flawed implementation is not sufficient by itself to establish that a task is good." Three distinct failures can hide behind a verifier that "rejects the flawed version":

1. **Over-fitting to one wrong answer.** The verifier rejects the specific flawed output but accepts other wrong answers. This is the mirror image of the verifier "co-designed with the author's own solution" (*Good Benchmarks* §7).
2. **Rejecting valid alternatives.** Legitimate dispersion among competent analysts is large ([R5](../research/evidence/R5-analysis-causal-econ-benchmarks.md) §6).
3. **Coincidence.** The flawed procedure gives the same answer as the correct one on the evaluation data. This is really six different problems with six different remedies (§2).

**What DeepEcon adds to established practice.** Seeding faults to test the tests is classic mutation testing (DeMillo, Lipton & Sayward 1978). Terminal-Bench-Science already verifies repair tasks on seeded hidden instances with named negative controls and independent "witness" implementations [P-full]. DeepEcon's contribution is **where the mutants come from**: realistic research mistakes designed by experts and documented with realism warrants. The machinery is borrowed and should be cited as such.

## 2. "Same number, wrong procedure": six kinds of equivalence

Adapted from [R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) §5 (P = correct procedure, F = flawed procedure).

| Type | Definition | Economics example | Can an outcome check catch it? | Remedy |
|---|---|---|---|---|
| **1. Semantic equivalence** | F(d) = P(d) for every admissible input | Clustering on `state_id` versus `state_name` when they map one-to-one | No, and it need not | Not a flaw: reclassify as a valid alternative or discard; exclude from mutation counts. Only this type is an "equivalent mutant" proper. |
| **2. Data-equivalence** | F ≈ P on the evaluation data, but not on other admissible inputs | TWFE ≈ heterogeneity-robust DiD when effects are nearly homogeneous; OLS ≈ 2SLS when endogeneity is weak in the sample | **Yes, with new inputs** | Hidden variants that exercise the separating feature (§5); record the separation margin |
| **3. Observation-equivalence** | F differs only in outputs the verifier does not observe | Wrong clustering level: same coefficient, different SE | Yes, if the verifier observes more | A benchmark-wide output schema that always includes SE, confidence interval, N, number of clusters, and the cluster variable (rubric SP-4); inference relations (§5) |
| **4. Tolerance-equivalence** | F falls inside an acceptance region widened for valid alternatives | A flawed estimate within the dispersion of valid estimators | Partly | Separate the three sources of variation (§4 item 6); tighten the estimand; separating hidden variants |
| **5. Power-equivalence** | F and P differ in sampling properties too subtly for the verifier's simulation budget | A test with size 7% instead of 5% | Only with large Monte Carlo budgets | Grade inference deterministically against conditional references (§4 item 7); never key tasks on small distortions |
| **6. Identification-equivalence** | Both compute valid statistics; the flaw lies in an untestable assumption | A comparison group whose trends diverge only after treatment; a violated exclusion restriction | **No**, not from observational data | Structured expert judgment (tier V3); sensitivity analysis as a required output; never a binary key (brief §4) |

## 3. The validation ladder

Run the rungs in order. A failure sends the task back to the shepherd. Every run is stored as a `validationRun`, and §3.1 says which rungs to re-run after a change.

| Rung | Run kind | Pass condition | Automatable? |
|---|---|---|---|
| L0 | **Static checks** | Schema valid; tiers correct; leakage scan clean (LK-1); environment pinned, offline, and identical for every task of a type (EN-1); output schema benchmark-wide (SP-4). | Yes |
| L1 | **Oracle** | The reference solution, run in the task environment with no privileged files, is accepted. Oracles can themselves be wrong (Barr et al. 2015), hence L3. | Yes |
| L2 | **No-op and trivial nulls** | Empty, default, constant, mean, zero-effect, and identity outputs are rejected on every **answer-changing** hidden instance. Invariance instances are exempt and listed; every task has a stated minimum number of answer-changing instances. | Yes |
| L3 | **Alternatives and independent witnesses** | Every accepted option in the decision space is accepted on the main data and on all hidden variants. At least one **structurally independent** witness is required. Qualifying witnesses: a clean-room re-implementation written from the paper, estimand, and codebook without reading the original code; or a blind expert solve (rubric SP-1). Several LLM-written implementations are **not** independent evidence; independently written versions tend to fail together (Knight & Leveson 1986; reported again for coding agents in 2026 [S]). | Run: yes. Choice of alternatives: human |
| L4 | **Negative controls (expert flawed variants)** | Every validated flawed variant is rejected, with separation margins recorded. | Run: yes. Design: human |
| L5 | **Mutation analysis (artificial mutants)** | Generated mutants (drop a fixed effect, change the cluster variable, shift timing by one period, alter a sample filter, flip a sign) are run. **Pass:** every surviving non-equivalent mutant has been triaged, and no survivor reveals a verifier gap. Survivor counts are reported by operator class. No confidence interval is reported, because designer-chosen mutants are not a random sample. | Yes, with human triage |
| L6 | **Metamorphic relations** | The relations in §5 hold for the reference and all alternatives, and are violated by the flawed variants they target. Relations are necessary conditions, not sufficient ones. | Yes |
| L7 | **Hidden-variant separation** | Answer-changing variants are built on bases the agent never sees (§5.1). **Deterministic families:** every correct solution matches its conditional reference on the same input. **Stochastic families:** simulation shows, with a one-sided 95% upper bound, that the probability of rejecting a correct solution is below 10⁻³ (with no rejections, about 3,000 draws). **Flawed variants:** each is rejected on the variants that satisfy its stated conditions, with a one-sided 95% lower bound of at least 0.90 (for example, 194 of 200 gives 0.942 by Clopper–Pearson). The kill matrix records flawed variants × checks, with margins. | Yes |
| L8 | **Shortcut and adversarial attacks** | Each of these attacks must fail:<br>(a) hard-coded published coefficients;<br>(b) trivial nulls (L2);<br>(c) copying from any file in the environment;<br>(d) "flag everything" in detection tasks;<br>(e) recall of the original package or paper (rubric LK-4);<br>(f) cheat trials by an agent briefed to get the reward without doing the work, run offline (the official configuration) and once online to measure what the offline rule protects;<br>(g) the **differential attack**: return the main-data or published answer plus the estimand-weighted difference between hidden and visible outcomes;<br>(h) constant outputs on invariance instances;<br>(i) "change nothing" and "always switch to the newest estimator" policies in correction tasks;<br>(j) agent code trying to write the reward or read hidden data (EN-4).<br>"No hack found" is evidence, not proof ([R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) §2.3). | Mostly yes |
| L9 | **Full-harness replay** | At least 300 replays of the oracle and of every accepted alternative, through the agent sandbox plus verifier, varying unfixed seeds, thread counts, and at least two hardware platforms. **Pass:** zero spurious failures, reported with the one-sided 95% upper bound (about 1% at 0 of 300). Re-running a deterministic verifier with fixed seeds on stored outputs cannot fail and does not count. | Yes |
| L10 | **Hint ladder and knowledge probe** | Pre-declared hints are given to agents in separate trials: H1 a design fact the instruction should carry; H2 names the pitfall; H3 names the method. A knowledge probe asks the key fact directly, outside the task. H2 and H3 trials, the knowledge probe, and the recognition probe (L8 e) disclose the crux, so they are exposures under §10: they send answer-key material to the calibration model's developer or API host, are logged (rubric LK-5), and that developer's later models are reported separately on the task (Rule 10). Results feed rubric SP-3 and SO-3. | Yes, with human reading |
| L11 | **Agent trials and crux alignment** | At least 5 trials for each of at least 3 configurations from at least 2 model families, on the frozen task version, with model IDs and dates. At least 4 of 5 failing trials fail at the stated crux. Calibration models are listed in the release, and their scores are reported as *calibration-exposed*. | Runs: yes. Analysis: human |
| L12 | **Independent review** | The blind expert solves and acceptance criteria from Stage 5 are re-checked against the L11 outputs. The domain reviewer and the benchmark reviewer sign off. | No |
| L13 | **Post-admission monitoring** | Issue reports and task repairs. Status classifications are revisited at each release against new methodological literature. | Partly |

### 3.1 Re-run matrix

| Change | Re-run |
|---|---|
| Instruction | L0–L12 |
| Verifier | L1–L9, and re-score all stored trials |
| Environment | L0–L12 (the environment counts as instruction, rubric SP-3) |

Hardening edits are logged together with the trial that prompted them. No edit may be justified **only** by an agent's success (§4 item 9), because filtering tasks against the evaluated models biases their scores (R1 §4; *Good Benchmarks* §3, §9).

## 4. Designing the acceptance region

**Evidence.** Competent analysts disagree, even on sign and significance, when given only a question and data: in Breznau et al.'s released data, 64.4% of 1,252 models were not significant, 19.5% significantly negative, and 16.1% significantly positive [P-page]. Repeated AI-agent runs vary far less than human analysts (2–27 times less in one 2026 study) [S]. Calibrating on agent runs alone would therefore reject legitimate alternatives ([R5](../research/evidence/R5-analysis-causal-econ-benchmarks.md)).

1. **Separate estimand, assumptions, and estimator** (Lundberg, Johnson & Stewart 2021 [U]):
   - **(a) Estimand.** State it in potential-outcome terms, with explicit weights over the treated (cohort, period) cells, the event window, and the population.
   - **(b) Identifying assumptions.** Comparison group, base period, and anticipation are stated in the instruction or chosen from a benchmark-wide convention vocabulary (item 4).
   - **(c) Estimator.** It is never part of the estimand.

   In staggered DiD, writing out the aggregation weights can effectively name the estimator. Rubric SP-3 records which phrases disclose the method.
2. **Tighten first.** Tighten the instruction until the remaining variation is small (*Good Benchmarks* §4).
3. **Hidden decision space.** For each consequential decision, list the options and mark each as reference, accepted, unjustifiable, or contested, with provenance and citations. Options carry `requires` and `excludes` constraints. For example: not-yet-treated controls *require* a no-anticipation window; imputation *requires* parallel trends in all pre-periods; never-treated controls are infeasible when every unit is eventually treated; a wild bootstrap must match the clustering level.
4. **Declarations only for non-crux conventions.** The agent may declare conventions from a vocabulary that is **benchmark-wide for the design family**, and so reveals nothing task-specific. Examples: small-sample factor, degrees-of-freedom rule, handling of singletons, counting of nested fixed effects.
   - **Crux decisions are graded only through outcomes on separating hidden variants.** Naming them in the output contract would disclose the crux and turn the task into multiple choice.
   - Each task has at most two multi-option decisions.
   - Every selectable combination's conditional reference is checked against a second implementation (GT-1).
   - A declaration–implementation consistency check runs on variants where the declared options separate.
   - Self-reported values are never graded alone (rubric VE-3).
5. **Intermediate outputs are outcomes.** Estimation-sample identifiers (or their hash), cohort sizes, and the number of clusters are produced by **re-executing the agent's code** in the verifier sandbox, not taken from its report.
6. **Three sources of variation, three mechanisms.**
   - **(i) Numerical noise:** a band from cross-software re-runs of the same declared estimator and convention. For deterministic estimators it is tiny.
   - **(ii) Conventions:** fixed in the instruction or declared from the vocabulary, each with its own conditional reference. Conventions can be as large as flaws: in R6's design, two defensible CR1 conventions differ by a factor of about 1.10.
   - **(iii) Substantive alternatives:** the decision space.

   **No default band is borrowed from another benchmark.** For example, an SE-ratio band of 0.8–1.25 would accept a wrong clustering level in R6's design, where unit-clustered over state-clustered SE is 1.195 and heteroskedasticity-only over state-clustered is 1.065.

   For stochastic outputs (bootstrap, randomization inference), the output contract fixes a minimum number of draws B, and the band adds k × the simulation SE at the declared B. Near p = 0.05, the simulation error of a p-value is about 0.007 at B = 999 and 0.015 at B = 199.
7. **Inference is graded deterministically.** The agent's SE, confidence interval, and p-value are compared with the conditional reference for the declared variance estimator, on the main data and on hidden variants. Size and coverage simulations are used only during validation (L4, L7). Grading size by re-running an agent's pipeline is infeasible: about 150 runs would be needed to detect a 10% size against 5%, and about 820 to detect 7% against 5%.
8. **Familywise control.** All of a task's thresholds are set jointly, before any agent output is seen. The familywise false-rejection probability for an implementation drawn from the accepted decision space must be at most 1%, estimated by simulation, as in Terminal-Bench-Science's `small-area-equivalence` task (R1 §8.3). Coverage gates report their binomial noise.
9. **Freeze before evaluation.** CausalVerify revised its scorer three times after outputs existed, moving its headline failure rate from 56.1% to 33.1% to 15.5% [P-page].
   - **Development.** Widening for a legitimately valid approach needs an expert's written justification and a re-run of all controls.
   - **Evaluation.** The verifier version is frozen; any change creates a new task version.
10. **Calibrate with experts.** Blind expert solves (rubric SP-1) supply human dispersion; agent runs alone understate it.
11. **Check discrimination.** If the region contains a flawed variant's output, tighten the estimand, choose another target analysis, add separating variants, or demote the task to tier V3.
12. **No knife-edge keys.** Never key a task on a significance change unless both p-values lie outside [0.02, 0.10].
13. **Contested decisions get no binary grade** (D-013, X-003).

## 5. Hidden variants and metamorphic relations

### 5.1 Answer-changing variants must use bases the agent never sees

If an answer-changing variant is built on the data the agent holds, a program can pass by arithmetic rather than estimation (the differential attack, L8g). Answer-changing hidden variants are therefore built on:
- held-out units, cohorts, or periods;
- bootstrap-resampled panels;
- outcome-perturbed copies.

Effect injection is then layered on top. References are computed on each variant by the reference and accepted implementations. Invariance checks may use the visible data.

### 5.2 Treated-cell weighting checks: effect injection

**What it tests.** Replace Y with Y + τ·D on the variant base, where D is the treatment as the instruction defines it and τ is an effect pattern within the class the instruction admits. For a pipeline that is linear in the outcome *on the estimand's scale*, with weights that do not depend on Y, the estimate shifts by **exactly the estimator's weighting of τ over treated cells**.

**Limits.**
- The shift equals the *estimand's* weighting only for estimators that are unbiased for the stated weighted ATT under arbitrary heterogeneity (imputation; Callaway–Sant'Anna with the matching aggregation).
- For 2SLS and other regression-defined estimands, it is a differential check against the conditional reference for the declared specification. With heterogeneous τ, the 2SLS shift is the estimator's own weighting (0.809 versus a complier mean of 0.975 in the review's check), and it changes with valid covariates (Blandhol et al. 2022 [U]).
- **It tests nothing about how the counterfactual Y(0) is built.** In the review's check, a naive treated-minus-untreated mean and a treated-only before/after comparison both moved by exactly the target. Hence §5.3.
- Exactness breaks for winsorizing or trimming on Y, standardized indices, data-driven bandwidths, LASSO-selected controls, and log, inverse-hyperbolic-sine, or PPML outcomes. Inject on the estimand's scale (multiplicatively for log estimands). For binary or bounded outcomes, injection can leave the outcome's support.

**What it catches.** Static TWFE under staggered adoption with heterogeneous effects: in R6's design, with a target ATT of 2.062, the imputation estimator moved by 2.062 and TWFE by 1.421. It also catches mistimed treatment: with τ = 1, a one-period-late coding moved by 0.686.

### 5.3 Counterfactual-side invariances (exact)

| Transformation | Correct procedure | Flaw exposed |
|---|---|---|
| **Control-span invariance:** add any vector in the span of the required fixed effects or controls (e.g., arbitrary αᵢ + λₜ) | Estimate unchanged | Missing fixed effects or controls. Naive comparisons changed by 6.93 and 7.95 in the review's check, while TWFE and imputation changed by 0.000 |
| **Instrument-orthogonal confounding:** add to the outcome a component orthogonal in-sample to [1, Z, W] but correlated with X | 2SLS unchanged | Using OLS where 2SLS is required: OLS changed by 0.713 in the review's check |

### 5.4 Inference relations

| Transformation | Correct procedure | Flaw exposed |
|---|---|---|
| **Duplicate every unit with a new unit ID but its original cluster ID** | A correctly cluster-robust SE at the assignment level is unchanged (ratio 1.0000 with CR0 and CR2, 0.9956 with CR1, so allow about 1–2%); unit-clustered and heteroskedasticity-only SEs shrink by about 1/√2 | Clustering finer than the assignment level, or none. It does **not** expose clustering coarser than necessary, which is often a contested choice (V3) |

### 5.5 Other invariances

| Transformation | Correct procedure | Flaw exposed |
|---|---|---|
| Add rows that the stated sample definition excludes | Unchanged | A missing sample filter |
| Rescale the instruments, or apply any nonsingular linear transformation to them | 2SLS unchanged | Ad hoc instrument handling |
| Shift the RD running variable and the cutoff together | Unchanged | Hard-coded cutoff |
| Permute rows; relabel identifiers consistently | Unchanged | Order-dependent manipulation; identifier-dependent merges |
| Shift calendar dates by a constant | Event-time effects unchanged | Calendar-tied timing. **Use only when the instruction's parameters are derived from the data and transformed consistently**; otherwise it grades an unstated requirement |
| Multiply or shift the outcome (linear models in levels only) | Coefficients and SEs scale; slopes are unchanged with an intercept or fixed effects | Hard-coded values |

**Regression discontinuity.** A constant injection moves a local-linear estimate at any bandwidth, and a global quartic, by exactly τ. RD's main pitfalls (bandwidth, polynomial order, inference) therefore have no exact relation. They are verified through conditional references for declared conventions, and through coverage simulations during validation.

## 6. Synthetic and derived data: licensing and realism

- **Derived works inherit the original licence.** Effect-injected, perturbed, and semi-synthetic data built on real covariates are derived from the original files. They are hidden-variant techniques for **redistributable** data, not substitutes for restricted data.
- **For restricted data, the only route is fully synthetic data.** Every variable is synthesized, with disclosure review and the data provider's permission where required. The reference check (GT-1) and the materiality check (RV-2) are re-run, and the failure mode's consequence is re-demonstrated, on the synthetic data.
- **Fully synthetic data lose real-data quirks:** duplicates, miscoded treatment, unbalanced panels. Those quirks drive the brief's failure mode #6. Task counts are therefore reported by failure-mode category × data route, so that bias toward estimator-choice flaws is visible.
- **Generator safeguards** (*Good Benchmarks* §7: "the verifier can quietly encode an assumption only you hold"):
  - document the data-generating process in the hidden tier;
  - have an independent economist review it;
  - every validated alternative must recover the truth;
  - calibrate realism, rather than maximizing the gap between correct and flawed results;
  - pair coverage checks with interval-width or contraction checks (R6 §3.9).

## 7. Correction and detection tasks: twins, decoys, and matchers

1. **Matched clean twins.** Each flawed package has a twin with no known consequential error, under the same instruction and the same restructured presentation (rubric LK-3).
2. **Scoring correction tasks.**
   - Flawed instances are scored on **repair**: the output matches the reference or a conditional reference.
   - Clean instances are scored on **preservation**. Each outcome is classified as *unchanged*; *changed to another accepted option* (neutral, reported as a valid but unnecessary change); or *changed to an unjustifiable option* (a false alarm).
   - The instruction states whether valid but different choices count as unnecessary changes.
   - Repair and preservation are reported separately, never pooled.
3. **Clean-control share.** The share is fixed per release, not disclosed to agents, and reported with every score.
4. **Detection tasks.** Recall, false-alarm rate, and localization are reported separately. Decoys (valid alternatives from the decision space) must not be flagged. The key lists **groups of equivalent locations and categories**, because a planted error can legitimately be located at several sites.
5. **Bounds.** With 0 false alarms in 30 clean controls, the 95% upper bound on the true rate is about 9.5% one-sided (11.6% two-sided). Report bounds with their sidedness.
6. **Matcher validation.** The rule-based or LLM matcher is validated on planted match and non-match fixtures (SPOT uses an LLM similarity step [P-page]).
7. **Natural errors.** An agent may find a real, unplanted error in a "clean" package. Such reports go to human adjudication and may lead to task repair; they are not false alarms by default.

These tasks measure prompted error-finding. They do not measure whether an agent avoids errors in its own work; that is the job of research-execution tasks.

## 8. Scoring and reporting

- **Execution and correction tasks:** binary reward per task, conjunctive across checks and hidden variants.
- **Detection tasks:** scored as in §7.
- **Trials:** at least five per evaluated configuration.
- **Reporting:** for each task type, the mean with a 95% confidence interval from a bootstrap that resamples tasks, keeping each task's trials together. Types are never pooled, and repair and preservation scores are reported separately.
- **Exposure labels:** models that touched construction (interviewer, generator, checkers, calibration agents) are listed, and their scores are marked *calibration-exposed*.
- **Release stability:** each release's contents are frozen; a withdrawal retires a task only at the next version.

## 9. Verification by validity layer, and tiers per graded output

Each failure mode has a **primary** validity layer (of five) plus optional secondary layers. TWFE under staggered adoption, for instance, is primarily statistical (the estimator does not target the stated weighted ATT), with interpretation as a secondary layer when its coefficient is read as that ATT. Agreement on the layer is reported.

**Tiers are assigned per graded output, not per layer:**
- **V1:** deterministic comparison.
- **V2a:** exact relation (injection, invariances).
- **V2b:** stochastic check with stated error rates.
- **V3:** structured judgment with an expert-consensus key.
- **V4:** open-ended judgment.

| Validity layer | Objectively verifiable | Typical tiers | Not objectively verifiable |
|---|---|---|---|
| Computational (implementation fidelity) | The code implements the stated design | V1, V2a | — |
| Measurement | Variables are constructed as defined | V1; V3 for whether a definition fits the construct | Contested proxies |
| Statistical | The procedure is appropriate for the estimand and design | V2a, V2b, V1 against conditional references | Trade-offs among valid procedures |
| Identification | Falsification computations and sensitivity outputs | V1 or V2a for the computations; V3 for recognizing threats | Whether untestable assumptions hold |
| Interpretation | Whether claims follow from given results | V3 | Contested nuances |

**V3 admission.** Each item type is first qualified by a pre-registered, set-level agreement study (Krippendorff's α or Gwet's AC1 of at least 0.8). Individual items are then admitted when at least 4 of 5 raters agree, or when a latent-class posterior is at least 0.95.

**LLM-as-judge (V4)** is used only in the unscored track, and reports its agreement with human graders.

## 10. Exposure of hidden material

1. **Every AI service, trial, or evaluation run that receives hidden-tier material or the package** is logged with the provider, the kind of account, and the date (rubric LK-5). Work, business, or API accounts are preferred; personal accounts are used with training off. This lowers the chance of training but does not prevent exposure ([AI use and integrity rules](../architecture/llm-use-policy.md) §3).
2. **Scored tasks.** Their answers stay unpublished until the task is retired. Scores of models whose provider received a task's answer key before the evaluation are reported separately, and new tasks are added over time (P-057). All models are evaluated through providers' APIs (D-038).
3. **Granularity.** All tasks and twins from one paper share one publication status.
4. **Credibility-criteria catalogue.** While a paper has unpublished tasks, the catalogue is published without that paper's identifiers.
5. **Contributor agreements** include a disclosure embargo.

## 11. Validating the validators

Every automated or LLM-based reviewer, judge, or matcher is itself tested. Terminal-Bench-Science requires its LLM rubric reviewer to catch 100% of planted defects whenever the rubric changes ([R1](../research/evidence/R1-terminal-bench-science.md) §4) [P-full]. DeepEcon's flawed packages and clean twins are natural planted-defect and non-defect fixtures.

Benchmark reviewers qualify in two ways: by shepherding one task through L12, and by passing a planted-defect calibration set.

## 12. Division of labour

| Activity | Automated | Shepherd | Contributor | Outside economists (blind, then unblinded) | Benchmark reviewer |
|---|---|---|---|---|---|
| Static checks, leakage and exposure logs | ✔ | Reviews hits | — | — | Audits |
| Oracle, nulls, replay, relations, injection | ✔ | Interprets | — | — | — |
| Flawed variants | — | Assists | ✔ | Classify status (after RV-2/L4/L7) | — |
| Decision space, conventions, alternatives | — | ✔ | ✔ | Check | — |
| Blind acceptance criteria and blind solves (SP-1) | — | Organizes | — | ✔ (before seeing the hidden tier) | — |
| Mutation triage, hidden variants | Runs | ✔ | — | Check data-generating processes | — |
| Attacks and cheat trials | ✔ | Designs | — | — | Checks |
| Agent trials, hint ladder, crux alignment | Runs | ✔ | Consulted | — | — |
| Admission | — | Recommends | — | Domain reviewer | ✔ (with release editor) |

## 13. Precedents

**Terminal-Bench-Science** ([R1](../research/evidence/R1-terminal-bench-science.md) §8) [P-full]:
- a repair task (`highdim-mediation-debiasing`) verified on seeded hidden instances;
- injected-error detection (`ehr-error-detection`);
- conjunctive statistical gates and metamorphic interventions;
- witness implementations;
- cheat trials and hardening loops.

**CausalVerify** ([R5](../research/evidence/R5-analysis-causal-econ-benchmarks.md) §4.1) [P-page]:
- design commitment before the data are revealed;
- an oracle arm;
- repair rounds;
- SE-ratio grading on synthetic twins.

**DeepEcon's distinctive contribution** is realistic, expert-designed negative controls drawn from published papers' own pipelines, used systematically across correction, detection, and execution tasks.

## 14. References

Verified at secondary-source level in [R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) §9 [S]:
- DeMillo, Lipton & Sayward (1978), *Computer* 11(4), 34–41.
- Chen, Cheung & Yiu (1998), Technical Report HKUST-CS98-01 (arXiv:2002.12543).
- Barr et al. (2015), *IEEE TSE* 41(5), 507–525.
- Knight & Leveson (1986), *IEEE TSE* SE-12(1), 96–109.
- Dorie et al. (2019), *Statistical Science* 34, 43–68.

Cited by the reviewing Claude agents, not yet verified [U]:
- Lundberg, Johnson & Stewart (2021), *American Sociological Review*, on separating estimands from estimators.
- Blandhol, Bonney, Mogstad & Torgovitsky (2022), NBER WP 29709, on 2SLS with covariates.
- Kolesár & Rothe (2018), *AER*, on clustering by a discrete running variable.
- Conley & Taber (2011); MacKinnon & Webb (2018), on inference with few treated clusters.

Primary: Bercovich (2026), *Good Benchmarks* [P-full].

## 15. Open methodological questions raised by v0.3.0

- How many answer-changing hidden instances are needed per task, and how they are generated without disclosing the crux.
- Whether a benchmark-wide convention vocabulary per design family is achievable without leaking crux decisions.
- The cost of blind expert solves and full-harness replays at scale (see the [cost model](../architecture/cost-and-effort-model.md)).

## 16. Changes

**v0.3.0** (review passes by Claude agents, 2026-11-05):
- Effect injection restated precisely: it is an estimator-weighting check, blind to the counterfactual Y(0). Counterfactual-side invariances added (control-span, instrument-orthogonal confounding).
- Answer-changing variants on unseen bases; differential and policy attacks added.
- Estimand, assumptions, and estimator separated. Declarations limited to non-crux conventions from a benchmark-wide vocabulary.
- Three-way split of variation, with no borrowed default band. Deterministic inference grading. Familywise control. Full-harness replay.
- Pass rules with confidence bounds; L5 triage rule; re-run matrix; hint ladder; agent-trial anchors; calibration-exposed labels.
- Repair versus preservation scoring; equivalent-location keys; sidedness of bounds.
- Licensing of derived data; fully synthetic data for restricted sources.
- Exposure rules for hidden material; scoring and reporting section; tiers per graded output (V1, V2a, V2b, V3, V4) with V3 admission rules.
- Cross-document consistency pass (2026-11-05): one-sided 95% bound for stochastic families (L7); crux-disclosing hint and probe trials are hidden-tier exposures (L10); instruction changes re-run from L0 and environment changes through L12 (§3.1); the bootstrap resamples tasks (§8); the TWFE example uses the five layers (§9).

**v0.2.0:**
- Clustering relation corrected.
- Equivalence taxonomy, kill matrix, clean twins, decision spaces, and freezing added.
