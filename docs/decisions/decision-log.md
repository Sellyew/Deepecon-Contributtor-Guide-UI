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

## Open

Unresolved questions. *(Populated as the Phase 1–4 deliverables are completed.)*

| ID | Question | Why it matters | Blocking? |
|---|---|---|---|
| O-001 | Will the benchmark be fully public, fully private, or split (public development set plus private held-out test set)? | Determines leakage controls, the submission channel (e.g., whether any public repository can hold task materials), licensing, and how contamination is handled. | Blocks submission design and release policy |
