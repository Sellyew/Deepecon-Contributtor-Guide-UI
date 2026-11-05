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
4. **Procedure tested through outcomes.** Agents deliver code; verifiers re-run it on hidden data variants and check econometric metamorphic relations. The strongest is **additive effect injection**: add a known effect to treated outcomes in the real data, and a correct estimator must move by exactly the estimand's weighting of that effect. In a numerical check, an imputation estimator moved by the target ATT of 2.062 while two-way fixed effects moved by 1.421 ([R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) Appendix A). This reconciles *Good Benchmarks*' "grade outcomes, not process" with the brief's "correct output is not correct procedure" ([verifier protocol](../methodology/verifier-validation-protocol.md) §5).
5. **Pre-registered consequences.** Contributors predict how a mistake will change the estimate before it is run. This tests understanding and prevents post-hoc rationalization.
6. **By-products with independent value.** A citable catalogue of credibility criteria, replacing journal-rank intuitions (brief §3.4); and flawed packages that double as planted-defect fixtures for validating AI reviewers.

### Where it may fail, and what would guard against each failure

| Failure mode | Why it matters | Guard |
|---|---|---|
| **"Same number, wrong procedure"**: the flawed procedure matches the correct one on the evaluation data | Six distinct cases ([verifier protocol](../methodology/verifier-validation-protocol.md) §2). Most can be caught with new inputs or more outputs. Identification-equivalence cannot be caught by any outcome check | Effect injection and other separating hidden variants; requiring standard errors and diagnostics as outputs; structured expert judgment for identification-equivalent cases |
| **Verifier co-designed with one solution** | Correct alternatives rejected; the many-analysts literature shows real legitimate dispersion | Acceptance regions calibrated on validated alternatives; the "two experts, two verifiers" test; tighten the estimand (*Good Benchmarks* §4, §7) |
| **Contamination**: published results and public packages | Agents can recall or look up answers; one study reports perfect scores on non-anonymized materials [S] | Offline task environments; perturbed or semi-synthetic data; re-execution on hidden data; restyled code; private held-out set (O-001) |
| **"One-sentence-fact" tasks** | Disclosing one fact (e.g., the right clustering level) may make a task trivial; *Good Benchmarks* §9 calls such tasks weak | Explicit policy (O-004): keep only when recognizing the fact from the disclosed design is the capability under test |
| **Contested "errors"** | Binary keys would encode a false ground truth | Status classification (established / conditional / contested); contested items leave scored tasks (X-003) |
| **AI-driven drift in contributions** | Experts agreeing with an AI interviewer can produce artificial tasks (*Good Benchmarks* §9) | Contributor-first elicitation, provenance, LLM-origin monitoring, human-authored instructions |
| **Errors in the "correct" package** | Published packages contain real errors (the I4R catalogue lists 122 across 12 papers [P-page]) | Independent checks; treat discoveries as findings; label clean controls "no known consequential error" |
| **Effort and yield** | Hard tasks can take more than 40 hours of expert and reviewer time (*Good Benchmarks* §10) | Quality over quantity; shepherd role; measure in the pilot |
| **Environment** (Stata, data licences) | Stata appears in 71.6% of packages [S]; about 72% of AEA intake cases involve restricted data [P-full] ([R8](../research/evidence/R8-replication-standards-and-econometric-pitfalls.md)) | R/Python ports checked for numerical equivalence on two platforms; effect-injected or semi-synthetic data; restricted data never shipped; a licensed Stata track only with leakage controls |
| **Novelty window** | Others are moving toward error-based evaluation in economics ([R4](../research/evidence/R4-replication-benchmarks.md) §5) [S] | Prioritize the distinctive parts; consider partnering (e.g., I4R, O-015) |

### What still needs methodological validation

How many consequential, discriminating mistakes an interview yields per paper; whether semi-synthetic variants preserve the mistake without encoding the contributor's assumptions; whether re-executing agent code under a minimal input–output contract works without becoming a format test; whether audit-and-correct tasks with clean controls measure judgment; whether economists agree enough to key identification and interpretation items; and how many shepherd hours an admitted task costs. These are listed in the [construction protocol](../methodology/benchmark-construction-protocol.md) §9 and targeted by the [pilot](../pilot/pilot-evaluation-plan.md).

## Question 2 — Expert interview design

> *How can an adaptive AI-guided interview extract economists' tacit knowledge about consequential research mistakes, while avoiding leading questions, fabricated errors, and superficial discussion?*

### The key risk, from evidence rather than intuition

The strongest danger is not that the AI asks bad questions. It is that experts **absorb the AI's views without noticing**. In a 2026 Anthropic study, 50 analysts with causal-inference experience worked with a Claude agent secretly given a random lean on four design choices. They followed the lean **86%** of the time; 77% repeated its arguments, and only 15% credited it. Self-rated ownership did not distinguish who had been swayed ([R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) §3.4) [P-page]. The study has limits: no human-only control, one task, one model. But it is the closest evidence to our situation. Asking for the expert's view first is necessary but not sufficient, and influence must be **measured by design**.

### Approach

The [protocol](../interview/expert-interview-protocol.md) (v0.2.0) adapts two established knowledge-elicitation methods to discovering consequential research mistakes:
- the **Critical Decision Method**: an incident, the contributor's own timeline, cues, options and their basis, and "what would a novice do?";
- **Applied Cognitive Task Analysis**: a record per decision of the difficult element, why it is difficult, common errors, and the cues and strategies used.

It moves from the paper's design (S1), to the decisions that made it credible (S2), to plausible wrong alternatives (S3), to their consequences and classification (S4), to code-level operationalization (S5) and task design (S6), and ends with the contributor's review and sign-off (S7). Sessions last 45–60 minutes. The research lead's example progression is built in as probes, not as a script.

### Safeguards

| Risk | Safeguards |
|---|---|
| **Experts absorbing the AI's views** | A **free-recall lock**: the contributor's unaided, timestamped list comes before any suggestion or code pointer. Exposure tracking on every statement. Influence reported as **measured** shares (LLM-originated, post-exposure, LLM-influenced) plus a false-endorsement rate on disclosed known-valid controls. The pilot randomizes whether suggestions are offered at all (O-017). |
| **Leading questions** | Ask before pointing: the contributor locates decisions in the code before the AI shows them. No yes/no endorsements; two-sided suggestions with rotated order; at most three per decision, from a vetted pitfall taxonomy only. A rejected suggestion is never re-raised. |
| **Fabricated errors** | "No realistic mistake here" is stated to be a complete answer, and there are no quotas. A mandatory realism warrant records whether the mistake was observed (where) or is hypothetical. An **evidence bundle** is required: the mechanism, the warrant, a test that distinguishes correct from flawed, and a cited rule. The status of each mistake (established, conditional, or contested) is set by **at least two independent, blind classifications** by other economists, not in the conversation. |
| **Superficial discussion** | Evidence-first: the AI reads the paper and code before asking, and never asks what they already say. Laddering continues until the mechanism is stated as an estimand, assumption, measurement, or inference property. The interviewer's own turns are short, so they cannot become the sophisticated-but-irrelevant discussion the brief warns about. |
| **Sycophancy, model toward expert** | No evaluative remarks. Disagreements cite file and line, and are never retracted without new evidence. Unresolved disagreements go to the shepherd. Checkers (citations, triviality, leakage) run in a fresh context without the conversation. |
| **Authority** | Statement-level provenance and contributor disposition. The contributor can edit, reject, or withdraw anything. Stage summaries use the contributor's own words, with a 1–4 accuracy rating. Agent-facing task text must be human-written or substantially human-edited. |

### How we will know it works

The protocol is first tested the way a checker is tested: against a baseline interviewer, with replicates, and with model-played personas (one that pushes back, one holding a wrong belief, one prone to deference). Transcripts are coded by two coders for leading questions and judgemental remarks. The pilot then measures real yield, recall of a sealed known-issues key, blind quality ratings, and measured AI influence, with the suggestion phase randomized. Perceived ownership is kept as an experience measure only, because it did not track influence in the deference study.

## Question 3 — Hosted contributor platform (Option A)

> *What would a rigorous but reasonably lightweight hosted platform require, and how should its parts interact?*

**Requirements.** A bilingual web application (sign-in, consent, uploads, staged interview with progress display, live dossier panel with provenance, review and submission), an interview orchestrator that uses the pinned model through tools (read file, search code, update dossier, record suggestion), a database, encrypted object storage, server-side validation and packaging, a minimal shepherd console, and monitoring with per-session cost caps. Details: [Option A design](../architecture/option-a-hosted-platform.md).

**A hosted interview does not require hosted execution.** The proposed MVP (A1) runs the interview on project servers while code runs under the contributor's control: generated run kits are executed by the contributor or a research assistant, and only outputs are uploaded. Execution can also happen on staff machines during shepherding, which suits *Good Benchmarks*' division of labour. A hosted R/Python sandbox (A2) can be added later for public-data papers. Stata in a hosted sandbox raises licensing questions [pending R9].

**Reference stack, verified** ([R9](../research/evidence/R9-hosted-stack-and-compliance.md)):
- a custom Next.js application on the Claude Messages API, with next-intl, Better Auth (magic links, ORCID through OpenID Connect), Neon Postgres, Cloudflare R2 (EU), and Langfuse (EU);
- hosting costs about **$13–210 a month** from pilot to 200 contributors.

Existing open-source interview platforms use non-commercial licences, so we reuse their ideas, not their code. Running the same skill server-side through the Agent SDK is technically feasible. Anthropic's terms, however, say customers running Claude Code in their products "may not pay for … Claude usage on their end users' behalf", so that variant needs confirmation (O-018).

**Regional constraint.** The Usage Policy prohibits facilitating access for users in unsupported regions, "including end users". A Claude-based platform therefore cannot serve contributors located in mainland China, Hong Kong, or Macau (O-007).

Effort: about 12–19 engineer-weeks beyond the shared core (A1 plus staff execution). Inference ≈ $17 per contribution at list prices.

## Question 4 — Local Claude Code skill (Option B)

> *How would the same contribution experience be implemented through a locally executed skill? Requirements, benefits, limitations, and costs?*

**Implementation.** A Claude Code plugin containing the interview skill (orchestration rules plus stage cards, probe library, and pitfall taxonomy loaded on demand), a schema-validating helper for state and provenance, run wrappers for Stata, R, and Python, layered protection of original files (read-only workspace, permission rules, a hook, an integrity checksum before export), a package doctor, and locale assets. Details: [Option B design](../architecture/option-b-local-skill.md).

**Requirements for contributors.**
- **Claude Code:** in a terminal (macOS 13+, Windows 10 1809+, Linux) or in the desktop app's Code tab, the no-terminal path. Cowork is unsuitable because it runs code on Anthropic's servers rather than with the contributor's Stata.
- **A paid plan or project-provided access:** Pro is $20 a month; Free cannot run Claude Code.
- **Location:** a supported region (mainland China, Hong Kong, and Macau are not supported).
- **Software:** Python for helper scripts and the paper's own software.
- **Setup:** comfort installing a plugin and workspace template, or a research assistant who has it.

Sources: [R2](../research/evidence/R2-claude-code-platform.md), [R3](../research/evidence/R3-access-pricing-policy-portability.md).

**Benefits.** Real local execution, including Stata, which appears in 71.6% of economics replication packages [S]. No project custody of unpublished materials. Lower project engineering and near-zero hosting.

**Limitations.**
- **Setup burden** for non-technical economists.
- **No enforced model.** A plugin cannot require a model; consistency needs project-controlled accounts or a gateway.
- **Default modes work against an interview.** Auto mode is the default and "nudges Claude to keep working without stopping for clarifying questions", so the skill must make waiting explicit.
- **Weak guarantees on file access.** Plugins cannot ship permission rules (hence a workspace template). Read-deny rules do not stop subprocesses from reading files.
- **Varying data terms.** Consumer plans train on data unless the user opts out, with feedback and safety exceptions. That exposes hidden materials unless the project provides commercial access.
- **Fast-moving client.** It ships several releases a week and marketplaces do not auto-update.
- **Regional limits** on who can use it.

**Costs.**
- **Contributors:** a paid plan (from $20 a month), unless the project provides access, plus time.
- **Project:** development (≈ 8–14 engineer-weeks beyond the shared core), plugin maintenance (≈ 0.05–0.15 FTE), and higher per-contributor support. Inference cost to the project is $0, or ≈ $17 per contribution if access is provided, subject to the terms question O-018. Reimbursing one month of Pro for 200 contributors ($4,000) would cost more than direct API inference (≈ $3,400).

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
