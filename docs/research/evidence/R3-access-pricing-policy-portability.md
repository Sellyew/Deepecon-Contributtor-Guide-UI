# R3: Contributor-side access, pricing, regional availability, data-use terms, and portability

| Field | Value |
|---|---|
| Topic | What contributors need in order to run the DeepEcon interview under Option A (hosted platform on the project's API account) or Option B (local Claude Code skill or plugin): Claude plans, prices and limits; supported regions, including mainland China, Hong Kong, Macau and Taiwan; whether a hosted platform may serve end users in unsupported regions; alternatives for contributors in mainland China; portability of Agent Skills (`SKILL.md`); data-use and retention terms; academic programmes and funding; a fact-check of the draft architecture documents |
| Date | 2026-11-05. All URLs were accessed on 2026-11-05. |
| Author | research agent |
| Scope | Official Anthropic pages on claude.com, www.anthropic.com, support.claude.com, code.claude.com and platform.claude.com (rendered text downloaded and read, legal pages including their version metadata). Primary documentation of other agent tools and Chinese model providers, read only where it is published in GitHub repositories: raw.githubusercontent.com, or blobless `git clone --depth 1`, nothing executed. The AEA Data Editor's site source on GitHub. Fact-check of `option-b-local-skill.md` §3.2, §5.3, §10, §11, §12, §16, §17; `option-a-hosted-platform.md` §10, §11, §16 (and two material items elsewhere); `cost-and-effort-model.md` §5 (and one item in §2). No legal conclusions are drawn. |
| Evidence labels | **[P-full]** primary source, full document read · **[P-page]** primary source, official page, README or source file read, or only the cited clauses of a longer document · **[S]** secondary (search snippet, news, blog) · **[U]** unverified: recollection, inference, or a source that could not be accessed |
| Evidence limits | **No web searches were possible.** The shared WebSearch budget for this turn was already exhausted on my first query, so this note contains no [S] claims. Three hosts were refused (see §11). Following the lead's rule I then stopped trying new hosts, so provider and vendor documentation sites, university pages and the Coefficient Giving site were not read. Claims that depend on them are [U]. |
| Status | Phase 1 (Discovery) evidence note. Sections marked "(b) Implications" and §9 are assessment, not decisions. Legal questions are flagged for review, not answered. |

Citation keys (for example **[PRICING]**) resolve to full URLs in §12.

---

## Summary (10 bullets max)

1. **Plans, November 2026.**
   - Free: $0.
   - Pro: $20 a month, or $17 a month billed annually ($200 up front).
   - Max: $100 a month. Max is "5x Pro usage every 5 hours and every week".
   - Ultra: $200 a month, the renamed Max 20x. Ultra is "10x Pro usage every week" and has no 5-hour limit for verified accounts.
   - Team, 2–150 seats. Standard seats cost $25 monthly or $20 billed annually and give 1.25× Pro per session. Premium seats cost $125 or $100 and give 6.25× Pro per session.
   - Enterprise: "US$20/seat/month, billed annually, 20 seat minimum", plus all usage at API rates.
   - Education: no published price.

   Every subscription plan except usage-based Enterprise has a 5-hour session limit and/or a weekly limit; usage-based Enterprise "ha[s] no plan or seat-level usage limits". Anthropic publishes no token or message quotas. [P-full PRICING; P-page HC-TEAM, HC-ULTRA, HC-ENT]
2. **Claude Code, Cowork and Opus by plan.** Claude Code is "included in all paid plans" and is not on Free. Cowork "Works with a paid plan". Opus is on every paid plan and not on Free. Claude Code defaults to Opus 5.5 on Pro, Max, Ultra, Team, Enterprise and the API. For Education, the pages I read do not say whether Claude Code or Cowork is included [U]. [P-full PRICING; P-page COWORK, CC-MODEL]
3. **Regions.** Mainland China, Hong Kong and Macau are absent from every Anthropic list I read; Taiwan is listed. The new Supported Regions Policy takes effect on **12 Nov 2026**. It covers "our apps (such as Claude.ai, Claude Code, and Cowork), our API … and Claude models offered through cloud platforms". It treats as unsupported "Use by persons while physically located in an unsupported region, including users and personnel of otherwise supported entities". [P-full SRP, HC-WHERE, API-REGIONS]
4. **Ownership rule.** The 4 Sep 2025 announcement "prohibits companies or organizations whose ownership structures subject them to control from jurisdictions where our products are not permitted, like China … more than 50% owned". The 2026 policy wording extends this to "entities incorporated or headquartered in an unsupported region and their users or personnel, regardless of whether such individuals are physically located in a supported region". As written, that wording does not exempt universities. How it applies to individual academics is ambiguous and needs **legal review**. [P-full NEWS-2025-09, SRP]
5. **A hosted platform serving end users in unsupported regions.** The in-force Usage Policy (15 Sep 2025) prohibits "Access or facilitate account or API access to Claude to persons, entities, or users in violation of our Supported Regions Policy". The 12 Nov 2026 version prohibits providing "others (including end users) with access". The Commercial Terms bind "Customer and its Users" to the Supported Regions Policy (D.2). The texts therefore address Option A's case directly. They do not say what diligence is expected, and they do not say whether relaying an interview through a person in a supported region counts as "facilitating" access. **Flag for legal review.** [P-page AUP-2025, AUP-2026, CTOS]
6. **Data-use terms.**
   - Consumer plans (Free, Pro, Max, Ultra, including Claude Code) may be trained on "unless you opt out". Retention is **5 years** if training is allowed and **30 days** if not. Feedback and safety-flagged content may be used for training even after opt-out.
   - Commercial terms: "Anthropic may not train models on Customer Content".
   - Retention under commercial terms: the Claude Code doc gives a 30-day standard retention, while the API doc says conversation content "is not retained by default" except for Covered Models (30 days). The two Anthropic statements are **inconsistent**.
   - Zero data retention (ZDR) is available only through sales, to qualified organisations. [P-page COTOS, PRIV, CC-DATA, API-RET, CTOS; P-full NEWS-2025-08, CC-ZDR]
7. **Ways the project could provide access in Option B exist, but each has conditions.**
   - Console members who sign in to Claude Code get per-user keys in a "Claude Code workspace". It is "the only workspace that supports per-user monthly spend limits".
   - Team seats are "assigned to one named individual", and reassignment "isn't designed for rotating one seat among several active users".
   - Anthropic's Claude apps gateway accepts only private-network addresses at sign-in.
   - Where Claude Code runs inside a customer's hosted product, customers "may not pay for, resell, or intermediate Claude usage on their end users' behalf". This condition also bears on Option A's Agent-SDK variant. [P-page API-WS, HC-SEATS, CC-APPSGW; P-full CC-LEGAL]
8. **Agent Skills portability.**
   - The open standard defines six frontmatter fields: `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` (the last is experimental).
   - Its showcase lists 46 clients, including ChatGPT & Codex, Gemini CLI, GitHub Copilot, VS Code and Cursor.
   - Claude Code adds `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths` and `shell`.
   - claude.ai and Cowork uploads reject non-spec fields with a hard error. [P-full AS-SPEC, AS-CLIENTS; P-page CC-SKILLS]
9. **Options in mainland China.**
   - Kimi Code CLI and Qwen Code read `SKILL.md` from `.agents/skills/`. [P-page KIMI-CODE, QWEN-CODE]
   - Moonshot's README states "we provide an OpenAI/Anthropic-compatible API". [P-page KIMI-K2]
   - Anthropic "doesn't support routing Claude Code to non-Claude models through any gateway". [P-page CC-LLMGW]
   - **Unverified:** Zhipu, DeepSeek, Alibaba and MiniMax endpoints for Claude Code, and the data-use or training terms of every Chinese provider [U].
   - Because the policy lists Claude Code itself as an Anthropic product, running Claude Code from mainland China against a third-party model raises its own **legal-review** question.
10. **Funding.**
    - AI for Science: "up to $50,000 in credits per project. Any researcher is eligible to apply" (27 Aug 2026).
    - Claude Team plan for scientists: Standard seats $0 and Premium seats $15 a month for 12 months, 1–25 seats, capped at 10,000 scientists. Eligibility covers PIs "in the natural sciences, mathematics, computer science, engineering, and related fields". Economics is not named, so eligibility is ambiguous.
    - The Sloan Foundation, which funds economics, now distributes Claude credits.
    - Coefficient Giving's "Benchmarking LLM Agents on Consequential Real-World Tasks" programme exists (ReplicatorBench acknowledgement); its terms are [U]. [P-full AI4S-2026-08, SCI, SCI-TERMS; P-page AI4S-2026-10, COS]

---

## 0. Method and what was read

- **Anthropic pages.** I downloaded the rendered HTML through the environment's agent proxy, converted it to text with my own script (`python3 -I`), and read it.
- **Legal-document versions.** Effective dates and version history come from the metadata embedded in each legal page. The Usage Policy, Supported Regions Policy, Commercial Terms and Consumer Terms each carry a `versionHistory` list. The archived Usage Policy (effective 2025-09-15) was read at its archive URL.
- **Markdown docs.** The code.claude.com and platform.claude.com pages were read as Markdown, via the `.md` endpoints those sites publish.
- **GitHub material.** Files were read through raw.githubusercontent.com, or through blobless `git clone --depth 1`, each clone in its own new directory. I read files only and executed nothing. R1 and R4 used the same route. Commit hashes and dates are given in §12.
- **What was not read.** Provider documentation sites, other vendors' own documentation sites, agentskills.io itself, university and IRB pages, and coefficientgiving.org (see §11).

---

## 1. Plans, prices, inclusions and usage limits (Q1)

### 1.1 (a) What the sources say

Prices are US list prices excluding tax: "Prices shown don't include applicable tax. Price and plans are subject to change at Anthropic's discretion." [P-full PRICING] Pro "Monthly pricing varies by region" [P-page HC-PRO].

| Plan | Price | Claude Code | Cowork | Opus-class | Fable (top "Mythos" tier) | Usage limits (as published) |
|---|---|---|---|---|---|---|
| **Free** | $0 [P-full PRICING] | No [P-full PRICING] | No: Cowork "Works with a paid plan" [P-page COWORK] | No [P-full PRICING] | No [P-full PRICING] | "Limited usage every 5 hours and every week" [P-full PRICING] |
| **Pro** | $20 billed monthly; $17 a month on annual billing ("$200 billed up front") [P-full PRICING] | Yes [P-full PRICING] | Yes: "Claude Cowork is included in your Pro plan … Claude Cowork consumes limits faster than Chat" [P-page COWORK] | Yes [P-full PRICING] | Usage credits only [P-full PRICING; P-page HC-FABLE] | 5-hour session limit plus a weekly limit. "Pro gives you at least 5x more usage per 5-hour session than Free" [P-full PRICING; P-page HC-PRO] |
| **Max** | $100 a month, monthly billing only [P-full PRICING; P-page HC-MAX] | Yes | Yes [P-page COWORK] | Yes | Included "up to half your weekly limit" [P-full PRICING] | "5x Pro usage every 5 hours and every week" plus a separate weekly Fable limit. "$100 a month in API credits" [P-full PRICING; P-page HC-MAX] |
| **Ultra** (formerly Max 20x) | $200 a month, monthly only [P-full PRICING; P-page HC-ULTRA] | Yes | Yes [P-page COWORK] | Yes | 50% of weekly limits [P-full PRICING] | "10x Pro usage every week". "No 5-hour limit for verified accounts"; a temporary limit applies until verification. "$200 a month in API credits" [P-full PRICING; P-page HC-ULTRA] |
| **Team, Standard seat** (2–150 seats) | $25 per seat per month billed monthly; $20 billed annually [P-full PRICING; P-page HC-TEAM] | Yes: "Claude Code and Claude Cowork" [P-full PRICING; P-page HC-TEAM] | Yes | Yes [P-full PRICING] | Usage credits [P-page HC-FABLE] | "1.25x the Pro plan's per-session usage allowance" plus a weekly limit; limits are per member [P-page HC-TEAM] |
| **Team, Premium seat** | $125 billed monthly; $100 billed annually [P-full PRICING; P-page HC-TEAM] | Yes | Yes | Yes | 50% of weekly limits [P-full PRICING] | "6.25x the Pro plan's per-session usage allowance" plus a weekly limit [P-page HC-TEAM]. A Team plan includes "Up to $500 per month in pooled API credits" [P-full PRICING] |
| **Enterprise** (self-serve or sales-assisted) | "US$20/seat/month, billed annually, 20 seat minimum. Usage cost scales with model and task" [P-full PRICING]. Self-serve minimum 20 seats; sales-assisted minimum 50 [P-page HC-ENT] | Yes. The seat gives access to "Claude on web, desktop, and mobile, plus Claude Code and Cowork" [P-page HC-ENT, HC-ENT-BILL] | Yes | Yes | Billed at API rates [P-page HC-FABLE] | Usage-based plans "have no plan or seat-level usage limits". Admins set organisation and per-user spend limits [P-page HC-ENT, HC-ENT-BILL] |
| **Education** | No price published; "Contact our Education team" [P-page EDU; P-full PRICING] | Not stated on the pages read [U] | Not stated [U] | "Access to the newest, most advanced Claude models" [P-page HC-EDU-USE] | Not stated [U] | "Increased usage limits: More messages per day compared to individual plans" [P-page HC-EDU-USE] |
| **Team plan for scientists** (promotional; see §7) | Standard $0 a month ("regularly $20"); Premium $15 a month ("regularly $100"), for 12 months [P-full SCI, SCI-TERMS] | "Access to Claude Science, Code, & Cowork" [P-full SCI] | Yes | Yes (as Team) [U: inferred from "everything in Claude Team"] | As Team [U] | Premium "5x more usage" [P-full SCI] |

### 1.2 (a) Usage-limit mechanics

- **Two limits.** "Paid plans have two types of usage limits: a session limit that resets every five hours, and weekly limits that reset once every week." [P-page HC-LIMITS]
- **One shared pool.** "your usage of all different Claude product surfaces (claude.ai, Claude Code, Claude Desktop) counts towards the same usage limit." [P-page HC-LIMITS]
- **No fixed quotas.** Anthropic says there is "no fixed message count" [P-full PRICING]. It also states: "we may limit your usage in other ways, such as weekly and monthly caps or model and feature usage, at our discretion. We don't guarantee uninterrupted service." [P-page HC-PRO, HC-MAX; P-full PRICING]
- **What uses the pool faster.** Usage depends on conversation length, features, model and effort level [P-page HC-LIMITS]. Cowork "consumes limits faster than Chat" [P-page COWORK].
- **Going past the limit.** Paid plans can turn on usage credits "to keep working at standard API rates" [P-full PRICING].
- **Intended use.** "Advertised usage limits for Pro, Max, and Ultra plans assume ordinary, individual usage of Claude Code and the Agent SDK." [P-full CC-LEGAL]

### 1.3 (b) Implications (assessment)

- **Option B needs a paid plan or access the project provides.** Free has no Claude Code, no Cowork and no Opus.
- **Whether Pro's limits cover a contribution is unknown.** A 1.5–3 hour interview plus agentic code work may exceed Pro's 5-hour session or weekly limits, especially at high effort, but nothing published lets us predict it. The pilot (PQ5) has to measure it.
- **Who pays for model access is now a concrete pricing question.** One month of Pro ($20) is close to the cost model's central API estimate per contribution ($17). Max ($100) costs about 6× that estimate.

---

## 2. Supported regions and the ownership/control rule (Q2)

### 2.1 (a) Exact current wording

The Supported Regions Policy, "Effective Nov 12, 2026", has audience "All users". The old URL https://www.anthropic.com/supported-countries now redirects to it. [P-full SRP]

> "Anthropic's products and services — including our apps (such as Claude.ai, Claude Code, and Cowork), our API and developer platform, and Claude models offered through cloud platforms and authorized resellers — are available only in the countries and regions listed below. Territories and dependencies of a listed country are also supported (for example, Puerto Rico as a territory of the United States).
>
> Any country or region not listed is unsupported. This includes:
> - Use by persons while physically located in an unsupported region, including users and personnel of otherwise supported entities.
> - Use by entities incorporated or headquartered in an unsupported region and their users or personnel, regardless of whether such individuals are physically located in a supported region.
> - Use by entities that are majority-owned or controlled, directly or indirectly, by persons or entities in unsupported regions, including use by their users or personnel, regardless of whether such individuals are physically located in a supported region." [P-full SRP]

- **One list for all products.** The policy uses one list for apps, API and cloud platforms; there are no separate Claude.ai and API lists [P-full SRP]. The API documentation keeps its own list: "Here are the countries, regions, and territories Anthropic can support access from" [P-full API-REGIONS].
- **The lists differ slightly.** The policy names 185 regions and the API page 175. The API page omits, among others, the Central African Republic, the DRC, Eritrea, Ethiopia, Libya, Mali, Nicaragua, Somalia, South Sudan and Sudan, and its Ukraine exception lists only Crimea, Donetsk and Luhansk. I take it to be older (my comparison). [P-full SRP, API-REGIONS]
- **Version history.** The policy page's `versionHistory` has a single entry with no previous version. I could not retrieve the wording of the earlier "supported countries" page; its PDF host was refused (§11). [P-page SRP metadata]

### 2.2 (a) Mainland China, Hong Kong, Macau, Taiwan

| Region | Supported Regions Policy (effective 2026-11-12) | Help Center "Where can I access Claude?" (dated 16 Mar 2026) | API docs list |
|---|---|---|---|
| Mainland China | Not listed, so unsupported [P-full SRP] | Not listed [P-full HC-WHERE] | Not listed [P-full API-REGIONS] |
| Hong Kong | Not listed | Not listed | Not listed |
| Macau | Not listed | Not listed | Not listed |
| Taiwan | **Listed** | **Listed** | **Listed** |

The "territories and dependencies" clause supports only territories of a **listed** country [P-full SRP]. China is not listed, so the clause does not bring in Hong Kong or Macau (my reading of the text).

### 2.3 (a) The September 2025 ownership/control restriction

"Updating restrictions of sales to unsupported regions", published 4 Sep 2025 [P-full NEWS-2025-09]:

> "This update prohibits companies or organizations whose ownership structures subject them to control from jurisdictions where our products are not permitted, like China, regardless of where they operate. This includes entities that are more than 50% owned, directly or indirectly, by companies headquartered in unsupported regions."

The 2026 policy restates the rule in §2.1's third bullet ("majority-owned or controlled, directly or indirectly, by persons or entities in unsupported regions"). It adds the second bullet on entities "incorporated or headquartered in an unsupported region and their users or personnel". [P-full SRP]

### 2.4 Effect on individual users and universities

**(a) What the text covers** [P-full SRP]:

- **Individuals by location.** Anyone "physically located in an unsupported region", "including users and personnel of otherwise supported entities". Under this wording a US- or EU-based contributor who travels to mainland China or Hong Kong falls outside supported use while there.
- **Entities by place of incorporation or headquarters**, "and their users or personnel, regardless of whether such individuals are physically located in a supported region". The wording does not distinguish universities, public bodies or non-profits from companies.
- **Entities by ownership or control**, majority-owned or controlled by persons or entities in unsupported regions.
- **No nationality criterion.** The text does not mention nationality or citizenship.

**(b) Ambiguities for legal review** (no conclusion offered):

1. Does "use by entities … and their users or personnel" reach a faculty member of a mainland-China, Hong Kong or Macau university who uses a **personal** account, while physically in a supported region, for a project run by a supported-region team? Or does it reach only use on the entity's behalf? The text does not say.
2. How does the rule treat Sino-foreign joint-venture campuses, or foreign universities' campuses in mainland China, if those are locally incorporated? It also covers branch campuses abroad controlled by mainland-China universities. Incorporation and control facts would have to be checked case by case [U].
3. Which version is operative before 12 Nov 2026? The in-force Usage Policy (2025-09-15) links to the URL that now serves the new policy (§3.1).

---

## 3. May a hosted platform on the Anthropic API serve end users in unsupported regions? (Q3)

### 3.1 (a) The texts

**Commercial Terms of Service**, effective 17 Jun 2025, the latest version [P-page CTOS]:

- **A.1** "Anthropic gives Customer permission to use the Services, including to power products and services Customer makes available to its own customers and end users ("Users")."
- **D.2** "Customer and its Users may only use the Services in compliance with these Terms, including (a) the Usage Policy …, (b) our policy on the countries and regions Anthropic currently supports ("Supported Regions Policy") and (c) our Service Specific Terms".
- **D.3** "Customer acknowledges, and must notify its Users, that factual assertions in Outputs should not be relied upon without independently checking their accuracy".
- **I.3.a** Anthropic may suspend access if "(ii) Customer or any User is using the Services in violation of Sections D.1 (Compliance), D.2 (Policies and Service Terms) or D.4 (Use Restrictions)".
- **M.8** "Customer may not export or provide access to the Services to persons or entities or into countries or for uses where it is prohibited under U.S. or other applicable international law."

**Usage Policy in force today**, effective 15 Sep 2025, "Do Not Abuse our Platform" [P-page AUP-2025]:

- Scope: the policy "applies to anyone who can submit inputs to Anthropic's products and/or services, including via any authorized resellers or passthrough access, all of whom we refer to as "users.""
- Prohibition: "Access or facilitate account or API access to Claude to persons, entities, or users in violation of our Supported Regions Policy" (linked to anthropic.com/supported-countries).

**Usage Policy effective 12 Nov 2026**, marked "isLatest" in the page metadata [P-page AUP-2026]:

- Scope: it applies to "anyone who submits inputs … This includes individuals using our apps …, developers and businesses using our API …, customers accessing Claude through cloud providers and authorized resellers, and **the end users of products or services integrating Claude**."
- "Access, facilitate, or provide others (including end users) with access to our products or services in violation of our Supported Regions Policy".
- "Resell, proxy, or otherwise provide access to Claude through unauthorized means, including services that route requests through consumer subscriptions or misrepresent the product or client being used".
- "All consumer-facing chatbots or AI agents that communicate directly with external users must disclose to users that they are interacting with AI rather than a human."
- Enforcement: "we may warn you or throttle, limit, suspend, or terminate your access".

**Supported Regions Policy:** unsupported use includes "Use by persons while physically located in an unsupported region, including users and personnel of otherwise supported entities" [P-full SRP].

### 3.2 (a) What the texts say when read together

- The Commercial Terms make the project's end users ("Users") subject to the Supported Regions Policy.
- The policy calls use by persons physically located in mainland China, Hong Kong or Macau unsupported.
- Both versions of the Usage Policy prohibit facilitating or providing access in violation of that policy. The 2026 version names "end users" explicitly.

The texts say these things expressly; they are not my inference. [P-page CTOS, AUP-2025, AUP-2026; P-full SRP]

### 3.3 (b) What is ambiguous: flag for legal review

1. **Expected diligence.** The texts do not say whether the project must geo-block, collect location attestations, or monitor for VPN use.
2. **Relayed interviews.** Suppose a research assistant in a supported region conducts the interview and relays a contributor's answers from mainland China. Is that "facilitating" access? The texts do not address mediated use.
3. **Affiliated personnel abroad.** For contributors affiliated with entities headquartered in unsupported regions but physically in supported regions, the policy says "regardless of whether such individuals are physically located in a supported region". How that applies to individual academics is ambiguous (§2.4).
4. **Timing.** The texts in force today (Usage Policy of 2025-09-15, plus the page behind the Supported Regions link) differ from the texts effective 2026-11-12. Recruitment will almost certainly fall under the new texts.
5. **Interaction with export law.** M.8 adds a separate obligation under U.S. and other law. That analysis belongs to counsel or R9.

### 3.4 (a) Related terms that constrain designs where the project provides access

**From the Claude Code legal-and-compliance page** [P-full CC-LEGAL]:

- On "preinstalling or running Claude Code in your products or services (e.g. in hosted sandboxes or other agent infrastructure)": "**Customers may not pay for, resell, or intermediate Claude usage on their end users' behalf.** Each end user must authenticate with their own Anthropic API key, Claude subscription plan credentials, or 3P inference provider credential … That usage is billed directly to the end user".
- On OAuth: "Anthropic does not permit third-party developers to offer Claude.ai login into their own applications, or to route requests through Free, Pro, Max, or Ultra plan credentials on behalf of their users."
- On API keys: "This does not restrict how customers provision and manage their own API keys … for use by the customer's own authorized users — provided the resulting usage is billed to the key owner … and is not resold or intermediated as described above."
- On developers: "Developers building products or services that interact with Claude's capabilities, including those using the Agent SDK, should use API key authentication through Claude Console".

**From the gateway documentation:**

- Claude apps gateway: "At `/login`, Claude Code requires the gateway's hostname or IP address to resolve only to private addresses … For a gateway you host, any public address outside a block you declare is rejected" [P-page CC-APPSGW].
- Other gateways: Anthropic "doesn't endorse, maintain, or audit third-party gateway products, and doesn't support routing Claude Code to non-Claude models through any gateway" [P-page CC-LLMGW].
- Billing through a gateway: "When developers connect through a gateway with a gateway credential, usage is billed to your organization's provider account at API rates" [P-page CC-GW].

**From the Console workspace documentation:** when an organisation member signs in to Claude Code with a Console account, "Claude Code mints a per-user API key in this workspace at sign-in". The Claude Code workspace "is the only workspace that supports per-user monthly spend limits" [P-page API-WS].

**From the Team seat documentation** [P-page HC-SEATS]:

- "Each seat on a Team plan is assigned to one named individual, and only that person may use it."
- "Reassigning a seat is meant for normal team changes, such as a user joining, leaving, or changing roles. It isn't designed for rotating one seat among several active users."

**(b) Questions for legal review:**

- Are external contributors "the customer's own authorized users", or members of the project's Console or Team organisation? The documents do not define this.
- Does Option A's alternative design count as "running Claude Code in your products or services"? In that design the Agent SDK runs the shared plugin server-side for contributors, and that category forbids paying for end users' usage. Or is it ordinary Agent-SDK development with the project's own API key, which the same page directs to Console API keys?

---

## 4. Practical alternatives for contributors in mainland China (Q4)

### 4.1 (a) Claude Code pointed at another endpoint: what Anthropic's docs say

- **The mechanism exists.** `ANTHROPIC_BASE_URL` (with `ANTHROPIC_AUTH_TOKEN`) points Claude Code at a gateway or proxy. "`ANTHROPIC_BASE_URL` changes where requests are sent, not which model answers them." [P-page CC-MODEL, CC-GW, CC-LLMGW]
- **Anthropic does not support non-Claude models this way:** "doesn't support routing Claude Code to non-Claude models through any gateway" [P-page CC-LLMGW].
- **Traffic still goes to Anthropic.** "Claude Code itself sends version checks and downloads directly to Anthropic, separate from the gateway path." [P-page CC-GW]
- **WebFetch check.** WebFetch "sends the requested hostname to api.anthropic.com"; the check "runs regardless of which model provider you use". If the network blocks api.anthropic.com, WebFetch fails unless `skipWebFetchPreflight` is set. [P-full CC-DATA]
- **The client itself is listed.** The Supported Regions Policy names **Claude Code** among the "apps" that "are available only in the countries and regions listed" [P-full SRP].
  - **(b) Legal-review flag:** running the Claude Code client in mainland China against a non-Anthropic model may itself be "use … of Anthropic's products" in an unsupported region. The text lists the client as a product but does not address this configuration.

### 4.2 (a) Chinese providers' Anthropic-compatible endpoints: what could and could not be verified

| Provider | Evidence obtained here | Status |
|---|---|---|
| Moonshot (Kimi) | Kimi-K2 README: "You can access Kimi K2's API on https://platform.moonshot.ai , we provide an OpenAI/Anthropic-compatible API for you. The Anthropic-compatible API maps temperature by `real_temperature = request_temperature * 0.6`" (repo HEAD 2025-10-31). Kimi Code CLI connects to "the Kimi Code managed service" through `/login` or to a Kimi Platform API key (OpenAI-compatible), and can also connect "Claude with an Anthropic API key" [P-page KIMI-K2, KIMI-CODE] | Anthropic-compatible API **confirmed as a 2025 README statement**. A Claude-Code-specific guide, current endpoint URL, pricing and 2026 status are **[U]** |
| Zhipu / Z.ai (GLM) | The GLM README cites "better real-world performance in applications such as Claude Code、Cline、Roo Code and Kilo Code" and points to the "Z.ai API Platform" (docs.z.ai). The GLM-5 README (HEAD 2026-10-15) covers GLM-5.3 API services on the Z.ai platform [P-page GLM] | A "GLM Coding Plan" or Anthropic-compatible endpoint is **[U]**: not stated in the READMEs; docs host not read |
| DeepSeek | No primary statement found. The DeepSeek-V3.2-Exp README does not mention Anthropic or Claude Code [P-page]; a third-party listing in awesome-deepseek-integration is not authoritative | **[U]** |
| Alibaba (Qwen / DashScope / Model Studio) | Qwen3-Coder README: "supporting most platforms such as **Qwen Code**, **CLINE**, **Claude Code**", with a "Prompt with Claude Code" demo (repo HEAD 2026-03-24) [P-page QWEN3-CODER] | Model **compatibility with Claude Code is stated**; a DashScope Anthropic-compatible endpoint is **[U]** |
| MiniMax | MiniMax-M2 README: SWE-bench scores were obtained "using the claude-code CLI (300 max steps) as the evaluation scaffold"; the API is on "MiniMax Open Platform" (repo HEAD 2026-10-26) [P-page MINIMAX] | Use with the Claude Code client is **implied**; a documented Anthropic-compatible endpoint is **[U]** |

**Data-use terms.** I read no provider's terms on training, retention or cross-border use of API or coding-plan inputs. All are **[U]**.

### 4.3 (a) Chinese agent CLIs and `SKILL.md`

| Tool | Skill support | Skill locations | Frontmatter it reads | Source |
|---|---|---|---|---|
| **Kimi Code CLI** (Moonshot; replaces the archived Kimi CLI) | Yes: "Agent Skills are a lightweight mechanism for extending model capabilities in Kimi Code CLI" | User: `~/.kimi-code/skills/`, `~/.agents/skills/`. Project: `.kimi-code/skills/`, `.agents/skills/` | `name` and `description` (both required in directory form), `type`, `whenToUse` (also `when_to_use`), `disableModelInvocation` (also `disable-model-invocation`), `arguments` | [P-page KIMI-CODE] (repo HEAD 2026-11-05) |
| Kimi CLI (Python; **archived**) | Yes, cited agentskills.io | Also read `~/.claude/skills/` and `.claude/skills/` | `name`, `description`, `license`, `compatibility`, `metadata`, `type` | [P-page KIMI-CLI] (HEAD 2026-09-22; README: "This project has been archived and is no longer maintained") |
| **Qwen Code** (Alibaba Qwen team) | Yes ("Agent Skills") | `~/.qwen/skills/`, `~/.agents/skills/`, `.qwen/skills/`, `.agents/skills/`; can add `~/.claude/skills` via `skills.directories` | `name` (a broader character set than the spec), `description`, `priority`, `paths`, `user-invocable`, `disable-model-invocation`. "Qwen Code reads the `allowedTools` frontmatter field. An `allowed-tools` field written for another agent is ignored." | [P-page QWEN-CODE] (repo HEAD 2026-11-05) |
| TRAE; Deep Code (deepcode.vegamo.cn) | Listed in the Agent Skills client showcase | — | — | [P-full AS-CLIENTS]. Their origin and availability in China are [U] |

Neither Kimi Code CLI nor Qwen Code appears in the agentskills.io client showcase. Their own documentation nevertheless documents `SKILL.md` support. [P-full AS-CLIENTS; P-page KIMI-CODE, QWEN-CODE]

### 4.4 (b) Implications for interview consistency and data-use (assessment)

- **No model parity.** A DeepEcon skill would *load* in Kimi Code CLI or Qwen Code, but the interview would be run by a different model with a different harness. Results from such sessions belong to a separate, unvalidated condition until the simulated-contributor protocol evaluation passes for that pair of harness and model.
  - Packages should record the harness, model and version.
  - Shepherds should treat these contributions as a stratum when analysing interview quality.
- **Harness-specific features will not carry over.** Hooks, permission rules, `allowed-tools` (ignored by Qwen Code), forked context and plugin packaging all differ by tool. Protection of the original package (Option B §6.1) would rest on the helper scripts and integrity checks, not on Claude Code hooks.
- **Data-use terms change.** Hidden-tier material (flawed variants, answer keys) sent to a provider whose training and retention terms are unknown is a contamination risk the project cannot assess today. Provider terms, and Chinese data rules (R9), must be checked before any recommendation.
- **"Point Claude Code at a Chinese endpoint" is the weakest fallback.** Anthropic does not support it, the client still contacts Anthropic, and it raises the legal question in §4.1. The cleaner fallbacks are the alternative harnesses above, or a non-Claude hosted interview (Option A variant). Both lose model parity.

---

## 5. Agent Skills open standard: who supports `SKILL.md`, and which fields are portable (Q5)

### 5.1 (a) The standard and its adopters

- **Origin.** "The Agent Skills format was originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products." Code is Apache-2.0 and documentation CC-BY-4.0. [P-full AS-README] (agentskills/agentskills @83021e2, 2026-11-04)
- **Format.** A skill is a folder with `SKILL.md` (YAML frontmatter plus Markdown). Optional folders are `scripts/`, `references/` and `assets/`.
- **Progressive disclosure.** Metadata is about 100 tokens, instructions under 5,000 tokens are recommended, and resources load on demand. "Keep your main `SKILL.md` under 500 lines." [P-full AS-SPEC]
- **Client Showcase.** It lists **46** clients [P-full AS-CLIENTS]: Junie, ZeroClaw, Gemini CLI, Autohand Code CLI, OpenCode, OpenHands, Mux, **Cursor**, Amp, Letta, Firebender, Goose, **GitHub Copilot**, **VS Code**, **Claude Code**, **Claude**, **ChatGPT & Codex**, Piebald, Factory, pi, Databricks Genie Code, Agentman, TRAE, Spring AI, Roo Code, Mistral AI Vibe, Command Code, Ona, VT Code, Qodo, Laravel Boost, Emdash, Snowflake Cortex Code, Kiro, Workshop, Google AI Edge Gallery, nanobot, fast-agent, bub, Tabnine, Vita, Superconductor, Deep Code, Pulumi Neo, Hermes Agent and OpenClaw.
  - A showcase entry is the standard's own listing, not verification by the vendor.

### 5.2 (a) Product-by-product evidence read here

| Product | Evidence | Notes |
|---|---|---|
| **Claude Code** | "Claude Code skills follow the Agent Skills open standard … Claude Code extends the standard" [P-page CC-SKILLS] | Reads `.claude/skills/` (personal, project, nested, enterprise) and plugin skills. **`.agents/skills/` is not listed** among its locations [P-page CC-SKILLS] |
| **Cowork, claude.ai, Skills API** | Skills must be enabled or uploaded to the claude.ai account; Cowork "don't read `~/.claude/skills/` on your machine" [P-page CC-SKILLS] | Upload accepts only the six spec fields (§5.3) |
| **Gemini CLI** | "Based on the Agent Skills open standard"; locations `~/.gemini/skills/`, `~/.agents/skills/`, `.gemini/skills/`, `.agents/skills/`. Activation is a tool call with a **consent prompt** [P-page GEMINI] (@1fe22af, 2026-11-04) | "The `.agents/skills/` alias provides an interoperable path" |
| **OpenAI Codex** | User docs live on developers.openai.com (not read). The open-source loader parses only `name`, `description` and `metadata.short-description` [P-page CODEX `codex-rs/skills/src/parser.rs` @e7f32cf, 2026-11-05]. VS Code's docs give Codex's locations as `.agents/skills/` and `~/.agents/skills/` [P-page VSCODE] | From reading the code: other keys appear to be ignored rather than rejected [U: inference] |
| **GitHub Copilot / VS Code** | "Agent Skills is an open standard that works across multiple AI agents, including GitHub Copilot in VS Code, Copilot CLI, the GitHub Copilot app, and the experimental OpenAI Codex integration" (the source's `{% data variables … %}` product-name placeholders resolved by me). Locations `.github/skills/`, `~/.copilot/skills/`; local sessions also read `.claude/skills/` and `.agents/skills/` [P-page VSCODE] (doc "DateApproved: 11/4/2026") | Supports `name`, `description`, `argument-hint`, `user-invocable`, `disable-model-invocation` and `context: fork` [P-page VSCODE] |
| **Cursor** | Listed with instructions at cursor.com/docs/context/skills [P-full AS-CLIENTS] | Cursor's own docs not read; field support [U] |
| **Kimi Code CLI, Qwen Code** | See §4.3 [P-page] | Both read `.agents/skills/` |

### 5.3 (a) Portable and Claude-specific frontmatter

**Spec fields** [P-full AS-SPEC]:

| Field | Required | Constraint |
|---|---|---|
| `name` | Yes | Max 64 characters; lowercase letters, numbers and hyphens; no leading, trailing or consecutive hyphens; "Must match the parent directory name" |
| `description` | Yes | Max 1,024 characters; non-empty |
| `license` | No | — |
| `compatibility` | No | Max 500 characters |
| `metadata` | No | String-to-string map |
| `allowed-tools` | No | "Experimental. Support for this field may vary between agent implementations" |

**Claude Code-only fields** [P-page CC-SKILLS]: `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`.

**Upload behaviour** [P-page CC-SKILLS]: "claude.ai skill uploads, the Skills API, and packaging with `package_skill.py` … `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`". "If you include any field the spec doesn't allow, packaging or upload fails with a hard error instead of ignoring the field".

**Support for non-spec fields outside Claude Code (partial convergence):**

| Field | VS Code | Kimi Code CLI | Qwen Code |
|---|---|---|---|
| `user-invocable` | Yes | — | Yes |
| `disable-model-invocation` | Yes | Yes (camelCase or kebab) | Yes |
| `argument-hint` | Yes | — | — |
| `context: fork` | Yes | — | — |
| `when_to_use` / `whenToUse` | — | Yes | — |
| `arguments` | — | Yes | — |
| `paths` | — | — | Yes |

Sources: [P-page VSCODE, KIMI-CODE, QWEN-CODE].

### 5.4 (b) Implications (assessment)

- **Two layers.** A DeepEcon skill can carry a **portable core**: spec-only frontmatter, stage cards in `references/`, helpers in `scripts/`. It can then add a **Claude Code layer** of plugin, hooks and Claude-only fields. Anything meant for Cowork or claude.ai must use spec-only frontmatter or the upload fails.
- **Locations.** One folder can serve several tools if it is placed, or symlinked, at `.claude/skills/<name>/` for Claude Code and `.agents/skills/<name>/` for Gemini CLI, Codex, Kimi Code CLI, Qwen Code and VS Code. Claude Code's docs do not list `.agents/skills/`.
- **The protocol must not depend on Claude-only behaviour.** Consent prompts (Gemini), whether skills load automatically or manually, and how tool permissions are granted all differ by tool. Data-protection controls must live in scripts and in the protocol text. Qwen Code's own docs state that "Everything in a `SKILL.md` body is an instruction to the model … following it depends on the model."

---

## 6. Data-use policies (Q6)

### 6.1 (a) Consumer plans (Free, Pro, Max, Ultra, including Claude Code signed in with these plans)

- **Training is opt-out.** The pricing table's "Model training" row reads "Opt-out" for Free, Pro, Max and Ultra, and "None by default" for Team and Enterprise [P-full PRICING].
- **Consumer Terms** (effective 8 Oct 2025): "We may use Materials … including training our models, unless you opt out of training through your account settings. Even if you opt out, we will use Materials for model training when: (1) you provide Feedback to us regarding any Materials, or (2) your Materials are flagged for safety review". "Materials" means Inputs and Outputs. [P-page COTOS]
- **Privacy Policy** (effective 10 Sep 2026) states the same opt-out rule with two exceptions that apply even after opt-out: conversations "flagged for safety review", and materials "you've explicitly reported … to us (for example via our feedback mechanisms)" [P-page PRIV].
- **The 2025 change** (announcement of 28 Aug 2025) [P-full NEWS-2025-08]:
  - "We're now giving users the choice to allow their data to be used to improve Claude".
  - Existing users had until 8 Oct 2025 to choose.
  - "We are also extending data retention to five years, if you allow us to use your data for model training … If you do not choose to provide your data for model training, you'll continue with our existing 30-day data retention period."
  - It "do[es] not apply to services under our Commercial Terms, including Claude for Work, Claude for Government, Claude for Education, or API use".
  - **Not verified:** whether the training toggle is preset to on at sign-up [U].
- **Claude Code documentation** confirms the 5-year and 30-day periods for consumer accounts and adds two retention rules [P-full CC-DATA]:
  - "Transcripts shared via /feedback, or via /bug and /share … are retained for 5 years".
  - Session-survey transcript sharing is opt-in and "retained for up to 6 months".

### 6.2 (a) Commercial plans and the API

- **No training.** Commercial Terms B: "Anthropic may not train models on Customer Content from Services." [P-page CTOS]
  - Claude Code doc: commercial users are not trained on "unless the customer has chosen to provide their data to us for model improvement (for example, the Developer Partner Program)" [P-full CC-DATA].
  - Team plan for scientists FAQ: "Claude does not train on your conversations, uploaded files, or research data." [P-full SCI]
- **Default retention: the two statements are inconsistent.**
  - Claude Code doc: "Commercial users (Team, Enterprise, and API): Standard: 30-day retention period" [P-full CC-DATA].
  - API retention doc: "Conversation content (your prompts and Claude's outputs) is not retained by default; the exception is Covered Models, which require 30-day retention". This sentence sits in a list of commitments for features that "necessarily require storage" [P-page API-RET].
  - The API doc refers standard retention to a privacy-centre article that I could not reach (§11). **Unresolved.**
- **Covered Models.** "Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, and Claude Mythos 5 … require 30-day data retention and are not available under ZDR unless expressly authorized by Anthropic." [P-page API-RET]
- **ZDR on the API.** "To request ZDR for your organization, contact the Anthropic sales team. ZDR is enabled per organization." [P-page API-RET]
  - It covers "Claude Code with API keys from a Commercial organization".
  - It does not cover Console usage, Managed Agents, consumer plans, the Team and Enterprise product interfaces (except Claude Code on Enterprise), Files API, code execution, or MCP connector [P-page API-RET].
- **ZDR for Claude Code on Enterprise.** "available to qualified accounts on Claude for Enterprise … not included in the standard Claude for Enterprise plan". [P-full CC-ZDR]
  - Under ZDR, flagged sessions may be retained "for up to 2 years". Cowork and claude.ai chat are not covered [P-full CC-ZDR].
- **Enterprise Compliance API.** It stores "Local session transcripts (from sessions on users' machines, in apps such as Cowork and Claude Code) … for 6 years by default, or for your organization's custom conversation retention period" [P-page API-RET].
- **Residency.** US-only inference (`inference_geo: "us"`) is "priced at 1.1x the standard rate across all token pricing categories" for Claude 4.6 and later models. The only documented values are `"global"` (the default) and `"us"`. [P-page API-RES, API-PRICE; P-full PRICING]
- **Education.** Anthropic states "the Anthropic Consumer Terms of Service and Privacy Policy do not apply to the use of the Claude for Education plan where Anthropic acts as the data processor"; use "is governed by the agreement between Anthropic and your university" [P-page HC-EDU-DATA].

### 6.3 (a) Claude Code client specifics [P-full CC-DATA]

- **What leaves the machine.** "Claude Code runs locally. To interact with the LLM, Claude Code sends data over the network. This data includes all user prompts and model outputs".
- **Local copies.** "Claude Code clients store session transcripts locally in plaintext under `~/.claude/projects/` for 30 days by default … Transcripts of sessions started or most recently continued in Claude Desktop or Cowork are exempt from that limit by default."
- **Telemetry and feedback.**
  - Metrics "never include your code, prompts, or file paths" (opt out with `DISABLE_TELEMETRY=1`).
  - Error reports are redacted.
  - `/feedback` sends "a copy of your conversation history including code" (disable with `DISABLE_FEEDBACK_COMMAND=1`).

### 6.4 University, IRB and AEA guidance on confidential data and commercial LLMs

**(a) AEA Data Editor.** The guidance page "Preparing your code for computational verification" (dated 2025-12-04; site source @519f186, 2026-10-22) [P-page AEA]:

- It advises: "You can use an AI assistant (such as Claude, ChatGPT, or GitHub Copilot) to guide you through this checklist".
- Its only data caution concerns a different system: "You should not upload sensitive data to the SIVACOR system".

I searched the published guidance, posts and pages sources for any statement on sending confidential or restricted data to commercial LLMs and found none (search of `_guidance`, `_posts`, `_pages`; drafts excluded).

**University, IRB and data-repository guidance** (ICPSR, FSRDC, data-use agreements) could not be accessed: search budget exhausted, hosts not tried. Typical data-use-agreement terms that forbid disclosure to unapproved third parties, and enclave rules that block external network services, are **[U]** recollection.

### 6.5 (b) Implications (assessment)

- **Consumer accounts carry contamination and retention risk in Option B.** Hidden-tier material could be trained on if the setting is on, and is kept for 5 years. Even with opt-out, `/feedback`, thumbs ratings and flagged content are exceptions. The disclosure screen in S0 should tell contributors to opt out and to avoid `/feedback` on hidden-tier sessions; the package should record the account type.
- **Commercial access makes terms uniform.** Under Option A, or Option B with access the project provides, no training occurs. Whether retention is 30 days or none needs resolving, and ZDR is only possible through sales.
- **Choose models with retention in mind.** Fable or Mythos models force 30-day retention.
- **Enterprise defaults need attention.** If the project gives contributors Enterprise seats, the organisation's Compliance-API retention of local transcripts (6 years by default) should be set deliberately.
- **The no-restricted-data rule is the prudent default.** Rule DP-28 keeps restricted data out of the model under both options. It matches the absence of any institutional "yes" in the sources read. Each contributor's data-use agreement and IRB must be the controlling authority [U: specific institutional rules not read].

---

## 7. Academic programmes and funding (Q7)

### 7.1 (a) What the sources say

**AI for Science**

- Launched 5 May 2025: "free API credits to support researchers working on high-impact scientific projects, with a particular focus on biology and life sciences". "Researchers attached to a research institution … can apply through our application form" [P-full AI4S-2025].
- Expanded 27 Aug 2026: "you can apply to our AI for Science program for up to $50,000 in credits per project. **Any researcher is eligible to apply.**" "To date, we've largely supported scientists using Claude for biological sciences. We are now looking to offer credits for researchers in other scientific fields as well" [P-full AI4S-2026-08].
- Programme page wording: "application-based and reviewed on merit" [P-full SCI].
- Extended to funders and institutions on 28 Oct 2026. Claude credits go to organisations "which will distribute these resources to ambitious researchers", including "The Alfred P. Sloan Foundation … supports original research and education in science, technology, engineering, mathematics, and economics" and the US NSF [P-page AI4S-2026-10].

**Claude Team plan for scientists** [P-full SCI, SCI-TERMS]

- **Price.** Standard seats "$0/month regularly $20/month"; Premium "$15/month regularly $100/month". "Promotional pricing for 12 months for verified research groups". Annual billing "$0 / $180 per seat". 1–25 seats per group. Capped at "an initial group of 10,000 Scientists".
- **Eligibility.** "Principal investigators (PIs) or equivalent at accredited universities and nonprofit research institutes working in the natural sciences, mathematics, computer science, engineering, and related fields". "Anthropic determines eligibility in its sole discretion".
- **Who can be added.** "Once a PI is verified, the PI may add members of their lab (including post doctorates, graduate students, and researchers)".
- **Location.** The redeemer must "be located in a region where the Plan is available".
- **Inclusions.** "Access to Claude Science, Code, & Cowork".
- **What the discount does not cover.** Extra usage is billed at standard rates. The promotion "does not apply to the Claude Developer Platform (API)".
- **Inactivity.** Pricing may end after "no Qualifying Usage for 90 consecutive days".

**Claude for Education** is a university-wide institutional plan with no public price. It includes "Dedicated API credits and educational features for student learning" [P-full PRICING; P-page EDU].

**Monthly API credits in subscriptions.** Max includes $100 a month, Ultra $200 a month, and Team "Up to $500 per month in pooled API credits" [P-full PRICING].

**Economic Futures Research Fund.** It "supports ambitious external research on interventions to prepare society for the economic impacts of AI" [P-page EF]. Its priorities concern workers, transitions, income support and public investment; benchmark construction is not among them.

**Campus programmes.** Student ambassador stipends of USD 3,600; the programme is "closed for Fall 2026" [P-page CAMPUS]. Not relevant.

**Coefficient Giving.** The ReplicatorBench README states: "This project is funded by Coefficient Giving as part of its 'Benchmarking LLM Agents on Consequential Real-World Tasks' program." [P-page COS; also reported in R4] The programme's eligibility, budget and whether it is open in 2026 are **[U]**; coefficientgiving.org was not tried (§11).

### 7.2 (b) Implications (assessment)

- **AI for Science fits project-side costs best.** It can fund either option: Option A's API bill, Option B access provided by the project, and validation trials. Economics is no longer excluded by the text ("Any researcher"), but merit review and fit are uncertain.
- **The Team plan for scientists is weaker for DeepEcon than it looks.**
  - Economics is not named, so eligibility rests on "related fields" and Anthropic's discretion.
  - Seats are for "members of their lab". External contributors from other universities do not obviously qualify.
  - It may suit a lead PI's own team or research assistants.
- **Sloan's role as a credit distributor** is a plausible economics-friendly channel [U: Sloan's application route not read].

---

## 8. Fact-check table (Q8)

Drafts were not edited. A **verdict** of *confirmed* means the claim holds. *Corrected* means a source contradicts or materially refines it. *Still unverifiable* means no primary source could be read in this session.

| # | Draft location | Claim (short quote) | Verdict | Correct fact | Citation |
|---|---|---|---|---|---|
| B1 | option-b §3.2 | "Other agent tools that read the open Agent Skills format … Could run a portable subset … [U] Pending R3" | **Confirmed, with limits** | The standard's showcase lists 46 clients. The own docs of Gemini CLI, VS Code/Copilot, Kimi Code CLI and Qwen Code confirm `SKILL.md` support. Codex's loader parses `SKILL.md`. Only the six spec fields are portable; hooks, plugins and permissions are not | AS-CLIENTS, AS-SPEC, GEMINI, VSCODE, KIMI-CODE, QWEN-CODE, CODEX |
| B2 | option-b §5.3 | "use the skill in another agent tool that reads the open skill format" | **Confirmed** | As B1. Tools read `.agents/skills/` (not read by Claude Code) or `.claude/skills/` (VS Code local sessions; the archived Kimi CLI) | CC-SKILLS, VSCODE, GEMINI, KIMI-CODE, QWEN-CODE |
| B3 | option-b §5.3 | "or point Claude Code at another provider's compatible endpoint [U: per R3]" | **Corrected (qualified)** | Technically possible via `ANTHROPIC_BASE_URL`, but Anthropic "doesn't support routing Claude Code to non-Claude models through any gateway"; the client still contacts Anthropic, and WebFetch checks hostnames with api.anthropic.com. Moonshot states an "Anthropic-compatible API" (2025 README). Zhipu, DeepSeek, Alibaba and MiniMax endpoints remain unverified. **Legal flag:** Claude Code is itself an Anthropic product "available only" in supported regions | CC-LLMGW, CC-GW, CC-DATA, SRP, KIMI-K2 |
| B4 | option-b §10 | "The contributor's account terms … [U: training and retention terms per R3]" | **Confirmed and specified** | Consumer accounts: training unless opted out; 5-year retention if on, 30-day if off; feedback and flagged content are exceptions; `/feedback` transcripts are kept 5 years. Commercial accounts: "may not train"; retention 30 days per the Claude Code doc, which conflicts with the API doc (see B5/A1) | COTOS, PRIV, NEWS-2025-08, CC-DATA, CTOS, API-RET |
| B5 | option-b §10 key point | "if a contributor uses a consumer plan with model-training use enabled, hidden-tier material … could enter training data" | **Confirmed; risk is broader** | Also applies after opt-out to material submitted as feedback (thumbs, `/feedback`) or flagged for safety review; retention reaches 5 years when training is on | COTOS, PRIV, CC-DATA |
| B6 | option-b §10 table | "Telemetry from the client … Possibly … [U: per R2]" | **Confirmed (R2 owns it)** | Metrics exclude code, prompts and paths; error reports are redacted; `/feedback` sends transcripts; session-survey transcript sharing is opt-in | CC-DATA |
| B7 | option-b §12 | "On a subscription the marginal cost is zero, but plan limits may bind [U]" | **Confirmed in principle; extent still unverifiable** | 5-hour and weekly limits apply across chat, Claude Code and Desktop; there are no published quotas; usage credits continue at API rates; Cowork "consumes limits faster". Whether a full contribution fits within Pro must be measured in the pilot | HC-LIMITS, PRICING, COWORK |
| B8 | option-b §12 | "Contributor subscription … Plan prices per R3 [U]" | **Filled in** | Pro $20 a month ($17 on annual billing); Max $100; Ultra $200; Team Standard $25 / $20; Premium $125 / $100; Enterprise $20 a seat (annual, minimum 20) plus usage; US prices excluding tax; regional prices vary | PRICING, HC-TEAM, HC-PRO |
| B9 | option-b §12 | "About $6–46 at Opus 5.5 API list prices" | **Confirmed (inputs)** | Opus 5.5: $4 input, $20 output, $0.20 cache read, $5 for 5-minute writes and $8 for 1-hour writes per million tokens | API-PRICE, PRICING |
| B10 | option-b §16 | "Hidden material enters model training through consumer accounts — Low–Medium [U: per R3]" | **Mechanism confirmed; likelihood still unverifiable** | Depends on each contributor's setting (default state at sign-up [U]) and on use of feedback; mitigated by commercial access the project provides, plus an opt-out instruction | COTOS, PRICING, NEWS-2025-08 |
| B11 | option-b §16, §17 | "Contributors in unsupported regions cannot use Claude"; "regional availability remains a hard constraint" | **Confirmed and broadened** | Mainland China, Hong Kong and Macau are unsupported; Taiwan is supported. The rule also covers anyone "physically located" there (including travellers) and, as written, personnel of entities headquartered there even when abroad | SRP, HC-WHERE, API-REGIONS |
| B12 | option-b §17 | "if the project reimburses subscriptions, B can cost *more* than A's direct API usage" | **Confirmed** | One month of Pro ($20) is about equal to the central API estimate ($17). Two or more months, or Max ($100), exceeds it. At 200 contributors, one month of Pro each is $4,000 against $3,404 central API cost (my arithmetic) | PRICING; cost doc §3 |
| B13 | option-b §11 | "Model provider … Availability by region (O-007); terms" | **Confirmed** | As B11. The policy also covers "Claude models offered through cloud platforms and authorized resellers", so routing through a cloud provider does not change regional eligibility | SRP |
| A1 | option-a §10 | "Commercial terms: no training on inputs by default [U: confirm current terms and default retention per R3]" | **Corrected** | It is not a default. Commercial Terms B: "Anthropic may not train models on Customer Content from Services" (opt-in programmes such as the Development Partner Program are customer choices). Default retention: 30 days per the Claude Code doc, versus "not retained by default" except Covered Models (30 days) per the API doc, **unresolved**. ZDR is available on request to eligible organisations; Fable and Mythos models require 30-day retention | CTOS, CC-DATA, API-RET |
| A2 | option-a §10 | "data residency options for US-only inference at a 1.1× price" | **Confirmed** | `inference_geo: "us"`, 1.1× on all token categories for Claude 4.6 and later models. Documented values are only `"global"` and `"us"` (no EU or Asia option documented) | API-RES, API-PRICE, PRICING |
| A3 | option-a §10 key points | "uniform and favourable … no consumer-account training exposure" | **Confirmed**; two additions | Commercial "may not train" applies to all contributors. Also: D.3 says the project "must notify its Users" that factual assertions in outputs need independent checking. The 2026 Usage Policy requires "consumer-facing chatbots or AI agents that communicate directly with external users" to disclose that users are "interacting with AI"; whether an expert interview is "consumer-facing" is unclear, but the disclosure is easy to provide | CTOS, AUP-2026 |
| A4 | option-a §10 | "GDPR; China's cross-border transfer rules [U: per R9]" | **Out of scope** (R9) | Not assessed here | — |
| A5 | option-a §11 | "regional policy for serving end users (O-007)" | **Confirmed: explicit terms exist** | Usage Policy 2025: "Access or facilitate … access to Claude to persons, entities, or users in violation of our Supported Regions Policy". Usage Policy 2026: "… provide others (including end users) with access …". Commercial Terms D.2 binds "Customer and its Users". Legal review needed on diligence and edge cases | AUP-2025, AUP-2026, CTOS, SRP |
| A6 | option-a §16 | "Provider terms restrict serving end users in some regions — Unknown [U: per R3]" | **Corrected** | Not unknown: the texts do restrict it (A5) for end users physically in unsupported regions and, as written, for personnel of entities headquartered there. What remains open is the expected diligence and the edge cases (§3.3) → legal review **before** recruitment | AUP-2025, AUP-2026, SRP, CTOS |
| A7 | option-a §11 | "Auth and e-mail services … Deliverability in some regions [U]" | **Out of scope** | Not assessed | — |
| C1 | cost §5, own-subscription row | "consumer plans may allow training use if opted in [U: R3]" | **Corrected** | Consumer plans permit training **unless the user opts out** ("Opt-out" on the pricing page; "unless you opt out" in the Consumer Terms), with 5-year retention when on; feedback and flagged-content exceptions apply even after opt-out | PRICING, COTOS, NEWS-2025-08 |
| C2 | cost §5, reimburse row | "One or more months of a plan per contributor [U: R3 prices] — may exceed direct API cost" | **Confirmed** | Prices as B8; comparison as B12. Max is monthly only, so reimbursement is per month | PRICING, HC-MAX |
| C3 | cost §5, API-keys row | "Project-issued API keys with spend caps … Commercial terms" | **Confirmed in a specific form; terms caveat** | Console organisation members who sign in to Claude Code get per-user keys in the Claude Code workspace, "the only workspace that supports per-user monthly spend limits"; other workspaces take monthly workspace caps. Usage is under Commercial Terms. Caveats: contributors join the project's Console organisation (legal review: "the customer's own authorized users"); regional rules apply per person | API-WS, CC-LEGAL, CTOS |
| C4 | cost §5, gateway row | "Project gateway (a small proxy issuing per-contributor tokens) … Enforceable at the gateway" | **Corrected (qualified)** | Anthropic's Claude apps gateway accepts only private-network addresses at `/login`, so it does not serve contributors on the open internet unless a private network or declared address blocks are used. A third-party gateway via `ANTHROPIC_BASE_URL` plus `ANTHROPIC_AUTH_TOKEN` bills the gateway's account at API rates, but Anthropic does not endorse or audit such gateways. Gateways can bound model choice (`availableModels`) but "The gateway decides where requests go, not which model the developer selects". Intermediating usage for end users is ambiguous under CC-LEGAL → legal review | CC-APPSGW, CC-GW, CC-LLMGW, CC-LEGAL |
| C5 | cost §5, sponsor row | "Sponsor credits (as Terminal-Bench-Science uses) … Reduced" | **Confirmed; programmes identified** | AI for Science: up to $50,000 per project, "Any researcher is eligible to apply". Team plan for scientists: eligibility for economics is ambiguous. Sloan and NSF distribute Claude credits. Coefficient Giving programme exists, details [U] | AI4S-2026-08, AI4S-2026-10, SCI, COS |
| C6 | cost §5, platform row | "Project API account … Commercial terms for everyone" | **Confirmed**; add regional constraint | Commercial terms apply. End users remain bound by the Supported Regions Policy (A5) | CTOS, SRP |
| X1 | cost §2 (outside the assigned sections) | "Sonnet 5.5 … cache read $0.20" | **Corrected** | Sonnet 5.5 cache read is **$0.10 per million tokens** (5% of $2). Opus 5.5 is $0.20. The Sonnet sensitivity estimates are slightly overstated | API-PRICE, PRICING |
| X2 | option-a §3.2 (outside the assigned sections) | "Claude Agent SDK running the same skill as Option B on the server … [U: feasibility per R2]" | **Terms question raised** | If this counts as "running Claude Code in your products or services (e.g. in hosted sandboxes or other agent infrastructure)", then "Customers may not pay for, resell, or intermediate Claude usage on their end users' behalf". That conflicts with Option A's "project pays". The same page directs Agent-SDK developers to Console API keys. **Ask Anthropic or counsel** | CC-LEGAL |
| X3 | option-a §3.2 / cost §4 (outside the assigned sections) | "Managed Agents … $0.08 per session-hour plus tokens" | **Confirmed** | "$0.08 per session-hour for active runtime"; standard token rates apply | PRICING |

---

## 9. Implications for cost distribution and accessibility (assessment, balanced)

### 9.1 Who pays, and what each party gets

| Dimension | Option A: hosted platform on the project's API account | Option B: local skill |
|---|---|---|
| **Default payer for inference** | Project, at about $17 per contribution (central; cost doc). Contributors pay nothing | Contributor, at **$20 a month or more** (Pro), possibly $100 (Max) if limits bind; Free cannot run Claude Code. The cost is a barrier for unfunded contributors and research assistants |
| **The project's options to move the cost back to itself** | Already there | (1) Console organisation membership with per-user monthly spend limits: same cost as A. (2) Team seats at $20–25 a month: named-seat rules. (3) Enterprise at $20 per seat per month, billed annually, plus usage, with a 20-seat minimum (at least $4,800 a year in seat fees): spend limits, organisation model restrictions, possible ZDR (qualified accounts). (4) Reimbursing subscriptions: costs the same as or more than A (B12). (5) Team plan for scientists, only if eligibility and the "members of their lab" scope fit |
| **Data-use terms** | Uniform commercial terms: no training; 30-day or no retention (unresolved); ZDR possible through sales | Mixed by default: consumer accounts (training unless opted out; 5-year retention when on) and commercial accounts. Uniform only if the project provides access |
| **Model consistency** | Enforced by the server | Not enforced on contributors' own accounts. Enterprise organisation default model and model restrictions, or gateway allowlists, can bound it [P-page CC-MODEL, CC-GW]; R2 should confirm |
| **What the contributor must have** | A browser (A1 also needs local execution of run kits) | A paid plan or access the project provides, Claude Code or Desktop, and local software |
| **Mainland China, Hong Kong, Macau** | Serving these end users with Claude is restricted by the terms (§3). A non-Claude provider for those users means no parity, separate terms review, and cross-border data issues (R9) | Contributors there are outside supported use. Alternative harnesses (Kimi Code CLI, Qwen Code) can load the skill, with no parity and unknown data terms. Claude Code pointed at Chinese endpoints raises the §4.1 legal question |
| **Travellers and affiliated staff** | The same rule applies to contributors temporarily in unsupported regions and, as written, to personnel of entities headquartered there | Same |
| **Programme funding** | AI for Science credits can fund the API bill directly | Credits help only if the project provides access through its own organisation; a contributor's own subscription is not grant-funded unless reimbursed |
| **Operational burden of the project paying** | Billing and spend caps in one account | Onboarding contributors into an organisation (invites, seats, spend limits), offboarding, regional checks per member |

### 9.2 Points for collaborators (balanced)

1. **Region rules do not favour either architecture.** They attach to the person's location and affiliation, not to who runs the software. Neither option is a regional work-around. Both need the same legal review (O-007) and both need a non-Claude fallback if China-based contributors are essential.
2. **Paying for model access removes most of B's cost advantage.** The data-use and consistency arguments for A largely disappear once B uses access the project provides. What separates the options then is engineering, operations and support, in line with the cost doc's §5 note.
3. **Contributor-funded B shifts cost and risk.** Contributors pay, and the project loses control of training exposure and model choice. This is acceptable only if the pilot shows that contributors already hold suitable plans and follow the opt-out guidance.
4. **The Free plan cannot run Option B.** A's browser-only interview remains the lower-barrier path for contributors who do not already pay for Claude. A1's local run kits keep a technical step in either option.
5. **One terms question matters for A's simplest shared-code design** (Agent SDK running the plugin server-side; X2). Resolve it with Anthropic before Option A adopts that design.

---

## 10. Open questions

1. **Legal review (O-007).** Under the 2026 Usage Policy and Supported Regions Policy, what must a supported-region project do to avoid "provid[ing] … end users … access" from unsupported regions? Geo-blocking, attestations? How are VPN use and relayed or research-assistant-mediated interviews treated?
2. **Legal review.** Scope of "entities incorporated or headquartered in an unsupported region and their users or personnel" for individual academics using personal accounts abroad, joint-venture campuses, and branch campuses.
3. **Legal review.** Is running the Claude Code client in mainland China with a non-Anthropic model "use" of an Anthropic product in an unsupported region?
4. **Anthropic or counsel.** Can external contributors be "the customer's own authorized users", or members of the project's Console, Team or Enterprise organisation? Can seats be reassigned sequentially as contributions finish?
5. **Anthropic.** Does Option A's server-side Agent-SDK design fall under "running Claude Code in your products", which forbids paying for end users' usage (X2)?
6. **Anthropic.** Standard retention for API and Claude Code commercial traffic: 30 days, or "not retained by default" (A1)? Read the commercial privacy-centre article and the DPA.
7. **Consumer setting.** Is the model-training toggle preset to on at sign-up?
8. **Eligibility.** Would Anthropic treat economics as a "related field" for the Team plan for scientists, and are economists competitive for AI for Science credits? Ask before budgeting.
9. **Chinese providers.** Current Anthropic-compatible endpoints and Claude Code guides (Zhipu, DeepSeek, Alibaba, MiniMax; Moonshot's 2026 status). Their training, retention and cross-border terms for API and coding-plan inputs. Whether those terms allow research use by contributors outside China.
10. **Coefficient Giving.** Eligibility, budget and timing of "Benchmarking LLM Agents on Consequential Real-World Tasks".
11. **Institutional rules.** University, IRB and data-use-agreement guidance on sending code or derived outputs from restricted-data projects to commercial LLMs. Needs targeted searching.
12. **Pre-12-Nov-2026 wording** of the supported-countries page (its URL now redirects).
13. **Benchmark release licensing.** Some benchmark materials may be drafted with Claude, such as flawed variants or summaries. If those are published and third parties later use them as training data, do Anthropic's restrictions apply? CTOS D.4 forbids training competing models, and HC-OUTPUTS says "Our Terms do not allow the use of Outputs to train models that are competitive with Anthropic's own. It is also a violation of our Terms to support a third party's attempt to do the same." Low priority; for counsel when the release licence is drafted.

---

## 11. Access problems

- **WebSearch.** The first query returned "this turn's web search budget is used up (limit: 200 WebSearch calls per turn, shared by every agent in it)". No searches were performed for this note. As the tool instructed, I did not query search engines by other means.
- **Refused hosts** (recorded):
  - `assets.claude.com`, the PDF of the Supported Regions Policy: proxy `CONNECT` 403.
  - `privacy.anthropic.com`, consumer retention article and privacy-policy update notes: proxy 403 ("connect_rejected").
  - `privacy.claude.com`, the commercial and consumer retention articles cited by the API docs: WebFetch `getaddrinfo ENOTFOUND` ("outside the session's allowed network domains").
  - `privacy.claude.com` would need to be allowed in the session's network settings to resolve A1 and §6.2.
- **Hosts I stopped trying.** After these failures I followed the rule and did not try new hosts. Not read:
  - provider docs: platform.moonshot.ai/.cn, docs.z.ai / bigmodel.cn, api-docs.deepseek.com, Alibaba Model Studio / DashScope docs, platform.minimax.io;
  - vendor docs: developers.openai.com, geminicli.com, cursor.com, code.visualstudio.com; docs.github.com is known to be blocked;
  - agentskills.io (its source was read via GitHub instead), coefficientgiving.org, university and IRB pages;
  - aeadataeditor.github.io (github.io was refused for another agent in this session; its source was read via git instead).
  - The proxy's failure log also shows earlier refusals for openai.com, huggingface.co, nber.org, osf.io, pnas.org, metr.org and api.crossref.org.
- **Routes that worked:**
  - claude.com, www.anthropic.com, support.claude.com, code.claude.com and platform.claude.com (including `.md` endpoints and `llms.txt`);
  - raw.githubusercontent.com, and blobless `git clone --depth 1` from github.com (as in R1 and R4).
  - Clones were read only. One `git grep` over a blobless clone was stopped because it downloaded every blob.
- **Version limits.** The Supported Regions Policy page has no earlier version in its metadata; the earlier "supported countries" wording could not be recovered. The kimi-cli repository is archived; current statements come from MoonshotAI/kimi-code. The Kimi-K2 README predates 2026 (HEAD 2025-10-31).

---

## 12. Sources

All accessed 2026-11-05. Labels show how each source was read.

**Anthropic: plans and programmes**
- **PRICING:** Claude pricing, https://claude.com/pricing [P-full]
- **COWORK:** https://claude.com/product/cowork [P-page]
- **EDU:** https://claude.com/solutions/education [P-page]
- **SCI:** Claude Team plan for scientists, https://claude.com/programs/team-plan-for-scientists [P-full]
- **SCI-TERMS:** Promotional Offer Terms, effective 27 Aug 2026, https://www.anthropic.com/legal/team-plan-for-scientists-terms [P-full]
- **CAMPUS:** https://claude.com/programs/campus [P-page]
- **AI4S-2025:** "Introducing Anthropic's AI for Science Program" (5 May 2025), https://www.anthropic.com/news/ai-for-science-program [P-full]
- **AI4S-2026-08:** "Expanding our support for scientists" (27 Aug 2026), https://www.anthropic.com/news/expanding-support-for-scientists [P-full]
- **AI4S-2026-10:** "AI for Science expands to foundations and research institutions" (28 Oct 2026), https://www.anthropic.com/news/ai-for-science-expands-foundations-research-institutions [P-page]
- **EF:** Economic Futures, https://www.anthropic.com/economic-futures [P-page]

**Anthropic: legal and policy** (effective dates from page metadata)
- **SRP:** Supported Regions Policy, effective 12 Nov 2026, https://www.anthropic.com/legal/supported-regions (redirect from https://www.anthropic.com/supported-countries and https://www.anthropic.com/claude-ai-locations) [P-full]
- **AUP-2026:** Usage Policy, effective 12 Nov 2026, https://www.anthropic.com/legal/aup [P-page: scope, "Do Not Abuse Our Platform", fraud section, additional guidelines]
- **AUP-2025:** Usage Policy, effective 15 Sep 2025 (archived), https://www.anthropic.com/legal/archive/22742366-2ef0-4c7a-a833-6523f10d3944 [P-page: scope and the Supported Regions bullet, from page data]
- **CTOS:** Commercial Terms of Service, effective 17 Jun 2025, https://www.anthropic.com/legal/commercial-terms [P-page: A–I, J.1, M.7–M.9]
- **COTOS:** Consumer Terms of Service, effective 8 Oct 2025, https://www.anthropic.com/legal/consumer-terms [P-page: §§1–4, export, governing law]
- **PRIV:** Privacy Policy, effective 10 Sep 2026, https://www.anthropic.com/legal/privacy [P-page: training, retention, transfers]
- **NEWS-2025-08:** "Updates to Consumer Terms and Privacy Policy" (28 Aug 2025), https://www.anthropic.com/news/updates-to-our-consumer-terms [P-full]
- **NEWS-2025-09:** "Updating restrictions of sales to unsupported regions" (4 Sep 2025), https://www.anthropic.com/news/updating-restrictions-of-sales-to-unsupported-regions [P-full]

**Anthropic Help Center** (support.claude.com)
- **HC-PRO:** https://support.claude.com/en/articles/8325606-what-is-the-pro-plan [P-full]
- **HC-MAX:** https://support.claude.com/en/articles/11049741-what-is-the-max-plan [P-full]
- **HC-ULTRA:** https://support.claude.com/en/articles/17728952-what-is-the-ultra-plan [P-full]
- **HC-TEAM:** https://support.claude.com/en/articles/9266767-what-is-the-team-plan [P-full]
- **HC-SEATS:** https://support.claude.com/en/articles/12004354-purchase-and-manage-seats-on-team-plans [P-page]
- **HC-ENT:** https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan (dated 1 Sep 2026) [P-page]
- **HC-ENT-BILL:** https://support.claude.com/en/articles/11526368-how-am-i-billed-for-my-enterprise-plan [P-page]
- **HC-LIMITS:** https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work [P-full]
- **HC-CC-PLAN:** https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-max-or-ultra-plan [P-page]
- **HC-FABLE:** https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan [P-page]
- **HC-WHERE:** https://support.claude.com/en/articles/8461763-where-can-i-access-claude (dated 16 Mar 2026) [P-full]
- **HC-EDU-USE:** https://support.claude.com/en/articles/11139144-use-claude-for-education-at-your-university [P-page]
- **HC-EDU-DATA:** https://support.claude.com/en/articles/11732894-who-owns-and-manages-the-data-of-my-claude-for-education-account [P-full]
- **HC-OUTPUTS:** https://support.claude.com/en/articles/12326764-can-i-use-my-outputs-to-train-an-ai-model (dated 16 Mar 2026) [P-page]. See Open question 13.

**Anthropic documentation**
- **CC-DATA:** https://code.claude.com/docs/en/data-usage [P-full]
- **CC-ZDR:** https://code.claude.com/docs/en/zero-data-retention [P-full]
- **CC-LEGAL:** https://code.claude.com/docs/en/legal-and-compliance [P-full]
- **CC-GW:** https://code.claude.com/docs/en/gateways [P-full]
- **CC-LLMGW:** https://code.claude.com/docs/en/llm-gateway [P-page]
- **CC-APPSGW:** https://code.claude.com/docs/en/claude-apps-gateway [P-page]
- **CC-MODEL:** https://code.claude.com/docs/en/model-config [P-page]
- **CC-SKILLS:** https://code.claude.com/docs/en/skills [P-page: overview, locations, frontmatter, Cowork section]
- **API-RET:** https://platform.claude.com/docs/en/manage-claude/api-and-data-retention [P-page]
- **API-RES:** https://platform.claude.com/docs/en/manage-claude/data-residency [P-page]
- **API-PRICE:** https://platform.claude.com/docs/en/about-claude/pricing [P-page]
- **API-WS:** https://platform.claude.com/docs/en/manage-claude/workspaces [P-page]; also https://platform.claude.com/docs/en/manage-claude/spend-limits-api (Enterprise member spend limits) [P-page]
- **API-REGIONS:** https://platform.claude.com/docs/en/api/supported-regions [P-full]

**Agent Skills standard and other agent tools** (GitHub; read via raw.githubusercontent.com or blobless clone; commit and date of repository HEAD)
- **AS-README, AS-SPEC, AS-CLIENTS:** agentskills/agentskills @`83021e2be457a9b6679148719c1f6074f0ad975e` (2026-11-04): `README.md`, `docs/specification.mdx`, `docs/snippets/clients.jsx`. https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/docs/specification.mdx [P-full]. Published at https://agentskills.io/specification (not fetched). Also `anthropics/skills` `spec/agent-skills-spec.md`, which reads: "The spec is now located at https://agentskills.io/specification" [P-full]
- **GEMINI:** google-gemini/gemini-cli @`1fe22af` (2026-11-04), `docs/cli/skills.md`, `docs/cli/creating-skills.md` [P-page]
- **CODEX:** openai/codex @`e7f32cf` (2026-11-05), `codex-rs/skills/src/parser.rs`; `docs/skills.md` points to https://developers.openai.com/codex/skills (not fetched) [P-page]
- **VSCODE:** microsoft/vscode-docs @`7b97a83` (2026-11-04), `docs/agent-customization/agent-skills.md` ("DateApproved: 11/4/2026") [P-page]
- **KIMI-CODE:** MoonshotAI/kimi-code @`2b8afaf` (2026-11-05), `docs/en/customization/skills.md`, `docs/en/configuration/providers.md` [P-page]
- **KIMI-CLI:** MoonshotAI/kimi-cli @`9ab1286` (2026-09-22), `README.md` (archived notice), `docs/en/customization/skills.md` [P-page]
- **QWEN-CODE:** QwenLM/qwen-code @`bff144a` (2026-11-05), `docs/users/features/skills.md` [P-page]

**Chinese model providers** (READMEs only)
- **KIMI-K2:** MoonshotAI/Kimi-K2 @`1b4022b` (2025-10-31), `README.md` [P-page]
- **GLM:** zai-org/GLM-4.5 `README.md` (main branch as of 2026-11-05; describes GLM-4.6 and 4.7); zai-org/GLM-5 @`83c03d3` (2026-10-15) `README.md` [P-page]
- **QWEN3-CODER:** QwenLM/Qwen3-Coder @`33bc6aa` (2026-03-24), `README.md` [P-page]
- **MINIMAX:** MiniMax-AI/MiniMax-M2 @`e2592b4` (2026-10-26), `README.md` [P-page]
- deepseek-ai/DeepSeek-V3.2-Exp `README.md` (main branch; no Anthropic or Claude Code mention) [P-page]

**Other**
- **COS:** CenterForOpenScience/llm-benchmarking `README.md` (main branch as of 2026-11-05), Acknowledgement section [P-page]. https://github.com/CenterForOpenScience/llm-benchmarking
- **AEA:** AEADataEditor/aeadataeditor.github.io @`519f186` (2026-10-22), `_guidance/preparing-replication-package.md` (dated 2025-12-04) and searched `_guidance`, `_posts`, `_pages` [P-page]. Published at https://aeadataeditor.github.io/ (not fetched).
- Project documents cross-referenced: `docs/research/evidence/R1-terminal-bench-science.md` (TBS sponsor credits), `docs/research/evidence/R4-replication-benchmarks.md` (Coefficient Giving mention), `docs/architecture/cost-and-effort-model.md` (central estimate of $17 per contribution; $3,404 for 200 contributions).
