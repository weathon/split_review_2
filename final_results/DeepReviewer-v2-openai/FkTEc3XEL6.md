## Summary
# Final Review Report

## Summary

This manuscript introduces MOCHA (Multi-sample Omics Cohorts with Human Annotation), a curated resource of 10 spatially resolved transcriptomics (SRT) datasets spanning 166 subjects and 201 tissue sections, each paired with expert pathologist-annotated spatial domain labels. The datasets cover diverse tissue types (breast, colorectal, kidney, lung, brain, olfactory bulb), disease contexts (multiple cancer subtypes and healthy tissue), species (human and mouse), and two technological platforms (10x Genomics Visium and ST). The paper describes the curation process, provides cohort-level summary statistics, and reviews standard preprocessing pipelines and multi-sample clustering methods relevant to the resource.

The core strength of MOCHA is its focus on multi-subject cohorts with expert annotations, a combination that is currently scarce in public SRT repositories and is critical for benchmarking multi-sample integration methods. The paper is clearly written and the dataset selection is well-motivated. However, the manuscript in its current form has several significant gaps: (1) no data access mechanism is provided, (2) Sections 3 and 4 are generic literature reviews rather than MOCHA-specific content, (3) the paper contains no benchmarking experiments or evaluation results despite being positioned as a resource for algorithm development and evaluation, (4) there is no Conclusion/Discussion section, and (5) several typos and formatting issues reduce presentation quality. The resource has potential value to the SRT community, but the paper requires substantial revision to deliver on its stated promises.

## Strengths
1. **Addresses a genuine gap in SRT resources.** The lack of multi-subject datasets with expert pathologist annotations is a real bottleneck for developing and evaluating multi-sample spatial domain identification methods. MOCHA's focus on curating such datasets with consistent format standards is a timely and potentially valuable contribution to the spatial transcriptomics community.

2. **Diverse cohort composition across tissues, diseases, species, and platforms.** The 10 cohorts include cancer subtypes (breast, colorectal, kidney, lung, renal cell), healthy brain tissue (DLPFC), and mouse olfactory bulb, spanning two technological platforms (10x Visium and ST). This diversity enables evaluation of method generalizability across biological contexts and technical modalities.

3. **Clear curation criteria and reproducible selection methodology.** The authors specify clear inclusion criteria (expression count matrix, spatial coordinates, pathologist annotations from H&E) and describe their search across multiple public repositories (10x Genomics, GEO, Spatial Research). Referencing the STImage-1K4M methodology provides a traceable curation framework.

4. **Integration of H&E images with molecular and spatial data.** Providing co-registered high-resolution H&E images alongside gene expression and spatial coordinates enables multimodal analysis, which is increasingly important for methods that combine histological and molecular information (e.g., iIMPACT, BayeSMART).

5. **Standardized data formats for Python and R ecosystems.** The stated goal of releasing data in formats compatible with both AnnData (Python) and Seurat (R) ecosystems is well-aligned with community practices and lowers the barrier for adoption.

## Weaknesses
### Major Weaknesses

**W1. No data access mechanism provided (Severity: Critical)**
The manuscript states that 'MOCHA is released in formats readily usable with Python and R and distributed for integration into existing pipelines' but provides no URL, GitHub repository, Zenodo DOI, or any other method to access the resource. For a paper whose entire contribution is a data resource, this omission is fundamental — reviewers and readers cannot evaluate, use, or verify the claimed contribution. *Evidence: Page 1 — Abstract and Page 1-2 — Introduction paragraph 4.*
**Fix:** Provide a public repository URL and/or DOI, along with a data availability statement in the manuscript. Include details on file formats (AnnData, Seurat objects), expected file sizes, and any access restrictions.

**W2. No benchmarking or evaluation results (Severity: Major)**
The abstract and introduction position MOCHA as a resource 'for developing and evaluating multi-sample SRT methods,' yet the manuscript contains zero experiments applying any method to the curated data. The paper describes what the resource contains but does not demonstrate its utility for evaluation. Without at least one demonstration experiment (e.g., comparing domain identification accuracy of BASS, BayeSMART, and STAGATE on MOCHA cohorts using the expert annotations as ground truth), the central claim remains unsubstantiated. *Evidence: Page 0 — Abstract ('for developing and evaluating'), throughout Sections 2-4.*
**Fix:** Add an experimental section applying 2-3 multi-sample clustering methods to MOCHA cohorts and comparing against the expert annotations. At minimum, provide one quantitative benchmark (e.g., ARI or NMI scores) across cohorts to demonstrate the resource's evaluation utility.

**W3. Sections 3 and 4 are generic literature reviews, not MOCHA-specific content (Severity: Major)**
Section 3 ('Pre-processing and Batch Effect Correction') reads as a tutorial on standard single-cell/spatial normalization, dimensionality reduction, and batch correction tools. Section 4 ('Multi-sample Spatial Clustering Methods') is a brief survey of three existing methods. Neither section describes what MOCHA specifically provides, recommends, or implements. Approximately 50% of the main text is background material that does not advance the paper's contribution. *Evidence: Page 1 — Section 3 paragraphs (lines 36-39), Page 1 — Section 4 (lines 98-107).*
**Fix:** Replace Sections 3 and 4 with MOCHA-specific content. Section 3 should describe the exact preprocessing pipeline applied to MOCHA datasets and the format of the released data. Section 4 should either be removed (with a brief reference to Table 2 as context) or replaced with benchmarking experiments using MOCHA data.

**W4. No Conclusion/Discussion section (Severity: Major)**
The paper ends abruptly after Section 4, followed by empty Author Contributions and Acknowledgments placeholders and then references. There is no synthesis of the contribution, discussion of limitations, or mention of future work. This is a structural omission for any academic paper. *Evidence: Page 1 — lines 108-115.*
**Fix:** Add a Conclusion section with: (1) summary of the resource and its intended use, (2) known limitations (cohort composition bias toward cancer, annotation variability across sources, platform coverage), (3) future directions (planned expansions, community contribution model, integration with additional data modalities).

**W5. Annotation provenance and quality control are not described (Severity: Major)**
The paper's core differentiating feature is 'expert pathologist annotations,' yet no details are provided about annotation protocols, number of annotators per dataset, inter-rater reliability, or quality control measures. Without this information, the reliability of the ground-truth labels — and thus the value of MOCHA as a benchmark resource — cannot be assessed. *Evidence: Page 1 — Section 2 (lines 15-16).*
**Fix:** Add a supplementary section describing the annotation provenance for each cohort. Include: number of pathologists involved, annotation guidelines, whether labels were independently verified, and a summary of annotation class distributions per cohort.

### Minor Weaknesses

**W6. Missing metadata in Table 1 and cohort description.** Table 1 lacks spatial resolution information (spot size), annotation class counts, and per-cohort spot/gene ranges (partially provided in Figure 1 but not in the table). Adding a metadata column for 'Annotation Classes' would improve usability. *Evidence: Page 1 — Table 1.*

**W7. Typographical errors.** 'scampy' (line 36) should be 'scanpy' (the correct name of the Python framework). Figure 2 caption reads 'AA standard pipeline' — should be 'A standard pipeline'. These errors reduce presentation quality. *Evidence: Page 1 — line 36 (scampy), line 97 (AA standard).*

**W8. Empty placeholder sections.** The Author Contributions and Acknowledgments sections are empty. These should either be removed or filled with standard text. *Evidence: Page 1 — lines 110-115.*

**W9. Claim-evidence mismatch in abstract.** The abstract states MOCHA provides 'protocols for handling batch effects in multi-sample integration,' but no MOCHA-specific protocols are presented — the paper only reviews existing tools. *Evidence: Page 0 — Abstract.*

**W10. Missing limitation guidance for users.** The paper does not discuss how dataset imbalance (94 subjects in BC.TNBC vs 3 in KC.TLS) or platform differences (Visium vs ST resolution) should be accounted for when using MOCHA for method evaluation. *Evidence: Page 1 — line 30.*

### Novelty & Comparison (Deferred)

External literature verification is unavailable in this run (Retrieval-Disabled Mode due to API token unavailability). Therefore, systematic novelty assessment against existing SRT repositories (SORC, Aquila, SODB, STOmicsDB, SpatialDB) and multi-sample analysis methods cannot be completed here. The authors are encouraged to provide a quantitative comparison table showing coverage of existing repositories versus MOCHA along axes such as: number of multi-subject cohorts, availability of pathologist annotations, H&E co-registration, and standardized format provision. Such a comparison would substantially strengthen the novelty positioning. Manual verification of novelty claims is required before publication.

## Score
**Final Score: 4/10**

**Rationale:** The final score prioritizes research value and novelty as primary dimensions. The MOCHA resource concept addresses a genuine gap — multi-subject SRT datasets with expert annotations are scarce and valuable for method development. However, the manuscript in its current form does not deliver on its central promises: there is no data access information (making the resource unusable), no benchmarking experiments (despite claiming evaluation utility), and approximately half the main text consists of generic literature review rather than original contribution. The absence of a Conclusion section, annotation provenance details, and comparative positioning against existing repositories further weakens the paper. These issues are fixable, but as submitted, the scientific contribution is substantially incomplete.

**Scoring breakdown:**
- Research value (concept): 6/10 — genuine gap, but unverifiable without data access
- Research value (demonstrated): 2/10 — no experiments, no data access, no validation
- Novelty strength: 4/10 — differentiated focus but no quantitative comparison to existing resources
- Methodological soundness: 3/10 — large sections are literature review; no methodological contribution
- Reproducibility: 1/10 — no data access mechanism provided
- Completeness: 3/10 — missing Conclusion, evaluation, annotation provenance

**Post-Revision Target:** 6-7/10 (achievable with data access URL, demonstration experiments, replacement of generic background with MOCHA-specific content, and addition of Conclusion and limitations).