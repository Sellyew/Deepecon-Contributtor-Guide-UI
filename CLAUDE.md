# CLAUDE.md — Project memory for DeepEcon Research Benchmark (working title)

Read this file at the start of every session. It records how we work, so the research lead does not have to repeat it.

## What this project is

An expert-driven benchmark that tests whether AI agents can do rigorous economics research (empirical implementation, causal identification, econometric reasoning, scientific judgment). Economists contribute by reviewing, selecting, rejecting, or supplementing candidate items the team prepares from a published paper (D-020, D-021); together they build a validated **correct** replication package and **deliberately flawed** packages encoding plausible, consequential mistakes, which are then turned into verifiable agent tasks.

- **Canonical requirements:** [`docs/requirements/2026-11-05-research-lead-brief.md`](docs/requirements/2026-11-05-research-lead-brief.md) and the **governing revision** [`docs/requirements/2026-11-06-research-lead-revision.md`](docs/requirements/2026-11-06-research-lead-revision.md) — both verbatim; never edit them. They record what the lead asked at the time; the decision log records what is in force now, and where they differ the decision log governs. Decisions are revised when the project's aims change: replace outdated rules and record what changed and why, rather than adding exceptions (research lead, 2026-11-07). The team's own plan is summarized in [`docs/requirements/2026-11-05-team-handover-plan.md`](docs/requirements/2026-11-05-team-handover-plan.md).
- **Decision status:** [`docs/decisions/decision-log.md`](docs/decisions/decision-log.md) — Decided / Proposed / Open / Rejected.
- **Current phase (2026-11-08):** the MVP is a **lightweight, self-hosted, bilingual contributor interface** with two functions, *Selection* (authors review, select, reject, or supplement candidate items the team prepared) and *Guidance* (what materials to provide and how to submit them). See the [MVP proposal](docs/architecture/mvp-contributor-interface.md) v0.8 (Proposed), the [implementation plan](docs/architecture/mvp-implementation-plan.md) v0.4 (v0.3 approved 2026-11-07, D-043; v0.4 applies D-044), and the draft [schemas](schemas/contributor-interface/README.md) 0.3.0. On 2026-11-07 the research lead reset the policy framework: AI use and benchmark integrity follow one short rule set, the [AI use and integrity rules](docs/architecture/llm-use-policy.md): decisions D-038 to D-042 (D-039 to D-042 drafted by Claude and approved by the research lead on 2026-11-07). They replace the earlier privacy, answer-key, tier, and local-model rules. The example package V5 is a demo task, reviewed at the structure level; the demo paper (D-024) has no author contact; the first real contributor is open (O-036). Milestone M1 (skeleton) of the [contributor site](implementations/contributor-interface/README.md) was built on 2026-11-07 and runs with the fictional examples only; contributors choose one paper at a time from the papers the team offers, through one personal link (D-044, D-045, details P-060). On 2026-11-07 the lead set the long-term direction "open to contribute, open to develop, controlled to evaluate" (D-046); the architecture for it is Proposed ([P-062](docs/architecture/open-development-controlled-evaluation.md)), partly settled on 2026-11-08 (D-047): in the first version only demo papers are public, scored papers are offered by invitation, and the evaluation manifest's hash will be published. M2 (Selection) is next.

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
3. **AI use and privacy (D-038 to D-042).** Follow the [AI use and integrity rules](docs/architecture/llm-use-policy.md). Restricted or confidential data never go into any AI service. The contributor site sends nothing to AI services and loads no third-party analytics, fonts, CDNs, or embedded content. Contributors' material goes to an AI service only with their consent. AI may help build tasks, but experts decide and people write the final text. Every AI provider that receives a task's answer-key material or package is recorded in its exposure log. The project deploys no models; all models are used through APIs (D-038).
4. **Provenance of content.** Contribution records always distinguish what the contributor said, what an LLM suggested, and what has been independently validated. Machine translations are labelled; originals are preserved.
5. **Leakage.** Reference solutions, flawed implementations, error labels, verifier internals, and hidden test data never go into agent-facing task materials or public channels by accident. Public task materials carry the project canary string (to be defined).
6. **Originals are sacred.** Tools never modify a contributor's original replication package; flawed variants live in separate, auditable locations.
7. **Dates and versions.** Use ISO dates (YYYY-MM-DD). Prices and product facts are dated and sourced because they change.
8. **Claude sessions are an AI service too.** Anything shared in a Claude session (including this one) reaches Anthropic and belongs in the exposure log (D-040). Before opening project materials (replication code, data, contributor responses, candidate items, answer keys), say so; open answer-key content only when the research lead asks, and say what was read. Contributors' material is shared only with their consent (D-042).
9. **Keep it lightweight.** Do not design AI-agent workflows, Claude Code-based systems, or elaborate interview processes (X-006, X-007). Prefer the team's handover plan and the example contribution package over new inventions.

## Repository map

| Path | Contents |
|---|---|
| `docs/requirements/` | Product requirements: the research lead's brief (2026-11-05), the governing revision (2026-11-06), and the team's handover plan |
| `docs/research/` | Deliverable 1, reading notes, evidence notes, source register |
| `docs/methodology/` | Deliverable 2: construction protocol, task-quality rubric, verifier validation, error taxonomy |
| `docs/interview/` | Deliverable 3: expert interview protocol |
| `schemas/` | Deliverable 4: contribution data schema (JSON Schema) and examples |
| `docs/architecture/` | **Current:** the [MVP contributor interface](docs/architecture/mvp-contributor-interface.md), the [AI use and integrity rules](docs/architecture/llm-use-policy.md), and the bilingual design. *Superseded records:* Option A, Option B, the decision brief, the cost model, submission mechanisms |
| `docs/pilot/` | Deliverable 8: pilot evaluation plan |
| `docs/decisions/` | Decision log and ADRs |
| `implementations/contributor-interface/` | The contributor site (Django), built milestone by milestone from the approved plan (D-043) |
| `validation/`, `tests/` | Rubric checks used by the site and the schema tests; Markdown checks |
| `protocol/`, `pilot/`, `contributor-docs/` | Placeholders |
| `reports/` | Generated, collaborator-facing renderings |

## Checks before committing

- `python3 tests/schema/test_contributor_interface.py` (current contributor-interface schemas, examples, and `validation/rubric_checks.py`), `python3 tests/schema/test_schema.py` (the superseded 0.3.0 schema), `python3 tests/docs/check_links.py` (relative links and heading anchors in all Markdown), `python3 tests/docs/check_report_version.py` (the HTML rendering in `reports/` matches the Markdown brief's version).
- `cd implementations/contributor-interface && .venv/bin/python manage.py test` (the contributor site; needs `pip install -r requirements.txt` in a virtual environment). When interface strings change, run `makemessages -l zh_Hans` and `compilemessages`, and fill in the Chinese draft for the team's review.
- When the implementation plan's estimates change, update the plan, MVP §9, and D-043 together; the cost model, decision brief, and assessment are superseded records.

## Before researching anything again

Read the dated evidence notes in [`docs/research/evidence/`](docs/research/evidence/) (R1–R9, 2026-11-05; R10 and R11, 2026-11-06; R12 and R13, 2026-11-07) first; they record what was verified, at which evidence level, and what could not be accessed. Re-verify only what is stale or marked [S]/[U]. Prices, plan terms, and policies change: re-check them before any public use.

## Environment notes (cloud sessions)

- Blocked by the environment's network policy (as of 2026-11-05): `arxiv.org`, `github.com` web pages and `api.github.com`, `docs.github.com`, `aclanthology.org`, `agentskills.io`, `api.crossref.org`, `www.aeaweb.org`, and several vendor and university sites. Ask the research lead for PDFs or to allow hosts in the environment's network settings. Never route around blocked hosts with proxy or mirror services.
- Reachable: `code.claude.com`, `platform.claude.com`, `www.anthropic.com`, `claude.com` pricing pages, `raw.githubusercontent.com`, and `git clone` of public repositories. Clone references read-only into the scratchpad; never execute their scripts.
- **WebSearch has a per-turn budget shared by all subagents (about 200 searches).** Parallel research agents exhausted it on 2026-11-05; plan searches accordingly, and prefer primary sources reachable by fetch or clone.
- The machine has 4 CPUs, so the Workflow tool runs about two agents at a time; independent background agents can run more in parallel.

## Corrections and standing preferences from the research lead

Record every correction here with its date so it is never repeated.

- **2026-11-06 (scope).** The first frontend must be much simpler: authors are contacted directly; no paper search or complex onboarding. *(Its "own paper is preconfigured" part was changed on 2026-11-07; see the paper pool entry.)*
- **2026-11-06 (focus).** The frontend does two things: Selection and Guidance (what materials to provide, how to prepare them, how to submit).
- **2026-11-06 (process).** Use the coauthor's example contribution package as the primary reference for the workflow, data structure, and submission requirements; do not assume its contents; do not finalize the schema or the implementation plan before reviewing it.
- **2026-11-06 (effort).** Do not continue designing expensive AI-agent workflows, Claude Code-based contributor systems, or elaborate expert-interview processes.
- **2026-11-06 (categories).** The V5 rubric is just an example: item categories and points differ by field (e.g., theoretical derivation errors). Never hard-code V5's conceptual / missing / technical groups; configure categories per paper.
- **2026-11-06 (file names).** Contributors provide their original file names; the team does the mapping.
- **2026-11-06 (runnable).** The team needs a full runnable replication package; code and documentation without data are not enough.
- **2026-11-06 (agent package).** Contributors may see the agent-facing candidate package.
- **2026-11-06 (languages, clarified).** The requirement is a bilingual **interface** (Chinese and English; more languages later), translated with an LLM and reviewed by the team. Do not translate papers, code, or item text. *(An earlier entry misread this as translating item text.)*
- **2026-11-06 (pilot paper).** The pilot paper (Muñoz & Otero 2025) is only a demo; the team has no contact with its authors. Do not plan author runs or author contact for it. Real contributors are usually authors of their own papers (D-022); the lead may have a first contact (O-036; the name is not recorded in the repository).
- **2026-11-06 (contributors' location).** Most contributors are outside mainland China.
- **2026-11-06 (hosting).** The lead asked whether a PC could host the demo, with servers and storage considered later; staged hosting was approved with the plan (D-043); O-021 stays open for the Stage 1 server.
- **2026-11-07 (framework reset).** The lead asked to replace outdated rules with a simpler, consistent set rather than add exceptions, and not to treat earlier decisions as permanent constraints. The rules in force are D-038 to D-042; the lead approved D-039 to D-042, drafted as P-056 to P-059, on 2026-11-07 ([AI use and integrity rules](docs/architecture/llm-use-policy.md)). AI may help the team and contributors build tasks, but experts decide. People write or rewrite what they submit and what the agent sees, and provenance is recorded per item. Answers of scored tasks stay unpublished, and evaluation is isolated. Exposure is logged, and affected scores are reported separately. Restricted data never go into AI; the site sends nothing; contributors' material is used only with consent. Earlier entries on privacy (2026-11-06), errors, answer keys, task tiers, local models, contributors and AI, and sequencing are superseded; see the decision log's table for 2026-11-07. Standing preference (2026-11-06, kept): the lead does not necessarily mind some benchmark materials being used for training; what matters is a valid evaluation.
- **2026-11-07 (held-out tier).** The lead deferred a held-out tier (tasks built with no AI use) to the next version, to be discussed with a coauthor (O-038). Do not reintroduce it before then.
- **2026-11-07 (models).** The project deploys no models and rents no computing; all models, including open-weight ones such as DeepSeek and Qwen, are used and evaluated through providers' APIs (D-038).
- **2026-11-07 (reliable safeguards).** The lead does not want to "rely on restrictions that sound reassuring but don't meaningfully solve the problem" (asked about training-off settings, feedback buttons, and private chats; answered in the AI use and integrity rules §3).
- **2026-11-07 (paper pool and links).** Each contributor chooses a paper from a pool the team offers; the personal link stays on that paper until the contributor changes it; one paper and one link at a time, so contributors are not confused. Sessions outlast a link's expiry and are stopped only by revoking the link, or after a year without use, which the lead approved: "The true contribution is the pack. I trust every contributor can finish within 1 year." The team never moves a contributor's chosen paper unless the contributor asks, through a danger zone with GitHub-style double confirmation (D-045). The task build date is added in M2 (D-044).
- **2026-11-07 (direction).** DeepEcon is "an open, community-driven resource" and "a credible benchmark": open contribution, open development (some validated tasks published with solutions and tools), controlled evaluation (scored tasks with unpublished answer keys). "Open" does not mean everything is public. Discovering a paper is separate from accessing its task materials. No return to three tiers and no AI-use rules that differ by task category; one contribution and review workflow for both sets (D-046). Do not over-engineer: the MVP is the contributor site, not a leaderboard platform.
- **2026-11-08 (first version).** Only demo papers are public in the first version; every invited contributor's paper stays private. Authors may choose public release only in a future version. Access to scored papers is by invitation first; a request-and-authorize step comes in a future version. Publish the evaluation manifest's hash before the first official run (D-047).
- **2026-11-08 (evaluation setup).** Use the same API + harness setup for all models, open-weight or closed, through each developer's official API; direct API-only evaluations may come later. Exposure to providers is tracked (Rule 10), not a reason to change the evaluation architecture (D-048). Do not propose routing models differently to avoid exposure.
- **2026-11-07 (reporting delegated work).** When reporting work done by subagents, call them AI agents (Claude instances run from this session), never "researchers" or "reviewers". Say what they read and did, and that a second agent of the same model family is not an independent human check.
