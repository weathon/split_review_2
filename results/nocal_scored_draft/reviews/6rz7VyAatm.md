Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper diagnoses evaluation blind spots in backdoor attacks on object detection (duplicate detections hidden by ASR, mAP as a poor ODA proxy, neglected trigger scaling/placement, dataset dependencies) and proposes BadDet+, which augments the detector loss with a log-barrier penalty that suppresses original-class predictions on trigger-bearing objects. The method unifies region misclassification (RMA) and object disappearance (ODA) under a single formulation. Experiments across COCO, MTSD, and real-world PTSD transfer, with four detector architectures, show that BadDet+ achieves high attack success rates while substantially reducing the true detection rate (TDR) compared to prior data-poisoning methods.

## Strengths

- **Clear diagnosis of concrete evaluation blind spots (Section 3).** The paper identifies four specific, well-documented weaknesses in prior object-detection backdoor evaluations: (i) ASR alone misses that RMA attacks often produce duplicate detections (target + original class simultaneously), (ii) mAP is a poor proxy for ODA success since non-disappearance artifacts (duplicate boxes, phantom boxes) can also depress mAP, (iii) trigger scaling and placement are neglected in existing evaluations, and (iv) some methods depend on curated datasets or scene sparsity assumptions. This analysis is empirically grounded, with concrete examples shown in Figure 1, and is a genuinely useful contribution independent of BadDet+ itself. (favorability-based signal: strongly positive)

- **The True Detection Rate (TDR) metric (Section 5.2).** TDR directly measures whether the original-class prediction is truly suppressed for triggered objects, complementing ASR which only checks for the presence of a target-class detection. This is a simple but important correction for RMA evaluation that directly addresses the duplicate-detection blind spot. (favorability-based signal: strongly positive)

- **Comprehensive evaluation.** The paper spans two datasets (COCO, MTSD), four architectures (FCOS, Faster RCNN, DINO, YOLOv5m6), synthetic-to-physical transfer via PTSD, and multiple trigger placements (fixed positions and random). This breadth meaningfully exceeds prior object-detection backdoor work. (favorability-based signal: strongly positive)

- **Physical-world validation on PTSD.** Real-world transfer evaluation using the Physical Traffic Sign Dataset provides concrete evidence about real-world effectiveness, which most prior work lacks. (favorability-based signal: strongly positive)

- **Elegant penalty formulation with clear design rationale (Section 4).** The log-barrier penalty (Eq. 1-2) activates sharply only when the original-class logit exceeds a threshold τ, remaining near-inactive below it. This design is well-motivated by the analysis of failure modes and avoids unnecessary degradation of clean-task performance. (favorability-based signal: strongly positive)

## Weaknesses

### Fatal
None.

### Major

- **Threat-model asymmetry between BadDet+ and baselines is not controlled for.** BadDet+ operates under a stronger threat model (the attacker can modify the training loss function), while baselines (BadDet, UBA, Align, Morph) assume data-poisoning only. The paper acknowledges this asymmetry (Section 4, Section 6) but the central empirical claim — "outperforms existing RMA and ODA baselines" — conflates two distinct factors: (a) the expanded threat model (loss manipulation vs. data-only) and (b) the specific log-barrier penalty design. A controlled ablation comparing BadDet+ with λ>0 against BadDet+ with λ=0 under the *same* data-poisoning conditions would isolate the penalty's marginal contribution. Without this, the reader cannot determine whether the penalty itself adds value or whether the results simply reflect the fact that an attacker with access to the training loss can achieve more. The paper has the data to run this comparison, and the λ=0 condition is already implicitly discussed for YOLO ("λ=0 is optimal for this architecture"). (favorability-based signal: moderately negative)

- **RMA training setup is underspecified.** The paper states that suppressing original-class logits via the penalty and then letting "the standard classification objective... naturally steer the model towards predicting the attacker's target class" achieves RMA (Section 4). However, the standard classification loss penalizes not predicting the *ground-truth* label. If ground-truth labels for triggered objects remain the original class y_i (as the formalism in Eq. 1-2 suggests, where y_i is called the "original label"), the standard loss actively competes with the penalty by encouraging prediction of y_i. The paper must clarify whether ground-truth boxes for RMA are also relabeled to the target class during BadDet+ training. If they are, then BadDet+ = standard data poisoning (stamping + relabeling) + penalty, and the "single unified mechanism" framing needs qualification — it is unified at the loss level but still requires task-specific data preparation for RMA vs. ODA. (favorability-based signal: neutral-to-slightly-negative)

### Minor

- **YOLO RMA shows BadDet outperforms BadDet+.** On MTSD/PTSD with YOLOv5 (Table 4), BadDet achieves higher ASR@50 (96.57 vs. 91.97 Fixed) and better TDR@50 (3.14 vs. 7.54, lower is better for attack) than BadDet+. The paper acknowledges this and notes "λ=0 is optimal for this architecture." While BadDet+ still achieves a high ASR@50 (91.97), the claimed advantage vanishes on this architecture, and no analysis is given for why YOLO specifically fails to benefit from the penalty. (favorability-based signal: strongly negative — but this is a caveat honestly reported, not a fatal flaw)

- **Defense evaluation over-claims relative to its scope.** The paper states "These results underscore the need for defenses explicitly tailored to object detection" (Section 5.3, p. 256) after testing only two generic defenses (FT and FT-SAM) with very small clean-data subsets (2-4% of MTSD). This evidence shows that two fine-tuning approaches with tiny data budgets are insufficient — not that object-detection-specific defenses are fundamentally needed. The limitation is acknowledged in Section 6, but the results-section claim over-reaches. (favorability-based signal: strongly negative)

- **No variance or confidence intervals reported for main results (Tables 1-4).** Given that PTSD results show notable variation across settings (e.g., BadDet+ DINO PTSD ASR@50 drops from 85.16 Fixed to 76.75 Random), some indication of run-to-run variability would help assess reliability. (favorability-based signal: neutral)

- **No discussion of computational overhead.** The penalty requires computing IoU between each prediction and each triggered ground-truth box at every training iteration, adding O(N·M) computation per image. The paper does not mention this cost. (favorability-based signal: slightly positive — minor omission)

### Trivial
None.

## Nice-to-Haves

- Summarize λ sensitivity findings in the main text (currently deferred entirely to Appendix A.5), especially since λ varies by three orders of magnitude across architectures (1 for FCOS, 0.001 for YOLO).
- Include run-to-run variance for main experimental results.

## Removed Points

These points from the input review were removed per meta-review filtering rules:

1. **Criticism about theoretical analysis being in appendix** — Removed per rule: "REMOVE weaknesses about missing appendix, missing proofs in appendix, or absent references." The appendix exists in the original submission (stripped by the parser).
2. **Abstract over-promising about theoretical analysis** — Same reason; this criticism penalizes the paper for deferred appendix content, which the rules forbid.
3. **Poisoning Ratio analysis (Figure 3) conflating two variables** — The critic claimed the plot conflates threat model and penalty, but the paper's stated purpose for Figure 3 is to show that increasing poisoning ratios for data-only methods does not close the gap. This is a valid framing for demonstrating limitations of data-only approaches.
4. **Section 3 "data poisoning alone is insufficient" depends on changed evaluation protocols** — The improved protocols are part of the paper's contribution; the claim is about effectiveness under proper evaluation.
5. **Suggestion to foreground Section 3 as primary contribution** — This is a restructuring suggestion, not a weakness.
6. **Missing related works** — Not appropriate to mention per instructions.

## Novel Insights

The most insightful observation to emerge from the review process is that the paper's evaluation-diagnosis contribution (Section 3) is arguably stronger and more cleanly separable from the method contribution than the paper's own framing suggests. The identification of ASR's failure to penalize duplicate detections — and the corresponding TDR fix — is a concrete, low-overhead improvement to evaluation practice that does not depend on adopting BadDet+ itself. This means the paper has a solid contribution even if a reader is skeptical of the loss-level threat model. Conversely, the method's claimed superiority over baselines is structurally entangled with the threat model expansion, and the paper would benefit from explicitly owning this framing rather than presenting it as a straightforward "outperforms" result.

## Suggestions

1. **Add a λ=0 controlled ablation.** Compare BadDet+ (λ>0) vs. BadDet+ (λ=0) under identical data-poisoning conditions across all architectures. This would isolate the penalty's marginal contribution and simultaneously address the threat-model fairness concern.
2. **Clarify RMA label setup.** State explicitly in Section 4 whether ground-truth boxes for RMA are relabeled to the target class during BadDet+ training.
3. **Analyze the YOLO failure case.** Investigate and report why YOLO does not benefit from the penalty — is it the architecture, training pipeline, or hyperparameter interaction?
4. **Tone down the defense conclusion.** Replace "underscore the need for defenses explicitly tailored to object detection" with a more measured statement reflecting the limited scope of defenses tested.
5. **Report variance** for main results, particularly PTSD transfer.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>