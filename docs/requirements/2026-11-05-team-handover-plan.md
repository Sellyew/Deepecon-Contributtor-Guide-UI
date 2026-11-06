# Team Handover Plan (summary)

| | |
|---|---|
| **What this is** | A faithful English summary of the research team's student handover package *DeepEcon 专家交互智能体 — 学生执行交接包* (dated 2026-11-05; "task and literature configuration" version), supplied by the research lead on 2026-11-06 with the [revised requirements](2026-11-06-research-lead-revision.md). The package has three files: a main plan (Word), a development task list (`开发任务清单.md`), and a README. |
| **Status** | Reference requirements from the research team. Where this plan and the 2026-11-06 requirements differ, **the 2026-11-06 requirements govern** (for example, every model call is optional and disabled by default). |
| **Omitted** | Personal names of the invited experts (recorded here by role only). The original files are not committed to this repository. |

---

## 1. Purpose and the expert's experience

The team starts from one paper and turns experts' review of **prepared candidate points** into implementable, verifiable, scoreable audit tasks. Experts are contacted in advance by e-mail or WeChat; the paper and the first-round division of work are agreed **before** anyone enters the system. An administrator pre-configures each expert's task.

The expert's path: open the assigned paper task → read a short explanation of the two task types and the target numbers → review prepared candidates in batches of about five → select or adjust → confirm → the team implements and checks → the task package and scoring rubric are frozen.

- About **15 candidates** are prepared per paper, shown in batches of about **5**. Experts may choose only some, skip, reject, reorder, revisit, or add their own. Fifteen is a pool, not a quota; quality and verifiability decide what enters the final package.
- No paper summary, free-form questionnaire, or paper re-selection is asked of the expert at entry.

## 2. Candidates: two dimensions, two symmetric options

- **Domain:** code engineering or economic analysis.
- **Task type:** **error** (identify and correct an erroneous analysis step) or **missing** (detect and supply a necessary step that was removed).
- **Target numbers** (`target_error_count`, `target_missing_count`) are planning targets set by the administrator, shown separately from confirmed counts; shortfalls are allowed.
- **Each card is one key point** and shows an *error* variant and a *missing* variant **at the same level**, each with feasibility, consequence, and evidence. There is no preselection, recommendation mark, or default tick. The expert may pick one, keep both (they become separate, traceable candidates), modify, mark "neither suitable" or "uncertain", or add a new option. If a variant is not applicable, the reason is shown; no feasible variant is invented.
- Example from the plan (illustrative only, not a claim about the pilot paper): for a control-group eligibility rule, the *error* variant wrongly admits ineligible units; the *missing* variant deletes the eligibility filter.
- The paper's own acknowledged limitations are recorded separately (`issue_class`), not as planted defects. A deliberate **omission** of a necessary step is distinguished from a **missing input** in the team's materials.
- Initial order uses a "teacher model's" estimates of importance, complexity, and difficulty for AI, with reasons and uncertainty; ranks are only a review order and do not imply that one type is preferable. Predictions, expert judgments, and measured difficulty are stored separately.

**Each confirmed candidate records:** (1) the original approach and its location; (2) what is changed or deleted; (3) the effect on identification, estimation, or interpretation; (4) what evidence the solver can see; (5) acceptable repairs and alternatives; (6) data and run dependencies; (7) the expert's confirmation and uncertainty.

## 3. Three verification rounds (team-side, after the expert's review)

1. **Academic confirmation:** the expert confirms the candidate states their judgment faithfully, the problem is real and important, solver materials can support discovery, and reasonable alternative explanations are stated. Output: a confirmed defect description and initial scoring points.
2. **Implementation check:** the team implements the change on a copy of the paper's code and returns the diff, input versions, run logs, and output changes; the original expert checks fidelity; third-party experts and the teacher model help review (economic judgment stays with people). Single defects first, then combinations.
3. **Package and rubric acceptance:** an independent reviewer first sees only the solver materials (clarity, sufficiency, answer leakage), then the answers and rubric. Unresolved disputes stay pending. The rubric scores location, economic explanation, repair validity, and verification, lists acceptable alternatives, and has rules for extra findings, false positives, and harmful edits. Package and rubric are frozen together; later changes create new versions.

A small number of agent trial runs compare misses, false alarms, repair quality, and review time, recorded per model-and-harness combination.

## 4. Prototype: simple front end, manual back office

- **Two entry points:** an **expert entry** (assigned task, candidate review) and an **administrator entry** (task configuration, candidate import, progress, export of confirmed drafts, back-filling verification results, freezing). Third-party review can happen offline and be recorded by the administrator.
- **Architecture:** invitation-only web page, server-side persistent database (SQLite for a single-machine prototype), private file storage, administrator entry; model keys only on the server.
- **Behaviour:** autosave with explicit success or failure; recovery after refresh; idempotent resubmission; visible conflicts between concurrent edits; exports of the expert confirmation record (JSON), a readable summary, an engineering task list, and a package manifest.
- **One page template** loads each assignment's paper PDF, appendix PDF, and candidate pool; experts see only their assigned tasks; evidence links open the specified PDF page and return to the card without losing edits.
- **Evidence references** record material ID, file version or checksum, PDF page index (from 1), printed page label (if any), section or figure, a locator note, who proposed it, and verification status; code references record path, version, and line range. Teacher-model locations are checked one by one by students; unchecked items are never shown as verified.
- **Deferred:** voice, complex accounts, real-time collaboration, automatic evaluation clusters, management dashboards. Code execution, review scheduling, notifications, and payments stay manual.
- **Optional conversational model** in the plan: DeepSeek V4 (low) or "GPT 6.1 Terra" (medium) to help discuss, ask follow-ups, and record faithfully; it may explain and clarify but never decides for the expert, never pads numbers, and never re-argues after a rejection. New AI suggestions are labelled "AI suggestion, awaiting your judgment"; the expert's original words and the model's summary are stored separately and echoed back for confirmation. *Under the 2026-11-06 requirements this model is optional and off by default; an external API (either model as a hosted service) transmits data to its provider.*

## 5. Suggested data objects (from the development task list)

All objects carry a stable ID, creation and modification times, and a version.

- **Project:** paper_id, paper_version, owner, status, target_error_count, target_missing_count.
- **Material:** material_id, paper_id, file_role (main text / appendix / code / answer), file_version, private_storage_key, source, type, checksum, access_scope, allowed_model_destinations, allowed_for_contestant.
- **Assignment:** assignment_id, expert_id, task_id, paper_id, role, first_round_scope, relationship_to_paper, prearranged_at.
- **Candidate:** candidate_id, origin (expert / AI / team), domain (engineering / economics), teacher_priority_estimates, initial_rank, expert_rank, proposed_options (both types, each with feasibility, reason, concrete change, and evidence), confirmed_options, injection_spec, evidence_refs, proposed_change, mechanism, visible_clues, valid_repairs, dependencies.
- **Decision:** candidate_id, candidate_version, expert_original_text, structured_text, action, reason, confirmed_by, confirmed_at.
- **Implementation, Review, Rubric, Release, EventLog** (team-side: patches, runs, review gates, rubric versions, frozen releases, audit log).

**Status rules:** execution states (not started, running, done, partial, failed, cancelled, superseded) are separate from academic states (awaiting expert, needs material, disputed, expert-confirmed, rejected, deferred). A generated candidate is not an academic confirmation; a successful run is not a correct repair; new material marks dependent confirmations "needs re-review"; re-runs create new suggestion versions and never overwrite confirmed content; releases are immutable.

## 6. Security acceptance tests (abridged)

Random, time-limited, revocable invitation credentials, never in ordinary logs; server-side checks on pages, APIs, downloads, and exports; experts see only assigned tasks (guessing IDs or copying URLs fails); private storage with authorized, short-lived download links; model keys never in HTML, builds, caches, or exports; restorable backups; write failures reported, never shown as saved; restricted data, answers, and keys never in unauthorized responses, browser logs, or solver exports; keyboard operation; no horizontal overflow on laptops and phones.

## 7. Pilot paper and material boundary

> **Clarified by the research lead, 2026-11-06:** this paper is a **demo** for building and testing the interface; the team has no contact with its authors (D-024).

- **Pilot:** Muñoz, Pablo, and Cristóbal Otero (2025), "Managers and Public Hospital Performance", *American Economic Review* 115(11): 4040–4074, doi:10.1257/aer.20240615. Replication package: openICPSR project 234421, version 1.
- **Experts:** two invited health and labor economists from the team's network; when they co-author tasks they belong to the task-writing team, and independent review is arranged separately.
- **Materials:** the inspected replication package contains Stata code and some public inputs; the **DEIS and SIRH raw-data directories are empty**. The team first builds a "paper result → script → input data" map to see which paths can be run. Patient and employee records need separate checks of usage permission and processing environment; restricted parts can collect expert judgment first, with repair verification only once data and authorization are in place.
- The package contains no raw patient or employee data and no model keys.

## 8. Decisions the plan leaves to the project lead

Who performs independent review and how it connects to the first-round assignment; the 15-candidate coverage and the two target numbers; who signs each verification round and how the one-rework limit is counted; what paper context agents receive, whether they may search, and run budgets; **which model, if any, assists experts and which materials may be sent to it**; deployment location, sign-in method, and data-retention period.

## 9. Design references cited by the plan

- Saris, Revilla, Krosnick & Shaeffer (2010), *Survey Research Methods* 4(1): 61–79, doi:10.18148/srm/2010.v4i1.2682 — item-specific response options outperform agree/disagree scales; motivates concrete, symmetric options.
- Gaube et al. (2021), *npj Digital Medicine* 4: 31, doi:10.1038/s41746-021-00385-9 — inaccurate advice lowers diagnostic accuracy whether labelled human or AI; motivates evidence checks, source labels, and human confirmation.

The plan notes that neither study validates this interface directly or shows that batches of five or this order are optimal. *(Both references are as cited by the plan; not re-verified here [U].)*
