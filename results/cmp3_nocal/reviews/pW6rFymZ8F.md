## Summary

EmbodiedMAE proposes a multi-modal masked autoencoder (RGB, depth, point cloud) trained on DROID-3D, a processed version of the DROID dataset with high-quality depth maps and point clouds extracted via ZED SDK. The model is evaluated across 70 simulated tasks (LIBERO, MetaWorld) and 20 real-world tasks on two robot platforms (SO100, xArm), showing strong results, particularly in multi-modal (RGBD, PC) settings. The two main contributions are the DROID-3D dataset and a practical 3D-capable visual backbone for robot manipulation.

## Strengths

1. **Extensive and ecologically valid evaluation.** The paper evaluates across 70 simulation tasks (LIBERO, MetaWorld) and 20 real-world tasks on two distinct robot platforms (low-cost SO100, high-precision xArm), using multiple policy backbones (RDT, ACT). This is among the more thorough evaluations for an embodied visual representation paper.

2. **DROID-3D dataset as a community resource.** Processing the full 76K trajectories of DROID through ZED SDK to produce temporally consistent metric depth maps and point clouds (~500 GPU-hours of processing) is a non-trivial engineering effort. The paper demonstrates that prior AI-estimated depth (e.g., SPA's CrocoV2-Stereo on 1/15 of DROID) is qualitatively less consistent. The dataset is a useful contribution independent of the model.

3. **Clear and large multi-modal gains.** On MetaWorld (Table 1), EmbodiedMAE-RGBD achieves 76.2% vs. DINOv2-RGBD's 54.4% (+21.8 pp); EmbodiedMAE-PC achieves 77.7% vs. DP3's 65.8% (+11.9 pp). The ACT ablation on LIBERO-Goal (Table 2) shows 90.8% (EmbodiedMAE-RGBD) vs. 82.2% (DINOv2-RGBD). These gaps are large and consistent.

4. **Demonstrated scaling behavior.** Performance improves monotonically from Small → Base → Large → Giant variants on both LIBERO (Figure 6) and MetaWorld, supporting the claim that the training paradigm scales with model capacity.

## Weaknesses

### Fatal
None.

### Major

1. **Missing comparison against MultiMAE, the method the architecture derives from.** The stochastic masking strategy (Section 2.2) explicitly follows Bachmann et al. (2022)/MultiMAE, and the cross-modal decoder (Section 2.3) uses the same attention-fusion mechanism. The core architecture is therefore MultiMAE applied to a new modality set (RGB+depth+point cloud instead of RGB+depth+semantic) with DINOv2 initialization. However, MultiMAE itself is never included as a baseline — not even retrained on the same DROID-3D data. Without this comparison, it is impossible to isolate whether strong results come from (a) the multi-modal MAE architecture per se, (b) the DROID-3D training data, (c) the specific modality choices, or (d) the DINOv2 initialization. This is the single most informative ablation the paper omits.

2. **Ablations skip the pre-training stage entirely.** Section 3.5 states explicitly: "Due to the prohibitive cost of ViT-Giant pre-training, our ablation studies focus on model distillation insights." Consequently, the paper never ablates: the contribution of each modality during pre-training, the stochastic masking strategy (choice of α, uniform vs. Dirichlet), the cross-modal decoder design, or training data scale. The distillation ablations are useful but do not address whether the multi-modal MAE pre-training design choices matter.

### Minor

1. **RGB-only results are overstated in the abstract and findings.** The abstract claims "consistently outperforms state-of-the-art vision foundation models." On MetaWorld (Table 1), EmbodiedMAE-RGB averages 73.0%, tying exactly with SPA at 73.0%, and SPA outperforms on the Medium difficulty level (62.8 vs. 60.4). The paper's default reference for "EmbodiedMAE" is the Large-scale RGB-only variant (line 175). The "consistent outperformance" claim holds cleanly only for multi-modal variants.

2. **LIBERO results reported only as learning curves without final aggregated success rates.** Figure 6 shows learning curves but no final success-rate table for LIBERO, making it difficult to assess improvement magnitudes over baselines quantitatively.

3. **Real-world evaluation uses 10 trials per task with no variance reporting.** Figure 8 reports single values based on 10 trials per task. For stochastic policy rollouts, this provides limited statistical power. No standard errors, confidence intervals, or trial-level results are reported.

4. **Depth quality comparison (Figure 2) is purely qualitative.** The paper asserts that DROID-3D depth is "superior and consistent" but provides no quantitative metrics (e.g., RMSE, temporal consistency scores). This weakens the evidence for DROID-3D's superiority.

5. **Re-coloring experiment (Figure 3, column 12) is over-interpreted.** The paper interprets localized color propagation as evidence that EmbodiedMAE "has implicitly learned object-level semantic segmentation." An alternative explanation is color propagation based on spatial proximity and depth/texture similarity without semantic understanding. The hedged wording ("suggests") partially addresses this.

6. **ACT ablation on MetaWorld (Table 3) compares EmbodiedMAE-PC only against DP3, missing baselines such as DINOv2-PC or SPA-PC.** This limits the informativeness of the ACT generalization experiment.

### Trivial

- The paper does not clarify whether the DP3 point cloud encoder (Section 2.2) is used with its original pre-trained weights or trained from scratch as part of EmbodiedMAE pre-training.

## Nice-to-Haves

- Compare against a variant trained on the original DROID (without ZED SDK 3D processing) to isolate the contribution of DROID-3D's improved depth quality.
- Include MultiMAE retrained on DROID-3D as a baseline (this is the most important addition; see Major weakness #1).
- Provide final aggregated LIBERO success rates in tabular form.
- Report variance (e.g., mean ± std across seeds) for real-world results.
- Provide quantitative metrics for the depth quality comparison (e.g., RMSE, temporal consistency).

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Methodological novelty is substantially thinner than the paper's framing suggests" / "described as if this is a novel design"** — REMOVED: The paper never uses the word "novel" for the architecture. It explicitly credits MultiMAE for the masking strategy ("Following Bachmann et al. (2022)") and frames the contribution as a framework applied to robot manipulation, not as a fundamentally new architecture. The missing MultiMAE baseline is retained as Major weakness #1.
- **"Claim about 3D VFMs underperforming MLPs lacks citation"** — REMOVED: The paper actually cites Ze et al. (2024) and Zhu et al. (2024) for this claim (line 15). The reviewer misread.
- **"PC-based policies underperform RGB-only on xArm, undercutting the paper's own motivation"** — REMOVED: The paper explicitly discusses this as a finding about sensor noise in real-world point clouds (lines 209-210), not as a contradiction of the multi-modal pre-training motivation.
- **"DROID-3D release plans not specified"** — REMOVED per policy: criticisms questioning release status/availability of cited resources are outside reviewer scope.
- **Generic framing criticisms** (e.g., "claim about consistent outperformance is defensible only if interpreted as multi-modal") — REMOVED: the specific factual inaccuracy about RGB-only results is retained as Minor weakness #1; the framing speculation is removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add MultiMAE (retrained on DROID-3D) as a baseline.** This is the single experiment that would most directly address the central methodological question. If EmbodiedMAE outperforms MultiMAE, that isolates the contribution of the DINOv2 initialization, point cloud modality, and distillation. If it does not, then the paper's primary contribution is the DROID-3D dataset, and the framing should be adjusted accordingly.

2. **Re-center the narrative on multi-modal results.** The paper's strongest evidence is in the RGBD and PC settings, where the gaps are large and consistent. Adjusting the abstract and findings to reflect this distinction would make the claims more defensible.

3. **Report variance for real-world results.** Even mean ± std over seeds would substantially strengthen believability.

4. **Provide LIBERO final success rates in tabular format** to allow quantitative comparison.

## Score and Decision

The paper contributes a valuable dataset (DROID-3D) and demonstrates that multi-modal MAE pre-training on high-quality robot 3D data yields strong representations for manipulation, particularly in multi-modal settings where the evidence is clear and large in magnitude. The evaluation scope is commendable and exceeds typical practice in this area.

However, the omission of MultiMAE as a baseline (the method the architecture derives from) and the absence of pre-training ablations leave the specific contribution of the paper's design choices unclear. The RGB-only results are overstated in the abstract. These are real gaps, but they do not invalidate the core empirical finding — that a multi-modal MAE trained on DROID-3D produces a strong backbone — nor diminish the dataset contribution.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>