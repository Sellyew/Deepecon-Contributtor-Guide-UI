# DeepEcon Research Benchmark *(working title)*

An expert-driven benchmark for evaluating whether AI agents can perform rigorous economics research — empirical implementation, causal identification, econometric reasoning, and scientific judgment — built from the experience of economists who publish in leading journals.

> **Project status (2026-11-07).** The MVP is a **lightweight, self-hosted, bilingual contributor interface**: invited authors review the candidate items the team prepared (*Selection*) and follow instructions for submitting a runnable replication package (*Guidance*). There is no AI interview and no Claude Code-based system. The site sends nothing to AI services; AI use in building tasks follows the [AI use and integrity rules](docs/architecture/llm-use-policy.md). Nothing has been implemented. Recommendations stay *Proposed* until the research lead approves them in the [decision log](docs/decisions/decision-log.md).

## The idea in one paragraph

From a published paper, the team prepares a validated **correct** replication and candidate **deliberate errors**: plausible, scientifically consequential modifications (an analysis step done wrongly, or a necessary step removed). The paper's authors or invited experts review these candidates in a simple bilingual website, choosing, rejecting, refining, or adding to them, and provide the replication materials needed. The team then implements the confirmed modifications, verifies them in three rounds, and turns them into short, verifiable tasks whose hidden verifiers accept correct work and reject the mistakes.

## Start here

| If you want… | Read |
|---|---|
| The current proposal | [MVP contributor interface](docs/architecture/mvp-contributor-interface.md) |
| What is in force now | The [decision log](docs/decisions/decision-log.md), which governs where it differs from the [research lead's revision of 2026-11-06](docs/requirements/2026-11-06-research-lead-revision.md) and the [team's handover plan](docs/requirements/2026-11-05-team-handover-plan.md) |
| What has been decided, proposed, left open, rejected, or superseded | [Decision log](docs/decisions/decision-log.md) |
| The original requirements | [Research lead's brief, 2026-11-05](docs/requirements/2026-11-05-research-lead-brief.md) |

## Documents

| Document | Status |
|---|---|
| [MVP contributor interface](docs/architecture/mvp-contributor-interface.md) (v0.7) and its [implementation plan](docs/architecture/mvp-implementation-plan.md) (v0.3) | **Current**, Proposed drafts |
| [AI use and integrity rules](docs/architecture/llm-use-policy.md) | **Current**, Decided 2026-11-07 (D-038 to D-042): AI use in building tasks, privacy, unpublished answers, isolation, exposure logging |
| [Example package V5: structural review](docs/requirements/2026-11-06-example-package-v5-review.md) | Reference (structure only; no rubric content) |
| [Bilingual design](docs/architecture/bilingual-design.md) | Current (principles and glossary) |
| [Verifier validation protocol](docs/methodology/verifier-validation-protocol.md), [task-quality rubric](docs/methodology/task-quality-rubric.md), [construction protocol](docs/methodology/benchmark-construction-protocol.md) | The team's internal methodology for turning confirmed candidates into tasks; interview-related passages superseded |
| [Research and methodology review](docs/research/research-and-methodology-review.md); [evidence notes](docs/research/evidence/); [reading notes](docs/research/reading-notes/) | Reference |
| [Contributor-interface schemas](schemas/contributor-interface/README.md) | **Current**, Proposed draft 0.2.0 with fictional empirical and theory examples and tests; the [earlier schema](schemas/README.md) is superseded |
| [Decision brief](docs/architecture/architecture-decision-brief.md), [Option A](docs/architecture/option-a-hosted-platform.md), [Option B](docs/architecture/option-b-local-skill.md), [interview protocol](docs/interview/expert-interview-protocol.md), [pilot plan](docs/pilot/pilot-evaluation-plan.md), [cost model](docs/architecture/cost-and-effort-model.md), [submission mechanisms](docs/architecture/submission-mechanisms.md), [initial assessment](docs/assessment/initial-assessment.md) | Superseded on 2026-11-06; kept as records |

## Repository layout

```
docs/
  requirements/     research lead's brief and 2026-11-06 revision (verbatim; never edited); team handover plan
  research/         Deliverable 1, reading notes, evidence notes
  methodology/      Deliverable 2: construction protocol, task-quality rubric, verifier validation
  interview/        Deliverable 3: expert interview protocol
  architecture/     Deliverables 5–7, submission, bilingual design, cost model
  pilot/            Deliverable 8
  assessment/       initial assessment (assessment questions 1–5)
  decisions/        decision log and decision records (ADRs)
schemas/            Deliverable 4: JSON Schema, illustrative example
protocol/           shared interview assets for either architecture (Phase 5; placeholder)
validation/         architecture-independent validation tools (Phase 5; placeholder)
implementations/
  contributor-interface/  the self-hosted MVP (not started; waiting for the example package)
  claude-code-skill/      Option B (rejected 2026-11-06; record only)
pilot/              pilot materials (placeholder)
tests/              automated tests: schema tests, Markdown link check, report version check
reports/            generated, collaborator-facing renderings
contributor-docs/   English and Chinese contributor guides (placeholder)
CLAUDE.md           project memory and working conventions
```

## Conventions

- **Decision status:** every item is *Decided*, *Proposed*, *Open*, or *Rejected* ([decision log](docs/decisions/decision-log.md)). Proposals never become decisions silently.
- **Evidence labels:** **[P-full]** primary source read in full · **[P-page]** primary abstract, landing page, or official documentation · **[S]** secondary · **[U]** unverified.

## Running the checks

```bash
python3 tests/schema/test_contributor_interface.py
```

```bash
python3 tests/schema/test_schema.py
```

```bash
python3 tests/docs/check_links.py
```

```bash
python3 tests/docs/check_report_version.py
```

The schema tests require Python 3.10+, `jsonschema` 4.18 or later, and `PyYAML`; the document checks use the standard library only.

## Licence

To be decided (Open question in the decision log). The illustrative example in `schemas/examples/` is fictional.
