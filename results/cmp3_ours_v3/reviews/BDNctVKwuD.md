## Summary

This paper makes two contributions: (1) ContrastiveCAM, an M-invariant variant of HiResCAM that provides class-versus-class explanations by subtracting pairwise HiResCAMs, and (2) Core-Focused Cross-Entropy (CFCE), a training loss that uses ContrastiveCAMs and core-region masks to suppress reliance on non-core image regions. The paper proves that HiResCAMs are not uniquely determined (due to softmax invariance), that ContrastiveCAMs remove this redundancy, and that CFCE is classification-calibrated w.r.t. the core-constrained risk. Experiments on Hard-ImageNet, Oxford-IIIT Pets, and PASCAL VOC show that CFCE+KL substantially reduces model reliance on non-core regions, as measured by core-ablation accuracy, RFS, and CAM IoU.

## Strengths

1. **Hard-ImageNet core-ablation results are genuinely striking.** Under gray-mask core ablation, CE accuracy drops to 75.94% while CFCE drops to 41.78% and CFCE+KL to 45.49% — a dramatic reduction in non-core reliance. ContrastiveCAM IoU jumps from 30.27% (CE w/ Arch) to 93.39% (CFCE+KL), and RFS goes from consistently negative (−0.18 to −0.23) to decisively positive (0.224–0.236). These are not incremental improvements; they represent a qualitatively different model behavior.

2. **Classification-calibration guarantee (Theorem 4.6).** CFCE is proven consistent with the core-constrained risk in the realizable setting. Many region-suppression methods are heuristic; CFCE has a principled theoretical connection to its optimization objective.

3. **Demonstration that approximate masks work.** Oxford-IIIT Pets experiments show that SAM-generated masks and bounding boxes achieve competitive alignment relative to ground-truth masks. This partially addresses the practical concern about requiring expensive pixel-level annotations, and results are honestly reported.

4. **Downstream segmentation improvements (Section 5.3).** Backbones trained with CFCE+KL transfer to segmentation (both frozen and end-to-end) with improved IoU on most PASCAL VOC classes, suggesting the alignment improvement reflects genuinely better feature representations.

5. **ContrastiveCAM M-invariance and class-versus-class granularity.** The formal removal of the additive ambiguity from HiResCAM (Theorem 3.5) is a clean mathematical contribution, and the pairwise class-versus-class explanations provide granularity that standard single-class CAMs lack.

## Weaknesses

### Fatal
None.

### Major

1. **The theoretical critique of HiResCAM is oversold.** Theorem 3.2 correctly observes that because softmax is invariant to constant logit shifts, many possible logit vectors (hence many possible HiResCAMs) can map to the same probability output. However, for a *fixed trained model and fixed input*, the activations and logits are uniquely computed, and the HiResCAMs are uniquely determined. The non-uniqueness is a property of the softmax function's relationship to logits — it is not a practical ambiguity in explanations from a single model. The abstract's phrasing ("HiResCAMs for a given input are not uniquely determined") and the claim that this "can, in principle, completely corrupt HiResCAM explanations" (line 17) imply a practical unreliability that does not follow from the theorem as stated. The paper would be stronger if it motivated ContrastiveCAM primarily through its class-versus-class granularity and direct connection to probabilities (Proposition 4.1), rather than centering the motivation on a theoretical issue that does not manifest as practical ambiguity for fixed models.

2. **The "Pareto improvement" claim on PASCAL VOC is not accurate.** The paper states: "We report a pareto improvement with increased Average Precision (AP) and Intersection-over-Union (IoU) scores" (lines 306–307). However, CFBCE+KL achieves valid AP of 87.19%, which is *below* CE (87.32%) and CE w/ Arch (88.85%). Only IoU improves (85.39% vs 44.50%). For CFBCE (without KL), AP of 88.39% is above CE but still below CE w/ Arch. This is an AP-IoU trade-off, not a Pareto improvement.

### Minor

1. **Asymmetric IoU evaluation in Table 2.** Baselines (CE, CORM, DFR) report only GradCAM IoU while CFCE methods report both GradCAM and ContrastiveCAM IoU. The paper acknowledges this (line 257), and the "CE w/ Arch" baseline does provide one ContrastiveCAM IoU anchor (30.27% → 93.39% is a fair within-metric comparison). However, a fully fair comparison would require ContrastiveCAM IoU for all baselines. As presented, the headline improvement mixes a method change with a metric change for some comparisons.

2. **Missing feature-alignment baselines on Oxford Pets and PASCAL VOC.** The Hard-ImageNet experiments compare against CORM and DFR. But the Pets and VOC tables compare only against CE and CE w/ Arch — no feature-alignment baselines from the cited related work (Aniraj et al. 2023, Ismail et al. 2021) are included. If the paper claims improvement over existing alignment methods, additional baselines on these datasets would strengthen that claim.

3. **No hyperparameter sensitivity analysis.** The divergence regularization (Eq. 18) has three scaling parameters (λ₁, λ₂, λ₃). Given that KL regularization has a strong effect (GradCAM IoU jumps from 18.88% to 51.52% with KL), sensitivity to these choices matters but is not discussed.

4. **CE w/ Arch degradation on Oxford Pets not discussed.** The CE w/ Arch model's binary validation IoU drops from 78.37% (standard CE) to 39.07% (±16.98). The paper does not comment on this instability, which is important for interpreting the CE w/ Arch baseline.

5. **Bias-zeroing assumption not tested.** Proposition 4.2 and the CFCE formulation rely on zeroing the final bias vector (line 166). The practical sensitivity to this assumption is not investigated.

6. **Computational overhead not discussed.** CFCE requires computing ContrastiveCAMs at every training step. The paper does not report training time or memory overhead, which is relevant for practitioners.

7. **Single-layer classifier scope limitation.** The theoretical analysis assumes a single-layer classifier (Eq. 1), covering many modern architectures but not deeper heads. The scope is stated but should be more prominently flagged.

### Trivial
None.

## Nice-to-Haves
- Report ContrastiveCAM IoU for all baselines in Table 2.
- Add at least one feature-alignment baseline (e.g., Aniraj et al. 2023) to the Oxford Pets experiments.
- Include error bars or variance for the segmentation bar chart (Section 5.3).
- Discuss how CFCE adapts to multilabel settings (CFBCE) in the main text rather than only in Appendix B.

## Removed Points
The input review's "Core-region mask requirement limits scope" point was removed because the paper honestly acknowledges this and provides SAM/BBOX experiments as mitigation. This is a scope characteristic, not an unaddressed weakness. The interpretation of γ as unclear was removed because the quantity is mathematically well-defined (γ = ‖R‖_F / ‖CAM^{HiRes}‖_F); the conceptual label is a minor semantic issue. The "practically vacuous" framing of the theoretical critique was re-cast as Major weakness #1 above (oversold framing) rather than a fatal flaw, because the mathematics itself is correct and the paper's stated claims are technically accurate when read precisely. Generic style nitpicks and reproducibility concerns about appendix content were removed per the filtering rules.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Reframe the motivation: de-emphasize the HiResCAM non-uniqueness as a practical concern and instead center ContrastiveCAM on its class-versus-class granularity and the direct probability connection (Proposition 4.1) — both are genuine advantages that do not require overselling a softmax artifact.
2. Compute ContrastiveCAM IoU for all baselines in Table 2 to enable a fully fair comparison.
3. Qualify the "Pareto improvement" claim on PASCAL VOC (it is IoU-dominated but not AP-dominated).
4. Add a brief sensitivity analysis for λ₁, λ₂, λ₃ (at minimum, cite values used and discuss stability).
5. Discuss why CE w/ Arch degrades on Pets binary IoU and whether this is expected.
6. Report training-time overhead.

## Score and Decision

**Calibration anchors (all retrieved across rounds):**

- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5lUdTogEL3.md` — avg 1.00 (Round 1, strong reject bracket). Weak, non-technical paper; our paper is orders of magnitude stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tDxGthJkSD.md` — avg 3.00 (Round 1, reject bracket). Object detection loss paper with limited novelty; our paper has more theoretical grounding and stronger empirical results.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6u6GjS0vKZ.md` — avg 4.25 (Round 1, borderline reject). Activation hue loss; modest classification improvements. Our paper has more dramatic results and broader evaluation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/T7q5LBGISH.md` — avg 5.25, rejected (Round 1, borderline). Saliency map smoothing; limited architecture testing, methodological confounds. Our paper has more comprehensive evaluation and theoretical contributions.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/EwAGztBkJ6.md` — avg 4.00, rejected (Round 1, borderline). Gradient interpretation generalization; reviewers found the problem framing contrived. Our paper addresses a better-motivated problem.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bkdWThqE6q.md` — avg 6.00, accepted (Round 2, narrow). Interpretable transformer; clear presentation but mostly qualitative evaluation and accuracy trade-offs. Comparable to our paper in overall merit.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/U7VW3KBm34.md` — avg 6.00, accepted (Round 2, narrow). XAI method (SRD); strong quantitative evaluation but limited to explanation quality, no training-time intervention. Comparable contribution level.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3b8CgMO5ix.md` — avg 5.50, rejected (Round 2, narrow). Weakly-supervised segmentation via explanations; had placeholder abstract content issues. Not a clean comparison.

**Round 1 bracket:** 5.5–6.5 (the paper is clearly stronger than score-4 and below papers, and clearly weaker than score-8 papers).

**Round 2 narrowing:** Compared against accepted papers at 6.00 (interpretable transformer, SRD), our paper has a similar profile: clear contributions with some methodological weaknesses, but sufficient empirical evidence to support the core claims. The oversold theoretical framing is a real weakness but does not invalidate the empirical contributions.

**Final score:** 6.0. The paper makes a genuine empirical contribution (dramatic reduction in non-core reliance on Hard-ImageNet), has theoretical grounding (classification calibration), shows approximate masks work, and demonstrates downstream transfer. The oversold HiResCAM framing, asymmetric evaluation, missing baselines on two datasets, and inaccurate "Pareto" claim are real weaknesses that require major revisions, but they do not invalidate the core findings.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>