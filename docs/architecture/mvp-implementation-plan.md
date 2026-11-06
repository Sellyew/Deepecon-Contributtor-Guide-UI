# MVP Implementation Plan: Contributor Interface

| | |
|---|---|
| **Status** | **Proposed** draft v0.1 (2026-11-06). For review by the research lead; nothing is built until it is approved. The answers to Q1–Q6 in the [MVP proposal](mvp-contributor-interface.md) §9 may change details but not the overall shape. |
| **Implements** | [MVP proposal v0.2](mvp-contributor-interface.md) · [contributor-interface schemas](../../schemas/contributor-interface/README.md) |
| **Principles** | Lightweight; self-hosted; no model and no third-party service in the default configuration (D-018); the team's existing formats are imported as they are. |

---

## 1. Stack

| Component | Choice | Why |
|---|---|---|
| Application | **Django** (one project with two apps, `contributors` and `papers`) | The built-in administration interface covers most of the administrator entry; it also provides internationalization, sessions, CSRF protection, migrations, and a mature security record |
| Pages | Server-rendered templates, plus a small vanilla JavaScript file for autosave and batch navigation | No build pipeline, no front-end framework, no external assets |
| Database | SQLite, in WAL mode | Enough for tens of contributors (team's plan); move to PostgreSQL on the same server if needed |
| Files | A private directory on an encrypted volume, outside the web root, served only by an authorized Django view (through the reverse proxy's internal-redirect feature) | Private storage, with downloads only after an authorization check |
| Translations | Django's gettext catalogues (`en`, `zh-Hans`), maintained by people | No machine translation (D-018) |
| Fonts | System font stacks (PingFang SC, Microsoft YaHei, Noto Sans CJK, then Latin fallbacks) | No web-font service |
| Reverse proxy | Caddy or nginx, with TLS | Uses the institution's certificate, or an ACME certificate if the lead accepts that external (non-AI) certificate authority (O-021) |
| Model gateway | A module whose only implemented mode in v1 is **Off**; every call raises an error | Modes 1 and 2 are added later, on request (P-035) |

## 2. Components

1. **Importers** (administrator, command line and admin page):
   - `import_rubric`: validates a `Rubric.json` against `rubric-import.schema.json` and stores it immutably, keyed by rubric version, preserving unknown fields.
   - `import_paper_config`: validates and stores `paper-config.json`.
   - Optionally `import_candidate_package`: stores the agent-facing ZIP and checks its SHA-256 against the configuration.
2. **Invitations.**
   - Tokens are generated with `secrets.token_urlsafe(32)` and stored as SHA-256 hashes, with an expiry and a revocation flag.
   - The first visit sets a session.
   - An optional passcode can be sent through a second channel (O-022).
   - Tokens never appear in logs: request logging records the path with the token removed.
3. **Contributor views:**
   - notice and consent;
   - my paper;
   - overview;
   - item review in batches of about five;
   - proposal form;
   - review and confirm;
   - guidance;
   - submission.

   Every view checks the session's assignment against the requested paper and item, on the server.
4. **Autosave API.** A JSON endpoint that writes one item review at a time. It uses an optimistic version number, so a concurrent edit returns a visible conflict rather than being silently overwritten. The page shows "saved" or "not saved" only after the server answers.
5. **Uploads.**
   - Chunked uploads with resumption; the server computes SHA-256 and shows it to the contributor.
   - A configurable size limit; for code and documentation, 200 MB is generous.
   - The data declaration must be ticked before uploading.
   - A file-type check warns about likely data files (`.dta`, `.csv` above a size threshold, `.sav`, `.parquet`), without blocking dictionaries.
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

## 4. Milestones

| # | Milestone | Done when | Estimate [U] |
|---|---|---|---|
| M1 | Skeleton | Django project, models, importers validating against the schemas, administration pages, invitation tokens, and both languages; runs with **synthetic** examples only | 1–1.5 engineer-weeks |
| M2 | Selection | Overview, item review in batches, proposals, autosave with conflicts, confirmation with versions, review export | 1–2 |
| M3 | Guidance and submission | Configurable checklist, guidance page, chunked upload with SHA-256 receipt, public-reference option, manifest export | 0.5–1 |
| M4 | Privacy and security pass | Every control in §3 tested; deployment on the chosen server with TLS, egress firewall, backups, and a restore test | 1–1.5 |
| M5 | First real configuration | The V5 paper configured from the team's files after Q1–Q6 are answered; a dry run by a team member as a contributor; fixes | 0.5–1 |
| | **Total** | | **≈ 4–7 engineer-weeks** for one developer |

The estimate assumes a developer familiar with Django; it excludes the team's work on items, translations of item text, and hosting procurement.

## 5. Acceptance tests (from the team's plan, adapted)

- A contributor's invitation opens their paper directly; there is no paper search and no questionnaire.
- All 15 V5-format items appear in their groups, in batches of about five. Fewer or more items work too, and proposals never overwrite prepared items.
- "Reject", "unsure", "keep only one", "revisit across batches", and "change then undo" are all saved correctly.
- Refreshing, losing the connection, timing out, submitting twice, and editing in two tabs never lose data silently.
- The confirmation summary shows the contributor's own words; confirmation creates a new version, and a frozen version cannot be changed.
- The upload shows a SHA-256 that matches the server's record; the data declaration is required; the public-reference option works without an upload.
- The privacy and security tests in §3 pass.
- The core actions can be done with a keyboard; there is no horizontal overflow on laptops or phones.

## 6. Not in v1

Model modes 1 and 2; e-mail sending; grading of agent submissions; code execution; reviewer accounts; dashboards; real-time collaboration. Each needs a separate request from the research lead.
