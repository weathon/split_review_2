## Summary

This paper presents MOCHA, a curated collection of multi-subject spatial transcriptomics datasets with expert pathologist annotations. It aggregates 10 cohorts (~191 samples across 166 subjects) spanning diverse tissue types, cancer contexts, and technology platforms, with standardized formats for molecular profiles, spatial coordinates, H&E images, and annotations. The paper identifies a genuine gap—multi-subject SRT resources for method development are scarce—but does not provide any evidence that MOCHA actually fills this gap.

## Strengths

- **Identifies a genuine gap** (favorability=8.40): Multi-subject SRT datasets with expert spatial annotations are indeed scarce, and standardized resources for developing multi-sample integration methods are needed.
- **Curates a reasonably comprehensive collection** (favorability=10.84): 10 cohorts spanning diverse tissue types (breast, colorectal, kidney, lung, brain, olfactory bulb), cancer contexts, and technology platforms (10x Visium and ST), with ~191 samples across 166 subjects.
- **Standardizes formats across cohorts** (favorability=8.23): Molecular profiles, spatial coordinates, H&E images, and pathologist annotations are provided in consistent formats, which could save downstream researchers substantial preprocessing effort.

## Weaknesses

### Fatal

- **No experimental evaluation whatsoever** (favorability=-4.38). The paper contains zero experiments. No baseline methods are run on MOCHA, no quantitative results are reported, and there is no demonstration that the resource enables meaningful comparison or methodological insight. For a dataset/benchmark paper, this is the decisive omission. Sections 3–4 describe existing preprocessing techniques and three methods (BayeSMART, BASS, STAGATE) but never apply any of them. The paper reads as a data listing, not a completed research contribution.

### Major

- **Central claim about annotation quality is unvalidated** (favorability=-1.61). The paper's main differentiator is that "each sample is paired with domain annotations from expert pathologists." Yet it provides: (a) no inter-rater reliability metrics, (b) no description of the annotation protocol (number of annotators, training, instructions), (c) no discussion of disagreement resolution, and (d) no analysis of annotation consistency across cohorts. This claim is asserted without evidence.

- **Tutorial content replaces dataset-specific analysis** (favorability=-2.25). Sections 3 (Pre-processing and Batch Effect Correction) and 4 (Multi-Sample Spatial Clustering Methods) are general tutorial material describing standard techniques (TMM, RLE, scater, scran, Seurat, Harmony) and three existing methods. This space should have been used for dataset-specific analysis: characterizing batch effects across MOCHA cohorts, analyzing how cohort structure serves different analytical goals, and providing a discussion of limitations. No such analysis exists.

- **No systematic comparison to existing repositories** (favorability=1.57). The introduction mentions SORC, Aquila, SODB, STOmicsDB, SpatialDB, and the paper cites STImage-1K4M, but provides no comparison table across dimensions like number of multi-subject cohorts, expert annotation availability, H&E image inclusion, and sample count. Without this, it is difficult to assess what MOCHA uniquely adds.

### Minor

- **Annotation category statistics deferred** (favorability=3.05). Per-cohort label distributions and annotation granularity are referenced only as "described in the Supplementary Material" without key summaries in the main text.

- **Cohort structure not analyzed for analytical purpose** (favorability=4.88). The dataset includes a single-subject multi-sample cohort (MOB.ST, 1 subject, 12 samples) and a multi-subject single-sample cohort (BC.TNBC, 94 subjects, 94 samples). These serve different analytical purposes, but the paper does not discuss this.

## Nice-to-Haves

- Run at least 2–3 multi-sample methods (e.g., BayeSMART, BASS, STAGATE) on MOCHA data and report domain-identification metrics against the expert annotations.
- Provide annotation validation: inter-rater agreement, per-cohort label distributions, and visual examples of annotations alongside H&E images.
- Include a comparison table against existing SRT repositories (SORC, Aquila, SODB, STOmicsDB, SpatialDB, STImage-1K4M).
- Characterize batch effects across MOCHA cohorts using standard metrics (e.g., PCA visualization by sample-of-origin).
- Add a discussion/limitations section.

## Removed Points

- Criticism about missing dataset access information (URL, DOI, GitHub) in the main text — removed per hard rule about missing appendix content (parser strips appendix; access info may exist there).
- Criticism about paper being "extremely shallow" with "four short sections" — overly subjective; merged into the existing weakness about tutorial content replacing dataset-specific analysis.
- Observations about MOB_ST having 1 subject and BC.TNBC having 1 sample/subject — these describe dataset structure but do not undermine utility; kept as a minor note about cohort analysis.
- Section-by-section editorial notes — granular comments, not standalone weaknesses.
- "Strengthening the Paper on Its Own Terms" suggestions — these are constructive suggestions, moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. The most critical need is adding experiments: running at least 2–3 baseline multi-sample methods on MOCHA and reporting metrics against the expert annotations. Without this, the paper cannot demonstrate that the resource serves its stated purpose.
2. Validate the annotation quality with inter-rater reliability metrics and a clear description of the annotation protocol.
3. Add dataset access information prominently in the main text and provide a comparison table against existing SRT repositories.

## Score and Decision

**Calibration Anchors (all rounds):**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|---|
| N/A (topically irrelevant) | P49gSPmrvN | 1.00 | R1 | No | Unrelated paper (science discourse analysis) |
| N/A (topically irrelevant) | u1cQYxRI1H | 0.50 (10.00) | R1 | No | Unrelated (illumination harmonization); score noted but irrelevant |
| BenchMol | 1JgWwOW3EN | 4.80 | R1 | Yes | Benchmark platform with extensive experiments on 23 methods; MOCHA lacks any experiments |
| DNALONGBENCH | opv67PpqLS | 5.67 | R1 | Yes | Benchmark with 5 tasks and 5 baselines run; MOCHA has no experiments |
| MFD (Fertilizer Dataset) | 6nnWnLK8If | 3.75 | R1 | Yes | Dataset paper with 7+ baseline models evaluated; MOCHA has no baselines |
| EBES | orEX9GKQAD | 4.00 | R1 | Yes | Benchmark with experiments on 7 datasets; MOCHA has no experiments |
| ivrit.ai | aOPTDchLBz | 2.50 | R2 | Yes | Pure dataset paper criticized for no baselines (favorability -2.48); MOCHA's analogous weakness is more severe (-4.38) with additional compounded weaknesses |
| LST-Bench | 2wwPG1wpsu | 2.50 | R2 | No | Benchmark with experiments on 11 models; not comparable |
| (other R2 hits) | Various | 2.50–3.00 | R2 | No | Topically unrelated |

**Round 1 bracket:** After comparing against MFD (3.75, has baselines), EBES (4.00, has experiments), and DNALONGBENCH (5.67, has experiments), MOCHA is clearly below all of them. The ivrit.ai anchor (2.50) is the closest comparison — both are pure dataset papers criticized for lacking baseline experiments. MOCHA's fatal weakness (no experiments, favorability -4.38) is more negative than ivrit.ai's analogous weakness (favorability -2.48), and MOCHA carries additional major weaknesses (no annotation validation, tutorial content replacing analysis) that ivrit.ai does not. Final bracket: **1.5–2.5**.

**Round 2 narrowing:** The narrow comparison against ivrit.ai (2.50) confirms MOCHA is worse — its single most negative weakness (-4.38) substantially undercuts even the strongest anchor weakness (-2.48), and compounded by additional major weaknesses not present in ivrit.ai. Score placed at **2.0**, between "strong reject" (1) and "reject" (3), reflecting a genuine curation effort undermined by a structurally incomplete paper.

**Final Score: 2.0** — The curation of 10 multi-subject SRT cohorts with standardized formats has genuine potential value, but the paper is fundamentally incomplete for its chosen class. A dataset resource paper must demonstrate utility (via experiments), validate its central quality claims (annotation reliability), and provide substantive dataset-specific analysis. This paper provides none of these. The weaknesses are structural, not cosmetic.

**Decision: Reject**

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>