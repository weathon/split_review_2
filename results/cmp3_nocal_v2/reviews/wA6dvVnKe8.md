## Summary

This paper proposes EDPA (Embedding Disruption Patch Attack), a model-agnostic adversarial patch attack for Vision-Language-Action (VLA) models, and a complementary adversarial fine-tuning defense for the visual encoder. EDPA requires only access to the VLA's encoder parameters (not the full model or action space), disrupting both the visual-embedding self-consistency and the visual–language alignment. It is evaluated across three VLA architectures (OpenVLA, OpenVLA-OFT, π₀) on the LIBERO simulation benchmark and drives failure rates to 100% on OpenVLA across all task suites. The defense, tested on OpenVLA, reduces EDPA-induced failures from ~100% to 39–91% with a modest clean-performance penalty.

## Strengths

1. **Model-agnostic attack design is a genuine improvement over prior work.** EDPA requires only encoder access and no knowledge of the action space, robotic manipulator, or LVLM backbone. In contrast, UADA and UPA need full model parameters plus specific knowledge of action structure or robot kinematics (Table 1, Section 2.2). This is a meaningful step toward more practical adversarial threat models for VLA systems.

2. **The attack is consistently effective across diverse VLA architectures.** EDPA drives OpenVLA's failure rate to 100% on all four LIBERO task suites (Table 2), and substantially increases failure rates for OpenVLA-OFT (62.0% average increase) and π₀ (31.4% average increase) (Table 3). The fact that a single attack formulation works on models with different architectures (token-prediction vs. flow-matching, single-camera vs. multi-camera) validates the core claim.

3. **The defense produces meaningful robustness gains with a modest clean-performance penalty.** Adversarial fine-tuning reduces EDPA-induced failure rates from ~100% to 39–91% depending on the task suite, while clean-condition failure rate increases by only 1.6% on average (Table 2). The defense also transfers to UADA and UPA attacks, suggesting it captures a general robustness property rather than overfitting to EDPA specifically.

4. **The analysis of patch visual structure (Section 5) is insightful.** The observation that patches consistently resemble robotic arms, and the explanation that this stems from limited viewpoint diversity in robotic training data, provides a testable hypothesis about why VLA models are vulnerable. This goes beyond mere attack evaluation to offer understanding of the underlying mechanism.

## Weaknesses

### Fatal

None.

### Major

- **The defense is evaluated on only a single model (OpenVLA), which limits the generality of the defense claims.** The paper states: "Due to our experimental results showed that OpenVLA exhibited the weakest robustness against EDPA, it was chosen as the primary model for defense evaluation" (p. 2). The defense is never evaluated on OpenVLA-OFT or π₀. Since the defense modifies only the visual encoder, and the encoders of these three models differ, it is possible that adversarial fine-tuning works differently—or causes performance collapse—on other models. The abstract's unqualified claim that "our proposed defense effectively mitigates this degradation" is therefore substantiated only for OpenVLA. The authors are transparent about the selection rationale, but the current evidence does not support the defense claim at the level of generality implied by the paper's framing. This is an evidential gap, not a fatal flaw, but it should be addressed (e.g., by testing on at least one additional model).

### Minor

- **No ablation separating the two loss components.** EDPA's objective (Equation 4) combines a patch contrastive loss (Equation 2) and an alignment loss (Equation 3) with α₁=0.8 weighting favoring the patch loss. There is no experiment showing what each loss contributes individually or whether the combination is synergistic. Running EDPA with α₁=1.0, α₁=0.0, and the default α₁=0.8 on a single task suite would cleanly demonstrate whether both objectives are necessary.

- **Patch placement protocol is underspecified.** The paper states the patch "can be randomly placed at any location within the image" (Section 3.1) but never specifies where the patch is actually placed during evaluation—whether at a fixed location, randomly per episode, or randomly per timestep. The location can dramatically affect attack success (occlusion of task-relevant regions vs. background). Without this detail, results are not fully reproducible.

- **Limited evidence on defense generalization to attack variants.** The defense is trained on EDPA-generated patches (Algorithm 1) and tested on EDPA patches from the same generation process. While generalization to UADA and UPA is tested (Table 2) and shows positive results, the paper does not test against EDPA variants with different hyperparameters (e.g., different α₁, different patch sizes, different random initializations). This makes it unclear whether the defense learns genuinely robust representations or adapts to the specific EDPA configuration.

### Trivial

- **The choice of K=1 inner attack iteration** for adversarial patch generation is unusually low (prior patch attacks typically use 10–100+ iterations) and deserves a brief justification in the main text.

- **Multi-camera patch optimization** is described as applying "separate adversarial patches to each camera independently" (Section 4.3), but it is not specified whether the patches are optimized jointly or independently. Clarifying this would aid reproducibility.

## Nice-to-Haves

- **Evaluate the defense on at least one additional model (OpenVLA-OFT or π₀).** This is the single most impactful missing experiment and would substantiate the generality of the defense claim.
- **Add a loss-component ablation** (α₁=1.0, α₁=0.0, default) on one task suite.
- **Specify the patch placement protocol clearly** (fixed vs. random per episode vs. random per timestep).
- **Provide details on how UADA and UPA were adapted to the LIBERO environment**, to ensure fair comparison.
- **Test cross-suite patch transfer** (e.g., do patches from Spatial transfer to Object?).
- **Quantitatively test the robotic-arm-overfitting hypothesis** (Section 5), e.g., by measuring whether patch effectiveness correlates with the presence of robotic-arm features in training data.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Circular relationship between attack and defense"** — The reviewer framed this as a weakness, but the defense training (Algorithm 1) follows standard adversarial training practice: training on adversarial examples generated by the same attack used at test time. Periodic patch reinitialization (every φ=1000 iterations) ensures diversity. The generalization concern is valid but is already partially addressed (tested against UADA/UPA) and is captured in the Minor weaknesses above with toned-down framing. The "circular" characterization is misleading.
- **"Encoder parameters ambiguity"** — The reviewer noted that "encoder parameters" could include both vision and language encoders. The paper's Section 3.1 clearly defines both as encoders, so this is not ambiguous.
- **"Patch contrastive loss drives embedding collapse"** — This is a design observation about the loss mechanism, not a weakness. The paper does not claim the opposite.
- **"Defense does not use task-specific action loss"** — This is a design choice that the paper explicitly acknowledges and justifies by showing clean performance is maintained (Table 2). Not a weakness.
- **"Incomplete comparison to prior work on multi-camera models"** — The paper transparently states why UADA/UPA are not applied to OpenVLA-OFT/π₀ (Section 4.3, p. 7: "these attacks are difficult to transfer to models other than OpenVLA due to their stringent application requirements"). This is a scope justification, not a flaw. Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Evaluate the defense on at least OpenVLA-OFT (which shares the same base architecture as OpenVLA but adds wrist-camera input) to extend the defense claims to a second model without requiring a fundamentally different training pipeline.
2. Add a one-table ablation of the two loss components (patch-only, alignment-only, combined) on a single LIBERO task suite to clarify each component's contribution.
3. State explicitly in the main text whether the patch is placed at a fixed location, a random location per episode, or per timestep in all evaluation settings.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>