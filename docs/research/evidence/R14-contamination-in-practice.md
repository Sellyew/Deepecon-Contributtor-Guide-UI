# R14: How much does task exposure matter in practice?

| Field | Value |
|---|---|
| Topic | Measured effects of training contamination on benchmark scores; what labs and benchmark builders do about public tasks; providers' API data terms; what this means for DeepEcon compared with Terminal-Bench-Science |
| Date | 2026-11-08. All sources accessed 2026-11-07 or 2026-11-08. |
| Author | lead collaborator (Claude session), answering the research lead's question of 2026-11-08: "Why are we so concerned about exposing tasks to model developers? … What exactly makes DeepEcon different from Terminal-Bench-Science in this respect?" |
| Method | Done by AI agents, not human researchers. Two Claude agents run from this session searched the literature and read public repositories and official pages; two more re-checked every claim (58 checks: 25 confirmed, 22 corrected, 11 left [S] or [U], none wrong). Corrections are applied below. A second agent of the same model family is not an independent human check |
| Evidence labels | As in the [evidence README](README.md). arxiv.org and most venue hosts were unreachable, so paper-level findings are mostly [S]; repository files and official pages read directly are [P-page] or [P-full] |
| Relation to other notes | Extends [R10](R10-contamination-and-evaluation-isolation.md), [R11](R11-llm-assistance-in-benchmark-construction.md) §4–5, [R12](R12-human-access-to-unreleased-answers.md), and [R13](R13-release-and-evaluation-practice.md) |

---

## 1. Short answer

*(assessment)*

1. **Incidental exposure usually has a small or unmeasurable effect on frontier models' scores on static question benchmarks.** GSM1k found "little to no signs of overfitting" for GPT, Claude, and Gemini, against drops of up to 8% (final version) for Mistral and Phi [S]. ARC's o3-preview scored 4 to 7 points higher on the public than the semi-private set, confounded with an easier public set [S]. In a TruthfulQA retro-holdout, frontier models' point estimates were +6 to +11 points but individually non-significant [P-page]. Early pre-training exposure tends to be forgotten (Bordt et al., ICML 2025) [P-page / S].
2. **Training on test material raises scores a lot.** One epoch of continued pre-training on HumanEval's test split took Gemini 1.0 Ultra from 74.4% to 89.0% (Gemini 1.5 report) [P-full]. Fine-tuning 13B models on paraphrased test sets reached GPT-4's level, and n-gram decontamination did not detect it (LMSYS) [P-page]. DeepSeek's 33B instruct model fell from about 53 to about 18 on LiveCodeBench problems released after its release, while GPT-4 showed no such break [P-page, read from the figure].
3. **Public agentic benchmarks built from public code became memorized by frontier models.** From the issue text alone, models named the files to change far more often on SWE-bench Verified than on fresh repositories (76% against 53%, "The SWE-Bench Illusion"; about 65% against 12 to 19% for Claude 3.5 and 3.7 Sonnet in another study) [S]. OpenAI stopped reporting SWE-bench Verified on 2026-02-23, citing flawed tests and models reproducing gold patches, and recommends SWE-bench Pro [S]. Anthropic screens SWE-bench problems for memorization and reports its ranking unchanged without them [P-page].
4. **Canaries and n-gram filters are leaky.** Parts of BIG-bench, which carries a canary, reached GPT-4's training data [S]; Gemini reports call n-gram decontamination "imperfect" [P-full]; TBS, HLE, and LAB-Bench reuse BIG-bench's canary GUID [P-page].
5. **Evaluation through official APIs is the weakest exposure channel.** Anthropic's commercial terms forbid training on API customer content [P-page]; OpenAI's API and Google's paid Gemini API are not used for training by default [S]; Alibaba's Model Studio FAQ says it never trains on customer data [S]; DeepSeek's API terms are unresolved [S]. Publication is a far wider channel: every crawler, mirror, and training corpus.
6. **Public benchmarks stay useful for a while, then lose credibility as they become prominent.** Terminal-Bench is "used by virtually all frontier labs" [P-page], and Anthropic reports TBS 0.1 [P-page]. SWE-bench Verified was released in August 2024 and dropped by OpenAI about 18 months later [S]. Terminal-Bench 2.0's authors list public distribution as a leakage risk and private splits as "under consideration" [S].

## 2. Why Terminal-Bench-Science can be public

- **Its tasks are meant to be hard to do, not hard to know.** Terminal-Bench's guidelines say "Obscure factual knowledge generally does not make tasks hard", because "it is likely that modern LLMs already know this fact" [P-page, `harbor-framework/terminal-bench-3@cfc7b6c` docs/task-guidelines.md line 41]. Many TBS tasks are verified on hidden simulated instances (R1).
- **It accepts the cost.** Its answers are public, its agents have open internet, and agents have fetched answers from its own pull requests (R12). It does not claim to measure new models free of contamination.

## 3. What makes DeepEcon different

*(assessment)*

| Factor | Terminal-Bench-Science | DeepEcon |
|---|---|---|
| What a published answer gives away | A long procedure that still has to be executed; hidden instances in many tasks | For **error-detection and correction** tasks, a short fact about a known public package (location, category, fix): exactly the kind of knowledge Terminal-Bench excludes as a source of difficulty. **Research-execution** tasks on hidden variants are closer to TBS |
| Public originals | Tasks are new artefacts | Correct replication packages are usually public, as SWE-bench's fixes are public commits; recall of the original can reveal a planted change (R1) |
| Set size | 70 tasks in v0.1 | Few papers at first; each memorized task moves the score more |
| Purpose | Broad capability signal | D-046: "a credible benchmark for comparing frontier models", including newly released ones |

## 4. Gaps

- No measurement of contamination effects on Terminal-Bench, TBS, or any economics or replication benchmark was found.
- Most paper-level effect sizes are [S]; the GSM1k figures differ between versions (up to 13% in arXiv v1, up to 8% at NeurIPS).
- Provider terms other than Anthropic's could not be read at the source and must be re-checked before relying on them.
