# Initial Assessment: Answers to the Five Questions

| | |
|---|---|
| **Status** | **Proposed** assessment, 2026-11-05, for the research lead. Recommendations are not decisions; see the [decision log](../decisions/decision-log.md). |
| **Questions** | From §14 of the [research lead's brief](../requirements/2026-11-05-research-lead-brief.md#14-immediate-assignment) |
| **Evidence** | [Reading notes](../research/reading-notes/) and [evidence notes R1–R9](../research/evidence/), with evidence labels: [P-full] primary, full text; [P-page] primary page; [S] secondary; [U] unverified |

---

## Question 1 — Scientific feasibility

> *Can combining correct and deliberately erroneous replication packages produce scientifically meaningful, objectively verifiable economics benchmark tasks? What are its strongest features, and where might it fail?*

### Short answer

**Yes, for a well-defined subset, under conditions; not as a universal method.**

- **Computational and statistical validity.** Pairing a validated reference implementation with expert-designed flawed variants can produce objectively verifiable tasks when an error leaves a computational or statistical signature that survives on the evaluation data. Examples: an estimator–implementation mismatch, wrong treatment timing, a wrong estimation sample, wrong clustering, two-way fixed effects under staggered adoption with dynamic effects.
- **Identification and interpretation.** The pairing cannot by itself create objective ground truth here. Untestable assumptions and contested judgments need expert-consensus answer keys, or they must stay unscored. This follows the research lead's own distinction among computational correctness, statistical validity, and identification validity (D-013).

### Strongest methodological features

1. **Negative controls built in.** Every expert-designed flawed variant is a test the verifier must fail. Weak verifiers that accept wrong answers are a known failure of agent benchmarks ([R1](../research/evidence/R1-terminal-bench-science.md) §3–§4; [R4](../research/evidence/R4-replication-benchmarks.md) summary). Terminal-Bench-Science already requires "measured separation" from structurally independent comparators [P-full]; DeepEcon's comparators would be *realistic research mistakes* rather than author-invented ones.
2. **Realism by construction.** The mistakes come from people who know which errors matter, with a recorded realism warrant. That directly addresses Safeguard G (real errors versus artificial mutations).
3. **A construct that is not yet saturated.** Plain reproduction is close to solved for frontier agents (Claude Code reaches 93.4% on SocSci-Repro-Bench) [P-page]. DeepEcon targets the *decisions* that make results credible, which existing economics benchmarks do not grade as executable outcomes ([R4](../research/evidence/R4-replication-benchmarks.md) §4–§5).
4. **Procedure tested through outcomes.** Agents deliver code; verifiers re-run it on hidden data variants and check econometric metamorphic relations (e.g., duplicating a panel with new cluster identifiers must shrink cluster-robust standard errors by about 1/√2). This reconciles *Good Benchmarks*' "grade outcomes, not process" with the brief's "correct output is not correct procedure" ([verifier protocol](../methodology/verifier-validation-protocol.md) §5).
5. **Pre-registered consequences.** Contributors predict how a mistake will change the estimate before it is run. This tests understanding and prevents post-hoc rationalization.
6. **By-products with independent value.** A citable catalogue of credibility criteria, replacing journal-rank intuitions (brief §3.4); and flawed packages that double as planted-defect fixtures for validating AI reviewers.

### Where it may fail, and what would guard against each failure

| Failure mode | Why it matters | Guard |
|---|---|---|
| **Equivalent mutants**: the flawed procedure gives the same number as the correct one on the evaluation data | No outcome check can then detect the mistake | Hidden data variants that separate them; semi-synthetic data; otherwise drop the variant ([validation ladder](../methodology/verifier-validation-protocol.md) L7) |
| **Verifier co-designed with one solution** | Correct alternatives rejected; the many-analysts literature shows real legitimate dispersion | Acceptance regions calibrated on validated alternatives; the "two experts, two verifiers" test; tighten the estimand (*Good Benchmarks* §4, §7) |
| **Contamination**: published results and public packages | Agents can recall or look up answers; one study reports perfect scores on non-anonymized materials [S] | Offline task environments; perturbed or semi-synthetic data; re-execution on hidden data; restyled code; private held-out set (O-001) |
| **"One-sentence-fact" tasks** | Disclosing one fact (e.g., the right clustering level) may make a task trivial; *Good Benchmarks* §9 calls such tasks weak | Explicit policy (O-004): keep only when recognizing the fact from the disclosed design is the capability under test |
| **Contested "errors"** | Binary keys would encode a false ground truth | Status classification (established / conditional / contested); contested items leave scored tasks (X-003) |
| **AI-driven drift in contributions** | Experts agreeing with an AI interviewer can produce artificial tasks (*Good Benchmarks* §9) | Contributor-first elicitation, provenance, LLM-origin monitoring, human-authored instructions |
| **Errors in the "correct" package** | Published packages contain real errors (the I4R catalogue lists 122 across 12 papers [P-page]) | Independent checks; treat discoveries as findings; label clean controls "no known consequential error" |
| **Effort and yield** | Hard tasks can take more than 40 hours of expert and reviewer time (*Good Benchmarks* §10) | Quality over quantity; shepherd role; measure in the pilot |
| **Environment** (Stata, data licences) | Proprietary software and restricted data break reproducible evaluation | R/Python ports checked for numerical equivalence; a licensed track; semi-synthetic data; restricted data never shipped |
| **Novelty window** | Others are moving toward error-based evaluation in economics ([R4](../research/evidence/R4-replication-benchmarks.md) §5) [S] | Prioritize the distinctive parts; consider partnering (e.g., I4R, O-015) |

### What still needs methodological validation

How many consequential, discriminating mistakes an interview yields per paper; whether semi-synthetic variants preserve the mistake without encoding the contributor's assumptions; whether re-executing agent code under a minimal input–output contract works without becoming a format test; whether audit-and-correct tasks with clean controls measure judgment; whether economists agree enough to key identification and interpretation items; and how many shepherd hours an admitted task costs. These are listed in the [construction protocol](../methodology/benchmark-construction-protocol.md) §9 and targeted by the [pilot](../pilot/pilot-evaluation-plan.md).

## Question 2 — Expert interview design

> *How can an adaptive AI-guided interview extract economists' tacit knowledge about consequential research mistakes, while avoiding leading questions, fabricated errors, and superficial discussion?*

### Approach

The [protocol](../interview/expert-interview-protocol.md) adapts knowledge-elicitation methods from cognitive task analysis, which retrospectively probe specific hard incidents (verification of these methods' literature: [R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md)). It moves from the paper's design (S1), to the decisions that made it credible (S2), to plausible wrong alternatives (S3), their consequences and classification (S4), their code-level operationalization (S5), and task design (S6), ending with the contributor's review and sign-off (S7).

The research lead's example progression ("What was the most difficult challenge?" → "What would an RA have done instead?" → "What would that change?" → "Where in the code?" → "How could a verifier tell?") is built in as probes, not as a script.

### Safeguards

| Risk | Safeguards |
|---|---|
| **Leading questions and anchoring** | Contributor-first rule: the AI offers suggestions only after the contributor's own ideas are exhausted, at most two or three at a time, framed neutrally with "not a mistake here" as an equal answer. A rejected suggestion is never re-raised. Every suggestion's disposition is logged, and a high share of AI-originated items triggers review. |
| **Fabricated errors** | No item enters the dossier without the contributor's own reasoning, a code location, a pre-registered predicted consequence, and — before admission — executed evidence and an independent domain review. The interviewer is forbidden to invent errors to fill a template; empty fields are acceptable. |
| **Superficial discussion** | Evidence-first questioning: the interviewer reads paper and code first and never asks what the artifacts already say. Laddering ("Why would it move in that direction?") continues until the mechanism is stated in terms of an estimand, an assumption, or an inference property. Vagueness and triviality checks raise visible flags. |
| **Sycophancy in either direction** | The interviewer disagrees with evidence ("At file:line the code clusters by county…") but never insists. It never flatters and never calls anything validated. Literature claims are checked by a separate, fresh-context verifier that does not see the draft (adopted from `interview-me`). |
| **Authority** | Every statement carries provenance (contributor, research assistant, AI-suggested, AI-summarized, reviewer) and the contributor's disposition. The contributor can edit, reject, or withdraw anything. Agent-facing task text must be human-written or substantially human-edited. |

### How we will know it works

A simulated-contributor test suite checks protocol mechanics: recall of a persona's known items; planting rate; challenging a persona's mistaken belief; one-or-two-questions discipline; stopping behaviour. The pilot then measures real yield, recall of a sealed known-issues key, blind quality ratings, AI-origin share, and perceived ownership.

## Question 3 — Hosted contributor platform (Option A)

> *What would a rigorous but reasonably lightweight hosted platform require, and how should its parts interact?*

**Requirements.** A bilingual web application (sign-in, consent, uploads, staged interview with progress display, live dossier panel with provenance, review and submission), an interview orchestrator that uses the pinned model through tools (read file, search code, update dossier, record suggestion), a database, encrypted object storage, server-side validation and packaging, a minimal shepherd console, and monitoring with per-session cost caps. Details: [Option A design](../architecture/option-a-hosted-platform.md).

**A hosted interview does not require hosted execution.** The proposed MVP (A1) runs the interview on project servers while code runs under the contributor's control: generated run kits are executed by the contributor or a research assistant, and only outputs are uploaded. Execution can also happen on staff machines during shepherding, which suits *Good Benchmarks*' division of labour. A hosted R/Python sandbox (A2) can be added later for public-data papers. Stata in a hosted sandbox raises licensing questions [pending R9].

**Lightweight paths.** Reuse an open-source AI-interview platform, or run the same skill as Option B server-side through the Claude Agent SDK [pending R2/R9]. Effort: about 11–18 engineer-weeks beyond the shared core (A1). Inference ≈ $17 per contribution at list prices.

## Question 4 — Local Claude Code skill (Option B)

> *How would the same contribution experience be implemented through a locally executed skill? Requirements, benefits, limitations, and costs?*

**Implementation.** A Claude Code plugin containing the interview skill (orchestration rules plus stage cards, probe library, and pitfall taxonomy loaded on demand), a schema-validating helper for state and provenance, run wrappers for Stata, R, and Python, layered protection of original files (read-only workspace, permission rules, a hook, an integrity checksum before export), a package doctor, and locale assets. Details: [Option B design](../architecture/option-b-local-skill.md).

**Requirements for contributors.** Claude Code (terminal or desktop app) and model access through their own plan or project-provided access [plan details pending R3]; the paper's software; and comfort installing a plugin — or a research assistant who has it.

**Benefits.** Real local execution, including Stata. No project custody of unpublished materials. Lower project engineering (≈ 7–12 engineer-weeks beyond the shared core) and near-zero hosting.

**Limitations.** Setup burden for non-technical economists. Interviewer consistency varies unless the project provides model access. Data-use terms vary with each contributor's account: consumer plans with training enabled would expose hidden materials [pending R3]. The plugin depends on a fast-moving client. Availability by region.

**Costs.**
- **Contributors:** a plan, unless the project provides access, plus time.
- **Project:** development, plugin maintenance (≈ 0.05–0.15 FTE), and higher per-contributor support. Inference cost to the project is $0, or ≈ $17 per contribution if access is provided.

## Question 5 — Architectural comparison

> *Which trade-offs should collaborators discuss, and what should a pilot measure?*

**Trade-offs to discuss** (detailed in the [decision brief](../architecture/architecture-decision-brief.md) §4):
1. consistency versus reach;
2. who runs the code;
3. custody versus dispersion of sensitive material;
4. building and operating versus supporting;
5. who pays for model access, and under which data-use terms.

Inference cost is small either way and should not drive the decision. Human effort (shepherds and reviewers) dominates under both options.

**What the pilot should measure** ([pilot plan](../pilot/pilot-evaluation-plan.md)):
- setup completion and time, by technical fluency;
- time to first substantive question, and drop-off points;
- candidate yield, and how many candidates become validated flawed variants;
- recall of a sealed known-issues key;
- blind quality ratings, with inter-rater agreement;
- AI-origin share of endorsed items, and perceived ownership;
- usability;
- tokens and cost per session, support minutes, and shepherd hours per admitted task;
- comfort with data flows.

Decision thresholds should be agreed **before** the pilot.

## The most important open questions

The full list is in the [decision log](../decisions/decision-log.md) (O-001 to O-016). The five that most constrain what happens next:

1. **O-002** — pilot both options or choose one now;
2. **O-001** — release policy (public, private, or split), which constrains submission and leakage controls;
3. **O-007** — legal review of participation by contributors in mainland China;
4. **O-009** — staffing of shepherds and reviewers, the dominant cost;
5. **O-014** — the project name, which collides with an existing "deepecon" econometrics package.
