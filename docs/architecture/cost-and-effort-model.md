# Cost and Effort Model (shared assumptions for Options A and B)

| | |
|---|---|
| **Status** | **Proposed** v0.2.0 (2026-11-05). Planning estimates, **not quotes**. To be calibrated with pilot measurements (Deliverable 8, PQ5). |
| **Reproducible** | [`cost-model/inference_model.py`](cost-model/inference_model.py) and [`cost-model/scenarios.py`](cost-model/scenarios.py) compute every number in §2–§3 from the assumptions below. |
| **Price sources** | Claude API list prices from Anthropic's API reference (cached 2026-10-06), confirmed on the pricing page on 2026-11-05 ([R3](../research/evidence/R3-access-pricing-policy-portability.md)) [P-page]. Claude plan prices from the pricing page (R3) [P-full]. Hosting anchors from vendor pricing pages ([R9](../research/evidence/R9-hosted-stack-and-compliance.md)) [P-page]. |
| **Rule** | Engineering and human effort are stated in **hours or engineer-weeks**, not dollars. Convert with your institution's fully loaded rates; the model does not invent salaries. |

---

## 1. Shared assumptions

Both options are costed on the **same** assumptions. Where the options genuinely differ, §4 lists the difference explicitly.

| ID | Assumption | Central | Range | Basis |
|---|---|---|---|---|
| A1 | Contributions (one paper each) | 10 / 50 / 200 | — | Brief §7 scenarios |
| A2 | Interview length, all sessions | ≈ 3 h, in 3+ sessions of ≤ 60 min | 2–5 h | Protocol v0.2.0 [U] |
| A3 | Interviewer turns per contribution | 100 | 60–160 | [U] |
| A4 | Average cached context per turn (protocol, paper text, code subset, dossier, history) | 100k tokens | 60k–180k | 40-page paper as text ≈ 30k tokens; relevant code ≈ 25k; history grows to ≈ 60k [U] |
| A5 | Output per turn, including model thinking | 2k tokens | 1k–4k | [U] |
| A6 | Agentic code work per contribution | 1.5M input / 150k output tokens | 0.5–4M / 50–400k | [U] |
| A7 | Prompt caching | 1-hour cache for interview turns; 5-minute cache for agentic loops | — | Human reply gaps of 1–10 minutes |
| A8 | Model | Claude Opus 5.5 | Sonnet 5.5 as a sensitivity case | Brief's stated preference; Claude Code's default [P-page] |
| A9 | Admitted tasks per contribution | 1.0 | 0.5–1.5 | Many candidates fail review (*Good Benchmarks* §10) [U] |
| A10 | Shepherd hours per admitted task | 20 h | 10–40 h | *Good Benchmarks* §10 reports more than 40 h for hard tasks [P-full] |
| A11 | Independent-review hours per task (two reviewers, plus status classification) | 8 h | 4–12 h | [U] |
| A12 | Package size | 40 MB median | heavy tail: ≈ 20% of AEA packages exceed 2 GB | AEA Data Editor 2024 report window [P-full, R8] |

## 2. Inference cost per contribution

**List prices** (dollars per million tokens):

| Model | Input | Output | Cache read |
|---|---|---|---|
| Opus 5.5 | 4 | 20 | 0.20 |
| Sonnet 5.5 | 2 | 10 | 0.10 (pricing page, 2026-11-05; the 2026-10-06 API reference listed 0.20) |

Cache writes cost 1.25× base input with the 5-minute cache and 2× with the 1-hour cache [P-page].

**Cost per contribution:**

| Model | Low | Central | High | High, no prompt caching |
|---|---|---|---|---|
| Opus 5.5 | **$6** | **$17** | **$46** | $159 |
| Sonnet 5.5 | $3 | $9 | $23 | $80 |

In the central Opus case, output (≈ $7.80) and interview input (≈ $4.40) dominate; session restarts that rewrite the cache add ≈ $2.40. Caching discipline cuts costs about threefold, but model and architecture choices move inference spending only by tens of dollars per contribution.

## 3. Scenario analysis (10 / 50 / 200 contributions)

Central estimates, with ranges in brackets:

| Contributions | Inference (Opus 5.5) | Shepherd hours | Review hours | Support hours, A | Support hours, B |
|---|---|---|---|---|---|
| 10 | $170 [$61–462] | 200 [50–600] | 80 [20–180] | 5 [2–10] | 10 [5–20] |
| 50 | $851 [$307–2,310] | 1,000 [250–3,000] | 400 [100–900] | 25 [12–50] | 50 [25–100] |
| 200 | $3,404 [$1,230–9,240] | 4,000 [1,000–12,000] | 1,600 [400–3,600] | 100 [50–200] | 200 [100–400] |

**Support assumptions [U].** Option A: 0.5 h per contributor (0.25–1). Option B: 1 h (0.5–2), reflecting more varied local environments. Both are to be measured in the pilot.

**The decision-relevant result.** At 200 contributions, the central estimate is about **4,000 shepherd hours** (roughly two full-time-equivalent years) and **1,600 review hours**, against about **$3,400 of inference**. Human effort dominates under either architecture. The architecture choice mainly moves **engineering effort** (§4) and **who pays for model access** (§5).

## 4. Costs that differ between the options

| Category | Option A — hosted platform | Option B — local skill |
|---|---|---|
| **Initial development** (engineer-weeks, beyond a shared core of 9–16) | 12–19 (A1 + staff execution); +3–6 for a hosted sandbox (A2) | 8–14 |
| **Fixed operating** | Hosting ≈ **$13–210 a month** from pilot to 200 contributors, excluding inference, e-mail, and paid error tracking. Estimated from verified anchors: Fly.io from $2.19/month ($33 for a 2 GB machine); Neon $0.106 per compute-unit hour plus $0.35/GB-month; Supabase Pro $25/month; Cloudflare R2 $0.015/GB-month; Langfuse Core $29/month [P-page, R9] | Static page plus upload endpoint: near zero to tens of dollars a month |
| **Variable per contribution (project)** | Inference ≈ $17. A2 sandbox ≈ $32 in total for 200 contributions at Managed Agents' $0.08 per session-hour [R9] | $0 by default; ≈ $17 if the project provides API access; more if it reimburses plans (§5) |
| **Contributor-side** | Time; for A1, their own compute and Stata licence | Time; a paid plan unless provided (Pro $20/month, or $17 billed annually; Free cannot run Claude Code) [P-full]; their own compute and licences |
| **Ongoing maintenance** | ≈ 0.1–0.25 FTE: deployments, security updates, monitoring, backups, processor agreements [U] | ≈ 0.05–0.15 FTE: plugin and template updates tracking several client releases a week; cross-platform regression runs [U] |
| **Support load** | Lower per contributor (one environment), plus run-kit questions | Higher per contributor (installation and environment diversity) |
| **Security and compliance** | Project custody of unpublished code and transcripts: security review, privacy notices, processor terms (GDPR standard contractual clauses) | Lighter for the project; each contributor's account terms govern most data flows |

## 5. Who pays for model access — a policy choice, partly independent of architecture

| Mechanism | Works with | Cost to project | Model consistency | Data-use terms | Caveat |
|---|---|---|---|---|---|
| Project API account behind the platform | A | ≈ $17 per contribution | Enforced | Commercial: Anthropic "may not train" | Regional policy applies to end users |
| Contributor's own plan | B | $0 | Recommended only | Consumer plans train unless the user opts out (5-year retention if on), with feedback and safety exceptions; commercial plans do not train [P-page/P-full] | Pro or higher required |
| Project reimburses plans | B | One month of Pro × 200 contributors = **$4,000**, more than ≈ $3,400 of direct API inference | Recommended only | As above | Admin overhead |
| Project-issued access through a Console "Claude Code workspace" with per-user monthly spend limits [P-page] | B | ≈ $17 per contribution | Recordable; enforceable only with organization-managed settings | Commercial | Whether external contributors may receive such access needs confirmation (O-018) |
| Team seats for contributors | B | Team Standard $25/month per seat ($20 annually); seats are named and not for rotation [P-full/P-page] | Organization-managed | Commercial | Seat management across 200 short-lived contributors |
| Project gateway | B | ≈ $17 plus a small service | Enforceable at the gateway | Commercial | Anthropic's gateway feature accepts only private-network addresses; a public gateway would be the project's own [P-page] |
| Sponsor or programme credits | A or B | Reduced | Depends | Depends | AI for Science: up to $50k in credits per project, "any researcher is eligible to apply" [P-full]; the Sloan Foundation distributes Claude credits [P-page]; a Team plan offer for scientists ($0 Standard seats for 12 months; economics not named; lab members only) [P-full] |

**Note.** If Option B uses project-provided commercial access to secure consistency and terms, its inference cost to the project equals Option A's. The remaining differences are then engineering, operations, and support.

## 6. Sensitivities: what would change these conclusions

- **Heavy hosted execution (A2) with large data.** Most target analyses should run in minutes (a selection criterion), but heavy-tailed package sizes (5% of AEA packages exceed 20 GB) would raise sandbox and storage costs for those papers.
- **A more expensive model.** Claude Fable 5.1 ($10 / $50 per million tokens) raises inference about 2.5×. That is still small next to human effort.
- **Contributor counts in the thousands.** Inference would reach tens of thousands of dollars, but shepherding would bind long before.
- **Shepherd efficiency** is the largest lever. Halving shepherd hours per task saves more than any architecture choice. Translating Stata packages to R or Python for task environments is a major shepherd cost, because 71.6% of packages use Stata [S, R8].
- **Contributor honoraria** (O-005) could exceed every other per-contribution cost. They do not depend on the architecture.

## 7. What the pilot must measure to replace these estimates

- Interview duration, sessions, and turns.
- Tokens and list-price cost per session.
- Agentic token use in operationalization.
- Support minutes per contributor and per option.
- Shepherd hours per admitted task and per stage, including translation.
- Review hours.
- The share of candidates that become admitted tasks.
