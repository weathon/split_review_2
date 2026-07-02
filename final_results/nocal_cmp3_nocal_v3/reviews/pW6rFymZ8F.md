## Summary

The paper presents EmbodiedMAE, a multi-modal masked autoencoder that learns joint representations across RGB, depth, and point cloud modalities for robot manipulation. It contributes DROID-3D, a processed version of the DROID dataset with high-quality ZED SDK depth maps and point clouds (76K trajectories, 350 hours). The method adapts the MultiMAE stochastic masking strategy with point cloud as a third modality, uses a DINOv2-style ViT encoder, and distills a Giant model into smaller variants. Evaluation spans 70 simulation tasks (LIBERO, MetaWorld) and 20 real-world tasks on two robot platforms.

## Strengths

1. **DROID-3D dataset is a genuine community resource.** The paper identifies that existing embodied datasets (BridgeDataV2, RH20T) have poor or missing depth data, and that prior AI-based depth estimation (CrocoV2-Stereo, used by SPA) lacks temporal consistency. Processing the full 76K trajectories of DROID with ZED SDK — providing temporally fused, metric depth — is a substantial engineering effort (~500 hours processing) that will benefit the community. This is the paper's clearest contribution.

2. **Extensive evaluation scope.** 70 simulation tasks (40 LIBERO + 30 MetaWorld) plus 20 real-world tasks across two robot platforms (SO100, xArm) is genuinely broad. The decision to test on both a low-cost open-source platform and a higher-performance commercial arm makes the real-world results more informative than typical single-platform evaluations.

3. **Practical insight about RGBD vs. point cloud.** The observation (Section 3.4) that point-cloud-based policies underperform RGBD policies in practice due to sensor noise from object reflectivity and lighting variations is a useful, non-obvious finding that will inform future 3D robot learning system design.

4. **Cross-modal reconstruction visualizations.** Figure 3's re-coloring experiment — where altering one RGB patch changes only the corresponding object's color in the depth-to-RGB prediction — provides compelling qualitative evidence that the model learns object-level semantic alignment across modalities.

## Weaknesses

### Major

1. **The headline claim "consistently outperforms all baselines" is contradicted by the paper's own evidence.** Table 1 shows EmbodiedMAE RGB at **73.0%** average on MetaWorld — *identical* to SPA RGB at **73.0%**. The paper states "Unless otherwise specified, 'EmbodiedMAE' refers to the Large-scale, RGB-only variant" (line 175) and Finding 1 (line 177) claims it "consistently outperforms all baseline VFMs." This is factually incorrect for MetaWorld RGB-only. Additionally, on the xArm platform RGB-only setting, the paper itself notes "comparable performance to SOTA baselines" (Figure 8 caption, line 207), not outperformance. The overall performance of EmbodiedMAE is strong, but these cases show the "consistently outperforms" framing is overstated.

2. **No statistical significance or variance reported for any result.** No error bars, standard deviations, confidence intervals, or multiple-seed runs are presented. Real-world tasks use only 10 trials per task. With single-run evaluations and differences of 1-2 percentage points on MetaWorld (Easy: 81.8 vs 80.9; Medium: 60.4 vs 62.8 where EmbodiedMAE *loses*), the reader cannot determine whether reported advantages are meaningful or noise.

3. **LIBERO results lack final numerical values in the main text.** LIBERO results are presented exclusively through Figure 6 (learning curves), with no table of final success rates. Learning curves can be selectively shown at particular gradient steps; final converged numbers are the standard for comparison. A main-table summary of LIBERO final performance is needed to evaluate the central claim.

4. **No ablation isolating the contribution of multi-modal pre-training vs. the dataset vs. initialization.** The paper does not compare EmbodiedMAE against a single-modal RGB-only MAE trained on DROID-3D. Without this, the value of multi-modal pre-training cannot be separated from the benefits of DROID-3D data and DINOv2 initialization. The model is initialized from DINOv2 weights (line 71) despite being described as trained "from scratch" (line 85), making this isolation even more important.

### Minor

1. **Depth quality comparison is only qualitative.** Figure 2 compares depth quality visually but provides no quantitative metrics (e.g., temporal consistency error, relative accuracy against ground truth).

2. **Computational cost of pre-training is underreported.** The paper states "nearly 500 hours of processing time" for DROID-3D creation but does not report GPU-hours for EmbodiedMAE pre-training, making it difficult to assess efficiency claims.

3. **Inconsistency in "from scratch" claim.** Line 85 states the Giant model is trained "from scratch," but line 71 says the ViT is "initialize[d] directly from DINOv2 pre-trained weights." The decoder and point cloud components are indeed trained from scratch, but the encoder starts from DINOv2 weights.

### Trivial

None.

## Nice-to-Haves

- A single-modal RGB-only MAE ablation trained on DROID-3D would directly isolate the value of multi-modal pre-training.
- Reporting LIBERO final success rates in a main-text table.
- Adding error bars (or at minimum 3-seed results) to all simulation results.
- Quantifying depth quality improvement with a metric rather than only visual comparison.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"The DINOv2-RGBD baseline is constructed by the authors and likely underoptimized."** The paper is explicit that this baseline adds "a trainable depth branch" to DINOv2 and describes it as "naive" fusion. The claim being tested is whether naive 3D fusion degrades performance — a claim supported by prior work (Zhu et al., 2024 cited). The speculation that a "properly designed" variant might perform better is not grounded in the paper's evidence.

- **"The methodological novelty is substantially narrower than the paper frames it."** The paper clearly cites MultiMAE and builds on its masking strategy. The contribution lies in the system: combining MultiMAE-style masking with point cloud modality (via DP3 encoder), DINOv2 architecture, distillation pipeline, and large-scale pre-training on the newly created DROID-3D dataset. Whether this constitutes sufficient novelty is a judgment call, but the paper does not overclaim architectural breakthrough — it frames EmbodiedMAE as a unified representation learning framework.

- **"Comparison to Octo / π0."** The paper's contribution is a vision backbone; Octo and π0 are full policy-level VLA models. Comparing at the vision-backbone level would require swapping their visual encoders into the same policy, which is outside the paper's scope.

- **"Language compatibility limitation."** The paper already acknowledges in the conclusion that EmbodiedMAE "does not natively support language instruction as input" (line 242) and discusses this as a future direction.

- **"DROID-3D release status."** The paper states the dataset "will be released upon publication" (line 53). This is standard for submissions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Revise the core claim: replace "consistently outperforms all baselines" with a more precise characterization. The method shows advantages on most benchmarks and particularly with multi-modal inputs, but the RGB-only variant ties with SPA on MetaWorld and is comparable on xArm.
2. Add error bars or multi-seed results across the evaluation, even if only for a subset of experiments. Without variance estimates, small performance differences are uninterpretable.
3. Include a single-modal MAE ablation trained on DROID-3D to isolate the contribution of multi-modal pre-training from the dataset contribution.
4. Reveal final LIBERO success rates in a main-text table (not only as learning curves).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>