## Summary
UniHM proposes a unified framework for generating dexterous hand manipulation sequences conditioned on free-form language instructions. The system combines a morphology-agnostic VQ-VAE tokenizer that maps heterogeneous hand kinematics into a shared codebook, a vision-language model (Qwen3-0.6B) for instruction-conditioned token generation, and a physics-guided dynamic refinement module that enforces contact, temporal smoothness, and generative priors. The method is trained solely on human-object interaction video data (DexYCB, OakInk) without requiring teleoperation data, and demonstrates generalization to unseen objects and real-world robotic execution.

## Strengths
- **First unified language-conditioned framework for dynamic dexterous manipulation beyond static grasps.** The paper addresses a genuine gap: prior language-guided dexterous work (SemGrasp, AffordDexGrasp) produces only static poses, while dynamic manipulation methods lack open-vocabulary control. UniHM's combination of VLM + tokenizer + physics refinement is a novel and well-motivated pipeline.
- **Morphology-agnostic codebook with cross-hand distillation is technically sound.** The staged training strategy (reference encoder → distillation → fine-tuning) elegantly handles the non-differentiability of VQ-VAE quantization when aligning heterogeneous hand kinematics. The ability to translate poses across hand types via Eq. (6) is a clean and practical contribution.
- **Strong empirical results across multiple metrics and settings.** On DexYCB and OakInk, UniHM outperforms four strong baselines (TM2T, MDM, FlowMDM, MotionGPT3) on MPJPE, FOL, FPL, and FID for both seen and unseen splits. Real-world success rates (Table 3) show substantial improvements over retargeted baselines (e.g., 65% vs 30% for seen Grab).
- **Ablation study convincingly validates each component.** The controlled experiments (Table 4) show that removing depth input, masked training, or physical refinement each degrades performance, confirming the necessity of all three design choices.

## Weaknesses

### Major
- **The VLM backbone (Qwen3-0.6B) is extremely small for a "vision language model."** The paper justifies this choice by citing data scarcity, but 0.6B parameters is more akin to a lightweight language model than a modern VLM (which typically range from 7B-70B). This raises questions about whether the method truly leverages "vision language model" capabilities or whether a simpler sequence model would suffice. The paper does not ablate the VLM size or compare against a non-VLM baseline (e.g., a transformer decoder without language pretraining).
- **The CLIPort-based perception module is a significant bottleneck that is not adequately evaluated.** The inference pipeline relies on CLIPort to estimate target trajectories from RGB-D, but the main experiments (Tables 1, 2) are conducted with ground-truth target trajectories during evaluation (as stated: "we post-process their outputs with our physics-guided refinement"). The real-world results (Table 3) are the only place where the full perception→generation pipeline is tested, and these use only 20 trials per condition (implied by percentages). The paper does not report perception accuracy (e.g., trajectory estimation error, object segmentation IoU) or ablate the CLIPort module's contribution to overall failure modes.
- **The "learning from video" claim is overstated.** The method uses retargeted MANO poses from existing HOI datasets (DexYCB, OakInk) as training data, not raw human video. The auto-annotation step (GPT-4o generating language descriptions from keyframes) is a useful data augmentation technique, but the core training data is still pre-processed 3D hand-object interaction sequences, not in-the-wild video. The paper should clarify this distinction and temper claims about eliminating teleoperation data—the method still requires 3D-annotated HOI datasets.
- **Diversity metric is consistently far from ground truth, and this is not discussed.** In Table 1, GT diversity is 125.53, while UniHM achieves 39.62 (seen) and 42.70 (unseen)—roughly 1/3 of the GT value. MotionGPT3 achieves much closer diversity (72.51 seen, 75.84 unseen). The paper claims "Diversity closer to the ground truth indicates a more reasonable generation" but then does not address why UniHM's diversity is so low. This suggests the model may be mode-collapsed or under-expressive, which is a significant concern for a generative model.

### Minor
- **The physics-guided refinement is frame-by-frame with only first- and second-order temporal priors.** This may not capture longer-range temporal dependencies (e.g., pre-grasp shaping, re-grasp planning). The paper does not analyze failure cases where the optimization gets stuck in local minima.
- **Real-world experiments are limited to a single dexterous hand (not specified which) with only 20 trials per condition.** The paper should report which hand was used, provide per-trial breakdowns, and include failure analysis (e.g., what caused the 35% failure rate on seen Grab?).
- **The paper claims "state-of-the-art" but only compares against motion generation baselines, not against other language-conditioned dexterous manipulation methods** (e.g., SemGrasp, AffordDexGrasp, DexGrasp Anything). While those methods produce static grasps, a comparison on the static-grasp subset would help contextualize the contribution.

### Trivial
- The paper uses "DexGYS" in related work but the citation (Wei et al., 2024) does not appear in the references section (though this may be a parser issue).

## Nice-to-Haves
- A comparison against a variant that replaces the VLM with a simple transformer decoder (no language pretraining) would isolate the benefit of the VLM backbone.
- Reporting the CLIPort trajectory estimation error (e.g., translation/rotation error on the target trajectory) would help diagnose whether failures come from perception or generation.
- A qualitative analysis of diversity: are the generated sequences genuinely different or nearly identical for the same prompt?

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Clarify the training/evaluation protocol: are Tables 1 and 2 evaluated with ground-truth target trajectories or CLIPort-estimated trajectories? If the former, the results do not reflect the full system's performance and the real-world gap may be larger than reported.
- Address the diversity discrepancy: either explain why low diversity is acceptable for manipulation tasks (e.g., task-constrained motions are inherently less diverse) or propose modifications to improve diversity.
- Add a comparison with static-grasp language-conditioned methods on a static-grasp subset to better position the work relative to the closest prior art.
- Report the specific dexterous hand used in real-world experiments and provide per-trial details.

## Score and Decision
The paper presents a novel and well-motivated framework for language-conditioned dexterous manipulation, with technically sound components (morphology-agnostic tokenizer, physics-guided refinement) and strong empirical results on standard benchmarks. However, the overclaimed "learning from video" framing, the unaddressed diversity issue, the lack of end-to-end evaluation with the perception module, and the very small VLM backbone raise concerns about the actual scope and robustness of the contribution. The paper is a solid contribution to the field but has several issues that should be resolved before acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>