# Initial Assessment: Answers to the Five Questions

| | |
|---|---|
| **Status** | **Proposed** assessment, 2026-11-05, for the research lead. Recommendations are not decisions; see the [decision log](../decisions/decision-log.md). Revised the same day after four independent reviews (econometrics, benchmark methodology, and one advocate for each architecture); the main corrections are listed at the end. |
| **Questions** | From §14 of the [research lead's brief](../requirements/2026-11-05-research-lead-brief.md#14-immediate-assignment) |
| **Evidence** | [Reading notes](../research/reading-notes/) and [evidence notes R1–R9](../research/evidence/), with evidence labels: [P-full] primary, full text; [P-page] primary page; [S] secondary; [U] unverified |

---

## Question 1 — Scientific feasibility

> *Can combining correct and deliberately erroneous replication packages produce scientifically meaningful, objectively verifiable economics benchmark tasks? What are its strongest features, and where might it fail?*

### Short answer

**Yes, for a well-defined subset, under conditions; not as a universal method.**

- **Computational and statistical validity.** Pairing a validated reference implementation with expert-designed flawed variants can produce objectively verifiable tasks when an error leaves a computational or statistical signature that survives on the evaluation data and on hidden variants. Examples: an estimator–implementation mismatch, wrong treatment timing, a wrong estimation sample, clustering finer than the assignment level, two-way fixed effects under staggered adoption with heterogeneous effects.
- **Identification and interpretation.** The pairing cannot by itself create objective ground truth here. Untestable assumptions and contested judgments need expert-consensus answer keys, or they must stay unscored. This follows the research lead's own distinction among computational correctness, statistical validity, and identification validity (D-013). The first release would therefore score computational and statistical validity only.

### Strongest methodological features

1. **Negative controls built in.** Every expert-designed flawed variant is a test the verifier must fail. Weak verifiers that accept wrong answers are a known failure of agent benchmarks ([R1](../research/evidence/R1-terminal-bench-science.md) §3–§4; [R4](../research/evidence/R4-replication-benchmarks.md) summary). Terminal-Bench-Science already requires "measured separation" from structurally independent comparators and verifies repair tasks on seeded hidden instances [P-full]; DeepEcon's comparators would be *realistic research mistakes* from the paper's own pipeline rather than author-invented ones.
2. **Realism by construction.** The mistakes come from people who know which errors matter, with a recorded realism warrant. That directly addresses Safeguard G (real errors versus artificial mutations).
3. **A construct that is not yet saturated.** Plain reproduction is close to solved for frontier agents (Claude Code reaches 93.4% on SocSci-Repro-Bench) [P-page]. DeepEcon targets the *decisions* that make results credible, which existing economics benchmarks do not grade as executable outcomes inside real replication packages ([R4](../research/evidence/R4-replication-benchmarks.md) §4–§5).
4. **Procedure tested partly through outcomes.** Agents deliver code; verifiers re-run it on answer-changing hidden variants built on data the agent never sees, and check exact relations. **Additive effect injection** checks how an estimator weights treated cells: for a pipeline linear in the outcome, adding a known effect moves the estimate by exactly that weighting. In a numerical check, an imputation estimator moved by the target ATT of 2.062 while two-way fixed effects moved by 1.421 ([R6](../research/evidence/R6-error-detection-and-verifier-methodology.md) Appendix A). Injection tests nothing about how the counterfactual is built, however: an independent econometric review found two clearly wrong estimators that also moved by exactly the target. **Counterfactual-side invariances** complement it (adding anything in the span of the required fixed effects must leave the estimate unchanged). Together they **partially** reconcile *Good Benchmarks*' "grade outcomes, not process" with the brief's "correct output is not correct procedure" ([verifier protocol](../methodology/verifier-validation-protocol.md) §5).
5. **Pre-registered consequences.** Contributors predict how a mistake will change the estimate, or only its standard error, before it is run. This tests understanding and prevents post-hoc rationalization.
6. **By-products with independent value.** A citable catalogue of credibility criteria, replacing journal-rank intuitions (brief §3.4); and flawed packages that double as planted-defect fixtures for validating AI reviewers.

### Where it may fail, and what would guard against each failure

| Failure mode | Why it matters | Guard |
|---|---|---|
| **"Same number, wrong procedure"**: the flawed procedure matches the correct one on the evaluation data | Six distinct cases ([verifier protocol](../methodology/verifier-validation-protocol.md) §2). Most can be caught with new inputs or more outputs. Identification-equivalence cannot be caught by any outcome check | Separating hidden variants on unseen bases; effect injection plus counterfactual-side invariances; a benchmark-wide output contract that always includes standard errors and diagnostics; structured expert judgment for identification-equivalent cases |
| **Verifier co-designed with one solution** | Correct alternatives rejected; the many-analysts literature shows real legitimate dispersion | Two outside economists who see only the agent-facing material write acceptance criteria and attempt the task blind; decision spaces with conditional references; tighten the estimand (*Good Benchmarks* §4, §7) |
| **Contamination**: published papers and public packages | Agents can recall the paper's specification, not only its numbers; one study reports perfect scores on non-anonymized materials [S] | Offline task environments; a recognition probe; restructured presentations shared by variant and clean twin; answer-changing variants on unseen bases; held-out tasks preferably from unpublished or post-cutoff papers; private held-out split (O-001) |
| **Hidden material leaks through model providers** | Flawed variants and answer keys are created in model sessions and exercised in trials | Exposure rule: commercial no-training terms for every session that sees hidden material; exposure log; split by paper (P-026) |
| **"One-sentence-fact" tasks** | Disclosing one fact (e.g., the right clustering level) may make a task trivial; *Good Benchmarks* §9 calls such tasks weak | A hint ladder and a knowledge probe separate capability from recall; such tasks are tagged and reported separately until O-004 is decided |
| **Contested "errors"** | Binary keys would encode a false ground truth | Blind status classification (established / conditional / contested), with conditions verified by diagnostics on the graded data; contested items leave scored tasks (X-003) |
| **AI-driven drift in contributions** | Experts agreeing with an AI interviewer can produce artificial tasks (*Good Benchmarks* §9) | Contributor-first elicitation, provenance, measured AI influence, human-authored instructions |
| **Errors in the "correct" package** | Published packages contain real errors (the I4R catalogue lists 122 across 12 papers [P-page]) | A clean-room re-implementation or blind solve as the independent check (a code port would inherit the errors); treat discoveries as findings; label clean controls "no known consequential error" |
| **Effort and yield** | Hard tasks can take more than 40 hours (*Good Benchmarks* §10); here, about 40 shepherd-team hours per contribution plus outside-economist time and about $500 of validation-trial compute per admitted task (central estimates [U]) | Quality over quantity; shepherd role; a methodology arm in the pilot measures yield and cost per validation rung |
| **Environment** (Stata, data licences) | Stata appears in 71.6% of packages [S]; about 72% of AEA intake cases involve restricted data [P-full] ([R8](../research/evidence/R8-replication-standards-and-econometric-pitfalls.md)) | R/Python ports checked for numerical equivalence; derived data inherit the licence, so restricted sources become **fully synthetic** data only; a licensed Stata track only with leakage controls |
| **Novelty window** | Others are moving toward error-based evaluation in economics ([R4](../research/evidence/R4-replication-benchmarks.md) §5) [S] | Prioritize the distinctive parts; consider partnering (e.g., I4R, O-015) |

### What still needs methodological validation

How many consequential, discriminating mistakes an interview yields per paper; how often flagship variants are data-equivalent and how many answer-changing hidden instances each task needs; whether fully synthetic data preserve a mistake's consequence; whether re-executing agent code works without becoming a format test; whether correction and detection tasks with clean controls measure judgment; whether economists agree enough to key identification and interpretation items; whether disguise defeats recognition of canonical papers; and how many hours and trials an admitted task costs. These are listed in the [research review](../research/research-and-methodology-review.md) §9 and targeted by the [pilot](../pilot/pilot-evaluation-plan.md)'s methodology arm.

## Question 2 — Expert interview design

> *How can an adaptive AI-guided interview extract economists' tacit knowledge about consequential research mistakes, while avoiding leading questions, fabricated errors, and superficial discussion?*

### The key risk, from evidence rather than intuition

The strongest danger is not that the AI asks bad questions. It is that experts **absorb the AI's views without noticing**. In a 2026 Anthropic study, 50 analysts with causal-inference experience worked with a Claude agent secretly given a random lean on four design choices. They followed the lean **86%** of the time; 77% repeated its arguments, and only 15% credited it. Self-rated ownership did not distinguish who had been swayed ([R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) §3.4) [P-page]. The study has limits: no human-only control, one task, one model. But it is the closest evidence to our situation. Asking for the expert's view first is necessary but not sufficient, and influence must be **measured by design**.

### Approach

The [protocol](../interview/expert-interview-protocol.md) (v0.2.1) adapts two established knowledge-elicitation methods to discovering consequential research mistakes:
- the **Critical Decision Method**: an incident, the contributor's own timeline, cues, options and their basis, and "what would a novice do?";
- **Applied Cognitive Task Analysis**: a record per decision of the difficult element, why it is difficult, common errors, and the cues and strategies used.

It moves from the paper's design (S1), to the decisions that made it credible (S2), to plausible wrong alternatives (S3), to their consequences and classification (S4), to code-level operationalization (S5) and task design (S6), and ends with the contributor's review and sign-off (S7). Sessions last 45–60 minutes. The research lead's example progression is built in as probes, not as a script.

### Safeguards

| Risk | Safeguards |
|---|---|
| **Experts absorbing the AI's views** | A **free-recall lock**: the contributor's unaided, timestamped list comes before any suggestion or code pointer. Exposure tracking on every statement; recall measured on pre-exposure items only. Influence reported as **measured** shares (LLM-originated, post-exposure, LLM-influenced), validated against blinded double human coding, plus a false-endorsement rate on known-valid controls, each endorsement adjudicated by an independent economist. The pilot randomizes suggestions over pre-registered decisions, after all free-recall locks (O-017). |
| **Leading questions** | Ask before pointing: the contributor locates decisions in the code before the AI shows them. No yes/no endorsements; two-sided suggestions with rotated order; at most three per decision, from a vetted pitfall taxonomy only. A rejected suggestion is never re-raised. |
| **Fabricated errors** | "No realistic mistake here" is stated to be a complete answer, and there are no quotas. A mandatory realism warrant records whether the mistake was observed (where) or is hypothetical. An **evidence bundle** is required: the mechanism, the warrant, a test that distinguishes correct from flawed, and a cited rule. The status of each mistake (established, conditional, or contested) is set by **blind classification** by economists outside the contribution, not in the conversation: one classifier for items matching a vetted-taxonomy entry, two for novel items. |
| **Superficial discussion** | Evidence-first: the AI reads the paper and code before asking, and never asks what they already say. Laddering continues until the mechanism is stated as an estimand, assumption, measurement, or inference property. The interviewer's own turns are short, so they cannot become the sophisticated-but-irrelevant discussion the brief warns about. |
| **Sycophancy, model toward expert** | No evaluative remarks. Disagreements cite file and line, and are never retracted without new evidence. Unresolved disagreements go to the shepherd. Checkers (citations, triviality, leakage) run in a fresh context without the conversation. |
| **Authority** | Statement-level provenance and contributor disposition. The contributor can edit, reject, or withdraw anything. Stage summaries use the contributor's own words, with a 1–4 accuracy rating. Agent-facing task text must be human-written or substantially human-edited. |

### How we will know it works

The protocol is first tested the way a checker is tested: against a baseline interviewer, with replicates, and with model-played personas (one that pushes back, one holding a wrong belief, one prone to deference). Transcripts are coded by two coders for leading questions and judgemental remarks. The pilot then measures real yield, recall of a sealed known-issues key (textbook and paper-specific items reported separately), blind quality ratings, and measured AI influence, with suggestions randomized. Quality and influence are compared on first-period sessions only, so that one arm's suggestions cannot prime the other. Perceived ownership is kept as an experience measure only, because it did not track influence in the deference study.

## Question 3 — Hosted contributor platform (Option A)

> *What would a rigorous but reasonably lightweight hosted platform require, and how should its parts interact?*

**Requirements.** A bilingual web application (sign-in with location attestation, consent, uploads, staged interview with progress display, live dossier panel with provenance, review and submission), an interview orchestrator that uses the pinned model through tools (read file, search code, update dossier, record suggestion) with separate suggestion and checker calls, a database, encrypted and versioned object storage, server-side validation and packaging, and monitoring with per-session cost caps. The shepherd console belongs to the shared core. Details: [Option A design](../architecture/option-a-hosted-platform.md).

**A hosted interview does not require hosted execution.** The proposed MVP (A1) runs the interview on project servers while code runs under the contributor's control, in their own Stata, R, or Python: generated run kits are executed by the contributor or a research assistant, and only outputs are uploaded. What A1 lacks, compared with Option B, is in-session iteration on a run. Execution can also happen on staff machines during shepherding, which suits *Good Benchmarks*' division of labour. A hosted R/Python sandbox (A2, managed or self-built) can be added for public-data papers; Stata in a hosted sandbox raises licensing questions [U: StataCorp terms not verified].

**Reference stack, verified** ([R9](../research/evidence/R9-hosted-stack-and-compliance.md)):
- a custom Next.js application on the Claude Messages API, with next-intl, Better Auth (magic links, ORCID through OpenID Connect), Neon Postgres, Cloudflare R2 (EU), and Langfuse (EU);
- hosting costs about **$13–210 a month** from pilot to 200 contributors;
- the API account's monthly spend caps ($500 Start, $1,000 Build) require the Build tier or above, and the Scale tier before recruitment waves [P-page].

**Custody.** The project and its processors hold uploads, drafts, and consented transcripts from the first session, including abandoned contributions. A variant that keeps materials in the browser until submission is worth assessing.

**Distinctive strengths.** The whole interviewer configuration is fixed; the recall lock, suggestion gate, and role separation are enforced server-side; and every consented session, including abandoned ones, is observable for research on the interview itself.

Existing open-source interview platforms use non-commercial licences, so we reuse their ideas, not their code. Running the same skill server-side through the Agent SDK is technically feasible. Anthropic's terms, however, say customers running Claude Code in their products "may not pay for … Claude usage on their end users' behalf", so that variant needs confirmation (O-018).

**Regional constraint.** The Usage Policy prohibits facilitating access for users in unsupported regions, "including end users". A Claude-based platform therefore cannot serve contributors located in mainland China, Hong Kong, or Macau (O-007). Its fallback would be a second model provider behind the same orchestrator, with a China-reachable host and PIPL duties.

Effort: about 12–19.5 engineer-weeks beyond the shared core (A1 plus staff execution). Inference ≈ $13 per contribution at list prices without in-session agentic work (≈ $17 with A2). About 15–35 minutes before the interview starts.

## Question 4 — Local Claude Code skill (Option B)

> *How would the same contribution experience be implemented through a locally executed skill? Requirements, benefits, limitations, and costs?*

**Implementation.** A Claude Code plugin delivered inside a downloadable workspace: the interview skill (orchestration rules plus stage cards and probe library), custom subagents for the suggestion generator and checkers, a schema-validating helper for state and provenance (shipped as binaries), run wrappers for Stata, R, and Python, layered protection of original files (read-only workspace, permission rules, a hook, an integrity checksum before export), a package doctor, and locale assets. The workspace pins, switch-blocks, and records the model, disables auto mode, and follows the client's stable channel. The vetted taxonomy and controls are best served from a project endpoint after each recall lock, because files in the plugin are readable. Details: [Option B design](../architecture/option-b-local-skill.md).

**Requirements for contributors.**
- **Claude Code:** in a terminal (macOS 13+, Windows 10 1809+, Linux) or in the desktop app's Code tab, the no-terminal path for the conversation. Cowork is unsuitable because it runs code on Anthropic's servers rather than with the contributor's Stata.
- **Commercial-terms access:** under the proposed exposure rule, hidden material may be handled only under no-training terms, so consumer plans are not enough for full contributions. Access comes from the project (if O-018 permits) or from the contributor's institution.
- **Location:** a supported region (mainland China, Hong Kong, and Macau are not supported).
- **Software:** the paper's own software; Python only where no helper binary exists.
- **Setup:** about 31–66 minutes before the interview, or a research assistant who installs and operates the tools (the economist still installs Claude Code for the interview).

Sources: [R2](../research/evidence/R2-claude-code-platform.md), [R3](../research/evidence/R3-access-pricing-policy-portability.md).

**Benefits.** Real local execution with in-session iteration, including Stata, which appears in 71.6% of economics replication packages [S]. Drafts never sit on project servers; the project receives the same package as under Option A at submission. Near-zero hosting.

**Limitations.**
- **Setup burden** for non-technical economists.
- **Consistency is recorded, not enforced.** The model is pinned and switches are blocked and recorded, but enforcement needs managed settings or a gateway. The client version, Claude Code's own system prompt, and contributors' user-level instructions, skills, plugins, and MCP servers vary; they are recorded per package.
- **Protocol safeguards are instruction-level.** The recall lock and suggestion gate rest on the helper and instructions rather than a server; the taxonomy and controls are readable unless served from an endpoint.
- **Weak guarantees on file access.** Plugins cannot ship permission rules (hence the workspace). Read-deny rules do not stop subprocesses from reading files.
- **Hidden-tier copies persist** on contributors' machines unless purged.
- **Limited research on the interview.** Only submitted packages carry metrics; abandoned contributions are invisible.
- **Fast-moving client.** It ships several releases a week; the workspace follows the stable channel and enables plugin auto-update (to be tested).
- **Regional limits** on who can use it; the portable skill can run in other agent tools as a fallback, without model parity.

**Costs.**
- **Contributors:** time, installation, and their own software.
- **Project:** development (≈ 11.5–20.5 engineer-weeks beyond the shared core, comparable to Option A once the upload endpoint, project page, subagents, and binaries are counted), maintenance (≈ 0.1–0.2 FTE), evaluation inference per certified client release, and higher per-contributor support. Inference ≈ $17 per contribution with project-provided access, or $0 where institutions provide access, subject to the terms question O-018.

## Question 5 — Architectural comparison

> *Which trade-offs should collaborators discuss, and what should a pilot measure?*

**Trade-offs to discuss** (detailed in the [decision brief](../architecture/architecture-decision-brief.md) §4):
1. consistency versus reach;
2. who runs the code;
3. custody versus dispersion of sensitive material;
4. building and operating versus supporting;
5. who pays for model access, and under which data-use terms;
6. how well each option supports research on the interview itself.

Inference cost is small either way and should not drive the decision, and engineering effort is comparable. Human effort (shepherds, reviewers, outside economists) and validation-trial compute dominate under both options. Whether the architecture changes shepherd hours is untested and could outweigh every other cost difference.

**What the pilot should measure** ([pilot plan](../pilot/pilot-evaluation-plan.md)):
- setup completion and time, with designed onboarding and unaided, by technical fluency;
- run-kit and research-assistant hand-off delays, in both arms;
- time to first substantive question, and drop-off points;
- candidate yield, and validated, operationalized flawed variants per contribution;
- recall of a sealed known-issues key, on pre-exposure items;
- blind quality ratings, with inter-rater agreement and a blinding check;
- AI-origin share of endorsed items, false endorsement of controls, and perceived ownership;
- usability;
- tokens and cost per session, support minutes, and shepherd hours by route;
- comfort with data flows;
- in a methodology arm: attrition, hours, and trials per validation rung.

Decision thresholds should be symmetric between the arms and registered **before** the first session.

## The most important open questions

The full list is in the [decision log](../decisions/decision-log.md) (O-001 to O-019). The six that most constrain what happens next:

1. **O-002 and O-019** — pilot both options, choose one now, or pilot one slice plus probes of the other;
2. **P-026 and O-018** — whether to adopt the exposure rule, and whether Anthropic's terms let the project provide access to external contributors (together they decide how Option B can run);
3. **O-001** — release policy (public, private, or split), which constrains submission and leakage controls;
4. **O-007** — legal review of participation by contributors in mainland China, Hong Kong, and Macau;
5. **O-009** — staffing of shepherds, reviewers, and outside economists, the dominant cost;
6. **O-014** — the project name, which collides with an existing "deepecon" econometrics package.

## Corrections after the independent reviews

- Effect injection was overclaimed as a test of procedure; it checks treated-cell weighting only (Q1, feature 4).
- Effect-injected and semi-synthetic data cannot substitute for restricted data; only fully synthetic data can (Q1, environment).
- A code port is not an independent check of the reference (Q1, errors in the "correct" package).
- Option B was credited with "no project custody" and lower engineering; custody differs only during drafting, and engineering is comparable (Q4).
- Option B's consistency and auto-mode limits were overstated in some respects (pinning, recording, and disabling auto mode are documented) and understated in others (user-level configuration; instruction-level safeguards) (Q4).
- Human effort was understated (Q1, effort and yield; Q5).
