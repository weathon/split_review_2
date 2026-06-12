## Summary

This paper addresses the sparse-view novel view synthesis problem in 3D Gaussian Splatting (3DGS). It identifies two key failure modes—overfitting in near-field, high-density regions and underfitting in far-field regions—and proposes D²GS, a unified framework with two modules: Depth-and-Density Guided Dropout (DD-Drop) to adaptively prune overfitted Gaussians, and Distance-Aware Fidelity Enhancement (DAFE) to boost supervision in distant areas. The paper also introduces a new evaluation metric, Inter-Model Robustness (IMR), based on optimal transport over Gaussian mixtures, to quantify the stability of learned representations across independent training runs. Experiments on LLFF and Mip-NeRF360 demonstrate consistent improvements over existing NeRF-based and 3DGS-based methods.

## Strengths

- **Clear problem analysis**: The paper provides a well-motivated breakdown of near-field overfitting and far-field underfitting in sparse-view 3DGS, supported by a visual comparison of Gaussian density distributions. This analysis directly drives the method design.
- **Principled adaptive dropout**: DD-Drop combines local (continuous) density-depth scoring with global (discrete) depth-stratified attenuation, which is more sophisticated than uniform dropout used in prior work. The ablation study confirms that both the density and depth signals contribute positively.
- **Complementary far-field enhancement**: DAFE uses monocular depth priors to construct a distance-aware loss that specifically targets underfitted distant regions, addressing a gap often overlooked by other sparse-view methods. The ablation with different depth estimators shows robustness to the choice of depth model.
- **Thorough experimental evaluation**: The paper evaluates on two standard benchmarks (LLFF and Mip-NeRF360), compares against a comprehensive set of baselines (7 NeRF-based and 6 3DGS-based), and includes detailed ablation studies on each component and hyperparameter. Performance gains are consistent across metrics.
- **Novel robustness metric**: IMR provides a distribution-level measure of Gaussian consistency across independent runs, moving beyond pixel-space metrics. While the metric’s utility requires further validation, it represents a thoughtful attempt to evaluate representation quality directly.

## Weaknesses

### Fatal

None.

### Major

1. **Modest absolute gains**: The PSNR improvements over competitive baselines (e.g., +0.59 dB over DropGaussian on LLFF 1/8, +0.35 dB on Mip-NeRF360) are consistent but relatively small. While statistically significant, the practical visual impact may be marginal in many cases. The paper would be strengthened by a discussion of perceptual significance or a statistical significance test.

2. **IMR metric lacks validation as a quality indicator**: The paper introduces IMR as a robustness metric but does not demonstrate that lower IMR is meaningfully correlated with better rendering quality or generalization. Table 3 shows that D²GS has both lower IMR and higher PSNR, but this could be coincidental. Without controlled experiments showing that IMR predicts rendering fidelity or generalisation to unseen views, its value as an evaluation tool remains unclear. The metric also depends on the chosen number of Gaussian samples and the entropic regularization, and no sensitivity analysis is provided.

3. **Dependence on monocular depth quality**: DAFE relies on a pretrained monocular depth estimator (DepthAnything V2) whose predictions may be inaccurate under sparse views or in textureless regions. Although the paper tests three different estimators, it does not discuss failure cases where erroneous depth masks could harm performance or how to detect/avoid such cases.

### Minor

- The global depth-stratified layering (tertile-based near/middle/far) is somewhat arbitrary and dataset-specific. While it performs well empirically, the paper does not analyze sensitivity to the choice of percentiles (why tertiles?).
- The design of the dropout score in Eq. (1) could be better justified. Since the goal is to suppress near-field Gaussians, it is counterintuitive that depth (distance from camera) enters positively (larger d → higher score), requiring the later layering multipliers to compensate. A simple redefinition (e.g., using inverse depth) might be cleaner.
- The IMR calculation uses a depth-stratified importance sampling to select ~10K Gaussians, but no analysis is provided on how sensitive IMR is to the sampling strategy or the sample size.
- The paper does not compare against recent feed-forward sparse-view methods like PixelSplat or MVSplat in the main tables, acknowledging them only in the related work. Including such comparisons would strengthen the evaluation, though the method is per-scene optimization, which is a different paradigm.

### Trivial

- None.

## Nice-to-Haves

- A study on the relationship between IMR and rendering performance across multiple methods (e.g., plot IMR vs. PSNR for all baselines) would help validate the metric as a useful signal.
- Discussion of failure cases where DAFE or DD-Drop might hurt (e.g., scenes with extremely sparse views where depth priors are unreliable, or scenes where overfitting and underfitting are less depth-correlated).

## Novel Insights

Beyond the paper’s own contributions, the key insight is that sparse-view 3DGS exhibits a spatially non-uniform failure pattern—not simply global overfitting—where near-field regions accumulate excessive Gaussians while far-field regions are starved. This observation suggests that any regularisation for sparse-view 3DGS should be spatially adaptive, a principle that could guide future method design. The use of optimal transport to compare 3DGS representations directly, rather than through rendered views, is also a novel perspective, though the practical value depends on further validation.

## Suggestions

- Perform a quantitative correlation analysis (e.g., Spearman rank correlation) between IMR and rendering metrics (PSNR, LPIPS) across multiple methods and random seeds to demonstrate that IMR captures meaningful robustness.
- For the depth-score in DD-Drop, consider using inverse depth or "closeness" (1/d) to make the dropout probability higher for near-field Gaussians, which would align more intuitively with the motivation and possibly simplify the design.
- Add a brief analysis of how the choice of depth percentile for DAFE masking affects performance on scenes with different depth distributions (e.g., indoor vs. outdoor).

## Score and Decision

**Score**: 7.0  
**Decision**: Accept

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>