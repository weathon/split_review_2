## Summary

MOCHA presents a curated collection of 10 multi-subject spatially resolved transcriptomics (SRT) datasets, each paired with expert pathologist annotations, standardized data formats, and guidance on preprocessing and batch correction. The resource aims to address the gap in benchmark datasets for evaluating multi-sample spatial domain identification methods.

## Strengths

- **Addresses a genuine gap**: Multi-subject SRT datasets with expert-derived spatial domain annotations are indeed scarce, and the paper clearly motivates why this limits method development for cohort-level studies. The curation of 10 cohorts spanning diverse tissues (breast cancer, colorectal cancer, kidney, lung, cortex, olfactory bulb), multiple platforms (10x Visium and ST), and varying scales (3–94 subjects) provides meaningful breadth.
- **Practical accessibility**: MOCHA is released in formats compatible with both Python and R ecosystems, and the paper provides concrete preprocessing guidance (normalization strategies, feature selection, batch correction via Harmony and Crescendo) that researchers can follow directly.

## Weaknesses

### Fatal

None.

### Major

- **No benchmarking experiments whatsoever**: This is the most significant shortcoming. A dataset/benchmark paper must demonstrate the resource's utility by actually running existing methods and revealing insights. The paper names three multi-sample clustering methods (BayeSMART, BASS, STAGATE) in Table 2 and describes them, but never evaluates any of them on MOCHA. Without benchmarking results—comparing methods across cohorts, demonstrating how annotation quality affects evaluation, or revealing which methods succeed/fail in which settings—it is impossible to assess whether MOCHA actually enables the "developing and evaluating multi-sample SRT methods" it claims to support. This is a fundamental omission for a resource paper.
- **Opaque annotation provenance and quality control**: The paper states that samples are "accompanied by spatial domain labels produced by an expert pathologist" but provides no detail on whether these annotations were generated de novo by the authors or extracted from original publications. There is no information on inter-annotator agreement, annotation consistency across cohorts, or any quality control procedures. Given that the expert annotations are the core differentiating value of MOCHA relative to existing repositories (SODB, STOmicsDB, etc.), this lack of detail undermines the central claim.
- **Insufficient differentiation from existing repositories**: The paper lists SODB, STOmicsDB, SpatialDB, SORC, and Aquila as existing resources but does not systematically compare MOCHA against them in terms of content, coverage, or unique value. The implicit claim is that expert pathologist annotations set MOCHA apart, but without demonstrating annotation quality and consistency, this advantage is asserted rather than evidenced.

### Minor

- **Sections 3 and 4 are review material, not contributions**: The preprocessing pipeline discussion (Section 3) and the method summary (Section 4) read as textbook-style overviews rather than novel analysis. They do not offer new observations about multi-sample challenges, nor do they synthesize findings from applying these methods to MOCHA data. These sections occupy substantial paper real estate without advancing the contribution.
- **Several cohorts are very small for multi-sample evaluation**: KC.TLS (3 samples, 3 subjects), LC.TLS (5 samples, 5 subjects), and MOB (12 samples but 1 subject) may be too small to meaningfully assess multi-sample integration methods. The paper does not discuss minimum cohort size requirements or acknowledge limitations of small-sample cohorts.
- **Missing discussion of annotation granularity and grouping**: The paper briefly mentions that cancer annotations can be grouped into four broad categories (immune, stroma, tumor, normal) but does not present the full annotation vocabulary, show example annotations overlaid on tissue images, or discuss how annotation granularity affects benchmarking difficulty.

### Trivial

None beyond parser-level issues.

## Nice-to-Haves

- A benchmark table comparing at least two methods (e.g., BASS vs. STAGATE) across several MOCHA cohorts with quantitative metrics (ARI, NMI) would enormously strengthen the paper.
- Visual examples of pathologist annotations overlaid on H&E images for representative samples from different cohorts.
- A comparison table showing what MOCHA provides relative to existing SRT repositories.

## Novel Insights

None beyond the paper's own contributions. The preprocessing and method review sections consolidate existing knowledge but do not offer new observations or insights derived from working with the curated data.

## Suggestions

1. **Run baseline experiments**: Apply at least BASS and STAGATE to 3–4 MOCHA cohorts, report quantitative clustering metrics (ARI, NMI) against the pathologist annotations, and discuss which method characteristics lead to better performance in which settings. This single addition would transform the paper from a data description into a genuine benchmark contribution.
2. **Detail the annotation protocol**: Describe who annotated each cohort, whether annotations were sourced from original publications or generated by the authors' pathologist(s), the annotation workflow, and any inter-rater reliability assessments.
3. **Sharpen differentiation**: Add a concrete comparison table showing MOCHA versus SODB, STOmicsDB, and SORC on dimensions like number of multi-subject cohorts, presence of expert annotations, availability of matched H&E images, and data format compatibility.

## Score and Decision

The paper identifies a legitimate need and the curation effort has value, but the contribution is significantly weakened by the absence of any benchmarking experiments and insufficient detail on the annotation process that constitutes its main differentiator. As submitted, MOCHA is closer to a data descriptor than a research contribution to a machine learning venue. The method review sections do not compensate for these gaps.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>