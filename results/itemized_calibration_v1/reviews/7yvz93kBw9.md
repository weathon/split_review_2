Now I'll produce the final consolidated review.

## Summary

This paper identifies two distinct failure modes in sparse-view 3DGS — near-field overfitting (excessive Gaussian density) and far-field underfitting (insufficient coverage) — and proposes D²GS, a unified framework with two complementary modules. The Depth-and-Density Guided Dropout (DD-Drop) mechanism adaptively suppresses overfitting in high-density near-field regions using local depth+density scoring combined with global depth-based stratification. The Distance-Aware Fidelity Enhancement (DAFE) module amplifies supervision in far-field regions using monocular depth priors. The paper also introduces Inter-Model Robustness (IMR), a distribution-level metric quantifying stability across independent training runs. Experiments on LLFF and Mip-NeRF360 show consistent improvements over per-scene optimization baselines.

## Strengths

- **Clear problem decomposition with well-matched module design.** The paper identifies two distinct spatial failure modes (near-field overfitting, far-field underfitting) and designs separate modules targeting each. This two-failure-mode framing is a genuinely useful conceptual contribution that goes beyond the uniform dropout strategy of prior work (e.g., DropGaussian). DD-Drop's two-level design (local continuous scoring via depth+density, global discrete stratification via depth tertiles) is internally coherent, and DAFE directly addresses the complementary underfitting issue.

- **Solid and consistent quantitative results.** On LLFF (3-view, 1/8 resolution), D²GS achieves 21.35 PSNR versus 20.85 (LoopSparseGS), 20.76 (DropGaussian), and 20.45 (CoR-GS), with corresponding gains in SSIM, LPIPS, and AVGE. On Mip-NeRF360, it improves over DropGaussian by 0.35 dB. The gains are modest but systematic across metrics, datasets, and resolutions (1/8 and 1/4). The ablation study (Table 4) convincingly shows each component contributes positively, with the full model achieving the best performance.

- **Thorough ablation and hyperparameter analysis.** Tables 4, 5, and 6 provide a detailed breakdown: the contributions of density score, depth score, depth-based layering, and DAFE are each isolated (Table 4); hyperparameters ω_depth, ω_density, r_min, r_max, τ, and λ_DAFE are swept (Table 5); and compatibility with three different monocular depth estimators is checked (Table 6). This is more comprehensive than many papers in this area.

## Weaknesses

### Major

- **IMR metric is oversold and incompletely evaluated.** IMR is presented as a third main contribution ("a Gaussian-distribution-based metric to assess robustness and fidelity beyond conventional 2D evaluations") but is only demonstrated on one of two datasets. Table 3 reports IMR only for LLFF (3-view and 6-view); no IMR results are provided for Mip-NeRF360, despite the paper claiming comprehensive evaluation on both datasets. The experimental protocol is additionally underspecified: the caption states "ten independent training models" without clarifying whether these use different random seeds, and the per-scene aggregation method (how individual scene IMR values are combined into the single number in Table 3) is not stated. While IMR *does* provide differentiated signal from PSNR (e.g., CoR-GS ranks 2nd in IMR but 4th in PSNR among methods, while DropGaussian ranks 4th in IMR but 2nd in PSNR — contradicting the reviewer claim that rankings are identical), its practical value remains unclear without broader evaluation. Listing an incompletely validated metric as a main contribution inflates the paper's claimed novelty.

### Minor

- **Central motivation rests on thin evidence.** Section 3.1's claim of spatial imbalance is supported by a single numerical comparison (11,450 vs. 6,112 and 3,082 vs. 5,224 Gaussian counts) from one scene, one method, and one pair of boxes, with the specific scene/dataset not identified in the text. Labeling this a "comprehensive analysis" (line 54) overstates the evidence. While illustrative examples are common for motivation, multi-scene, multi-method statistics would substantially strengthen the empirical foundation for the paper's two-module design.

- **No error bars or variance estimates for main results.** Tables 1, 2, and 4 report single numbers without standard deviations or confidence intervals. This is a notable omission given that the paper itself documents significant run-to-run variance (Figure 3 shows PSNR ranging from 14.62 to 18.63 across 10 training rounds for prior methods). Variance reporting would clarify whether the observed improvements are statistically significant.

- **DD-Drop local vs. global interaction is not analyzed.** The local scoring gives far-field Gaussians higher depth scores (d̃_i ≈ 1), while the global stratification reduces their dropout probability by 70% (λ_far = 0.3). These mechanisms have opposing directional effects on far-field Gaussians. The net behavior and the relative contribution of each component are asserted rather than demonstrated. An ablation isolating local-only and global-only configurations would clarify whether both are necessary.

- **λ_middle and λ_far are not ablated.** These hyperparameters (set to 0.7 and 0.3 "based on experimental experience," line 76) govern the global stratification mechanism but are not swept in the hyperparameter ablation (Table 5), unlike r_min, r_max, ω_depth/ω_density, τ, and λ_DAFE.

### Trivial

None.

## Nice-to-Haves

- Report IMR on Mip-NeRF360 and clarify the aggregation protocol (per-scene averaging? number of seeds?).
- Include standard deviations alongside mean metrics in main tables.
- Ablate λ_middle and λ_far, and analyze the interaction between local scoring and global stratification.
- Discuss how the proposed per-scene optimization approach relates to feed-forward alternatives (PixelSplat, MVStplat, HiSplat) cited in related work, which also target sparse-view settings but differ in paradigm.

## Removed Points

These points from the input reviews are flagged for removal; treat them with caution:

- **"IMR ranking is the same as PSNR/SSIM/LPIPS ranking"** (from Harsh Critic, Issue 1). This is factually contradicted by the paper's data: CoR-GS and DropGaussian swap order between IMR and PSNR, meaning IMR does provide differentiated signal. **Removed as factually incorrect.**
- **Missing ε (entropic regularization strength) for IMR.** The paper's appendix was stripped by the parser; this specification likely resides there. **Removed per rules about stripped appendix content.**
- **Bures shape term Taylor expansion not validated.** The derivation is deferred to the appendix (stripped). **Removed.**
- **Missing feed-forward method comparisons.** Feed-forward methods (PixelSplat, MVStplat, HiSplat) represent a different paradigm (generalizable feed-forward vs. per-scene optimization). The paper's scope is explicitly per-scene optimization. **Downgraded to Nice-to-Have per scope-creep rule.**
- **Pure formatting/style nitpicks, typos, grammar issues.** These are parser artifacts or standard reviewer noise. **Removed per hard rules.**

## Novel Insights

None beyond the paper's own contributions. The review confirms that the paper's core insight — that near-field overfitting and far-field underfitting are distinct failure modes requiring complementary treatment — is valid and leads to measurable improvements. The main actionable findings are the need to (a) substantiate the IMR metric's claimed status by evaluating it on both datasets and clarifying its protocol, and (b) strengthen the empirical basis of the motivation section.

## Suggestions

1. Reclassify IMR from a "main contribution" to a secondary analysis, or demonstrate its value more thoroughly by reporting it on Mip-NeRF360, clarifying the aggregation method, and showing a case where IMR reveals robustness differences that PSNR/SSIM miss.
2. Add multi-scene, multi-method Gaussian-count statistics (e.g., a bar chart across all LLFF scenes) to support the spatial imbalance claim in Section 3.1.
3. Add standard deviations to main experimental tables (Tables 1, 2, 4).
4. Ablate λ_middle and λ_far, and include an ablation isolating the local scoring mechanism from the global stratification mechanism to validate their complementary design.

## Score and Decision

### Calibration Analysis

I examined the following anchor papers from the review corpus:

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| HiSplat (SBzIbJojs8) | 6.00 | Round 1 | Yes | Feed-forward sparse-view 3DGS, accepted. Stronger novelty (first hierarchical feed-forward 3DGS) with similar thorough ablation. D²GS has weaker novelty but comparable empirical validation. |
| FreeSplatter (VpGsy4hKMc) | 5.00 | Round 1 | Yes | Pose-free sparse-view, rejected. Major issues: insufficient method detail, weak ablation, unfair comparisons. D²GS is substantially stronger on methodology and ablation. |
| RAIN-GS (R9lgWYE508) | 5.75 | Round 2 | Yes | Per-scene 3DGS initialization, rejected. Issues: insufficient novelty, lack of compelling use case. D²GS has clearer motivation and stronger ablation, placing it slightly above. |
| Ref-Gaussian (xPxHQHDH2u) | 6.50 | Round 1 | Yes | 3DGS for reflections, accepted. Stronger contribution and SOTA results. D²GS is below this benchmark. |
| Geo-3DGS (c4Nh4A8Xn5) | 5.00 | Round 2 | No | Multi-view consistency for 3DGS, rejected. D²GS has stronger empirical grounding. |
| Hi-Gaussian (L3WnnnBRdu) | 5.75 | Round 2 | No | Single-view 3DGS, rejected. D²GS is comparable in quality with mixed review profile. |
| Injecting Inductive Bias (vkj5ARRCeY) | 5.75 | Round 2 | No | 3DGS geometry, rejected. Mixed reviews (8,6,6,3). D²GS has more consistent scores across potential dimensions. |

**Round 1 bracket**: 5.0–6.0. The paper has genuine, well-validated core contributions (DD-Drop + DAFE) placing it above FreeSplatter/Geo-3DGS (5.0), but the oversold IMR contribution and thin motivation evidence prevent it from reaching the clear-accept level of Ref-Gaussian (6.5). The strongest shared weaknesses with the 5.0–5.75 anchors are: (a) insufficiently validated claimed contribution (compare FreeSplatter's weak ablation), and (b) marginal-but-consistent improvements (compare RAIN-GS). The strongest shared strengths are: thorough ablation, clear motivation, and systematic evaluation.

**Narrowing**: The itemized comparison with RAIN-GS (5.75) is most instructive. D²GS shares RAIN-GS's "modest improvement" profile but has stronger ablation and clearer motivation. However, D²GS adds the IMR overclaim that RAIN-GS lacks. This places D²GS slightly below HiSplat (6.0, whose hierarchical contribution was more novel) and slightly above RAIN-GS. The final score of **5.5** reflects a paper with solid, well-evaluated core methodology that is held back by an overclaimed secondary contribution and thin motivational evidence — both addressable issues.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>