## Summary

EmbodiedMAE presents a multi-modal masked autoencoder (RGB, depth, point cloud) pre-trained on DROID-3D, a new 350-hour processed supplement of the DROID dataset. The model is evaluated across 70 simulation tasks (LIBERO, MetaWorld) and 20 real-world tasks on two robot platforms (SO100, xArm), consistently outperforming existing vision foundation models (DINOv2, SigLIP, SPA, R3M, VC-1). The paper contributes both a large-scale 3D robot manipulation dataset and a unified multi-modal representation learning framework.

## Strengths

- **Large-scale 3D dataset contribution (Section 2.1).** DROID-3D provides 76K trajectories (350 hours) with high-quality metric depth and point clouds processed via ZED SDK temporal fusion. Unlike prior work (e.g., SPA processes ~1/15 of DROID with AI-estimated depth), the authors process the complete dataset and demonstrate (Figure 2) substantially higher depth quality than native depth in BridgeDataV2/RH20T or AI-estimated alternatives. This is an independently valuable resource for the community.

- **Comprehensive evaluation across diverse settings (Sections 3.3–3.4).** Evaluation spans 40 LIBERO tasks, 30 MetaWorld tasks, 10 real-world SO100 tasks, and 10 real-world xArm tasks on two distinct robot platforms (low-cost open-source and high-performance). Consistent performance improvements across all settings convincingly demonstrate generalization beyond simulation.

- **Creative cross-modal probing (Section 3.2, Figure 3 column 12).** The re-coloring experiment — where an altered RGB patch injected during depth-to-RGB reconstruction causes only the corresponding object to change color — provides compelling qualitative evidence of learned object-level semantic understanding and cross-modal correspondence, despite no explicit segmentation training.

- **Principled masking strategy (Section 2.2).** The Dirichlet-distributed stochastic masking across modalities (following MultiMAE) is well-motivated, with the concentration parameter α providing a clean knob to control inter-modal reliance while maintaining symmetric design to avoid modality bias.

## Weaknesses

### Fatal
None.

### Major

- **Confound between in-domain fine-tuning and multi-modal architecture.** The ViT encoder is initialized from DINOv2 pre-trained weights (Section 2.2, line 71: "allows us to initialize the ViT directly from DINOv2 pre-trained weights"). The primary baseline comparison is against DINOv2 used as a *frozen* feature extractor. This conflates two factors: (a) fine-tuning on in-domain manipulation data (DROID-3D), and (b) the multi-modal masked autoencoding objective. The paper lacks an ablation where DINOv2 is fine-tuned on DROID-3D with an *RGB-only* MAE objective (controlling for in-domain adaptation) while keeping everything else equal. Without this control, we cannot cleanly attribute gains to the multi-modal architecture rather than to simply fine-tuning a strong backbone on in-domain robot data. The comparison against SPA (which also trains on DROID data with implicit 3D priors) partially addresses this but does not isolate the multi-modal design. This is the most impactful missing experiment in the paper.

- **Inconsistency in "trained from scratch" claim.** Section 2.4 states "we first train a ViT-Giant EmbodiedMAE model from scratch on the DROID-3D dataset." Section 2.2 states the ViT "allows us to initialize the ViT directly from DINOv2 pre-trained weights." These are contradictory: the model is not trained "from scratch" — it inherits DINOv2's visual capabilities. The paper should be precise about what is learned from scratch (the decoder, patchifiers, cross-modal components) versus what is fine-tuned (the ViT encoder). This inconsistency matters because it affects how readers interpret the contribution of the multi-modal MAE training relative to the base DINOv2 capabilities.

### Minor

- **No variance or statistical significance reporting.** Success rates are reported as point estimates without error bars, standard deviations, or confidence intervals. MetaWorld (Table 1) lacks any indication of multiple seeds. Real-world evaluations (Figure 8) use 10 trials per task. LIBERO learning curves (Figure 6) use 150 trials but without variance across seeds. Robotics evaluation is inherently noisy, making it difficult to assess whether reported differences (e.g., 77.7% vs. 73.0% on MetaWorld average) are statistically meaningful.

- **DP3 baseline comparison conflates representation and policy architecture (Table 1, Figure 8).** DP3 (Ze et al., 2024) is a full policy architecture, not a vision foundation model. Comparing EmbodiedMAE-PC (representation learned by EmbodiedMAE + RDT policy head) against DP3 conflates representation quality with policy architecture differences. The paper should be clearer about this distinction or add a fairer comparison controlling for the policy head.

- **Decoder architecture is underspecified (Section 2.3).** The number of cross-attention layers, dimensionality of query/key/value projections, and structure of the "modality-shared ViT decoder" are not provided. The claim of "reducing computational cost by approximately a factor of three" lacks a clear baseline (three separate decoders?).

- **Missing training hyperparameters.** Total training steps and batch size are not reported (Section 2.5). The DP3 encoder initialization for point cloud patchification (Section 2.2) is not specified.

- **Ablation scope limited to distillation parameters (Section 3.5).** Ablations cover masking ratio, feature alignment positions, and loss ratio during distillation, but due to prohibitive cost there is no ablation of core architectural choices (e.g., with vs. without cross-modal decoder fusion). The finding that masking ratios ≥ 100% (feature alignment loss only, no MAE reconstruction) perform well somewhat undercuts the emphasis on the multi-modal MAE reconstruction objective.

### Trivial

- The "nearly 500 hours" processing time for DROID-3D (Section 2.1) is reported without specifying the hardware configuration, making the resource cost difficult to contextualize.

## Nice-to-Haves

- Adding a controlled ablation that fine-tunes DINOv2 on DROID-3D with an RGB-only MAE objective would cleanly isolate whether the multi-modal design is the source of improvement.
- Reporting results with error bars (3–5 seeds for simulation; confidence intervals or bootstrap for real-world) would substantially strengthen the quantitative claims.
- Clarifying the "from scratch" / DINOv2-initialized language throughout Sections 2.2 and 2.4.
- Adding decoder architectural details (layer counts, dimensions) and complete training hyperparameters (steps, batch size) for reproducibility.

## Removed Points

These points are flagged to be removed, treat them with caution:

- "No open-source release at time of review" — Removed per hard rule: the paper states code and dataset will be released upon publication. Penalizing future availability is not appropriate.
- Formatting nitpicks about parser artifacts in tables and figure captions — These are parser errors, not author problems.
- Speculative "the appendix may specify X but…" concerns — Removed per hard rule: the paper's appendix was stripped by the parser system; what is missing from the main text should be flagged as a reproducibility detail, not a fatal omission.
- Criticism that "SigLIP performs poorly" contradicts paper's own reporting — this is a finding, not a weakness.

## Novel Insights

The harsh critic provides one genuinely useful framing that goes beyond the paper's own self-assessment: the central attribution problem. The paper's headline claim is that EmbodiedMAE outperforms existing VFMs, but the most scientifically interesting sub-claim — that the *multi-modal* design specifically is responsible for the gains — is partially confounded with in-domain fine-tuning of a DINOv2 backbone. This is a concrete, testable hypothesis that one additional ablation experiment could resolve, and it would substantially strengthen the paper's contribution narrative. Separately, the cross-modal probing experiment (re-coloring in Figure 3, column 12) is a clever diagnostic that the paper could feature more prominently; it provides genuinely novel evidence of emergent object-level understanding that few prior VFM papers have demonstrated.

## Suggestions

1. **Highest priority:** Add a controlled ablation that fine-tunes DINOv2 on DROID-3D with the same MAE training setup but RGB-only. This will isolate whether the multi-modal design is the source of improvement versus simple in-domain fine-tuning.
2. Add error bars or multiple-seed evaluations for at least the simulation benchmarks (LIBERO, MetaWorld).
3. Fix the contradictory "from scratch" / DINOv2-initialized language in Sections 2.2 and 2.4. Be explicit about which components are initialized from DINOv2 and which are randomly initialized.
4. Provide decoder architectural specifications (layer counts, dimensions) and report total training steps and batch size.
5. Restructure the DP3 comparison: either present it as a separate system-level comparison rather than a direct VFM baseline, or add an RDT-policy + DP3-representation control.
6. Consider adding a brief discussion of the ablation finding that masking ratios ≥ 100% work well — does this suggest the MAE reconstruction loss is secondary to feature alignment?

## Score and Decision

Round 1 bracket: 5.0 – 7.0 (derived from calibration search against 30 anchor papers covering similar topics in robot manipulation, multi-modal learning, and representation learning).

**Anchors consulted:**
- *The Power of the Senses: M3L* (4.33) — masked multimodal learning for manipulation, but simulation-only with 3 tasks. EmbodiedMAE has far broader evaluation (90 tasks + real-world) and a dataset contribution. EmbodiedMAE is stronger.
- *MV3D-MAE* (5.25) — MAE for 3D from 2D pretraining, but evaluated on classification/segmentation, not manipulation. EmbodiedMAE targets a more challenging downstream task with real-world validation.
- *Building Generalist Robot Policy from Pre-trained Visual Representations* (3.40) — studies VFMs but does not contribute a new model or dataset. EmbodiedMAE contributes both.
- *Vision-Language Foundation Models as Effective Robot Imitators* (6.50) — single benchmark (CALVIN), narrower scope but polished evaluation. EmbodiedMAE's evaluation is broader but has the attribution confound. Comparable quality.
- *RDT-1B* (7.00) — full action foundation model, strong real-world results but some baseline fairness concerns. Uses same policy architecture as EmbodiedMAE. Slightly stronger overall, but addressing a different part of the pipeline.

Final score: The paper has genuine contributions (dataset, framework, comprehensive evaluation) that place it clearly above the 4–5 range. However, the missing ablation that isolates the effect of multi-modal training from in-domain fine-tuning is a significant evidential gap that prevents it from reaching the 7+ tier. Score 6.0 reflects a borderline-accept paper with clear value and an actionable path to strengthening.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>