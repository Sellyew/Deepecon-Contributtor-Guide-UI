# R2: Claude Code platform capabilities for Option B and for a shared interview protocol

| Field | Value |
|---|---|
| Topic | Claude Code (terminal CLI, Desktop app, IDE extensions, cloud sessions), Claude Cowork, and the Claude Agent SDK, as they bear on Option B (a contributor plugin run locally) and on running one interview protocol in both Option A and Option B. Covers skills, plugins and marketplaces, hooks, permissions and sandboxing, checkpointing and resume, model selection, language and output styles, surfaces, data handling, third-party providers and gateways, costs, and server-side use through the Agent SDK. Ends with a fact-check of the Claude Code claims marked [U] in the Option B design, in bilingual design §4, and in Option A §3.2. |
| Date | 2026-11-05 |
| Author | research agent |
| Scope | Read-only study of Anthropic's official documentation as served on 2026-11-05: about 90 Claude Code pages (Markdown renderings listed in `https://code.claude.com/docs/llms.txt`), 4 claude.com docs pages on Cowork and plugin platform support, 3 Claude Help Center articles on Cowork, and 2 Agent Skills pages on platform.claude.com. Version context: the Claude Code changelog's newest entry is v2.1.318, dated 2026-11-04; Claude Desktop v4.16336.0 (2026-11-03) bundles Claude Code 2.1.317 [P-page; CC-changelog, CCOM-desktop-changelog]. Nothing was installed, executed, or cloned. The draft design files were not edited. |
| Verification labels | **[P-full]** primary source, the whole page read · **[P-page]** primary official page, only the cited sections read · **[S]** secondary source · **[U]** unverified, or my inference |
| Status | Phase 1 (Discovery) evidence note. Sections marked "Implications" and §14 are assessment, not project decisions. |

**Citation shorthand.** `CC-<page>` is `https://code.claude.com/docs/en/<page>` (fetched as the `.md` rendering the docs index links to). `SDK-<page>` is `https://code.claude.com/docs/en/agent-sdk/<page>`. `CCOM-<page>` is `https://claude.com/docs/<page>`. `HC-<id>` is a support.claude.com article. `PLAT-<page>` is a platform.claude.com page. Section 17 gives every full URL; all were accessed on 2026-11-05.

**Product names in this note** follow the documentation as served today: "Google Cloud's Agent Platform, formerly Vertex AI" [P-page; CC-google-vertex-ai]; current models include Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable 5.1 [P-page; CC-model-config].

---

## Summary (10 bullets)

1. **Skills fit the interview protocol, with two portability limits.** A skill is a `SKILL.md` file plus optional supporting files. Its description is always in context. Its body loads when the skill is invoked and then stays in the conversation. After compaction, only the first 5,000 tokens of each invoked skill are re-attached, within a combined budget of 25,000 tokens. Claude Code accepts 20 frontmatter fields. claude.ai uploads and the Skills API accept only six (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`) and reject any other field with a hard error. Plugin skills are invoked as `/plugin-name:skill-name`. [P-full; CC-skills]
2. **Plugins and marketplaces are mature and scriptable.** The manifest is `.claude-plugin/plugin.json`; only `name` is required, and `version` keeps users on that version until it changes. A marketplace is a `.claude-plugin/marketplace.json` in a git repository, URL, or local path. Installation takes two steps, `/plugin marketplace add <owner>/<repo>[#ref]` then `/plugin install <plugin>@<marketplace-name>`, or one step from the shell: `claude plugin install <plugin> --marketplace <owner>/<repo>` (v2.1.292+). Third-party marketplaces do **not** auto-update by default. A repository can also carry the plugin itself under `.claude/skills/<name>/`, where it loads as `<name>@skills-dir` after workspace trust. [P-full; CC-plugins-install, CC-manifest. P-page; CC-plugin-loading]
3. **Plugins cannot ship permission rules.** A plugin's `settings.json` honours only `agent` and `subagentStatusLine`; every other key is dropped. A *workspace* `.claude/settings.json` can ship deny rules, sandbox configuration, `model`, `language`, `autoMemoryEnabled`, and `extraKnownMarketplaces` plus `enabledPlugins`. Option B therefore needs two layers: a plugin that carries the protocol and hooks, and a workspace template that carries the policy. [P-full; CC-components. P-page; CC-settings-ref, CC-permissions]
4. **Hooks provide real enforcement for Claude's own file tools; shell commands are only partly covered.** There are 33 hook events. A `PreToolUse` hook blocks a call with exit code 2 or with `permissionDecision: "deny"`, and that block holds even in `bypassPermissions` mode. Plugins ship hooks in `hooks/hooks.json`, and those hooks fire whenever the plugin is enabled.
   - **Edit/Write tools:** blocking edits under `original/` is robust, because these tools pass absolute paths.
   - **Shell commands:** blocking shell writes is best-effort only.
   - **OS-level enforcement:** this needs the Bash sandbox, which runs on macOS, Linux and WSL2 but not on native Windows. [P-page; CC-hooks, CC-hooks-guide, CC-sandboxing]
5. **Read-deny rules do not guarantee confidentiality.** They cover built-in file tools, `@`-mentions and the Bash file commands Claude Code recognizes. The docs say: "They don't apply to … arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself." The sandbox enforces paths at OS level only for shell commands, and only where the sandbox runs. Replication code that reads restricted data will still put its output in front of the model. [P-page; CC-permissions, CC-sandboxing]
6. **No plugin or skill can *require* a model.**
   - **Skill `model`:** lasts one turn only.
   - **Plugin options:** a plugin can make one of its agents (with its own `model`) the default main thread, and can ship a `PreModelSwitch` hook that blocks switches the user requests. Neither stops automatic safety fallback (e.g., Opus 5.5 → Opus 5 for biology-flagged requests), and the user's own settings override plugin defaults.
   - **Strict enforcement:** needs managed settings (`availableModels` + `enforceAvailableModels`, `deniedModels`), i.e. accounts provided by an organization or a gateway.
   - **Defaults:** the `default` model is Opus 5.5 on Pro, Max, Ultra, Team, Enterprise and the API (v2.1.280+), at default effort `medium`. [P-page; CC-model-config, CC-skills, CC-hooks, CC-components]
7. **Several defaults change how the interview behaves.**
   - **Auto mode** is the built-in starting permission mode for interactive terminal and VS Code sessions (v2.1.283+). It "nudges Claude to keep working without stopping for clarifying questions, though Claude still asks when your prompt or a skill explicitly relies on it."
   - **Auto memory** is on by default.
   - **Transcripts** are stored locally as plaintext JSONL for 30 days (Desktop and Cowork transcripts are exempt by default).
   - **Language:** a documented `language` setting exists. Claude Code passes its value "verbatim to Claude as an instruction to always respond in that language". It can go in any settings file, but not in a plugin. [P-page; CC-permission-modes, CC-memory, CC-sessions, CC-settings-ref. P-full; CC-data-usage]
8. **Surfaces: the no-terminal path for Option B is the Desktop app's Code tab, not Cowork.**
   - **CLI:** runs on macOS 13+, on Windows 10 1809+ natively (Git for Windows optional) or under WSL, and on Ubuntu 20.04+, Debian 10+ and Alpine 3.19+.
   - **Desktop Code tab:** "runs the same underlying engine". It installs plugins without a terminal in local and SSH sessions (not in WSL or cloud sessions) and requires a paid plan.
   - **Cowork:** loads plugin skills, agents and hooks. Since 2026-10-06 on Pro, Max and Ultra, it "Runs code and shell commands in an isolated environment on Anthropic's servers"; Team and Enterprise run it in the cloud or in a local isolated VM. Either way it cannot run a contributor's licensed Stata. [P-page; CC-setup, CC-desktop. P-full; HC-13345190, CCOM-platform-support]
9. **Data handling depends on the account terms.**
   - **What is sent:** prompts, file contents and command outputs held in context go to the provider with every request.
   - **Consumer plans (Free, Pro, Max, Ultra):** data trains models when the user's setting is on (5-year retention); otherwise retention is 30 days.
   - **Commercial terms (Team, Enterprise, API, cloud providers):** no training by default and 30-day retention; zero data retention (ZDR) is available to qualified Enterprise accounts.
   - **Telemetry:** excludes code and prompts, and can be turned off.
   - **Gateways:** supported, but Anthropic "doesn't support routing Claude Code to non-Claude models through any gateway". [P-full; CC-data-usage. P-page; CC-how-claude-code-works, CC-costs, CC-gateways]
10. **The Agent SDK can host the same plugin on a server.**
    - **What loads:** the plugin from a local path (`plugins: [{ type: "local", path }]`), plus skills, hooks, permissions and sessions.
    - **Runtime model:** each session is one `claude` subprocess with a working directory on disk.
    - **Hosting patterns:** the docs describe a container per task, and "hybrid" containers that resume from a `SessionStore`. A container per session is recommended for isolation, not required.
    - **Authentication:** third-party products must use API-key authentication, not claude.ai login.
    - **Costs:** official guidance is about $13 per developer per active day (enterprise average); `/cost` is an alias of `/usage`. [P-full; SDK-overview, SDK-plugins, SDK-hosting. P-page; CC-costs, CC-commands]

---

## 1. Skills

### 1.1 What the sources say

**Definition and standard.**
- A skill is a `SKILL.md` "with instructions"; "Claude uses skills when relevant, or you can invoke one directly with `/skill-name`." "Unlike CLAUDE.md content, a skill's body loads only when it's used." [P-full; CC-skills]
- "Claude Code skills follow the Agent Skills open standard, which works across multiple AI tools." Claude Code adds invocation control, subagent execution and dynamic context injection. [P-full; CC-skills]
- Custom commands (`.claude/commands/*.md`) are merged into skills and keep working; skills add supporting files and invocation control. [P-full; CC-skills]

**Frontmatter fields supported by Claude Code.** "All fields are optional. Only `description` is recommended." "Claude Code ignores a field it doesn't recognize without reporting an error." Boolean fields also accept `yes`/`no`/`on`/`off`/`1`/`0`. YAML that fails to parse loads the skill with no fields set. [P-full; CC-skills]

| Field | Documented behaviour (CC-skills, [P-full]) |
|---|---|
| `name` | Command name; defaults to the directory name. In a plugin it replaces the last segment of `/plugin:name` |
| `description` | When to use the skill. The listing truncates `description` + `when_to_use` at **1,536 characters** |
| `when_to_use` | Extra trigger text; counts toward the 1,536-character cap |
| `argument-hint`, `arguments` | Autocomplete hint; named positional arguments for `$name` substitution |
| `disable-model-invocation` | `true`: Claude cannot invoke the skill on its own, and the description is removed from context. If Claude tries anyway, Claude Code "blocks the call" |
| `user-invocable` | `false`: hidden from the `/` menu; only Claude can invoke it |
| `allowed-tools` | Pre-approves tools "during the turn that invokes this skill. The grant clears when you send your next message." Not gated by workspace trust |
| `disallowed-tools` | Removes tools while the skill is active; clears at the next message |
| `model` | "The override applies for the rest of the current turn and isn't saved to settings. The session model resumes when you send your next prompt." Ignored if excluded by `availableModels` |
| `effort` | `low`/`medium`/`high`/`xhigh`/`max` for the rest of the current turn; overridden by `CLAUDE_CODE_EFFORT_LEVEL` |
| `context: fork`, `agent`, `background` | Run the skill in a subagent that "doesn't see your conversation history"; runs in the background by default |
| `hooks` | Registered when the skill is invoked and kept "for the rest of the session" |
| `paths` | Glob patterns that limit automatic activation |
| `shell` | `bash` (default) or `powershell` for inline commands |
| `metadata`, `license`, `compatibility` | Accepted; Claude Code does not act on them (`compatibility` is a string of at most 500 characters) |

**Portability across surfaces.**
- Claude Code accepts every field above. "claude.ai skill uploads, the Skills API, and packaging with `package_skill.py`" accept only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`.
- Any other field causes a hard error: `Unexpected key(s) in SKILL.md frontmatter: argument-hint. Allowed properties are: allowed-tools, compatibility, description, license, metadata, name`. [P-full; CC-skills]
- Platform rules (API / claude.ai):
  - `name`: at most 64 characters, lowercase letters, digits and hyphens only, no XML tags, must not contain "anthropic" or "claude".
  - `description`: non-empty, at most 1,024 characters, no XML tags. [P-page; PLAT-skills-overview]
- "Claude Code-only body features, such as dynamic context injection, don't function in claude.ai chat or through the API." [P-full; CC-skills]

**Directory structure and progressive disclosure.**
- Claude Code's example layout is `SKILL.md` (required), `reference.md`, `examples.md`, and `scripts/helper.py` ("executed, not loaded"). Supporting files should be linked from `SKILL.md` so Claude knows when to read them. Claude Code does not mandate `references/` or `assets/` directory names. [P-full; CC-skills]
- Whether the open standard defines such directories is [U], because agentskills.io was unreachable (§16).
- The platform overview describes three levels:

  | Level | When loaded | Size |
  |---|---|---|
  | Metadata | Always | about 100 tokens per skill |
  | Instructions | When triggered | "Under 5k tokens" |
  | Resources | As needed | "None until accessed"; "Scripts run through bash, and only their output enters context" |

  [P-page; PLAT-skills-overview]

**Size guidance.**
- "Keep `SKILL.md` under 500 lines." [P-full; CC-skills]
- Best practices add: keep references "one level deep from `SKILL.md`"; give a table of contents to reference files longer than 100 lines; "Tested with Haiku, Sonnet, and Opus". [P-page; PLAT-skills-bp]
- The skill listing budget "scales at 1% of the model's context window" (configurable). [P-full; CC-skills]

**Lifecycle and compaction.** "the rendered `SKILL.md` content enters the conversation as a single message and stays there across later turns … Claude Code does not re-read the skill file on later turns." On auto-compaction, "Claude Code re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens." The troubleshooting advice: "put the most important instructions near the top of `SKILL.md`", and move rules that must always hold into hooks. [P-full; CC-skills]

**Invocation.**
- A skill name at the start of a message runs the skill. After plain text, "the name gives Claude permission to run the skill but doesn't run it".
- Plugin skills are named `/my-plugin:review`. "The bare `/fancy` also invokes the skill unless another command already uses that name."
- Permission rules `Skill(name)` and `Skill(name *)` allow or deny skills.
- Through the Agent SDK or `claude -p`, only the first of several stacked skills loads. [P-full; CC-skills]

**Locations and precedence.**
- Same-named skills resolve enterprise > personal (`~/.claude/skills/`) > project (`.claude/skills/`).
- Plugin skills are namespaced, so "Both load".
- Nested `.claude/skills/` directories load when Claude touches files there.
- `--add-dir` directories load their skills.
- Skills enabled on the claude.ai account sync into terminal sessions (v2.1.273+) and run as `/anthropic-skills:<name>` when the short name collides.
- "Cowork sessions and cloud sessions … don't read `~/.claude/skills/` on your machine". [P-full; CC-skills]

**Dynamic context injection.**
- `` !`command` `` runs before the skill is sent to the model. A failed command "aborts the entire skill invocation". Injected commands are checked against permission rules, and outside auto mode anything other than "allow" aborts the invocation.
- In a Cowork session "Claude Code replaces every `!` command line with the `disableSkillShellExecution` placeholder". Synced skills never run these commands on the user's machine. [P-full; CC-skills]

**Evaluation tooling.**
- `claude plugin eval` (v2.1.269+) runs each case "in a fresh, isolated non-interactive session with only your plugin loaded", by default also *without* the plugin, and scores the runs with graders, including LLM judges. A case can seed an "earlier conversation to continue" via `context.history_file`. [P-page; CC-plugin-evals]
- The skill-creator plugin runs a similar loop with its own `evals/evals.json` format. [P-full; CC-skills]

### 1.2 Implications (assessment)

- **Two-tier skill layout.** The protocol should load as a single entry skill (for example `contribute`, with `disable-model-invocation: true` so it never fires in unrelated sessions). Stage cards and probes should be supporting files read on demand. The stance and the invariant rules (one or two questions per turn, provenance, no invented errors, preserve originals) belong in the first part of `SKILL.md`, within the 5,000-token re-attach window. [U: design inference]
- **Portable core.** To reuse the same `SKILL.md` in Claude Code, on claude.ai/Cowork and through the Skills API, keep its frontmatter to the six spec fields and do not rely on `!` injection. Behaviour specific to Claude Code (hooks, model and effort hints, forks) goes in plugin components around the skill. [U: inference from CC-skills]
- **Protocol regression testing.** `claude plugin eval` with `history_file` fixtures can regression-test individual interview turns, such as "does the next turn ask exactly one focused question?". It is non-interactive, so a multi-turn simulated contributor needs an Agent SDK harness (§12). [U: inference]

---

## 2. Plugins, marketplaces, and distribution

### 2.1 What the sources say

**Manifest (`.claude-plugin/plugin.json`).**
- "The manifest is optional." "`name` is the only required key." [P-full; CC-manifest]
- `version` is "not checked against semver. Setting it pins the plugin to that version until you change it." [P-full; CC-manifest]
- Other fields: `displayName`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `metadata`, `defaultEnabled`, `dependencies`, `settings`, `userConfig`, `channels`, plus component paths (`skills`, `commands`, `agents`, `hooks`, `mcpServers`, `lspServers`, `outputStyles`, `workflows`) and `experimental.{themes,monitors,evals}`.
- Unknown top-level keys are stripped with a warning; `claude plugin validate` "is the authoritative check". [P-full; CC-manifest]
- Names: kebab-case, with no spaces, `@`, `:`, or path separators. Names starting with `claude-`, `anthropic-`, `anthropics-` or `cc-plugin-` are errors. [P-full; CC-manifest]

**Components and default layout.**
- Default locations: `skills/<name>/SKILL.md`, `commands/`, `agents/`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `output-styles/`, `themes/`, `monitors/monitors.json`, `workflows/`, `bin/` (put on the Bash tool's `PATH` while enabled), and `settings.json`. [P-full; CC-manifest, CC-components]
- "A `CLAUDE.md` at the plugin root isn't loaded as context." [P-full; CC-manifest]
- Plugin `settings.json`: "Only two keys take effect from a plugin, `agent` and `subagentStatusLine`; every other key is dropped." "plugin defaults are the lowest layer, so a user's own `agent` in `~/.claude/settings.json` overrides yours." [P-full; CC-components]
- Plugin agents' frontmatter fields `permissionMode`, `hooks`, `mcpServers` and `initialPrompt` are ignored. [P-full; CC-components]
- `userConfig` declares options (`string`/`number`/`boolean`/`directory`/`file`; `options` gives a picker, v2.1.271+). The values are substituted as `${user_config.KEY}` into skill and agent content, MCP/LSP configuration, and exec-form hook `args`. They are exported to hooks as `CLAUDE_PLUGIN_OPTION_<KEY>`. [P-full; CC-manifest]
- Path variables: `${CLAUDE_PLUGIN_ROOT}` changes with each version ("don't write state there"). `${CLAUDE_PLUGIN_DATA}` (`~/.claude/plugins/data/<id>/`) survives updates and is deleted on uninstall unless `--keep-data` is given. [P-full; CC-manifest]

**Component support by surface** [P-full; CCOM-platform-support]:

| Component | Chat | Cowork | Claude Code |
|---|---|---|---|
| Skills, commands | Loads (commands as skills) | Loads | Loads |
| Agents | Ignored | Loads | Loads |
| Hooks | Ignored | Loads | Loads |
| Local MCP server | Ignored | Loads only "when the Cowork session runs on your computer" | Loads |
| Top-level `bin/` | Plugin can't be installed | Plugin can't be installed | Loads |
| LSP servers, output styles, themes, `settings` | Ignored | Ignored | Loads |

**Marketplace (`.claude-plugin/marketplace.json`).**
- Required: `name`, `owner` (with `name`), and `plugins` (each entry needs `name` and `source`). Optional: `description`, `version`, `metadata.pluginRoot`, `forceRemoveDeletedPlugins`, `allowCrossMarketplaceDependenciesOn`, `renames`.
- Plugin source types: relative path, `github` (`repo`, `ref`, `sha`), `url` (git), `git-subdir`, `npm`, `archive` (zip over HTTPS with `sha256`, v2.1.224+), and `command`.
- Official and look-alike names are reserved, and so are names starting with `claudeai-`. [P-page; CC-marketplace-ref]

**Install, update, and uninstall commands (exact syntax).**

| Action | In a session | From the shell |
|---|---|---|
| Add marketplace | `/plugin marketplace add anthropics/claude-plugins-official`; pin with `/plugin marketplace add your-org/plugins#v1.2.0`; also accepts a git URL, a local path (start with `./`), or a hosted `marketplace.json` URL | `claude plugin marketplace add <source>` |
| Install | `/plugin install commit-commands@claude-plugins-official`; opens the details pane to choose a scope | `claude plugin install <plugin>@<marketplace> [--scope user\|project\|local] [--config KEY=VALUE]` |
| Add and install in one step | `/plugin install deploy-helper --marketplace your-org/plugins` (v2.1.275+) | `claude plugin install deploy-helper --marketplace your-org/plugins` (v2.1.292+) |
| Update | **Installed** tab → **Update now** | `claude plugin update <plugin>@<marketplace>` |
| Uninstall | `/plugin uninstall <plugin-name>@<marketplace-name>` | `claude plugin uninstall <plugin>@<marketplace> [--scope …] [--keep-data]` |
| Enable/disable | `/plugin` **Installed** tab | `claude plugin enable\|disable <plugin>@<marketplace>` |
| Apply changes | `/reload-plugins` (`--force` if it would invalidate the prompt cache) | Takes effect at next start |

Sources for the table: [P-full; CC-plugins-install. P-page; CC-plugin-cli. P-full; CC-skills]

- Scopes: user (`~/.claude/settings.json`), project (`.claude/settings.json`, committed), local (`.claude/settings.local.json`). "local … overrides the project setting, and the project setting overrides the user setting." [P-full; CC-plugins-install]
- The terminal, Desktop local sessions and VS Code "read the same settings files". [P-full; CC-plugins-install]

**Versioning and pinning.**
- The computed version comes from the manifest `version` first, then from the marketplace entry's `version`. Without either, it falls back to the commit SHA, the archive SHA-256, or `unknown`, depending on the source type.
- With `"version": "1.0.0"` set, users stay on the cached copy "however many commits they push".
- Ways to hold users on a version: `ref`/`sha` on entries, `#<ref>` on `marketplace add`, and two marketplaces as release channels. `claude plugin tag` creates `<name>--v<version>` tags.
- Old version directories are removed 14 days after an update. [P-page; CC-plugin-loading, CC-host-mkt, CC-plugin-cli]

**Auto-update.**
- On by default for Anthropic's official marketplaces (except `knowledge-work-plugins` and `first-party-plugins`); "Off by default: every other marketplace, including … third-party marketplaces".
- Toggled per marketplace in `/plugin` → **Marketplaces**, or with `"autoUpdate": true` on an `extraKnownMarketplaces` entry. `marketplace.json` has "no field to turn it on".
- The pass runs after the first message "a random delay of up to ten minutes" later. The running session keeps the old version; new versions load at the next launch or on `/reload-plugins`.
- `DISABLE_AUTOUPDATER`, `DISABLE_UPDATES` and `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` turn the pass off. [P-full; CC-plugins-install. P-page; CC-plugin-loading, CC-host-mkt, CC-settings-ref]

**Team distribution through repository settings.**
- A repository's `.claude/settings.json` can declare `extraKnownMarketplaces` and `enabledPlugins`.
- Marketplace entries are honoured "only after you accept the workspace trust dialog for that folder".
- "A plugin that the marketplace lists by a relative path loads from the marketplace copy once the repository's `extraKnownMarketplaces` entries apply". An external-source plugin instead shows "enabled in project settings but isn't installed" until the contributor runs `claude plugin install <name>@<marketplace> --scope project`.
- Cloud sessions do not install repository-declared plugins. [P-page; CC-plugins-org, CC-plugin-loading, CC-cloud-environments, CC-settings-ref]

**Distribution without a marketplace.**
- `claude --plugin-dir <dir|.zip>` or `--plugin-url <zip-url>` loads a plugin for one session.
- Moving the plugin folder under `~/.claude/skills/` makes it load at startup.
- A plugin under a repository's `.claude/skills/<name>/` (with `.claude-plugin/plugin.json`) loads as `<name>@skills-dir` "only after the same trust check" as project allow rules, and only from the session's primary working directory. Its MCP servers go through per-server approval, and its background monitors do not load. [P-page; CC-publish, CC-plugin-cli, CC-plugin-loading. P-full; CC-skills]

**Enterprise managed settings.**
- Delivered by one of:
  - server-managed settings (claude.ai admin console; Teams and Enterprise);
  - MDM (macOS plist, Windows registry);
  - a `managed-settings.json` file at `/Library/Application Support/ClaudeCode/` (macOS), `/etc/claude-code/` (Linux, WSL), or `C:\Program Files\ClaudeCode\` (Windows).
- Plugin controls:
  - Managed `extraKnownMarketplaces` + `enabledPlugins` force-install plugins; disabling them at user scope "doesn't stop it from loading".
  - `strictKnownMarketplaces` and `blockedMarketplaces` gate marketplace sources.
  - `allowManagedHooksOnly` blocks user, project, local and plugin hooks (except force-enabled plugins).
  - `disableSideloadFlags` rejects `--plugin-dir` and `--plugin-url`. [P-page; CC-plugins-org, CC-managed-settings, CC-hooks]

**Cowork and claude.ai side.**
- Plugins are added under **Customize > Plugins**, by GitHub marketplace URL or **Upload plugin** (zip).
- They are saved to the account and reach Claude Code "as a synced plugin" (`<name>@synced`) in terminal sessions.
- Limits: 200 MB and 5,000 files per plugin; 25 marketplaces per user. [P-full; CCOM-plugins, CCOM-cowork-plugins, CCOM-platform-support. P-page; CC-plugin-loading]

### 2.2 Implications (assessment)

- **Plugin vs. repository template.** Both routes are documented and can be combined. A plugin from a DeepEcon marketplace gives updates and namespacing. A **workspace template** (a repository or zip) can carry the plugin under `.claude/skills/deepecon-contributor/` **and** the policy file `.claude/settings.json`, which a plugin cannot provide. A frozen workspace snapshot also gives "sessions finish on the version they started with" (Option B §14) for free. [U: design inference]
- **Updates.** Updates will not reach contributors automatically unless they or the workspace settings turn `autoUpdate` on. A pre-flight version check (already proposed) is necessary, not optional. [U: inference]
- **Contributors without GitHub access.** For regions where GitHub is slow or unreachable, `archive` sources, `--plugin-dir <zip>`, and "unzip into `~/.claude/skills/`" are documented alternatives to a GitHub marketplace. [P-page; CC-marketplace-ref, CC-publish]
- **Cowork compatibility.** If the plugin should also be uploadable to claude.ai/Cowork, it must not have a top-level `bin/`, and it should not depend on output styles or plugin settings, which Cowork ignores. [P-full; CCOM-platform-support]

---

## 3. Hooks

### 3.1 What the sources say

**Events (33).**
- Per session: `SessionStart`, `Setup`, `SessionEnd`.
- Per turn: `UserPromptSubmit`, `UserPromptExpansion`, `Stop`, `StopFailure`, `MessageDisplay`.
- Tool calls: `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`.
- Agents and tasks: `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `TeammateIdle`.
- Context, configuration and files: `PreCompact`, `PostCompact`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`.
- Model switches: `PreModelSwitch`, `PostModelSwitch`.
- MCP and notifications: `Elicitation`, `ElicitationResult`, `Notification`. [P-page; CC-hooks]

**Handlers.** Five types: `command`, `http`, `mcp_tool`, `prompt`, and `agent` (experimental). Matching hooks run in parallel. The default timeout is 600 s for command hooks. [P-page; CC-hooks]

**Where hooks fire.** "Claude Code fires the same hook events wherever it runs: sessions in the terminal, IDE extensions, the Desktop app, and cloud sessions." [P-page; CC-hooks]

**How a `PreToolUse` hook blocks.**
- Exit code **2** blocks the call; stderr becomes the reason shown to Claude.
- Alternatively, exit 0 and print `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "…"}}`. Valid decisions are `allow`, `deny`, `ask` and `defer` (`defer` works only with `-p`). `updatedInput` can rewrite the tool's input.
- Precedence across hooks: "`deny` > `defer` > `ask` > `allow`".
- "Exit code 1 without valid JSON output is a non-blocking error … If your hook is meant to enforce a policy, use `exit 2`."
- A failing or timed-out hook lets the action through unless `"onFailure": "block"` (v2.1.295+) is set. [P-page; CC-hooks]

**Strength of the block.**
- "a hook that returns `permissionDecision: "deny"` blocks the tool even in `bypassPermissions` mode or with `--dangerously-skip-permissions`."
- A hook's "allow" "doesn't bypass deny rules from settings".
- Exception: with neither managed settings nor a Team/Enterprise login, an installed *mod* "can approve a call that … a `PreToolUse` hook blocked". [P-page; CC-hooks-guide, CC-permissions]

**Matching.**
- For `Write`/`Edit`/`Read`, "`tool_input.file_path` is always absolute", so "a hook that matches on paths can't be bypassed via `~` or a relative spelling". On Windows, paths arrive with backslashes.
- The `if` filter for Bash is best-effort: "use the permission system rather than a hook to enforce a hard allow or deny."
- On Windows without Git Bash, shell commands go to the PowerShell tool, so "A hook that matches only `Bash` never fires there"; exec form (`command` + `args`) is recommended. [P-page; CC-hooks]

**Blind spot.** "PreToolUse runs only when Claude calls a tool. By default, files you reference with `@` in your prompt are added without any tool call … no PreToolUse hook fires for them." A `Read` deny rule does block those paths. [P-page; CC-hooks]

**Plugins and skills.**
- Plugin hooks live in `hooks/hooks.json` (wrapped in a top-level `"hooks"` key) or in the manifest.
- "A plugin's hooks don't wait for one of the plugin's skills or commands to be used … they fire on their events from then on."
- Skill-frontmatter hooks register on invocation for the rest of the session; `once: true` removes a hook after its first success.
- An `ask` prompt shows the source as `[plugin:<name>]`. [P-full; CC-components. P-page; CC-hooks]

**Trust and disabling.**
- Interactive sessions hold back hooks "from every settings file … until you accept the workspace trust dialog"; `-p`/SDK sessions treat the folder as trusted.
- `disableAllHooks` (any scope, subject to precedence) turns hooks off.
- `allowManagedHooksOnly` restricts hooks to managed sources. [P-page; CC-hooks]

**Hooks useful to the protocol.**
- `SessionStart` with matcher `compact` re-injects context after compaction; its plain stdout is added to context.
- `PreCompact` can block compaction.
- `PreModelSwitch` (v2.1.251+) can block `/model`, picker, `/config` and SDK switches, but not "switches it makes on its own, such as an automatic model fallback".
- `PostModelSwitch` fires on every model change, including fallback and resume.
- `SessionEnd` has a 1.5-second default budget.
- `additionalContext` strings are capped at 10,000 characters. [P-page; CC-hooks, CC-hooks-guide]

**Security.** "Command hooks execute shell commands with your full user permissions." Hooks run outside the sandbox. [P-page; CC-hooks, CC-sandboxing]

### 3.2 Can `original/` be protected from edits and shell commands? (assessment)

| Path to modify `original/` | Mechanism | Strength | Platforms |
|---|---|---|---|
| Edit / Write / NotebookEdit tools | `Edit(/original/**)` deny rule in workspace `.claude/settings.json`, plus a plugin `PreToolUse` hook on `Edit\|Write\|NotebookEdit` | Strong: enforced by Claude Code, with absolute paths [P-page; CC-permissions, CC-hooks] | All |
| Recognized shell file commands (`sed -i`, `tee`, `>` redirect) | `Edit` deny rules also cover "file commands Claude Code recognizes in Bash … and … redirections" | Moderate [P-page; CC-permissions] | All |
| Other shell commands, scripts, Stata/R/Python writing files | Plugin hook parsing the command (best-effort); sandbox `filesystem.denyWrite` (OS-level, applies to child processes) | Weak without the sandbox; strong with it [P-page; CC-sandboxing] | Sandbox: macOS, Linux, WSL2 only |
| Hooks, MCP servers, monitors, the user's `!` commands | Not covered by the sandbox | None (they run with full user rights) [P-page; CC-sandboxing] | All |
| Anything | OS read-only attribute on `original/` + checksum manifest verified before export (Option B §6.1, layers 1 and 4) | Detection of change, not prevention | All |

**Conclusion [U: assessment].** The five-layer design in Option B §6.1 is sound, but layer 2 must move from the plugin to the workspace settings (§4). On native Windows, which has no sandbox, the guarantee rests on OS file permissions plus the integrity check. The Desktop app's WSL sessions do not load plugins (§8.2), so Windows contributors who use the Desktop app get the unsandboxed native path.

---

## 4. Permissions and sandboxing

### 4.1 What the sources say

**Rules.**
- Rule types are `allow`, `ask` and `deny`, evaluated "deny, then ask, then allow". "An allow rule can't carve an exception out of a deny rule."
- Deny from any scope beats allow from any scope; managed rules cannot be overridden.
- "Permission rules are enforced by Claude Code, not by the model." [P-page; CC-permissions]

**`Read` and `Edit` rules.**
- They use gitignore patterns: `//abs`, `~/home`, `/relative-to-settings-source`, `./relative-to-cwd`.
- "`Write(path)`, `NotebookEdit(path)`, and `Glob(path)` rules never match". Use `Edit(...)`.
- A `Read` deny also blocks Edit/Write on the same path. It covers `@`-mentions, pasted image paths, directory listings and IDE context.
- **Limit (verbatim):** "Read and Edit deny rules apply to Claude's built-in file tools, to file commands Claude Code recognizes in Bash, such as `cat`, `head`, `tail`, `sed`, and `tee`, and to the targets of Bash redirections such as `> file` and `< file`. They don't apply to a command that reads files without naming them, such as `grep -r pattern .` run from the directory that holds the file, or to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself. For OS-level enforcement that blocks all processes from accessing a path, enable the sandbox."
- A Bash deny rule "covers the invocation Claude usually produces and isn't a security boundary around the program" (e.g., `/usr/bin/curl` and `sh -c` forms are not matched). [P-page; CC-permissions]

**Protected paths.** Writes to `.git`, `.claude` (with exceptions), `.mcp.json`, shell rc files and similar "are never auto-approved, except in `bypassPermissions` mode". `permissions.allow` rules "do not pre-approve protected-path writes". [P-page; CC-permission-modes]

**Workspace trust.** "`permissions.allow` rules and `permissions.additionalDirectories` entries in a project's `.claude/settings.json` grant capability, so Claude Code applies them only after you accept the workspace trust dialog … `deny` and `ask` rules aren't affected, since they only restrict." [P-page; CC-permissions]

**Permission modes.**

| Mode | Behaviour |
|---|---|
| `default` (labelled Manual) | Prompts before edits and commands |
| `acceptEdits` | Auto-accepts edits and common filesystem commands |
| `plan` | Explore and propose; no edits |
| `auto` | A classifier reviews actions instead of prompts |
| `dontAsk` | Auto-denies anything that would prompt (CLI only) |
| `bypassPermissions` | No prompts; for containers and VMs only |

- **Built-in starting mode:** `auto` "In a terminal or through the VS Code extension … with Claude Code v2.1.283 or later"; `default` for `claude -p` and the Agent SDK.
- **Project settings files:** `defaultMode` set to `"auto"` or `"bypassPermissions"` in `.claude/settings.json` "doesn't take effect"; other values apply. `disableAutoMode: "disable"` (any file) removes auto mode.
- **Auto mode and questions:** "Auto mode also nudges Claude to keep working without stopping for clarifying questions, though Claude still asks when your prompt or a skill explicitly relies on it."
- **Desktop:** a mode picked in a local session "is remembered per folder and outranks a `defaultMode` in the project's `.claude/` settings". [P-page; CC-permission-modes, CC-settings-ref, CC-desktop]

**Bash sandbox.**
- Off by default; enabled with `/sandbox` or `sandbox.enabled`. Covers "Bash, PowerShell, and Monitor commands and the processes they start".
- Platforms: macOS (Seatbelt) and Linux/WSL2 (`bubblewrap` + `socat`). "On native Windows, Claude Code runs commands unsandboxed." WSL1 is not supported.
- Defaults: writes allowed to the working directory, a temp directory and added directories; reads to "Most of the machine, including credential files"; network "through a proxy on your machine that checks each host against your allowed domains, which start empty".
- Paths from `Read`/`Edit` deny rules "are merged into the final sandbox configuration".
- Escape hatch: Claude can retry a failed command with `dangerouslyDisableSandbox` (prompted in Manual mode). `allowUnsandboxedCommands: false` disables the retry; `failIfUnavailable: true` makes startup fail instead of running unsandboxed.
- Outside the sandbox: built-in file tools, hooks, local MCP servers, monitors, and the user's `!` commands.
- "Sandboxing reduces risk but is not a complete isolation boundary." [P-page; CC-sandboxing, CC-setup]

**Can a plugin ship permission settings?** No. Plugin `settings.json` keeps only `agent` and `subagentStatusLine` [P-full; CC-components]. All `permissions.*` and `sandbox.*` keys have scope "Any file", meaning user, project, local or managed [P-page; CC-settings-ref].

### 4.2 Implications for restricted data (assessment)

- A `Read(./restricted/**)` deny rule in the workspace settings keeps the restricted folder away from Claude's file tools, `@`-mentions and casual `cat`. It does **not** stop a script Claude writes and runs from printing the data, unless the sandbox is on and lists the path in `denyRead`.
- With the sandbox on, the replication run itself cannot read the data either. Code that must touch restricted data therefore has to run outside Claude's sandboxed shell, e.g. by the contributor or an RA, or through an excluded wrapper whose output is limited to aggregates.
- The honest disclosure is: "we reduce the chance that the model reads restricted files; any output of code that reads them, and anything the model reads, goes to the model provider." [U: assessment]

---

## 5. Checkpointing, rewind, and session resume

### 5.1 What the sources say

**Checkpoints.**
- "Every prompt you send that starts a turn creates a new checkpoint". Snapshots are kept for "the 100 most recent checkpoints in a session" and saved with the conversation, so `/rewind` works after resume. They are deleted in the retention sweep "about 30 days after the session last saved one".
- `/rewind` (aliases `/checkpoint`, `/undo`) or double-Esc offers: restore code and conversation, restore conversation only, restore code only, summarize from here, or summarize up to here. [P-full; CC-checkpointing, CC-commands]

**Documented limitations.**
- "A file that only Bash commands changed isn't tracked and stays as it is."
- Subagent edits are usually not restored (except a foreground forked skill).
- External changes and concurrent sessions are not tracked.
- Messages sent mid-turn get no checkpoint.
- Symlinked and hard-linked paths are skipped.
- "Checkpoints are designed for quick, session-level recovery … continue using version control". [P-full; CC-checkpointing]

**Resume.**
- Commands: `claude --continue`, `claude --resume [<name>|<id>|<transcript-path>]`, `/resume`.
- What is restored: the conversation (after compaction: the summary plus later messages), the model (with exceptions), the agent, and the permission mode for terminal resumes.
- Not restored: `--settings`, `--plugin-dir`, `--add-dir`, `--fallback-model` "pass them again". [P-page; CC-sessions]

**Transcripts.**
- Stored as JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`. "The entry format is internal to Claude Code and changes between versions."
- Retention: 30 days by default (`cleanupPeriodDays`). "Transcripts of sessions started or most recently continued in Claude Desktop or Cowork are exempt from that limit by default."
- `CLAUDE_CODE_SKIP_PROMPT_HISTORY=1` suppresses transcript writes. `claude purge` deletes local data. [P-page; CC-sessions. P-full; CC-data-usage]

**Auto memory.**
- On by default in local sessions.
- Stored at `~/.claude/projects/<project>/memory/`. The first 200 lines or 25 KB of `MEMORY.md` load into every session.
- Memory files are excluded from the retention sweep.
- Disable with `autoMemoryEnabled: false` (any settings scope) or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. [P-page; CC-memory]

### 5.2 Implications (assessment)

- **Record of truth.** Option B §5.2 is right to keep the record of truth in `.deepecon/`. An interview spread over several weeks can outlive the 30-day transcript and snapshot retention. Neither JSONL nor checkpoints are a stable interface.
- **Flawed variants in git.** `work/` should be a git repository. Flawed variants created by Stata/R/Python runs (Bash) are exactly the changes checkpoints do not track.
- **Auto memory and leakage.** The workspace settings should set `"autoMemoryEnabled": false`. This keeps hidden-tier facts (error labels, answer keys) from being written into cross-session memory (brief Safeguard F). [U: assessment]

---

## 6. Model selection and effort

### 6.1 What the sources say

**Aliases.** `default`, `best`, `fable`, `sonnet`, `opus`, `haiku`, `sonnet[1m]`, `opus[1m]`, `opusplan`. On the Anthropic API: `opus` → Opus 5.5, `sonnet` → Sonnet 5.5, `haiku` → Haiku 5.5. On Bedrock and Google Cloud's Agent Platform, `opus` → Opus 5.5 but `sonnet` → Sonnet 4.5. On Microsoft Foundry, `opus` → Opus 4.6. "To pin to a specific version, use the full model name, for example `claude-opus-5-5`". [P-page; CC-model-config]

**Selection order.**
1. `/model` during the session.
2. `claude --model`.
3. `ANTHROPIC_MODEL`.
4. The `model` setting.
5. `ANTHROPIC_DEFAULT_MODEL`.

Typing `/model <name>` "saves your choice as the default for new sessions". "The `model` setting is an initial selection, not enforcement." Project or managed `model` "reapplies on the next launch". [P-page; CC-model-config, CC-settings-ref]

**Plans.**
- `default` resolves to Opus 5.5 on "Pro, Max, Ultra, Team, Enterprise, and Anthropic API" (since v2.1.280; earlier, Sonnet 5 on Pro and Team Standard).
- Fable models are never the default and may bill to usage credits.
- Claude Code requires a Pro, Max, Ultra, Team or Enterprise subscription for the Desktop app. The documented CLI account types are those plans plus Console (API) accounts, cloud providers, and a cloud gateway; the Free plan is not listed [P-page; CC-desktop-qs, CC-auth; "Free not listed" is my reading, U].

**Restriction.**
- `availableModels` (any file) restricts named models, skill and subagent models included. `enforceAvailableModels` extends the restriction to the Default option; when managed settings exist, it is read only from them.
- `deniedModels` and `availableModelsMatch: "exact"` are managed-only.
- Enterprise admins can restrict models per role in the admin console. [P-page; CC-model-config, CC-settings-ref]

**Session-wide agent.**
- "Run the main thread as a named subagent, so Claude Code applies that subagent's system prompt, tool restrictions, and model to your session" (`agent` setting or `--agent`).
- "a custom subagent's system prompt replaces the default Claude Code system prompt entirely".
- A plugin's `settings.json` may set `agent`, at the lowest precedence. [P-page; CC-settings-ref, CC-sub-agents. P-full; CC-components]

**Automatic fallback.**
- For safety-classifier flags, Opus 5.5 biology-flagged requests "re-run on Opus 5" and cybersecurity-flagged requests on Opus 4.8. "After a fallback, the session continues on the fallback model."
- Availability fallback chains (`--fallback-model`, `fallbackModel`) last one turn.
- A fallback target excluded by `availableModels` "does not run". [P-page; CC-model-config]

**Effort.**
- Levels `low`/`medium`/`high`/`xhigh`/`max`. Opus 5.5 "defaults to `medium`".
- Resolution order: `CLAUDE_CODE_EFFORT_LEVEL` > in-session choice > `--effort` > settings (`modelSettings`, `effortLevel`) > the model default.
- A top-level `effortLevel` in project, local or managed settings "applies to every model".
- `maxEffortLevel` caps effort. Skill and subagent `effort` frontmatter overrides for that turn or that agent.
- `ultrathink` in a prompt requests deeper reasoning for one turn. [P-page; CC-model-config]

### 6.2 Can a skill or plugin pin or require a model? (synthesis)

| Lever | Who can set it | Scope | Overridable by the contributor? | Evidence |
|---|---|---|---|---|
| Skill `model` frontmatter | Plugin | Current turn only | Yes (next prompt resumes the session model) | [P-full; CC-skills] |
| `context: fork` + `model` | Plugin | The forked subagent, which does not see the conversation | n/a (unsuitable for a multi-turn interview) | [P-full; CC-skills] |
| Plugin `settings.json` → `agent` with `model:` in the agent file | Plugin | Whole session, wherever the plugin is enabled | Yes (user `agent` setting or `--agent`); whether `/model` overrides it mid-session is undocumented [U] | [P-full; CC-components. P-page; CC-sub-agents] |
| Plugin `PreModelSwitch` hook (exit 2) | Plugin | Blocks user- and SDK-requested switches | Yes (`disableAllHooks`, editing settings); does not block automatic fallback | [P-page; CC-hooks] |
| Workspace `.claude/settings.json`: `model`, `availableModels`, `enforceAvailableModels`, `effortLevel` | Workspace template | New sessions in that folder | Yes; when no managed list exists, user-settings `availableModels` entries are concatenated | [P-page; CC-model-config, CC-settings-ref] |
| Managed settings (server-managed for Team/Enterprise, MDM, file) | Organization admin | Enforced | No | [P-page; CC-model-config] |
| Claude apps gateway per-group `availableModels` | Gateway operator | Enforced on sessions signed in to the gateway | No | [P-page; CC-gateways] |

**Recording the model actually used.**
- `SessionStart` hook input may carry `model` ("It can be omitted").
- `PostModelSwitch` input carries `from_model` and `to_model`, with `source` values including `auto` and `resume`.
- The status line JSON has `model.id` and `version`.
- "There is no `$CLAUDE_MODEL` environment variable." [P-page; CC-hooks, CC-statusline]

### 6.3 Implications (assessment)

- **Steer, do not enforce.** Option B can steer the model reliably but cannot guarantee it. A realistic package:
  - workspace `model: "claude-opus-5-5"` plus a fixed `effortLevel`;
  - a plugin `PreModelSwitch` hook that asks the contributor to confirm, rather than refuses;
  - `SessionStart` and `PostModelSwitch` hooks that write the model, effort and Claude Code version into `.deepecon/`;
  - a package field that flags any deviation.
- **Model homogeneity.** If identical models are a hard scientific requirement, they require project-provided accounts under managed settings (for example a claude.ai Team organization with server-managed settings) or a project-run gateway. That moves inference cost back to the project (open question O-006). [U: assessment]
- **Do not use the plugin `agent` setting at user scope.** It would take over every Claude Code session the contributor runs, including unrelated ones. Use it only inside the DeepEcon workspace (project or local scope), if at all. [U: inference from CC-components]

---

## 7. Language and output styles

### 7.1 What the sources say

**`language` setting** (verbatim): "Have Claude respond in a language other than English by default. There is no fixed list for responses: Claude Code passes the value verbatim to Claude as an instruction to always respond in that language … Claude Code doesn't check the value". It also sets the voice-dictation language and the language of generated session titles. Scope: any settings file. Example: `"language": "japanese"`. [P-page; CC-settings-ref]

**Output styles.**
- Built-in styles: Default, Proactive, Concise, Explanatory, Learning. Custom styles are Markdown files with `name`, `description` and `keep-coding-instructions`.
- On the full system prompt, custom styles "leave out Claude Code's section of built-in software engineering instructions" unless `keep-coding-instructions: true`.
- Plugins can ship styles (`output-styles/`, named `<plugin>:<name>`). `force-for-plugin: true` applies a style "automatically whenever the plugin is enabled … Overrides the user's `outputStyle` setting."
- The style is chosen with `/output-style` or the `outputStyle` setting (case-sensitive).
- "It doesn't guarantee that something always happens".
- Styles apply to the main conversation and forks, not to other subagents. [P-full; CC-output-styles]
- Chat and Cowork ignore plugin output styles. [P-full; CCOM-platform-support]

**Localized documentation.** The Claude Code documentation has a Simplified Chinese edition (`https://code.claude.com/docs/zh-CN/…`; the index lists 228 pages). Whether it is complete and current relative to English is [U]. [P-page; CC-zh-index]

### 7.2 Implications (assessment)

- **Language control.** The bilingual design's approach (one English protocol, language chosen at S0, stored in state) remains the primary control and works on every surface. The `language` key can back it up in the workspace settings. But its "always respond in that language" wording may conflict with steps that must produce English artifacts, such as English working translations and agent-facing tasks; this needs a pilot test.
- **Interviewer persona.** A plugin output style could carry the interviewer stance, possibly with `force-for-plugin` in the workspace only. It is ignored on Cowork and chat, so the protocol must not depend on it. [U: assessment]
- **Chinese onboarding.** The official Chinese docs can serve the Chinese-language installation guide, with links checked at release time. [U]

---

## 8. Surfaces

### 8.1 Terminal CLI

**System requirements.** macOS 13.0+; Windows 10 1809+ or Windows Server 2019+; Ubuntu 20.04+; Debian 10+; Alpine Linux 3.19+. 4 GB+ RAM, x64 or ARM64. Internet connection required. "Location: Anthropic supported countries". [P-page; CC-setup]

**Windows options.**

| Option | Requires | Sandboxing |
|---|---|---|
| Native | None; Git for Windows optional | Not supported |
| WSL 2 | WSL 2 enabled | Supported |
| WSL 1 | WSL 1 enabled | Not supported |

- On native Windows without Git for Windows, Claude Code runs shell commands through the PowerShell tool. [P-page; CC-setup]

**Installation and updates.**
- Native installer: `curl -fsSL https://claude.ai/install.sh | bash` (macOS, Linux, WSL) or `irm https://claude.ai/install.ps1 | iex` (PowerShell). Homebrew, WinGet, apt, dnf and apk are also available.
- Native installs auto-update; `autoUpdatesChannel: "stable"` and `minimumVersion` are available. [P-page; CC-setup]

### 8.2 Desktop app (Code tab)

- **Same engine:** "Desktop runs the same underlying engine with a graphical interface." Desktop and the CLI "read the same configuration files", and "Hooks and skills defined in settings apply to both". [P-page; CC-desktop]
- **Platforms:** macOS (universal), Windows x64 and ARM64, Linux (beta, apt/.deb for Ubuntu and Debian). "The desktop app includes Claude Code, so you don't need to install Node.js or the CLI". [P-page; CC-desktop, CC-desktop-qs]
- **Plugins:** "You can install plugins from the desktop app without using the terminal" via **+ → Add plugins**, in local and SSH sessions. "The plugin browser is not available in cloud sessions … Plugins aren't available in WSL sessions." [P-page; CC-desktop]
- **Adding a third-party marketplace from the Desktop UI is not documented** in the pages read [U]. The two documented routes (repository settings after trust; a repository-embedded `@skills-dir` plugin) need no typed commands.
- **Permission modes:** Manual, Accept edits, Plan and Auto in a selector; `dontAsk` is CLI-only.
- **Commands with an interactive terminal panel:** commands with no argument form "such as `/permissions`, reply with `isn't available in this environment`"; edit settings files instead.
- **Integrated terminal and editing:** an integrated terminal is available, and file attachments include PDFs.
- **Moving sessions between surfaces:** `/desktop` or `claude --desktop` moves a CLI session into Desktop.
- **Third-party providers:** only "via Claude Desktop on 3P". [P-page; CC-desktop]

### 8.3 IDE extensions

- **VS Code:** has a **Manage plugins** dialog (`/plugins`) with scopes and `userConfig` forms. The VS Code extension never reads a project's `.claude/settings.json` "for the starting permission mode".
- **JetBrains:** "runs Claude Code in the IDE's terminal". [P-full; CC-plugins-install. P-page; CC-permission-modes, CC-components]

### 8.4 Web and cloud sessions (claude.ai/code)

- Cloud sessions run on Anthropic-managed VMs.
- They load the repository's committed `CLAUDE.md`, `.claude/skills`, hooks and permission rules.
- They do not install plugins declared in `.claude/settings.json`, and they do not load the user's `~/.claude/skills`. [P-page; CC-cloud-environments]

### 8.5 Claude Cowork

- **Availability:** "Claude Cowork is available on paid plans (Pro, Max, Ultra, Team, and Enterprise)". Claude Desktop for macOS, Windows and Linux (beta) on all paid plans; web and mobile with plan conditions. (Help article last updated 2026-10-30.) [P-full; HC-13345190]
- **Where code runs:** "Cowork runs your tasks in the cloud … Runs code and shell commands in an isolated environment on Anthropic's servers." "On October 6, 2026, new Cowork tasks on Pro, Max, and Ultra plans run in the cloud … you can't switch back." "When a task needs a file in the cloud, Claude fetches a copy of just that file." "For new tasks that run only on your computer, use Claude Code in the desktop app." [P-full; HC-13345190. P-page; HC-15520349]
- **Team and Enterprise:** "Sessions in the cloud" or "Local sessions: Claude's work runs on the user's computer, with code in an isolated virtual machine." Cloud is on by default for Team and off by default for Enterprise. (Updated 2026-11-02.) [P-page; HC-13455879]
- **Plugins in Cowork:**
  - Skills, commands, agents and hooks load.
  - Local MCP servers load only when the session runs on the computer.
  - Plugins with a top-level `bin/` cannot be installed.
  - `${user_config.*}` values are not prompted for.
  - Output styles and settings are ignored.
  - Cowork "doesn't read the Claude Code CLI's `~/.claude` directory". [P-full; CCOM-platform-support, CCOM-cowork]
- **Shell commands and deny rules:** in Desktop Cowork sessions, shell commands go through `mcp__workspace__bash`. Claude Code applies whole-tool `Bash` deny rules to it, but "never applies a `Bash` allow rule". [P-page; CC-permissions]
- **Permissions:** Cowork has its own Manual, Auto and Skip modes. [P-full; HC-13345190]
- **Policy delivery:** server-managed settings are not delivered to Cowork sessions in the Desktop app. [P-page; CC-server-managed]

### 8.6 Remote Control

- A local session can be steered from claude.ai/code or the mobile app while "code execution and filesystem access stay on your machine".
- While a session is connected, its transcript is also stored on Anthropic servers.
- Requirements: Pro, Max, Ultra, Team or Enterprise sign-in. Not available with API keys, gateways, Bedrock, Vertex or Foundry, or with `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. [P-page; CC-remote-control, CC-data-usage]

### 8.7 Can a non-technical economist run the plugin without a terminal? (assessment)

- **Yes, through the Desktop Code tab.** Install the app, sign in with a paid plan, open the DeepEcon workspace folder, and accept the trust dialog. The workspace settings then register and enable the plugin, or the plugin is embedded as `@skills-dir`. After that, `/deepecon-contributor:contribute` or the slash menu starts the interview. The documentation supports every step except a pure-UI way to add a *third-party marketplace* [U].
- **Remaining friction for non-technical users:**
  - Unpacking or cloning a workspace.
  - Installing Stata, R or Python, and possibly Python for the helper scripts (§11).
  - Windows users get no sandbox.
  - Auto mode is the default unless the workspace sets otherwise.
- **Cowork is not a full Option B surface.** It cannot run the contributor's own software, and it copies files to the cloud. It could host an *interview-only* mode, e.g. the economist converses while an RA performs S5 in Claude Code, but with Cowork's data flows and without the workspace policy layer. [U: assessment]

---

## 9. Data handling

### 9.1 What the sources say

- **What is sent.** "To interact with the LLM, Claude Code sends data over the network. This data includes all user prompts and model outputs, encrypted in transit via TLS 1.2+." "Claude's context window holds your conversation history, file contents, command outputs, CLAUDE.md, auto memory, loaded skills, and system instructions." "Claude Code sends your full conversation with every request, and each time Claude uses tools it sends another request carrying that batch of tool results." [P-full; CC-data-usage. P-page; CC-how-claude-code-works, CC-costs]
- **Training.**
  - Consumer (Free, Pro, Max, Ultra): "We will train new models using data from Free, Pro, Max, and Ultra accounts when this setting is on (including when you use Claude Code from these accounts)."
  - Commercial (Team, Enterprise, API, third-party platforms, Claude Gov): "Anthropic does not train generative models using code or prompts sent to Claude Code under commercial terms, unless the customer has chosen to provide their data". [P-full; CC-data-usage]
- **Retention.**
  - Consumer: 5 years if training is allowed, 30 days otherwise.
  - Commercial: 30 days standard; ZDR "available to qualified accounts for Claude Code on Claude for Enterprise".
  - Feedback reports (`/feedback`, `/bug`, `/share`): kept 5 years.
  - Session-survey transcript sharing: up to 6 months, only after an explicit **Yes**. [P-full; CC-data-usage]
- **Local storage.**
  - Transcripts: "Claude Code clients store session transcripts locally in plaintext under `~/.claude/projects/` for 30 days by default". Desktop and Cowork transcripts are exempt by default. [P-full; CC-data-usage]
  - Credentials: macOS Keychain; a mode-`0600` file on Linux. [P-full; CC-security]
- **Telemetry.**
  - Metrics "never include your code, prompts, or file paths" (opt out with `DISABLE_TELEMETRY=1`).
  - Error reports, for Pro/Max/Ultra sign-ins, are redacted (opt out with `DISABLE_ERROR_REPORTING=1`).
  - `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` disables all non-essential traffic. It also disables auto-updates and feature flags, and with them claude.ai skill sync and Remote Control.
  - Telemetry, error reporting and `/feedback` are off by default on Bedrock, Agent Platform, Foundry and Claude Platform on AWS. Session surveys and the WebFetch domain check (hostname only) still run. [P-full; CC-data-usage. P-page; CC-env-vars]
- **Encryption at rest by provider.**
  - Anthropic API: AES-256.
  - Bedrock: AWS KMS customer-managed keys available.
  - Google: CMEK available.
  - Foundry "Hosted on Azure": prompts stay in Azure. [P-full; CC-data-usage]

### 9.2 Implications (assessment)

- The contamination risk in Option B §10 is real by construction. A contributor on a consumer plan with the training setting on sends hidden-tier material (flawed variants, consequence labels) under terms that allow training.
- Mitigations, in order of strength:
  1. Project-provided commercial access: Team seats, Console API keys, or a gateway.
  2. A documented check, recorded in the package, that the training setting is off.
  3. `/feedback` disabled via `DISABLE_FEEDBACK_COMMAND=1` in the workspace `env`, plus auto memory off.
- Whether the workspace can safely set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` needs a trade-off decision: it also disables plugin auto-update, synced skills and Remote Control. [U: assessment]

---

## 10. Third-party providers and gateways

### 10.1 What the sources say

**Providers.**

| Provider | Switch | Other variables |
|---|---|---|
| Amazon Bedrock | `CLAUDE_CODE_USE_BEDROCK=1` | `AWS_REGION` |
| Google Cloud's Agent Platform (formerly Vertex AI) | `CLAUDE_CODE_USE_VERTEX=1` | `CLOUD_ML_REGION`, `ANTHROPIC_VERTEX_PROJECT_ID` |
| Microsoft Foundry | `CLAUDE_CODE_USE_FOUNDRY` | `ANTHROPIC_FOUNDRY_API_KEY`, or Entra ID |
| Claude Platform on AWS | `CLAUDE_CODE_USE_ANTHROPIC_AWS=1` | — |

- Pin models with `ANTHROPIC_DEFAULT_OPUS_MODEL` and the related variables. [P-page; CC-amazon-bedrock, CC-google-vertex-ai, CC-microsoft-foundry, CC-claude-platform-on-aws, CC-3p]
- Commercial terms apply to these providers (§9). Regions follow each cloud's regions. The Anthropic plans' availability follows "Supported countries". [P-page; CC-3p]

**Gateways.**
- Gateways are configured with `ANTHROPIC_BASE_URL` (or the provider-specific base-URL variables).
- Anthropic ships its own "Claude apps gateway" in the `claude` binary: IdP sign-in, per-group `availableModels` and managed settings, per-user spend limits, OTLP metrics.
- Other gateways also work, but "Anthropic doesn't endorse, maintain, or audit third-party gateway products, and doesn't support routing Claude Code to non-Claude models through any gateway."
- "When developers connect through a gateway with a gateway credential, usage is billed to your organization's provider account at API rates, and their claude.ai subscriptions aren't used or charged." [P-page; CC-gateways, CC-llm-gateway]

**Non-Anthropic models.** Not officially supported (quotation above). The Agent Skills format is described as an open standard "which works across multiple AI tools"; which tools, and how faithfully, was not verifiable here [U]. [P-page; CC-llm-gateway. P-full; CC-skills]

### 10.2 Implications (assessment)

- The "point Claude Code at another provider's compatible endpoint" fallback in Option B §5.3 is outside Anthropic's support. Treat it as rejected for the protocol-validated path.
- The documented route to data control and uniform terms is:
  - **project-provided access:** Console API keys, or a Claude apps gateway in front of the API, Bedrock, Agent Platform or Foundry;
  - **project-defined limits:** per-contributor credentials and spend limits.
- That route also delivers managed model restrictions, which Option B otherwise lacks (§6.2). [U]

---

## 11. Costs and usage limits

### 11.1 What the sources say

- **Official guidance:** "Across enterprise deployments, the average cost is around $13 per developer per active day and $150-250 per developer per month, with costs remaining below $30 per active day for 90% of users." [P-page; CC-costs]
- **Commands:** `/usage` shows session cost, plan limits and a usage breakdown; "`/cost` and `/stats` are aliases". The dollar figure is computed locally at list price and is "an estimate". For subscribers, "the session cost figure isn't relevant for billing purposes". [P-page; CC-costs, CC-commands]
- **Subscription limits:**
  - Team and Enterprise: "each member's Claude Code usage draws from a per-seat allowance that resets on a rolling five-hour window and a weekly window. The allowance is shared with Claude chat and Cowork". Usage credits allow continuing past it.
  - Pro, Max and Ultra: plan usage limits and usage credits apply. Exact quotas are not in the pages read (R3). [P-page; CC-costs]
- **API and Console:**
  - Workspace spend limits.
  - Rate-limit recommendations: for example, "100-500 users: 15k-20k" tokens per minute (TPM) per user.
  - `--max-budget-usd` (print mode only). [P-page; CC-costs, CC-cli-ref]
- **Prompt cache:** Claude Code uses a one-hour TTL for the main conversation only "on a Claude subscription within your plan's included usage". With API keys, cloud providers or usage credits it is five minutes, unless `promptCacheTtl: "1h"` is set. [P-page; CC-prompt-caching]
- **Agent SDK hosting:** "A minimally provisioned container runs roughly $0.05 per hour, while a single long agent session can spend dollars in tokens." [P-full; SDK-hosting]

### 11.2 Implications (assessment)

- **Cost model check.** The $6–46 per contribution in the cost model (API list prices) is plausible against Anthropic's $13 per active-developer-day average. Interviews are lighter on tool output than coding but longer in wall-clock time.
- **Cache TTL.** Human response gaps longer than five minutes make the cache TTL matter. If the project pays per token, the workspace should set `promptCacheTtl: "1h"`, which would need re-costing in the cost model.
- **Subscription limits.** On subscriptions, the five-hour windows can interrupt a 2–3 hour interview session. The pilot should measure this. [U: assessment]

---

## 12. Claude Agent SDK for a hosted Option A

### 12.1 What the sources say

- **What it is:** a library "that runs the Claude Code binary, with Claude Code's capabilities, such as built-in tools, permissions, sessions, and hooks". Skills, commands and memory "Load automatically from your project's `.claude/` and from `~/.claude/`"; plugins load "by local path". [P-full; SDK-overview]
- **Loading plugins:** `plugins: [{ type: "local", path: "./my-plugin" }]`; "The `type` field must be `"local"`". Marketplace plugins must be downloaded first. Plugin skills are invoked by sending `/plugin-name:skill-name` as the prompt. [P-full; SDK-plugins]
- **Settings sources:** when `settingSources` is omitted, the SDK reads the same filesystem settings as the CLI; `settingSources: []` isolates it. Managed policy and `~/.claude.json` are read regardless. [P-page; SDK-features]
- **Runtime:** "The Agent SDK spawns and supervises a `claude` CLI subprocess that owns a shell, a working directory, and session files on disk … One agent session maps to one subprocess."
  - Local state is lost on container restart unless a `SessionStore` adapter mirrors transcripts.
  - Documented patterns: ephemeral (a container per task), long-running, **hybrid** ("Ephemeral containers that hydrate from a `SessionStore` on startup … Best for sessions that span many interactions but sit idle between them"), and multi-agent container.
  - Starting resources: 1 GiB RAM, 5 GiB disk and 1 CPU per agent.
  - Multi-tenant isolation inside one container is documented: per-tenant `cwd` and `CLAUDE_CONFIG_DIR`, `settingSources: []`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, and per-tenant egress rules.
  - Known limits: no top-level session timeout (use `maxTurns`), and memory grows over long sessions. [P-full; SDK-hosting]
- **User input:** "Claude requests user input in two situations: when it needs permission to use a tool … and when it has clarifying questions (via the `AskUserQuestion` tool). Both trigger your `canUseTool` callback". For long waits, a `PreToolUse` hook can return `defer` so the process can exit and resume later. [P-page; SDK-user-input]
- **Authentication and terms:** "Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK." Use is governed by the Commercial Terms of Service. [P-full; SDK-overview]
- **Alternative:** Managed Agents is "A hosted agent harness that runs the agent loop, with sessions in an Anthropic-managed cloud sandbox or a self-hosted sandbox". Its pricing and beta status were not checked here. [P-full; SDK-overview]

### 12.2 Implications (assessment)

- **Feasibility.** Running the Option B plugin unchanged inside Option A is documented and feasible. "Unchanged" needs three qualifications:
  1. The web app must implement the interaction surface: chat streaming, `canUseTool` for `AskUserQuestion`, and permission prompts if any tool needs one.
  2. Each active interview needs a process with a filesystem holding the paper and code, i.e. a container or an isolated directory. The hybrid pattern lets idle interviews release compute.
  3. Interviews run on the project's API key under commercial terms, which is what Option A wants anyway.
- **Execution split.** For A1 (no hosted execution), `allowedTools`/`disallowedTools` can withhold Bash, so the shared plugin's S5 stage must degrade to "generate a run kit". A2 would enable Bash inside the sandboxed container.
- **One protocol, two hosts.** Both hosts can share one skill directory and stage-card set. Only the transport and the S5 execution adapter differ. This is the strongest technical argument for a shared protocol. [U: assessment]

---

## 13. Fact-check table

### 13.1 Claims marked [U] that concern Claude Code

| # | Location | Claim (short quote) | Verdict | Correct fact | Citation |
|---|---|---|---|---|---|
| 1 | option-b §2.1 step 4 | "`/plugin marketplace add <org>/deepecon-contributor` then `/plugin install deepecon-contributor@<org>` [U: exact syntax per R2]; or, in the desktop app, the equivalent UI" | **Corrected** (in part) | `/plugin marketplace add <owner>/<repo>` (optionally `#<ref>`), then `/plugin install <plugin>@<marketplace-name>`, where the marketplace name is the `name` field of `marketplace.json`, not the GitHub org. One-step forms: `/plugin install <plugin> --marketplace <owner>/<repo>` (v2.1.275+) and `claude plugin install <plugin> --marketplace <owner>/<repo>` (v2.1.292+). Desktop: **+ → Add plugins** lists plugins "from your marketplaces"; adding a third-party marketplace from the Desktop UI is not documented [U]. Typing-free alternatives: workspace `extraKnownMarketplaces` + `enabledPlugins` (after trust), or an embedded `@skills-dir` plugin | [P-full; CC-plugins-install#add-a-marketplace](https://code.claude.com/docs/en/plugins/install); [P-page; CC-plugins-org#require-plugins-per-repository](https://code.claude.com/docs/en/plugins/org) |
| 2 | option-b §3.2 row 1 | "Claude Code in a terminal (macOS, Linux, Windows) … [U: OS support details per R2]" | **Confirmed, with qualification** | macOS 13.0+, Windows 10 1809+ / Server 2019+, Ubuntu 20.04+, Debian 10+, Alpine 3.19+; 4 GB RAM; x64/ARM64. Windows runs natively (Git for Windows optional, otherwise PowerShell) or in WSL. Not full capability everywhere: no sandbox on native Windows or WSL1. Availability limited to "Anthropic supported countries" | [P-page; CC-setup#system-requirements](https://code.claude.com/docs/en/setup); [P-page; CC-sandboxing](https://code.claude.com/docs/en/sandboxing) |
| 3 | option-b §3.2 row 2 | "Claude Code in the desktop app … plugins and skills supported [U: verify parity of plugins, hooks, and permission prompts]" | **Confirmed, with exceptions** | Same engine and settings; hooks fire in Desktop; plugins via UI in local and SSH sessions only (not WSL, not cloud). Permission modes Manual, Accept edits, Plan, Auto (no `dontAsk`); `/permissions` unavailable, so edit settings files. Mode chosen per folder outranks project `defaultMode`. Paid plan required | [P-page; CC-desktop](https://code.claude.com/docs/en/desktop); [P-page; CC-hooks](https://code.claude.com/docs/en/hooks) |
| 4 | option-b §3.2 row 3 | Cowork "Potentially the most accessible … if they support plugins, local files, and code execution [U]" | **Corrected** | Plugins: skills, commands, agents and hooks load; `bin/` plugins refused; output styles and settings ignored. Local files: reachable through the Desktop app. Code execution: "in an isolated environment on Anthropic's servers" (Pro/Max/Ultra since 2026-10-06), or a local isolated VM for Team/Enterprise local sessions. It cannot run the contributor's installed Stata, and it fetches file copies to the cloud. Paid plans only | [P-full; HC-13345190](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork); [P-page; HC-15520349](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile); [P-full; CCOM-platform-support](https://claude.com/docs/plugins/platform-support) |
| 5 | option-b §3.2 row 4 | "Other agent tools that read the open Agent Skills format … [U]" | **Still unverifiable** | Anthropic states the format is an open standard "which works across multiple AI tools". Only six frontmatter fields are portable. The standard's site (agentskills.io) was unreachable; other tools are for R3 | [P-full; CC-skills](https://code.claude.com/docs/en/skills) |
| 6 | option-b §5.1 tree | "`.claude-plugin/plugin.json` # name, version, description [U: format per R2]" | **Confirmed** | The manifest is optional; only `name` is required (kebab-case; `claude-` and other prefixes reserved); `version` pins users until changed; other plugin folders sit at the plugin root, not inside `.claude-plugin/` | [P-full; CC-manifest](https://code.claude.com/docs/en/plugins/manifest-reference) |
| 7 | option-b §5.1 tree | "`hooks/` # protect originals; record session metadata [U]" | **Confirmed, with limits** | `hooks/hooks.json` with a top-level `"hooks"` key; active whenever the plugin is enabled. `PreToolUse` can deny; `SessionStart`/`PostModelSwitch`/`SessionEnd` can log. Hooks run with full user rights, outside the sandbox. On Windows without Git Bash, use exec form | [P-full; CC-components#hooks](https://code.claude.com/docs/en/plugins/components); [P-page; CC-hooks](https://code.claude.com/docs/en/hooks) |
| 8 | option-b §5.1 | "Progressive disclosure keeps the model's context small … stage cards … are read when a stage begins [U: progressive-disclosure behaviour per R2]" | **Confirmed, with caveat** | Descriptions are always in context. The body loads on invocation and stays (not re-read). Supporting files load only when read, then stay in history. After compaction only the first 5,000 tokens per skill are re-attached (25,000 combined). Keep `SKILL.md` under 500 lines | [P-full; CC-skills#skill-content-lifecycle](https://code.claude.com/docs/en/skills); [P-page; PLAT-skills-overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) |
| 9 | option-b §5.2 | "Claude Code's own session history and checkpoints are a convenience, not the record of truth [U: checkpoint semantics per R2]" | **Confirmed** | Checkpoints track Claude's file-tool edits per prompt (last 100). They miss Bash-only changes, most subagent edits, external edits and symlinks. Snapshots and transcripts expire after about 30 days by default. "Not a replacement for version control". The transcript format is internal | [P-full; CC-checkpointing](https://code.claude.com/docs/en/checkpointing); [P-page; CC-sessions](https://code.claude.com/docs/en/sessions) |
| 10 | option-b §5.3 | "Whether a plugin or skill can *require* a model is pending R2 [U]" | **Corrected** (answer: no) | Skill `model` lasts one turn. Plugin `agent` default and `PreModelSwitch` hook steer but are overridable and do not stop automatic fallback. Enforcement needs managed settings (`availableModels` + `enforceAvailableModels`, `deniedModels`) or a gateway | [P-full; CC-skills](https://code.claude.com/docs/en/skills); [P-page; CC-model-config#restrict-model-selection](https://code.claude.com/docs/en/model-config); [P-page; CC-hooks#premodelswitch](https://code.claude.com/docs/en/hooks) |
| 11 | option-b §5.3 | "the package records the model actually used, as reported by the client or a session hook [U]" | **Confirmed in part** | `SessionStart` input may include `model` ("can be omitted"). `PostModelSwitch` reports every change, including `auto` fallback and `resume`. The status line JSON has `model.id` and `version`. No `$CLAUDE_MODEL` variable. Single-turn fallback-chain substitutions do not fire `PostModelSwitch` | [P-page; CC-hooks](https://code.claude.com/docs/en/hooks); [P-page; CC-statusline](https://code.claude.com/docs/en/statusline); [P-page; CC-model-config#fallback-model-chains](https://code.claude.com/docs/en/model-config) |
| 12 | option-b §5.3 | "point Claude Code at another provider's compatible endpoint [U: per R3]" | **Corrected** | Anthropic "doesn't support routing Claude Code to non-Claude models through any gateway". Supported: Anthropic API, Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, Microsoft Foundry (Claude models) | [P-page; CC-llm-gateway](https://code.claude.com/docs/en/llm-gateway); [P-page; CC-gateways](https://code.claude.com/docs/en/gateways) |
| 13 | option-b §6.1 item 2 | "Plugin-provided settings deny edits and writes under `original/` [U: whether plugins can ship such settings, per R2]" | **Corrected** | Plugins cannot: plugin `settings.json` keeps only `agent` and `subagentStatusLine`. Put `Edit(/original/**)` (not `Write(...)`, which never matches) in the workspace `.claude/settings.json`, where deny rules apply even before trust, or in managed settings | [P-full; CC-components#default-settings](https://code.claude.com/docs/en/plugins/components); [P-page; CC-permissions](https://code.claude.com/docs/en/permissions) |
| 14 | option-b §6.1 item 3 | "A pre-tool-use hook blocks any edit, write, or shell command that targets `original/` [U: hook mechanics per R2]" | **Confirmed for file tools; corrected for shell commands** | Edit/Write/NotebookEdit: robust (absolute `file_path`). Bash/PowerShell: best-effort (the hook sees only the command string, not what scripts write). Use exit 2 and `onFailure: "block"`, match `Bash\|PowerShell`, and add sandbox `denyWrite` where available | [P-page; CC-hooks#pretooluse](https://code.claude.com/docs/en/hooks); [P-page; CC-sandboxing](https://code.claude.com/docs/en/sandboxing) |
| 15 | option-b §6.3 | "The plugin then denies the model read access to them [U: read-deny rule support, per R2]" | **Corrected** | Read deny rules exist but must be set in a settings file, not by a plugin. They cover built-in tools, `@`-mentions, IDE context, recognized Bash commands and redirections, but "don't apply to … arbitrary subprocesses". OS-level coverage only with the sandbox (not native Windows). Outputs of code that reads the data still reach the model | [P-page; CC-permissions#read-and-edit](https://code.claude.com/docs/en/permissions) |
| 16 | option-b §10 row 2 | "[U: training and retention terms per R3]" | **Confirmed** (Claude Code docs; legal terms are for R3) | Consumer (Free/Pro/Max/Ultra): training when the setting is on (5-year retention), otherwise 30 days. Commercial: no training unless opted in; 30 days; ZDR for qualified Enterprise. Local transcripts: plaintext, 30 days | [P-full; CC-data-usage](https://code.claude.com/docs/en/data-usage) |
| 17 | option-b §10 last row | "Telemetry from the client … Possibly … Client settings [U: per R2]" | **Confirmed, with detail** | Metrics exclude code, prompts and paths (`DISABLE_TELEMETRY`); error reports for Pro/Max/Ultra (`DISABLE_ERROR_REPORTING`); `/feedback` uploads the transcript (`DISABLE_FEEDBACK_COMMAND`); `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` disables all of these. Off by default on cloud providers, except surveys and the WebFetch hostname check | [P-full; CC-data-usage#telemetry-services](https://code.claude.com/docs/en/data-usage) |
| 18 | option-b §11 | "Python runtime … [U: whether Claude Code already provides a usable runtime]" | **Still unverifiable; nothing documented** | The docs mention bundled ripgrep and a bundled Claude Code binary (Desktop, SDK); none mentions Python. Plugin Node dependencies install with the user's own npm or Bun from `PATH`; Python dependencies must be installed by a hook into `${CLAUDE_PLUGIN_DATA}`. Treat Python as a prerequisite | [P-page; CC-setup](https://code.claude.com/docs/en/setup); [P-page; CC-plugin-loading#node-js-package-dependencies](https://code.claude.com/docs/en/plugins/loading) |
| 19 | option-b §12 | "On a subscription the marginal cost is zero, but plan limits may bind [U]" | **Confirmed qualitatively** | Usage counts against plan limits. Team/Enterprise: a per-seat allowance with rolling five-hour and weekly windows, shared with chat and Cowork; usage credits beyond that. Exact Pro/Max/Ultra quotas are not documented in the pages read (R3). A gateway credential replaces the subscription and is billed per token | [P-page; CC-costs](https://code.claude.com/docs/en/costs); [P-page; CC-gateways](https://code.claude.com/docs/en/gateways) |
| 20 | option-b §14 | "Updates: through the marketplace [U: auto-update behaviour per R2]" | **Corrected/qualified** | Off by default for third-party marketplaces. Turned on by the user (`/plugin` → Marketplaces) or by `"autoUpdate": true` on an `extraKnownMarketplaces` entry. Applies after the first message plus up to 10 minutes; new versions load at the next session or on `/reload-plugins`. A `version` pin blocks commit tracking | [P-full; CC-plugins-install#keep-plugins-updated](https://code.claude.com/docs/en/plugins/install); [P-page; CC-plugin-loading#when-auto-update-runs](https://code.claude.com/docs/en/plugins/loading) |
| 21 | option-b §16 | "Hidden material enters model training through consumer accounts … Low–Medium [U: per R3]" | **Mechanism confirmed; likelihood still unverifiable** | Consumer data is used for training when the setting is on; the `/feedback` and survey paths upload transcripts only on explicit action. No documented base rate | [P-full; CC-data-usage](https://code.claude.com/docs/en/data-usage) |
| 22 | bilingual §4 Option B | "Whether Claude Code offers a documented response-language setting that the plugin can rely on is pending R2 [U]" | **Confirmed it exists; a plugin cannot set it** | `language` (any settings file): "passes the value verbatim to Claude as an instruction to always respond in that language"; not validated; also sets dictation language and session titles. Plugin settings cannot carry it; workspace or user settings can | [P-page; CC-settings-ref#language](https://code.claude.com/docs/en/settings-reference); [P-full; CC-components](https://code.claude.com/docs/en/plugins/components) |
| 23 | option-a §3.2 (Orchestration row) | "Claude Agent SDK running the **same skill** as Option B on the server, each session in an isolated container [U: feasibility per R2]" | **Confirmed feasible, with requirements** | Plugins load via `plugins: [{type:"local", path}]`; skills, hooks and permissions work. One `claude` subprocess with a working directory per session; `SessionStore` for resumption; `canUseTool` for questions and approvals; API-key auth only. A container per session is a documented pattern, not a requirement (shared-container multi-tenancy is also documented) | [P-full; SDK-plugins](https://code.claude.com/docs/en/agent-sdk/plugins); [P-full; SDK-hosting](https://code.claude.com/docs/en/agent-sdk/hosting); [P-full; SDK-overview](https://code.claude.com/docs/en/agent-sdk/overview) |
| 24 | option-a §3.2 (last paragraph) | "…the *same* plugin as Option B inside per-session containers … at the price of operating containers even for A1 [U: per R2]" | **Confirmed in substance** | The SDK needs a process with a filesystem per session even when contributor code never runs. Idle cost can be reduced with the documented "hybrid" pattern. Bash can be withheld for A1 via allowed and disallowed tools | [P-full; SDK-hosting](https://code.claude.com/docs/en/agent-sdk/hosting) |

Out of R2 scope (not Claude Code): bilingual §4 Option A [U] items (`next-intl`, self-hosted CJK fonts) → R9. Option B §2.1, §13 and §16 timing, effort and likelihood estimates → pilot or cost model. Plan prices → R3.

### 13.2 Spot checks of related claims not marked [U]

| Location | Claim | Verdict | Note and citation |
|---|---|---|---|
| option-b §6.2 | "The contributor approves commands through the client's permission prompts, or pre-approves the wrappers only." | **Needs qualification** | Interactive terminal and VS Code sessions start in **auto mode** (classifier, no routine prompts) on v2.1.283+. Desktop remembers a mode per folder. A workspace can set `defaultMode: "default"` or `disableAutoMode`. A skill's `allowed-tools` grant lasts one turn; persistent pre-approval needs project allow rules, which require trust. [P-page; CC-permission-modes, CC-skills] |
| option-b §2.1 step 6 | "`/deepecon-contributor:contribute`" | **Confirmed** | Plugin skills run as `/<plugin>:<skill>`; the bare `/contribute` also works when no other command uses it. [P-full; CC-skills] |
| option-b §2.1 step 3 | "Terminal installer or desktop app" | **Confirmed** | "The desktop app includes Claude Code, so you don't need to install Node.js or the CLI". [P-page; CC-desktop-qs] |
| option-b §15 | "International reach depends on model availability in each contributor's region" | **Consistent** | CLI requirement: "Location: Anthropic supported countries"; the list itself is for R3. [P-page; CC-setup] |

---

## 14. Implications for DeepEcon (assessment)

All points in this section are my assessment [U], built on the sourced facts above.

1. **Package Option B as plugin + workspace, not plugin alone.**
   - The **plugin** carries what Claude Code lets plugins carry: protocol skill and stage cards, hooks, helper scripts, an optional output style, and `userConfig`.
   - The **workspace template** carries what only settings files can carry:
     - `Edit`/`Read` deny rules for `original/` and restricted folders;
     - sandbox configuration;
     - `model` and `effortLevel`;
     - `language`;
     - `autoMemoryEnabled: false`;
     - `disableAutoMode` or `defaultMode` as decided;
     - `extraKnownMarketplaces` + `enabledPlugins`, or the plugin embedded as `@skills-dir`.
   - This should update Option B §5.1 and §6.1. It also answers the brief's "standalone skill, plugin, or repository template" question: the template carries policy, the plugin carries the protocol.
2. **Model consistency is "recommended and recorded", not "required".**
   - The design must accept heterogeneity, or buy enforcement with project-provided org accounts (server-managed settings) or a gateway.
   - In either case, record model, effort and Claude Code version per session via hooks. Run the simulated-contributor protocol evaluations for every model on the supported list.
3. **Interview behaviour under default auto mode must be tested, not assumed.**
   - Auto mode nudges Claude not to stop for questions unless a skill relies on asking. The skill must state that asking is the task.
   - The workspace could start in Manual mode for S5, at the cost of more prompts for non-technical users. This trade-off belongs in the pilot (PQ items).
4. **Long sessions need protocol state outside the conversation.**
   - Keep invariant rules in the first 5,000 tokens of `SKILL.md`.
   - Re-inject the current stage and pending question with a `SessionStart` (`compact`) hook, or on each turn with `UserPromptSubmit`.
   - Treat `.deepecon/` as the record of truth. Claude Code transcripts and checkpoints are conveniences that expire after 30 days.
5. **Protecting originals:**
   - **Strong** on macOS, Linux and WSL2 (deny rules + hook + sandbox `denyWrite` + OS read-only + checksum).
   - **Weaker** on native Windows (no sandbox), which is also what Windows users get in the Desktop app, since its WSL sessions have no plugins.
   - The integrity check before export is the backstop that makes the guarantee auditable on all platforms.
6. **Restricted data cannot be fully protected by Claude Code configuration.**
   - The honest design keeps restricted microdata out of the workspace the model operates in.
   - Data-touching runs go through wrappers that emit aggregates, or are done by the contributor or an RA outside the session.
   - The S0 disclosure should say plainly what deny rules do and do not cover.
7. **The non-technical path is the Desktop Code tab; Cowork is not a substitute.**
   - Cowork runs code in Anthropic's cloud on consumer plans and in a VM elsewhere, so it cannot use the contributor's Stata, and its data flow resembles a hosted service.
   - An "economist in Cowork or chat for the interview, RA in Claude Code for S5" split is technically possible because skills load on both surfaces. It changes the privacy analysis, however, and should be evaluated as a hybrid, not as Option B.
8. **Project-provided commercial access is the single lever that fixes several Option B weaknesses together:**
   - uniform no-training terms;
   - enforceable model allowlists;
   - spend limits;
   - one support configuration.
   - It turns Option B's "cost shifted to contributors" into project cost, which strengthens the cost-model finding that inference cost is not a decisive differentiator.
9. **A shared protocol across Options A and B is technically well supported.**
   - Keep `SKILL.md` frontmatter to the six Agent Skills spec fields and avoid `!` injection. The same skill then loads in Claude Code (Option B), in an Agent SDK container (Option A), and in claude.ai/Cowork (hybrids).
   - Confine host-specific behaviour (hooks, execution adapters, UI) to thin layers.
10. **Distribution and support:**
    - Plugin auto-update is off for our marketplace by default, so the pre-flight version check is mandatory.
    - GitHub-independent routes (archive or zip, `~/.claude/skills/`, claude.ai upload without `bin/`) exist for contributors who cannot reach GitHub.
    - Claude Code releases several times a week: v2.1.300 on 2026-10-14, v2.1.318 on 2026-11-04 [P-page; CC-changelog]. Many behaviours above are gated by version. The support matrix should name a minimum Claude Code version and a regression run per release.
11. **Windows and runtime prerequisites.**
    - Hooks should be exec-form programs that match `Bash|PowerShell`.
    - Claude Code ships no Python. Either require Python 3 (and say so in the checklist) or ship the helper as platform binaries; a `bin/` folder is fine for Claude Code but blocks claude.ai/Cowork installation.

---

## 15. Open questions

1. **Desktop app and third-party marketplaces.** Can a contributor add a third-party marketplace from the Desktop UI? Does the Desktop Code tab load plugins synced from claude.ai (documented for terminal sessions only)? Do Desktop local sessions show the workspace trust dialog and apply a project's `extraKnownMarketplaces`? (Test in the pilot.)
2. **`/model` vs. a plugin `agent`.** Does `/model` override the model of a session-wide `agent` set by plugin `settings.json`? Is the plugin `settings.json` honoured for synced plugins? (Undocumented.)
3. **Cowork local sessions.** In Team/Enterprise local VM sessions, do plugin `PreToolUse` hooks run inside the VM, and can they match Cowork's `mcp__workspace__bash` tool?
4. **Usage limits.** What are the current Pro/Max/Ultra usage limits for a 2–3 hour, document-heavy interview? (R3; measure in the pilot.)
5. **Regional availability.** What do "Anthropic supported countries" and provider availability mean for mainland-China contributors? (R3.)
6. **`language` vs. English artifacts.** Does the `language` setting's "always respond" instruction interfere with English working translations and English agent-facing artifacts? (Pilot test with zh-Hans.)
7. **Agent Skills standard.** Does the open standard define optional `scripts/`, `references/`, `assets/` directories, and which non-Anthropic tools implement which fields? (agentskills.io unreachable; R3.)
8. **Stata under the sandbox.** Do Stata licence checks, temp files and network access work inside the macOS and Linux sandbox? This needs a hands-on test before relying on the sandbox for S5.
9. **Documentation inconsistencies to watch.**
   - The platform Agent Skills overview says "Custom Skills do not sync across surfaces" and that claude.ai skills "cannot be centrally managed by admins". Claude Code docs describe claude.ai skill sync into terminal sessions (v2.1.273+), and claude.com docs describe organization-provided plugins.
   - The plugin-hosting page says a user or an admin turns auto-update on. The settings reference allows `autoUpdate` on `extraKnownMarketplaces` in any settings file, so whether a repository file can turn it on needs a test. [P-page; PLAT-skills-overview, CC-skills, CC-host-mkt, CC-settings-ref]

---

## 16. Access problems

- **agentskills.io** (Agent Skills open standard): `curl` returned `CONNECT tunnel failed, response 403` from the session proxy for `https://agentskills.io/specification.md` and `https://agentskills.io/llms.txt`. This was recorded as a blocked host, not a DNS failure. No retry or proxy workaround was attempted. Claims about the standard rest only on Anthropic's own pages.
- **Not needed and not attempted:** arxiv.org, github.com and docs.github.com, which are known to be unreachable. No clones were made.
- **Reachable and used:** code.claude.com (docs index and `.md` pages), claude.com/docs, support.claude.com (HTML, text extracted locally), platform.claude.com.
- **WebSearch** was used once, only to find the Cowork help article ([S]; eweek.com and other results were not relied on).
- **Help Center articles:** these are dynamic HTML. Their text was extracted with a local script; "last updated" dates come from the page metadata (13345190: 2026-10-30; 15520349: 2026-10-30; 13455879: 2026-11-02).

---

## 17. Sources

All accessed 2026-11-05. Code pages were fetched as `<URL>.md`, as listed in the docs index.

**Claude Code documentation (code.claude.com)**
- CC-llms (index): https://code.claude.com/docs/llms.txt [P-full]; Simplified Chinese index CC-zh-index: https://code.claude.com/docs/_llms/zh-cn.txt [P-page]
- CC-skills: https://code.claude.com/docs/en/skills [P-full]
- CC-plugins-overview: https://code.claude.com/docs/en/plugins/overview [P-full]
- CC-plugins-install: https://code.claude.com/docs/en/plugins/install [P-full]
- CC-manifest: https://code.claude.com/docs/en/plugins/manifest-reference [P-full]
- CC-components: https://code.claude.com/docs/en/plugins/components [P-full]
- CC-marketplace-ref: https://code.claude.com/docs/en/plugins/marketplace-reference [P-page]
- CC-plugin-cli: https://code.claude.com/docs/en/plugins/cli-reference [P-page]
- CC-plugin-loading: https://code.claude.com/docs/en/plugins/loading [P-page]
- CC-plugins-org: https://code.claude.com/docs/en/plugins/org [P-page]
- CC-publish: https://code.claude.com/docs/en/plugins/publish [P-page]
- CC-host-mkt: https://code.claude.com/docs/en/plugins/host-marketplace [P-page]
- CC-plugin-evals: https://code.claude.com/docs/en/plugin-evals [P-page]
- CC-hooks: https://code.claude.com/docs/en/hooks [P-page]
- CC-hooks-guide: https://code.claude.com/docs/en/hooks-guide [P-page]
- CC-permissions: https://code.claude.com/docs/en/permissions [P-page]
- CC-permission-modes: https://code.claude.com/docs/en/permission-modes [P-page]
- CC-sandboxing: https://code.claude.com/docs/en/sandboxing [P-page]
- CC-settings-ref: https://code.claude.com/docs/en/settings-reference [P-page]
- CC-checkpointing: https://code.claude.com/docs/en/checkpointing [P-full]
- CC-sessions: https://code.claude.com/docs/en/sessions [P-page]
- CC-memory: https://code.claude.com/docs/en/memory [P-page]
- CC-model-config: https://code.claude.com/docs/en/model-config [P-page]
- CC-sub-agents: https://code.claude.com/docs/en/sub-agents [P-page]
- CC-output-styles: https://code.claude.com/docs/en/output-styles [P-full]
- CC-costs: https://code.claude.com/docs/en/costs [P-page]
- CC-commands: https://code.claude.com/docs/en/commands [P-page]
- CC-cli-ref: https://code.claude.com/docs/en/cli-reference [P-page]
- CC-env-vars: https://code.claude.com/docs/en/env-vars [P-page]
- CC-tools-ref: https://code.claude.com/docs/en/tools-reference [P-page]
- CC-data-usage: https://code.claude.com/docs/en/data-usage [P-full]
- CC-security: https://code.claude.com/docs/en/security [P-full]
- CC-desktop: https://code.claude.com/docs/en/desktop [P-page]
- CC-desktop-qs: https://code.claude.com/docs/en/desktop-quickstart [P-page]
- CC-setup: https://code.claude.com/docs/en/setup [P-page]
- CC-auth: https://code.claude.com/docs/en/authentication [P-page]
- CC-feature-availability: https://code.claude.com/docs/en/feature-availability [P-page]
- CC-cloud-environments: https://code.claude.com/docs/en/cloud-environments [P-page]
- CC-remote-control: https://code.claude.com/docs/en/remote-control [P-page]
- CC-3p: https://code.claude.com/docs/en/third-party-integrations [P-page]
- CC-amazon-bedrock: https://code.claude.com/docs/en/amazon-bedrock [P-page]
- CC-google-vertex-ai: https://code.claude.com/docs/en/google-vertex-ai [P-page]
- CC-microsoft-foundry: https://code.claude.com/docs/en/microsoft-foundry [P-page]
- CC-claude-platform-on-aws: https://code.claude.com/docs/en/claude-platform-on-aws [P-page]
- CC-gateways: https://code.claude.com/docs/en/gateways [P-page]
- CC-llm-gateway: https://code.claude.com/docs/en/llm-gateway [P-page]
- CC-managed-settings: https://code.claude.com/docs/en/managed-settings [P-page]
- CC-server-managed: https://code.claude.com/docs/en/server-managed-settings [P-page]
- CC-prompt-caching: https://code.claude.com/docs/en/prompt-caching [P-page]
- CC-how-claude-code-works: https://code.claude.com/docs/en/how-claude-code-works [P-page]
- CC-statusline: https://code.claude.com/docs/en/statusline [P-page]
- CC-changelog: https://code.claude.com/docs/en/changelog [P-page]

**Claude Agent SDK documentation**
- SDK-overview: https://code.claude.com/docs/en/agent-sdk/overview [P-full]
- SDK-plugins: https://code.claude.com/docs/en/agent-sdk/plugins [P-full]
- SDK-hosting: https://code.claude.com/docs/en/agent-sdk/hosting [P-full]
- SDK-features: https://code.claude.com/docs/en/agent-sdk/claude-code-features [P-page]
- SDK-user-input: https://code.claude.com/docs/en/agent-sdk/user-input [P-page]

**claude.com documentation**
- CCOM-cowork: https://claude.com/docs/cowork/overview [P-full]
- CCOM-platform-support: https://claude.com/docs/plugins/platform-support [P-full]
- CCOM-cowork-plugins: https://claude.com/docs/cowork/guide/plugins [P-full]
- CCOM-plugins: https://claude.com/docs/plugins/overview [P-full]
- CCOM-desktop-changelog: https://claude.com/docs/cowork/changelog [P-page]

**Claude Help Center**
- HC-13345190: https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork (updated 2026-10-30) [P-full]
- HC-15520349: https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile (updated 2026-10-30) [P-page]
- HC-13455879: https://support.claude.com/en/articles/13455879-use-claude-cowork-on-team-and-enterprise-plans (updated 2026-11-02) [P-page]

**Claude platform (Agent Skills)**
- PLAT-skills-overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview [P-page]
- PLAT-skills-bp: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices [P-page]

**Secondary (pointer only)**
- WebSearch, 2026-11-05, query "Claude Cowork availability plans macOS Windows …": results included eWeek ("Anthropic Opens Claude Cowork to All Paid Plans on macOS, Windows") and several blogs [S]. Used only to locate HC-13345190; no claim here rests on them.
