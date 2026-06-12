## Summary

The paper introduces BadDet+, a unified penalty-based backdoor attack framework for object detection that uses a log-barrier penalty to suppress original-class predictions for trigger-bearing objects, unifying region misclassification attacks (RMA) and object disappearance attacks (ODA) under a single mechanism. The authors also identify significant evaluation shortcomings in prior object-detection backdoor work—duplicate detections ignored by ASR in RMA, misleading use of mAP for ODA, and lack of trigger robustness checks—and propose a more rigorous evaluation protocol. Experiments span four architectures, two datasets, and physical-world validation, demonstrating consistently high attack success with preserved clean-task performance.

## Strengths

- **Systematic diagnosis of prior evaluation flaws.** The paper identifies specific, empirically demonstrated weaknesses in prior work: BadDet's duplicate detections where both target and original class are predicted (Figure 1a), UBA's phantom boxes from zero-sized training boxes (Figure 1b-c), and Align's sensitivity to trigger scale (Appendix A.2.2). These are not straw-man arguments but concrete, reproducible failure modes that prior evaluations overlooked.

- **Technically clean and principled formulation.** The log-barrier penalty in Eq. 1/2 provides a soft constraint that sharply penalizes original-class logits exceeding a threshold on trigger-bearing objects, while remaining inactive otherwise. Viewing ODA as an RMA where the target is background is an elegant unification that exploits the structure of modern detectors. The two-formulation approach (sigmoid for per-class logits, softmax-compatible for multi-class normalized logits) demonstrates careful attention to architectural diversity.

- **Comprehensive and rigorous experimental evaluation.** The study covers 4 architectures (FCOS, Faster RCNN, DINO, YOLOv5), 2 datasets (COCO, MTSD), physical validation (PTSD), multiple trigger placements (high, low, both, random), poisoning ratio sweeps, and defense evaluations. This breadth substantially exceeds prior work and establishes a credible benchmark. The inclusion of naive attack variants (UBA Box, Align Random) that attempt simple fixes is a particularly valuable contribution, demonstrating that straightforward patches to prior methods do not eliminate failure modes.

- **Honest treatment of limitations and methodological rigor.** The authors transparently report that BadDet+ underperforms BadDet on YOLO for RMA (Table 4), acknowledge the stronger threat model, and restrict defense evaluation scope rather than overclaiming. The proposed TDR metric directly addresses the identified gap in ASR evaluation for RMA, and instance-level ASR for ODA avoids the dataset-level mAP confounds.

- **Valuable poisoning-ratio analysis.** Figure 3 convincingly shows that increasing poisoning ratios for existing data-poisoning attacks (UBA, BadDet) either fails to improve ASR without degrading mAP or does so only marginally. This analysis directly motivates the stronger threat model and provides an important empirical insight about the fundamental difficulty of backdooring object detectors via data poisoning alone.

## Weaknesses

### Fatal
None.

### Major

- **Stronger threat model assumption.** BadDet+ assumes the attacker can control the training loss, not merely the training data. While the authors justify this through outsourced training scenarios and ML-as-a-service platforms, this is a meaningfully stronger assumption than standard data poisoning assumed by prior work. The paper's key claim—that existing data-poisoning attacks are unreliable—is used to justify this stronger model, but this argument is somewhat circular: if the attacker can manipulate the loss, many attacks become easier. The practical prevalence of this threat model compared to pure data poisoning is asserted but not evidenced with concrete statistics or case studies.

- **Architecture-dependent performance inconsistency.** BadDet+ underperforms standard BadDet on YOLOv5 for both ASR@50 (87.04 vs 93.25) and TDR@50 (14.00 vs 7.64) in the MTSD RMA setting (Table 4). The authors mention that λ=0 is optimal for YOLO but do not provide results with that setting, leaving it unclear whether BadDet+ has any advantage over BadDet on this architecture. Since the paper claims a unified framework, this architecture-specific failure weakens the generality claim and deserves fuller exploration.

- **Limited defense evaluation scope.** The defense evaluation is restricted to FT and FT-SAM with 2-4% clean data. While the authors acknowledge this, the fact that object-detection backdoor defenses are underdeveloped is itself partly a consequence of the attack literature being limited. A more complete picture would include at least one complementary defense category (e.g., Neural Cleanse-style anomaly detection adapted to detection, or input-space transformations) to bound the attack's robustness from multiple angles.

### Minor

- **Hyperparameter sensitivity not fully characterized.** The approach introduces ρ (IoU threshold), τ (confidence boundary), λ (penalty weight), and poisoning ratio. While λ sensitivity is in the appendix, the interaction between τ and the target detector's confidence distribution is not explored. Different architectures may have very different logit ranges, making τ highly architecture-dependent. A sensitivity analysis showing robustness to τ selection would strengthen the practical guidance.

- **Limited physical-world diversity.** Physical validation is conducted solely on traffic signs (PTSD). While this is a legitimate and safety-critical domain, the generalization to other physical settings (pedestrians, vehicles in diverse conditions) remains untested. The claim of "stronger synthetic-to-physical transfer" is bounded by this single physical domain.

- **Clean-task cost on DINO.** Across Tables 1-4, DINO consistently shows the largest mAP drops from clean baseline (e.g., from 50.4 to 44.43 for ODA in Table 1, and from 59.3 to 53.19 in Table 3). While this is partly architecture-specific, the paper does not discuss why DINO is more sensitive or whether this cost is acceptable in practice.

### Trivial

- In Section 5.3, the text states "λ=0 is optimal" for YOLO, which likely should reference the actual hyperparameter value used or confirm whether zero penalty is indeed intended.

## Nice-to-Haves

- A clearer discussion of the computational overhead of BadDet+ during training compared to standard data-poisoning approaches would help practitioners assess the trade-off.
- A brief analysis of whether the log-barrier penalty induces any measurable change in the learned feature representations (e.g., via activation visualization or feature-space analysis) would complement the theoretical discussion in Appendix A.7.
- Extending the physical validation to at least one non-traffic-sign domain would substantially strengthen the real-world impact claims.

## Novel Insights

The paper's most genuinely novel insight is that object detection backdoors face a fundamentally different challenge than image classification backdoors: data poisoning alone is insufficient because the detector's multi-task nature (classification + localization) and duplicate prediction mechanisms create persistent failure modes (dual detections, phantom boxes, incomplete disappearance) that do not scale away with increased poisoning ratios. This finding reframes the problem space and suggests that the object detection community cannot simply transfer classification backdoor intuitions or defenses. The observation that existing evaluation metrics (ASR, mAP) systematically overstate attack success in detection is also a valuable methodological contribution that should shape future work in this area.

## Suggestions

- Investigate the YOLO-specific failure mode more thoroughly. Provide BadDet+ results with λ=0 for YOLO in the main paper and discuss what architectural properties (e.g., grid-based detection head, loss formulation) cause the method to lose its advantage. If BadDet+ offers no improvement over BadDet on YOLO, this should be stated explicitly as a limitation.
- Consider a brief case study (even a single paragraph) of the threat model in a concrete real-world pipeline (e.g., fine-tuning from a public pretrained model) to ground the stronger assumption in practical terms.
- Add a discussion paragraph addressing the tension between the authors' finding that data poisoning is insufficient and the broader backdoor literature's reliance on data poisoning—does this suggest a fundamental gap that needs to be addressed, or are object detectors uniquely robust?

## Score and Decision

The paper makes solid contributions: a rigorous diagnosis of evaluation blind spots in existing object-detection backdoor work, a technically sound unified attack formulation, and a comprehensive experimental study that sets a higher bar for this subfield. The main concern is the stronger threat model, which is partially mitigated by the empirical evidence that data poisoning alone is insufficient, but limits the direct comparability with prior work and the practical scope. The architecture-dependent inconsistency on YOLO and limited defense evaluation are moderate concerns. Overall, the paper advances the state of the art in object-detection backdoor research through improved methodology and evaluation rigor, and will be a useful reference for both attackers and defenders.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept