## Summary

The paper presents D²GS, a framework for improving sparse-view 3D Gaussian Splatting by addressing two identified failure modes: overfitting in near-camera high-density regions and underfitting in distant low-coverage areas. It introduces a Depth-and-Density Guided Dropout (DD-Drop) mechanism that spatially adaptively masks Gaussians, a Distance-Aware Fidelity Enhancement (DAFE) module that strengthens supervision in far-field regions using monocular depth masks, and a novel Inter-Model Robustness (IMR) metric based on Wasserstein distance over Gaussian mixtures to quantify stability across training runs.

## Strengths

- **Clear and well-illustrated problem diagnosis.** The paper provides concrete quantitative evidence for its two failure mode observations—for instance, showing that DropGaussian produces 11,450 Gaussians in near-field regions versus 6,112 for the dense-view baseline (green box in Figure 1), and only 3,082 versus 5,224 in far-field (red box). This spatial imbalance analysis provides solid motivation for the proposed dual-module design.

- **Novel stability metric (IMR).** The Inter-Model Robustness metric is a genuinely novel contribution. Grounding it in 2-Wasserstein distance and optimal transport over opacity-weighted Gaussian mixture distributions is principled, and the entropic regularization with Sinkhorn solving makes it computationally tractable. This metric fills a real gap in the 3DGS evaluation toolkit, as traditional image-space metrics (PSNR, SSIM) cannot capture distributional instability across runs (as vividly shown by the 14.62–18.63 PSNR fluctuation in Figure 3 left).

- **Comprehensive ablation studies.** The paper provides progressive component ablation (Table 4), hyperparameter sensitivity analysis (Table 5), and depth estimator robustness (Table 6), systematically validating each contribution. The fact that DAFE shows consistent gains across MiDaS, DPT, and DepthAnything V2 is reassuring for practical deployment.

## Weaknesses

### Fatal
None.

### Major

- **Incremental methodological novelty.** Both DD-Drop and DAFE apply well-established techniques (spatially-varying dropout and mask-weighted loss) in a relatively straightforward manner to the sparse-view 3DGS problem. The DD-Drop score (Equation 1) is a simple weighted sum of normalized depth and density; the global layering into three depth bins with hand-tuned attenuation factors (λ_middle = 0.7, λ_far = 0.3) adds modest sophistication. DAFE is essentially a depth-thresholded L1 loss weighted by a binary mask. While effective, neither component represents a significant conceptual leap beyond DropGaussian's uniform dropout idea.

- **Modest quantitative improvements.** On LLFF 1/8 resolution, the gain over DropGaussian is 0.59 dB PSNR; over LoopSparseGS, it is 0.50 dB. On Mip-NeRF360, the gain over DropGaussian is 0.35 dB. While consistent, these improvements are incremental rather than transformative, and the 1/4 resolution results on LLFF show the SSIM actually tied with CoR-GS (0.695 vs 0.696) and LPIPS slightly worse than LoopSparseGS (0.254 vs 0.274 lower is better—so this is better, but the SSIM tie is notable). The practical significance of these gains for end users is debatable.

- **IMR metric's practical significance is unclear.** The IMR values across methods are closely clustered (e.g., 3.039 vs 3.162 for 3-view, Table 3), and it is not established what magnitude of difference constitutes a practically meaningful improvement in robustness. The depth-stratified importance sampling to ~10,000 Gaussians and the first-order Taylor approximation of the Bures metric introduce approximations whose effect on the final metric values is not analyzed. Without more characterization (e.g., sensitivity to sampling strategy, correlation with downstream task performance), IMR's utility beyond this specific comparison remains uncertain.

### Minor

- **Missing comparison with recent strong baselines.** The paper mentions feed-forward methods (PixelSplat, MVStplat, HiSplat) in related work but does not compare against them. Omitting LoopSparseGS from the Mip-NeRF360 comparison (Table 2) and IMR evaluation (Table 3) is also notable, as it was competitive on LLFF.

- **Dependency on monocular depth estimation.** The DAFE module's effectiveness depends on the quality of monocular depth maps, yet the paper does not analyze failure cases or sensitivity to depth estimation errors in challenging scenarios (e.g., textureless regions, reflective surfaces). Table 6 shows robustness across estimators but all are state-of-the-art; degradation with weaker estimators is not explored.

### Trivial
None.

## Nice-to-Haves

- A comparison against feed-forward sparse-view methods (PixelSplat, MVStplat, HiSplat) would strengthen the positioning.
- Analysis of computational overhead from DD-Drop (k-NN density estimation) and DAFE (monocular depth inference) relative to the baseline 3DGS would be valuable for practitioners.
- Visualization of how the learned Gaussian distributions differ between D²GS and baselines in 3D space (e.g., spatial distribution heatmaps) would complement the IMR analysis.

## Novel Insights

The paper's most novel insight is the proposal of measuring 3DGS robustness through distributional consistency across independent training runs, formalized via the IMR metric. The observation that PSNR can fluctuate by ~4 dB across identical training configurations (Figure 3 left) highlights an underappreciated source of unreliability in 3DGS, and the Gaussian mixture Wasserstein framework provides a principled way to quantify this. However, beyond the paper's own contributions, the two failure modes (overfitting near, underfitting far) are natural consequences of sparse coverage and the proposed solutions are direct applications of standard regularization techniques.

## Suggestions

- Provide a convergence/efficiency analysis comparing training time and memory overhead of D²GS versus the baseline and DropGaussian.
- Investigate whether the IMR metric correlates with downstream task performance (e.g., surface reconstruction quality, 3D object detection) to establish its broader utility.
- Consider a scene-adaptive mechanism for the depth threshold τ in DAFE rather than the fixed 5%, as optimal far-field coverage likely varies across scenes.

## Score and Decision

The paper presents a competent and well-structured contribution to sparse-view 3DGS with clear problem motivation, solid experimental validation, and a novel robustness metric. However, the core methodological contributions (DD-Drop and DAFE) are incremental applications of established techniques, and the quantitative gains, while consistent, are modest. The IMR metric is the most interesting contribution but requires further validation of its practical significance. This places the paper in the borderline accept category—it is above the median submission quality but does not rise to a clear accept.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>