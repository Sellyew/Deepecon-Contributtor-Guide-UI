# Deliverable 8 — Pilot Evaluation Plan

| | |
|---|---|
| **Status** | **Proposed** v0.1.0 (2026-11-05). Not yet reviewed by the research lead. Execution belongs to Phases 5–6, after the architecture review. |
| **Purpose** | Replace theoretical argument with evidence: run the *same scientific content* through both contribution workflows and compare what contributors actually experience and produce. |
| **Requirement** | Brief, Deliverable 8 (D-016): one published paper; one validated correct implementation; at least one plausible, consequential error; an expert-guided interview; an erroneous implementation and its results; a proposed task; an initial verifier; a standardized package. |

---

## 1. Pilot questions

| ID | Question | Why it matters for the decision |
|---|---|---|
| PQ1 | Can economists of differing technical fluency start and complete a contribution in each workflow, and where do they get stuck? | Accessibility (brief §7) |
| PQ2 | Do the workflows differ in the **quality** of what is produced, judged blind by independent reviewers? | Scientific quality — the central criterion |
| PQ3 | Do they differ in **intellectual ownership**: does the dossier reflect the contributor's reasoning rather than the model's suggestions? | Human authority (D-008); *Good Benchmarks* §9 |
| PQ4 | Does in-session code execution (local in B, hosted or hand-off in A) change the rate at which failure modes become **operationalized, validated** flawed variants? | The real value of local execution |
| PQ5 | What does each workflow cost per contribution: tokens and dollars at list price, staff support time, shepherd time? | Cost model calibration |
| PQ6 | How comfortable are contributors with the data flows each workflow implies? | Privacy (Safeguard E) |
| PQ7 | Does the interview protocol itself work: yield, recall of known issues, leading-question rate, stopping behaviour? | Protocol validity, independent of architecture |

## 2. What is held constant (the "same scientific content")

- **One paper**, with **two target analyses** of comparable difficulty (needed for the crossover design in §4).
- **One reference implementation** per target analysis, built and independently checked by the project team *before* any session (construction Stage 1).
- **A sealed known-issues key**: critical decisions and failure modes for each target analysis, compiled by the project team and one independent economist, sealed before the sessions. It measures recall without being shown to anyone during sessions; items participants raise that are not in the key are scored separately as novel items.
- **The same protocol version, probe library, schema, packager, and model** (Claude Opus 5.5 at a fixed effort level) in both arms. To isolate workflow effects from account effects, the project supplies model access in both arms. Setup of a contributor's *own* account is measured separately (§5, M1).
- **The same output contract:** both arms must produce a schema-valid package.

## 3. What is built for the pilot (Phase 5, "thin vertical slices")

Both slices share the architecture-independent core (protocol assets, schema, validator, packager). Neither is a full product.

| Slice | Minimum functionality | Out of scope for the pilot |
|---|---|---|
| **A-slice** (hosted) | Sign-in, language choice, upload of paper and code, staged interview with progress display, dossier review screen with provenance badges, package export. Execution through **A1** (hand-off scripts the contributor or RA runs locally) — or A2 if collaborators want to test hosted execution. | Public onboarding site, admin dashboards, scaling, polished design system |
| **B-slice** (local) | Plugin with the interview skill, local state helper, protection of original files, run wrappers for Stata, R, and Python, packager; English and Chinese installation guides. | Marketplace polish, automatic updates, support for other agent harnesses |

## 4. Study design

**Participants.** Six to ten economists with Top-5 or leading-field publications, stratified by technical fluency: *fluent* (uses terminal-based AI tools or writes most of their own code) versus *non-fluent* (delegates code to research assistants). Two research assistants support the RA-assisted condition. Recruitment of an **original author** of the pilot paper is desirable (it tests Path B) but not required.

**Recommended design: within-subject crossover on two target analyses.** Each participant contributes to target analysis T1 in one workflow and T2 in the other, with order and target–workflow pairing counterbalanced:

| Sequence | First session | Second session |
|---|---|---|
| 1 | A-slice on T1 | B-slice on T2 |
| 2 | B-slice on T1 | A-slice on T2 |
| 3 | A-slice on T2 | B-slice on T1 |
| 4 | B-slice on T2 | A-slice on T1 |

*Why:* every participant experiences both workflows, so preference and experience comparisons are within-person, and individual differences — large among senior experts — do not masquerade as workflow effects. Using different target analyses limits carry-over of content, while the paper and the overall scientific material stay the same.

*Cost:* about two sessions of 90–120 minutes per participant. If that is too demanding for senior economists, use the **fallback between-subjects design**: one workflow per participant, stratified by fluency, plus a 15-minute guided exposure to the other workflow at the end for preference elicitation. The fallback cannot separate workflow effects from person effects at this sample size; its conclusions would be correspondingly weaker.

**RA-assisted condition.** At least one non-fluent participant per arm works with a research assistant who performs operationalization (S5) from the hand-off specification.

**Order of activities.**

1. **Dry runs** with simulated contributors (interview protocol §15) on both slices, to fix mechanical problems before involving experts.
2. **Setup test** on participants' own machines: B-slice installation and A-slice sign-up, timed, without staff help unless requested (requests are logged).
3. **Sessions** (recorded with consent).
4. **Asynchronous completion:** operationalization and package finalization within one week.
5. **Debrief interview** (20 minutes, semi-structured).
6. **Blind review:** two independent economists and one benchmark reviewer rate every package with the rubric subset RV-1 to RV-4, GT-2, GT-3, and SP-3, without knowing which workflow produced it. Inter-rater agreement is reported.
7. **Shepherding:** the project converts the best candidate from each arm into a full task (Stages 5–6), recording hours, so that the pilot also yields a proposed task, an initial verifier, and a complete standardized package (the Deliverable 8 requirements).

## 5. Measures

| ID | Measure | Instrument or source | PQ |
|---|---|---|---|
| M1 | Setup time and setup failures; staff help requests | Timed setup test; logs | PQ1 |
| M2 | Time to first substantive question; total active time; drop-off stage | Session logs | PQ1 |
| M3 | Candidate yield: failure modes endorsed; operationalized; validated with a material consequence | Packages; shepherd records | PQ2, PQ4 |
| M4 | Recall of the sealed known-issues key; number of novel items rated valid by reviewers | Key comparison; blind review | PQ2, PQ7 |
| M5 | Blind quality ratings (rubric subset) and inter-rater agreement | Reviewer forms | PQ2 |
| M6 | LLM-origin share of endorsed items; share of weak endorsements | Provenance fields; suggestion ledger | PQ3, PQ7 |
| M7 | Perceived ownership ("The dossier reflects my reasoning") and perceived interviewer quality | Post-session questionnaire (Likert items, defined before the pilot) | PQ3 |
| M8 | Usability | A validated short instrument (e.g., UMUX-Lite or SUS; choose one before the pilot) | PQ1 |
| M9 | Tokens, list-price cost, staff support minutes, shepherd hours per admitted task | Usage logs; time sheets | PQ5 |
| M10 | Comfort with data flows; anything participants declined to share | Questionnaire items; debrief | PQ6 |
| M11 | Protocol adherence: questions per turn, leading-phrasing incidents, stopping behaviour | Transcript coding by two coders | PQ7 |

## 6. Analysis plan

- With six to ten participants, the analysis is **descriptive and qualitative**. Report counts, medians, and ranges with every individual data point; avoid significance tests that the sample cannot support.
- Within-subject differences (crossover) are reported per participant.
- Transcripts are coded for protocol adherence and for moments of friction, by two coders with agreement reported.
- Blind ratings are compared across arms only descriptively; the main use is to detect large differences.

## 7. Pre-registered decision guidance (proposed thresholds; the research lead sets the final values)

Writing these down before the pilot keeps the architecture decision honest.

| If the pilot shows… | …it favours | Proposed threshold |
|---|---|---|
| Non-fluent participants cannot complete B-slice setup unaided | A, or a hybrid with hosted onboarding | Fewer than 3 of 4 non-fluent participants complete setup within 30 minutes without help |
| Hand-off execution (A1) stalls operationalization | B, or A2 (hosted execution) | Under half of A1 contributions reach a run flawed variant within one week |
| Blind quality ratings are similar across arms | Decide on accessibility, cost, privacy, and sustainability | Median rating difference within one rubric level |
| LLM-origin share is high in one arm | That arm's interaction design needs revision before scaling, whichever is chosen | More than 50% of endorsed items LLM-originated |
| Participants decline to share materials in one arm | The other arm, or a design change to the data flow | Two or more participants decline |
| Inference cost per contribution is small relative to shepherd time | Do not let inference cost drive the decision | Inference below 10% of total per-task cost |

## 8. Choosing the pilot paper

**Criteria (in priority order).**

1. Public replication package with **redistributable data** and modest compute.
2. **Two target analyses** of comparable difficulty, each with at least one **established**, consequential pitfall (rubric GT-2).
3. A design familiar to most applied economists (for example, staggered-adoption difference-in-differences, or regression discontinuity), so that participants across fields can contribute.
4. An **available expert**, ideally an original author (Path B).
5. Moderate fame: very famous papers are well-understood (good for recall measurement) but heavily memorized (bad for the eventual task); the pilot mainly tests workflows, so this is secondary here.

**Candidate archetypes** (illustrations to be verified by the team before selection; none is a recommendation yet):

| Archetype | What makes it attractive | What to verify |
|---|---|---|
| Staggered-adoption DiD using public state-level panels (e.g., a policy-adoption study of the kind used to illustrate two-way fixed effects problems in Goodman-Bacon 2021) | Established pitfalls in estimator choice, treatment timing, and clustering; small data | Package availability, licence, whether two target analyses exist |
| Sharp regression discontinuity with public data | Established pitfalls in bandwidth, polynomial order, manipulation testing, and clustering | Same |
| Shift-share (Bartik) design with public data | Established inference pitfalls (exposure-robust standard errors) | Compute size; licence |

The choice of paper — and whether a collaborator can contribute their own paper — is an Open question for the research lead.

## 9. Ethics and data handling

- A study of economists' experience with a tool is likely **human-subjects research** under many institutions' rules, even when it qualifies for exemption. Obtain IRB or ethics-committee review (or a documented exemption) at the lead's institution before recruiting ([evidence note R9](../research/evidence/R9-hosted-stack-and-compliance.md) summarizes guidance).
- Informed consent covers recording, transcript retention, data flows to the model provider, and the right to withdraw.
- No restricted or confidential microdata are used: the pilot paper's data must be public.
- Participants are offered an honorarium and/or contributor credit (the policy is an Open question).

## 10. Timeline (indicative, after Phase 5 authorization)

| Week | Activity |
|---|---|
| 1–2 | Select paper; build and independently check reference implementations; seal known-issues key; ethics submission |
| 2–5 | Build the two thin slices on the shared core (estimates in the [decision brief](../architecture/architecture-decision-brief.md)) |
| 5–6 | Simulated-contributor dry runs; fixes |
| 6–9 | Setup tests, sessions, asynchronous completion, debriefs |
| 9–11 | Blind review; shepherding two candidates into full tasks; validation ladder |
| 11–12 | Pilot report and decision memo for collaborators |

## 11. Pilot outputs

1. Two complete, standardized contribution packages (one per arm), each with a reference implementation, at least one validated flawed variant with results, a proposed task, and an initial verifier that has climbed the validation ladder through at least L4.
2. A pilot report answering PQ1–PQ7, including the pre-registered decision table.
3. Revised protocol, rubric, and schema (new versions logged).
4. Calibrated cost and effort figures replacing the planning estimates in the decision brief.
