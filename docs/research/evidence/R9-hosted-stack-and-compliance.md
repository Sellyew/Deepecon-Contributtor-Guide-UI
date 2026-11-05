# R9: Hosted-platform stack, cost anchors, and compliance for Option A

| Field | Value |
|---|---|
| Topic | Technology choices, verified cost anchors, and compliance constraints for **Option A** (hosted bilingual contributor platform with an LLM interviewer on the project's Claude API account). Includes a fact-check of the `[U]` claims in the Option A, cost, bilingual, submission and pilot drafts. **Neither architecture is selected;** this note informs both the Option A design and the A-versus-B comparison. |
| Date | 2026-11-05. All URLs accessed 2026-11-05. |
| Author | research agent |
| Scope | (1) open-source AI-interview platforms and chat frameworks; (2) internationalization and CJK typography; (3) authentication; (4) secure storage; (5) sandboxed execution, R/Python, Stata; (6) cost anchors and a small-deployment estimate; (7) compliance and ethics (Anthropic terms, GDPR, PIPL, reachability, ICP, IRB); (8) submission-related vendor facts; (9) fact-check table; a proposed reference stack with two alternatives. |
| Evidence labels | **[P-full]** primary source read in full. **[P-page]** primary landing page, official doc page, pricing page, README, licence or repository file read by me. **[S]** secondary (WebSearch summaries of pages I did not open; unofficial copies of legal texts). **[U]** unverified, including my own background knowledge. |
| Evidence limits | (a) The shared WebSearch budget for this turn ran out after 7 successful queries of mine (the 8th was refused). (b) Two host failures (ideas.repec.org, sentry.io) triggered the stop rule, so no further new hosts were tried. (c) Several vendor facts come from the vendors' **public documentation repositories** (the sources of their docs and pricing pages), read through raw.githubusercontent.com at the commits listed in "Sources". These are labelled [P-page] but can lag or lead the live sites. (d) Chinese legal texts were read from an **unofficial** GitHub mirror and are labelled [S]. Nothing here is legal advice; every compliance point is flagged for legal review. |
| Relation to other notes | Overlaps R3 (access, pricing, policy) on Anthropic's regional policy and data terms, R2 (Claude Code platform) on the Agent SDK, and R7 (expert elicitation and AI interviews) on the Geiecke & Jaravel platform; R7's licence and commit facts agree with §2.1. Where this note touches those topics it reports only what the sources say; R2 and R3 should reconcile. |

## Summary (10 bullets max)

1. **Anthropic's regional policy is the most consequential compliance finding.** The Supported Regions Policy (version effective **2026-11-12**) lists neither mainland China nor Hong Kong or Macau. It names as unsupported "use by persons while physically located in an unsupported region, including users and personnel of otherwise supported entities". The Commercial Terms bind "Customer and its Users", defined as the customer's "own customers and end users", to that policy (§A.1, §D.2) [P-page]. This applies to Option A's contributors. The policy's product list also includes Claude Code, so it reaches Option B too. Legal review is needed before recruiting anyone located there (O-007).
2. **Anthropic's data terms are favourable, but data at rest sits in the US.** The Commercial Terms (effective 2025-06-17) say "Anthropic may not train models on Customer Content from Services", and they incorporate a DPA (effective 2025-02-24) with EU SCCs Modules 2/3, a UK Addendum and a Swiss Addendum [P-page]. Workspace geo, which sets where data is stored at rest, is **`us` only**. Inference geo is `global` (default) or `us` at 1.1× price [P-page]. EU contributors' data therefore reaches the US under the SCCs.
3. **Managed Agents: the $0.08 per session-hour figure is confirmed; the availability claim needs correcting.** Runtime is billed only while a session is `running`; idle time is free. Hard per-session USD budgets exist. The product is beta on the **Claude API, Claude Platform on AWS and Claude Models on Google Cloud (Anthropic-managed)**, so "first-party API only" is inaccurate. It is not ZDR-eligible, and session transcripts persist until deleted. The cloud sandbox runs Ubuntu 24.04 with up to 8 GB RAM and 10 GB disk. Python is pre-installed and R is not; packages can be installed via `apt` and `pip` [P-page]. The code-execution tool is Python 3.11 only, has no internet and no runtime installs, and costs $0.05 per container-hour after 1,550 free hours per month [P-page].
4. **The Geiecke & Jaravel platform is a source of interview patterns, not a base to build on.** It lives at `github.com/friedrichgeiecke/interviews` [P-page]:
   - **Stack and storage.** Python and Streamlit; transcripts are stored as files on the instance; logins are "very basic"; deployment is documented as an Azure Web App.
   - **Licence.** The code is under PolyForm Noncommercial 1.0.0, which permits use by educational and public research organizations.
   - **Cost.** The press reports about £3–4 per participant, including recruitment [S].
   - **Fit.** It has no upload, code index, dossier, database or i18n layer. Its interviewer prompt design (non-directive, one question at a time, closing codes, respondent rating of the final summary) is worth reusing.
5. **None of the off-the-shelf chat apps fits; a custom app does.** Facts per framework [P-page]:
   - **Vercel AI SDK** (Apache-2.0): routes model strings through Vercel's AI Gateway by default unless a provider package is used.
   - **Chainlit:** "community-maintained" since 2025-05-01.
   - **Open WebUI:** its licence forbids removing the branding above 50 users in a 30-day window without permission.
   - **LibreChat:** MIT. **Streamlit:** Apache-2.0.

   A staged interview with provenance tracking needs a custom app, built on the AI SDK or directly on the Anthropic SDK.
6. **i18n and fonts.** Library facts [P-page]:
   - **next-intl 4.14.9** (MIT, released 2026-10-02) supports ICU plurals/select, the App Router, Server Components and locale routing.
   - **Lingui** (PO catalogs, extraction CLI, Server Components support) is the strongest choice if the translator workflow matters most.
   - **i18next** needs a plugin for ICU.
   - **Paraglide's** README does not list Next.js.

   One Noto Sans SC variable font file is **17.8 MB** [P-page], so use system fonts or self-hosted subsets. Whether Google Fonts is reachable from mainland China is contested in secondary sources [S]; no measurement was read [U].
7. **Authentication.** Auth.js "is now part of Better Auth", and its README recommends that new projects start with Better Auth [P-page]. Better Auth has a magic-link plugin and a generic OIDC plugin with discovery [P-page]. ORCID supports OpenID Connect sign-in on its Public API [P-page]. Its public credentials are reportedly free for non-commercial use and tied to an individual's record [S]. Supabase's built-in SMTP delivers only to project team members, at **2 messages per hour** [P-page], so production needs a custom SMTP provider.
8. **Cost anchors and estimate.**
   - **Verified [P-page]:** Fly.io Machines from $2.19 per month, performance-1x with 2 GB at $33 per month; Supabase Pro $25 per month; Neon $0.106 per CU-hour plus $0.35 per GB-month; Cloudflare R2 $0.015 per GB-month with free egress; GCS Standard (us-central1) about $0.020 per GiB-month; Langfuse Core $29 per month.
   - **Not verified [U]:** Vercel Pro, Render, AWS S3 and Fargate, E2B, Modal and Sentry plan prices.
   - **Estimate:** about **$13–$210 per month** for pilot to 200 contributors, excluding inference, e-mail and paid Sentry. This is consistent with the drafts' "tens to low hundreds".
9. **PIPL and ICP rules (unofficial text copies [S]), plus two topics left unverified.**
   - **PIPL** reaches processing outside China in some cases (Art. 3(2)). Exporting personal information requires separate consent (Art. 39). Overseas processors covered by Art. 3(2) must have an in-China representative (Art. 53).
   - **2024 Provisions:** a non-CIIO processor exporting non-sensitive data of fewer than 100,000 people (cumulative since 1 January) is exempt from assessment, standard contract and certification. Notice and separate-consent duties still apply.
   - **ICP filing:** a non-commercial site offered in mainland China needs an ICP filing; Cloudflare says this includes delivery through a CDN [P-page].
   - **Unverified [U]:** StataCorp's server and container licensing terms, and US Common Rule / IRB guidance.
10. **Fact-check results and proposed stack.** I made 28 in-scope checks: 24 `[U]`-marked claims plus 4 related unmarked claims (Managed Agents availability, A2 sandbox cost, the submission note on docs.github.com, and the pilot's ethics statement). Of these, **14 are confirmed, 4 corrected, 2 partly confirmed and 8 still unverifiable**. One further discrepancy sits outside the `[U]` set: the Sonnet 5.5 cache-read price is **$0.10/MTok**, not $0.20. The **proposed reference stack** is Next.js + next-intl + Better Auth + Neon Postgres + Cloudflare R2 + the Anthropic SDK + Langfuse (EU region) + Sentry, on Fly.io in the EU. A2 adds Managed Agents or E2B. The alternatives are (1) Supabase-integrated and (2) Managed-Agents-centric.

---

## 1. Method

- **Read in full, or substantially [P-page]:**
  - Anthropic's Commercial Terms, DPA and Supported Regions Policy (www.anthropic.com).
  - Anthropic platform documentation (platform.claude.com, Markdown versions): pricing, Managed Agents overview, environments, cloud sandbox reference, sessions, code-execution tool, ZDR and retention, data residency, rate limits, Files API.
  - Google Cloud pricing pages for Cloud Storage and Cloud Run.
- **Read from vendors' public documentation repositories (raw.githubusercontent.com):**
  - Fly.io (`superfly/docs`), Supabase (`supabase/supabase`), Neon (`neondatabase/website`), Cloudflare (`cloudflare/cloudflare-docs`).
  - Langfuse (`langfuse/langfuse-docs`), Sentry (`getsentry/sentry-docs`), GitHub (`github/docs`).
- **Read from shallow or tree-only clones** (new empty directories under the scratchpad `refs/`; nothing executed):
  - `friedrichgeiecke/interviews`, `AEADataEditor/docker-stata`, `modal-labs/modal-examples`.
  - Tree listings of `e2b-dev/code-interpreter`, `e2b-dev/E2B`, `modal-labs/modal-client`, `LawRefBook/Laws`, `MicrosoftDocs/microsoft-365-docs` and `awsdocs/amazon-s3-userguide`.
- **READMEs, licences and package manifests:** Vercel AI SDK, Chainlit, Open WebUI, LibreChat, Streamlit; next-intl, i18next, react-i18next, i18next-icu, FormatJS, Lingui, Paraglide; Auth.js, Better Auth, ORCID-Source; W3C clreq, google/fonts, Source Han Sans; E2B, Daytona, Modal.
- **WebSearch:** 7 successful queries before the shared budget ran out (Geiecke & Jaravel ×4, Google Fonts in China, W3C clreq, ORCID terms). These results are [S].
- **Scripts:** my own, in a separate scratchpad directory, run with `python3 -I`, to convert HTML to text and URL-encode paths.

---

## 2. Existing AI-interview platforms and chat frameworks

### 2.1 Geiecke & Jaravel, "Conversations at Scale"

**What the sources say**

- **Identity.** The repository is `friedrichgeiecke/interviews` (commit `94297760`, 2026-02-09). Its README is titled "Conversations at Scale: Robust AI-led Interviews", cites SSRN 4974382, and gives a BibTeX entry dated 2026 [P-page]. The earlier version is CEPR DP19705 (2024), "…with a Simple Open-Source Platform" [S]. An LSE listing shows the paper as forthcoming in, or published by, the *Review of Economic Studies* (online 2026-10-27) [S].
- **Stack.** Python and **Streamlit** (`streamlit==1.54.0`). It supports the OpenAI, Anthropic (`anthropic==0.78.0`), Google and Azure APIs, and text or voice input. The full-voice interviewer is OpenAI-only [P-page].
- **Deployment model** [P-page]:
  - It runs locally (conda) or as an **Azure Web App** (Python 3.13) deployed through GitHub Actions.
  - "This version of the interview platform does not use a separate database". Transcripts, JSON backups and metadata are files on the instance, downloaded over FTPS.
  - Basic B2/B3 instances "are typically sufficient" for tests or a few participants.
- **Authentication** [P-page]:
  - Usernames and passwords live in `.streamlit/secrets.toml`. Alternatively, in a Qualtrics mode, the password is computed as `alpha + beta × username` from a random numeric ID.
  - The tutorial calls these logins "very basic" and points to Streamlit's OIDC authentication for anything stronger.
  - Partial transcripts are restored on re-login, and each username can complete only one interview.
- **Interviewer design** (`config.py`) [P-page]:
  - The system prompt is the interview outline plus general instructions plus control codes.
  - The instructions ask for "one question at a time", non-directive and non-leading questions ("never suggest possible answers"), follow-ups that elicit "palpable evidence", "cognitive empathy", and no long paraphrasing.
  - Codes `5j3k` (problematic content) and `x7y8` (end) trigger fixed closing messages in the front end.
  - At the end, the interviewer writes a summary and the respondent rates it on a 1–4 scale.
  - The default model in the shipped config is `gpt-4.1-2025-04-14`.
- **Licence** [P-page]:
  - The code is **PolyForm Noncommercial 1.0.0** and the documentation is **CC BY-NC 4.0** ("strictly for non-commercial research only").
  - PolyForm permits "any noncommercial purpose". It adds that "use by any charitable organization, educational institution, public research organization … is use for a permitted purpose regardless of the source of funding".
- **Data-protection advice in the README.** Studies "need … institutional review board / ethics committee approvals" and must tell respondents that "their interview data will be sent to third-party AI providers" [P-page].
- **Reported cost per interview.** Not found in the materials I could read. A *Times Higher Education* article reportedly estimates about **£3–4 per participant**, including Prolific recruitment [S]. The paper's own figure is [U].

**Implications (analysis)**

- **As a base for Option A: not recommended.** It lacks almost every Option A component: document and code upload, a code index and viewer, a structured dossier with provenance, a database, an i18n framework, account authentication, an RA mode, and protection of originals. Its security model (file storage on a public instance, linear-formula passwords) is unsuitable for unpublished code.
- **Licence.** University use appears permitted under PolyForm. Any sponsor or industry partner in operations, or relicensing of derived code, needs **legal review**, because derivatives inherit the noncommercial terms.
- **As a design reference: valuable.** Its prompt structure matches the brief's §5.1 behaviours. The "summary + contributor rating" step maps directly onto Stage 7 (Finalize and review). Its codes-to-UI pattern is a simple and testable way to end sessions.

### 2.2 General chat-application frameworks

| Framework | Licence and status | Facts relevant to a structured, stateful, bilingual interview with uploads | Fit for Option A |
|---|---|---|---|
| **Vercel AI SDK** (`vercel/ai`, package `ai` 7.0.163) | Apache-2.0 [P-page] | Provider-agnostic TypeScript toolkit with UI hooks for Next.js, React, Svelte and Vue, and a Next.js App Router route example. A `ToolLoopAgent` agent abstraction. "**By default, the AI SDK uses the Vercel AI Gateway**" for plain model strings; direct provider packages (`@ai-sdk/anthropic`) are also documented [P-page] | **High** for a custom UI. If used, call the Anthropic provider directly to avoid adding a gateway processor in the data path (analysis) |
| **Chainlit** (`Chainlit/chainlit`) | Apache-2.0. "**Chainlit is now community-maintained.** As of May 1st 2025, the original Chainlit team has stepped back from active development" [P-page] | Python chat UI; ships a `zh-CN` translation file (`backend/chainlit/translations/zh-CN.json`) [P-page]. File upload, OAuth and data-layer features not verified here [U] | **Medium for a pilot slice only**; maintenance risk |
| **Open WebUI** | "Open WebUI License": BSD-3 terms **plus a branding clause**. Licensees may not alter or remove "Open WebUI" branding unless end users do not exceed **50 in any rolling 30-day period**, with written permission, or under an enterprise licence [P-page] | General-purpose self-hosted chat for Ollama and OpenAI-compatible APIs; README in many languages, including 简体中文 [P-page] | **Low.** Built as a general chat hub, not a staged protocol; licence constraint |
| **LibreChat** | MIT [P-page] | Multi-user auth (OAuth2, LDAP, e-mail), agents, a code-interpreter API, file handling, translations, Langfuse trace integration [P-page] | **Low–medium.** Powerful but general; heavy to bend into a staged interview with a dossier |
| **Streamlit** | Apache-2.0 [P-page] | Used by Geiecke & Jaravel (above) | **Low–medium**, for throwaway prototypes |

**Implications (analysis).** Option A's distinctive surfaces are the progress-by-stage interview, the live dossier with provenance badges, the code viewer citing lines, diff approval, and RA hand-offs. They are product-specific. Frameworks save time on chat streaming and auth, not on these. A custom Next.js app with the Anthropic SDK (optionally the AI SDK UI hooks) is the most direct route. Chainlit is the fastest throwaway pilot path if the team prefers Python.

---

## 3. Internationalization and CJK typography

### 3.1 i18n libraries (React / Next.js)

| Library | Version, licence | ICU plural/select | Next.js App Router / Server Components | Translation-workflow tooling | Source |
|---|---|---|---|---|---|
| **next-intl** | 4.14.9 (2026-10-02), MIT | Yes: "ICU message syntax … cardinal & ordinal plurals, enum-based label selection and rich text" | Yes: "App Router, Server Components, static rendering"; internationalized routing with localized pathnames; type-safe keys | JSON catalogs; type-checked keys | [P-page] |
| **i18next / react-i18next** | 26.7.1 / 17.1.12, MIT | Only via the **i18next-icu** plugin (uses FormatJS `intl-messageformat`; with it, "only the ICU message format is respected") | Framework-agnostic; App Router integration not checked [U] | Large ecosystem [U] | [P-page] |
| **FormatJS / react-intl** | react-intl 12.1.6, BSD-3-Clause | Native ICU | Not checked [U] | `@formatjs/cli` (Rust-backed) for extraction | [P-page] |
| **Lingui** | core 6.12.0, MIT | ICU-based messages | React Server Components support; Next.js example project | **PO catalogs by default** ("which almost every translation tool understands"); CLI `extract`/`compile`/validate; SWC and ESLint plugins; comments and context for translators | [P-page] |
| **Paraglide JS** | 3.1.0, MIT | ICU MessageFormat 1 via plugin; plurals via `Intl.PluralRules` | README lists TanStack Start, SvelteKit, React Router, Astro, Vue, Solid and vanilla JS. **Next.js is not listed** | Compiler-first, typed message functions; inlang ecosystem | [P-page] |

**Implications (analysis).** next-intl is the lowest-friction choice for a Next.js App Router stack, and it covers the bilingual design's ICU and locale-prefixed routing requirements. If professional translators or reviewers will work in a TMS, Lingui's PO-file workflow is a real advantage. The choice between the two can be deferred to the prototype. The draft's claim that next-intl is "the usual choice" is a popularity claim that I could not verify.

### 3.2 CJK typography

- **Line breaking.** W3C *Requirements for Chinese Text Layout* (clreq; editor's draft in `w3c/clreq`, latest published version a 2025-03-19 Group Draft Note [S]) [P-page]:
  - Most punctuation marks are prohibited from appearing at line start or line end.
  - In mainland China, the national standard GB/T 15834—2011 sets the rules.
  - Implication: rely on browser line-breaking and test punctuation at line edges; do not hand-insert breaks.
- **Font size and loading** [P-page]:
  - The Google Fonts copy of **Noto Sans SC** is a single variable TTF of **17,772,300 bytes** (`google/fonts`, `ofl/notosanssc/NotoSansSC[wght].ttf`). Its metadata lists a `chinese-simplified` subset and OFL licensing.
  - Adobe **Source Han Sans** (SIL OFL 1.1) offers WOFF2 builds and "Region-specific Subset" variable fonts.
  - Implication: never ship a full CJK font per page. Use a system font stack first (platform availability of specific families such as PingFang SC or Microsoft YaHei is [U]), with optional self-hosted, subset WOFF2 fonts.
- **Google Fonts from mainland China** [S]. Search summaries of pages I did not open report **conflicting** evidence:
  - Vendor blogs and forum posts say it is blocked.
  - A 2018 Google Groups post, attributed to a Google Fonts programme manager, reportedly said the API works in mainland China while `fonts.google.com` does not.
  - A cdnjs GitHub issue reports blocking at one point.
  - No measurement source (for example, GreatFire or OONI) was read, so reachability remains [U]. The draft's recommendation to self-host still holds, on file-size and third-party-dependency grounds alone.

---

## 4. Authentication and identity

| Option | What the sources say | Label |
|---|---|---|
| **Auth.js** (`nextauthjs/next-auth`) | "Auth js is now part of Better Auth … We recommend new projects to start with Better Auth unless there are some very specific feature gaps (most notably stateless session management without a database)." Supports e-mail/passwordless, OAuth 2/OIDC providers, passkeys; JWTs encrypted by default (JWE). A built-in GitHub provider exists (`providers/github.ts`); **no `providers/orcid.ts`** on `main` | [P-page] |
| **Better Auth** (`better-auth/better-auth`, 1.7.17, MIT) | **Magic link** plugin ("When a user enters their email, a link is sent … when the user clicks on the link, they are authenticated"). **Generic OAuth** plugin: "add any OAuth 2.0 or OpenID Connect (OIDC) provider", with `discoveryUrl`, "PKCE and issuer validation enabled by default" | [P-page] |
| **Supabase Auth** | Built-in SMTP "is not meant for production use". It sends only to addresses in the project's team, with a limit of **2** messages per hour. Custom SMTP (Resend, AWS SES, Postmark, SendGrid, …) is required for production. Pro plan includes **100,000 MAU**, then $0.00325 per MAU | [P-page] |
| **Clerk, Auth0** | Features and prices not verified in this session | [U] |
| **ORCID OAuth / OIDC** | ORCID "supports the Basic OpenID Provider conformance profile". Clients request the `openid` scope (or `/authenticate`) and receive an `id_token` (subject = ORCID iD). Discovery at `https://orcid.org/.well-known/openid-configuration`; implicit-flow tokens last 10 minutes; the `amr` (MFA) claim is returned only on the Member API | [P-page] (`ORCID-Source/orcid-web/ORCID_AUTH_WITH_OPENID_CONNECT.md`) |
| ORCID Public API terms | Public API credentials are free for non-commercial use. They are issued after accepting the Public Client Terms, are "tied to an individual's ORCID record" and are not transferable; 100k reads/day per registered public client; the client secret must stay server-side. The Public API can be used to sign users in | [S] (search summaries of info.orcid.org pages) |
| **GitHub OAuth** | Built-in providers in Auth.js and Better Auth (above) | [P-page] |
| Users in mainland China | E-mail deliverability to Chinese providers and institutional mail, and the reachability of Google or GitHub sign-in, were not verified | [U] |

**Implications (analysis).**

- E-mail magic links (Better Auth plus a reputable SMTP provider) are the most universal sign-in method. ORCID via generic OIDC is a low-cost add-on that also verifies researcher identity.
- **Terms review:** check whether a project-level registration fits ORCID's "individual, non-commercial" Public API wording, or whether the lead's institution's ORCID membership should be used.
- Do not make GitHub or Google sign-in the only route.
- Measure magic-link delivery and latency to Chinese mailboxes (e.g., QQ, 163, university addresses) in the pilot setup test (M1).

---

## 5. Secure storage

| Need | Cloudflare R2 | Google Cloud Storage | AWS S3 | Supabase Storage |
|---|---|---|---|---|
| Price (storage) | **$0.015 / GB-month** (Standard); IA $0.01; Class A $4.50/M; Class B $0.36/M; **egress free**; free tier 10 GB-month, 1M Class A, 10M Class B [P-page] | Standard, Iowa (us-central1): **$0.000027397 per GiB-hour** (≈ $0.020/GiB-month at 730 h) [P-page] | Not verified [U] | Pro: 100 GB included, then $0.0213/GB [P-page] |
| Encryption at rest | "All objects stored in R2, including their metadata, are encrypted at rest" (AES-256, GCM), automatic; TLS in transit [P-page]; an SSE-C (customer-supplied key) example page exists in the docs tree (not read) | [U] (docs page redirected to an unreachable host) | [U] | [U] |
| Presigned upload/download | Expiry from **1 second to 7 days (604,800 s)** [P-page] | [U] | [U] | [U] |
| Size limits | Object ≤ 5 TiB less 5 GiB (4.995 TiB); single-part upload ≤ **5 GiB**; multipart ≤ 4.995 TiB, ≤ 10,000 parts [P-page] | [U] | [U] | Max upload: 50 MB (Free), **500 GB** (Pro/Team) [P-page] |
| Retention / deletion | **Bucket locks** (retention rules; strictest rule wins) and **object lifecycles** [P-page] | [U] | [U] | [U] |
| Access logs | **Audit logs** for configuration changes (free, always on); **Data Access Logs** for object operations such as `GetObject`/`PutObject` [P-page] | [U] | [U] | [U] |
| Data location | Location hints (best effort) and **jurisdictional restrictions**: `eu`, `us`, `fedramp` (FedRAMP for Enterprise) [P-page] | Many regions, including EU and Hong Kong (asia-east2) [P-page] | [U] | Single primary region per project; choose a specific EU region to pin data in the EU [P-page] |
| Malware scanning | No built-in scanner found in the docs I read [U]. **Event notifications** to a queue enable an asynchronous scan-on-arrival worker [P-page] | [U] | [U] | [U] |

**Implications (analysis).**

- R2 alone covers the platform's storage needs: encryption by default, short-lived presigned upload URLs, EU jurisdiction, object-level access logs and lifecycle deletion, at negligible cost (§7).
- **Lock versus delete.** WORM bucket locks conflict with contributors' right to withdraw (D-008) and with GDPR erasure requests. Use versioning plus audit logs rather than locks on contributor originals, and record checksums in the database.
- Scan uploads asynchronously (for example, a queue consumer running an AV engine; tool not evaluated) and never execute uploads on application servers. In A1 nothing is executed server-side.

---

## 6. Sandboxed execution, R/Python, and Stata

### 6.1 Anthropic-hosted options

**Code-execution tool (Messages API)** [P-page]:

- Runs "Python and Bash" in a sandbox with **1 CPU, 5 GiB RAM and 5 GiB disk**, Python 3.11.
- "The container has **no internet access**, so Claude can't download packages at runtime: only the pre-installed libraries are available". These include pandas, numpy, scipy, scikit-learn and **statsmodels**.
- Pricing: **free** when web search or web fetch (`_20260209`) is in the request. Otherwise 1,550 free hours per month per organization, then **$0.05 per hour per container**, with a 5-minute minimum. Execution time is billed when files are attached, even if the tool is not called.
- Not ZDR-eligible: "Container data retained up to 30 days".
- *Consequence:* no R and no Stata. This option is unsuitable for replication packages.

**Claude Managed Agents** [P-page]:

- **Status:** "Managed Agents is in beta" on the **Claude API, Claude Platform on AWS and Claude Models on Google Cloud (Anthropic managed)**, for all models. The beta header is `managed-agents-2026-04-01`. (Per the Anthropic skill reference, it is not offered on Bedrock, Vertex AI (Google-managed) or Foundry [P-page].)
- **Pricing:**
  - Tokens at model rates, plus **$0.08 per session-hour** of runtime.
  - Runtime "is measured to the millisecond and accrues only while the session's status is `running`"; idle time is not billed.
  - Runtime "replaces the code execution container-hour billing model"; the 1.1× US-inference multiplier applies; batch discounts do not.
- **Budgets:** a session budget is "a hard ceiling on the session's list cost", in US cents. The session pauses with `budget_reached`. Because "the request that crosses it completes first", spend can land slightly past the cap. A budget can be attached only at creation.
- **Sandbox:**
  - Ubuntu 24.04 LTS, x86_64, **up to 8 GB memory and 10 GB disk**.
  - Pre-installed: Python 3.10–3.13, Node.js, Go, Rust, Java, Ruby, PHP, C/C++, PostgreSQL 16, Redis 7, git, pandoc.
  - The environment `packages` field supports **apt, cargo, gem, go, npm, pip** (there is no CRAN field). Under `limited` networking, `allow_package_managers` must be true.
- **Data handling:**
  - "No feature is eligible for ZDR or HIPAA readiness"; "session transcripts persist until you delete them".
  - Workspace geo is `us` (the only option); self-hosted sandboxes keep tool execution on your own infrastructure.

### 6.2 Third-party sandboxes

| Provider | What the sources say | R / Python | Price |
|---|---|---|---|
| **E2B** | Apache-2.0 SDKs; "open-source infrastructure that allows you to run AI-generated code in secure isolated sandboxes". The code-interpreter template's default kernels are `["python", "r", "javascript", "bash", "java"]`; R is installed with `apt` `r-base` plus **IRkernel** from CRAN [P-page] | **R and Python** in the default template [P-page]; econometrics packages (fixest, did, …) not tested [U] | [U] |
| **Modal** | SDK Apache-2.0; the platform is proprietary. Images via `from_registry`, `from_dockerfile`, `apt_install`, `micromamba_install`; `modal.Sandbox.create` [P-page, SDK source] | Any image (for example, an R base image) [U: not tested] | [U] |
| **Daytona** | "**This repository is no longer maintained.** As of June 2026, Daytona's core development has moved to a private codebase"; public code remains under **AGPL-3.0** (tag v0.190.0). Sandboxes run "Python, TypeScript, and JavaScript" [P-page] | Python [P-page]; R [U] | [U] |
| **Fly Machines** | Billed by the second while running. Prices per 30 days: shared-cpu-1x/256 MB $2.19, …, performance-1x/2 GB **$33.00**, performance-2x/4 GB $66.00; stopped Machines billed only for rootfs at $0.15/GB-month [P-page] | Any OCI image [U: not tested] | ≈ $0.045/h for performance-1x (derived: $33/730 h) |
| **AWS Fargate** | Not verified | [U] | [U] |

### 6.3 Stata

- **AEA Data Editor images** (`AEADataEditor/docker-stata`, commit `fdbec27`, 2026-10-07; primary source now `ssc-ng/docker-stata`, images on Docker Hub under `sscng/…`) [P-page]:
  - "The image created by these instructions contains binary code that is © Stata. Permission was granted by Stata to Lars Vilhuber to post these images, without the license. **A valid license is necessary to build and use these images.**"
  - "You need a Stata license to run the image"; the licence file is mounted at runtime (`-v "${STATALIC}":/usr/local/stata/stata.lic`).
  - Image sizes are about 1.1–1.9 GB (`stata18-*`).
- **StataCorp's own terms** for servers, containers and cloud (concurrent-user, network or cloud licences): **not verified**. stata.com was not reachable under the stop rule, and no search was possible [U].

**Implications (analysis).**

- A hosted sandbox can serve **R and Python** (E2B ships R; Managed Agents can install R via `apt` [U: untested]).
- **Stata in A2 is blocked** until StataCorp confirms in writing which licence type permits running contributor-submitted do-files in project-operated containers.
- A1 (run kits under the contributor's own licence) remains the only Stata path that is already documented.
- If A2 is adopted, Managed Agents' hard per-session budgets are a real cost-control advantage. Its non-ZDR, persist-until-deleted transcripts require an explicit deletion job.

---

## 7. Cost anchors and a small-deployment estimate

### 7.1 Verified anchors (list prices, USD, 2026-11-05)

| Item | List price | Unit / notes | Source | Label |
|---|---|---|---|---|
| Fly.io Machine, shared-cpu-1x 256 MB / 512 MB / 1 GB | $2.19 / $3.69 / $6.70 | per 30 days continuous; billed per second; "no monthly platform fee" | `superfly/docs` `about/pricing.mdx` @941ab70 | [P-page] |
| Fly.io Machine, shared-cpu-2x 2 GB / performance-1x 2 GB / performance-2x 4 GB | $13.39 / $33.00 / $66.00 | per 30 days | same | [P-page] |
| Fly.io outbound data | $0.02/GB (N. America, Europe); $0.04/GB (Asia-Pacific, Oceania, S. America); $0.12/GB (Africa, India) | inbound free | same | [P-page] |
| Fly.io Managed Postgres | $38 (Basic) to $1,922 (Performance) per month; storage $0.28/GB-month | — | same | [P-page] |
| Fly.io support (optional) | $29/month Standard; $199 Premium | — | same | [P-page] |
| **Supabase Pro** | **$25/month** | Includes $10 compute credits (one Micro project, ≈$10/month); 100,000 MAU; 8 GB disk then $0.125/GB; 250 GB egress then $0.09/GB; 100 GB files then $0.0213/GB; daily backups kept 7 days. Free projects pause after 1 week of inactivity | `supabase/supabase` `packages/shared-data/plans.ts`, `pricing.ts`; docs `manage-your-usage/compute.mdx` | [P-page] |
| **Neon Launch** | **$0.106/CU-hour**; storage **$0.35/GB-month** | No monthly minimum; 1 CU ≈ 4 GB RAM; scale-to-zero after 5 min; Free plan: 100 CU-h/project; page `updatedOn` 2026-11-04 | `neondatabase/website` `content/docs/introduction/plans.md` | [P-page] |
| **Cloudflare R2** | **$0.015/GB-month** | Class A $4.50/M, Class B $0.36/M; egress free; 10 GB-month free | `cloudflare/cloudflare-docs` `r2/pricing.mdx` @434ad44 | [P-page] |
| **Google Cloud Storage** Standard, us-central1 | $0.000027397/GiB-hour (≈ **$0.020/GiB-month**) | as displayed | cloud.google.com/storage/pricing | [P-page] |
| AWS S3 Standard | **not verified** | — | aws.amazon.com not tried (stop rule); AWS docs repo archived | [U] |
| Google Cloud Run (request-based, us-central1) | $0.000024/vCPU-s; $0.0000025/GiB-s; $0.40 per million requests | free tier 180,000 vCPU-s, 360,000 GiB-s, 2M requests/month | cloud.google.com/run/pricing | [P-page] |
| Vercel Pro | **not verified** | — | vercel.com not tried | [U] |
| Render | **not verified** | — | render.com not tried | [U] |
| **Langfuse Cloud** | Hobby free (50k units/month, 30-day data access); **Core $29/month** (100k units included, then $8 per 100k, 90-day access); Pro $199/month (3-year access); data region US, EU or JP. Self-hosting: open-source core free (MIT outside `ee/`; copyright ClickHouse, Inc.) | — | `langfuse/langfuse-docs` `PricingTable.tsx` @1cb2e10; `langfuse/langfuse` LICENSE | [P-page] |
| Sentry | Free Developer plan exists; paid plans include a preset volume plus a pay-as-you-go budget. **Plan prices not verified** | — | `getsentry/sentry-docs` `docs/pricing/index.mdx` @956cb3b; sentry.io refused | [P-page] / [U] |
| E2B, Modal, Daytona per CPU-hour | **not verified** | — | — | [U] |
| **Claude Managed Agents runtime** | **$0.08 per session-hour** | while `running` only; plus tokens; web search $10 per 1,000 | platform.claude.com pricing | [P-page] |
| Claude code-execution tool | $0.05 per container-hour | after 1,550 free hours/month/org; 5-min minimum | same | [P-page] |
| Claude US-only inference | ×1.1 on all token categories | `inference_geo: "us"` | same | [P-page] |
| Claude Opus 5.5 | $4 input / $20 output; 5-min write $5; 1-h write $8; cache hit $0.20 per MTok | — | same | [P-page] |
| Claude Sonnet 5.5 | $2 / $10; 5-min write $2.50; 1-h write $4; **cache hit $0.10** per MTok | 0.05× base | same | [P-page] |
| Anthropic API monthly spend caps by usage tier | Start $500; Build $1,000; Scale $200,000; Custom none | org can set lower limits | platform.claude.com rate limits | [P-page] |

### 7.2 Estimate for a small deployment (pilot to 200 contributors). **ESTIMATE, not a quote**

These are my arithmetic on the anchors above, excluding inference (already in the cost model), staff time, e-mail delivery [U] and paid Sentry [U].

| Scenario | Components (monthly) | Total per month |
|---|---|---|
| **Lean A1 pilot** (≤ 10 active contributors/month) | 1 × Fly shared-cpu-1x 1 GB ($6.70) + Neon 0.25 CU × ~200 active h = 50 CU-h ($5.30) + 2 GB storage ($0.70) + R2 within free tier ($0) + Langfuse Hobby ($0) + Sentry free plan ($0; limits [U]) | **≈ $13** |
| **Production-like A1** (up to 200 contributors over ~12 months; redundancy) | 2 × Fly performance-1x 2 GB ($66) + Postgres: Supabase Pro ($25), *or* Neon 1 CU always on (730 CU-h = $77.38) + 10 GB ($3.50) + R2 100 GB ((100 − 10) × $0.015 = $1.35) + Langfuse Core ($29) + optional Fly Standard support ($29) + ~50 GB Asia-Pacific egress ($2) | **≈ $123–$208** |
| **A2 increment** (hosted sandbox) | e.g., 200 contributions × 2 running sandbox-hours = 400 h: Managed Agents runtime 400 × $0.08 = **$32 in total** (tokens counted in the inference model); Fly performance-1x ≈ $18 in total | small, one-off per contribution |
| **Option B comparator** (static page + upload endpoint) | Fly 256 MB ($2.19) or Cloud Run free tier + R2 free tier | **≈ $0–$5** |

**Reading.** Hosting runs at **≈ $13–$210 per month**, or ≈ $160–$2,500 per year. That is the same order as, or below, the cost model's central inference estimate for 200 contributions ($3,404). Both are dwarfed by shepherding (≈ 4,000 h). The drafts' "tens to low hundreds of dollars per month" is consistent with these anchors.

---

## 8. Compliance and ethics

> Statements below report what the texts say. **They are not legal conclusions**; every implication is flagged for review by the lead institution's legal, data-protection and research-ethics offices.

### 8.1 Anthropic: commercial terms, DPA, training, retention, data location [P-page]

- **Contracting entity (Commercial Terms, effective 2025-06-17).** "Anthropic Ireland, Limited if Customer resides in the European Economic Area, Switzerland or UK, and Anthropic, PBC if Customer resides anywhere else."
- **Users.** "…permission to use the Services, including to power products and services Customer makes available to its own customers and end users ('Users')" (§A.1).
- **Training.** "Anthropic may not train models on Customer Content from Services" (Inputs and Outputs).
- **DPA.** "Data submitted through the Services will be processed in accordance with the Anthropic Data Processing Addendum ('DPA'), which is incorporated into these Terms by reference."
- **Notice duty (§D.3).** The Customer "must notify its Users that factual assertions in Outputs should not be relied upon without independently checking their accuracy".
- **DPA (effective 2025-02-24):**
  - EU SCCs "Module Two (controller to processor) and/or Module Three (processor to processor) … are hereby incorporated by reference and will be deemed to have been executed"; UK Addendum and Swiss Addendum.
  - General authorization for subprocessors, with prior notice and a **15-day** objection window; list at anthropic.com/subprocessors.
  - Deletion of Customer Data at the end of the agreement, with exceptions (legal requirement, disputes, "to combat harmful use").
- **Retention (platform docs):**
  - "Conversation content (your prompts and Claude's outputs) is not retained by default; the exception is Covered Models, which require 30-day retention". The Covered Models are Fable 5.1, Mythos 5.1, Fable 5 and Mythos 5; **Opus 5.5 and Sonnet 5.5 are not listed**.
  - Flagged chats or sessions may be retained "for up to 2 years", even under ZDR.
  - Files API files are kept until deleted; Managed Agents transcripts "persist until you delete them".
  - The commercial retention help-centre article (privacy.claude.com) was not read [U].
- **Data location.** "Workspace geo: controls where data is stored at rest …"; "Currently, `"us"` is the only available workspace geo". `inference_geo` is `global` (default) or `us` (×1.1). There is no EU inference option.

### 8.2 Supported Regions Policy [P-page]

- The page carries an "Effective Nov 12, 2026" date. That is a **future** version, posted before today; the version currently in force was not separately read [U].
- The policy covers "our apps (such as Claude.ai, **Claude Code**, and Cowork), our API and developer platform, and Claude models offered through cloud platforms and authorized resellers".
- Unsupported uses include:
  - "Use by persons while physically located in an unsupported region, including users and personnel of otherwise supported entities".
  - Use by entities headquartered in, or majority-owned from, unsupported regions.
- The country list includes Taiwan and Singapore but **not** mainland China, Hong Kong or Macau.
- **Implication (flag for legal review, O-007).** Serving an interview powered by the project's Anthropic account to contributors physically located in mainland China, Hong Kong or Macau appears to conflict with this text under either architecture. Hosting location or CDN choices do not change it. This note does not suggest workarounds. R3, which read the policy versions in full, agrees. It also reports a Usage Policy clause, in force since 2025-09-15, prohibiting anyone from "access or facilitate account or API access to Claude to persons, entities, or users in violation of our Supported Regions Policy". That clause is directly relevant to a hosted platform; see R3 §2.

### 8.3 GDPR (EU contributors)

- **Sources:**
  - Anthropic offers a DPA with SCCs (§8.1) [P-page].
  - Supabase "provides a Data Processing Agreement (DPA)" and lets projects pin to a specific EU region [P-page].
  - Neon reports SOC 2 Type 1/2, SOC 3, ISO 27001 and ISO 27701, and says it "adhere[s] to GDPR" [P-page].
  - R2 offers an `eu` jurisdiction [P-page]; Langfuse offers an EU data region [P-page].
  - DPAs of Fly.io, Vercel, Sentry and the e-mail providers were not read [U].
- **GDPR articles** (controller–processor contracts, international-transfer chapter, lawful basis, information duties): article-level text not read in this session [U].
- **Implications (analysis; legal review):**
  - The lead's institution is likely the controller. Every vendor in the data path (Anthropic, host, database, storage, tracing, error tracking, e-mail) needs a processor agreement.
  - EU contributors' transcripts and code reach Anthropic's US workspace, so the SCC route is the relevant transfer mechanism.
  - LLM traces in Langfuse and Sentry contain transcripts. Choose EU regions or self-host, and scrub personal data.

### 8.4 China's PIPL and cross-border rules [S: unofficial copies, `LawRefBook/Laws` @3f9be6b]

**What the texts say**

- **PIPL (2021), Art. 3.**
  - The law applies to processing inside China.
  - It also applies to processing **outside** China of personal information of natural persons in China, when the purpose is "以向境内自然人提供产品或者服务为目的" (providing products or services to natural persons in China) or "分析、评估境内自然人的行为" (analysing or assessing their behaviour).
- **PIPL Art. 13** lists lawful bases, including consent and contract necessity.
- **PIPL Art. 38** sets the conditions for a processor providing personal information abroad: a CAC security assessment, certification, the CAC standard contract, or other conditions.
- **PIPL Art. 39** requires notice of the overseas recipient's identity, contact details, purposes, methods and categories, and **单独同意 (separate consent)**.
- **PIPL Art. 53.** Overseas processors covered by Art. 3(2) "应当在中华人民共和国境内设立专门机构或者指定代表" (must establish a dedicated office in China or designate a representative there) and report it to the authorities.
- **Provisions on Promoting and Regulating Cross-Border Data Flows (2024-03-22):**
  - **Art. 3:** data from "学术合作" (academic cooperation) and similar activities that contains **no personal information or important data** is exempt.
  - **Art. 5(4):** a non-CIIO processor that, cumulatively since 1 January, exports non-sensitive personal information of **fewer than 100,000 people** is exempt from the assessment, the standard contract and certification.
  - **Art. 7:** CAC assessment for CIIOs, important data, ≥ 1,000,000 people, or ≥ 10,000 people's sensitive personal information.
  - **Art. 8:** standard contract or certification for 100,000–1,000,000 people (non-sensitive) or fewer than 10,000 people (sensitive).
  - **Art. 10:** notice, **separate consent** and a personal-information impact assessment remain required.
- **Measures for Certification of Personal Information Export (2025-10-14),** in force **2026-01-01**. Overseas processors apply through their in-China office or representative.
- **Network Data Security Management Regulations,** in force 2025-01-01, **Art. 26.** Overseas processors that designate a representative under PIPL Art. 53 must report it to the city-level CAC office.

**Implications (analysis; legal review).**

- A foreign-hosted platform that collects data directly from contributors in China is analysed mainly under **Art. 3(2) (extraterritorial)** rather than the "export" rules. Those rules govern processors *in* China who send data abroad, for example a Chinese co-investigator's institution that forwards materials.
- Whether interviewing economists counts as "providing products or services" to them is a legal question.
- DeepEcon's scale (≤ 200 people) is far below the 100,000-person threshold, but notice and separate-consent duties do not depend on volume.
- This analysis interacts with §8.2: if Anthropic's policy excludes contributors physically in mainland China, the PIPL question mainly concerns Chinese contributors abroad or China-based co-investigators.

### 8.5 Reachability from mainland China and ICP filing

- **Cloudflare's China Network documentation** [P-page]:
  - "Traffic routed through servers outside the country faces significant latency and reliability issues due to China's network boundaries".
  - In-China delivery runs on JD Cloud data centres.
  - An ICP number is needed for sites "hosted on a server in Mainland China or delivered to visitors in China through a CDN". An **ICP filing (备案)** covers non-commercial sites. Eligible filers include representative offices, WFOEs, joint ventures, local companies and individuals.
  - This is a vendor's description, not a legal opinion.
- **Legal texts** [S, unofficial copies]:
  - 互联网信息服务管理办法 (Measures on Internet Information Services; 2024 revision), Art. 4: licensing for commercial services and **filing for non-commercial services**; "未取得许可或者未履行备案手续的，不得从事互联网信息服务" (no internet information service may be provided without a licence or a completed filing).
  - 非经营性互联网信息服务备案管理办法 (Measures on Filing of Non-commercial Internet Information Services; 2005), Art. 5: filing is required for non-commercial services "在中华人民共和国境内" (inside the People's Republic of China). Art. 22: a fine of 10,000 yuan and closure for unfiled services.
- **Reachability of specific foreign services** (GitHub, Google services, Dropbox, OneDrive, Box, Anthropic): no measurement source was read [U].

### 8.6 Ethics review for the usability pilot

- **Field precedent [P-page].** The Geiecke & Jaravel README requires IRB or ethics approvals, and consent disclosure of third-party AI providers, for studies using its platform.
- **US Common Rule (45 CFR 46) and university IRB guidance on usability studies: not read in this session [U].** My background knowledge, unverified:
  - The 2018 Common Rule defines research as a systematic investigation designed to contribute to generalizable knowledge.
  - It defines a human subject as a living individual about whom an investigator obtains information through interaction.
  - Exemption category (d)(2) covers interviews and surveys under conditions on identifiability and risk.
  - Many IRBs treat product-improvement usability testing as non-research, and treat studies intended for publication as research.
- **Implication.** Keep the pilot plan's requirement (IRB or ethics determination before recruitment, O-013). The pilot is designed to produce publishable comparisons, which makes a "research" determination likely [U]. The consent text should name the model provider, US processing and retention.

---

## 9. Submission-related vendor facts

| Fact | Finding | Label |
|---|---|---|
| GitHub per-file limits | Git warns above **50 MiB**; GitHub "blocks files larger than **100 MiB**"; browser uploads ≤ **25 MiB** (`data/variables/large_files.yml`) | [P-page] `github/docs` @58b7b56 |
| GitHub repository size | "ideally less than 1 GB, and less than 5 GB is strongly recommended" | [P-page] |
| Git LFS | Max file size **2 GB** (Free, Pro), **4 GB** (Team), **5 GB** (Enterprise Cloud); included storage and bandwidth **10 GiB/month** (Free, Pro) and **250 GiB/month** (Team, Enterprise) | [P-page] |
| Gmail / Outlook attachment limits | Not verified (search budget exhausted; hosts not tried) | [U] |
| Dropbox / Box / OneDrive / Google Drive file requests (uploads without an account?) | Not verified; Microsoft's file-request admin docs are in a non-public repository | [U] |
| Reachability of these services in mainland China | Not verified | [U] |

---

## 10. Fact-check table (draft files not edited)

Verdicts: **confirmed**, **corrected**, **partly confirmed**, **still unverifiable**.

| # | File: line | Claim (short quote) | Verdict | Correct fact / evidence | Citation |
|---|---|---|---|---|---|
| 1 | option-a: 39 | "E-mail magic link (optionally ORCID [U])" | **Confirmed** (feasible) | ORCID supports OIDC sign-in (`openid` scope, discovery). Public-API terms (non-commercial, individual-bound) need review | ORCID-Source OIDC doc [P-page]; info.orcid.org [S] |
| 2 | option-a: 75 | "TypeScript web framework … (e.g., Next.js) [U]" | **Confirmed** (viability) | next-intl and the AI SDK document App Router support | §2.2, §3.1 [P-page] |
| 3 | option-a: 76 | "ICU-message library … (e.g., `next-intl`) [U]"; alternatives "react-i18next, FormatJS" | **Confirmed** | next-intl 4.14.9 MIT, ICU, App Router/RSC. react-i18next needs `i18next-icu` for ICU; FormatJS is natively ICU | §3.1 [P-page] |
| 4 | option-a: 77 | "E-mail magic links via an auth library or service; optional ORCID sign-in [U]" | **Corrected** (refined) | Auth.js "is now part of Better Auth" and recommends Better Auth for new projects. Better Auth: magic-link and generic OIDC plugins. Supabase built-in SMTP is not for production (team-only, 2/hour) | §4 [P-page] |
| 5 | option-a: 80 | "…or Anthropic Managed Agents (beta)" (Agent SDK part "[U: feasibility per R2]") | **Confirmed** (Managed Agents part); Agent SDK part deferred to R2 | "Claude Managed Agents is in beta" | platform.claude.com Managed Agents overview [P-page] |
| 6 | option-a: 81 | "Container sandbox service with per-session isolation and resource limits [U: provider per R9]" | **Confirmed** (candidates exist; choice open) | E2B (R and Python kernels), Managed Agents (≤ 8 GB/10 GB, apt/pip), Modal (any image), Fly Machines (per-second). Daytona OSS unmaintained since June 2026 | §6 [P-page] |
| 7 | option-a: 81 | "Managed Agents' per-session container ($0.08 per session-hour plus tokens; beta; first-party API only)" | **Corrected** | Price and beta confirmed. Billed **only while `running`**. Available on **Claude API, Claude Platform on AWS and Claude Models on Google Cloud (Anthropic managed)**, not only first-party. Not ZDR-eligible; transcripts persist until deleted | platform.claude.com pricing and overview [P-page] |
| 8 | option-a: 138 | "Needs a Stata licence valid for server or container use [U: per R9]" | **Still unverifiable** | StataCorp pages not reachable. AEA/ssc-ng images: "A valid license is necessary to build and use these images"; licence mounted at runtime | `AEADataEditor/docker-stata` README [P-page]; StataCorp [U] |
| 9 | option-a: 169 | "no training on inputs by default [U: … default retention per R3]; … US-only inference at a 1.1× price" | **Confirmed** (training, 1.1×); retention partly | "Anthropic may not train models on Customer Content from Services". 1.1× confirmed. Docs: conversation content "not retained by default" except Covered Models (30 days); flagged content up to 2 years. **Add:** workspace geo (storage at rest) is US-only | Commercial Terms; pricing; retention and data-residency docs [P-page] |
| 10 | option-a: 175 | "data-protection obligations (GDPR; China's cross-border transfer rules) [U: per R9]" | **Confirmed** (in substance; legal review) | Anthropic DPA with SCCs. PIPL Arts. 3(2), 38, 39, 53; 2024 Provisions thresholds; 2026 certification measures | §8.1 [P-page]; §8.4 [S] |
| 11 | option-a: 185 | "Deliverability in some regions [U]" | **Still unverifiable** | No deliverability evidence read. Measure in the pilot (M1). Note the Supabase built-in SMTP restriction | §4 |
| 12 | option-a: 193 | "Hosting … tens to low hundreds of dollars per month … [U: per R9]" | **Confirmed** (as estimate) | ≈ $13–$210/month from verified anchors, excluding e-mail and paid Sentry [U] | §7 |
| 13 | option-a: 226 | "API rate limits depend on the account's usage tier [U]" | **Confirmed** | Limits "are defined by usage tier"; monthly spend caps Start $500, Build $1,000, Scale $200,000; Custom by arrangement | platform.claude.com rate limits [P-page] |
| 14 | option-a: 232 | "reuse ideas from open-source AI-interview platforms (their code is under non-commercial licences …) or the Agent SDK [U: per R9/R2]". Revised by another author during this session; it previously read "reuse an open-source AI-interview platform" | **Confirmed** (current wording) | Geiecke & Jaravel is Streamlit with file storage, basic logins, and PolyForm Noncommercial (code) / CC BY-NC 4.0 (docs) licences. Reuse its ideas and prompt patterns, not its code base; consistent with R7. Agent SDK part deferred to R2 | §2.1 [P-page]; R7 |
| 15 | option-a: 236 | "Provider terms restrict serving end users in some regions — Unknown [U: per R3]" | **Corrected** | Documented: the Supported Regions Policy (effective 2026-11-12) excludes mainland China, Hong Kong and Macau and covers "persons while physically located in an unsupported region"; Commercial Terms §D.2 binds "Customer and its Users". Legal review | §8.2 [P-page] |
| 16 | cost: 63 (A) | "Hosting …: tens to low hundreds of dollars per month at this scale [U: R9]" | **Confirmed** (as estimate) | as #12 | §7 |
| 17 | cost: 63 (B) | "Static project page and upload endpoint: near zero to tens of dollars per month [U: R9]" | **Confirmed** (as estimate) | Fly from $2.19/month; Cloud Run free tier; R2 free tier 10 GB-month → ≈ $0–$5 | §7 [P-page] |
| 18 | cost: 64 | "A2 sandbox time (small; e.g., Managed Agents charges $0.08 per session-hour plus tokens)" | **Confirmed** | Add "only while running"; example 400 h = $32 | §6.1, §7 |
| 19 | bilingual: 44 | "`next-intl` is the usual choice; `react-i18next` and FormatJS are alternatives [U]" | **Partly confirmed** | Technical fit confirmed; "usual choice" (popularity) not verified | §3.1 [P-page] |
| 20 | bilingual: 46 | "Fonts should be self-hosted … third-party font services, which may be unreachable from mainland China [U]" | **Still unverifiable** (reachability) | Evidence conflicts [S]. Recommendation supported on other grounds: Noto Sans SC variable TTF = 17.8 MB [P-page] | §3.2 |
| 21 | submission: 7 | "docs.github.com and several vendor sites are outside its allowed network domains" | **Corrected** | GitHub Docs' source is readable via the `github/docs` repository; GitHub limits verified (#24) | §9 [P-page] |
| 22 | submission: 28 | "Several common services are blocked or unreliable there [U]" | **Still unverifiable** | No measurement data read. Cloudflare documents "significant latency and reliability issues" for traffic routed outside China | §8.5 [P-page] |
| 23 | submission: 37 | "attachment limits around 20–25 MB on common providers [U]" | **Still unverifiable** | Official Gmail/Outlook pages not reachable | §9 |
| 24 | submission: 43 | "GitHub rejects files above about 100 MB without Git LFS [U]" | **Confirmed** (precise) | Blocks > **100 MiB**; warns > 50 MiB; browser ≤ 25 MiB; LFS per-file max 2/4/5 GB by plan; LFS 10 GiB free storage and bandwidth (Free/Pro) | `github/docs` [P-page] |
| 25 | submission: 50 | "Reachability from mainland China depends on hosting and CDN choices [U]" | **Partly confirmed** | In-China delivery requires in-China infrastructure (Cloudflare China Network via JD Cloud) **and an ICP filing or licence**; ICP rules (Art. 4/8; filing measures Art. 5) | §8.5 [P-page]/[S] |
| 26 | submission: 56 | "uploaders often need no account [U]" | **Still unverifiable** | Vendor help pages not reachable | §9 |
| 27 | submission: 57 | "several such services are blocked in mainland China [U]" | **Still unverifiable** | No measurement data read | §9 |
| 28 | pilot: 133 | "likely human-subjects research … even when it qualifies for exemption … R9 summarizes guidance" | **Still unverifiable** (primary guidance not read) | Common Rule and IRB pages not reachable; background summary in §8.6 [U]; field precedent: Geiecke & Jaravel README requires IRB approval [P-page]. Keep the requirement | §8.6 |
| — | cost: 33 (not marked [U]) | "**Sonnet 5.5** input $2, output $10, cache read **$0.20**" (also `inference_model.py` line 7) | **Corrected** (extra) | Live pricing: Sonnet 5.5 cache hits **$0.10/MTok** (0.05× base). Affects only the Sonnet sensitivity case. Opus 5.5 values ($4/$20/$0.20; 1-h write $8) confirmed | platform.claude.com pricing [P-page] |

**Tally of the 28 in-scope rows** (24 `[U]`-marked claims; rows #7, #18, #21 and #28 are related unmarked claims checked because they concern the same facts): 14 confirmed (#1, 2, 3, 5, 6, 9, 10, 12, 13, 14, 16, 17, 18, 24), 4 corrected (#4, 7, 15, 21), 2 partly confirmed (#19, 25), 8 still unverifiable (#8, 11, 20, 22, 23, 26, 27, 28). Line numbers refer to the drafts as they stood at about 10:00 UTC on 2026-11-05. Other authors were editing them in parallel.

**Out of scope here** (not hosting, stack, sandbox, Stata, compliance, ethics or vendor limits): pilot timings and likelihoods (option-a: 34, 234); engineering and maintenance estimates (option-a: 202; cost: 66; submission: 50 effort); Agent SDK feasibility (option-a: 85, R2); interview and token assumptions A2–A12 and support hours (cost: 19–29, 54); subscription terms and prices (cost: 75–76, R3); Claude Code language setting (bilingual: 53, R2).

---

## 11. Option A reference stack (Proposed; not a decision)

### 11.1 Reference stack

| Layer | Proposed choice | Rationale (evidence) |
|---|---|---|
| Web and API | **Next.js (App Router, TypeScript)** monolith in a container | One codebase for pages, chat streaming and API routes; best-supported target of next-intl and the AI SDK [P-page] |
| Hosting | **Fly.io Machines** in an EU region (e.g., Frankfurt `fra`), two machines in production | Transparent per-second pricing [P-page]; container hosting suits long streaming turns (Vercel limits and prices not verified [U]) |
| LLM orchestration | **Anthropic TypeScript SDK** server-side: tool use, streaming, prompt caching (1-h TTL), structured outputs, pinned model; per-session budgets in app code. Optional AI SDK UI hooks for the chat pane, using `@ai-sdk/anthropic` directly, **not** the default AI Gateway | Full access to Claude API features; no extra processor in the data path [P-page: AI SDK gateway default] |
| i18n | **next-intl 4.x**, locale-prefixed routes, JSON catalogs; Lingui if a PO/TMS workflow is required | §3.1 [P-page] |
| Fonts | System CJK font stack; optional self-hosted subset WOFF2 (Source Han / Noto, OFL) | §3.2 |
| Auth | **Better Auth** magic links plus generic OIDC (ORCID) with a reputable SMTP provider (vendor [U]) | §4 [P-page] |
| Database | **Neon** Postgres (Launch, pay-per-use, scale-to-zero) | $0.106/CU-h; no minimum [P-page] |
| Object storage | **Cloudflare R2**, `eu` jurisdiction; presigned uploads (≤ 1 h); data-access logs; lifecycle deletion; event-notification scan queue | §5 [P-page] |
| LLM tracing | **Langfuse** Cloud (EU region, Hobby or Core) or self-hosted (MIT core) | §7 [P-page] |
| Error tracking | **Sentry**, with PII scrubbing | Plan prices [U] |
| A2 sandbox (only if adopted) | **Claude Managed Agents** sandbox (hard USD budgets; apt/pip; R via apt [U]) **or E2B** (R kernel built in) | §6 [P-page] |

**Risks of the reference stack.**

- About seven vendors means about seven processor agreements.
- Better Auth and next-intl are single-maintainer-led projects [U].
- The Anthropic Supported Regions Policy (§8.2) limits reach regardless of hosting.
- US-only workspace geo means EU-to-US transfers.
- Malware scanning must be built.

### 11.2 Alternative 1: Supabase-integrated, fewer vendors

- **What.** Next.js + next-intl on Fly.io (or Vercel [U]), with **Supabase Pro** providing Postgres, Auth (custom SMTP), Storage (≤ 500 GB per file) and row-level security, in a specific EU region; plus the Anthropic SDK and Langfuse.
- **Rationale.**
  - One vendor for database, auth and files.
  - A published DPA [P-page]; $25/month covers the pilot [P-page].
  - Fewer contracts for a small academic team.
- **Risks.**
  - Coupling to Supabase APIs, so portability is lower than Postgres + S3-compatible storage.
  - The default SMTP is unusable in production [P-page].
  - Supabase Storage's encryption, scanning and log details were not verified [U].
  - The Free plan pauses after 1 week of inactivity [P-page], so use Pro for the pilot.

### 11.3 Alternative 2: Managed-Agents-centric

- **What.** A thin Next.js app handles auth, the dossier database, uploads and the review UI. **Claude Managed Agents** runs the agent loop and per-session sandbox: materials are mounted as session resources, outputs are written to `/mnt/session/outputs/`, and budgets are set per session.
- **Rationale.**
  - Least orchestration code to own.
  - A built-in sandbox for A2.
  - Platform-enforced hard per-session spend caps.
  - Versioned agent configurations, matching "one protocol version per release" [P-page].
- **Risks.**
  - **Beta.**
  - Not ZDR-eligible, and transcripts persist until deleted, so a deletion job is needed.
  - Workspace geo is US-only.
  - No R pre-installed; no Stata.
  - Available only on Anthropic-operated surfaces [P-page].
  - Deeper single-vendor lock-in.
  - Runtime billing is trivial, but tokens for agentic sessions can exceed the cost model's interview estimate. Use budgets.

**Pilot-only shortcut (not an alternative architecture).** A Chainlit A-slice (Python, Anthropic Python SDK) could test the interview fastest. Chainlit has been community-maintained since 2025-05-01 [P-page], and the slice would be rewritten if Option A is chosen.

---

## 12. Implications for the architecture documents (proposed edits for the authors; not applied)

1. **Option A §3.2 / §6.2 (Managed Agents).** Replace "first-party API only" with "Claude API, Claude Platform on AWS, Claude Models on Google Cloud (Anthropic managed)". Add "runtime billed only while running", "not ZDR-eligible; transcripts persist until deleted", and "no R pre-installed; apt/pip available".
2. **Option A §16 risks.** Change "Provider terms restrict serving end users in some regions — Unknown" to "documented (Supported Regions Policy, effective 2026-11-12); legal review", and apply the same to Option B.
3. **Option A §10.** Add that workspace geo (at-rest storage) is US-only and that the Commercial Terms incorporate a DPA with SCCs.
4. **Option A §3.2 auth row.** Name Better Auth (Auth.js is now part of it) and require a custom SMTP provider.
5. **Option A §6.2 Stata row.** Keep [U]; add the AEA/ssc-ng runtime-licence fact; require written confirmation from StataCorp before any A2 Stata support.
6. **Cost model.** Correct the Sonnet 5.5 cache-read price to $0.10/MTok (§2 and `inference_model.py`). Replace the hosting [U] with the §7 anchors and the ≈ $13–$210/month estimate.
7. **Submission mechanisms.** Replace the GitHub [U] with the verified limits; keep e-mail and file-request limits [U]; correct the header note about docs.github.com.
8. **Bilingual design §4.** Keep self-hosting or system fonts, justified by file size and dependency risk rather than by an unverified reachability claim.
9. **Pilot plan §9.** Keep the IRB/ethics requirement; consent should disclose Anthropic as processor, US storage and retention; note the evidence gap.

---

## Open questions

1. **Regional policy (legal).** Does Anthropic's Supported Regions Policy (effective 2026-11-12) bar the project from serving contributors physically in mainland China, Hong Kong or Macau under Option A, and under Option B via Claude Code? What text is in force before 2026-11-12? (O-007; R3.)
2. **PIPL applicability.** Would a foreign-hosted platform interviewing China-based economists fall under PIPL Art. 3(2), requiring an Art. 53 representative? Would a Chinese co-investigator institution forwarding materials trigger the Art. 38–39 export duties?
3. **GDPR roles.** Who is the controller? Do DPAs exist and fit for every vendor (Fly.io, Neon, Cloudflare, Langfuse, Sentry, SMTP)? Is the SCC route acceptable for US-only Anthropic storage?
4. **Stata.** Will StataCorp confirm in writing which licence permits running contributor-submitted do-files in project-operated containers?
5. **IRB.** Will the lead institution classify the pilot as research and, if so, which exemption applies? What consent language covers AI data flows?
6. **Unverified prices.** Vercel Pro, Render, AWS S3 and Fargate, E2B, Modal, Sentry, Auth0, Clerk and the transactional e-mail providers need checking from an unrestricted network before collaborators see a consolidated budget.
7. **ORCID terms.** Project-level Public API registration, or the institution's ORCID membership?
8. **Retention.** What retention periods apply to transcripts in our database, Langfuse, Sentry and (if used) Managed Agents? How are deletions propagated on withdrawal?
9. **Upload policy.** Accept only PDFs and code text in A1, or also data files? This determines the scope of malware scanning.
10. **Mainland China reachability.** If (1) permits any role for contributors in China at all, which documented measurements or on-the-ground tests will settle reachability of the site, sign-in e-mail and storage?

---

## Access problems

- **WebSearch budget exhausted.** On my 8th query, WebSearch returned "this turn's web search budget is used up (limit: 200 WebSearch calls per turn, shared by every agent in it)". No further searches were possible, and I did not work around the limit. A follow-up session can continue the searches.
- **Host failures (stop rule triggered):**
  1. `ideas.repec.org`: WebFetch DNS failure (ENOTFOUND, host outside the allowed network).
  2. `sentry.io`: proxy `connect_rejected` (CONNECT 403, policy denial).
  - After these two failures I tried **no new hosts**.
  - One further refusal happened by **redirect**: `cloud.google.com/storage/docs/...` redirected to `docs.cloud.google.com`, which the proxy refused (CONNECT 403, three requests within about 2 s). Those pages (GCS signed URLs, quotas, default encryption) were not read.
- **Not attempted because of the stop rule:** stata.com, aws.amazon.com (S3, Fargate, GuardDuty), vercel.com, render.com, e2b.dev, modal.com, daytona.io, clerk.com, auth0.com, privacy.claude.com, support.google.com, learn.microsoft.com, dropbox.com, box.com, eur-lex.europa.eu, ecfr.gov, hhs.gov, university IRB sites, greatfire.org, explorer.ooni.org, cac.gov.cn, miit.gov.cn, ssrn.com and zenodo.org.
- **Known blocked (per the lead):** arxiv.org; github.com web UI and API (not used).
- **What worked:**
  - raw.githubusercontent.com, `git clone --depth 1`, blob-less tree clones and `git ls-remote` against github.com.
  - www.anthropic.com and platform.claude.com.
  - cloud.google.com (pricing pages only).
- **Non-public repositories** (git asked for credentials, so treated as private or non-existent): `MicrosoftDocs/OfficeDocs-SharePoint`, `MicrosoftDocs/OfficeDocs-Exchange`, `MicrosoftDocs/OfficeDocs-Support`, `AEADataEditor/docker-r`.
- **Archived source:** `awsdocs/amazon-s3-userguide` is archived and its content deleted (last commit 2023-06-15), so S3 facts stay [U].
- **Consequence.** Every price or limit marked [U] above must be verified on the vendor's official page before it is quoted to collaborators.

---

## Sources

All accessed 2026-11-05. "raw" means read via raw.githubusercontent.com; commit SHAs are the files' pinned commit, or the branch HEAD observed by `git ls-remote` at the time of reading.

**Anthropic (primary, read directly)**
- Commercial Terms of Service, effective 2025-06-17: https://www.anthropic.com/legal/commercial-terms [P-page]
- Data Processing Addendum, effective 2025-02-24: https://www.anthropic.com/legal/data-processing-addendum [P-page]
- Supported Regions Policy, effective 2026-11-12: https://www.anthropic.com/supported-countries [P-page]
- Pricing: https://platform.claude.com/docs/en/about-claude/pricing.md [P-page]
- Managed Agents: https://platform.claude.com/docs/en/managed-agents/overview.md ; …/managed-agents/environments.md ; …/managed-agents/cloud-containers.md ("Cloud sandbox reference") ; …/managed-agents/sessions.md [P-page]
- Code execution tool: https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool.md [P-page]
- Data retention and ZDR: https://platform.claude.com/docs/en/build-with-claude/zero-data-retention.md ; https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md [P-page]
- Data residency: https://platform.claude.com/docs/en/manage-claude/data-residency.md [P-page]
- Rate limits: https://platform.claude.com/docs/en/api/rate-limits.md [P-page]
- Files API: https://platform.claude.com/docs/en/build-with-claude/files.md [P-page]
- Claude Code `claude-api` skill reference (Anthropic, cache date 2026-10-06; used for platform availability and session-budget semantics, cross-checked against live pages above) [P-page]

**Google Cloud (primary, read directly)**
- Cloud Storage pricing: https://cloud.google.com/storage/pricing [P-page]
- Cloud Run pricing: https://cloud.google.com/run/pricing [P-page]

**Vendor documentation repositories (primary sources of official docs/pricing pages; raw)**
- Fly.io pricing: `superfly/docs` @941ab703541804f90768d8fcf9b560c273ef11f0 `about/pricing.mdx` (live: https://fly.io/docs/about/pricing/) [P-page]
- Supabase: `supabase/supabase` branch master (HEAD d421451672fc): `packages/shared-data/plans.ts`, `packages/shared-data/pricing.ts`, `packages/shared-data/config.ts`, `apps/docs/content/guides/auth/auth-smtp.mdx`, `apps/docs/content/guides/auth/rate-limits.mdx`, `apps/docs/content/guides/platform/manage-your-usage/compute.mdx`, `apps/docs/content/guides/security/gdpr-compliance.mdx`, `apps/docs/content/guides/platform/regions.mdx` [P-page]
- Neon: `neondatabase/website` branch main (HEAD 2d91b454b093): `content/docs/introduction/plans.md` (updatedOn 2026-11-04), `content/docs/security/compliance.md` [P-page]
- Cloudflare: `cloudflare/cloudflare-docs` @434ad44206263b4782d6b773e0ee224f55be7214: `src/content/docs/r2/pricing.mdx`, `r2/platform/limits.mdx`, `r2/api/s3/presigned-urls.mdx`, `r2/reference/data-location.mdx`, `r2/reference/data-security.mdx`, `r2/buckets/bucket-locks.mdx`, `r2/platform/audit-logs.mdx`, `r2/buckets/event-notifications.mdx`, `china-network/index.mdx`, `china-network/concepts/icp.mdx` (live: https://developers.cloudflare.com/r2/pricing/) [P-page]
- Langfuse: `langfuse/langfuse-docs` @1cb2e1078d32f46814f88f521876bdd77bbbc83e `components/home/pricing/PricingTable.tsx`; `langfuse/langfuse` (HEAD 4de0ac3bbbcc) `LICENSE` [P-page]
- Sentry: `getsentry/sentry-docs` @956cb3b2d371cfe2d4fe80f9d5e36d31a25892cc `docs/pricing/index.mdx` [P-page]
- GitHub Docs: `github/docs` @58b7b56aa507ad1269b9f8e9e89a172f0976c7ce: `data/variables/large_files.yml`, `content/repositories/working-with-files/managing-large-files/about-large-files-on-github.md`, `…/about-git-large-file-storage.md`, `content/billing/concepts/product-billing/git-lfs.md` (live: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) [P-page]

**Open-source projects (README, licence, manifests; raw or clone)**
- Geiecke & Jaravel: `friedrichgeiecke/interviews` @94297760dedd567d7b5c2e7119a20ca657e486c0 (clone): `README.md`, `tutorial-online-interviews.md`, `config.py`, `requirements.txt`, `LICENCE-CODE`, `LICENCE-DOCS` [P-page]
- `vercel/ai` (HEAD 8e8033a73dd4): `packages/ai/README.md`, `packages/ai/package.json`, `LICENSE` [P-page]
- `Chainlit/chainlit` (HEAD 190ea74239d9): `backend/README.md`, `LICENSE`, `backend/chainlit/translations/zh-CN.json` [P-page]
- `open-webui/open-webui` (HEAD c38885a1a737): `README.md`, `LICENSE` [P-page]
- `danny-avila/LibreChat` (HEAD f4154b649efa): `README.md`, `LICENSE` [P-page]
- `streamlit/streamlit` (HEAD fc66ba0c4566): `README.md`, `LICENSE` [P-page]
- i18n: `amannn/next-intl` (HEAD b9fc98a81495) README, package.json, CHANGELOG; `i18next/i18next` (3cc577491839); `i18next/react-i18next` (a6b635dfb482); `i18next/i18next-icu` (097d2d507bc5); `formatjs/formatjs` (f50f21bcd53d); `lingui/js-lingui` (c04c7e9d92c0); `opral/paraglide-js` (3cce33f1179e) [P-page]
- Auth: `nextauthjs/next-auth` (a1a16a5a7780) README and `packages/core/src/providers/{github,nodemailer}.ts` (no `orcid.ts`); `better-auth/better-auth` (9342a73e3635) README, `docs/content/docs/plugins/{magic-link,generic-oauth}.mdx`, package.json; `ORCID/ORCID-Source` (1af586cfcb6f) `orcid-web/ORCID_AUTH_WITH_OPENID_CONNECT.md` [P-page]
- CJK: `w3c/clreq` (08a701fafc77) `index.html`; `google/fonts` (fbe81817505e) `ofl/notosanssc/METADATA.pb` and `NotoSansSC[wght].ttf` (HEAD request, content-length 17,772,300); `adobe-fonts/source-han-sans` (0b993716f691, release branch README) [P-page]
- Sandboxes: `e2b-dev/code-interpreter` @c49b78602c29e44d07e196604de515dfa6b12744 `README.md`, `template/template.py`, `template/build_docker.py`, `LICENSE`; `e2b-dev/E2B` @b1f9a3e1 `README.md`, `LICENSE`; `modal-labs/modal-client` @c4afaa086ab82fa74ac7dac6be4d21422799da60 `README.md`, `LICENSE`, `py/modal/_image.py`; `modal-labs/modal-examples` @780dc941 (clone, grep only); `daytonaio/daytona` (ec4c21b2d597) `README.md`, `LICENSE` at tag v0.190.0 [P-page]
- Stata: `AEADataEditor/docker-stata` @fdbec27bae7ee57a4830a5b74126219d2ad5dc99 (clone) `README.md` [P-page]

**Legal texts (unofficial copies; [S])**
- `LawRefBook/Laws` @3f9be6bd09d60656ef66b44f0b4604b18c61df74:
  - 行政法/个人信息保护法(2021-08-20).md (Personal Information Protection Law)
  - 部门规章/国家互联网信息办公室/促进和规范数据跨境流动规定(2024-03-22).md (Provisions on Promoting and Regulating Cross-Border Data Flows)
  - …/个人信息出境认证办法(2025-10-14).md (Measures for Certification of Personal Information Export)
  - …/个人信息出境标准合同办法(2023-02-03).md (Measures on the Standard Contract for Personal Information Export)
  - 行政法规/网络数据安全管理条例(2024-09-24).md (Network Data Security Management Regulations)
  - 行政法规/互联网信息服务管理办法(2024-12-06).md (Measures on Internet Information Services)
  - 部门规章/工业和信息化部/非经营性互联网信息服务备案管理办法(2005-03-20).md (Measures on Filing of Non-commercial Internet Information Services)

**Secondary (WebSearch summaries; pages not opened by me) [S]**
- Geiecke & Jaravel: https://cepr.org/publications/dp19705 ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4974382 ; https://cep.lse.ac.uk/_NEW/PUBLICATIONS/abstract.asp?index=12671 ; https://www.timeshighereducation.com/node/734252 (≈ £3–4 per participant)
- ORCID: https://info.orcid.org/public-client-terms-of-service/ ; https://info.orcid.org/documentation/integration-guide/registering-a-public-api-client/ ; https://info.orcid.org/what-is-orcid/services/public-api/
- Google Fonts and mainland China (conflicting): https://www.chinafy.com/blog/how-to-fix-font-loading-issues-in-china ; https://groups.google.com/g/noto-font/c/Gfbyoup5QV4 ; https://www.github.com/cdnjs/cdnjs/issues/682 ; https://github.com/joway/fonts ; https://appinchina.co/does-google-fonts-api-work-in-china ; https://discourse.webflow.com/t/webfont-js-is-blocked-in-china/113727
- W3C clreq published note: https://www.w3.org/TR/2025/DNOTE-clreq-20250319/

**Unreachable or not attempted primary sources** (see "Access problems"): ideas.repec.org (DNS), sentry.io/pricing (proxy 403), docs.cloud.google.com (proxy 403 via redirect); stata.com, aws.amazon.com, vercel.com, render.com, e2b.dev, modal.com, eur-lex.europa.eu, ecfr.gov and others not attempted.
