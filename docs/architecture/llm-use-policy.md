# AI Use and Benchmark Integrity Rules

| | |
|---|---|
| **Status** | **Decided** v1.0 (2026-11-07), written at the research lead's instruction to replace outdated rules with a simpler, consistent set; the wording is open to the lead's review. Recorded as D-034 to D-038 in the [decision log](../decisions/decision-log.md). It replaces the LLM use policy v0.1–v0.3 and decisions D-018, D-031, D-032, and D-033, and rewords D-021 (see the decision log's table of items superseded on 2026-11-07). |
| **Applies to** | The team, invited contributors, and the evaluation of models |
| **Evidence** | [R10](../research/evidence/R10-contamination-and-evaluation-isolation.md) (contamination and evaluation isolation); [R11](../research/evidence/R11-llm-assistance-in-benchmark-construction.md) (AI in benchmark construction) |

---

## 1. What the rules protect against

| Problem | Can we prevent it? | What we do |
|---|---|---|
| **The evaluated agent finds the answers during the test**: in its files, on the internet, in version history, or from the grader | Yes: we control the test environment | Isolate the evaluation (Rule 9) |
| **A model was trained on our answers**, so it scores by memory, not reasoning | No. Every model, including open-weight ones, is evaluated through its provider's API (D-038), so every evaluated provider receives our task packages and the agents' work. Material sent to an AI service while building tasks also stays with that provider. Account settings and contract terms lower the chance of training; they do not stop the provider from receiving and keeping the material (§3) | Keep the answers of scored tasks unpublished (Rule 8). Record which providers received what (Rule 10). Report affected scores separately and keep adding new tasks (Rule 10) |
| **Tasks reflect an AI's judgment instead of economists'**, carry AI writing patterns, or favour the model family that drafted them | Largely, through how tasks are built | Experts decide; people write the final text; each item records its origin; no filtering by frontier-model success (Rules 4–7) |
| **Privacy and law** | Yes | Restricted data never go into AI services; the site sends nothing; contributors' material is used only with consent (Rules 1–3) |

## 2. The rules

**Privacy and law**

- **Rule 1. Restricted or confidential data never go into any AI service, by anyone.** *Why:* data agreements and law.
- **Rule 2. The contributor site sends nothing to AI services** and loads no third-party analytics, fonts, CDNs, or embedded content. An AI feature is added to the site only if the research lead configures it. *Why:* this is what we promise contributors.
- **Rule 3. The team sends a contributor's unpublished materials or responses to an AI service only with that contributor's consent.** Contributors decide how they use AI with their own materials. *Why:* consent.

**Building tasks**

- **Rule 4. AI may help the team and contributors** draft, vary, check, and word candidate items and other materials, through any AI service. *Why:* established benchmarks do this routinely under expert review (evidence note R11).
- **Rule 5. Experts decide.** Every item is validated by an expert in the contributor review. Where an item can be run, its effect on the results is confirmed by running it. *Why:* the benchmark's ground truth is economists' judgment.
- **Rule 6. People write or rewrite what they submit** (decisions, reasons, comments, proposed items, README text) and the final text and code edits the agent sees. AI output is never used as it is. *Why:* the tasks must reflect the authors' own scientific judgment, and AI writing has patterns an evaluated AI could exploit.
- **Rule 7. Provenance.** Each item records who drafted it (the team, the contributor, or an AI service, with its model family) and whether AI helped review it. Results are reported by these origins. Items are never kept or dropped because frontier models solve or miss them. *Why:* this measures generator bias and AI influence instead of guessing at them; filtering by model success biases comparisons between models (evidence note R11 §4).

**Answers and evaluation**

- **Rule 8. Answers of scored tasks stay unpublished** until the task is retired. Demo and development tasks may be published, with the project canary. *Why:* publication is the one leak we fully control.
- **Rule 9. Evaluation isolation.** During a test the agent can reach only the instruction, the candidate package, and its model's endpoint. It has no answer files, rubric, original package, version history, or other internet access. Grading runs outside the agent's environment. Before release, a team member tries to find the answers from inside that environment. Task packages use the restructured presentation (neutral names), as in V5. *Why:* stops the agent from looking answers up (evidence note R10 §3).
- **Rule 10. Exposure log and separate reporting.**
  - **Log:** for each task, which AI providers received its answer-key material (while building or reviewing it) or its package (in an evaluation run), when, and through what kind of account.
  - **Report separately:** a model's scores on tasks whose answer keys its provider received before the evaluation.
  - **Renew:** add new tasks over time, and retire tasks whose answers become public.

  *Why:* detection is the safeguard that works when prevention cannot be verified (evidence note R10 §2: held-out comparisons, dating against training cutoffs).
- **Rule 11. Practice, not a guarantee.**
  - With answer-key material, prefer work, business, or API accounts.
  - On personal accounts, switch model training off, avoid the feedback buttons, and never share conversations publicly.

  *Why:* it closes the leak path that is documented (consumer chat data used for training) and costs nothing. It is not a guarantee, so Rule 10 still applies.

## 3. How reliable are "training off" settings?

Not reliable enough to count as protection, which is why Rule 11 is practice and Rule 10 is the safeguard.

- **The material is still sent and kept.** For example, Anthropic keeps consumer conversations for 30 days with training off, and conversations given feedback or flagged for safety review may still be used for training [P-page, evidence note R3 §6].
- **Courts can override deletion.** In May 2025 a US court ordered OpenAI to preserve ChatGPT conversations users had deleted, temporary chats, and API outputs without a zero-retention agreement; Enterprise and Edu accounts were excluded [S] ([Engadget](https://www.engadget.com/ai/openai-appeals-court-order-forcing-it-to-preserve-all-chatgpt-data-120032364.html); [JD Supra](https://jdsupra.com/legalnews/court-orders-openai-to-retain-all-9674278)). Its current status was not checked.
- **We cannot verify a contributor's settings**, and providers change their defaults. Shared chat links were indexed by search engines in 2025 [S, evidence note R11 §4].
- **Evaluation sends the packages anyway.** With public original packages, a flawed package reveals the planted errors by comparison with the original (evidence note R10 §3).

## 4. What changed from the earlier rules

| Earlier rule | Now | Why |
|---|---|---|
| D-018: no project content to any external AI service | Rules 1–4 | The lead now wants AI in task construction and flexible author use. The privacy safeguards that matter stay: restricted data, the site, consent |
| D-021 and X-007: no AI-generated flawed packages | Rules 4–6 | "We do not need an AI agent" (revision ¶3) was not a ban; AI may now help, and experts decide |
| D-031: answer keys only to a local model | Removed | No local models (D-038); exposure is logged and reported (Rule 10) |
| D-032: development, evaluation, and held-out tiers, with a deferred clarification | Rules 8 and 10 | Every model is evaluated through APIs, so no task stays private from providers; a separate held-out tier would add rules without adding protection. Kept: unpublished answers, exposure dates, separate reporting, new tasks |
| D-033: no local model, so held-out material goes to no model | D-038 | The lead clarified that open-weight models are evaluated through APIs |
| P-054 and P-055: tier fixed before drafting; no AI on items for some papers; tier hidden from contributors | Rules 4–7, 10, and 11 | One rule for everyone; exposure is logged instead of forbidden |
| Rubric gate LK-5 and verifier-protocol §10: consumer accounts never see hidden material; held-out split on local models | Rules 10 and 11 | Logged and reported instead; no local models |

## 5. What contributors are told

The Guidance page asks contributors to:
- write in their own words;
- say whether AI helped and whether they entered the items;
- never put restricted data into an AI tool;
- prefer accounts that do not train on their input.

It also explains why ([MVP](mvp-contributor-interface.md) §5.6).

## 6. This design work

The Claude sessions used to write these documents are an AI service like any other: material shared in them reaches Anthropic and belongs in the exposure log. The V5 package was uploaded on 2026-11-06; only its structure was read. It is logged as received by Anthropic and is a demo task. If the research lead's Claude account is a personal plan, model training should be switched off: consumer plans, including Claude Code used with them, may be trained on unless the user opts out [P-page, evidence note R3 §6]. Answer-key content is opened in a Claude session only when the research lead asks.
