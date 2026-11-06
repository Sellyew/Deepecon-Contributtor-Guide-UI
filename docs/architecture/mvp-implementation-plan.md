# MVP Implementation Plan: Contributor Interface

| | |
|---|---|
| **Status** | **Proposed** draft v0.2 (2026-11-06). For review by the research lead; nothing is built until it is approved. v0.2 adds configurable categories per field (D-025), the map-and-panel review screen, team-side translation with review (D-029), and runnable packages with data routes (D-027). |
| **Implements** | [MVP proposal v0.3](mvp-contributor-interface.md) · [contributor-interface schemas](../../schemas/contributor-interface/README.md) |
| **Principles** | Lightweight; self-hosted; no model and no third-party service in the default configuration (D-018); the team's existing formats are imported as they are. |

---

## 1. Stack

| Component | Choice | Why |
|---|---|---|
| Application | **Django** (one project with two apps, `contributors` and `papers`) | The built-in administration interface covers most of the administrator entry; it also provides internationalization, sessions, CSRF protection, migrations, and a mature security record |
| Pages | Server-rendered templates, plus a small vanilla JavaScript file for autosave, keyboard shortcuts, and keeping the map and item panel in sync. The map is plain HTML and CSS (nested lists in a grid, with markers); the matrix is an HTML table | No build pipeline, no front-end framework, no charting library, no external assets |
| Database | SQLite, in WAL mode | Enough for tens of contributors (team's plan); move to PostgreSQL on the same server if needed |
| Files | A private directory on an encrypted volume, outside the web root, served only by an authorized Django view (through the reverse proxy's internal-redirect feature) | Private storage, with downloads only after an authorization check |
| Translations | Django's gettext catalogues (`en`, `zh-Hans`), maintained by people | No machine translation (D-018) |
| Fonts | System font stacks (PingFang SC, Microsoft YaHei, Noto Sans CJK, then Latin fallbacks) | No web-font service |
| Reverse proxy | Caddy or nginx, with TLS | Uses the institution's certificate, or an ACME certificate if the lead accepts that external (non-AI) certificate authority (O-021) |
| Model gateway | A module that refuses every call unless a model is explicitly configured. In v1 its only caller is the offline `translate_items` command; contributor-facing code never calls it | Local (Mode 1) or external API (Mode 2) only by the research lead's configuration (O-033) |

## 2. Components

1. **Importers** (administrator, command line and admin page):
   - `import_paper_config`: validates `paper-config.json`, including the categories for the paper's field.
   - `import_rubric`: stores the team's rubric file as it is, keyed by version, and normalizes it through the configured categories (`validation/rubric_checks.py`). It refuses the import if any check fails.
   - `import_item_map`: validates the item map (nodes, edges, anchors, excerpts) against the rubric.
   - `import_candidate_package`: stores the agent-facing ZIP that contributors may download, and checks its SHA-256.
   - `translate_items`: drafts translations through the model gateway when a model is configured, and stores them as unreviewed; a team member reviews them in the admin page.
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

| Control | How it is checked |
|---|---|
| No outbound connections in the default configuration | Release test: run the server in a network namespace with egress denied and exercise every page and export; the server's firewall (nftables or ufw) also denies egress except the operating-system update mirror, if the lead allows it |
| No external assets | A Content-Security-Policy of `default-src 'self'`; a test scans rendered pages for any `http(s)://` resource that is not the site's own |
| Authorization on every request | Tests with two contributors and two papers: guessed IDs, copied URLs, and other assignments' API calls, files, and exports are all refused (team plan, acceptance tests) |
| Field visibility | A test that contributor pages and API responses contain only the configured item fields; points, tiers, scoring methods, and researchers-only material never appear |
| Agent-facing exports | A test that exports marked agent-facing contain no expert-only field |
| Tokens and content kept out of logs | A test that greps the logs after a scripted session for tokens and for contributor text |
| Backups | An encrypted nightly backup to project storage, plus a documented restore test before launch |
| Withdrawal | An administrator action that deletes a contributor's reviews, proposals, and uploads, recorded in the event log |
| Translation | The gateway refuses every call without explicit configuration; each draft records model and mode; a test shows contributors never see an unreviewed translation; external-API mode, if ever configured, logs metadata only and is refused for contributor responses and restricted data |
| Uploaded data | Stored encrypted; readable only by team accounts with the data role; deleted according to the contributor agreement and the data's terms; never sent to any model |

## 4. Milestones

| # | Milestone | Done when | Estimate [U] |
|---|---|---|---|
| M1 | Skeleton | Django project, models, importers for configuration, rubric, and item map (both example fields), administration pages, invitation tokens, and both languages; runs with **synthetic** examples only | 1.5–2 engineer-weeks |
| M2 | Selection | Overview; the map and item panel with the matrix toggle; layered cards; the four answers, reasons, and ticks; proposals; "Ask the team"; autosave with conflicts; confirmation with versions; review export | 2–3 |
| M3 | Guidance and submission | Configurable checklist; guidance page; resumable upload with SHA-256 receipt; dataset declarations and routes; public-reference option; manifest export | 1–1.5 |
| M4 | Translation and privacy pass | The `translate_items` command behind the gateway; the review workflow; every control in §3 tested; deployment with TLS, egress firewall, backups, and a restore test | 1–2 |
| M5 | First real configuration | The pilot paper configured from the team's files, with categories, item map, and reviewed translations; a dry run by a team member as a contributor; fixes | 0.5–1.5 |
| | **Total** | | **≈ 6–10 engineer-weeks** for one developer |

The estimate assumes a developer familiar with Django; it excludes the team's work on items, translations of item text, and hosting procurement.

## 5. Acceptance tests (from the team's plan, adapted)

- A contributor's invitation opens their paper directly; there is no paper search and no questionnaire.
- Items appear in the paper's configured categories: the V5 profile and the theory example both work. Fewer or more items work, and proposals never overwrite prepared items.
- Selecting a marker on the map opens its item; moving to the next item moves the ring on the map; selecting a result highlights the items that affect it.
- Locations and excerpts show the author's original file names; only reviewed translations appear, with their label.
- "Reject", "unsure", "keep only one", "revisit across batches", and "change then undo" are all saved correctly.
- Refreshing, losing the connection, timing out, submitting twice, and editing in two tabs never lose data silently.
- The confirmation summary shows the contributor's own words; confirmation creates a new version, and a frozen version cannot be changed.
- The upload shows a SHA-256 that matches the server's record; restricted or confidential datasets cannot be declared without a route; the public-reference option works without an upload.
- The privacy and security tests in §3 pass.
- The core actions can be done with a keyboard; there is no horizontal overflow on laptops or phones.

## 6. Not in v1

Any model use other than the offline translation command; e-mail sending; grading of agent submissions; code execution; reviewer accounts; dashboards; real-time collaboration. Each needs a separate request from the research lead.
