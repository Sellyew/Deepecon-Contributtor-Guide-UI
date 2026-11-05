# R4: AI-agent benchmarks for computational reproduction and replication, with emphasis on economics and social science

| Field | Value |
|---|---|
| Topic | Existing benchmarks and studies that evaluate AI agents on reproducing or replicating published research, especially in economics and the social sciences. The note also covers adjacent work on error detection and causal-identification judgment, and checks whether the name "DeepEcon" is already taken. |
| Date | 2026-11-05. All URLs were accessed on 2026-11-05. |
| Author | research agent |
| Scope | The 14 benchmarks and studies named in the assignment, a broad search for economics- and social-science-specific work from 2025 and 2026, three targeted questions ((a) flawed packages or injected errors, (b) identification and inference judgment, (c) tacit knowledge from original authors), a comparison table, a statement of what DeepEcon would and would not add, and the name-collision check. |
| Evidence labels | **[P-full]** primary source, full text read. **[P-page]** primary source, abstract, landing page, README, repository file or official doc page read. **[S]** secondary source (search-engine summary, blog, news, aggregator). **[U]** unverified. |
| Evidence limits | **I could not read the full text of any benchmark paper in this note.** arxiv.org and most publisher, proceedings and aggregator hosts are unreachable from this environment (see "Access problems"). [P-page] claims come from GitHub READMEs fetched through raw.githubusercontent.com, or from files in shallow clones that I read but did not execute. [S] claims come from the WebSearch tool's summaries of result pages, usually arXiv abstract or HTML pages, which I did not open myself. Paper-level numbers labelled [S] should be checked against the PDFs before anyone cites them externally. |
| Relation to other notes | This note uses the project's reading notes on Bercovich (2026), *Good Benchmarks* (`docs/research/reading-notes/good-benchmarks-bercovich-2026.md`), which record a full-text read, as the yardstick for the implications. |

## Summary (10 bullets max)

1. **Reproduction from supplied code and data is close to saturated for frontier coding agents, including in social science.** Claude Code reaches 93.4% task-level accuracy on SocSci-Repro-Bench (221 tasks from 54 social-science papers) [P-page]. Princeton's HAL team treats CORE-Bench Hard as "solved" at 95.5% after manual validation; automatic grading gives 77.78% [S]. A DeepEcon task that only asks an agent to re-run a package would measure little.
2. **Economics-relevant reproduction and replication benchmarks already exist.** They are REPRO-Bench (ACL 2025; 112 social-science papers built from public reproduction reports [P-page], mostly economics and political science [S]), ReplicatorBench (KDD 2026; replication with new data from the SCORE project, economics papers included) [P-page], SocSci-Repro-Bench (2026) [P-page], and a methods-only reimplementation study on 48 papers from the Institute for Replication (I4R) [S]. A 2026 NBER workflow was run on 4,452 economics replication packages [S]. None of these targets methodological judgment as the graded construct.
3. **The Institute for Replication's randomized "AI games" (Brodeur et al., PNAS 2026) are the closest human-plus-AI precedent in economics.** I recomputed the reproduction rates from the released data: 31/33 human-only teams, 32/35 AI-assisted teams and 13/35 AI-led teams. The study scored teams on detecting major and minor coding errors against a catalogue of **naturally occurring** errors (122 entries over 12 papers) [P-page].
4. **On (a), I found no benchmark built from deliberately flawed replication packages (code plus data).** Error injection exists only in paper text (FLAWS, PaperAudit-Bench, LimitGen-Syn, a clinical-trial study), as planted pitfalls for AI-scientist systems in machine learning, or as one corrupted-model task in RE-Bench [S/P-page]. Economics benchmarks use natural errors only: REPRO-Bench's 1–4 reproducibility rating and I4R's error catalogue [P-page].
5. **On (b), identification and inference judgment is now partly covered, mostly outside full replication packages.** CausalReasoningBenchmark (2026) scores the identification specification separately from the estimate. CauSciBench (ICML 2026) finds method selection is the bottleneck. CausalVerify (2026) has the agent commit to a design before seeing the data, and an "oracle arm" separates design failures from execution failures. BLADE grades analysis decisions [S]. NBER WP 35588 tests econometric coding when the method is already named [S].
6. **On (c), original authors are already used to define ground truth, but not to elicit mistakes.** PaperBench co-develops rubrics with authors and ships author addenda for the agent and for the judge [P-page/S]. ReplicationBench co-develops tasks with original authors and uses tolerances the authors submit [S]. SPOT uses author-confirmed errata [S]. None of them elicits authors' knowledge of plausible mistakes or critical decisions.
7. **Interpretation is the layer most open to manipulation.** In one 2026 study, a confirmatory prompt moved Claude Code's support verdicts from 10% to 90% while its coefficient estimates barely changed [S]. Separately, SocSci-Repro-Bench reports that prompt framing can nudge agents toward confirmatory specification search [S].
8. **Verifier false negatives and LLM judges are recurring problems.** CORE-Bench's automatic grader rejected correct alternative techniques [S]. ScienceAgentBench released a "verified" split in April 2026 to reduce false negatives [P-page]. PaperBench, ReplicatorBench, EXP-Bench and BixBench all rely on LLM judges [P-page].
9. **Contamination is a measured risk for social-science replication.** When materials were not anonymized, both agents on SocSci-Repro-Bench reportedly scored 100% [S]. Published Top-5 replication packages are public, so DeepEcon cannot rely on secrecy of the original package.
10. **The name "DeepEcon" is taken.** An MIT-licensed Python econometrics package `deepecon` exists on PyPI and GitHub (SepineTam/DeepEcon), with an English and Chinese README and the same maintainer as the widely used MCP-for-Stata tool [P-page]. An Econ-ARK page also points to a site, deepecon.org, for deep-learning solution methods [S]. Collision risk is moderate to high in the Chinese-speaking empirical-economics community.

---

## 1. Method

- **Searches (WebSearch, standard and extended modes).** Queries covered each named benchmark plus the following:
  - "economics replication benchmark agent", "AEA replication package LLM", "econometrics agent benchmark 2026", "Stata agent benchmark"
  - "social science agent benchmark 2026", "causal inference agent benchmark", "EconBench/EconAgentBench", "ReplicatorBench"
  - error-injection queries (scientific papers, replication packages, economics referees) and many-analysts queries
  - one Chinese-language query, and the "DeepEcon" name in English and Chinese
- **Primary repository material** was read via raw.githubusercontent.com: READMEs for CORE-Bench, REPRO-Bench, PaperBench, SciReplicate-Bench, LMR-Bench, AutoReproduce, EXP-Bench, SUPER, ScienceAgentBench, RE-Bench, LAB-Bench, BixBench, COS llm-benchmarking/ReplicatorBench, SocSci-Repro-Bench, I4R AI-Games, SepineTam/DeepEcon and SepineTam/stata-mcp.
- **Shallow clones** were made into new empty directories under the scratchpad's `refs/`. I read files only and executed nothing from them; I used my own scripts, run with `python3 -I`, to parse data files.
  - `uiuc-kang-lab/REPRO-Bench`, commit 75f112f, 2025-11-02
  - `siegelz/core-bench`, commit e32a298, 2025-11-23
  - `CenterForOpenScience/llm-benchmarking`, commit fb6a804, 2026-06-24
  - `I4Replication/AI-Games`, commit c2721bb, 2026-06-02
  - an existing scratchpad clone of `harbor-framework/terminal-bench-science`, commit 9276073, 2026-11-04

---

## 2. Findings by benchmark

### 2.1 Reproduction when code and data are supplied

#### CORE-Bench (Siegel et al., 2024)
- **Identity.** "CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark", by Zachary Siegel, Sayash Kapoor, Nitya Nadgir, Benedikt Stroebl and Arvind Narayanan (Princeton). arXiv:2409.11363 (Sept 2024), listed as TMLR 2024 [S]. Repository: https://github.com/siegelz/core-bench [P-page].
- **Capability measured.** "the ability of agents to computationally reproduce scientific papers". The agent installs dependencies, runs the code, and answers questions about the outputs in `report.json`. The set has 270 tasks from 90 papers in computer science, social science and medicine, using Python or R [P-page]. There are three difficulty levels [S]; the harness names levels such as `codeocean_hard`, and CORE-Bench-Medium needs Docker-in-Docker [P-page].
- **Construction.** Curated by the authors from public code "capsules", which the harness downloads from corebench.cs.princeton.edu [P-page]. The authors say the tasks can be refreshed from public repositories to address contamination and saturation [S]. No domain-expert authoring is reported in the sources I could read [S].
- **Verification.** Numeric answers count as correct if they fall inside a **95% prediction interval** computed from several reference runs (`t.ppf(0.975, n-1)·sd·sqrt(1+1/n)`). Strings must match exactly (case-insensitive) and lists must match exactly (`benchmark/evaluations.py`) [P-page].
- **Contamination.** The test set ships GPG-encrypted, and the password is printed in the README; this protects against crawlers, not people [P-page].
- **Economics coverage.** In the public train split, 14 of 45 capsules are "Social Sciences" (Computer Science 19, Medical 12), and the code is Python (27) or R (18), with **no Stata** [P-page, my count from `core_train.json`]. The social-science titles are mostly psychology, political science and methods; one is an experimental-economics study (real-effort experiments on Payments for Ecosystem Services) [P-page].
- **Headline results.** At release, the best agent reached about 21% on the hardest tier (GPT-4o-based CORE-Agent) [S]. In December 2025, HAL reported Claude Code with Claude Opus 4.5 at 77.78% under automatic grading and 95.5% after manual validation, and said "we're treating CORE-Bench Hard as solved" [S] (https://hal.cs.princeton.edu/corebench_hard; https://substack.com/@sayash/note/c-183913356).
- **Limitations.**
  - The automatic grader marked "correct but slightly distinct" techniques as wrong [S].
  - The original harness "is no longer actively maintained"; the README recommends HAL [P-page].

#### SUPER (Bogin et al., 2024)
- **Identity.** "SUPER: Evaluating Agents on Setting Up and Executing Tasks from Research Repositories", Ben Bogin and seven co-authors (AI2 and University of Washington). EMNLP 2024; arXiv:2409.07440 [S]. Repository: https://github.com/allenai/super-benchmark [P-page].
- **Capability measured.** Setting up and running ML/NLP research repositories "in the GitHub wild" [P-page].
- **Construction.** Three sets: Expert (45 problems), Masked (152) and AutoGen (602) [P-page]; one secondary summary gives 604 for AutoGen [S]. The Expert set has expert-annotated solutions and about three manually extracted "landmarks" per task [S]. How the experts were recruited is not reported in the sources I could access.
- **Verification.** Gold answers, plus landmark-based partial credit [S].
- **Cost.** Running on Modal costs about 2–3 cents per problem on CPU [P-page].
- **Results.** GPT-4o solved 16.3% of the Expert set and 46.1% of the Masked set [S].
- **Economics coverage.** None.

#### REPRO-Bench (Hu et al., 2025)
- **Identity.** "REPRO-Bench: Can Agentic AI Systems Assess the Reproducibility of Social Science Research?" (the README says "…Social Science Papers?"), UIUC Kang lab. The README calls it an "ACL 2025 paper" [P-page]; the ACL Anthology lists it as Findings (2025.findings-acl.1210) [S]. arXiv:2507.18901 [S]. Repository: https://github.com/uiuc-kang-lab/REPRO-Bench. Dataset: https://huggingface.co/datasets/chuxuan/REPRO-Bench [P-page].
- **Capability measured.** Judging the reproducibility of a whole paper, end to end. The agent receives the paper PDF and the full replication package and must output an integer score on a four-level scale [P-page; prompt in `SWE-agent/config/reproduce.yaml`]:
  - 1: "major findings in the paper are irreproducible"
  - 2: "minor inconsistencies and/or errors in the provided data and/or code"
  - 3: "rounding errors or equivalent issues"
  - 4: "fully reproducible"
- **Construction.**
  - 112 task instances, each "PDFs + code + data", with "gold-standard reproducibility annotations" and "public reproduction reports" [P-page].
  - Reported sources include I4R and mass-reproducibility efforts in economics and political science, Retraction Watch, and audits flagged on social media [S].
  - SocSci-Repro-Bench's authors describe the set as drawing on nine economics journals and three political science journals [S].
  - Packages average 4.2 GB and 142 files [S].
- **Verification.** Exact match between the agent's integer score and the gold score (`evaluation.py`) [P-page]. The task does not ask the agent to localize or describe errors.
- **Results.**
  - Three baseline agents (AutoGPT, CORE-Agent, SWE-Agent; GPT-4o) scored at most 21.4% accuracy, below the 25% expected from random guessing over four classes [S].
  - The authors' REPRO-Agent reaches 36.6%, a 71% relative improvement [S].
  - Agents did better on R packages than on Stata packages [S].
- **Errors.** The benchmark contains **naturally** flawed packages (scores 1–3) taken from human reproduction reports. Nothing is injected [P-page/S].
- **Economics coverage.** High: mostly economics and political science [S].

#### SocSci-Repro-Bench (Alizadeh, Mosleh, Gilardi, Tucker, 2026)
- **Identity.**
  - README citation: "Evaluating AI Coding Agents in Social Science Reproducibility" (2026) [P-page].
  - arXiv:2606.11447 is titled "AI Coding Agents Can Reproduce Social Science Findings", and the arXiv listing adds Atoosa Kasirzadeh as an author [S].
  - Repository: https://github.com/malizad/SocSci-Repro-Bench [P-page].
- **Capability measured.** Reading the original code, setting up the environment, executing the pipeline and reporting specific quantitative results [P-page].
- **Construction.**
  - 221 tasks from 54 papers, across four disciplines and twelve domains (one secondary summary says 13 domains) [P-page; S].
  - Papers are "either **fully reproducible** with available materials or **demonstrably non-reproducible** due to missing data". Gold answers "No Data" or "No Code or Data" test whether the agent recognizes an infeasible task [P-page].
  - Code is in R, Python or Stata, across political science, sociology, economics and psychology [P-page].
  - Reportedly, only tasks whose outputs matched across three independent manual runs were kept [S].
- **Licensing and contamination.**
  - Licensed CC BY 4.0. Anonymized materials are on Harvard Dataverse [P-page].
  - With non-anonymized materials, both agents reportedly scored 100%, which the authors flag as a contamination concern [S]. Results are also stratified by training cutoff [S].
- **Results.** From the README table [P-page], averaged over three runs:

  | Metric | Claude Code | Codex |
  |---|---|---|
  | Task-level accuracy | 93.4% | 62.1% |
  | Paper-level accuracy | 78.0% | 35.8% |

  - At paper level, Claude Code reproduced all Python papers, 75% of R papers and 71.4% of Stata papers. Many Stata failures were because Stata was not installed in the environment [S].
  - Another secondary summary gives 88.9% and 76.5% on an anonymized version; this conflicts with the README [S].
- **Other finding.** Subtle prompt framing can nudge agents toward confirmatory specification search [S].

### 2.2 Replication from the paper, without the authors' code

#### PaperBench (OpenAI, 2025)
- **Identity.** "PaperBench: Evaluating AI's Ability to Replicate AI Research", by Starace, Jaffe, Sherburn, Aung, Chan, Maksin, Dias, Mays, Kinsella, Thompson, Heidecke, Glaese and Patwardhan [P-page README citation]. ICML 2025; arXiv:2504.01848 [S]. Code: https://github.com/openai/preparedness/tree/main/project/paperbench; the README also points to `openai/frontier-evals` for the Git-LFS data [P-page].
- **Capability measured.** Replicating 20 ICML 2024 Spotlight and Oral papers from scratch. The run has three stages: the agent builds a codebase; the codebase is executed in a fresh GPU container; then it is graded [P-page].
- **Construction and expert role.**
  - Each paper has `rubric.json`, `addendum.md` ("information from the author that is helpful for replication"), an optional `judge.addendum.md` ("information from the author that is helpful for the judge") and `blacklist.txt` (sites the agent may not use, such as the original codebase) [P-page].
  - Rubrics are hierarchical, with 8,316 gradable leaves, and are "co-developed with the author(s) of each ICML paper" [S].
  - The sources I could read do not report how authors were compensated.
- **Verification.**
  - An LLM judge grades against the rubric. A separate JudgeEval checks judge accuracy [P-page]. The o3-mini SimpleJudge reaches F1 = 0.83 on JudgeEval at about $66 per paper [S].
  - A lighter "Code-Dev" variant grades only code-development requirements; the README calls it "less rigorous" [P-page].
- **Results.**
  - README leaderboard dated 2025-04-02 [P-page]:

    | Agent | Score |
    |---|---|
    | IterativeAgent o1-high, 36 h limit | 26.0 ± 0.3% |
    | BasicAgent claude-3.5-sonnet | 21.0 ± 0.8% |

  - Human ML PhDs reached 41.4% after 48 hours on a 3-paper subset [S]; other paper versions report different human and agent figures [S].
- **Economics coverage.** None.

#### ReplicationBench (Ye et al., 2025)
- **Identity.** "ReplicationBench: Can AI Agents Replicate Astrophysics Research Papers?", Christine Ye and co-authors. arXiv:2510.24591 (Oct 2025; v2 Nov 2025) [S]. I found no repository URL. A Harbor adapter is reported to cover 90 expert-reviewed numeric tasks [S].
- **Capability measured.** Replicating the core contributions of astrophysics papers: setup, derivations, data analysis and code [S].
- **Construction and expert role.**
  - Every task is "co-developed with the original paper authors". v1 has 107 tasks from 19 papers; v2 has 111 tasks from 20 papers [S].
  - A "ReplicationBench-Plus" adds 58 LLM-generated, expert-curated tasks from 11 further papers [S].
  - Domain experts reviewed agent trajectories to catalogue failure modes [S].
  - Compensation is not reported in the sources I could access.
- **Verification.** Numeric answers are compared to ground truth within **author-submitted tolerances**; code tasks use grading functions or unit tests [S].
- **Results.** The best model scored under 20% in v1 (Claude 3.7 Sonnet, 19.3%) and 22% in a later version (Claude Sonnet 4.5) [S].
- **Economics coverage.** None.

#### SciReplicate-Bench (Xiang et al., 2025)
- **Identity.** COLM 2025 [P-page README]; arXiv:2504.00255 [S]. Repository: https://github.com/xyzCS/SciReplicate-Bench [P-page].
- **Construction.** 100 tasks from 36 NLP papers published in 2024; the recent window is meant to limit leakage [S].
- **Verification.** Execution accuracy, CodeBLEU and "reasoning graph accuracy". The repository contains `Evaluation.py` and `Reason_Process_ACC.py` [P-page].
- **Results.** The best configuration reached 39% execution accuracy [S].
- **Running requirements.** Running all reference code needs one A100 80 GB GPU, and the data is distributed through SharePoint links [P-page].
- **Economics coverage.** None.

#### LMR-Bench (2025)
- **Identity.** EMNLP 2025 (Anthology 2025.emnlp-main.314); arXiv:2506.17335 [S]. Repository: https://github.com/du-nlp-lab/LMR-Bench [P-page].
- **Task.** Given a paper and a repository with masked methods, write the missing code. There are 28 tasks from 23 NLP papers in nine categories, with per-project Dockerfiles [P-page].
- **Verification.** Annotated unit tests, an LLM judge and human evaluation [P-page].
- **Economics coverage.** None.

#### ResearchCodeBench (Hua et al., 2025)
- **Identity.** NeurIPS 2025 Datasets & Benchmarks track; arXiv:2506.02314 [S].
- **Construction.** 212 coding challenges from 20 machine-learning papers from 2024–25. Snippets are removed from the original repositories and checked with unit tests [S]. The benchmark is designed for community expansion [S].
- **Results.** The best model, Gemini-2.5-Pro-Preview, scored 37.3% [S].
- **Economics coverage.** None.

#### AutoReproduce and ReproduceBench (Zhao et al., 2025/26)
- **Identity.** README title: "AutoReproduce … (ACL26 Main)" [P-page]; arXiv:2505.20662 [S]. Repository: https://github.com/AI9Stars/AutoReproduce [P-page].
- **Construction.** ReproduceBench pairs datasets with "human-curated reference code". Scoring uses "align-score" at high, low and mixed levels [P-page]. It covers 13 papers [S].
- **Results.** On 89.74% of runs the code executed; the average performance gap to the official implementations is 22.1% or 30.13%, depending on the version [S].
- **Limitation.** The README says "The current code is just a demo" [P-page].
- **Economics coverage.** None.

#### EXP-Bench (Kon et al., 2025)
- **Identity.** Listed in the ICLR 2026 proceedings; arXiv:2505.24785 [S]. Repository: https://github.com/Just-Curieous/Curie/tree/main/benchmark/exp_bench [P-page].
- **Task.** From a research question and incomplete starter code, design, implement, run and analyze an experiment. There are 461 tasks from 51 papers [P-page] and 12,737 gradable subtasks [S].
- **Construction.** A semi-automated pipeline extracts the tasks, followed by "lightweight human verification" [S].
- **Verification.** An LLM judge, o3-mini by default [P-page].
- **Results.** Only 0.5% of experiments were complete and executable [S]. The README warns that evaluation can take "days, for a single LLM+Agent combination" [P-page].
- **Economics coverage.** None.

### 2.3 Scientific data analysis and research-and-development agents

#### ScienceAgentBench (Chen et al., 2024)
- **Identity.** ICLR 2025; arXiv:2410.05080 [S]. Repository: https://github.com/OSU-NLP-Group/ScienceAgentBench [P-page].
- **Construction and experts.** "we extract 102 tasks from 44 peer-reviewed publications in four disciplines and engage nine subject matter experts to validate them". Each task's target output is a self-contained Python program [P-page]. The four disciplines are bioinformatics, computational chemistry, geographical information science, and psychology and cognitive neuroscience [S].
- **Verification.** Evaluation programs check the outputs; GPT-4o judges visualizations; the best of three trajectories is scored [P-page].
- **Updates.** On 2026-04-30 the team released a "**verified version … to mitigate false negatives in evaluation**" [P-page].
- **Contamination and licensing.** Only task inputs are public on Hugging Face. The full benchmark is a password-protected zip with the request "Please DO NOT redistribute". Most tasks are licensed CC BY 4.0 [P-page]. Test datasets were modified to reduce reliance on memorization [S].
- **Results.** The best agent solved 32.4% of tasks, or 34.3% with expert-provided knowledge; o1-preview with self-debug reached 42.2% [S].
- **Economics coverage.** None; psychology is the closest field.

#### RE-Bench (METR, 2024)
- **Identity.** arXiv:2411.15114, Wijk et al. [P-page README citation]. Repository: https://github.com/METR/RE-Bench. It is now marked **"DEPRECATED"** [P-page].
- **Construction.** Seven open-ended ML engineering environments in the METR Task Standard format. Each task is scored by a continuous function, and the README lists the starting score and the official solution's score [P-page].
- **Expert role.** Experts served as baselines rather than authors: 71 eight-hour attempts by 61 experts, recruited through METR staff networks, METR hiring applicants and graduate-student outreach [S]. Compensation is not stated in the sources I could access.
- **Contamination.** Solutions are password-protected, and the README informally asks users to keep the tasks out of training data [P-page].
- **Results.** With a 2-hour budget the best agents scored about 4× the human experts; with 32 hours, humans scored about 2× the agents [S].
- **Error-related.** One task, "Fix Embedding", gives the agent "a corrupted model with permuted embeddings" to recover [P-page]. This is an engineering corruption, not a methodological error.
- **Economics coverage.** None.

#### LAB-Bench (FutureHouse, 2024)
- **Identity.** arXiv:2407.10362. Repository: https://github.com/Future-House/LAB-Bench [P-page].
- **Construction.** Multiple-choice questions in 8 categories and 30 subtasks, including LitQA2, DbQA, FigQA, TableQA, ProtocolQA ("troubleshooting biological protocols"), SeqQA and Cloning Scenarios [P-page].
- **Contamination.** About 80% of the set is public and **20% is held out privately** "to monitor for training contamination"; a canary string is included [P-page].
- **Verification.** Accuracy, precision and coverage on the multiple-choice answers [P-page].
- **Economics coverage.** None.

#### BixBench (FutureHouse with ScienceMachine, 2025)
- **Identity.** arXiv:2503.00096. Repository: https://github.com/Future-House/BixBench [P-page].
- **Construction.** v1.5 has "205 questions derived from 60 real-world, published Jupyter notebooks" [P-page]; v1 had 53 scenarios and 296 questions [S].
- **Verification.** "LLM-based graders for open-ended answer or exact match for MCQs" [P-page].
- **Results.** The best open-answer accuracy was about 17% in v1 and v2 and 21% in v3 [S].
- **Economics coverage.** None.

#### Other adjacent benchmarks
- **DiscoveryBench** (ICLR 2025; arXiv:2407.01725) [S]
  - 264 tasks extracted manually from 20+ papers in six domains; a secondary summary says these include sociology and economics.
  - Also 903 synthetic tasks.
  - The best system scores about 25%.
- **BLADE** (EMNLP 2024 Findings; arXiv:2408.09667) [S]
  - 12 datasets, with ground truth from independent expert analyses.
  - Peers validated alternative decisions, and the authors collected **negative examples of "unjustifiable" decisions**.
  - Agents are scored against the ground-truth analysis decisions.
- **Terminal-Bench-Science** (https://github.com/harbor-framework/terminal-bench-science) [P-page, clone at commit 9276073]
  - At that commit there are 83 `task.toml` files: earth sciences 10, engineering 11, life sciences 24, mathematical sciences 21, physical sciences 17.
  - The README says tasks "are authored and reviewed by domain experts across the life, physical, earth, mathematical, and engineering sciences". There is **no social-science or economics domain**.
  - Task names include `statistics/highdim-mediation-debiasing` and `medicine/ehr-error-detection`.

### 2.4 Institute for Replication (I4R) studies

#### Brodeur et al. (2026), "AI-assisted teams outperform AI-led teams but not human-only teams…", PNAS 123(22), e2524747123
- **Sources.** Reproducibility package: https://github.com/I4Replication/AI-Games. The pre-analysis plan was preregistered on OSF (https://osf.io/sz2g8/) on 2 May 2024 after a pilot at the University of Toronto [P-page]. Earlier versions: IZA DP 17645 (Jan 2025) and I4R DP 195 [S].
- **Design.**
  - Researchers were randomly assigned to human-only, AI-assisted (ChatGPT as a collaborator) and AI-led (ChatGPT with minimal human oversight) teams, to reproduce published results, detect coding errors and propose robustness checks [S]. The paper reports 288 researchers [S].
  - My count from the released data, applying the repository's cleaning filters [P-page]:
    - 103 teams: 33 human-only, 35 AI-assisted, 35 AI-led
    - events: Toronto 27, Sheffield 13, Ottawa 12, Virtual Europe 16, Virtual North America 12, Tilburg 9, Cornell 8, Bogotá 6
    - 12 papers
    - 58 teams worked in R and 45 in Stata
  - The 12 papers used in the games are [P-page; my match of the `Master` sheet against the 17-row `Papers` sheet]:
    - economics: REStud 2024, JPE 2022, four *Economic Journal* papers (2022–2024) and one *AEJ: Applied* paper (2021);
    - other social science: APSR 2021, two *Nature Human Behaviour* papers (2023), *Political Analysis* 2023 and *Psychological Science* 2024.
- **Results.** Reproduction rates were 94% for human-only teams, 91% for AI-assisted and 37% for AI-led. Human-only teams found significantly more major errors. AI-led teams found fewer errors of every kind, proposed weaker robustness checks and took longer [S]. My recomputation from the released data [P-page]:

  | Arm | Teams that reproduced |
  |---|---|
  | Human-only | 31/33 |
  | AI-assisted | 32/35 |
  | AI-led | 13/35 |
- **How errors were verified.** Teams' error reports were re-coded by the research team. The coding columns include "error - reevaluated", "1-major", "2-minor", "6-false positive", "3-pre-regression", "4-regression", "5-transcription/post-regression", "7-error known by I4R" and "8-caused by chatgpt coding" [P-page].
- **Raw tabulation of error codes.** My tabulation, which may differ from the paper's final coding [P-page]:

  | Arm | Major | Minor | False positive | Errors introduced by ChatGPT coding |
  |---|---|---|---|---|
  | Human-only | 56 | 33 | 24 | — |
  | AI-assisted | 26 | 49 | 9 | — |
  | AI-led | 8 | 24 | 37 | 14 |
- **Known-error catalogue.** The sheet "all known errors by paper" has 122 rows for 12 papers, 11 of them coded "not an error". Of the 122, 51 were "known before" the games (sources such as "I4Rreport") and 71 were "discovered during the games" [P-page]. **The errors occur naturally; none was planted.** Examples, quoted from the catalogue [P-page]:
  - "Education was entered as continuous in regression models, so the -3105 values become massive outliers and materially distort estimates"
  - "Individuals with missing income values are all categorized in the lowest income"
  - "unemployed dummy includes retired people"
  - "regression is missing weighting"
  - Several zero-imputation problems that "inflate correlations"
- **Assessment.** These entries are exactly the "substantive implementation errors" (failure mode 6) in the research lead's brief, observed in real economics and political-science packages.

#### Mass reproducibility
- **Working paper.** I4R DP 107, "Mass Reproducibility and Replicability: A New Hope" (2024) [S].
- **Published version.** "Reproducibility and robustness of economics and political science research", *Nature* 652, 151–156 (April 2026), DOI 10.1038/s41586-026-10251-x [S].
- **Results** [S]:
  - 110 articles, of which the working paper gives 79 in economics and 31 in political science.
  - More than 85% of results were computationally reproducible.
  - About 72% of statistically significant estimates stayed significant with the same sign under re-analysis.
  - Teams with more experience found *lower* robustness.
  - The authors note the sample was not representative.

#### "Replication Engine"
- A proposal by Brodeur and Barbarioli at the Institute for Progress (2025) for automated agents that check code execution and look for coding and data errors at publication (https://ifp.org/wp-content/uploads/The-Replication-Engine-Brodeur-Barbarioli.pdf) [S].
- An I4R blog post from February 2026 reports first model comparisons. Preliminary results are slated for NeurIPS 2026, and I4R has applied for a SSHRC grant of $95,000 (https://www.i4replication.org/blog/the-ai-replication-engine-first-experiments-and-whats-next) [S].

### 2.5 Economics- and social-science-specific work, 2025–2026

#### ReplicatorBench (Center for Open Science and partners, 2026)
- **Identity.** arXiv:2602.11354 (11 Feb 2026). The README says "to appear in KDD 2026 AI4Sciences track" [P-page]. KDD '26 pages 11693–11704, DOI 10.1145/3770855.3819003 [S]. Repository: https://github.com/CenterForOpenScience/llm-benchmarking (Apache 2.0) [P-page].
- **Funding.** "funded by Coefficient Giving as part of its 'Benchmarking LLM Agents on Consequential Real-World Tasks' program" [P-page].
- **Capability measured.** *Replication* of claims, often with new data, in the order Extract → Design (preregistration) → Execute → Interpret [P-page].
- **Findings** [S]:
  - Agents can design and execute analyses but struggle to retrieve the new data needed.
  - Both replicable and non-replicable claims are included.
  - There are about 1,568 gradable checkpoints.
- **Construction.**
  - Each study folder holds `original_paper.pdf`, `initial_details.txt` (the claim and hypothesis), `replication_data/` (`.csv`, `.dta`, `.R`, `.do`, …), a human preregistration, a human replication report, and one or more `expected_post_registration*.json` files, which are "expert-annotated ground truth" and allow alternative acceptable variants [P-page].
  - The ground truth comes from SCORE human replications [S].
  - The repository has 39 numbered study folders (only some contain evaluation outputs) [P-page]. The arXiv v1 abstract reports 19 instances [S], while the ODU-hosted KDD PDF, as summarized by search, reports 39 instances with economics the largest group at 10 [S]. **This discrepancy is unresolved.**
  - Folder titles that look like economics papers (my classification, from titles only) include "Price Subsidies, Diagnostic Tests, and Targeting of Malaria Treatment…", "Caste as an Impediment to Trade", "Demographics and Entrepreneurship", "Promotions and Incentives: The Case of Multistage Elimination Tournaments" and "Uniform price auctions and fixed price offerings in IPOs: an experimental comparison" [P-page for the titles].
- **Verification.** "An **LLM-as-judge** system that benchmarks agent performance against expert-annotated ground truths" (GPT-4o for the extraction stage) [P-page].
- **Robustness module (in development).** The `robustness/` directory pairs papers with **Multi100 human peer evaluations** (file `multi100_peer-eval-not-reviewed_processed_data.csv`) [P-page]. Its directory names indicate economics papers among them, such as `Hendricks_QuartJournEco_2018`, `McDevitt_JournPoliEco_2014` and `Anderson_AmEcoJourn_2011`. Evaluators rated each analysis on:
  - whether the pipeline is acceptable (on a quality scale)
  - whether the conclusion follows from the results
  - whether there are code mismatches
- **Note on licensing.** The repository redistributes the original papers as PDFs [P-page].

#### Other 2025–2026 economics and social-science work

| Work | Identity and status | What it reports | Label |
|---|---|---|---|
| "Read the Paper, Write the Code: Agentic Reproduction of Social-Science Results" | Kohler, Zollikofer, Einsiedler, Hoyle, Ash. arXiv:2604.21965 (Apr 2026) | Agents get structured methods descriptions under strict isolation and never see the original code, results or paper. 48 papers from the I4R corpus previously verified as reproducible; 54% use Stata. The top three agents match the sign of the original coefficient in >85% of cases. The dominant cause of failure is underspecified methods reporting. Economics papers were reproduced less accurately than political-science papers. | [S] |
| "LLM-Assisted Replication for Quantitative Social Science" | Kubota et al. arXiv:2602.18453 (Feb 2026) | An LLM workflow; the case study is Bryson (1996). | [S] |
| "An LLM Workflow That Reproduces, Improves, and Extends Published Economics Research" | Schwartz, Andrews, Shapiro. NBER WP 35782 (Sept 2026), https://www.nber.org/papers/w35782 | Applied to 4,452 replication packages from five economics journals. Flags *possible* discrepancies in 3,460, speeds a calculation up more than 10× in 496, and produces an "aligned extension" in 923. Flags are not confirmed errors, though the authors report an LLM evaluation of a sample. Built with **BootLoops** (Schwartz; MIT licence; Anthropic-funded; released Oct 2026), which also ported Stata and MATLAB code to open source. Points to github.com/MetaEconomics for release. | [S] |
| "Scaling Reproducibility: An AI-Assisted Workflow for Large-Scale Replication and Reanalysis" | Yiqing Xu and Leo Yang Yang. arXiv:2602.16733 (Feb/Mar 2026); companion site reproai.org | Researchers write fixed diagnostic templates and AI executes them. Covers 384 studies and 3,382 models. An earlier evaluation focused on instrumental-variables designs reached 87% end-to-end success on 92 papers. | [S] |
| "An Agentic Approach Towards Replication Package Quality Evaluation" | Mbida and Angermeir. arXiv:2606.02006; ESEM 2026 | A "replication package linter" for software-engineering artifacts: 51 criteria, 5 packages, 75.4% agreement with a manual baseline. | [S] |
| "AI Agents and Prompt Engineering in Econometric Coding" | Galiani, López, Sosa. NBER WP 35588 (2026) | 40 econometric tasks in Stata, R and Python on simulated data, with the **method stated** and a reference output. Moving from chatbot to constrained agent raises success from 74% to 96% (NBER listing) or 79% to 97% (IDEAS listing). Agent runs cost 3.1–5.0× more. | [S] |
| "Can AI Master Econometrics?" (MetricsAI) | Chen et al. arXiv:2506.00856 (2025) | Tasks from published papers and PhD coursework. v2 reports "perfect replication" above 50% for coursework and 27% for published-paper tasks. | [S] |

#### Causal identification benchmarks (relevant to question (b))

| Benchmark | Identity | What it does and finds | Label |
|---|---|---|---|
| CausalReasoningBenchmark | Sawarni, Tan, Syrgkanis (Stanford). arXiv:2602.20571 (Feb 2026; v2 May 2026) | 173 queries over 138 datasets from 85 papers and 4 textbooks. The agent outputs a structured **identification specification** and a point estimate with **standard error**; the two are scored separately. Five design families: IV, RDD, DiD, conditional exogeneity, RCT. A third-party summary says models reach 84% on high-level strategy but 30% on complete specifications (unconfirmed). | [S] |
| CauSciBench | Acharya et al. ICML 2026 (PMLR v306) | 300+ queries from publications, QRData-CI and synthetic sources. "Selection of an appropriate causal inference method" is the key bottleneck, and models default to correlational methods. | [S] |
| CausalVerify | arXiv:2609.07944 (Sept 2026) | 259 contexts from real papers, 100 synthetic scenarios, and 23 paper–"synthetic twin" pairs. The agent's **design is committed and hashed before the data are revealed**. Its code is then executed and checked against a fixed canonical estimate. An **oracle arm** substitutes the reference design to separate design failures from execution failures. 15.5% of workflows that ran successfully still failed verification. | [S] |

#### Out of scope or tangential
- **Economic decision-making benchmarks** test agents as economic actors, not empirical research. They are EconEvals (arXiv:2503.18825), EconWebArena (2506.08136), EconGym (NeurIPS 2025), EcoGym (2602.09514) and EcoAgent-Bench (2608.05519) [S].
- **AI economics-research systems evaluated by LLM judges** [S]:
  - Project APE (Zurich Social Catalyst Lab) ranks AI-generated papers in a TrueSkill tournament judged by an LLM on dimensions including "identification strategy"; human papers win about 82.9% of matchups.
  - Related: "The Ideation Bottleneck" (2604.03338), HLER (2603.07444), and Zampa (HEID WP 14-2026).
- **Stata tooling.** MCP-for-Stata (formerly Stata-MCP, https://github.com/SepineTam/stata-mcp) lets agents run a local Stata installation "for regression analysis, econometrics, paper replication, and empirical research". It is licensed AGPL-3.0, with READMEs in several languages including Chinese [P-page]. I found no published benchmark or leaderboard for it [S].

### 2.6 Error-detection and error-injection benchmarks (relevant to question (a))

| Work | Errors are… | Domain | Key facts | Label |
|---|---|---|---|---|
| SPOT (arXiv:2505.11855, May 2025) | **Real**, confirmed by the original authors (errata and retractions from WithdrarXiv and PubPeer) | Several disciplines | 83 papers, 91 errors. o3 recall 21.1%, precision 6.1%. | [S] |
| FLAWS (arXiv:2511.21843, Nov 2025, CMU) | **Injected into paper text by LLMs** (Gemini 2.5 Pro, GPT-5) | Peer-reviewed papers | 713 paper–error pairs. GPT-5 has 39.1% identification accuracy at k=10. Authors plan to extend to economics. | [S] |
| PaperAudit-Bench (arXiv:2601.19916, Jan 2026; listed as EMNLP 2026 main 474) | **Synthetic, in text** | AI/ML | 220 papers with more than 10 errors each. | [S] |
| LimitGen (ACL 2025) | **Controlled flaws inserted** (Syn), plus real reviewer limitations (Human) | AI | GPT-4o found about half of the "very obvious" limitations. | [S] |
| "Hidden Pitfalls of AI Scientist Systems" (arXiv:2509.08713) | **Planted pitfall conditions** (benchmark selection, data leakage, metric misuse, post-hoc selection) | ML AI-scientist systems | An auditor working from the paper alone reached about 51%, rising to about 82% with logs and code. | [S] |
| Toda, "Can AI Refute Economic Theory?" (arXiv:2606.05383, Jun 2026) | **Known real errors** | Economic theory (4 papers) | No model found the errors without substantial human guidance. | [S] |
| Clinical-trial error seeding (medRxiv 2026) | **Seeded** methodological errors | RCT manuscripts | Major-error detection ranged from 53% to 96%. **Clean control reports were falsely flagged for 14–29% of error types.** | [S] |
| ICLR-2026 review audit (arXiv:2608.28626) | **Injected and verified detectable** | ML manuscripts | 145 errors across 55 manuscripts. Detection rose from 12.1% to 22.2% with a one-sentence verification instruction. Criticizes earlier injection studies for not checking that errors are detectable. | [S] |

### 2.7 Analytic flexibility and interpretation
- **"Many AI Analysts, One Dataset"** (Bertran, Fogliato, Wu; arXiv:2602.18710). Effect sizes and conclusions varied widely, and sometimes reversed, across models and prompts [S].
- **"The Agentic Garden of Forking Paths"** (arXiv:2607.01507). Agents given opposing prior-belief personas reached divergent conclusions, and many of those reports still passed methodological review [S].
- **"AI Coding Agents in Social Science: Methodologically Diverse, Empirically Consistent, Interpretively Vulnerable"** (Alizadeh, Gilardi, Mosleh, Kasneci; arXiv:2606.11456) [S]:
  - 20 runs each of Claude Code and Codex on a many-analysts immigration dataset.
  - Estimates stay close to the human consensus.
  - An explicit confirmatory prompt moved Claude Code's support verdicts **from 10% to 90%** while its coefficient distribution "barely changes".

### 2.8 Is "DeepEcon" already in use?
- **GitHub and PyPI.** `SepineTam/DeepEcon` describes itself as "DeepEcon：Your one-stop Python package for econometric algorithms". It is published on PyPI as `deepecon`, licensed MIT, has English and Chinese READMEs, and offers an `OLS` estimator [P-page]. A DeepWiki page describes its modular estimator framework [S]. The same maintainer, SepineTam, runs MCP-for-Stata [P-page].
- **deepecon.org.** An Econ-ARK material page on the Krusell–Smith deep-learning method points to "deepecon.org" for documentation of deep-learning methods. This appears linked to Maliar, Maliar and Winant (2021, *JME*), "Deep learning for solving dynamic economic models" [S]. I did not open deepecon.org, so its content is [U].
- **No other uses found.** I found no AI benchmark, model or company called "DeepEcon" [S; negative search result, not exhaustive].

---

## 3. Comparison table

Domain experts are rarely documented with recruitment or compensation details; "—" means I could not find the information in the sources I could access.

| Benchmark (year; venue) | Domain | Task type | Construction | Expert role | Verification | Error-based tasks? | Economics coverage | Evidence |
|---|---|---|---|---|---|---|---|---|
| CORE-Bench (2024; TMLR) | CS, social science, medicine | Re-run supplied code and data; answer questions | Curated from public code capsules; 270 tasks/90 papers | Benchmark authors | Numeric within 95% prediction interval; exact strings | No | Low: social science is mostly psychology and politics; R/Python only | P-page, S |
| SUPER (2024; EMNLP) | ML/NLP repositories | Set up and run repositories | 45 expert, 152 masked, 602 auto-generated | Expert solutions annotated | Gold answer plus landmarks | No | None | P-page, S |
| REPRO-Bench (2025; ACL Findings) | Social science (economics, political science) | Rate reproducibility 1–4 from paper and package | Mined from public reproduction reports (I4R etc.); 112 papers | Report authors, indirectly | Exact match to gold score | **Natural** errors, rating only | **High** | P-page, S |
| SocSci-Repro-Bench (2026; arXiv) | Political science, sociology, economics, psychology | Run original code; report numbers; recognize infeasible tasks | 221 tasks/54 papers; reproducible or non-reproducible because data are missing | Benchmark authors | Gold values; "No Data" controls | Negative controls only | Medium | P-page, S |
| I4R AI games (2026; PNAS); a randomized trial, not a benchmark | Economics, political science, psychology | Reproduce, find errors, propose robustness checks | 12 published papers; 103 teams | Human researchers; I4R coders adjudicate | Human adjudication against a known-error catalogue | **Natural** errors (51 known + 71 discovered) | **High** | P-page, S |
| PaperBench (2025; ICML) | ML | Replicate from scratch | 20 ICML 2024 papers; hierarchical rubrics | **Original authors** co-write rubrics and addenda | LLM judge, itself evaluated on JudgeEval | No | None | P-page, S |
| ReplicationBench (2025; arXiv) | Astrophysics | Replicate core results | Expert-written tasks, plus a set of LLM-generated, expert-curated tasks | **Original authors** co-develop tasks and set tolerances | Numeric tolerance; unit tests | No | None | S |
| SciReplicate-Bench (2025; COLM) | NLP | Implement an algorithm from the paper | 100 tasks/36 papers | — | Execution accuracy, CodeBLEU, reasoning graph | No | None | P-page, S |
| LMR-Bench (2025; EMNLP) | NLP | Fill in masked functions | 28 tasks/23 papers | Annotators wrote unit tests | Unit tests, LLM judge, humans | No | None | P-page, S |
| ResearchCodeBench (2025; NeurIPS D&B) | ML | Implement new code snippets | 212 challenges/20 papers | — | Unit tests | No | None | S |
| AutoReproduce/ReproduceBench (2025; ACL 2026) | AI | Reproduce experiments | 13 papers with human reference code | Curators | Alignment scores; performance gap | No | None | P-page, S |
| EXP-Bench (2025; ICLR 2026) | AI | Design, run and analyze experiments | Semi-automated extraction from 51 papers | Light human checks | LLM judge plus execution | No | None | P-page, S |
| ScienceAgentBench (2024; ICLR 2025) | Bioinformatics, chemistry, GIS, psychology | Write a data-analysis program | 102 tasks/44 publications | 9 experts validate | Evaluation scripts; LLM judge for figures; verified split (2026) | No | None | P-page, S |
| RE-Bench (2024; METR) | ML research and engineering | Open-ended optimization | 7 environments by METR | 61 human baselines | Continuous scores | One corrupted-model task | None | P-page, S |
| LAB-Bench (2024) | Biology | Multiple-choice subtasks | Authored questions; 20% held out privately | — | Multiple-choice accuracy | Protocol troubleshooting (details not verified) | None | P-page |
| BixBench (2025) | Bioinformatics | Analysis capsules, open or multiple-choice | 60 notebooks | Expert curation | LLM grader or exact match | No | None | P-page, S |
| ReplicatorBench (2026; KDD) | Social and behavioral sciences | Extract → design → execute → interpret, with new data | SCORE human replications; 19 or 39 instances | Human replicators' reports; annotators | **LLM judge** against expert JSON; checkpoints | Non-replicable claims included | **High** (economics the largest group, per [S]) | P-page, S |
| Kohler et al. (2026; arXiv) | Social science (I4R corpus) | Reimplement from methods text only | 48 verified papers | — | Coefficient and sign agreement | No | High | S |
| NBER WP 35782 (2026); a workflow, not a benchmark | Economics (5 journals) | Reproduce, check, improve, extend | 4,452 packages | — | Automated flags; LLM evaluation of a sample | Finds natural discrepancies (unconfirmed) | **High** | S |
| NBER WP 35588 (2026) | Econometrics | Code a named method on simulated data | 40 tasks | Economist authors | Reference outputs | No | High (methods only, not papers) | S |
| CausalReasoningBenchmark (2026) | Causal inference | Identification specification plus estimate and SE | 173 queries/85 papers + textbooks | — | Design and estimate scored separately | No | Partial | S |
| CauSciBench (ICML 2026) | Causal inference | End-to-end causal analysis | 300+ queries | — | — | No | Partial | S |
| CausalVerify (2026) | Quasi-experimental designs | Commit to a design, then execute | 259 real contexts plus synthetic twins | — | Canonical estimate; oracle arm | No (but separates design from execution failures) | Partial | S |
| SPOT / FLAWS / PaperAudit / LimitGen (2025–26) | Papers (mostly ML/AI) | Detect errors in paper **text** | Real (SPOT) or LLM-injected | Authors confirm errors (SPOT) | Recall and precision; automated metric | **Yes, in text, not in code** | None or planned | S |
| Terminal-Bench-Science (2026) | Natural, engineering and mathematical sciences | Expert-authored terminal tasks | Domain experts author and review | Expert authors | Programmatic verifiers | One task named "ehr-error-detection" | **None** | P-page |

---

## 4. Direct answers to questions (a), (b) and (c)

**(a) Does any existing benchmark use deliberately flawed replication packages or injected methodological errors?**
- **Not in executable replication packages, and not in economics, as far as my searches found.** This is a search-based finding, not an exhaustive survey.
- Error injection does exist in three other forms:
  - in the text of papers: FLAWS, PaperAudit-Bench, LimitGen-Syn, a clinical-trial seeding study and an ICLR audit [S];
  - as planted pitfalls for ML AI-scientist systems ("Hidden Pitfalls") [S];
  - as one engineering corruption task in RE-Bench [P-page].
- Social-science benchmarks use **naturally occurring** flaws instead:
  - REPRO-Bench's ordinal score derived from human reproduction reports [P-page];
  - I4R's catalogue of known errors, used to score human and AI teams [P-page];
  - SocSci-Repro-Bench's non-reproducible controls with missing data [P-page];
  - ReplicatorBench's non-replicable claims [S].
- BLADE comes closest at the level of individual decisions: it collects expert-labelled "unjustifiable" analysis decisions as negatives [S]. They are decision labels, not runnable packages.

**(b) Does any benchmark evaluate identification-strategy or statistical-inference judgment, beyond reproducing numbers?**
- **Yes, partially.** Mostly on curated causal-inference tasks rather than complete replication packages.
  - CausalReasoningBenchmark scores the identification specification separately from the estimate and standard error [S].
  - CauSciBench scores method selection end to end [S].
  - CausalVerify commits the design before the data are revealed and uses an oracle arm [S].
  - BLADE scores analysis decisions [S].
  - ReplicatorBench uses an LLM judge on the design and interpretation stages [P-page].
- **Human-judged precedents:**
  - The Multi100 peer evaluations in the COS robustness module ask whether the pipeline is acceptable and whether the conclusion follows from the results [P-page].
  - The I4R games include robustness-check quality, judged by humans [S].
- **Gaps:** I found no benchmark that grades choices about **inference** in published economics packages (clustering level, few-cluster corrections, inference with staggered treatment timing) as an executable outcome check.

**(c) Does any benchmark collect tacit expert knowledge from original authors?**
- **Partly, but not about mistakes.**
  - PaperBench ships author-written `addendum.md` and `judge.addendum.md` files and co-developed rubrics [P-page/S].
  - ReplicationBench co-develops tasks with original authors and uses tolerances the authors submit [S].
  - SPOT relies on authors confirming their own errors [S].
  - Toda (2026) uses his own knowledge of errors in four theory papers [S].
- **None elicits authors' knowledge of plausible mistakes, rejected alternatives or critical decisions** through a structured interview, or turns that knowledge into paired correct and flawed packages.

---

## 5. What DeepEcon would and would not add (assessment)

**Statement of the addition.** Each element below has precedents in isolation. As of 2026-11-05 I found no benchmark that combines them, especially elements 1 and 2 for empirical economics.
1. **Executable correct packages paired with expert-designed flawed packages** from published empirical economics papers.
2. **Each flaw is a realistic, scientifically consequential mistake** in identification, inference, sample construction, treatment timing or variable definition. Each comes with a documented consequence and with evidence that it is wrong rather than an alternative valid choice.
3. **The flaws are turned into outcome-verified tasks** for detecting errors, correcting them without changing the target estimand, and judging identification and inference. These are graded so that computational, statistical and identification validity are kept apart.
4. **The knowledge comes from original authors or expert replicators** through a structured, AI-guided interview.

**What DeepEcon would not add (overlaps to acknowledge explicitly):**
1. **Re-running economics or social-science packages when code and data are supplied.** CORE-Bench, REPRO-Bench, SocSci-Repro-Bench, the I4R games, NBER WP 35782 and Xu & Yang already cover this, and it is near saturation for frontier agents [P-page/S].
2. **Reimplementing from the paper without the original code.** PaperBench and ReplicationBench cover this outside social science, and Kohler et al. covers it for 48 social-science papers [S].
3. **Using original authors to define ground truth or tolerances.** PaperBench and ReplicationBench already do this [P-page/S].
4. **Error injection as a technique.** FLAWS, PaperAudit, LimitGen and mutation testing establish it. DeepEcon's novelty lies in *where* errors are injected (executable economics packages) and *who* designs them (domain experts), not in injection itself.
5. **Separating identification from estimation, or design from execution.** CausalReasoningBenchmark and CausalVerify already do this on curated causal tasks.
6. **Testing econometric coding when the method is specified.** NBER WP 35588 and MetricsAI already cover this.
7. **Evaluating analytic flexibility and how vulnerable interpretation is.** The many-analysts studies, Alizadeh et al. (2606.11456) and BLADE cover this.
8. **Using natural errors with human adjudication.** The I4R games, REPRO-Bench and SPOT already do this.

**The window for novelty may be short.**
- FLAWS plans to extend to economics [S].
- I4R's Replication Engine includes an agent that looks for coding errors [S].
- COS is building a robustness module on Multi100 evaluations [P-page].
- The NBER WP 35782 workflow already flags discrepancies at scale [S].

---

## 6. Implications for DeepEcon (assessment, not decisions)

1. **Narrow the novelty claim, cite the closest precedents, and place DeepEcon relative to them.** The precedents to name are the I4R games, REPRO-Bench, ReplicatorBench, SocSci-Repro-Bench, PaperBench's author addenda, CausalVerify and CausalReasoningBenchmark. Claiming novelty for "AI reproduction of economics papers" would be wrong.
2. **Do not make plain reproduction a main task type.** Frontier agents score above 90% on social-science reproduction tasks when code and data are supplied. At most, keep a few "research execution" tasks as a floor or calibration set. This matches Bercovich's "hard for interesting reasons" criterion (reading notes §3).
3. **The paired correct/flawed design gives negative controls for free.** That matters because error-detection systems raise false alarms: in the clinical-trial study, clean reports were flagged for 14–29% of error types [S]. DeepEcon should score detection tasks on both kinds of package, so that agents that flag everything are penalized.
4. **Check that every injected error can be detected.** The ICLR-audit critique [S] and Bercovich's solvability criterion (reading notes §5) both require evidence that a competent agent could find the error from the information available. This corresponds to item 9 of the research lead's error template ("a procedure for detecting or verifying the mistake").
5. **Use natural errors as well as designed ones.** The I4R known-error catalogue (122 entries, coded major or minor and by pipeline stage) shows that consequential errors occur in real Top-5 and field-journal packages [P-page]. Partnering with I4R could provide realistic errors that already meet the brief's safeguard G (real errors rather than artificial mutations). Licensing and authors' consent are open questions.
6. **Reuse CausalVerify's patterns.**
   - Committing to a design before the data are revealed directly tests the "estimator–implementation mismatch" failure mode in the brief.
   - The oracle arm is the same idea as Bercovich's "over-specification fairness check".
7. **Plan for verifier false negatives from the start.** CORE-Bench had to be re-graded by hand, and ScienceAgentBench released a "verified" split, because correct alternative techniques were rejected [S/P-page]. DeepEcon's verifiers should list acceptable alternative implementations and widen as agents reveal legitimate approaches (Bercovich §7). Each release should be audited by hand on a sample.
8. **Keep LLM judges to the reasoning and interpretation tasks, and test the judge itself.** PaperBench's JudgeEval (F1 0.83) shows how to do this [S]. The many existing LLM-judged benchmarks are not evidence that judges are reliable for economics identification arguments.
9. **Contamination cannot be solved by keeping the original materials secret, because they are public.** Two options:
   - grade software that the agent writes, run on hidden perturbed datasets or "synthetic twins" (as in CausalVerify and reading-notes implication 2);
   - keep the flawed packages and verifiers private.

   SocSci-Repro-Bench's reported 100% score on non-anonymized materials [S] is the warning. The NBER WP 35782 corpus of LLM-processed packages may also become training data.
10. **Treat Stata as a robustness risk.** Agents' worse performance on Stata partly reflects environment gaps, such as Stata not being installed [S]. A licensed Stata image cannot be redistributed. DeepEcon must decide whether evaluation environments include Stata, use R or Python equivalents (as BootLoops ported code [S]), or allow both. Ports must then be checked for numerical equivalence.
11. **Interpretation tasks are worth including in the first release, and need careful framing.** Prompt framing can flip verdicts while estimates stay the same [S]. Agent-facing instructions must therefore be neutral, and graders should check claims against what the design supports. This is the brief's failure mode 5.
12. **Contributor workflow.** No benchmark found documents how domain experts are recruited or paid in enough detail to copy. Coefficient Giving's "Benchmarking LLM Agents on Consequential Real-World Tasks" programme, which funds ReplicatorBench [P-page], is a possible source of funding.
13. **The name needs a decision.** "DeepEcon" collides with an existing econometrics package in the same Chinese-speaking empirical-economics and AI-tools community that this bilingual project targets [P-page]. Check trademarks and consider a more distinctive name before any public launch.

---

## 7. Open questions

1. Can DeepEcon access I4R's known-error catalogue and reports, or COS/SCORE data, under licences that allow redistribution as benchmark tasks? What consent would original authors need to give?
2. What standard of evidence will show that a designed flaw is an error and not a defensible alternative (Bercovich §9)? Who adjudicates?
3. Should agent-facing tasks require Stata, allow any language, or provide verified R or Python ports? What is the licence and robustness cost of each?
4. What is ReplicatorBench's actual instance count (19 or 39) and its economics share? How well does its LLM judge agree with humans? Both need the full KDD paper.
5. Will NBER WP 35782 publish its discrepancy flags? If so, they could be a source of candidate natural errors, but also a contamination path for any DeepEcon task built on the same papers.
6. How should false positives be scored in error-detection tasks, for example precision-weighted scoring or penalties for flagging clean packages?
7. Should error-correction tasks be graded only by outcome (re-running on hidden data variants), and how can DeepEcon guarantee that "preserving the target estimand" can be checked by a program?
8. Did PaperBench and ReplicationBench pay original authors, and how much author time did each task take? The answer is needed to plan the effort of Path B ("contributing one's own paper").
9. Where exactly do the CausalReasoningBenchmark and CausalVerify task sets overlap with economics designs? Could they serve as external validation, or as a baseline for DeepEcon's identification-reasoning tasks?

---

## 8. Access problems

- **arxiv.org and export.arxiv.org.** Blocked: CONNECT returns 403, as recorded in the proxy status. No arXiv full text could be read.
- **WebFetch failures (ENOTFOUND, host outside the session's allowed network):**
  - docs.iza.org (IZA DP 17645 PDF)
  - econpapers.repec.org
  - nomadit.co.uk (Metascience 2025 abstract)
  - micahaltman.com
  - www.cs.odu.edu (the ReplicatorBench KDD PDF)
  - www.cos.io (the ReplicatorBench blog post)
- **curl with no connection (status 000):**
  - aclanthology.org, openreview.net, proceedings.neurips.cc, huggingface.co (so the REPRO-Bench, SUPER and BixBench datasets could not be inspected)
  - i4replication.org, www.pnas.org, www.nber.org, osf.io, www.semanticscholar.org, hal.science
  - malizad.github.io (the SocSci-Repro-Bench paper PDF)
- **Reachability probe denied.** A broader probe of other hosts (other github.io pages, storage.googleapis.com and similar) was denied by the session's permission classifier. Those hosts were therefore not tested. I did not attempt workarounds.
- **What did work.** raw.githubusercontent.com and `git clone --depth 1` from github.com. Repository content is the basis of every [P-page] label.
- **Consequence.** Every paper-level number in this note is [S] unless it came from a repository. Before citing any [S] number in a collaborator-facing document, check it against the PDF.

---

## 9. Sources

All accessed 2026-11-05. "raw" means the README or file was read via raw.githubusercontent.com; "clone" means files were read from a shallow clone.

**Repositories and other primary material**
- CORE-Bench: https://github.com/siegelz/core-bench (raw README; clone: `benchmark/evaluations.py`, `benchmark/dataset/core_train.json`)
- REPRO-Bench: https://github.com/uiuc-kang-lab/REPRO-Bench (raw README; clone: `SWE-agent/config/reproduce.yaml`, `SWE-agent/evaluation.py`)
- PaperBench: https://github.com/openai/preparedness/tree/main/project/paperbench (raw README)
- SciReplicate-Bench: https://github.com/xyzCS/SciReplicate-Bench (raw README)
- LMR-Bench: https://github.com/du-nlp-lab/LMR-Bench (raw README)
- AutoReproduce: https://github.com/AI9Stars/AutoReproduce (raw README)
- EXP-Bench: https://github.com/Just-Curieous/Curie/tree/main/benchmark/exp_bench (raw README)
- SUPER: https://github.com/allenai/super-benchmark (raw README)
- ScienceAgentBench: https://github.com/OSU-NLP-Group/ScienceAgentBench (raw README)
- RE-Bench: https://github.com/METR/RE-Bench (raw README)
- LAB-Bench: https://github.com/Future-House/LAB-Bench (raw README)
- BixBench: https://github.com/Future-House/BixBench (raw README)
- ReplicatorBench / COS LLM Benchmarking: https://github.com/CenterForOpenScience/llm-benchmarking (raw READMEs; clone: `replicatorbench/data/original/*`, `replicatorbench/validator/README.md`, `robustness/data/*`)
- SocSci-Repro-Bench: https://github.com/malizad/SocSci-Repro-Bench (raw README)
- I4R AI Games (PNAS 2026 reproducibility package): https://github.com/I4Replication/AI-Games (raw README; clone: `code/cleaning.R`, `data/AI games.xlsx`)
- Terminal-Bench-Science: https://github.com/harbor-framework/terminal-bench-science (existing scratchpad clone, commit 9276073)
- DeepEcon package: https://github.com/SepineTam/DeepEcon (raw README)
- MCP-for-Stata / Stata-MCP: https://github.com/SepineTam/stata-mcp (raw README)
- Project reading notes: `docs/research/reading-notes/good-benchmarks-bercovich-2026.md`

**Secondary sources: search-engine summaries of these pages, which I did not open myself**
- CORE-Bench: https://arxiv.org/abs/2409.11363 ; https://mlanthology.org/tmlr/2024/siegel2024tmlr-corebench ; https://hal.cs.princeton.edu/corebench_hard ; https://substack.com/@sayash/note/c-183913356
- REPRO-Bench: https://arxiv.org/abs/2507.18901 ; https://aclanthology.org/2025.findings-acl.1210 ; https://www.emergentmind.com/topics/repro-bench
- PaperBench: https://arxiv.org/abs/2504.01848 ; https://mlanthology.org/icml/2025/starace2025icml-paperbench ; https://cdn.openai.com/papers/22265bac-3191-44e5-b057-7aaacd8e90cd/paperbench.pdf
- ReplicationBench: https://arxiv.org/abs/2510.24591 ; https://astrobiology.com/2025/10/31/replicationbench-can-ai-agents-replicate-astrophysics-research-papers/ ; https://arxiv.org/pdf/2609.04298 (Harbor adapters)
- SciReplicate-Bench: https://arxiv.org/abs/2504.00255
- LMR-Bench: https://arxiv.org/abs/2506.17335 ; https://aclanthology.org/anthology-files/pdf/emnlp/2025.emnlp-main.314.pdf
- AutoReproduce: https://arxiv.org/abs/2505.20662
- EXP-Bench: https://arxiv.org/abs/2505.24785 ; https://proceedings.iclr.cc/paper_files/paper/2026/hash/c411f5b2d9c55f1685e72db224ad8b0e-Abstract-Conference.html
- ResearchCodeBench: https://arxiv.org/abs/2506.02314 ; https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd0d0a873cc3e601c76f46dccc3d4c5f-Abstract-Datasets_and_Benchmarks_Track.html
- SUPER: https://arxiv.org/abs/2409.07440 ; https://aclanthology.org/2024.emnlp-main.702.pdf
- ScienceAgentBench: https://arxiv.org/abs/2410.05080 ; https://mlanthology.org/iclr/2025/chen2025iclr-scienceagentbench
- RE-Bench: https://arxiv.org/abs/2411.15114
- BixBench: https://arxiv.org/abs/2503.00096
- I4R and Brodeur et al.:
  - https://doi.org/10.1073/pnas.2524747123
  - https://www.rff.org/publications/journal-articles/ai-assisted-teams-outperform-ai-led-teams-but-not-human-only-teams-in-assessing-research-reproducibility-in-quantitative-social-science/
  - https://docs.iza.org/dp17645.pdf (not reachable)
  - https://ideas.repec.org/p/zbw/i4rdps/107.html
  - https://eprints.lancs.ac.uk/id/eprint/236673/
  - https://emiguel.econ.berkeley.edu/research/reproducibility-and-robustness-of-economics-and-political-science-research/
  - https://ifp.org/wp-content/uploads/The-Replication-Engine-Brodeur-Barbarioli.pdf
  - https://www.i4replication.org/blog/the-ai-replication-engine-first-experiments-and-whats-next
- ReplicatorBench: https://arxiv.org/abs/2602.11354 ; https://www.cs.odu.edu/~jwu/downloads/pubs/soos-2026-kdd/soos-2026-kdd.pdf ; https://www.cos.io/blog/benchmarking-llm-agents-on-scientific-tasks-introducing-replicatorbench
- SocSci-Repro-Bench and companion paper: https://arxiv.org/abs/2606.11447 ; https://www.themoonlight.io/en/review/ai-coding-agents-can-reproduce-social-science-findings ; https://arxiv.org/abs/2606.11456 ; https://papers.cool/arxiv/2606.11456
- Kohler et al.: https://arxiv.org/abs/2604.21965 ; https://elliottash.com/papers/Kohler-Zollikofer-Einsiedler-Hoyle-Ash-Read-Paper-Write-Code-Agentic-Reproduction-Social-Science-Results.pdf
- Kubota et al.: https://arxiv.org/abs/2602.18453
- NBER WP 35782 and BootLoops: https://www.nber.org/papers/w35782 ; https://economics.mit.edu/sites/default/files/2026-09/metascience.pdf ; https://www.unite.ai/schwartz-releases-bootloops-1-0-an-open-source-llm-harness-for-science/ ; https://the-decoder.com/open-source-bootloops-harness-supports-ai-models-in-performing-precise-scientific-calculations/
- Xu & Yang: https://arxiv.org/abs/2602.16733
- Mbida & Angermeir: https://arxiv.org/abs/2606.02006 ; https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESEM.2026.58
- NBER WP 35588 (Galiani et al.): https://www.nber.org/papers/w35588 ; https://cepr.org/voxeu/columns/letting-ai-agents-write-econometric-code
- MetricsAI: https://arxiv.org/abs/2506.00856
- CausalReasoningBenchmark: https://arxiv.org/abs/2602.20571
- CauSciBench: https://proceedings.mlr.press/v306/acharya26a.html
- CausalVerify: https://arxiv.org/pdf/2609.07944
- BLADE: https://arxiv.org/abs/2408.09667
- DiscoveryBench: https://arxiv.org/abs/2407.01725
- Error detection and injection:
  - SPOT: https://arxiv.org/abs/2505.11855
  - FLAWS: https://arxiv.org/abs/2511.21843
  - PaperAudit-Bench: https://arxiv.org/abs/2601.19916 ; https://aclanthology.org/2026.emnlp-main.474/
  - LimitGen: https://aclanthology.org/2025.acl-long.1009
  - Hidden Pitfalls: https://arxiv.org/abs/2509.08713
  - Toda: https://arxiv.org/abs/2606.05383 ; https://marginalrevolution.com/marginalrevolution/2026/06/how-well-does-current-ai-find-errors-in-economics-papers.html
  - Clinical trials: https://www.medrxiv.org/content/10.64898/2026.10.25.26366455v2
  - ICLR audit: https://arxiv.org/abs/2608.28626
- Analytic flexibility: https://arxiv.org/abs/2602.18710 ; https://arxiv.org/pdf/2607.01507
- Economic decision benchmarks (out of scope): https://arxiv.org/abs/2503.18825 ; https://arxiv.org/pdf/2506.08136 ; https://arxiv.org/pdf/2506.12110 ; https://arxiv.org/html/2602.09514v1 ; https://arxiv.org/abs/2608.05519
- AI economics-research systems: https://bhanneke.github.io/RISE/projects/ape/ ; https://arxiv.org/pdf/2604.03338 ; https://arxiv.org/pdf/2603.07444 ; https://repec.graduateinstitute.ch/pdfs/Working_papers/HEIDWP14-2026.pdf
- DeepEcon name: https://pypi.org/project/deepecon/ ; https://deepwiki.com/SepineTam/DeepEcon ; https://deploy-preview-74--econark-website.netlify.app/materials/deep-learning-euler-method-krusell-smith ; https://web.stanford.edu/%7Emaliars/Files/JME2021.pdf
