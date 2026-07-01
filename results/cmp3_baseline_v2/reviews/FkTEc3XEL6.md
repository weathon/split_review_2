## Summary
MOCHA is a curated collection of 10 multi-subject spatially resolved transcriptomics (SRT) datasets, each paired with expert pathologist annotations of spatial domains. The paper describes the datasets, standard preprocessing pipelines, batch effect correction strategies, and a brief summary of existing multi-sample clustering methods. The stated goal is to provide a resource for developing and evaluating multi-sample SRT methods.

## Strengths
- **Addresses a genuine gap**: Multi-sample SRT datasets with expert annotations are scarce, and the paper correctly identifies this as a bottleneck for method development.
- **Diverse coverage**: The 10 cohorts span multiple tissue types (breast, colorectal, kidney, lung, brain, mouse olfactory bulb), disease contexts, and two technology platforms (10x Visium and ST), offering useful heterogeneity.
- **Clear motivation and structure**: The paper is well-organized, and the need for multi-sample benchmarks is convincingly argued.

## Weaknesses
### Fatal
- **No baseline experiments or benchmarks**: The paper provides no experimental results demonstrating how the dataset can be used to evaluate multi-sample methods. For a dataset paper at a top venue, this is a critical omission—the utility of the resource is asserted but not validated.
- **Data and code availability not stated**: The paper does not specify where the curated data, annotations, or preprocessing code can be accessed. Without a repository or DOI, the resource is not reproducible or usable by the community, which undermines the entire contribution.

### Major
- **Annotation quality is unverified**: The paper claims “expert pathologist” annotations for every sample, but provides no details on annotation protocol, inter-rater reliability, quality control, or consistency across cohorts. This is essential for a resource intended as a gold standard for evaluation.
- **Lack of depth**: The paper is very short (≈4 pages of content) and reads more like a technical report or data announcement than a full research paper. The description of preprocessing and batch correction is generic and not specific to MOCHA. The summary of multi-sample methods (Table 2) lists only three methods, omitting many relevant approaches (e.g., PRECAST, SpaGCN, GraphST), and provides no comparative analysis.
- **No discussion of limitations**: The paper does not address potential issues such as batch effects within cohorts, annotation biases, platform differences, or the representativeness of the selected cohorts.

### Minor
- **Figure captions contain OCR artifacts** (e.g., “AA standard pipeline” in Figure 2 caption).
- **Duplicate references** (Ståhl & et al., 2016 appears twice in the reference list).

### Trivial
- Some references are incomplete (e.g., “Ståhl & et al., 2016” format).

## Nice-to-Haves
- Include baseline results (e.g., using BASS, STAGATE, or BayeSMART) on a subset of MOCHA to demonstrate how the dataset can be used for evaluation.
- Provide a public GitHub repository or Zenodo link with the curated data, annotations, and preprocessing scripts.
- Add an analysis of annotation consistency (e.g., inter-rater agreement or comparison with automated methods).

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Add a dedicated experiments section that uses MOCHA to benchmark at least two multi-sample methods, reporting metrics such as ARI or NMI against the expert annotations.
- Clearly state data availability in the main text (e.g., a link to a repository or a DOI).
- Include details on the annotation process: number of pathologists, annotation guidelines, and any quality control steps.

## Score and Decision
The paper identifies a real need and curates a potentially useful resource, but it lacks the experimental validation and data accessibility required for a dataset paper at ICLR. The absence of benchmarks and a clear data release are fatal flaws.

MY FINAL SCORE: 3
MY FINAL DECISION: Reject