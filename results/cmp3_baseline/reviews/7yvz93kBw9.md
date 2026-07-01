## Summary

This paper addresses the instability and quality degradation of 3D Gaussian Splatting (3DGS) under sparse-view conditions. The authors identify two failure modes—overfitting in near-field regions with excessive Gaussian density and underfitting in far-field regions with insufficient coverage—and propose a unified framework D²GS. It consists of a Depth-and-Density Guided Dropout (DD-Drop) that adaptively masks redundant Gaussians, and a Distance-Aware Fidelity Enhancement (DAFE) module that strengthens supervision in distant areas using monocular depth priors. Additionally, the paper introduces an Inter-Model Robustness (IMR) metric based on optimal transport to evaluate the stability of learned Gaussian distributions across independent training runs. Experiments on LLFF and Mip-NeRF360 datasets show consistent improvements over several baselines.

## Strengths

- **Clear problem identification and motivation.** The paper provides empirical evidence (Figure 1) showing that sparse-view 3DGS leads to spatial imbalance: too many Gaussians near the camera and too few in distant regions. This analysis directly motivates the two complementary modules.
- **Novel adaptive dropout strategy.** DD-Drop goes beyond uniform dropout (used in DropGaussian) by combining local density and depth scores with global depth-based layering. This spatially-aware regularization is well-motivated and ablation studies confirm its effectiveness.
- **Introduction of a robustness metric for 3DGS.** The IMR metric, grounded in 2-Wasserstein distance and optimal transport, provides a principled way to quantify the stability of learned 3D representations. This is a valuable addition beyond standard image-space metrics.
- **Thorough experimental evaluation.** The method is compared against multiple NeRF-based and 3DGS-based baselines on two standard datasets. Ablation studies systematically validate each component and hyperparameter choices. The inclusion of IMR comparisons further strengthens the evaluation.

## Weaknesses

### Fatal
None.

### Major
- **Incremental gains over strong baselines.** While D²GS achieves the best numbers, the improvements over the closest competitor (DropGaussian) are modest: +0.59 dB PSNR on LLFF 1/8, +0.55 dB on LLFF 1/4, and +0.35 dB on Mip-NeRF360. The gains are consistent but small, raising the question of practical significance.
- **Limited validation of the IMR metric.** The IMR is introduced as a new evaluation tool, but the paper does not demonstrate that it correlates with rendering quality or that it provides insights beyond existing metrics. The metric is only reported for four methods on LLFF; no analysis of its sensitivity, reliability, or relationship to PSNR/SSIM is provided. The first-order Taylor approximation of the Bures metric (Eq. 11) is used without validation that it does not distort the distance measure.
- **Dependence on external depth priors.** DAFE relies on a monocular depth estimator (DepthAnything V2). While the ablation shows robustness across different estimators, the quality of the depth prior directly affects the mask and thus the supervision. In scenes where monocular depth is unreliable, the benefit may diminish. The paper does not discuss failure cases or limitations of this dependency.

### Minor
- **The IMR formulation (Eq. 14) is somewhat ad-hoc.** The choice of ln(∑S_ij² / ∑S_ij) is not justified; a simple average Wasserstein distance would be more interpretable. The authors should explain why this particular form is preferred.
- **Computational overhead is not discussed.** DD-Drop requires k-nearest neighbor density estimation and per-Gaussian score computation, and IMR involves solving an optimal transport problem (even with sampling). The paper does not report training time or memory cost compared to baselines.
- **The analysis of failure modes is qualitative.** The claim of "systematic analysis" is based on counting Gaussians in two hand-picked regions (Figure 1). A more rigorous analysis (e.g., per-depth-bin density statistics across the whole scene) would strengthen the motivation.

### Trivial
- The term "AVGE" is used without definition in the main text; it is defined in the caption of Table 1 but could be clarified earlier.

## Nice-to-Haves
- A study showing how IMR correlates with rendering quality (e.g., scatter plot of IMR vs. PSNR across many runs) would greatly strengthen the metric's credibility.
- An analysis of where D²GS still fails (e.g., scenes with highly reflective surfaces or extreme depth ranges) would provide a balanced view.
- Reporting training time and GPU memory would help practitioners assess the practical cost.

## Novel Insights

Beyond the paper's own contributions, the key insight is that sparse-view 3DGS suffers from a spatial imbalance that can be addressed by coupling local density-aware regularization with global depth-based supervision. The idea of using optimal transport to compare Gaussian distributions across independent training runs is a novel way to assess representation stability, though its practical utility remains to be fully demonstrated.

## Suggestions
- Validate the IMR metric by showing its correlation with rendering quality variance or with the consistency of novel views across runs.
- Provide a more rigorous analysis of the failure modes, e.g., by plotting Gaussian density as a function of depth for dense vs. sparse training.
- Discuss the computational overhead of DD-Drop and IMR, and consider providing a runtime comparison.

## Score and Decision

The paper makes a solid contribution with a well-motivated method and thorough experiments. The weaknesses (incremental gains, limited validation of IMR, external depth dependency) are not fatal but prevent the paper from being a strong accept. I recommend acceptance.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>