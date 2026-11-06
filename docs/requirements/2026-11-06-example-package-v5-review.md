# Example Contribution Package V5: Structural Review

| | |
|---|---|
| **What this is** | A structural review of the example contribution package supplied by the research lead on 2026-11-06 (`DeepEcon_V5_Research_Package_20261105`, prepared by one of the lead's coauthors). It is the primary reference for the contributor workflow, data structure, and submission requirements (D-023). |
| **Inspection boundary** | The master README, the checksum file, and the agent-facing task contract (`04_task/`) were read in full. For the expert-only folder and the researchers-only report, **only the structure was inspected**: file names and sizes, JSON key names, types, array lengths, point totals, and document headings. No rubric criteria, item titles, item locations, repairs, guides, patches, or results were read. *Reason:* the package's own README says expert materials and the report must never reach a candidate agent's filesystem or conversation, and Claude models may later be evaluated on such tasks; reading the answer key in a Claude session would be exactly that leakage. The agent-facing code files were not read either; they are not needed for the interface design. |
| **Integrity** | The SHA-256 hashes in `SHA256.json` match the three files (checked 2026-11-06). The master README states that the 50 candidate files match the hashes in the expert package. |
| **Not committed** | No file from the package is copied into this repository. |

---

## 1. Package layout

| Part | Contents | Audience |
|---|---|---|
| `00_READ_ME_FIRST.txt` | What each part is and who may see it; "for a clean evaluation, place only the candidate ZIP in a fresh session/workspace" | Research team |
| `01_Report_Researchers_Only/` | A 3-page Chinese pilot report: findings and goals; task materials and conditions; scoring structure and the academic threshold for missing analyses; results and disputed items (one table: submission label, 学理 40, 补全 42, 技术 18, extra deductions, provisional total; 8 submissions); where submissions differ; literature basis; next steps; 6 references | Research team only |
| `02_Candidate_Only/` | **The only material given to an evaluated agent:** one ZIP, 50 files, about 117 KB | Evaluated agent |
| `03_Expert_Only_Do_Not_Upload/` | Rubric, score template, expert guides, independent-review note, checks, candidate hashes, mapping from V4, a V4→V5 patch, and archived V4 files; 18 files, about 153 KB | Experts and graders only |
| `SHA256.json` | SHA-256 of the three parts | Integrity |

## 2. The agent-facing task (read in full: `04_task/`)

- **Folders:** `01_article/article.txt` (a 255-word research background under a neutral title); `02_code/` (a 43-file Stata workflow plus 2 short notes: master script, dependencies, data construction, analysis stacks, 14 chart scripts, 11 table scripts, and supporting programs); `03_codebook/` (a study dictionary and command contracts); `04_task/` (instructions and a file index). The file names are neutral (`10_policy_dates.do`, `40_chart_01.do`, `50_table_01.do`), so the workflow is presented in a restructured form rather than the original package's layout.
- **Task:** a **static review**. The agent submits a reasoned audit and a complete revised copy of the code, with a change list (`AUDIT.md`, `CHANGE_LIST.md`) and any additional analysis programs the study aims require. Each substantive change must connect the code evidence to the research aims: mechanism, affected conclusion, repair, and its assumptions.
- **Constraints:** no search, browsing, running, simulation, or testing; no claims of execution. A verified false assertion costs 10 points per distinct root cause; an unsupported removal of a valid analysis costs 20 (not stacked); genuine limitations and qualified questions are not penalized.
- **No data:** the package contains no patient-level data, and the expert checks record that Stata was not executed and that data were not available.

## 3. The expert rubric (structure only)

`Rubric.json` (version label `v5_strict_rubric_1`, maximum 100) has three item groups, which correspond to the team plan's candidate dimensions:

| Group (report label) | Items | Points per item | Group total | Item fields | Score tiers |
|---|---|---|---|---|---|
| `conceptual` (学理) | 5 (one-letter IDs) | 8 | 40 | id, points, title, files, criterion, scoring_method, allowed_scores, tiers, critical_requirements (3), evidence_record_required (5), and a historical component-weight object (specific diagnosis; abstract-linked mechanism and estimand argument; implemented repair and downstream consistency; assumptions and limits) | 0, 2, 4, 6, 8 |
| `missing` (补全) | 3 (two-character IDs) | 14 | 42 | id, points, title, available_evidence_and_boundary, acceptable_work, scoring_method, allowed_scores, tiers, critical_requirements (4), evidence_record_required (5), historical weights (goal and specific gap; complete abstract-linked argument; implemented feasible analysis; assumptions and interpretation) | 0, 3, 6, 10, 14 |
| `technical` (技术) | 7 (three-character IDs) | 3 (4 items) or 2 (3 items) | 18 | id, points, title, file, repair, scoring_method, allowed_scores, tiers, evidence_record_required (3), historical weights (evidence and explanation; implemented correct repair) | 0, 1, 3 (or 0, 1, 2) |

Rubric-level sections: `penalties` (per-root penalties for verified false assertions and unsupported removals; rules for same root, genuine limitations, novel valid findings, severity), `gates` (no substantive justification, review only, code only, unavailable data, unclear cases, no half points), `global_policy` (eleven rules: coarse scores, critical versus minor, complete code, execution, equivalent solutions, supported deletion, partial credit, no unstated floor, penalty overlap, rescoring, machine reading), `candidate_version`, and `calibration_status`.

**Other expert files (structure only):**
- `Score_Template.json`: one record per item (id, maximum, allowed scores, score, answer evidence, code evidence, critical requirements met, rationale), penalty roots, raw and net scores, a global no-justification gate, unresolved adjudications, and whether execution was verified.
- `Static_Checks.json` and `Strict_Rubric_Checks.json`: counts and consistency flags (files, do-files, word counts, links, group totals, integer tiers, candidate unchanged, source unchanged; status `STATIC_CONSISTENCY_ONLY`).
- `Candidate_SHA256.json`: a hash for each of the 50 candidate files.
- `Mapping_From_V4.json`: renamed files (20), removed files (8), and fixes (5) between versions; `Changes_From_V4.patch` (58 hunks); archived V4 files.
- `Expert_Guide.txt` (917 words), `Previous_Expert_Guide_V5.txt`, `Independent_Review.txt` (67 words).

## 4. What this settles for the contributor interface

1. **The prepared candidates are rubric items.** The Selection screen shows the 15 items in their three groups. A contributor's decisions decide which items enter the rubric and how they are worded. The team's existing rubric file can be imported directly (P-041): on 2026-11-06 the V5 rubric passed the draft import schema and consistency checks (only pass/fail and error paths were printed, no content).
2. **The task is a static code review with no data.** For tasks of this kind, contributors need to supply code and documentation, not data, so restricted microdata never need to be uploaded and package sizes are small (the whole candidate package is about 117 KB).
3. **Three material tiers already exist** (agent-facing, expert-only, researchers-only), each with SHA-256 manifests. The site stores and exposes them separately (P-043); contributors see expert-only material for their own paper only.
4. **Versioning is explicit** (V4 → V5 with mappings, patches, and frozen hashes). The site records which rubric and candidate version a contributor reviewed.
5. **The agent-facing presentation is restructured** (neutral title and file names). A contributor reviewing errors in their own paper may need locations in their original file names; that requires a mapping from the original package to the candidate files (question Q2 in the [MVP proposal](../architecture/mvp-contributor-interface.md)).

## 5. Observations for the research lead (methodology, outside the interface)

- The V5 design grades a static audit against a 15-item rubric with coarse integer tiers, rather than re-executing the agent's code. That fits restricted-data papers and avoids execution costs, but it makes grader agreement central: the rubric's checks are labelled `STATIC_CONSISTENCY_ONLY`. Measuring agreement between two independent graders on the pilot submissions would show whether the tiers are reproducible. The `calibration_status` field may already record plans for this; it was not read.
- The penalty rules (10 points per false-assertion root, 20 per unsupported removal) are part of what the agent sees, which is good practice: the agent is told how it will be scored.
