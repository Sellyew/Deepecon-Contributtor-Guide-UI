# Research Lead's Revised Requirements (2026-11-06)

*Verbatim record of the research lead's message of 2026-11-06. Only Markdown formatting was added; the text is unchanged. Never edit this file. The message was accompanied by the team's handover package, summarized in [2026-11-05-team-handover-plan.md](2026-11-05-team-handover-plan.md).*

---

This is not what I had in mind. I want to clarify several important requirements.

First, I do not want any project content or contributor data to be sent to Anthropic or any other external AI provider. I will use DeepSeek with my own API key if needed, or deploy a model locally. We should have full control over model selection, deployment, and data transmission. The system must not depend on Anthropic's infrastructure or require contributors to use Claude Code, Team, or Enterprise subscriptions.

Second, the first version of the frontend should be much simpler than what you have proposed. We will contact the paper authors directly, so the paper-selection interface should already include each author's own paper as an available option. We do not need a complex paper discovery or onboarding process.

Third, we have already prepared the potential errors locally. We do not need an AI agent to interview authors from scratch to discover mistakes or generate flawed replication packages. Instead, contributors should be able to review the predefined errors, select the ones they consider appropriate, and optionally suggest additional errors or provide comments.

The frontend should therefore focus on two things:

1. Selection: Allow authors to select their paper and review, select, reject, or supplement the candidate errors we have already prepared.
2. Guidance: Clearly explain what materials the authors need to provide, how to prepare them, and how to submit their contribution.

I will provide an example contribution package prepared by one of my coauthors in my next message. Please examine that package carefully and use it as the primary reference for designing the actual contribution workflow, data structure, and submission requirements. Do not assume its contents before reviewing it.

Finally, data privacy is a non-negotiable requirement. I do not want any research data, replication code, paper materials, contributor responses, or intermediate outputs transmitted to Anthropic or any other third-party AI service. If we need an LLM, I will handle its deployment myself. Any external API integration must be optional, explicitly configured, and disabled by default. Using my own DeepSeek API key would still involve transmitting data to an external provider unless I deploy the model locally, so the architecture must clearly distinguish these two cases.

Please revise the entire MVP proposal accordingly. Do not continue designing an expensive AI-agent workflow, a Claude Code-based contributor system, or an elaborate expert interview process.

Our immediate goal is a lightweight, privacy-preserving, bilingual contributor interface that lets invited authors select from prepared benchmark materials, provide feedback, and follow clear instructions for submitting the required replication packages.

Please wait until I provide the example package before finalizing the contribution schema or implementation plan.
