# Deliverable 8 — Pilot Evaluation Plan

| | |
|---|---|
| **Status** | **Proposed** v0.2.0 (2026-11-05). Not yet reviewed by the research lead. Execution belongs to Phases 5–6, after the architecture review. v0.2.0 integrates four independent reviews (§12); every threshold stays a proposal until the research lead registers it (§7). |
| **Purpose** | Replace theoretical argument with evidence: run the *same scientific content* through both contribution workflows, compare what contributors actually experience and produce, and test the construction method end to end. |
| **Requirement** | Brief, Deliverable 8 (D-016): one published paper; one validated correct implementation; at least one plausible, consequential error; an expert-guided interview; an erroneous implementation and its results; a proposed task; an initial verifier; a standardized package. |
| **Builds on** | [Interview protocol](../interview/expert-interview-protocol.md) · [verifier validation protocol](../methodology/verifier-validation-protocol.md) (VVP) v0.3.0 · [rubric](../methodology/task-quality-rubric.md) · [Option A](../architecture/option-a-hosted-platform.md) · [Option B](../architecture/option-b-local-skill.md) · [cost model](../architecture/cost-and-effort-model.md) |

---

## 1. Pilot questions

| ID | Question | Why it matters for the decision |
|---|---|---|
| PQ1 | Can economists of differing technical fluency start and complete a contribution in each workflow, and where do they get stuck? | Accessibility (brief §7) |
| PQ2 | Do the workflows differ in the **quality** of what is produced, judged by reviewers who do not know the arm? | Scientific quality — the central criterion |
| PQ3 | Do they differ in **intellectual ownership**: does the dossier reflect the contributor's reasoning rather than the model's suggestions? | Human authority (D-008); *Good Benchmarks* §9 |
| PQ4 | Does in-session execution (B; A2 if tested) change how often failure modes become **operationalized, validated** flawed variants, compared with hand-offs (A1 run kits; research-assistant mode in either arm)? | The real value of local execution |
| PQ5 | What does each workflow cost per contribution and per task: inference at list price, support, shepherd hours by execution route (including dropped candidates), outside-economist hours, validation-trial compute? | Cost model calibration |
| PQ6 | How comfortable are contributors with the data flows each workflow implies? | Privacy (Safeguard E) |
| PQ7 | Does the interview protocol itself work: yield, recall of known issues, leading-question rate, stopping behaviour? Answered on a less canonical paper (§8). | Protocol validity, independent of architecture |
| PQ8 | Which rungs of the validation ladder fail? How often are flagship variants data-equivalent? Does re-execution degenerate into format compliance? Do two blind economists agree on SP-1? | Validity and cost of the construction method ([construction protocol](../methodology/benchmark-construction-protocol.md) §9), independent of architecture |

## 2. What is held constant (the "same scientific content")

- **One paper** for the A/B comparison (D-016), with **two target analyses** of comparable difficulty, ideally differing in some critical decisions. R8's candidate pairs are the same specification on another outcome, one reason why M3–M6 use first-period data only (§6).
- **One reference implementation** per target analysis, checked before any session by a clean-room re-implementation (rubric GT-1; VVP L3).
- **A sealed known-issues key** per target analysis (critical decisions and failure modes), compiled by the project team and one independent economist, and never shown during sessions. Each item is tagged **textbook** or **paper-specific** (this paper's data, code or setting). Items not in the key are scored as novel.
- **The same** protocol version, probe library, schema, packager, suggestion procedure and model (Claude Opus 5.5 at a fixed effort level) in both arms, under **commercial no-training terms** (§3.1), with one output contract: a schema-valid package, normalized for review (§4).

## 3. What is built for the pilot (Phase 5, "thin vertical slices")

Both slices share the architecture-independent core (protocol assets, schema, validator, packager). Neither is a full product. Both are frozen during the sessions, and fixes between sessions are logged.

| Slice | Minimum functionality | Out of scope for the pilot |
|---|---|---|
| **A-slice** (hosted) | Sign-in, language choice, upload, staged interview with progress display, separate suggestion and checker calls, dossier review with provenance badges, export, research-assistant invitation. **A1** run kits with **staff execution** as the fallback (A's proposed MVP); A2 only if collaborators want it. An off-the-shelf component library and one usability dry run | Public onboarding site, admin dashboards, scaling, a bespoke design system |
| **B-slice** (local) | One downloadable workspace registering the plugin (interview skill, suggestion and checker subagents, state helper, protection of originals, Stata/R/Python run wrappers, packager); pin, block and record model controls; status line and local dossier page; suggestions and controls served from the project endpoint; research-assistant hand-off bundle; **B-staff** fallback; installation guides in English and Chinese | Marketplace polish, automatic updates, other agent harnesses |

**Effort** ([cost model](../architecture/cost-and-effort-model.md)): roughly 8–14 engineer-weeks for whichever slice is built second [U], beyond the shared core and the first slice. **Open question O-019, for the research lead:** build one full slice plus setup and hand-off probes of the other. That would test rules 1–3 (§7) for both arms, but could not compare yield, quality or influence (rules 4–7). Choosing which slice to build in full would itself lean the decision, so it must not rest on ease of implementation (D-005).

### 3.1 Keeping the arms comparable

- **Model access.** Flawed variants and error labels are created in the sessions, so every session runs under commercial no-training terms (VVP §10): A on the project's API account; B on project-provided commercial access (pending O-018) or the participant's institutional commercial account. Consumer plans are not used, even with the training opt-out. If O-018 is unresolved at recruitment, B participants need institutional accounts.
- **B-arm environment audit.** At setup and in each package (Option B's package doctor): client and plugin versions, access route, model-deviation flags, and any user-level `CLAUDE.md`, skills, plugins, MCP servers or output styles (names and hashes, not contents). Provided access standardizes data terms, not the whole interviewer configuration (Option B §5.3), and identical access in both arms would hide that. The audit shows how much real-world variation the B sessions carried: the evidence for the tie-break's "real-world account conditions" (§7).
- **A design baseline.** B runs in a finished commercial client, A in a thin slice; the component library and dry run give A a usable baseline. Differences in usability (M8) and drop-off (M2) may still reflect product maturity, and are reported with that caveat.
- **Fallbacks.** Both arms keep their staff fallback and research-assistant mode. Staff-completed contributions are reported by route, with their shepherd hours (M9).
- **Concealment and observation.** In both arms, suggestion assignments and known-valid controls stay hidden from participants until the suggestion step. Both slices send session metrics to the project during the pilot, so abandoned sessions are seen in both. The report states which measures each architecture could collect at scale without that instrumentation (Option A §5.4; Option B §4, F12).

## 4. Study design

**Participants.** At least eight economists with Top-5 or leading-field publications, two per sequence, one from each fluency stratum: *fluent* (uses terminal-based AI tools or writes most of their own code) or *non-fluent* (delegates code to research assistants). Further participants keep sequences and strata balanced. An **original author** of the pilot paper is desirable (it tests Path B) but not required.

**Recommended design: crossover on two target analyses**, with order and pairing counterbalanced:

| Sequence | First period | Second period |
|---|---|---|
| 1 | A-slice on T1 | B-slice on T2 |
| 2 | B-slice on T1 | A-slice on T2 |
| 3 | A-slice on T2 | B-slice on T1 |
| 4 | B-slice on T2 | A-slice on T1 |

*What it buys:* within-person comparisons of experience and preferences. It does **not** yield valid within-person evidence on quality, recall or influence: the second period is primed by the first, and with two participants per sequence, carry-over cannot be separated from the effect of the arm (Grizzle 1965 [U]). Those outcomes use first-period sessions only (§6).

**Sessions** are capped at 45–60 minutes (interview protocol §5). A contribution spans several sessions, about three under the cost model's assumption A2 [U], so a crossover participant gives about six, plus setup, asynchronous work and a debrief. If that is too demanding, use the **fallback between-subjects design**: one workflow per participant, stratified by fluency, with both setup tests and a 15-minute guided exposure to the other workflow. Since M3–M6 are compared between subjects in either design, the fallback loses only the within-person comparisons of M2, M7 and M8.

**Research-assistant condition.** At least two non-fluent participants, one starting in each arm, work in both arms with their own (or a project-provided) research assistant, who performs operationalization (S5) from the hand-off specification (A: platform invitation; B: hand-off bundle, Option B §2.2).

**Suggestion experiment (O-017).** The units are the critical decisions pre-registered for each target analysis from the design map; decisions not on the list get no suggestions. Assignment is balanced, not random coin flips: each participant has the gated suggestion phase (protocol §7) on for half of the listed decisions, and each decision has it on for half the participants in each arm, target analysis and period. Assignments stay concealed until the suggestion step. All free-recall locks of a contribution (S2 decisions, S3 failure modes) are recorded before any suggestion in it, overriding the protocol's "one complete, then breadth" order (§6) for the pilot, so a suggestion on one decision cannot prime recall on another. The outcome is the number of endorsed items with a complete evidence bundle that arm-blind reviewers rate valid; rule 7 (§7) applies.

**Methodology arm (PQ8).** Every candidate that reaches a run flawed variant with a material consequence under RV-2 — or, if capacity is short, a random sample of at least six, stratified by arm — goes through L0–L12 (VVP §3). This includes two blind outside economists for SP-1, the hint ladder and knowledge probe (L10, which now carries SP-3), and agent trials (L11). Each rung records hours by role, the outcome (pass, pass after repair, fail, dropped) and the reason; the report gives attrition by rung. Shepherds know the arm, so results are reported by arm but stay out of the A/B decision rules.

**Order of activities.**

1. **Dry runs** with simulated contributors on both slices (protocol §15), plus the A-slice usability dry run; the cost of one suite pass is recorded.
2. **Cognitive-interview pretest** of the probe library, with three to five economists per language.
3. **Registration** of the decision list, suggestion assignment, sealed keys and §7 thresholds.
4. **Setup test** on participants' own machines, for both arms in counterbalanced order, with the designed onboarding available (one onboarding session, or the participant's research assistant). Help requests are logged, and unaided completion is recorded separately. *B setup* is complete when the workspace opens with the plugin loaded and the skill starts in the participant's language; whether the reference implementation then runs through the run wrappers is recorded. The *A1 run-kit test* is complete when, after sign-in, a sample run kit for the reference implementation has run and its outputs are uploaded. The B-arm environment audit happens here.
5. **Sessions**, recorded with consent.
6. **Asynchronous completion**, with each hand-off timed from the variant's approval.
7. **Debrief** (20 minutes, semi-structured), including preferences.
8. **Arm-blind review** of normalized packages (one rendering; client, platform and path identifiers sealed). Two independent economists and one benchmark reviewer rate (i) each endorsed item's validity, blind to arm, suggestion condition and provenance; (ii) each candidate on RV-1 to RV-4, GT-2, GT-3 and the other candidate-stage gates (PR-1 comes from the automated provenance checks); (iii) each package on an anchored 1–7 scale (for example, 1 no usable candidate, 4 usable after substantial revision, 7 ready for task construction). They also guess each package's arm. SP-3 is not rated blind, because it needs agent trials (VVP L10).
9. **Methodology arm**, as above.

**Other roles.** Two arm-blind economists and a benchmark reviewer; the economist who co-compiles the key; two coders; and, per methodology-arm task, the ladder's roles (VVP §12): shepherd, two blind SP-1 economists, GT-2 classifiers, a clean-room witness implementer, and domain and benchmark reviewers. SP-1's economists must not have seen the hidden tier, so they cannot be participants or arm-blind reviewers.

## 5. Measures

| ID | Measure | Instrument or source | PQ |
|---|---|---|---|
| M1 | Completion and time for B setup and the A1 run-kit test, with and without the designed onboarding; failures; help requests; access route; environment audit | Timed setup test; logs | PQ1 |
| M2 | Time to first substantive question; total active time; sessions per contribution; drop-off stage | Session metrics from both slices | PQ1 |
| M3 | Candidate yield: failure modes endorsed with a complete evidence bundle; operationalized; validated (run, re-run by the project, material under RV-2); execution route; time from approval to a run variant | Packages; hand-off logs; shepherd records | PQ2, PQ4 |
| M4 | Recall of the sealed key on **pre-exposure items only**, separately for textbook and paper-specific items; novel items rated valid | Key comparison; arm-blind review | PQ2, PQ7 |
| M5 | Share of candidates passing all candidate-stage gates; RV-1 to RV-4, GT-2, GT-3; 1–7 rating; inter-rater agreement; arm guesses | Arm-blind review forms | PQ2 |
| M6 | **Measured AI influence:** LLM-originated, post-exposure, and LLM-influenced shares of endorsed items; false-endorsement rate on known-valid controls; weak endorsements; the suggestion-experiment outcome | Free-recall lists; exposure flags; suggestion ledger; double coding; arm-blind review | PQ3, PQ7 |
| M7 | Perceived ownership and perceived interviewer quality — **an experience measure only**, not evidence of validity: self-rated ownership did not distinguish experts who followed an AI's planted lean ([R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) §3.4) | Post-session questionnaire (items defined before the pilot) | PQ1 |
| M8 | Usability, with the product-maturity caveat (§3.1) | A validated short instrument (UMUX-Lite or SUS; chosen before the pilot) | PQ1 |
| M9 | Inference tokens and cost; support minutes; shepherd hours by stage and route, including dropped candidates and staff-run S5; reviewer and outside-economist hours by role; validation trials and their compute | Usage logs; time sheets; trial logs | PQ5 |
| M10 | Comfort with data flows; anything participants declined to share | Questionnaire items; debrief | PQ6 |
| M11 | Protocol adherence: questions per turn, leading-phrasing incidents, stopping behaviour | Transcript coding by two coders | PQ7 |
| M12 | Hours and outcome per rung L0–L12; attrition by rung; data-equivalent flagship variants (VVP §2, type 2); agent-trial failures caused by the output format rather than the crux; SP-1 agreement | Validation runs; shepherd records | PQ8 |

## 6. Analysis plan

- **Descriptive.** Report counts, medians and ranges with every individual data point; avoid significance tests the sample cannot support; give exact (Clopper–Pearson) 95% intervals for pooled proportions. With four first-period contributions per arm, only large differences are detectable.
- **M3–M6: first period only**, compared between arms and stratified by fluency and target analysis. Second-period data are secondary, and second-period items related to a first-period suggestion or code pointer are marked post-exposure.
- **M1, M2, M7, M8: within-person**, with period effects reported by arm.
- **Influence measures are validated.** Shared vocabulary makes texts similar without any influence, and similarity is not comparable across English and Chinese. Two coders, blind to the arm, the similarity score and whether the suggestion was shown, judge whether each endorsed item derives from a logged suggestion; suggestion-off decisions, coded against the suggestions that would have been shown, give the baseline. An endorsed known-valid control counts as false only if the arm-blind reviewers, who do not know which items are controls, rate it invalid: in context, a participant may rightly reject a "valid" control.
- **Quality ratings.** The minimal important difference on the 1–7 scale is fixed before the first session (proposed: 1 point). Inter-rater agreement and arm guesses are reported; if guesses clearly beat chance, the comparison is reported as unblinded.
- **Transcripts** are coded for adherence and friction by two coders, with agreement reported.
- **Methodology arm:** candidates entering, passing, repaired and dropped at each rung, with hours by role.

## 7. Pre-registered decision rules (proposed thresholds; the research lead sets the final values)

Writing these down before the pilot keeps the architecture decision honest. Each rule applies identically to both arms. The research lead sets the final values, which are recorded in the [decision log](../decisions/decision-log.md), with who approved them and when, before the first session, and then frozen. A contribution is one participant's work on one target analysis. Rules 4–7 use first-period data; rules 3 and 8 use both periods.

| # | If the pilot shows… | Proposed threshold | …it favours |
|---|---|---|---|
| 1 | Non-fluent economists cannot set up B | Fewer than 3 of 4 non-fluent participants complete B setup within 60 minutes using the designed onboarding (desktop app plus one onboarding session, or their research assistant); unaided completion reported separately | A, or a B variant without the economist's own installation (Option B §3.2; untested here) |
| 2 | Non-fluent economists cannot run A1 run kits | Fewer than 3 of 4 non-fluent A1 contributors, or their research assistants, can run a run kit within 60 minutes using the same designed onboarding; unaided completion reported separately | B, A2, or staff execution |
| 3 | Operationalization stalls | In either arm, fewer than half of the contributions with an approved variant, or fewer than half of the research-assistant-mode contributions, reach a run flawed variant within one week of approval | The other arm, or the stalling arm's own remedy (A: A2 or staff execution; B: Remote Control or SSH variants, or B-staff). If both stall, neither; staff execution becomes the default route |
| 4 | One arm yields more validated variants | Validated, operationalized variants per contribution differ by one or more (all routes counted; route reported) | The higher arm |
| 5 | Quality differs | The share of candidates passing all candidate-stage gates differs by at least 25 percentage points, or paired differences favour one arm, by at least the minimal important difference, in at least 75% of pairs (first-period participants matched on fluency stratum and target analysis) | The better arm. Otherwise quality counts as similar, and the tie-break applies |
| 6 | AI influence is high in one arm | Pooled over the arm's participants: LLM-influenced share (validated coding) above 50% of endorsed items, or adjudicated false endorsement of more than 25% of known-valid controls | Revising that arm's interaction design before scaling, whichever arm is chosen. The same values serve as PR-1's provisional thresholds |
| 7 | Suggestions change valid yield | Valid endorsed items per decision, suggestions on minus off, differ by at least a minimum set before the first session (proposed: 0.5 per decision) | A gain: keep the gated phase in both arms. A loss, or rule 6 exceeded on suggestion-on decisions: drop or narrow it in both. Otherwise record "inconclusive" and keep O-017 open |
| 8 | Participants decline to share materials in one arm | Two or more participants decline in one arm only | The other arm, or a change to that arm's data flow |
| 9 | Interview inference is a minor cost | Interview inference is below 10% of the total cost per task taken through L12, counting validation-trial compute and all hours, with shepherd hours valued at a rate R that the research lead sets (the cost model states effort in hours) | Inference cost does not drive the decision. Otherwise the cost model is revised before deciding |

**Tie-break.** If no rule favours an arm, or the rules conflict, the report sets the evidence side by side, and the decision rests on accessibility, consistency and quality control under real-world account conditions, cost, privacy, sustainability. The environment audit and the observation note (§3.1) inform the second criterion.

## 8. Choosing the pilot paper

**Criteria (in priority order).**

1. Public replication package with **redistributable data** and modest compute.
2. **Two target analyses** of comparable difficulty, each with at least one **established**, consequential pitfall (rubric GT-2, RV-2), ideally differing in some critical decisions.
3. A design familiar to most applied economists (for example, staggered-adoption difference-in-differences, or regression discontinuity), so that participants across fields can contribute.
4. An **available expert**, ideally an original author (Path B).
5. **Fame.** On a canonical paper, recall of the key hits a ceiling and the LLM-originated share is ill-defined, because participants and model alike know the textbook pitfalls. The key therefore includes paper-specific items, and recall is reported separately for textbook and paper-specific items. A less canonical paper that meets criteria 1–4 is preferred for the whole pilot. Otherwise PQ7's recall and influence measures come from an add-on of at least two contributions (one per slice) on a less canonical paper, ideally a participating author's own. None has been identified yet (O-008).

**Candidates verified in [R8](../research/evidence/R8-replication-standards-and-econometric-pitfalls.md) §5** (no recommendation). All four are Top-5 papers with small public data copied into methods packages, and all are canonical teaching examples. Contamination is therefore high: acceptable for comparing workflows, but not for released tasks or for PQ7.

| Candidate | Design | Data facts | Concerns |
|---|---|---|---|
| Stevenson & Wolfers (2006, *QJE*) | Staggered DiD (the illustration in Goodman-Bacon 2021) | `divorce` data in the CRAN package `bacondecomp` (MIT); 3,366 × 147; 692 KB [P-page] | No codebook; provenance and licence of the data [U]. State-specific trends are a contested threat in this literature (Wolfers 2006 [U]), so not a binary key |
| Ludwig & Miller (2007, *QJE*) | Sharp RD (Head Start) | `headstart.csv`, 2,810 counties, 511 KB, with a pre-period placebo outcome; R, Stata, and Python code in a methods repository without a licence file [P-page] | Noisy outcome; a manipulation test means little for a 1960 poverty rate |
| Meyersson (2014, *Econometrica*) | Sharp RD | `polecon`, 2,629 municipalities, 311 KB; no licence file [P-page] | The main teaching example of a widely used RD primer |
| Autor, Dorn & Hanson (2013, *AER*) | Shift-share | Copies in ShiftShareSE (GPL-3), Goldsmith-Pinkham–Sorkin–Swift (MIT), and Borusyak–Hull–Jaravel (GPL-3; 11.5 MB) [P-page] | Licensing of derived data; Stata-version sensitivity. Three independent reference implementations are an advantage |

The original replication-package locations for all four are [U]. Archetypes, with pitfall statuses as corrected by the econometric review (R8 numbering):

| Archetype | Verifiable pitfalls | What to verify |
|---|---|---|
| Staggered-adoption DiD on public state-level panels | Estimator choice under staggered adoption (conditional on effect heterogeneity, shown by diagnostics on the graded data); treatment timing; clustering | Package availability, licence, two target analyses |
| Sharp regression discontinuity with public data | Established: a global high-order polynomial (P10a); conventional confidence intervals at the MSE-optimal bandwidth (P10b); clustering by a discrete running variable (Kolesár & Rothe 2018 [U]). Bandwidth choice (P10c) is a decision-space node, not a failure mode; manipulation testing has no computational consequence. No exact relation tests these pitfalls (VVP §5.5): they are verified through conditional references and validation-time coverage simulations | Same |
| Shift-share (Bartik) design with public data | Exposure-robust standard errors (P12): conditional on shock-based identification (P13), which must be shown to hold | Compute size; licence |

The choice of paper, and whether a collaborator can contribute their own paper, is an Open question for the research lead (O-008).

## 9. Ethics and data handling

- A study of economists' experience with a tool is likely **human-subjects research** under many institutions' rules, even when it qualifies for exemption. Obtain IRB or ethics-committee review (or a documented exemption) at the lead's institution before recruiting (O-013; [evidence note R9](../research/evidence/R9-hosted-stack-and-compliance.md) summarizes guidance).
- Informed consent covers recording, transcript retention, session metrics, the environment audit, data flows to the model provider, and the right to withdraw.
- No restricted or confidential microdata are used: the pilot paper's data must be public.
- Hidden-tier material follows the exposure rules (VVP §10): commercial no-training terms only, every exposure logged (rubric LK-5). After submission, B participants purge local hidden-tier copies and transcripts (Option B §5.2), and A deletes uploads under its retention policy.
- Participants are offered an honorarium and/or contributor credit (the policy is an Open question, O-005).

## 10. Timeline (indicative [U], after Phase 5 authorization)

| When | Activity |
|---|---|
| During the build | Select the paper (and any PQ7 paper); clean-room reference implementations; seal the keys; ethics review; settle model access (O-018); recruit |
| Build | Shared core (pilot subset) and both slices. Effort is in the [cost model](../architecture/cost-and-effort-model.md); calendar time depends on staffing |
| Weeks 1–2 after the build | Simulated-contributor dry runs; A-slice usability dry run; cognitive-interview pretest (EN/ZH); fixes; registration |
| Weeks 3–8 | Setup tests, sessions, asynchronous completion, debriefs |
| Weeks 9–11 | Arm-blind review |
| Weeks 6–18 | Methodology arm (L0–L12), starting as soon as the first candidate qualifies |
| Weeks 18–20 | Pilot report and decision memo for collaborators |

## 11. Pilot outputs

1. Standardized contribution packages from both arms. For each arm that yields an eligible candidate, at least one package has a reference implementation, at least one validated flawed variant with results, a proposed task, and an initial verifier taken through **L12**, with each rung's outcome recorded (the Deliverable 8 requirements).
2. The ladder record: attrition by rung, hours by role, and answers to PQ8.
3. A pilot report answering PQ1–PQ8 against the registered rules, with the environment audit, the blinding check and the observation note.
4. Revised protocol, rubric, schema and cost model (new versions logged), with measured figures replacing the planning estimates (cost model §7).

## 12. Changes

**v0.2.0** (independent reviews, 2026-11-05):
- Analysis: M3–M6 on first-period sessions, between subjects and stratified by fluency; within-person comparisons only for experience measures; cross-period post-exposure marking; at least eight participants; period effects.
- Decision rules symmetric between arms and registered in advance: setup rules for B and for A1 run kits with designed onboarding; stall rules for any hand-off; validated variants; a quality rule on gate pass rates and matched pairs (anchored 1–7 scale); pooled influence thresholds; a suggestion rule with a minimum difference; a restated cost rule; an expanded tie-break.
- A balanced suggestion experiment with all recall locks first; blind validity ratings, influence coding and control adjudication; normalized packages and arm guesses; SP-3 out of blind review.
- Fair arms: commercial terms in both, without consumer plans; B environment audit; A design baseline; staff fallbacks and research-assistant modes in both; concealment; both arms observed.
- A methodology arm through L0–L12 (PQ8, M12); outputs through L12.
- Paper-specific key items; PQ7 on a less canonical paper; corrected RD and shift-share statuses; sessions within the 45–60-minute cap; costs linked to the cost model; O-019.

**v0.1.0** (2026-11-05): first draft.
