Now let me write the final consolidated review.

## Summary

D²GS addresses overfitting in near-field and underfitting in far-field regions for sparse-view 3D Gaussian Splatting through two modules: a Depth-and-Density Guided Dropout (DD-Drop) strategy that adaptively masks Gaussians based on local density and camera distance, and a Distance-Aware Fidelity Enhancement (DAFE) module that strengthens supervision in distant regions using monocular depth priors. The paper also proposes Inter-Model Robustness (IMR), a metric based on optimal transport over Gaussian mixtures to quantify distribution-level stability across training runs.

## Strengths

1. **Well-motivated problem analysis with concrete evidence (Section 3.1, Figure 1).** The paper identifies two distinct failure modes — near-field overfitting (11,450 vs 6,112 Gaussians, comparing sparse-view to dense-view) and far-field underfitting (3,082 vs 5,224) — and supports them with countable evidence. This diagnosis goes beyond the generic "sparse views are hard" observation found in prior work.

2. **Method design is tightly coupled to the identified problems.** DD-Drop suppresses near-field overfitting through density-guided dropout; DAFE compensates for far-field underfitting through targeted supervision. The ablation (Table 4) confirms each module contributes positively, and the ablation is more thorough than is typical (Tables 4–6 cover hyperparameter sensitivity, depth estimator choice, and component contributions).

3. **Consistent improvement across datasets and metrics.** D²GS outperforms all baselines on both LLFF and MipNeRF360 across PSNR, SSIM, LPIPS, and AVGE. The improvement is directional (0.35–0.92 dB PSNR depending on dataset and resolution) and holds against both NeRF-based and 3DGS-based methods.

4. **The IMR metric addresses a genuine gap.** Figure 3 convincingly shows PSNR ranging 14.62–18.63 across runs for the same method, motivating a distribution-level robustness metric. The use of optimal transport over Gaussian mixtures is a principled foundation.

## Weaknesses

### Fatal
None.

### Major

1. **No statistical significance or variance is reported for any main result, despite the paper's own emphasis on training instability (Figure 3).** Tables 1, 2, 4, and 5 report only point estimates. The paper's Figure 3 shows PSNR varies by ~4 dB across runs for a baseline method, yet the reported pairwise gains (0.35–0.92 dB) are well within that range. Without variance over multiple seeds (3–5 runs), the reader cannot determine whether the improvements are robust or within run-to-run noise. The IMR results (Table 3, from 10 runs) partially address stability but do not establish significance for the primary PSNR/SSIM comparisons. This gap is self-consistent: a paper that motivates a new metric by highlighting instability should itself control for variance in its core comparisons.

### Minor

2. **Design tension between the local depth score and global layering in DD-Drop.** In Eq. (1), the local depth score d̃_i assigns *higher* values to farther Gaussians, which increases their dropout probability — the opposite spatial direction from the stated goal (suppressing near-field overfitting). The global layering (Eq. 2) then applies λ_far = 0.3 to correct this by *decreasing* far-field dropout. The paper claims the two mechanisms "facilitate fine-grained local tuning while preserving global structural coherence" but never acknowledges that the local depth score component pulls against the layering's intent. The net behavior is sensible (the global layering dominates numerically), but the design incoherence is not discussed. The ablation (Table 4) corroborates this: adding the depth score to density+layering yields only +0.15 dB (21.17 vs 21.02), consistent with the two mechanisms being partially redundant or at odds.

3. **IMR metric has limitations that are not adequately discussed.**

   a) **Depth-stratified importance sampling introduces a confound.** The sampling strategy oversamples far-field Gaussians because "far-field Gaussians are more prone to noise and instability," but this directly favors methods (like D²GS with DAFE) that specifically improve far-field stability. The resulting IMR values conflate overall distribution-level robustness with targeted improvements in oversampled regions. The paper does not discuss this bias.

   b) **IMR conflates "consistently good" with "consistently bad."** A method that always converges to a poor local minimum would score well on IMR. The claim that IMR "provides a more direct evaluation of 3D representation quality" overstates what a consistency-only metric captures (standard rendering metrics remain necessary).

   c) **No variance is reported for IMR itself** (Table 3), even though it is computed from 10 runs and bootstrap confidence intervals would be straightforward.

4. **Missing ablation cell.** Table 4 omits a "Density Score only" condition (no Depth Score, no Layering). The closest existing row blends density score with layering (Row 2, PSNR 21.02), making it impossible to isolate the standalone contribution of the density score from the layering mechanism. Adding this cell would cleanly separate the two design choices.

5. **Depth-threshold specification is underspecified for reproducibility (Section 3.2).** The paper says thresholds D_near and D_middle are "determined by the first and second tertiles of the depth distribution" but does not specify (a) what distribution this refers to (SfM point cloud depths? Gaussian centers? monocular depth maps?), (b) whether computed per-scene, per-view, or globally, nor (c) whether fixed at initialization or recomputed during training.

### Trivial

6. The conclusion describes gains as "significant" without tempering this with the modest magnitude (0.35–0.92 dB) or the method's dependence on external monocular depth priors.

## Nice-to-Haves

- Compare IMR against simpler alternatives (standard deviation of PSNR across runs, mean pairwise Chamfer distance between Gaussian centers) so readers can interpret what the metric adds.
- Include LoopSparseGS, FSGS, and DNGaussian in the IMR comparison (Table 3) for a more complete picture.

## Removed Points

- **First-order Taylor expansion validity range.** The critic noted the Bures metric approximation (Eq. 11) may be poor for Gaussians with very different covariances. The paper defers the derivation to Appendix A, which the parser strips; the discussion may exist in the full submission. Removed per rule on appendix content.
- **IMR formulation being "ad-hoc."** The paper explicitly motivates Eq. (14) ("To specifically penalize model pairs with large divergence"). The ratio of sum-of-squares to sum-of-values is a standard dispersion measure. This characterization is too strong.
- **"Modest improvement margin" as a standalone weakness.** The critic noted gains of 0.35–0.92 dB are modest. This is a factual observation about magnitude but not a flaw in the method — consistent directional improvement across multiple metrics and datasets is a genuine result. The framing concern is folded into Trivial weakness #6 about the conclusion.
- **Criticisms about "Missing Appendix" or "Missing References."** These are removed per hard rules (parser strips these sections; all references exist in the original submission).

## Novel Insights

None beyond the paper's own contributions.

**Calibration.** The following anchor papers from the human-review corpus were used for score calibration:

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| GeoGS3D (single-view 3D reconstruction with GS) | 3.40 | R1 | Lower contribution and weaker experiments than D²GS |
| FreeSplatter (pose-free sparse-view 3DGS) | 5.00 | R1 | Comparable goal area but had novelty/fairness issues; D²GS is cleaner but has variance gap |
| RAIN-GS (relaxing initialization for 3DGS) | 5.75 | R1/R2 | Similar-level contribution; D²GS has better ablation but RAIN-GS had more consistent evaluation |
| Hi-Gaussian (hierarchical GS for single-view) | 5.75 | R2 | Comparable scope; D²GS has more thorough ablation |
| HiSplat (hierarchical GS for sparse-view) | 6.00 | R2 | Clean borderline-accept; D²GS comparable but missing variance reporting |
| NoPoSplat (pose-free sparse 3DGS) | 8.00 | R1 | Stronger contribution (feed-forward, pose-free); D²GS is a different category (per-scene optimization) |
| VBGS (variational Bayes GS) | 4.50 | R2 | Weaker experimental validation than D²GS |
| Injecting Inductive Bias to 3DGS | 5.75 | R1/R2 | Similar contribution level; noted small gains and training slowdown |

**Round 1 bracket:** [4.5, 6.0]. **Narrowing:** Compared against RAIN-GS (5.75), Hi-Gaussian (5.75), and HiSplat (6.00). D²GS has a well-motivated problem analysis and thorough ablation comparable to this band, but the absence of variance reporting — despite the paper's own emphasis on instability — is a distinctive gap that lowers confidence. **Final score:** 5.5, placing it between the reject-tier papers (~4.5–5.75) and the accept-tier paper HiSplat (6.00).

## Suggestions

1. **Report mean ± std over 3–5 seeds** for all main quantitative results (Tables 1, 2, 4, 5). This directly addresses the tension between the paper's emphasis on instability and the use of point estimates.
2. **Clarify the interaction between the local depth score and global layering** in Section 3.2. Either explain why the opposing pull of the two sub-mechanisms is deliberate, or simplify by removing the depth term from the local score (the ablation suggests it contributes little beyond density+layering).
3. **Specify the depth distribution source** used for tertile-based partitioning in Section 3.2 (SfM points, Gaussian centers, or depth maps; per-scene or per-view; static or recomputed).
4. **Add the missing ablation cell** (Density Score only, no Depth Score, no Layering) to Table 4.
5. **Report IMR with confidence intervals** (e.g., bootstrap over runs) and discuss the bias introduced by depth-stratified importance sampling.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>