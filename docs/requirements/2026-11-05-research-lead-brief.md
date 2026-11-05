# Research Lead Brief — DeepEcon Research Benchmark (working title)

> **Status:** Canonical statement of the project's objectives and requirements, as written by the research lead on 2026-11-05.
> **Provenance:** The wording below is the research lead's initial project brief, reproduced verbatim. Only Markdown formatting (heading levels, bullet markers, bold labels) was added for readability; no sentences were added, removed, or reworded. Do not edit the text below; record any changes, clarifications, or decisions in [`docs/decisions/decision-log.md`](../decisions/decision-log.md) instead.
> **Mid-session addendum (2026-11-05):** The research lead supplied the PDF of Bercovich (2026), *Good Benchmarks* (arXiv:2607.12217v1), because arxiv.org is not reachable from the cloud environment.

---

I am starting a new research and software development project in this repository: DeepEcon Research Benchmark (working title).
Our goal is to build an expert-driven benchmark that evaluates whether AI agents can perform rigorous economics research, particularly in empirical implementation, causal identification, econometric reasoning, and scientific judgment.
We hope to collaborate with economists who have published in the Top Five economics journals (AER, Econometrica, JPE, QJE, and REStud) and leading field journals. Their research experience will provide the foundation for constructing scientifically meaningful, difficult, and verifiable benchmark tasks.
Our immediate objective is to design a system that helps these economists contribute benchmark tasks through an AI-guided interview and a structured research workflow.
We are considering two alternative contribution architectures:

* Option A — Hosted Contributor Platform: We build and operate a bilingual web application with an integrated LLM-powered interview. Contributors interact with our platform, and we manage the application and its AI services.
* Option B — Local Claude Code Skill: We develop a reusable skill that contributors run in their own Claude Code environments, ideally using Claude Opus 5.5 or another sufficiently capable model. The skill guides the research process locally and produces a standardized contribution package.

Both approaches are serious candidates. We have not selected one.
I want to compare these architectures with my collaborators before making a final decision. Your job is to develop both alternatives sufficiently that we can understand their scientific, technical, financial, and operational implications.
Do not prematurely select one architecture or begin implementing one at the expense of the other.

## 1. Our Collaboration Principles

I want our collaboration to be structured, precise, and rigorous, even if it takes more time.
This project combines research methodology, benchmark construction, LLM-agent engineering, human-computer interaction, and academic collaboration.
Treat me as the research lead and yourself as a research-engineering collaborator.
I expect you to:

* Challenge assumptions when they are not sufficiently justified.
* Distinguish established facts from proposals and unresolved questions.
* Investigate relevant existing work before making novelty claims.
* Explain architectural and methodological tradeoffs clearly.
* Prioritize scientific validity over technical sophistication.
* Design polished, intuitive, professional interfaces and workflows.
* Maintain reusable project documentation and decision records.
* Preserve important decisions and learn from corrections so that I do not need to repeat myself.
* Prefer modular, maintainable, testable solutions.
* Avoid unnecessary complexity and premature implementation.

When producing important research documents or visual materials, the results should be polished enough to share with academic collaborators.
Do not simply agree with my suggestions. I want independent, evidence-based technical and methodological judgment.
However, do not silently redefine the project's scientific objectives.

## 2. Background: Why Economics Needs Better AI Benchmarks

Economists increasingly use large language models and AI agents to support research.
These tools can write code, manipulate datasets, conduct literature searches, reproduce empirical findings, and assist with econometric analysis.
However, even highly capable AI agents sometimes make mistakes that appear surprisingly fundamental to experienced economists.
For example:

1. Estimator–implementation mismatch. An agent claims to estimate one econometric specification, but its actual code implements a different estimator.
2. Unaddressed identification threats. An identification strategy contains a recognizable threat, but the agent fails to identify or address it.
3. Irrelevant methodological discussion. Instead of engaging with the actual identification challenge, the agent produces extensive, apparently sophisticated but logically irrelevant discussion.
4. Incorrect statistical inference. An agent obtains plausible coefficient estimates but uses an inappropriate standard-error estimator, clustering level, or inference procedure.
5. Misleading causal interpretation. An agent produces technically correct regressions but makes causal claims unsupported by the research design.
6. Substantive implementation errors. The agent constructs the wrong estimation sample, mishandles treatment timing, misdefines variables, or introduces inconsistencies across analytical steps.

These mistakes are particularly troubling because the resulting output can appear professional, complete, and convincing.
There are two broad approaches to improving the reliability of AI-assisted economics research.

**Approach 1: Better harness engineering**
Researchers and developers are building increasingly sophisticated AI research workflows.
Examples include Pedro Sant'Anna's academic workflow, Claude Code-based research systems, and emerging integrated agent platforms.
These systems improve reliability through structured workflows, specialized skills, verification procedures, and multi-agent collaboration.

**Approach 2: Better underlying models**
AI developers can improve models through training, reinforcement learning, evaluations, and domain-specific feedback.
However, both approaches face a deeper problem:
How do we determine whether an AI agent is actually good at economics research?
Researchers and engineers are building better tools, but there is no sufficiently established, comprehensive, and widely accepted standard for evaluating the scientific quality of AI-assisted economics research.
Existing scientific-agent benchmarks, including Stanford's Terminal-Bench-Science, provide valuable methodological foundations.
Nevertheless, the particular challenges of economics research require careful adaptation.
Our project aims to produce a rigorous, economics-specific benchmark that can help:

* AI developers identify weaknesses in models' economics research capabilities.
* Harness engineers evaluate whether their workflows improve research reliability.
* Economists assess which AI systems can be trusted for particular research tasks.
* The broader research community develop more transparent standards for AI-assisted empirical research.

Please carefully review existing economics and social-science AI benchmarks before asserting novelty. We need to identify exactly what our project adds beyond existing replication, coding, and scientific-agent evaluations.

## 3. Core Benchmark Construction Method

Our proposed construction approach is based on actual research published in leading economics journals.
We want to leverage economists' accumulated experience, especially their understanding of the decisions and mistakes that materially affect a paper's scientific credibility.

### 3.1. Two contribution pathways

**Path A: Reproducing a selected paper**
We prepare a curated collection of papers from the Top Five economics journals, potentially extending later to leading field journals.
A contributing economist selects a paper and prepares a correct replication package.
Where possible, the contributor uses publicly available replication materials, supplementing them with independently verified implementations.

**Path B: Contributing one's own paper**
Ideally, an original author contributes their own paper and its existing replication package.
This allows us to capture knowledge that may not be fully documented in the published article, such as difficult implementation decisions, rejected alternatives, methodological challenges, and errors encountered during research.
Both pathways should ultimately produce standardized benchmark contribution packages.

### 3.2. Correct replication package

Each contribution should include a scientifically validated implementation of the relevant research task.
Depending on the paper, this may include:

* Research data, where legally distributable.
* Data documentation and variable definitions.
* Replication code.
* Software and dependency specifications.
* Sample construction procedures.
* The target estimators and identifying assumptions.
* Expected numerical results.
* Important intermediate outputs.
* Instructions for reproducibility.

The correct package provides evidence of how the research task should be implemented.
However, matching published coefficients does not automatically establish scientific correctness.
The replication should be independently checked when feasible.

### 3.3. Deliberately flawed replication packages

This is a central innovation we want to explore.
We will ask expert contributors to identify plausible, scientifically consequential mistakes that could occur when implementing the paper's research design.
For example, a researcher may know that a particular estimation choice was essential because a more obvious alternative would have produced an invalid or misleading result.
We want to make that knowledge explicit.
For each identified mistake, we ideally obtain:

1. A description of the mistake.
2. The methodological or economic reasoning that makes it incorrect.
3. Why the mistake is realistic and easy to overlook.
4. The specific implementation change that introduces the mistake.
5. A deliberately incorrect version of the replication code.
6. The results produced by the incorrect implementation.
7. The difference between the correct and incorrect outputs.
8. The scientific consequences of the error.
9. A procedure for detecting or verifying the mistake.
10. Evidence that the error is genuinely incorrect, rather than an alternative valid approach.

The correct and incorrect replication packages jointly form the empirical foundation of our benchmark.
We want mistakes that are meaningful from an economist's perspective.
We do not want arbitrary coding bugs, formatting problems, artificial puzzles, or ambiguous tasks that are difficult only because the instructions are poor.

### 3.4. What distinguishes a top-journal paper from a weaker one?

An additional objective is to extract the methodological knowledge underlying high-quality research.
What important research decisions helped make a paper sufficiently convincing for a leading journal?
Which mistakes, if introduced, would substantially weaken its scientific contribution?
For example:

* What identification problem did the authors resolve?
* Which robustness check addressed an important alternative explanation?
* Why was one estimator preferable to an apparently reasonable alternative?
* Which seemingly minor implementation detail was critical to the interpretation?
* What methodological shortcut would have undermined the paper's conclusions?

Contributors may express these intuitions in terms of what makes a paper suitable for a top journal rather than a lower-ranked journal.
However, journal placement is not an objective ground-truth label for methodological quality.
We should translate these intuitions into explicit, scientifically defensible criteria, rather than asking an AI system to predict journal rankings.

### 3.5. From replication packages to benchmark tasks

An important distinction:
The correct and incorrect replication packages are source materials for benchmark construction. They are not necessarily the benchmark tasks themselves.
We need to transform these materials into precise, solvable, verifiable tasks.
Possible task types include:

**Research Execution**
Given the data and research instructions, can an AI agent correctly implement the intended empirical analysis?

**Error Detection**
Given an apparently legitimate research implementation, can the agent identify a scientifically consequential mistake?

**Error Correction**
Can the agent repair the implementation while preserving the intended estimand and research design?

**Identification and Methodological Reasoning**
Can the agent recognize a critical identification assumption, explain a relevant threat, and determine whether available evidence addresses it?

**Research Interpretation**
Can the agent distinguish evidence-supported claims from invalid or overextended interpretations?

These task categories may require different evaluation methods.
Please investigate which should be included in the first release and which require additional methodological development.

## 4. Benchmark Quality Standards

A central methodological reference is:
Ivan Bercovich (2026), "Good Benchmarks"
https://arxiv.org/abs/2607.12217v1
Please read the original paper carefully.
Use its criteria for good benchmark tasks to guide our construction process.
We are especially interested in:

* Verifiability.
* Clear task specifications.
* Solvability.
* Real-world scientific relevance.
* Intrinsic, meaningful difficulty.
* Outcome-based evaluation.
* Stable and reproducible evaluation environments.

Do not treat these as a checklist that can be satisfied with generic statements.
Instead, translate the criteria into an operational rubric that expert contributors and reviewers can apply to individual economics tasks.
For instance:

* Can the task distinguish correct economic reasoning from plausible but incorrect reasoning?
* Does the task evaluate a capability that matters in actual economics research?
* Is the task's difficulty intrinsic, or does it arise from missing instructions?
* Can alternative correct implementations receive credit?
* Is there a defensible ground truth?
* Can the expected result be independently verified?
* Can the task be completed using only the information legitimately available to the evaluated agent?

**Verifier validation**
We also want to develop a rigorous validation procedure.
A benchmark task should ideally have:

* At least one validated correct implementation.
* Alternative valid implementations where feasible.
* One or more scientifically meaningful incorrect implementations.
* A verifier that accepts correct results and rejects incorrect results.
* Independent review of the task and verifier.

Investigate the usefulness of:

* Oracle tests.
* Negative-control tests.
* Mutation testing.
* Metamorphic testing.
* Independent reference implementations.
* Expert review.
* Adversarial testing against shortcuts and hard-coded answers.

A deliberately flawed implementation is not sufficient by itself to establish that a task is good.
For example, a flawed procedure may occasionally produce the same numerical answer as the correct one.
Similarly, some identification assumptions cannot be verified directly from observational data.
We should distinguish computational correctness, statistical validity, and identification validity.
Do not impose artificial binary answers on genuinely contested or underidentified methodological questions.

## 5. The Central Contribution Experience: An AI-Guided Expert Interview

Regardless of which technical architecture we choose, the most important functional component will be an LLM-guided conversation that helps economists identify and formalize valuable benchmark tasks.
I have a reference skill:
https://github.com/pedrohcgs/claude-code-my-workflow/blob/main/.claude/skills/interview-me/SKILL.md
Please read it carefully.
This skill is designed to transform a fuzzy research idea into a structured research specification.
I like its general approach:

* Structured but adaptive conversations.
* One focused question at a time.
* Follow-up questions driven by previous responses.
* Progressive clarification of concepts.
* Explicit probing of research assumptions.
* A structured written output at the end.

However, our objective is fundamentally different.
We are not interviewing an economist to generate a new research proposal.
We are interviewing an economist to discover scientifically consequential mistakes and critical research decisions in an existing paper, and to turn that knowledge into verifiable benchmark tasks.
We need to create our own specialized interview protocol.

### 5.1. Desired behavior

The interviewer should:

* Begin by understanding the paper and its empirical strategy.
* Use the paper and replication materials as evidence whenever possible.
* Ask one or two focused questions per turn.
* Avoid presenting a long questionnaire.
* Build on the economist's previous answers.
* Probe vague explanations until the underlying economic reasoning is clear.
* Ask for concrete estimators, assumptions, code locations, data operations, or expected consequences.
* Distinguish established mistakes from methodological disagreements.
* Ask the economist to explain why an error is consequential.
* Explore how the error might be reproduced and detected.
* Avoid leading the contributor into agreeing with suggested mistakes.
* Avoid inventing errors merely to fill a template.
* Summarize emerging findings and allow corrections.
* Know when to stop asking questions.

The conversation should resemble a productive methodological discussion between experienced economists.

### 5.2. Possible interview stages

* Stage 1: Understand the Paper — What is the research question, empirical strategy, and main contribution?
* Stage 2: Identify the Critical Scientific Decisions — Which decisions were especially important for achieving credible results?
* Stage 3: Discover Failure Modes — What plausible mistakes could have undermined the analysis?
* Stage 4: Examine Consequences — What would these mistakes change in the estimation, statistical inference, identification, or interpretation?
* Stage 5: Operationalize the Mistakes — Can we construct executable erroneous implementations and document their consequences?
* Stage 6: Evaluate Task Quality — Can the mistake be turned into a realistic, well-specified, solvable, and verifiable benchmark task?
* Stage 7: Finalize and Review — Does the proposed task faithfully reflect the contributor's scientific reasoning?

These stages are preliminary and may be revised.
The interaction should be adaptive rather than mechanically following a predetermined sequence.

### 5.3. Example questioning

For instance, the interviewer might ask:
"What was the most difficult empirical challenge you encountered while developing this paper?"
After the economist responds:
"Suppose a research assistant overlooked that challenge. What apparently reasonable approach might they have taken instead?"
Then:
"What would that change in the estimated quantity or the causal interpretation?"
Then:
"Could we reproduce this mistake by modifying a specific part of the replication code?"
Finally:
"How could an independent verifier distinguish the correct implementation from this mistake?"
These are examples of the desired reasoning progression, not mandatory questions.

### 5.4. Structured outputs

Each interview should progressively produce a structured task specification.
Possible fields include:

* Paper metadata.
* Contributor metadata and relationship to the paper.
* Research objective.
* Empirical design.
* Target AI capability.
* Critical scientific decision.
* Plausible mistake.
* Reason the mistake is scientifically consequential.
* Correct implementation.
* Incorrect implementation.
* Expected and observed outputs.
* Ground-truth evidence.
* Verification strategy.
* Alternative valid solutions.
* Task-quality assessment.
* Data and software requirements.
* Unresolved concerns.
* Expert review status.

Please propose a suitable machine-readable schema.
Preserve the distinction between:

1. Contributor-facing information.
2. Internal task construction and validation materials.
3. Agent-facing benchmark instructions.
4. Hidden evaluation materials.

The evaluated AI agent must not inadvertently receive the correct answer or the known-error labels.

### 5.5. Human authority

The LLM is an interviewer and research assistant.
It is not the ultimate scientific authority.
The economist must be able to edit, reject, refine, or withdraw suggestions.
The system should make clear which statements came from the contributor, which came from the LLM, and which have been independently validated.

## 6. Two Alternative System Architectures

This is the central architectural decision we need to study.
Please design both options seriously and compare them on equivalent assumptions.
Neither should be treated as a strawman or a temporary fallback.
The scientific workflow, contribution schema, quality standards, and expected outputs should remain as consistent as possible across the two architectures.

### OPTION A — We Build and Operate a Hosted Contributor Platform

Under this approach, our research team builds and operates a dedicated contributor-facing web application.
An economist visits our website and completes the entire contribution workflow through an interactive interface.
We provide the application, the LLM-powered interview, and the relevant backend services.

**Expected contributor experience.** The contributor:

1. Opens the Economics Benchmark website.
2. Reads an introduction explaining the project and its academic motivation.
3. Chooses English or Chinese.
4. Selects a paper from our curated collection or contributes their own.
5. Uploads or references permitted replication materials.
6. Enters an AI-guided interview.
7. Works with the AI interviewer to identify critical research decisions and scientifically consequential errors.
8. Develops candidate benchmark tasks and associated replication materials.
9. Reviews the resulting structured contribution.
10. Submits it to our project team.

The interface should clearly show progress and explain what is expected at every stage.

**Technical questions.** Please investigate:

* Suitable frontend and backend architectures.
* LLM API integration and model selection.
* Conversation-state management.
* Document and code ingestion.
* Secure handling of contributor materials.
* Whether code should execute on our servers, in isolated environments, or on the contributor's computer.
* Integration with Stata, R, Python, and other research software.
* Authentication and contributor identity.
* Persistent drafts and revision history.
* Cost controls and usage limits.
* Export and submission mechanisms.
* Human review and feedback workflows.
* Infrastructure monitoring, deployment, and maintenance.

A key question is whether a hosted interview necessarily requires hosted code execution.
Please consider designs where the conversation is hosted but sensitive code or datasets remain under the contributor's control.

**Potential advantages.** The platform might offer a more accessible experience for senior economists who do not use terminal-based AI tools.
It could also provide consistent model behavior, centralized version control, standardized interactions, and easier contribution management.

**Potential disadvantages.** We may need to bear significant costs for LLM inference, hosting, engineering, security, storage, maintenance, and contributor support.
The handling of potentially sensitive research materials may be particularly challenging.
Please assess these advantages and disadvantages rather than assuming them.

### OPTION B — Contributors Run Our Claude Code Skill Locally

Under this approach, we do not initially develop a full hosted AI application.
Instead, we develop a well-designed, reusable Economics Benchmark Contributor Skill.
Contributors install or clone our project repository and run the skill within their own Claude Code environment.
They can use Claude Opus 5.5, if available to them, or another sufficiently capable model.
The skill performs the guided interview and helps the contributor construct and validate benchmark materials.

**Expected contributor experience.** The contributor:

1. Visits our public project page or GitHub repository.
2. Reads the project introduction and contribution guidelines.
3. Downloads or clones the contributor toolkit.
4. Opens the toolkit in Claude Code.
5. Selects English or Chinese.
6. Invokes our contribution skill.
7. Provides the paper and existing replication materials.
8. Participates in an adaptive methodological interview.
9. Uses the AI assistant to inspect code, identify candidate errors, and construct flawed implementations.
10. Runs appropriate local validation procedures.
11. Reviews and approves the resulting materials.
12. Exports a standardized contribution package.
13. Submits it to our project team.

The skill should handle progress tracking, intermediate records, structured specifications, and export preparation.

**Technical questions.** Please investigate:

* Claude Code skill architecture and packaging.
* Whether to distribute the workflow as a standalone skill, plugin, or repository template.
* Installation and update procedures.
* Supporting scripts and reference files.
* Local conversation state and checkpointing.
* Integration with existing replication repositories.
* Stata, R, Python, and other software dependencies.
* Safe execution and preservation of original files.
* Local validation and test generation.
* Automatic generation of structured task specifications.
* ZIP or GitHub-based submission.
* Versioning and compatibility.
* Bilingual conversation behavior.
* User support and troubleshooting.

The workflow should preserve the original replication package and construct deliberate errors in separate files or directories.
Changes should be auditable.
The skill should never silently overwrite the researcher's original work.

**Potential advantages.** This may substantially reduce our hosting and model-inference expenses.
It also provides direct access to the contributor's local research environment, where data, code, and scientific software may already be configured.
We can focus development effort on the quality of the interview, task specifications, and validation process.

**Potential disadvantages.** Contributors need access to Claude Code, suitable models, and potentially relevant research software.
Some senior economists may not want to install or operate such tools.
Model behavior may also differ depending on contributors' versions, settings, and model access.
Local code execution does not guarantee offline inference. Contributors must understand what information may be transmitted to an external model service.
Please assess these advantages and disadvantages rather than assuming this architecture is necessarily superior.

**Accessibility and research assistants.** For both approaches, consider whether a senior economist could participate primarily through the interview while a research assistant handles code execution and technical details.
We should preserve the economist's intellectual contribution without requiring every contributor to be proficient in software engineering.

## 7. Required Comparison of Option A and Option B

I want to discuss these alternatives with my academic collaborators.
Therefore, the comparison must be decision-oriented, balanced, and sufficiently concrete.
Please produce two complete, comparable designs.
For each approach, explain:

* What the contributor actually experiences.
* What we need to build.
* What third-party tools or services we depend on.
* Who pays for LLM inference and computation.
* How replication materials are processed.
* How the expert interview operates.
* How correct and incorrect packages are generated.
* How outputs are validated.
* How contributions are submitted.
* How the system handles data privacy and licensing.
* What maintenance and support our team must provide.
* How the system could scale to many international contributors.

**Comparison dimensions.** Evaluate both architectures against at least these dimensions:

* Scientific quality — Can we maintain consistent task definitions, interview behavior, and verifier standards?
* Contributor accessibility — How difficult is it for a nontechnical economist to participate?
* Expert engagement — Which approach better supports thoughtful, substantive contributions from leading researchers?
* Development effort — How much engineering work is required for a functional MVP?
* Operating costs — How do model inference, compute, storage, and maintenance costs differ?
* Cost distribution — Which costs are paid by our team, and which are shifted to individual contributors?
* Privacy and confidentiality — How are unpublished code, restricted datasets, and sensitive research materials handled?
* Reproducibility — How easily can we reproduce submitted implementations and verify their results?
* Quality control — How do we enforce consistent contribution standards?
* Version management — How do we update the interview protocol or task-quality rubric without breaking existing contributions?
* Scalability — How does each option perform as the number of contributors and tasks grows?
* Long-term sustainability — Which architecture is easier to maintain across multiple years?

**Cost and effort estimates.** Where possible, provide realistic engineering-effort and operational-cost estimates.
State assumptions explicitly, including contributor count, average interview length, expected model usage, file sizes, and compute requirements.
Do not invent precise prices or imply that estimates are verified if they are not.
Distinguish:

* Initial development costs.
* Fixed operating costs.
* Variable costs per contribution.
* Contributor-side costs.
* Ongoing maintenance effort.

A simple scenario analysis for 10, 50, and 200 contributors would be useful if adequate assumptions can be established.

**Hybrid possibilities.** Also consider whether a hybrid architecture might eventually be appropriate.
For example:

* Hosted onboarding and project introduction, with local research execution.
* A shared interview protocol that can run in both the web interface and Claude Code.
* A lightweight website plus a downloadable contribution skill.
* A hosted interface for nontechnical experts and a local skill for technically experienced contributors.

However, do not use a hybrid proposal to avoid evaluating the two main options separately.
The primary output must preserve a clear comparison between Option A and Option B.

## 8. Submission and Contribution Management

We have also not decided how contributors should submit their completed work.
Possible approaches include:

* Email submission — Contributors export a standardized package and send it to our team.
* GitHub submission — Contributors submit through a pull request to a dedicated repository.
* Hosted submission — The application provides a secure upload workflow.
* Hybrid submission — Contributors choose between simpler and more technical submission paths.

Please evaluate these approaches independently from the two interface architectures.
In particular, do not assume that a local Claude Code Skill must use GitHub submission, or that a hosted application must maintain its own submission database.
We need to consider:

* Convenience for contributors.
* Access and permission management.
* Confidential materials.
* File size and data licensing.
* Automated validation.
* Reviewer workflows.
* Version history.
* Auditability.
* Future benchmark publication.

The initial submission system should be simple, but the underlying contribution package should be standardized.

## 9. Bilingual Design

Both architectures must support English and Simplified Chinese from the beginning.
The user should be able to select their preferred language.
Language support includes:

* Project introduction.
* Onboarding.
* Workflow guidance.
* AI interviews.
* Scientific terminology.
* Validation feedback.
* Contribution summaries.
* Export instructions.
* Documentation.

Use a language-independent task schema.
Preserve contributors' original statements. If translated versions are created, distinguish machine-generated translations from original responses.
For the hosted architecture, investigate an appropriate internationalization framework.
For the local skill, investigate how language selection should control the interview and generated documents without duplicating the entire scientific protocol.
The system should be extensible to additional languages in the future.

## 10. Scientific and Engineering Safeguards

The project must maintain several important distinctions.

* **A. Task quality versus task difficulty.** We are not trying to make tasks difficult through ambiguity or hidden information. We want realistic challenges that distinguish reliable economic reasoning from plausible mistakes.
* **B. Correct output versus correct research procedure.** A correct numerical estimate does not guarantee a correct research design. A task's evaluation should match the capability it claims to measure.
* **C. Scientific judgment versus executable verification.** Not every methodological concern can be evaluated using a simple numerical test. We need explicit procedures for distinguishing objectively verifiable tasks from tasks requiring expert judgment.
* **D. Contributor-generated material versus independently validated benchmark content.** A contributor's submission should initially be treated as a candidate task. It should pass independent checks before inclusion in an official benchmark release.
* **E. Local execution versus data privacy.** Running code locally does not automatically mean that data remain private when a remote model is involved. The system must clearly communicate relevant data flows and permissions.
* **F. Benchmark construction versus benchmark leakage.** Reference solutions, deliberately incorrect implementations, verification criteria, and hidden test data should not inadvertently become visible in evaluated agents' task environments.
* **G. Real errors versus artificial mutations.** A useful error should correspond to a plausible mistake in actual research practice. Artificial code modifications are valuable for testing a verifier, but they do not automatically constitute high-quality economics benchmark tasks.

## 11. Expected Project Deliverables

Before extensive implementation, I want the following design documents.

* **Deliverable 1 — Research and Methodology Review.** Review the reference literature and existing benchmark projects. Explain: what current benchmarks measure; how they collect expert contributions; how tasks are constructed and verified; how our correct-versus-incorrect replication approach differs; which parts of our proposal require further methodological validation.
* **Deliverable 2 — Benchmark Construction Protocol.** Develop a complete workflow covering: Paper selection → Correct replication → Expert interview → Critical error identification → Erroneous implementation → Task construction → Verifier development → Independent review → Benchmark admission. Identify which stages can be automated and which require human scientific judgment.
* **Deliverable 3 — Expert Interview Skill Specification.** Develop a reusable, model-agnostic conversational protocol inspired by the `interview-me` skill. It should define: interview objectives; interview stages; adaptive question selection; follow-up strategies; evidence collection; error-discovery procedures; scientific quality checks; stopping conditions; structured outputs; human review requirements. For Option B, this should be directly implementable as a Claude Code Skill. For Option A, the same interview logic should be reusable in the hosted application.
* **Deliverable 4 — Contribution Data Schema.** Define a standardized, language-independent format for storing: paper information; correct replication materials; incorrect replication materials; interview records; error descriptions; verification evidence; benchmark task specifications; reviewer decisions; submission metadata. Avoid coupling the schema to either frontend architecture.
* **Deliverable 5 — Option A: Hosted Architecture Proposal.** Provide an architecture diagram, contributor journey, recommended technology stack, component responsibilities, hosting requirements, expected costs, major risks, and a realistic MVP implementation plan.
* **Deliverable 6 — Option B: Local Skill Architecture Proposal.** Provide an architecture diagram, contributor journey, proposed repository structure, skill design, supporting scripts, installation process, expected contributor requirements, major risks, and an MVP implementation plan.
* **Deliverable 7 — Architecture Decision Brief.** Produce a polished, concise report suitable for discussing with my collaborators. Include: a one-page executive summary; a side-by-side comparison of both options; the key tradeoffs; cost and effort assumptions; major scientific and operational risks; conditions under which each option would be preferable; possible hybrid strategies; decisions we need to make before implementation. A recommendation is welcome, but it must follow the comparison rather than replace it.
* **Deliverable 8 — Pilot Evaluation Plan.** Design a pilot using one published economics paper and its replication materials. The pilot should involve: one validated correct implementation; at least one plausible, scientifically consequential error; an expert-guided interview; an erroneous implementation and its results; a proposed benchmark task; an initial verifier; a standardized contribution package. The same scientific content should be used to evaluate the two alternative contribution workflows. Design the pilot so that we can compare actual contributor experience rather than relying exclusively on theoretical architecture arguments.

## 12. Proposed Development Process

I want the project to proceed in stages.

* **Phase 1 — Discovery.** Inspect the repository and read the reference materials. Identify existing assets, relevant tools, methodological concerns, and architectural dependencies. Do not start building the frontend or skill yet.
* **Phase 2 — Shared Methodology.** Define the benchmark construction pipeline, task-quality rubric, expert interview protocol, and standardized contribution schema. These should be reusable across both architectures.
* **Phase 3 — Parallel Architecture Design.** Develop Option A and Option B as two complete candidate designs. Use comparable levels of detail and consistent assumptions. Do not favor whichever option is easier for you to implement.
* **Phase 4 — Collaborator Decision Package.** Prepare the side-by-side architecture comparison and executive summary. Clearly identify unresolved decisions. At this stage, we will discuss the designs with collaborators and decide whether to select one architecture, develop a hybrid, or prototype both.
* **Phase 5 — Prototype and Pilot.** Only after reviewing the architectural decision should we proceed with implementation. Start with the smallest functional vertical slice necessary to evaluate the contributor experience.
* **Phase 6 — Validation and Iteration.** Test the workflow using actual or simulated expert contributions. Evaluate the scientific quality of the resulting tasks, the usefulness of the interview, and the reliability of the verification process. Use the findings to improve the system before recruiting a larger contributor network.

## 13. Repository Organization and Project Memory

Please inspect the existing repository before proposing changes.
If this is a new repository, propose a clean structure separating:

* Research and methodological references.
* Product requirements.
* Architecture decisions.
* Interview skill instructions.
* Contribution schemas.
* Validation utilities.
* Frontend implementation, if selected.
* Local skill implementation, if selected.
* Pilot materials.
* Tests and quality assurance.
* Generated reports.
* Contributor documentation.

Maintain an explicit distinction between:

* **Decided:** Requirements that we have already agreed upon.
* **Proposed:** Recommendations that require review.
* **Open:** Questions that have not yet been resolved.
* **Rejected:** Alternatives we considered but decided not to pursue, with reasons.

Do not silently convert proposals into decisions.
Keep documentation concise enough to be useful but detailed enough to prevent repeated discussions.

## 14. Immediate Assignment

Start by reading the following sources:

1. Good Benchmarks — https://arxiv.org/abs/2607.12217v1
2. Claude Code academic workflow — interview-me skill — https://github.com/pedrohcgs/claude-code-my-workflow/blob/main/.claude/skills/interview-me/SKILL.md
3. Stanford Terminal-Bench-Science — https://github.com/harbor-framework/terminal-bench-science
4. Claude Code documentation, particularly the current skills, plugins, model selection, and local execution capabilities.
5. Relevant existing economics and social-science agent benchmarks, including computational replication and econometric evaluation projects.

Verify the relevant details using the original sources rather than relying on my descriptions alone.
Then prepare an initial assessment addressing five questions.

* **Question 1 — Scientific feasibility.** Can our proposed approach of combining correct and deliberately erroneous replication packages produce scientifically meaningful, objectively verifiable economics benchmark tasks? What are its strongest methodological features, and where might it fail?
* **Question 2 — Expert interview design.** How can we use an adaptive AI-guided interview to extract economists' tacit knowledge about consequential research mistakes? How do we avoid leading questions, fabricated errors, and superficial methodological discussion?
* **Question 3 — Hosted contributor platform.** What would a rigorous but reasonably lightweight hosted platform require? How should the frontend, LLM services, replication materials, execution environment, and contribution workflow interact?
* **Question 4 — Local Claude Code Skill.** How would we implement the same contribution experience through a locally executed Claude Code Skill? What are the requirements, benefits, limitations, and costs for both contributors and our research team?
* **Question 5 — Architectural comparison.** Which tradeoffs should I discuss with my collaborators before choosing between these alternatives? What information should we collect through a pilot to make the decision more evidence-based?

## 15. Final Working Instructions

For this first stage:

1. Inspect the repository.
2. Review and verify the reference materials.
3. Critically evaluate the proposed benchmark construction methodology.
4. Design a shared scientific workflow and interview protocol.
5. Develop two comparable architectural proposals.
6. Produce a collaborator-ready decision brief.
7. Identify the most important open questions.

Do not commit to Option A or Option B.
Do not start extensive implementation.
Do not treat a hosted platform as inherently more professional or a local skill as inherently more cost-effective without examining the assumptions.
The central priority is to establish a credible method for transforming economists' research experience into high-quality, independently verifiable benchmark tasks.
The two technical architectures are alternative ways of implementing that same scientific mission.
Our goal is not merely to build a platform where economists can submit replication packages.
Our goal is to create a reliable, scalable process through which economists can teach AI evaluation systems what genuinely good economics research requires—and which mistakes a competent research agent must be able to avoid, recognize, or correct.
