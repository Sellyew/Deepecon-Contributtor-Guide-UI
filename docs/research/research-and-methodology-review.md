# Deliverable 1 — Research and Methodology Review

| | |
|---|---|
| **Status** | **Proposed** v0.1.0 (2026-11-05). A search-based review, not a systematic survey. |
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

### 3.2 Data analysis, causal inference, and econometric reasoning

*Pending evidence note [R5](evidence/R5-analysis-causal-econ-benchmarks.md).*

R4 identified partial coverage of identification and inference judgment on curated causal tasks, all [S]:
- CausalReasoningBenchmark scores the identification specification separately from the estimate.
- CauSciBench finds method selection is the bottleneck.
- CausalVerify commits the design before revealing the data, with an "oracle arm".
- BLADE grades analysis decisions against expert-annotated justifiable and unjustifiable choices.
- NBER WP 35588 tests econometric coding when the method is named.

No benchmark found grades **inference** choices (clustering level, few-cluster corrections, inference under staggered timing) in published economics packages as executable outcome checks.

### 3.3 Error detection and injected flaws

*To be completed with evidence note [R6](evidence/R6-error-detection-and-verifier-methodology.md).*

R4 found error injection in three settings: in **paper text** (FLAWS, PaperAudit-Bench, LimitGen-Syn, a clinical-trial seeding study); as planted pitfalls for AI-scientist systems in machine learning; and in one corrupted-model task in RE-Bench [S/P-page]. TBS's `ehr-error-detection` injects errors into data [P-full]. **No benchmark found builds deliberately flawed, executable economics replication packages** (code plus data) designed by domain experts.

### 3.4 Legitimate analytic dispersion

*Pending evidence note R5 (many-analysts and multiverse literature).*

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
3. **Contamination is measurable.** Non-anonymized materials can lead to perfect scores [S]. → Offline environments, perturbed data, re-execution on hidden data, a private held-out set.
4. **Interpretation is manipulable.** A confirmatory prompt moved an agent's support verdicts from 10% to 90% with unchanged estimates [S]. → Neutral agent-facing instructions; claim-level grading.
5. **Statistical verification is mature in TBS.** Hidden simulated instances, metamorphic interventions, and witness implementations are established practice ([R1](evidence/R1-terminal-bench-science.md) §8) [P-full].

## 6. What DeepEcon adds — and what it does not

**The addition** (each element has precedents in isolation; the combination appears new for empirical economics as of 2026-11-05):

1. **Executable correct packages paired with expert-designed flawed packages** from published empirical economics papers.
2. Each flaw is a **realistic, scientifically consequential mistake** — in identification, inference, sample construction, treatment timing, or variable definition — with a documented consequence, a realism warrant, and evidence that it is wrong rather than a valid alternative.
3. The flaws become **outcome-verified tasks** (error correction, research execution where the flaw is the crux, structured detection with clean controls), graded so that computational, statistical, identification, and interpretation validity are kept apart.
4. The knowledge comes from **original authors or expert replicators through a structured AI-guided interview** with statement-level provenance.

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

*To be completed with evidence notes R6 (software testing, benchmark validity) and R7 (knowledge elicitation, AI-led interviews).*

## 8. Economics-specific grounding

*To be completed with evidence note R8 (replication standards, data licensing, econometric pitfalls, documented real and contested errors).*

## 9. What requires further methodological validation

1. **Yield:** consequential, realistic, discriminating failure modes per paper and per interview hour.
2. **Discriminability on real data:** how often flagship flawed variants are equivalent mutants on the evaluation data; how often semi-synthetic variants are needed.
3. **Semi-synthetic realism:** whether generated data preserve the mistake's consequence without encoding the contributor's assumptions (*Good Benchmarks* §7).
4. **Re-execution practicality:** whether agents' code runs reliably under a minimal contract without measuring format compliance.
5. **Clean controls:** whether audit-and-correct tasks with clean controls separate judgment from over-correction.
6. **Expert agreement:** whether economists agree enough to key identification and interpretation items (V3).
7. **Interview validity:** whether the AI-guided interview elicits contributor-originated content rather than AI-planted content (LLM-origin share, recall of a sealed key).
8. **Effort:** shepherd hours per admitted task, by stage.
9. **"One-sentence-fact" tasks:** whether they measure capability or recall (O-004).

## 10. Sources

Full source lists, with URLs, access dates, and evidence labels, are in each evidence note ([index](evidence/README.md)). Primary references used throughout:
- Bercovich, I. (2026). *Good Benchmarks*. arXiv:2607.12217v1 [P-full].
- Terminal-Bench-Science repository, commit `9276073` (2026-11-04) [P-full].
- `pedrohcgs/claude-code-my-workflow`, `interview-me` skill, commit `7586127` (2026-11-04) [P-full].
