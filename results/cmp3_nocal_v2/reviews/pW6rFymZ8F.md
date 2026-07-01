## Summary

EmbodiedMAE presents a unified 3D multi-modal representation learning framework for robot manipulation. It contributes (1) DROID-3D, a large-scale augmentation of the DROID dataset with high-quality depth maps and point clouds (76K trajectories, 350 hours), and (2) a multi-modal masked autoencoder trained on DROID-3D using stochastic masking, cross-modal decoding, and teacher-student distillation. The model is evaluated across 70 simulation tasks (LIBERO, MetaWorld) and 20 real-world tasks on two robot platforms, outperforming several baseline vision foundation models.

## Strengths

1. **DROID-3D is a substantial resource contribution.** The paper processes the full DROID dataset using ZED SDK temporal fusion and AI-augmented enhancement, producing synchronized RGB, depth maps, and point clouds at scale (76K trajectories, 350 hours). This is significantly more comprehensive than prior efforts such as SPA, which processed only ~1/15 of DROID with estimated depth. The 500 hours of processing time reflects genuine engineering investment.

2. **Comprehensive evaluation.** The paper evaluates across 40 LIBERO tasks, 30 MetaWorld tasks, and 20 real-world tasks on two distinct robot platforms (SO100 low-cost, xArm high-performance). This breadth is more thorough than typical VFM-for-robotics evaluations, and the inclusion of both a low-cost and a high-performance robot demonstrates robustness across hardware regimes.

3. **Well-motivated stochastic masking design.** The Dirichlet-based masking strategy with symmetric distribution avoids modality bias and forces cross-modal inference. The cross-attention decoder with shared transformer components is computationally efficient (~3× savings). Qualitative results (Figure 3, re-coloring experiment) provide reasonable evidence of object-level semantic understanding.

## Weaknesses

### Fatal

None.

### Major

1. **Data-vs-architecture confound is not cleanly resolved.** EmbodiedMAE is pre-trained on DROID-3D (in-domain robot manipulation data), while most baselines (DINOv2, SigLIP, R3M, VC-1) are pre-trained on out-of-domain data (web images, static scenes, egocentric video). The one baseline also trained on DROID data (SPA, ~1/15 subset with AI-estimated depth) ties EmbodiedMAE-RGB on the MetaWorld average (73.0 vs. 73.0) and lags modestly elsewhere. The paper lacks a controlled experiment training a standard MAE or ViT on the same DROID-3D data, which would isolate whether the gains come from the multi-modal architecture or simply from large-scale in-domain pre-training. SPA provides partial control, but the confound remains unresolved for the core architectural claim.

2. **No error bars, confidence intervals, or multiple-seed results.** Every numerical result (Tables 1–3, Figures 6, 8) is reported as a single point estimate. There is no mention of the number of policy training seeds, no standard deviations, and no confidence intervals. On MetaWorld, EmbodiedMAE-RGB and SPA-RGB both average 73.0 with per-difficulty-level differences of 0.9, −2.4, and 2.0 percentage points — differences too small to interpret without variance estimates. Real-world tasks use only 10 trials each. This makes it impossible for the reader to assess whether reported improvements are statistically reliable.

3. **Ablation results are in tension with the paper's central framing.** The ablation on masking ratio (Section 3.5) shows that configurations with "≥ 100% masking" (i.e., no MAE reconstruction loss, only feature alignment/distillation) perform *better* than configurations that include the MAE loss. The paper states "ratios ≥ 100% perform better, suggesting feature alignment's predominant role." While the Giant teacher model is pre-trained with MAE loss, this result means that during distillation — the procedure that produces the models actually deployed for downstream tasks — the MAE reconstruction loss is not the primary driver of performance. The paper's title, abstract, introduction, and method section consistently emphasize the multi-modal MAE as the core contribution, yet the evidence suggests feature alignment (distillation) dominates. The paper would benefit from reframing or explaining this tension convincingly.

### Minor

1. **No ablation or analysis of the Dirichlet concentration parameter α.** The masking strategy uses α=1 (uniform) by default, with the stated rationale of avoiding modality bias. No analysis is provided to justify this choice or explore whether non-uniform masking could improve performance.

2. **Initialization of new modalities is not discussed.** The ViT encoder is initialized from DINOv2 pre-trained weights (an RGB-only model). The paper does not explain how the depth and point cloud patchifiers/embeddings are initialized, which could influence the learned cross-modal representations.

3. **Limitations section is too brief.** Only one limitation is acknowledged (no native language support). Other relevant limitations are omitted: reliance on proprietary ZED SDK software, the substantial computational cost of the data processing pipeline (500 hours), and the restriction of evaluation to tabletop manipulation (not mobile manipulation or navigation).

### Trivial

1. **Table 1 column headers appear duplicated** in the extracted text, making the intended layout harder to parse at a glance.

## Nice-to-Haves

- An ablation of the Dirichlet α parameter to justify the uniform default.
- A discussion of how depth and point cloud branches are initialized relative to the DINOv2-initialized RGB branch.
- Including the full ablation table (currently deferred to the appendix) in the main paper would improve readability.

## Removed Points

These points were flagged during review synthesis and removed with justification:

1. **"DINOv2-RGBD comparison is unknown / potentially unfair."** Removed per hard rule: the implementation details exist in Appendix A.3, which was stripped by the parser but is present in the original submission. The full submission contains this information.

2. **"Introduction does not explain why 3D VFMs underperform."** Removed: this is a literature-cited empirical observation that the paper's subsequent method addresses. A deep causal theory is not required.

3. **"PC-based policies contradict the paper's motivation about 3D being critical."** Removed: the paper discusses this finding honestly and with appropriate nuance, acknowledging that modality quality matters. This is not a weakness.

4. **"Table 4 ablation table is in the appendix."** Removed per hard rule about missing appendix content.

5. **"The ACT ablation is too thin."** Removed: the ACT results are presented as a supplementary check of generalizability, not a primary claim. Limiting to one suite and one modality is a reasonable scope choice for a supplementary experiment.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Run a controlled experiment** training a standard ViT-MAE or DINOv2 from scratch on DROID-3D. This is the single most informative control: it disentangles the architecture contribution from the data contribution. If EmbodiedMAE outperforms this control, the architecture is validated. If not, the paper's contribution is better framed around the dataset and distillation procedure rather than the multi-modal MAE architecture.

2. **Report variance estimates** across at least 3 policy training seeds for all simulation benchmarks. This is essential for making claims of competitive advantage credible, especially where differences between methods are small.

3. **Acknowledge the distillation-dominance result in the framing.** If the MAE reconstruction loss is dispensable during distillation, either explain why MAE pre-training of the teacher remains critical despite this, or reframe the contribution around the distillation procedure with MAE pre-training as a supporting step.

4. **Add the DINOv2-RGBD comparison details** to the main text, given how prominently the "naive depth integration degrades DINOv2" claim features in the argumentation.

5. **Expand the limitations section** to cover computational cost of data processing, reliance on proprietary SDK, and scope constraints (tabletop manipulation only).

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>