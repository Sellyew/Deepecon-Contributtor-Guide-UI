# CLAUDE.md — Project memory for DeepEcon Research Benchmark (working title)

Read this file at the start of every session. It records how we work, so the research lead does not have to repeat it.

## What this project is

An expert-driven benchmark that tests whether AI agents can do rigorous economics research (empirical implementation, causal identification, econometric reasoning, scientific judgment). Economists contribute tasks through an AI-guided interview: from a published paper, they help build a validated **correct** replication package and **deliberately flawed** packages encoding plausible, consequential mistakes, which are then turned into verifiable agent tasks.

- **Canonical requirements:** [`docs/requirements/2026-11-05-research-lead-brief.md`](docs/requirements/2026-11-05-research-lead-brief.md) and the **governing revision** [`docs/requirements/2026-11-06-research-lead-revision.md`](docs/requirements/2026-11-06-research-lead-revision.md) — both verbatim; never edit them. Where they differ, the 2026-11-06 revision governs. The team's own plan is summarized in [`docs/requirements/2026-11-05-team-handover-plan.md`](docs/requirements/2026-11-05-team-handover-plan.md).
- **Decision status:** [`docs/decisions/decision-log.md`](docs/decisions/decision-log.md) — Decided / Proposed / Open / Rejected.
- **Current phase (2026-11-07):** the research lead redirected the MVP to a **lightweight, self-hosted, privacy-preserving, bilingual contributor interface** with two functions, *Selection* (authors review, select, reject, or supplement candidate errors the team prepared locally) and *Guidance* (what materials to provide and how to submit them). See the [MVP proposal](docs/architecture/mvp-contributor-interface.md). No AI interview, no Claude Code, no external AI by default. The example contribution package V5 was reviewed at the structure level on 2026-11-06 ([review](docs/requirements/2026-11-06-example-package-v5-review.md)); the lead answered Q1–Q6 the same day (D-025 to D-029). The MVP proposal v0.3, draft [schemas](schemas/contributor-interface/README.md) 0.2.0, and the [implementation plan](docs/architecture/mvp-implementation-plan.md) v0.2 are Proposed; MVP v0.4 adds D-030 (bilingual interface; no translation of item text) and D-031 (answer keys only to local models), and the [LLM use policy](docs/architecture/llm-use-policy.md); proposals P-049 (now the general run kit for contributors' restricted data; O-034 closed as moot) and P-050 (O-035). P-051 to P-053 (task tiers against contamination, evaluation-time isolation, hosting) answered the lead's questions of the same day, with evidence note R10; the lead then adopted the tiers as **D-032** (which narrows D-031 to held-out tasks; D-018 unchanged) and said the pilot paper is a **demo** with no contact with its authors (D-024 clarified). MVP v0.5, the implementation plan v0.3 (staged hosting: the demo on a team member's computer, a server only before the first outside contributor, P-053), and the LLM use policy v0.2 are Proposed. The first real contributor is open (O-036). P-054 (Proposed, awaiting the lead; evidence note R11) answers the lead's question on LLM assistance in building tasks: LLM assistance would be allowed under expert review, with the model's location set by each task's tier (fixed before drafting) and provenance recorded per item. On 2026-11-07 the lead decided not to deploy local models (**D-033**), suggested that contributors may use AI tools if they rewrite AI-generated content in their own words (P-055, Proposed; MVP v0.6 §5.6), and asked to revise the construction process for AI use before revisiting D-032's clarification (O-037). No implementation yet.

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
3. **Privacy by default (D-018).** No research data, replication code, paper materials, contributor responses, or intermediate outputs go to Anthropic or any other third-party AI service. The system works with no model at all; a model is used only if the research lead deploys or configures it. Always distinguish a **locally deployed model** (data stay on project hardware; the project will not deploy one, D-033) from an **external API** (e.g., the DeepSeek API with the lead's key: data leave the project); external integrations are optional, explicitly configured, and disabled by default. No third-party analytics, fonts, CDNs, or embedded content in the contributor site. *(The former A/B neutrality rule was superseded on 2026-11-06: Option B is rejected and the MVP is decided, D-019, D-020.)*
4. **Provenance of content.** Contribution records always distinguish what the contributor said, what an LLM suggested, and what has been independently validated. Machine translations are labelled; originals are preserved.
5. **Leakage.** Reference solutions, flawed implementations, error labels, verifier internals, and hidden test data never go into agent-facing task materials or public channels by accident. Public task materials carry the project canary string (to be defined).
6. **Originals are sacred.** Tools never modify a contributor's original replication package; flawed variants live in separate, auditable locations.
7. **Dates and versions.** Use ISO dates (YYYY-MM-DD). Prices and product facts are dated and sourced because they change.
8. **Claude sessions are an external AI service too.** Anything shared in a Claude session (including this one) is processed by Anthropic. Before asking for or opening project materials (replication code, data, paper materials, contributor responses, candidate errors), say so and offer structure-only or synthetic alternatives; never fetch or open such materials on your own initiative. Expert-only and researchers-only materials (rubrics, answer keys, guides, pilot results) are inspected only at the structure level (file names, key names, counts), because Claude models may later be evaluated on these tasks; read their content only if the research lead explicitly asks, and say what was read. *(Practice adopted 2026-11-06 for the V5 package. V5 is now a development task (D-032), so the contamination reason no longer applies to it, but D-018 still does.)*
9. **Keep it lightweight.** Do not design AI-agent workflows, Claude Code-based systems, or elaborate interview processes (X-006, X-007). Prefer the team's handover plan and the example contribution package over new inventions.

## Repository map

| Path | Contents |
|---|---|
| `docs/requirements/` | Product requirements: the research lead's brief (2026-11-05), the governing revision (2026-11-06), and the team's handover plan |
| `docs/research/` | Deliverable 1, reading notes, evidence notes, source register |
| `docs/methodology/` | Deliverable 2: construction protocol, task-quality rubric, verifier validation, error taxonomy |
| `docs/interview/` | Deliverable 3: expert interview protocol |
| `schemas/` | Deliverable 4: contribution data schema (JSON Schema) and examples |
| `docs/architecture/` | **Current:** the [MVP contributor interface](docs/architecture/mvp-contributor-interface.md) and the bilingual design. *Superseded records:* Option A, Option B, the decision brief, the cost model, submission mechanisms |
| `docs/pilot/` | Deliverable 8: pilot evaluation plan |
| `docs/decisions/` | Decision log and ADRs |
| `protocol/`, `validation/`, `implementations/`, `pilot/`, `tests/`, `contributor-docs/` | Placeholders until Phase 5 |
| `reports/` | Generated, collaborator-facing renderings |

## Checks before committing

- `python3 tests/schema/test_contributor_interface.py` (current contributor-interface schemas, examples, and `validation/rubric_checks.py`), `python3 tests/schema/test_schema.py` (the superseded 0.3.0 schema), `python3 tests/docs/check_links.py` (relative links and heading anchors in all Markdown), `python3 tests/docs/check_report_version.py` (the HTML rendering in `reports/` matches the Markdown brief's version).
- When a document's numbers change (engineering weeks, hours, costs), update the [cost model](docs/architecture/cost-and-effort-model.md) and its scripts first, then the brief, the assessment, the decision log, and the HTML rendering.

## Before researching anything again

Read the dated evidence notes in [`docs/research/evidence/`](docs/research/evidence/) (R1–R9, 2026-11-05; R10 and R11, 2026-11-06) first; they record what was verified, at which evidence level, and what could not be accessed. Re-verify only what is stale or marked [S]/[U]. Prices, plan terms, and policies change: re-check them before any public use.

## Environment notes (cloud sessions)

- Blocked by the environment's network policy (as of 2026-11-05): `arxiv.org`, `github.com` web pages and `api.github.com`, `docs.github.com`, `aclanthology.org`, `agentskills.io`, `api.crossref.org`, `www.aeaweb.org`, and several vendor and university sites. Ask the research lead for PDFs or to allow hosts in the environment's network settings. Never route around blocked hosts with proxy or mirror services.
- Reachable: `code.claude.com`, `platform.claude.com`, `www.anthropic.com`, `claude.com` pricing pages, `raw.githubusercontent.com`, and `git clone` of public repositories. Clone references read-only into the scratchpad; never execute their scripts.
- **WebSearch has a per-turn budget shared by all subagents (about 200 searches).** Parallel research agents exhausted it on 2026-11-05; plan searches accordingly, and prefer primary sources reachable by fetch or clone.
- The machine has 4 CPUs, so the Workflow tool runs about two agents at a time; independent background agents can run more in parallel.

## Corrections and standing preferences from the research lead

Record every correction here with its date so it is never repeated.

- **2026-11-06 (privacy).** No project content or contributor data may be sent to Anthropic or any other external AI provider. The research lead controls model selection and deployment (DeepSeek with their own key, or a local model; *2026-11-07: no local model will be deployed, D-033*); external APIs are optional, explicitly configured, disabled by default, and always distinguished from local deployment. The system must not depend on Anthropic infrastructure or require Claude Code, Team, or Enterprise subscriptions.
- **2026-11-06 (scope).** The first frontend must be much simpler: authors are contacted directly and their own paper is preconfigured; no paper discovery or complex onboarding.
- **2026-11-06 (errors).** Candidate errors are prepared locally by the team. No AI interview to discover mistakes and no AI-generated flawed packages; contributors review, select, reject, or supplement the prepared candidates and may comment. *(Scope question raised the same day: the lead's words were "We do not need an AI agent to interview authors from scratch to discover mistakes or generate flawed replication packages" (revision ¶3), and the lead is "not convinced we need to prohibit LLM assistance during task construction". P-054 (a) proposes reading this entry as concerning the contributor-facing system, so that the team may use LLMs in its own preparation of candidates, outside the site, under expert review. Not yet confirmed: until the lead decides, this entry stands as written.)*
- **2026-11-06 (focus).** The frontend does two things: Selection and Guidance (what materials to provide, how to prepare them, how to submit).
- **2026-11-06 (process).** Use the coauthor's example contribution package as the primary reference for the workflow, data structure, and submission requirements; do not assume its contents; do not finalize the schema or the implementation plan before reviewing it.
- **2026-11-06 (effort).** Do not continue designing expensive AI-agent workflows, Claude Code-based contributor systems, or elaborate expert-interview processes.
- **2026-11-06 (categories).** The V5 rubric is just an example: item categories and points differ by field (e.g., theoretical derivation errors). Never hard-code V5's conceptual / missing / technical groups; configure categories per paper.
- **2026-11-06 (file names).** Contributors provide their original file names; the team does the mapping.
- **2026-11-06 (runnable).** The team needs a full runnable replication package; code and documentation without data are not enough.
- **2026-11-06 (agent package).** Contributors may see the agent-facing candidate package.
- **2026-11-06 (languages, clarified).** The requirement is a bilingual **interface** (Chinese and English; more languages later), translated with an LLM and reviewed by the team. Do not translate papers, code, or item text. *(An earlier entry misread this as translating item text.)*
- **2026-11-06 (answer keys).** Answer-key material is never sent to any API provider; only a locally deployed model may process it (D-031). Local clients of hosted models (e.g., Claude Code, Cursor) count as API providers. *(Narrowed the same day by D-032; see the next entry. Since D-033 there is no local model, so held-out material goes to no model.)*
- **2026-11-06 (task tiers).** The lead agreed to development, evaluation, and held-out task tiers (D-032). D-031's local-only rule now covers held-out tasks; other answer-key material follows D-018, which is **not** relaxed: no project content goes to an external AI service unless the lead explicitly configures one. The lead said they do not necessarily mind some benchmark materials being used for training; what matters is a valid evaluation. Published development tasks are public material, and the canary lets the team detect training use. A clarification of D-032's held-out and exposure wording is deferred until the construction process is revised (O-037).
- **2026-11-06 (pilot paper).** The pilot paper (Muñoz & Otero 2025) is only a demo; the team has no contact with its authors. Do not plan author runs or author contact for it. Real contributors are usually authors of their own papers (D-022); the lead may have a first contact (O-036; the name is not recorded in the repository).
- **2026-11-06 (contributors' location).** Most contributors are outside mainland China.
- **2026-11-06 (hosting).** The lead asked whether a PC could host the demo, with servers and storage considered later; P-053 (Proposed) answers yes, with staged hosting; O-021 stays open.
- **2026-11-07 (local models).** The project will not deploy its own local models (D-033). Do not propose local deployment; any LLM use goes through an external service the lead configures, or through contributors' own tools (P-055).
- **2026-11-07 (contributors and AI).** The lead suggested letting authors work with AI, provided they rewrite AI-generated content in their own words, with a clear explanation of why: the tasks must reflect the authors' own scientific judgment and avoid obvious AI-generated patterns (P-055, Proposed).
- **2026-11-07 (sequence).** Revise the construction process for AI use first, then revisit D-032's clarification (O-037).
- **2026-11-07 (reporting delegated work).** When reporting work done by subagents, call them AI agents (Claude instances run from this session), never "researchers" or "reviewers". Say what they read and did, and that a second agent of the same model family is not an independent human check.
