# Contributor interface (implementation)

**Status: milestone M1 (skeleton) built on 2026-11-07**, after the research lead approved the [implementation plan](../../docs/architecture/mvp-implementation-plan.md) (D-043). The site runs with the fictional examples only. Next is M2, the Selection screens.

One Django application (Django 5.2, a long-term-support release) for the [MVP contributor interface](../../docs/architecture/mvp-contributor-interface.md). Pages are rendered on the server. It uses SQLite in WAL mode and private file storage, and loads nothing from other websites. It sends nothing to AI services: the model gateway refuses every call (D-042). It follows the [AI use and integrity rules](../../docs/architecture/llm-use-policy.md).

## What M1 contains

| Part | Where |
|---|---|
| Settings for both stages: Stage 0 (the demo computer, loopback only) and Stage 1 (a server, M6). All state lives in one data folder | `deepecon_site/settings.py` |
| Security headers (`default-src 'self'`, no referrer, no caching), log redaction of invitation tokens, and the model gateway that refuses every call | `deepecon_site/middleware.py`, `logging_filters.py`, `gateway.py` |
| Models: papers, rubric versions, items, item maps, candidate packages, the exposure log (Rule 10), and the event log | `papers/models.py` |
| Importers for the paper configuration, rubric, item map, and candidate package, each checked against the [schemas](../../schemas/contributor-interface/README.md) and [`validation/rubric_checks.py`](../../validation/rubric_checks.py) and refused if any check fails. A rubric version, once imported, is never overwritten; a changed configuration is checked again against the stored rubric and item map; a package is accepted only against the SHA-256 in the configuration. After an evaluation run, a task's publication status and designation date cannot change (Rule 8). Available as commands and as an administration page, which needs the permission to change papers | `papers/importers.py`, `papers/management/commands/`, `papers/admin.py` |
| Personal links: one per contributor at a time (a new link revokes the earlier ones), random tokens stored only as SHA-256 hashes. A link is shown once, never stored or logged. The session remembers the link and checks it on every request: revoking the link ends sessions opened with it, while its expiry only stops new sign-ins (D-044); otherwise a session lasts while it is used, and a year without use ends it (D-045). Creating and revoking links need their own admin permissions | `contributors/models.py`, `contributors/access.py`, `contributors/admin.py`, `create_invitation` |
| Choosing a paper (D-044, P-060): the link opens one paper at a time, the contributor's current paper. Contributors choose it from the papers offered to them (their assignments, and papers the team marks "open to all contributors" on the paper's admin page), seeing citations only until they choose; they can change it from the notice or "My paper" after a confirmation, and earlier work is kept. The team moves a paper the contributor chose only at their request, through the "Danger zone" on the contributor's page (D-045), and an assignment's contributor and paper cannot be changed once it exists. Every choice is in the event log | `contributors/views.py`, `templates/contributors/papers.html`, `choose.html` |
| Contributor pages: invitation landing, the list of papers and the confirmation for changing paper, notice and consent (dated and changeable; worded for authors or for invited experts), "My paper", and the package download. Every page checks the requested paper against the current paper on the server | `contributors/views.py`, `templates/contributors/` |
| Interface languages: English and Simplified Chinese. The Chinese catalogue is **machine-drafted by Claude and awaits the team's review** (M4) | `locale/zh_Hans/LC_MESSAGES/django.po` |
| Demo loader: the fictional empirical and theory examples (both open to all), synthetic packages, and three demo contributors: two authors whose link opens their paper, and an invited expert who chooses one | `contributors/management/commands/load_demo.py` |
| Exposure log (Rule 10): entries are added and viewed, never edited or deleted; the recorder's name comes from the account, and an evaluation run needs the pinned model version and its release date | `papers/models.py`, `papers/admin.py` |
| Tests (99): importers, links and revocation, choosing and changing paper, consent, access to other papers, admin permissions, language switching, the link migration, security headers, external assets, private storage, the gateway, network imports, and log redaction | `*/tests.py` |

## Run the demo (Stage 0)

```bash
python3 -m venv .venv
```

```bash
.venv/bin/pip install -r requirements.txt
```

```bash
.venv/bin/python manage.py migrate
```

```bash
.venv/bin/python manage.py load_demo
```

```bash
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

`load_demo` prints one invitation link per demo contributor; the links are shown only once. To reach the team pages at `http://127.0.0.1:8000/team-admin/`, first create an account:

```bash
.venv/bin/python manage.py createsuperuser
```

At Stage 0 the server refuses to listen on any address other than the loopback address. The data folder is `data/` unless `DEEPECON_DATA_DIR` says otherwise. Keep it on an encrypted disk.

## Import a paper

```bash
.venv/bin/python manage.py import_paper_config path/to/paper-config.json
```

```bash
.venv/bin/python manage.py import_rubric PAPER_ID path/to/rubric.json
```

```bash
.venv/bin/python manage.py import_item_map PAPER_ID path/to/item-map.json
```

```bash
.venv/bin/python manage.py import_candidate_package PAPER_ID path/to/candidate.zip
```

The same imports are available on the team administration page (Papers, then "Import the team's files"). To offer a paper to every invited contributor, open the paper and tick "open to all contributors"; for a scored task, do this only if any invited contributor may see its items, and otherwise create assignments for individual contributors. Unticking it stops new choices only: contributors who already chose the paper keep it (Assignments, filtered by the paper and "Chosen by the contributor"); to withdraw it, delete those assignments.

To invite someone, create the link from an assignment (Assignments, action "Create a personal link, opening this paper unless the contributor has chosen one"), or from a contributor (Contributors, action "Create the personal link"), which opens their current paper, or the list of papers offered to them if they have none. To re-issue a link, use the contributor row: a paper the contributor chose stays theirs.

If a contributor asks the team to move their link (to another paper offered to them, or back to the list of papers), open the contributor's page and use "Move or rewind this link…" in the Danger zone. It follows GitHub's steps for deleting a repository: a page of effects, "I have read and understand these effects", then the date and channel of the request and the contributor's ID typed exactly. The move is recorded in the event log. Or run, with an assignment ID (`a-…`) or a contributor ID (`c-…`):

```bash
.venv/bin/python manage.py create_invitation PUBLIC_ID
```

Each contributor has one link at a time: a new link revokes the earlier ones.

## Tests and translations

```bash
.venv/bin/python manage.py test
```

When interface strings change, update the catalogue and compile it (this needs GNU gettext):

```bash
.venv/bin/python manage.py makemessages -l zh_Hans --no-location -i "data/*"
```

```bash
.venv/bin/python manage.py compilemessages -l zh_Hans
```

## Stage 1 settings (M6)

Stage 1 is set by environment variables: `DEEPECON_STAGE=1`, `DEEPECON_SECRET_KEY`, `DEEPECON_ALLOWED_HOSTS`, `DEEPECON_SITE_BASE_URL`, and optionally `DEEPECON_DATA_DIR` and `DEEPECON_INVITATION_DAYS`. At Stage 1, debugging is off, cookies are secure, HTTPS is required, and `load_demo` is refused.

## Not yet built

- **M2:** the overview, the review screen, answers with the per-item AI disclosure, proposals, "Ask the team", autosave, confirmation, and export; each task's build date for the exposure log (Rule 10, D-044).
- **M3:** guidance, uploads, and the submission manifest.
- **M4:** the reviewed Chinese catalogue, the data quarantine, and the remaining §3 controls.
- **M5:** the demo paper.
- **M6:** the server.
