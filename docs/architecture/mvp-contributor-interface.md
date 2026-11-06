# MVP: Privacy-Preserving Contributor Interface

| | |
|---|---|
| **Status** | **Proposed** draft v0.4 (2026-11-06). v0.3 recorded the research lead's answers (D-025 to D-028) and proposed the layered item card (§4.2) and the map-and-panel review screen (§4.1). v0.4 corrects the translation scope: the **interface** is bilingual and extensible, and item text, papers, and code are not translated (D-030). It adds the rule that answer-key material never goes to any API provider (D-031), and makes proposals for the pilot's restricted data (O-034, §5.4) and the data-sharing check (O-035, §5.5). |
| **Requirements** | [Research lead's revision, 2026-11-06](../requirements/2026-11-06-research-lead-revision.md) (governs) · [team handover plan](../requirements/2026-11-05-team-handover-plan.md) · [example package V5 review](../requirements/2026-11-06-example-package-v5-review.md) |
| **Companion documents** | [Implementation plan](mvp-implementation-plan.md) · [contributor-interface schemas](../../schemas/contributor-interface/README.md) · [LLM use policy](llm-use-policy.md) |
| **Supersedes** | The decision brief, Options A and B, the interview protocol, the pilot plan, and the cost model (kept as records) |

---

## 1. What the first version does

Invited contributors (the paper's authors, or invited domain experts) use a small website whose interface is in English and Simplified Chinese, with more languages possible later. It has two functions.

1. **Selection.** The contributor opens their own paper and reviews the items the team prepared: the deliberate errors and removed steps that will become a benchmark task. For each item they keep it, keep it with changes, reject it, or mark it as unsure. They can comment and propose additional items.
2. **Guidance.** The contributor learns what to provide (a full runnable replication package and their original file names), how to prepare it, and how to submit it.

No step needs an AI model, and the site sends nothing to any AI provider (§7). The interface text is translated by the team, from an LLM draft reviewed by people (§6.3). Item text, papers, and code are shown in their original language and are not translated (D-030).

**Out of scope for v1.**
- Ruled out by the research lead on 2026-11-06: an AI interview; AI-generated errors or flawed packages; Claude Code or other client software; paper discovery; complex onboarding.
- Deferred: code execution on the site; grading of agent submissions; real-time collaboration; dashboards; e-mail sent from the site.

## 2. Decisions recorded on 2026-11-06

| ID | Decision (research lead) | Effect on the design |
|---|---|---|
| D-025 | V5's three groups and points are **one example**. Item categories and points differ by field; theory papers, for instance, may have derivation errors. | Categories are configured per paper, as a label, a one-line meaning, the rubric array that holds the items, and which item fields fill each display role. The team's rubric file is imported as it is, whatever its structure. |
| D-026 | Contributors provide their **original file names**, and the team does the mapping. | The checklist asks for original names. The team builds the map, and every location on the site is shown with the original name first. |
| D-027 | The team needs a **full runnable package**. | The guidance asks for a package a journal data editor would accept, with data or a route to run with data (§5). |
| D-028 | Contributors may download the **agent-facing package**. | It is a download on the paper page. |
| D-030 | The **interface** is bilingual (Chinese and English), with more languages possible later; interface text is translated with an LLM and reviewed by the team. (Clarifies an earlier misreading, D-029, that item text would be translated.) | Interface strings live in translation catalogues, and a language is added with a reviewed catalogue. Item text, papers, and code stay in their original language. |
| D-031 | **Answer-key material is never sent to any API provider**; any LLM processing of it happens only on a locally deployed model. | Applies to candidate items, rubrics, item maps, flawed code, guides, and contributor responses. See the [LLM use policy](llm-use-policy.md). |

## 3. The contributor's path

| Step | Screen | Content |
|---|---|---|
| 1 | **Invitation and notice** | A personal link from the team, a choice of language, and a short notice: what is stored, who can see it, that no AI service processes the contributor's material, how to withdraw, and a request to keep the items confidential (they are answer-key material). |
| 2 | **My paper** | The citation, the task version, and a download of the agent-facing package (D-028). |
| 3 | **Overview** | The purpose in one paragraph, and the statement that **the items are deliberate modifications made to build a benchmark task, not claims about the published paper**. One line per category, for example *conceptual error*, *missing analysis*, *technical error*, or *derivation error* for a theory paper. Planning targets, not quotas. An estimate of the time needed (about 2–3 minutes per item [U: to be measured]). |
| 4 | **Review** | The map and the item panel side by side (§4). |
| 5 | **Propose an addition** | Available throughout: category (or "not sure"), location, what would change, why it matters, and a suggested fix. |
| 6 | **Review and confirm** | All answers in the contributor's own words; confirming creates a numbered version, which they can revise until the team freezes the paper. |
| 7 | **Materials guidance** | The checklist for this paper, preparation steps, and the data routes (§5). |
| 8 | **Submit** | An upload with a SHA-256 receipt, a public reference, or another agreed channel, with the datasets declared (§5.3). |

## 4. The review screen

### 4.1 Whole picture and local change, on one screen (answers Q3)

```
┌───────────────────────── Paper: … · 6 of 15 reviewed · ● conceptual ● missing ● technical ─┐
│ MAP (whole picture)                     │ ITEM A · conceptual                    ◀ prev  next ▶ │
│                                         │ Comparison group admits units already treated        │
│ Data construction                       │ "The control group includes units treated before     │
│   code/build/registry_merge.do   ●T01   │  the window, which shrinks the main estimate."       │
│   code/build/panel.do            ●A  ◉  │                                                      │
│ Analysis                                │ Where   code/build/panel.do, lines 40–41             │
│   code/analysis/event.do         ●M1    │ Change  original                 modified            │
│ Results in the paper                    │         keep if first_treat>year keep if first_treat │
│   Table 2           ← A, T01            │                                  >= year - 2         │
│   Figure 3          ← M1, T01           │ Affects Table 2                                      │
│                                         │ ▸ What a correct answer must do                      │
│ [stages ▾] [results ▾] [matrix]         │ [ Keep ] [ Keep with changes ] [ Reject ] [ Unsure ] │
│                                         │ ▸ Reason · Comment · Other valid repairs · Ask team  │
└─────────────────────────────────────────┴──────────────────────────────────────────────────────┘
```
*(Fictional content.)*

- **The map** shows the paper's workflow in stages: data construction, analysis, and results. For a theory paper it shows the argument instead: assumptions, derivations, propositions, appendices. Each item is a coloured marker on the file or step it changes; filled once reviewed, outlined if not. The selected item is ringed.
- **The results column** lists the paper's tables and figures (or propositions). Next to each, the items that affect it. Selecting a result highlights those items on the map.
- **The item panel** shows the selected item's local change: the original and modified lines side by side, with the author's own file name and line numbers, the results it affects, and the controls. Moving to the next item moves the ring on the map, so the contributor always sees where they are.
- **A matrix toggle** gives the same information as a table of results × items, for contributors who prefer a grid.
- **On a phone** the map becomes a list grouped by stage, and an item opens full screen.
- **Paired variants:** where the team prepared both an *error* and a *missing* version of the same key point, the two markers are joined, and both appear side by side in the panel with equal weight.

The map comes from a file the team prepares for each paper (the [item map](../../schemas/contributor-interface/item-map.schema.json)). It lists the nodes (files or sections), their order, and, for each item, its anchors, the results it affects, the excerpt before and after, and a one-line summary. It is built from the master script, the authors' results map, and their original file names (D-026). It is expert-only material and is shown only to the assigned contributor.

### 4.2 The item card: show the decision first, the detail on request (answers Q1)

| Layer | Shown | Content |
|---|---|---|
| 1. Headline | Always | Title, category, and one plain-language sentence on what was changed and why it matters (written by the team) |
| 2. Local change | Always | Original and modified excerpt, side by side, with the author's own file name and line numbers (for theory papers, the original and modified passage with its equation or proposition number) |
| 3. Why it matters | Always | The results it affects (linked to the map) and the expected consequence in one line |
| 4. What a correct answer must do | One click | The team's description, the acceptable repair or work, and the critical requirements |
| 5. Scoring | Hidden by default | Points (as a weight), score tiers, and scoring rules; a category can show the weight if the team wants (`weight` role) |

**Interaction details proposed for a better experience:**
- **One-tap answers:** Keep, Keep with changes, Reject, Unsure. After Reject, optional reason chips appear: not realistic; not consequential; repair wrong; other.
- **Optional ticks** (realistic, consequential, repair correct) and short text fields, folded until needed.
- **"Ask the team"** on every item: a short question stored on the site, which the team answers in the admin page. The answer appears next time the contributor opens the item. There is no AI and no e-mail; the team can also reply by its usual channel.
- **Keyboard shortcuts:** arrow keys for previous and next; K, C, R, U for the four answers.
- **Interface language switch** (English / 中文, more later) on every page. Item text appears in its original language, and contributors may answer in either language; answers are stored as written.
- **Progress and time:** "6 of 15 reviewed, about 20 minutes left". The session resumes where the contributor left off, and "Unsure" counts as reviewed, so nobody feels forced to decide.
- **A download of their own review** (a PDF or Markdown summary) after confirmation, for their records. It carries the confidentiality notice.

## 5. Guidance: a full runnable package (answers Q4)

### 5.1 Can missing pieces without data make the package runnable?

**No.** Code and documentation without data let the team read and review the workflow, which is enough for the static agent task in V5. They do not let the team run it. The team's second verification round (team handover plan §3) needs the reference and modified versions run, so the team needs the data or a route to run with the data. Each dataset therefore follows one of four routes:

| Dataset | Route | What the team can then do |
|---|---|---|
| The author may share it | **Include it** in the upload. It is stored encrypted on the project server and accessible to the team only | Run everything |
| It is public elsewhere | **Give its source and version**; the team downloads it | Run everything |
| Restricted or confidential, such as administrative health or personnel records | **Never upload it.** Choose one of:<br>(a) the author or their RA runs the team's modified versions in the authorized environment and returns logs and outputs;<br>(b) the team applies to the provider for access;<br>(c) a secure environment where authorized team members run it;<br>(d) a fully synthetic substitute built from the codebook | With (a)–(c), run everything. With (d), check only that the code runs, not the results |
| Not yet decided | Record it as "to be decided" | The team follows up |

For the pilot paper, the public package's restricted data directories are empty (team handover plan §7), so route (a) or (b) will be needed (§5.4).

### 5.2 Checklist (configured per paper; default for empirical papers)

The guidance follows what journal data editors already ask for: the AEA/SSDE **Data and Code Availability Standard** and its **template README** [P-full/P-page, R8 §2.1]. Many authors will have prepared their package this way for publication. The checklist entries:

1. **README following the template README:** a data availability statement for each dataset, software and versions, expected run time, licences.
2. **Complete code** from raw inputs to every table and figure, with one master script that runs everything in order.
3. **Dependencies:** user-written packages included or pinned, with software versions.
4. **Data:** the data you may share, and for each dataset you may not, its source, terms, and the route from §5.1.
5. **A log of your own complete run**, with the outputs it produced, so the team can compare its run with yours.
6. **The results map:** which script produces each table and figure in the paper.
7. **Your original file names**, kept as they are (D-026). The team maps them to the task files.
8. Optional: known qualifications or limitations you want recorded.

If the public package already contains an entry, the contributor confirms it rather than resending it.

For a **theory paper** the default checklist is different: the LaTeX source of the paper and appendix, any code used to check derivations or compute examples, and the original file names. Both defaults are in the [examples](../../schemas/contributor-interface/examples/).

### 5.3 Preparation and submission
- **Prepare:**
  - keep the original folder structure and file names;
  - do not tidy the code;
  - use relative paths;
  - run the master script once from a clean copy and keep the log.
- **Submit:**
  - upload one ZIP; the upload is resumable and shows a SHA-256 receipt;
  - or give the public reference (DOI or URL and version) and upload only what is missing;
  - or use another channel agreed with the team (for very large packages, for example an institutional transfer).
- **Declare** each dataset's route, and confirm that nothing restricted or confidential is included. If any data are included, the contributor also confirms permission to share them with the project.

### 5.4 Proposal for the pilot paper's restricted data (O-034)

1. **First, read the package's data availability statement.** The public openICPSR package's README should say how each restricted dataset can be obtained and by whom. That decides how expensive route (b) is. *(Not read here.)*
2. **Start with route (a), the author runs.** Ask the authors whether they or a research assistant still have authorized access.
   - The team sends one **run kit**: the reference code and every confirmed modified version, applied to a copy of the original package, with a single script that runs them all in turn and collects the outputs.
   - The authors run it inside their authorized environment and return only logs and the aggregate tables and figures.
   - Before sending, they check the outputs against their data agreement's disclosure rules, for example small cells.
   - The authors already see the items as reviewers, so the run kit reveals nothing new to them.
3. **In parallel, build a fully synthetic stand-in (d)** from the codebook, with the same variable names, types, and panel structure. The team uses it to check that every modified version runs and produces its outputs before anything is sent to the authors. One round with the authors then usually suffices. The synthetic data never replace the real results.
4. **Fall back to route (b)**, applying for access, or (c), a secure environment, if the authors no longer have access or cannot run the kit.

### 5.5 What the data-sharing check means (O-035)

When a contributor includes data in an upload, the project then holds those data. The data's own licence or data-use agreement decides whether that is allowed:
- some sources allow redistribution to anyone, for example IPUMS extracts within its terms;
- others forbid passing data to third parties, for example PSID or WRDS (Compustat, CRSP) [P-full, R8];
- confidential administrative data usually need a formal agreement.

If an author uploads data that may not be shared with the project, by mistake or misunderstanding, the project would be in breach of the provider's terms. **The proposal:**
- **Quarantine.** Uploads that include data stay encrypted and unopened until a named team member, the **data steward**, has checked each dataset's declared terms against its source.
- **Clear.** A dataset that passes the check is released to the team.
- **Delete.** A dataset that fails is deleted. The contributor is told why and offered route (a).
- **Record.** Each check is logged with the dataset, its terms, and the decision.

## 6. Administrator functions (v1)

### 6.1 Configure a paper
- **Import the team's rubric file as it is.**
- **Configure categories** for the paper's field. For each category, give its label and its one-line meaning in both languages, which rubric array holds its items, which item fields fill each display role, and which roles contributors see. The V5 categories are one profile and a theory paper's another; both are in the [examples](../../schemas/contributor-interface/examples/).
- **Import the item map** (§4.1) and the original-file-name map (D-026).
- **Set the materials checklist** and the submission settings.

### 6.2 Run the review
- Create and revoke invitation links; the team delivers them through e-mail or WeChat.
- Follow progress and answer "Ask the team" questions.
- Export each contributor's review (JSON and a readable bilingual summary) and a list of suggested rubric changes.
- Receive submissions and verify their SHA-256.
- Freeze the paper's version; every action goes into an event log.

### 6.3 Interface languages (D-030)

All interface text (buttons, notices, the overview, category meanings, the guidance, and the checklist) is kept in translation catalogues, one per language.

1. **Draft.** The team drafts the Chinese catalogue with an LLM.
2. **Review.** A team member reviews and corrects it.
3. **Ship.** The reviewed catalogue is committed with the code.

Interface text contains no project material, so drafting it with any LLM leaks nothing. Per-paper interface text, such as a category's one-line meaning and the checklist entries, goes through the same draft-and-review step. Because these entries describe categories, not planted errors, they may be drafted with any model. **Item text is not translated.**

**Adding a language** means adding one catalogue and the per-paper labels, then reviewing both; no code changes.

## 7. Privacy and data-flow architecture

- **Default flows:**
  - the contributor's browser and the project server only;
  - no analytics, web fonts, content delivery networks, or embedded third-party content;
  - outbound traffic blocked.
- **Model modes:**
  - Mode 0, Off: the site itself uses no model in v1;
  - Mode 1, a local model, keeps data on project hardware;
  - Mode 2, an external API such as DeepSeek with the lead's key, sends data out of the project. It needs explicit configuration and is **never** used for answer-key material (D-031), contributor responses, or restricted data;
  - the team's own use of LLMs outside the site follows the [LLM use policy](llm-use-policy.md).
- **Data on the server.** Data are uploaded now (D-027), but only data the author may share. They go to the encrypted project server, never to any AI service, and are readable only by team members with the data role. Retention and deletion follow the contributor agreement and the data's terms. Restricted and confidential data are never uploaded (§5.1).
- **Storage tiers:**
  - agent-facing (the candidate package);
  - expert-only (rubric, item map);
  - researchers-only (pilot reports; never shown to contributors);
  - contributor-submitted (packages, answers, messages).
- **Access controls:**
  - invitation credentials are random, time-limited, revocable, stored hashed, and never logged;
  - every request is authorized on the server;
  - logs record actions and IDs, never text or file contents.

## 8. Data model (draft 0.2.0)

Five JSON Schemas in [`schemas/contributor-interface/`](../../schemas/contributor-interface/README.md), with fictional empirical and theory examples and 16 tests. The team's real V5 rubric imports through the generic path, and its scoring fields never reach the contributor view (checked 2026-11-06; only pass/fail was printed).

| Schema | Holds |
|---|---|
| Rubric import | The team's own rubric file, preserved as it is |
| Paper configuration | Field, citation, categories (field roles and visible roles), localized interface text (category labels and meanings, checklist), languages, original-file-name map, checklist, submission settings |
| Item map | Workflow or argument nodes and edges; per item: anchors, affected results, original and modified excerpts, summary, consequence, pairing |
| Contributor review | Answers per item, proposals, "Ask the team" messages, confirmations |
| Submission manifest | Channel, files and hashes, package information (master script, README, software, run log, expected outputs, run time), datasets with their availability and route, declarations |

## 9. Implementation

See the [implementation plan](mvp-implementation-plan.md) v0.2:
- one Django application, server-rendered, with SQLite and encrypted storage;
- the map and item panel rendered on the server with plain HTML and CSS;
- resumable uploads for multi-gigabyte packages;
- about 6–9.5 engineer-weeks for one developer [U: planning estimate].

## 10. Open questions

| ID | Question | Proposed default |
|---|---|---|
| O-027 | Does the layered card (§4.2) suit contributors? | Pilot it with the first paper's two experts |
| O-029 | Does the map with the item panel (§4.1) suit contributors? | Pilot it, with the matrix toggle as the alternative |
| O-034 | Which route the pilot paper's restricted data take | §5.4: read the data availability statement; route (a) with a run kit, checked first on a synthetic stand-in; fall back to (b) or (c) |
| O-035 | Who checks that data included in an upload may be shared with the project? | §5.5: a named data steward, with uploads quarantined until checked |
| O-021, O-022, O-025, O-026 | Hosting; invitation delivery; what may be sent at evaluation time; confidentiality agreement | Unchanged |
