# Evidence notes (Phase 1 discovery)

Working research notes produced by AI research agents (Claude subagents) under the direction of the lead collaborator, itself a Claude session; no human researcher took part unless a note says so. R1–R9 date from 2026-11-05; R10 (written by the lead collaborator directly) and R11 (by subagents) from 2026-11-06. Each note is **dated**, **labels every factual claim** with an evidence level, and separates what sources say from our assessment. They are working material, not polished deliverables: the synthesis lives in [Deliverable 1](../research-and-methodology-review.md) and the design documents.

| Evidence level | Meaning |
|---|---|
| **[P-full]** | Primary source, full text (or the full cited section) read |
| **[P-page]** | Primary source, abstract, landing page, README, or official documentation page read |
| **[S]** | Secondary source (search snippet, blog, news, a survey citing it) |
| **[U]** | Unverified: recollection, inference, or a source that could not be accessed |

| Note | Topic |
|---|---|
| [R1](R1-terminal-bench-science.md) | Terminal-Bench-Science and the Harbor task format: anatomy, lifecycle, rubrics, verifier validation, leakage, reuse options |
| [R2](R2-claude-code-platform.md) | Claude Code: skills, plugins, hooks, permissions, surfaces, model selection, data handling, Agent SDK |
| [R3](R3-access-pricing-policy-portability.md) | Plans and prices, regional availability, data-use terms, alternative endpoints, Agent Skills portability, academic programmes |
| [R4](R4-replication-benchmarks.md) | Reproduction and replication benchmarks, with emphasis on economics and social science; name-collision check |
| [R5](R5-analysis-causal-econ-benchmarks.md) | Data-analysis, causal-inference, statistical, and economics-reasoning benchmarks; many-analysts literature |
| [R6](R6-error-detection-and-verifier-methodology.md) | Error-detection benchmarks; benchmark-validity methodology; software-testing techniques for verifier validation |
| [R7](R7-expert-elicitation-and-ai-interviews.md) | Knowledge elicitation, AI-led interviews, sycophancy and anchoring; patterns from Sant'Anna's workflow; critique of the draft protocol |
| [R8](R8-replication-standards-and-econometric-pitfalls.md) | Replication-package standards and licensing; catalogue of econometric pitfalls; documented real and contested errors; pilot candidates |
| [R9](R9-hosted-stack-and-compliance.md) | Hosted-platform stack, cost anchors, sandboxes, Stata licensing, data protection, ethics review |
| [R10](R10-contamination-and-evaluation-isolation.md) | Training contamination versus evaluation-time leakage: held-out splits, semi-private sets, dating, isolation failures (2026-11-06) |
| [R11](R11-llm-assistance-in-benchmark-construction.md) | LLM assistance in benchmark construction: Terminal-Bench family rules, practice in 20 other benchmarks, exposure and measurement risks, provider data-use defaults (2026-11-06) |
| [R12](R12-human-access-to-unreleased-answers.md) | Who may see a task's unreleased answers: Terminal-Bench's public development, held-out sets and their custodians, cross-review by assignment, confidentiality terms (2026-11-07) |
| [R13](R13-release-and-evaluation-practice.md) | How benchmarks release, refresh, and officially evaluate tasks: versioning, errata, maintainer-run evaluation, fixed conditions, selection after results (2026-11-07) |
| [R14](R14-contamination-in-practice.md) | How much task exposure matters in practice: measured contamination effects, lab practice, API data terms, and why DeepEcon differs from Terminal-Bench-Science (2026-11-08) |

**Environment limits that shaped these notes.** arxiv.org, github.com (web and API), docs.github.com, and several vendor sites were outside the cloud environment's allowed network domains. Papers on arXiv were therefore often verified only through search-engine snippets ([S]) or alternative hosts. *Good Benchmarks* was read in full from a PDF supplied by the research lead.
