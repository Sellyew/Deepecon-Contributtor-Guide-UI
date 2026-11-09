# R15: What DeepEcon can still learn from Terminal-Bench-Science

| Field | Value |
|---|---|
| Topic | Which Terminal-Bench-Science (TBS) practices DeepEcon should adopt now, adopt later, or not copy, after DeepEcon's methodology already borrowed parts of TBS |
| Date | 2026-11-09. TBS read at commit `f3566474` (committed 2026-11-09), read-only sparse clone; no scripts run. |
| Author | lead collaborator (Claude session), answering the research lead's question of 2026-11-09: "Can we learn something from TBS?" |
| Method | Done by AI agents, not human researchers. Four Claude agents run from this session each took one lens (task design and verification; contribution and review; quality assurance and leakage; community, credit, and releases). They read [R1](R1-terminal-bench-science.md), R12 to R14, the decision log, the methodology documents, and the current TBS repository, and proposed 32 lessons. A fifth agent checked every TBS citation and every claim about DeepEcon's documents (corrections applied below). A sixth judged fit with DeepEcon's decisions and the "keep it lightweight" rule, merged duplicates, and kept 19. A second agent of the same model family is not an independent human check |
| Evidence labels | As in the [evidence README](README.md). TBS files are [P-full] or [P-page] at `f3566474`; recommendations are *(assessment)* |

---

## 1. The headline

*(assessment)*

- **"Labs use TBS" does not mean TBS's scores are free of contamination.** TBS's own trial-analysis rubric lists "Prior knowledge of the answer" as a route to unearned credit: "A contaminated task can be answered without exploiting anything, so this route leaves no trace of misbehavior … Judge the shape of the work instead", and prescribes that such a task "must be regenerated with fresh parameters or retired" (`rubrics/trial-analysis.toml`) [P-page].
- **TBS can publish its answers because of how its tasks are built, not because exposure is harmless.** Its rubrics exclude difficulty that comes from knowing a fact ("Obscure factual knowledge generally does not make tasks hard", `rubrics/task-proposal.md`; criterion `novel`: "Not solvable through training corpus memorization", `rubrics/task-implementation.toml`) [P-page]. Many tasks grade a procedure by re-running it on inputs the agent never saw ("the verifier re-runs the submitted procedure on six sealed systems freshly drawn from the disclosed family", `traffic-flux-inversion/README.md`) [P-page], or have keys too large to recall (755 row IDs among 800,859 rows in `ehr-error-detection`) [P-full].
- **The transferable lesson is about task design.** DeepEcon's procedure-keyed tasks (re-estimation graded on hidden data variants) can be public development tasks with little loss. Its fact-keyed tasks (a short planted error and its fix) cannot be made safe to publish by any TBS mechanism.

## 2. Adopt now (cheap; proposed as P-064)

| Lesson | TBS practice | What DeepEcon does | Proposal |
|---|---|---|---|
| **Classify each candidate by what its key gives away** | Rubrics exclude fact-based difficulty (above) | R14 §3 states the asymmetry; O-004 ("one-sentence-fact" tasks) is open; nothing acts on it | Construction protocol Stages 3 and 5 record per candidate: fact-keyed or procedure-keyed, and whether hidden data variants are feasible. Fact-keyed tasks get their own reported score; long-lived comparisons rest mainly on procedure-keyed tasks. Team-side only; no site change |
| **A DeepEcon canary, now** | Every file and comment carries a canary, but it is BIG-bench's GUID, so a probe cannot attribute contamination to TBS (R1 §1.8, R14) [P-page] | CLAUDE.md convention 5: "to be defined" | Two fresh GUIDs: one public, on all published material (demo and development tasks); one unpublished tripwire inside evaluation internals, whose appearance anywhere signals a leak. Neither in agent-facing files; the harness strips header lines |
| **Whose turn it is, and checks before people look** | One responsible reviewer per slot, labels "waiting on author" or "waiting on reviewer"; mechanical checks run before reviewers are assigned; a daily sweep re-runs every check on every merged task after nine tasks stayed non-compliant "for days with a green Actions tab" (`REVIEWING.md`, `TASK_REVIEW_AUTOMATION.md`) [P-page] | M2 builds "Ask the team" and freezing (plan §2 item 7) | M2: an optional team owner per paper; the admin lists questions unanswered first, oldest first; freezing blocks on a missing build date or missing item provenance; a `check_papers` command re-runs every importer check on every paper when a rule changes |
| **Credit and conflicts, written before the first invitation** | One co-authorship point per merged task; conflicts of interest disclosed per task ("Disclosure is not a strike against the task; concealing it is grounds for exclusion"); everything attributed publicly task by task (`CONTRIBUTING.md`, `task-template.toml`) [P-page] | O-005 (credit) is open and blocks recruitment | One contributor-terms page, drafted for the lead: credit per contribution to a paper, independent of model scores and of the development/evaluation draw; one optional conflict-of-interest line that includes ties to AI developers (a human route of exposure Rule 10 does not see); people credited now, but names linked to evaluation papers only once those papers are published or retired, since a public author list would reveal which papers are in the evaluation set |

## 3. Adopt later (task building and the first evaluation version, E1)

- **Tell the agent its code will be re-run on other data.** TBS's `well_specified` criterion requires stating anything "no amount of expertise recovers", such as "a verification input drawn differently from the public one"; tasks state the ranges of the private inputs [P-page]. DeepEcon's VVP §5 already builds hidden variants (borrowed from TBS); add one sentence to the output contract (rubric SP-4) and state the limit: re-execution does not protect a short fix the agent already knows.
- **EHR-style scoring for detection tasks:** recall counted by equivalence group, and pre-labelled natural errors that earn precision credit only [P-full]. Instances fixed per evaluation version, not drawn per run (per-run draws add noise and break the published manifest hash, D-047).
- **Cheat trials as a written, judged red-team step** (`/cheat`, `rubrics/cheat-analysis.toml`) [P-page], but with the scope reversed: the paper, the public original package, and the model's memory are in scope.
- **A rule-based recall check on trajectories** for evaluation tasks, following TBS's "judge the shape of the work" signals (the answer appears before the work; the agent names the source paper or repository). Deterministic, on the harness's tool-call log, with flagged passes read by a team member; reported beside P-063's gaps, never as silent rescoring.
- **Treat by-products that come close to the answer as answer-key material:** TBS keeps oracle logs, verifier output, and trajectories off public channels, because "a public job is world-readable forever" [P-page]. A one-page list for DeepEcon (verifier logs, hint texts, passing trajectories, calibration reports, task READMEs of evaluation papers).
- **Immutable numbered releases with DOIs and a manifest** (`RELEASING.md`) [P-full], with a stricter rule than TBS's (5 of its 70 v0.1 tasks changed on main without a patch release, R13): any change to what the agent sees or how it is graded is a new version. Deposit D-047's manifest hash with the release record for a third-party timestamp. Needs O-010 (licence) and O-014 (name) first.
- **Reviewers from finished contributors**, by assignment, with a light fixed load and never on their own paper (TBS: "Top contributors are invited into reviewer & maintainer status") [P-page]. A lever on O-009 (staffing).
- **Publish the development set in Harbor format, or ship a converter** (O-011): part of why labs run TBS is that it ships in a format an existing harness runs.

## 4. Do not copy

- **Generator-injected, generic errors as scored items.** EHR's errors are safe to publish because they are generated and many; DeepEcon measures paper-specific, expert-validated design errors (X-005, D-039).
- **TBS's public, contributor-built propose-build-PR workflow.** DeepEcon's team prepares items and economists review them (D-020, D-021, X-006, X-007). Selection asks economists only domain questions, never engineering ones; the team may use TBS's PR checklist internally.
- **Open agent internet, an honour sentence, and red-team scoping that excludes the benchmark's own copies.** Agents fetched answers from TBS's own pull requests (R12); DeepEcon isolates the evaluation (D-041). If DeepEcon adopts Harbor, Harbor's default public network and TBS's out-of-scope clause must not come with it.
- **Curating the scored set after seeing results**, or a "lite" set used as a moving cut (TBS planned v0.1 as the set "published after the evals decide what to cut", R13). Set-asides and repairs happen before D-047's hash is published and are counted in the release notes.
- **Maintenance as a condition of credit.** TBS can withdraw co-authorship from unreachable authors (`CONTRIBUTING.md`) [P-page]; DeepEcon's team owns the code, and its contributors are invited economists. Instead: one optional, credited failure-analysis round per paper at E1.

## 5. Changes in TBS since R1 (clone of 2026-11-04)

At `f3566474` (2026-11-09), by the AI agents' own counts: 90 task directories (83 in R1); new trial-analysis and cheat-analysis rubrics; `authoring/hint.md` deleted before merge (R12); the red-team prompt puts the benchmark's own copies out of scope (R12).
