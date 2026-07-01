## Summary
This paper investigates adversarial robustness in Vision-Language-Action (VLA) models. It proposes the Embedding Disruption Patch Attack (EDPA), a model-agnostic adversarial patch attack that requires only access to the VLA's visual and language encoders, and an adversarial fine-tuning scheme for the visual encoder as a defense. Experiments on the LIBERO simulation benchmark show that EDPA dramatically increases failure rates across OpenVLA, OpenVLA-OFT, and π0 models, while the proposed defense partially mitigates this degradation on OpenVLA.

## Strengths
- **Timely and important problem:** Adversarial robustness of VLA models is critical for safe embodied AI deployment, yet severely underexplored. The paper directly addresses this gap.
- **Practical attack design:** EDPA requires only encoder parameters, avoiding the stringent assumptions of prior attacks (e.g., knowledge of action space, robotic platform, or full model parameters). This makes it more applicable to real-world black-box scenarios.
- **Comprehensive evaluation across models:** The attack is tested on three different VLA models and four task suites from LIBERO, demonstrating generality beyond a single architecture.
- **Reasonable defense formulation:** The adversarial fine-tuning objective (matching latent representations for clean and perturbed inputs) is principled and requires no modification to the LVLM backbone.

## Weaknesses
### Fatal
None.

### Major
1. **Defense evaluated only on OpenVLA:** The adversarial fine-tuning is applied and tested solely on OpenVLA. The paper justifies this by noting OpenVLA is the weakest against EDPA, but the defense's effectiveness on other models (OpenVLA-OFT, π0) remains unknown. This limits the generality claims.
2. **Defense leaves high residual failure rates:** After defense, failure rates on Long tasks remain near 91% for EDPA and 97% for UADA. While the defense reduces failure rates, the resulting robustness is still unacceptable for any practical deployment, undermining the practical value of the defense.
3. **Simulation-only evaluation:** All experiments are performed in the LIBERO simulator. For a paper claiming real-world relevance and physical realizability (patches as stickers), the lack of any real-robot or even photo-realistic validation is a significant gap.
4. **Limited comparison to embedding-level attacks:** The paper mentions prior work on adversarial attacks targeting LVLM embeddings (Zhang et al., 2022; Bagdasaryan et al., 2024), but does not compare EDPA against such methods adapted to the VLA setting. This makes it difficult to assess whether the embedding disruption approach offers unique benefits over existing techniques.

### Minor
- **Hypothesis about encoder overfitting to robot arm is speculative:** While the visualizations are intriguing (patches resemble robotic arms), the paper provides no controlled experiment (e.g., arm removal, viewpoint diversity test) to substantiate the claim.
- **Single metric (Failure Rate) may be insufficient:** The paper uses only task success/failure. Additional metrics such as action trajectory similarity, number of steps completed, or severity of failure would provide a richer picture of attack impact.

### Trivial
None.

## Nice-to-Haves
- Real-robot validation with printed adversarial patches.
- Defense evaluation on π0 and OpenVLA-OFT.
- Comparison against embedding-level attacks (e.g., adversarial illusions).
- Ablation on patch size and placement.
- Analysis of defense's impact on clean performance across all models.

## Novel Insights
Beyond the paper's direct contributions, the observation that adversarial patches consistently take on structural patterns resembling robotic arms is thought-provoking. It suggests that VLA encoders overfit to the robot arm's appearance due to limited viewpoint diversity in training data—a hypothesis that could drive future work in dataset augmentation or domain randomization to improve robustness.

## Suggestions
- Evaluate the adversarial fine-tuning defense on at least one other model (e.g., π0) to support generality.
- Conduct a physical-world experiment using printed patches placed in a real camera view, even if only on a small set of tasks.
- Compare EDPA with an embedding-level baseline (e.g., adapting adversarial illusions for patch constraints on VLA encoders).
- Report failure rates broken down by task type and patch location to give insight into when the attack/defense works best.

## Score and Decision
The paper addresses an important problem with a practical attack and a sensible defense. However, the defense is evaluated on only one model, still yields high failure rates, and the real-world applicability is unvalidated. These limitations prevent a stronger recommendation.

MY FINAL SCORE: 6.0
MY FINAL DECISION: Accept