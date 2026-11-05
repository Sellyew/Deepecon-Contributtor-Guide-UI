# Reading notes — Bercovich (2026), *Good Benchmarks*

| Field | Value |
|---|---|
| Citation | Ivan Bercovich (2026). *Good Benchmarks*. arXiv:2607.12217v1 [cs.AI], 13 July 2026. 7 pp. |
| Read by | Project lead's research-engineering collaborator (Claude), full text, 2026-11-05 |
| Source used | PDF supplied by the research lead (arxiv.org is not reachable from the cloud environment) |
| Verification level | **Primary — full text read.** Section numbers below refer to the paper. |

## What kind of document this is

*Established fact (from the text):* The paper is a short practitioner essay ("This post is about designing good tasks"), drawn from the Terminal-Bench experience, where contributors "collectively spent thousands of hours developing and reviewing hundreds" of tasks, and from conversations with named Terminal-Bench contributors. It cites five references (Terminal Wrench; Dell'Acqua et al. on the "jagged frontier"; Krakovna et al. on specification gaming; Merrill et al., *Terminal-Bench*, ICLR 2026; METR on reward hacking).

*Our assessment:* Its criteria are **expert practitioner guidance, not empirically validated findings.** The paper does not report measurements of inter-rater agreement, verifier error rates, or the effect of any practice on benchmark validity. We should use it as a well-informed design standard, and where our rubric depends on it, say so, rather than presenting it as established measurement science.

## The seven properties of a good task (§1)

The abstract compresses them as: *"Good tasks are correct, solvable, verifiable, well-specified, and hard for interesting reasons. The best tasks describe a real problem an experienced practitioner would recognize, in language a practitioner would use, with tests that verify the outcome rather than the approach."*

| # | Property | Operational content given in the paper |
|---|---|---|
| 1 | **Verifiable** | Checkable by a program "all-but-guaranteed to detect errors and all-but-guaranteed to accept correct solutions." Reject subjective grading. "Re-running the verifier hundreds of times should show no failures" (timeouts, crashes). |
| 2 | **Well-specified** | The description "completely describes what a correct outcome looks like." Heuristic: if two experts each wrote a verifier from the description, anyone passing one would pass the other. |
| 3 | **Solvable** | A solution or a convincing argument of solvability; someone who knows exactly what to do can solve it within the time and resource limits. |
| 4 | **Difficult** | Hard "for a 'good reason'". |
| 5 | **Realistic and valuable** | "There is a real scenario where a person is paid to do this, and the task mirrors how they actually do it." A puzzle is not enough. |
| 6 | **Outcome-verified** | "We are grading outcomes, not the process to get there." |
| 7 | **Robust** | Same behaviour across time and hardware meeting stated resources; "no unpinned dependencies, no reliance on live external services." |

Additional §1 guidance: the ideal task "can be described in two paragraphs and forces the agent to think before doing anything." "The goal isn't to make the task easy, but to make it unambiguous." "The difficulty should be intrinsic, not a missing fact."

## Key principles by section

**§2 Start from real work.** Early Terminal-Bench tasks were "things one of us had to do at work," converted to the task format; built by people with graduate degrees and practising engineers, with "a lot of peer review."

**§3 What difficulty actually means.**
- Tricky ≠ hard. Deceptive puzzles and hints that mislead create trickiness, not difficulty.
- The common failure is "the mismatch between what we ask for and what we actually want"; the gap is in what is implicit.
- Anti-pattern: start from a working prompt and remove tokens until it fails ("reverse backprop/GEPA"); "It doesn't really make it hard."
- "The hardest tasks tend to be hard the first time." Avoid medium-hard tasks made artificially hard by ambiguity.
- Format-compliance failures (a dollar sign in a float field) measure format compliance, not the target capability.
- Tasks that are "too wide" (many little deliverables) or concatenations of many tasks raise the chance of going off the rails without any one part being hard.
- Near-misses: if an agent gets 90 subgoals right and misses 5, consider focusing the task on those 5. If the near-miss is a single quantitative threshold, "the fix is a new conceptual challenge in the same domain, not a tighter threshold."
- If fixing a bug turns a task from very hard to very easy, look closer at what made it hard.

**§4 Focus on the outcome.** Brief instructions that state the final goal and leave latitude. Do not tell the agent how it will be tested, but state the expected end result so that meeting the instructions implies passing the tests. "Brevity is a KPI." Heuristic: "be as broad as possible and as specific as necessary." If an instruction admits several reasonable approaches, "either the verifier has to accept all of them, or the instruction needs to be tighter"; tightening is usually simpler "because verifiers are the hard part." Full-page requirement documents are usually AI-generated and unaudited: "an instruction can be perfectly well specified and still wrong."

**§5 Prove the task is solvable.** The reference solution should solve the problem "the way an agent would." A hard-coded answer implying knowledge not evident from the instructions signals underspecification. "A proper oracle for a diagnostic task interrogates the system" — it investigates before answering. The deeper test: the author can give "a complete, self-contained path from the instructions to the verified answer," at the level of detail acceptable in their field. Underspecified tasks often arise from "building collaboratively with an AI and then removing pieces of the solution, with no evidence that the removed piece can be reconstructed from the rest."

**§6 Build a controlled environment.** Everything the agent needs is in the environment; the oracle must work from the same information, without privileged information (a common failure in synthetic tasks). Ask whether the environment is hackable; explain *why* a hack is possible and fix the cause; after fixing, re-run the normal solution, because "a fixer can make the task impossible too."

**§7 Make the verifier mean something.**
- Test outcomes, not implementations; do not check which libraries were used; source-code string matching is brittle; "test on examples beyond the one you handed the agent."
- Common root cause of bad verifiers: "a verifier co-designed with the author's own solution: built backwards from one answer rather than derived from the instruction."
- Accepting alternative correct paths is "a discovery process": run agents, see what they try, and widen the verifier where they are legitimately right.
- **Synthetic-data warning:** "When you generate the data from a hypothesis, the verifier can quietly encode an assumption only you hold."
- **Fairness check:** "temporarily over-specify the instruction (name the method, add hints) and confirm a well-guided agent can produce an answer the verifier accepts." If it can, the verifier is fair conditional on the method; if not, look harder at the verifier.
- LLM-as-judge "will find some issues, but not everything"; a human still needs to look at trajectories.
- Should the agent return the answer, or "a piece of software that produces the answer? The latter tends to be more verifiable, more testable."
- Process constraints are justified only as anti-cheat measures.

**§8 Run the task and watch it fail.** Run the oracle, run agents in batches of five, read failures, and ask whether they fail because the task is hard or because it is unfair. Check **crux alignment**: "does what actually broke match what you said would be hard?" Red flags (each "a reason to look closer," none disqualifying alone): pass rate swings on tiny changes; many agents converging on the same wrong answer; review that keeps returning critical concerns after two or three iterations; large instruction surface; hard-coded solution; solution with privileged information; too synthetic; high run-to-run variability in pass rate or cost.

**§9 Keep authorship and review human.**
- LLM-written instructions are recognizable: "the tone is wrong, it's verbose, it's over-structured, and it reads like it was written to maximize the probability the agent succeeds."
- "AI is really good at reviewing tasks. But if the author is also using AI to handle the feedback, it becomes an AI dialogue and the tasks become worse." "If you agree with everything the AI tells you, you end up hill climbing toward a hard task that is too artificial."
- Two kinds of feedback: benchmark correctness (validity, metadata, instruction shape) and deeper correctness, which "takes a domain expert."
- Reviewer bar: "a reviewer who could solve it themselves, and who has made a task before."
- "Being a domain expert and being able to build a good task are different skills." A domain expert "can rarely certify that a task is correct, because certifying it takes an understanding of agent evaluation, not just the domain." Conversely, specialized-sounding work "can fool a non-expert reviewer."
- A model that works: a reviewer **shepherds** each task end to end, ideally the same person "from idea to merge."
- Disputes of the form "this is standard in our field" need "a standard of evidence," like Wikipedia's citation policy. Diagnostic: specify the disputed fact in the instruction; "if the task drops from very hard to very easy, it wasn't testing agentic behavior, it was testing a one-sentence fact, and the task is weak either way."

**§10 Why this matters.** The first several Terminal-Bench 3 proposals were rejected. Some tasks took "months of back-and-forth and well over forty hours of work between a reviewer and an author, both part-time experts." "It's very hard to build a SOTA benchmark for volume." "Quality over quantity."

## Implications for DeepEcon (our analysis — proposals, not decisions)

1. **The paper directly challenges an AI-guided contribution process (§9).** Our central component is an LLM interviewer. Bercovich's warning is that AI-mediated authoring drifts toward artificial, checkbox-satisfying tasks, and that LLM-written instructions are worse than human-written ones. The interview protocol therefore needs explicit safeguards: the contributor originates the scientific content; LLM suggestions are labelled and tracked; agent-facing instructions are written or heavily edited by a human; and an "AI suggestion acceptance rate" is monitored as a quality signal.
2. **"Outcome-verified" versus our Safeguard B ("correct output vs. correct procedure").** These are reconcilable without grading process directly: ask the agent for *software that produces the answer* (§7), then re-run it on hidden variants of the data whose correct outputs are known. A correct procedure passes on held-out variants; a memorized or hard-coded number does not. This preserves outcome-based grading while testing the procedure. *(Corrected 2026-11-05: only partially reconcilable; see [Corrections](#corrections-2026-11-05).)*
3. **Our deliberately flawed implementations map onto the paper's verifier-validation logic.** They are expert-designed negative controls: a verifier must reject them. But §7's "verifier co-designed with the author's own solution" warning applies equally to flawed packages: a verifier built to reject one specific flawed output may still accept other wrong answers, or reject legitimate alternatives.
4. **The "two experts, two verifiers" heuristic (§1) is directly operational** as a well-specification test: two economists independently write acceptance criteria from the agent-facing instruction; disagreements reveal underspecification.
5. **The over-specification fairness check (§7) fits economics well.** Name the estimator or the inference procedure in a temporary version of the instruction; a well-guided agent should then pass. If it does, the residual difficulty lies in *choosing* the method, which is the capability we want to measure.
6. **The "one-sentence fact" diagnostic (§9) creates a genuine tension for economics.** Some of the lead's motivating failure modes (e.g., clustering at the wrong level) may collapse to "one-sentence facts" when the key fact is disclosed. Whether recognizing the need for that fact *is* the target capability is an open methodological question we must resolve explicitly (logged in the decision log as Open).
7. **Domain expert ≠ task builder (§9).** This supports a two-role design: the economist supplies scientific ground truth; a benchmark "shepherd" (our team) handles task and verifier engineering. It also implies that a contribution workflow should not expect economists alone to certify verifiers.
8. **Economics of effort (§10).** Forty-plus hours per task for difficult tasks is a realistic planning anchor for the hardest items. Scale projections must account for shepherd time, not only contributor time.
9. **Robustness (§1, §6) has economics-specific consequences:** proprietary software (Stata) and live data downloads violate "no unpinned dependencies, no live services" unless handled deliberately.
10. **Standard of evidence (§9).** Our ground-truth records should cite authoritative econometric sources for claims that an implementation is wrong, which shortens "this is standard in our field" disputes.

## Corrections (2026-11-05)

*Added on 2026-11-05 after a cross-document consistency review. The notes above are kept unchanged as a dated record; where they conflict with this section, this section supersedes them.*

- **Implication 2 holds only in part.** Outcome grading and procedural correctness are only *partially* reconcilable ([decision log](../../decisions/decision-log.md) P-007). Effect injection alone is blind to how the counterfactual is built, so it is paired with counterfactual-side invariances; answer-changing variants must use bases the agent never sees, or a program can pass by arithmetic (the differential attack); and identification-equivalent flaws cannot be caught by any outcome check. See the [verifier validation protocol](../../methodology/verifier-validation-protocol.md) §2 and §5.
