# R10: Training contamination versus evaluation-time leakage in established benchmarks

| Field | Value |
|---|---|
| Topic | How established benchmarks separate public and held-out material, protect answer keys, and isolate the evaluation environment; what this implies for DeepEcon |
| Date | 2026-11-06. Searches run 2026-11-06. |
| Author | lead collaborator (Claude session), answering the research lead's question of 2026-11-06 on training use and evaluation isolation |
| Evidence labels | As in the [evidence README](README.md). Every new claim here is **[S]**: it comes from search-engine summaries, because the primary pages (arxiv.org, arcprize.org, labs.scale.com) are outside this session's network allowlist. Claims carried over from R1, R4, R6 and R8 keep their original labels. Text marked *(assessment)* is analysis, not a sourced fact. |
| Relation to other notes | Extends [R1](R1-terminal-bench-science.md) §1.6 (TBS internet policy) and [R4](R4-replication-benchmarks.md) implication 9 (contamination and public originals). Supported D-032 (adopted from P-051 on 2026-11-06; replaced on 2026-11-07 by D-035 and D-038) and proposals P-052 (adopted as D-036) and P-053 in the [decision log](../../decisions/decision-log.md); §4 adds small-server price anchors to those in [R9](R9-hosted-stack-and-compliance.md) §7. |

---

## 1. Two different failure modes

*(assessment)*

| | Evaluation-time leakage | Training contamination |
|---|---|---|
| What happens | The agent **reaches** the answer while working: answer files in its container, the internet, version-control history, the grader | The model **already knows** the answer because the task and its answer were in its training data |
| Fixed by isolating the evaluation environment? | Yes | **No.** The knowledge is in the weights and enters the sandbox with the model |
| Established remedies | Separate agent and grader environments; no answers in the agent image; network rules; trajectory audits | Canary strings; a private held-out split for comparison; dating tasks against model training cutoffs; refreshing tasks; no-retention agreements with providers |

## 2. What established benchmarks do

| Benchmark | Public material | Held-out or protected material | Evaluation-time controls | Label |
|---|---|---|---|---|
| Terminal-Bench-Science | Everything, answer keys included, on public GitHub and Hugging Face, with a canary GUID | None | Tests and solutions never enter the agent image; separate verifier container with no public network; the agent phase has open internet, so protection there rests on a "do not cheat" instruction and a post-hoc LLM audit | [P-full, R1] |
| BIG-bench and Harbor | Canary GUID | — | — | [P-page, R6]; a canary works only if corpus builders filter on it |
| LAB-Bench | About 80% | About 20% held out privately "to monitor for training contamination"; canary | — | [P-page, R4] |
| ScienceAgentBench, RE-Bench, CORE-Bench | Task inputs | Password-protected or GPG-encrypted answers (CORE-Bench prints the password in its README: protection against crawlers, not people) | — | [P-page, R4] |
| Humanity's Last Exam | Public question set | A private held-out set used to measure overfitting to the public set; scores on it are not published | — | [S] |
| ARC-AGI (ARC Prize) | Public evaluation set | **Semi-private** set: run through commercial APIs, so treated as partly exposed; confidentiality agreements with providers that no data are retained; only new high-score claims verified. **Private** set: never sent to APIs; run only offline (Kaggle, no internet) | Overfitting flagged when public and semi-private scores differ by more than 10 percentage points | [S] |
| SWE-Bench Pro | Public set from copyleft repositories | A held-out set (kept private as a control) and a commercial set from private codebases (only results released) | — | [S] |
| LiveCodeBench | Everything | None; instead each problem carries its release date, and a model is scored only on problems released after its training cutoff. Scores of several models fell for problems released after their cutoffs | — | [S] |
| FrontierMath | — | The funder had access to most problems and solutions; a holdout set was withheld from it. The arrangement was disclosed late and criticized, and the lab could not independently verify the funder's reported score | — | [S] |
| PaperBench | Papers and rubrics | — | The agent has internet access, but a per-paper blacklist forbids the authors' original code (and, in some descriptions, online replications) | [S] |
| SWE-bench Verified | Everything | — | Agents were reported to read **future commits** through `git log --all`, which revealed the fixes; a later variant rebuilt repositories without future commits and hid test files | [S] |
| SocSci-Repro-Bench | — | — | Both agents reportedly scored 100% on non-anonymized materials | [S, R4] |

## 3. What this implies for DeepEcon

*(assessment)*

1. **Isolation is necessary but not sufficient.** It stops an agent from *looking up* answers. It cannot stop a model that *trained* on them. No benchmark in §2 relies on isolation alone; each that cares about contamination adds a held-out split, dating, or refreshes.
2. **Blanket secrecy is not the norm.** Terminal-Bench-Science publishes its answer keys; most benchmarks publish most material. Strict handling is reserved for a held-out portion. D-031 (all answer-key material local-only) is therefore stricter than common practice. (D-031 and D-032 were replaced on 2026-11-07 by D-035: exposure is logged and reported rather than prevented, because all models are evaluated through APIs, D-038.)
3. **DeepEcon has a special exposure.** The original replication packages are public. A flawed package plus the public original *is* the answer key (a diff), so evaluation-time internet access is more dangerous here than in TBS, and models may have memorized the originals. The restructured presentation (neutral names, as in V5) and an offline agent environment matter more than in most benchmarks.
4. **Evaluating a closed model exposes its task.** The provider receives the agent-facing package and the whole trajectory. ARC's "semi-private" tier names this honestly; a held-out tier must either stay with open-weight models run locally or rely on a no-retention agreement.
5. **Hidden channels need testing.** The SWE-bench case shows that leaks come from places nobody thought of (version-control history). An isolation check should try to find answers from inside the agent environment before release.

## 4. Small-server price anchors (for O-021)

Both from search summaries of third-party listings and an official pricing page whose table did not extract cleanly; check the provider's own page before any commitment.

| Provider | Size | Price | Label |
|---|---|---|---|
| Hetzner Cloud (CX22, possibly replaced by CX23 in 2026) | 2 vCPU, 4 GB RAM, 40 GB disk | About €3.79–4.59 a month before VAT; sources disagree after 2026 price changes | [S] |
| Alibaba Cloud Simple Application Server (regions include Hong Kong and Singapore) | Plans with 2 vCPU | Official tiers of about US$4.5, 9, 15, 19 and 35 a month; Hong Kong overage traffic US$0.153/GB | [S] |

*(assessment)* A server big enough for the contributor site costs roughly US$4–20 a month; object storage for backups costs about US$0.015–0.020 per GB-month ([R9](R9-hosted-stack-and-compliance.md) §7, [P-page]).

## 5. Search log

Searches (WebSearch, standard mode, 2026-11-06): Hetzner CX22 price; Alibaba Cloud Simple Application Server price; HLE private held-out set; ARC Prize semi-private and private sets; FrontierMath holdout; LiveCodeBench release dates; SWE-Bench Pro held-out and commercial subsets; PaperBench blacklist; SWE-bench Verified future-commit leak. Fetches of arxiv.org, arcprize.org and labs.scale.com failed (outside the network allowlist).
