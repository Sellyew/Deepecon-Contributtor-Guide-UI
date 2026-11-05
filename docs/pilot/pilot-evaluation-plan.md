# Deliverable 8 — Pilot Evaluation Plan

| | |
|---|---|
| **Status** | **Proposed** v0.2.0 (2026-11-05). Not yet reviewed by the research lead. Execution belongs to Phases 5–6, after the architecture review. v0.2.0 integrates four independent reviews (§12). |
| **Purpose** | Replace theoretical argument with evidence: run the *same scientific content* through both contribution workflows, compare what contributors experience and produce, and test the construction method end to end. |
| **Requirement** | Research lead's brief, Deliverable 8 (D-016): one published paper; one validated correct implementation; at least one plausible, consequential error; an expert-guided interview; an erroneous implementation and its results; a proposed task; an initial verifier; a standardized package. |
| **Builds on** | [Interview protocol](../interview/expert-interview-protocol.md) · [verifier validation protocol](../methodology/verifier-validation-protocol.md) (VVP) v0.3.0 · [rubric](../methodology/task-quality-rubric.md) · [Option A](../architecture/option-a-hosted-platform.md) · [Option B](../architecture/option-b-local-skill.md) · [cost model](../architecture/cost-and-effort-model.md) |

---

## 1. Pilot questions

| ID | Question | Why it matters for the decision |
|---|---|---|
| PQ1 | Can economists of differing technical fluency start and complete a contribution in each workflow, and where do they get stuck? | Accessibility (research lead's brief §7) |
| PQ2 | Do the workflows differ in the **quality** of what is produced, judged by reviewers blind to the arm? | Scientific quality — the central criterion |
| PQ3 | Do they differ in **intellectual ownership**: does the dossier reflect the contributor's reasoning rather than the model's suggestions? | Human authority (D-008); *Good Benchmarks* §9 |
| PQ4 | Does in-session execution (B; A2 if tested) change how often failure modes become **operationalized, validated** flawed variants, compared with hand-offs (A1 run kits; research-assistant mode)? | The real value of local execution |
| PQ5 | What does each workflow cost per contribution and per task: inference, support, shepherd hours by execution route (including dropped candidates), outside-economist hours, validation-trial compute? | Cost model calibration |
| PQ6 | How comfortable are contributors with the data flows each workflow implies? | Privacy (Safeguard E) |
| PQ7 | Does the interview protocol itself work: yield, recall of known issues, leading-question rate, stopping behaviour? Recall uses a less canonical paper (§8). | Protocol validity, independent of architecture |
| PQ8 | Which rungs fail? How often are flagship variants data-equivalent? Does re-execution degenerate into format compliance? Do two blind economists agree on SP-1? | Validity and cost of the construction method ([construction protocol](../methodology/benchmark-construction-protocol.md) §9) |

## 2. What is held constant (the "same scientific content")

- **One paper** for the A/B comparison (D-016), with **two target analyses** of comparable difficulty, ideally differing in some critical decisions (R8's candidate pairs are the same specification on another outcome).
- **One reference implementation** per target analysis, checked before any session by a clean-room re-implementation (rubric GT-1; VVP L3).
- **A sealed known-issues key** per target analysis (critical decisions and failure modes), compiled by the project team and one independent economist and never shown during sessions. Each item is tagged **textbook** or **paper-specific** (this paper's data, code or setting). Items not in the key are scored as novel.
- **The same** protocol version, probe library, schema, packager, suggestion procedure and model (Claude Opus 5.5 at a fixed effort level) in both arms, under **commercial no-training terms** (§3.1), with one output contract: a schema-valid package, normalized for review.

## 3. What is built for the pilot (Phase 5, "thin vertical slices")

Both slices share the architecture-independent core (protocol assets, schema, validator, packager); neither is a full product. Both are frozen during sessions; fixes are logged.

| Slice | Minimum functionality | Out of scope for the pilot |
|---|---|---|
| **A-slice** (hosted) | Sign-in, language choice, upload, staged interview with progress display, separate suggestion and checker calls, dossier review with provenance badges, export, research-assistant invitation; **A1** run kits with **staff execution** as the fallback (A's proposed MVP); A2 only if collaborators want it; an off-the-shelf component library and one usability dry run | Public onboarding site, admin dashboards, scaling, a bespoke design system |
| **B-slice** (local) | A downloadable workspace registering the plugin (interview skill, suggestion and checker subagents, state helper, protection of originals, Stata/R/Python run wrappers, packager); pin, block and record model controls; status line and dossier page; suggestions and controls served from the project endpoint; research-assistant hand-off bundle; **B-staff** fallback; EN/ZH installation guides | Marketplace polish, automatic updates, other agent harnesses |

**Effort** ([cost model](../architecture/cost-and-effort-model.md)): roughly 8–14 engineer-weeks for whichever slice is built second [U]. **Open question O-019, for the research lead:** one full slice plus setup and hand-off probes of the other would test the setup rules (1–2, §7) for both arms and probe hand-offs (rule 3), but could not compare yield, quality or influence (rules 4–7). Choosing which slice to build in full would itself lean the decision, so ease of implementation must not drive it (D-005).

### 3.1 Keeping the arms comparable

- **Model access.** Flawed variants and error labels arise in sessions, so all sessions use commercial no-training terms (VVP §10): the project's API account in A; in B, project-provided commercial access (pending O-018) or an institutional commercial account, never a consumer plan, even with the training opt-out. In B, project-provided API keys serve terminal users; the desktop app, rule 1's designed onboarding, requires a Pro, Max, Ultra, Team, or Enterprise subscription sign-in, and Console (API) accounts are documented only for the terminal client ([R2](../research/evidence/R2-claude-code-platform.md) §6.1 [P-page]; whether the app accepts API keys is [U]). B participants who use the desktop app therefore need Team or Enterprise seats, project-provided (also subject to O-018) or institutional. Team Standard seats cost $25 per seat per month ($20 billed annually) and are named, not meant for rotation ([R3](../research/evidence/R3-access-pricing-policy-portability.md) [P-full/P-page]): roughly $25–50 per desktop participant for one to two seat-months [U], instead of about $17 of API usage per contribution, plus seat management. If O-018 is unresolved, B participants need institutional accounts.
- **B-arm environment audit** (at setup and in each package, via Option B's package doctor): client and plugin versions, access route, model-deviation flags, and any user-level `CLAUDE.md`, skills, plugins, MCP servers or output styles (names and hashes, not contents). Provided access standardizes data terms, not the whole interviewer configuration (Option B §5.3). The audit shows how much real-world variation the B sessions carried, which identical access would otherwise hide (tie-break, §7).
- **A design baseline.** A thin slice faces a finished commercial client; the component library and dry run give A a usable baseline, but usability (M8) and drop-off (M2) differences may still reflect product maturity and carry that caveat.
- **Fallbacks.** Both arms keep their staff fallback and research-assistant mode; staff-completed contributions are reported by route, with shepherd hours (M9).
- **Concealment and observation.** Both arms hide suggestion assignments and known-valid controls until the suggestion step and send session metrics to the project, so abandoned sessions are seen; the report states which measures each architecture could collect at scale without this pilot-only instrumentation (Option A §5.4; Option B §4, F12).

## 4. Study design

**Participants.** At least eight economists with Top-5 or leading-field publications: two per sequence, one from each fluency stratum (*fluent*: uses terminal-based AI tools or writes most of their own code; *non-fluent*: delegates code to research assistants). An **original author** of the pilot paper is desirable (it tests Path B), not required.

**Recommended design: crossover on two target analyses**, with order and pairing counterbalanced:

| Sequence | First period | Second period |
|---|---|---|
| 1 | A-slice on T1 | B-slice on T2 |
| 2 | B-slice on T1 | A-slice on T2 |
| 3 | A-slice on T2 | B-slice on T1 |
| 4 | B-slice on T2 | A-slice on T1 |

*What it buys:* within-person comparisons of experience and preferences, not of quality, recall or influence: the second period is primed by the first, and with two participants per sequence, carry-over is inseparable from the arm effect (Grizzle 1965 [U]).

**Sessions** are capped at 45–60 minutes (interview protocol §5); a contribution takes about three (cost model, assumption A2 [U]), so a crossover participant gives about six, plus setup and a debrief. If too demanding, use the **fallback between-subjects design**: one workflow per participant (stratified by fluency), both setup tests, and a 15-minute guided exposure to the other workflow. As M3–M6 are compared between subjects anyway, the fallback loses only the within-person comparisons of M2, M7 and M8.

**Research-assistant condition.** At least two non-fluent participants, one starting in each arm, work in both arms with their own (or a project-provided) research assistant, who performs operationalization (S5) from the hand-off specification (A: platform invitation; B: hand-off bundle, Option B §2.2).

**Suggestion experiment (O-017).** The units are critical decisions pre-registered for each target analysis from the design map; unlisted decisions get no suggestions. Assignment is balanced: each participant has the gated suggestion phase (protocol §7) on for half the listed decisions, and each decision has it on for half the participants per arm, target analysis and period. All free-recall locks of a contribution (S2 decisions, S3 failure modes) precede any suggestion (protocol §6–§7), so no suggestion can prime recall on another decision. The outcome is endorsed items with a complete evidence bundle that arm-blind reviewers rate valid (rule 7).

**Methodology arm (PQ8).** Every candidate whose flawed variant has been run and shows a material consequence under RV-2 (or, if capacity is short, a random sample of at least six, stratified by arm) goes through the validation ladder up to independent review (rungs L0–L12, VVP §3), staffed as the ladder requires (VVP §12). Its blind SP-1 economists, who must not have seen the hidden tier, cannot be participants or arm-blind reviewers. SP-3 is assessed here, through the hint ladder (L10). Each rung records hours by role, outcome (pass, pass after repair, fail, dropped) and reason. Shepherds know the arm, so results are reported by arm but stay out of the decision rules.

**Order of activities.**

1. **Preparation:** dry runs with simulated contributors on both slices (protocol §15), recording the cost of one suite pass; the A-slice usability dry run; a cognitive-interview pretest of the probes (three to five economists per language); registration of the decision list, suggestion assignment, sealed keys and §7 thresholds.
2. **Setup test** on participants' own machines, both arms in counterbalanced order, with the designed onboarding available (one onboarding session, or the participant's research assistant); help requests are logged, unaided completion recorded separately, and the environment audit taken. *B setup* is complete when the workspace opens with the plugin loaded and the skill starts in the participant's language; the *B run test*, when the reference implementation has run through the run wrappers (the model's in-session help allowed); the *A1 run-kit test*, when a sample run kit for the reference implementation has run and its outputs are uploaded.
3. **Sessions**, recorded with consent; **asynchronous completion**, each hand-off timed from the variant's approval; a 20-minute **debrief**, including preferences.
4. **Arm-blind review** of normalized packages (one rendering; client, platform and path identifiers sealed). Two independent economists and a benchmark reviewer rate (i) each endorsed item's validity, blind to arm, suggestion condition and provenance; (ii) each candidate on the candidate-stage gates RV-1 to RV-3 and, as preliminary ratings of later criteria, on RV-4, GT-2 and GT-3 (the remaining candidate-stage gates, LK-5 and PR-1, are checked from the exposure log and the provenance and influence records, not rated blind); (iii) each package on an anchored 1–7 scale (e.g., 1 no usable candidate, 4 usable after substantial revision, 7 ready for task construction). They also guess each package's arm. SP-3 needs agent trials, so it is not rated blind.
5. **Methodology arm**, as above.

## 5. Measures

| ID | Measure | Instrument or source | PQ |
|---|---|---|---|
| M1 | Completion and time for B setup, the B run test, and the A1 run-kit test, with and without designed onboarding; help requests; access route; environment audit | Setup test; logs | PQ1 |
| M2 | Time to first substantive question; active time; sessions per contribution; drop-off stage | Session metrics (both slices) | PQ1 |
| M3 | Yield: failure modes endorsed with a complete evidence bundle; operationalized; validated (run, re-run by the project, material under RV-2); route; time from approval until a variant has been run | Packages; logs; shepherd records | PQ2, PQ4 |
| M4 | Recall of the sealed key on **pre-exposure items only**, separately for textbook and paper-specific items; novel items rated valid | Key comparison; arm-blind review | PQ2, PQ7 |
| M5 | Share of candidates passing all candidate-stage gates; RV-1 to RV-4, GT-2, GT-3; 1–7 rating; inter-rater agreement; arm guesses | Arm-blind review | PQ2 |
| M6 | **Measured AI influence:** LLM-originated, post-exposure and LLM-influenced shares of endorsed items; false endorsement of known-valid controls; weak endorsements; the suggestion-experiment outcome | Recall lists; exposure flags; suggestion ledger; double coding; arm-blind review | PQ3, PQ7 |
| M7 | Perceived ownership and interviewer quality — **an experience measure only**: self-rated ownership did not distinguish experts who followed an AI's planted lean ([R7](../research/evidence/R7-expert-elicitation-and-ai-interviews.md) §3.4) | Post-session questionnaire, fixed in advance | PQ1 |
| M8 | Usability, with the product-maturity caveat (§3.1) | UMUX-Lite or SUS, chosen before the pilot | PQ1 |
| M9 | Inference cost; support minutes; shepherd hours by stage and route, including dropped candidates and staff-run S5; reviewer and outside-economist hours by role; validation-trial compute | Usage logs; time sheets | PQ5 |
| M10 | Comfort with data flows; anything participants declined to share | Questionnaire items; debrief | PQ6 |
| M11 | Protocol adherence: questions per turn, leading-phrasing incidents, stopping behaviour | Transcript coding by two coders | PQ7 |
| M12 | Hours and outcome per rung L0–L12; attrition by rung; data-equivalent flagship variants (VVP §2, type 2); trial failures due to the output format, not the crux; SP-1 agreement | Validation runs; shepherd records | PQ8 |

## 6. Analysis plan

- **Descriptive.** Counts, medians and ranges with every data point; no significance tests the sample cannot support; exact (Clopper–Pearson) 95% intervals for pooled proportions. With four first-period contributions per arm, only large differences show.
- **M3–M6: first period only**, between arms, stratified by fluency and target analysis. Second-period data are secondary; their items related to a first-period suggestion or code pointer are marked post-exposure.
- **M1, M2, M7, M8: within-person**, with period effects reported by arm.
- **Influence measures are validated.** Shared vocabulary makes texts similar without influence, and similarity is not comparable across English and Chinese. Two coders, blind to arm, similarity score and whether the suggestion was shown, judge whether each endorsed item derives from a logged suggestion; suggestion-off decisions, coded against the suggestions that would have been shown, give the baseline. An endorsed known-valid control counts as false only if the arm-blind reviewers, unaware which items are controls, rate it invalid: in context, a participant may be right that a "valid" control is a mistake.
- **Ratings.** The minimal important difference on the 1–7 scale is fixed in advance (proposed: 1 point). Inter-rater agreement is reported for all ratings and coding; if arm guesses clearly beat chance, the quality comparison counts as unblinded.

## 7. Pre-registered decision rules (proposed thresholds; the research lead sets the final values)

Each rule applies identically to both arms. The research lead sets the final values, recorded in the [decision log](../decisions/decision-log.md) with who approved them and when, before the first session; they are then frozen. A contribution is one participant's work on one target analysis; rules 4–7 use first-period data, rules 3 and 8 both periods.

| # | If the pilot shows… | Proposed threshold | …it favours |
|---|---|---|---|
| 1 | B setup or the B run test fails | Fewer than 3 of 4 non-fluent participants complete B setup, and then the B run test, each within 60 minutes using the designed onboarding (desktop app, with a Team or Enterprise seat as in §3.1, plus one onboarding session; or their research assistant); unaided completion reported separately | A, or a B variant without the economist's own installation (Option B §3.2; untested here) |
| 2 | A1 run kits fail | Fewer than 3 of 4 non-fluent A1 contributors, or their research assistants, can run a run kit within 60 minutes with the same designed onboarding; unaided completion reported separately | B, A2, or staff execution |
| 3 | Operationalization stalls | In either arm, fewer than half of the contributions with an approved variant, or of the research-assistant-mode contributions, have a flawed variant run within one week of approval | The other arm, or the stalling arm's remedy (A: A2 or staff execution; B: Remote Control, SSH or B-staff). If both stall, neither; staff execution becomes the default |
| 4 | Yield differs | Validated, operationalized variants per contribution differ by one or more on average (all routes counted; route reported) | The higher arm |
| 5 | Quality differs | The share of candidates passing all candidate-stage gates (rubric Stages 2–4) differs by at least 25 percentage points, or paired differences favour one arm, by at least the minimal important difference, in at least 75% of pairs (first-period participants matched on fluency stratum and target analysis) | The better arm; otherwise quality counts as similar (tie-break) |
| 6 | AI influence is high in one arm | Pooled over the arm's participants: LLM-influenced share (validated coding) above 50% of endorsed items, or adjudicated false endorsement of more than 25% of known-valid controls | Revising that arm's interaction design before scaling, whichever is chosen (also PR-1's provisional thresholds) |
| 7 | Suggestions change valid yield | Valid endorsed items per decision, suggestions on minus off, differ by at least a minimum set in advance (proposed: 0.5 per decision) | A gain: keep the gated phase in both arms. A loss, or rule 6 exceeded on suggestion-on decisions: drop or narrow it. Otherwise record "inconclusive" and keep O-017 open |
| 8 | Participants decline to share | Two or more participants decline to share materials in one arm only | The other arm, or a change to that arm's data flow |
| 9 | Inference is a minor cost | Interview inference below 10% of the total cost per task taken through L12, counting validation-trial compute and all hours (shepherd hours at a rate R set by the research lead) | Inference cost does not drive the decision; otherwise revise the cost model first |

**Tie-break.** If no rule favours an arm, or the rules conflict, the evidence is set side by side and the decision rests on accessibility, consistency and quality control under real-world account conditions, cost, privacy, sustainability. The environment audit and observation note (§3.1) inform the second criterion.

## 8. Choosing the pilot paper

**Criteria (in priority order).**

1. Public replication package with **redistributable data** and modest compute.
2. **Two target analyses** of comparable difficulty, each with at least one **established**, consequential pitfall (rubric GT-2, RV-2), ideally differing in some critical decisions.
3. A design familiar to most applied economists (e.g., staggered-adoption difference-in-differences or regression discontinuity), so participants across fields can contribute.
4. An **available expert**, ideally an original author (Path B).
5. **Fame.** On a canonical paper, participants and model alike know the textbook pitfalls, so recall of the key hits a ceiling and the LLM-originated share is ill-defined. The key therefore includes paper-specific items, and recall is reported separately for textbook and paper-specific items. A less canonical paper meeting criteria 1–4 is preferred for the whole pilot; otherwise PQ7's recall and influence measures come from at least two added contributions (one per slice) on such a paper, ideally a participating author's own. None is identified yet.

**Candidates verified in [R8](../research/evidence/R8-replication-standards-and-econometric-pitfalls.md) §5** (no recommendation; data facts there). All are Top-5 papers with small public data copied into methods packages and canonical teaching examples, so contamination is high: acceptable for comparing workflows, not for released tasks or PQ7. The original package locations are [U]. The choice, including a collaborator's own paper, is Open (O-008).

| Candidate | Design; public copy | Concerns |
|---|---|---|
| Stevenson & Wolfers (2006, *QJE*) | Staggered DiD (Goodman-Bacon 2021's illustration [U]); `divorce` in the CRAN package `bacondecomp` (MIT) [P-page] | No codebook; data provenance and licence [U]. State-specific trends are a contested threat in this literature (Wolfers 2006 [U]), not a binary key |
| Ludwig & Miller (2007, *QJE*) | Sharp RD (Head Start); `headstart.csv`, with a pre-period placebo outcome; no licence file [P-page] | Noisy outcome; a manipulation test means little for a 1960 poverty rate |
| Meyersson (2014, *Econometrica*) | Sharp RD; `polecon`; no licence file [P-page] | The main teaching example of a widely used RD primer |
| Autor, Dorn & Hanson (2013, *AER*) | Shift-share; copies in ShiftShareSE, Goldsmith-Pinkham–Sorkin–Swift and Borusyak–Hull–Jaravel [P-page] | Licensing of derived data; Stata-version sensitivity; three third-party implementations, useful for differential testing; whether any qualifies as GT-1's clean-room check (same target analysis, written without reading ADH's code) is [U] |

**Pitfall statuses by archetype** (R8 numbering, as corrected by the econometric review); for each, verify package availability, licence and two target analyses:
- *Staggered DiD:* estimator choice under staggered adoption (conditional on effect heterogeneity, shown by diagnostics on the graded data); treatment timing; clustering.
- *Sharp RD:* established are a global high-order polynomial (P10a), conventional confidence intervals at the MSE-optimal bandwidth (P10b), and clustering by a discrete running variable (P22; Kolesár & Rothe 2018 [U]). Bandwidth choice (P10c) is a decision-space node, not a failure mode, and manipulation testing has no computational consequence. No exact relation tests them (VVP §5.5); they need conditional references and validation-time coverage simulations.
- *Shift-share:* conventional standard errors (P12) are an error only under shock-based identification (P13). That assumption cannot be shown to hold from data: the instruction must state it, and shock-level balance tests and the effective number of shocks are recorded as supporting diagnostics.

## 9. Ethics and data handling

- The study is likely **human-subjects research** under many institutions' rules, even if exempt: obtain ethics review or a documented exemption before recruiting (O-013; [R9](../research/evidence/R9-hosted-stack-and-compliance.md) summarizes guidance). Consent covers recording, transcript retention, session metrics, the environment audit, data flows to the model provider, and withdrawal.
- The pilot paper's data must be public; no restricted or confidential microdata are used.
- Hidden-tier material follows VVP §10, with every exposure logged (rubric LK-5). After submission, B participants and their research assistants purge local hidden-tier copies (including imported hand-off bundles) and transcripts (Option B §5.2), and A1 participants and their research assistants delete run kits and their outputs; A deletes uploads under its retention policy.
- Honorarium and/or contributor credit: an Open question (O-005).

## 10. Timeline (indicative [U], after Phase 5 authorization)

| When | Activity |
|---|---|
| Build | Shared core (pilot subset) and both slices; calendar time depends on staffing. In parallel: paper selection, clean-room reference implementations, sealed keys, ethics review, model access (O-018; Team seats for B-arm desktop users), recruitment |
| Weeks 1–2 after the build | Preparation (§4, step 1); fixes |
| Weeks 3–8 | Setup tests, sessions, asynchronous completion, debriefs |
| Weeks 9–11 | Arm-blind review |
| Weeks 6–18 | Methodology arm (L0–L12), from the first eligible candidate |
| Weeks 18–20 | Pilot report and decision memo |

## 11. Pilot outputs

1. Standardized packages from both arms; for each arm with an eligible candidate, at least one with a reference implementation, a validated flawed variant with results, a proposed task, and an initial verifier taken through **L12**, each rung's outcome recorded (the Deliverable 8 requirements).
2. The ladder record: attrition by rung and hours by role (PQ8).
3. A report answering PQ1–PQ8 against the registered rules.
4. Revised protocol, rubric, schema and cost model, with measured figures replacing planning estimates (cost model §7).

## 12. Changes

**v0.2.0** (independent reviews, 2026-11-05):
- First-period, between-subject analysis of M3–M6; at least eight participants; decision rules symmetric between arms and registered in advance.
- Balanced suggestion experiment; blind ratings, coding and adjudication; normalized packages; SP-3 out of blind review.
- Commercial terms, staff fallbacks and observation in both arms; B environment audit; A design baseline.
- Methodology arm through L0–L12 (PQ8); paper-specific key items; PQ7 on a less canonical paper; corrected RD and shift-share statuses; sessions within the cap; O-019.
- Cross-document consistency pass (2026-11-05): Team or Enterprise seats for B-arm desktop users and API keys for terminal users, with the seat cost (§3.1, rule 1, §10); a B run test matching the A1 run-kit test (§4, M1, rule 1); candidate-stage gates as in the rubric's stage map (§4); the shift-share condition stated as an untestable identifying assumption (§8); the ADH implementations not assumed to meet GT-1 (§8); local hidden-tier copies deleted in both arms (§9); clearer methodology-arm and rule 3 wording; the research lead's brief named explicitly.

**v0.1.0** (2026-11-05): first draft.
