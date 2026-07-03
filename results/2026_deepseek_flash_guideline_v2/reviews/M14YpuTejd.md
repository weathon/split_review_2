Now I have everything I need. Let me produce the final consolidated review.

---

## Summary

This paper identifies three misconceptions in the emerging online map-based motion prediction evaluation protocol: (1) inappropriate data splits cause a train-val gap because the online mapping model evaluates on the same data distribution it was trained on; (2) the limited perception range of online mapping models (typically 30×60m) cannot cover agents up to 100m away; and (3) reporting only ego-vehicle metrics masks the failure to model other agents, especially distant ones. The authors propose **OMMP-Bench** with a spatially-disjoint three-way data split (map train / motion train / motion val), stratified evaluation metrics (moving vs. static, close vs. far non-ego), and a boundary-free image-feature baseline using deformable attention. Experiments across 2 map models × 2 motion models × 4 method variants (16 combinations) validate the corrections.

## Strengths

1. **Quantifies the train-val gap with concrete mAP numbers.** Figure 3 documents that online maps on the training set achieve 87.6 mAP while maps on the validation set drop to 50.3 mAP under the default protocol. The proposed spatially-disjoint split nearly eliminates this gap (48.9 on motion train vs. 50.3 on motion val), proving the two-stage paradigm suffers from a measurable distribution shift.

2. **Empirically demonstrates the range misalignment.** Table 2 shows MapTR's mAP collapses from 0.124 (30×60m) to 0.014 (100×100m); MapTRv2-CL from 0.164 to 0.002. Table 3 shows that a GT map at the larger range improves motion prediction (minADE 0.6003 vs. 0.6154), cleanly isolating the bottleneck as online map quality at range, not motion model design.

3. **Proposes stratified evaluation metrics that reveal hidden insights.** Table 6 shows Moving agents minADE 0.6307 vs. Static 0.002 — static cases are trivial and would dominate pooled metrics. The close/far split (0.5585 vs. 0.6997) shows far-agent performance is systematically worse, directly supporting the critique that existing metrics are non-discriminative.

4. **Demonstrates that improving ego-vehicle prediction does not necessarily transfer to other agents.** Section 4.2 reports that for MapTRv2-CL+DenseTNT, the uncertainty-prediction method improves ego minADE but *increases* minADE on far non-ego agents by 4.1%, validating that ego-only evaluation can mislead conclusions about method quality.

5. **Boundary-free baseline effectively mitigates the range issue.** The image-feature baseline reduces far-agent minADE by up to 12.7% (MapTRv2-CL+HiVT: 0.6999→0.6274) and achieves best overall results (Table 4: 0.6163 vs. base 0.6375), validating that the range misalignment can be addressed without enlarging the map perception range.

## Weaknesses

### Fatal
None.

### Major

1. **Table 5 contains a clear labeling error that undermines the map-element-ablation analysis.** Rows 2 and 3 both show the configuration (Divider ✗, Boundary ✓, Ped. crossing ✗, Centerline ✗) but report different minADE values (0.6829 vs. 0.6558). Row 3 appears intended to be a centerline-only ablation (Centerline ✓ instead of Boundary ✓), which would support the text's claim that "centerlines are most helpful." However, as presented, the analysis is unverifiable. The authors must correct this and re-verify the conclusions about individual element importance. Note that the paper's core contributions (data split, metrics, range analysis) do not depend on this table, but the map-formulation analysis (Sec. 3.5) needs the fix.

### Minor

1. **The two data-split issues are not experimentally separated.** The paper identifies (i) the train-val gap from two-stage training and (ii) spatial overlap between training/validation scenes as distinct problems. Table 1 convincingly demonstrates issue (i) — Row 3 default (0.6839) vs. Row 1 proposed (0.6308). However, issue (ii) is cited from prior work (Yuan et al., 2024) and the proposed split addresses both simultaneously; there is no ablation that isolates the spatial-overlap effect alone. The paper slightly overclaims on this distinction.

2. **No variance or statistical significance reported.** All tables report point estimates without standard deviations or confidence intervals. For a benchmark that aims to replace an existing evaluation protocol, and given that many differences are on the order of 0.01 minADE, it is unclear whether reported gaps are stable across random seeds. This is standard practice in the field but limits the reliability of fine-grained comparisons.

3. **Minor formatting issue in Table 7.** Column headers read "minDE" instead of "minFDE" (line 284).

### Trivial
None beyond the above.

## Nice-to-Haves
- Report the map accuracy (mAP) of online mapping models directly on the motion training vs. motion validation sets under both protocols, to directly measure the distribution shift rather than proxying it only through downstream metrics.
- Include an ablation that varies spatial overlap while controlling for the train-val gap (or vice versa) to clarify whether the careful manual split is strictly necessary beyond any simple partitioning.
- Discuss how the findings might generalize beyond nuScenes (the only dataset with all required modalities).

## Removed Points

These points were raised by the reviewers but are removed from the main weakness list. Treat with caution — they may reflect misunderstandings or artifacts of the review process.

1. **"Boundary-free baseline is critically underspecified" (Harsh Critic #2, framed as a major weakness):** The harsh critic claimed the baseline description is too sparse to be reproducible. However, the paper states that "detailed rules of the pipeline" are in Appendix A (line 327). The parser strips appendices from all papers, so this criticism partly reflects a review-process artifact, not an author omission. The core description (Eq. 1, camera projection via intrinsics/extrinsics, Figure 7 architecture diagram) is at a level comparable to method sections in many conference papers. This is addressed as Minor weakness #3 in a softened form.

2. **"SOTA claim is unjustified" (implied by harsh critic):** Table 4 shows the baseline outperforms all compared methods (base, unc, bev) within the benchmark's specific setup. "SOTA" is qualified by the benchmark scope. This is not a real weakness.

3. **"Use of original code vs. re-implementation unclear" (harsh critic):** This is a generic reproducibility nitpick about trivial implementation details. Removed per hard rules.

4. **Strength Finder's generic/superficial strengths:** Several claimed strengths (e.g., "this paper addressed an important problem") are generic and not grounded in specific evidence. These are dropped. Only concrete, evidence-backed strengths are retained.

## Novel Insights

None beyond the paper's own contributions. The key observation — that the two-stage training paradigm conflates evaluation through (a) the map model seeing motion training data, (b) the range mismatch between mapping and prediction, and (c) ego-only metrics — is the paper's own contribution. No reviewer surfaced a genuinely novel insight outside the paper's framing.

## Suggestions

1. **Fix Table 5:** Correct the labeling error — Row 3 should almost certainly be centerline-only (✗, ✗, ✗, ✓ with value 0.6558). Re-verify that the text's conclusions about individual element importance hold after correction.

2. **Add variance information:** Report standard deviations across multiple seeds or bootstrap confidence intervals for key tables (especially Tables 1, 4, and 7) to establish the reliability of fine-grained comparisons.

3. **Separate the two data-split effects:** Consider adding an ablation that isolates spatial overlap from the train-val gap, or at a minimum qualify the claim about spatial overlap being an empirically demonstrated separate effect.

4. **Fix the typo:** Change "minDE" to "minFDE" in Table 7 column headers.

## Score and Decision

Calibration was attempted but the calibration corpus was not accessible on disk, so I calibrate against my knowledge of ICLR review standards. The paper identifies genuine, consequential flaws in a nascent evaluation protocol, provides concrete evidence across 16 experimental combinations, proposes a well-motivated benchmark with cleanly-defined splits and metrics, and introduces a simple baseline that validates the analysis. The primary weakness is a fixable labeling error in one table (Table 5) that does not affect the core claims about data splits, range misalignment, or metrics. The paper is a solid benchmark contribution with diagnostic value to the community.

**Score:** 6.5  
**Decision:** Accept  

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>