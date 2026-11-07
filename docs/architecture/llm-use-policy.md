# AI Use and Benchmark Integrity Rules

| | |
|---|---|
| **Status** | **Proposed** v1.0 (2026-11-07). Drafted by Claude, the research-engineering collaborator, at the research lead's request for a simpler, consistent set of rules, and applied provisionally until the lead approves or amends it. Recorded as proposals P-056 to P-059 and decision D-038 (the lead's own) in the [decision log](../decisions/decision-log.md). The lead's instruction of 2026-11-07 replaced the earlier rules D-018, D-031, D-032, and D-033 and the LLM use policy v0.1–v0.3, and reworded D-021; see the decision log's table of items superseded on 2026-11-07. |
| **Applies to** | The team, invited contributors, and the evaluation of models |
| **Evidence** | [R10](../research/evidence/R10-contamination-and-evaluation-isolation.md) (contamination and evaluation isolation); [R11](../research/evidence/R11-llm-assistance-in-benchmark-construction.md) (AI in benchmark construction) |

---

## 1. What the rules protect against

| Problem | Can we prevent it? | What we do |
|---|---|---|
| **The evaluated agent finds the answers during the test**: in its files, on the internet, in version history, or from the grader | Yes: we control the test environment | Isolate the evaluation (Rule 9) |
| **A model was trained on our answers**, so it scores by memory, not reasoning | Only partly. An evaluation through an API cannot contaminate the model being tested, but it gives the model's developer, and any API host, the task package and the agent's work, which later models could be trained on. Material sent to an AI service while building a task likewise reaches that service. Account settings and contract terms lower the chance of training; they do not stop the provider from receiving the material, and only a zero-retention agreement limits how long it is kept, with exceptions (§3) | Keep the answers of scored tasks unpublished (Rule 8). Record which developers and hosts received what, and when (Rule 10). Report scores separately where a model's developer had our material before that model was released, and keep adding new tasks (Rule 10) |
| **Tasks reflect an AI's judgment instead of economists'**, carry AI writing patterns, or favour the model family that drafted them | Largely, through how tasks are built | Experts decide; people write the final text; each item records its origin; no adversarial filtering (Rules 4–7) |
| **Privacy and law** | For the team and the site, yes; for contributors' own tools, we can only ask | Licensed and restricted data never go into AI services; the site sends nothing; contributors are told what evaluation does and consent to other uses (Rules 1–3) |

## 2. The rules

**Privacy and law**

- **Rule 1. Data whose licence or agreement does not allow passing them to third parties never go into any AI service, by anyone, including through an evaluated agent.** This covers restricted and confidential data and licensed data such as PSID or WRDS files. Tasks built on such data give the agent a fully synthetic stand-in or data whose terms allow it. *Why:* data agreements and law; an evaluated agent's work reaches its API provider.
- **Rule 2. The contributor site sends nothing to AI services** and loads no third-party analytics, fonts, CDNs, or embedded content. An AI feature is added to the site only if the research lead configures it. *Why:* this is what we promise contributors.
- **Rule 3. Contributors are told, before they agree to take part, that the finished task is sent through their APIs to each AI company whose models are evaluated, which receives it and may keep it.** Apart from that, the team uses a contributor's unpublished materials or responses with an AI service only if the contributor agrees; the choice is recorded with its date and can be changed. Contributors decide how they use AI with their own materials. *Why:* informed consent.

**Building tasks**

- **Rule 4. AI may help the team and contributors** draft, vary, check, and word candidate items and other materials, within Rules 1, 3, and 11. *Why:* established benchmarks do this routinely under expert review (evidence note R11).
- **Rule 5. Experts decide.** Every item is validated by an expert in the contributor review. Where an item can be run, its effect on the results is confirmed by running it. An item that was both drafted and reviewed with AI help is checked again by a second person, without AI, before it is accepted. *Why:* the benchmark's ground truth is economists' judgment, not an AI checking an AI.
- **Rule 6. People write or rewrite what they submit** (decisions, reasons, comments, proposed items, README text) and the final text the agent sees. AI-written text is never used as it is. Code edits, whoever drafted them, are checked by a person and pass the naturalness review (rubric LK-3). *Why:* the tasks must reflect the authors' own scientific judgment, and AI writing has patterns an evaluated AI could exploit.
- **Rule 7. Provenance and no adversarial filtering.**
  - **Provenance:** each item records who drafted it (the team, the contributor, or an AI service, with its model family) and whether AI helped review it. Results are reported by these origins. AI help is self-reported and probably undercounted (evidence note R7 §1), so these comparisons are descriptive.
  - **No adversarial filtering:** items are never kept because particular models miss them. The only difficulty screen is the rubric's saturation check (DF-3), which may set aside a task that every calibration configuration solves; pass rates are reported, not targeted.

  *Why:* provenance measures generator bias and AI influence instead of guessing at them; keeping what particular models miss biases comparisons between models (evidence note R11 §4).

**Answers and evaluation**

- **Rule 8. Answers of scored tasks stay unpublished** until the task is retired.
  - A **scored task** is unpublished and counts toward reported scores.
  - A **demo or development task** may be published, with the project canary, and is not scored. The research lead designates a task as demo or development, with the date, before any evaluation run of it; a scored task is not redesignated later. V5 and the demo paper's tasks are demo tasks.
  - A retired scored task may be published.

  *Why:* publication is the one leak we fully control; fixing the designation in advance prevents choosing which tasks count after seeing the scores.
- **Rule 9. Evaluation isolation.** During a test the agent can reach only the instruction, the candidate package, and its model's endpoint.
  - It has no answer files, rubric, original package, version history, or other internet access.
  - Grading runs outside the agent's environment.
  - Before release, a team member tries to find the answers from inside that environment.
  - Task packages use the restructured presentation (neutral names, no author names or original paths), as in V5.

  *Why:* stops the agent from looking answers up (evidence note R10 §3).
- **Rule 10. Exposure log and separate reporting.**
  - **Log:** for each task, which AI services received its answer-key material (while it was built or reviewed) or its package and an agent's work (in an evaluation run), when, and through what kind of account. Name the model's developer and, if different, the API host. AI coding assistants that open files containing this material count as AI services. Each task also records when it was built. For each evaluation run, record the exact model version (a pinned snapshot, not an alias) and its release date.
  - **Report separately:** a model's scores on tasks whose answer-key material, package, or earlier evaluation trajectories reached that model's developer before that model version was released. A model released before any such exposure has a clean score on the task.
  - **Limits:** with few tasks, only large effects are detectable. *(assessment, illustration:* with 30 tasks in each group and solve rates near one half, a 95% interval on the difference is about ±25 percentage points, and wider when tasks cluster by paper.*)* Each report gives the number of exposed and clean tasks and a confidence interval (VVP §8). Comparisons between models use only tasks clean for every model compared.
  - **Renew:** add new tasks over time, and retire tasks whose answers become public.

  *Why:* dating each exposure against model releases is the safeguard the project controls, as LiveCodeBench dates problems against training cutoffs (evidence note R10 §2). It discloses likely contamination with its uncertainty; it does not prove a model was not trained on the answers.
- **Rule 11. Practice, not a guarantee.**
  - With answer-key material, prefer accounts whose current terms, checked and dated, exclude training: business or enterprise plans, or a paid API whose terms say so. This excludes Google's unpaid API tier; the DeepSeek API's terms are unresolved (evidence note R11 §5).
  - On personal accounts, switch model training off, avoid the rating and feedback buttons, and never share conversations publicly.

  *Why:* it narrows the documented leak path (consumer chat data used for training by default) at little cost. It does not close it. The provider still receives and keeps the material, and conversations given feedback or flagged for safety review may still be used for training (§3). So Rule 10 still applies.

## 3. How reliable are "training off" settings?

Not reliable enough to count as protection. That is why Rule 11 is practice and Rule 10 is the safeguard.

- **The material is still sent and kept.** For example, Anthropic keeps consumer conversations for 30 days with training off, and conversations given feedback or flagged for safety review may still be used for training [P-page, evidence note R3 §6]. Zero-retention agreements, available only through sales to qualified organisations, limit keeping, though even then flagged sessions may be kept for up to 2 years [P-page/P-full, evidence note R3 §6.2].
- **Courts can override deletion.** In May 2025 a US court ordered OpenAI to preserve ChatGPT conversations users had deleted, temporary chats, and API outputs without a zero-retention agreement; Enterprise and Edu accounts were excluded [S] ([Engadget](https://www.engadget.com/ai/openai-appeals-court-order-forcing-it-to-preserve-all-chatgpt-data-120032364.html); [JD Supra](https://jdsupra.com/legalnews/court-orders-openai-to-retain-all-9674278)). Its current status was not checked.
- **We cannot verify a contributor's settings**, and providers change their defaults. Shared chat links were indexed by search engines in 2025 [S, evidence note R11 §4].
- **Evaluation sends the packages anyway.** With public original packages, a flawed package reveals the planted errors by comparison with the original (evidence note R10 §3).

## 4. What changed from the earlier rules

| Earlier rule | Now | Why |
|---|---|---|
| D-018: no project content to any external AI service | Rules 1–4 | The lead now wants AI in task construction and flexible author use. The privacy safeguards that matter stay: licensed and restricted data, the site, informed consent |
| D-021 and X-007: no AI-generated flawed packages | Rules 4–6 | "We do not need an AI agent" (revision ¶3) was not a ban; AI may now help, and experts decide |
| D-031: answer keys only to a local model | Removed | No local models (D-038); exposure is logged and reported (Rule 10) |
| D-032: development, evaluation, and held-out tiers, with a deferred clarification | Rules 8 and 10 | Evaluation through APIs exposes a task only to models released after the run. A held-out tier, with no AI use while building its tasks, would keep more tasks clean for newly released models and keep rubrics away from all providers, at the cost of per-paper limits on AI use. The reset gives this up for simplicity and relies on dating exposures against model releases and on adding new tasks. Kept: unpublished answers, exposure dates, separate reporting, new tasks |
| D-033: no local model, so held-out material goes to no model | D-038 | The lead clarified that open-weight models are evaluated through APIs |
| P-054 and P-055: tier fixed before drafting; no AI on items for some papers; tier hidden from contributors | Rules 4–7, 10, and 11 | One rule for everyone; exposure is logged instead of forbidden |
| Rubric gate LK-5 and verifier protocol §10 and L10: consumer accounts never see hidden material; held-out split on local models | Rules 10 and 11 | Logged and reported instead; no local models |

## 5. What contributors are told

The Guidance page asks contributors to:
- write in their own words;
- say whether AI helped, and whether they entered the items;
- never put restricted or licensed data into an AI tool;
- prefer accounts that do not train on their input;
- avoid rating or feedback buttons when the items are in the conversation.

It also explains why, and what evaluation does with the finished task ([MVP](mvp-contributor-interface.md) §3 step 1 and §5.6).

## 6. This design work

The Claude sessions used to write these documents are an AI service like any other: material shared in them reaches Anthropic and belongs in the exposure log.

- **V5:** the package was uploaded on 2026-11-06, but only its structure was read. It is logged as received by Anthropic and is a demo task.
- **Account terms:** if the research lead's Claude account is a personal plan, model training should be switched off. Consumer plans, including Claude Code used with them, may be trained on unless the user opts out [P-page, evidence note R3 §6].
- **Answer keys:** answer-key content is opened in a Claude session only when the research lead asks.
