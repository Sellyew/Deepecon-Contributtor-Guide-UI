# Reading notes — `interview-me` skill (Sant'Anna, *claude-code-my-workflow*)

| Field | Value |
|---|---|
| Source | `pedrohcgs/claude-code-my-workflow`, `.claude/skills/interview-me/SKILL.md` (987 words) |
| Version read | Repository HEAD `7586127` (merge of PR #173, 2026-11-04) |
| Read by | Claude, full text, 2026-11-05 |
| Verification level | **Primary — full text read** (cloned read-only into the session scratchpad) |

## What the skill does (established, from the text)

- **Purpose:** "Interactive interview that formalizes a fuzzy research idea into a structured spec (RQ, hypotheses, identification, data needs, empirical strategy)." Its description lists trigger phrases and exclusions ("NOT for lit review … or ideation from scratch").
- **Frontmatter:** `name`, `description`, `argument-hint` (`[brief topic or 'start fresh'] [--no-verify]`), `allowed-tools: ["Read", "Write", "Agent", "Task"]`.
- **Conversation mechanics:** "Do NOT use AskUserQuestion. Ask questions directly in your text responses, one or two at a time. Wait for the user to respond before continuing."
- **Six phases**, each with 1–2 example questions: (1) Big Picture, including a paper-type classification; (2) Theoretical Motivation; (3) Data and Setting; (4) Identification ("What's the biggest threat to a causal interpretation?"); (5) Expected Results; (6) Contribution.
- **Length:** "typically 5-8 exchanges"; "If the researcher has a clear vision after 4-5 exchanges, move to the specification. Don't over-interview."
- **Output:** a Markdown *Research Specification Document* with fixed headings, saved to `quality_reports/specs/research_spec_[topic].md`, a location other skills (`/grant-proposal`, `/preregister`, …) read from.
- **Post-flight verification (Chain-of-Verification):** if the spec cites papers, extract claims → write verification questions → spawn a separate `claim-verifier` agent **in a fresh context ("not a conversation fork, which would inherit the draft")**, giving it the claims and sources but *not* the draft → reconcile as PASS / PARTIAL / FAIL.
- **Decision records:** when the researcher chooses among live alternatives, write an ADR (Status / Problem / Options / Decision + rationale / Consequences / Rejected alternatives). No ADR when there was a single uncontested path.
- **Style rules:** "Be curious, not prescriptive"; "Probe weak spots gently" ("What would a skeptic say about…?"); "Build on answers"; "Know when to stop."

## What we should adopt

1. One or two questions per turn, asked in plain conversational text rather than form widgets.
2. Phased structure with example questions *as guidance, not a script*.
3. A downstream contract: the output lands in a known location and a known format that later steps consume.
4. **Fresh-context verification** of claims, deliberately isolated from the draft to avoid anchoring. This maps well onto our need to verify contributors' methodological claims independently.
5. ADRs for decisions with live alternatives (e.g., why one estimator rather than another).
6. Gentle skeptical probing ("What would a skeptic say…?") rather than assertion.

## Where our use case differs (our analysis)

| Dimension | `interview-me` | DeepEcon expert interview |
|---|---|---|
| Object | A new, fuzzy idea | An existing, published paper and its replication package |
| Goal | Generate a research spec | Elicit consequential decisions and plausible mistakes; turn them into verifiable tasks |
| Evidence | The researcher's intentions | The paper, the code, the data, and executable results |
| Length | 5–8 exchanges, one sitting | Likely several hours across sessions; must be resumable |
| State | None beyond the final file | Persistent, structured, versioned state with provenance per statement |
| Output | Markdown with fixed headings | Machine-readable records in four visibility tiers (contributor, internal, agent-facing, hidden) |
| Epistemic risk | Hallucinated citations | Leading the expert, fabricated or trivial errors, AI-drifted task design (Bercovich §9), leakage of answers into agent-facing text |
| Human authority | Implicit | Explicit: every field records who asserted it (contributor / LLM / validated) and contributor sign-off |
| Stopping rule | Exchange count / "clear vision" | Evidence-based sufficiency criteria per candidate error, plus contributor fatigue and diminishing returns |

## Gaps we must design for

- No resumability, checkpointing, or progress tracking.
- No provenance distinction between what the researcher said and what the model inferred.
- No safeguard against leading questions beyond the style guidance.
- No machine-readable output or schema validation.
- No handling of code or data as evidence (file and line references, executed outputs).
- No bilingual behaviour.
