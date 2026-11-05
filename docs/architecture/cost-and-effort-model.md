# Cost and Effort Model (shared assumptions for Options A and B)

| | |
|---|---|
| **Status** | **Proposed** v0.3.0 (2026-11-05). Planning estimates, **not quotes**. To be calibrated with pilot measurements (Deliverable 8, PQ5). v0.3.0 integrates the independent reviews (§8). |
| **Reproducible** | [`cost-model/inference_model.py`](cost-model/inference_model.py) and [`cost-model/scenarios.py`](cost-model/scenarios.py) compute every number in §2–§4 from the assumptions below. |
| **Price sources** | Claude API list prices from Anthropic's API reference (cached 2026-10-06), confirmed on the pricing page on 2026-11-05 ([R3](../research/evidence/R3-access-pricing-policy-portability.md)) [P-page]. Claude plan prices from the pricing page (R3) [P-full]. Hosting anchors from vendor pricing pages ([R9](../research/evidence/R9-hosted-stack-and-compliance.md)) [P-page]. |
| **Rule** | Engineering and human effort are stated in **hours or engineer-weeks**, not dollars. Convert with your institution's fully loaded rates; the model does not invent salaries. |

---

## 1. Shared assumptions

Both options are costed on the **same** assumptions. Where the options genuinely differ, §4 lists the difference explicitly. Every assumption marked [U] is to be measured in the pilot.

| ID | Assumption | Central | Range | Basis |
|---|---|---|---|---|
| A1 | Contributions (one paper each) | 10 / 50 / 200 | — | Brief §7 scenarios |
| A2 | Interview length, all sessions | ≈ 3 h, in 3+ sessions of ≤ 60 min | 2–5 h | Interview protocol [U] |
| A3 | Interviewer turns per contribution | 100 | 60–160 | [U] |
| A4 | Average cached context per turn (protocol, paper text, code subset, dossier, history) | 100k tokens | 60k–180k | 40-page paper as text ≈ 30k tokens; relevant code ≈ 25k; history grows to ≈ 60k [U] |
| A5 | Output per turn, including model thinking | 2k tokens | 1k–4k | [U] |
| A6 | Agentic code work per contribution, **only where the model runs code in the session** (Option B, A2) | 1.5M input / 150k output tokens | 0.5–4M / 50–400k | [U]. A1 run kits and staff execution do not run such loops |
| A7 | Prompt caching | 1-hour cache for interview turns; 5-minute cache for agentic loops | — | Human reply gaps of 1–10 minutes. Option B with API keys needs `promptCacheTtl: "1h"` (Option B §12) |
| A8 | Model | Claude Opus 5.5 | Sonnet 5.5 as a sensitivity case | Brief's stated preference; Claude Code's default [P-page] |
| A9 | Admitted tasks per contribution | 1.0 | 0.2–1.5 | Many candidates fail review (*Good Benchmarks* §10); Terminal-Bench-Science merged 70 of 386 pull requests [S] [U] |
| A10 | Shepherd-team hours: screening and early stages for **every** candidate, including those dropped | 10 h per contribution | 5–20 h | [U] |
| A11 | Shepherd-team hours per **admitted** task (Stages 5–8, clean-room witness, hidden variants, validation ladder) | 30 h | 15–60 h | *Good Benchmarks* §10: "well over forty hours" for hard tasks the author builds [P-full]; the methodology review judges 40 h nearer a floor here [U] |
| A12 | Reviewer hours per admitted task (domain reviewer and benchmark reviewer) | 8 h | 4–12 h | [U] |
| A13 | Outside-economist hours per admitted task (blind SP-1 solves, status classification, V3 raters, calibration) | 15 h | 5–35 h | [Construction protocol](../methodology/benchmark-construction-protocol.md) staffing; methodology and econometrics reviews [U] |
| A14 | Validation-trial compute per admitted task (L8 attacks, L10 hint ladder, L11 agent trials: ≈ 50–150 trials at ≈ $5) | $500 | $250–750 | Methodology review, from Terminal-Bench-Science's trial costs (R1 §2.8) [U] |
| A15 | Package size | 40 MB median | heavy tail: ≈ 20% of AEA packages exceed 2 GB | AEA Data Editor 2024 report window [P-full, R8] |

v0.2.0 assumed 20 shepherd hours per admitted task and 0.5–1.5 admitted tasks per contribution. The reviews showed that this left out effort on dropped candidates and the work the validation ladder now requires, so the central shepherd-team effort per contribution doubles (§3).

## 2. Inference cost per contribution

**List prices** (dollars per million tokens):

| Model | Input | Output | Cache read |
|---|---|---|---|
| Opus 5.5 | 4 | 20 | 0.20 |
| Sonnet 5.5 | 2 | 10 | 0.10 (pricing page, 2026-11-05; the 2026-10-06 API reference listed 0.20) |

Cache writes cost 1.25× base input with the 5-minute cache and 2× with the 1-hour cache [P-page].

**Cost per contribution:**

| Model and route | Low | Central | High | High, no prompt caching |
|---|---|---|---|---|
| Opus 5.5, with in-session agentic work (Option B; A2) | **$6** | **$17** | **$46** | $159 |
| Opus 5.5, without it (A1 run kits; staff execution) | $5 | $13 | $35 | — |
| Sonnet 5.5, with in-session agentic work | $3 | $9 | $23 | $80 |

In the central Opus case, output (≈ $7.80, of which ≈ $3 is agentic) and interview input (≈ $4.40) dominate; session restarts that rewrite the cache add ≈ $2.40; agentic work costs ≈ $4 in all (its output included above). Caching discipline cuts costs about threefold, but model and architecture choices move inference spending only by tens of dollars per contribution.

## 3. Scenario analysis (10 / 50 / 200 contributions)

Central estimates, with crude bounds in brackets (all-low and all-high combinations):

| Contributions | Admitted tasks | Interview inference (Opus 5.5) | Shepherd-team hours | Reviewer hours | Outside-economist hours | Validation-trial compute |
|---|---|---|---|---|---|---|
| 10 | 10 [2–15] | $170 [$61–462] | 400 [80–1,100] | 80 [8–180] | 150 [10–525] | $5,000 [$500–11,250] |
| 50 | 50 [10–75] | $851 [$307–2,310] | 2,000 [400–5,500] | 400 [40–900] | 750 [50–2,625] | $25,000 [$2,500–56,250] |
| 200 | 200 [40–300] | $3,404 [$1,230–9,240] | 8,000 [1,600–22,000] | 1,600 [160–3,600] | 3,000 [200–10,500] | $100,000 [$10,000–225,000] |

Interview inference is shown at the $17 route; under A1 or staff execution it is about a quarter lower.

**Route- and option-specific hours** (central [bounds]):

| Contributions | Extra shepherd hours, A staff execution (S5 on project machines) | Support hours, A | Support hours, B |
|---|---|---|---|
| 10 | 40 [20–60] | 8 [2–15] | 10 [5–20] |
| 50 | 200 [100–300] | 38 [12–75] | 50 [25–100] |
| 200 | 800 [400–1,200] | 150 [50–300] | 200 [100–400] |

**Support assumptions [U].** Option A: 0.75 h per contributor (0.25–1.5), covering the web platform and run-kit questions on contributors' own machines. Option B: 1 h (0.5–2), reflecting installation and more varied local environments.

**The decision-relevant result.** At 200 contributions, the central estimate is about **8,000 shepherd-team hours** (roughly four to five full-time-equivalent years), **1,600 reviewer hours**, **3,000 outside-economist hours**, and **$100,000 of validation-trial compute**, against about **$3,400 of interview inference**. Human effort and validation compute dominate under either architecture, and neither depends much on the architecture. What the architecture does move:
- **Engineering effort** is now comparable (§4).
- **Shepherd hours by execution route** are untested and could outweigh every other difference: staff execution moves operationalization onto shepherds (≈ 800 extra hours at 200 contributions), while under A1 and Option B contributors submit variants they have already run. A 10% difference in shepherd-team hours (≈ 800 hours) exceeds the central engineering difference between the options. The pilot measures it (M9).
- **Who pays for model access** (§5) and **operations** (§4).

## 4. Costs that differ between the options

| Category | Option A — hosted platform | Option B — local skill |
|---|---|---|
| **Initial development** (engineer-weeks, beyond a shared core of 10–17.5 that now includes the shepherd console) | ≈ 12–19.5 (A1 + staff execution); hosted sandbox (A2): managed integration +1.5–3, self-built +3–6 | ≈ 11.5–20.5, including the upload endpoint, project page, privacy notice, subagents, helper binaries, and status line; optional controls endpoint +0.25–0.5 |
| **Fixed operating** | Hosting ≈ **$13–210 a month** from pilot to 200 contributors, excluding inference, e-mail, and paid error tracking. Estimated from verified anchors: Fly.io from $2.19/month ($33 for a 2 GB machine); Neon $0.106 per compute-unit hour plus $0.35/GB-month; Supabase Pro $25/month; Cloudflare R2 $0.015/GB-month; Langfuse Core $29/month [P-page, R9] | Static page plus upload endpoint: ≈ $0–5 a month [R9 estimate] |
| **Variable per contribution (project)** | Inference ≈ $13 (A1, staff) or ≈ $17 (A2). A2 sandbox ≈ $32 in total for 200 contributions at Managed Agents' $0.08 per session-hour [R9] | ≈ $17 with project-provided API access; $0 where institutions provide commercial access. Consumer plans are admissible only for agent-tier or public material under the exposure rule (§5) |
| **Contributor-side** | Time; for A1, their own compute and Stata licence | Time; their own compute and licences; installation |
| **Ongoing maintenance** | ≈ 0.1–0.25 FTE: deployments, security updates, monitoring, backups, processor agreements [U] | ≈ 0.1–0.2 FTE: plugin and workspace compatibility with the client's stable channel, the upload endpoint, cross-platform regression runs [U] |
| **Evaluation inference** (simulated-contributor regression suite: 15 simulated contributions per pass ≈ $255, range $92–693) | Per protocol or pinned-model change, ≈ 4–8 passes a year: ≈ **$1,500 a year** ($370–5,500) [U] | Per certified stable client release; certifying monthly ≈ **$3,100 a year** ($1,100–8,300); certifying every weekly stable release at the high per-pass cost would reach ≈ $36,000 [U] |
| **Support load** | ≈ 0.75 h per contributor: the web platform plus run-kit questions on heterogeneous machines | ≈ 1 h per contributor: installation and environment diversity |
| **Shepherd hours by route** | Staff execution adds ≈ 4 h (2–6 h) per contribution for S5 [U]; A1 as Option B | Contributors or RAs pre-do part of S5 [U] |
| **Security and compliance** | Custody of uploads, drafts, abandoned contributions, and consented transcripts from the first session, with processors (hosting, database, storage, tracing, error tracking): security review, privacy notice, processor agreements, GDPR standard contractual clauses | Lighter during drafting; the **same duties for submitted packages**; hidden-tier copies persist on contributors' machines (purge step, agreement) |

**Pilot slices.** Building thin slices of both options for the pilot costs roughly **8–14 engineer-weeks for whichever slice is built second** [U], on top of the shared core and the first slice. A cheaper variant (one slice plus setup and hand-off probes of the other) is an open question (O-019).

## 5. Who pays for model access — a policy choice, partly independent of architecture

The [verifier protocol](../methodology/verifier-validation-protocol.md) §10 (Proposed) requires commercial no-training terms for any session that sees hidden-tier material. Because flawed variants and answer keys are created inside the interview, this constrains Option B's access mechanisms.

| Mechanism | Works with | Cost to project | Model consistency | Data-use terms | Admissible for hidden-tier work? | Caveat |
|---|---|---|---|---|---|---|
| Project API account behind the platform | A | ≈ $13–17 per contribution | Enforced | Commercial: Anthropic "may not train" | Yes | Regional policy applies to end users |
| Project-issued access through a Console "Claude Code workspace" with per-user monthly spend limits [P-page] | B | ≈ $17 per contribution | Pinned and recorded; enforceable only with organization-managed settings | Commercial | Yes | Permitted for "the customer's own authorized users"; whether external contributors count needs confirmation (O-018) |
| Institutional commercial access (e.g., a university agreement) | B | $0 | Pinned and recorded; enforced only if the institution manages settings | Commercial | Yes | Depends on each contributor's institution |
| Team seats for contributors | B | Team Standard $25/month per seat ($20 annually); seats are named and not for rotation [P-full/P-page] | Organization-managed | Commercial | Yes | Seat management across 200 short-lived contributors; also enables Remote Control and web sessions |
| Project gateway | B | ≈ $17 plus a small service | Enforceable at the gateway | Commercial | Yes | Anthropic's gateway feature accepts only private-network addresses; a public gateway would be the project's own [P-page] |
| Contributor's own consumer plan | B | $0 | Pinned and recorded | Consumer plans train unless the user opts out (5-year retention if on), with a safety-flag exception [P-page/P-full] | **No** (agent-tier or public material only) | Pro or higher required |
| Project reimburses consumer plans | B | One month of Pro × 200 contributors = **$4,000**, more than ≈ $3,400 of direct API inference | As above | As above | **No** | Admin overhead |
| Sponsor or programme credits | A or B | Reduced | Depends | Depends | Depends | AI for Science: up to $50k in credits per project, "any researcher is eligible to apply" [P-full]; the Sloan Foundation distributes Claude credits [P-page]; a Team plan offer for scientists ($0 Standard seats for 12 months; economics not named; lab members only) [P-full] |

**Note.** With project-provided commercial-terms access, Option B's inference cost to the project equals Option A's A2 route and is about $4 per contribution above A1 and staff execution. Engineering is comparable. The remaining differences are operations, evaluation inference, support, custody, and shepherd hours by route.

## 6. Sensitivities: what would change these conclusions

- **Shepherd efficiency** is the largest lever. Halving shepherd-team hours saves more than any architecture choice. Translating Stata packages to R or Python for task environments is a major shepherd cost, because 71.6% of packages use Stata [S, R8].
- **Admission rate (A9).** At 0.2 admitted tasks per contribution, five contributions are needed per task and screening effort per admitted task rises fivefold, so recruitment and screening, rather than construction, become the binding constraints.
- **Validation-trial compute** is architecture-independent but about 15–45 times interview inference per task. Sponsor credits matter more here than for the interview.
- **Heavy hosted execution (A2) with large data.** Most target analyses should run in minutes (a selection criterion), but heavy-tailed package sizes (5% of AEA packages exceed 20 GB) would raise sandbox and storage costs for those papers.
- **A more expensive model.** Claude Fable 5.1 ($10 / $50 per million tokens) raises inference about 2.5×. That is still small next to human effort.
- **Contributor counts in the thousands.** Inference would reach tens of thousands of dollars, but shepherding would bind long before.
- **Contributor honoraria** (O-005) could exceed every other per-contribution cost. They do not depend on the architecture.

## 7. What the pilot must measure to replace these estimates

- Interview duration, sessions, and turns; tokens and list-price cost per session; agentic token use in operationalization.
- Setup time before the interview, with and without designed onboarding; research-assistant hand-off delays in both arms.
- Support minutes per contributor and per option.
- Shepherd-team hours per stage, for admitted **and** dropped candidates, by execution route, including translation and the clean-room check.
- Reviewer and outside-economist hours, including blind solves.
- Validation trials per task and their cost.
- The share of candidates that become admitted tasks.
- The cost of one evaluation-suite pass.

## 8. Changes

**v0.3.0** (independent reviews, 2026-11-05):
- Shepherd-team effort restated to include dropped candidates (10 h per contribution plus 30 h per admitted task); admitted tasks per contribution widened to 0.2–1.5.
- New lines: outside-economist hours, validation-trial compute, evaluation inference, staff-execution hours, route-specific inference ($13 without in-session agentic work).
- Engineering restated as comparable (A ≈ 12–19.5, B ≈ 11.5–20.5 beyond a shared core of 10–17.5 with the shepherd console); maintenance A 0.1–0.25 FTE, B 0.1–0.2 FTE; support A 0.75 h.
- Access mechanisms assessed against the exposure rule; custody stated symmetrically.

**v0.2.0:** verified prices and hosting anchors (R3, R9); Sonnet cache-read price corrected.
