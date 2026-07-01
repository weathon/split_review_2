## Summary

The paper introduces MOCHA, a curated resource of ten multi-subject spatial transcriptomics (SRT) datasets that include gene expression, spatial coordinates, H&E images, and expert pathologist domain annotations. The goal is to fill a gap in publicly available multi-sample SRT datasets with ground-truth spatial labels, thereby enabling development and evaluation of multi-sample spatial domain identification and batch-correction methods. The paper also outlines preprocessing pipelines and briefly surveys existing multi-sample clustering methods.

## Strengths

- **Identifies a genuine need**: Multi-sample SRT datasets with expert-derived annotations are scarce, and the paper correctly highlights this bottleneck for method development in cohort-level spatial analyses. The curation of ten diverse cohorts across multiple tissues, platforms (10x Visium, ST), and disease contexts provides broad coverage.
- **Combines molecular, spatial, and histological data with labels**: Each sample pairs molecular profiles, spatial coordinates, and H&E images with pathologist-generated domain labels, which is a valuable combination for supervised benchmarking and representation learning.
- **Provides a standardised organisational framework**: The paper mentions standardised data organisation and efficient storage formats, which are critical for reproducibility and ease of use in large-scale multi-sample studies.

## Weaknesses

### Fatal
- **No demonstration of utility**: The paper claims MOCHA is for “training and evaluation of multi-sample SRT methods” but provides zero experiments, baselines, or usage examples. Without any benchmark or even a simple analysis (e.g., annotation consistency, batch-effect visualisation, or domain identification by an existing method), the resource’s value and quality remain unsubstantiated. A dataset paper that aims to serve the community must include at least a proof-of-concept or baseline evaluation.
- **No access to the resource**: The paper does not provide a URL, DOI, or repository link for MOCHA. A dataset described without pointing to a downloadable resource cannot be used or verified, which fundamentally undermines the contribution.

### Major
- **Insufficient detail on curation and annotations**: It is unclear whether the pathologist annotations were newly generated or merely re-used from the original publications. The curation process is described only at a high level (searching repositories and checking criteria). No information is given about annotation protocols, inter-annotator agreement, or how boundaries (e.g., between tumour and stroma) were defined. The claim that annotations can be grouped into “immune, stroma, tumor, and normal” is stated but not validated or mapped per dataset.
- **Lack of comparison with existing resources**: The paper lists SORC, Aquila, SODB, STOmicsDB, and SpatialDB but does not systematically compare MOCHA against them. What distinguishes MOCHA (e.g., multi-subject structure, expert labels) is asserted but not quantified. A table contrasting features, number of multi-subject cohorts, annotation availability, and supported tasks would help justify the novelty.
- **Superficial description of data structure**: The “standardised data organisation” and “efficient storage formats” are mentioned but never concretely specified. For example, are files in HDF5, AnnData, or another format? How are annotations encoded? Without this information, users cannot assess the ease of integration into their pipelines.
- **Preprocessing section reads as generic tutorial**: Section 3 describes well-known normalisation, dimensionality reduction, and batch-correction methods without indicating which steps were actually applied to MOCHA data or which protocols are recommended for future users. The resource is supposed to come with “protocols,” but none are delivered in the paper.

### Minor
- **Inconsistent naming in figures**: Figure 1 labels cohorts with underscores and slight misspellings (e.g., “DLPC_10x” instead of “DLPFC_10x”, “RCC_TL8_10x” instead of “RCC.TLS_10x”), which may cause confusion even if resulting from OCR.
- **Overly brief methods survey**: Table 2 lists only three multi-sample methods (BayeSMART, BASS, STAGATE) with minimal comparison; the selection criteria are not justified.

### Trivial
- Redundant references (e.g., Ståhl 2016 appears twice in the reference list).

## Nice-to-Haves
- Provide a downloadable link to the full dataset and a clear data dictionary.
- Include a baseline benchmark by running a few multi-sample spatial clustering methods (e.g., BASS, STAGATE) on MOCHA and reporting standard metrics (e.g., ARI, NMI) per cohort to demonstrate reproducibility and utility.
- Add a comparative table of existing SRT databases (SORC, Aquila, SODB) highlighting MOCHA’s unique features (multi-subject, expert annotations, H&E co-registration).

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions
1. Provide public access to the curated data (with a DOI) and a detailed data card describing file formats, annotation schema, and recommended preprocessing steps.
2. Include a small set of reproducible experiments—e.g., domain clustering on one or two MOCHA cohorts using an existing multi-sample method—to verify that the resource works as intended and to set a reference baseline.
3. Clarify whether annotations are newly generated or repurposed, and if repurposed, cite the original annotation sources. If new, describe the annotation protocol and inter-rater reliability.

## Score and Decision

Given the absence of experimental validation and the lack of a downloadable resource, the paper does not currently fulfill the requirements of a usable dataset contribution. The idea is timely, but the execution is incomplete.

MY FINAL SCORE: 3.0<score>3.0</score>
MY FINAL DECISION: Reject<decision>Reject</decision>