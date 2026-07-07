Here is the final consolidated review:

## Summary

This paper proposes EDPA (Embedding Disruption Patch Attack), an adversarial patch attack on Vision-Language-Action (VLA) models that requires access only to the visual encoder parameters — a meaningful reduction from prior work (UADA/UPA) which needed the full LVLM backbone, action space knowledge, or robot-platform information. The attack uses two objectives: maximizing the discrepancy between clean and adversarial visual representations, and disrupting vision-language alignment. EDPA is evaluated on three VLA models (OpenVLA, OpenVLA-OFT, π₀) on the LIBERO benchmark, achieving near-100% failure rates on OpenVLA and substantial increases on the others. The paper also proposes an adversarial fine-tuning defense that recovers some robustness, evaluated on OpenVLA.

## Strengths

- **Genuinely reduced access requirements for attack.** EDPA needs only the visual encoder parameters — not the LVLM backbone, action-space knowledge, or robot-platform details. Table 1 and Figure 1 make this contrast explicit against UADA/UPA. This is a meaningful practical improvement over prior work (Wang et al., 2024).
- **Evaluation across three architecturally distinct VLA models.** EDPA's attack effectiveness is demonstrated on OpenVLA, OpenVLA-OFT, and π₀ — models with different architectures and camera configurations. The single-camera vs. multi-camera analysis (Sections 4.2–4.3) provides a sensible comparative story about why multi-camera models are more robust.
- **The adversarial fine-tuning defense shows cross-attack generalization.** On OpenVLA, the defense reduces failure rates not only against EDPA but also against UADA and UPA (Table 2). This suggests that regularizing the encoder's embedding space may be a broadly useful strategy beyond defending against the proposed attack alone.

## Weaknesses

### Fatal

None.

### Major

- **Defense evaluated on only one model (OpenVLA), the worst-case model.** The paper states: "OpenVLA exhibited the weakest robustness against EDPA, it was chosen as the primary model for defense evaluation" (Section 1, line 25). This selection bias means we have no evidence the defense generalizes to OpenVLA-OFT or π₀. The paper's own hypothesis (Section 5) suggests π₀'s encoder has different training dynamics (more diverse data, less overfitting), which could mean the fine-tuning behaves entirely differently. Since the defense is presented as a general method ("adversarial fine-tuning scheme for the visual encoder," Section 3.3), this single-model evaluation is a significant evidential gap.

- **No defense baselines for comparison.** The defense is compared only against the undefended model and a random noise baseline (Table 2). Standard defense methods — PGD-based adversarial training on the visual encoder, randomized smoothing, input purification, or even simple Gaussian augmentation — are not evaluated. Without any defense baselines, the reader cannot calibrate whether the proposed adversarial fine-tuning is genuinely strong or merely better than doing nothing, which weakens the contribution of the defense half of the paper.

### Minor

- **Multi-camera evaluation uses separate patches per camera, limiting real-world conclusions about physical attack feasibility.** Section 4.3 states: "we apply separate adversarial patches to each camera independently for evaluation" because real-time alignment across camera views is infeasible. In any realistic physical attack, a single patch would appear in both camera views simultaneously. The paper acknowledges this (Section 6), but consequently the multi-camera results do not validate that a single physical patch can attack these models. The numbers in Table 3 are therefore difficult to interpret as evidence for a practical physical threat in multi-camera settings.

- **Defense still leaves very high failure rates, but the framing is optimistic.** After adversarial fine-tuning, EDPA still achieves failure rates of 39.4% (Spatial), 58.6% (Object), 73.9% (Goal), and 91.2% (Long) on OpenVLA (Table 2). The abstract frames this as "effectively mitigates this degradation." While the reduction from 100% is substantial, the absolute failure rates remain problematic for a method described as effective mitigation.

### Trivial

None.

## Nice-to-Haves

- **Inner attack iterations K=1 sensitivity analysis**: The paper fixes K=1 with sensitivity analysis deferred to Appendix C. While 50,000 outer iterations with batch size 16 provide 800k total gradient steps, a main-paper sensitivity analysis would strengthen confidence in the attack's optimality.
- **Cross-model transfer test**: Testing whether a patch optimized on one VLA's encoder degrades another VLA's performance (without re-optimization) would be informative even as a negative result. The paper's framing of "model-agnostic" is about attack requirements, not transferability, so this is not a weakness but would strengthen the paper.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Model-agnostic" framing overreach / cross-model transfer not tested**: The paper defines "model-agnostic" explicitly as "not requiring prior knowledge of the model architecture, action space, or the controlled robotic manipulator" (abstract). This is a reasonable, clear definition that differs from transferability. The paper's usage is consistent with its own definition. The criticism asks for a different property (cross-model transfer without re-optimization) that the paper neither claims nor scopes in.
- **Post-hoc hypothesis about visual encoder overfitting**: The paper clearly labels this as "a hypothesis" and "likely because" (Section 5). Calling a hypothesis speculative is tautological — that is the nature of discussion-section hypotheses.
- **Missing related works**: Cannot verify without external sources.
- **Formatting/style nitpicks**: Parser artifacts, not author errors.
- **K=1 inner iteration undersupported** (moved to Nice-to-Haves): The weight from the scoring model (+3.00) indicates this is not actually a weakness given the 50k outer iterations; the paper also references Appendix C for sensitivity analysis.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Evaluate the defense on at least one additional VLA model (ideally π₀) to test whether the adversarial fine-tuning generalizes.
2. Add at least one standard defense baseline (e.g., PGD-based adversarial training on the visual encoder) so readers can calibrate the defense's relative effectiveness.
3. For multi-camera settings, test whether a single patch applied with appropriate transforms to both camera views (even in simulation) can degrade performance, as a proof of concept for real physical attack feasibility.
4. Report and discuss absolute failure rates after defense more transparently rather than focusing primarily on relative reductions.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/KBSHR4h8XV.md | 3.33 | 1 | Yes | VLA paper with more severe methodological weaknesses (-7.22, -6.86); our paper has comparable negative weights but a cleaner attack contribution |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XFeiq8FMEF.md | 4.40 | 1 | Yes | HardPatch adversarial patch on LVLMs; has weaker negatives (-5.89 worst) than our paper, but our attack novelty is clearer |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wvFnqVVUhN.md | 6.25 | 1 | Yes | Large-scale VLM transferability study with extensive experiments; our paper lacks this breadth of evaluation |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/YzFNJ571A7.md | 4.00 | 2 | Yes | DynVLA MLLM attack with extreme -10.82 weakness (limited innovation); our paper's worst negatives are less severe |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/q8XGHj7yrC.md | 3.50 | 2 | No | LVLM robustness to visual transformations; limited topical overlap |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7OO8tTOgh4.md | 5.25 | 1 | No | Non-targeted VLM attack via entropy maximization; stronger experimental validation |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/K7xpl3LZQp.md | 6.25 | 2 | No | LVLM copyright tracking via adversarial attacks; well-received |

**Round 1 bracket**: After comparing weighted items, the paper sits between the 3.33 anchor (similar worst-negative magnitude but weaker strengths) and the 4.40 anchor (weaker negatives). The two major weaknesses (-6.16 defense only on OpenVLA, -6.96 no defense baselines) pull the score below 5.5, while the solid attack contribution and cross-model evaluation keep it above 3.0.

**Final placement**: The paper is a borderline paper. Its attack contribution is genuinely novel and reasonably well-evaluated across three models. However, the defense half — presented as a core contribution — is substantially under-supported (one model, no baselines). This imbalance between the two claimed contributions justifies a score in the borderline-reject range. The paper would be stronger if the defense were either substantially expanded or explicitly framed as preliminary.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>