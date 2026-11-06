# LLM Use and Answer-Key Leakage

| | |
|---|---|
| **Status** | **Proposed** team policy v0.1 (2026-11-06), answering the research lead's question: "if we discuss locally with a public LLM, will it cause leakage, and is there a solution?" Builds on D-018 and D-031. |
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

## 2. Why leakage matters here

1. **Confidentiality.** The answer key (planted errors, repairs, rubrics) leaves project control. Even under no-training terms the provider keeps a copy for its retention period.
2. **Contamination.** A provider that trains on the material may release models that already know the answers. Their scores on those tasks would then measure recall, not research ability. The benchmark evaluates exactly these providers' models.

## 3. Material classes and allowed tools

| Class | Examples | Allowed tools |
|---|---|---|
| **Public** | The published paper; the public replication package | Any |
| **Agent-facing, before release** | The candidate package for an unreleased task | Local model only, unless the research lead approves otherwise for a specific task; any exception is logged |
| **Answer-key** | Candidate items, rubrics, item maps, flawed code and diffs, expert guides, contributors' reviews and comments, pilot results | **Local model only (D-031).** Never paste into a hosted chatbot or coding assistant |
| **Restricted data** | Patient, personnel, or other licensed microdata | **No model at all**, and only in environments the data's terms allow |

## 4. Solutions

1. **Give the team a sanctioned local model.**
   - Serve an open-weight model on a project GPU server or a strong workstation, reachable only from the team's network, with outbound traffic blocked and no telemetry.
   - Point a simple chat interface, or the IDE assistants students already use, at it.
   - If the safe path is as easy as the public one, people will use it. Hardware needs depend on the model size [U]: smaller open-weight models run on one GPU workstation, while the largest need multi-GPU servers.
2. **Label the material.** Expert-only folders and files carry a visible header such as "ANSWER-KEY MATERIAL: local tools only". V5's `Expert_Only_Do_Not_Upload` folder name already does this.
3. **Add a canary string.**
   - Embed one random GUID in every answer-key file and every task package.
   - If a model ever reproduces it, the material reached training data. Terminal-Bench-Science uses this practice [P-full, R1].
   - It detects leakage; it does not prevent it.
4. **Keep an exposure log.** When anything reaches a provider, by accident or by decision, record what, which provider and service, and when. That provider's models are then marked *exposed* for the affected tasks: their scores are reported separately, or the task is refreshed before they are evaluated on it.
5. **If a hosted service is ever unavoidable,** use it only with the research lead's approval, under commercial no-training terms with zero data retention, and log it.

## 5. This design work

These documents are prepared with Claude, which is a hosted model. The V5 package file was uploaded to the Claude session, so it is stored on Anthropic's infrastructure: in the upload and in the session's cloud container. Only its structure entered the model's context. How Anthropic may use stored session files depends on the account's terms [U: account type not known to me].

**Recommendations:**
- record V5 as exposed to Anthropic in the exposure log;
- treat Claude models as exposed for the V5 task, or refresh that task before evaluating them;
- in future, share only structure or synthetic stand-ins with any hosted assistant, as CLAUDE.md now requires.

The extracted working copies in the session's scratch area were deleted on 2026-11-06.
