# Submission and Contribution Management

> **Superseded on 2026-11-06.** The research lead revised the MVP ([revised requirements](../requirements/2026-11-06-research-lead-revision.md)): no AI interview, no Claude Code-based system, and no project data sent to any external AI service by default. The current proposal is the [MVP contributor interface](mvp-contributor-interface.md). This document is kept as a record and is no longer the basis for the design. Submission requirements will be redesigned from the example contribution package (D-023).

| | |
|---|---|
| **Status** | **Proposed** v0.1.0 (2026-11-05). Not yet reviewed by the research lead. |
| **Scope** | Brief §8: how contributors hand over completed work, evaluated **independently of the two interface architectures** (D-015). |
| **Evidence labels** | GitHub limits verified from GitHub's documentation source repository ([R9](../research/evidence/R9-hosted-stack-and-compliance.md)) [P-page]. E-mail and file-request limits and reachability from mainland China remain [U]. Package sizes from the AEA Data Editor ([R8](../research/evidence/R8-replication-standards-and-econometric-pitfalls.md)) [P-full]. |

---

## 1. Separate three layers

Discussions of "submission" usually mix three different things. Separating them is what allows the contributor-facing channel to stay simple while the package stays standardized (brief §8).

| Layer | Question it answers | Recommendation in brief |
|---|---|---|
| **Package** | *What* is handed over? | One standardized, schema-valid package (manifest, tier directories, checksums), identical whatever the channel ([schema](../../schemas/README.md)) |
| **Transport** | *How* does it reach us? | Simple, private, browser-based upload as the default; Git for technical contributors who want it |
| **Internal review store** | *Where* does it live while shepherds and reviewers work on it? | A private Git repository with automated checks, plus object storage for large files |

Neither architecture implies a transport. Option B can produce a ZIP that goes through an upload link; Option A can push straight into the internal store without keeping a submission database of its own.

## 2. Requirements

From the brief: contributor convenience; access and permission management; confidential materials; file size and data licensing; automated validation; reviewer workflows; version history; auditability; future benchmark publication. Added by this analysis:

- **Leakage control.** Packages contain hidden-tier material (flawed variants, answer keys). Any channel that can make them public, or expose them to web crawlers, is unsuitable unless the release policy makes everything public (Open question O-001).
- **Reachability for contributors in mainland China.** Several common services are blocked or unreliable there [U — needs verification with contributors on the ground].
- **Withdrawal.** Contributors can withdraw (D-008), so the store must support deletion with an audit trail.
- **Size.** The median AEA replication package is 40.4 MB, but about 20% exceed 2 GB and 5% exceed 20 GB [P-full, R8]. Packages carry data only when they are redistributable, but the channel must still handle large code and output bundles.
- **Integrity.** Checksums are verified on receipt.

## 3. Options

### 3.1 E-mail

- **For:** universally familiar; no new account.
- **Against:** attachment limits around 20–25 MB on common providers [U], below the median package size; no access control after sending; copies persist in several mailboxes; weak audit trail; automated validation only through brittle mailbox parsing; easily forwarded — a leakage risk for hidden material.
- **Assessment:** acceptable only as a fallback for small packages, ideally as an encrypted archive with the passphrase sent separately.

### 3.2 GitHub pull request to a dedicated repository

- **Public repository:** excellent automation (continuous-integration checks on every pull request), review tooling, version history, and audit — this is how Terminal-Bench-Science works. But a public repository exposes hidden material to the world and to training-data crawlers. It is compatible with DeepEcon only if the benchmark itself is fully public and canary-marked (O-001).
- **Private repository:** keeps the automation and history, but every contributor needs a GitHub account, an invitation, and working knowledge of Git. That is a barrier for many senior economists. GitHub blocks files above 100 MiB; Git LFS allows 2, 4, or 5 GB per file depending on the plan [P-page, R9].
- **Assessment:** ideal as the **internal review store**, operated by staff. Optional transport for technically fluent contributors.

### 3.3 Hosted upload

- **What:** a minimal web page issuing per-contributor, time-limited upload links (presigned URLs to encrypted object storage), or the upload step of the Option A platform.
- **For:** browser-only; large files via multipart upload; encryption at rest; access logs; validation on arrival (schema, checksums, leakage scan) with immediate feedback.
- **Against:** something must be built and operated — about one to two engineer-weeks for a standalone minimal version [U: planning estimate], or nearly free inside Option A. Reachability from mainland China depends on hosting and CDN choices [U].
- **Assessment:** strongest default transport for most contributors.

### 3.4 Institutional or commercial file-request services

- **What:** "request files" features of services such as Box, OneDrive, Dropbox, or Google Drive.
- **For:** no engineering; uploaders often need no account [U]; universities frequently have enterprise agreements with data-protection terms.
- **Against:** limited automated validation (webhooks or APIs at best); vendor-specific retention and access semantics; several such services are blocked in mainland China [U].
- **Assessment:** a good zero-engineering option for the **pilot**, when the lead's institution has an approved service.

### 3.5 Hybrid

A simple default path for everyone (upload link) and a technical path (private Git) for contributors who prefer it, both feeding the same internal review store.

## 4. Comparison

Ratings are qualitative judgments for DeepEcon's situation, not measurements.

| Criterion | E-mail | Public GitHub PR | Private GitHub PR | Hosted upload | File-request service |
|---|---|---|---|---|---|
| Contributor convenience | High | Low–Medium | Low | High | High |
| Access and permission management | None | Open to all | Good (per-user invitations) | Good (per-contributor links) | Fair |
| Confidential and hidden materials | Weak | **Unsuitable** | Good | Good | Fair–Good (depends on contract) |
| Large files | Poor | Needs LFS | Needs LFS | Good | Good |
| Licensing records | Manual | Manual (in manifest) | Manual (in manifest) | Enforced at upload | Manual |
| Automated validation | Poor | Excellent | Excellent | Good | Poor–Fair |
| Reviewer workflow | Poor | Excellent | Excellent | Needs internal store | Needs internal store |
| Version history | Poor | Excellent | Excellent | Fair (versioned uploads) | Fair |
| Auditability | Poor | Excellent | Excellent | Good (logs) | Fair |
| Future publication | — | Direct | Via release build | Via release build | Via release build |
| Engineering effort | None | Low | Low | Low (minimal) / none in A | None |

## 5. Recommendation (proposed)

1. **Standardize the package first**. Every channel carries the same schema-valid package; the channel is recorded in `submission.channel`.
2. **Pilot:** an institutionally approved file-request service or a minimal hosted upload link, followed by staff intake into the internal store.
3. **MVP and beyond:** a hosted upload with validation on arrival — embedded in the platform under Option A, standalone under Option B — plus an optional private-Git path for technical contributors.
4. **Internal review store:** a private Git repository per release, with continuous-integration checks (schema validation, leakage scan, validation-ladder runs) and object storage for large files referenced by checksum. Reviewers work in pull requests opened by staff, so contributors never need GitHub.
5. **E-mail** only as a fallback for small packages without hidden material, or as encrypted archives.
6. **Publication** is a separate build step from the internal store: agent-tier materials and public metadata, canary-marked. The hidden tier stays private unless O-001 decides otherwise.

## 6. Open questions

- O-001 (release policy) determines whether any public channel is acceptable.
- Which storage and transport options are reliable for contributors in mainland China, and whether a region-specific path is needed.
- Retention and deletion policy for packages, transcripts, and withdrawn contributions.
- Handling of **unpublished** code or data in Path B (embargo, confidentiality agreements).
