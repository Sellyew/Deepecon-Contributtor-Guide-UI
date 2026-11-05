# Cost and Effort Model (shared assumptions for Options A and B)

| | |
|---|---|
| **Status** | **Proposed** v0.1.0 (2026-11-05). Planning estimates, **not quotes**. Calibrate with pilot measurements (Deliverable 8, PQ5). |
| **Reproducible** | [`cost-model/inference_model.py`](cost-model/inference_model.py) and [`cost-model/scenarios.py`](cost-model/scenarios.py) compute every number in §3–§5 from the assumptions below. |
| **Price sources** | Claude API list prices from Anthropic's API reference (cached 2026-10-06) [P-page]. Hosting, sandbox, and subscription prices: pending evidence notes [R9](../research/evidence/R9-hosted-stack-and-compliance.md) and [R3](../research/evidence/R3-access-pricing-policy-portability.md); marked [U] until then. |
| **Rule** | Engineering and human effort are given in **hours or engineer-weeks**, not dollars. Multiply by your institution's fully loaded rates; the model does not invent salaries. |

---

## 1. Shared assumptions

Both options are costed on the **same** assumptions. Any assumption that differs between them is listed explicitly in §4.

| ID | Assumption | Central | Range | Basis |
|---|---|---|---|---|
| A1 | Contributions (one paper each) | 10 / 50 / 200 | — | Brief §7 scenarios |
| A2 | Interview length, all sessions | ≈ 3 h | 2–5 h | Protocol stage estimates [U] |
| A3 | Interviewer turns per contribution | 100 | 60–160 | A2 at about 1.5–2 minutes per exchange [U] |
| A4 | Average cached context per turn (protocol, paper text, code subset, dossier, history) | 100k tokens | 60k–180k | 40-page paper as text ≈ 30k tokens; relevant code ≈ 25k; history grows to ≈ 60k [U] |
| A5 | Output per turn, including model thinking | 2k tokens | 1k–4k | Adaptive thinking at medium/high effort [U] |
| A6 | Agentic code work per contribution (reading code, drafting variants, runs) | 1.5M input / 150k output tokens | 0.5–4M / 50–400k | [U] |
| A7 | Prompt caching | 1-hour cache for interview turns; 5-minute for agentic loops | — | Human reply gaps of 1–10 minutes |
| A8 | Model | Claude Opus 5.5 | Sonnet 5.5 as a sensitivity case | Brief's stated preference |
| A9 | Admitted tasks per contribution | 1.0 | 0.5–1.5 | Many candidates fail review (*Good Benchmarks* §10) [U] |
| A10 | Shepherd hours per admitted task | 20 h | 10–40 h | *Good Benchmarks* §10 reports more than 40 h for hard tasks [P-full] |
| A11 | Independent-review hours per task (two reviewers) | 8 h | 4–12 h | [U] |
| A12 | Package size (code, documentation, outputs; data only if redistributable) | 50 MB | 5 MB – 2 GB | [U] |

## 2. Inference cost per contribution

Prices per million tokens (Anthropic first-party list prices, cached 2026-10-06) [P-page]: **Opus 5.5** input $4, output $20, cache read $0.20; **Sonnet 5.5** input $2, output $10, cache read $0.20. Cache writes cost 1.25× base input (5-minute) or 2× (1-hour). Batch processing costs 50% of standard (not applicable to live interviews).

| Model | Low | Central | High | High, no prompt caching |
|---|---|---|---|---|
| Opus 5.5 | **$6** | **$17** | **$46** | $159 |
| Sonnet 5.5 | $3 | $10 | $26 | $80 |

In the central case, output (about $7.80) and interview input (about $4.40) dominate; session restarts that rewrite the cache cost about $2.40 (`inference_model.py`).

**Interpretation.** Even the uncached worst case is small next to the human effort in §3. Caching discipline matters — it cuts costs by about 3× — but the model choice and the architecture choice change inference spending only by tens of dollars per contribution.

## 3. Scenario analysis (10 / 50 / 200 contributions)

Central estimates, with ranges in brackets.

| Contributions | Inference (Opus 5.5) | Shepherd hours | Independent-review hours | Support hours, Option A | Support hours, Option B |
|---|---|---|---|---|---|
| 10 | $170 [$61–462] | 200 [50–600] | 80 [20–180] | 5 [2–10] | 10 [5–20] |
| 50 | $851 [$307–2,310] | 1,000 [250–3,000] | 400 [100–900] | 25 [12–50] | 50 [25–100] |
| 200 | $3,404 [$1,230–9,240] | 4,000 [1,000–12,000] | 1,600 [400–3,600] | 100 [50–200] | 200 [100–400] |

Support assumptions [U]: 0.5 h per contributor for Option A (range 0.25–1) and 1 h for Option B (range 0.5–2), reflecting the heterogeneity of local environments. Both should be measured in the pilot.

**The decision-relevant result.** At 200 contributions, the central estimate is about **4,000 shepherd hours** (roughly two full-time-equivalent years) and **1,600 review hours**, against about **$3,400 of inference**. Human effort dominates under either architecture. The architecture choice mainly moves **engineering effort** (§4) and **who pays for inference** (§5), not the total cost of the benchmark.

## 4. Costs that differ between the options

| Category | Option A — hosted platform | Option B — local skill |
|---|---|---|
| **Initial development** (engineer-weeks, beyond the shared core of 9–16) | 11–18 (A1); +3–6 for a hosted sandbox (A2) | 7–12 |
| **Fixed operating costs** | Hosting (application, database, storage, e-mail, observability): tens to low hundreds of dollars per month at this scale [U: R9] | Static project page and upload endpoint: near zero to tens of dollars per month [U: R9] |
| **Variable cost per contribution, paid by the project** | Inference ≈ $17 (central); A2 sandbox time (small; e.g., Managed Agents charges $0.08 per session-hour plus tokens) | None by default; ≈ $17 if the project provides API access; subscription cost if the project reimburses plans |
| **Contributor-side costs** | Time; for A1, their own compute and Stata licence | Time; model access (own plan, or project-provided); own compute and licences |
| **Ongoing maintenance** | ≈ 0.1–0.25 FTE: deployments, security updates, monitoring, backups [U] | ≈ 0.05–0.15 FTE: plugin updates tracking client releases, cross-platform regression runs [U] |
| **Support load** | Lower per contributor (one environment), plus run-kit questions in A1 | Higher per contributor (installation and environment diversity) |
| **Security and compliance** | Project holds unpublished code and transcripts: security review, privacy notices, possibly data-protection agreements | Lighter for the project; the contributor's machine and account terms govern most data flows |

## 5. Who pays for inference — a policy choice, partly independent of architecture

| Mechanism | Works with | Project pays | Model consistency | Data-use terms |
|---|---|---|---|---|
| Project API account behind the platform | A | ≈ $17 per contribution | Enforced | Commercial terms for everyone |
| Contributor's own subscription | B | Nothing | Not enforced | Contributor's plan terms (consumer plans may allow training use if opted in) [U: R3] |
| Project reimburses subscriptions | B | One or more months of a plan per contributor [U: R3 prices] — may exceed direct API cost | Not enforced | As above |
| Project-issued API keys with spend caps | B | ≈ $17 per contribution | Recommended model, logged | Commercial terms |
| Project gateway (a small proxy issuing per-contributor tokens) | B | ≈ $17 per contribution, plus a small service to operate | Enforceable at the gateway | Commercial terms |
| Sponsor credits (as Terminal-Bench-Science uses) | A or B | Reduced | Depends | Depends |

**Note.** If Option B uses project-provided API access to secure consistency and commercial terms, its inference cost to the project becomes the same as Option A's, and the remaining cost differences are engineering, operations, and support.

## 6. Sensitivities — what would change these conclusions

- **Heavy hosted execution (A2) with large data:** sandbox compute could become material if packages require hours of CPU per run. Most target analyses should run in minutes (selection criterion).
- **A much more expensive model** (e.g., Claude Fable 5.1 at $10 / $50 per million tokens) raises inference about 2.5×. That is still small next to human effort.
- **Contributor count in the thousands:** inference reaches tens of thousands of dollars, but shepherding would then be the binding constraint long before.
- **Shepherd efficiency:** the largest lever. Halving shepherd hours per task (better interviews, better tooling, reusable verifier components) saves more than any architecture choice.
- **Contributor honoraria** (Open question O-005) could exceed every other per-contribution cost; they are architecture-neutral.

## 7. What the pilot must measure to replace these estimates

Interview duration and turns; tokens and list-price cost per session; agentic token use in operationalization; support minutes per contributor and per option; shepherd hours per admitted task and per stage; review hours; and the share of candidates that become admitted tasks.
