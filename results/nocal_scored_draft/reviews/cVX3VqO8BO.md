Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper proposes UniHM, a framework for generating sequential dexterous hand manipulation trajectories from open-vocabulary language instructions. The pipeline couples (1) a morphology-agnostic VQ-VAE codebook that maps multiple hand types into a shared discrete latent space, (2) a Vision Language Model (Qwen3-0.6B) that generates manipulation token sequences conditioned on language and visual input, and (3) a physics-guided dynamic refinement module that enforces contact and smoothness constraints. The paper claims state-of-the-art results on DexYCB and OakInk datasets, and demonstrates real-world execution on a physical dexterous hand.

## Strengths

- **Problem framing is well-motivated.** Prior language-guided dexterous manipulation work (SemGrasp, AffordDexGrasp) generates only static grasp poses. Extending to full temporal sequences from open-vocabulary language is a genuinely important and under-explored direction.

- **Morphology-agnostic codebook is a sensible design.** The shared VQ-VAE codebook with per-hand encoder/decoder pairs plus distillation-based alignment (Eq. 3) addresses a real bottleneck — most dexterous manipulation work is hand-specific, limiting cross-hardware transfer. The forward-compatibility claim (adding a new hand by training only its encoder/decoder while reusing the codebook) is practically appealing.

- **Decoupled inference architecture has practical merit.** Separating scene perception (CLIPort, fine-tuned under distribution shift) from HOI sequence generation (frozen VLM) is a well-motivated engineering choice that improves data efficiency and robustness. This modularity is clearly described in Section 3.3.

- **Real-world validation.** The paper evaluates on a physical dexterous hand across four manipulation primitives (Grab, Pick&Place, Pull&Push, Open&Close) with both seen and unseen objects, demonstrating practicality beyond simulation.

## Weaknesses

### Major

1. **Missing comparison against relevant dexterous-specific baselines.** The paper compares against full-body human motion generation models (TM2T, MDM, FlowMDM, MotionGPT3) and claims state-of-the-art results. Yet the related work (Section 2.2) cites HOIGPT, Multi-GraspLLM, and DexGrasp Anything — methods designed for dexterous or hand-object-interaction tasks — without comparing against any of them. HOIGPT, which generates HOI sequences from text, is the most natural point of comparison, even if the others target static grasps. The real-world evaluation (Table 3) likewise compares only against MDM+Dex-Retargeting and MotionGPT3+Dex-Retargeting — generic human motion models with a retargeting step added on. This gap weakens the paper's central SOTA claims.

2. **Unanalyzed train/inference perception gap.** The paper states (Section 3.3) that during training the VLM conditions on ground-truth target trajectories and object point clouds, while at inference a separate CLIPort module estimates these quantities. However, it never specifies whether Tables 1 and 2 (main simulation results) use ground-truth trajectories or CLIPort estimates. If they use ground truth, the results reflect an oracle perception setup that does not match real-world deployment. The paper provides no analysis of how CLIPort errors propagate to downstream manipulation quality, making it impossible to assess how much of the reported performance depends on idealized perception.

3. **Missing reproducibility-critical details.** The paper does not state how many random seeds or trials were used for the standard deviations reported in Tables 1, 2, and 4. It is also unclear whether the FID metric uses standard ImageNet Inception features or a task-specific feature space. The number of codebook entries (K) and latent dimension (d_z) are defined symbolically but never given numeric values. While some hyperparameter values may reside in the (stripped) appendix, the number of evaluation trials and the FID feature definition are core experimental choices that should be stated in the main text or by explicit appendix reference.

### Minor

4. **Overclaimed scope relative to evaluation.** The title and abstract claim "open-vocabulary" and "open-world" capabilities. The evaluation is confined to within-distribution generalization — seen/unseen splits of DexYCB (10 YCB objects) and OakInk (100 objects/32 categories). The real-world experiments test basic primitives but do not evaluate on genuinely novel object categories, novel scene compositions, or compositional language instructions (e.g., "grasp the red mug and place it next to the blue bowl"). The claims should be calibrated to the evidence.

5. **Diversity metric inconsistency on DexYCB.** The paper states "Diversity closer to the ground truth indicates a more reasonable generation" (line 253). On DexYCB (Table 1), MotionGPT3's diversity (72.51 seen, 75.84 unseen) is substantially closer to GT (125.53) than the proposed method's (39.62 seen, 42.70 unseen). The paper does not discuss this. (The pattern reverses on OakInk — Ours is closer to GT — making this a resolvable inconsistency, but the paper's silence on the DexYCB result is a gap in the evaluation narrative.)

6. **Frame-by-frame optimization limitation not discussed.** The physics refinement (Section 3.4) optimizes each frame sequentially while treating previous optimized frames as fixed. The paper does not discuss the potential limitations of this greedy approach compared to a full-trajectory batch optimization, which could miss long-range dependencies in contact sequences.

### Trivial

None.

## Nice-to-Haves

- A failure analysis with representative failure cases would strengthen the paper's practical utility.
- Inference speed/runtime analysis would help assess real-world deployability.
- An ablation comparing separate codebooks per hand vs. the shared codebook would directly validate the paper's strongest architectural claim.
- A version of Tables 1/2 using CLIPort-estimated trajectories (if they currently use GT) would quantify the perception gap.

## Removed Points

These points are flagged to be removed; treat them with caution:
- "No code release or checkpoint access" — removed per hard rules (availability-based criticism).
- "Paper oversimplifies prior work" — the paper says "most language-guided approaches" focus on static grasps (line 17), which is a qualified claim.
- "Hyperparameter values not given (λ_c, λ_vel, λ_acc, α, k, β, K, d_z)" — removed because these may reside in the appendix (the paper references Fig.D2, confirming an appendix exists that the parser stripped).
- "No inference speed/runtime analysis" and "No failure analysis" — moved to Nice-to-Haves.
- "Section-by-section notes" about oversimplification and individual minor implementation quibbles — folded into broader weaknesses or removed as overly granular.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add comparisons against HOIGPT or, at minimum, provide a clear quantitative justification for why it cannot be compared. For the real-world evaluation, include a dexterous-hand method as a baseline if feasible.
2. Clearly state whether Tables 1/2 use ground-truth or CLIPort-estimated trajectories. If they use GT, add a version with CLIPort estimates and analyze the drop to quantify the perception gap.
3. Report the number of random seeds/trials used for all means and standard deviations, and clarify the FID feature space.
4. Temper the "open-world" and "open-vocabulary" claims to match the evaluation scope, or add experiments that genuinely test compositionality and novel object categories.

## Score and Decision

This paper tackles an important problem and proposes a well-structured pipeline with genuine architectural innovations (shared codebook, decoupled perception/generation, physics refinement). The real-world validation is commendable.

However, the evaluation does not adequately support the claimed SOTA results. The baselines are primarily human motion models rather than dexterous-specific methods, the perception gap is unanalyzed, and key experimental details are missing. The scope claims outpace the evidence. These are not fatal to the paper's core contribution — the approach is still novel and the ablation studies confirm each component's value — but they prevent the current submission from being a convincing demonstration of SOTA performance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>