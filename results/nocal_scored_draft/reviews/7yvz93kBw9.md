Now let me compose the final review.

## Summary

This paper proposes D²GS, a method for sparse-view 3D Gaussian Splatting that addresses two identified failure modes: overfitting in near-field regions (excessive Gaussian density) and underfitting in far-field regions (insufficient Gaussian coverage). The method introduces a Depth-and-Density Guided Dropout (DD-Drop) mechanism that adaptively regularizes Gaussians based on their spatial context, and a Distance-Aware Fidelity Enhancement (DAFE) module that adds targeted supervision in distant regions using monocular depth priors. The paper also proposes an Inter-Model Robustness (IMR) metric to evaluate the stability of learned Gaussian distributions across independent training runs. Experiments on LLFF and Mip-NeRF360 show consistent improvements over baselines.

## Strengths

- **Clear, well-motivated problem analysis with concrete quantitative evidence.** Section 3.1 identifies two failure modes (near-field overfitting with 11,450 vs. 6,112 Gaussians; far-field underfitting with 3,082 vs. 5,224 Gaussians) supported by specific counts from the paper. This gives the method a clean conceptual foundation.

- **DD-Drop module is thoughtfully designed.** The combination of a local continuous scoring function (normalized depth + density) with a global discrete layering mechanism (attenuation coefficients by depth tertile) provides principled adaptive regularization, balancing fine-grained spatial adaptation with coarse scene-level structure.

- **Consistent improvements across two datasets and multiple metrics.** The method outperforms several strong baselines (DropGaussian, CoR-GS, LoopSparseGS) on LLFF and Mip-NeRF360 across PSNR, SSIM, LPIPS, and AVGE. The gains over DropGaussian (~0.6 dB on LLFF 1/8, ~0.35 dB on Mip-NeRF360) are modest but consistent.

- **Well-structured ablation study.** Table 4 progressively adds components, and the hyperparameter sweeps in Table 5 provide useful sensitivity analysis for key design choices.

## Weaknesses

### Fatal
None.

### Major

- **No variance or error bars reported for main quantitative results (Tables 1 and 2).** The paper's own Figure 3 demonstrates large run-to-run variance (PSNR 14.62–18.63) for prior methods under sparse views, yet the headline PSNR/SSIM/LPIPS numbers in Tables 1 and 2 are single values with no indication of multiple runs, standard deviation, or statistical significance. The ~0.59 dB PSNR improvement over DropGaussian on LLFF could easily fall within run-to-run noise, and without variance estimates, the reader cannot evaluate whether the reported improvements are real or an artifact of a favorable seed. This is the paper's most significant evidential gap.

### Minor

- **IMR is overclaimed as evaluating "representation quality."** The introduction states IMR provides "a more direct evaluation of 3D representation quality," but the metric actually measures consistency/reproducibility across independent training runs. Consistency and quality are orthogonal — a method that always outputs the same blurry blob would have excellent IMR but poor quality. The method section appropriately frames IMR as measuring robustness/stability (Section 3.4 title: "Inter-Model Robustness Assessment"), but the intro claim goes beyond what the evidence supports.

- **The "systematic analysis" of failure modes (Contribution 1) is overstated.** Section 3.1 examines only two hand-selected bounding boxes from a single scene. While this provides a useful motivating observation, calling it a "systematic" or "comprehensive" analysis is not justified.

- **Missing implementation details affecting reproducibility.** (a) The k-NN density estimation (Section 3.2) does not specify k or the distance metric. (b) The source of the depth distribution for computing tertiles (initial SfM point cloud vs. current Gaussians at each training step) is not stated. (c) The DAFE mask threshold (Equation 4) uses monocular depth with unknown scale/shift, and the paper does not discuss sensitivity to this ambiguity.

### Trivial
None.

## Nice-to-Haves

- Include runtime/computational cost comparison showing overhead of monocular depth estimation, k-NN density estimation, and IMR computation relative to DropGaussian.
- Analyze the interaction between DD-Drop and DAFE beyond the additive ablation in Table 4.
- Validate IMR against rendering quality by showing whether lower IMR correlates with higher PSNR across methods.
- Add a limitations section discussing where D²GS still struggles (e.g., very sparse 2-view settings, scenes with extreme depth ranges).

## Removed Points

These points were flagged for removal from the harsh critic input; treat with caution.

1. **"Opacities can exceed 1.0 in IMR weighting"** — The paper specifies α as "opacity for rendering," which in standard 3DGS is sigmoided to (0,1). The concern reflects a misunderstanding of the rendering pipeline.

2. **"Missing baselines on Mip-NeRF360"** — The critic questions why the full baseline set was not carried over, but this is an unanswered question, not a demonstrated weakness. The paper reports results for the most relevant 3DGS-based competitors.

3. **"DAFE contributes only +0.18 dB / affects only 5% of pixels"** — The paper accurately attributes gains jointly to DD-Drop and DAFE. The ablation (Table 4) clearly shows relative contributions. This is a descriptive observation, not a flaw.

4. **Various sub-points about IMR formula choice, sensitivity to ε, computational cost** — These are speculative concerns not grounded in an error in the paper. Sensitivity analysis of every engineering choice in a newly proposed metric is a nice-to-have, not a required weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Report all main results (Tables 1 and 2) as means and standard deviations over multiple runs (ideally the same 10 runs used for IMR). Without this, the core quantitative claims cannot be properly evaluated.
- Clarify whether IMR measures representation quality or training reproducibility, and adjust claims in the introduction accordingly.
- Add the missing implementation details: k for k-NN, distance metric, source of depth distribution for tertile computation, and discussion of monocular depth scale ambiguity for the DAFE threshold.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>