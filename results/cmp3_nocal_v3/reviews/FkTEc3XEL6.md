Now I have all the cross-verification I need. Every weakness has been checked against the actual paper text. Let me produce the final consolidated review.

---

## Summary

MOCHA proposes a curated resource of 10 multi-subject spatial transcriptomics cohorts (spanning breast, colorectal, kidney, lung, brain, and olfactory bulb tissues from human and mouse) with pathologist-annotated spatial domain labels. The paper describes the cohort selection, lists basic molecular characteristics, and outlines generic preprocessing pipelines and existing multi-sample clustering methods.

## Strengths

- **Well-motivated problem.** The paper correctly identifies (lines 14–18) that multi-sample SRT method evaluation is hampered by a lack of curated, multi-subject datasets with ground-truth annotations — a genuine bottleneck in the field.

- **Reasonable cohort coverage.** The 10 cohorts in Table 1 (lines 34–45) span multiple tissue types, two technology platforms (10x Visium, ST), both human and mouse samples, and a useful range of cohort sizes (3–94 subjects). The selection covers most major publicly available SRT datasets of this type.

## Weaknesses

### Fatal

1. **No demonstration that the resource is usable or useful.** This is a dataset/benchmark resource paper, yet it contains zero experiments. There are no benchmark results, no ARI/NMI evaluations of any multi-sample method against the claimed annotations, no comparison showing that MOCHA enables evaluations that existing resources do not. The abstract claims "protocols for handling batch effects" — but Section 3 describes only standard existing tools (scater, scran, Seurat, scanpy, Harmony, Crescendo) with nothing MOCHA-specific. A reader cannot assess whether this resource has any utility because the paper never uses it for anything. For a dataset contribution, this is a structural failure — the resource's value is asserted, not evidenced.

2. **No information on how to access or use the dataset.** A dataset paper must tell readers where the data lives, in what format, and how to load it. The paper provides: no hosting URL, no repository name, no file format (h5ad? Seurat object? zarr?), no download procedure, no code snippet, no license or terms of use. The vague statement "released in formats readily usable with Python and R" (line 24) does not constitute access information. Without this, the paper's primary function as a resource announcement is unfulfilled.

3. **The main body is substantively incomplete.** Excluding figure captions and tables, the paper contains approximately 55–60 lines of prose. Sections 3 (Pre-processing and batch effect correction, lines 57–65) and 4 (Multi-sample spatial clustering methods, lines 76–90) describe only standard existing tools and methods — they contain zero MOCHA-specific content and read as generic tutorial material. The core contribution — the curated data, annotations, schema, format, organization — is essentially undiscussed in the main text beyond Table 1, Figure 1, and the mention of four broad annotation categories (line 90) deferred to Supplementary Material.

### Major

4. **No validation of the expert annotations.** The paper's central value proposition hinges on pathologist-delineated spatial domain labels (line 10, 24, 28, 90). Yet it provides: no information on how many pathologists generated the annotations, no inter-annotator agreement metrics (kappa, F1, or any reliability measure), no annotation guidelines, no verification protocol, no resolution or granularity per sample. Without this, the claim of "expert-derived annotations" (line 10) is unverifiable. Existing repositories (SORC, Aquila) and the original publications for many of these datasets already contain annotations; MOCHA cannot differentiate itself without demonstrating annotation quality.

5. **No comparison with or differentiation from existing resources.** The Introduction (line 16) acknowledges that "several repositories have been developed" (SORC, Aquila, SODB, STOmicsDB, SpatialDB) and claims that "multi-subject datasets with expert-generated spatial annotations remain limited." Yet the paper never directly compares MOCHA to these resources in a table or prose — what annotations does each provide? What cohorts overlap? What is uniquely contributed? Without this, the claimed gap is unsubstantiated, and the reader cannot assess whether MOCHA fills a genuine need or duplicates existing infrastructure.

### Minor

6. **The annotation schema is absent from the main text.** Line 90 mentions that annotations can be grouped into four broad categories (immune, stroma, tumor, normal) but refers to the Supplementary Material for the mapping. Given that each of the 10 cohorts has different domain labels, a main-text table showing how original labels map to these categories is essential for understanding the resource. The Supplementary Material may contain this, but the main text should stand alone.

### Trivial

None.

## Nice-to-Haves

- Run 2–3 multi-sample methods (e.g., BASS, STAGATE, BayeSMART) on MOCHA cohorts using the pathologist annotations as ground truth and report ARI/NMI. This single addition would transform the paper from a dataset announcement into a usable benchmark.
- Validate a subset of annotations with inter-annotator agreement statistics.
- Add a "Data Access and Format" subsection specifying hosting platform, file format, a code snippet for loading a sample, and license terms.
- Add a comparison table showing what SORC/Aquila/SODB provide vs. what MOCHA adds.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"The note about 'Rest of paper (reference and Appendix) is removed' at line 244 suggests the appendix contained additional material."** — Per policy, appendix content stripped by the parser should not be treated as absent. However, the reviewer's core point (that key information belongs in the main body) remains valid and is preserved in the weaknesses above.
- **"No benchmark results" framed as a missing-experiment criticism.** — This is actually the first Fatal weakness and is kept; the duplication is removed.

## Novel Insights

None beyond the paper's own contributions. The review surfaces structural completeness criteria for dataset/benchmark papers but does not identify any insight about the science itself that the paper missed.

## Suggestions

1. Add benchmark experiments using 2–3 multi-sample methods on MOCHA data with the pathologist annotations as ground truth.
2. Add inter-annotator agreement statistics for at least a subset of the annotations.
3. Add a "Data Access and Format" subsection specifying hosting platform, file format (e.g., h5ad), download URL, license, and a code snippet.
4. Add a comparison table with existing resources (SORC, Aquila, SODB, STOmicsDB, SpatialDB) showing what annotations and cohorts each provides.
5. Add a main-text table mapping each cohort's original domain labels to the four broad annotation categories.

## Score and Decision

The paper identifies a genuine need and selects reasonable cohorts, but it does not deliver a complete research contribution. A dataset/benchmark paper must demonstrate that the resource exists, is accessible, has validated annotations, and enables something useful. This paper provides none of these. Sections 3 and 4 are generic filler. The core claims in the abstract ("standardized data organization, efficient storage formats, protocols") are never substantiated. The paper reads as an incomplete project proposal rather than a finished research article.

MY FINAL SCORE: <score>1</score>
MY FINAL DECISION: <decision>Reject</decision>