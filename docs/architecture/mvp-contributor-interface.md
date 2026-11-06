# MVP: Privacy-Preserving Contributor Interface

| | |
|---|---|
| **Status** | **Proposed** draft v0.2 (2026-11-06). v0.2 rebuilds the workflow, data model, and guidance from the [example contribution package V5](../requirements/2026-11-06-example-package-v5-review.md) (D-023). Six questions for the research lead (§9) may still change details. |
| **Requirements** | [Research lead's revision, 2026-11-06](../requirements/2026-11-06-research-lead-revision.md) (governs) · [team handover plan, 2026-11-05](../requirements/2026-11-05-team-handover-plan.md) · [example package V5 review](../requirements/2026-11-06-example-package-v5-review.md) · [original brief](../requirements/2026-11-05-research-lead-brief.md) |
| **Companion documents** | [Implementation plan](mvp-implementation-plan.md) · [contributor-interface schemas](../../schemas/contributor-interface/README.md) |
| **Supersedes** | The decision brief, Options A and B, the interview protocol, the pilot plan, and the cost model (kept as records) |

---

## 1. What the first version does

Invited contributors (the paper's authors, or invited domain experts) use a small bilingual website, in English and Simplified Chinese, for two things.

1. **Selection.** The contributor opens their own paper, already configured, and reviews the **candidate items the team prepared**. In the V5 package these are the 15 rubric items of a benchmark task. For each item the contributor says whether to keep it as is, keep it with changes, reject it, or mark it as unsure, with optional reasons and comments. They may also propose additional items.
2. **Guidance.** The contributor reads which materials the team needs from them, how to prepare them, and how to submit them, and then uploads them or records where they already are.

No step needs an AI model. The site runs on infrastructure the project controls, and by default it sends nothing to any AI provider (§6).

**Out of scope for v1.**
- Decided by the research lead on 2026-11-06:
  - an AI interview;
  - AI-generated errors or flawed packages;
  - Claude Code or any client software for contributors;
  - paper discovery;
  - onboarding beyond a short notice.
- Deferred, as in the team's plan:
  - code execution;
  - grading of agent submissions;
  - an online review platform;
  - real-time collaboration;
  - dashboards;
  - e-mail from the site.

## 2. What the example package settled

From the [structural review](../requirements/2026-11-06-example-package-v5-review.md):

| Finding | Consequence for the interface |
|---|---|
| A finished contribution is a **static code-review task**. The agent receives a short neutral abstract, a 43-file Stata workflow, a codebook, and instructions, and submits an audit plus revised code. | Contributors review the planted items. For tasks like this, the materials they supply are **code and documentation, not data**. |
| The prepared candidates are **15 rubric items in three groups** with fixed points: *conceptual* (学理, 5 × 8), *missing* (补全, 3 × 14), and *technical* (技术, 7 items of 2–3 points), totalling 100. | The Selection screen shows items grouped this way. The team's `Rubric.json` format is imported as it is (P-041). |
| Materials sit in **separate tiers**: agent-facing (the candidate ZIP), expert-only (rubric, guides, checks), and researchers-only (the pilot report). Each part carries a SHA-256 manifest. | The site keeps these tiers apart and adds a fourth, contributor-submitted materials (P-043). Contributors see expert-only fields only for their own paper, and only the fields the configuration allows. |
| Versions are explicit (V4 → V5, with file mappings, patches, and frozen hashes). | Every review records the rubric version and candidate version the contributor saw. |
| The agent-facing presentation is **restructured**, with neutral titles and file names. | Locations shown to authors may need their original file names (Q2). |
| The package contains no patient-level data, and Stata was not executed. | Restricted microdata are never needed for static-review tasks and are never uploaded. |

## 3. The contributor's path

| Step | Screen | Content |
|---|---|---|
| 1 | **Invitation and notice** | The contributor opens a personal invitation link (sent by the team through e-mail or WeChat) and chooses English or 中文. A short notice says what is stored, who can see it, that no AI service processes it, and how to withdraw. It also asks the contributor to keep the items confidential, because they are answer-key material. The contributor accepts. |
| 2 | **My paper** | The contributor's paper (full citation) and the task version, for example "V5", already configured. Usually there is one; there is no search. |
| 3 | **Overview** | One paragraph on the purpose. A plain statement that **the items are deliberate modifications made to build a benchmark task, not claims that the published paper contains these problems**. One line on each group:<br>• *conceptual*: an economic-analysis error planted in the code;<br>• *missing*: a necessary analysis removed, which a careful researcher should add;<br>• *technical*: a code-level error.<br>The planned number of items per group, shown as targets rather than quotas. A list of all items with their status: not reviewed, kept, kept with changes, rejected, unsure. |
| 4 | **Item review**, about five items per screen | Each card shows, by default:<br>• the item's ID, group, and title;<br>• **where** it is: files, with the author's original file names when a mapping is configured (Q2);<br>• **what was changed and what a correct answer must do**: for *conceptual*, the criterion; for *missing*, the available evidence and boundary plus the acceptable work; for *technical*, the repair;<br>• the critical requirements.<br>By default the card does **not** show points, score tiers, the scoring method, evidence-record rules, or historical weights (Q1).<br>**The contributor answers:** keep as is / keep with changes / reject / unsure. Optional ticks: a realistic mistake; consequential for the paper's conclusions; the stated repair or acceptable work is correct. Optional text: suggested wording, other valid repairs, comment. A rejection asks for a short reason (not realistic, not consequential, repair or acceptable work wrong, other), but the reason is not required.<br>Where the team prepared both an *error* and a *missing* version of the same key point (as in the team's plan), both appear side by side with equal weight and no preselection.<br>The contributor can move between screens, revisit items, and reorder. |
| 5 | **Propose an addition** (optional, available throughout) | Group (or "not sure"), location, what would be changed, why it matters, and a suggested repair. It is stored as contributor-originated and does not replace any prepared item. |
| 6 | **Review and confirm** | A summary of every answer, in the contributor's own words. The contributor confirms. Each confirmation creates a numbered version, and they can return and revise until the team freezes the paper's version. |
| 7 | **Materials guidance** | The checklist configured for this paper, with preparation steps and the rules on data (§4). |
| 8 | **Submit** | Either upload one ZIP, with a SHA-256 receipt shown on screen, or give the public reference (DOI or repository URL and version) of a package the team should use, plus uploads of any missing pieces. The page then shows receipt status. |

**Interaction rules** from the team's plan:
- one column, one main action per screen;
- autosave that reports success or failure explicitly, and recovery after a refresh;
- "reject" and "unsure" are as easy as "keep", nobody is asked to fill a quota, and stopping early is fine;
- the site works with a keyboard and on laptops; on phones it supports reading and simple choices.

## 4. Guidance: what contributors provide

**Default checklist for static-review tasks**, derived from the V5 candidate package. The administrator marks each entry as required, optional, or not needed for each paper. If the team already holds the public replication package, most entries become "confirm or fill gaps" (Q4).

| # | Material | Why the team needs it | V5 counterpart |
|---|---|---|---|
| 1 | **Complete analysis code**, from raw inputs to every table and figure, with the master script and the run order | The task is built from the real workflow | `00_run_all.do` and the 43-file workflow |
| 2 | **Dependencies:** user-written commands (ado files) or their exact names and versions, plus the software version | Static review needs to know what each command does | `01_dependencies.do` |
| 3 | **Variable dictionary:** each variable's name, definition, unit, source, and construction, plus sample restrictions | Reviewers judge measurement and sample choices from it | `study_dictionary.txt` |
| 4 | **Documentation of custom programs:** inputs, outputs, and assumptions | Reviewers can judge a program without running it | `command_contracts.txt` |
| 5 | **Results map:** which script produces each table and figure in the paper | Connects the code to the paper's claims | Table and chart scripts; file index |
| 6 | **Known qualifications and limitations** the authors want recorded (optional) | Keeps genuine limitations apart from planted items | The analysis and qualification notes |
| 7 | **Confirmation of the short research background** the team drafts for agents, that it is accurate and gives nothing away (optional) | Agents see only this abstract | `article.txt` (255 words) |

**Preparation steps** shown on the page:
1. Keep your original file names and folder structure. Do not tidy or rewrite the code; the team needs the workflow as it is.
2. Use plain-text formats: `.do`, `.ado`, `.R`, `.py`, `.txt`, `.md`, or `.csv` for dictionaries, in UTF-8.
3. Add a short README listing what is included and anything missing.
4. Put everything in one ZIP file. Code and documentation are usually small; the whole V5 candidate package is about 117 KB.

**Data rules** shown on the page:
- **Do not include data.** This applies to raw or restricted data and to any file derived from them (P-027). It covers patient-level and personnel records and anything covered by a data-use agreement.
- **Describe the data instead,** in the dictionary: source, access conditions, and coverage.
- The upload screen repeats this rule and asks the contributor to confirm it before uploading.

**Submission:** upload on the site, or give the public reference (DOI or URL and version) plus uploads of the missing pieces. If a contributor cannot upload, the team arranges another channel and records it.

## 5. Administrator functions (v1)

- **Configure:**
  - **Import the team's rubric file** (`Rubric.json`, in the V5 format) as the source of the items.
  - **Paper configuration:** citation, task version, candidate-package hash, group targets, which item fields contributors see, optional Chinese display text for items, an optional mapping from original to candidate file names, and the materials checklist.
  - **Contributors and assignments.**
- **Optionally attach the agent-facing candidate ZIP**, so that contributors can see exactly what an agent sees (Q5).
- **Invite:** create and revoke invitation links. The team delivers them through e-mail or WeChat; the site sends no e-mail.
- **Follow up:** progress per contributor and per item.
- **Export:**
  - the contributor's review as JSON;
  - a readable bilingual summary;
  - a list of suggested rubric changes against the imported version, which the team applies offline to produce the next rubric version.
- **Receive submissions:** verify SHA-256 hashes and record receipt.
- **Freeze** a paper's review version, and keep an event log.

## 6. Privacy and data-flow architecture

### 6.1 Principle
Research data, replication code, paper materials, contributor responses, and intermediate outputs are never sent to Anthropic or any other third-party AI service (D-018). The site works completely without any model.

### 6.2 Data flows in the default configuration

| Flow | What travels | Between |
|---|---|---|
| Contributor ↔ site | Pages; the assigned paper's items, in the configured fields; the contributor's answers and uploads | The contributor's browser and the project server only, over TLS |
| Administrator ↔ site | Configuration, imports, exports | The team and the project server, over TLS; optionally limited to the team's network or a VPN |
| Invitations | The link only | The team's existing e-mail or WeChat channel |
| Backups | Encrypted copies | Project-controlled storage |
| **Anything else** | **Nothing** | No analytics, error-tracking service, content delivery network, web fonts, or embedded third-party content. Every asset is served by the project server, and outbound network access from the server is blocked by default |

### 6.3 Model integration: three modes

| Mode | Meaning | Where the data go | Default |
|---|---|---|---|
| **0: Off** | No model calls; every feature works | Nowhere | **On** (v1 implements only this mode) |
| **1: Local model** | A model on hardware the project controls | Stays inside project infrastructure | Off |
| **2: External API** | A provider's hosted API, for example the DeepSeek API with the research lead's key | **Leaves the project** and is processed under the provider's terms | Off; needs explicit configuration **and** a per-material permission |

**Using a DeepSeek API key is Mode 2, not Mode 1.** v1 ships a single gateway module that refuses every call; Modes 1 and 2 are added only when the research lead asks. Even then:
- expert-only material, contributor responses, and restricted material are never eligible for Mode 2 (P-035);
- every call is logged as metadata only;
- the server's firewall allows only the configured endpoint;
- machine translation counts as a model call.

### 6.4 Storage tiers and access

| Tier | Example (V5) | Who can see it on the site |
|---|---|---|
| **Agent-facing** | The candidate ZIP | The administrator; the assigned contributor, if configured (Q5) |
| **Expert-only** | The rubric and guides | The administrator; the assigned contributor sees only the configured item fields for their own paper |
| **Researchers-only** | Pilot reports, model results | The administrator only; never imported into contributor views |
| **Contributor-submitted** | Uploaded ZIPs, answers | The administrator and the contributor who submitted it |

**Access and handling rules:**
- **Invitation credentials** are random (at least 128 bits), time-limited, and revocable; they are stored hashed and never logged.
- **Every request is authorized on the server**: pages, the API, files, and exports.
- **Files are private:** stored outside the web root on an encrypted disk, and downloaded only through authorized, short-lived links.
- **Logs** record actions and object IDs, never contributor text or file contents.
- **Withdrawal** deletes the contributor's material; a retention period is set before launch.
- **Agent-facing exports** never include expert-only fields.

## 7. Data model (draft)

Defined as JSON Schemas in [`schemas/contributor-interface/`](../../schemas/contributor-interface/README.md), with synthetic examples and tests.

| Object | Purpose | Key fields |
|---|---|---|
| **Paper configuration** | One configured paper and task version | paper_id, citation, replication-package reference, task_version, rubric_version, candidate_version, candidate-package SHA-256, group targets, visible item fields, optional item translations, optional file-name map, materials checklist |
| **Rubric import** | The team's `Rubric.json`, imported as it is | version, maximum, the arrays `conceptual`, `missing`, and `technical` (each item has id, points, and title, plus group-specific description fields). All other fields are preserved untouched and hidden from contributors unless configured |
| **Contributor review** (export) | One contributor's answers | assignment, relationship to the paper (author or invited expert), language, rubric and candidate versions, one review per item (verdict, checks, reason, suggested wording, other valid repairs, comment), proposals, confirmations (numbered versions with timestamps and hashes) |
| **Submission manifest** | What the contributor provided | channel (upload, public reference, or another agreed channel), files with sizes and SHA-256 (the package's own convention), checklist entries covered, a declaration that no data are included, receipt and verification |

Internal fields such as tiers, scoring methods, and historical weights stay with the team's grading workflow. The site preserves them so that an export can be traced back to the exact rubric version.

## 8. Implementation

See the [implementation plan](mvp-implementation-plan.md) (Proposed draft). In brief:
- **Stack:** one Django application with server-rendered pages, SQLite, encrypted local storage, the built-in administration interface, and English and Chinese message catalogues.
- **Defaults:** no external assets, and outbound traffic blocked.
- **Milestones:** five, beginning with synthetic data and ending with the V5 paper as the first real configuration.
- **Effort:** about 4–7 engineer-weeks for one developer [U: planning estimate].

## 9. Questions for the research lead

| # | Question | Proposed default |
|---|---|---|
| Q1 | Which item fields do contributors see? | Title, location, the description (criterion; evidence boundary and acceptable work; repair), and critical requirements. Not shown: points, tiers, scoring method, evidence-record rules |
| Q2 | Should locations use the author's **original** file names? That needs a mapping from the original package to the candidate files, like `Mapping_From_V4.json` but from the original package | Yes, if the team can produce the mapping; otherwise show the candidate file names with a note |
| Q3 | Do contributors review the **three rubric groups** (as in V5) or **key points with paired error and missing variants** (as in the team's plan)? | The three groups, showing paired variants only where the team prepared both |
| Q4 | What must authors provide when their replication package is already public (as on openICPSR)? | Confirm the public package and supply only what is missing (dictionary, custom-program notes, results map); no data |
| Q5 | Should contributors see the **agent-facing candidate package**, so they can judge whether each item is discoverable from what an agent sees? | Yes, as an optional download for the assigned contributor |
| Q6 | The rubric items are written in English. Who provides Chinese display text for Chinese-speaking contributors? | The team, by hand; no machine translation by default |

Earlier open questions still apply: hosting and operator (O-021), invitation delivery and a second factor (O-022), model use (O-023), evaluation-phase exposure (O-025), confidentiality (O-026), release policy (O-001), credit (O-005), ethics (O-013), the name (O-014), and who operates and funds the site after the initial period (O-020).

## 10. Points for the research lead

1. **Framing for authors.** The overview and every card say that the items are deliberate modifications made to build a benchmark task, not claims about the published paper (P-037).
2. **Easy agreement.** "Reject" and "unsure" are as easy as "keep", nothing is preselected, and the reasons and ticks are optional but visible. Acceptance and rejection rates are reported per paper (P-038).
3. **Grader agreement (methodology).** V5 grades a static audit against coarse rubric tiers, so whether two independent graders agree matters more than any interface choice. The rubric checks are labelled consistency-only. Measuring agreement between two independent graders on the eight pilot submissions would show whether the tiers are reproducible. The rubric's `calibration_status` field may already address this; I did not read it.
4. **The evaluation phase.** Evaluating a closed model sends the agent-facing package to its provider. The V5 README already keeps expert materials out of agent sessions. The same rule should decide what may ever be sent to a provider (O-025).
5. **This design work.** I inspected the V5 expert folder and report only at the level of structure, for the reason the package's own README gives (see the [review](../requirements/2026-11-06-example-package-v5-review.md)). Tell me if you want me to read particular fields' contents.
