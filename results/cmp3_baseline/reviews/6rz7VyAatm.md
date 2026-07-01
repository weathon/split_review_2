## Summary

This paper identifies critical evaluation blind spots in existing backdoor attacks for object detection—namely that ASR ignores retained true-class detections in RMA, mAP is a poor proxy for ODA, and existing attacks lack robustness to trigger scale and placement. To address these issues, the authors propose BadDet+, a unified penalty-based attack framework that augments the detector loss with a log-barrier term to suppress true-class confidence on trigger-bearing objects. BadDet+ achieves consistently high attack success rates with low true-detection rates across COCO, MTSD, and physical-world PTSD benchmarks, outperforming prior methods while maintaining clean-task mAP.

## Strengths

- **Clear diagnosis of evaluation flaws in prior work.** The paper convincingly shows that existing evaluations of RMA and ODA attacks are unreliable: ASR overstates success by ignoring duplicate detections, mAP confounds disappearance with other failure modes, and trigger-scale/placement robustness is untested. This analysis alone is a valuable contribution.
- **Principled unified formulation.** The log-barrier penalty is theoretically grounded (Appendix A.7) and elegantly unifies RMA and ODA by treating background as a special target class. The derivation from a "penalty wall" that only activates when original-class confidence exceeds a threshold is clean and well-motivated.
- **Extensive and rigorous experimental evaluation.** The paper tests across four architectures (FCOS, Faster R-CNN, DINO, YOLOv5), two datasets (COCO, MTSD), and physical-world transfer (PTSD) with multiple trigger placements and scales. Ablations on poisoning ratio, λ sensitivity, and trigger variants provide thorough characterization.
- **Honest and well-scoped discussion of limitations.** The paper openly acknowledges where the method does not improve over baselines (YOLO RMA), the stronger threat model assumption, and the restricted defense study. This strengthens the credibility of the claims.

## Weaknesses

### Fatal
None.

### Major

1. **Threat model assumes training-time loss manipulation, which is stronger than standard data poisoning.** While the authors motivate this by showing data-poisoning attacks are unreliable, the practical setting where an attacker can directly modify the loss function (rather than only poisoning training data) is less common. This may limit the real-world applicability of the attack and makes the comparison with data-poisoning baselines somewhat asymmetric. The paper would benefit from a more detailed discussion of scenarios where loss manipulation is feasible (e.g., if the attacker controls the training code or uses a malicious optimizer).

2. **Defense evaluation is narrow.** Only fine-tuning (FT) and FT-SAM are considered, using very small clean subsets (2–4% of MTSD). Many other defense categories (pruning-based, test-time detection like TRACE, input-level transformations such as compression or diffusion purification) are excluded. While the authors explicitly scope these out, the claim that BadDet+ is "robust" to defenses is only supported for a limited family of fine-tuning approaches. The results are still informative but the wording in the abstract ("robustness to fine-tuning-based defenses") should be precise.

### Minor

1. **Performance on YOLO for RMA is not superior to BadDet.** In Table 4, BadDet achieves higher ASR@50 and lower TDR@50 than BadDet+ on YOLOv5 (ASR@50: 96.57 vs 91.97; TDR@50: 3.14 vs 7.54). The paper acknowledges this but does not fully explain why the proposed penalty mechanism underperforms on this architecture. A brief analysis of architectural differences (e.g., YOLO's one-stage design, different loss components) would strengthen the discussion.

2. **The paper does not evaluate object generation attacks (OGA).** While the authors note that existing OGA methods perform well under their protocol, omitting this threat model leaves the "unified" claim incomplete. Given that OGA is one of the four original BadDet threat models, showing that BadDet+ can (or cannot) be extended to OGA would be a natural addition.

### Trivial

- The paper uses only a blue square trigger for the main experiments; alternative triggers are in the appendix but not integrated into the main results. This is acceptable but a brief main-text note on trigger universality would improve clarity.

## Nice-to-Haves

- An analysis of computational overhead (training time, memory) of the penalty term compared to data-poisoning baselines.
- A study on the impact of the IoU threshold ρ and confidence threshold τ on attack performance.
- A comparison with a "white-box" version of BadDet where the same loss manipulation is allowed, to better isolate the benefit of the log-barrier design.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. For the defense evaluation, consider testing at least one additional defense category (e.g., input-level transformations like JPEG compression or Gaussian blur) to broaden the claim of robustness. Even if not exhaustive, it would show that BadDet+ survives simple countermeasures.
2. Provide concrete guidance on selecting the penalty weight λ for new architectures (e.g., a heuristic based on the magnitude of the detection loss ℒ_det).
3. Clarify in the conclusion that the stronger threat model is a limitation and discuss potential ways to achieve similar results with data-poisoning-only attacks (e.g., by using a surrogate model to approximate the penalty).

## Score and Decision

The paper makes a strong, well-supported contribution to understanding and improving backdoor attacks in object detection. The flaws (strong threat model, narrow defense study) are acknowledged and do not invalidate the core results. The work is thorough, clearly written, and should be of high interest to the security community.

**Score:** 8

**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>