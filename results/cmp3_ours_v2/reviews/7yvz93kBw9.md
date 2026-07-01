## Summary

The paper proposes D²GS, a framework for sparse-view 3D Gaussian Splatting that addresses two identified failure modes: overfitting in near-field regions (excessive Gaussian density) and underfitting in far-field regions (insufficient Gaussian coverage). It introduces (1) **DD-Drop**, a depth-and-density guided dropout strategy combining a local continuous scoring function with a global discrete depth-based layering mechanism, (2) **DAFE**, which uses monocular depth priors to construct a binary mask and amplify supervision in distant regions, and (3) **IMR**, a distribution-based metric measuring inter-model stability via optimal transport between independently trained Gaussian mixtures. Experiments on LLFF and Mip-NeRF360 show consistent PSNR gains of 0.35–0.59 dB over the most relevant baseline (DropGaussian).

## Strengths

1. **Well-motivated problem diagnosis (Section 3.1).** The paper provides concrete quantitative evidence for spatial imbalance in sparse-view 3DGS: the near-field Gaussian count increases from 6,112 (dense) to 11,450 (sparse), while the far-field drops from 5,224 to 3,082. This documents a specific failure pattern — spatial overfitting and underfitting — that uniform dropout strategies fail to address because they treat all regions equally.

2. **Cleanly decomposed method design.** The DD-Drop module combines a continuous local scoring function (Eq. 1: weighted combination of normalized depth and density) with a discrete global layering mechanism (Eq. 2: depth-tertile-dependent attenuation). The progressive dropout schedule (Eq. 3) is a sensible addition. The ablation in Table 4 confirms that each component — density score, depth score, depth-based layering, and DAFE — contributes positively, and the parameter sweeps in Table 5 justify the chosen configurations (ω_depth=ω_density=0.5, r_min=0.05, r_max=0.3).

3. **Consistent experimental results.** D²GS achieves best results across all metrics on both LLFF (two resolutions) and Mip-NeRF360, against a broad set of baselines including NeRF-based, 3DGS-based, and depth-supervised methods. Gains over DropGaussian (the most relevant baseline) are 0.35–0.59 dB PSNR — modest but consistent across settings. The visual comparisons (Figure 4) support the quantitative results.

4. **Novel evaluation perspective with IMR.** Shifting evaluation from image-space to distribution-space by measuring stability of learned Gaussian representations across independent training runs is a conceptually interesting direction. The use of optimal transport over Gaussian mixtures to quantify inter-model divergence (Section 3.4) is technically well-grounded, and the metric addresses a genuine need in assessing 3DGS robustness.

## Weaknesses

### Fatal
None.

### Major

1. **IMR metric proposed as a contribution without adequate validation (Section 3.4, Table 3).** The IMR metric is listed as a main contribution (abstract, introduction), but its informativeness is not established:
   - **No validation that IMR measures what it claims.** The paper asserts IMR captures "robustness" / "stability" of Gaussian distributions, but provides no evidence — correlation with PSNR variance across runs, sensitivity to known perturbations, or comparison with alternative stability measures — that lower IMR corresponds to more robust models. In Table 3, the relationship between IMR and rendering quality is non-monotonic: DropGaussian has substantially *better* PSNR than 3DGS (20.76 vs. 19.22) yet *worse* IMR (3.205 vs. 3.162). Without an anchor, readers cannot interpret whether the reported differences (e.g., 3.039 vs. 3.205) are meaningful.
   - **Arbitrary formulation and uninterpretable scale.** The ratio ΣS²/ΣS followed by a log (Eq. 14) is presented without justification. Why this specific weighting and log transform rather than variance, mean pairwise distance, or maximum divergence? The resulting values (≈3.0–3.2) sit on a scale with no stated interpretation — there is no indication of what constitutes a "good" IMR value or how large a difference of ~0.17 is relative to natural variation.
   - **Uncharacterized approximation error.** The metric subsamples ~10,000 Gaussians via depth-stratified importance sampling from models with 20k–310k Gaussians (as few as 3% of primitives in some scenes). The error introduced by this approximation is not analyzed.

   *Impact:* This weakness is significant because IMR is framed as a contribution, but the current evidence does not demonstrate its utility. If the paper demoted IMR to a supplementary analysis and focused contributions on DD-Drop + DAFE, this concern would be substantially reduced.

2. **Inconsistency between Figure 2 and Section 3.3 for the DAFE module.** Figure 2's caption defines the DAFE loss with three region-specific terms: L_DAFE = λ_near L_near + λ_mid L_mid + λ_far L_far. However, Section 3.3 defines a single binary mask M_dis (Eq. 4, thresholding at τ·D_max) and a single loss term applied only to far-field masked pixels (Eq. 5). The text and ablation (Tables 4–5) consistently describe a single far-field loss. This discrepancy must be resolved — if the implementation uses three losses, the equations in Section 3.3 are incomplete; if it uses one, the figure caption is incorrect.

### Minor

3. **DAFE contributes very modest gains relative to its framing in the "unified framework."** From the ablation (Table 4), adding DAFE on top of full DD-Drop improves PSNR by +0.18 dB (21.17 → 21.35). The design — monocular depth estimation + binary threshold mask + L1 loss on masked pixels — is a straightforward application of widely-used depth-supervision techniques (Deng et al., 2022; Niemeyer et al., 2022; Yang et al., 2025, among those cited in the paper). Presenting DAFE as a co-equal module alongside DD-Drop somewhat overstates its contribution.

4. **Depth information is double-counted in DD-Drop without discussion.** The local score S_i (Eq. 1) already incorporates depth via ω_depth · d̃_i. The global mechanism (Eq. 2) then bins Gaussians by depth tertiles and applies depth-dependent attenuation (λ_far < λ_middle < 1). Depth influences dropout probability through *both* continuous scoring and discrete layering. This is not necessarily wrong — the two channels could capture different granularities — but the paper does not discuss whether the double-counting is intentional or redundant. The ablation in Table 4 partially addresses this (rows 2–5 show cumulative gains) but does not isolate the contribution of depth-based layering without the depth score, so potential redundancy cannot be assessed.

5. **No statistical significance assessment.** Given the modest PSNR margins (0.35–0.59 dB over DropGaussian), the paper would benefit from reporting standard deviations across runs or conducting significance tests. This is standard practice when margins are within the range of possible run-to-run variance.

6. **Limited evaluation scope.** Experiments are conducted on only two datasets (LLFF and Mip-NeRF360). Many sparse-view reconstruction papers additionally evaluate on DTU or NeRF-Synthetic (Blender) to demonstrate generality across scene types (object-level vs. scene-level). The core method's depth-based spatial partitioning may behave differently on object-centric data.

### Trivial

7. The main text (line 198) refers to "Diet-NeRF" (the common name for Jain et al., 2021) while the corresponding table entry lists "DistNeRF" — the naming should be consistent.

8. The 3DGS baseline shows an unusual PSNR drop from 19.22 (1/8 resolution) to 16.94 (1/4 resolution) on LLFF (Table 1). Typically higher resolution yields comparable or better metrics. The paper does not remark on this.

## Nice-to-Haves

- Validate IMR by showing it correlates with PSNR variance across runs, or demote its status from a main contribution to a supplementary analysis.
- Add standard deviations or confidence intervals to the main quantitative results.
- Discuss failure cases (e.g., when the monocular depth prior is inaccurate).
- Explicitly state why feed-forward methods (PixelSplat, MVSplat, HiSplat) are not compared — they operate under different paradigms (generalizable feed-forward vs. per-scene optimization).

## Removed Points

The following items from the input review were removed per filtering rules:

- **Criticisms about missing KNN implementation details (k, when density is recomputed, Sinkhorn ε, number of models N for IMR):** These are addressed in "More Implementation Details are presented in Appendix B," which is stripped by the parser. Missing appendix content cannot be held against the paper.
- **Feed-forward method comparison omission:** Criticizing the absence of quantitative comparison with PixelSplat/MVSplat/HiSplat is scope creep — these are different paradigms (feed-forward generalizable vs. per-scene optimization). The paper does not claim to outperform them.
- **IMR correlation with PSNR:** The original framing claimed IMR "never shows that lower IMR correlates with better rendering quality." The paper does not claim IMR measures rendering quality; it claims IMR measures distribution stability. The core concern (inadequate validation) is retained in Major Weakness 1 but reframed accurately.
- **Reproducibility nitpicks about implementation details:** Minor hyperparameter disclosure is not required beyond what the appendix provides.
- **"Extensive" in abstract is slightly overstated:** Semantic nitpick below the threshold for a review.
- **Missing related works:** Cannot confirm existence of missing references; rule prohibits mentioning missing related works.

## Novel Insights

None beyond the paper's own contributions. The reviews surface no diagnostic perspective that the paper itself does not already articulate.

## Suggestions

1. **Resolve the DAFE formulation discrepancy.** Clarify whether DAFE uses one far-field mask (per Section 3.3) or three region-specific losses (per Figure 2 caption). If one mask, correct the figure; if three losses, provide the full formulation and ablation results.

2. **Either validate IMR or adjust its framing.** The simplest fix: show that IMR correlates with PSNR variance across N=10 training runs (e.g., a scatter plot of IMR vs. PSNR standard deviation across methods). If validation is not feasible, explicitly frame IMR as a preliminary diagnostic tool rather than a claimed contribution.

3. **Add an ablation isolating depth-based layering without the depth score** (or vice versa, with density score held constant) to show whether the two depth channels are complementary or redundant.

4. **Report standard deviations** for the main results (Tables 1–2), especially given the modest PSNR margins over DropGaussian.

## Score and Decision

**Round-1 Bracket:** 5.5–6.5, calibrated against HiSplat (6.0, Accept) on the same topic of sparse-view 3DGS, with similar strengths (clear motivation, thorough ablations, consistent results) and comparable weaknesses (modest margins, some questionable design choices). The paper is stronger than FreeSplatter (5.0, Reject) and RAIN-GS (5.75, Reject), whose core contributions faced more fundamental practical-relevance challenges. D²GS's core DD-Drop contribution is sound and well-supported; the main unresolved issue is the unvalidated IMR metric, which is addressable in revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>