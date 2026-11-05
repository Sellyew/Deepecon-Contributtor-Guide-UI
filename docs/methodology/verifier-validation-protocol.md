# Verifier Validation Protocol

| | |
|---|---|
| **Status** | **Proposed** v0.2.0 (2026-11-05). Part of Deliverable 2. Not yet reviewed by the research lead. Changes from v0.1.0 are listed in §13. |
| **Purpose** | Establish, with recorded evidence, that a task's verifier accepts correct work and rejects scientifically consequential mistakes, so that the benchmark score means what it claims. |
| **Inputs** | A task candidate with a reference implementation, at least one validated flawed variant, and a draft verifier (see the [construction protocol](benchmark-construction-protocol.md)). |
| **Outputs** | `validationRun` records (see the [schema](../../schemas/README.md)), a **kill matrix**, and a pass/fail decision on rubric criteria VE-1 to VE-5, SO-1 to SO-3, DF-1, EN-2, EN-4, LK-1, and LK-2 ([rubric](task-quality-rubric.md)). |
| **Evidence** | [R1](../research/evidence/R1-terminal-bench-science.md) (Terminal-Bench-Science practice), [R5](../research/evidence/R5-analysis-causal-econ-benchmarks.md) (analytic dispersion, causal benchmarks), [R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) (testing techniques, error detection, numerical checks) |

---

## 1. Why a flawed implementation is not enough

The research lead's brief (§4) states the core difficulty: "A deliberately flawed implementation is not sufficient by itself to establish that a task is good." Three distinct failures can hide behind a verifier that "rejects the flawed version":

1. **Over-fitting to one wrong answer.** The verifier rejects the specific flawed output but accepts other wrong answers. This is the negative-side version of the verifier "co-designed with the author's own solution" (*Good Benchmarks* §7).
2. **Rejecting valid alternatives.** The verifier rejects a different estimator that identifies the same estimand. Legitimate dispersion among competent analysts is large ([R5](../research/evidence/R5-analysis-causal-econ-benchmarks.md) §6).
3. **Coincidence.** On the evaluation data, the flawed procedure gives the same answer as the correct one, so no outcome check on that data can separate them. This is really six different problems with six different remedies (§2).

**What DeepEcon adds to established practice.** Seeding faults to test the tests is classic mutation testing (DeMillo, Lipton & Sayward 1978). Terminal-Bench-Science already uses named negative controls and independent "witness" implementations [P-full]. DeepEcon's contribution is **where the mutants come from**: experts design them as realistic research mistakes, each with a realism warrant. The technique itself is not new and should be cited as such.

## 2. "Same number, wrong procedure": six kinds of equivalence

Adapted from [R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) §5 (P = correct procedure, F = flawed procedure).

| Type | Definition | Economics example | Can an outcome check catch it? | Remedy |
|---|---|---|---|---|
| **1. Semantic equivalence** | F(d) = P(d) for every admissible input | Clustering on `state_id` versus `state_name` when they map one-to-one | No, and it need not | Not a flaw. Reclassify as a valid alternative or discard; exclude from mutation scores. Only this type is an "equivalent mutant" proper. |
| **2. Data-equivalence** | F ≈ P on the evaluation data, but not on other admissible inputs | TWFE ≈ heterogeneity-robust DiD when effects are nearly homogeneous; OLS ≈ 2SLS when endogeneity is weak in the sample | **Yes, with new inputs** | Hidden variants that exercise the separating feature, e.g. effect injection (§5). Record the separation margin. |
| **3. Observation-equivalence** | F differs only in outputs the verifier does not observe | Wrong clustering level: same coefficient, different SE | Yes, if the verifier observes more | Require SE, confidence interval, N, number of clusters, and first-stage statistics as outputs, stated in the instruction. Use inference relations (§5). |
| **4. Tolerance-equivalence** | F falls inside an acceptance region widened for valid alternatives | A flawed estimate within the dispersion of valid estimators | Partly | Declared-choice grading with conditional references (§4); hidden variants where F leaves the region; tighten the estimand. |
| **5. Power-equivalence** | F and P differ in sampling properties too subtly for the verifier's simulation budget | A test with size 7% instead of 5%; mild under-coverage | Only with large Monte Carlo budgets | Do not key tasks on small distortions. Report the verifier's own power. |
| **6. Identification-equivalence** | Both compute valid statistics; the flaw lies in an untestable assumption | A comparison group whose trends diverge only after treatment; a violated exclusion restriction | **No**, not from observational data. Semi-synthetic data can catch it only by encoding the assumption in the generator (*Good Benchmarks* §7). | Structured expert judgment (tier V3); require sensitivity analysis as an output; never force a binary key (brief §4). |

## 3. The validation ladder

Run the rungs in order; a failure sends the task back to the shepherd. Each run is stored as a `validationRun`.

| Rung | Run kind | What it establishes | Pass condition | Automatable? |
|---|---|---|---|---|
| L0 | Static checks | Package integrity | Schema valid; tiers correct; leakage scan clean (LK-1); environment pinned and offline (EN-1); verifier isolation (EN-4). | Yes |
| L1 | **Oracle** | Solvability from agent-facing materials (SO-1); the verifier accepts correct work | The reference solution, run in the task environment with no privileged files, is accepted. Oracles can themselves be wrong (the test-oracle problem; Barr et al. 2015); hence L3 and the independent check in construction Stage 1. | Yes |
| L2 | **No-op and trivial nulls** | The verifier is not trivially satisfied | Empty, default, constant, mean, zero-effect, and identity outputs are rejected on every hidden instance. | Yes |
| L3 | **Alternative valid implementations** | Other correct paths get credit (GT-4, VE-1) | Every accepted option in the decision space is accepted on the main data and on all hidden variants. **Several LLM-written implementations are not independent evidence:** independently written versions tend to fail together (Knight & Leveson 1986; reported again for coding agents in 2026 [S]). At least one structurally independent witness is required: a different author, software, or method. | Run: yes. Choosing alternatives: human |
| L4 | **Negative controls (expert flawed variants)** | Consequential mistakes are rejected (VE-2) | Every validated flawed variant is rejected, with separation margins recorded. The flagship variant is rejected on the main data or killed by a stated hidden variant. | Run: yes. Design: human |
| L5 | **Mutation analysis (artificial mutants)** | Verifier sensitivity beyond the expert variants | Report a mutation score **with a confidence interval** over generated mutants: drop a fixed effect, change the cluster variable, shift timing by one period, alter a sample filter, flip a sign. Classify each survivor (§2): semantically equivalent → exclude; data-equivalent → add a separating hidden variant, or document as undetectable on this design; verifier gap → fix; valid alternative → add to L3. | Yes, with human triage |
| L6 | **Metamorphic relations** | Procedure-level correctness without exact keys (VE-3) | The relations in §5 hold for the reference and all alternatives, and the relevant relations are violated by the flawed variants they target. Relations are necessary conditions, not sufficient ones. | Yes |
| L7 | **Hidden-variant separation** | No flaw survives as data-equivalent (type 2) | Each flawed variant is rejected on at least 95% of hidden variants; each correct solution is accepted on 100%. The **kill matrix** (flawed variants × checks, with margins) is recorded. | Yes |
| L8 | **Shortcut and adversarial attacks** | The score cannot be obtained without the capability (VE-4, EN-2) | All of these fail: hard-coded published coefficients; memorized values; copying from any file in the environment; "flag everything" answers in detection tasks; diffing against the public source package; an adversarial agent instructed to obtain the reward without doing the work. "No hack found" is evidence, not proof: hardening loops reduce but do not eliminate exploits ([R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) §2.3). | Mostly yes |
| L9 | **Repeat stability** | No flakiness (VE-5) | Hundreds of repeated verifier runs (*Good Benchmarks* §1) with zero spurious failures. | Yes |
| L10 | **Guided-agent fairness** | The verifier is fair conditional on the method (SO-3) | With the method named in a temporary instruction, strong agents pass. Terminal-Bench-Science reads graded hints this way: a pass with a hint the instruction could carry means the task is underspecified; a fail without hints but a pass with them means it is genuinely hard; a fail with every hint means it is broken. | Yes, with human reading of failures |
| L11 | **Agent trials and crux alignment** | Difficulty is intrinsic and located where claimed (DF-1, DF-3) | Batches of five trials per configuration across several models. The shepherd reads the failures, which must occur at the stated crux. | Runs: yes. Analysis: human |
| L12 | **Independent review** | Domain correctness and benchmark correctness (PR-2, SP-1) | Domain reviewer and benchmark reviewer sign off; the dual-verifier specification test passes. | No |
| L13 | **Post-admission monitoring** | Validity over time | Issue reports and task repairs; L1–L9 are re-run when the environment changes. | Partly |

## 4. Designing the acceptance region

Two pieces of evidence shape this section ([R5](../research/evidence/R5-analysis-causal-econ-benchmarks.md)).

**Competent analysts disagree, even on sign and significance, when given only a question and data.** In Breznau et al.'s released data, 64.4% of 1,252 models were not significant, 19.5% significantly negative, and 16.1% significantly positive [P-page]. Further specification narrows the dispersion but does not remove it: with shared cleaned data, the Many Economists study still found an interquartile range of 2.4 percentage points [S].

**Repeated AI-agent runs vary far less than human analysts** (2–27 times less in one 2026 study [S]). Tolerances calibrated only on agent runs would therefore reject legitimate alternatives.

1. **Fix the estimand and the decisions that matter first.** Tighten the instruction until the remaining variation is small (*Good Benchmarks* §4). With open specifications, no single tolerance band separates errors from valid alternatives.
2. **Build a hidden decision space.** For each consequential decision, list the options and mark each as reference, accepted, unjustifiable, or contested, with provenance and citations. BLADE uses expert-annotated decision spaces this way, but grades decisions rather than estimates [P-page].
3. **Grade against declared choices** when more than one option is accepted. The agent declares its choices. The verifier checks them against the decision space and recomputes the reference for that exact combination (a *conditional reference*). This separates three cases: a valid choice correctly implemented, a valid choice wrongly implemented, and an unjustifiable choice.
4. **Treat compact intermediate outputs as outcomes.** Estimation-sample identifiers (or their hash), cohort sizes, and the number of clusters catch errors that barely move the headline number.
5. **Use a tolerance only for numerical noise.** Express it in reference standard-error units, with a separate band on the ratio of standard errors (CausalVerify uses 0.5 SE and 0.8–1.25 [P-page]). Calibrate it from reference re-runs and cross-software implementations. Admit it only if it accepts every validated correct implementation and rejects every validated flawed variant.
6. **Freeze the verifier before evaluation.** CausalVerify revised its scorer three times after outputs existed, and its headline failure rate moved from 56.1% to 33.1% to 15.5% [P-page].
   - *Development:* agent trials may reveal legitimate alternatives; *Good Benchmarks* §7 calls this "a discovery process". Any widening needs an expert's written justification and a re-run of all controls.
   - *Evaluation:* the verifier version is frozen. Later changes create a new task version.
7. **Calibrate with experts, not agent runs.** Where residual dispersion matters, a small staged calibration study with economists measures it directly.
8. **Check discrimination.** If the region contains a flawed variant's output, take one of four routes: tighten the estimand, choose another target analysis, add separating hidden variants (L7), or demote the task to tier V3.
9. **Avoid knife-edge decisions.** Never key a task on a significance decision when the reference p-value is near the threshold.
10. **Contested decisions get no binary grade** (D-013, X-003). Exclude them, or grade recognition and abstention in the experimental track.

## 5. Metamorphic relations and hidden-variant families for econometrics

A metamorphic relation states how the output must change when the input is transformed. It checks a procedure without an exact answer key. Every relation is first verified on the reference and on all alternatives. **Some relations are model-specific:** scaling or shifting the outcome behaves differently for log outcomes, PPML, and ratio estimands, without any error in the code.

| Transformation of the input | Required behaviour of a correct procedure | Typical flaw it exposes |
|---|---|---|
| **Additive effect injection.** Replace Y with Y + τ·D on the real data, where D is the treatment as the instruction defines it and τ is an effect pattern within the class the instruction admits. | For estimators linear in Y, the estimate moves by **exactly** the estimand's weighting of τ, because the real untreated outcomes cancel in the difference. In R6's numerical check (Appendix A), the target ATT was 2.062: the imputation estimator moved by 2.062 and TWFE by 1.421. With a constant τ = 1, TWFE estimated with treatment coded one period late moved by 0.686. | Static TWFE under staggered adoption with heterogeneous effects; mistimed treatment. The check is exact and noise-free. It encodes only the estimand's definition, which sidesteps most of *Good Benchmarks*' synthetic-data warning. |
| IV variant: inject τᵢXᵢ. | Just-identified 2SLS moves by Cov(Z, τX)/Cov(Z, X); OLS moves by Cov(X, τX)/Var(X). | Using OLS where 2SLS is required, even where the two coincide on the base data. |
| RD variant: inject τ·1[X ≥ c]. | A local-linear estimate at a fixed bandwidth moves by exactly τ. Data-driven bandwidth selectors must be checked empirically. | Wrong side of the cutoff; wrong running variable. |
| Add rows that the stated sample definition excludes. | All outputs unchanged. | A missing sample filter. |
| **Duplicate every unit with a new unit ID but its original cluster ID.** | A correctly cluster-robust SE at the assignment level is unchanged (ratio ≈ 1; 0.9956 with CR1 small-sample factors in R6's design, so allow about 1–2% tolerance). Unit-clustered and heteroskedasticity-only SEs shrink by about 1/√2. | Clustering finer than the assignment level, or no clustering. It does **not** expose clustering coarser than necessary, which is often a contested choice (V3). |
| Rescale the instruments, or apply any nonsingular linear transformation to them. | 2SLS estimates unchanged. | Ad hoc instrument handling. |
| Shift the RD running variable and the cutoff together. | Estimate unchanged. | Hard-coded cutoff. |
| Permute the row order; relabel identifiers consistently. | All outputs unchanged. | Order-dependent data manipulation; identifier-dependent merges. |
| Shift every calendar date by a constant. | Event-time effects unchanged. | Timing tied to calendar values instead of adoption dates. |
| Multiply the outcome by c; add a constant to the outcome (linear models in levels only). | Coefficients and SEs scale by c, with t unchanged; slopes unchanged when there is an intercept or fixed effects. | Hard-coded values; ad hoc transformations. |
| Randomly reassign treatment (placebo). | Estimates centred on zero across draws. | Mechanical correlation introduced by the procedure. |

**Hidden-variant families.**
- Resamples (bootstrap, subsamples) test stability.
- Effect injection gives exact checks of how the point estimate weights the data.
- Full simulations with known truth are kept for **inference** checks (coverage, size), with large enough Monte Carlo budgets.

## 6. Semi-synthetic data: uses and dangers

Semi-synthetic datasets keep the real design (covariates, treatment timing, cluster structure) and simulate outcomes with known effects. The 2016 ACIC data-analysis challenge used this approach to compare causal-inference methods (Dorie et al. 2019) [S]. It supplies ground truth for statistical-validity tasks and defeats memorized published results.

*Good Benchmarks* §7 names the danger: "When you generate the data from a hypothesis, the verifier can quietly encode an assumption only you hold." Safeguards:

- **Prefer effect injection** (§5) where it suffices. It keeps the real untreated outcomes and encodes only the estimand's definition.
- **Document the data-generating process** in the hidden tier, and have an independent economist review it.
- **Every validated alternative estimator must recover the truth.** If only the contributor's estimator does, the generator encodes that estimator's assumptions.
- **Calibrate realism.** Noise and heterogeneity magnitudes should be plausible for the setting, not tuned to maximize the gap between the correct and flawed procedures.
- **Pair coverage checks with interval-width or contraction checks.** A procedure that ignores the data can pass a calibration check while being useless [P-full, R6 §3.9].

## 7. Error-detection tasks: clean twins, decoys, and matchers

Most error-detection benchmarks do not measure false alarms on clean material. Where matched clean twins were used, models that looked identical on recall differed by 79 points in false-alarm rate [S] ([R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) §1.4). Rules:

1. **Matched clean twins.** Each flawed package has a twin with no known consequential error, presented under the same instruction.
2. **Decoys.** Valid alternatives that look like mistakes (drawn from the decision space) must not be flagged.
3. **Separate scores.** Report recall, false-alarm rate, and localization separately. Never combine them into one number that hides the false-alarm rate.
4. **Enough controls to bound false alarms.** With 0 false alarms in 30 clean controls, the 95% upper bound on the true false-alarm rate is still about 9.5%. Report bounds, not just point estimates.
5. **Test the matcher.** The rule-based or LLM procedure that matches an agent's report to the planted error is itself validated on planted match and non-match fixtures. SPOT uses an LLM similarity step for this [P-page].
6. **Adjudicate natural errors.** An agent may find a real, unplanted error in a "clean" package; published packages contain real errors ([R4](../research/evidence/R4-replication-benchmarks.md)). Such reports go to a human adjudication route, which may lead to task repair. By default they do not count as false alarms.

## 8. Verification by validity layer

| Validity layer | What can be verified objectively | Recommended tier and methods | What cannot be verified objectively |
|---|---|---|---|
| Computational correctness (implementation fidelity) | Whether the code implements the stated design | V1: numeric tolerance; intermediate outputs; hidden-variant re-execution; effect injection | — |
| Measurement validity | Whether variables are constructed as defined, and whether definitions match the construct | V1 for construction against the definition; V3 for whether the definition fits the construct | Whether a proxy captures the construct, where experts disagree |
| Statistical validity | Whether the procedure is appropriate for the estimand and design | V2: effect injection, metamorphic relations, simulations with known truth, established statistical results | Choices among valid procedures with different finite-sample trade-offs |
| Identification validity | Whether stated falsification tests were run correctly, and what they show | V2 for the computational part; V3 for recognizing threats; sensitivity analysis (e.g., bounds under limited violations of parallel trends) as a required output | Whether untestable assumptions hold (identification-equivalence, §2 type 6) |
| Interpretation validity | Whether specific claims follow from given results | V3: claim classification with an expert-consensus key; contested claims excluded or keyed as acceptable sets | Nuanced judgments where credible experts disagree |

**Agreement standard for V3 keys (proposed).** At least three independent economists label each item without seeing each other's labels. An item enters the scored set only if all agree, or if a pre-registered agreement statistic clears a pre-registered threshold. Each item carries written rationales and citations.

**LLM-as-judge (V4).** Useful for triage and review assistance, but never the sole grader of a scored task. *Good Benchmarks* §7 notes that an LLM judge "will find some issues, but not everything." Any LLM-judged track reports its agreement with human graders.

## 9. Validating the validators

Every automated or LLM-based reviewer, judge, or matcher used in the pipeline is itself tested. Terminal-Bench-Science keeps a set of intentionally broken tasks and requires its LLM rubric reviewer to catch 100% of the planted defects whenever the rubric changes ([R1](../research/evidence/R1-terminal-bench-science.md) §4) [P-full].

DeepEcon already has natural fixtures for this: its expert-designed flawed packages are planted-defect fixtures, and its clean twins are non-defect fixtures. A reviewer model, matcher, or automated check that fails on them is not fit for gating.

## 10. Division of labour

| Activity | Automated | Shepherd | Contributor | Independent reviewers |
|---|---|---|---|---|
| Static checks, leakage scan | ✔ | Reviews hits | — | — |
| Oracle, null, repeat-stability, metamorphic, and effect-injection runs | ✔ | Interprets | — | — |
| Designing flawed variants | — | Assists | ✔ (scientific content) | Domain reviewers classify status |
| Decision space and alternative implementations | — | ✔ | ✔ | Domain reviewer checks |
| Mutation analysis and survivor triage | Generates and runs | ✔ (classifies by §2) | — | — |
| Hidden variants and semi-synthetic data | Runs | ✔ | Consulted | Domain reviewer checks |
| Shortcut and cheat trials | ✔ | Designs attacks | — | Benchmark reviewer checks |
| Agent trials and crux alignment | Runs | ✔ (reads trajectories) | Consulted on surprises | — |
| Dual-verifier specification test | — | Organizes | — | ✔ |
| Admission decision | — | Recommends | — | ✔ (release editor decides) |

## 11. Precedents

Terminal-Bench-Science already uses most of these elements in its statistics tasks ([R1](../research/evidence/R1-terminal-bench-science.md) §8) [P-full]:
- many hidden simulated instances generated from fixed seeds;
- conjunctive gates on bias, RMSE, and coverage;
- metamorphic interventions;
- byte-identical reruns;
- named negative controls;
- a structurally independent "witness" implementation.

It also runs adversarial cheat trials and a hacker–fixer hardening loop. CausalVerify commits each agent's design before the data are revealed, and uses an "oracle arm" that substitutes the reference design ([R5](../research/evidence/R5-analysis-causal-econ-benchmarks.md) §4.1) [P-page].

DeepEcon adds no new testing machinery. What it adds is **realistic, expert-designed negative controls**, used systematically across detection, correction, and execution tasks.

## 12. References

Verified at secondary-source level in [R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) §9 [S]; the full texts were not accessible from this environment.

- DeMillo, R. A., Lipton, R. J., & Sayward, F. G. (1978). Hints on test data selection: Help for the practicing programmer. *Computer*, 11(4), 34–41.
- Chen, T. Y., Cheung, S. C., & Yiu, S. M. (1998). *Metamorphic testing: A new approach for generating next test cases.* Technical Report HKUST-CS98-01, Hong Kong University of Science and Technology. Reposted as arXiv:2002.12543.
- Barr, E. T., Harman, M., McMinn, P., Shahbaz, M., & Yoo, S. (2015). The oracle problem in software testing: A survey. *IEEE Transactions on Software Engineering*, 41(5), 507–525.
- Knight, J. C., & Leveson, N. G. (1986). An experimental evaluation of the assumption of independence in multiversion programming. *IEEE Transactions on Software Engineering*, SE-12(1), 96–109.
- Dorie, V., Hill, J., Shalit, U., Scott, M., & Cervone, D. (2019). Automated versus do-it-yourself methods for causal inference: Lessons learned from a data analysis competition. *Statistical Science*, 34, 43–68.

Primary source: Bercovich (2026), *Good Benchmarks* [P-full].

## 13. Changes from v0.1.0

- **Corrected the clustering relation.** Duplicating the panel with fresh cluster IDs shrinks every SE type by 1/√2, so it discriminates nothing. Duplicating units within their original clusters does discriminate (R6 §8, verified numerically).
- **Added exact and invariance relations:** additive effect injection (exact for estimators linear in Y), IV and RD injection variants, and sample-filter, instrument-rescaling, and RD-shift invariances. Relations are now marked as model-specific where they are.
- **Added mutation-testing machinery:** the six-type equivalence taxonomy (§2), the kill matrix, mutation scores with confidence intervals, and four-way survivor triage.
- **Added rules for error-detection tasks (§7):** clean twins, decoys, separate detection scores, false-alarm bounds, matcher validation, and adjudication of natural errors.
- **Added** that several LLM-written implementations do not count as independent evidence (L3).
- **Added acceptance-region rules from R5 (§4):** decision spaces, declared-choice grading, intermediate outputs, SE-unit tolerances, freezing, and expert calibration.
- **Added** measurement validity to the validity-layer table.
- **Replaced** the unverified [U] references with verified ones.
