## Summary

This paper presents MOCHA, a curated collection of 10 publicly available spatially resolved transcriptomics (SRT) cohorts spanning multiple cancer types and normal tissues, each with co-registered H&E images and pathologist-provided spatial domain annotations. The goal is to provide a resource for developing and evaluating multi-sample SRT methods — addressing the genuine scarcity of multi-subject datasets with expert annotations.

## Strengths

- **Cohort diversity is a genuine asset.** The 10 cohorts span 6 cancer types, normal brain tissue (human and mouse), multiple platforms (10x Visium and ST), and substantially different scales (3 to 94 subjects). This breadth is valuable for stress-testing multi-sample integration methods across realistic heterogeneity levels.
- **H&E co-registration + pathologist annotations for every sample** is a strong inclusion criterion that many existing repositories do not enforce, making MOCHA a potentially cleaner resource for benchmark-quality evaluation.
- **The paper correctly identifies a real gap:** multi-subject SRT datasets with expert spatial annotations are scarce relative to single-sample benchmarks like DLPFC, and a well-curated resource combining multiple cohorts would serve the community.

## Weaknesses

### Fatal

- **No data access information is provided.** The paper states that MOCHA "is released in formats readily usable with Python and R" (Section 1, line 24) but gives no URL, DOI, GitHub repository, Zenodo link, data availability statement, or any mechanism for accessing the resource. For a dataset paper, this is a critical omission — the contribution cannot be verified, used, or built upon.

- **No experiments, baseline results, or validation of any kind.** The paper is positioned as a resource "for developing and evaluating multi-sample SRT methods" (Abstract, line 10) and "for training and evaluation" (Section 1, line 20), yet it contains zero experimental results. No method is run on MOCHA; no clustering metrics (ARI, NMI, etc.) are reported; no comparison with single-sample analysis is provided. The paper does not demonstrate that the resource actually works as claimed or that the annotations are usable for evaluation. A dataset paper that claims to support evaluation but provides no evaluation data is fundamentally incomplete.

### Major

- **No quantitative comparison to existing repositories.** The paper acknowledges SORC, Aquila, SODB, STOmicsDB, and SpatialDB (Section 1, lines 16-18) but provides no comparison of MOCHA's coverage (datasets, subjects, samples, annotation types, platforms) against these resources. The claimed value-add is asserted rather than demonstrated.

- **Curation pipeline and harmonization are not described.** The paper does not specify what file format conversions were performed, what common gene set was used for concatenation, what quality control was applied, whether any samples/spots were excluded, or how annotation schemas were harmonized across cohorts (the four-category grouping is mentioned in one sentence at line 90 without detail). The curation effort is opaque, making it impossible to assess the resource's quality or reproduce its construction.

### Minor

- **Sections 3 and 4 consist largely of generic background text not specific to MOCHA.** Section 3 describes standard preprocessing pipelines (scater, scran, Seurat, Harmony, Crescendo) without stating what was actually applied to MOCHA data or with what parameters. Section 4 summarizes three multi-sample methods (BayeSMART, BASS, STAGATE) in a generic table with no MOCHA-specific results. These sections occupy approximately half the paper body but contribute no MOCHA-specific information.

- **Some datasets weaken the "multi-subject" framing.** MOB.ST has only 1 subject (though with 12 samples, it is multi-sample but not multi-subject). DLPFC (3 subjects, 12 samples) is already a widely used public benchmark, so its inclusion adds limited novelty. BC.TNBC uses the older ST technology with substantially lower resolution than 10x Visium, and the paper does not discuss how platform differences affect the combined resource's usability.

- **No Discussion or Limitations section.** The paper ends after Section 4 with no discussion of caveats: annotation heterogeneity across cohorts, platform differences, small sample sizes in some cohorts, potential selection bias, or recommended use cases.

### Trivial

None.

## Nice-to-Haves

1. Provide a data availability URL/DOI and license information.
2. Run and report baseline results from at least 2–3 standard methods (BASS, STAGATE, BayeSMART) on the MOCHA cohorts, reporting clustering metrics (ARI, NMI) against the pathologist annotations.
3. Describe the curation pipeline in detail: format conversions, common gene set, QC procedures, annotation standardization.
4. Include a table quantitatively comparing MOCHA's coverage against existing repositories (SORC, Aquila, SODB, STOmicsDB, SpatialDB).
5. Add a PCA/UMAP visualization colored by cohort to characterize batch effects.
6. Add a Discussion/Limitations section addressing annotation heterogeneity, platform differences, and usage caveats.

## Removed Points

- "No new annotations — curation is purely selection and organization": removed because the paper presents itself as a curated resource aggregating existing data, consistent with its stated goal. It never claims to produce new pathologist annotations. The substantive concern (opaque curation pipeline) is retained in the Major weaknesses above.
- Various section-by-section formatting/style observations: removed as they do not affect the core assessment.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The paper identifies a worthwhile gap, but as written it is an extended abstract rather than a complete conference submission. The two fatal issues — no data access and no experimental validation — must be resolved before the resource can be evaluated. The authors should (1) provide access to the curated data, (2) run and report baseline results from standard multi-sample SRT methods demonstrating that the resource works, (3) describe the curation pipeline transparently, and (4) quantitatively compare coverage against existing repositories.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>