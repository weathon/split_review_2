## Summary

This paper addresses sparse-view 3D Gaussian Splatting by identifying two failure modes—near-field overfitting (excess Gaussians) and far-field underfitting (insufficient Gaussians)—and proposes a two-module framework (D²GS) to remedy them: a Depth-and-Density Guided Dropout (DD-Drop) that adaptively masks redundant Gaussians, and a Distance-Aware Fidelity Enhancement (DAFE) module that boosts supervision in distant regions. The paper also introduces an Inter-Model Robustness (IMR) metric to quantify training stability across runs. Results on LLFF and Mip-NeRF360 show consistent improvements over optimization-based baselines.

## Strengths

+ **Well-motivated problem diagnosis (Section 3.1).** The paper documents the spatial-imbalance failure pattern with concrete primitive-count evidence: near-field Gaussians balloon to 11,450 vs. 6,112 in the dense-view reference, while far-field Gaussians drop to 3,082 vs. 5,224. This quantitative characterization is more compelling than generic "sparse views are hard" motivation.

+ **Complementary design of DD-Drop and DAFE.** The two modules target opposite failure modes (overfitting vs. underfitting) at different pipeline levels (Gaussian-level dropout vs. image-level loss modulation). The ablation study (Table 4) confirms each module contributes independently and their combination outperforms either alone.

+ **Thorough ablation studies (Tables 4–6).** Step-wise ablations demonstrate the contribution of each component, hyperparameter sweeps cover sensible ranges, and the depth estimator ablation (MiDas, DPT, DepthAnything V2) shows DAFE's robustness to the choice of depth prior.

+ **IMR metric (Section 3.4).** The paper identifies a genuine blind spot—standard image-space metrics (PSNR, SSIM, LPIPS) say nothing about whether the underlying 3D representation is stable across training runs. The IMR metric, grounded in optimal transport over Gaussian mixtures, is a sensible attempt to fill this gap, albeit with validation limitations noted below.

## Weaknesses

### Fatal
None.

### Major

**1. No variance reporting on main results (Tables 1 and 2), despite the paper's emphasis on robustness.** The paper motivates IMR precisely because "repeated training… can produce results with considerable variance" (Section 3.4) and shows PSNR fluctuating between 14.62 and 18.63 across runs (Figure 3). Yet Tables 1 and 2 report PSNR, SSIM, LPIPS, and AVGE as single numbers with no standard deviations, confidence intervals, or any run-to-run variability. Given that Figure 3 demonstrates ~4 dB PSNR fluctuations for a baseline, the reader cannot assess whether D²GS's 0.5–0.9 dB advantage over competitors exceeds the evaluation noise. The IMR table (Table 3) reports cross-run consistency for the Gaussian distribution, but this is a different quantity from the variance of *image quality metrics* across runs. This omission is self-undermining for a paper whose central claim is improved robustness.

### Minor

**2. The DD-Drop depth score's directional role is unclearly described (Section 3.2, Eq. 1–2).** The depth score $\tilde{d}_i$ is min-max normalized Euclidean distance to the camera, so near-field Gaussians receive *low* depth scores (~0) and far-field Gaussians receive *high* scores (~1). Since the paper states that near-field regions are prone to overfitting and should be dropped more, a reader would expect near-field Gaussians to receive higher scores. The depth-based layering in Eq. (2) compensates by attenuating far-field dropout (λ_far=0.3), and the ablation (Table 4) confirms the overall design works (depth score alone with layering improves PSNR by 1.70 dB). However, the description of *how* the depth score contributes is misleading—it likely functions by tempering the density signal rather than directly identifying overfitted regions. The authors should clarify this interaction or reformulate the score direction.

**3. The IMR metric is under-validated as a meaningful measure of 3D representation quality (Section 3.4, Table 3).** IMR measures *consistency* across training runs, but consistency is not equivalent to accuracy (a method that always produces the same blurry output would have excellent IMR but poor PSNR). Table 3 shows rank inconsistencies (e.g., at 6-view, CoR-GS has worse IMR than 3DGS despite better PSNR), and the absolute IMR differences between methods are small (~0.03–0.16 on a ~3.1 scale) with no significance testing. The metric would benefit from validation showing correlation with PSNR variance or detection of known degeneracies that image metrics miss.

**4. Feed-forward methods mentioned in Related Work are excluded from experimental comparison.** The Related Work cites PixelSplat, MVSplat, and HiSplat as "recent feed-forward methods [that] further advance sparse-view NVS," but D²GS compares only against optimization-based methods. While this is standard practice in the per-scene optimization literature (feed-forward methods involve a fundamentally different inference paradigm), the paper's claim of "state-of-the-art novel view synthesis" (contribution list) should clarify this scope limitation.

**5. Computational cost is not analyzed.** DD-Drop requires per-iteration k-nearest-neighbor density estimation, and DAFE requires a monocular depth estimator. Neither cost is quantified. Training time overhead relative to DropGaussian/3DGS should be reported.

### Trivial
None.

## Nice-to-Haves

- **Directly visualize the spatial distribution of Gaussians before and after each module** (not just as motivation in Figure 1 but as evidence of the method working). Show that DD-Drop reduces Gaussian density in near-field regions and DAFE increases it in far-field regions, with counts analogous to the 11,450/6,112/3,082/5,224 numbers in Section 3.1.
- **Report failure cases** — scenes or viewpoints where D²GS underperforms baselines.
- **Validate IMR** by demonstrating its correlation with PSNR variance across scenes.

## Removed Points

These points are flagged for removal; treat them with caution:
- "Depth score is formulated in the wrong direction, and the method works despite it, not because of it" → Downgraded to Minor. The method plainly works (ablation confirms contribution across all configurations), and the issue is one of description clarity, not invalidation.
- "K value for KNN not specified" / "How camera distance is defined during training" → Likely in Appendix B, which was stripped by the parser per system constraints.
- "Monocular depth relative ordering reliability" → Partly addressed by ablating across three depth estimators (Table 6).
- "Baseline numbers regenerated or taken from original paper" → Speculative.
- "Statistical significance of IMR differences" → Subsumed under the IMR validation weakness above.

## Novel Insights

None beyond the paper's own contributions. The spatial-imbalance diagnosis with primitive-count evidence is the paper's own novel observation, not a synthetic insight from the reviews.

## Suggestions

1. **Report means and standard deviations (or ranges) for PSNR/SSIM/LPIPS across multiple seeds** on the main results tables. This is the single most impactful fix—without it, the paper's emphasis on robustness is contradicted by the evaluation format.
2. **Clarify the DD-Drop depth score interaction** — either reformulate so near-field Gaussians receive higher depth scores, or explicitly state that the depth score tempers the density signal while the layering provides the spatial selectivity.
3. **Validate the IMR metric** by showing correlation with PSNR variance across scenes or its ability to detect collapsed Gaussians that image metrics miss.
4. **Report training time** overhead of DD-Drop and DAFE relative to base 3DGS/DropGaussian.

## Score and Decision

**Calibration anchors consulted (all rounds):**

| Anchor | Avg Score | Round | Itemized | Comparison to D²GS |
|--------|-----------|-------|----------|---------------------|
| HiSplat (SBzIbJojs8) | 6.0 | R1 | Yes | Feed-forward sparse-view 3DGS; accepted. D²GS has stronger diagnostic motivation but a major evaluation weakness HiSplat lacks. |
| FreeSplatter (VpGsy4hKMc) | 5.0 | R1 | Yes | Pose-free GS; rejected. D²GS has clearer contribution and fewer novelty concerns. |
| NoPoSplat (P4o9akekdf) | 8.0 | R1 | Yes | Pose-free GS; strongly accepted. Significantly more novel; D²GS is not at this level. |
| RAIN-GS (R9lgWYE508) | 5.75 | R2 | Yes | Relaxing initialization for 3DGS; rejected. D²GS has stronger motivation and ablations but similar-magnitude weakness. |
| IBGS (vkj5ARRCeY) | 5.75 | R2 | Yes | Geometry-focused 3DGS; rejected. Marginal improvement vs. compute cost was fatal. D²GS improvements are clearer. |

**Bracket reasoning (Round 1):** D²GS sits between RAIN-GS (5.75) and HiSplat (6.0). It has a stronger problem diagnosis than RAIN-GS but shares a similar-magnitude weakness. Its contributions are clearer than FreeSplatter (5.0) but less novel than HiSplat (6.0). **Initial bracket: 5.0–6.0.**

**Narrowing (Round 2):** D²GS's major weakness (variance reporting, impact -9.97) is comparable in severity to RAIN-GS's novelty concerns (-10.00, -10.00) and IBGS's marginal-improvement gap (-9.55, -9.90). Unlike RAIN-GS/IBGS which had reviewers scoring 5–6 with novelty doubts, D²GS has a *fixable methodological gap* rather than a fundamental contribution issue. Placing it slightly below HiSplat (which had no major weakness) but above the 5.0 papers gives **final score: 5.5**.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>