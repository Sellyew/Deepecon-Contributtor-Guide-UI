# Deliverable 5 — Option A: Hosted Contributor Platform

> **Superseded on 2026-11-06.** The research lead revised the MVP ([revised requirements](../requirements/2026-11-06-research-lead-revision.md)): no AI interview, no Claude Code-based system, and no project data sent to any external AI service by default. The current proposal is the [MVP contributor interface](mvp-contributor-interface.md). This document is kept as a record and is no longer the basis for the design.

| | |
|---|---|
| **Status** | **Proposed design** v0.2.1 (2026-11-05). One of two candidate architectures; **not selected**. Comparable in depth and assumptions to [Option B](option-b-local-skill.md). v0.2.0 replaced v0.1.0's unverified claims with verified facts; v0.2.1 integrates the independent fairness reviews (§19). |
| **Shared foundations** | [Construction protocol](../methodology/benchmark-construction-protocol.md) · [Interview protocol](../interview/expert-interview-protocol.md) · [Schema](../../schemas/README.md) · [Submission](submission-mechanisms.md) · [Bilingual design](bilingual-design.md) · [Cost and effort model](cost-and-effort-model.md) |
| **Evidence** | Hosted stack, costs, compliance: [R9](../research/evidence/R9-hosted-stack-and-compliance.md). Terms and regions: [R3](../research/evidence/R3-access-pricing-policy-portability.md). Agent SDK and cloud providers: [R2](../research/evidence/R2-claude-code-platform.md). AI-interview precedents: [R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md). Software and data facts: [R8](../research/evidence/R8-replication-standards-and-econometric-pitfalls.md). Labels: [P-full], [P-page], [S], [U]. |

---

## 1. Summary

The project operates a **bilingual web application**. A contributor signs in, uploads the paper and the replication code, and conducts the interview in the browser. The model runs on the project's Claude API account, with a pinned model and fixed settings. The application keeps the dossier in a database with full provenance and produces the same standardized package as Option B.

The decisive design question is **who runs code**. A hosted interview does **not** require hosted execution. Stata appears in 71.6% of economics replication packages [S], and a hosted Stata deployment raises licensing problems. Three execution routes are therefore specified:

- **A1 — run kits under the contributor's control.** The platform generates a patch and run script. The contributor or a research assistant runs it locally, in their own Stata, R or Python, and uploads the *outputs*, never the data.
- **Staff execution.** Shepherds run reference and variants on project machines during task construction. These are machines the project licenses for Stata where it holds suitable licences.
- **A2 — hosted R/Python sandbox.** For public, redistributable data only.

**Proposed MVP:** A1 together with staff execution. Add A2 if the pilot shows that hand-offs stall operationalization (pilot §7, rule 3, which can also point to staff execution or to Option B).

| Property | Option A |
|---|---|
| Where the interview runs | Project servers, calling the Claude API under the project's commercial account |
| Where code runs | A1: contributor's or RA's machine (including Stata). Staff: project machines. A2: project sandbox (R/Python). |
| Who pays for inference | The project |
| Who holds materials during drafting | The project and its processors, from the first upload (§10) |
| What the project operates | Web application, database, file storage, model orchestration, (A2) sandbox, internal review pipeline, support |
| Model consistency | Enforced: the whole interviewer configuration (prompt, tools, model, effort level) is fixed server-side for everyone |

## 2. Contributor experience

### 2.1 Journey (the brief's 10 steps, refined)

| # | Step | What the contributor sees and does | Typical time [U: measure in the pilot] |
|---|---|---|---|
| 1 | Open the site | Landing page (English / 中文) | — |
| 2 | Read the introduction | Motivation, what a contribution involves, credit policy, data-flow summary, eligibility by location (§10.3) | 5–10 min |
| 3 | Choose a language | Switcher on every page; the choice is remembered | — |
| 4 | Sign in and consent | E-mail magic link, or ORCID sign-in (ORCID supports OpenID Connect; review the terms of its public API [S]); consent and data-flow disclosure (S0); **location attestation**, with a sign-in country check logged per session (§10.3) | 3–5 min |
| 5 | Choose a paper | Curated collection (Path A) or own paper (Path B) | 2–5 min |
| 6 | Provide materials | Upload the paper PDF and the replication code (ZIP); declare data availability; restricted data are never uploaded. Variant (a) in §3.3 keeps the code in the browser instead | 5–15 min |
| 7 | Interview | Protocol stages S1–S4 and S6 in a chat pane, in sessions of at most 45–60 minutes. A progress bar and a live dossier panel show provenance and exposure badges; a code viewer highlights cited files and lines **after** the contributor has located them (ask before pointing) | 1.5–3 h over 3+ sessions |
| 8 | Operationalize | A1: download a run kit, run it or have an RA run it, upload outputs. Staff: the shepherd runs it later. A2: the sandbox runs it. | A1: 0.5–2 h, possibly days of waiting; A2: minutes |
| 9 | Review | Dossier review screen in the contributor's language; edit, reject, or withdraw anything | 15–30 min |
| 10 | Submit | One button; confirmation e-mail; shepherd feedback later in the platform | 1 min |

**Before the interview starts** (steps 2 and 4–6): about **15–35 minutes**, with nothing to install [U: from this table; to be measured]. Option B's corresponding steps take about 31–66 minutes, plus obtaining commercial-terms access from the project (if O-018 permits) or the contributor's institution (Option B §2.1, §10.2). Run kits (step 8) still need a working Stata, R or Python installation on someone's machine.

### 2.2 Research-assistant mode

The economist invites an RA to the contribution from inside the platform. The RA sees the run kits and the hand-off specification, executes them, and uploads outputs. The economist approves the results in the review screen and installs nothing. Provenance attributes each action. The hand-off can still wait on the RA's schedule.

## 3. Architecture

### 3.1 Diagram

```mermaid
flowchart LR
  B[Contributor's browser] <--> W[Web application: pages, chat, dossier and code views, i18n]
  W <--> API[Application API: auth, sessions, dossier, uploads]
  API <--> DB[(Postgres: accounts, sessions, dossier, provenance, exposure, ledger)]
  API <--> OS[(Encrypted, versioned object storage: uploads, run outputs, packages)]
  API <--> ORC[Interview orchestrator: protocol assets + tools; separate suggestion and checker calls]
  ORC <--> LLM[(Claude API, project account, pinned model)]
  ORC --> IDX[Ingestion workers: PDF text, code index]
  ORC -. A2 only .-> SB[Sandbox: R/Python]
  B -. A1 run kit .-> LOC[Contributor or RA machine: Stata/R/Python]
  LOC -. outputs only .-> API
  API --> IR[(Internal review store: private Git + object storage)]
  IR --> SH[Shepherds: staff execution, task construction]
```

### 3.2 Reference stack (proposed) and alternatives

Based on [R9](../research/evidence/R9-hosted-stack-and-compliance.md) §2.2 and §11. A custom application fits the staged, stateful interview better than generic chat frameworks:
- Chainlit has been community-maintained since 2025-05;
- Open WebUI's licence restricts removing its branding above 50 users;
- the Vercel AI SDK routes through Vercel's gateway by default unless the Anthropic provider package is used directly [P-page].

| Layer | Reference choice | Notes |
|---|---|---|
| Web and API | Next.js with server routes | — |
| Internationalization | `next-intl` (current 4.x) | Lingui if translators work in standard translation-management tools [P-page] |
| Authentication | Better Auth (successor to Auth.js): e-mail magic links; ORCID via OpenID Connect | ORCID public-API terms need review [S] |
| Database | Neon Postgres ($0.106 per compute-unit hour plus $0.35 per GB-month) [P-page] | Alternative: Supabase Pro ($25/month) [P-page] |
| File storage | Cloudflare R2 in the EU jurisdiction ($0.015 per GB-month, no egress fees) [P-page] | Encrypted; versioned; presigned uploads |
| Model access | Anthropic SDK called directly (Messages API with tools, streaming, prompt caching) | The standard developer model: the project pays for its own application's usage |
| LLM tracing | Langfuse (EU; Core $29/month) [P-page] | Traces contain transcripts: same data handling as the database |
| Errors | Sentry | Plan pricing unverified [U] |
| Hosting | Fly.io in the EU (from $2.19/month; a 2 GB performance machine is $33/month) [P-page] | — |

Every service in this table that stores or traces content is a **processor** of unpublished code and transcripts (§10.1).

**Alternatives.**

1. **Supabase-integrated.** Authentication, database, and storage from one vendor: fewer moving parts, more lock-in.
2. **Managed-Agents-centric.** Anthropic runs the agent loop and a per-session container. It is billed at model tokens plus $0.08 per session-hour while running, with hard per-session dollar budgets. It is in beta on the Claude API, on Claude Platform on AWS, and on Anthropic-managed Google Cloud. The sandbox has Python but no R pre-installed (apt and pip installs are allowed). Transcripts are kept until deleted, and the service is not covered by zero data retention [P-page].
3. **Claude Agent SDK running the same skill as Option B on the server (hybrid H2).** Technically feasible: the SDK loads the same plugin, skills, and hooks, with one subprocess per session and API-key authentication [P-full/P-page, R2]. However, Anthropic's terms for "running Claude Code in your products or services (e.g. in hosted sandboxes or other agent infrastructure)" state: "Customers may not pay for, resell, or intermediate Claude usage on their end users' behalf. Each end user must authenticate with their own … credential" [P-full, R3]. That conflicts with "the project pays". **Ask Anthropic or counsel before adopting this variant** (O-018).

### 3.3 Variants that address Option A's weaknesses

These are labelled design options, not part of the MVP. Each needs a feasibility check.

| Variant | What changes | Addresses | Status |
|---|---|---|---|
| **(a) Browser-held materials** | The browser holds the package folder (File System Access API or an in-memory copy) and sends excerpts to the orchestrator only when the model asks for them; nothing is persisted on the server until submission | The brief's request (§6) for designs where "the conversation is hosted but sensitive code or datasets remain under the contributor's control"; project custody during drafting. Gives A Option B's "files the model never reads stay local" property | [U: engineering assessment; browser support varies] |
| **(b) EU-region model route** | Call Claude through Amazon Bedrock or Google Cloud's Agent Platform with EU region selection and customer-managed keys, instead of the Anthropic API | US storage of API data at rest (§10.1). On both clouds the `opus` alias resolves to Opus 5.5, and regions follow each cloud's regions [P-page, R2] | [U: Opus 5.5 availability and price in EU regions not verified]. The Supported Regions Policy still applies |
| **(c) In-browser execution** | WebAssembly builds of R or Python run public-data packages in the browser | Shortens the A1 round trip for public-data R/Python packages | [U: package coverage and performance not verified]; no Stata |

## 4. Functional decomposition (identical to Option B's table)

| Function | How Option A provides it | Runs where | Who pays |
|---|---|---|---|
| F1 Onboarding and consent | Web pages + S0 screen; location attestation | Project | Project |
| F2 Identity | Accounts (magic link, optional ORCID); sign-in country check | Project | Project |
| F3 Materials ingestion | Upload; PDF text extraction; code indexing | Project | Project |
| F4 Interview engine | Orchestrator + pinned model | Project → Claude API | Project |
| F5 State and provenance store | Database (with exposure and ledger tables) | Project | Project |
| F6 Code execution | A1 run kits; staff execution; A2 sandbox | A1 local; staff and A2 on project infrastructure | A1 contributor; staff and A2 project |
| F7 Validation | Server-side validator (schema, leakage, comparisons) | Project | Project |
| F8 Packaging | Server-side packager | Project | Project |
| F9 Submission | In-app submit → internal review store | Project | Project |
| F10 Review and feedback | Shepherd console (shared core); comments; follow-up sessions | Project | Project |
| F11 Internationalization | i18n framework + locale assets | Project | Project |
| F12 Telemetry and cost control | Per-session token and dollar caps, rate limits, cost dashboards; consented session logs, including abandoned sessions | Project | Project |
| F13 Support and updates | Central deployment; documentation; support inbox | Project | Project |

## 5. How the expert interview operates

### 5.1 Protocol hosting

The orchestrator assembles the interviewer's instructions from the shared protocol assets for the chosen locale. The model reaches the materials through tools rather than holding everything in context: file listing, file reading with line numbers, code search, and PDF page retrieval. In stages S1–S4 the contributor and the model discuss the same code, with line references, as in Option B.

The interviewer updates the dossier only through schema-validated tool calls (`update_dossier`, `record_recall_list`, `record_prediction`, `record_suggestion`), which enforce provenance and exposure tracking. The suggestion generator and the checkers (citations, triviality, leakage) are **separate model calls with restricted inputs** (interview protocol §10). The free-recall lock and the suggestion gate are enforced by the server: the vetted taxonomy and its known-valid controls never reach the contributor's browser, so the contributor cannot read ahead.

### 5.2 Model selection, consistency, and cost control

- **One pinned model** (e.g., Claude Opus 5.5 at a fixed effort level) and one protocol version per release. Every contributor gets the same interviewer: same system prompt, tools, model, and effort level. This makes contributions comparable and protocol evaluations meaningful.
- **Prompt caching** for the stable prefix. A one-hour cache lifetime suits human response gaps; writes cost 2× base input, and reads cost 0.05× on Opus 5.5.
- **Budgets:** per-session token and dollar caps, with graceful checkpointing.
- **Account tier.** API usage tiers carry monthly spend caps: $500 at Start, $1,000 at Build, $200,000 at Scale [P-page, R9]. Thirty contributions in one month cost about $390 at the A1 central estimate ($511 with A2), and 50 at the high estimate about $1,770 ($2,310 with A2) ([cost model](cost-and-effort-model.md)). The caps are **ample only at the Build tier or above**, and the account should move to the Scale tier before recruitment waves. Evaluation trials run in a separate workspace, with spend alerts on both.
- **Refusal handling:** server-side fallback configuration, per the provider's guidance. A flagged turn may then be answered by a fallback model unless refusals are left to stand; the same applies to Option B. The safety classifiers "most often flag cybersecurity and biology content", which is rare in economics [P-page: Claude Code model-configuration documentation, read 2026-11-05].

### 5.3 State, provenance, and resumption

The dossier, free-recall lists, suggestion ledger, and checkpoints live in the database. Sessions resume from the last contributor-confirmed summary. Transcripts are kept only with consent and for a defined retention period.

### 5.4 Research on the interview itself

Because every consented session is logged centrally, including sessions that are abandoned, Option A can measure drop-off (pilot M2) and AI influence (M6) over all contributors, not only those who submit. Protocol variants and the randomized suggestion phase (interview protocol §15; pilot §4) can be assigned on the server without the contributor seeing the assignment. Every AI-interview platform reviewed in [R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) §3.1 is hosted (Geiecke & Jaravel on Streamlit, Wuttke et al. on Chainlit, Anthropic Interviewer on Claude.ai).

### 5.5 Bilingual behaviour

Per the [bilingual design](bilingual-design.md):
- framework message catalogs for the interface;
- locale assets for probes and templates;
- glossary-anchored model output;
- originals preserved, with English working translations labelled.

A full Chinese webfont (Noto Sans SC) is 17.8 MB [P-page], so the platform uses system fonts or self-hosted subsets.

## 6. Replication materials

### 6.1 Ingestion and protection of originals

The application never modifies an original. Objects are **versioned**, checksums are kept in the database, and variants are stored as patches against the originals. Originals are deleted on withdrawal or on an erasure request, with an audit entry. Write-once bucket locks are not used, because they would conflict with contributors' right to withdraw (D-008) and with GDPR erasure ([R9](../research/evidence/R9-hosted-stack-and-compliance.md) §5).

On the contributor's or RA's machine, a run kit copies the original package into a separate working directory, applies the patch only there, and verifies a checksum manifest of the original before uploading outputs; a mismatch blocks the upload.

### 6.2 Execution routes

| | A1 — run kits under the contributor's control | Staff execution | A2 — hosted sandbox |
|---|---|---|---|
| What runs where | Patch, run script (Stata/R/Python), and output template on the contributor's or RA's machine | Shepherd machines, during task construction | Isolated R/Python containers |
| Data movement | None: only outputs (results JSON, logs) are uploaded | Public data only, unless a data-use agreement covers staff | Public, redistributable data only |
| Stata | Works under the contributor's licence. The difference from Option B is that the model does not iterate on the run within the session | Needs project licences valid for that use [U: StataCorp terms not verified] | Needs licences valid for server or container use [U]; AEA's Stata images require a licence mounted at run time [P-page, R8] |
| Environments | Heterogeneous contributor machines, as in Option B; outputs are re-run centrally | Project machines | Project images |
| Feedback to the contributor | Within the session or days later | Days later; predictions are pre-registered either way | Minutes |
| Engineering | Run-kit generator, output parser, cross-platform test matrix and guides | None beyond the internal pipeline | **Managed:** integrate a hosted sandbox (e.g., Managed Agents' container has Python but no R by default; Anthropic's code-execution tool is Python 3.11 only, with no internet, at $0.05 per container-hour after 1,550 free hours a month [P-page]). **Self-built:** containers, quotas, and security hardening |
| Risk | Hand-off friction may stall S5 | Shepherd time; slower loop | Security of executing uploaded code; licensing |

Variant (c) in §3.3 would add in-browser execution for public-data R/Python packages.

### 6.3 Restricted data

About 72% of AEA intake cases involve some access restriction [P-full, R8]. The S0 disclosure forbids uploading restricted or confidential microdata (P-015). Upload screens require a data-availability declaration and reject data-file types unless the data are declared public. With A1 and staff execution, no data upload is needed at all. Agent-facing material from restricted sources can only be fully synthetic ([verifier protocol](../methodology/verifier-validation-protocol.md) §6).

## 7. How correct and flawed packages are produced

| Artifact | Produced by | How |
|---|---|---|
| Reference implementation | Contributor or RA (A1), staff, or sandbox (A2) | Run the original; outputs uploaded or recorded |
| Independent check | Internal pipeline | A clean-room re-implementation or a correct blind solve ([verifier protocol](../methodology/verifier-validation-protocol.md) L3); the open-source port used in task environments is a separate artifact |
| Flawed variants | The model drafts the minimal diff; the contributor approves it in a diff viewer | Stored as a patch; executed through a run kit, staff, or the sandbox |
| Consequence evidence | Server-side comparison | The benchmark-wide materiality rule ([rubric](../methodology/task-quality-rubric.md) RV-2); hidden-variant checks where data permit |

## 8. Validation

Server-side checks: schema validation, leakage scan, integrity checks, and comparison against the pre-registered predictions. Results are shown to the contributor immediately and repeated in the internal pipeline, where everything is re-run.

## 9. Submission

In-app submission writes the package directly into the internal review store; no separate submission database is needed. Contributors can download their package at any time.

## 10. Privacy, confidentiality, licensing, and regional terms

### 10.1 Data flows

| Data | Leaves the contributor's machine? | To whom | Under which terms |
|---|---|---|---|
| Paper, code, declarations, interview text, drafts | Yes, from the first upload (variant (a) defers code until submission) | Project servers (EU hosting proposed) **and the project's processors**: hosting, database, object storage, LLM tracing, error tracking (§3.2) | Project privacy notice, processor agreements, and retention policy |
| Content needed for each turn | Yes | Anthropic, under the project's commercial account | Anthropic "may not train models on Customer Content". A data processing addendum with EU standard contractual clauses (plus UK and Swiss addenda) is part of the terms. API data at rest is stored in the US; inference is global by default, or US-only at 1.1× price [P-page, R3/R9]. Default retention is stated inconsistently: 30 days in the Claude Code documentation versus "not retained by default" (except certain models) in the API documentation, unresolved [P-page, R3 §6.2]. Zero data retention is available on the API to qualified organizations through sales; it is not available on consumer plans [P-page, R3 §6.2] |
| Data (A1, staff) | No | — | — |
| Run kits (A1): flawed-variant patches and run scripts, and the outputs they produce | Arrive from the project on the contributor's or RA's machine, where copies persist; only outputs are uploaded | — | Each download recorded in the exposure log, as for Option B's hand-off bundles; deletion after upload and after acceptance under the contributor agreement |
| Data (A2), public only | Yes | Project sandbox | Project terms |

**Exposure rule.** The [verifier protocol](../methodology/verifier-validation-protocol.md) §10 requires that any session that sees hidden-tier material (flawed variants, answer keys) runs under commercial no-training terms. Option A meets this by construction.

### 10.2 Obligations that come with custody

- **Unpublished code, drafts, and transcripts.** The project holds them from the first session, including contributions that are later abandoned. This requires security controls, minimal retention, processor agreements, and deletion on withdrawal. Under Option B the project receives the same code, dossier, and consented transcript at submission; the difference is custody of drafts and abandoned contributions.
- **Run-kit copies (A1).** Run kits carry hidden-tier material (flawed-variant patches) to contributors' and RAs' machines, where copies persist with their outputs. Each download is recorded in the exposure log; the kit asks for deletion after upload, and the contributor agreement asks for deletion after acceptance, as for Option B's local copies (Option B §10.1).
- **EU contributors (GDPR).** Personal data goes to the US under the standard contractual clauses; variant (b) could keep model traffic in the EU [U].
- **Contributors in mainland China (PIPL).** China's Personal Information Protection Law (Articles 3(2), 39, and 53) would apply. The 2024 exemption for transfers involving fewer than 100,000 people still leaves consent duties [S, unofficial copies]. Hosting inside mainland China would require an ICP filing [S].

### 10.3 Regional availability

The Usage Policy in force (2025-09-15) prohibits facilitating "account or API access to Claude to persons, entities, or users in violation of our Supported Regions Policy". The version effective 2026-11-12 adds "(including end users)". The Commercial Terms bind "Customer and its Users" to that policy, and allow suspension if "Customer or any User" breaches it. The Supported Regions Policy does not list mainland China, Hong Kong, or Macau [P-full/P-page, R3/R9].

A Claude-based hosted platform therefore **cannot serve contributors located in those regions**. Introduction-page text is not enough: sign-up requires a location attestation, and each session logs a sign-in country check. The level of checking Anthropic expects (geo-blocking, VPN detection) is unresolved (R3 §3.3; O-007).

**The constraint is the same for both options; the fallbacks are not.**
- **Option A** would need a second model-provider integration, a China-reachable host (with an ICP filing if hosted in mainland China), and PIPL duties as custodian. In exchange, the provider is **replaceable behind the orchestrator**: the interface, state, and protocol enforcement carry over, and only the model call changes (re-validated per interview protocol §15).
- **Option B's** portable skill can run in other agent tools without project hosting, but loses its Claude-specific hooks, permissions, and packaging (Option B §5.3, §10.3).

A human interviewer using the same protocol is a third route. None of these has model parity, and all need legal review (O-007).

## 11. Third-party dependencies

| Dependency | Role | Risk |
|---|---|---|
| Claude API | Inference | Pricing and model changes; refusals; regional policy; suspension of the project account (§16) |
| Hosting, database, object storage | Application | Moderate lock-in; small cost at this scale; processors of unpublished material |
| Sandbox provider (A2) | Execution | Security; cost; licensing; beta status for Managed Agents |
| Auth and e-mail services | Identity | Deliverability in some regions [U] |
| Observability services | Operations | Traces contain transcripts |

## 12. Costs (assumptions shared with Option B; details in the [cost model](cost-and-effort-model.md))

| Cost | Who pays | Order of magnitude |
|---|---|---|
| Inference per contribution | Project | ≈ $13 central ($5–35) at Opus 5.5 list prices with prompt caching, because A1 and staff execution run no agentic loops in the session; ≈ $17 ($6–46) with A2 |
| Hosting (app, database, storage, tracing) | Project | ≈ $13–210 a month from pilot to 200 contributors, excluding inference, e-mail, and paid error tracking [R9 estimate from verified anchors] |
| Sandbox (A2) | Project | ≈ $32 in total for 200 contributions at Managed Agents' session-hour rate [R9 estimate] |
| Development | Project | §13 |
| Operations and security | Project | 0.1–0.25 FTE; periodic security review |
| Support | Project | ≈ 0.75 h per contributor (0.25–1.5) [U]: the web platform plus run-kit questions on contributors' and RAs' machines; ≈ 150 h at 200 contributions, against Option B's ≈ 200 h |
| Evaluation inference | Project | A simulated-contributor regression suite per protocol or model change ([cost model](cost-and-effort-model.md) §4) |
| Contributor-side | Contributor | Time only (A1: their own compute and Stata licence) |
| Shepherding and review | Project | Likely the largest cost. Under staff execution, shepherds also perform the S5 operationalization (≈ 4 h, 2–6 h, per contribution routed to it [U]; the same holds for Option B's B-staff); under A1, as under Option B's local route, contributors pre-do part of it. Measured in the pilot (M9) |

## 13. MVP build plan

| Component | Effort (engineer-weeks) [U: planning estimates] |
|---|---|
| Shared core: protocol assets, schema tooling, validator, packager, internal review pipeline, shepherd console | 10–17.5 (shared with Option B; counted once) |
| Web app shell, authentication, location attestation and sign-in country check, i18n, layout | 2.25–3.5 |
| Uploads, ingestion workers (PDF text, code index), materials viewer | 1.5–2.5 |
| Interview orchestrator: tools, recall locks, exposure tracking, separate suggestion and checker calls, streaming, caching, budgets | 3–4.5 |
| Dossier panel, provenance and exposure badges, review and diff screens | 1.5–2.5 |
| Run-kit generator (copy-then-patch, checksum check of the original) and output intake (A1) | 1–1.5 |
| Run-kit cross-platform test matrix (macOS / Windows / Linux × Stata / R / Python) and guides (EN/ZH) | 1–2 |
| Security hardening, privacy notice and processor agreements, deployment, monitoring | 1.5–3 |
| **Option A-specific total (A1 plus staff execution)** | **≈ 12–19.5**, plus the shared core |
| Hosted sandbox (A2), if added | Managed integration +1.5–3; self-built +3–6 |

The shepherd console (1–1.5 engineer-weeks) moved to the shared core in v0.2.1, because shepherds need it under either option.

**Milestones**
1. Sign-in, upload, and S0–S1 with the design map.
2. S2–S4 with recall locks, dossier, provenance, and exposure tracking.
3. Run kits and S5.
4. Review and submission.
5. Security review and pilot release.

## 14. Operations and maintenance

- **Versioning.** One deployment serves everyone. The protocol version is pinned per contribution, so updates never break sessions in progress. The interviewer is re-evaluated only when the project changes its pinned model or protocol.
- **Monitoring.** Uptime, errors, token spend per session, spend alerts per workspace, cost dashboards, abuse protection, and the sign-in country log.
- **Security.** Dependency updates, access reviews, backups, incident response, and deletion requests.
- **Support.** The web application, plus run-kit questions on contributors' and RAs' own machines, which are as varied as Option B's.

## 15. Scalability

From 10 to 200 contributors the load is a few concurrent interviews, which is modest; costs grow roughly linearly with inference. The account tier must match the planned monthly volume (§5.2). Project effort scales with shepherding, as in Option B, and more slowly with support. International reach is bounded by the regional policy (§10.3) and by whether the site can be reached from each region.

## 16. Risks

The risk registers of both options use one inclusion rule: every risk rated Medium or higher in likelihood or impact is listed.

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Engineering takes longer than planned | Medium–High: more components to build | Medium | Narrow MVP (A1 + staff execution); proven components; reuse ideas, not code, from open interview platforms (non-commercial licences: CC BY-NC 4.0, PolyForm Noncommercial; Wuttke et al.'s is CC0 [P-page]) |
| Breach of unpublished code, drafts, or transcripts (held from upload) | Low–Medium | High | Encryption, minimal retention, processor agreements, access control, security review; no data upload in A1; variant (a) |
| Restricted data uploaded despite the declaration (e.g., inside the code archive) | Low–Medium | High | Data-type rejection; declaration; scan on upload; deletion and incident procedure |
| Project API account suspended or capped | Low–Medium | High: all interviews stop | Location attestation and country checks; monitoring; a separate evaluation workspace; Scale tier before recruitment waves; spend alerts |
| A1 hand-offs stall operationalization | Medium [U: pilot] | Medium–High | Staff execution; RA mode; reminders; A2 for public-data papers |
| Hidden-tier run kits and outputs persist on contributors' or RAs' machines | Medium | Medium–High | Deletion step after upload; deletion after acceptance in the agreement; exposure log |
| A run kit modifies the contributor's local original | Low | High | Copy-then-patch run kits; checksum check before upload |
| Contributors in mainland China, Hong Kong, or Macau cannot be served with Claude | Certain under the current policy for those located there | High for that group | Legal review; second-provider route with validation caveats (O-007) |
| Agent SDK variant (H2) conflicts with end-user payment terms | Medium–High | Medium | Prefer the Messages API path; ask Anthropic (O-018) |
| Operating burden persists after the grant period | Medium | Medium | Small stack; managed services; a sunset plan |
| Support load exceeds capacity (run-kit questions on varied machines) | Medium | Medium | Run-kit test matrix and guides; office hours; FAQ |
| Interview less evidence-anchored than with local code access | Medium | Medium | Code index and viewer; staff execution; A2; RA mode |

## 17. The brief's stated advantages and disadvantages, assessed

| Claim in the brief | Assessment |
|---|---|
| "More accessible experience for senior economists who do not use terminal-based AI tools." | **Likely true for the interview** (browser only, about 15–35 minutes before it starts). **Not automatically true for operationalization:** A1 still asks someone to run code. Staff execution and A2 remove that, the first at the cost of shepherd time, the second only for public-data R/Python packages. |
| "Consistent model behaviour, centralized version control, standardized interactions, easier contribution management." | **True.** This is Option A's strongest scientific advantage: the whole interviewer configuration is fixed, the protocol's recall lock and suggestion gate are enforced server-side, uniform commercial data terms apply, and all consented sessions are observable for research on the interview (§5.4). |
| "Significant costs for inference, hosting, engineering, security, storage, maintenance, support." | **Mixed.** Inference (≈ $13–17 per contribution) and hosting (≈ $13–210 a month) are small. **Engineering, security, and maintenance are the real costs:** ≈ 12–19.5 engineer-weeks beyond the shared core, which is comparable to Option B's ≈ 11.5–20.5, plus ongoing operations. |
| "Handling of potentially sensitive research materials may be particularly challenging." | **True, but bounded by design.** A1 and staff execution keep data off the platform; uploads are limited to code and documents; retention can be short; variant (a) could keep code in the browser during drafting. Under both options Anthropic receives what the model reads, and the project receives the submitted package. Option A additionally holds drafts and abandoned contributions, with its processors. |

## 18. Open questions specific to Option A

1. A1 plus staff execution, or A2, for the MVP? If A2, managed integration or a self-built sandbox?
2. Build on the Claude API directly (reference), on Managed Agents (beta), or on the Agent SDK (terms question O-018)?
3. Hosting region and retention periods, given EU contributors (standard contractual clauses) and the US storage of API data.
4. Are Opus 5.5 and its pricing available in EU regions on Bedrock or Google Cloud's Agent Platform (variant (b))?
5. Would browser-held materials (variant (a)) remove project custody of code during drafting without degrading the interview?
6. Who operates and pays for the platform after the initial project period?

## 19. Changes

**v0.2.1** (independent fairness reviews, 2026-11-05):
- Custody stated with its processors, drafts, and abandoned contributions; exposure rule noted.
- Versioned storage with deletion on withdrawal, instead of write-once objects.
- Location attestation and sign-in country check; account suspension and spend-cap risk; "ample only at the Build tier or above".
- Variants (a) browser-held materials, (b) EU-region model route, (c) in-browser execution.
- Run-kit cross-platform test matrix and guides costed; shepherd console moved to the shared core; A2 split into managed and self-built.
- A1's Stata use and environment diversity stated; research-on-the-interview advantage and provider replaceability credited; unequal China fallbacks stated.
- Inference without in-session agentic work (≈ $13); pre-interview setup time (15–35 minutes); one risk-inclusion rule for both options.
- Cross-document consistency pass (2026-11-05): A1 run kits recorded as hidden-tier copies on contributors' and RAs' machines (data flows, custody, risks) and specified as copy-then-patch with a checksum check of the original; four risks added (run-kit copies, local originals, support load, restricted data in uploads); engineering overrun's basis stated; spend-cap examples at the A1 rate; B-staff noted beside staff execution.

**v0.2.0:**
- Reference stack and verified cost anchors from R9.
- Managed Agents corrected: not first-party-only; Python without R; transcripts retained until deleted.
- Agent SDK variant flagged for the end-user payment terms.
- Data terms specified: no training, a DPA with standard contractual clauses, US storage.
- Regional policy facts added.
- **Staff execution** added as an execution route.
- Stata dominance and the prevalence of restricted data noted.
- Interview orchestrator scope updated for protocol v0.2.0.
