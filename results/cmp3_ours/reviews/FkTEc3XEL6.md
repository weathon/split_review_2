Now I have all the information I need. Let me write the final, authoritative review.

## Summary

The paper introduces MOCHA, a curated collection of 10 publicly available spatial transcriptomics (SRT) datasets spanning multiple cancer types and normal tissues, with expert pathologist annotations provided for each sample. The stated goal is to provide a resource for developing and evaluating multi-sample SRT methods, filling what is genuinely a gap in the availability of multi-subject SRT data with expert spatial annotations.

## Strengths

1. **Correctly identifies a genuine bottleneck in the field.** As stated in the Introduction (lines 16–17), multi-subject SRT datasets with expert spatial annotations are indeed scarce, and this scarcity constrains method development for multi-sample integration. This is a well-motivated target for a resource paper.

2. **Diverse and useful cohort selection.** The 10 cohorts (Table 1, lines 34–45) span multiple cancer types (breast, colorectal, kidney, lung, renal cell), two normal tissues, human and mouse, and two technology platforms (10x Visium, ST). BC.TNBC with 94 subjects is notably large for SRT and offers meaningful scale for benchmarking. The tabulation of cohort metadata (tissue, technology, subjects, samples) is clear and directly useful.

3. **Figure 1 provides basic molecular characterization** (spot counts, gene counts, sparsity) across cohorts, giving prospective users a quick sense of data scale and sparsity.

## Weaknesses

### Fatal
None.

### Major

1. **No experiments or validation demonstrating that the resource serves its stated purpose.** The paper claims (Abstract, line 10) that MOCHA is "a curated resource for developing and evaluating multi-sample SRT methods," but it performs no experiments to substantiate this. There are no baseline method runs, no benchmarking results, no clustering metrics (ARI, NMI, etc.), no assessment of annotation quality or utility. The paper has no Results section, no Experiments section, and no Conclusion. The paper's own Table 2 lists three existing multi-sample methods (BayeSMART, BASS, STAGATE), yet none are ever applied to the curated data. For a resource paper at a venue like ICLR, the minimal expectation is to demonstrate that the data enables meaningful evaluation — e.g., running 2–3 existing methods and reporting performance against the annotations. Without this, the paper describes what the resource could enable rather than showing that it does.

2. **Annotation methodology is completely unspecified, making the core asset unverifiable.** The paper's key value-add over existing public datasets is "expert pathologist annotations" (Abstract, line 10; Section 2, line 28). Yet zero details are provided about: how many pathologists were involved, their qualifications, the annotation protocol (manual delineation, semi-automated, consensus), annotation resolution (spot-level or region-level), whether inter-annotator reliability was assessed, whether existing annotations were adapted or created de novo, or whether annotations were validated by a second expert. Without this information, prospective users cannot assess the quality or trustworthiness of the resource's central asset. This is a critical omission for any dataset paper that claims expert-derived labels as its differentiator.

3. **The paper is structurally incomplete.** It has no Conclusion, Discussion, or Limitations section — it ends at Section 4 and jumps directly to References. Section 3 (Pre-processing, lines 57–65) describes generic textbook-level methodology (TMM, RLE, PCA, t-SNE, Harmony) without specifying what preprocessing was actually applied to the MOCHA cohorts or providing the pipeline code. This section reads as background knowledge, not as a description of what was done. Section 4 lists three multi-sample methods in a table with one sentence each and provides no analysis or user guidance. The total substantive content is roughly 3–4 pages, which is underdeveloped for a conference submission.

### Minor

4. **No data access information provided in the paper.** The abstract (lines 23–24) states that "MOCHA is released in formats readily usable with Python and R," but the paper contains no URL, DOI, repository link, download instructions, or license information. For a dataset paper, this information is necessary for the resource to be usable. This is partly mitigated if the data is accessible via the cited individual publications, but the curated, standardized release that is the paper's contribution cannot be accessed from the paper itself.

5. **The four-domain grouping (immune, stroma, tumor, normal) is mentioned but not substantiated.** Section 4 (line 90) states that annotations can be grouped into four broad categories and refers to "Supplementary Material" for details. The supplementary material is not available in this submission. Moreover, it is unclear how this grouping applies to the two normal-tissue cohorts (DLPFC, MOB) that contain no tumor or immune microenvironments in the same sense. The paper acknowledges "a majority of the cancer studies" but does not clarify the annotation schema for the non-cancer datasets.

6. **MOB is single-subject.** The MOB cohort (Table 1, line 44) has 1 subject and 12 samples, which is multi-sample but not multi-subject. The paper should clarify whether this cohort is included for multi-sample (within-subject) evaluation and provide a rationale, or qualify the "multi-subject" framing.

### Trivial
None.

## Nice-to-Haves

- Running 2–3 existing multi-sample methods on a subset of MOCHA cohorts and reporting standard clustering metrics (ARI, NMI) against the expert annotations.
- Documenting the annotation protocol in full detail (number of pathologists, qualifications, consensus process, annotation resolution, inter-annotator agreement).
- Providing the dataset access URL, format specification, and basic loading/processing code.
- Adding a Conclusion or Discussion section covering limitations (cohort size imbalance, platform heterogeneity, annotation resolution limits).
- Adding a PRISMA-style flow diagram and search terms for the curation process.

## Removed Points

These points were raised in the input review but are removed per the filtering rules:

- **Figure caption typos ("TL8" for "TLS", "DLPC" for "DLPFC"):** Removed per the hard rule on typos/formatting artifacts (parser issues in extracted text, not author errors in the original submission).
- **Missing ethical considerations / IRB approval:** The parser strips appendix content; such discussion may exist in the original submission's supplementary material and cannot be verified.
- **No dataset splits or evaluation protocols:** This is a nice-to-have for a resource paper; the absence does not undermine the curation work itself.
- **Preprocessing section is a "textbook summary":** This criticism is subsumed under Major weakness #3 (structural incompleteness).

## Novel Insights

None beyond the paper's own contributions. The input reviews did not surface any perspective that the paper itself does not already suggest (i.e., that a curated multi-subject SRT resource with annotations would be valuable).

## Suggestions

1. **Most critical:** Add a benchmarking section that runs 2–3 existing multi-sample methods (BASS, STAGATE, BayeSMART) on a representative subset of the MOCHA cohorts and reports clustering accuracy (ARI, NMI) against the expert annotations. This is the single change that would transform the paper from an announcement into a demonstrated contribution.
2. Document the annotation protocol in full — pathologist qualifications, numbers, annotation resolution, consensus process, and inter-annotator agreement statistics.
3. Provide a URL/DOI for the curated dataset, along with format specifications and basic loading code.
4. Add Conclusion and Limitations sections discussing cohort size imbalance, platform heterogeneity, and annotation resolution limits.
5. Clarify the handling of non-cancer cohorts (DLPFC, MOB) with respect to the four-domain grouping, and add a rationale for including the single-subject MOB dataset.

## Score and Decision

**Bracket (Round 1):** 1.5 – 2.5. Based on calibration, anchor papers serving as dataset/benchmark contributions with actual experiments (KidSat: 2.00, MCIL: 2.33) were scored in the low-reject range. MOCHA is even less complete — it lacks any experimental validation — placing it at or below these anchors.

**Calibration anchors used (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| KidSat (JEmNgjuQHU) | 2.00 | R1 | Dataset+benchmark with experiments and open code; scored 2.00 reject. MOCHA has no experiments, less complete. |
| MCIL benchmark (gNoqEdT2wO) | 2.33 | R2 | Benchmark dataset with model evaluations and baselines; scored 2.33. MOCHA lacks any such evaluation. |
| OpenMeta (PN3i4b6NED) | 3.50 | R2 | Metagenomics benchmark with 20+ methods evaluated; scored 3.50 reject. Substantially more experiments than MOCHA. |
| STBench (oecFal31WP) | 5.75 | R1 | LLM spatio-temporal benchmark with 13 models and 60k+ QA pairs; scored 5.75. Far more extensive evaluation infrastructure. |
| DNALONGBENCH (opv67PpqLS) | 5.67 | R1 | Genomics benchmark with 5 tasks and baselines; scored 5.67. Complete with experiments and analysis. |
| GeST (8e9KpZyksc) | 4.33 | R2 | Spatial transcriptomics method with pre-training experiments; scored 4.33. Full experimental section. |

**Narrowing:** The bracket narrows to 1.5–2.5 because every anchor in the 3+ range had substantive experiments/evaluations, while MOCHA has none. KidSat at 2.00 had actual benchmarking experiments and was still rejected. MOCHA's omission of any experimental demonstration, combined with missing annotation methodology and missing data access, makes it significantly less complete. The paper identifies a real gap and provides a useful cohort description, which prevents a score of 1 (strong reject for papers with no redeeming content).

**Final score:** 2.0 — The paper identifies a genuine need and provides a reasonable curation of 10 cohorts with metadata. However, it is fundamentally incomplete as a conference submission: it lacks any experimental validation, documents none of the annotation methodology that constitutes its core value-add, provides no data access, and is structurally underdeveloped (missing conclusion, discussion, and results sections). These gaps are structural, not incremental, and would require substantial additions (experiments, annotation documentation, data release) to constitute a complete contribution.

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>