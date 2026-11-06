# LLM Use and Answer-Key Leakage

| | |
|---|---|
| **Status** | **Proposed** team policy v0.2 (2026-11-06). v0.1 answered the research lead's question: "if we discuss locally with a public LLM, will it cause leakage, and is there a solution?" v0.2 applies the task tiers the lead agreed the same day (D-032): the local-only rule now covers held-out tasks, and D-018 governs the rest. Builds on D-018, D-031, and D-032. |
| **Applies to** | Everyone who prepares, reviews, or handles benchmark materials: the team, students, and invited contributors |

---

## 1. Short answer

**What matters is where the model runs, not where you type.**

| Situation | Does the material leave the project? | Leakage? |
|---|---|---|
| A hosted chatbot or API: ChatGPT, Claude, DeepSeek's web chat or API, Kimi, Qwen online, and so on | Yes. Every prompt and pasted file goes to the provider's servers | **Yes** |
| A tool that runs "locally" but calls a hosted model: Claude Code, Cursor, IDE assistants, desktop chat apps | Yes. The client is local, but every prompt and every file the tool reads is sent to the provider | **Yes** |
| An **open-weight model running on project hardware**, for example an open-weight DeepSeek or Qwen model served on the team's GPU server, with outbound traffic blocked | No | **No** leakage to any provider. Using a model does not change its weights, and nothing is sent anywhere if the serving software has no telemetry and the machine cannot reach the internet |
| Fine-tuning a local model on answer-key material | Not while the weights stay local | Yes, if the fine-tuned weights are ever shared or published |

So discussing project materials with a local *client* of a public model leaks them, while discussing them with a public *open-weight* model that runs on your own hardware does not.

## 2. Three different risks

| Risk | What goes wrong | Handled by |
|---|---|---|
| **Confidentiality** | Project content or contributor data leave project control. Even under no-training terms the provider keeps a copy for its retention period | D-018 and this policy |
| **Training contamination** | A provider trains on a task and its answers, and its later models recall them. Their scores on that task then measure recall, not research ability, and the benchmark evaluates exactly these providers' models | The task tiers (D-032): exposure dates, a held-out tier, replacement of exposed tasks |
| **Leakage during evaluation** | The evaluated agent finds the answers while working, for example from the internet, version-control history, or the grader | The evaluation design (P-052), not this policy |

An isolated evaluation environment stops the third risk but not the second: a model that has learned the answers brings them into the sandbox ([R10](../research/evidence/R10-contamination-and-evaluation-isolation.md) §1).

## 3. Material classes and allowed tools

| Class | Examples | Allowed tools |
|---|---|---|
| **Public** | The published paper; the public replication package; development tasks once published | Any |
| **Development and evaluation tasks, unpublished** (D-032) | Candidate packages, candidate items, rubrics, item maps, flawed code and diffs, expert guides, pilot results | **No external AI service by default (D-018).** The research lead may explicitly configure one, such as the DeepSeek API with the lead's own key, for a stated use; an evaluation task's agent-facing package, however, goes to a provider only in an evaluation run of that provider's models (D-032). Each use and each run is logged with the provider, its terms, and the date (§4) |
| **Held-out tasks** (D-032) | Everything belonging to a held-out task: answer key, grader, item map, flawed code, expert guides, and its agent-facing package | **Local model only (D-031, D-032)** for all team work. Never paste into a hosted chatbot or coding assistant. Only exception: for evaluation, the agent-facing package (never the answer key or grader) may be run on a closed model under a no-retention agreement, configured by the research lead and logged (D-032; clarification pending) |
| **Contributor responses and unpublished materials** | Reviews, comments, proposals, messages, unpublished code | **Local model only** (proposed: stricter than D-018, which allows an API the research lead configures; P-035; contributors have not consented to anything else) |
| **Restricted data** | Patient, personnel, or other licensed microdata | **No model at all**, and only in environments the data's terms allow |

## 4. Solutions

1. **Label the material by tier.** Held-out folders and files carry a visible header such as "HELD-OUT: local tools only"; other answer-key files carry "ANSWER-KEY MATERIAL: no external AI without the lead's approval". V5's `Expert_Only_Do_Not_Upload` folder name already does this.
2. **Add a canary string.**
   - Embed one random GUID in every answer-key file and every task package.
   - If a model ever reproduces it, the material reached training data. Terminal-Bench-Science uses this practice [P-full, R1].
   - It detects leakage; it does not prevent it.
3. **Keep an exposure log.** Record what reached a provider or the public, which provider and service, under which terms, and when, whether by accident, by decision, or through a closed-model evaluation run.
   - A closed-model evaluation run exposes only the agent-facing package, and only to that provider. The run is logged, that provider's models with a later training cutoff are reported separately on the task, and the task keeps its tier.
   - If a task's answer key or grader reaches a provider or the public, or its agent-facing package is published, that date is the task's **exposure date**: the task moves to the development tier and is replaced (D-032).
   - This reading of D-032 awaits the research lead's confirmation.
4. **Offer a sanctioned local model if the team wants LLM help on held-out tasks or contributors' responses.**
   - Serve an open-weight model on a project GPU server or a strong workstation, reachable only from the team's network, with outbound traffic blocked and no telemetry.
   - Point a simple chat interface, or the IDE assistants students already use, at it.
   - If the safe path is as easy as the public one, people will use it. Hardware needs depend on the model size [U]: smaller open-weight models run on one GPU workstation, while the largest need multi-GPU servers.
   - It is not needed for validity: the held-out tier can be handled without any model.
5. **If a hosted service is used for development or evaluation material,** use it only with the research lead's explicit configuration (D-018), under commercial no-training terms with zero data retention where available, and log it.

## 5. This design work

These documents are prepared with Claude, which is a hosted model. The V5 package file was uploaded to the Claude session, so it is stored on Anthropic's infrastructure: in the upload and in the session's cloud container. Only its structure entered the model's context. How Anthropic may use stored session files depends on the account's terms [U: account type not known to me].

**Recorded:**
- V5 is exposed to Anthropic (exposure date 2026-11-06) and is a **development task** (D-032), so its exposure does not affect headline scores;
- in future, only structure or synthetic stand-ins are shared with any hosted assistant, as CLAUDE.md requires (D-018 applies to every tier).

The extracted working copies in the session's scratch area were deleted on 2026-11-06.
