# R8: Replication-package standards, data licensing, and a citation-checked catalogue of consequential econometric pitfalls

| Field | Value |
|---|---|
| Topic | (a) Replication-package standards and data licensing in economics: the Data and Code Availability Standard (DCAS), journal policies and archives, data-editor checks, reported reproducibility, restricted data, package size, software, Stata containers and licensing, redistributability of common datasets, default licences. (b) A catalogue of consequential econometric pitfalls: the mistake, its consequence, a computational detection idea, and its status, with a citation check for every reference. (c) Documented real errors and well-known contested cases. (d) Candidate papers for the three pilot archetypes in the [pilot plan](../../pilot/pilot-evaluation-plan.md) §8. |
| Date | 2026-11-05. All sources accessed 2026-11-05. Corrections added 2026-11-05: see [Corrections](#corrections-2026-11-05-independent-econometric-review) and [further corrections](#corrections-2026-11-05-cross-document-consistency-review). |
| Author | research agent |
| Scope | Top-5 journals (AER, Econometrica, JPE, QJE, REStud) and the field journals that appear in the same standards documents. Pitfalls: the 35 references named in the assignment, plus eight additions verified at [P-page] or [S]. Pilot: four Top-5 candidates and one field-journal alternate. Institute for Replication (I4R) material already in [R4](R4-replication-benchmarks.md) §2.4 is cross-referenced, not repeated. |
| Evidence labels | **[P-full]** primary source, full text read (a whole policy page, blog post, standard, data file or report section). **[P-page]** primary source read in part: landing page, abstract, README, repository file, or an author's own software documentation. **[S]** secondary: search-engine summary, third-party documentation or bibliography, aggregator. **[U]** unverified: my domain knowledge, or a claim I could not check here. Text marked *(assessment)* is my analysis, not a sourced fact. |
| How primary sources were reached | Most official sites in this area are built from public GitHub repositories: DCAS, the AEA Data Editor's guidance and blog, the AEA Data Editor's annual-report repositories, the REStud and JPE Data Editor sites, and the Social Science Data Editors (SSDE) site and databases. I read their **source files** through raw.githubusercontent.com or shallow `git clone`. I did not see the rendered pages. Commit identifiers are listed under Sources. |
| Evidence limits | www.aeaweb.org (DNS failure) and api.crossref.org (proxy refusal) failed. Under the two-failure rule I then stopped trying new hosts, so openICPSR, Harvard Dataverse, Zenodo, journal and publisher sites, StataCorp and data-provider sites were not tried. The WebSearch budget, shared across agents, was exhausted after 12 queries. **No journal article was read in full.** Many volume, issue and page details in §3.2 remain [U]. Facts about QJE's policy are [U]. |
| Relation to other notes | Complements [R4](R4-replication-benchmarks.md). Uses the rubric's `established` / `conditional` / `contested` statuses ([task-quality rubric](../../methodology/task-quality-rubric.md) GT-2; decision-log D-013, X-003). Informs [construction protocol](../../methodology/benchmark-construction-protocol.md) Stage 0, decisions P-015 (no restricted microdata in packages) and P-016 (open-source environments by default), and pilot plan §8. |

## Summary (10 bullets max)

1. **Four of the Top-5 endorse DCAS v1.0; QJE does not appear.** DCAS v1.0 is dated 15 December 2022 and has 16 rules [P-page/P-full]. Its endorser file lists 19 journals: AER and the other AEA journals (but not Papers and Proceedings), Econometrica, JPE and REStud among them, but not QJE [P-page]. QJE is also absent from the SSDE members list [P-page]. QJE's own policy is [U].
2. **Archives and checks differ by journal.** AEA uses openICPSR and runs pre-publication reproducibility checks for all regular AEA journals, with only basic checks for Papers and Proceedings [P-full]. JPE uses Harvard Dataverse, and "eventual publication … is conditional on a positive outcome" of its checks [P-page]. REStud uses Zenodo [P-full]. The Econometric Society journals use Zenodo [P-page].
3. **Default licences are open, but third-party restrictions remain.** CC BY 4.0 is the AEA repository default, with Modified BSD suggested for code; REStud recommends CC BY 4.0 [P-full]. A deposit licence does not override third-party terms. In November 2024 the PSID asked many authors to remove PSID extracts from published AEA packages [P-full].
4. **Common data sources differ sharply in redistributability** (SSDE terms-of-use database) [P-full]:
   - IPUMS sample extracts may be published "to meet journal requirements".
   - PSID, WRDS (Compustat, CRSP), the World Values Survey, DHS, the UK Data Archive and Kilts–Nielsen may not be redistributed.
   - US federal works are public domain unless explicitly restricted. CPS- and NLSY-specific terms are [U].
5. **Restricted data are the norm in AEA submissions.** At intake, 379 of 528 "cases" (about 72%) had some access restriction, and 105 were "very difficult to obtain" [P-full; the unit and time window are not stated, U]. In the 2024 report year, 103 manuscripts involved a data use agreement (DUA) or non-disclosure agreement (NDA) [P-full].
6. **Most packages are small, with a heavy tail.** In the 2024 report window, the median AEA package was 40.4 MB and the mean 3.3 GB. About 20% of packages rounded to more than 2 GB and 5% to more than 20 GB (n = 458) [P-full].
7. **Stata dominates, and Stata containers carry licensing constraints.** Stata scripts appear in 71.6% of more than 8,000 packages, MATLAB in 24.5%, R in 9.8% and Python in 4.1% [S]. The AEA Data Editor's Stata images contain © Stata binaries, posted with StataCorp's permission but without a licence. Users must mount a valid licence at run time [P-page]. Results can change with the Stata version or the processor count [P-full].
8. **Passing a data-editor check is not the same as being correct.** The AEA reports give decision outcomes, not a reproducibility rate: 80.6% of manuscripts were accepted after one round, many of them "with changes" [P-full]. I4R found coding errors in about a quarter of the studies it reproduced (26% in economics) [S].
9. **Pitfall catalogue (§3).** It has 21 entries:
   - 14 have an `established` core and a computational signature, so metamorphic or simulation checks can detect them.
   - Several are `conditional`.
   - Kelly's spatial-noise critique, how far the literature is affected by Young's findings, and IV strength thresholds are `contested` *(assessment)*.
   - Of the 35 named references, 18 have venue and year confirmed (9 at [P-page], 9 at [S]), 4 only as working papers or bare mentions, and 13 not at all [U]. Crossref and publisher hosts were blocked.
   - *Corrected 2026-11-05: P10 split, an entry (P22) added, and P12, P14 and P15 reclassified; see [Corrections](#corrections-2026-11-05-independent-econometric-review).*
10. **Pilot candidates (§5).** Stevenson & Wolfers (2006, QJE), Ludwig & Miller (2007, QJE), Meyersson (2014, Econometrica) and Autor, Dorn & Hanson (2013, AER).
    - Each has public, small (≤ 12 MB) data redistributed by the authors of methods software (`bacondecomp`, `rdpackages`, `ShiftShareSE`, and the GPSS and BHJ replication repositories).
    - The licence is either missing or is a software licence [P-page].
    - The original package locations are [U].
    - All four are canonical teaching datasets, so contamination is high.
    - No recommendation is made.

## Corrections (2026-11-05, independent econometric review)

*Added on 2026-11-05 after an independent econometric review of the project's methodology. The findings in the rest of this note are kept unchanged as its dated record; where they conflict with this section, this section supersedes them. The corrected statuses are Proposed (decision-log P-033) until the research lead approves them. The references are the reviewer's and were not checked here: where §3.2 verifies a venue, that is noted, but the reviewer's reading of the source remains [U].*

### Status corrections in the catalogue (§3.1)

| Entry | Status in §3.1 | Corrected status | Reviewer's reason | References |
|---|---|---|---|---|
| **P10a** RD with a global high-order polynomial | E (as part of P10) | E | A real error. P10 bundled two real errors with a non-error. | Gelman & Imbens (2019) [U] (R26, unverified in §3.2) |
| **P10b** RD with a conventional confidence interval at the MSE-optimal bandwidth | E (as part of P10) | E | A real error; the valid counterpart is bias-corrected inference. | Calonico, Cattaneo & Titiunik (2014) (R25: venue [P-page]; reading [U]) |
| **P10c** RD bandwidth choice | E (as part of P10) | Not a failure mode: a decision-space node | A chosen bandwidth combined with bias-corrected inference is valid. | — |
| **P22** *(added)* RD standard errors clustered by a discrete running variable | — | E | A practice associated with Lee & Card (2008) that has been shown to give poor coverage and is now discouraged. | Lee & Card (2008) [U]; Kolesár & Rothe (2018), *AER* [U] |
| **P12** shift-share regression with conventional standard errors | E | C | Exposure-robust standard errors follow from shock-based identification, so the error is conditional on which framework applies (P13). | Adão, Kolesár & Morales (2019) (R31) and Borusyak, Hull & Jaravel (2022) (R30): venues [P-page]; reading [U] |
| **P14** relying only on robust or clustered standard errors in randomized experiments | E for the tool; X for the extent of the problem | X or C, to be settled when the taxonomy is vetted | Relying on these standard errors is itself a contested choice, not an established error. | Young (2019) (R32) [U] |
| **P15** many outcomes or subgroups with no multiple-testing correction | E for the need; C for the family | C | Whether a correction is required depends on how the family of tests is defined. | R33–R35 as in §3.2 |

**Other remarks from the same review (no status change):**
- **P11 (manipulation test).** It has no computational consequence of its own, and §5 notes that it means little for a 1960 poverty rate. It is a diagnostic, not a flaw with a consequence, which matters for how RD tasks and pilot archetypes are described.
- **No exact relation for RD pitfalls.** A constant injected effect moves a local-linear estimate at any bandwidth, and a global quartic, by exactly τ ([verifier protocol](../../methodology/verifier-validation-protocol.md) §5.5). P10a, P10b and P22 are therefore verified through conditional references for declared conventions and through coverage simulations during validation.
- **Re-classification.** Statuses are revisited at each release against new methodological literature (verifier protocol L13).

### Grading of inference-only pitfalls (§3.1 P6; §3.3)

The detection ideas for P6 ("it should be about 5%") and in §3.3 ("size simulations … with the rejection rate as the score") would grade an agent by the size of its test. That is infeasible: detecting a size of 10% against 5% takes about 150 re-runs of the agent's pipeline, and 7% against 5% about 820 ([verifier protocol](../../methodology/verifier-validation-protocol.md) §4 item 7). A 5% key would also fail correct conventional inference with few treated clusters (Conley & Taber 2011; MacKinnon & Webb 2018 [U]). Inference is therefore graded deterministically, against the conditional reference for the declared variance estimator; size and coverage simulations are used only to validate verifiers (rungs L4 and L7).

## Corrections (2026-11-05, cross-document consistency review)

*Added on 2026-11-05 after a cross-document consistency review. As with the corrections above, the rest of this note is kept unchanged as its dated record; where it conflicts with this section, this section supersedes it.*

- **Share of inference-only entries (§3.3; §6 item 8).** "About half" should read "about a third": 7 of the 21 entries (P6, P7, P8, P12, P14, P15, P20) change mainly inference, and only P6, P7, P12 and P14 change standard errors alone (§3.1, *Changes* column; P8 also moves the point estimate, and P15 and P20 also affect interpretation). After the status corrections above, P10b and P22 also change inference only.
- **Restricted data (§6 item 3).** Implication 3 is superseded by decision-log P-027 and the [verifier protocol](../../methodology/verifier-validation-protocol.md) §6: semi-synthetic data on real covariates inherit the original licence and serve only redistributable data; for restricted sources the route is fully synthetic data, with disclosure review and the provider's permission where required.
- **ADH implementations and GT-1 (§5, D4 pros; §6 item 12).** The three public ADH implementations (`ShiftShareSE`, GPSS, BHJ) support differential testing. They were written by methods authors to reproduce their own papers' analyses, so whether any meets GT-1's clean-room standard (a re-implementation of the same target analysis by someone who has not read the original code; P-028, Proposed) is [U]. The same applies to the `rdpackages` scripts for the RD candidates.

---

## 1. Method

- **Searches.** 12 WebSearch queries covered DCAS endorsers, the AEA Data Editor's reports, the template README, AEA licensing, software shares, Stata in Docker, and I4R error rates. Three further queries, on the Econometric Society, QJE and JPE policies, were refused because the shared budget was exhausted.
- **Primary material via GitHub.** I fetched raw files and made shallow or partial clones of:
  - DCAS
  - the AEA Data Editor's guidance, blog, annual-report repositories (2021–2024), `docker-stata`, `replication-template` and cumulative summary
  - the REStud and JPE Data Editor sites
  - the SSDE site, terms-of-use database and guidance
  - authors' package repositories and CRAN mirrors (github.com/cran)
  - the `rdpackages-replication` repositories
  - Jonathan Roth's website source
  - the replication repositories of Borusyak, Hull & Jaravel and of Goldsmith-Pinkham, Sorkin & Swift
- **Handling downloaded material.** I executed nothing from downloaded material. I read CSV headers with `head`, and listed one ZIP archive's contents with `python3 -I`. I did not load R data files.
- **Failures.** Two hosts failed: www.aeaweb.org (DNS) and api.crossref.org (proxy 403). I then stopped trying new hosts.

---

## 2. Findings (a): standards, archives, checks, licences

### 2.1 The Data and Code Availability Standard (DCAS)

- **Identity.** Version **1.0**, dated **15 December 2022**, DOI 10.5281/zenodo.7436134. The authors are Miklós Koren, Marie Connolly, Joan Llull and Lars Vilhuber, and the standard is maintained by the SSDE [P-page: `_config.yml` and README of github.com/social-science-data-editors/dcas]. The site carries the disclaimer "Journal policies may vary." [P-page].
- **Content.** There are 16 rules in four groups [P-full: `_data/rules.csv`]:
  - Data: (1) Data Availability Statement, (2) raw data, (3) analysis data, (4) format, (5) metadata, (6) citation.
  - Code: (7) data transformation, (8) analysis, (9) format.
  - Supporting materials: (10) instruments, (11) ethics, (12) pre-registration, (13) documentation.
  - Sharing: (14) location, (15) licence, (16) omissions.
- **Rules that matter most for DeepEcon** [P-full]:
  - Rule 3: "Analysis data is provided as part of the replication package unless they can be fully reproduced from accessible data within a reasonable time frame."
  - Rule 13: the README lists "all software and hardware dependencies and requirements (including the expected run time)" and follows the SSDE template README.
  - Rule 15: "A license specifies the terms of use of code and data in the replication package. The license allows for replication by researchers unconnected to the original parties."
- **Endorsement procedure.** A journal is listed after adapting its policy so that it "implements all points of the DCAS" and links to datacodestandard.org [P-page: README].
- **Template README.** The current development version in the repository is 1.2.rc1 [P-page: template-README.md].
  - It asks authors to state rights ("documented permission to redistribute/publish the data"), to list software versions, and to give run time and storage in bands from "<10 minutes" to "> 14 days" and from "<25 MB" to "> 250 GB" [P-page].
  - The citable v1.1 has DOI 10.5281/zenodo.7293838 [S]. The AEA Data Editor's PSID post links to that DOI [P-full].

### 2.2 Who endorses DCAS, where packages are archived, and who checks them

| Journal | Endorses DCAS v1.0 | Data editor | Archive | Pre-publication check | Licence rule |
|---|---|---|---|---|---|
| **AER**, plus AEJ: Applied, Policy, Macro, Micro, AER: Insights, JEL, JEP | Yes [P-page]. AEA Papers and Proceedings is not listed [P-page]. | Lars Vilhuber, Cornell [P-page] | AEA Data and Code Repository at openICPSR. Other trusted repositories are accepted, and duplicate deposits are discouraged [P-full] | Comprehensive checks for all regular AEA journals; basic checks for Papers and Proceedings [P-full] | CC BY 4.0 by default; Modified BSD suggested for code [P-full] |
| **Econometrica**, with Quantitative Economics and Theoretical Economics | Yes [P-page]; the policy is described as compatible with DCAS [S] | Joan Llull [P-page] | Zenodo community `es-replication-repository` [P-page] | [U] | [U] |
| **JPE** | Yes [P-page] | Florian Oswald [P-page] | Harvard Dataverse, `JPE` [P-page] | "The JPE will perform reproducibility checks … of all conditionally accepted papers … Eventual publication of the paper is conditional on a positive outcome of those checks." [P-page] | The licence must "allow for unrestricted access to all files" and replication use. A non-proprietary copy of the data files (for example `.csv`) is "required in every case" [P-page] |
| **QJE** | Not in the endorser file [P-page] | Not in the SSDE members list [P-page] | [U] | [U] | [U] |
| **REStud** | Yes [P-page] | Andrea Moro, Vanderbilt [P-page] | Zenodo community `restud-replication`; packages are uploaded as ZIP [P-full] | Checked by the Data Editor; exemptions only if requested at first submission [P-full] | CC BY 4.0 recommended; "Other (Attribution)" allowed [P-full] |

- **Field journals in the DCAS endorser file** [P-page]: Canadian Journal of Economics, Econometrics Journal, Economic Inquiry, Economic Journal, JEEA and Review of Financial Studies.
- **Their archives** [P-page: SSDE `members.csv`]:
  - Economic Journal and Econometrics Journal: Zenodo, `ej-replication-repository`.
  - JEEA: Zenodo, `jeea_replication`.
  - Review of Financial Studies: Harvard Dataverse, `rfs`.
  - Canadian Journal of Economics: Borealis.
  - Economic Inquiry: ICPSR.
- **AEA policy revision.** A search result shows an archived AEA page titled "Previous Data and Code Availability Policy (February 2024 - February 2026)" [S], which implies a revision in February 2026. Neither version could be read [U].

### 2.3 Restricted, confidential and proprietary data

**AEA.**
- **Policy text.** As quoted by the AEA Data Editor on 2026-05-08: "In rare cases where any of requirements (i)-(iv) above cannot be met due to valid constraints beyond the authors' control, the AEA data editor and the journal editor may choose to modify the requirement(s) … However, in these cases the source of the data must still be disclosed to the AEA data editor prior to final acceptance of the paper." [P-full for the post; the policy page itself was not reached].
- **Guidance** [P-full: "Privately sharing restricted-access data with the AEA Data Editor", 2021-04-08]:
  - "Do NOT upload the restricted-access data to openICPSR."
  - Authors may share data privately only if their DUA, NDA or licence permits it.
  - The Data Editor can sign NDAs (the Cornell standard NDA is preferred), use a secure upload, or work in Cornell's secure remote-access environments.
  - "Whatever restrictions are imposed on the data typically convey to other replicators as well."
- **Limits of the check.** "If we have, or can acquire in a reasonable time, all of the resources needed, then we conduct a computational check. If not, we conduct only a visual inspection of the code" [P-full: reproducibility-checks guidance].
- **Anonymous data providers.**
  - The Data Editor verifies that the provider is legitimate.
  - There were 5 such cases in the 12 months before May 2026 [P-full].
  - The published title-page footnote states that the provider's identity was revealed to the Data Editor [P-full].

**REStud** [P-full: policy and simulated-data pages, repository commit aae52a0, 2026-10-23].
- An exemption must be requested in the cover letter at first submission.
- If the Data Editor cannot get temporary access, authors "must supply a simulated (synthetic) dataset together with the corresponding simulated output".
- The goal "is not to reproduce your published results. It is to verify that your code is complete, self-contained, and logically consistent".
- Simulated data must keep the same variable names, types and formats as the real data, and respect sign and support restrictions. Matching the distribution is not required.
- Authors must preserve confidential data for at least five years.

**JPE** [P-page].
- The exemption request must be made at first submission.
- Authors must either give temporary access to the data or include "a synthetic or simulated dataset that enables users to execute the code and verify that it generates all outputs".
- Data must be preserved for at least five years.

**WRDS (source of Compustat and CRSP).**
- WRDS allows raw data to be shared with a journal or its auditor "only for audit purposes", provided the data are not retained, reused or redistributed, and are deleted afterwards [P-page: SSDE information page quoting WRDS guidance as of 2025-11-11].

### 2.4 What data-editor checks measure, and the reproducibility figures reported

- **AEA scale.**
  - Since 2019, about 3,244 manuscripts and 5,064 reports have been handled.
  - The lab now handles about 400 articles a year, and 2,066 of the manuscripts have been published (excluding JEP).
  - Papers and Proceedings articles get a "cursory review" [P-full: "Impacts of the AEA Verification Process", dated 2026-10-07].
- **2024 report window (2023-12-01 to 2024-11-30)** [P-full: report source, repository commit fdadd6d]:
  - 684 requests covering 507 manuscripts.
  - 446 reports (343 manuscripts) returned to editors.
  - Eight manuscripts were sent to external replicators.
  - Median processing time across all rounds ranged from 41 to 95 days, depending on the journal.
- **Rounds.**
  - Of 217 manuscripts in the rounds table (AER, AER: Insights and the four AEJs), 175 (80.6%) were accepted, with or without changes, after one round; 37 needed two rounds and 5 (2.3%) needed three [P-full: `tables/n_rounds.tex` and `latexnums.tex`; I computed the denominator].
  - Earlier report years give 77.8% (2021 report) and 91.9% and 84.5% (2022 and 2023 reports) [P-full: `latexnums.tex`; definitions may differ slightly between years].
- **Last recommendation on record, conditional-acceptance stage, 2024 report** [P-full: report Table 1]:
  - Accept: 31
  - Accept with changes: 249
  - Conditional accept: 120
  - Conditional accept, manuscript ready: 2
  - Revise and resubmit: 2
- **What these figures are not** *(assessment)*. They are not a reproducibility rate.
  - "Accept with changes" allows "minor fixable bugs in code" and "minor numerical differences in a small number of table cells" [P-full].
  - Restricted-data packages may receive only a code inspection [P-full].
  - I found no single "share fully reproduced" statistic in the 2021–2024 report sources I searched (negative finding, not exhaustive).
- **After publication.**
  - In the 2024 report year there were 42 post-publication modification actions.
  - "A large number were initiated by the data custodians at the PSID" for packages posted before 2020 [P-full].
  - Some updates followed I4R Replication Games [P-full].
- **I4R.** See R4 §2.4 for the PNAS and Nature studies. New here:
  - The I4R Replication Games paper (IZA DP 16912) reports coding errors in about a quarter of studies once minor issues are excluded: 26% in economics against 16% in political science [S].
  - The major errors it lists include "a large number of duplicated observations, incomplete interaction in difference-in-differences regressions, miscoding of the treatment variable" [S].
- **Historical baseline.** McCullough, McGeary & Harrison (2006) examined the archive of the *Journal of Money, Credit and Banking*: "Of more than 150 empirical articles, fewer than 15 could be replicated." [S: abstract as reproduced in the AEA Data Editor's bibliography].

### 2.5 How common restricted data are

- **AEA intake classification.** The figure in the 2026-05-08 post classifies data access into five categories [P-full; I read the figure visually]:

  | Access category | Cases | Can be shared privately with the Data Editor |
  |---|---|---|
  | No restriction | 149 | n/a |
  | Very easy to obtain | 73 | 31 |
  | Moderately easy to obtain | 45 | 27 |
  | Moderately difficult to obtain | 156 | 70 |
  | Very difficult to obtain | 105 | 41 |
  | **Any restriction** | **379** | **169 (44.6%)** |

  - Authors make the first classification on the Data and Code Availability Form, and the team may recode it [P-full]. Whether a "case" is a manuscript or a data source, and the time window, are not stated [U].
  - Any restriction: 379 of 528 cases, about 72% (my computation).
  - *(Assessment)* "Restricted" includes registration-required public data such as PSID and IPUMS. The "very difficult" category (about 20%) is the closer proxy for confidential administrative data.
- **Agreements.** In the 2024 report year, 103 manuscripts involved a DUA or NDA: 5 DUAs, 1 DUA plus an informal NDA, 2 formal NDAs and 95 informal NDAs. The 2023 report year had 66 [P-full]. Set against 507 manuscripts received, that is roughly one in five (my computation; the denominators are not strictly comparable).
- **Data supplied without the right to redistribute it.** The 2023 report names "the World Values Survey, the Panel Study of Income Dynamics, the Socio-Economic Panel, the UN COMTRADE database, and even in one case a Compustat extract" as data that authors had inadvertently included without redistribution rights [P-full].

### 2.6 Package size and file counts (AEA Data and Code Repository)

| Report year (Dec–Nov) | Deposits | Median | Mean | 75th percentile | Rounds to > 2 GB | Rounds to > 20 GB | Total | Files |
|---|---|---|---|---|---|---|---|---|
| 2021 | n/a | 35.4 MB | 2.29 GB | (reported as 7,448 MB, which contradicts the 19% share above 2 GB; probably computed differently, U) | 19% | 3% | n/a | n/a |
| 2022 | 427 | 30.2 MB | 2.28 GB | 635 MB | 15% | 3% | 951 GB | 51,394 |
| 2023 | 496 | 35.3 MB | 2.16 GB | 813 MB | 17% | 3% | 1,045 GB | 54,864 |
| 2024 | 458 | 40.4 MB | 3.32 GB | 1.45 GB | 20% | 5% | 1,486 GB | 65,812 |

- **Source and definitions** [P-full: `latexnums.tex` and `05_prepare_icpsr2.R` in each report repository].
  - Sizes are reported in MB, where 1 MB = 1024² bytes.
  - The "> 2 GB" share is the share of deposits whose size *rounded to whole GB* exceeds 2.
  - The report text phrases these as "larger than 2GB" and "larger than 20GB".
- **Repository limits.**
  - openICPSR: a hard limit of 1,000 files (as of 2021), and it "struggles" above 30 GB (as of 2022). Opaque ZIP files are "generally prohibited" [P-full/P-page].
  - Zenodo: 50 GB and 100 files per record by default.
  - Harvard Dataverse: up to 1 TB free [P-page: AEA guidance].
- **Very large packages.** Packages over 30 GB go to Zenodo. The AEA community there held 23 published deposits totalling 617 GB [P-full].
- **Overall stock.** The AEA repository held 5,094 published packages, with 540,713 downloads [P-full].

### 2.7 Software shares

- **Kranz (December 2023), across more than 8,000 economics articles with packages** [S: R-bloggers syndication; Kranz's original page not reached]:
  - Stata `.do` scripts appear in 71.6% of packages, MATLAB in 24.5%, R in 9.8% and Python in 4.1%. Shares exceed 100% because some packages use several languages.
  - R grew from 1.4% (2010) to over 20% (2023), and Python from 0.4% to almost 10%.
- **AEA 2024 report.** The empirical literature "remains dominated by Stata and MATLAB, but open-source software (R, Python, Julia) is being increasingly used". Open-source packages "can often be more challenging to reproduce" because versions change quickly and environments are rarely pinned [P-full].
- **Package practices** [P-full: 2023 report]:
  - Only "Between 28 and 50% of packages" contain a master script.
  - Very few packages use containers.
- **Other indicators.** In the I4R AI games, 58 teams worked in R and 45 in Stata (R4) [P-page via R4]. In a 48-paper I4R corpus, 54% of papers use Stata (R4) [S].

### 2.8 Stata in containers: images and licensing

- **AEA Data Editor images** [P-page: README of github.com/AEADataEditor/docker-stata, commit fdbec27, which names github.com/ssc-ng/docker-stata as the primary source]:
  - "The image … contains binary code that is © Stata. Permission was granted by Stata to Lars Vilhuber to post these images, without the license. A valid license is necessary to build and use these images."
  - The licence file is bind-mounted at run time (`-v stata.lic:/usr/local/stata/stata.lic`), or passed as a BuildKit secret during the build.
  - Variants: `be`, `se` and `mp`; `-i` images include help files; `-x` (GUI) images are explicitly not functional.
  - Example images are about 1.1–1.9 GB.
  - The README's examples now use the Docker Hub namespace `sscng`. The 2022–2024 AEA reports cite `hub.docker.com/u/dataeditors` [P-full].
- **StataCorp FAQ "run Stata in a Docker container"** [S]: licence information must never be shared with or embedded in the image. Bind-mount it at run time, and keep all use within the licence terms.
- **StataCorp blog** [S]: licences may be used on cloud virtual machines. Shared machines need enough cores for the licensed number of users.
- **Free cloud licence for the AEA.** Stata gave the AEA Data Editor "a free license to use Stata 17/18 for one year in cloud applications" [P-full: 2023 and 2024 reports].
- **SSDE Docker guidelines** [P-full]:
  - If software needs a licence or API key, the image creator must ensure that it "is not included in the container as distributed".
  - Analysis data and code should not be inside the container.
  - Containers should be preserved as tar files, because registries "regularly prune" images.

### 2.9 Evidence that results drift across platforms and versions

- **Processor-dependent convergence** (AEA Data Editor, 2026-07-24) [P-full].
  - A first-stage model converged only on some combinations of Stata version and processor count.
  - StataCorp found that the Hessian was numerically singular: the model was not identified on any platform.
  - The post's lesson: "**We only detect some of these issues.**"
- **Memory varies across platforms** (AEA Data Editor, 2026-10-08) [P-page]. Authors should "report computational requirements as measurements, and say where you measured them".
- **Different answers across Stata versions** (Florian Oswald on the JPE Data Editor site, 2025-12-23, affiliation given as "EJ Data Editor") [P-full].
  - The built-in `xporegress` gave different results in Stata 16 and Stata 18, even with `version 16` set, in an *Economic Journal* 2024 package.
  - "Data Editors do not care about backward compatibility": they want "a very specific description of the required environment".
- **Version notes from authors** (Borusyak, Hull & Jaravel replication README, update dated 2025-03-01) [P-page]. Run under `version 16`, because sorting changed and the `mixed` command "reports different standard errors than in our original analysis".

### 2.10 Can common datasets be redistributed?

| Dataset or provider | Terms (quoted) | Redistributable in a public package? | Source |
|---|---|---|---|
| IPUMS USA and IPUMS CPS samples (also ATUS, NHGIS, NHIS, MEPS) | "You will not redistribute the data without permission. You may publish a subset of the data to meet journal requirements for accessing data related to a particular publication." | Yes, as a journal-replication subset. Other redistribution requires permission. The AEA *requires* sample extracts plus extract specifications | [P-full: SSDE terms-of-use database, entry dated 2022-12-09; AEA report template] |
| IPUMS USA full count; IPUMS International | "You may not redistribute any data from IPUMS USA Full Count data"; "redistribution of the data to third parties is prohibited" | No | [P-full: SSDE database] |
| CPS public-use files from Census or BLS (not via IPUMS); NLSY (BLS) | US federal works are not copyright-protected and are in the public domain "unless explicitly prohibited" | Probably yes; dataset-specific terms not checked | [P-full for the database's generic entry, which itself cites Wikipedia]; CPS and NLSY specifics [U]; NLSY geocode files are restricted [U] |
| PSID | "Not transfer PSID public data that has been downloaded from the website, including user-created data extracts, to any third parties" | No. Deposit in the PSID repository on openICPSR instead | [P-full: SSDE database; AEA Data Editor post of 2024-11-01] |
| Compustat and CRSP (WRDS) | "authorized to use … only if you are an authorized user" | No. Can be shared with a data editor for audit only | [P-full: SSDE database and WRDS page]; one Compustat extract was found in a package [P-full] |
| Administrative or confidential data (Census FSRDC, IRS, BLS restricted) | Disclosure review (Census DRB) numbers and disclaimers required | No | [P-page: AEA report template; AEA post on FSRDC packages, 2024-04-09] |
| World Values Survey; DHS; UK Data Archive; Kilts–Nielsen | WVS: "the data files themselves are not redistributed"; DHS: redistribution "is not permitted" | No | [P-full: SSDE database; AEA post of 2024-04-29] |
| UN Comtrade | 2024 policy: no permission needed for some uses, including small extractions (≤ 100,000 records) | Conditional | [P-full: SSDE database, entry dated 2024-10-29] |
| Penn World Table; OECD; CEPII-BACI | CC BY 4.0; "Generally open with exceptions"; Etalab open licence | Yes | [P-full: SSDE database] |

A useful heuristic from the AEA Data Editor: "If the website asks for registration, it is highly likely that there are redistribution restrictions." [P-full: post of 2024-04-29].

### 2.11 Default licences of replication packages

- **AEA** [P-full: licensing guidance; 2024 report §Intellectual Property; FAQ on reuse].
  - "At the AEA Data and Code Repository, CC BY 4.0 … is the default license."
  - For code, Modified BSD is suggested, and a dual-licence template is provided: BSD for code, CC BY for "databases, images, tables, text".
  - Authors retain copyright, and the Data Editor vets licences.
  - The AEA "will insist on an open license that allows for replication by researchers unconnected to the original parties".
  - Deposits migrated from the AEA website in 2019 are "(© AEA)", with automatic permission to "use and re-publish them" with citation.
  - Most newer deposits use mixed CC BY/BSD or CC BY.
- **REStud.** CC BY 4.0 recommended; any licence must permit replication use [P-full]. **JPE.** The licence must permit unrestricted access and replication use [P-page]. **Econometric Society.** [U].
- **SSDE template README.** For code it offers the placeholder "MIT/BSD/GPL [choose one!]". For data, "Authors should actively select a license", noting that some licences are "sticky", that is, inherited from the original provider [P-page].
- **What this means** *(assessment)*.
  - A CC BY or BSD deposit licence grants only the rights the authors hold.
  - Third-party data inside such a deposit keeps the provider's terms; the PSID take-downs show this.
  - DeepEcon must therefore check rights **file by file**.

---

## 3. Findings (b): catalogue of consequential pitfalls

How to read the catalogue:
- **Consequence codes:** PE = point estimate; SE = standard errors and inference; ID = identification; INT = interpretation or estimand.
- **Status** follows rubric GT-2:
  - `established` (E): a consensus error;
  - `conditional` (C): an error under stated, checkable conditions;
  - `contested` (X): genuine methodological disagreement, which belongs on the experimental track.
- The **mechanism** cells are sourced where labelled. The **detection** and **status** columns are *(assessment)*.
- Reference IDs (R1, R2, …) point to the citation check in §3.2.

### 3.1 Catalogue

| ID | The mistake | Why it matters (sourced where labelled) | Changes | How to detect or verify computationally *(assessment)* | Status *(assessment)* | Refs |
|---|---|---|---|---|---|---|
| P1 | Static two-way fixed effects (TWFE) DiD with staggered adoption when effects vary across cohorts or over time | The TWFE estimator "equals a weighted average of all possible two-group/two-period DD estimators" [S: Goodman-Bacon WP abstract]. Weights "may be negative … the linear regression coefficient may for instance be negative while all the ATEs are positive" [S: de Chaisemartin & D'Haultfœuille WP abstract]. The problems come from conflating parallel trends and no-anticipation with "implicit assumptions that restrict treatment effect heterogeneity" [S: Borusyak, Jaravel & Spiess WP abstract]. | PE, INT | Run the Goodman-Bacon decomposition (share of later-vs-earlier comparisons) and check for negative weights. **Simulation:** add known, heterogeneous and growing effects to semi-synthetic untreated outcomes. Heterogeneity-robust estimators (Callaway–Sant'Anna, Sun–Abraham, imputation) recover the true ATT; TWFE does not. **Metamorphic:** adding a late-treated cohort, or dropping the never-treated units, moves the TWFE coefficient but leaves cohort-specific ATT(g,t) unchanged. **Null control:** with zero planted effects, all estimators give about 0. | E for the algebra; C for materiality, which depends on how much effects vary | R1–R5, R9 |
| P2 | TWFE event study with leads and lags under staggered timing | "the coefficient on a given lead or lag can be contaminated by effects from other periods, and apparent pretrends can arise solely from treatment effects heterogeneity" [S: Sun & Abraham WP abstract]. The interaction-weighted estimator is "consistent … even under heterogeneous treatment effects", using never-treated or last-treated units as controls [P-page: author README]. | PE (each event-time coefficient), INT | **Simulation:** with true zero pre-trends and heterogeneous effects, TWFE leads differ from 0 while robust leads stay near 0. Check this on hidden variants. Also check the control group used (never-treated or last-treated). | E | R4, R3, R5 |
| P3 | Event-study normalization and binning; reading new-method event-study plots as if they were TWFE plots | Recent methods' default plots "construct the pre-treatment coefficients asymmetrically from the post-treatment coefficients", so they "may show a kink or jump at the time of treatment even when the TWFE event-study shows a straight line" [P-page: Roth 2026 abstract]. Equivalence with distributed lags and identification through binning or normalization: [U]. | PE (level), ID, INT | **Metamorphic:** moving the reference period from −1 to −2 shifts all coefficients by a constant while differences stay the same. Check the rank of the full set of relative-time dummies (an extra normalization is needed without never-treated units [U]). Report how endpoints are binned. Check that pre-period coefficients are built the way the method states (Roth 2026). | E for the normalization algebra; C for how to read plots | R8, R10 |
| P4 | Treating a passed pre-trends test as validation of parallel trends | "conventional pre-trends tests may have low power", and "conditioning the analysis on the result of a pre-test can distort estimation and inference" [P-page: Roth 2022 abstract]. Robust inference instead bounds post-treatment violations relative to pre-trends [P-page: Rambachan & Roth 2023 abstract; HonestDiD README]. | SE (coverage), INT, PE (through selection) | Compute the pre-test's power against a stated violation (`pretrends`). Report HonestDiD sensitivity: the "breakdown" value of the bound M̄. **Simulation:** under a calibrated linear violation, estimates conditional on passing the test are biased. | E for low power and pre-test bias; C for the choice of restriction set | R7, R8 |
| P5 *(added)* | Choosing the outcome scale (levels or logs) without noticing that parallel trends depends on it | Parallel trends holds under all monotone transformations only under a stronger condition on the CDF of untreated potential outcomes, which has testable implications [P-page: Roth & Sant'Anna 2023 abstract]. | ID | **Metamorphic:** a monotone transformation that flips the sign or significance flags sensitivity to functional form. Run the falsification test. | E for the result; C for which scale is appropriate | R11 |
| P6 | Clustering at the wrong level, or ignoring serial correlation in DiD | Over-rejection when errors are serially correlated and SEs are not clustered; clustering as a design question (level of assignment and sampling) [U: BDM 2004; AAIW 2023; Cameron & Miller 2015]. | SE only | **Placebo-law simulation:** assign fake treatments to clusters in the real data and measure the rejection rate under the agent's SE choice (it should be about 5%). *Corrected 2026-11-05: a check for validating verifiers, not a grading key ([Corrections](#corrections-2026-11-05-independent-econometric-review)).* **Metamorphic:** duplicating every observation k times leaves clustered SEs about the same but shrinks non-clustered SEs by about √k. | E for the serial-correlation problem; C for the clustering level, which depends on the design-based or sampling view | R12–R14, R16 |
| P7 | Few clusters, or few treated clusters, with the usual cluster-robust variance estimator | A wild cluster bootstrap improves inference with clustered errors [S: CGM 2008 title]; fast implementations exist [S]. Size of the problem: [U]. | SE | Report the number of clusters and treated clusters. Compare cluster-robust p-values with wild-cluster-restricted bootstrap p-values. Simulate size using the actual cluster structure. | E for the over-rejection; C for which bootstrap variant | R15–R17 |
| P8 | Weak instruments: conventional 2SLS t-test, the "F > 10" habit, or a non-robust first-stage F under heteroskedastic or clustered errors | The tF procedure adjusts t critical values for first-stage F; in `ivDiag` the critical value reaches 1.96 only when F ≥ 106.09, from the table in Lee et al. (2022) [S]. Diagnostics include the effective F and the Anderson–Rubin test and confidence set [S]. The weak-IV result itself: [U: Staiger & Stock 1997; Stock & Yogo 2005]. | SE (coverage); PE (bias towards OLS [U]) | Compute the effective F. **Metamorphic:** it is "invariant to any nonsingular linear transformation" of the instruments [S: `ivDiag` source], and so are the 2SLS estimates. Report the Anderson–Rubin confidence set and tF. **Monte Carlo:** coverage of the conventional confidence interval at the estimated first-stage strength. | E for the problem; X for thresholds and rules of thumb, which are still evolving | R18–R22 |
| P9 | Interpreting the IV estimate as an ATE or population effect; ignoring monotonicity | IV identifies a local average treatment effect for compliers under monotonicity [U: Imbens & Angrist 1994]. | INT; ID if monotonicity fails | Mostly needs expert-judged (V3) grading. **Semi-synthetic test:** with heterogeneous effects and a known complier share, check the agent's claims against the true LATE and ATE. Comparing estimates across instruments shows complier heterogeneity. | E for the theorem; C for monotonicity | R23 |
| P10 | RD with global high-order polynomials, an ad hoc bandwidth, or conventional confidence intervals | `rdrobust` provides "local-polynomial point estimators and robust confidence intervals" and data-driven bandwidth selection [P-page: `rdrobust` description; CCT 2014 title]. That this is the current standard is my assessment. The case against high-order polynomials: [U: Gelman & Imbens 2019]. | PE, SE | **Metamorphic:** adding or removing observations far outside the bandwidth should leave a local estimate unchanged, while a global polynomial moves. Placebo cutoffs should give about 0. Check stability around the MSE-optimal bandwidth and coverage under simulation. | E. *Corrected 2026-11-05: split into P10a (E), P10b (E) and P10c (a decision-space node), and P22 (E) added; see [Corrections](#corrections-2026-11-05-independent-econometric-review).* | R24–R26 |
| P11 | RD without a manipulation test, or treating "no rejection" as proof of no sorting | Density tests at the cutoff [S: McCrary 2008; Cattaneo, Jansson & Ma 2020]. | ID | Run `rddensity` and test covariate continuity. **Hidden variant:** plant manipulation (move mass across the cutoff) and expect the agent to detect it. Run a "donut" robustness check. | E as a diagnostic; passing it is not proof (INT) | R27–R28 |
| P12 | Shift-share regression with conventional standard errors (clustered by region, or heteroskedasticity-robust) | Shift-share designs need AKM or AKM0 confidence intervals [P-page: `ShiftShareSE` description]. Conventional SEs over-reject when regions with similar sector shares have correlated residuals [U]. | SE | AKM-style **placebo:** random sector shocks, with the rejection rate of conventional SEs measured. Compare AKM and state-clustered SEs on the same data; the `ShiftShareSE` vignette replicates AKM Table V, column 1, on ADH data [P-page]. | E. *Corrected 2026-11-05: C ([Corrections](#corrections-2026-11-05-independent-econometric-review)).* | R29, R31 |
| P13 | Unexamined identification in a shift-share (Bartik) design: shares or shocks? | Rotemberg weights show which industries drive the estimate; each is "the misspecification elasticity for each individual instrument" [P-page: GPSS README]. A shock-level view uses shock-level aggregates [P-page: BHJ README, `ssaggregate`]. Exogeneity conditions and the incomplete-shares control: [U]. | ID, INT | Compute Rotemberg weights; drop the top industries one at a time. Run shock-level balance tests and compute the effective number of shocks. Check the incomplete-shares control. | E for the frameworks; C for which framework applies | R29–R31 |
| P14 | Relying only on asymptotic robust or clustered SEs in randomized experiments | Randomization tests reassess "seemingly significant" results [U: Young 2019]. A Stata implementation exists [P-page: `ritest` README]. | SE | Re-randomize treatment, respecting the actual strata and clusters, and compare with analytic p-values. **Metamorphic:** relabelling unit IDs should not change the randomization-inference p-value beyond simulation noise. | E for the tool's validity; X for the extent of the problem in the published literature. *Corrected 2026-11-05: X or C ([Corrections](#corrections-2026-11-05-independent-econometric-review)).* | R32 |
| P15 | Many outcomes or subgroups with no multiple-testing correction | Romano–Wolf FWER control is implemented in `wildrwolf` [S]. "Anderson (2008) sharpened two-stage q-values is the standard in applied micro" [S: Sant'Anna workflow rule]. | SE, INT | Count the tests reported. Recompute Romano–Wolf p-values or FDR q-values and check headline claims against the adjusted values. | E for the need; C for how the family is defined (pre-registration). *Corrected 2026-11-05: C ([Corrections](#corrections-2026-11-05-independent-econometric-review)).* | R33–R35 |
| P16 | log(1+Y) or arcsinh(Y) effects read as percentage effects when Y can be zero | ATEs for "log-like" transformations "depend on the units of the outcome"; "one can obtain a treatment effect of any magnitude simply by re-scaling the units of Y". Alternatives include Poisson regression and separate extensive- and intensive-margin effects [P-page: Chen & Roth abstract]. | PE, INT (estimand) | **Metamorphic scale test:** multiply Y by 100 (cents instead of dollars). A log-like ATE moves materially when there is an extensive margin; a Poisson or level-percentage estimand does not. | E, a mathematical result; C for which remedy to use | R36 |
| P17 | Gravity or other log-linearized model estimated by OLS on log(Y), dropping zeros | "under heteroskedasticity, the parameters of log-linearized models estimated by OLS lead to biased estimates of the true elasticities" [S: Santos Silva & Tenreyro abstract, reproduced in the `gravity` package bibliography]. | PE, sample | Count the zeros dropped. Compare OLS on log(Y) with PPML. **Simulation:** heteroskedastic multiplicative errors with a known elasticity. | E for the bias; C for PPML versus other pseudo-maximum-likelihood estimators | R37 |
| P18 | "Bad controls": conditioning on variables affected by the treatment | Post-treatment controls bias causal comparisons [U: Angrist & Pischke 2009]. | PE, ID | Audit timing (is the control measured after treatment?). Regress the candidate control on treatment. **Semi-synthetic test:** a design with a known mediator. Often needs expert grading (V3). | E for the concept; C for whether a given control is bad | R38 |
| P19 | Synthetic control with conventional SEs, poor pre-treatment fit, or a cherry-picked donor pool | The synthetic control method [P-page: ADH 2010, cited in the `Synth` documentation by two of its authors]. Placebo-based inference and feasibility conditions: [U: Abadie 2021]. | SE, INT, PE (donor pool) | Distribution of post/pre RMSPE ratios across in-space placebos; in-time placebos; leave-one-donor-out. Check that weights are non-negative and sum to 1. Results should not depend on donor order. | E for placebo-based inference; C for design details | R39–R40 |
| P20 | Ignoring spatial correlation, for example in persistence regressions | GMM with cross-sectional dependence, which underlies Conley SEs [S: Conley 1999]. The claim that persistence results reflect spatial noise: [U: Kelly 2019, 2020]. | SE; INT (persistence claims) | Compute Moran's I on residuals. Compare Conley SEs across distance cutoffs. **Spatial-noise placebo:** regress the outcome on simulated spatially autocorrelated noise and calibrate t-statistics. | E for spatial SEs; X for Kelly's critique of the literature | R41–R42 |
| P21 *(added; computational layer)* | Fragile computation: platform- or version-dependent convergence; models that are not identified but still return numbers | See §2.9 [P-full/P-page]. | Reproducibility of PE and SE | Run the reference implementation on at least two platforms, versions and thread counts. Fail on missing SEs, a singular Hessian, or `quietly` around estimation. Pin versions (`version` alone is not enough [P-full]). | E (documented cases) | §2.9 |

### 3.2 Citation check

"Verified" means confirmed in a source I read. Volume, issue and pages from my memory are given only as [U].

| ID | Reference | Verified here (label: source) | Still unverified |
|---|---|---|---|
| R1 | Goodman-Bacon, "Difference-in-differences with variation in treatment timing" | Journal of Econometrics, 2021 (ScienceDirect pii S0304407621001445) [S: Naqvi DiD resources]. NBER WP w25018 (2018) abstract [S: `didimputation` bibliography] | 225(2): 254–277 [U] |
| R2 | de Chaisemartin & D'Haultfœuille, "Two-way fixed effects estimators with heterogeneous treatment effects" | AER 2020, DOI 10.1257/aer.20181169 [S: Naqvi]. NBER WP w25904 abstract [S] | 110(9): 2964–2996 [U] |
| R3 | Callaway & Sant'Anna, "Difference-in-differences with multiple time periods" | Journal of Econometrics 2021, DOI 10.1016/j.jeconom.2020.12.001 [P-page: the authors' `did` package CITATION] | 225(2): 200–230 [U] |
| R4 | Sun & Abraham, "Estimating dynamic treatment effects in event studies with heterogeneous treatment effects" | Journal of Econometrics 2021 [S: `fixest` documentation; Naqvi, pii S030440762030378X] | 225(2): 175–199 [U] |
| R5 | Borusyak, Jaravel & Spiess, "Revisiting event-study designs: robust and efficient estimation" | Working-paper versions only (2021 and 2023) [P-page: author README; S: bibliography] | REStud 2024, 91(6): 3253–3285 [U] |
| R6 | Roth, Sant'Anna, Bilinski & Poe, "What's trending in difference-in-differences? A synthesis of the recent econometrics literature" | Journal of Econometrics 2023 (pii S0304407623001318) [P-page: Roth's site] | 235(2): 2218–2244 [U] |
| R7 | Roth, "Pre-test with caution: event-study estimates after testing for parallel trends" | AER: Insights 2022, DOI 10.1257/aeri.20210236 [P-page: Roth's site] | 4(3): 305–322 [U] |
| R8 | Rambachan & Roth, "A more credible approach to parallel trends" | REStud 2023, DOI 10.1093/restud/rdad018 [P-page: Roth's site; `HonestDiD` DESCRIPTION by Rambachan] | 90(5): 2555–2591 [U] |
| R9 | Roth & Sant'Anna, "Efficient estimation for staggered rollout designs" *(added)* | JPE Microeconomics 2023, DOI 10.1086/726581 [P-page: Roth's site] | Volume and pages [U] |
| R10 | Schmidheiny & Siegloch, "On event studies and distributed-lags in two-way fixed effects models: identification, equivalence, and generalization" | Not verified | JAE 2023, 38(5): 695–713 [U] |
| R10a | Roth, "Interpreting event-studies from recent difference-in-differences methods" *(added)* | Japanese Economic Review 2026 (special issue), DOI 10.1007/s42973-026-00235-x [P-page: Roth's site] | Volume and pages [U] |
| R11 | Roth & Sant'Anna, "When is parallel trends sensitive to functional form?" *(added)* | Econometrica 2023 [P-page: Roth's site] | Volume and pages [U] |
| R12 | Bertrand, Duflo & Mullainathan, "How much should we trust differences-in-differences estimates?" | Not verified | QJE 2004, 119(1): 249–275 [U] |
| R13 | Cameron & Miller, "A practitioner's guide to cluster-robust inference" | Not verified | JHR 2015, 50(2): 317–372 [U] |
| R14 | Abadie, Athey, Imbens & Wooldridge, "When should you adjust standard errors for clustering?" | Not verified | QJE 2023, 138(1): 1–35 [U] |
| R15 | Cameron, Gelbach & Miller, "Bootstrap-based improvements for inference with clustered errors" | REStat 2008, 90(3): 414–427 [S: `sandwich` documentation] | DOI [U] (the documentation gives the NBER t0344 DOI) |
| R16 | MacKinnon, Nielsen & Webb, "Cluster-robust inference: a guide to empirical practice" *(added)* | Journal of Econometrics, DOI 10.1016/j.jeconom.2022.04.001 [S: `sandwich` documentation, listed as forthcoming] | Year, volume and pages [U] |
| R17 | Roodman, MacKinnon, Nielsen & Webb (2019), `boottest` *(added)* | Stata Journal 2019, DOI 10.1177/1536867X19830877 [S: `fwildclusterboot` DESCRIPTION] | Title [U] |
| R18 | Staiger & Stock, "Instrumental variables regression with weak instruments" | Not verified | Econometrica 1997, 65(3): 557–586 [U] |
| R19 | Stock & Yogo, "Testing for weak instruments in linear IV regression" | Not verified | In Andrews & Stock (eds.), *Identification and Inference for Econometric Models*, CUP 2005, pp. 80–108 [U] |
| R20 | Andrews, Stock & Sun, "Weak instruments in instrumental variables regression: theory and practice" | Annual Review of Economics 2019, 11: 727–753, DOI 10.1146/annurev-economics-080218-025643 [S: `ShiftShareSE` vignette bibliography] | — |
| R21 | Lee, McCrary, Moreira & Porter, "Valid t-ratio inference for IV" | AER 2022, 112(10): 3260–90, DOI 10.1257/aer.20211063 [S: `ivDiag` documentation] | — |
| R22 | Lal, Lockhart, Xu & Zu, "How much should we trust instrumental variable estimates in political science? Practical advice based on 67 replicated studies" *(added)* | Political Analysis 2024, 32(4): 521–540, DOI 10.1017/pan.2024.2 [S: `ivDiag` documentation] | — |
| R23 | Imbens & Angrist, "Identification and estimation of local average treatment effects" | Not verified | Econometrica 1994, 62(2): 467–475 [U] |
| R24 | Imbens & Lemieux, "Regression discontinuity designs: a guide to practice" | Not verified | Journal of Econometrics 2008, 142(2): 615–635 [U] |
| R25 | Calonico, Cattaneo & Titiunik, "Robust nonparametric confidence intervals for regression-discontinuity designs" | Econometrica 2014, 82(6): 2295–2326 [P-page: `rdrobust` documentation by the authors] | — |
| R26 | Gelman & Imbens, "Why high-order polynomials should not be used in regression discontinuity designs" | Not verified | JBES 2019, 37(3): 447–456 [U] |
| R27 | McCrary, "Manipulation of the running variable in the regression discontinuity design: a density test" | Journal of Econometrics 2008, 142(2): 698–714, DOI 10.1016/j.jeconom.2007.05.005 [S: `rdd` documentation] | — |
| R28 | Cattaneo, Jansson & Ma, "Simple local polynomial density estimators" *(added)* | JASA 2020, 115(531): 1449–1455 [S: `rddensity` documentation] | — |
| R29 | Goldsmith-Pinkham, Sorkin & Swift, "Bartik instruments: what, when, why, and how" | 2019 working paper cited in the authors' README [P-page] | AER 2020, 110(8): 2586–2624 [U] |
| R30 | Borusyak, Hull & Jaravel, "Quasi-experimental shift-share research designs" | REStud 2022, 89(1), first page 181 (from the article URL) [P-page: authors' replication README] | Last page (213) [U] |
| R31 | Adão, Kolesár & Morales, "Shift-share designs: theory and inference" | QJE 2019, 134(4): 1949–2010, DOI 10.1093/qje/qjz025 [P-page: `ShiftShareSE` documentation by Kolesár] | — |
| R32 | Young, "Channeling Fisher: randomization tests and the statistical insignificance of seemingly significant experimental results" | Not verified (`ritest` README links a related Young paper only) | QJE 2019, 134(2): 557–598 [U] |
| R33 | Anderson, "Multiple inference and gender differences in the effects of early intervention: a reevaluation of the Abecedarian, Perry Preschool, and Early Training projects" | Cited as "Anderson (2008)" [S: Sant'Anna workflow] | JASA 2008, 103(484): 1481–1495 [U] |
| R34 | List, Shaikh & Xu, "Multiple hypothesis testing in experimental economics" | 2015 working paper cited in the authors' code README [P-page] | Experimental Economics 2019, 22(4): 773–793 [U] |
| R35 | Romano & Wolf (2005a, 2005b) *(added)* | DOIs 10.1198/016214504000000539 and 10.1111/j.1468-0262.2005.00615.x [S: `wildrwolf` DESCRIPTION] | — |
| R36 | Chen & Roth, "Logs with zeros? Some problems and solutions" | QJE 2024, 139(2), first page 891 (from the article URL). A corrigendum exists [P-page: Roth's site] | Last page (936) [U]; content of the corrigendum [U] |
| R37 | Santos Silva & Tenreyro, "The log of gravity" | REStat 2006, 88(4): 641–658, DOI 10.1162/rest.88.4.641 [S: `gravity` package bibliography] | — |
| R38 | Angrist & Pischke, *Mostly Harmless Econometrics: An Empiricist's Companion* | Not verified | Princeton University Press, 2009; "bad control" section [U] |
| R39 | Abadie, Diamond & Hainmueller, "Synthetic control methods for comparative case studies: estimating the effect of California's tobacco control program" | JASA 2010, 105(490): 493–505 [P-page: `Synth` documentation by Hainmueller and Diamond] | — |
| R40 | Abadie, "Using synthetic controls: feasibility, data requirements, and methodological aspects" | Not verified | JEL 2021, 59(2): 391–425 [U] |
| R41 | Conley, "GMM estimation with cross sectional dependence" | Journal of Econometrics 1999, 92(1): 1–45 [S: `conleyreg` bibliography] | — |
| R42 | Kelly, "The standard errors of persistence" (2019) and "Understanding persistence" (2020) | Not verified | Working papers (CEPR or UCD); whether they were later published [U] |

**Tally.** The assignment names 35 references.
- **18 have venue and year confirmed.**
  - 9 at [P-page]: R3, R6, R7, R8, R25, R30, R31, R36, R39.
  - 9 at [S]: R1, R2, R4, R15, R20, R21, R27, R37, R41.
- **4 are confirmed only as working papers or bare in-text mentions:** R5, R29, R33, R34.
- **13 could not be verified at all [U]:** R10, R12, R13, R14, R18, R19, R23, R24, R26, R32, R38, R40, R42.
- The eight additions (R9, R10a, R11, R16, R17, R22, R28, R35) are verified at [P-page] or [S].
- *Before any collaborator-facing use, verify every [U] element against Crossref or the publisher's page.*

### 3.3 Patterns for detection *(assessment)*

- **About half the catalogue changes only inference** (P6, P7, P8, P12, P14, P15, P20). A verifier that compares point estimates alone will pass these flawed variants as if they were "equivalent mutants". The output contract must include SEs or CIs and must name the inference method. Hidden-variant tests should include **size simulations**: placebo treatments or placebo shocks, with the rejection rate as the score. *(Corrected 2026-11-05: size simulations validate verifiers but do not grade agents; see [Corrections](#corrections-2026-11-05-independent-econometric-review). "About half" should read "about a third"; see [further corrections](#corrections-2026-11-05-cross-document-consistency-review).)*
- **Metamorphic relations available from the sources:**
  - effective-F invariance (P8);
  - unit-rescaling sensitivity of log-like ATEs (P16);
  - shifting the reference period (P3);
  - locality of RD estimates (P10);
  - invariance to duplication under clustering (P6).
  These map directly to verifier-ladder rung L6 in the [verifier validation protocol](../../methodology/verifier-validation-protocol.md).
- **Semi-synthetic data with planted effects** (P1, P2, P9, P17, P18) give a known truth. This separates *statistical validity* from *identification validity*, as decision D-013 requires.
- **Items that probably need expert-judged (V3) grading or the experimental track:** P9 (LATE interpretation), P13 (choosing the shares or shocks framework), P18 (bad controls), P20 (Kelly), and the threshold disputes in P8.

---

## 4. Findings (c): documented errors and contested cases

| Case | Original paper | Critique or replication | What was found (as widely reported) | How it was found | Classification *(assessment)* |
|---|---|---|---|---|---|
| Reinhart–Rogoff | Reinhart & Rogoff, "Growth in a time of debt", AER 2010, 100(2): 573–578, DOI 10.1257/aer.100.2.573 [S: AEA Data Editor bibliography] | Herndon, Ash & Pollin, Cambridge Journal of Economics 2014, 38(2): 257–279, DOI 10.1093/cje/bet075 [S] | A spreadsheet error left out several countries, plus selective exclusion of available data and unconventional weighting [U] | A graduate student's replication from the authors' spreadsheet [U] | Mixed: an **established** coding error, plus **contested** analytic choices (weighting and exclusions) |
| Donohue–Levitt | Donohue & Levitt, QJE 2001, 116(2): 379–420 [U] | Foote & Goetz, QJE 2008, 123(1): 407–423; reply by Donohue & Levitt, QJE 2008, 123(1): 425–440 [U] | State-by-year interactions described in the paper were missing from the code; a per-capita arrests specification weakened the results [U] | Re-running the authors' code and data [U] | An **established** mismatch between the stated estimator and its implementation (failure mode 1 in the brief). The substantive conclusion remained **debated** after the reply [U] |
| Police and crime | Levitt, AER 1997, 87(3): 270–290 [U] | McCrary, AER 2002, 92(4): 1236–1243 [U] | A weighting or programming error; the corrected estimates were imprecise [U] | Replication [U] | **Established** coding error |
| Colonial origins | Acemoglu, Johnson & Robinson, AER 2001, 91(5): 1369–1401 [U] | Albouy, AER 2012, 102(6): 3059–3076; reply AER 2012, 102(6): 3077–3110 [U] | How the settler-mortality series was constructed (assignment of data across countries) [U] | Data-construction audit [U] | **Contested**: methodological and data disagreement |
| "Worm wars" | Miguel & Kremer, Econometrica 2004, 72(1): 159–217 [U] | Aiken et al. (2015) and Davey et al. (2015), International Journal of Epidemiology 44(5); response by Hicks, Kremer & Miguel (2015) [U] | A pure replication found coding errors, some acknowledged, notably in the spillover estimates. A "statistical replication" using different analysis choices weakened some results, which the original authors disputed [U] | A third-party replication programme [U] | Mixed: **established** coding errors plus **contested** analytic choices |
| I4R Replication Games | Many papers | Brodeur et al., IZA DP 16912 [S] | Coding errors in about a quarter of studies (26% in economics); major examples were duplicated observations, incomplete DiD interactions and a miscoded treatment [S] | Teams reproducing papers in one-day events [S] | **Established**, naturally occurring implementation errors (failure mode 6) |
| I4R AI games catalogue | 12 papers | Brodeur et al., PNAS 2026 (R4) | 122 catalogued errors, for example "Education was entered as continuous … -3105 values become massive outliers" [P-page via R4] | Randomized team study | **Established** |
| Processor-dependent convergence | An AEA submission | AEA Data Editor, 2026 [P-full] | A model that was not identified "converged" only on some platforms | Pre-publication verification together with StataCorp | **Established** computational and statistical problem |
| JMCB archive | More than 150 articles | McCullough, McGeary & Harrison, JMCB 2006, 38(4): 1093–1107 [S] | "fewer than 15 could be replicated" [S] | Archive audit | Reproducibility failure (archive quality), not an econometric error |

**Implication** *(assessment)*.
- **Established errors** are suitable for scored tasks:
  - implementation does not match the description (Donohue–Levitt);
  - wrong data ranges (Reinhart–Rogoff);
  - duplicates or miscoded treatment (I4R).
- **Contested cases** (AJR–Albouy; the worm-wars analysis choices) are interpretation or design disagreements. Under X-003 they belong only on the experimental track, perhaps as "which assumptions differ" tasks without a binary key.
- Several cases **mix** the two. The interview should separate the computational error from the disputed choice, as Stage 3 of the construction protocol proposes.

---

## 5. Findings (d): pilot candidates (no recommendation)

Archetype labels follow pilot plan §8. "Public copy" means data redistributed by a third party, usually a methods author, that I could inspect. I did not check any original journal package, because the archive hosts were not reachable.

| | **D1 Stevenson & Wolfers (2006, QJE)**, "Bargaining in the shadow of the law: divorce laws and family distress" [title, volume and pages U] | **D2 Ludwig & Miller (2007, QJE)**, "Does Head Start improve children's life chances? Evidence from a regression discontinuity design", 122(1): 159–208, DOI 10.1162/qjec.122.1.159 [S] | **D3 Meyersson (2014, Econometrica)**, "Islamic rule and the empowerment of the poor and pious", 82(1): 229–269, DOI 10.3982/ecta9878 [S] | **D4 Autor, Dorn & Hanson (2013, AER)**, "The China syndrome: local labor market effects of import competition in the United States", 103(6): 2121–2168, DOI 10.1257/aer.103.6.2121 [S] |
|---|---|---|---|---|
| Archetype | Staggered-adoption DiD on a public state panel. The assignment says Goodman-Bacon (2021) uses it [U] | Sharp RD on the 1960 county poverty rate [variable names P-page; design detail U] | Sharp RD on the vote margin of close elections [variables P-page; design detail U] | Shift-share IV on commuting zones over two periods [P-page] |
| Original package location | [U] | [U] | [U] (Econometric Society supplementary material [U]) | [U]. Probably openICPSR, since the AEA migrated about 2,500 pre-2019 packages there [P-full], but not verified |
| Public copy | `divorce` dataset in the CRAN package `bacondecomp` v0.1.1 (2020) [P-page] | `headstart.csv` / `.dta` in `rdpackages-replication/CTV_2017_JPAM` (Cattaneo, Titiunik & Vazquez-Bare 2017, JPAM 36(3): 643–681) [P-page/S] | `CIT_2020_CUP_polecon.csv` / `.dta` in `rdpackages-replication/CIT_2020_CUP` (the Cattaneo–Idrobo–Titiunik 2020 Cambridge Element) [P-page] | (i) `ADH` in the CRAN package `ShiftShareSE`; (ii) the GPSS `bartik-weight` repository; (iii) the BHJ `shift-share` repository, with `ADH.zip` reproducing BHJ Tables 1–4 and C1–C5. Original source: David Dorn's website [P-page via documentation; site not accessed] |
| Data and redistributability | 3,366 observations × 147 variables, documented only as "Data from Stevenson and Wolfers (2006, QJE)" [P-page]. The package licence is MIT. The data's own licence and provenance are [U] | 2,810 counties. Variables: running variable `povrate60`; mortality outcomes (ages 5–9 Head Start-related, injuries, all causes, by race; **pre-period placebo** `mort_age59_related_preHS`); 1960 and 1990 census covariates [P-page]. The repository has **no LICENSE file** [P-page]. Data licence [U] | 2,629 municipalities. Variables `X` (margin), `Y`, `T`, `vshr_islam1994`, `hischshr1520m` and covariates [P-page]. **No LICENSE file** [P-page]. Licence and provenance of the Turkish data [U] | `ShiftShareSE` is GPL-3: 722 commuting zones × 2 periods, outcomes for total, manufacturing and non-manufacturing employment shares, and a share matrix [P-page]. GPSS is MIT-licensed; its authors say they "are only able to provide the data for … ADH directly here, as the others use data from IPUMS, which prohibits the posting of a full dataset" [P-page]. BHJ is GPL-3 [P-page]. The underlying inputs include IPUMS-derived and trade data whose terms are [U] |
| Software | R (`bacondecomp`); a Stata version exists [U] | R, Stata and Python scripts [P-page] | R, Stata and Python scripts [P-page] | R (`ShiftShareSE`); Stata and R (GPSS, BHJ) [P-page] |
| Size | `divorce.rda` 692 KB, compressed [P-page] | CSV 511 KB; dta 377 KB [P-page] | CSV 311 KB; dta 273 KB [P-page] | `ADH.rda` 1.2 MB; GPSS ADH inputs about 10 MB; BHJ `ADH.zip` 11.5 MB [P-page] |
| Possible two target analyses *(assessment)* | Two outcomes from the 147-variable file, once a codebook exists [U] | Main mortality effect, plus the pre-period placebo or the race-specific outcome | Female outcome `Y`, plus the male outcome `hischshr1520m` (my reading of the name [U]) | Manufacturing versus non-manufacturing employment-share change |
| Pros *(assessment)* | Top-5; tiny; the archetypal staggered DiD for P1–P4, P6 and P7; the decomposition gives checkable intermediate outputs | Top-5; tiny; classic sharp RD for P10 and P11; CTV (2017) re-examined inference approaches on these data, giving an independent reference [S] | Top-5; tiny; close-election RD with covariates and density testing (P10, P11); reference code in three languages | Top-5; the canonical application of all three shift-share papers, so **three independent reference implementations** exist for the GT-1 independent check *(GT-1 status [U]; see [further corrections](#corrections-2026-11-05-cross-document-consistency-review))*; established pitfalls P12 and P13 |
| Cons *(assessment)* | Undocumented variables; licence and provenance unknown; original package not located; extremely familiar in DiD teaching | Rare-event mortality outcomes make estimates noisy, which may blur the consequences of flaws; licence unstated; well-known teaching example; a manipulation test means little for a 1960 poverty rate | The main teaching example of a widely used RD primer, so contamination is very high; licence unstated; only a subset of the paper's variables | Very famous; Stata version sensitivity noted by BHJ [P-page]; ambiguous licensing of derived data; exposure-robust SEs need share matrices, which makes the environment more complex |

- **Field-journal alternate (not Top-5).** Cheng & Hoekstra (2013, JHR), castle-doctrine laws: `castle` in `bacondecomp`, 520 observations × 159 variables, 81 KB [P-page]. It is also used in the package vignette [P-page].
- **General caveat** *(assessment)*. For every candidate, the data's legal status rests on redistribution by methods authors under a software licence (MIT or GPL) or under no licence at all. That is evidence of community practice, not a grant of rights. The pilot uses the data internally, so the risk there is lower than for a public release.

---

## 6. Implications for DeepEcon (assessment, not decisions)

1. **Add a file-level licence gate to Stage 0.**
   - Neither DCAS compliance nor a CC BY deposit licence establishes the right to redistribute *each file*; the PSID take-downs of pre-2020 packages show this.
   - For every data file, record its provenance, the provider's terms (using the SSDE terms-of-use database as a starting point) and the evidence of redistribution rights.
   - Treat "registration required" as a red flag.
2. **Prefer packages from the DCAS era with a data editor**: AEA after 2019, JPE, REStud and the Econometric Society.
   - Their licences have been vetted (AEA).
   - JPE requires non-proprietary copies of data files, which eases R and Python environments under decision P-016.
   - Their READMEs follow a template.
   - Be cautious with QJE until its policy is verified.
3. **Plan for semi-synthetic data as the main route, not the exception.** *(Superseded 2026-11-05 for restricted data; see [further corrections](#corrections-2026-11-05-cross-document-consistency-review).)*
   - About 72% of AEA intake "cases" involve some restriction, and about 20% are "very difficult".
   - REStud and JPE packages with **simulated data plus simulated output** are useful precedents and raw material. They are designed to exercise the code path, not to reproduce the paper, so DeepEcon still needs its own design-preserving semi-synthetic variants.
4. **Size screen.** The median package (about 40 MB) is unproblematic, but about 1 in 5 exceeds about 2 GB. Target analyses should run on bounded analysis datasets. Protocol Stage 0's "under about 1 hour" compute screen needs a matching storage screen.
5. **Ports from Stata will be routine, and tolerances must allow for documented drift.**
   - Stata appears in about 72% of packages.
   - Cross-version and cross-platform differences are documented (`xporegress`; processor-dependent convergence).
   - Verifier tolerances must be set empirically (rung L9, repeat stability).
   - Avoid target analyses near numerical non-identification.
   - Run reference implementations on at least two platforms.
6. **A licensed Stata track has a specific leakage risk.**
   - The licence must be mounted at run time, and in an agent-accessible container the evaluated agent could read it, which matters for compliance and security.
   - StataCorp's permission covers Vilhuber's posting of the images; whether it extends to DeepEcon's redistribution is [U].
   - Large-scale automated evaluation needs explicit licensing terms.
   - This supports P-016.
7. **"Passed a data-editor check" does not mean "correct".**
   - Data-editor checks are computational.
   - I4R finds coding errors in about a quarter of the studies it reproduced.
   - The GT-1 independent check of the reference implementation therefore stays necessary.
   - I4R's error types (duplicates, incomplete DiD interactions, miscoded treatment) are ready-made, realistic flaw templates that satisfy Safeguard G.
8. **Output contracts must include inference.** About half the catalogued pitfalls change only SEs, so tasks that score only coefficients cannot detect them. Hidden-variant tests should include placebo-based size checks. *(Corrected 2026-11-05: about a third; see [further corrections](#corrections-2026-11-05-cross-document-consistency-review).)*
9. **Use the statuses in §3.1 for admission.** *(Statuses corrected 2026-11-05; see [Corrections](#corrections-2026-11-05-independent-econometric-review).)*
   - `established` pitfalls with computational signatures (P1–P4, P6–P8, P10–P12, P16, P17, P19, P21) suit V1 and V2 scoring.
   - `conditional` items need the conditions shown in the task data.
   - `contested` items (P8 thresholds, P14's literature-wide claims, P20 Kelly, AJR–Albouy, the worm wars) belong on the experimental track (X-003).
10. **Citation hygiene is itself a task for the pipeline.** Here, 13 of the 35 named references could not be verified at all, and 4 more only as working papers, because Crossref and publisher hosts were blocked. The Stage 3 citation-verification step needs network access to Crossref or publisher sites, or a pre-built verified bibliography.
11. **Contamination.** All four pilot candidates are canonical *teaching* datasets with public method implementations. That suits a pilot that compares workflows (pilot plan §8, criterion 5) but not admitted tasks, which would need perturbed or semi-synthetic variants.
12. **ADH as a cross-validation testbed.** Three independent public implementations (`ShiftShareSE`, GPSS, BHJ) let an "independent reference implementation" check (GT-1) run almost free on the shift-share archetype. The same holds, to a lesser degree, for the RD candidates (R, Stata and Python scripts by the `rdpackages` team). *(Corrected 2026-11-05: whether these meet GT-1 is [U]; see [further corrections](#corrections-2026-11-05-cross-document-consistency-review).)*

---

## 7. Open questions

1. What are QJE's data policy, archive and pre-publication checks? Does QJE plan to endorse DCAS? (Everything about QJE here is [U].)
2. What changed in the AEA policy revised in February 2026 [S]? Does it affect licences or restricted data?
3. Does IPUMS's exception ("publish a subset … to meet journal requirements") cover redistribution inside a benchmark? Or is IPUMS's permission needed?
4. Are software licences (MIT, GPL-3) attached by methods authors to repositories that contain third-party-derived data, such as `bacondecomp`, `ShiftShareSE`, GPSS and BHJ, valid grants for that data? Can data in repositories with no licence (`rdpackages-replication`) be used at all? This needs legal review.
5. Where are the original packages of the four pilot candidates, and what are their licences, sizes and software? This requires openICPSR, Dataverse, Econometric Society and QJE access.
6. Will StataCorp license automated, containerized, large-scale agent evaluation? How would the licence file be protected from the evaluated agent?
7. For which pitfalls can V1 or V2 verifiers reach acceptable false-negative and false-positive rates? Each needs a small simulation study, for example a size simulation for P6, P7 and P12.
8. Should computational fragility (P21) be a task family in its own right, or only a verifier-design concern?
9. Should contested cases feed interpretation tasks, graded by expert panels or with several keys?
10. Could the AEA's five-category access classification, self-reported on the Data and Code Availability Form, serve as the Stage 0 screen in DeepEcon's own intake form?
11. The 13 fully unverified references in §3.2 need verification before any external use, as do the volume and page details marked [U] and the case details in §4.

---

## 8. Access problems

- **www.aeaweb.org.** WebFetch failed with `getaddrinfo ENOTFOUND`, the host being outside the session's allowed network. As a result the AEA policy, FAQ and Papers and Proceedings pages were not read. I used the AEA Data Editor's GitHub-hosted guidance, blog and report sources instead, including their quotations of the policy.
- **api.crossref.org.** The proxy refused the connection (`CONNECT tunnel failed, response 403`). After these two failures I stopped trying new hosts, as instructed.
- **Hosts therefore not tried:** www.openicpsr.org, dataverse.harvard.edu, zenodo.org, www.econometricsociety.org, academic.oup.com, www.journals.uchicago.edu, www.stata.com, www.ipums.org, psidonline.isr.umich.edu, simba.isr.umich.edu, www.bls.gov, www.census.gov, hub.docker.com, ddorn.net, www.nber.org, ssrn.com and the Data Editor sites as rendered pages.
- **WebSearch.** The shared budget (200 calls per turn across all agents) ran out after my 12th query. Three planned queries, on the Econometric Society, QJE and JPE policies, did not run. The JPE gap was filled from the JPE Data Editor's GitHub source.
- **Proxy status check.** The command `curl "$HTTPS_PROXY/__agentproxy/status"` was denied by the permission classifier. I did not retry it or work around it.
- **Repository names that did not resolve.** `git clone` of `skranz/skranz.github.io` and `restud/restud.github.io` failed with an authentication prompt, meaning the repository does not exist under that name. This was not a network failure.
- **Not used:** arxiv.org (known to be blocked), and any proxy, mirror or reader service.
- **Consequence.** Every claim marked [S] or [U] should be checked against the primary page before it is cited outside the project.

---

## 9. Sources

All sources were accessed on 2026-11-05. "raw" means the file was read through raw.githubusercontent.com; "clone" means a shallow or partial `git clone` from github.com. Short hashes are commits.

**Standards and SSDE**
- DCAS: https://datacodestandard.org/ (rendered page not accessed). Source: https://github.com/social-science-data-editors/dcas (raw; HEAD 6e18582): `_config.yml`, `README.md`, `_data/rules.csv`, `_data/journals.csv`, `journals.md`, `index.md`.
- DCAS v1.0 Zenodo record: https://zenodo.org/records/7436134 [S: search result; not accessed].
- Template README: https://github.com/social-science-data-editors/template_README (raw `template-README.md`; HEAD 698bde9). v1.1 DOI https://doi.org/10.5281/zenodo.7293838 [S].
- SSDE site, members list: https://github.com/social-science-data-editors/social-science-data-editors.github.io (clone 33ec387, 2026-10-21), `_data/members.csv`.
- SSDE terms-of-use database and related pages: https://social-science-data-editors.github.io/reference/TermsOfUse.html (rendered page not accessed). Source: https://github.com/social-science-data-editors/reference (clone 320eaf4, 2026-09-14): `_data/termsofuse.csv`, `_data/verifications.csv`, `_data/trusted-repositories.csv`, `_information/WRDS.md`.
- SSDE guidance: https://github.com/social-science-data-editors/guidance (clone 69f4e63, 2026-10-05): `docs/Guidance/docker-guidelines.qmd`, `docs/Guidance/Requested_information_hosting.qmd`.

**AEA Data Editor**
- Guidance site: https://aeadataeditor.github.io/aea-de-guidance/ (rendered page not accessed). Source: https://github.com/AEADataEditor/aea-de-guidance (raw `website/*.md`; HEAD 5c6a019). Pages read: `Licensing_guidance.md`, `LICENSE-template.md`, `sharing-restricted-data.md`, `reproducibility-checks.md`, `guidelines-other-repositories.md`, `faq/reuse-data-licensing.md`, `faq/more-than-1000-files.md`, `third-party-request.md`, `protocol-3rd-party-replication.md`, `myst.yml`.
- Blog: https://aeadataeditor.github.io/ (rendered page not accessed). Source: https://github.com/AEADataEditor/aeadataeditor.github.io (clone 519f186, 2026-10-22). Posts read:
  - `2024-04-29-use-and-reuse-of-data`
  - `2024-11-01-psid-requests`
  - `2026-05-08-private-data`, with `images/figure_access_provision.png`
  - `2026-07-24-stata-convergence-across-platforms`
  - `2023-01-25-dcas-compliance`
  - `2024-04-09-census-packages`
  - `2026-10-08-memory-across-platforms` (partly)
  - `2026-08-12-PSA-Github` (opening only)
- Annual reports: https://github.com/AEADataEditor/report-aea-data-editor-2024 (clone fdadd6d; `AEADataEditor_Report2024.tex`, `sec_*.tex`, `tables/*.tex`, `programs/05_prepare_icpsr2.R`, `README.md`). Also `-2023` (ddad56a), `-2022` (81eac52) and `-2021` (2fdaa8c).
  - The 2023 report is cited in its repository as Vilhuber (2024), AEA Papers and Proceedings 114: 878–90, DOI 10.1257/pandp.114.878 [P-page]. The 2024 repository README repeats this citation, apparently copied over; the 2024 report's publication details are [U].
  - Deposits: https://doi.org/10.3886/E212781V1 (2024) and https://doi.org/10.3886/E198444V1 (2023), not accessed.
- Cumulative summary: https://aeadataeditor.github.io/aea-cumulative-summary/impacts_of_aea_data_editing.html (rendered page not accessed). Source: https://github.com/AEADataEditor/aea-cumulative-summary (raw `impacts_of_aea_data_editing.md`; HEAD 5a09292).
- Stata images: https://github.com/AEADataEditor/docker-stata (raw README; HEAD fdbec27). Pointer to https://github.com/ssc-ng/docker-stata (not accessed).
- Report template language: https://github.com/AEADataEditor/replication-template (raw `sample-language-report.md`; HEAD 9b7b646).
- AEA policy pages, not reachable: https://www.aeaweb.org/journals/data/data-code-policy ; https://www.aeaweb.org/journals/policies/data-code/ ; archived-policy title at https://swlb1.aeaweb.org/journals/data/archive/2024-2026 [S: search result only].

**Other journals' data editors**
- REStud: https://restud.github.io/data-editor/ and https://restud.dataeditor.group/ (rendered pages not accessed). Source: https://github.com/restud/data-editor (clone aae52a0, 2026-10-23): `policy.md`, `synthetic-data.md`, `zenodo.md`, `index.md`, `after-acceptance.md`.
- JPE: https://jpedataeditor.github.io/ (rendered page not accessed). Source: https://github.com/jpedataeditor/jpedataeditor.github.io (clone 9598d58, 2026-10-22): `policy.qmd`, `posts/20240505-stataversions/index.qmd`.
- Econometric Society policy: https://econometricsociety.org/publications/es-data-editor-website/data-and-code-availability-policy [S: search summary only].

**Software shares, Stata licensing, I4R (secondary)**
- Kranz, "Usage shares of programming languages in economics research" (Dec 2023): https://www.r-bloggers.com/2023/12/usage-shares-of-programming-languages-in-economics-research/ [S].
- StataCorp, Docker FAQ: https://www.stata.com/support/faqs/unix/run-stata-docker-container/ [S]. StataCorp blog on cloud licences: https://blog.stata.com/?p=5682 [S].
- I4R Replication Games: https://docs.iza.org/dp16912.pdf ; https://www.iza.org/index.php/publications/dp16912/1/citations/bibtex [S].
- Brodeur et al. (2026), *Nature*: https://eprints.lancs.ac.uk/id/eprint/236673/ ; https://emiguel.econ.berkeley.edu/research/reproducibility-and-robustness-of-economics-and-political-science-research/ [S]. See also R4.
- Vilhuber talk listing: https://cowles.yale.edu/events/2025/best-practices-reproducible-science-lessons-2400-replication-packages-prof-lars-vilhuber [S].

**Methods: authors' pages and packages**
- Roth's website source: https://github.com/jonathandroth/jonathandroth.github.io (clone 2ab0781, 2026-10-12), `_pages/papers.md`.
- `pretrends`: https://github.com/jonathandroth/pretrends (raw README).
- `HonestDiD`: https://github.com/asheshrambachan/HonestDiD (raw README); CRAN mirror https://github.com/cran/HonestDiD (raw DESCRIPTION).
- `did`: https://github.com/cran/did (raw DESCRIPTION, `inst/CITATION`).
- `EventStudyInteract`: https://github.com/lsun20/EventStudyInteract (raw README).
- `did_imputation`: https://github.com/borusyak/did_imputation (raw README). `didimputation`: https://github.com/cran/didimputation (clone 57b34a9; `inst/references.bib`) and https://github.com/kylebutts/didimputation (raw README).
- `did_multiplegt_dyn`: https://github.com/Credible-Answers/did_multiplegt_dyn (raw README). CRAN mirrors `DIDmultiplegt` and `DIDmultiplegtDYN` (raw DESCRIPTION).
- `bacondecomp`: https://github.com/cran/bacondecomp (raw and clone ddc3872; DESCRIPTION, LICENSE, `man/divorce.Rd`, `man/castle.Rd`, `man/bacon.Rd`, vignette, data file sizes).
- `fixest`: https://github.com/cran/fixest (raw `man/sunab.Rd`).
- `staggered`: https://github.com/jonathandroth/staggered (raw README) and https://github.com/cran/staggered (raw DESCRIPTION).
- `rdrobust`: https://github.com/cran/rdrobust (raw DESCRIPTION, `man/rdrobust.Rd`) and https://github.com/rdpackages/rdrobust (raw README).
- `rddensity`: https://github.com/cran/rddensity (raw `man/rddensity.Rd`). `rdd`: https://github.com/cran/rdd (raw `man/DCdensity.Rd`, `man/IKbandwidth.Rd`).
- `ShiftShareSE`: https://github.com/cran/ShiftShareSE (raw and clone 94bc2f8; DESCRIPTION, `man/ADH.Rd`, vignette and `library.bib`) and https://github.com/kolesarm/ShiftShareSE (raw README).
- GPSS `bartik-weight`: https://github.com/paulgp/bartik-weight (clone 722ceb8; README, LICENSE.md, file sizes).
- BHJ `shift-share`: https://github.com/borusyak/shift-share (clone 802724b; README, LICENSE, listing of `ADH.zip`).
- `sandwich`: https://github.com/cran/sandwich (raw `man/vcovCL.Rd`).
- `fwildclusterboot` and `wildrwolf`: https://github.com/cran/fwildclusterboot ; https://github.com/cran/wildrwolf (raw DESCRIPTION).
- `ivDiag`: https://github.com/cran/ivDiag (clone 13b47a7; DESCRIPTION, `man/ivDiag.Rd`, `man/tF.Rd`, `R/effF.R`). `ivmodel`: https://github.com/cran/ivmodel (raw DESCRIPTION).
- `Synth`: https://github.com/cran/Synth (raw DESCRIPTION, `man/synth.Rd`).
- `conleyreg`: https://github.com/cran/conleyreg (raw `man/conleyreg.Rd`, `inst/REFERENCES.bib`).
- `gravity`: https://github.com/cran/gravity (raw `man/ppml.Rd`, `inst/REFERENCES.bib`).
- `eventstudyr`: https://github.com/cran/eventstudyr (raw DESCRIPTION, `man/EventStudy.Rd`).
- `mht`: https://github.com/seidelj/mht (raw README). `ritest`: https://github.com/simonheb/ritest (raw README).
- `eventdd`, `xtevent`, `conley-se` READMEs (raw; no relevant citations found): https://github.com/damiancclarke/eventdd ; https://github.com/JMSLab/xtevent ; https://github.com/darinchristensen/conley-se.
- DiD resources list: https://github.com/asjadnaqvi/DiD (branch `revert-25-i18n/zh-cn`, clone 495eb06; `docs/reading/04_resources.md`). Current site: https://asjadnaqvi.github.io/DiD/ (not accessed).
- Sant'Anna workflow: https://github.com/pedrohcgs/claude-code-my-workflow (clone 7586127, 2026-11-04), `.claude/rules/inference-robustness.md`.

**Pilot data**
- https://github.com/rdpackages-replication/CIT_2020_CUP (clone 62bb142, 2026-05-19): README, `CIT_2020_CUP_polecon.csv` header and row count, `.R` script, file sizes.
- https://github.com/rdpackages-replication/CTV_2017_JPAM (clone 7dd5dea, 2026-05-19): README, `headstart.csv` header and row count, file sizes.
- `bacondecomp`, `ShiftShareSE`, GPSS and BHJ: as listed above.

**Replication literature and case-study citations**
- AEA Data Editor bibliographies (`refs-zotero.bib`, `references.bib` in the report repositories) for Reinhart & Rogoff (2010), Herndon, Ash & Pollin (2014), McCullough, McGeary & Harrison (2006) and Chang & Li (2015) [S].
- I4R AI games catalogue, via [R4](R4-replication-benchmarks.md) §2.4.
