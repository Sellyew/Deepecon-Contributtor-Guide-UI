# R11: LLM assistance in benchmark construction: practice and risks

| Field | Value |
|---|---|
| Topic | How established benchmarks use LLMs to generate, refine, filter, and validate tasks; whether this creates contamination, leakage, or measurement risks; what follows for DeepEcon's candidate items |
| Date | 2026-11-06. All sources accessed 2026-11-06. |
| Author | lead collaborator (Claude session), answering the research lead's question of 2026-11-06 |
| Method | Everything here was done by AI agents, not by human researchers: Claude subagents launched from this session, with web search, fetching of reachable pages, and read-only clones of public repositories. Five research agents covered five slices: the Terminal-Bench family; expert-written question benchmarks; agent, code, and science benchmarks; the risk literature; and LLM-injected versus natural errors. Their reports made 286 claims. Five further Claude agents, the verifiers, re-checked 150 of them and two takeaways, 152 checks in all: 109 held as stated, 20 were corrected, and 23 could not be confirmed, mostly because the source host was unreachable or not fetched. None was refuted. Where a claim was re-checked, the wording here follows the verifier's correction. Rows that rest on claims no verifier re-checked keep the reporter's label. Four more Claude agents then reviewed this note against the verified results. The verifiers are separate model instances but the same model family, so their checks catch misquotes and wrong labels but are not independent in the way a human check would be. |
| Evidence labels | As in the [evidence README](README.md). Repository files read from fresh clones are [P-page] or [P-full], with the commit. Claims seen only in search summaries are [S]. Text marked *(assessment)* is analysis. |
| Access limits | Unreachable hosts: arxiv.org, openai.com, help.openai.com, ai.google.dev, cdn.deepseek.com, tbench.ai, huggingface.co, openreview.net, and several journal and press hosts. Paper-level claims are therefore mostly [S]; repository-level claims are primary. |
| Relation to other notes | Extends [R1](R1-terminal-bench-science.md) §1.3 and §5, [R4](R4-replication-benchmarks.md) §2.6, [R5](R5-analysis-causal-econ-benchmarks.md) (BLADE), [R6](R6-error-detection-and-verifier-methodology.md), [R3](R3-access-pricing-policy-portability.md) §6, and [R10](R10-contamination-and-evaluation-isolation.md). Informed proposal P-054, which the research lead's framework reset of 2026-11-07 replaced with D-039 and D-040 ([decision log](../../decisions/decision-log.md); [AI use and integrity rules](../../architecture/llm-use-policy.md)). |

---

## 1. Short answer

*(assessment)*

1. **No established benchmark examined bans LLM assistance in construction.** The norm is LLM assistance, usually under human or expert review.
2. **Where benchmarks restrict LLMs, the rules are of three kinds.** None is a ban motivated by contamination.
   - **Authorship rules**, motivated by quality: the instruction and the reference solution, plus tests in rubric guidance (the Terminal-Bench family).
   - **Destination rules**, about services that may train on the material (METR).
   - **Validation rules**, motivated by independence: GPQA's non-expert validators had web access but no AI assistants [S, one secondary summary].
3. **In DeepEcon a drafted candidate error *is* the answer key.**
   - With a locally run model, the lead's distinction between assisting construction and exposing answers holds exactly.
   - With a hosted model, drafting sends answer-key material to that provider. Under D-032 the task is then exposed, so it can only be a development task.
4. **The larger documented risks are to measurement, not leakage:**
   - errors that are unrealistic, easier than real ones, or not actually wrong, depending on how they are generated;
   - bias toward or against the model family that drafted or filtered the items;
   - style artifacts an agent could exploit.

   Expert review addresses realism. It does not remove generator-family bias or reviewers' anchoring on the proposals.

## 2. The Terminal-Bench family (repositories cloned 2026-11-06)

| Practice | Evidence | Label |
|---|---|---|
| TBS's authorship rules cover the agent-facing instruction and the reference solution, attested in the PR checklist. CONTRIBUTING says "Write this file yourself as a domain expert without AI assistance for best quality". The checklist asks for a human-written `instruction.md` and a `solve.sh` "written by a human (with minimal help from a language model)". The rubric asks that "Tests should be hand-written, readable, and concise", as LLM-judged guidance that is not enforced. There is no rule for environments or data | `harbor-framework/terminal-bench-science@1afc8ec`: CONTRIBUTING.md, `.github/pull_request_template.md`, `rubrics/task-implementation.toml` | [P-full] / [P-page] |
| The stated reason is quality; no TBS document gives leakage or contamination as the reason. *Good Benchmarks* §9 adds that an author who lets AI answer AI review drifts toward worse, artificial tasks | grep over CONTRIBUTING, REVIEWING, TASK_REVIEW_AUTOMATION, rubrics, PR template; project reading notes on Bercovich (2026) | [P-page]; [P-full] |
| Enforcement is self-attestation plus advisory detection. A reviewer-run Pangram check is "Advisory — it gates nothing". A GPTZero script exists but is not wired into CI. The rubric judge is told "Instructions may be created with language-model assistance. Evaluate the final text, not its presumed authorship" | TASK_REVIEW_AUTOMATION.md; `ci_checks/check-ai-detection.py`; `rubrics/task-implementation.toml` | [P-full] / [P-page] |
| Terminal-Bench 3 is stricter about prose. Its rubric says "LLM-generated instructions raise concern and should be flagged", and README explanations "MUST be written completely by a human". Yet it expects development "with a coding agent" | `harbor-framework/terminal-bench-3@fbf8a8c` | [P-full] / [P-page] |
| Harbor, the framework underneath, expects coding agents to help build tasks: its `create-task` skill guides an agent through writing one. For contributions to the framework itself (not tasks), its CONTRIBUTING says "Code can be written by agents. Docs ... should be written by a human with AI assistance" and "you are in charge of the *first* draft and the *last* draft but can use agents in between" | `harbor-framework/harbor@7367e80` | [P-page] / [P-full] |
| **TBS sends complete unreleased tasks, solutions and tests included, to hosted providers during review.** Implementation review: Codex with GPT-6 Astra, which reads all task files. Trial and cheat analysis: Claude Code with Claude Opus 5.5, since 2026-11-05. Hardening: Gemini 3.5 Flash. Red-team trials: Kimi K3.1 Pro (agent-facing material and trajectories only). Contributors run the same checks on their own keys. No provider's data-use terms are cited | `.github/llm-config.yml`; Harbor `checker.py`, `analyzer.py` | [P-page] |
| TBS's only recorded worry about model-API exposure concerns intermediaries. Routing judges through a router was logged as an accepted risk, because "unreleased-task material (instruction.md, tests/, ground_truth.json, full trajectories)" passed through "a shared account pool whose retention is unknown". TBS gives no reason for allowing direct provider calls. *(assessment)* They cost it little: its PRs sit on a public repository and its answer keys are committed at merge | `.github/llm-config.yml` comments; TASK_REVIEW_AUTOMATION.md | [P-page] |
| TBS warns against adversarial filtering. Generating many candidates and keeping those that frontier models fail risks "finding trivial corners of capability gaps specific to the current models" | CONTRIBUTING.md §Task Difficulty | [P-full] |

## 3. Other benchmarks

| Benchmark | LLM role in construction | Human gate | Documented problems | Label |
|---|---|---|---|---|
| Humanity's Last Exam | Every candidate was run against frontier models and rejected if they solved it. About 13,000 submissions reached expert review, giving about 2,500 questions at release (since revised). An LLM judges at evaluation | Expert review rounds | FutureHouse, in an audit that was itself agent-assisted, estimated that 29 ± 3.7% of 321 text-only biology and chemistry answers conflict with the literature. It attributed this to "the incentive used to build the benchmark". The HLE team's own follow-up put the share at about 18% of a biology and chemistry subset | [S]; 2,500 in README [P-page] |
| GPQA | None found in the repository (papers not read); LLMs appear only as baselines. Answer-only baselines check whether the options give the answer away | Expert writers, expert validators, and non-expert solvers working without AI assistants | — | [P-page]; validators without AI [S] |
| MMLU-Pro | GPT-4-Turbo extracted answers and generated extra distractors (from 4 to 10 options). Models flagged likely false negatives for the experts | Two expert review phases | Many generated distractors were in fact correct answers ("false negatives"): 1,953 in the MMLU source alone | [S]; README [P-page] |
| SuperGPQA | Quality inspection that is rule-based, then LLM-based, then expert ("Human-LLM collaborative filtering") | More than 80 expert annotators | — | [S] |
| SimpleQA | Questions kept only if GPT-4-family answers were wrong (adversarial collection) | A second trainer answered each question independently [U] | SimpleQA Verified later found noisy labels and redundant questions | [S]; human gate [U] |
| HealthBench | LLM-generated conversations from physician-defined scenarios; physicians were shown model reference completions | 262 physicians wrote the rubrics | — | [P-page] / [S] |
| FrontierMath | Expert-written; a later LLM-assisted audit flagged problems that mathematicians confirmed | Peer review by mathematicians | Error estimates conflict across low-quality secondary sources | [S] |
| SWE-bench Verified | None reported | Professional developers screened 1,699 samples | Weak tests; agents read future commits (R10) | [S] |
| BigCodeBench | GPT-4 expanded seed tasks; annotators refactored the programs and wrote tests with LLM help | Tasks "pre-evaluated on other LLMs, and cross-checked by 7 additional human experts"; 11 experts solved a sample at 97% | — | [P-page] (blog source) |
| ScienceAgentBench | Human-written tasks; the rubrics for human evaluation were reportedly drafted by GPT-4o and revised by experts | "multiple rounds of manual validation by annotators and subject matter experts" | False negatives in evaluation, hence a verified split | [P-page] / [S] |
| SciCode | GPT-4 was reportedly one of three validation rounds | Scientists wrote gold solutions and tests | — | [P-page] / [S] |
| PaperBench | o1 helped authors understand papers but could not write reliable rubrics end to end. An optional OpenAI call categorizes rubric nodes | Rubrics co-developed with one author of each paper | Writing rubrics by hand limited the benchmark to 20 papers | [P-page] / [S] |
| BixBench | An LLM proposed candidate questions for each expert-built analysis capsule | Experts approved, rejected, or edited each question. This is the closest analogue to DeepEcon's Selection step | — | [S]; repository [P-page] |
| ReplicationBench-Plus | An LLM given the paper proposed up to 10 tasks per paper; experts curated 58 | Kept apart from the 111 expert tasks by a paper-level `source` field | The release evaluation code, the default loader, and the Harbor adapter all use expert tasks only. No comparison of results by source has been published | [P-page]; LLM generation [S] |
| BLADE (social-science data analysis) | LLM-generated negatives for "select the unjustifiable option" questions, flagged `is_llm_generated` | Expert review of alternatives | Some LLM negatives are implausible or infeasible with the data (R5) | [P-page] |
| SWE-smith (training data, not evaluation) | LLM-planted bugs ("chaos monkey testing"; "subtle and challenging to detect") and LLM rewrites of functions | None per instance: a bug is kept if at least one test fails and at least one still passes | Model-rated difficulty depends on the method. 441 of 1,000 planted (LM Modify) bugs are rated easy, against 438 of 2,294 real SWE-bench tasks, but LLM rewrites are rated harder than real tasks (mean 5.272 against 5.014) | [P-page] |
| FLAWS; PaperAudit-Bench | LLMs insert errors into paper text | No documented human check of realism | In FLAWS, errors inserted by GPT-5 were harder to find, and only about 5% of them survived filtering. The authors cannot separate the effect of the generator from that of the filter. *(assessment)* FLAWS discards errors that the inserting model finds itself, which may make each subset adversarial to its own inserter | [S]; PaperAudit code [P-page] |
| SPOT (real errors) | Two GPT-4o filtering passes and GPT-4.1 normalization of papers. GPT-4.1 also matches flags to errors at evaluation | The original authors confirm each error | Even real-error benchmarks use LLMs in processing | [P-page] |
| METR (RE-Bench, task template) | No authorship rule. A destination rule: "Avoiding providing evaluation material to APIs or services that may use the material for training". Task repositories are kept private | — | — | [P-page] |

## 4. Risks of LLM-assisted construction

| Risk | Evidence | Size | Mitigations |
|---|---|---|---|
| **Exposure to the provider** that runs the model | Balloccu et al. (EACL 2024): about 42% of roughly 212 papers that evaluated ChatGPT or GPT-4 sent benchmark data through the ChatGPT web interface, whose terms then allowed training. This measures *permitted* exposure, not proven training [S]. Shared chat links were indexed by search engines in 2025 [S]. ARC-AGI-2 runs hosted models only on a "semi-private" set "with low leakage probability", and keeps a fully private set for self-contained models [P-page] | Depends on the channel and its terms, not on LLM use as such; zero for a local model | A local model, or an API under terms that exclude training, configured by the research lead. Never personal chat accounts. Log every use |
| **Generator or self-preference bias** | LLM judges recognize and favour their own outputs (Panickssery et al. 2024). As MT-Bench judges, GPT-4 gave its own answers about a 10% higher win rate and Claude-v1 about 25% (Zheng et al. 2023) [S]. In LLM-generated translation benchmarks each model ranked itself first; the bias came from both the generated data and the LLM judge, and was largest when one model did both [S]. In retrieval the effect on rankings was small [S]. No study measures it for planted errors in research code | Unknown for DeepEcon; it could favour or disfavour the drafting family | Record the drafting model for each item. Where practical, draft with a family outside the evaluated set, or with several families. Report scores by drafting family |
| **Adversarial-filtering bias** | Phang et al. (2022): filtering against a chosen model makes rankings unstable and over-samples contested labels [S]. HLE's construction makes low scores for the filter models partly a product of its design [S]. TBS warns against the practice [P-full] | Large for comparisons across model families | Never keep or drop candidates by whether frontier models catch them (consistent with P-034) |
| **Unrealistic, easier, or not-actually-wrong errors** | Difficulty depends on how errors are generated. SWE-smith's planted bugs are rated easier than real tasks, but its LLM rewrites are rated harder [P-page]. BugPilot: bugs an agent was told to plant were "out-of-distribution" and "far less useful for training" than bugs an agent introduced by accident while adding a feature. Both kinds are LLM-generated, and an LLM (o3) judged their similarity to real bugs [P-page, authors' blog]. LLM mutants resemble real faults more than rule-based mutants do, but are more often equivalent, that is, not wrong [S]. Some of BLADE's LLM negatives are implausible [P-page] | Unknown: no source reports how many LLM-planted errors experts reject. Nearby figures measure other things. Experts rejected about 17% (53 of 316) of an LLM detector's flags on real errors (To Err Is Human), and Black Spatula reports about 10% wrong flags [S]. About 5% of GPT-5-inserted FLAWS errors survived an automated filter [S] | Expert review for realism and consequence. A "not actually an error" verdict in review. Where an item is executable, confirm its effect by running it. Prefer generation procedures that resemble how errors arise in practice over prompts to "insert a subtle bug" |
| **Style artifacts** | In one study, choices-only prompting was most accurate on HellaSwag, the only dataset whose distractors were model-written [S]. TBS's procedural injector left shortcut artifacts that review found [P-full, R1] | Untested for code edits in hand-written Stata or R *(assessment)* | People edit accepted changes to the author's style; artifact probes before release (P-052) |
| **Expert review is necessary but not sufficient** | HLE had high defect rates (in statements, answer keys, or rationales) despite expert review: about 29% of a text-only biology and chemistry subset by FutureHouse's estimate, about 18% by the HLE team's own follow-up [S]. FrontierMath reportedly corrected many problems after release, but secondary sources conflict on the numbers [S]. The later audits that found these problems were often LLM-assisted. Reviewers anchor on suggestions (R7) | — | Keep the contributor's "propose an addition" path prominent. Use LLMs as reviewers too, in an advisory role only. Reviewers work without hosted AI assistants |

## 5. Provider data-use defaults (dated 2026-11-06; re-check before relying on them)

| Provider | API or business use | Consumer chat use | Label |
|---|---|---|---|
| Anthropic | Commercial terms: "Anthropic may not train models on Customer Content from Services" | Consumer plans may be trained on unless the user opts out; feedback and safety-flagged content are exceptions | [P-page], R3 §6 |
| OpenAI | API and ChatGPT Business, Enterprise and Edu are not used to improve models by default | Personal ChatGPT plans are trained on by default unless "Improve the model for everyone" is turned off | [S] |
| Google | Gemini API paid services are not used to improve products (from a forum quote of an older version of the terms; not verified as current). The unpaid tier may be read by reviewers and used | Gemini Apps activity is used for training, on by default for adults | [S] |
| DeepSeek | The Open Platform terms let customers use outputs freely; whether DeepSeek trains on API traffic is **unresolved** | The consumer app may use inputs to improve services, with an opt-out | [S] / [U] |

## 6. Implications for DeepEcon

*(assessment; summarized as proposal P-054)*

*2026-11-07: superseded by the research lead's framework reset. No models are deployed; all are used through APIs (D-038). The tier rules below (items 2 and 6, and §1 item 3) are replaced by D-039 and D-040: AI may help everyone, exposure is logged, and affected scores are reported separately. Items 1, 3, 4, and 5 carry over into D-039; item 7 remains advice to the team, not a rule.*

1. **No prohibition is needed.** LLMs may help draft, vary, refine, and check candidate items, provided experts validate every item. Each executable change is confirmed by running it, by the contributor through the run kit where the data are restricted (P-049).
2. **Where the model runs is the leakage question**, and it follows the tiers already decided (D-018, D-032). Each task's tier is set before any drafting.
   - **Questions about public material only** (understanding the published paper and its public package, with no candidate errors in the prompt or the answer) expose nothing new. The LLM use policy (Proposed) allows any tool for public material, but D-018's text covers "paper materials", so the research lead should confirm.
   - **Development tasks:** a local model, or an external API that the research lead explicitly configures under written, dated no-training terms. The DeepSeek API's training terms are unresolved (§5), so it does not qualify until they are checked.
   - **Evaluation and held-out tasks:** a local model only. A hosted model would receive answer-key material, and under D-032 and its pending clarification (b) the task would then be exposed and become a development task. Keeping such a task in the evaluation tier would need the lead to amend D-032. ARC's semi-private set is not a direct precedent: it exposes test inputs during evaluation, not answer keys during construction.
   - **Whatever the tier:** restricted data go to no model, and contributors' unpublished materials and responses go only to a local model (LLM use policy §3; P-035).
3. **Provenance per item is the main validity safeguard.** Record whether each candidate came from the team, an LLM (which model, and whether it ran locally or externally), or the contributor, and who edited and validated it. Convention 4 and the team's plan ("origin (expert / AI / team)") already require this. Report results by origin and by drafting family; no published benchmark has done so for planted research errors.
4. **People write or finally edit agent-facing text and code edits**, as in the Terminal-Bench family. This also reduces style artifacts.
5. **Never filter candidates by whether frontier models miss them.**
6. **Contributors review candidates without hosted AI assistants**, and the Guidance pages say so.
   - Pasting candidates into a hosted assistant exposes answer-key material (LLM use policy §3).
   - AI help would also weaken the independence of the expert check.
7. **Prefer generation procedures that resemble how errors arise in practice.** Examples: a model or team member re-implementing a step under realistic instructions; the authors' recalled mistakes; real errata and replication reports. Avoid prompts to "insert a subtle bug".

## 7. Corrections to earlier notes

- **R1 §5** (2026-11-05), "Trial analysis" row: TBS's `analyze` judge moved from Codex with GPT-6 Astra to Claude Code with Claude Opus 5.5 on 2026-11-05 [P-page, `.github/llm-config.yml` comments]. R1 also missed the rubric line on hand-written tests (§2 above).

## 8. Gaps

- The papers for HLE, Terminal-Bench 2.0, MMLU-Pro, BigCodeBench, PaperBench, and FLAWS were not read (arXiv is blocked), so their construction details are [S].
- No study found measures generator-family bias for planted errors in code or empirical research. None compares how hard LLM-planted and human-designed errors are to detect on the same paper.
- No source reports expert acceptance or rejection rates for LLM-planted errors.
- No current, primary OpenAI, Google, or DeepSeek terms were read; the §5 entries other than Anthropic's are [S].
