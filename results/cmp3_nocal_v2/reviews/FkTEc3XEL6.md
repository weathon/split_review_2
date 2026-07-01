## Summary

MOCHA proposes a curated collection of multi-subject spatially resolved transcriptomics (SRT) datasets, each paired with expert pathologist annotations of spatial domains. The paper identifies a genuine gap—existing SRT repositories lack multi-sample cohorts with consistent human-annotated labels—and catalogs 10 cohorts spanning diverse tissues, cancer types, and technologies (10x Visium and ST), totaling 166 subjects/samples. Table 1 provides the core concrete contribution.

## Strengths

- **Clear gap identification.** The introduction (Section 1) convincingly argues that multi-sample SRT method development is constrained by the scarcity of datasets combining gene expression, spatial coordinates, H&E images, and expert domain labels across subjects. The paper contrasts this gap with existing repositories (SORC, Aquila, SODB, STOmicsDB, SpatialDB).

- **Concrete curation output.** Table 1 enumerates 10 cohorts with tissue type, technology, and subject/sample counts (ranging from 94 subjects in BC.TNBC to 3 in KC.TLS). The cohorts span breast cancer subtypes (HER2+, HP, TNBC, NP), colorectal cancer, kidney/lung/RCC cancers with TLS, DLPFC, and mouse olfactory bulb—covering both human and mouse data across two technology platforms.

## Weaknesses

### Major

- **No data access mechanism.** The paper states MOCHA "is released in formats readily usable with Python and R" (line 24) but provides no URL, repository (GitHub, Zenodo, Hugging Face, etc.), DOI, or download instructions anywhere in the manuscript. A dataset paper without any way to access the data cannot be evaluated for correctness, completeness, or usability by reviewers or the community.

- **No experimental validation or utility demonstration.** The paper contains zero experiments: no clustering accuracy metrics, no baseline results from running existing methods on MOCHA cohorts, no comparison of methods against the pathologist annotations, no ablation studies, no case studies, and no runtime or scalability analysis. The central claim—that MOCHA is "a curated resource for developing and evaluating multi-sample SRT methods" (Abstract, line 10)—is asserted but never demonstrated. This is a structural gap for a resource/benchmark paper at any major venue. Even a single experiment (e.g., running STAGATE or BASS on the DLPFC cohort and reporting ARI against the expert labels) would substantiate the claim.

### Minor

- **Annotation characterization is deferred to supplementary.** The paper's main differentiator from existing repositories is expert pathologist annotations, yet the main text only states that annotations can be grouped into four broad categories (immune, stroma, tumor, normal) and that details are in the Supplementary Material (line 90). The main paper should summarize at minimum: per-cohort label taxonomies, label counts, annotation resolution (per-spot vs. per-cell), whether annotations are newly generated or repurposed, and any quality assurance measures. While the supplementary likely contains these details as stated, the main paper should provide sufficient characterization of its central asset.

- **Sections 3 and 4 contain predominantly generic tutorial content.** Section 3 (Pre-processing and batch effect correction, ~20 lines) and Section 4 (Multi-sample spatial clustering methods, ~14 lines) together constitute roughly 40% of the paper body but read as a literature review of standard normalization techniques, batch correction with Harmony, and summaries of three existing methods (BayeSMART, BASS, STAGATE). Apart from Figure 2 (illustrated with the KC_TLS_10x cohort) and the brief annotation-grouping statement (line 90), these sections contain minimal MOCHA-specific content. This space would be better used for resource characterization and validation.

### Trivial

None.

## Nice-to-Haves

- Running at least one multi-sample method (e.g., STAGATE, BASS, or BayeSMART) on one or more MOCHA cohorts and reporting domain identification performance against the expert annotations would substantially strengthen the paper.
- Quantitative comparison against existing repositories (SORC, Aquila, SODB, etc.) showing what MOCHA uniquely provides.
- Discussion of limitations: annotation resolution (per-spot vs. per-cell), platform coverage (only 10x Visium and ST), potential annotation errors.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution.

- "Figure description is garbled (RCC_TL8_10x instead of RCC.TLS_10x)" — removed per formatting-artifact rule; underscore/period differences and minor abbreviation variations ("TL8" vs "TLS") are parser-side artifacts from PDF extraction, not author errors.
- "Since the image is not rendered, these data are not usable" — removed per formatting-artifact rule; images are stripped by the parser, not absent from the original submission.
- Any criticisms that annotation details are entirely absent from the submission — removed per appendix-stripping rule; the paper explicitly states annotation details are "described in the Supplementary Material" (line 90), which the parser removes.
- "No comparison to existing resources" — this is a nice-to-have rather than a missing requirement; the paper's curation is its own contribution and does not require outperforming other databases.
- "No discussion of limitations" — demoted to Nice-to-Haves; not a required section for all resource paper formats.
- All speculative criticisms (e.g., "could the metric be measuring a proxy") — not applicable as there are no experiments to critique.
- The input reviewer's statement that "Sections 3 and 4 are generic tutorials with no MOCHA-specific content" — partially inaccurate; Figure 2 is illustrated with KC_TLS_10x and Section 4 contains the annotation grouping statement. The criticism is demoted to Minor and rephrased to reflect the presence of some MOCHA-specific content.

## Novel Insights

None beyond the paper's own contributions. The reviews identify structural gaps in the submission (missing data access, missing experiments, generic tutorial content) rather than offering novel analytical insights about the method or domain.

## Suggestions

1. Provide a functioning data access link (GitHub, Zenodo, or institutional repository) with clear documentation and a minimal code example that loads and inspects the data.
2. Run at least one existing multi-sample SRT method (e.g., STAGATE or BASS) on the DLPFC cohort and report domain identification accuracy (e.g., ARI or NMI) against the pathologist annotations.
3. Move annotation details from supplementary into the main paper—at minimum the label taxonomy per cohort, number of labels, and annotation protocol summary.
4. Condense Sections 3 and 4 to 2–3 sentences each and replace the freed space with resource characterization (annotation statistics, data format documentation, quality analysis).

## Score and Decision

The paper identifies a real need and provides a useful catalog of 10 multi-subject SRT cohorts. However, it lacks two essential components of a publishable dataset paper: (1) any mechanism to access the data, and (2) any experimental validation that the resource supports meaningful evaluation. The remaining content is partly generic tutorial material. These gaps are structural and cannot be addressed by minor revision. The core idea has merit and could form the basis of a strong resource paper if the data were released and basic baselines were provided, but the current submission does not meet the standards for acceptance.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>