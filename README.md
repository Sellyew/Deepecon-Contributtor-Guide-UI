# DeepEcon Research Benchmark *(working title)*

An expert-driven benchmark for evaluating whether AI agents can perform rigorous economics research — empirical implementation, causal identification, econometric reasoning, and scientific judgment — built from the experience of economists who publish in leading journals.

> **Project status (2026-11-05): design phase, decision package ready for review.** Phases 1–4 of the [plan](docs/requirements/2026-11-05-research-lead-brief.md#12-proposed-development-process) have produced complete drafts of Deliverables 1–8, revised after four independent reviews (econometrics, benchmark methodology, and one advocate for each architecture). **No contribution architecture has been selected** and nothing has been implemented. All recommendations are *Proposed* until the research lead approves them in the [decision log](docs/decisions/decision-log.md).

## The idea in one paragraph

From a published paper, an economist helps build a validated **correct** replication of a specific result and one or more **deliberately flawed** versions, each encoding a plausible, scientifically consequential mistake: the wrong estimator, inference procedure, sample, or treatment timing, or an unsupported interpretation. An AI-guided interview helps the economist make that tacit knowledge explicit. A benchmark team then turns these source materials into short, verifiable tasks whose hidden verifiers accept correct work and reject the expert-identified mistakes. Contributions reach the project through one of two candidate architectures under comparison: a **hosted bilingual web platform** (Option A) or a **Claude Code skill run locally** (Option B).

## Start here

| If you want… | Read |
|---|---|
| The decision we need to make, in a few pages | [Architecture decision brief](docs/architecture/architecture-decision-brief.md) (Deliverable 7); a designed rendering is in [`reports/`](reports/README.md) |
| Answers to the five assessment questions | [Initial assessment](docs/assessment/initial-assessment.md) |
| What has been decided, proposed, left open, and rejected | [Decision log](docs/decisions/decision-log.md) |
| The original requirements | [Research lead's brief](docs/requirements/2026-11-05-research-lead-brief.md) |

## Deliverables

| # | Deliverable | Document | Status |
|---|---|---|---|
| 1 | Research and methodology review | [docs/research/research-and-methodology-review.md](docs/research/research-and-methodology-review.md) | Proposed draft |
| 2 | Benchmark construction protocol | [docs/methodology/benchmark-construction-protocol.md](docs/methodology/benchmark-construction-protocol.md), with the [task-quality rubric](docs/methodology/task-quality-rubric.md) and [verifier validation protocol](docs/methodology/verifier-validation-protocol.md) | Proposed draft |
| 3 | Expert interview protocol | [docs/interview/expert-interview-protocol.md](docs/interview/expert-interview-protocol.md) | Proposed draft |
| 4 | Contribution data schema | [schemas/](schemas/README.md) (JSON Schema, example, tests) | Proposed draft |
| 5 | Option A — hosted platform | [docs/architecture/option-a-hosted-platform.md](docs/architecture/option-a-hosted-platform.md) | Proposed draft |
| 6 | Option B — local Claude Code skill | [docs/architecture/option-b-local-skill.md](docs/architecture/option-b-local-skill.md) | Proposed draft |
| 7 | Architecture decision brief | [docs/architecture/architecture-decision-brief.md](docs/architecture/architecture-decision-brief.md) | Proposed draft |
| 8 | Pilot evaluation plan | [docs/pilot/pilot-evaluation-plan.md](docs/pilot/pilot-evaluation-plan.md) | Proposed draft |

Supporting analyses: [submission mechanisms](docs/architecture/submission-mechanisms.md) · [bilingual design](docs/architecture/bilingual-design.md) · [cost and effort model](docs/architecture/cost-and-effort-model.md) · [reading notes](docs/research/reading-notes/) · [evidence notes](docs/research/evidence/).

## Repository layout

```
docs/
  requirements/     research lead's brief (verbatim; never edited)
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
  hosted-platform/      Option A (not started; pending decision)
  claude-code-skill/    Option B (not started; pending decision)
pilot/              pilot materials (placeholder)
tests/              automated tests: schema tests, Markdown link check, report version check
reports/            generated, collaborator-facing renderings
contributor-docs/   English and Chinese contributor guides (placeholder)
CLAUDE.md           project memory and working conventions
```

## Conventions

- **Decision status:** every item is *Decided*, *Proposed*, *Open*, or *Rejected* ([decision log](docs/decisions/decision-log.md)). Proposals never become decisions silently.
- **Evidence labels:** **[P-full]** primary source read in full · **[P-page]** primary abstract, landing page, or official documentation · **[S]** secondary · **[U]** unverified.
- **Architecture neutrality:** Options A and B are developed to the same depth on the same assumptions.

## Running the checks

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
