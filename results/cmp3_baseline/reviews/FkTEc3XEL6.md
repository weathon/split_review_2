## Summary

MOCHA is a curated resource for multi-sample spatially resolved transcriptomics (SRT) research that aggregates 10 cohorts with gene expression matrices, spatial coordinates, H&E images, and expert pathologist domain annotations. The paper describes the dataset collection, preprocessing pipelines including batch effect correction methods, and provides an overview of existing multi-sample spatial clustering methods that can be evaluated using this resource.

## Strengths

- **Addresses a genuine gap in the field**: The paper correctly identifies that multi-subject SRT datasets with expert annotations are scarce, which constrains method development for cohort-level analyses. This is a real bottleneck in the community.
- **Curates diverse cohorts**: The 10 cohorts span multiple tissue types (breast cancer, colorectal cancer, kidney cancer, lung cancer, brain, mouse olfactory bulb), technologies (10x Visium, ST), and subject counts (from 3 to 94), providing useful heterogeneity for benchmarking.
- **Includes expert annotations**: Having pathologist-derived spatial domain labels across all samples is a valuable resource that many existing repositories lack, enabling supervised evaluation of domain identification methods.

## Weaknesses

### Fatal
None.

### Major
- **No quantitative analysis or benchmarking**: The paper describes the dataset and preprocessing pipelines but provides no experimental results demonstrating the utility of MOCHA. There are no benchmark comparisons of existing methods on the curated data, no evaluation of annotation quality, no analysis of batch effect severity across cohorts, and no demonstration that MOCHA enables new insights. As a resource paper, the lack of any validation experiments is a significant omission.
- **Limited novelty in curation**: The paper aggregates publicly available datasets that are already accessible through GEO, 10x Genomics, and other repositories. The primary new contribution is the expert annotations, but the paper does not describe the annotation process in sufficient detail (e.g., number of pathologists, inter-annotator agreement, annotation guidelines). Without this, it is unclear how reliable or reproducible the annotations are.
- **No standardized evaluation protocol**: While the paper claims to provide "standardized data organization" and "protocols for handling batch effects," it does not define concrete evaluation metrics, train/test splits, or reproducible benchmarking pipelines that would allow fair comparison of methods. The paper reads more as a survey of existing methods and preprocessing steps than as a usable resource.

### Minor
- **The paper is very short and lacks depth**: At approximately 4 pages of content (excluding references), the paper provides only high-level descriptions. Key details about data formats, download links, annotation schemas, and usage examples are missing or relegated to a removed appendix.
- **Table 2 is incomplete**: Only three multi-sample methods are listed (BayeSMART, BASS, STAGATE), but the paper mentions others (e.g., iIMPACT, BayesSpace) in the introduction. A more comprehensive survey would strengthen the paper's value as a resource.
- **Figure 1 has a typo**: "DLPC_10x" should be "DLPFC_10x" and "TL8" appears instead of "TLS" in several cohort names.

### Trivial
- The paper states "Rest of paper (reference and Appendix) is removed" at the end, suggesting the submitted version is incomplete.

## Nice-to-Haves

- A companion website or GitHub repository with code to reproduce the preprocessing pipelines and download the data in standardized formats.
- A small-scale benchmarking experiment (e.g., comparing BASS, STAGATE, and BayeSMART on 2-3 cohorts) to demonstrate the value of the expert annotations for evaluation.
- Analysis of inter-annotator agreement or annotation confidence scores.

## Novel Insights

None beyond the paper's own contributions. The paper does not present new methodological insights or unexpected findings from the data.

## Suggestions

- Add a benchmarking section with quantitative results (e.g., ARI, NMI, or F1 scores) comparing existing multi-sample methods on MOCHA cohorts, using the expert annotations as ground truth.
- Provide detailed documentation of the annotation process: number of pathologists, annotation guidelines, inter-rater reliability, and how ambiguous regions were handled.
- Define a standardized evaluation protocol with clear train/validation/test splits, evaluation metrics, and a leaderboard or reference implementation to facilitate fair comparisons.
- Include a table or figure showing the distribution of domain labels (immune, stroma, tumor, normal) across cohorts to help users understand the annotation landscape.

## Score and Decision

The paper addresses a real need in the SRT community, but in its current form it is more of a proposal or position paper than a complete resource contribution. The lack of any experimental validation, benchmarking, or detailed annotation methodology makes it difficult to assess the quality and utility of the curated data. The paper would benefit substantially from adding quantitative results and a reproducible evaluation framework.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>