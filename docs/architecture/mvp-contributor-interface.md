# MVP: Privacy-Preserving Contributor Interface

| | |
|---|---|
| **Status** | **Proposed** draft v0.1 (2026-11-06). Replaces the Option A / Option B proposals as the basis for the first version. **Sections 6–8 are provisional:** the contribution data model, the submission requirements, and the implementation plan will be finalized only after the example contribution package has been reviewed (D-023). |
| **Requirements** | [Research lead's revision, 2026-11-06](../requirements/2026-11-06-research-lead-revision.md) (governs) · [team handover plan, 2026-11-05](../requirements/2026-11-05-team-handover-plan.md) · [original brief](../requirements/2026-11-05-research-lead-brief.md) |
| **Supersedes** | The [decision brief](architecture-decision-brief.md), [Option A](option-a-hosted-platform.md), [Option B](option-b-local-skill.md), the [interview protocol](../interview/expert-interview-protocol.md), the [pilot plan](../pilot/pilot-evaluation-plan.md), and the [cost model](cost-and-effort-model.md). They are kept as records only. |

---

## 1. What the first version does

Invited contributors use a small bilingual website (English and Simplified Chinese). Contributors are the paper's authors or invited domain experts. The website has two functions.

1. **Selection.** The contributor opens their own paper, which the team has already configured. They review the candidate errors the team prepared locally. For each candidate they can select, modify, reject, mark as uncertain, or comment, and they can propose additional errors.
2. **Guidance.** The contributor reads what materials to provide, how to prepare them, and how to submit them. They then upload the materials or record the agreed submission channel.

**No step of this workflow needs an AI model.** The website runs on infrastructure the project controls and, by default, sends nothing to any AI provider (§5).

**Out of scope for the first version:**
- Decided by the research lead on 2026-11-06:
  - an AI interview;
  - AI-generated errors or flawed packages;
  - Claude Code or any other client software for contributors;
  - paper discovery;
  - onboarding beyond a short notice.
- Deferred, as in the team's plan:
  - code execution;
  - an online review platform;
  - real-time collaboration;
  - voice;
  - dashboards;
  - automatic evaluation;
  - sending e-mail from the site.

## 2. Users and roles

| Role | Who | What they do on the site |
|---|---|---|
| **Contributor** | An author of the paper, or an invited domain expert. The assignment records which (`relationship_to_paper`) | Reviews the candidates for their assigned paper(s), comments, proposes additions, follows the guidance, submits materials |
| **Administrator** | Research team | Configures papers, materials, candidates, targets, and invitations; follows progress; exports decisions; receives submissions; freezes versions |
| *Later, offline in v1* | Implementers, independent reviewers | Work outside the site, as in the team's three verification rounds; the administrator records the results |

## 3. The contributor's path

| Step | Screen | Content |
|---|---|---|
| 1 | **Invitation and notice** | The contributor opens a personal invitation link (sent by the team by e-mail or WeChat), chooses English or 中文, and reads a short notice: what is stored, who can see it, that no AI service processes it, how to withdraw, and a confidentiality request for the candidate material (§5.4). Then they accept. |
| 2 | **My paper** | The contributor's paper is already listed (usually one), with title, version, and a team contact. They open it; there is no search or catalogue. |
| 3 | **Task overview** | One paragraph on the purpose. The candidates are **deliberate, hypothetical modifications prepared to build benchmark tasks, not claims that the published paper contains these errors.** The two types are explained in one line each: *error* (an analysis step is done wrongly) and *missing* (a necessary step is removed). The team's target numbers are shown as planning targets, not quotas. Below is a list of all candidates with their status: not yet reviewed, needs material, selected, rejected, uncertain. |
| 4 | **Candidate review**, about five per batch | Each card covers one key point:<br>• **where** it is: a paper page or a code file and lines, with an excerpt shown on request or the PDF opened at that page;<br>• **the proposed modification**: where the team prepared both an *error* and a *missing* variant, they are shown side by side with equal weight and no preselection;<br>• **the expected consequence**, as prepared by the team.<br>**Actions:** select one or both variants; edit a variant (the original is kept); reject, with an optional reason (not realistic, not consequential, not implementable, other); mark uncertain; skip for now; comment.<br>The contributor can move between batches, revisit, and reorder. |
| 5 | **Propose an addition** (optional, available throughout) | A short form: location, what would be changed, why it matters, and an optional expected consequence. The addition is stored as contributor-originated and does not replace any prepared candidate. |
| 6 | **Review and confirm** | A summary of every action, with the contributor's own words as entered. The contributor confirms. Each confirmation creates a new version, and they can return and revise until the team freezes the paper's version. |
| 7 | **Materials guidance** | What to provide (a checklist), how to prepare it (steps), the rules for restricted data, and how to submit. *The content depends on the example package (§8).* |
| 8 | **Submit materials** | The contributor uploads to the project server (resumable, with a checksum receipt) or records that the materials go through another agreed channel. The page then shows receipt status. |

**Interaction rules** carried over from the team's plan:
- one column, with one main action per screen;
- evidence opens on request and returns to the same card without losing edits;
- autosave reports success or failure explicitly, and a refresh restores state;
- "neither suitable" and "uncertain" are as easy as "select", nobody is asked to fill a quota, and stopping early is fine;
- rejections and uncertainty count as reviewed but not as confirmed;
- the site works with a keyboard and on laptops; on phones it supports reading, choosing, and short edits.

## 4. Administrator functions (v1)

- **Configure:**
  - papers (title, version, PDFs, code index);
  - contributors and assignments;
  - targets for each type;
  - the candidate pool, imported from the file the team prepares locally (the format is settled from the example package).
- **Invite:** create and revoke invitation links. The team delivers them through its existing e-mail or WeChat contact, so the site sends no e-mail in v1.
- **Follow up:** progress per contributor and per candidate.
- **Export:**
  - the contributor's decisions as JSON;
  - a readable bilingual summary;
  - an engineering task list for the team's implementation round.
- **Receive submissions:** verify checksums and record receipt.
- **Freeze** a paper's decision version; later changes create a new version. Every change goes into an event log.

A built-in administration interface is enough; no separate review platform is built.

## 5. Privacy and data-flow architecture

### 5.1 Principle

Research data, replication code, paper materials, contributor responses, and intermediate outputs are never sent to Anthropic or any other third-party AI service (D-018). The site works completely without any model. A model is used only if the research lead deploys or configures one, and every external integration is off until explicitly configured.

### 5.2 Data flows in the default configuration

| Flow | What travels | Between |
|---|---|---|
| Contributor ↔ site | Pages, the assigned paper's candidates and evidence, the contributor's responses, uploads | The contributor's browser and the project server only, over TLS |
| Administrator ↔ site | Configuration, imports, exports | The team and the project server, over TLS; optionally restricted to the team's network or a VPN |
| Invitations | The link only, no research content | The team's existing e-mail or WeChat channel |
| Backups | Encrypted copies | Project-controlled storage |
| **Anything else** | **Nothing** | The site has no analytics, error-tracking service, content delivery network, web fonts, maps, or embedded third-party content. All scripts, styles, and fonts are served by the project server, and outbound network access from the server is blocked except for destinations the administrator configures |

Hosting is itself a choice about who can access the machine: an institutional server, or a virtual machine the project rents (O-021). Neither is an AI service, but the choice decides who operates the hardware and where the data reside.

### 5.3 Model integration: three modes

| Mode | Meaning | Where the data go | Default |
|---|---|---|---|
| **0: Off** | No model calls. Every contributor and administrator feature works. | Nowhere | **On** (v1 runs in this mode) |
| **1: Local model** | A model served on hardware the project controls, for example an open-weight model run by the research lead | Stays inside project infrastructure; no third party receives it | Off; enabled by configuration |
| **2: External API** | A provider's hosted API, for example the DeepSeek API with the research lead's own key | **Leaves project infrastructure.** The provider processes it under its own terms, outside project control | Off; needs explicit configuration **and** a per-material permission |

**Using a DeepSeek API key is Mode 2, not Mode 1.** Only a model running on the project's own hardware is Mode 1.

**Enforcement:**
- **One gateway.** All model calls go through a single server module, and nothing else in the code base may open a model connection. The gateway refuses every call in Mode 0.
- **Explicit configuration.** Modes 1 and 2 need explicit settings (mode, endpoint, model name). The administrator page always shows the current mode.
- **Per-material permission.** Each material carries `allowed_model_destinations` (from the team's plan). A call in Mode 2 is refused unless every input is marked as allowed for that destination.
- **Proposed default for Mode 2 (P-035):** contributor responses, restricted materials, unpublished materials, and candidate answer material are never eligible for external models.
- **Disclosure and logging.** Contributors are told before any of their content could reach a model. Every call is logged with metadata only (time, mode, destination, material IDs), never content.
- **Network check.** The server's outbound firewall permits only the configured model endpoint. A release test confirms that in Mode 0 no outbound connection succeeds.
- **Machine translation is a model call.** No external translation service is used. Contributor text is stored as written; if translation is needed, a person or a Mode 1 model does it.

Running a large open-weight model locally needs substantial GPU hardware; the exact requirements depend on the model and are unverified here [U]. A smaller local model is cheaper, but its quality for these tasks is unvalidated.

### 5.4 Storage, access, and confidentiality

- **Invitation credentials:**
  - random (at least 128 bits), time-limited, and revocable;
  - stored only as hashes and never written to logs;
  - optionally paired with a short passcode sent through a second channel (O-022).
- **Server-side authorization on every request** (page, API, file preview, download, export). A contributor reaches only the materials and candidates of their own assignments; guessing an ID or copying a URL fails.
- **Private storage.** Files sit outside the web root on an encrypted disk. Downloads use short-lived links issued after the authorization check.
- **Logs** record actions and object IDs, never invitation credentials, contributor text, or file contents.
- **Retention and withdrawal.** Contributor responses and uploads are deleted on withdrawal, subject to the contributor agreement. A retention period is set before launch.
- **Candidates are answer-key material.** They are never public and never appear in any material prepared for evaluated agents. The notice asks contributors to keep them confidential (O-026).

### 5.5 Restricted data

The site never asks for restricted microdata. The upload screen warns against including it, and the guidance explains how to document data access instead. For the pilot paper, the public replication package already has empty DEIS and SIRH raw-data directories (team handover plan §7). Derived files built from restricted data inherit the original licence (P-027).

## 6. Data model *(provisional; finalized from the example package)*

The model starts from the team's objects (handover plan §5) and keeps only what the contributor interface needs. Team-side objects (implementation, review, rubric, release) stay in the team's own workflow until the back office is designed.

| Object | Purpose | Key fields (provisional) |
|---|---|---|
| **Paper** | A configured paper (the team's *Project*) | paper_id, paper_version, title, citation, status, target_error_count, target_missing_count |
| **Material** | A file attached to a paper | material_id, paper_id, file_role, file_version, checksum, private_storage_key, access_scope, allowed_model_destinations (default: none), allowed_for_contestant |
| **Assignment** | A contributor's access to a paper | assignment_id, contributor_id, paper_id, relationship_to_paper (author / invited expert), invited_at, invitation status |
| **Candidate** | A prepared key point | candidate_id, paper_id, version, origin (team / contributor), domain (engineering / economics), variants (*error* and/or *missing*: description, location, expected consequence, feasibility note), evidence_refs (file, PDF page index, printed page, code path and lines), display order |
| **Decision** | A contributor's response to a candidate | candidate_id, candidate_version, action (select-error, select-missing, select-both, modify, reject, uncertain, skip), reason, original text, edited variant text, comment, version, confirmed_at |
| **Proposal** | A contributor-suggested addition | proposal_id, paper_id, location, description, rationale, expected consequence |
| **Submission** | Materials the contributor provides | submission_id, assignment_id, channel (upload / other agreed channel), files and checksums, declared contents, restricted-data declaration, status |
| **EventLog** | Audit trail | actor, operation, object_id, before and after version, timestamp |

Rules from the team's plan apply:
- a team-prepared candidate is never shown as confirmed until the contributor confirms it;
- new material marks dependent decisions "needs re-review";
- confirmed content is never overwritten;
- frozen versions are immutable.

The team's teacher-model estimates and ranks are internal fields. They set the initial order but are not shown as recommendations.

## 7. Technology direction *(provisional; decided in the implementation plan)*

- **Shape.** One server application with server-rendered pages and a little progressive enhancement, SQLite (as the team's plan suggests), private files on the server's encrypted disk, and message catalogues for English and Simplified Chinese.
- **Leading candidate: Django.** Its built-in administration interface covers most of the administrator entry, and it has internationalization, sessions, CSRF protection, and migrations. The final choice depends on the example package and on the team's skills.
- **Fonts.** System font stacks (PingFang SC, Microsoft YaHei, Noto Sans CJK, then Latin fallbacks); no Google Fonts or other external font service, whose reachability from mainland China is also contested [S].
- **Uploads.** Chunked, resumable uploads to the server, with size limits set from the example package and a published fallback channel for very large packages.
- **Deployment.** One server behind a TLS reverse proxy, with outbound traffic blocked by default and restorable encrypted backups.

## 8. What the example package should settle

The review of the example contribution package (expected next) should answer these questions before the schema and the implementation plan are finalized.

1. **Structure:** the folder layout, file naming, and which files are the paper, code, data, outputs, and documentation.
2. **Candidate errors:** how a prepared candidate is represented (fields, error and missing variants, evidence locations, expected consequences, code changes), and how the contributor's choices are recorded.
3. **What contributors provide:** code, data or data-access documentation, logs, a README, the map from paper results to scripts, software versions, licences.
4. **Size and format:** typical and maximum size; compression; checksums.
5. **Restricted data:** how it is documented, and what may and may not be sent.
6. **Versioning and confirmation:** how the coauthor marked what was confirmed, changed, or added.
7. **Languages:** which parts are in English or Chinese, and what must be bilingual.

## 9. What carries over from the earlier work

- **Still useful, as the team's internal methodology** for turning confirmed candidates into verified tasks: the [verifier validation protocol](../methodology/verifier-validation-protocol.md), the [rubric](../methodology/task-quality-rubric.md), and the [construction protocol](../methodology/benchmark-construction-protocol.md). They are to be aligned with the team's three verification rounds. Their passages that assume an AI interview, Options A and B, or Claude-based sessions are superseded.
- **Proposals that remain open for review:**
  - derived data inherit the licence (P-027);
  - an independent check of the reference (P-028);
  - the materiality rule (P-029);
  - scoring (P-030);
  - contamination controls (P-032);
  - pitfall-status corrections (P-033).
- **Also kept:** the bilingual principles and glossary ([bilingual design](bilingual-design.md)) and the evidence labels.
- **Superseded:**
  - the Option A versus Option B comparison;
  - the AI interview protocol and its influence measures;
  - the exposure rule's implications for Claude accounts;
  - the A/B pilot;
  - the cost model.

## 10. Points for the research lead

1. **Framing for authors.** An author shown "errors" in their own paper may read them as criticism. The overview and every card should say plainly that these are deliberate modifications for building tasks (P-037). The paper's own acknowledged limitations are recorded separately, as the team's plan already does.
2. **Easy agreement.** Contributors shown prepared errors may accept them without much scrutiny. The team's design of symmetric variants, no preselection, and no quotas is the right defence. I would add an optional one-line reason when a contributor selects a candidate, and report acceptance and rejection rates per paper; the team's plan already records rejection reasons.
3. **The evaluation phase.** Evaluating a closed model as an agent means sending the agent-facing task material to that model's provider. The privacy rule therefore cannot cover that phase in the same way. I suggest deciding now what may be sent at evaluation time (agent-facing material only, never candidate answers or contributor responses), and how held-out tasks are protected (O-025).
4. **The teacher model in the team's plan** ranks and proposes candidates. It falls under the same modes: if it is a hosted model, such as either candidate named in the plan used through its API, it is Mode 2 and is off by default.
5. **This design work.** These documents are prepared with Claude, so anything shared in that work, including the example package, reaches Anthropic. Where material should not, share its structure and synthetic stand-ins instead.

## 11. Open questions

| ID | Question |
|---|---|
| O-021 | Where the site is hosted and who operates it: an institutional server or a project-controlled virtual machine; region; reachability for contributors in mainland China and elsewhere; backups |
| O-022 | How invitations reach contributors and whether a second factor (a passcode by a second channel) is required |
| O-023 | Whether v1 uses any model at all; if so, for which tasks, in Mode 1 or Mode 2, and for which material classes |
| O-024 | The submission channel and limits for replication packages (to be settled from the example package) |
| O-025 | What may be sent to model providers when the finished benchmark is used to evaluate closed models |
| O-026 | Whether contributors agree to keep candidate material confidential, and how this is recorded |
| O-001, O-005, O-013, O-014, O-020 | Release policy; contributor credit; ethics review; project name; who operates and funds the site after the initial period (unchanged) |
