# MVP Implementation Plan: Contributor Interface

| | |
|---|---|
| **Status** | **Proposed** draft v0.3 (2026-11-06). For review by the research lead; nothing is built until it is approved. v0.2 added configurable categories per field (D-025), the map-and-panel review screen, and runnable packages with data routes (D-027); interface languages are catalogues reviewed by the team, and item text is not translated (D-030). v0.3 stages the hosting (P-053): everything up to the demo runs on a team member's computer, and deployment to a server moves to its own milestone (M6), done only before the first outside contributor. On 2026-11-07 it was updated for the framework reset (D-038 to D-042): the gateway row, the record of whether a task is published, the per-item AI disclosure, and the exposure log. |
| **Implements** | [MVP proposal v0.7](mvp-contributor-interface.md) · [contributor-interface schemas](../../schemas/contributor-interface/README.md) |
| **Principles** | Lightweight; self-hosted; no model and no third-party service in the site (D-042); the team's existing formats are imported as they are. |

---

## 1. Stack

| Component | Choice | Why |
|---|---|---|
| Application | **Django** (one project with two apps, `contributors` and `papers`) | The built-in administration interface covers most of the administrator entry; it also provides internationalization, sessions, CSRF protection, migrations, and a mature security record |
| Pages | Server-rendered templates, plus a small vanilla JavaScript file for autosave, keyboard shortcuts, and keeping the map and item panel in sync. The map is plain HTML and CSS (nested lists in a grid, with markers); the matrix is an HTML table | No build pipeline, no front-end framework, no charting library, no external assets |
| Where it runs | **Stage 0:** a team member's computer with full-disk encryption; the application listens only on the loopback address (127.0.0.1), with synthetic examples and the demo paper only. **Stage 1** (M6): one small project-controlled server outside mainland China, before the first outside contributor (P-053) | No server decision is needed for the demo; moving is installing the pinned application with Stage 1 settings and, if wanted, copying the data folder (M6) |
| Database | SQLite, in WAL mode | Enough for tens of contributors (team's plan); move to PostgreSQL on the same server if needed |
| Files | A private directory on an encrypted volume, outside the web root, served only by an authorized Django view (streamed by Django at Stage 0; through the reverse proxy's internal-redirect feature at Stage 1) | Private storage, with downloads only after an authorization check |
| Interface languages | Django's gettext catalogues (`en`, `zh-Hans`; a language is added as one more catalogue), drafted with an LLM and reviewed by the team; per-paper labels are localized in the paper configuration | Interface text contains no project material (D-030); item text is not translated |
| Fonts | System font stacks (PingFang SC, Microsoft YaHei, Noto Sans CJK, then Latin fallbacks) | No web-font service |
| Reverse proxy (Stage 1) | Caddy or nginx, with TLS | Uses the institution's certificate, or an ACME certificate if the lead accepts that external (non-AI) certificate authority (O-021) |
| Model gateway | A module that refuses every call; v1 has no caller | Any later AI feature in the site is configured by the research lead; it never receives restricted data, and contributors' material only with their consent (D-042). The project deploys no models (D-038) |

## 2. Components

1. **Importers** (administrator, command line and admin page):
   - `import_paper_config`: validates `paper-config.json`, including the categories for the paper's field. The administrator records whether the task is published or unpublished, and keeps the task's exposure log: which AI providers received its answer-key material or package, when, and through what kind of account (D-040).
   - `import_rubric`: stores the team's rubric file as it is, keyed by version, and normalizes it through the configured categories (`validation/rubric_checks.py`). It refuses the import if any check fails.
   - `import_item_map`: validates the item map (nodes, edges, anchors, excerpts) against the rubric.
   - `import_candidate_package`: stores the agent-facing ZIP that contributors may download, and checks its SHA-256.
2. **Invitations.**
   - Tokens are generated with `secrets.token_urlsafe(32)` and stored as SHA-256 hashes, with an expiry and a revocation flag.
   - The first visit sets a session.
   - An optional passcode can be sent through a second channel (O-022).
   - Tokens never appear in logs: request logging records the path with the token removed.
3. **Contributor views:**
   - notice and consent;
   - my paper;
   - overview;
   - the review screen: the map (stages, files or sections, results, item markers, matrix toggle) beside the item panel (headline, local change, why it matters, what a correct answer must do, answer controls);
   - "Ask the team" messages on each item;
   - proposal form;
   - review and confirm;
   - guidance;
   - submission.

   Every view checks the session's assignment against the requested paper and item, on the server.
4. **Autosave API.** A JSON endpoint that writes one item review at a time. It uses an optimistic version number, so a concurrent edit returns a visible conflict rather than being silently overwritten. The page shows "saved" or "not saved" only after the server answers.
5. **Uploads.**
   - Chunked uploads with resumption for packages of several gigabytes; the server computes SHA-256 and shows it to the contributor.
   - A configurable size limit (default 20 GB), and another agreed channel for anything larger.
   - A dataset declaration form: each dataset's availability and route (included, public elsewhere, restricted or confidential with its route). It requires the declaration that nothing restricted is included and, if data are included, permission to share them.
   - Packages are unpacked only for listing file names and sizes; nothing is executed on the server.
6. **Exports** (administrator):
   - the contributor review as JSON, validated against `contributor-review.schema.json`;
   - a readable bilingual summary (HTML or Markdown);
   - suggested rubric changes as a diff against the imported rubric;
   - the submission manifest as JSON.
7. **Freeze.** Freezing locks a paper's review version; later edits open a new version. An event log records actor, operation, object, versions, and time.

## 3. Security and privacy controls

Controls marked *(Stage 1)* apply once the site runs on a server (M6). On the demo computer the site is reached only from that computer (loopback address only) and holds only synthetic and demo material.

| Control | How it is checked |
|---|---|
| Stage 0 binding | A request from a second machine on the same network is refused |
| No outbound connections in the default configuration | Release test (the firewall part is Stage 1): run the server in a network namespace with egress denied and exercise every page and export; the server's firewall (nftables or ufw) also denies egress except the operating-system update mirror, if the lead allows it |
| No external assets | A Content-Security-Policy of `default-src 'self'`; a test scans rendered pages for any `http(s)://` resource that is not the site's own |
| Authorization on every request | Tests with two contributors and two papers: guessed IDs, copied URLs, and other assignments' API calls, files, and exports are all refused (team plan, acceptance tests) |
| Field visibility | A test that contributor pages and API responses contain only the configured item fields; points, score tiers, scoring methods, and researchers-only material never appear |
| Agent-facing exports | A test that exports marked agent-facing contain no expert-only field |
| Tokens and content kept out of logs | A test that greps the logs after a scripted session for tokens and for contributor text |
| Backups *(Stage 1)* | An encrypted nightly backup to a second location, plus a documented restore test before the first outside contributor |
| Withdrawal | An administrator action that deletes a contributor's reviews, proposals, and uploads, recorded in the event log |
| Model gateway | A test that the gateway refuses every call in v1 and that no module other than the gateway opens a model connection |
| Uploaded data | Quarantined, encrypted and unopened, until the data steward has checked each dataset's terms (MVP §5.5); then readable only by team accounts with the data role; deleted according to the contributor agreement and the data's terms; never sent to any model |

## 4. Milestones

| # | Milestone | Done when | Estimate [U] |
|---|---|---|---|
| M1 | Skeleton | Django project, models, importers for configuration, rubric, and item map (both example fields), administration pages, invitation tokens, and both languages; schemas 0.3.0 with the fields the AI use and integrity rules need (see the [schema README](../../schemas/contributor-interface/README.md)); runs with **synthetic** examples only | 1.5–2 engineer-weeks |
| M2 | Selection | Overview; the map and item panel with the matrix toggle; layered cards; the four answers, reasons, and ticks; the per-item AI disclosure (D-039); proposals; "Ask the team"; autosave with conflicts; confirmation with versions; review export | 2–3 |
| M3 | Guidance and submission | Configurable checklist; guidance page; resumable upload with SHA-256 receipt; dataset declarations and routes; public-reference option; manifest export | 1–1.5 |
| M4 | Languages and privacy pass | Reviewed Chinese catalogue; data quarantine and steward check; every control in §3 not marked Stage 1 tested on the demo computer | 0.75–1 |
| M5 | Demo configuration | The demo paper (D-024) configured from the team's files, with categories and item map; a dry run by a team member as a contributor; fixes | 0.5–1.5 |
| M6 | Stage 1 deployment (only before the first outside contributor, O-036) | One server outside mainland China with TLS, egress firewall, encrypted disk, backups, and a restore test; demo invitations and test accounts revoked; a reachability test from mainland China and from abroad; the Stage 1 controls in §3 tested | 0.25–0.5 |
| | **Total** | | **≈ 6–9.5 engineer-weeks** for one developer |

The estimate assumes a developer familiar with Django; it excludes the team's work on items (and any synthetic stand-in for the run kit), the team's review of the interface catalogue, and hosting procurement.

## 5. Acceptance tests (from the team's plan, adapted)

- A contributor's invitation opens their paper directly; there is no paper search and no questionnaire.
- Items appear in the paper's configured categories: the V5 profile and the theory example both work. Fewer or more items work, and proposals never overwrite prepared items.
- Selecting a marker on the map opens its item; moving to the next item moves the ring on the map; selecting a result highlights the items that affect it.
- Locations and excerpts show the author's original file names; switching the interface language changes every interface string but no item text.
- "Reject", "unsure", "keep only one", "revisit across batches", and "change then undo" are all saved correctly.
- Refreshing, losing the connection, timing out, submitting twice, and editing in two tabs never lose data silently.
- The confirmation summary shows the contributor's own words; confirmation creates a new version, and a frozen version cannot be changed.
- The upload shows a SHA-256 that matches the server's record; restricted or confidential datasets cannot be declared without a route; the public-reference option works without an upload.
- The privacy and security tests in §3 pass.
- The core actions can be done with a keyboard; there is no horizontal overflow on laptops or phones.

## 6. Not in v1

Any model use; e-mail sending; grading of agent submissions; code execution; reviewer accounts; dashboards; real-time collaboration. Each needs a separate request from the research lead.
