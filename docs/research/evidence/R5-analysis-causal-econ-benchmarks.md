# R5: Benchmarks of data analysis, causal inference, statistical reasoning and economics reasoning, and the many-analysts evidence on legitimate dispersion

| Field | Value |
|---|---|
| Topic | (1) Benchmarks that grade LLMs or agents on data analysis, statistical reasoning, causal inference and economics reasoning, with a close study of how BLADE builds and grades sets of acceptable analysis decisions. (2) The many-analysts and multiverse literature, read for quantitative evidence on how far competent analysts' estimates legitimately disagree. (3) What this implies for how DeepEcon credits alternative valid implementations, and where DeepEcon would differ from existing causal and econometric benchmarks. |
| Date | 2026-11-05. All URLs were accessed on 2026-11-05. |
| Author | research agent |
| Scope | The benchmarks named in the assignment (BLADE, DiscoveryBench, QRData, DSBench, DA-Code, InfiAgent-DABench, StatQA, CLadder, CaLM, Corr2Cause); deeper checks of five pointers from R4 (CausalReasoningBenchmark, CauSciBench, CausalVerify, NBER WP 35588, MetricsAI); economics-specific reasoning benchmarks (EconLogicQA, EconNLI, STEER, EconEvals, EconWebArena, BenCSSmark), plus other 2025–2026 economics or causal benchmarks found while searching; many-analysts studies (Silberzahn et al. 2018; NARPS 2020; Breznau et al. 2022; Huntington-Klein et al. 2021 and 2025; Menkveld et al. 2024; Multi100) and the specification-curve and multiverse methods. |
| Evidence labels | **[P-full]** primary source, full text read. **[P-page]** primary source: abstract, landing page, README, repository file or released data read by me. **[S]** secondary source (a search-engine summary of a page I did not open, a blog, an aggregator). **[U]** unverified: my background knowledge, not checked in this session. |
| Evidence limits | **No paper in this note was read in full.** Every [P-page] claim comes from a GitHub repository, read through raw.githubusercontent.com or a shallow `git clone`. Where I give counts "by my count", I computed them with my own read-only scripts (run with `python3 -I`) from released benchmark files. I executed no code from any downloaded repository. The web-search budget ran out part-way through (see "Access problems"), so several many-analysts numbers remain [U]. |
| Relation to other notes | This note extends R4 (`docs/research/evidence/R4-replication-benchmarks.md`) and does not repeat it. R4 §2.5–§2.7 and §5 gave one-line, mostly [S] pointers to CausalReasoningBenchmark, CauSciBench, CausalVerify, BLADE, DiscoveryBench, NBER WP 35588, MetricsAI and to studies of AI analysts' analytic flexibility. Here those pointers are verified against repositories where possible and corrected where needed. The benchmark-quality yardstick is the project's reading notes on Bercovich (2026), *Good Benchmarks* (`docs/research/reading-notes/good-benchmarks-bercovich-2026.md`). |

## Summary (10 bullets max)

1. **BLADE is the closest precedent for a set of acceptable answers, but it grades analysis decisions, not estimates.** In the released repository, 12 datasets carry expert annotations: 502 ground-truth decision specifications (120 conceptual variables, 176 data transforms, 206 statistical models) by my count, while the paper reports 536 [S]. Peers reviewed 541 alternative transforms and judged 154 of them not suited to the variable they were meant to build. Of the 145 multiple-choice items that ask which option is unjustifiable, 101 have an LLM-generated option as the correct answer. Transforms are matched by running them on the data and comparing the resulting column values; models and variables are matched by an LLM judge. No point estimate or standard error is graded [P-page].
2. **General data-analysis benchmarks deal with legitimate analytic flexibility mostly by fixing the method in the instructions or by using an LLM judge; none encodes identification or inference choices.** InfiAgent-DABench puts "constraints" in each question and grades by exact match. QRData accepts numbers within ±3%. DiscoveryBench uses an LLM to compare the agent's hypothesis with the gold one. DSBench uses an LLM to check answers [P-page]. Economics is a small share: 16 of DiscoveryBench's 264 real tasks are labelled economics, and 4 of BLADE's 12 annotated datasets come from economics studies [P-page, my count].
3. **Applied causal-inference benchmarks already cover method recognition, design specification and estimate recovery on real, largely social-science and economics papers.** CauSciBench has 175 real queries from 96 papers: 59 OLS, 43 IV, 32 DiD, 24 RDD and others. It counts an effect as correct within 5% of the reference, and it stores standard errors without grading them [P-page, my count and code reading]. CausalReasoningBenchmark scores the identification specification separately from the estimate and its standard error; its abstracts report 79%/34% in one version and 84%/30% in another [S].
4. **CausalVerify (Sept 2026) is the most rigorous precedent, and R4's description of it is confirmed.** The agent commits to a design, which is hashed before any data are revealed. An "oracle arm" substitutes the gold design. 66 of 426 workflows that ran without error (15.5%) failed verification. Using the gold design raised joint point-and-SE recovery from 15.0% to 51.5%, yet 48.5% still failed. The result depends on tolerance (27.2% at a 10% band, 14.1% at 100%), and the scorer was revised three times as it was developed (56.1% → 33.1% → 15.5%). Its gold design records list "admissible implementations" and keep "paper-faithful" inference separate from "modernized" inference [P-page]. Gold designs and synthetic twins were built by Claude-family agents, which the authors flag as a threat to validity [P-page].
5. **Formal causal-reasoning and economics-reasoning benchmarks test something else.** They pose questions on synthetic scenarios or text, not empirical implementation on real research data. This covers CLadder, Corr2Cause, CaLM and CausalDS, and EconLogicQA, EconNLI, STEER/STEER-ME, EconEvals, EconWebArena, BenCSSmark and EconCausal. Their overlap with DeepEcon is low [P-page/S].
6. **When only the question and the data are given, competent analysts disagree even on sign and significance.**
   - In the Crowdsourced Replication Initiative (Breznau et al.) released data, 1,252 models have confidence intervals. By my count, 64.4% are not significant, 19.5% are significantly negative and 16.1% significantly positive [P-page].
   - The README states that all coded research steps together explain at most 2.6% of effect-size variance [P-page].
   - Huntington-Klein et al. (2021) report that the standard deviation of estimates across replicators was roughly 3–4 times the mean reported standard error [S].
7. **Specifying more of the design shrinks dispersion, but not to zero, and peer acceptability is permissive.** In the 146-team "Many Economists" study, the stage that gave teams common cleaned data reached an IQR of 2.4 percentage points, and the authors argue "the optimal level of researcher variation is not zero" [S]. In Multi100 peer evaluations, only 1.6% of first-task pipelines were rated "unacceptable" (8 of 489) [P-page, my count]. Peer judgement therefore yields a very wide acceptable set and cannot serve as an answer key by itself.
8. **AI agents appear to vary less than humans.** A 2026 Federal Reserve Board paper finds that human economists' estimates were spread 2–27 times more widely than repeated Claude Code runs, with similar central estimates [S]. Tolerances calibrated only on agent runs would therefore reject legitimate human-style alternatives.
9. **Implication (assessment):**
   - Grade numbers only after the estimand and the decisions that matter are fixed.
   - Represent the remaining alternatives as a declared, expert-validated decision space with each option marked accepted, unjustifiable or contested.
   - Compare each declared option with its own reference value.
   - Use tolerance bands in standard-error units, checked against two conditions: every known valid result falls inside the band, and every known flawed result falls outside it.
10. **Novelty (conservative).** Causal-design recognition and specification, estimate recovery, SE checks on synthetic twins and set-valued analysis decisions all exist already. I found none of the following:
    - expert-designed flawed versions of real economics replication packages used both as negative controls for verifiers and as executable error-detection and error-correction tasks;
    - errors in inference choices (for example, the clustering level) graded by execution inside real packages;
    - decision spaces, including rejected alternatives, elicited from the papers' original authors.

---

## 1. Method

- **Prior notes read first:** the research lead's brief (§2–§4), the Bercovich reading notes, and R4 (§2.5–§2.7 and §5 in full, plus the sections needed to avoid duplication).
- **Web searches.** I ran about 35 WebSearch queries (standard and extended) before the shared per-turn search budget was exhausted. They covered every named benchmark and many-analysts study, plus broader queries for 2025–2026 economics and causal benchmarks ("LLM agents empirical economics econometrics", "Can large language models … empirical economics", NBER/SSRN). Search summaries are labelled [S].
- **Repository reads.** All were made on 2026-11-05. I read files and executed nothing from these repositories.
  - Raw READMEs and individual files: QRData (`benchmark/QRData.json`, `benchmark/eval.py`), DSBench, DA-Code, InfiAgent (including `examples/DA-Agent/README.md` and `data/da-dev-questions.jsonl`), StatQA, CLadder, CaLM, Corr2Cause, CauSciBench, CausalVerify (two repositories), EconNLI, STEER, STRIDES (InterveneBench), CRI (Breznau et al.; README, `data/cri.csv`, `code/01_CRI_Descriptives.Rmd`), specr, multiverse.
  - Shallow clones, each into its own empty directory (partial clones with a blob size filter where the data were large):

    | Repository | Commit | Date |
    |---|---|---|
    | `behavioral-data/BLADE` | 6118fa8 | 2024-10-25 |
    | `allenai/discoverybench` | c31fcf0 | 2025-06-08 |
    | `causalNLP/CauSciBench` | d9bb43a | 2026-07-05 |
    | `causalverify/causalverify` | 60b6015 | 2026-10-22 |
    | `poldrack/narps` | 0a9d71a | 2020-03-12 |
    | `NickCH-K/ManyEconomists` | 7b8590b | 2022-07-14 |

  - Earlier clone reused: R4's clone of `CenterForOpenScience/llm-benchmarking` (commit fb6a804), for its Multi100 peer-evaluation file.
- **My scripts** (scratchpad `r5/scripts/`): `blade_stats.py`, `discoverybench_stats.py` and `cri_stats.py`, plus inline `python3 -I` one-liners.

---

## 2. Data-analysis and statistical-reasoning benchmarks

### 2.1 BLADE (Gu et al., 2024): close study

**Identity.**
- "BLADE: Benchmarking Language Model Agents for Data-Driven Science", by Ken Gu, Ruoxi Shang, … Mike A. Merrill, Jeffrey Heer and Tim Althoff (University of Washington). arXiv:2408.09667 [P-page, README citation]. Findings of EMNLP 2024 [S].
- Code is under Apache 2.0 and data under ODC-By 1.0 [P-page].
- The README still says "We are working on a hold-out test set. Details soon!" [P-page].

**Capability measured.** Writing "justifiable analyses" of open research questions from data. Agents must "iteratively integrate scientific domain knowledge, statistical expertise, and data understanding to make nuanced analytical decisions" [P-page]. An agent submits three things: conceptual variables (independent, dependent, controls and moderators), a data-transform function, and a statistical-model function [P-page]. A second task asks multiple-choice questions on whether a decision is justifiable [P-page].

**Construction: where the questions and data come from.**
- The README says the research questions and datasets come from "existing research papers, crowd-sourced analysis studies and statistic textbooks", with "analyses from expert annotators" [P-page].
- The repository holds 14 dataset folders (plus a toy one). Twelve carry annotations [P-page, my count]: soccer, hurricane, teachingratings, mortgage, affairs, caschools, reading, panda_nuts, fish, crofoot, boxes and amtl.
- `fertility` and `conversation` have data and research questions but no annotations at this commit [P-page].
- Sources quoted in the dataset descriptions [P-page]:
  - soccer: the Silberzahn et al. red-card question, linked to DOI 10.1177/2515245917747646;
  - hurricane: "from the Simonsohn et al.'s Specification curve analysis paper";
  - teachingratings: Hamermesh and Parker (2005), *Economics of Education Review*;
  - mortgage: the Boston Fed study of mortgage lending (Munnell et al. 1996);
  - affairs: Fair (1978);
  - caschools: all 420 K-6 and K-8 California school districts, 1998–1999.
- Teachingratings, mortgage, affairs and caschools are economics studies or economics-teaching data (my classification).

**Construction: how the decision space was built.** This is my reading of the annotation files, where the paper's own description was not accessible.
1. *Independent expert analyses.* Each annotated dataset has an `annotations.csv`. It holds a dependency graph rooted at `ROOT_SPEC_ID` and one JSON specification per decision [P-page]:
   - Transform specifications carry `specification`, `code`, `rationale`, `trans_verb` (for example "derive"), input-to-output column mappings, and `branches` with dependencies and conditions. This is a multiverse-style tree of data-processing paths.
   - Conceptual-variable specifications carry `variable_type`, `concept`, the columns they derive from, and a rationale.
   - Model specifications carry a model name and specification.
   - Timestamps fall in June 2024. Annotator identities are blank (`annotator: null`) [P-page].
2. *Size of the decision space, by my count* [P-page]:
   - Conceptual variables: 120 in total, from 4 (hurricane) to 18 (reading, teachingratings) per dataset.
   - Transforms: 176 in total, from 5 (caschools) to 39 (soccer).
   - Model specifications: 206 in total, from 4 (amtl) to 73 (panda_nuts) and 41 (soccer).
   - The total is 502 decision specifications. The paper reports "536 ground truth analysis decisions" [S]. I could not reconcile the two counts; the difference may be in how decisions are counted or what is released.
3. *Peer validation of alternatives.* The search summary of the paper says analysts were asked "to validate alternative decisions from their peers and LM-generated decisions seeded by analysts' own decisions" [S]. The released files contain the review records [P-page; counts are mine]:
   - **541** reviewed transform alternatives (`annotate_transform_spec_json`). "Is suited to the conceptual variable?": Yes 356, **No 154**, Unsure 31. "Is the rationale reasonable?": Yes 336, No 143, Unsure 61, missing 1. "Are the steps reasonable?": Yes 402, No 7, Unsure 25, missing 107.
   - **82** reviewed conceptual-variable alternatives (`annotate_cvar_spec_json`). "Is reasonable?": Yes 50, No 5, Unsure 10, missing 17. "Can be derived from the data?": Yes 60, No 18, Unsure 4.
   - Reviewers wrote free-text explanations. One example: "While this is reasonable to include this in the model, I do not agree this is the IV … This could serve as control though."
4. *Negative ("unjustifiable") examples and multiple-choice questions.* `mcq_dataset.json` holds **188** questions, matching the paper's "188 multiple choice" [S] [P-page, my count]:
   - 20 ask for the unjustifiable conceptual variable;
   - 125 ask for the unjustifiable transform;
   - 43 ask for the justifiable transform.
   - Each option carries an `is_llm_generated` flag. In the questions that ask for the unjustifiable option, the correct answer is LLM-generated in **18 of 20** variable questions and **83 of 125** transform questions; in "select the justifiable" questions it is LLM-generated in 16 of 43 [P-page].
   - An example of an LLM-generated unjustifiable control in caschools is "School's reputation", which is not a column in the data [P-page].

**Verification (code read; `blade_bench/eval/`)** [P-page].
- *Transforms.* The agent's transform code is executed. The resulting column values are hashed ("value" match), and the data-flow graph is hashed ("graph" match). Hashes are intersected with those of the ground-truth transforms, and categorical columns have their own value hash. **This is outcome-based matching of intermediate data artefacts, not an LLM judgement.**
- *Statistical models.* An LLM judge returns all matching pairs. Its instruction reads: "two models are the same if give[n] the same data, the model specification would lead to the same results … 'logistic regression' is equivalent to a 'binomial GLM with a logit link' … not equivalent to 'linear regression'."
- *Conceptual variables.* An LLM judge rates similarity on a 5–10 scale, and a match counts when similarity is **≥ 8** ("Very Strongly Related" or closer).
- *Scores.*
  - Coverage@k: the share of ground-truth decisions matched across k runs (default 10).
  - Hit rate: the share of the agent's decisions that match some ground-truth decision.
  - Per-dimension F1 is the harmonic mean of these two, and the overall score weights each dimension by its number of decisions.
  - A diversity metric is also available.
- *Code observation.* At this commit the *unweighted* score is computed as `(f1_cvars + f1_models + f1_models_cvars + 0.5 * f1_gspecs + 0.5 + f1_vspecs) / 4`. That adds a constant 0.5 where `0.5 * f1_vspecs` was presumably intended (my reading of `final_metrics.py`, lines 135–137). The weighted score is unaffected. I do not know which score the paper reports.

**Results** [S]. "Most LMs are decent at discerning decisions and generating non-empty executable analyses, but their analyses are basic and lack diversity" (v1). Agents that interact with the data show "improved, but still non-optimal, diversity" in their decisions. I could not read per-model numbers.

**Limitations (my assessment from the files).**
- No point estimate, standard error, confidence interval or significance conclusion is graded. Two analyses that match on decisions can still differ in their numbers, and the reverse can also happen.
- Inference choices (standard-error type, clustering, few-cluster corrections) are not a decision category.
- Most negatives are LLM-generated single decisions, some of which are implausible. They are not realistic expert-designed mistakes.
- Matching models and variables depends on an LLM judge, and the judge's agreement with humans is not documented in the repository.
- There are only 12 datasets, mostly outside economics, and they are older public data that are likely to appear in training corpora.

**What DeepEcon can borrow (assessment).**
- The decision-tree data model, with branches, rationales, reviewer judgements and an `is_llm_generated` provenance flag. It fits directly onto the brief's fields "Alternative valid solutions" and "Evidence that the error is genuinely incorrect, rather than an alternative valid approach" (§3.3 item 10, §5.4).
- Matching intermediate artefacts by execution: hashing the estimation sample, constructed variables or the treatment-timing variable is outcome-based and needs no LLM.
- Scoring both precision and recall, so that an agent cannot gain credit by enumerating every option.

### 2.2 DiscoveryBench (Majumder et al., 2024; ICLR 2025)

- **Identity.** "DiscoveryBench: Towards Data-Driven Discovery with Large Language Models", Allen AI. arXiv:2407.01725. ICLR 2025 [S; proceedings PDF listed at proceedings.iclr.cc]. Repository: https://github.com/allenai/discoverybench; datasets are ODC-BY [P-page].
- **Capability.** Each task is a goal plus one or more datasets, and solving it "requires both statistical analysis and semantic reasoning" [P-page].
- **Construction.**
  - The real split has **264 queries** in 158 metadata files: 239 test and 25 train, by my count [P-page].
  - Queries by domain label [P-page, my count]: meta science 100, sociology 69, humanities 38, biology 26, **economics 16** and engineering 15.
  - The economics tasks come from World Bank education and GDP data (12) and from an "immigration_offshoring_effect_on_employment" folder that uses an offshoring instrumental-variable file (4, train split).
  - The sociology tasks use National Longitudinal Survey (NLS) extracts on socioeconomic status, incarceration and BMI.
  - Workflow tags include data selection (139 queries), standardization (115), feature engineering (112), data cleaning (104), integration (104), meta-regression (100) and regression (65) [P-page].
  - There are also 903 synthetic tasks [S].
- **Verification.** `eval/eval.py` uses an LLM (configured as GPT-family models) [P-page]:
  - It decomposes the gold and predicted hypotheses into sub-hypotheses, each with a context, variables and relations.
  - The score is context match × variable F1 × relation score. The relation score is 1.0 for a match and 0.5 for a partial match, on a specificity hierarchy such as "there exists a relationship" > "positive" > "positive AND linear".
- **Results.** The best system scores about 25% [S].
- **Relevance.**
  - The grading is entirely LLM-judged on natural-language conclusions.
  - Gold hypotheses sometimes include coefficients. One is "Per unit increased ease of immigration reduces 0.1059 unit of the share of offshore employment" [P-page], so answers bind to one specification without any declared tolerance or alternatives.

### 2.3 QRData (Liu et al., 2024; Findings of ACL 2024)

- **Identity.** "Are LLMs Capable of Data-based Statistical and Causal Reasoning? Benchmarking Advanced Quantitative Reasoning with Data", Findings of ACL 2024, pp. 9215–9235 [P-page, README BibTeX].
- **Construction, by my count from `benchmark/QRData.json`** [P-page]:
  - 411 questions: 248 multiple choice and 163 numerical.
  - Keyword tags: "Causality" 269, "Statistics" 142, "Difference in differences" only 4.
  - Sources:
    - three causal-discovery datasets (neuropathic pain 100, Arctic sea ice 50, flow cytometry 50);
    - IHDP (30) and "Jobs" (10) for treatment-effect estimation;
    - textbook exercises from *OpenIntro Statistics*, *Quantitative Social Science* and *Causal Inference for the Brave and True*.
- **Verification.** Numerical answers count as correct inside a **±3% relative band** (`error_scale = 0.03` in `eval.py`). Multiple-choice answers count when the prediction's prefix matches the answer [P-page].
- **Results** [S]:
  - GPT-4 reaches about 58% and the best open model (Deepseek-coder-instruct) about 37%.
  - "All models including GPT-4 and Gemini struggle with causal reasoning."
  - Models "acquire causal knowledge from the pretraining corpus, but can hardly integrate the knowledge with the provided data".
- **Relevance.** Most "causal" items test causal discovery, not econometric identification. The fixed ±3% band does not depend on sampling uncertainty.

### 2.4 DSBench, DA-Code, InfiAgent-DABench, StatQA (brief)

| Benchmark | What I verified | Secondary claims |
|---|---|---|
| **DSBench** (Jing et al.; ICLR 2025) | The README says data-analysis and modelling tasks were collected "from modeloff and kaggle". It says DSBench "is used for OpenAI's new ChatGPT agent evaluation" (news item dated 2025-07-17). Data-analysis answers are judged by a script that calls an OpenAI model (`compute_answer.py`). Data come from the ModelOff financial-modelling competitions via the Eloquens website. Use is non-commercial [P-page]. | 466 data-analysis and 74 data-modelling tasks. The best agent solves 34.12% of data-analysis tasks and reaches a 34.74% relative performance gap [S]. |
| **DA-Code** (Huang et al.; EMNLP 2024) | Runs in a Docker sandbox and is evaluated against gold files with a timeout. Only 100 examples are in the repository; the full set is on Google Drive [P-page]. | 500 tasks in data wrangling, machine learning and exploratory analysis. The best LLM reaches 30.5% [S]. |
| **InfiAgent-DABench** (Hu et al.; ICML 2024) | Each question comes with **"constraints … that narrow down the solution into a closed-form"** and an output format, and is scored by exact match. Because "most models hardly follow the format requirements", GPT-3.5 first reformats the answer. Only the validation set is public [P-page]. By my count the public dev file has **257 questions on 52 CSVs** (82 easy, 87 medium, 88 hard). A typical constraint reads: "Do not perform any further data cleaning or preprocessing steps before calculating the correlation" [P-page]. | The ICML version has 603 questions on 124 CSVs and covers 34 LLMs [S]. |
| **StatQA** (Zhu et al.; NeurIPS 2024 D&B) | 11,623 examples on choosing statistical methods and judging whether they apply, especially hypothesis tests. GPT-4o's best score is 64.83%, and fine-tuned open models beat in-context methods. "LLMs primarily make applicability errors, whereas humans mostly make statistical task confusion errors." The benchmark is built automatically with scripts that call GPT models [P-page]. | Contingency-table and variance tests are hardest; chain-of-thought gives small decreases or no effect [S]. |

**Pattern (assessment).** These benchmarks show two ways of avoiding analytic flexibility. InfiAgent-DABench tightens the instruction until only one answer is acceptable (Bercovich §4: "tightening is usually simpler"). DSBench and DiscoveryBench use an LLM judge. Neither approach suits DeepEcon's identification and inference tasks: tightening removes the choice DeepEcon wants to test, and LLM judges are unvalidated for economics arguments (R4 implication 8).

---

## 3. Formal causal-reasoning benchmarks (brief)

| Benchmark | What I verified | Secondary claims | Relevance to DeepEcon |
|---|---|---|---|
| **CLadder** (Jin et al.; NeurIPS 2023) | Yes/no questions "that generally require statistical and causal inference". Query types include ATE, marginal, correlation, ETT, NDE and NIE, tagged by rung of the ladder of causation. They are set in synthetic "self-contained, hypothetical world[s]", for example an instrumental-variable story about proximity to college [P-page]. | 10K questions with answers from "an oracle causal inference engine". It introduces the CausalCoT prompt. "Highly challenging" for LLMs [S]. | Low. The causal graph is given, and there are no data or implementation. |
| **Corr2Cause** (Jin et al.; ICLR 2024) | Data are generated by enumerating DAGs and checking d-separation (`data_gen.cpp`) [P-page]. | More than 200K samples and 17 LLMs, with near-random performance. Fine-tuned models fail out of distribution [S]. | Low. Pure inference from stated correlations. |
| **CaLM** (Chen et al.; 2024 technical report) | A four-module taxonomy: causal target, adaptation, metric and error. CaLM Lite has 9,200 items, "approximately one-tenth" of the full set [P-page]. | 126,334 samples, 28 models, 92 causal targets, 7 metrics and 12 error types; a 315-page report [S]. | Low to moderate. Its error taxonomy is a model for DeepEcon's failure-mode codes. |
| **CausalDS** (Leban, Saarinen, Sun; arXiv:2607.08093, July 2026) | Not read. | Freshly generated synthetic causal "scenes" with imperfect data. Abstention is scored directly: when the target is not identified, the correct answer is to decline. Separate axes cover correctness, uncertainty quantification, abstention and tool use. An aggregator reports 953 scenes [S, unconfirmed]. | Moderate. Scoring abstention is directly relevant to DeepEcon's "do not impose binary answers on underidentified questions" (brief §4). |

---

## 4. Applied causal-inference and econometrics benchmarks (deepening R4)

### 4.1 CausalVerify (Zhang, Correia, Parra, Xie; arXiv:2609.07944, v2 26 Sept 2026)

- **Identity.**
  - Repository: https://github.com/causalverify/causalverify (MIT code; data licensed per component).
  - The authors are at the Department of Finance, Universidad Autónoma de Madrid, and CSIC [P-page, `yonghongzhang-io/causalverify` README].
  - v1 was a "NeurIPS 2026 Datasets & Benchmarks submission (frozen)", and v2 matches the arXiv v2 paper [P-page].
  - The title changed between versions ("An Execution-Grounded Benchmark for LLM Causal Inference Workflows" → "End-to-End Verification of Causal Analyses by Language Models") [P-page/S].
- **Design** [P-page, README]. Four layers are reported "as a profile, not a ranking" and are never aggregated:
  - V1 method recognition;
  - V2 design specification;
  - V3 executable implementation;
  - V4 estimand recovery.

  The framework's claim is "V1 ⇏ V2 ⇏ V3 ⇏ V4".
- **Three arms** [P-page]:
  - **Executable arm.** 100 fixed-seed synthetic scenarios (30 DiD, 24 event study, 24 IV, 22 RDD). The model writes runnable R code in one call. **V4 passes if the extracted estimate is within 50% of the canonical estimate on the same realised data.** The authors say the model ranking is "identical at every tolerance from 10% to 100%".
  - **Real-paper arm.** 259 archived **economics** papers, with method names "blacklisted from the context". The model proposes an identification plan, scored against LLM-consensus labels. In a blinded 30-paper audit, agreement was κ = 0.61 for method and κ = 0.29 for effect direction.
  - **Paired bridge.** 23 paper–twin pairs, 20 seeds each, nine models.
    - Stage 1: the model commits to a structured Causal Design Representation (CDR), "hashed before any data".
    - Stage 2: it implements the design in Python on a synthetic twin that preserves the paper's identification structure.
    - Pass rule: **point estimate within 0.5 canonical SE, and SE ratio in [0.8, 1.25]**.
    - An **oracle arm** substitutes the gold CDR and its pinned conventions.
- **Reference values** [P-page]. The canonical estimate is computed "on the *realised* dataset — rather than the ideal DGP parameter, which would penalise models for finite-sample deviation". The coefficient-extraction judge agreed with blinded human annotation on 90.9% of 44 comparable cells.
- **Results** [P-page]:
  - 66 of 426 executing workflows (15.5%, 95% CI 12.1–19.2) fail verification. The failure share is 27.2% at a 10% tolerance and 14.1% at 100%.
  - Ranking models by execution agrees with ranking by recovery (Kendall τ = 0.81). Keyword-based scoring of the stated effect direction is uninformative (τ between −0.20 and 0.10).
  - In the paired study, 140 of 187 scored commitments (74.9%) pass the design layer.
  - The oracle raises joint point-and-SE recovery from **15.0% to 51.5%**, yet **48.5% of eligible seeds still fail** under the reference design.
  - A single repair round mostly fixes "mechanical" failures, not conceptual ones (32 of 41 repairs in a pilot).
- **Threats the authors disclose** [P-page]:
  - The gold CDRs, the twins and the design-layer adjudication "were produced by Claude-family agents under the authors' rulings". Without the two Claude models, the oracle contrast is 9.3% → 39.4%.
  - On the newest pairs, the whole oracle gain comes from Claude models, so the benchmark "cannot separate stronger models from models that share conventions with the agent family that built the references".
  - The executable-arm scorer changed three times after most outputs existed (executed-but-wrong share 56.1% → 33.1% → 15.5%).
- **Gold-design format** (from `experiments/v2_paired/gold_cdr/paper_14_gold_cdr_v1.json`, Card and Krueger 1994) [P-page]:
  - Fields: estimand, outcome definition, identifying variation, comparison group, sample definition, unit of analysis, time structure, fixed effects, controls, weights, `clustering`, `target_coefficient` and identification assumptions.
  - The target coefficient reads: "admissible implementations include the difference of group-time means and the saturated 2x2 regression".
  - Inference is recorded as `primary_inference: PAPER_FAITHFUL_UNCLUSTERED` with `modernized_inference: ROBUSTNESS_ONLY`.
  - Each field has a provenance record with an evidence anchor (page or table), a confidence level and an ambiguity note, for example "Table 5 robustness re-weights part-time at 0.4/0.6".
  - The schema is frozen and versioned (`cdr_schema_v1.0/1.2.json`).
- **Correction to R4.** R4's description is confirmed. One addition matters: the real-paper arm (259 economics papers) is graded only at the text level against LLM-consensus labels. Execution-grounded scoring applies only to synthetic scenarios and synthetic twins.

### 4.2 CauSciBench (Acharya et al.; ICML 2026)

- **Identity.**
  - Repository: https://github.com/causalNLP/CauSciBench; code MIT, with dataset-specific licences [P-page].
  - An ICML 2026 poster titled "CauSciBench: Can LLMs Automate Causal Inference in Real-World Scientific Research?" exists, alongside a same-named NeurIPS 2025 entry [S]. I did not resolve how the two relate.
- **Capability.** The full pipeline: parse the data description and query, identify treatment and outcome, choose the method and method-specific variables (instrument, running variable, time variable), implement, and interpret [P-page].
- **Construction, by my count from `data/metadata_csv/`** [P-page]:

  | Split | Queries | Sources | Methods |
  |---|---|---|---|
  | Real | 175 | 96 distinct papers; 66 queries flagged as randomized trials | OLS 59, IV 43, DiD 32, RDD 24, matching 11, GLM 6 |
  | Synthetic | 143 | generated data | IV 37, DiD 31, OLS 20, matching 20, RDD 20, front-door 15 |
  | QRData-CI | 39 | QRData | — |

  - The total is 357, matching `data/README.md`.
  - Real papers include classic economics designs (titles as listed in the metadata): Card and Krueger's minimum-wage study, the Maimonides-rule class-size paper, "Does Compulsory School Attendance Affect Schooling and Earnings?", "The China syndrome", college proximity and the return to schooling, LaLonde's evaluation of training programs, and the minimum legal drinking age. Many political-science field experiments are also included.
- **Verification** (`evaluation/metrics.py`) [P-page]:
  - method-selection accuracy and macro-F1;
  - **effect accuracy, counted correct within 5% relative error** (`thresh=5.0`);
  - treatment and outcome accuracy;
  - Jaccard-style overlap of control variables;
  - completion rate.

  The reference SE is stored for every real query, but I found no SE metric in `metrics.py` (my code reading).
- **Results** [S]. Seven frontier models were evaluated on 300+ queries. "Method selection" is the main bottleneck, and models do worse on real datasets. R4's [S] claim that models "default to correlational methods" remains unverified.
- **Relevance.**
  - This is the closest benchmark in data to DeepEcon's Path A: real published economics designs, with a reference estimate per query.
  - But each query is reduced to one CSV with one reference value, and a fixed 5% band. That band ignores the estimate's standard error and is either too tight or too loose depending on precision (my assessment).
  - Inference is not graded.

### 4.3 CausalReasoningBenchmark (Sawarni, Tan, Syrgkanis; arXiv:2602.20571)

- **Format** [S]. Each query asks for a structured **identification specification** (strategy, treatment, outcome, controls and design-specific elements) and a **point estimate with a standard error**. The two are scored separately "to separate reasoning errors from numerical errors".
- **Size and results** [S]. The abstracts disagree between versions:
  - one reports 173 queries, 132 datasets and 79 papers, with 79% for the high-level strategy and 34% for full-specification correctness;
  - another reports 173 queries, 138 datasets, and 85 papers plus 4 textbooks, with 84% and 30%.

  R4 called the 84%/30% figures third-party and unconfirmed. They appear in an abstract version [S], but are still not checked against a PDF.
- **Data** [S]. On Hugging Face (`syrgkanislab/CausalReasoningBenchmark`, tagged for causal inference and econometrics). I found no GitHub repository, and I could not inspect the dataset (Hugging Face was not attempted; it was unreachable in R4). How the standard error is scored and what tolerances apply are **unknown**.

### 4.4 InterveneBench (Shi et al.; arXiv:2603.15542, March 2026)

- **Benchmark** [S]. 744 peer-reviewed social-science policy studies. Models must reason about interventions and identification assumptions without given causal graphs. The authors also propose STRIDES, a multi-agent design–check–refine system.
- **Repository** [P-page]. It holds a test set and a "legacy" set, and calls itself "an anonymized repository for review only … treat the paper PDF as the authoritative reference".
- **Relevance.** Tests study design in text, not implementation.

### 4.5 NBER WP 35588: Galiani, López and Sosa, "AI Agents and Prompt Engineering in Econometric Coding" (2026)

- **New detail beyond R4** [S]:
  - The NBER abstract says moving "from the chatbot to the constrained agent raises task success from 74 to 96 percent, at about eight additional cents per run".
  - For Claude Sonnet 4.6 and GPT-5.4 run through Codex, "few-shot prompting improves the chatbot far more than the constrained agent, indicating that prompting and agency act as substitutes".
  - The IDEAS listing reports 40 tasks in Stata, R and Python, a rise from 79% to 97%, and agent runs costing 3.1–5.0 times as much.
  - The authors' VoxEU column says letting models run code "makes the prompt and the software matter far less".
- **Still unverified.** The PDF was not reachable. Task construction, whether results are matched exactly or within a tolerance, and the reason the two versions disagree remain unknown.
- **Relevance.** The method is specified in each task. The benchmark therefore measures implementing a named method, the layer that §2.4's pattern says is close to saturation for agents. Bercovich's "over-specification fairness check" (reading notes §7) would make it the *easy* version of a DeepEcon task.

### 4.6 MetricsAI: "Can AI Master Econometrics?" (arXiv:2506.00856, 2025)

- **New detail** [S]:
  - The agent is built on MetaGPT, with tools for OLS, PanelOLS, IV-2SLS, DiD, RDD and propensity scores.
  - Tasks come from published papers and PhD coursework.
  - The abstract reports: GPT-4o "under 50%" success on complex tasks; general-purpose agents about 30% "partial replication"; MetricsAI above 90% "directional replication".
  - R4's v2 figures (above 50% "perfect replication" on coursework and 27% on published-paper tasks) use a different metric.
- **Assessment.** "Directional", "partial" and "perfect" replication are different success criteria. These numbers should not be compared with other benchmarks without the definitions.

---

## 5. Economics-specific reasoning benchmarks and related 2025–2026 work

| Work | What it measures | Construction and verification | Status and evidence | Overlap with DeepEcon |
|---|---|---|---|---|
| **EconLogicQA** (Quan and Liu; Findings of EMNLP 2024) | Ordering interconnected economic events into a logical (not chronological) sequence | Multiple-choice questions generated by GPT-4 from business news, then human-reviewed | An aggregator lists GPT-4-Turbo at 0.57 and GPT-4 at 0.55 (unverified) [S] | Low |
| **EconNLI** (Guo and Yang, HKUST; Findings of ACL 2024, pp. 982–994) | Whether an economic premise event entails a hypothesis event; classification and generation | Dataset and construction notebooks are on GitHub [P-page] | Models are "far from perfect" [S] | Low |
| **STEER / STEER-ME** (Raman, Lundy, Amouyal, Levine, Leyton-Brown, Tennenholtz; ICML 2024 / NeurIPS 2025) | Economic rationality: strategic reasoning (STEER) and non-strategic microeconomic reasoning (STEER-ME) | Built on a taxonomy of economic "elements". "Dynamic" questions are generated from templates by autoSTEER, with fixed Hugging Face snapshots. Multiple-choice and free formats; accuracy plus calibration; built on Inspect [P-page] | 14 LLMs in the ICML paper [S]; 64 elements (secondary summary) [S] | Low. Its template generation is a useful pattern for fighting contamination. |
| **EconEvals** (Fish, Shephard, Li, Shorrer, Gonczarowski; arXiv:2503.18825) | Agents' decisions in unknown environments (procurement, scheduling, task allocation, pricing), plus "litmus tests" of tradeoffs with no right answer (efficiency vs equality, patience, collusiveness) | Synthetic, with scalable difficulty (Basic, Medium, Hard) [S] | The title may have changed in a later version [S] | Low, since agents are tested as economic actors. The litmus-test idea (measuring *tendencies* where no ground truth exists) is relevant to contested methodological questions. |
| **EconWebArena** (Liu and Quan; NeurIPS 2025) | Retrieving precise, time-sensitive economic data from 82 live authoritative websites | 360 tasks; LLM-generated candidates filtered by humans [S] | Large performance gaps [S] | Low. Depends on live web services (Bercovich's robustness criterion). |
| **BenCSSmark** (Chatelain, Ollion et al.; arXiv:2605.04886; LREC 2026, pp. 848–859) | A position paper with a benchmark of tasks from ongoing or published social-science projects, for example detecting gender- or class-related papers among abstracts | Part of the French "Pantagruel" LLM project [S] | A machine review (pith.science) says its claimed benefits are asserted without measurements [S] | Low (text-classification tasks for computational social science). It shares DeepEcon's motivation of bringing social-science tasks into LLM evaluation. |
| **EconCausal** (Lee, Yun, Cha, Park, Park, Kim; arXiv:2510.07231, v4) | Context-dependent signs of causal effects | 10,490 treatment–outcome–sign triplets from 2,595 NBER papers later published in top economics and finance journals [S] | One version: 88% in fixed contexts, a 32.6-point drop when the sign must be revised across contexts, and null effects recognized only 13.8% of the time (9.5% in v1). The label space omits magnitude and statistical strength [S] | Moderate on interpretation; no data or implementation |
| **EconBench** (Yan; SSRN 6803400, May 2026) | "Structural" economic reasoning beyond recall | 4,200 expert-curated items in five reasoning strata, with release promised [S] | — | Low. Name collision risk with any "EconBench"-style naming. |
| **Grundl (2026), "Claude Code as an Empirical Economist: Like Humans but Without the Tails"** (Federal Reserve Board; SSRN 6219138) | Claude Code (Opus 4.5) against human economists on the same causal-inference tasks with the same instructions | Uses the human results and instructions of the Many Economists study (§6) [S] | "Typical" estimates are similar; human spread is "roughly 2 to 27 times larger" than spread across Claude Code runs [S] | **High** for calibrating tolerances (§8) |
| Other, out of scope | HouseholdBench (NBER WP 35927; predicting household behaviour from 6 surveys and 32 tasks) [S]; NBER WP 35188 (agents building economic datasets from primary sources) [S]; "Wrong and More Confident" (arXiv:2607.23424; LLMs taking a graduate economics exam; title only) [S]; LiveMacroEval (EMNLP 2026; nowcasting) [S]; Ludwig, Mullainathan and Rambachan, "Large Language Models: An Applied Econometric Framework" (arXiv:2412.07031; argues a validation sample is needed to assess LLM output errors; a framework, not a benchmark) [S] | — | — | Low |

I also did **not find** a published benchmark that grades agents on difference-in-differences, IV or RDD implementation *inside full economics replication packages*. A search summary pointed to an "empirical_agent" project on an aggregator page that scores agents against econometric benchmarks in Docker, but I could not open or verify it [S/U].

---

## 6. Many-analysts and multiverse evidence

### 6.1 Quantitative summary

| Study | Setting | Analysts | What was fixed | Dispersion found | Evidence |
|---|---|---|---|---|---|
| Silberzahn et al. (2018), *Advances in Methods and Practices in Psychological Science* | Soccer red cards and players' skin tone | 29 teams, 61 analysts | Question and data | Odds ratios 0.89 to 2.93 (median 1.31). 20 teams (69%) found a significant positive effect and 9 (31%) did not | Numbers [U]. DOI 10.1177/2515245917747646 as linked in the BLADE README [P-page]; BLADE reuses the data [P-page] |
| Botvinik-Nezer et al. (2020), *Nature* (NARPS) | One fMRI dataset | 70 teams [U] | Nine ex-ante hypotheses [P-page] and data | Teams reported a binary decision and a confidence rating (1–10) for each hypothesis. The "fundamental value" for each hypothesis is "the actual fraction of teams reporting significant results". Three teams changed decisions after the project ended. Prediction markets matched the fundamental value only for hypothesis 7 [P-page, supplementary captions in the repository]. "No two teams chose identical workflows" [U] | Repository captions [P-page]; team count [U] |
| Breznau, Rinke, Wuttke et al. (2022), *PNAS* (Crowdsourced Replication Initiative) | Immigration and support for social policy (ISSP data) | 73 teams (README) | Hypothesis and data | "Taking all research steps as predictors explains at most 2.6% of total effect size variance, and 10% of the deviance in subjective conclusions." The codebook has 107 model-design steps (README) [P-page]. By my count from `data/cri.csv`, excluding the original study coded as team 0: 1,261 models from 72 team IDs, of which 1,253 have an AME. Of the 1,252 with a confidence interval, **64.4% are not significant, 19.5% significantly negative, 16.1% significantly positive**. Team conclusions: 38 reject, 8 support, 10 "not testable", 16 mixed. 37 of 72 teams had at least one significantly positive and one significantly negative model of their own (median 12 models per team, range 1–112) [P-page] | README and data [P-page]; PNAS DOI linked from the README; full paper not read |
| Huntington-Klein et al. (2021), *Economic Inquiry* 59(3): 944–960 | Two published applied-microeconomics studies, each replicated by 7 researchers who built the data themselves | 2 × 7 | Original question and raw data | "No two replicators reported the same sample size". Significance changed, and for one study the sign changed. **The SD of estimates was roughly 3–4 times the mean reported SE** | [S] |
| Huntington-Klein, Pörtner, McCarthy and the Many Economists Collaborative (2025), NBER WP 33729 (IZA DP 17744; I4R DP 209; listed as forthcoming in *JEL*) | Effect of DACA on full-time employment | 146 teams [S] | Three stages: an open task, then a fixed research design, then common cleaned data [S] | **Stage 3 (common cleaned data): IQR of 2.4 percentage points.** Teams varied widely in controls, weighting and functional form, "but not all of this variation drives the variation in effect sizes". "The optimal level of researcher variation is not zero" [S]. An author's post cites an IQR of 3.1 pp overall [S]. Stage 1 and stage 2 IQRs not obtained | [S] |
| Menkveld et al. (2024), *Journal of Finance*, "Nonstandard Errors" (#fincap) | Market-microstructure hypotheses on one futures dataset | 164 teams [U] | Six hypotheses and data [U] | Across-team "non-standard errors" are of the same order as standard errors; they decline after peer feedback; participants underestimate them [U] | [U]; not verified in this session |
| Multi100 peer evaluations (COS robustness module) | Re-analyses of claims from social- and behavioural-science papers | 273 analysts, 136 evaluators, 73 papers in this file | Claim and data | By my count over 489 evaluations: first-task pipeline rated high quality 57.3%, medium 31.7%, low 9.4%, **unacceptable 1.6%**. "Conclusion follows from results" 94.5%. Second task: unacceptable 3.7%, incomplete 4.3%. Of evaluators who executed the code, 19 found mismatches and 185 did not [P-page] | File `multi100_peer-eval-not-reviewed_processed_data.csv`, labelled "not-reviewed" [P-page]; the Multi100 paper itself was not read [U] |
| Grundl (2026) | The Many Economists tasks | Claude Code runs compared with the 146 human teams | Same instructions as the human teams | Human dispersion 2–27 times that of Claude Code runs; similar central tendency [S] | [S] |

AI analysts on many-analysts tasks are covered in R4 §2.7 and not repeated here:
- "Many AI Analysts, One Dataset" (Bertran et al.);
- "The Agentic Garden of Forking Paths";
- Alizadeh et al. (2606.11456), which ran 20 runs each of Claude Code and Codex on a many-analysts immigration dataset and found estimates close to the human consensus.

### 6.2 Specification curve and multiverse analysis (methods)

- **Citations** [S, as cited in the specr README]. Steegen, Tuerlinckx, Gelman and Vanpaemel (2016), "Increasing Transparency Through a Multiverse Analysis", *Perspectives on Psychological Science* 11(5): 702–712. Simonsohn, Simmons and Nelson (2020), "Specification curve analysis", *Nature Human Behaviour* 4: 1208–1214.
- **What the method does.** A multiverse or specification curve runs every combination of defensible processing and analysis choices and reports the whole distribution of results. specr implements the "three test statistics proposed by Simonsohn et al. (2020)" [S]. The multiverse R package says Steegen et al. "first put forth the concept" and Simonsohn et al. "a similar notion called the specification curve" [S].
- **Worked examples** [S]. The multiverse package demonstrates Steegen et al.'s re-analysis of "The fluctuating female vote" and Simonsohn et al.'s re-analysis of "Female hurricanes are deadlier than male hurricanes".
- **Link to BLADE** [P-page]. BLADE's `hurricane` dataset comes from the specification-curve paper. Its `fertility` research question ("effect of hormonal fluctuations associated with fertility on women's religiosity") appears to correspond to the topic of the study Steegen et al. re-analysed; that correspondence is my inference.
- **Not verified.** The specific shares of significant specifications reported in these two papers are [U] and are not given here.

### 6.3 What the evidence shows, and what it does not

- *What the sources show.*
  - With only a question and data, competent analysts' estimates spread over several standard errors and over conflicting conclusions about significance and even sign (CRI [P-page]; Huntington-Klein 2021 [S]; Silberzahn [U]).
  - Coded decisions explain little of that spread (CRI ≤ 2.6% [P-page]).
  - Fixing the design and the cleaned data narrows it, but residual variation remains (Many Economists [S]).
  - Peers judge almost all independent pipelines acceptable (Multi100 [P-page]).
- *What the sources do not show (assessment).*
  - Dispersion across analysts is not the same as *legitimate* dispersion. It mixes defensible choices, different interpretations of the question and outright errors, and the studies I could access do not separate these cleanly.
  - Peer acceptability ratings measure tolerance more than correctness.
  - The dispersion of a human panel also does not carry over to AI agents, which appear to cluster more tightly (Grundl [S]).

---

## 7. Comparison table

Domain experts' roles are rarely documented in the sources I could access; "—" means not found.

| Benchmark (year; venue) | Capability graded | Data | Construction; expert role | Ground truth and alternatives | Verification | Economics content | Headline result | Evidence |
|---|---|---|---|---|---|---|---|---|
| BLADE (2024; EMNLP Findings) | Analysis decisions: variables, transforms, models; discerning justifiable decisions | 12 real datasets (14 folders) | Expert analysts' independent analyses plus peer review of alternatives, some LLM-seeded | **Set-valued**: 502 specifications in a branching tree; 188 MCQs | Transforms by value/graph hash; models and variables by an LLM judge (≥ 8 of 10); coverage@k, hit rate, F1 | 4 of 12 datasets | Basic, low-diversity analyses | P-page, S |
| DiscoveryBench (2024; ICLR 2025) | Data-driven hypothesis discovery | 264 real tasks plus 903 synthetic | Manually extracted from papers | Single gold hypothesis per query | LLM-judged context × variables × relations | 16 of 264 economics-labelled; 69 sociology | ~25% best | P-page, S |
| QRData (2024; ACL Findings) | Statistical and causal reasoning with data | 411 questions, 195 data sheets [S] | Textbooks and datasets | Single answer | ±3% relative band; MC prefix match | Little (textbook social science) | GPT-4 58% | P-page, S |
| DSBench (2024; ICLR 2025) | Data analysis and modelling | ModelOff and Kaggle | Collected from competitions | Single answer | LLM-checked answers | Financial modelling | 34.12% | P-page, S |
| DA-Code (2024; EMNLP) | Agentic data-science code | 500 tasks [S] | — | Gold files | Scripted comparison | — | 30.5% | P-page, S |
| InfiAgent-DABench (2024; ICML) | Closed-form data analysis | 257 public (dev) / 603 [S] | Questions with human filtering | Single answer; **method fixed by constraints** | Exact match after GPT-3.5 reformatting | — | — | P-page, S |
| StatQA (2024; NeurIPS D&B) | Whether a statistical method applies | 11,623 synthetic-template items | Automated construction; human comparison study | Single answer | Accuracy | — | GPT-4o 64.83% | P-page |
| CLadder (2023; NeurIPS) | Formal causal inference by rung | Synthetic stories | Causal inference engine | Single yes/no | Accuracy | — | "Highly challenging" | P-page, S |
| CaLM (2024; report) | Causal-reasoning taxonomy | 126,334 items [S] | Taxonomy-driven | Single answer | 7 metrics [S] | — | 50 findings [S] | P-page, S |
| Corr2Cause (2023; ICLR 2024) | Causation from correlations | 200K+ synthetic | DAG enumeration | Single answer | Accuracy | — | Near random | P-page, S |
| CausalDS (2026; arXiv) | Causal reasoning with abstention | Synthetic scenes | Generated | Includes "decline to answer" | Multi-axis | — | Not verified | S |
| CauSciBench (2025–26; ICML 2026) | End-to-end applied causal inference | 175 real (96 papers), 143 synthetic, 39 QRData | Replications of published results | Single reference estimate plus SE (SE not graded) | Method accuracy; **effect within 5%**; variable overlap | **High** (many classic economics designs) | Method selection is the bottleneck [S] | P-page, S |
| CausalReasoningBenchmark (2026; arXiv) | Identification specification **and** estimate with SE | 173 queries over 132 or 138 datasets | Curated from papers and textbooks | Structured specification | Scored separately; tolerance unknown | Partial | 84%/30% or 79%/34% by version | S |
| CausalVerify (2026; arXiv; NeurIPS D&B submission) | Four layers: method, design, execution, estimand recovery | 259 economics-paper contexts; 100 synthetic; 23 synthetic twins | Gold designs **built by Claude-family agents under the authors' rulings** | Gold design records with **admissible implementations**; canonical estimate on the realised data | 50% band (executable arm); **0.5 SE and SE ratio 0.8–1.25** (paired arm); hash-committed design; oracle arm | **High** | 15.5% executed-but-wrong; oracle 15.0% → 51.5% | P-page |
| InterveneBench (2026; arXiv) | Intervention reasoning and study design | 744 studies [S] | — | — | — | Policy studies | Models fall short [S] | P-page, S |
| NBER WP 35588 (2026) | Econometric coding with the method named | 40 simulated-data tasks [S] | Economist authors | Reference output | — | Methods only | 74→96% or 79→97% by version | S |
| MetricsAI (2025; arXiv) | Agent replication of econometric tasks | Papers and PhD coursework | — | Published results | "Directional" or "partial" replication | High | >90% directional (own agent) | S |
| EconCausal (2025–26; arXiv) | Signs of causal effects in context | 10,490 triplets from 2,595 papers | Extracted from published studies | Single sign label | Accuracy | High (text only) | Null effects recognized 13.8% | S |
| STEER / STEER-ME (2024 / 2025) | Economic rationality | Template-generated | Taxonomy of elements | Single answer | Accuracy and calibration | Theory | — | P-page, S |
| EconLogicQA, EconNLI, EconEvals, EconWebArena, BenCSSmark, EconBench | Economic event logic; NLI; decisions; web retrieval; CSS text tasks; structural reasoning | Text, synthetic or live web | LLM-generated plus human review (several) | Single answer | Accuracy | Theory or text | Varied | S (some P-page) |

---

## 8. Implications for alternative valid implementations (assessment, not decisions)

### 8.1 How much legitimate dispersion to expect

1. **When a task gives only a question and data, there is no defensible single numeric answer.**
   - The many-analysts studies show spreads of several standard errors (Huntington-Klein 2021 [S]) and conflicting signs (CRI [P-page]).
   - A tolerance band wide enough to accept every competent open-ended answer would also accept many consequential errors. A band narrow enough to reject errors would reject legitimate alternatives.
   - Bercovich's rule (§4) applies directly: "either the verifier has to accept all of them, or the instruction needs to be tighter".
2. **Specification is the main lever, and the Many Economists design shows how to measure it.**
   - Fixing the research design and the cleaned data cut dispersion to an IQR of 2.4 pp in the DACA study [S].
   - DeepEcon can run the same staged comparison as calibration for each task family:
     - an "open" version;
     - an "estimand and design fixed" version;
     - a "data fixed" version.

     Each version would be solved by several economists, or at least several independent reference implementations.
   - Tasks whose dispersion stays large after fixing should not be graded numerically.
3. **Agent runs cannot set tolerances by themselves.**
   - If humans spread 2–27 times more widely than agents (Grundl [S]), bands derived from agent runs will reject legitimate human alternatives.
   - This is the verifier false-negative problem that R4 documented for CORE-Bench and ScienceAgentBench.
   - Calibration should use expert implementations.
4. **Dispersion is not legitimacy.**
   - A spread across analysts includes errors.
   - Brief §3.3 item 10 ("evidence that the error is genuinely incorrect, rather than an alternative valid approach") therefore needs evidence for each decision, not "it falls outside the panel's spread".

### 8.2 Using BLADE-style decision spaces to define acceptable answer sets

**Proposal.** Each task carries a hidden **decision space**: a tree of decision nodes, adapted from BLADE's annotation format and CausalVerify's design record. Typical nodes are:
- the estimand and target population;
- the sample definition;
- variable construction;
- treatment timing;
- the estimator;
- fixed effects and controls;
- weights;
- inference (SE type, clustering level, few-cluster correction);
- the scope of interpretation.

For each node, the options are labelled:
- `reference`: the validated correct package;
- `accepted`: a justifiable alternative, with rationale and citation;
- `unjustifiable`: a known error, ideally one of the expert-designed flawed packages, with evidence;
- `contested`: experts disagree; not graded as a binary outcome.

Each option also records its **provenance**: contributor, LLM-suggested or reviewer, following BLADE's `is_llm_generated` flag and the brief's §5.5 requirement to say where each statement came from. CausalVerify's split between `PAPER_FAITHFUL` and modernized inference is a ready-made way to handle inference conventions that have changed since publication.

**How the set grades an answer: compare each declared choice with its own reference.**
1. The agent submits code plus a machine-readable manifest of its choices for the nodes that matter.
2. *Check the declared options.* Every declared option must be `accepted` or `reference`. An `unjustifiable` option fails the task. This targets failure modes 1, 4 and 6 in the brief.
3. *Check that the code does what it declares.* The verifier recomputes the reference result for *that declared combination* and compares it with the agent's output. The tolerance covers only numerical and stochastic noise. If the declaration and the implementation disagree, as in an "estimator–implementation mismatch", this check fails.
4. *Check intermediate artefacts by execution, as BLADE does.* Examples are a hash of the estimation sample's unit-by-period identifiers, or a hash of a constructed treatment-timing variable. This catches sample and timing errors that leave the headline number nearly unchanged.
5. *Replay the code on hidden data variants.* The agent's code is re-run on perturbed or synthetic-twin data with known references (reading-notes implication 2; R4 implication 9; CausalVerify's twins). This separates procedures that agree by chance on the released data.

**Lessons from BLADE to avoid repeating (assessment).**
- (a) Its negatives are mostly LLM-generated (101 of 145 "select the unjustifiable" answers), and some are not even feasible with the data. DeepEcon's `unjustifiable` options should be realistic expert-designed mistakes (brief safeguard G).
- (b) BLADE scores only *coverage* of the space and never whether the resulting *numbers* are right. DeepEcon needs both.
- (c) BLADE's LLM matching of models and variables is unvalidated in the repository. Where DeepEcon can check a node by execution, it should not use an LLM.
- (d) An "accepted" set built by asking for peer acceptability will be too broad: Multi100 rated 98.4% of pipelines acceptable. Acceptance should require a stated rationale and, for consequential nodes, a citation (Bercovich §9's "standard of evidence").

### 8.3 When to use tolerance bands and when to fix the estimand explicitly

| Situation | Recommended grading | Why |
|---|---|---|
| Estimand, sample and estimator fixed; differences come only from numerics (bootstrap, optimizer, Stata vs R defaults) | A **tolerance band** calibrated from repeated reference runs and independent cross-software implementations (CORE-Bench's prediction interval, R4). Express it in **SE units** (CausalVerify uses 0.5 SE) and add an **SE-ratio check** when inference is graded (CausalVerify: 0.8–1.25) | A fixed relative band (QRData ±3%, CauSciBench 5%, CausalVerify's executable arm 50%) ignores precision. It is too strict for noisy estimates and too lax for precise ones. CausalVerify's error rates move from 27.2% to 14.1% across bands |
| Estimand fixed, but several valid estimators or specifications give materially different numbers (for example, two heterogeneity-robust staggered-DiD estimators) | A **declared-choice decision space** (§8.2) with a reference per accepted option | No single band separates the valid options from the flawed ones |
| Choosing the estimand or design *is* the capability being tested (identification judgement) | **Grade the decision**: accepted versus unjustifiable options, scored with precision and recall. A numeric check is secondary | Fixing the estimand would remove the capability being tested (Bercovich's "one-sentence fact" tension, reading notes implication 6) |
| Experts disagree, or the question is not identified from the data | **Do not grade it as binary.** Exclude it, or grade with a rubric whether the agent recognises the issue, states its consequence or abstains (as CausalDS scores abstention) | Brief §4: "Do not impose artificial binary answers on genuinely contested or underidentified methodological questions" |
| A flawed procedure gives nearly the same number as the correct one on the released data | Check the decision or intermediate artefact directly, or **replay on hidden data** where the flaw diverges. If neither works, drop the numeric check for that flaw | Brief §4: "a flawed procedure may occasionally produce the same numerical answer as the correct one" |

**A testable admission rule for any numeric band (proposal).**
- Let r be the reference result, V the outputs of all validated `accepted` implementations, and F the outputs of all validated flawed packages.
- A band [r − h, r + h] is admissible only if two conditions hold:
  - it accepts every valid output: max over V of |v − r| ≤ h;
  - it rejects every flawed output: min over F of |f − r| > h.
- If no h satisfies both, the task needs a choice-conditional reference or a decision-level check instead.
- Bercovich's "two experts, two verifiers" test (reading notes implication 4) and the "over-specification fairness check" (implication 5) should be run before a band is frozen.
- Bands should be fixed *before* agent outputs are seen. CausalVerify's three scorer revisions after outputs existed (56.1% → 33.1% → 15.5%) show how much measured error rates can move otherwise.

### 8.4 Consequences for the contribution schema and interview (proposal)

- The interview should ask the contributor to list the **alternatives they considered and rejected**, and the alternatives they would accept. These become `accepted` and `unjustifiable` nodes, each with a rationale and evidence anchor (CausalVerify's provenance fields: evidence anchor, confidence, ambiguity note).
- A second economist should **validate the alternatives**, as BLADE's peer-review step does. The validation is recorded, and options the LLM suggested are flagged.
- The agent-facing instruction should state the estimand and the decisions that matter, at the level the task's target capability allows.
- The decision space, references and flawed outputs stay hidden. This preserves the brief's §5.4 separation between agent-facing and hidden evaluation materials.

---

## 9. Where existing benchmarks already test causal and econometric reasoning, and where DeepEcon would differ

### 9.1 Coverage map

| Layer | Already graded by | How | Gaps relevant to DeepEcon |
|---|---|---|---|
| Choosing a statistical method or judging it applicable | StatQA, QRData [P-page] | Accuracy on single answers | Textbook-level |
| Formal causal inference with the graph given | CLadder, Corr2Cause, CaLM [P-page]; CausalDS [S] | Accuracy; abstention (CausalDS) | No real data or implementation |
| Recognizing the design or method from a real study | CauSciBench [P-page]; CausalReasoningBenchmark [S]; CausalVerify real-paper arm (259 economics papers) [P-page]; InterveneBench [S] | Method labels; LLM-consensus labels (CausalVerify, κ = 0.61 against a blinded audit) | Text-level only |
| Specifying the design (treatment, outcome, controls, instrument, running variable, timing) | CauSciBench (treatment, outcome, control overlap) [P-page]; CausalReasoningBenchmark [S]; CausalVerify paired arm, design checked against gold records [P-page]; BLADE variables [P-page] | Field matching; outcome-blind adjudication | References built by LLM agents (CausalVerify) or by benchmark authors |
| Data construction and sample definition | BLADE (transforms checked by execution) [P-page]; DiscoveryBench (only through final hypotheses), DA-Code, DSBench, InfiAgent [P-page] | Value hashing (BLADE); otherwise only the final answer | Not on real economics pipelines |
| Recovering the point estimate | QRData ±3%; CauSciBench 5%; CausalVerify 50%, or 0.5 SE on twins [P-page]; CausalReasoningBenchmark [S]; NBER 35588; MetricsAI [S] | Fixed relative bands (except CausalVerify's SE-scaled band) | Bands not calibrated to valid alternatives or flawed packages |
| **Statistical inference (SE, clustering)** | CausalVerify paired arm (SE ratio 0.8–1.25 on synthetic twins) [P-page]; CausalReasoningBenchmark asks for the SE (scoring unknown) [S]. CauSciBench stores the SE but does not grade it [P-page] | Checks on synthetic twins | **No benchmark found that grades clustering-level or few-cluster choices by execution on real packages** |
| Interpretation and claims | DiscoveryBench (LLM-judged), EconCausal (sign and null) [S]; R4 §2.7 studies | LLM judge or label accuracy | Not tied to what a specific design supports |
| **Detecting errors in an existing implementation** | None found among these benchmarks. BLADE's MCQs ask for single unjustifiable decisions [P-page] | — | **Open** |
| **Correcting errors while keeping the estimand** | CausalVerify's repair round, on agents' *own* failing code with typed feedback [P-page] | One stateless repair call | Not expert-designed errors |
| Credit for alternative valid implementations | BLADE (set-valued decisions); CausalVerify ("admissible implementations"); ReplicatorBench's acceptable variants (R4) [P-page] | Matching decisions; enumerated admissible options | No combination of decision sets with numeric references for each option |

### 9.2 Where DeepEcon would differ (conservative statement)

DeepEcon would **not** be first at any of the following:
- causal-design recognition or specification on real economics papers (CauSciBench, CausalVerify, CausalReasoningBenchmark);
- separating design failures from execution failures (CausalVerify's layers and oracle arm);
- SE-scaled verification on synthetic twins (CausalVerify);
- set-valued ground truth for analysis decisions (BLADE);
- calibrating against many-analysts panels (Grundl).

As of 2026-11-05 I did **not find**:
1. **Expert-designed flawed versions of real economics replication packages.** These would serve both as *negative controls* that verifiers must reject and as *error-detection and error-correction tasks* graded by execution. CausalVerify's oracle arm swaps in a correct design; it does not plant wrong ones. BLADE's negatives are single, mostly LLM-generated decisions.
2. **Errors in inference choices graded inside real packages**, such as the wrong clustering level, ignoring few clusters, or inappropriate inference with staggered treatment. CausalVerify checks the SE only on synthetic twins and under paper-faithful conventions.
3. **Tasks set inside the paper's actual multi-step pipeline** (data construction, sample restrictions, variable definitions across files), not on one cleaned CSV per query (CauSciBench) or a synthetic twin (CausalVerify). Plain reproduction of packages is already covered and near saturation (R4); the difference lies in reasoning tasks inside the package.
4. **Decision spaces elicited from original authors**, including rejected alternatives. CausalVerify's gold records were built by LLM agents under the authors' rulings, and BLADE's by expert analysts, not by the papers' authors.
5. **Grading that keeps computational, statistical and identification validity separate**, with an explicit "contested" category. CausalVerify's four-layer profile is close in spirit, so this difference is modest and should not be overclaimed.

**Risks to this claim.**
- The field is moving monthly: CausalVerify v2 came out in September 2026 and CausalDS in July 2026.
- My search was cut short by the search budget.
- Several benchmarks (CausalReasoningBenchmark, the NBER 35588 PDF, CauSciBench's paper) were seen only through summaries.

DeepEcon's novelty should be stated as *the combination*, especially items 1 and 2, and the collaborator brief should cite CausalVerify, CauSciBench, CausalReasoningBenchmark and BLADE as the closest precedents.

---

## 10. Open questions

1. **Calibration.** For DeepEcon's first task families, how large is the residual dispersion across independent expert implementations once the estimand and the key decisions are fixed? Should DeepEcon run a small Many-Economists-style staged calibration study?
2. **Contested options.** Who decides that an option is "contested" rather than "accepted" or "unjustifiable", and on what standard of evidence (Bercovich §9)?
3. **Gaming the manifest.** Grading against the agent's declared choices rewards honest declarations. How do we stop agents from declaring the reference option while implementing something else? Comparing outputs with each declared option's reference, plus hidden-data replay, should catch it, but this needs testing.
4. **Paper-faithful and modern inference.** When the published paper's inference is now considered inadequate (for example, unclustered SEs), which is the reference? CausalVerify's split between `PAPER_FAITHFUL` and `ROBUSTNESS_ONLY` is one model.
5. **Units for tolerances.** For point estimates, should tolerances be in SE multiples, relative percentages or prediction intervals from reference re-runs? What tolerance applies to SEs themselves (CausalVerify uses a ratio of 0.8–1.25)?
6. **LLM judges.** For decision nodes that cannot be checked by execution, such as interpretation, what agreement between the judge and humans is required? BLADE documents none, and CausalVerify reports 90.9% only for coefficient extraction.
7. **Numbers to verify before external use.**
   - Many-analysts studies: Silberzahn's odds-ratio range, NARPS's team count, all Menkveld et al. figures, and the Many Economists stage 1 and 2 IQRs.
   - Benchmarks: CausalReasoningBenchmark's version figures, NBER 35588's two sets of figures, and the reason BLADE's 502 specifications differ from the 536 reported.
8. **Reuse and licensing.** Could DeepEcon reuse or extend existing assets: BLADE's data (ODC-By), CauSciBench's real-paper queries (licences vary by dataset), or CausalVerify's design schema (MIT)? Would doing so speed up construction or blur DeepEcon's distinctiveness?

---

## 11. Access problems

- **DNS failures (WebFetch, ENOTFOUND, "outside the session's allowed network domains"):**
  - `aclanthology.org` (BLADE paper page);
  - `www.ebi.ac.uk` (Europe PMC API, tried for the many-analysts papers).

  After this second failure I **stopped trying new hosts**, as instructed. Both hosts would need to be allowed in the session's network settings.
- **Web-search budget exhausted.** After about 35 queries the tool returned "this turn's web search budget is used up (limit: 200 WebSearch calls per turn, shared by every agent in it)". The limit can be raised with `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`, or searching can continue in a follow-up message. Searches I could not run:
  - the Menkveld et al., Silberzahn et al., Botvinik-Nezer et al. and Multi100 abstracts;
  - the Many Economists stage-level IQRs;
  - repositories for EconEvals, EconWebArena, EconCausal and BenCSSmark;
  - World Bank blog details.
- **Not attempted, because they were known to be unreachable in R4:** arxiv.org, huggingface.co (so the CausalReasoningBenchmark data and CauSciBench CSVs were not inspected), nber.org, pnas.org, osf.io, openreview.net, proceedings.neurips.cc and semanticscholar.org.
- **Denied by the permission classifier:** reading the proxy README and status endpoint.
- **What worked:** raw.githubusercontent.com and `git clone --depth 1` from github.com. These are the basis of every [P-page] label.
- **Consequence:** this note has **no [P-full] sources**. Paper-level numbers labelled [S] or [U] must be checked against the PDFs before they are cited in collaborator-facing documents.

---

## 12. Sources

All accessed 2026-11-05. "raw" means the file was read via raw.githubusercontent.com from the default branch; "clone" gives the commit.

**Primary repository material [P-page]**
- BLADE: https://github.com/behavioral-data/BLADE (clone 6118fa8). Files read: `README.md`, `blade_bench/datasets/*/{info.json,annotations.csv,mcq_dataset.json}`, `blade_bench/eval/match/*.py`, `blade_bench/eval/metrics/{final_metrics,calc_metrics}.py`, `blade_bench/eval/llm/{model_similarity,conceptual_var_similarity}.py`, `blade_bench/baselines/lm/mcq.py`.
- DiscoveryBench: https://github.com/allenai/discoverybench (clone c31fcf0). Files read: `discoverybench/real/**/metadata_*.json`, `eval/eval.py`.
- QRData: https://github.com/xxxiaol/QRData (raw: `README.md`, `benchmark/QRData.json`, `benchmark/eval.py`).
- DSBench: https://github.com/LiqiangJing/DSBench (raw: `README.md`, `data_analysis/readme.md`).
- DA-Code: https://github.com/yiyihum/da-code (raw README).
- InfiAgent-DABench: https://github.com/InfiAgent/InfiAgent (raw: `README.md`, `examples/DA-Agent/README.md`, `examples/DA-Agent/data/da-dev-questions.jsonl`).
- StatQA: https://github.com/HKUSTDial/StatQA (raw README).
- CLadder: https://github.com/causalNLP/cladder (raw README).
- CaLM: https://github.com/OpenCausaLab/CaLM (raw README).
- Corr2Cause: https://github.com/causalNLP/corr2cause (raw README).
- CauSciBench: https://github.com/causalNLP/CauSciBench (raw README; clone d9bb43a). Files read: `data/README.md`, `data/metadata_csv/{real,synthetic,qr}_input.csv`, `evaluation/metrics.py`.
- CausalVerify: https://github.com/causalverify/causalverify (raw README; clone 60b6015). Files read: `experiments/v2_paired/cdr_schema_v1.2.json`, `experiments/v2_paired/gold_cdr/paper_14_gold_cdr_v1.json`. Earlier README: https://github.com/yonghongzhang-io/causalverify (raw).
- InterveneBench / STRIDES: https://github.com/Sii-yuning/STRIDES (raw README).
- EconNLI: https://github.com/Irenehere/EconNLI (raw README).
- STEER / STEER-ME: https://github.com/narunraman/STEER (raw README).
- Crowdsourced Replication Initiative (Breznau et al.): https://github.com/nbreznau/CRI (raw: `README.md`, `data/cri.csv`, `code/01_CRI_Descriptives.Rmd`).
- NARPS: https://github.com/poldrack/narps (clone 0a9d71a). Files read: `README.md`, `ImageAnalyses/README.md`, `ImageAnalyses/SuppTablesInfo.tsv`, `ImageAnalyses/metadata_files/narps_neurovault_images_details_responses_corrected.csv`.
- Many Economists Project: https://github.com/NickCH-K/ManyEconomists (clone 7b8590b; README stub only).
- Multi100 peer evaluations, via COS: https://github.com/CenterForOpenScience/llm-benchmarking (R4's clone fb6a804; `robustness/data/_aggregate_eval/gt/multi100_peer-eval-not-reviewed_processed_data.csv`).
- specr: https://github.com/masurp/specr (raw README; its citations are used as [S]).
- multiverse: https://github.com/MUCollective/multiverse (raw README; used as [S]).
- Project files: `docs/requirements/2026-11-05-research-lead-brief.md`; `docs/research/reading-notes/good-benchmarks-bercovich-2026.md`; `docs/research/evidence/R4-replication-benchmarks.md`.

**Secondary sources: search-engine summaries of these pages, which I did not open myself [S]**
- BLADE: https://arxiv.org/abs/2408.09667 ; https://idl.uw.edu/papers/blade
- DiscoveryBench: https://arxiv.org/abs/2407.01725 ; https://proceedings.iclr.cc/paper_files/paper/2025/file/0d70af566e69f1dfb687791ecf955e28-Paper-Conference.pdf ; https://mlanthology.org/iclr/2025/majumder2025iclr-discoverybench
- QRData: https://arxiv.org/abs/2402.17644 ; https://preview.aclanthology.org/setup/2024.findings-acl.548
- DSBench: https://arxiv.org/abs/2409.07703 ; https://iclr.cc/virtual/2025/poster/30458
- DA-Code: https://arxiv.org/abs/2410.07331 ; https://aclanthology.org/2024.emnlp-main.748
- InfiAgent-DABench: https://proceedings.mlr.press/v235/hu24s.html ; https://arxiv.org/abs/2401.05507
- StatQA: https://arxiv.org/abs/2406.07815 ; https://nips.cc/virtual/2024/poster/97546
- CLadder: https://proceedings.neurips.cc/paper_files/paper/2023/hash/631bb9434d718ea309af82566347d607-Abstract.html ; https://arxiv.org/abs/2312.04350
- CaLM: https://arxiv.org/abs/2405.00622
- Corr2Cause: https://arxiv.org/abs/2306.05836 ; https://www.research-collection.ethz.ch/items/ec00f25b-0f42-4866-a9b4-e71d955296cd
- CausalDS: https://arxiv.org/abs/2607.08093 ; https://aiweekly.co/alerts/hf-paper-causalds-953-scene-causal-reasoning-benchmark-for-data-science-agents
- CausalReasoningBenchmark: https://arxiv.org/abs/2602.20571 ; https://huggingface.co/datasets/syrgkanislab/CausalReasoningBenchmark
- CauSciBench: https://icml.cc/virtual/2026/poster/60944 ; https://neurips.cc/virtual/2025/loc/san-diego/124112 ; https://zhijing-jin.com/files/papers/2025_CauSciBench.pdf
- CausalVerify: https://arxiv.org/abs/2609.07944
- InterveneBench: https://arxiv.org/abs/2603.15542
- NBER WP 35588: https://www.nber.org/papers/w35588 ; https://ideas.repec.org/p/nbr/nberwo/35588.html ; https://cepr.org/voxeu/columns/letting-ai-agents-write-econometric-code
- MetricsAI: https://arxiv.org/abs/2506.00856
- EconLogicQA: https://arxiv.org/abs/2405.07938 ; https://sotaverified.org/papers/econlogicqa-a-question-answering-benchmark
- EconNLI: https://aclanthology.org/2024.findings-acl.58/ ; https://arxiv.org/abs/2407.01212
- STEER: https://arxiv.org/abs/2402.09552 ; https://icml.cc/virtual/2024/poster/33120 ; https://mlanthology.org/icml/2024/raman2024icml-steer. STEER-ME: https://arxiv.org/abs/2502.13119 (as linked from the STEER README)
- EconEvals: https://arxiv.org/abs/2503.18825 ; https://www.alphaxiv.org/abs/2503.18825
- EconWebArena: https://arxiv.org/abs/2506.08136 ; https://neurips.cc/virtual/2025/132568
- BenCSSmark: https://arxiv.org/abs/2605.04886 ; https://aclanthology.org/2026.lrec-1.64/ ; https://pith.science/paper/2605.04886
- EconCausal: https://arxiv.org/abs/2510.07231
- EconBench (SSRN): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6803400
- Grundl (2026): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6219138 ; https://policy.fi/ai-econ/
- HouseholdBench: https://www.nber.org/papers/w35927. NBER WP 35188: https://www.nber.org/system/files/working_papers/w35188/w35188.pdf
- "Wrong and More Confident": https://arxiv.org/abs/2607.23424. LiveMacroEval: https://aclanthology.org/2026.emnlp-main.800/
- Ludwig, Mullainathan, Rambachan: https://arxiv.org/abs/2412.07031 ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5094968
- Huntington-Klein et al. (2021): https://doi.org/10.1111/ecin.12992 ; https://econpapers.repec.org/RePEc:bla:ecinqu:v:59:y:2021:i:3:p:944-960 ; https://digitalcommons.oberlin.edu/faculty_schol/4406
- Many Economists (2025): https://www.nber.org/papers/w33729 ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5241499 ; https://blogs.worldbank.org/en/impactevaluations/same-data--same-research-design--different-results ; https://nickchk.com/ ; https://www.linkedin.com/posts/nick-huntington-klein-34292a13_the-sources-of-researcher-variation-in-economics-activity-7300232552747876353-Ru7H
- Specification curve and multiverse citations (via the specr README): https://doi.org/10.1038/s41562-020-0912-z ; https://doi.org/10.1177/1745691616658637

**Linked but not opened (bibliographic pointers only)**
- Breznau et al., PNAS: https://www.pnas.org/doi/10.1073/pnas.2203150119 (linked from the CRI README)
- Silberzahn et al., AMPPS: https://journals.sagepub.com/doi/10.1177/2515245917747646 (linked from the BLADE README)
- Many Economists *JEL* resubmission PDF: https://static1.squarespace.com/static/53c31c5ce4b053fc7d131b18/t/698bb992970cca10f153bf15/1770764690354/2025-11-jel-resubmission.pdf (surfaced by search; not fetched)

**Unverified background knowledge [U]:** the Silberzahn et al. figures; NARPS's 70 teams and "no two identical workflows"; all Menkveld et al. (2024) figures; the publication details of the Multi100 paper.
