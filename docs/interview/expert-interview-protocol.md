# Deliverable 3 — Expert Interview Protocol (model-agnostic specification)

| | |
|---|---|
| **Status** | **Proposed** protocol v0.1.0 (2026-11-05). Not yet reviewed by the research lead; not yet tested with economists. |
| **Inspired by** | Sant'Anna's `interview-me` skill ([reading notes](../research/reading-notes/interview-me-skill.md)); knowledge-elicitation methods from cognitive task analysis ([evidence note R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md)); Bercovich (2026), *Good Benchmarks*, especially §9 |
| **Implements** | Stage 2–4 of the [construction protocol](../methodology/benchmark-construction-protocol.md); writes records defined in the [schema](../../schemas/README.md) |
| **Architecture independence** | One protocol, two hosts: a Claude Code skill (Option B) or a server-side orchestrator (Option A). Host-specific notes are confined to §14. |

---

## 1. Purpose and non-purposes

**Purpose.** Help an experienced economist make explicit what they know about a published paper's *critical research decisions* and the *plausible, consequential mistakes* those decisions guard against, and turn that knowledge into a contributor-approved **candidate dossier** from which verifiable tasks can be built.

**Objectives.**

| ID | Objective |
|---|---|
| O1 | Elicit the critical decisions behind 1–3 target analyses, with the reasons they were necessary. |
| O2 | Elicit plausible failure modes for those decisions, each with a realism warrant. |
| O3 | Establish each failure mode's mechanism, validity layer, established/conditional/contested status, and a **pre-registered** predicted consequence. |
| O4 | Operationalize at least one failure mode as a code-level change, run it when execution is available, and compare observed with predicted consequences. |
| O5 | Sketch candidate tasks: what the agent would deliver, what would convince the expert, which alternative approaches deserve credit. |
| O6 | Produce a dossier with complete provenance, signed off by the contributor. |

**Non-purposes.** The interview does not: design the final verifier (the shepherd does); write the final agent-facing instruction by itself (*Good Benchmarks* §9; it must be human-authored); evaluate the paper's overall quality or journal placement (X-001); generate new research ideas; or certify anything as validated.

## 2. Interviewer stance

1. **Peer methodologist, not examiner.** The conversation should feel like a productive methodological discussion between experienced economists (brief §5.1).
2. **The expert is the authority** (D-008). The interviewer may disagree, citing evidence ("At `analysis.do`, line 212, the clustering variable appears to be `county_id`; you mentioned state-level clustering. Could you help me reconcile these?"), but it never insists, and it records the disagreement.
3. **Evidence first.** Read the paper and the code before asking. Never ask the expert what the artifacts already say; ask what the expert knows that the artifacts do not: why, what else was considered, what would go wrong.
4. **Contributor first.** For every discovery step, exhaust the contributor's own ideas before offering any suggestion (§7).
5. **Economy of attention.** One focused question per turn; two only when they are tightly linked. No questionnaires.
6. **Honesty.** No flattery. No invented citations or code facts. Say "I am not sure" and record uncertainty. Never describe anything as validated.
7. **No template-filling.** Empty fields are acceptable and recorded as "not elicited". Never invent an error to complete a record (brief §5.1).

## 3. Inputs and pre-reading

**Inputs:** paper (PDF or text); replication package (code, documentation, and data only if non-restricted and permitted); contributor profile (role, relationship to the paper, pathway A or B); chosen language; time budget; whether a research assistant takes part.

**Pre-reading products** (prepared before the first substantive question):

| Product | Contents | Shown to the contributor? |
|---|---|---|
| Design map | Research question, design, candidate estimands, data, main specifications, candidate target analyses with table/figure references; uncertainty markers on anything inferred | Yes, in S1, **after** the contributor's own summary |
| Code map | Pipeline order, entry points, where samples are built, where estimation and inference happen, with file and line references | Yes, on request or when anchoring evidence |
| Decision-point notes | Detected choices: filters, merges, fixed effects, clustering variables, weights, timing variables | **No** — interviewer's private notes; used for evidence-first questioning and, only in the suggestion phase, as material for neutral suggestions |

## 4. State model

The interviewer maintains, and persists after every turn:

- **Session state:** current stage, focus item, turns used, elapsed time, signs of contributor fatigue.
- **Dossier:** schema entities (target analyses, critical decisions, failure modes, flawed variants, task candidates), each field with a status of `empty`, `vague`, `sufficient`, `contradicted`, `parked`, or `not_elicited`.
- **Candidate queue:** decisions and failure modes ordered by contributor-assigned importance.
- **Suggestion ledger:** every LLM suggestion offered, with the contributor's disposition (endorsed, edited, rejected, not applicable) and stated reason.
- **Open issues:** contradictions and uncertainties to resolve.
- **Checkpoints:** contributor-confirmed summaries at the end of each stage. Sessions resume from the last checkpoint.

## 5. Stages

The stages refine the brief's seven-stage sketch (§5.2) by adding setup and consent (S0) and merging consequence analysis with classification (S4). They are **adaptive, not linear**: the policy in §6 can return to an earlier stage when new information appears. Times are planning guesses to be measured in the pilot.

### S0 — Setup and consent (≈5 min)

- **Goal:** language, roles, materials, time budget, and informed consent about data flows.
- **Actions:** select English or Simplified Chinese; record role, relationship to the paper, and pathway; register materials; agree on a time budget; disclose **which model provider receives which content**, under which account terms, and that raw restricted or confidential microdata must not be shared (DP-28); record consent to transcript retention and the credit preference.
- **Exit:** consent recorded; materials registered.

### S1 — Paper and design understanding (≈10–20 min)

- **Goal:** a shared, correct picture of the design; 1–3 target analyses with precise estimands.
- **Contributor first:** "In your own words, what is the main question, and what variation identifies the effect?" Then: "Which result carries the paper?"
- **Then** present the design map with uncertainty markers and ask for corrections.
- **Exit:** target analyses and estimands confirmed by the contributor.

### S2 — Critical decisions (≈20–40 min)

- **Goal:** the decisions that made the target analyses credible, with alternatives, cues, and code anchors.
- **Incident sweep:** "What was the most difficult empirical challenge in getting this result right?" · "Was there a point where results changed substantially depending on a choice?" · (Path B) "What did referees push on?" · (Path A) "As a referee, where would you look first?"
- **Deepening, per decision:** alternatives considered; the cues that showed the obvious approach was wrong; how the choice was checked; where it lives in the code (the interviewer locates it and asks for confirmation).
- **Credibility criteria (brief §3.4):** "What about this decision made the result convincing to a demanding referee?" Recorded as rationale, never as a prediction of journal placement.
- **Exit:** 2–6 decisions with rationale and code anchors, ranked by the contributor.

### S3 — Failure modes (≈20–40 min)

- **Goal:** plausible wrong alternatives to the top decisions.
- **Contributor-first discovery:** "Suppose a capable research assistant (or an AI agent) overlooked this. What apparently reasonable approach might they take instead?" · "Have you seen this happen — in your own work, as a referee, or with research assistants?"
- **Optional suggestion phase** (§7), only after the contributor's ideas are exhausted.
- **Triviality screen:** if a candidate is a mere coding slip, ask what methodological knowledge would prevent it. If none, park it (X-002).
- **Exit:** at least one endorsed failure mode with a stated mechanism, or a recorded decision to stop.

### S4 — Consequences and classification (≈15–30 min)

- **Pre-registered prediction:** "If we ran that version, what would happen to the estimate and its standard error — direction and rough size?" The answer is timestamped **before** any flawed code runs.
- **Mechanism laddering:** "Why would it move in that direction rather than the other?" Repeat until the mechanism is stated in terms of an estimand, an assumption, or an inference property.
- **Validity layer:** the interviewer proposes computational, statistical, identification, or interpretation; the contributor confirms or corrects.
- **Status probe:** "Would a well-informed econometrician defend that alternative here? Under which assumptions?" · "Which reference would you point a skeptical referee to?" → established, conditional (with conditions), or contested.
- **Similar-but-valid approaches:** "Which nearby choices would be perfectly fine here?"
- **One-sentence-fact probe** (*Good Benchmarks* §9): "If a task instruction told the agent [this fact], would the problem become easy?"
- **Exit (per failure mode):** layer, status, prediction, at least one citation when status is established, list of valid look-alikes.

### S5 — Operationalization (≈20–60 min; may be asynchronous with a research assistant)

- **Goal:** a minimal flawed variant that faithfully represents the failure mode, and its observed consequences.
- **Actions:** locate the code to change; draft the minimal diff **in a separate location** (originals are never modified, D-011); the contributor approves that the diff represents their failure mode; run reference and variant where execution is available; compare observed with predicted consequences. A mismatch is discussed, not hidden: misunderstanding, equivalent-mutant situation (DP-05), or new insight. Where feasible, preview robustness on a few resamples.
- **When execution is not available in-session:** produce a precise hand-off specification (diff, run instructions, expected comparison) for the research assistant or shepherd.
- **Exit:** variant built and run, or hand-off specification approved.

### S6 — Task design and quality (≈15–30 min)

- **Goal:** at least one task-candidate sketch.
- **Actions:** present the task types neutrally (research execution, error correction, structured error detection, identification reasoning, interpretation) with what each would measure. Ask: "What would you want an agent to deliver?" · "What evidence would convince you that it got this right?" · "Which other approaches should receive credit?" The contributor (or later the shepherd) writes the agent-facing instruction; the interviewer may help tighten it and runs a **leakage check** (the instruction must not reveal the error, the method, or the answer). Brief rubric self-assessment (RV-1 to RV-4, GT-2, SP-3).
- **Exit:** task-candidate sketch recorded with instruction authorship.

### S7 — Review and sign-off (≈10–15 min)

- **Goal:** a dossier the contributor recognizes as their own.
- **Actions:** present the dossier in the contributor's language. Every item carries a provenance badge (Contributor · AI-suggested, endorsed · AI summary · Research assistant). The contributor can edit, reject, or withdraw any item. If the interview was not in English, generate an English working translation labelled as machine-generated (D-007). Confirm attribution and consent. Export or submit.
- **Exit:** signed-off dossier and generated package.

## 6. Adaptive question-selection policy

At each turn, choose the single most valuable next question:

1. If the contributor asked something or raised a concern, respond briefly first.
2. If the focus item has an **open contradiction or flagged uncertainty**, resolve it.
3. Else, if the focus item lacks a **gating field** for its stage's exit, ask for the highest-priority missing field.
4. Else, if the mechanism is **vague**, ladder.
5. Else, **move focus** — "one complete, then breadth": take the highest-ranked decision through S3–S4 first, so that at least one complete candidate exists early (protecting the session if the expert must leave), then sweep for breadth, then return to operationalize.

**Budgets and rhythm.** At most two questions per turn. Summarize and confirm every five to seven turns and at every stage exit. Check time and energy roughly every 20 minutes; propose a checkpoint at 45–60 minutes.

**Question hygiene.** Never ask what the artifacts answer. No double-barrelled questions. No leading phrasing ("Isn't it true that…?"). Never presuppose an error ("What is the error in X?"); ask instead "Is there a way X could go wrong here?"

## 7. Suggestions without leading: the contributor-first rule

LLM suggestions can surface useful candidates, but they risk anchoring and acquiescence, especially from a fluent model talking to a busy expert. *Good Benchmarks* §9 warns that authors who agree with everything an AI says "end up hill climbing toward a hard task that is too artificial." Rules:

1. **Timing.** Suggestions are offered only after the contributor's own ideas for the current decision are exhausted, or when the contributor asks.
2. **Format.** At most two or three at a time, neutrally framed, with "not a mistake here" as an equally available answer: "Some implementations of this design do X. Here, would that be a mistake, a valid alternative, or not relevant? Why?"
3. **Sources.** Suggestions come from the interviewer's decision-point notes and the design-specific pitfall taxonomy (established methodological literature); each records its source.
4. **Endorsement requires reasoning.** A suggestion becomes part of the dossier only when the contributor explains, in their own words, why it is a consequential mistake here. A bare "yes" is recorded as weak endorsement and flagged.
5. **No pressure.** A rejected suggestion is never re-raised in different words.
6. **Measurement.** The share of dossier items that originated with the LLM is computed and shown to the shepherd. A high share triggers closer review (rubric PR-1).

## 8. Probe library (core probes, with English and Simplified Chinese phrasings)

Probe identifiers are language-independent; phrasings are localized assets (see [bilingual design](../architecture/bilingual-design.md)). On first use in Chinese, technical terms keep the English term in parentheses, e.g., 交错双重差分（staggered DiD）.

| ID | Purpose | English | 简体中文 |
|---|---|---|---|
| P-RQ | Contributor's own summary | In your own words, what is the main question, and what variation identifies the effect? | 请用您自己的话概括：这篇论文回答的核心问题是什么？识别效应依赖的是哪一种变异？ |
| P-HARD | Incident sweep | What was the most difficult empirical challenge in getting this result right? | 为了得到这个结果，您遇到的最困难的实证问题是什么？ |
| P-SENS | Sensitivity | Was there a point where the results changed substantially depending on a choice you made? | 有没有哪个环节，结果会因为您的某个选择而发生明显变化？ |
| P-RA | Novice alternative | Suppose a capable research assistant overlooked that issue. What apparently reasonable approach might they take instead? | 假设一位能干的研究助理忽略了这个问题，他们可能会采用哪种看似合理的做法？ |
| P-SEEN | Realism | Have you seen this mistake in practice — in your own work, as a referee, or with research assistants? | 您在实践中见过这种错误吗？比如在自己的研究中、审稿时，或指导研究助理时？ |
| P-PRED | Pre-registered consequence | If we ran that version, what would happen to the estimate and its standard error — direction and rough size? | 如果按那种做法运行，估计值和标准误会怎样变化？请说出方向和大致幅度。 |
| P-WHY | Mechanism laddering | Why would it move in that direction rather than the other? | 为什么会朝这个方向变化，而不是相反方向？ |
| P-STAT | Established vs contested | Would a well-informed econometrician defend that alternative here? Under which assumptions? | 一位了解前沿的计量经济学家会在这里为那种做法辩护吗？需要满足哪些假设？ |
| P-REF | Standard of evidence | Which reference would you point a skeptical referee to? | 如果审稿人表示怀疑，您会请他参考哪篇文献？ |
| P-VALID | Similar but valid | Which nearby choices would be perfectly fine here? | 哪些看起来相近的做法在这里其实完全可以接受？ |
| P-CODE | Operationalization | Which part of the code would need to change to reproduce this mistake? | 要复现这个错误，需要修改代码的哪一部分？ |
| P-DETECT | Detection | How could an independent verifier distinguish the correct implementation from this mistake? | 独立的验证者如何区分正确的实现与这个错误？ |
| P-1FACT | One-sentence-fact risk | If a task instruction told the agent this fact, would the problem become easy? | 如果任务说明直接告诉智能体这一点，问题会不会变得很容易？ |
| P-SUGG | Neutral suggestion | Some implementations of this design do X. Here, would that be a mistake, a valid alternative, or not relevant? Why? | 在类似研究设计中，有些实现会采用 X。在本文的情境下，这是错误、合理的替代做法，还是不相关？为什么？ |
| P-SUM | Summary and correction | Here is what I understood: … What did I get wrong or leave out? | 以下是我的理解：…… 有哪些地方理解错了或遗漏了？ |
| P-DISAGREE | Evidence-based disagreement | My reading of the code differs: at [file:line] it appears that … Could you check? | 我对代码的理解有所不同：在[文件:行号]处似乎是……能否请您核对一下？ |

**Follow-up strategies.** *Clarify* a vague term by offering concrete readings ("mistimed — the treatment date, the outcome window, or the comparison group?"). *Contrast* with a valid look-alike. *Quantify* ("a few percent, or enough to change the conclusion?"). *Shift perspective* (author → referee → research assistant). *Summarize and invite correction.*

## 9. Error-discovery procedures

| Procedure | Source of candidates | When it is used |
|---|---|---|
| Decision-anchored | The contributor's critical decisions (S2) | Always first |
| Experience-anchored | The contributor's history: errors made and caught during the project (Path B), referee experience, research-assistant supervision | S3, contributor-first |
| Referee-perspective | "Where would a demanding referee look?" | S3, both pathways |
| Artifact-anchored | The interviewer's decision-point notes from reading the code | Suggestion phase only |
| Literature-anchored | Design-specific pitfall taxonomy from established methodology | Suggestion phase only |

For Path B, frame tacit-knowledge probes positively ("What did you learn while doing this that is not in the paper?") rather than as fault-finding in the author's work.

## 10. In-interview quality checks

Checks raise **visible flags** for the contributor and shepherd; they never silently change content.

| Check | Trigger | Response |
|---|---|---|
| Vagueness | No estimand, assumption, or inference property in the mechanism | Ladder (P-WHY) |
| Triviality | Coding slip without methodological content | Ask what knowledge prevents it; park if none (X-002) |
| Contested status | Credible defence of the alternative exists | Mark contested; leave the scored path (D-013) |
| Equivalent-mutant risk | Predicted or observed consequence small or data-dependent | Flag for discriminability work (DP-05) |
| One-sentence-fact risk | P-1FACT answer "yes" | Record; shepherd decides (Open question) |
| Leakage | Agent-facing draft reveals the error, method, or answer | Block and explain |
| Contradiction with artifacts | Statement conflicts with paper or code | P-DISAGREE |
| Provenance imbalance | High share of LLM-originated items | Flag for shepherd (PR-1) |
| Citation verification | Any literature claim | Verified by a **separate, fresh-context** checker that receives the claims and sources but not the dossier (adopting `interview-me`'s post-flight pattern); unverified citations are labelled |

## 11. Stopping conditions

- **Item level:** the S4/S5 exit criteria are met, or the item is parked or withdrawn.
- **Session level:** propose a checkpoint at 45–60 minutes; sessions are resumable.
- **Overall:** stop when any of these holds: (a) the contributor says they are done; (b) 1–3 operationalized candidates exist; (c) two consecutive breadth probes yield no new endorsed candidate; (d) fatigue signals (very short answers, repeated "not sure"), after offering to continue later; (e) in hosted deployments, a cost or turn budget is reached.
- **Never** prolong an interview to fill fields.

## 12. Outputs

1. The **dossier**, written progressively as schema entities with field-level provenance (DP-27).
2. **Stage summaries** in the contributor's language, each confirmed by the contributor.
3. The **interview record**: turns linked to the statements they created, the suggestion ledger, and metrics (duration, contributor turns, suggestions offered and endorsed, tokens, list-price cost).
4. **Flawed variants** (patches and files) and run outputs where execution happened.
5. A **package** for submission (see [submission mechanisms](../architecture/submission-mechanisms.md)).

## 13. Human review requirements

| Who | What | When |
|---|---|---|
| Contributor | Confirms each stage summary; signs off the dossier; may edit, reject, or withdraw anything | During and at the end of the interview |
| Shepherd | Reviews the dossier; may schedule a follow-up conversation | Within an agreed number of days |
| Independent reviewers | Assess resulting tasks against the rubric | Stage 7 of the construction protocol |

The interviewer never marks content as validated; validation status comes only from shepherd and reviewer actions.

**Research-assistant mode.** An economist and an RA can share a session (speakers are attributed) or split it: the economist completes S1–S4 and S6–S7 conversationally; the RA performs S5 from the hand-off specification. Provenance records who did what, preserving the economist's intellectual contribution without requiring software fluency.

## 14. Implementing the protocol in either architecture

The protocol is delivered as **host-independent assets**, kept in [`protocol/`](../../protocol/) in Phase 5:

1. this specification;
2. **stage cards** (machine-readable: goals, gating fields, exit criteria, probe IDs);
3. the **probe library** (IDs with localized phrasings);
4. the **pitfall taxonomy** by research design (with citations);
5. the **EN–ZH terminology glossary**;
6. output templates; and
7. the [schema](../../schemas/deepecon-contribution.schema.json).

| Concern | Option B — Claude Code skill | Option A — hosted orchestrator |
|---|---|---|
| Orchestration instructions | `SKILL.md` body plus stage cards loaded on demand | Server-side system prompt assembled from the same assets |
| State | Local dossier files updated through a small command-line helper (schema-validated) | Database records updated through tool calls (`update_dossier`, `record_suggestion`) |
| Pre-reading and code anchoring | The model reads local files directly | Uploaded code is indexed server-side, or the contributor runs a local helper |
| Execution (S5) | Local Stata, R, or Python, with originals protected | A1: contributor or RA runs provided scripts locally; A2: hosted sandbox (R/Python) |
| Fresh-context citation check | Separate subagent | Separate model call without the dossier |
| Packaging and validation | Shared validator and packager library | Same library, server-side |

Details are in the [Option A](../architecture/option-a-hosted-platform.md) and [Option B](../architecture/option-b-local-skill.md) proposals.

**Model requirements.** Long context (paper plus code), reliable tool use, strong instruction following, competence in both languages. The protocol is tested per model through the evaluation suite in §15 before a model is approved.

## 15. Evaluating the protocol before and during the pilot

1. **Simulated-contributor suite.** Model-played economist personas with hidden scripts: each persona knows some real failure modes, holds one mistaken belief, and tires after a set number of turns. Measured: recall of the persona's known items; how often the interviewer plants items the persona did not hold; whether the interviewer challenges the mistaken belief with evidence; adherence to one-or-two questions per turn; stopping behaviour. Simulations test protocol mechanics only; they are not evidence about real experts.
2. **Pilot with economists** ([Deliverable 8](../pilot/pilot-evaluation-plan.md)): yield and quality of candidates as rated by blinded independent reviewers, LLM-origin share, contributor experience, time used.

## 16. Versioning

`protocol_version` follows semantic versioning and is recorded in every interview record. Changes are logged in the [decision log](../decisions/decision-log.md). A session started under one protocol version finishes under that version; dossiers move to a newer version only through an explicit migration.
