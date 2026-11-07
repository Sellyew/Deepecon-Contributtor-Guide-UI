# Contributor interface (implementation)

**Status: milestone M1 (skeleton) built on 2026-11-07**, after the research lead approved the [implementation plan](../../docs/architecture/mvp-implementation-plan.md) (D-043). The site runs with the fictional examples only. Next is M2, the Selection screens.

One Django application (Django 5.2, a long-term-support release) for the [MVP contributor interface](../../docs/architecture/mvp-contributor-interface.md). Pages are rendered on the server. It uses SQLite in WAL mode and private file storage, and loads nothing from other websites. It sends nothing to AI services: the model gateway refuses every call (D-042). It follows the [AI use and integrity rules](../../docs/architecture/llm-use-policy.md).

## What M1 contains

| Part | Where |
|---|---|
| Settings for both stages: Stage 0 (the demo computer, loopback only) and Stage 1 (a server, M6). All state lives in one data folder | `deepecon_site/settings.py` |
| Security headers (`default-src 'self'`, no referrer, no caching), log redaction of invitation tokens, and the model gateway that refuses every call | `deepecon_site/middleware.py`, `logging_filters.py`, `gateway.py` |
| Models: papers, rubric versions, items, item maps, candidate packages, the exposure log (Rule 10), and the event log | `papers/models.py` |
| Importers for the paper configuration, rubric, item map, and candidate package, each checked against the [schemas](../../schemas/contributor-interface/README.md) and [`validation/rubric_checks.py`](../../validation/rubric_checks.py) and refused if any check fails. Available as commands and as an administration page | `papers/importers.py`, `papers/management/commands/`, `papers/admin.py` |
| Invitations: random tokens stored only as SHA-256 hashes, with expiry and revocation. A link is shown once, never stored or logged | `contributors/models.py`, `contributors/admin.py`, `create_invitation` |
| Contributor pages: invitation landing, notice and consent (dated and changeable), "My paper", and the package download. Every page checks the assignment on the server | `contributors/views.py`, `templates/contributors/` |
| Interface languages: English and Simplified Chinese. The Chinese catalogue is **machine-drafted by Claude and awaits the team's review** (M4) | `locale/zh_Hans/LC_MESSAGES/django.po` |
| Demo loader: the fictional empirical and theory examples, synthetic packages, and three demo contributors | `contributors/management/commands/load_demo.py` |
| Tests: importers, invitations, consent, access to other papers, language switching, security headers, external assets, the gateway, network imports, and log redaction | `*/tests.py` |

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

The same imports are available on the team administration page (Papers, then "Import the team's files"). To invite someone, go to Assignments and use the action "Create an invitation link", or run:

```bash
.venv/bin/python manage.py create_invitation ASSIGNMENT_ID
```

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

- **M2:** the overview, the review screen, answers with the per-item AI disclosure, proposals, "Ask the team", autosave, confirmation, and export.
- **M3:** guidance, uploads, and the submission manifest.
- **M4:** the reviewed Chinese catalogue, the data quarantine, and the remaining §3 controls.
- **M5:** the demo paper.
- **M6:** the server.
