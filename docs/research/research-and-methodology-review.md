# Deliverable 1 — Research and Methodology Review

| | |
|---|---|
| **Status** | **Proposed** v0.2.0 (2026-11-05). A search-based review, not a systematic survey. v0.2.0 corrects the novelty statement (§6), the account of effect injection (§7.2), and the validation agenda (§9) after independent reviews; see §11. |
| **Purpose** | Establish what existing benchmarks measure, how they collect expert contributions, and how they construct and verify tasks; state precisely what DeepEcon's correct-versus-flawed approach adds and what it does not; identify what still needs methodological validation. |
| **Evidence** | Reading notes on [*Good Benchmarks*](reading-notes/good-benchmarks-bercovich-2026.md) and [`interview-me`](reading-notes/interview-me-skill.md); evidence notes [R1–R9](evidence/). Labels: **[P-full]** primary, full text · **[P-page]** primary abstract, landing page, or documentation · **[S]** secondary · **[U]** unverified. |

---

## 1. Scope and method

**What was reviewed.**
- The research lead's named references: Bercovich (2026), *Good Benchmarks*; the `interview-me` skill; Terminal-Bench-Science.
- Claude Code documentation.
- AI-agent benchmarks for reproduction and replication, data analysis, causal and econometric reasoning, and error detection.
- Benchmark-validity methodology and software-testing techniques for validating verifiers.
- Knowledge-elicitation methods and evidence on AI-led interviews.
- Economics replication-package standards and the econometric-pitfalls literature.

**How.** Primary sources were used wherever reachable: repositories cloned read-only, official documentation, journal and proceedings pages. Each claim carries an evidence label. Nine dated evidence notes record the details, URLs, and access problems ([index](evidence/README.md)).

**Limits.**
- arxiv.org, github.com (web and API), docs.github.com, and some vendor sites were outside the cloud environment's allowed network domains. Many arXiv papers were therefore verified only through search snippets ([S]) or alternative hosts. *Good Benchmarks* was read in full from a PDF supplied by the research lead.
- The landscape moves quickly, and this review is a snapshot as of 2026-11-05. "We found no benchmark that…" means no such benchmark turned up in targeted searches. It is not proof of absence.

## 2. The central references

### 2.1 Bercovich (2026), *Good Benchmarks* [P-full]

A short practitioner essay distilled from the Terminal-Bench experience. Good tasks are **verifiable, well-specified, solvable, difficult for a good reason, realistic and valuable, outcome-verified, and robust**. The paper's operational heuristics are directly usable:

- two experts writing verifiers from the same instruction should accept the same answers;
- reference solutions must solve the task "the way an agent would", without privileged information;
- verifiers must not be "co-designed with the author's own solution";
- the fairness check over-specifies the instruction temporarily and confirms that a guided agent passes;
- crux alignment checks that failures happen where the task claims to be hard;
- disputes over "standard practice" need a standard of evidence.

It also warns that **AI-mediated authoring degrades tasks** (§9) and that hard tasks can take **more than 40 hours** of expert and reviewer time (§10).

It is expert guidance, not an empirical study. The project uses it as a design standard, translated into the [task-quality rubric](../methodology/task-quality-rubric.md). Two tensions with DeepEcon's plans are flagged as Open questions:
- an AI-guided interview risks exactly the drift §9 describes (addressed by the protocol's safeguards);
- some economics failure modes may reduce to "one-sentence facts" (O-004).

### 2.2 Terminal-Bench-Science (TBS) and the Harbor format ([R1](evidence/R1-terminal-bench-science.md)) [P-full]

**Task anatomy.** A Harbor task is a directory with an instruction, metadata, environment, reference solution, and tests. TBS adds a reviewer README and an `authoring/` folder that never reaches the agent. Reward is binary, the verifier runs in a separate container, and the agent phase has open internet.

**Review process.**
- Lifecycle: Propose → Build → Review. Reviews include an LLM rubric review; parallel domain and technical reviewers; and a final "bar-raiser".
- Rubrics: a 7-criterion proposal rubric that echoes *Good Benchmarks* almost verbatim, and a 39-criterion implementation rubric.
- Validation: the oracle must score 1 and a no-op must score 0; agent trials; graded-hint runs (TBS's version of the fairness check); adversarial cheat trials; a hacker–fixer hardening loop.
- TBS validates its own LLM reviewer against intentionally broken tasks, with a 100% catch-rate gate.

**Relevance.** Statistics tasks in TBS already use most of what DeepEcon's verifier protocol proposes: many hidden simulated instances, conjunctive gates, metamorphic interventions, byte-identical reruns, named negative controls, and a structurally independent "witness" implementation. One TBS task (`ehr-error-detection`) injects errors into real data and scores detection, so injected-error detection is **not** new in itself.

**Scope.** TBS covers the life, physical, earth, mathematical, and engineering sciences and excludes economics subject matter by rule ("an in-scope method … applied to an out-of-scope subject is still out of scope").

**Leakage.** Answer keys and verification data are public, while agents have internet access. That model does not fit tasks derived from public economics papers.

**Implication.** TBS is a methodology and tooling donor (Apache-2.0), not a venue for DeepEcon's core tasks (O-011).

### 2.3 Sant'Anna's `interview-me` skill [P-full]

A compact skill that turns a fuzzy idea into a research specification. It uses six phases, one or two questions per turn, and about five to eight exchanges, and saves a Markdown spec. A post-flight step verifies citations in a **fresh context** that does not see the draft. DeepEcon adopts its conversational discipline, its downstream file contract, and the fresh-context verification. It must add what the skill lacks for our purpose:
- persistent, resumable state;
- statement-level provenance;
- safeguards against leading questions;
- machine-readable output;
- code and data as evidence;
- bilingual behaviour.

([Reading notes](reading-notes/interview-me-skill.md).)

## 3. What current benchmarks measure

### 3.1 Reproduction and replication ([R4](evidence/R4-replication-benchmarks.md))

| Benchmark | What it measures | How it is verified | Relevance to DeepEcon |
|---|---|---|---|
| CORE-Bench (2024) | Reproducing results from supplied code and data (CodeOcean capsules, including social science) | Answers to questions about outputs; manual validation reported | Treated as solved at the hardest level [S] |
| REPRO-Bench (ACL 2025) | Assessing the reproducibility of 112 social-science papers (mostly economics and political science) from public reproduction reports | Ordinal reproducibility score | Uses natural flaws; grades assessment, not methodological judgment [P-page] |
| SocSci-Repro-Bench (2026) | Reproduction tasks from 54 social-science papers (221 tasks) | Task-level accuracy | Claude Code reaches 93.4% [P-page]; contamination warning when materials are not anonymized [S] |
| ReplicatorBench (KDD 2026) | Replication with new data, from the SCORE project; includes economics | LLM judge on design and interpretation stages | Replication, not error judgment [P-page] |
| PaperBench (2025) | Replicating ML papers from scratch | Author-co-developed rubrics, LLM judge | Precedent for using original authors to define ground truth [P-page/S] |
| ReplicationBench (2025) | Replicating astrophysics papers | Tasks co-developed with original authors; author-set tolerances | Same precedent [S] |
| I4R "AI games" (Brodeur et al., PNAS 2026) | Human-only versus AI-assisted versus AI-led teams reproducing economics papers | Reproduction rates (recomputed in R4: 31/33, 32/35, 13/35); detection of **naturally occurring** coding errors against a catalogue of 122 errors in 12 papers | Closest human-plus-AI precedent in economics [P-page] |

**Pattern.** Reproduction with supplied code and data is near saturation. Economics benchmarks use naturally occurring errors, not designed ones, and none grades methodological judgment as an executable outcome.

### 3.2 Data analysis, causal inference, and econometric reasoning ([R5](evidence/R5-analysis-causal-econ-benchmarks.md))

| Benchmark | What it grades | Ground truth and alternatives | Economics content | Evidence |
|---|---|---|---|---|
| BLADE (EMNLP Findings 2024) | Analysis **decisions** (variables, transforms, models) | **Set-valued**: 502 expert specifications; peers judged 154 of 541 alternative transforms unsuited. In 101 of 145 multiple-choice items asking for the unjustifiable option, that option was LLM-generated | 4 of 12 datasets | [P-page] |
| CauSciBench (ICML 2026) | End-to-end applied causal inference on 175 real queries from 96 papers | Single reference estimate; effect correct within 5%; standard errors stored but **not graded** | High | [P-page] |
| CausalReasoningBenchmark (2026) | Identification specification and estimate, scored separately | Structured specification; reported figures differ between versions | Partial | [S] |
| CausalVerify (Sept 2026) | Method, design, execution, estimand recovery | Design hashed before data are revealed; gold designs list **admissible implementations**; 0.5 SE plus an SE ratio of 0.8–1.25 on the paired arm. Swapping in the reference design raised joint recovery from 15.0% to 51.5%; the scorer was revised three times after outputs existed (56.1% → 33.1% → 15.5%) | High (259 economics-paper contexts) | [P-page] |
| NBER WP 35588 (2026) | Econometric coding when the method is named | Reference outputs on simulated data | Methods only | [S] |
| QRData, InfiAgent-DABench, DiscoveryBench, DSBench, DA-Code, StatQA | General data analysis | Single answers: fixed methods, ±3% bands, or LLM judges | Small | [P-page/S] |
| CLadder, Corr2Cause, CaLM, EconLogicQA, EconNLI, STEER, EconEvals, EconWebArena, BenCSSmark, EconCausal | Formal causal or economic reasoning on synthetic or text items | Single answers | Theory or text | [P-page/S] |

**What this means for DeepEcon.**
- Method choice, design specification, and estimate recovery on real economics papers are already covered, most rigorously by CausalVerify, together with CauSciBench and CausalReasoningBenchmark.
- No benchmark found grades **inference choices** (clustering level, few-cluster corrections, inference under staggered timing) inside real economics replication packages as executable outcomes. The nearest precedents work elsewhere: CausalVerify grades standard-error ratios on synthetic twins, and a Terminal-Bench-Science causal-inference task verifies a code repair on seeded hidden instances ([R1](evidence/R1-terminal-bench-science.md) §8.2) [P-full].
- No benchmark found uses **expert-designed flawed versions of real replication packages**, either as verifier negative controls or as executable detection and correction tasks.
- CausalVerify's post-hoc scorer revisions are a direct warning for DeepEcon's verifier protocol: freeze verifiers before evaluation.

### 3.3 Error detection and injected flaws ([R6](evidence/R6-error-detection-and-verifier-methodology.md), [R4](evidence/R4-replication-benchmarks.md))

| Family | Examples | What we learn |
|---|---|---|
| Natural errors in papers | SPOT: 83 papers, 91 author-confirmed errors; no model exceeds 21.1% recall or 6.1% precision [P-page] | Detection is hard; precision is very low |
| Errors injected into paper text | FLAWS (GPT-5 finds 39.1% at k = 10) [S]; PaperAudit-Bench (8 error categories) [P-page]; LimitGen (11 perturbation types) [P-page]; Liu & Shah 2023 (GPT-4 found 7 of 13 planted errors) [S] | Injection into *text*, not runnable code |
| Errors injected into data | Terminal-Bench-Science `ehr-error-detection` (69 injected error clusters; recall 1.0 and precision ≥ 0.1 required) [P-full, R1] | Injected-error detection exists as a task format |
| Natural errors in economics packages | I4R AI games: a catalogue of 122 natural errors in 12 papers [P-page] | Real consequential errors exist in Top-5 packages |
| Economics-specific evidence | No model found known errors in four economic-theory papers without heavy human help (Toda 2026) [S]; remaining agent errors in econometric code are increasingly silent [S] | Thin but suggestive |

**Clean controls are rarely used, and they matter.** SPOT counts every unmatched flag as a false positive but has no clean twins [P-page]. A 2026 benchmark with matched clean twins found that models with identical recall differed by 79 points in false-alarm rate [S].

**No benchmark found builds deliberately flawed, executable economics replication packages** (code plus data) designed by domain experts.

### 3.4 Legitimate analytic dispersion ([R5](evidence/R5-analysis-causal-econ-benchmarks.md) §6)

- **With only a question and data, competent analysts disagree on sign and significance.** In Breznau et al.'s released data, 64.4% of 1,252 models are not significant, 19.5% significantly negative, and 16.1% significantly positive. Coded research steps explain at most 2.6% of the variance [P-page].
- **In applied microeconomics,** the spread of estimates across analysts was about three to four times the mean reported standard error (Huntington-Klein et al. 2021) [S].
- **More specification narrows dispersion but not to zero.** In the Many Economists study, 146 teams given shared cleaned data still had an interquartile range of 2.4 percentage points; its authors note that "the optimal level of researcher variation is not zero" [S].
- **Peers accept almost every pipeline.** In Multi100, only 1.6% of first-task pipelines were rated unacceptable [P-page].
- **AI agents vary less than humans.** In one 2026 study, human estimates were 2–27 times more dispersed than repeated Claude Code runs on the same tasks [S]. Calibrating acceptance regions on agent runs alone would therefore reject legitimate human alternatives.

**Consequences, adopted in the [verifier protocol](../methodology/verifier-validation-protocol.md) §4:**
- separate the estimand, the identifying assumptions, and the estimator, and fix the estimand before grading numbers;
- use a hidden decision space (reference / accepted / unjustifiable / contested), with constraints between options;
- allow declarations only for non-crux conventions from a benchmark-wide vocabulary, and grade crux decisions through outcomes on separating hidden variants;
- separate numerical noise, conventions, and substantive alternatives, and borrow no default tolerance band from another benchmark;
- calibrate with blind expert solves, and freeze verifiers before evaluation.

Several figures here are [S] or [U] and must be checked against the original papers before appearing in a public document.

## 4. How existing projects collect expert contributions

| Project | Who contributes | How | What is collected |
|---|---|---|---|
| Terminal-Bench-Science | Domain researchers (mostly PhD students, postdocs, engineers) | Web proposal form → GitHub pull request; reviewers act as shepherds (DRIs) | Complete tasks built by contributors themselves [P-full] |
| PaperBench | Original paper authors | Co-developed rubrics; author addenda for the agent and the judge | Ground-truth rubrics [P-page/S] |
| ReplicationBench | Original authors | Co-developed tasks; author-set tolerances | Task definitions and tolerances [S] |
| BLADE | Expert analysts | Annotation of analysis decisions as justifiable or not | Decision labels [S] |
| I4R games | Replicators | Reproduction teams; catalogue of natural errors | Error catalogue [P-page] |

**Gap.** None of these elicits original authors' knowledge of **plausible mistakes, rejected alternatives, or critical decisions** through a structured interview, or turns that knowledge into paired correct and flawed packages ([R4](evidence/R4-replication-benchmarks.md) §4c). R1 also notes that TBS ships Claude Code skills for **reviewers**, not for contributor elicitation.

## 5. How tasks are constructed and verified: lessons

1. **Verifier false negatives are common.** CORE-Bench's automatic grader rejected correct alternative techniques, and ScienceAgentBench released a "verified" split to reduce false negatives ([R4](evidence/R4-replication-benchmarks.md)) [S/P-page]. → DeepEcon calibrates acceptance regions on validated alternatives and widens them as agents reveal legitimate approaches.
2. **LLM judges are widespread and under-validated for economics.** PaperBench reports a judge evaluation (F1 0.83) [S]; most benchmarks do not. → LLM judges only in the unscored track, with measured agreement.
3. **Contamination is measurable.** Non-anonymized materials can lead to perfect scores [S]. Perturbed data defeat memorized numbers but not memory of the paper or its package. → Offline environments; a recognition probe; restructured presentations shared by flawed variants and clean twins; answer-changing hidden variants built on data the agent never sees; a private held-out split handled under exposure rules.
4. **Interpretation is manipulable.** A confirmatory prompt moved an agent's support verdicts from 10% to 90% with unchanged estimates [S]. → Neutral agent-facing instructions; claim-level grading.
5. **Statistical verification is mature in TBS.** Hidden simulated instances, metamorphic interventions, and witness implementations are established practice ([R1](evidence/R1-terminal-bench-science.md) §8) [P-full].

## 6. What DeepEcon adds — and what it does not

**The addition.** As far as targeted searches found (2026-11-05; several sources [S]), no benchmark builds tasks from published empirical-economics replication packages paired with expert-designed flawed variants, each with a realism warrant and an independent classification as established or conditional, and verifies them by re-running agents' code on hidden variants of the paper's own pipeline. The elements have precedents:
- repair tasks verified on hidden instances (Terminal-Bench-Science `highdim-mediation-debiasing`) [P-full];
- injected-error detection (Terminal-Bench-Science `ehr-error-detection`) [P-full];
- repair rounds and standard-error-ratio grading on synthetic twins (CausalVerify) [P-page];
- layer-separated scoring (CausalVerify, CausalReasoningBenchmark) [P-page/S];
- author-defined ground truth (PaperBench, ReplicationBench) [P-page/S].

The first release would score computational and statistical validity only; identification and interpretation would stay in an experimental, unscored track. The distinctive element is therefore **where the negative controls come from**: realistic, consequential mistakes designed by experts in the paper's own pipeline.

**How the knowledge is collected** is part of the method, not a claimed contribution: original authors or expert replicators are interviewed through a structured AI-guided protocol with statement-level provenance, whose validity is itself still to be established (§9, item 7).

**What it does not add** (overlaps to acknowledge in any public description):
- re-running packages when code and data are supplied (CORE-Bench, REPRO-Bench, SocSci-Repro-Bench, I4R);
- reimplementing papers without code (PaperBench, ReplicationBench, social-science reimplementation studies);
- using authors to define ground truth (PaperBench, ReplicationBench);
- error injection as a technique (FLAWS, PaperAudit, LimitGen, mutation testing, TBS's EHR task);
- separating identification from estimation on curated causal tasks (CausalReasoningBenchmark, CausalVerify);
- testing coding when the method is specified (NBER WP 35588, MetricsAI);
- many-analysts dispersion and interpretation vulnerability (the many-analysts studies, BLADE);
- natural errors with human adjudication (I4R, REPRO-Bench, SPOT).

**The window may be short.** FLAWS reportedly plans an economics extension; I4R's Replication Engine includes an error-finding agent; COS is building a robustness module ([R4](evidence/R4-replication-benchmarks.md) §5) [S].

## 7. Methodological foundations borrowed from other fields

### 7.1 Knowledge elicitation and AI-led interviews ([R7](evidence/R7-expert-elicitation-and-ai-interviews.md))

**Elicitation methods.** The Critical Decision Method (Klein, Calderwood & MacGregor 1989; Hoffman, Crandall & Shadbolt 1998) and Applied Cognitive Task Analysis (Militello & Hutton 1998) supply the probe structure:
- an incident;
- the expert's own timeline;
- cues, options, and the basis for choosing among them;
- novice hypotheticals;
- a record per decision of the difficult element, why it is difficult, common errors, and the cues and strategies used [S].

For contested questions, structured expert-judgment methods use several independent experts rather than one interview: Cooke's classical model, SHELF, and Delphi [S]. Question-form research warns that agree/disagree endorsements invite acquiescence and satisficing (Schuman & Presser 1981; Krosnick 1991, 1999) [S].

**AI-led interviews.**
- Interviewer quality is reported comparable to human interviewers in short opinion interviews (Geiecke & Jaravel) [S].
- Error profiles differ: AI interviewers mostly miss follow-ups (42% of violations) and make judgemental remarks (36%) (Wuttke et al.) [P-page; about 7 interviews per arm].
- Anthropic Interviewer reports 97.6% satisfaction among 1,250 participants in 10–15-minute interviews; its authors acknowledge demand effects [P-page].
- **No study found covers hours-long elicitation of technical knowledge from senior experts.**
- The open interview platforms all forbid suggesting answers, "not even a broad theme" [P-page].
- Their code carries non-commercial licences: Chopra & Haaland CC BY-NC 4.0; Geiecke & Jaravel PolyForm Noncommercial; Wuttke et al. CC0 [P-page]. Reuse is therefore of ideas, not code, unless the project's licence (O-010) is compatible.

**Deference.** In a 2026 Anthropic study, 50 analysts with causal-inference experience followed a Claude agent's secretly randomized lean on design choices 86% of the time; 77% repeated its arguments and 15% credited it; self-rated ownership did not distinguish followers [P-page]. Sycophancy also runs from model to user (Perez et al. 2022; Sharma et al. 2023) [P-page]. These findings drive the interview protocol's free-recall locks, exposure tracking, measured influence, and independent status classification (protocol v0.2.1 §0).

**Sant'Anna's workflow repository** (MIT licence, v2.6.0) is a template that users fork and update with manual git pulls, not a plugin [P-full]. It tests its own checks with planted defects and clean controls, and evaluates skills against a no-skill baseline with replicates [P-full], a practice the interview protocol adopts (§15). `interview-me` itself has not been evaluated, and the repository's journal profiles are unsourced referee-taste heuristics rather than methodological requirements [P-full; assessment].

### 7.2 Software testing and benchmark validity ([R6](evidence/R6-error-detection-and-verifier-methodology.md))

**Testing techniques, each with a hard limit** (references verified at [S] level):

| Technique | Key reference | Hard limit |
|---|---|---|
| Test oracles | Barr et al. 2015, *IEEE TSE* 41(5) | The oracle can itself be wrong |
| Mutation testing | DeMillo, Lipton & Sayward 1978, *Computer* 11(4) | Equivalent mutants cannot be identified automatically in general |
| Metamorphic testing | Chen, Cheung & Yiu 1998, HKUST technical report | Relations are necessary, not sufficient |
| N-version programming | Knight & Leveson 1986, *IEEE TSE* SE-12(1) | Independently written versions fail together; reported again for coding agents in 2026 [S] |
| Simulation-based calibration | — | Default calibration checks miss a model that ignores the data [P-full] |
| Semi-synthetic causal benchmarks | Dorie et al. 2019, *Statistical Science* 34 (ACIC 2016) | Encode the generator's assumptions |

**Benchmark-validity audits keep finding verifiers that are too weak** [S/P-page]:
- SWE-bench+: 31.08% of passed patches were suspect because of weak tests.
- The Agentic Benchmark Checklist: performance mis-estimated by up to 100% in relative terms.
- Terminal Wrench: 331 hackable environments, including one passed by replaying training labels.
- Hacker–fixer hardening cut exploits only from 50% to 39%.
- ImpossibleBench: GPT-5 exploited tests in 76% of one class of impossible tasks.

**Two contributions from R6 to our protocol.**
1. **"Same number, wrong procedure" is six different problems.** The types are semantic, data, observation, tolerance, power, and identification equivalence, and each has a different remedy.
2. **Additive effect injection is an exact, noise-free check, but of one thing only.** For a pipeline that is linear in the outcome on the estimand's scale, adding a known effect to treated outcomes moves the estimate by exactly the estimator's weighting of that effect over treated cells. An independent econometric review showed that this tests nothing about how the counterfactual is built: two clearly wrong estimators (a treated-minus-untreated mean and a treated-only before/after comparison) moved by exactly the target. Counterfactual-side invariances (adding anything in the span of the required fixed effects or controls; adding confounding orthogonal to the instruments) complement it, and answer-changing variants must be built on data the agent never sees, or a program can pass by arithmetic. R6 also showed that the draft protocol's clustering relation was wrong as written. All of this is incorporated in [verifier protocol](../methodology/verifier-validation-protocol.md) v0.3.0 (§5).

## 8. Economics-specific grounding ([R8](evidence/R8-replication-standards-and-econometric-pitfalls.md))

**Standards and archives.**
- The AEA Data Editor's Data and Code Availability Standard (DCAS) v1.0 (2022-12-15; 16 rules) is endorsed by 19 journals, including the AEA journals, *Econometrica*, *JPE*, and *REStud*. *QJE* does not appear on the list [P-page/P-full].
- Archives differ: AEA uses openICPSR, with pre-publication reproducibility checks; *JPE* uses Harvard Dataverse, and publication is conditional on its checks; *REStud* and the Econometric Society journals use Zenodo [P-full/P-page].
- Passing a data-editor check is not correctness: I4R found coding errors in about a quarter of economics studies it reproduced [S].

**Licensing and restrictions.**
- Deposit licences (CC BY 4.0 by default) do not override third-party terms. In November 2024, PSID extracts were removed from many AEA packages [P-full].
- Redistributability differs by source:
  - IPUMS extracts may be published to meet journal requirements;
  - PSID and WRDS (Compustat, CRSP) data may not be redistributed;
  - US federal works are generally public domain [P-full].
- About 72% of AEA intake cases involved some access restriction [P-full; unit and window unstated].

**Software and size.**
- Stata appears in 71.6% of more than 8,000 packages, R in 9.8%, and Python in 4.1% [S].
- AEA's Stata Docker images require a licence mounted at run time [P-page], and results can vary with the Stata version and processor count [P-full].
- The median package is 40.4 MB; about 20% exceed 2 GB [P-full].

**Pitfall catalogue.** R8 catalogues 21 consequential pitfalls, each with its consequence and a computational signature where one exists. Fourteen have an established core plus a computational signature; three are contested (Kelly's spatial-noise critique, how widespread Young's findings are, and weak-IV thresholds); about half change only standard errors. This catalogue seeds the **vetted pitfall taxonomy** the interview protocol requires (§7, §14). An independent econometric review corrected several statuses (see R8's corrections section): the regression-discontinuity entry is split into two established errors (global high-order polynomials; conventional confidence intervals at the MSE-optimal bandwidth) and a decision-space node (bandwidth choice); clustering by a discrete running variable is added as an established error; shift-share exposure-robust inference and multiple-testing corrections are conditional; robust standard errors in randomized trials are contested or conditional. Every entry still needs sign-off by a named econometrician, and 13 of the 35 references remain [U] in bibliographic detail.

**Established versus contested.** Documented errors such as Reinhart–Rogoff and Donohue–Levitt (Foote & Goetz 2008) differ in kind from contested methodological disputes, such as the Acemoglu–Johnson–Robinson and Albouy debate or the re-analyses of Miguel & Kremer. This is the distinction the protocol's independent status classification is designed to preserve (R8 §4).

## 9. What requires further methodological validation

1. **Yield:** consequential, realistic, discriminating failure modes per paper and per interview hour.
2. **Discriminability on real data:** how often flagship flawed variants are data-equivalent on the evaluation data, and how many answer-changing hidden instances, on data the agent never sees, each task needs.
3. **Synthetic-data realism:** whether fully synthetic data for restricted sources preserve the mistake's consequence without encoding the contributor's assumptions (*Good Benchmarks* §7), given that they lose real-data quirks such as duplicates and miscoded treatment.
4. **Re-execution practicality:** whether agents' code runs reliably under a benchmark-wide output contract without measuring format compliance.
5. **Clean controls:** whether correction and detection tasks with clean controls separate judgment from over-correction, with repair and preservation scored separately.
6. **Expert agreement:** whether economists agree enough to key identification and interpretation items (V3), and whether two blind outside economists agree on a task's acceptance criteria.
7. **Interview validity:** whether the AI-guided interview elicits contributor-originated content rather than AI-planted content (LLM-originated share, recall of a sealed key on pre-exposure items, false endorsement of known-valid controls).
8. **Effort and cost:** shepherd-team hours per stage for admitted and dropped candidates; outside-economist hours; validation trials per task.
9. **"One-sentence-fact" tasks:** whether they measure capability or recall (O-004), measured with the hint ladder and knowledge probe.
10. **Recognition:** whether restructured presentations and ports stop evaluated models from recognizing canonical papers and repairing flaws from memory.

The pilot's methodology arm takes surviving candidates (or a random sample of at least six, stratified by arm) through validation rungs L0–L12 to test items 1–6, 8, and 10 ([pilot plan](../pilot/pilot-evaluation-plan.md)).

## 10. Sources

Full source lists, with URLs, access dates, and evidence labels, are in each evidence note ([index](evidence/README.md)). Primary references used throughout:
- Bercovich, I. (2026). *Good Benchmarks*. arXiv:2607.12217v1 [P-full].
- Terminal-Bench-Science repository, commit `9276073` (2026-11-04) [P-full].
- `pedrohcgs/claude-code-my-workflow`, `interview-me` skill, commit `7586127` (2026-11-04) [P-full].

## 11. Changes

**v0.2.0** (independent reviews, 2026-11-05): novelty statement narrowed and precedents added (§6), with the interview moved into the method description; effect injection restated with its limits and complements (§7.2); acceptance-region lessons updated (§3.4); contamination lesson extended to memory of methods (§5); pitfall-status corrections noted (§8); validation agenda extended (§9).
