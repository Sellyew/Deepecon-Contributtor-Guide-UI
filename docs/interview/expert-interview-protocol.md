# Deliverable 3 — Expert Interview Protocol (model-agnostic specification)

| | |
|---|---|
| **Status** | **Proposed** protocol v0.2.1 (2026-11-05). Not yet reviewed by the research lead; not yet tested with economists. v0.2.1 integrates two independent reviews of 2026-11-05 (econometric; benchmark methodology); changes are listed in §17. |
| **Built on** | Sant'Anna's `interview-me` skill ([reading notes](../research/reading-notes/interview-me-skill.md)); the Critical Decision Method and Applied Cognitive Task Analysis; evidence on AI-led interviews, sycophancy, and expert deference ([evidence note R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md)); Bercovich (2026), *Good Benchmarks*, §9 |
| **Implements** | Stages 2–4 of the [construction protocol](../methodology/benchmark-construction-protocol.md); writes records defined in the [schema](../../schemas/README.md) |
| **Architecture independence** | One protocol, two hosts: a Claude Code skill (Option B) or a server-side orchestrator (Option A). Host-specific notes are confined to §14. |

---

## 0. The central risk this protocol is designed around

An AI interviewer can shape what an expert "knows". In a 2026 Anthropic study, 50 analysts with causal-inference experience worked with a Claude agent that had been given a secret, randomly assigned lean on four design choices, each with two defensible options, among them difference-in-differences versus levels adjustment ([R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) §3.4) [P-page]:

- the analysts followed the agent's lean **86%** of the time;
- **77%** repeated the agent's arguments, sometimes verbatim, but only **15%** credited the agent;
- self-rated confidence and ownership did **not** distinguish those who followed from those who did not.

The study has no human-only control and covers one task and one model, but it is the closest evidence to our situation. Three consequences shape everything below:

1. Asking for the contributor's view *first* is necessary but not sufficient.
2. "Who said it first" and self-reported ownership under-measure AI influence.
3. Influence must be **measured by design**: timestamped free recall, exposure tracking, and seeded controls.

*Good Benchmarks* §9 reaches the same conclusion from benchmark practice: authors who agree with whatever an AI says "end up hill climbing toward a hard task that is too artificial."

## 1. Purpose and non-purposes

**Purpose.** Help an experienced economist make explicit what they know about a published paper's *critical research decisions* and the *plausible, consequential mistakes* those decisions guard against. Turn that knowledge into a contributor-approved **candidate dossier** from which verifiable tasks can be built.

| ID | Objective |
|---|---|
| O1 | Elicit, in the contributor's own words, the critical decisions behind 1–3 target analyses and why they were necessary. |
| O2 | Elicit plausible failure modes for those decisions, each with a realism warrant: observed where, or hypothetical. |
| O3 | Establish each failure mode's mechanism, validity layer, a **pre-registered** predicted consequence, and a test that distinguishes correct from flawed. The contributor's view of whether the mistake is established or contested is recorded as a claim (§13). |
| O4 | Operationalize at least one failure mode as a code-level change; run it when execution is available; compare observed with predicted consequences. |
| O5 | Sketch candidate tasks: what the agent would deliver, what would convince the expert, which alternatives deserve credit. |
| O6 | Produce a dossier with complete provenance and measured AI influence, signed off by the contributor. |

**Non-purposes.** The interview does not:
- design the final verifier;
- write the final agent-facing instruction (it must be human-authored);
- settle whether a mistake is established or contested (independent experts do, §13);
- evaluate the paper's overall quality or journal placement (X-001);
- generate new research;
- certify anything as validated.

## 2. Interviewer conduct

1. **Peer methodologist, not examiner.** The tone is that of a productive discussion between experienced economists (brief §5.1).
2. **The expert is the authority** (D-008), but the interviewer does not abandon evidence. A disagreement grounded in the paper or code is stated with its location, never retracted without new evidence, and, if unresolved, recorded for the shepherd rather than settled by persuasion.
3. **No evaluative remarks.** No praise ("great point"), no judgment of answers. AI interviewers' most common guideline violations are judgemental remarks and missed follow-ups [P-page, R7 §3].
4. **Short turns.** About 120 words at most per interviewer turn, except summaries. One focused question per turn; two only when tightly linked. Long, sophisticated interviewer turns would reproduce the brief's failure mode #3 inside the interview.
5. **Contributor first, always.** The contributor's own ideas are recorded before any suggestion or code pointer (§4, §7).
6. **Ask before pointing.** Ask the contributor where and how a decision is implemented *before* showing code. A question aimed at a specific line is itself a suggestion (R7, risk R3).
7. **Honesty.** No invented citations or code facts. Say "I am not sure". Never describe anything as validated.
8. **No template-filling, no quotas.** "There is no realistic mistake here" is a complete answer. Empty fields are recorded as "not elicited".

## 3. Inputs and pre-reading

**Inputs:** paper; replication package (code, documentation, and data only if non-restricted and permitted); contributor profile (role, relationship to the paper, pathway); language; time budget; whether a research assistant takes part.

| Pre-reading product | Contents | Use |
|---|---|---|
| Design map | Research question, design, candidate estimands, data, main specifications, candidate target analyses, with uncertainty markers | Shown in S1 **after** the contributor's own summary |
| Code map | Pipeline order, entry points, sample construction, estimation, inference, with file and line references | Shown only **after** the contributor has described the pipeline (P-TIMELINE) and located decisions (P-LOCATE) |
| Decision-point notes | Detected choices (filters, merges, fixed effects, clustering variables, weights, timing variables) | **Private.** Never used to steer the contributor before free recall; used later only through the gated suggestion process (§7) and for evidence-based disagreement about statements already made |

## 4. State model, free-recall lock, and exposure tracking

The interviewer maintains, and persists after every turn:

- **Session state:** stage, focus item, turns, elapsed time, fatigue signals (answer length, rate of "not sure").
- **Dossier:** schema entities, each field with a status of `empty`, `vague`, `sufficient`, `contradicted`, `parked`, or `not_elicited`.
- **Free-recall lists.** For each target analysis, the contributor's **unaided** list of critical decisions (S2) and of plausible mistakes (S3), timestamped before any suggestion, code pointer, or design-map detail about those decisions.
- **Exposure flags.** Every item records `exposure`:
  - `pre_exposure` — stated before any related suggestion or pointer;
  - `post_exposure` — stated afterwards, with the IDs of the preceding suggestions or pointers.

  These flags record the contributor's exposure to AI content. They are distinct from the *exposure log* of hidden material, which records which models saw hidden-tier material ([verifier protocol](../methodology/verifier-validation-protocol.md) §10; rubric LK-5).
- **Suggestion ledger.** Every suggestion offered: its source entry, the order in which the options were presented, whether it was a known-valid control (§7), and the contributor's disposition and reasoning.
- **Open issues:** contradictions and uncertainties.
- **Checkpoints:** stage summaries with the contributor's accuracy rating; sessions resume from the last one.

**Influence metrics** (computed, not self-reported):

| Metric | Meaning |
|---|---|
| LLM-originated share | Share of endorsed items first stated by the model |
| Post-exposure share | Share of endorsed items first stated after a related suggestion or pointer |
| LLM-influenced share | Post-exposure items whose wording is close to a logged suggestion or interviewer statement (text similarity above a validated threshold; see below) |
| False-endorsement rate | Share of known-valid controls that the contributor endorsed as mistakes, counting only endorsements that an independent economist has adjudicated as false |

**Computation rules.**

- **Recall on pre-exposure items only.** Wherever recall of a known-issues key is measured (protocol evaluation, §15; the pilot), an item counts as recalled only if it was stated before any related suggestion or pointer. Post-exposure items are reported separately.
- **Validated similarity.** Economists share technical vocabulary ("not-yet-treated", "negative weights"), so wording can be close without any influence, and similarity scores are not comparable between English and Chinese. The threshold is therefore validated in each interview language against blinded double human coding of influence, with items from suggestion-off decisions (§7) as the baseline.
- **Adjudicated controls.** Whether a control is valid depends on context, and an original author's objection to one may be correct. Each endorsement of a known-valid control is adjudicated by an independent economist before it counts as false.
- **Pooled thresholds.** One contributor's share can rest on one or two items. Thresholds that judge the protocol or a workflow (the pilot's decision rules) are applied to counts pooled across participants and reported with exact (Clopper–Pearson) 95% confidence intervals. For a single contribution, the provisional thresholds of rubric PR-1 (an LLM-influenced share above 50% of endorsed items; false endorsement of more than a quarter of known-valid controls) trigger shepherd review.

## 5. Stages

Stages are **adaptive, not linear**: the policy in §6 can return to an earlier stage. They refine the brief's sketch by adding setup and consent (S0) and merging consequence analysis with classification (S4).

**Sessions are capped at 45–60 minutes.** A typical contribution takes three or more sessions. Work that needs more time, such as one arm of the pilot, is split into several sessions, each resumed from the last checkpoint; no single session runs longer. All evidence on AI interviews comes from short sessions, and satisficing grows with fatigue ([R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) P12).

### S0 — Setup and consent

- Language (English or Simplified Chinese); role; relationship to the paper; pathway; materials; time budget.
- **Data-flow disclosure:** which model provider receives which content, under which account terms. Raw restricted or confidential microdata must not be shared (P-015).
- **Account terms for hidden material.** The interview itself creates hidden-tier material (failure modes, flawed variants, answer keys), so a session runs only under commercial terms that exclude training, with zero data retention where available. A consumer account is not sufficient, even with the training opt-out ([verifier protocol](../methodology/verifier-validation-protocol.md) §10). Each session is entered in the exposure log (rubric LK-5).
- **Disclosure embargo:** the contributor agreement embargoes disclosure of the hidden material (verifier protocol §10).
- **Confidentiality:** describe patterns, never identifiable manuscripts under review; transcripts are treated as sensitive and potentially re-identifying.
- **Interview design disclosure:** "Later I may raise alternatives for you to judge. Some will be choices that are perfectly valid in this setting; your judgment, not agreement, is what helps."
- Consent to transcript retention; credit preference.

### S1 — Paper and design understanding

- **Contributor first** (P-RQ): research question and identifying variation in the contributor's own words; then "Which result carries the paper?"
- Then the design map, with uncertainty markers, for correction.
- **Exit:** 1–3 target analyses with estimands, confirmed by the contributor.

### S2 — Critical decisions (Critical Decision Method sweeps)

1. **Free-recall lock** (P-RECALL): the contributor's unaided list of decisions that required judgment, timestamped.
2. **Timeline** (P-TIMELINE): raw data to estimate in three to six steps, marking where judgment was needed — *before* the code map is shown.
3. **Deepening, per decision:**
   - cues (P-CUE): what showed the obvious approach was wrong;
   - options and basis (P-OPTIONS): alternatives considered and why they were rejected;
   - self-monitoring (P-SELFMON): how the implementation was checked;
   - location (P-LOCATE): where the decision lives in the code, from memory, before the interviewer shows it.
4. **Credibility criteria** (brief §3.4): "What about this decision made the result convincing to a demanding referee?" Recorded as rationale, never as a journal-placement prediction.
5. **Recording format:** a cognitive-demands row per decision — *difficult element · why difficult · common errors · cues and strategies* — adapted from Applied Cognitive Task Analysis.

**Exit:** 2–6 decisions with rationale and code anchors, ranked by the contributor.

### S3 — Failure modes

1. **Free-recall lock:** for each top decision, the contributor's unaided list of plausible mistakes, timestamped. All of these locks are taken before the first suggestion of the contribution (§7).
2. **Novice hypothetical with permission** (P-RA): the permission sentence comes first.
3. **Realism warrant, mandatory** (P-SEEN). Each item records `observed_in_practice`: own project, refereeing (pattern only), RA supervision, published literature, or hypothetical. Hypothetical-only items are flagged.
4. **Knowledge-audit probes:** anomalies that would reveal the mistake (P-NOTICE); software defaults that could produce it silently (P-DEFAULT).
5. **Gated suggestion phase** (§7), only after all locks, and only if the session's design includes it. In the pilot, suggestions are randomized over pre-registered decisions (§7, item 9; Deliverable 8).
6. **Triviality** is judged by a separate checker (§10), not by the interviewer in conversation, to avoid feedback sycophancy.

**Exit:** at least one endorsed failure mode with a stated mechanism, or a recorded decision that the contributor sees no realistic mistake.

### S4 — Consequences and classification

1. **Pre-registered prediction** (P-PRED), timestamped before any flawed code runs. Coarse categories, including a change in the standard error or confidence interval alone, and optionally three quantiles. Predictions are information, never a score of the expert.
2. **Mechanism laddering** (P-WHY) until the mechanism is stated in terms of an estimand, an assumption, a measurement property, or an inference property.
3. **Validity layer, classified by the contributor first** from a neutral list: implementation fidelity (computational correctness), measurement validity, statistical validity, identification validity, interpretation validity. The contributor names one primary layer and any secondary layers; static TWFE under staggered adoption, for example, is both a statistical and an estimand–estimator problem ([verifier protocol](../methodology/verifier-validation-protocol.md) §9). The interviewer then notes any disagreement, with reasons.
4. **Status as a claim** (P-STAT, P-REF): the contributor's view (established, conditional, or contested), with references. This is **recorded, not settled**: status is decided by independent classification (§13).
5. **Similar-but-valid approaches** (P-VALID) and the **one-sentence-fact probe** (P-1FACT).
6. **Evidence bundle as the exit condition.** For each failure mode:
   - the mechanism;
   - the realism warrant;
   - a failing case or a test that distinguishes correct from flawed (P-DETECT);
   - a cited rule or standard.

   Without all four, the item stays a candidate.

### S5 — Operationalization (may be asynchronous with a research assistant)

- Locate the change; draft the minimal diff **in a separate location** (originals are never modified, D-011). The contributor approves that the diff represents their failure mode.
- Run reference and variant where execution is available. Compare observed with predicted consequences. Discuss mismatches openly: misunderstanding, data-equivalence (the flawed procedure gives nearly the same number on these data; [verifier protocol](../methodology/verifier-validation-protocol.md) §2, type 2), or a new insight. Preview robustness where feasible.
- Without in-session execution: an approved hand-off specification for the research assistant or shepherd.

### S6 — Task design and quality

- Present the task types neutrally, with what each would measure.
- Ask: what the agent should deliver; what evidence would convince the expert; which other approaches deserve credit.
- The contributor or shepherd writes the agent-facing instruction. The interviewer may help tighten it and runs a **leakage check**.
- Brief rubric self-assessment (RV-1 to RV-4). The P-1FACT answer is recorded as a prediction for rubric SP-3, which is tested later with agent trials (hint ladder, verifier protocol L10).

### S7 — Review and sign-off

- The dossier is shown in the contributor's language. Each item carries a provenance badge and an exposure flag; influence metrics are shown.
- The contributor can edit, reject, or withdraw anything, and gives a 1–4 accuracy rating for each stage summary.
- An English working translation, labelled machine-generated, is added if needed (D-007).
- Attribution and consent are confirmed; the package is exported or submitted.

## 6. Adaptive question-selection policy

At each turn, choose the single most valuable next question:

1. If the contributor asked something or raised a concern, respond briefly first.
2. If a **free-recall lock** for the current stage is not yet recorded, take it.
3. If the focus item has an **open contradiction** or flagged uncertainty, resolve it.
4. Else ask for the highest-priority missing **gating field** (the evidence bundle in S4).
5. Else, if the mechanism is **vague**, ladder.
6. Else **move focus** — "one complete, then breadth". First take the S3 free-recall locks for all ranked decisions, so that no suggestion precedes any lock (§7). Then take the highest-ranked decision through S3–S4, so at least one complete candidate exists early; then sweep for breadth; then return to operationalize. Decisions that surface only after the first suggestion are recorded as post-exposure.

**Rhythm.** At most two questions per turn. Summarize every five to seven turns and at every stage exit, in the contributor's own words, with an accuracy rating. Check time and energy roughly every 20 minutes. Propose a checkpoint by 45–60 minutes.

**Question hygiene.** Never ask what the artifacts answer. No double-barrelled questions. No yes/no or agree/disagree endorsements: offer substantive alternatives with reasons. No presupposition: ask "Is there a realistic way this could go wrong?", not "What is the error?". Rotate the order of options.

## 7. Suggestions: a gated, measured exception

The open AI-interview platforms forbid suggesting answers altogether, "not even a broad theme" [P-page, R7 §3.2]. This protocol allows a narrow exception, because the AI's reading of the code can surface candidates an expert would miss. The deference evidence (§0) means the exception must be controlled and measured:

1. **After all locks only.** No suggestion is offered until every free-recall lock has been recorded: the S2 list of decisions and the S3 list of mistakes for each ranked decision. A suggestion on one decision would otherwise prime free recall on the next.
2. **Few.** At most three per decision and about ten per session.
3. **Vetted sources only.** Each suggestion cites an entry in the **pitfall taxonomy**, which a named econometrician has signed off with citations. Unvetted entries cannot seed suggestions. Suggestions from the interviewer's code reading are labelled as such and limited to the same format.
4. **Both sides argued.** The case that the choice would be a mistake here *and* the case that it would be acceptable here, in rotated order (P-SUGG).
5. **Known-valid controls.** Some suggestions are vetted valid alternatives, as disclosed at S0. Each endorsement of one is adjudicated by an independent economist before it counts as false (§4). The false-endorsement rate is reported.
6. **Endorsement needs the evidence bundle.** A bare "yes" is recorded as a weak endorsement and does not enter the scored path.
7. **No pressure.** A rejected suggestion is never raised again in different words.
8. **Measured.** Every suggestion goes into the ledger. The metrics in §4 are computed and shown to the shepherd; a high LLM-influenced share triggers deeper review (rubric PR-1).
9. **Randomized where the design calls for it** (the pilot, Deliverable 8). Suggestions are randomized over decisions pre-registered from the design map, not over decisions the contributor generates during the interview. The assignment is fixed before the first session and balanced, so that each pre-registered decision has suggestions on for half the participants. Suggestions are offered only for decisions assigned "on", and only after all locks (item 1); the suggestion-off decisions are the baseline for the influence measures (§4).

## 8. Probe library

Probe identifiers are language-independent; phrasings are localized assets ([bilingual design](../architecture/bilingual-design.md)). On first use in Chinese, technical terms keep the English term in parentheses. **All phrasings must be pretested with cognitive interviews** (three to five economists per language) before the pilot (Willis 2005 [S]).

**The Chinese phrasings are unreviewed drafts.** Bilingual economists have not yet reviewed them, nor the seed glossary terms they use (bilingual design, appendix). This includes the P-PRED option on the standard error or confidence interval added in v0.2.1 (标准误 and 置信区间 as in the glossary; 估计值 as in the existing probes).

| ID | Purpose | English | 简体中文 |
|---|---|---|---|
| P-RQ | Own summary | In your own words, what is the main question, and what variation identifies the effect? | 请用您自己的话概括：这篇论文回答的核心问题是什么？识别效应依赖的是哪一种变异？ |
| P-RECALL | Free-recall lock | Before I show you anything from the code: which decisions in getting this result right required real judgment? Please list them in your own words. | 在我展示任何代码内容之前：要得到这个结果，哪些决策需要真正的判断？请用您自己的话列出来。 |
| P-TIMELINE | Contributor's timeline | Walk me from the raw data to the estimate in three to six steps, and mark where judgment was needed. | 请用三到六个步骤，带我从原始数据走到最终估计值，并标出哪些环节需要判断。 |
| P-HARD | Incident | Which part of getting this result right took the most judgment? Was there a moment when the results changed with a choice? | 要得到这个结果，哪个环节最需要判断？是否有某个时刻，结果随着某个选择而改变？ |
| P-CUE | Cues | What told you the obvious approach was wrong? What did you see in the data or the output? | 是什么让您意识到显而易见的做法是错的？您在数据或输出中看到了什么？ |
| P-OPTIONS | Options and basis | Which alternatives did you consider, and on what basis did you reject them? | 您考虑过哪些替代做法？依据什么排除了它们？ |
| P-SELFMON | Self-monitoring | How did you check that the code implements what the paper says? | 您是如何核实代码确实实现了论文所述内容的？ |
| P-LOCATE | Ask before pointing | As you remember it, where in the code is this decision implemented? | 据您回忆，这个决策在代码中的哪个位置实现？ |
| P-RA | Novice hypothetical, with permission | If there is no realistic way to get this wrong, that is a complete and useful answer. Otherwise: suppose a capable research assistant overlooked this issue. What apparently reasonable approach might they take instead? | 如果这里不存在现实的出错方式，这本身就是完整且有用的回答。否则：假设一位能干的研究助理忽略了这个问题，他们可能会采用哪种看似合理的做法？ |
| P-SEEN | Realism warrant (required) | Where have you seen this mistake: in your own project, while refereeing (please describe the pattern only, never a manuscript under review), when supervising research assistants, in the published literature — or is it hypothetical? | 您在哪里见过这种错误：自己的项目中、审稿时（请只描述模式，切勿涉及审稿中的具体稿件）、指导研究助理时、已发表文献中——还是仅为假设？ |
| P-NOTICE | Anomalies | What pattern in the sample size, standard errors, signs, or event-time coefficients would make you suspect this mistake? | 样本量、标准误、符号或事件时间系数出现什么样的模式，会让您怀疑存在这个错误？ |
| P-DEFAULT | Software behaviour | Which software default or package behaviour could produce this silently? | 哪些软件默认设置或程序包行为可能在不知不觉中导致这个问题？ |
| P-PRED | Pre-registered consequence | If we ran that version, which is closest: immaterial; changes significance; changes the sign; changes the magnitude materially without changing the sign; changes the standard error or confidence interval without moving the estimate; something else? If you like, also give a low, middle, and high guess for the estimate. | 如果按那种做法运行，哪种情况最接近：影响不大；改变显著性；改变符号；幅度显著变化但符号不变；改变标准误或置信区间但估计值不变；其他？如愿意，也可给出估计值的低、中、高三个猜测。 |
| P-WHY | Mechanism laddering | Why would it move in that direction rather than the other? | 为什么会朝这个方向变化，而不是相反方向？ |
| P-STAT | Status (recorded as a claim) | Would a well-informed econometrician defend that alternative here? Under which assumptions? | 一位了解前沿的计量经济学家会在这里为那种做法辩护吗？需要满足哪些假设？ |
| P-REF | Standard of evidence | Which reference would you point a skeptical referee to? | 如果审稿人表示怀疑，您会请他参考哪篇文献？ |
| P-VALID | Similar but valid | Which nearby choices would be perfectly fine here? | 哪些看起来相近的做法在这里其实完全可以接受？ |
| P-CODE | Operationalization | Which part of the code would need to change to reproduce this mistake? | 要复现这个错误，需要修改代码的哪一部分？ |
| P-DETECT | Distinguishing test | How could an independent verifier tell the correct implementation from this mistake? | 独立的验证者如何区分正确的实现与这个错误？ |
| P-1FACT | One-sentence-fact risk | If a task instruction told the agent this fact, would the problem become easy? | 如果任务说明直接告诉智能体这一点，问题会不会变得很容易？ |
| P-SUGG | Balanced suggestion | Some implementations of this design make a different choice: [X]. The case that it would be a mistake here: [A]. The case that it would be acceptable here: [B]. Which is closer to right for this paper — or is it not relevant? Please explain in your own terms. *(Order of A and B rotated.)* | 在类似研究设计中，有些实现采用了不同的选择：[X]。认为这在本文中是错误的理由：[A]。认为这在本文中可以接受的理由：[B]。哪一种更符合本文的情况——还是两者都不相关？请用您自己的话说明。*（A、B 顺序轮换。）* |
| P-SUM | Summary with accuracy rating | Here is my summary, using your own words where I could: … How accurate is it, from 1 (misleading) to 4 (accurate)? What should change? | 以下是我的总结，尽量使用了您的原话：…… 准确度如何？请从 1（有误导）到 4（准确）打分。需要修改哪些地方？ |
| P-DISAGREE | Evidence-based disagreement (only about statements already made) | My reading of the code differs: at [file:line] it appears that … Could you check? | 我对代码的理解有所不同：在[文件:行号]处似乎是……能否请您核对一下？ |

## 9. Error-discovery procedures

| Procedure | Source of candidates | When used |
|---|---|---|
| Decision-anchored | The contributor's free-recall decisions (S2) | Always first |
| Experience-anchored | Errors the contributor made, caught, refereed, or supervised (Path B: "What did you learn that is not in the paper?") | S3, before any suggestion |
| Anomaly-anchored | What patterns in outputs would reveal a mistake (P-NOTICE) | S3; also yields metamorphic checks for verifiers |
| Referee-perspective | "Where would a demanding referee look?" | S3 |
| Artifact-anchored | Interviewer's decision-point notes | Gated suggestion phase only (§7) |
| Literature-anchored | Vetted pitfall taxonomy | Gated suggestion phase only (§7) |

## 10. Separate roles and in-interview checks

The conversational interviewer is **not** the judge of validity, the recorder, or the suggestion generator (R7 P7):

| Role | Implementation | Sees the conversation? |
|---|---|---|
| Interviewer | The conversational model | Yes |
| Recorder | Deterministic logging of turns, timestamps, exposure, provenance | Yes (verbatim) |
| Suggestion generator | Separate model call restricted to vetted taxonomy entries and decision-point notes; produces balanced P-SUGG items | Only the decision and the free-recall list |
| Checkers (citations, triviality, leakage) | Separate fresh-context calls | No; they see only the claims or drafts to check |

| Check | Trigger | Response |
|---|---|---|
| Vagueness | No estimand, assumption, measurement, or inference property in the mechanism | Ladder (P-WHY) |
| Triviality (checker) | Candidate looks like a coding slip without methodological content | Flag for the contributor and shepherd (X-002); never decided by the interviewer |
| Data-equivalence risk | Predicted or observed consequence small or data-dependent | Flag for discriminability work: hidden variants that separate the procedures (verifier protocol §2, type 2) |
| One-sentence-fact risk | P-1FACT answer is "yes" | Record as a prediction, to be tested by the hint ladder and the knowledge probe (verifier protocol L10; rubric SP-3); O-004 stays open |
| Inference-only consequence | P-PRED answer is a change in the standard error or confidence interval alone | Record. Materiality is judged by rubric RV-2 (criterion 2, the SE ratio or coverage; criterion 4 if significance changes), and the task's standard error and confidence interval are graded deterministically against conditional references (verifier protocol §4 item 7) |
| Leakage (checker) | Agent-facing draft reveals the error, method, or answer | Block and explain |
| Contradiction with artifacts | A statement conflicts with paper or code | P-DISAGREE |
| Influence | High LLM-influenced share or false-endorsement rate | Flag for shepherd review (PR-1) |
| Citation verification (checker) | Any literature claim | Fresh-context verification without the dossier (adopted from `interview-me`); unverified citations labelled |

## 11. Stopping conditions

- **Item level:** the S4 evidence bundle is complete, or the item is parked or withdrawn.
- **Session level:** checkpoint by 45–60 minutes; earlier on fatigue signals.
- **Overall:** stop when any of these holds:
  - (a) the contributor says they are done;
  - (b) 1–3 operationalized candidates exist;
  - (c) two consecutive breadth sweeps yield nothing new;
  - (d) fatigue signals persist after offering to continue later;
  - (e) in hosted deployments, a cost or turn budget is reached.
- **Never** prolong an interview to fill fields; "no realistic mistake here" is a valid outcome.

## 12. Outputs

1. The **dossier** as schema entities with field-level provenance and exposure flags.
2. **Stage summaries** in the contributor's language, each with an accuracy rating.
3. The **interview record**: turns linked to statements, the suggestion ledger, free-recall lists, influence metrics (§4), and usage metrics (duration, turns, tokens, list-price cost).
4. **Flawed variants** and run outputs where execution happened.
5. **Exposure-log entries** for the sessions: which hidden-tier material the interviewer and helper models saw, under which terms, and when (rubric LK-5).
6. A **package** for submission ([submission mechanisms](../architecture/submission-mechanisms.md)).

## 13. Human review requirements

| Who | What | When |
|---|---|---|
| Contributor | Confirms each stage summary with an accuracy rating; signs off; may edit, reject, or withdraw anything | During and at the end |
| Shepherd | Reviews the dossier, influence metrics, and flags; may schedule a follow-up | Within an agreed number of days |
| **Independent status classification** | Economists not involved in the contribution classify each failure mode (established / conditional / contested) **independently and blind** to one another, with reasons: one classifier for an item that matches a vetted-taxonomy entry with a canonical citation, two for a novel item. Each condition is verified by a recorded diagnostic on the evaluation data and on every hidden-variant family used for grading. A second round only with stated reasons; the default is "needs review" | After the materiality check and the first verifier rungs (rubric RV-2; verifier protocol L4, L7); feeds rubric GT-2 |
| Independent reviewers | Assess resulting tasks against the rubric | Construction Stage 7 |

The interviewer never marks content as validated. The contributor's status judgment is a claim; status comes from independent classification. This follows structured expert-judgment practice for contested questions: Cooke's classical model, SHELF, and Delphi [S]; see D-013.

**Research-assistant mode.** An economist and an RA can share a session (speakers attributed) or split it: the economist completes S1–S4 and S6–S7; the RA performs S5 from the hand-off specification. Provenance records who did what.

## 14. Implementing the protocol in either architecture

Host-independent assets, kept in [`protocol/`](../../protocol/) in Phase 5:
1. this specification;
2. **stage cards** (goals, gating fields, exit criteria, probe IDs);
3. the **probe library** with localized, pretested phrasings;
4. the **vetted pitfall taxonomy** (entries signed off by a named econometrician, with citations; also lists known-valid alternatives for use as controls). It is seeded from the 21-entry catalogue in [R8](../research/evidence/R8-replication-standards-and-econometric-pitfalls.md) §3, whose entries are not yet vetted, with the status corrections of an independent econometric review ([R8, Corrections](../research/evidence/R8-replication-standards-and-econometric-pitfalls.md#corrections-2026-11-05-independent-econometric-review); decision-log P-033):
   - the regression-discontinuity entry P10 is split into **P10a** global high-order polynomial (established), **P10b** conventional confidence interval at the MSE-optimal bandwidth (established), and **P10c** bandwidth choice, which is not a failure mode but a decision-space node;
   - **clustering by a discrete running variable** is added as established (P22);
   - **P12** (conventional standard errors in shift-share designs) becomes conditional on shock-based identification (P13);
   - **P14** (relying only on robust or clustered standard errors in randomized experiments) becomes contested or conditional;
   - **P15** (no multiple-testing correction) becomes conditional on how the family of tests is defined.

   Statuses are re-classified at each release against new methodological literature (verifier protocol L13);
5. the **EN–ZH glossary**;
6. output templates;
7. the [schema](../../schemas/deepecon-contribution.schema.json).

| Concern | Option B — Claude Code skill | Option A — hosted orchestrator |
|---|---|---|
| Interviewer | `SKILL.md` plus stage cards loaded on demand | Server-side system prompt assembled from the same assets |
| Recorder and state | Local dossier files written through a schema-validating helper that timestamps and tags exposure | Database records written through tool calls with the same validation |
| Suggestion generator and checkers | Separate subagents with restricted inputs | Separate model calls with restricted inputs |
| Execution (S5) | Local Stata, R, or Python with originals protected | Run kits (A1), staff execution, or hosted R/Python sandbox (A2) |
| Model access terms (S0) | Commercial no-training terms, with zero data retention where available, because sessions create hidden-tier material: project-provided access if O-018 permits, or the contributor's institutional commercial account; a consumer plan is not enough, even with the training opt-out | The project's commercial account, server-side, under the same terms |
| Packaging and validation | Shared validator and packager library | Same library, server-side |

**Model requirements.** Long context (paper plus code), reliable tool use, strong instruction following, and competence in both languages. Each model must pass the evaluation in §15 before it is approved.

## 15. Evaluating the protocol

Before any economist is interviewed, the protocol is evaluated the way a checker is evaluated ([R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md), principle P14):

1. **Baseline arm.** A generic interviewer prompt without this protocol, run on the same personas, so improvements are measured, not assumed.
2. **Manipulation check.** Confirm that each protocol rule actually changes behaviour (e.g., the suggestion gate).
3. **Replicates.** At least three runs per persona and model, with a variance gate.
4. **Personas.** Model-played economists with hidden scripts:
   - a persona that knows specific real failure modes, to measure recall (on pre-exposure items only, §4);
   - one holding a wrong belief, to see whether the interviewer challenges it with evidence;
   - one that pushes back on correct observations;
   - one attached to a favourite but invalid candidate;
   - one prone to deference, to measure how much the interviewer plants.

   The formats follow published sycophancy test sets [P-page].
5. **Qualified automated checks.** Every automated check (leakage, triviality, influence metrics) is tested on seeded defects and clean controls before it is trusted. The similarity threshold behind the LLM-influenced share is validated against blinded double human coding, with suggestion-off decisions as the baseline (§4).
6. **Transcript coding by two coders.** The coding scheme uses the categories from Wuttke et al. (guidance, judgement, follow-up, active listening, naturalness), plus leading-question and presupposition codes; agreement is reported.

Simulations test mechanics only; they are not evidence about real experts. The [pilot](../pilot/pilot-evaluation-plan.md) then measures real behaviour, including a suggestion phase randomized over pre-registered decisions (§7, item 9).

## 16. Versioning

`protocol_version` follows semantic versioning and is recorded in every interview record. A session started under one version finishes under it; dossiers move to a newer version only through an explicit migration. Changes are logged in the [decision log](../decisions/decision-log.md).

## 17. Changes

**v0.2.1** (independent reviews, 2026-11-05: econometric and benchmark-methodology reviews; aligned with [verifier protocol](../methodology/verifier-validation-protocol.md) v0.3.0):

- **P-PRED** adds the option "changes the standard error or confidence interval without moving the estimate" (schema category `changes_inference_only`); the check table records inference-only predictions. The Chinese phrasings are marked as unreviewed (§8).
- **Influence measures** (§4): recall computed on pre-exposure items only; the LLM-influenced share's similarity threshold validated against blinded double human coding, with suggestion-off decisions as the baseline; each endorsement of a known-valid control adjudicated by an independent economist before it counts as false; thresholds pooled across participants, with exact confidence intervals.
- **Suggestions** (§6, §7): all free-recall locks before any suggestion; randomization over pre-registered decisions from the design map, balanced so that each decision has suggestions on for half the participants.
- **Taxonomy seed corrections** (§14): P10 split into P10a, P10b, and P10c; clustering by a discrete running variable added as established; P12 conditional, P14 contested or conditional, P15 conditional; re-classification at each release.
- **Status classification** (§13) follows rubric GT-2: one classifier for vetted-taxonomy items with a canonical citation, two for novel items, after the materiality check and verifier rungs L4 and L7, with conditions verified on the graded data.
- **Exposure rules** (S0, §12, §14): sessions run under commercial no-training terms because they create hidden-tier material; consumer plans are not enough; sessions are entered in the exposure log; contributor agreements carry a disclosure embargo. The contributor's exposure *flags* (§4) are distinguished from this log.
- **Validity layers** (S4): one primary layer plus any secondary layers.
- **Terminology and gates aligned with the verifier protocol:** "data-equivalence" (verifier protocol §2, type 2) replaces "equivalent mutant" in S5 and §10; the P-1FACT answer is a prediction tested later by the hint ladder, not an in-interview SP-3 assessment (S6, §10).
- **Session length:** sessions are capped at 45–60 minutes; longer work, such as a pilot arm, spans several sessions (§5).

**v0.2.0** (from v0.1.0), driven by the evidence and critique in [R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) §6 (risk and improvement IDs refer to that note):

- Added §0, the deference evidence.
- **Free-recall locks, exposure tracking, and influence metrics** replace "who said it first" provenance alone (I-1, I-2).
- Suggestions redesigned: gated, few, vetted, two-sided, order-rotated, with known-valid controls (I-3, I-14).
- **Ask before pointing**; private decision-point notes no longer steer questions (I-4).
- Permission sentence and **mandatory realism warrant** (I-5).
- **S2–S4 restructured** around Critical Decision Method sweeps and an ACTA-style cognitive-demands record (I-6).
- **Evidence bundle** as the S4 exit (I-7).
- Status recorded as a claim and **classified independently** by at least two economists (I-8).
- The contributor classifies validity layers first; "measurement validity" added (I-9).
- Categorical predictions with optional quantiles (I-10).
- Conduct rules: no evaluative remarks, short turns, summaries with accuracy ratings (I-11).
- Separate roles (I-12).
- Sessions of 45–60 minutes (I-13).
- An evaluation suite with a baseline, replicates, and personas (I-15).
- Pilot randomization of the suggestion phase and ownership used only as an experience measure (I-16).
- Cognitive-interview pretest of the probe library (I-17).
- Confidentiality instruction (I-18).

## References for the elicitation methods

Verified at [S] level in [R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) §2.1. Specific probe lists attributed to these sources remain [U] until checked against the originals.

- Klein, G. A., Calderwood, R., & MacGregor, D. (1989). Critical decision method for eliciting knowledge. *IEEE Transactions on Systems, Man, and Cybernetics*, 19(3), 462–472.
- Hoffman, R. R., Crandall, B., & Shadbolt, N. (1998). *Human Factors*, 40(2), 254–276 (the subtitle varies across records; check the journal page before citing).
- Militello, L. G., & Hutton, R. (1998). Applied cognitive task analysis (ACTA): A practitioner's toolkit for understanding cognitive task demands. *Ergonomics*, 41(11), 1618–1641.
- Crandall, B., Klein, G., & Hoffman, R. R. (2006). *Working Minds: A Practitioner's Guide to Cognitive Task Analysis*. MIT Press.
- Willis, G. B. (2005). *Cognitive Interviewing: A Tool for Improving Questionnaire Design*. Sage.
- Schuman, H., & Presser, S. (1981). *Questions and Answers in Attitude Surveys*. Academic Press. Krosnick, J. A. (1999). Survey research. *Annual Review of Psychology*, 50, 537–567.
- Expert-judgment methods for contested questions: Cooke (1991); O'Hagan (2019), *The American Statistician* 73(sup1); Dalkey & Helmer (1963), *Management Science* 9(3).
- Herdağdelen, Joren & Tamkin (2026), "How AI agents shape experts' judgment calls", Anthropic [P-page].
