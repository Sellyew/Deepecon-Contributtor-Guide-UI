# Decision Log

This register is the single place where the project's decision status is recorded. Every item has exactly one status:

| Status | Meaning | Who can set it |
|---|---|---|
| **Decided** | A requirement the research lead has stated or approved. | Research lead only |
| **Proposed** | A recommendation awaiting review. Not binding. | Anyone; usually the research-engineering collaborator |
| **Open** | An unresolved question. | Anyone |
| **Rejected** | An alternative considered and not pursued, with the reason. | Research lead (or by explicit agreement) |

**Rules.** Proposals are never silently converted into decisions; a status change requires an explicit note of who approved it and when. Larger decisions with live alternatives get an Architecture/Methodology Decision Record in [`adr/`](adr/) using [`adr/0000-template.md`](adr/0000-template.md). IDs are never reused.

*Last updated: 2026-11-05 (initial version).*

---

## Decided

All items below are stated requirements from the research lead's brief of 2026-11-05 ([verbatim brief](../requirements/2026-11-05-research-lead-brief.md)); section numbers refer to that brief.

| ID | Decision | Source |
|---|---|---|
| D-001 | The benchmark evaluates whether AI agents can perform rigorous economics research — empirical implementation, causal identification, econometric reasoning, and scientific judgment — and is built from economists' expertise. | Intro, §2 |
| D-002 | Two contribution pathways: **Path A** (contributor reproduces a paper from a curated Top-5 collection) and **Path B** (original author contributes their own paper). Both produce standardized contribution packages. | §3.1 |
| D-003 | Each contribution centres on a scientifically validated **correct** replication package and one or more expert-identified, deliberately **flawed** packages. These are *source materials* for task construction, not necessarily the tasks themselves. | §3.2–3.3, §3.5 |
| D-004 | Errors must be plausible and scientifically consequential from an economist's perspective; ideally documented with the ten elements listed in §3.3. | §3.3 |
| D-005 | Two architectures — **Option A** (hosted platform) and **Option B** (local Claude Code skill) — are developed to comparable depth on equivalent assumptions. **Neither is selected.** The choice (one, hybrid, or prototyping both) is made with collaborators after Phase 4. | Intro, §6, §12 |
| D-006 | The scientific workflow, contribution schema, quality standards, and expected outputs stay as consistent as possible across both architectures. | §6 |
| D-007 | English and Simplified Chinese are supported from the beginning in both architectures; the task schema is language-independent; contributors' original statements are preserved and machine translations are labelled; the design is extensible to more languages. | §9 |
| D-008 | Human authority: the LLM is an interviewer and research assistant, not the scientific authority. Contributors can edit, reject, refine, or withdraw suggestions. The system records whether each statement came from the contributor, from the LLM, or has been independently validated. | §5.5 |
| D-009 | Four information tiers are kept separate: contributor-facing; internal construction and validation; agent-facing instructions; hidden evaluation materials. The evaluated agent must not receive the correct answer or known-error labels. | §5.4, §10F |
| D-010 | Contributor submissions are **candidate** tasks until they pass independent checks for inclusion in an official release. | §10D |
| D-011 | Original replication materials are preserved; deliberate errors live in separate files or directories; changes are auditable; the researcher's work is never silently overwritten. | §6 Option B |
| D-012 | *Good Benchmarks* (Bercovich 2026) guides task quality, translated into an operational rubric for economics tasks rather than used as a generic checklist. | §4 |
| D-013 | Computational correctness, statistical validity, and identification validity are distinguished; genuinely contested or underidentified questions do not receive artificial binary answers. | §4 |
| D-014 | The project proceeds in phases (Discovery → Shared Methodology → Parallel Architecture Design → Collaborator Decision Package → Prototype and Pilot → Validation and Iteration). No extensive implementation before the architecture decision is reviewed. | §12, §15 |
| D-015 | Submission mechanisms are evaluated independently of the two interface architectures. The initial submission system is simple; the contribution package is standardized. | §8 |
| D-016 | A pilot uses one published paper and the same scientific content to compare the two contribution workflows on actual contributor experience. | §11 (Deliverable 8) |
| D-017 | Documentation uses the Decided / Proposed / Open / Rejected vocabulary, and proposals are never silently converted into decisions. | §13 |

## Rejected

Alternatives the research lead explicitly ruled out in the brief.

| ID | Rejected alternative | Reason given | Source |
|---|---|---|---|
| X-001 | Asking an AI system to predict journal rankings as a proxy for methodological quality. | Journal placement is not an objective ground-truth label; intuitions about "top-journal quality" must be translated into explicit, scientifically defensible criteria. | §3.4 |
| X-002 | Tasks built from arbitrary coding bugs, formatting problems, artificial puzzles, or ambiguity — tasks that are hard only because instructions are poor or information is hidden. | Such tasks do not measure economic reasoning; difficulty must be realistic and intrinsic. | §3.3, §10A |
| X-003 | Imposing binary answers on genuinely contested or underidentified methodological questions. | They would encode a false ground truth. | §4 |
| X-004 | Using a hybrid proposal as a substitute for evaluating Options A and B separately. | The primary output must preserve a clear A-versus-B comparison. | §7 |
| X-005 | Treating artificial code mutations as high-quality benchmark tasks by default. | Mutations help test verifiers but do not automatically represent plausible research mistakes. | §10G |

## Proposed

Recommendations from the research-engineering collaborator, awaiting the research lead's review. *(Populated as the Phase 1–4 deliverables are completed.)*

| ID | Proposal | Rationale (short) | Where argued |
|---|---|---|---|
| P-001 | Adopt the repository structure described in the root [`README.md`](../../README.md). | Separates research, requirements, decisions, protocol, schemas, validation, both implementations (placeholders only), pilot, tests, reports, and contributor docs, as the brief requests. | §13 of the brief; root README |
| P-002 | Label every factual claim in project documents with an evidence level: **[P-full]** primary source read in full; **[P-page]** primary abstract/landing page/official doc; **[S]** secondary; **[U]** unverified. | Implements "distinguish established facts from proposals"; makes stale or unverified claims visible. | [`CLAUDE.md`](../../CLAUDE.md) |
| P-003 | Classify every critical decision and failure mode by **validity layer**: computational, statistical, identification, or interpretation (the lead's three layers plus interpretation). | Makes the brief's distinction operational; interpretation covers failure modes #3 and #5. | [Construction protocol](../methodology/benchmark-construction-protocol.md) |
| P-004 | Assign every task a **verifiability tier**: V1 deterministic computational; V2 statistical with known truth; V3 structured judgment with an expert-consensus key; V4 open-ended judgment. Scored releases use V1–V2, and V3 only after an agreement study. | Implements Safeguard C and *Good Benchmarks* #1/#6. | [Verifier validation](../methodology/verifier-validation-protocol.md) |
| P-005 | **First-release scope:** score error correction and research execution; score structured error detection only alongside clean controls; keep identification reasoning and interpretation in an unscored experimental track pending a V3 agreement study. | Outcome-verifiable today; trade-off stated in O-003. | Construction protocol §6 |
| P-006 | Introduce a **shepherd** role: a benchmark-team member owns task and verifier engineering for each contribution, from candidate to admission. | *Good Benchmarks* §9: domain expertise and task-building are different skills; shepherding works. | Construction protocol §2 |
| P-007 | Verify procedures through outcomes: agents deliver code under a minimal I/O contract, and verifiers **re-execute it on hidden data variants** and check econometric **metamorphic relations**. | Reconciles "outcome-verified" (*Good Benchmarks*) with "correct procedure" (Safeguard B); defeats memorized coefficients. | Verifier validation §3, §5 |
| P-008 | Adopt the **validation ladder** (L0–L13) and the **acceptance-region** method for numeric tasks, including the equivalent-mutant check. | A flawed implementation alone does not validate a task (brief §4). | Verifier validation |
| P-009 | Adopt the **task-quality rubric** v0.1 (34 criteria in 10 groups, 18 gates, three assessment stages), adapting Terminal-Bench-Science's Apache-2.0 rubrics where they fit. | Operational translation of *Good Benchmarks*. | [Rubric](../methodology/task-quality-rubric.md) |
| P-010 | Interview rules: **evidence first, contributor first**; LLM suggestions only after the contributor's own ideas are exhausted, neutrally framed, recorded with dispositions; **pre-registered consequence predictions**; LLM-origin share monitored. | Guards against leading questions, anchoring, and AI-driven task drift (*Good Benchmarks* §9). | [Interview protocol](../interview/expert-interview-protocol.md) |
| P-011 | Interview stages S0–S7 (adds setup and consent; merges consequence analysis with classification), with an adaptive question-selection policy and explicit stopping rules. | Refines the brief's seven-stage sketch. | Interview protocol §5–§11 |
| P-012 | Final **agent-facing instructions are human-written or substantially human-edited**; authorship recorded; unedited LLM drafts are not admissible. | *Good Benchmarks* §9. | Rubric SP-2 |
| P-013 | Contribution schema v0.1.0 (JSON Schema 2020-12) with statement-level provenance, labelled translations, and `const`-enforced visibility tiers. | Deliverable 4; tested. | [Schema](../../schemas/README.md) |
| P-014 | Submission: standardize the package; default transport is a private browser upload (file-request service for the pilot); internal review in a private Git repository with automated checks; GitHub as optional transport for technical contributors only; e-mail as fallback. | Keeps the contributor path simple while hidden material stays private. | [Submission mechanisms](../architecture/submission-mechanisms.md) |
| P-015 | Raw restricted or confidential microdata are never sent to any model provider or included in packages, in either architecture. | Safeguard E; data-use agreements. | Interview protocol S0; schema `submission` |
| P-016 | Task environments use open-source software (R or Python) by default; any Stata-only task forms a separately reported licensed track. | *Good Benchmarks* #7 (robust, pinned environments). | Construction protocol Stage 0 |
| P-017 | Build an **architecture-independent core** (protocol assets, schema, validator, packager, internal review pipeline) whichever option is chosen. | Avoids duplicated work; makes prototyping both options cheaper. | Interview protocol §14 |
| P-018 | Pilot design: within-subject crossover on two target analyses of one paper, project-supplied model access in both arms, sealed known-issues key, blind review, pre-registered decision thresholds. | Compares real contributor experience on the same scientific content. | [Pilot plan](../pilot/pilot-evaluation-plan.md) |
| P-019 | Bilingual principles: one protocol with localized surfaces; codes in data; originals preserved; reviewed EN–ZH glossary; English agent-facing tasks in the first release. | Brief §9. | [Bilingual design](../architecture/bilingual-design.md) |

## Open

Unresolved questions. *(Populated as the Phase 1–4 deliverables are completed.)*

| ID | Question | Why it matters | Blocking? |
|---|---|---|---|
| O-001 | Will the benchmark be fully public, fully private, or split (public development set plus private held-out test set)? | Determines leakage controls, the submission channel (e.g., whether any public repository can hold task materials), licensing, and how contamination is handled. | Blocks submission design and release policy |
| O-002 | Which architecture: Option A, Option B, a hybrid, or prototype both for the pilot? | The central decision; to be taken with collaborators after Phase 4. | Blocks Phase 5 |
| O-003 | Accept the first-release scope in P-005, given that failure modes #3 (irrelevant methodological discussion) and #5 (misleading causal interpretation) would be under-measured until V3 keys are validated? | Trade-off between verifiability and coverage of the brief's motivating failures. | Blocks release planning, not design |
| O-004 | How to treat "one-sentence-fact" tasks — tasks that become trivial once a single fact (e.g., the correct clustering level) is stated, where recognizing that fact may itself be the capability under test? | *Good Benchmarks* §9 calls such tasks weak; several of the brief's motivating failures have this shape. | No |
| O-005 | Contributor incentives and credit: co-authorship on a benchmark paper, named contributor credit, honoraria, or a combination? | Drives recruitment and engagement of senior economists; affects the cost model. | Blocks recruitment |
| O-006 | Who pays for contributors' model usage under Option B: contributors, project reimbursement, project-provided seats, or project-issued API access? | Cost distribution, model consistency, and data-use terms all depend on it. | Blocks Option B design finalization |
| O-007 | Access for contributors in mainland China under each option (product availability, terms for serving users in unsupported regions, network reachability, cross-border data rules). | Bilingual requirement implies Chinese-speaking contributors; requires legal review. | Blocks recruitment in China |
| O-008 | Pilot paper selection, and whether a collaborator can contribute their own paper (Path B). | Required for Deliverable 8. | Blocks pilot |
| O-009 | Staffing: who serves as shepherds and independent reviewers, and how many hours are available? | Shepherd time is likely the dominant cost. | Blocks scaling plans |
| O-010 | Licence for the repository, protocol, schema, and released tasks. | Affects reuse by other benchmarks and harness builders. | No |
| O-011 | Relationship to Terminal-Bench-Science and the Harbor task format: adopt the format, contribute economics tasks there, or stay independent? | Reuse of tooling and community versus control over release policy. | No |
| O-012 | Language of agent-facing tasks (English only in the first release, as proposed in P-019?). | Construct validity versus bilingual reach. | No |
| O-013 | Ethics review for the pilot (and for retaining interview transcripts for research on the protocol). | Human-subjects rules at the lead's institution. | Blocks pilot |
| O-014 | **Project name.** "DeepEcon" collides with an existing MIT-licensed Python econometrics package `deepecon` (bilingual README; same maintainer as a widely used Stata MCP tool) and a deepecon.org site ([R4](../research/evidence/R4-replication-benchmarks.md) §2.8) [P-page/S]. Keep, or choose a distinctive name before any public launch? | Confusion in exactly the Chinese-speaking empirical-economics community the project targets; trademark risk. | Blocks public launch |
| O-015 | Partner with the Institute for Replication (I4R), whose catalogue of naturally occurring errors in published packages (122 entries over 12 papers in the PNAS 2026 "AI games" study) could supply realistic errors alongside expert-designed ones? | Real errors satisfy Safeguard G directly; licensing and authors' consent unresolved. | No |
| O-016 | Funding for model use and validation trials: project budget, sponsor API credits (as Terminal-Bench-Science uses), or programmes funding agentic benchmarks? | Affects cost distribution under both options. | No |
