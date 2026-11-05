# CLAUDE.md — Project memory for DeepEcon Research Benchmark (working title)

Read this file at the start of every session. It records how we work, so the research lead does not have to repeat it.

## What this project is

An expert-driven benchmark that tests whether AI agents can do rigorous economics research (empirical implementation, causal identification, econometric reasoning, scientific judgment). Economists contribute tasks through an AI-guided interview: from a published paper, they help build a validated **correct** replication package and **deliberately flawed** packages encoding plausible, consequential mistakes, which are then turned into verifiable agent tasks.

- **Canonical requirements:** [`docs/requirements/2026-11-05-research-lead-brief.md`](docs/requirements/2026-11-05-research-lead-brief.md) — verbatim; never edit it.
- **Decision status:** [`docs/decisions/decision-log.md`](docs/decisions/decision-log.md) — Decided / Proposed / Open / Rejected.
- **Current phase (2026-11-05):** Phases 1–4 (discovery, shared methodology, parallel architecture design, decision package). **No implementation yet. No architecture selected.**

## Roles and collaboration principles

- The user is the **research lead**; Claude is a **research-engineering collaborator**.
- Challenge assumptions that are not sufficiently justified. Give independent, evidence-based judgment; do not simply agree.
- Never silently redefine the project's scientific objectives. Raise disagreements explicitly instead.
- Investigate existing work before any novelty claim.
- Prioritize scientific validity over technical sophistication. Prefer modular, testable, simple solutions; avoid premature implementation.
- Documents meant for collaborators must be polished enough to share with academic economists.
- Keep documentation concise but sufficient to prevent repeated discussions.

## Non-negotiable conventions

1. **Status vocabulary.** Every recommendation is *Proposed* until the research lead approves it. Never convert a proposal into a decision without recording who approved it and when.
2. **Evidence labels.** Label factual claims: **[P-full]** primary source read in full; **[P-page]** primary abstract, landing page, README, or official doc page; **[S]** secondary source; **[U]** unverified. Never present [U] as fact. Never invent citations, numbers, prices, or URLs.
3. **Architecture neutrality.** Options A (hosted platform) and B (local Claude Code skill) are developed to the same depth, on the same assumptions. Neither is a strawman. A hybrid never substitutes for the A-versus-B comparison. Do not favour the option that is easier to implement.
4. **Provenance of content.** Contribution records always distinguish what the contributor said, what an LLM suggested, and what has been independently validated. Machine translations are labelled; originals are preserved.
5. **Leakage.** Reference solutions, flawed implementations, error labels, verifier internals, and hidden test data never go into agent-facing task materials or public channels by accident. Public task materials carry the project canary string (to be defined).
6. **Originals are sacred.** Tools never modify a contributor's original replication package; flawed variants live in separate, auditable locations.
7. **Dates and versions.** Use ISO dates (YYYY-MM-DD). Prices and product facts are dated and sourced because they change.

## Repository map

| Path | Contents |
|---|---|
| `docs/requirements/` | Product requirements (the research lead's brief) |
| `docs/research/` | Deliverable 1, reading notes, evidence notes, source register |
| `docs/methodology/` | Deliverable 2: construction protocol, task-quality rubric, verifier validation, error taxonomy |
| `docs/interview/` | Deliverable 3: expert interview protocol |
| `schemas/` | Deliverable 4: contribution data schema (JSON Schema) and examples |
| `docs/architecture/` | Deliverables 5–7: Option A, Option B, submission, bilingual design, costs, decision brief |
| `docs/pilot/` | Deliverable 8: pilot evaluation plan |
| `docs/decisions/` | Decision log and ADRs |
| `protocol/`, `validation/`, `implementations/`, `pilot/`, `tests/`, `contributor-docs/` | Placeholders until Phase 5 |
| `reports/` | Generated, collaborator-facing renderings |

## Environment notes (cloud sessions)

- `arxiv.org` is not reachable from the cloud environment's network policy; ask the research lead for PDFs, or have the environment's allowed domains updated. Do not route around blocked hosts with proxy or mirror services.
- `github.com` web pages and `api.github.com` are blocked, but `git clone` and `raw.githubusercontent.com` work. Clone references read-only into the scratchpad; never execute their scripts.

## Corrections and standing preferences from the research lead

Record every correction here with its date so it is never repeated.

- *(none yet)*
