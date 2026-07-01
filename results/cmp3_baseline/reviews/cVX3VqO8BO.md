## Summary

UniHM proposes a unified framework for generating dexterous hand manipulation sequences conditioned on open-vocabulary language instructions. The system combines a shared VQ-VAE codebook that spans multiple hand morphologies (MANO, Shadow, Allegro, etc.), a small VLM (Qwen3-0.6B) that generates manipulation tokens from language, RGB-D observations, and target trajectories, and a physics-guided dynamic refinement module that enforces smoothness and contact feasibility. Evaluations on DexYCB and OakInk show improvements over text-to-motion baselines, and real-world experiments demonstrate that the generated sequences can be executed physically.

## Strengths

- **Addresses an important and timely problem.** Generating sequential, physically feasible dexterous manipulation from free-form language is directly relevant to embodied AI and robotics, and the community needs methods that go beyond static grasp pose prediction.
- **Unified hand tokenizer with cross-morphology generalization.** The idea of distilling heterogeneous hand kinematics into a shared codebook via knowledge distillation is practical and could reduce the effort of deploying methods across different robotic hands. Eq. (6) makes cross-hand translation straightforward.
- **Multi-objective energy-based refinement.** The combination of contact, generative, and temporal priors in a Gauss-Newton optimization (Eq. 16-18) is well motivated, and the asymmetric contact penalty (Eq. 12) handles penetration and separation asymmetrically, which is appropriate for grasp optimization.
- **Real-world validation.** Table 3 and Figure 3 show that at least some of the generated sequences can be executed on physical hardware, which strengthens the claim of physical feasibility beyond simulation.

## Weaknesses

### Fatal

None.

### Major

- **Misleading comparisons and weak baselines.** All evaluated baselines (TM2T, MDM, FlowMDM, MotionGPT3) are generic text-to-motion models for full-body or single-character motion, *not* designed for hand-object interaction. The substantial gap in Tables 1 and 2 likely reflects that these methods were repurposed without proper adaptation for dexterous manipulation (even with post-processing). The paper lacks comparisons to language-guided dexterous grasp methods such as SemGrasp, AffordDexGrasp, or Multi-GraspLLM, which are the most directly relevant prior work (and cited in the related work section). Without fair baselines, the claimed "state-of-the-art" status is not supported.

- **Key component (CLIPort-based trajectory planner) is underspecified.** The method relies on CLIPort to predict the full target trajectory \(\mathcal{T}_{\text{tar}} \in \text{SE}(3)^K\) from RGB-D + language. How CLIPort is trained, what supervision it uses, how the trajectory is represented, and how the trajectory length \(K\) is determined are all omitted. This is a critical perception-to-action pipeline component, and its evaluation is entirely absent (e.g., no ablation on trajectory prediction accuracy). The claim that only CLIPort needs fine-tuning under domain shift is plausible but unvalidated.

- **Overclaimed novelty.** The paper describes itself as "the first unified, language-conditioned framework for dynamic dexterous hand manipulation beyond static grasps." However, HOIGPT (cited in the paper) already generates sequential 3D hand-object interactions from text, and Multi-GraspLLM handles multiple robotic hands. The incremental contribution—applying a similar tokenization and VLM approach to longer dexterous sequences with a physics refinement—is real but less drastic than claimed. The "learning from video without teleoperation" claim is also overstated because the training data come from controlled multi-view capture setups (DexYCB, OakInk) with precise 3D labels, not from in-the-wild human video.

- **Frame-by-frame optimization can accumulate errors.** The physics refinement solves sequentially (step t uses \(q_{t-1}^{\text{opt}}, q_{t-2}^{\text{opt}}\)). If a single frame suffers a poor local minimum, the error propagates through the temporal prior. The paper does not evaluate trajectory-level stability (e.g., whether later frames diverge from the intended motion) or compare against a batch optimization that solves all frames jointly.

### Minor

- **Diversity metric is inconsistent.** In Tables 1-2, the reported Diversity for the proposed method is often notably lower than ground truth (e.g., 39.62 vs 125.53 on DexYCB seen, 42.70 vs 125.53 unseen) and lower than MotionGPT3. This suggests mode collapse or lack of variation across prompts, but the paper does not analyze why or whether this matters for physical execution quality.

- **Contact model is simplified.** The point-to-plane distance with a smooth penalty (Eq. 12) captures neither friction cones nor force closure. While a tractable approximation, the paper does not quantify how often the resulting grasps are dynamically unstable (i.e., can resist external perturbations). The real-world success rate (< 65%) implicitly reflects this gap.

- **Ablation results for "w/o Depth Input" degrade significantly** (MPJPE from 61.40 to 85.47), yet the paper dismisses this as "pose estimation and 3D reconstruction degrade substantially." This is not surprising, but the ablation conflates depth usage with the entire perception pipeline. A cleaner control would keep depth but ablate the CLIPort trajectory planner.

### Trivial

- The dataset description in Section 4.1 has a redundant phrase ("10 objects, 20 objects") that appears to be a formatting artifact.

## Nice-to-Haves

- A comparison against the retargeting-only baseline (e.g., directly retargeting MANO poses from the dataset to the target hand without any generation) would isolate the benefit of the learned generation module.
- Reporting the reconstruction fidelity of the unified codebook (e.g., mean joint angle reconstruction error per hand morphology) would strengthen the claim of cross-morphology representation quality.
- A breakdown of the real-world failure cases (e.g., collisions, slipping, unable to follow the trajectory) would help future improvements.

## Novel Insights

Beyond the paper's own contributions, the key insight is that a shared discrete token space can be built across different dexterous hand designs by distilling encoder representations rather than directly aligning poses. This decoupling of perception (VLM token prediction) from embodiment (hand-specific decoder) is a practically useful design pattern for cross-embodiment robot learning. However, the paper does not deeply explore how the codebook size or token dimensionality affects generalization to new morphologies, and the demonstration remains limited to five hands.

## Suggestions

1. **Add proper baselines.** Compare with SemGrasp, AffordDexGrasp, or DexGrasp Anything for the generation part, even if those baselines only produce static grasps—this would clarify the advantage of sequential generation. For the VLM component, include HOIGPT as a baseline that also produces HOI sequences from text.
2. **Validate the CLIPort trajectory planner.** Provide quantitative metrics (e.g., trajectory endpoint error, trajectory alignment to ground truth) and an analysis of how often planner errors cause downstream failure.
3. **Run batch optimization** as a post hoc comparison to the sequential frame-by-frame optimization to test whether error accumulation is a practical concern.
4. **Evaluate diversity more carefully.** Report the coverage of generated grasps (e.g., contact maps, hand orientations) across different prompts for the same object to show that the model does not collapse to a single mode.
5. **Release the codebook and trained models** to strengthen reproducibility, especially since the paper claims cross-morphology generalization as a core contribution.

## Score and Decision

The paper tackles a relevant problem and contains several building blocks (shared tokenizer, energy-based refinement) that are sound. However, the evaluation is weakened by inappropriate baselines (generic motion models rather than language-conditioned dexterous grasp methods), an underspecified perception component (CLIPort trajectory planner), and overclaimed novelty relative to existing sequential HOI generation work (HOIGPT) and multi-hand grasp generation (Multi-GraspLLM). The real-world results are encouraging but limited (< 65% success on seen tasks). These issues collectively lower the confidence in the claimed SOTA status and the paper's overall impact for ICLR.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>