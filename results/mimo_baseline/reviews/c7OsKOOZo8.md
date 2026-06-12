## Summary

This paper proposes an end-to-end framework for multi-view diabetic retinopathy (DR) grading that eliminates the need for external lesion or vessel annotations. The two core contributions are: (1) GALP, which generates lesion proposals on-the-fly from grade-conditioned evidence maps derived via stage-wise auxiliary classifiers, and (2) LGRF, a mixture-of-experts based cross-view fusion module that selectively routes and integrates lesion proposal features across views. Experiments on MFIDDR (4-view) and DRTiD (2-view) benchmarks show the method matches or surpasses externally-informed baselines without requiring additional annotations.

## Strengths

- **Well-motivated problem with practical significance.** The paper clearly articulates a genuine practical tension: externally-informed models perform better but require costly annotations and increase deployment burden, while pure end-to-end models underperform on subtle lesions. The proposed self-derived lesion proposal approach directly addresses this gap in a principled way.

- **Strong empirical results across two datasets.** On MFIDDR, the lesion-free variant (83.9% Acc) matches or exceeds several externally-informed methods (e.g., LFMVDR with lesion at 82.2%, CVSA with vessel at 82.6%). On DRTiD, the end-to-end method achieves 76.0% accuracy, surpassing even CrossFIT (75.6%) which uses OD and macular coordinates. With lesion annotations added via SPADE, the method achieves 84.6% accuracy, a new SOTA on MFIDDR. These are convincing results that support the paper's central claims.

- **Well-structured ablation study.** Table 4 cleanly isolates the contribution of each component (GALP, Experts, LGRF), with each removal producing a clear accuracy drop (1.2–1.6 percentage points), demonstrating complementary contributions. The hyperparameter analysis in Figure 3 provides practical guidance on key design choices (retention ratio, number of experts, expert activation count).

- **Clear technical exposition.** The method is described with well-defined mathematical formulations (Eqs. 1–20) that are consistent and traceable. The architecture diagram (Figure 2) provides a useful visual summary of the pipeline.

## Weaknesses

### Fatal
None.

### Major

- **Limited generalizability evidence.** Both evaluation datasets are Chinese ophthalmology datasets (MFIDDR from the Shanghai-based group, DRTiD similar origin). There is no evaluation on international benchmarks or diverse populations, which limits the confidence that the self-derived lesion proposal mechanism generalizes across different image acquisition protocols, ethnicities, and disease manifestation patterns. The authors could at least discuss this limitation.

- **The "lesion proposals" are really class activation map peaks, not lesion detectors.** The paper consistently frames GALP outputs as "lesion proposals," but what is actually generated are top-K regions from grade-conditioned CAMs. There is no evaluation showing these proposals actually correspond to anatomical lesions (e.g., by comparing against ground-truth lesion segmentation masks, which are available in MFIDDR). Without this validation, the claim that GALP "recovers small, low-contrast lesions" (Contribution 1) remains unsubstantiated — the model may simply be learning discriminative regions that happen to correlate with grade but are not anatomically meaningful lesions.

- **Fairness of comparison concerns.** The method uses Swin-B backbone, while some baselines use lighter architectures (ResNet50, VGG19 for MVCNN variants). The paper notes backbone choices are matched to "prior SOTA works," but this makes cross-method comparisons less controlled. A uniform backbone comparison would strengthen the experimental claims considerably.

### Minor

- **Grade 1 performance lags behind best externally-informed methods.** On MFIDDR (Table 2), Grade 1 F1 for the lesion-free variant is 69.7%, while SMVDR-M achieves 71.7%. Grade 1 (mild DR) represents the earliest actionable stage, so this gap is clinically relevant and worth discussing.

- **The cyclic adjacency in LGRF (view i attends to view i+1) is a design choice that lacks justification.** Why not attend to all other views? The paper does not explain why restricting to one adjacent view is preferable, nor does it compare against all-to-all cross-view attention.

- **The claim of "interpretability" (Contribution 2) is made but not evaluated.** No qualitative visualization of proposals or attention maps is provided to demonstrate that the model indeed attends to clinically meaningful regions. For a method motivated partly by interpretability, this is a missed opportunity.

### Trivial
None.

## Nice-to-Haves

- A qualitative visualization showing the top-K lesion proposals overlaid on fundus images, ideally compared against ground-truth lesion annotations from MFIDDR, would significantly strengthen the paper's narrative.
- A computational cost comparison (FLOPs, inference time) against the simpler end-to-end baselines and the heavier externally-informed methods would help assess the practical efficiency of the approach.
- Analysis of failure cases, particularly where self-derived proposals diverge from actual lesion locations, would deepen understanding of the method's limitations.

## Novel Insights

The paper's most interesting observation is that CAM-derived grade-conditioned evidence maps can serve as effective surrogates for expert-annotated lesion maps in a multi-view DR grading pipeline, enabling competitive performance without any external annotations. The finding that even coarse, self-generated proposals (top-50% of spatial regions ranked by CAM activation) suffice for effective cross-view fusion is practically valuable. Additionally, the demonstration that a current view can effectively select which experts should process another view's lesion proposals (contextual expert gating) is a useful architectural contribution that could extend beyond DR grading.

## Suggestions

- Add lesion localization evaluation using MFIDDR's available segmentation masks to validate that GALP proposals correspond to actual lesions.
- Include a uniform-backbone comparison (all methods using Swin-B) to isolate the contribution of the architectural design from backbone capacity.
- Provide qualitative visualizations of the grade-conditioned evidence maps and resulting lesion proposals.
- Discuss the cyclic adjacency design choice and consider comparing against all-pairs cross-view attention.

## Score and Decision

The paper presents a well-motivated and technically sound approach to an important practical problem. The experimental results are strong, with the lesion-free variant convincingly matching or exceeding many externally-informed baselines. However, the central claim that GALP generates meaningful "lesion proposals" lacks direct validation against ground-truth lesion masks, the generalizability beyond Chinese datasets is uncertain, and backbone non-uniformity across comparisons introduces confounding factors. These issues are significant but do not invalidate the overall contribution. The paper represents solid incremental work with clear practical value.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>