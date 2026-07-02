## Summary

D²GS proposes two complementary modules for sparse-view 3D Gaussian Splatting: (1) DD-Drop, a depth-and-density-aware dropout strategy to suppress overfitting in near-field regions, and (2) DAFE, a distance-aware fidelity enhancement using monocular depth priors to improve underfitted far-field regions. A new evaluation metric (IMR) measures distribution-level stability across independent training runs. Results on LLFF and Mip-NeRF360 show consistent improvements over several baselines.

## Strengths

- **Well-motivated, data-driven architectural design.** The paper identifies two opposing failure modes (near-field overfitting vs. far-field underfitting) with quantitative evidence (Gaussian counts: 11,450 vs. 6,112 in near-field; 3,082 vs. 5,224 in far-field) and designs separate, targeted modules for each.

- **Consistent empirical improvement across datasets and metrics.** D²GS outperforms the strongest prior methods (LoopSparseGS, DropGaussian, CoR-GS) on both LLFF and Mip-NeRF360 across multiple metrics, with concrete PSNR gains of 0.35–0.59 dB. Qualitative results (Figure 4) show visible artifact reduction.

- **Reasonably thorough ablation study.** Tables 4–6 progressively add components, explore hyperparameters (dropout rates, weights, masking thresholds), and compare three different monocular depth estimators. This gives a credible picture of which design choices matter and how they interact.

- **IMR proposes a genuinely new evaluation axis.** Measuring distribution-level stability across independent runs via 2-Wasserstein distance with entropic-regularized optimal transport (Eqs. 10–13) is a creative and principled idea that existing image-space metrics do not capture.

## Weaknesses

### Fatal
None.

### Major

- **Main quantitative results (Tables 1–2) lack variance reporting despite the paper's own demonstration of training instability.** Figure 3 (left) shows that PSNR for a baseline method varies from ~14.6 to ~18.6 across 10 runs — a 4 dB range. Yet Tables 1 and 2 report only single-point PSNR/SSIM/LPIPS values with no standard deviations, confidence intervals, or indication of how many seeds were run. The paper states "All experiments run on a single H20 GPU" (line 196). The reported improvements over baselines (0.35–0.59 dB) are an order of magnitude smaller than the documented instability range. Without variance information, the reader cannot assess whether the reported gains are statistically reliable. The IMR results (Table 3) are based on 10 runs, but the headline quantitative comparisons — the primary evidence for the "state-of-the-art" claim — give no such information. The ablation studies (Tables 4–6) similarly report only point estimates.

- **Asymmetric comparison: DAFE uses a strong external depth prior that baselines do not employ.** DAFE (Section 3.3) leverages DepthAnything V2 to generate distance-aware masks for far-field supervision. None of the main 3DGS-based baselines — 3DGS, FSGS, CoR-GS, LoopSparseGS, or DropGaussian — use monocular depth supervision. The ablation (Table 4) partly mitigates this: DD-Drop alone accounts for 1.95 dB of improvement (19.22→21.17) vs. the 3DGS baseline, while DAFE adds only 0.18 dB. However, the "state-of-the-art" claim over methods that don't use depth priors conflates the contribution of the core algorithmic idea (DD-Drop) with the addition of an off-the-shelf depth model. A controlled baseline (e.g., DropGaussian augmented with equivalent depth supervision) would cleanly isolate which gains come from DD-Drop versus the depth prior.

### Minor

- **IMR metric is proposed without any validation.** The paper does not show that IMR correlates with run-to-run PSNR variance (the natural validation target), demonstrate what numerical differences on the IMR scale mean (e.g., 3.039 vs. 3.162 in Table 3), or provide evidence that IMR captures information that image-space metrics miss. The concept is promising, but its usefulness is asserted rather than demonstrated.

- **The claimed "systematic analysis" of failure modes overstates what Section 3.1 provides.** Contribution 1 states the paper "systematically analyze[s] the failure modes of 3DGS in sparse-view settings." Section 3.1 provides a single illustrative comparison (one scene, one baseline method, dense vs. 3-view). This is a motivating observation, not a systematic analysis across scenes, methods, or conditions.

- **DAFE mask update schedule is ambiguous.** Equation (4) defines the binary mask using monocular depth thresholds, but the paper does not state whether this mask is computed once from initial depth maps and kept fixed, or updated during training. If fixed, errors in monocular depth estimation could lead to persistently incorrect masking in regions where depth is misestimated.

- **The DD-Drop design double-counts depth without justification.** Depth appears in the local scoring function (Eq. 1 via d̃_i) and again in the global depth-based layering (Eq. 2 via λ multipliers). The paper does not explain why density alone could not drive the local score while depth drives the global partition. The ablation (Table 4) shows that global layering contributes only ~0.07 dB beyond the local scoring alone (row 4: 21.10 vs. row 5: 21.17), which the paper does not discuss.

- **IMR's depth-stratified importance sampling introduces a mechanical bias.** The paper acknowledges (line 176) that far-field Gaussians are oversampled because they are "more prone to noise and instability," but this means methods that happen to perform better in far-field regions will mechanically have lower IMR. This potential confound is not analyzed.

- **The LLFF 1/8 resolution results (~378×504) are at a very low resolution.** Gains at this resolution may not transfer to full resolution. The paper does report 1/4 resolution as well, partially mitigating this concern, but the primary comparison uses the lower resolution.

### Trivial
None.

## Nice-to-Haves

- Validating the IMR metric by showing its correlation with image-space metric variance (e.g., a scatter plot of IMR vs. PSNR standard deviation across methods and scenes).
- Adding a controlled baseline where a top competitor (e.g., DropGaussian) is augmented with the same monocular depth supervision, to isolate DD-Drop's standalone contribution.
- Reporting the computational cost of IMR computation (Sinkhorn iterations, wall-clock time) for practicality assessment.

## Removed Points

These points from the harsh review were removed per filtering rules — treat with caution:

- **Implementation details in Appendix B being stripped or inaccessible**: Per rule — parser strips appendices from all papers; the original submission contains them.
- **Missing results on DTU/BlendedMVS**: Scope creep — the paper evaluates on standard benchmarks (LLFF, Mip-NeRF360); requesting additional datasets is a nice-to-have, not a valid weakness.
- **Undisclosed hyperparameters (k-NN k, Sinkhorn ε, iterations)**: Per rule — these are standard implementation details the paper states are in Appendix B, which exists in the original submission.
- **Reproducibility concerns about unreleased code/models**: Per rule — cited entities are assumed to exist as of the review date.
- **Formatting/style nitpicks**: Per rule — parser artifacts are not author errors.
- **Typos, grammar, or broken characters**: Per rule — parser-induced artifacts, not present in the original submission.

## Novel Insights

Beyond the paper's own contributions, the reviews surface a broader methodological observation: the severity of the variance problem in sparse-view 3DGS evaluation. The paper documents a 4 dB PSNR swing across runs for a baseline method (Figure 3), yet the field standard practice — followed by this paper and its baselines alike — is to report single-run point estimates for headline comparisons. This gap between documented instability and reporting practice is larger than just this paper; it suggests that empirical evidence for many claims in the sparse-view 3DGS literature may be weaker than presented. The IMR metric, even if unvalidated in this paper, points toward a real missing piece in the evaluation toolkit.

## Suggestions

1. **Report all main results (Tables 1–2, ablations) with means and standard deviations over at least 3–5 random seeds.** This is the single highest-leverage improvement and directly addresses the most significant evidential gap.
2. **Add a controlled baseline** (e.g., DropGaussian + DAFE-equivalent depth supervision) to separate the effect of DD-Drop from the effect of the depth prior.
3. **Validate the IMR metric** by showing its correlation with PSNR standard deviation across runs, or by demonstrating that it captures differences that image metrics miss.
4. **Clarify the DAFE mask computation schedule** (fixed vs. updated) and discuss the small contribution of global layering (~0.07 dB, from Table 4 row 4 vs. row 5).
5. **Tone down the "systematic analysis" claim** in Contribution 1 to match what Section 3.1 actually provides.

## Score and Decision

The paper makes a genuine and architecturally clean contribution — the DD-Drop strategy is more principled than uniform dropout, the motivation is well-supported by data, and the ablation evidence is internally consistent. However, the missing variance reporting in the headline results is a significant evidential gap given the paper's own demonstration of training instability, and the asymmetric depth prior complicates the SOTA claim. These are fixable issues, and the paper's core contribution (DD-Drop) would survive the fix. On balance, this is a borderline accept with clear room for improvement.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>