# R11: LLM assistance in benchmark construction: practice and risks

| Field | Value |
|---|---|
| Topic | How established benchmarks use LLMs to generate, refine, filter, and validate tasks; whether this creates contamination, leakage, or measurement risks; what follows for DeepEcon's candidate items |
| Date | 2026-11-06. All sources accessed 2026-11-06. |
| Author | lead collaborator (Claude session), answering the research lead's question of 2026-11-06 |
| Method | Five research agents (the Terminal-Bench family; expert-written question benchmarks; agent, code, and science benchmarks; the risk literature; LLM-injected versus natural errors), each followed by an independent verifier who re-opened sources and corrected labels. Of 150 claims re-checked, 109 held as stated, 20 were corrected, and 21 could not be re-checked because their hosts were unreachable; none was refuted. Only verified wording is used here. |
| Evidence labels | As in the [evidence README](README.md). Repository files read from fresh clones are [P-page] or [P-full], with the commit. Claims seen only in search summaries are [S]. Text marked *(assessment)* is analysis. |
| Access limits | arxiv.org, openai.com, help.openai.com, ai.google.dev, cdn.deepseek.com, tbench.ai, huggingface.co, openreview.net, and several journal and press hosts were unreachable. Most paper-level claims are therefore [S]; repository-level claims are primary. |
| Relation to other notes | Extends [R1](R1-terminal-bench-science.md) §1.3 and §5, [R4](R4-replication-benchmarks.md) §2.6, [R5](R5-analysis-causal-econ-benchmarks.md) (BLADE), [R6](R6-error-detection-and-verifier-methodology.md), [R3](R3-access-pricing-policy-portability.md) §6, and [R10](R10-contamination-and-evaluation-isolation.md). Supports proposal P-054 in the [decision log](../../decisions/decision-log.md). |

---

## 1. Short answer

*(assessment)*

1. **No established benchmark examined bans LLM assistance in construction.** The norm is LLM assistance under human or expert review.
2. **Where benchmarks restrict LLMs, the rules are of two kinds**, and neither is a ban motivated by contamination:
   - **authorship rules** for agent-facing text, motivated by quality (the Terminal-Bench family);
   - **destination rules** about services that may train on the material (METR).
3. **In DeepEcon a drafted candidate error *is* the answer key.** Drafting it with a hosted model therefore exposes the answer key to that provider. With a locally run model, the lead's distinction between assisting construction and exposing answers holds exactly. With a hosted model, it holds only as far as the provider's terms are trusted.
4. **The larger documented risks are to measurement, not leakage:**
   - errors that are unrealistic or easier than real ones;
   - "errors" that are not actually wrong;
   - bias toward or against the model family that drafted or filtered the items;
   - style artifacts an agent could exploit.

   Expert review addresses realism. It does not remove generator-family bias or reviewers' anchoring on the proposals.

## 2. The Terminal-Bench family (repositories cloned 2026-11-06)

| Practice | Evidence | Label |
|---|---|---|
| TBS restricts AI help only for the agent-facing instruction and the reference solution. CONTRIBUTING says "Write this file yourself as a domain expert without AI assistance for best quality". The PR checklist asks for a human-written `instruction.md` and a `solve.sh` "written by a human (with minimal help from a language model)". The implementation rubric says "Tests should be hand-written, readable, and concise" (LLM-judged guidance, not enforced). There is no rule for environments or data | `harbor-framework/terminal-bench-science@1afc8ec`: CONTRIBUTING.md, `.github/pull_request_template.md`, `rubrics/task-implementation.toml` | [P-full] / [P-page] |
| The stated reason is quality. No TBS document gives leakage or contamination as the reason. *Good Benchmarks* §9 adds that an author who lets AI answer AI review drifts toward worse, artificial tasks | grep over CONTRIBUTING, REVIEWING, TASK_REVIEW_AUTOMATION, rubrics, PR template; project reading notes on Bercovich (2026) | [P-page]; [P-full] |
| Enforcement is self-attestation plus advisory detection. A reviewer-run Pangram check is "Advisory — it gates nothing". A GPTZero script exists but is not wired into CI. The rubric judge is told "Instructions may be created with language-model assistance. Evaluate the final text, not its presumed authorship" | TASK_REVIEW_AUTOMATION.md; `ci_checks/check-ai-detection.py`; `rubrics/task-implementation.toml` | [P-full] / [P-page] |
| Terminal-Bench 3 is stricter about prose: its rubric says "LLM-generated instructions raise concern and should be flagged"; README explanations "MUST be written completely by a human"; yet it expects development "with a coding agent" | `harbor-framework/terminal-bench-3@fbf8a8c` | [P-full] |
| Harbor, the framework underneath, expects coding agents to help build tasks. Its `create-task` skill guides an agent through writing the task. Its CONTRIBUTING says "Code can be written by agents. Docs ... should be written by a human with AI assistance" and "you are in charge of the *first* draft and the *last* draft but can use agents in between" | `harbor-framework/harbor@7367e80` | [P-page] / [P-full] |
| **TBS sends complete unreleased tasks, solutions and tests included, to hosted providers during review.** Implementation review: Codex with GPT-6 Astra, which reads all task files. Trial and cheat analysis: Claude Code with Claude Opus 5.5, since 2026-11-05. Hardening: Gemini 3.5 Flash. Red-team trials: Kimi K3.1 Pro. Contributors run the same checks on their own keys. No provider's data-use terms are cited | `.github/llm-config.yml`; Harbor `checker.py`, `analyzer.py` | [P-page] |
| TBS's only recorded worry about model-API exposure concerns intermediaries. Routing judges through a router was logged as an accepted risk because "unreleased-task material (instruction.md, tests/, ground_truth.json, full trajectories)" passed through "a shared account pool whose retention is unknown". TBS tolerates direct provider calls because its tasks are public anyway: PRs are on a public repository and answer keys are committed at merge | `.github/llm-config.yml` comments; TASK_REVIEW_AUTOMATION.md | [P-page] |
| TBS warns against adversarial filtering: generating many candidates and keeping those that frontier models fail risks "finding trivial corners of capability gaps specific to the current models" | CONTRIBUTING.md §Task Difficulty | [P-full] |

## 3. Other benchmarks

| Benchmark | LLM role in construction | Human gate | Documented problems | Label |
|---|---|---|---|---|
| Humanity's Last Exam | Every candidate was run against frontier models and rejected if they solved it; about 13,000 submissions reached expert review, giving 2,500 questions; LLM judge at evaluation | Expert review rounds | A FutureHouse audit (itself agent-assisted) estimated 29 ± 3.7% of 321 text-only biology and chemistry answers conflict with the literature, attributed to the "stump the model" incentive | [S]; counts in README [P-page] |
| GPQA | None found; LLMs only as baselines; answer-only baselines check for option artifacts | Expert writers, expert validators, non-expert solvers | — | [P-page] |
| MMLU-Pro | GPT-4-Turbo extracted answers and generated extra distractors (4 to 10 options); models flagged likely false negatives for experts | Two expert review phases | Many generated distractors were in fact correct answers ("false negatives"; 1,953 in the MMLU source alone) | [S]; README [P-page] |
| SuperGPQA | Rule-based, then LLM-based, then expert quality inspection ("Human-LLM collaborative filtering") | More than 80 expert annotators | — | [S] |
| SimpleQA | Questions kept only if GPT-4-family answers were wrong (adversarial collection) | Second trainer's independent answer | SimpleQA Verified later found noisy labels and redundancy | [S] |
| HealthBench | LLM-generated conversations from physician-defined scenarios; physicians shown model reference completions | 262 physicians wrote the rubrics | — | [P-page] / [S] |
| FrontierMath | Expert-written; a later LLM-assisted audit flagged problems that mathematicians confirmed | Peer review by mathematicians | Error estimates conflict across low-quality secondary sources | [S] |
| SWE-bench Verified | None reported | Professional developers screened 1,699 samples | Weak tests; agents read future commits (R10) | [S] |
| BigCodeBench | GPT-4 expanded seed tasks; annotators refactored and wrote tests with LLM help | Tasks "pre-evaluated on other LLMs, and cross-checked by 7 additional human experts"; 11 experts solved a sample at 97% | — | [P-page] (blog source) |
| ScienceAgentBench | Human-written tasks; rubrics for human evaluation reportedly drafted by GPT-4o and revised by experts | "multiple rounds of manual validation by annotators and subject matter experts" | False negatives in evaluation, hence a verified split | [P-page] / [S] |
| SciCode | GPT-4 reportedly one of three validation rounds | Scientists wrote gold solutions and tests | — | [P-page] / [S] |
| PaperBench | o1 helped authors understand papers but could not write reliable rubrics end to end; an optional OpenAI call categorizes rubric nodes | Rubrics co-developed with one author of each paper | Rubric writing by hand limited the benchmark to 20 papers | [P-page] / [S] |
| BixBench | An LLM proposed candidate questions for each expert-built analysis capsule | Experts approved, rejected, or edited each question (the closest analogue to DeepEcon's Selection step) | — | [S]; repository [P-page] |
| ReplicationBench-Plus | An LLM given the paper proposed up to 10 tasks per paper; experts curated 58 | Kept separate from the 111 expert tasks by a paper-level `source` field | The release evaluation code, the default loader, and the Harbor adapter all use expert tasks only; no comparison of results by source published | [P-page] |
| BLADE (social-science data analysis) | LLM-generated negatives for "select the unjustifiable option" questions, flagged `is_llm_generated` | Expert review of alternatives | Some LLM negatives are implausible or infeasible with the data (R5) | [P-page] |
| SWE-smith (training data, not evaluation) | LLM-planted bugs ("chaos monkey testing"; "subtle and challenging to detect") | None per instance; kept if at least one test fails | On a model-rated scale, 441 of 1,000 LM Modify bugs are easy, against 438 of 2,294 real SWE-bench tasks | [P-page] |
| FLAWS; PaperAudit-Bench | LLMs insert errors into paper text | No documented human realism check | The inserting model changes difficulty; FLAWS discards errors its inserter can find, making each subset adversarial to its own inserter | [S]; PaperAudit code [P-page] |
| SPOT (real errors) | GPT-4o filtering passes and GPT-4.1 matching around a human gate | Original authors confirm each error | Even real-error benchmarks use LLMs in processing | [P-page] |
| METR (RE-Bench, task template) | No authorship rule; a destination rule: "Avoiding providing evaluation material to APIs or services that may use the material for training"; task repositories kept private | — | — | [P-page] |

## 4. Risks of LLM-assisted construction

| Risk | Evidence | Size | Mitigations |
|---|---|---|---|
| **Exposure to the provider** that runs the model | Balloccu et al. (EACL 2024): about 42% of roughly 212 papers that evaluated ChatGPT or GPT-4 sent benchmark data through the ChatGPT web interface, whose terms then allowed training; this measures *permitted* exposure, not proven training [S]. Shared chat links were indexed by search engines in 2025 [S]. ARC-AGI-2 runs hosted models only on a "semi-private" set "with low leakage probability", and keeps a fully private set for self-contained models [P-page] | Depends on the channel and terms, not on LLM use as such. Zero for a local model | Local model; or an API under terms that exclude training, configured by the research lead; never personal chat accounts; log every use |
| **Generator or self-preference bias** | LLM judges recognize and favour their own outputs (Panickssery et al. 2024; MT-Bench reported about 10% for GPT-4 and 25% for Claude-v1) [S]. In LLM-generated translation benchmarks each model ranked itself first; in retrieval the effect on rankings was small [S]. No study measures it for planted errors in research code | Unknown for DeepEcon; could favour or disfavour the drafting family | Record the drafting model per item; prefer a drafting model outside the evaluated set, or several families; report scores by drafting family |
| **Adversarial-filtering bias** | Phang et al. (2022): filtering against a chosen model makes rankings unstable and over-samples contested labels [S]; HLE's construction makes low scores for the filter models partly a product of design [S]; TBS warns against it [P-full] | Large for comparisons across model families | Do not keep or drop candidates by whether frontier models catch them (consistent with P-034) |
| **Unrealistic, easier, or not-actually-wrong errors** | Asking an LLM to "insert a bug" gives local, easier bugs (SWE-smith difficulty ratings [P-page]; BugPilot: deliberately planted bugs are local and less useful than bugs arising in real work [P-page, authors' blog]). LLM mutants resemble real faults more than rule-based ones but are more often equivalent, that is, not wrong [S]. LLM negatives in BLADE are partly implausible [P-page] | Moderate; expert rejection shares of about 10–30% are typical where LLM flags are checked by people [S] | Expert review against realism and consequence; executable confirmation that the error changes results as claimed; a "not actually an error" verdict in review |
| **Style artifacts** | Model-written options are easier to spot from style alone (choices-only shortcuts strongest where distractors are model-written) [S]; TBS's procedural injector left shortcut artifacts found in review [P-full, R1] | Untested for code edits in hand-written Stata or R *(assessment)* | Humans edit accepted changes to the author's style; artifact probes before release (P-052) |
| **Expert review is necessary but not sufficient** | HLE and FrontierMath had high answer-key error rates despite expert review; later audits, often LLM-assisted, found them [S]. Reviewers anchor on suggestions (R7) | — | Keep the contributor's "propose an addition" path prominent; use LLMs also as reviewers, advisory only |

## 5. Provider data-use defaults (dated 2026-11-06; re-check before relying on them)

| Provider | API or business use | Consumer chat use | Label |
|---|---|---|---|
| Anthropic | Commercial terms: "Anthropic may not train models on Customer Content from Services" | Consumer plans may be trained on unless the user opts out; feedback and safety-flagged content are exceptions | [P-page], R3 §6 |
| OpenAI | API and ChatGPT Business, Enterprise, Edu not used to improve models by default | Personal ChatGPT plans trained on by default unless "Improve the model for everyone" is off | [S] |
| Google | Gemini API paid services not used to improve products; unpaid tier may be read by reviewers and used | Gemini Apps activity used to train, on by default for adults | [S] |
| DeepSeek | Open Platform terms let customers use outputs freely; whether DeepSeek trains on API traffic is **unresolved** | Consumer app may use inputs to improve services, with an opt-out | [S] / [U] |

## 6. Implications for DeepEcon

*(assessment; summarized as proposal P-054)*

1. A prohibition is not needed. LLMs may help draft, vary, refine, and check candidate items, provided experts validate every item and each change is confirmed by running it.
2. Where the model runs is the leakage question, and it follows the tiers already decided (D-018, D-032):
   - **Questions about public material only** (understanding the published paper and its public package, with no candidate errors in the prompt or the answer) expose nothing new. The LLM use policy (Proposed) allows any tool for public material, but D-018's text covers "paper materials", so the research lead should confirm.
   - **Development tasks:** a local model, or an external API the research lead configures.
   - **Evaluation tasks:** a local model. D-032 says their agent-facing packages reach a provider only in an evaluation run, and a drafted error is part of that package and of the answer key. Hosted drafting would need the lead to amend D-032, for example ARC-style: log it and report that provider's models separately on the task. DeepSeek's API training terms are unresolved (§5), and DeepSeek's models may be evaluated.
   - **Held-out tasks:** local model only (D-031, D-032).
3. Provenance per item is the main validity safeguard. Record whether each candidate came from the team, an LLM (which model, local or external), or the contributor, and who edited and validated it. Convention 4 and the team's plan ("origin (expert / AI / team)") already require this. Report results by origin and by drafting family; no published benchmark has done so for planted research errors.
4. Agent-facing text and code edits are written or finally edited by people, as in the Terminal-Bench family. This also reduces style artifacts.
5. Do not filter candidates by whether frontier models miss them.

## 7. Corrections to earlier notes

- **R1 §5** (2026-11-05), "Trial analysis" row: TBS's `analyze` judge moved from Codex with GPT-6 Astra to Claude Code with Claude Opus 5.5 on 2026-11-05 [P-page, `.github/llm-config.yml` comments]. R1 also missed the rubric line on hand-written tests (§2 above).
- **Balloccu et al.:** the "about 42%" figure refers to about 90 of roughly 212 papers that evaluated ChatGPT or GPT-4, not to all 255 papers screened [S].

## 8. Gaps

- The papers for HLE, Terminal-Bench 2.0, MMLU-Pro, BigCodeBench, PaperBench, and FLAWS were not read (arXiv is blocked); their construction details are [S].
- No study found measures generator-family bias for planted errors in code or empirical research, or compares how hard LLM-planted and human-designed errors are to detect on the same paper.
- No current, primary OpenAI, Google, or DeepSeek terms were read; §5 entries other than Anthropic's are [S].
