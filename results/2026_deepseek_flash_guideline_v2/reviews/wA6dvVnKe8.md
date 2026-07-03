## Summary

This paper proposes EDPA (Embedding Disruption Patch Attack), an adversarial patch attack for Vision-Language-Action (VLA) models that requires only access to the visual and language encoders — no action-space or robot-manipulator knowledge. EDPA uses two objectives: a patch contrastive loss to maximize embedding discrepancy between clean and adversarial visual inputs, and an image-instruction alignment loss to disrupt cross-modal semantic alignment. The paper also proposes an adversarial fine-tuning defense that trains the visual encoder to produce consistent representations for both clean and attacked inputs. Experiments on the LIBERO benchmark across three VLA models (OpenVLA, OpenVLA-OFT, π₀) show that EDPA drives failure rates to 100% on untuned OpenVLA and substantially increases failures on other models, while the defense reduces failure rates by 34.2% on average against EDPA.

## Strengths

1. **Practical attack design with reduced prerequisites**: Unlike prior attacks (UADA, UPA) that require knowledge of the action space or robotic manipulator structure, EDPA operates using only encoder parameters (Table 1). The paper validates EDPA on three distinct VLA models (OpenVLA, OpenVLA-OFT, π₀) with different architectures and camera configurations, demonstrating the method's applicability beyond a single model.

2. **Defense generalizes to unseen attack methods**: The adversarial fine-tuning scheme is trained exclusively on EDPA-generated patches but measurably reduces failure rates against UADA (e.g., from 98.9%→65.4% on Spatial) and UPA (99.1%→46.6% on Spatial), both of which use fundamentally different attack objectives. This cross-attack transfer is a nontrivial finding beyond what prior work demonstrated.

3. **Thorough experimental evaluation**: Results cover all four LIBERO task suites (Spatial, Object, Goal, Long) with 10 tasks × 50 executions each, averaged over three random seeds, providing sufficient breadth to assess generalization across different task types and difficulty levels.

4. **Insightful patch visualization analysis**: The observation that generated patches consistently resemble robotic arms, paired with the hypothesis about visual encoder overfitting to limited camera viewpoints in robotic datasets (Section 5), provides qualitative insight beyond the numerical results and connects to a deeper vulnerability in VLA training procedures.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **"Model-agnostic" framing is somewhat overstated.** The title and abstract describe EDPA as "model-agnostic," but the attack still requires white-box access to (and gradient computation through) the specific visual and language encoders of the target model. The paper's operational definition (Section 3.2: "requires no access to the VLM backbone or prior knowledge of the model architecture and action space") clarifies what is meant, but the headline term "model-agnostic" could mislead readers into thinking no model-specific access is needed. The paper demonstrates the method on three different VLA models, which supports the claim that the methodology transfers, but the access requirement (encoder gradients) is nontrivial. A more precise descriptor such as "action-space-agnostic" or "backbone-agnostic" would better match the evidence.

2. **Defense effectiveness is highly uneven across task suites, which is under-discussed.** The paper reports an average FR reduction of 34.2% against EDPA (line 194), but this masks severe disparities: 60.6% reduction on Spatial vs. only 8.8% on Long (where FR drops from 100% to just 91.2%, leaving the VLA almost entirely non-functional). Against UADA on Goal (98.6%→91.6%) and Long (99.6%→97.4%), improvement is marginal. The averaging gives a misleading impression of uniform effectiveness, and the paper does not discuss why the defense fails on harder task suites. This is important for understanding real-world deployment limitations.

3. **No ablation of the two loss components in the main text.** EDPA combines patch contrastive loss (Eq. 2) and image-instruction alignment loss (Eq. 3) with α₁=0.8. The paper references Appendix C for hyperparameter sensitivity, but the main text would benefit from a basic isolation of each loss (e.g., α₁=0, α₁=1, α₁=0.8). Without this, the reader cannot assess whether both losses are necessary or whether one dominates.

4. **No justification for K=1 inner attack iterations.** The number of inner attack iterations is set to K=1 (line 184) without explanation. While the outer loop runs 50,000 iterations, the dynamics of single-step vs. multi-step patch updates per encoder state are substantively different and merit discussion or experimental comparison.

### Trivial

1. **Table 1 does not distinguish between visual-only and both-encoder access.** EDPA requires both the visual encoder and language encoder, whereas the "Encoder Parameters" row shows a checkmark for all three methods without reflecting this distinction. Clarifying would improve precision.

## Nice-to-Haves

- A cross-model transfer experiment (testing whether a patch generated for one visual encoder degrades a different model's performance) would further strengthen claims about generality, though this goes beyond what the paper currently asserts.
- Evaluating the defense on multi-camera models (OpenVLA-OFT, π₀) would be informative for understanding its broader applicability.
- Showing an example of the patch placed in a real LIBERO observation scene would help readers assess physical-world plausibility.
- Per-suite statistical comparison of clean performance degradation (beyond the 1.6% average) would clarify whether the robustness/accuracy trade-off is significant.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- Harsh critic's claim that "cross-model transfer testing is required" for the "model-agnostic" framing: The paper defines "model-agnostic" operationally as not requiring action-space/robot-manipulator knowledge and demonstrates the methodology on three VLA models. The critic interprets "model-agnostic" as requiring zero-shot cross-model transfer of a single patch, which is not the standard usage in adversarial ML and imposes a stronger requirement than the paper makes.
- Harsh critic's complaint about clean performance degradation not being statistically tested: The paper reports means and standard deviations per suite; this level of reporting is standard for the subfield.
- Harsh critic's point that the defense only uses EDPA patches during training: This is a design choice, not a flaw — the defense is explicitly designed for EDPA, and the cross-attack transfer to UADA/UPA is reported as an additional finding.
- Strength Finder's generic strengths (e.g., "addressed an important problem"): Removed for lacking specific, concrete evidence tied to the paper's content.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Replace or qualify "model-agnostic" in the title/abstract with a more precise term such as "action-space-agnostic" or "encoder-only" adversarial attack.
2. When reporting defense results, provide a per-suite breakdown in the text (not just the table) and explicitly discuss why the Long suite sees minimal improvement.
3. Add a basic ablation of α₁ in the main paper (α₁=0, 1, 0.8) to isolate the contribution of each loss term.
4. Provide a brief justification or sensitivity study for the choice K=1.

## Score and Decision

This paper makes a genuine contribution to the under-explored area of adversarial robustness in VLA models. The attack (EDPA) is meaningfully more practical than prior work — removing the need for action-space or robot-manipulator knowledge is a real step forward. The evaluation is thorough across multiple models, task suites, and random seeds. The defense, while showing uneven results, provides a nontrivial starting point and demonstrates cross-attack generalization.

The weaknesses are real but fixable: the "model-agnostic" framing slightly overstates what is demonstrated, the defense results are presented in a way that obscures their unevenness, and the paper lacks basic ablations in the main text. None of these issues invalidate the core contribution — they are matters of precision, presentation, and analysis depth rather than methodological flaws.

Given the clear contribution to an important and underexplored problem, the thorough evaluation, and the fact that the weaknesses are addressable in revision, the paper merits acceptance.

**Calibration note:** The calibration retrieval tool was unavailable due to a filesystem error, so numerical anchoring against human-reviewed papers could not be performed. The score of 6 reflects a holistic assessment: a solid, non-groundbreaking paper with a clear practical contribution, evaluated thoroughly, and needing minor framing/presentation fixes. It is not strong enough for 7+ (which would require either a deeper theoretical contribution, more uniformly strong defense results, or broader cross-model validation), and not weak enough for 4-5 (the attack's practical advantages over prior work are real and clearly demonstrated).

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>