# Contributor interface (implementation)

**Status: milestone M3 (Guidance and submission) built on 2026-11-26**, after M1 (skeleton, 2026-11-07) and M2 (Selection, 2026-11-26). The research lead approved the [implementation plan](../../docs/architecture/mvp-implementation-plan.md) (D-043), started M2 with D-049 and M3 with D-050. The site runs with the fictional examples only. Next is M4: the reviewed Chinese catalogue, the data steward's check of uploaded data, and the remaining privacy controls.

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
| Demo loader: the fictional empirical (scored) and theory (demo) examples, synthetic packages, and three demo contributors: two authors whose link opens their paper, and an invited expert, assigned the scored example, who chooses between it and the demo paper, the only one open to all | `contributors/management/commands/load_demo.py` |
| Exposure log (Rule 10): entries are added and viewed, never edited or deleted; the recorder's name comes from the account, and an evaluation run needs the pinned model version and its release date | `papers/models.py`, `papers/admin.py` |
| Tests: importers, links and revocation, choosing and changing paper, consent, access to other papers, admin permissions, language switching, the link migration, security headers, external assets, private storage, the gateway, network imports, and log redaction | `*/tests.py` |

## What M2 adds

| Part | Where |
|---|---|
| Answers, proposals, questions, and confirmations. Each answer has an optimistic version, so a page that is out of date (another tab saved since) is told so and never overwrites. The per-answer AI disclosure (D-039) records the tool, the type of account, and whether the items or package were entered | `contributors/models.py` (`ItemReview`, `Proposal`, `Question`, `Confirmation`) |
| The Selection rules in one place: what the contributor may see of each item (only the roles the paper configuration marks visible), saving with conflicts, numbered confirmations holding the SHA-256 of what was confirmed, the review export (validated against `contributor-review.schema.json` before it is returned), and the checks before freezing | `contributors/review.py` |
| Overview ("My paper"): what we ask, the paper's categories, progress with an estimate of the time left, and the ways to start, continue, propose, confirm, and ask the team | `contributors/views.py`, `templates/contributors/my_paper.html` |
| Review screen: the whole-picture map with a coloured marker per item (filled once answered; selecting a result highlights the items that affect it, shown only where the paper configuration makes that visible), one item at a time with the original and modified change side by side, the four answers (Keep, Keep with changes, Reject, Unsure), the main reason for a rejection, the three ticks, suggested wording, and the AI disclosure. Paired versions of one key point appear side by side in rubric order on both items' pages, and the choice between them is one answer for the pair. An answer other than Reject moves to the next item; after the last, to the confirmation page. A matrix view shows which items affect which results | `contributors/selection_views.py`, `templates/contributors/review_item.html`, `review_matrix.html` |
| Everything works as plain form posts. `review.js` (from the site's own files, as the security policy requires) adds autosave and keyboard shortcuts: ← and → move between items; K, C, R, and U answer | `static/review.js` |
| Proposals of new items (any configured category, or "Not sure"), questions to the team (general or about one item, answered on the team pages), confirmation of a numbered version, and a Markdown copy of the contributor's own review | `selection_views.py`, `templates/contributors/propose.html`, `confirm.html` |
| Team pages: each paper's build date (needed by the exposure log, Rule 10) and team owner; reviews with progress; freezing (refused if the paper has no build date, an item lacks provenance, or the answers do not match a version the contributor confirmed (D-050); warns about unanswered items), unfreezing, and the JSON export; the question queue with the waiting time and owner; withdrawal at a contributor's request | `papers/admin.py`, `contributors/admin.py` |
| `check_papers` re-runs today's import checks on every stored paper and fails if one has a problem; `make_tripwire` writes the unpublished tripwire GUID to the data folder (mode 0600) and prints only its path ([canary rules](../../docs/methodology/canary.md)) | `papers/management/commands/` |
| Chinese interface strings for M2, **machine-drafted by Claude and awaiting the team's review** | `locale/zh_Hans/LC_MESSAGES/django.po` |
| Tests for the Selection rules, the export, freezing, the admin actions, `check_papers`, `make_tripwire`, and the contributor screens in both languages | `contributors/test_selection.py`, `papers/tests.py` |

## What M3 adds

| Part | Where |
|---|---|
| Guidance page per paper: the checklist configured for the paper (with the public package, if there is one, named so that the contributor confirms what it already holds), how to prepare the package, the four data routes, how to send it, and the rules for using AI tools (MVP §5) | `submissions/views.py`, `templates/submissions/guidance.html` |
| Submit page: how the materials reach the team (upload, public reference, or another agreed channel, as the paper allows), the package (master script, README, software, run log, outputs, run time), one row per dataset with its availability and, for restricted or confidential data, the route by which the team can still run the code, the checklist coverage, and two declarations. Saving keeps a draft; submitting creates a numbered version holding the manifest and its SHA-256, after checking what is still missing | `submissions/forms.py`, `manifest.py`, `templates/submissions/submit.html` |
| Uploads: ZIP archives sent in 8 MiB chunks that resume where they stopped (choose the same file again), up to 20 GiB unless the paper says otherwise. The receipt is the file's SHA-256, which the contributor can compare with their own copy. Archives are stored in private storage under generated names (mode 0600); only their list of file names and sizes is read, and nothing is extracted or run. Without JavaScript the form posts the whole file | `submissions/storage.py`, `static/upload.js` |
| Team pages: submissions with their datasets and checklist, uploads (size, SHA-256, and the list of names and sizes; no download until the data steward's check in M4), and submitted versions with the receipt and verification actions and the manifest export (validated against `submission-manifest.schema.json` 0.3.0). The team neither edits nor deletes contributors' submissions; withdrawal deletes them, uploaded files included | `submissions/admin.py`, `contributors/admin.py` |
| Chinese interface strings for M3, **machine-drafted by Claude and awaiting the team's review** (the rules for using AI tools follow the reviewed-draft text in MVP §5.6) | `locale/zh_Hans/LC_MESSAGES/django.po` |
| Tests for guidance, chunked and resumed uploads, refusals, access by other contributors and papers, submissions by every channel, dataset routes, the theory paper, the manifest export, and withdrawal | `submissions/tests.py` |

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

The same imports are available on the team administration page (Papers, then "Import the team's files"). To offer a demo or development paper to every invited contributor, open the paper and tick "open to all contributors". Scored papers cannot be opened to all: offer them by creating assignments (D-047). Unticking it stops new choices only: contributors who already chose the paper keep it, and their work (D-045). An assignment with no answers, proposals, questions, or confirmations can still be deleted (Assignments, filtered by the paper and "Chosen by the contributor"); one with work cannot be deleted, so a contributor's work is never lost as a side effect.

To invite someone, create the link from an assignment (Assignments, action "Create a personal link, opening this paper unless the contributor has chosen one"), or from a contributor (Contributors, action "Create the personal link"), which opens their current paper, or the list of papers offered to them if they have none. To re-issue a link, use the contributor row: a paper the contributor chose stays theirs.

If a contributor asks the team to move their link (to another paper offered to them, or back to the list of papers), open the contributor's page and use "Move or rewind this link…" in the Danger zone. It follows GitHub's steps for deleting a repository: a page of effects, "I have read and understand these effects", then the date and channel of the request and the contributor's ID typed exactly. The move is recorded in the event log. Or run, with an assignment ID (`a-…`) or a contributor ID (`c-…`):

```bash
.venv/bin/python manage.py create_invitation PUBLIC_ID
```

Each contributor has one link at a time: a new link revokes the earlier ones.

## Check, freeze, and export reviews

Before an evaluation run, and after the rules change, re-check every stored paper:

```bash
.venv/bin/python manage.py check_papers
```

Set each paper's build date and team owner on its admin page. When a contributor has finished, freeze the review (Assignments, action "Freeze the selected reviews"); the contributor can then read it but not change it. Freezing is refused without a build date, with items lacking provenance, or when the answers do not match a version the contributor confirmed (D-050: ask them to confirm again); it warns when items are unanswered. The event log records the hash of what was frozen and the confirmed version it matches. Export it as JSON with the action "Export the selected review as JSON", which needs the permission to view answers, proposals, questions, confirmations, and consent. Contributors' answers, proposals, questions, confirmations, and consent cannot be edited or deleted on the team pages. Questions from contributors wait in Questions, unanswered first, then oldest first; answer them there.

If a contributor asks to withdraw from a paper, open the assignment and use "Withdraw…" in its Danger zone (it needs the permission to delete assignments). After the same confirmation steps as moving a link, it deletes their answers, proposals, questions with the team's answers, confirmed versions, and consent on that paper, and the assignment itself, as the notice promises. The event log records who did it, the date and channel of the request, and how many records were deleted, not their content. Nothing else on the team pages deletes a contributor's work.

Answers belong to the rubric version they were given on. After the team imports a new rubric version, its items are reviewed afresh: the review screen shows the contributor's answer to the earlier version as a note, and the export holds only answers to the current version.

Create the unpublished tripwire GUID once per installation. It is written to the data folder and never printed; never paste it into any AI service, this session included. Replacing it (`--replace`) keeps the old one, renamed, for leak probes:

```bash
.venv/bin/python manage.py make_tripwire
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

- **M4:** the reviewed Chinese catalogue, the data steward's check before anyone opens uploaded data (and the team's download after it), and the remaining §3 controls.
- **M5:** the demo paper.
- **M6:** the server.
