# Open to Contribute, Open to Develop, Controlled to Evaluate

| | |
|---|---|
| **Status** | **Proposed** v0.3 (2026-11-08; §7 revised the same day), drafted by Claude at the research lead's request. The three principles are the lead's (D-046). The lead settled the first version's choices on 2026-11-08 (D-047): only demo papers are public, access is by invitation, and the evaluation manifest's hash is published; §4, §5, §6, and §9 now say so. The rest is a recommendation (P-062) until the lead approves it. |
| **Replaces** | P-061 (scored tasks only by assignment), withdrawn |
| **Builds on** | D-038 to D-045; the [AI use and integrity rules](llm-use-policy.md); the [construction protocol](../methodology/benchmark-construction-protocol.md) Stage 8; the [verifier validation protocol](../methodology/verifier-validation-protocol.md) §8; evidence notes [R10](../research/evidence/R10-contamination-and-evaluation-isolation.md), [R12](../research/evidence/R12-human-access-to-unreleased-answers.md), [R13](../research/evidence/R13-release-and-evaluation-practice.md) |
| **Scope** | The long-term shape that M2 and later milestones should fit. It adds one small step to the contributor site (§4); everything about official evaluation comes after the MVP |

---

## 1. Summary

*(assessment and proposal)*

- **One workflow, two sets.** Every task goes through the same contribution, AI-use rules, and expert validation. After validation, each **paper** is drawn into either the **development set** (published with solutions and grading tools) or the **evaluation set** (answer keys and grading materials unpublished). The draw is random within each admitted batch, recorded, and made before any official run.
- **Discovery is separate from access.** Every listed paper shows its citation and what contributions it needs. Development papers can be opened by any invited contributor. Evaluation papers need the team's authorization: a contributor asks, the team grants.
- **Official scores come from frozen, versioned evaluation sets run by the team** under a fixed protocol, with exposure tracked per task. New tasks enter in the next version; evaluation papers stay for as long as they are informative and retire only on events (§7).
- **What already exists covers most of this.** D-040 already separates scored from development tasks and fixes the designation before any evaluation run; the methodology already freezes releases, requires a blind independent reviewer, and forbids tuning tasks to models. The changes are mostly wording, the draw, and one access step on the site.

## 2. What other benchmarks do

From [R12](../research/evidence/R12-human-access-to-unreleased-answers.md) and [R13](../research/evidence/R13-release-and-evaluation-practice.md); labels there. Repository facts are primary; ARC policy, FrontierMath, and Scale details rest on search summaries [S].

| | Contribution | Access to unreleased material | Official evaluation | Task release |
|---|---|---|---|---|
| **Terminal-Bench-Science** | Open: anyone proposes and submits through public GitHub; two assigned reviewers and a final reviewer per task | None to protect: tasks, solutions, and tests are public before and after merge | Maintainers run release evaluations; v0.1 was cut "after the evals decide what to cut" | Immutable versioned releases with DOIs; a manifest defines each release; repairs go into new versions |
| **Terminal-Bench** (2.0 to 4.1) | Open, through public PRs | Public ("an open-internet benchmark") | Moved from self-reported to maintainer-run; conditions enforced in code: dataset digest, at least 5 trials, no overrides, pinned harness versions | Per-task versions: a patch reuses results, a minor change regrades them, a major change re-runs them |
| **ARC-AGI** | The ARC team builds tasks; paid testers attempt them | Public sets open; semi-private and private sets held by the ARC team | The team runs hosted models on the semi-private set and acknowledges it leaks over time; the private set runs only offline [S] | Generations are new benchmarks; hidden sets reused for years, then retired, not published |
| **Humanity's Last Exam** | Open call to experts, with prizes and co-authorship; reviewers assigned by organizers [S] | Public set open; a private held-out set held by the organizers [S] | Pinned judge model, fixed settings, confidence intervals | Public set revised over time; a dated per-question change log since 2026 |
| **FrontierMath** | Contracted mathematicians under NDAs [S] | Mostly private, held by Epoch; the funder sees most problems except a holdout [S] | Epoch runs evaluations itself on private problems [S] | Versioned as a whole; v2 corrected or removed about 150 problems after an audit, and scores are not comparable across versions [S] |
| **METR, Scale SEAL** | Staff and contracted task authors | Private suites held by the organization | Run by the organization, partly under NDA; Scale features a model only the first time its developer meets a set [S] | Versioned suites; METR pins suite commits |
| **LiveBench, LiveCodeBench, SWE-rebench** | Built by the maintainers from fresh sources | Newest items withheld for a period (LiveBench [S]) | Scores by date window against model cutoffs | Dated items or monthly slices; cadence hard to keep up (LiveCodeBench has not been refreshed since mid-2025) |

**What this means for DeepEcon** *(assessment)*:

- **Open contribution with public development data** is the Terminal-Bench model, and it works at scale (TBS reports 376 contributors [S]). Its weakness is that nothing is unreleased, so it has no clean comparison of new models.
- **Controlled evaluation** in every benchmark that has it means a protected set held by the organizers and run by them under fixed conditions, as at ARC, Epoch, METR, and Scale. Discovery and contribution can stay open while access to the protected set is by assignment (R12).
- **No benchmark found does exactly what the lead proposes,** one open workflow feeding both a public development set and a protected evaluation set. The nearest are HLE (an open call feeding a public set and a private set) and ARC (public, semi-private, and private sets of one design).
- **Two failure modes are documented and worth designing out.** Curating the evaluation set after seeing results (TBS v0.1, HLE-Rolling's replacements) and breaking comparability by editing sets without versions (HLE before 2026, ARC-AGI-2's in-place fixes, LiveCodeBench).
- **API evaluation exposes the protected set.** ARC has a fully private set for offline runs; DeepEcon does not, because it deploys no models (D-038). Its protection must therefore come from fresh tasks and exposure dating (D-040), as at LiveCodeBench and Scale.

## 3. The architecture

```
contribute ──► validate ──► admit to a batch ──► draw (per paper, recorded) ─┬─► development set: published, solutions and tools
(same rules)   (same bar)                                                    └─► evaluation set: frozen version, run by the team
                                                                                    │
                                                         retire at the next version ┘──► development set
```

| Part | Development set | Evaluation set |
|---|---|---|
| Purpose | Help AI researchers develop, train, and test systems | Credible comparisons of newly released models |
| Published | Instruction, package, solution, verifier, rubric, all with the canary | Instruction and package only to evaluated models through their APIs; answer key and grading materials unpublished |
| Who sees task materials while building | Any invited contributor who chooses the paper | Authors and contributors the team authorizes |
| Who runs it | Anyone | The team, under the version's fixed protocol |
| Contributor AI use | D-039, D-042, identical for both | Same; exposure is logged (Rule 10) |
| Leaves the set | Never | Only when an event retires it (§7) |

**The unit is the paper, not the task.** All tasks from one paper go to the same set. A published development task reveals the paper's correct implementation, which would make an evaluation task from the same paper easier to solve by comparison.

## 4. Discovery and access on the site (the only change to the MVP)

**First version (D-047): invitation only.** Scored papers are offered by assignment; only demo or development papers can be "open to all contributors", which the site now enforces. The listing and request step below come in a future version.

The pool already exists (D-044, P-060). In that future version, two changes:

1. **"Open to all contributors" becomes "Listed in the pool".** A listed paper shows its citation, its set (development, or evaluation with access on request), and a short note of the contributions it needs (for example, "author review", "expert review", "replication package"), taken from an optional field in the paper configuration.
2. **Choosing depends on the set.**
   - **Development paper:** "Choose this paper" works as now.
   - **Evaluation paper:** the button reads "Ask to work on this paper". It records a request; the contributor sees only the citation until the team authorizes. The team authorizes in the administration pages (one action, logged), and the paper then works like any other assigned paper.

*Implementation, when it comes:* one field on Assignment (requested or authorized; everything the team creates is authorized), one admin action, one page state, and the access check that already exists. About half a day. The current internal values `scored` and `demo_or_development` can stay, with new labels on screen; renaming them can wait for the next schema version.

**Public discovery** (a read-only page of listed papers for economists without an invitation, with a way to ask for one) belongs after the server exists (M6). The site stays invitation-only until then.

## 5. Which validated papers become development and which evaluation

**First version (D-047):** the development set is the demo papers only (D-024, V5, and the fictional examples); every invited contributor's paper stays private, in the evaluation set. Authors may choose public release in a future version. The steps below apply once the lead sets a development share above zero.

1. **Same bar for both.** The draw happens after validation, so every paper passes the same review (construction protocol Stage 7, including the blind independent reviewer, rubric PR-2).
2. **Pre-stated exceptions go to development before the draw:** demo papers (D-024, V5); papers whose planted errors or solutions are already public; and any paper whose author asks for public release. These are decided without looking at model results.
3. **The rest are drawn at random within each admitted batch,** stratified by field, with a share set by the research lead (for example, one third development). The seed and the outcome are recorded in the decision log with the date.
4. **Never moved because of scores.** An evaluation paper moves to development only by retirement (§6) or a documented defect, never because models did well or badly on it. This is Rule 8's existing "designation before any evaluation run", made mechanical.

*Why random:* calibration trials (rubric DF-3) show how models do before admission, so any designation by judgment could, even unintentionally, keep the tasks models fail. TBS's first release was cut "after the evals decide what to cut" (R13), although its own guide warns against adversarial filtering. A recorded draw removes the question.

## 6. Minimum safeguards for official scores

| Safeguard | Already decided | To add |
|---|---|---|
| Expert validation | D-039 (expert decides; second check without AI for AI-drafted, AI-reviewed items); construction protocol Stage 7; rubric PR-2 | Nothing |
| Test isolation | D-041 (Rule 9) | Nothing |
| Exposure tracking | D-040 (Rule 10): exposure log, pinned model versions and release dates, separate reporting | The task build date (M2, D-044) |
| Fixed evaluation conditions | VVP §8: at least five trials, confidence intervals by bootstrap over tasks | A protocol per evaluation version, enforced by the harness rather than by prose, as Terminal-Bench does: pinned harness, instruction, tools, network allowlist (the model's API only), time and cost limits, trials, sampling settings, judge model if any. Every model in a comparison runs under the same protocol |
| Versioned task sets | Construction protocol Stage 8: each release is frozen; withdrawals take effect at the next version | A manifest per evaluation version (task IDs and SHA-256 of each instruction, package, verifier and rubric), with the version's protocol. **The manifest's hash is published before the first official run (D-047)**, so anyone can later check that the set was not changed after seeing results. No major benchmark does this yet (R13); it costs one line in a release note |
| Who runs | — | Only the team runs official evaluations, through providers' APIs (D-038). Self-reported runs on the evaluation set do not count |
| Defects found after results | — | A defect (wrong verifier, ambiguous instruction) is judged by a reviewer without seeing per-model results where possible, recorded, and the task is removed for all models in a dated erratum; the fix enters the next version. Terminal-Bench's rule fits: a fix that changes only grading regrades the saved runs; one that changes what the agent sees means re-running |

## 7. Continuous updates and official comparisons

*Revised 2026-11-08 after the research lead asked why evaluation tasks should not be kept longer. The earlier recommendation, retiring each paper after two versions, followed benchmarks that harvest items cheaply; it does not suit DeepEcon.*

- **Keep evaluation papers for as long as they stay informative.** Expert-built benchmarks keep their protected sets for years: ARC-AGI-1's private set reportedly from 2020 to 2024, and HLE, FrontierMath, and METR keep and revise theirs [S] (R10, R13). Fast rotation belongs to benchmarks that harvest new items cheaply from contests or GitHub (LiveBench, LiveCodeBench, SWE-rebench). DeepEcon's tasks take expert time and its papers appear slowly, so retiring them early would waste the scarcest input.
- **Retirement is triggered by events, not by age:**
  - its answers become public: at once (D-040);
  - a defect that cannot be repaired: at the next version;
  - a new generation of the evaluation set replaces the old one, when enough new papers exist, as ARC moved from ARC-AGI-1 to ARC-AGI-2. The research lead decides when.

  A retired paper joins the development set unless its author asked to keep it private.
- **Age is not the real limit; exposure is.** Rule 10 reports a model's scores separately on tasks whose material reached that model's **developer** before the model's release. A task run through a developer's own API is exposed for that developer's later models however long it is kept. Two ways to keep long-lived tasks clean, without changing the rule:
  - **Run open-weight models through third-party API hosts.** The host receives the task; the model's developer does not, so the task stays clean for the developer's later models. This fits D-038 (models through APIs, no self-deployment). *(assessment)*
  - **Run closed models through cloud platforms whose terms keep customer traffic from the model's developer**, if such terms exist and hold. This is unverified [U] and must be checked per platform and dated before the first official run (O-039). It rests on the host's terms, but it removes the developer, which is the party Rule 10 is about.

  Where a developer does receive the tasks through its own API, scores are reported separately, as agreed.
- **A measurable check, not a promise.** Track the gap between scores on exposed and never-exposed tasks, as ARC tracks the gap between its public and semi-private sets [S]. With few tasks it detects only large effects (Rule 10's illustration: about ±25 percentage points with 30 tasks a side), so it is a warning signal, not proof of cleanliness.
- **Versions.** The evaluation set is released as numbered versions (for example `eval-2027.1`). A version adds the papers validated since the last one; older papers stay unless an event retires them. The cadence follows the supply of validated papers, not a calendar.
- **Comparisons are within one version and one protocol,** using the tasks clean for every model compared (D-040), with full-set scores and exposure labels beside them. A model whose API has been withdrawn is reported on the versions it was run on, never imputed.

## 8. What changes in the existing decisions and plan

| Item | Change proposed | Why |
|---|---|---|
| D-040, Rule 8 | "Scored" becomes **evaluation**; "demo or development" becomes **development**. Development tasks **are** published with solutions and grading tools (now "may be"). Designation is per paper, by the recorded draw of §5. Retired evaluation tasks join the development set | Principles 2 and 3 |
| D-022, X-009 | Contributors may browse listed papers (citation and contribution needs); access to evaluation materials needs authorization. Search stays out of the MVP | Principle 1; discovery is not access |
| P-060 (a), (b) | "Open to all contributors" becomes "listed in the pool"; access follows the set | §4 |
| P-061 | Withdrawn | Replaced by this proposal |
| P-036, P-043 | Contributors see the citations of listed papers, and task materials only of development papers they choose or evaluation papers they are authorized for | §4 |
| Implementation plan | M2 gains the request-and-authorize step (about half a day) and the build date. A post-MVP milestone "E1: first evaluation version" covers the manifest, the protocol, and the first official runs | Keeps the MVP small |
| Notice (MVP §3 step 1) | Says that a development paper's tasks, solutions, and grading tools are published, and an evaluation paper's are not | Informed consent (D-042) |
| Construction protocol Stage 8 | The release editor runs the draw and freezes each version | §5, §6 |

**Unchanged:** AI-assisted contribution with disclosure and expert validation (D-039); privacy and consent (D-042); evaluation of all models through APIs and no local deployment (D-038); isolation (D-041); one link and one paper at a time (D-044, D-045); the deferred held-out tier (O-038). There are no task tiers with different AI rules.

## 9. Trade-offs and choices for the research lead

*Answered on 2026-11-08 (D-047): 1 (only demo papers in the first version), 2 (authors' choice in a future version; invited contributors' papers private for now), 4 (invitation first; request and authorization later), and the published manifest hash. Item 3 is answered from practice in §7; the recommendation was revised on 2026-11-08 to keep evaluation papers until an event retires them.*

1. **The share of development papers.** More development papers make DeepEcon more useful for building systems; fewer evaluation papers widen the confidence intervals (Rule 10's illustration: about ±25 percentage points with 30 tasks a side). Early on, with few papers, a small development share (or only the demo papers) may be wise.
2. **Authors' choice.** Letting an author send their paper to the public set before the draw respects authors and is harmless to validity, since it happens before any results; letting them keep it out of the public set is equally harmless. Either way it must be decided before the draw.
3. **Evaluation papers and contributors' AI use.** With one rule set for everyone, a contributor's AI use on an evaluation paper exposes its items to that provider; it is logged and reported, as already agreed. The alternative, different rules for evaluation papers, is what the lead asked to avoid.
4. **Retirement:** events rather than a fixed period (§7, revised 2026-11-08); the lead decides when a new generation replaces the evaluation set.
5. **Authorization workload.** Each request to work on an evaluation paper needs a team decision; with few contributors this is small.
