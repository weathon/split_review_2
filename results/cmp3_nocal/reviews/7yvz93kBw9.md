## Summary

This paper identifies two failure modes in sparse-view 3DGS (near-field overfitting and far-field underfitting) and proposes D²GS, comprising two modules: Depth-and-Density Guided Dropout (DD-Drop) for adaptive regularization of near-field Gaussians, and Distance-Aware Fidelity Enhancement (DAFE) for targeted supervision of far-field regions. The paper also introduces Inter-Model Robustness (IMR), a Wasserstein-distance-based metric for evaluating the stability of learned 3D Gaussian distributions across independently trained models. Experiments on LLFF and MipNeRF360 show consistent improvements over prior methods.

## Strengths

1. **Empirically grounded problem diagnosis (Section 3.1, Figure 1).** The paper identifies two concrete failure modes — near-field overfitting and far-field underfitting — with quantitative evidence (11,450 vs. 6,112 Gaussians in near-field; 3,082 vs. 5,224 in far-field, comparing sparse to dense training). This diagnosis is the paper's strongest contribution and genuinely clarifies why sparse-view 3DGS degrades.

2. **Clean two-part method design.** DD-Drop and DAFE map directly onto the two diagnosed failure modes (overfitting → dropout, underfitting → extra supervision). The ablation in Table 4 confirms each component adds positive value and their combination is better than either alone.

3. **Comprehensive hyperparameter ablations (Table 5).** The paper systematically tests the key parameters of both modules (dropout rate range, depth/density weighting, mask threshold, DAFE loss weight), lending credibility to the reported default configuration.

## Weaknesses

### Fatal
None.

### Major

1. **Missing multi-run statistics for main quantitative results (Tables 1 and 2).** The paper's central claim of "significant improvement" is supported only by single-point PSNR/SSIM/LPIPS estimates. Section 3.4 and Figure 3 (left) themselves demonstrate that training the same algorithm can produce substantial PSNR variation across runs (the figure shows values ranging from 14.62 to 18.63, a ~4 dB spread). Yet the reported gains over DropGaussian (0.35–0.59 dB PSNR) are an order of magnitude smaller than this documented variance. Without error bars or multi-run statistics on the main results, the reader cannot assess whether the improvements are statistically meaningful or reflect favorable run selection. This is partially mitigated by: (i) the consistency of gains across all metrics and both datasets, (ii) the monotonic improvement in the ablation study (Table 4), and (iii) the IMR metric (Table 3) which does report multi-run statistics. However, the inconsistency — reporting variance for IMR but not for the primary benchmarks — is a significant evidential gap that should be addressed.

2. **IMR metric is proposed as a contribution but never validated.** The paper lists IMR as a third contribution (abstract and introduction) but provides no evidence that it measures what it claims: no correlation analysis between IMR and established image metrics, no comparison to simpler stability baselines (e.g., variance of PSNR across runs), and no interpretation of what a numerical difference like 3.039 vs. 3.162 means in practical terms. IMR is also only reported on LLFF (Table 3), not on MipNeRF360, despite being presented as a general metric. The technical construction (Wasserstein + OT on GMMs) is sound, but without any validation, IMR remains an interesting proposal rather than a demonstrated useful contribution.

### Minor

1. **DD-Drop design tension not analyzed.** The local dropout score S_i assigns higher scores to Gaussians farther from the camera (the normalized depth score d̃_i is larger for deeper Gaussians), while the global mechanism applies attenuation factors (λ_far=0.3) that reduce dropout probability for far-field Gaussians. The net effect on far-field Gaussians depends on whether the 0.3× attenuation outweighs the higher base score from depth. The paper does not analyze this trade-off, report the empirical distribution of dropout probabilities across depth bins, or justify why two counteracting forces are preferable to a simpler design (e.g., using only density for scoring and only depth for attenuation).

2. **Limited evaluation scope.** The method is evaluated on two datasets (LLFF, MipNeRF360) at 3-view and 6-view settings, with no 2-view evaluation (the hardest sparse-view regime). The method is only built on top of DropGaussian; no experiments test DD-Drop or DAFE in other 3DGS backbones (e.g., FSGS, CoR-GS) to demonstrate generality. There is also no runtime, memory, or convergence analysis despite the added computational cost of KNN density estimation and monocular depth inference.

3. **No limitations discussion.** The conclusion (Section 5) does not discuss when the method might fail — e.g., scenes with inaccurate monocular depth priors, cases where depth-based masking is too aggressive, or known limitations of the IMR metric.

4. **Minor inconsistency in DAFE threshold reporting.** The text (line 245) states "selecting the top 5% of the farthest depth values yields the best performance," but Table 5 shows τ=10% achieves PSNR 21.26 vs. τ=5% at 21.25 — a negligible difference, but the text claims a specific best value that the table does not fully support.

### Trivial
None.

## Nice-to-Haves
- Report multi-run statistics (mean ± std) for the main tables (Tables 1, 2) — this single change would significantly strengthen the paper's central claim.
- Validate IMR by showing it correlates with PSNR variance across runs, or that it surfaces stability differences that image-space metrics miss.
- Add cross-backbone experiments testing DD-Drop and DAFE in other sparse-view 3DGS frameworks.
- Discuss how DD-Drop relates to the co-adaptation perspective in Chen et al. (2025), which is cited but not compared.
- Acknowledge and analyze the tension between depth-based scoring and depth-based attenuation in DD-Drop.

## Removed Points
These points are flagged to be removed; treat them with caution:
- "The k in k-nearest neighbors for density estimation is never specified" — removed per hard rule classifying undisclosed hyperparameters as nitpicks.
- "The Bures metric approximation conditions not noted in main text (paper points to appendix)" and "IMR depth-stratified importance sampling underspecified" — removed per hard rule about missing appendix content (appendix is stripped by the parser; these details likely appear there).
- "The progressive dropout description is just a global linear warmup" — semantic nitpick about terminology, removed.
- "Related work omission of comparison to Chen et al. (2025)" — Chen et al. (2025) is cited in the paper; requesting deeper discussion is a suggestion, not a weakness.
- "Figure 3 left shows ~4 dB PSNR variance for DropGaussian" — the paper attributes the figure to "the previous method" generally, not DropGaussian specifically; the broader concern about missing error bars is retained in Major weakness #1.
- "The IMR formula is scale-dependent" — the Wasserstein distances have meaningful units; scale dependence may be by design. This is an observation, not a verified flaw.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Add error bars / standard deviations to Tables 1 and 2 by running each method with at least 5 random seeds.
- Strengthen IMR validation: correlate IMR values with multi-run PSNR variance across methods.
- Include at least one cross-backbone experiment (e.g., applying DD-Drop + DAFE to FSGS or CoR-GS) to demonstrate generality.
- Add a brief limitations paragraph to the conclusion.
- Report IMR on MipNeRF360 for completeness.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>