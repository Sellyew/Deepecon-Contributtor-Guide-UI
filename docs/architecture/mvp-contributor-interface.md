# MVP: Privacy-Preserving Contributor Interface

| | |
|---|---|
| **Status** | **Proposed** draft v0.6 (2026-11-07). v0.3 recorded the research lead's answers (D-025 to D-028) and proposed the layered item card (§4.2) and the map-and-panel review screen (§4.1). v0.4 corrects the translation scope: the **interface** is bilingual and extensible, and item text, papers, and code are not translated (D-030). It adds the rule that answer-key material never goes to any API provider (D-031), and makes proposals for the pilot's restricted data (O-034, §5.4) and the data-sharing check (O-035, §5.5). **v0.5** records the task tiers (D-032), which narrow D-031 to held-out tasks while D-018 stays unchanged; records that the pilot paper is a demo with no contact with its authors (D-024, clarified), so §5.4 becomes the general route for contributors' restricted data; and proposes staged hosting: the demo on a team member's computer, then one small server before the first outside contributor (§9, P-053). **v0.6** (2026-11-07) records that no local model will be deployed (D-033); proposes that contributors may use AI tools if what they submit is their own judgment in their own words (§5.6, P-055); and defers the D-032 clarification until the construction process is revised (O-037). |
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
- Ruled out by the research lead on 2026-11-06: an AI interview; AI generation of errors or flawed packages on the site (whether the team may use LLMs in its own preparation of candidates, outside the site, is proposal P-054); Claude Code or other client software; paper discovery; complex onboarding.
- Deferred: code execution on the site; grading of agent submissions; real-time collaboration; dashboards; e-mail sent from the site.

## 2. Decisions recorded on 2026-11-06

| ID | Decision (research lead) | Effect on the design |
|---|---|---|
| D-025 | V5's three groups and points are **one example**. Item categories and points differ by field; theory papers, for instance, may have derivation errors. | Categories are configured per paper, as a label, a one-line meaning, the rubric array that holds the items, and which item fields fill each display role. The team's rubric file is imported as it is, whatever its structure. |
| D-026 | Contributors provide their **original file names**, and the team does the mapping. | The checklist asks for original names. The team builds the map, and every location on the site is shown with the original name first. |
| D-027 | The team needs a **full runnable package**. | The guidance asks for a package a journal data editor would accept, with data or a route to run with data (§5). |
| D-028 | Contributors may download the **agent-facing package**. | It is a download on the paper page. |
| D-030 | The **interface** is bilingual (Chinese and English), with more languages possible later; interface text is translated with an LLM and reviewed by the team. (Clarifies an earlier misreading, D-029, that item text would be translated.) | Interface strings live in translation catalogues, and a language is added with a reviewed catalogue. Item text, papers, and code stay in their original language. |
| D-031 | **Answer-key material is never sent to any API provider**; any LLM processing of it happens only on a locally deployed model. Narrowed by D-032 to held-out tasks. | Held-out answer keys and graders go to no model (since D-033, no local model exists); a held-out agent-facing package reaches a closed model only in a logged evaluation run under a no-retention agreement (D-032); other answer-key material follows D-018 (no external AI unless the lead configures it). See the [LLM use policy](llm-use-policy.md). |
| D-032 | **Task tiers:** development tasks (V5 is one) may be published with a canary; evaluation tasks keep answer keys unpublished; a few held-out tasks keep their answer keys and graders on project hardware, and closed models see only their agent-facing package, under a no-retention agreement (clarification deferred, O-037). Each task records when its material first reached a provider or the public. D-018 is unchanged. | The site records each paper's tier, visible to administrators only. Every contributor is asked to keep the items confidential (§3 step 1, O-026); this is essential for evaluation and held-out tasks. |
| D-024 (clarified) | The pilot paper is a **demo** for building and testing the interface; the team has no contact with its authors. | The demo paper is configured for dry runs by team members. It needs no data, because the site runs no code (§5.4). |
| D-033 | **No locally deployed model** (2026-11-07). | Gateway Mode 1 is not planned; held-out answer keys and graders are processed by no model; whether open-weight models may still be run as evaluated systems is open (O-037); contributors' own AI use is proposal P-055 (§5.6). |

## 3. The contributor's path

| Step | Screen | Content |
|---|---|---|
| 1 | **Invitation and notice** | A personal link from the team, a choice of language, and a short notice: what is stored, who can see it, that the site sends nothing to any AI service; that the finished task, built from their package, will be used to evaluate AI models and may later be published (D-032), while their reviews, comments, and messages are not published; how to withdraw; and a request to keep the items confidential (they are answer-key material), with the rules for using AI tools (§5.6). |
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

For the demo paper, the public package's restricted data directories are empty (team handover plan §7) and the team has no contact with its authors, so the interface demo uses no data; a synthetic stand-in to rehearse the run kit (§5.4) is optional team work outside the engineering estimate.

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

### 5.4 Restricted data in contributed papers: the run kit (P-049)

Contributors are usually the paper's authors. If they or their research assistant still have authorized access to the data [U: depends on each data agreement], the run kit lets the team obtain real results without receiving any restricted data. *(O-034 asked this for the pilot paper; it was closed because that paper is a demo, D-024.)*

1. **First, read the package's data availability statement, and ask the contributor for the data editor's report if their journal produced one.** Some inputs may turn out to be public, or aggregate derived files may be shareable; the team then runs most versions itself. The report also says whether the original results were ever reproduced: for restricted data, the AEA Data Editor sometimes only inspects the code [P-full, R8 §2.4].
2. **Build the run kit** after Selection, so that it contains only the items the contributor confirmed. It is code only:
   ```
   runkit_<paper>/
     README_EN.txt, README_ZH.txt   what it does, time needed, what to send back
     settings.do                    the only file to edit: the path to the data
     run_all.do                     runs each version in its own copy, writes results/
     versions/ref/                  the original code, changed only in its data path
                                    and neutralized display commands (recorded as a diff)
     versions/combined/             all confirmed items applied together
     versions/item_<id>/            one confirmed item each, applied alone
     check_outputs.do               lists every output and flags the small cells it can
                                    detect (an aid, not a guarantee)
   ```
   - Each item runs **alone**, as well as in the combined package, because the candidate package mixes all items and only separate runs show each item's effect.
   - The data are **built once**; each version reruns only from the first step it changes.
   - Commands that print individual records (for example `list`) are removed or neutralized.
   - File names are shown for Stata; the kit uses the package's own language.
   - **The kit is answer-key material.** Its README asks that it be kept confidential and not opened with hosted AI tools ([LLM use policy](llm-use-policy.md) §3); its files carry the tier label and the canary; an RA who runs it is covered by the contributor's confidentiality agreement (O-026).
3. **Test it first on a fully synthetic stand-in** built from the codebook, with the same variable names, types, and panel structure, so the kit runs on the first try. The synthetic data never replace the real results.
4. **The contributor or their RA runs it** where the data already are: they edit one line, run one script (about 1–2 hours of their time [U]; the machine can run overnight), and check the outputs against their data agreement's disclosure rules or, where the data provider requires it, submit them to the provider's own disclosure review (for example the Census Disclosure Review Board for FSRDC data [P-page, R8 §2.10]).
5. **They return** `results.zip` through the submission page: logs, tables, and figures for each version, a file list with SHA-256, and a short note (software version, run time, errors). **No data.**
6. **The team compares** the reference outputs with the published paper, and each version with the reference, and records each item's measured effect.

**Fallbacks**, in order of effort: the data provider's own remote-execution service, if it has one [U]; an access application (route b); a secure environment (route c); and, labelled as such, a static check plus the synthetic run, which shows that each version runs and changes the outputs but not by how much. For a held-out task (D-032), the kit goes only to the contributor's own authorized environment, under the confidentiality agreement; the data provider's remote-execution service is not used.

**The demo paper** needs no data; a synthetic stand-in to rehearse the kit is optional.

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

### 5.6 Using AI tools (P-055, proposed)

Contributors may use AI tools, provided what they write for us is their own judgment in their own words. Under this proposal they may put the items, or the task package they download, into an AI tool only for development-tier papers; for evaluation and held-out papers they are asked to review without AI tools (rule 3) until D-032 is revisited (O-037). This is narrower than the research lead's suggestion of 2026-11-07. It also needs the lead's confirmation that contributors' own AI use with development-tier items is an accepted exception to D-018 (P-055). The Guidance page shows the text below in the contributor's interface language.

**Draft text (English)**

> **Using AI tools**
>
> You may use AI tools such as ChatGPT or DeepSeek to help you understand code, check your reasoning, or improve your language. Please follow three rules.
>
> 1. **Your judgment, in your own words.** Everything you write for us (each decision, reason, comment, and proposed error, and any README text you write) should state your own judgment and be written, or rewritten, by you. This does not apply to your original code and data, which we need exactly as they are. Please do not paste AI output as it is.
> 2. **Tell us if AI helped.** Tick "AI helped with this", name the tool and the type of account, and say whether training was switched off and whether you entered the items or the task package. This does not count against your contribution; it lets us describe the benchmark accurately.
> 3. **Keep the items safe.** If we ask you to review a paper without AI tools, please do not put its items, the task package you download from this site, or your comments on them into any AI tool. Otherwise, if you use an AI tool with the items or the package, choose a setting that does not use your conversations for training (see the list below), do not use the tool's feedback buttons, and never share the conversation publicly. Never put restricted or confidential data into any AI tool.
>
> **Why this matters**
>
> - The benchmark tests whether AI systems can do economics research well: for example, whether they find and correct mistakes that economists consider plausible and consequential, or notice and supply a necessary step that was removed. Your judgment is the standard the AI is measured against. If AI-written reasoning entered the tasks unchanged, the benchmark would partly measure agreement with another AI rather than with an economist.
> - AI-written text has recognizable patterns. An AI being tested could use them to find the answers without doing the economics.
> - Tasks shaped by one AI model can be easier or harder for models of the same family, which would make comparisons between AI systems unfair.
> - The items are the benchmark's answers. An AI service that trains on what you paste could pass the answers to future models, which would then score well by memory rather than by reasoning.

**Draft text (Chinese; machine-drafted by Claude, to be reviewed by the team under D-030)**

> **使用 AI 工具**
>
> 您可以使用 ChatGPT、DeepSeek 等 AI 工具来帮助理解代码、检验推理或润色语言。请遵守以下三条规则。
>
> 1. **您的判断，您自己的表述。** 您为我们撰写的每项内容（每个决定、理由、评论、新提出的错误，以及您撰写的 README 文字）都应表达您本人的判断，并由您亲自撰写或改写。此规则不适用于您原有的代码和数据：我们需要它们保持原样。请不要直接粘贴 AI 的输出。
> 2. **如有 AI 协助，请告诉我们。** 请勾选“AI 协助了此项”，注明所用工具和账户类型，并说明是否已关闭训练、是否输入了条目或任务包。这不会影响对您贡献的评价，只是让我们能够如实描述本评测基准。
> 3. **保护好这些条目。** 如果我们请您在不使用 AI 工具的情况下审阅某篇论文，请不要将该论文的条目、您从本网站下载的任务包或您对条目的评论输入任何 AI 工具。在其他情况下，如果您借助 AI 工具处理这些条目或该任务包，请选择不会将您的对话用于训练的设置（见下方列表），不要使用工具的反馈按钮，也不要公开分享对话。任何情况下都不要将受限或保密数据输入任何 AI 工具。
>
> **为什么这很重要**
>
> - 本评测基准检验 AI 系统能否胜任经济学研究，例如能否发现并纠正经济学家认为确实可能出现且有实质性影响的失误，或发现并补上被删除的必要步骤。您的判断就是衡量 AI 的标准。如果 AI 撰写的推理原封不动地进入任务，评测基准在一定程度上衡量的就成了与另一个 AI 的一致程度，而非与经济学家的一致程度。
> - AI 撰写的文字有可辨认的模式。接受测试的 AI 可能借助这些模式找到答案，而无需进行经济学推理。
> - 由某个 AI 模型塑造的任务，对同一系列的模型可能更容易或更难，这会使不同 AI 系统之间的比较有失公平。
> - 这些条目就是本评测基准的标准答案。用您所粘贴的内容训练模型的 AI 服务，可能把答案传给未来的模型，使其靠记忆而非推理取得高分。

**Settings list for the Guidance page** (compiled 2026-11-07 from R3, accessed 2026-11-05, and R11, accessed 2026-11-06, and not re-checked since; providers change these, so re-check before each invitation round. The Label column is for the team and is not shown on the Guidance page.)

| Tool | Setting that excludes training | Label |
|---|---|---|
| ChatGPT, personal plans | Turn off "Improve the model for everyone"; business and enterprise plans are not used for training by default | [S], [R11](../research/evidence/R11-llm-assistance-in-benchmark-construction.md) §5 |
| Claude, consumer plans | Turn off model training in your account settings (conversations flagged for safety review may still be used); commercial plans are not used for training | [P-page], R3 §6 |
| Gemini app | Gemini Apps activity is used for training by default for adults; the setting that turns this off is to be confirmed before the first invitation round | [S] default, [U] setting, R11 §5 |
| DeepSeek app | The app may use inputs to improve services, with an opt-out; the setting's name and location are to be confirmed before the first invitation round | [S]/[U], R11 §5 |

Feedback buttons can send a whole conversation for training even after opting out: Anthropic states this for its consumer plans [P-page, R3 §6]; whether OpenAI and other providers do the same is unverified [U].

**For the team.**
- Papers in the evaluation and held-out tiers are reviewed without AI tools; their contributors are asked to do so but are not told the tier.
- Each use a contributor reports is entered in the exposure log.
- Allowing AI tools gives up one safeguard: reviewers who work without AI keep the expert check independent ([R11](../research/evidence/R11-llm-assistance-in-benchmark-construction.md) §4). Rewriting in one's own words does not prevent anchoring: in one study, 77% of analysts repeated an AI agent's argument and 15% credited it ([R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) §1). The per-item disclosure is therefore used to report AI-assisted and unassisted validations separately, and AI-assisted decisions on LLM-drafted items are re-checked.
- When D-032 is revisited (O-037), the research lead will decide whether AI use under no-training settings can also be allowed for evaluation-tier items.

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

Interface text contains no project material, so drafting it with any LLM leaks nothing. Per-paper interface text, such as a category's one-line meaning and the checklist entries, goes through the same draft-and-review step. Because these entries describe categories, not planted errors, they may be drafted with a model the research lead has configured (D-018); for held-out papers, by hand only (D-031, D-032, D-033). **Item text is not translated.**

**Adding a language** means adding one catalogue and the per-paper labels, then reviewing both; no code changes.

## 7. Privacy and data-flow architecture

- **Default flows:**
  - the contributor's browser and the project server only;
  - no analytics, web fonts, content delivery networks, or embedded third-party content;
  - outbound traffic blocked.
- **Model modes:**
  - Mode 0, Off: the site itself uses no model in v1;
  - Mode 1, a local model, would keep data on project hardware; it is not planned (D-033);
  - Mode 2, an external API such as DeepSeek with the lead's key, sends data out of the project. It needs explicit configuration (D-018) and is **never** used for held-out tasks (D-031, D-032), contributor responses (proposed, P-035), or restricted data; it never carries an evaluation task's agent-facing package (D-032); any other use is logged with its provider, terms, and date;
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

See the [implementation plan](mvp-implementation-plan.md) v0.3:
- one Django application, server-rendered, with SQLite and encrypted storage;
- the map and item panel rendered on the server with plain HTML and CSS;
- resumable uploads for multi-gigabyte packages;
- about 6–9.5 engineer-weeks for one developer [U: planning estimate].

**Where it runs (P-053, staged).**
- **Stage 0, the demo:** a team member's computer with full-disk encryption, with synthetic examples and the demo paper only. The application listens only on the computer's own loopback address (127.0.0.1), so it is reached only from that computer. Others see it by screen sharing, with the meeting service's recording and AI features switched off. The demo data folder is kept outside any workspace opened by a hosted AI coding assistant. No decision about servers or storage is needed for this stage.
- **Stage 1, before the first outside contributor uses it with real material:** the same application on one small project-controlled server outside mainland China (most contributors are outside mainland China: research lead, 2026-11-06).
  - A site hosted outside mainland China, and not delivered through a content delivery network in China, needs no ICP filing, the registration required for websites hosted in mainland China [P-page/S, R9 §8.5; not a legal opinion].
  - Ideally the university provides the server; otherwise a rented one costs about US$4–20 a month (an assessment from [S] list prices, R10 §4; check the provider's own page before committing).
  - It has HTTPS, an encrypted disk, an outbound firewall, nightly encrypted backups with a restore test, and one named administrator.
  - Before invitations go out, the site is tested from mainland China and from abroad, because traffic from mainland China to servers outside it can face "significant latency and reliability issues" [P-page, R9 §8.5].
- **Moving between stages** means installing the same pinned application on the server with its own Stage 1 settings and, if the demo configuration is kept, copying the data folder after revoking all demo invitations and test accounts (plan M6).
- **Not proposed:** exposing the demo computer through a tunnel service.

## 10. Open questions

| ID | Question | Proposed default |
|---|---|---|
| O-027 | Does the layered card (§4.2) suit contributors? | Pilot it with the first paper's two experts |
| O-029 | Does the map with the item panel (§4.1) suit contributors? | Pilot it, with the matrix toggle as the alternative |
| O-035 | Who checks that data included in an upload may be shared with the project? | §5.5: a named data steward, with uploads quarantined until checked |
| O-021 | Hosting | §9: staged, a team member's computer for the demo, then one small server outside mainland China before the first outside contributor (P-053) |
| O-036 | The first real contributor and paper | A possible contact the research lead named (the name is not recorded here); the paper's field sets its categories (D-025) |
| O-037 | AI use in building tasks, then D-032's held-out and exposure wording | Revise the construction process for the team (P-054) and contributors (P-055) first, then revisit D-032 and decide whether its clarifications (a) and (b) are still needed |
| O-022, O-026 | Invitation delivery; confidentiality agreement | Unchanged; confidentiality is asked of every contributor and is essential for evaluation and held-out tasks (D-032) |
