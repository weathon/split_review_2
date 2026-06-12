## Summary

This paper diagnoses evaluation blind spots in existing backdoor attacks for object detection (e.g., ASR ignoring duplicate detections in RMA, mAP as a poor proxy for ODA) and proposes BadDet+, a unified attack framework that augments the detector loss with a log-barrier penalty to suppress original-class predictions for trigger-bearing objects. The framework covers both region misclassification (RMA) and object disappearance (ODA) attacks, and the authors demonstrate through extensive experiments on COCO, MTSD, and the physical PTSD benchmark that it achieves higher attack success and lower true detection rates than prior work while preserving clean-task mAP.

## Strengths

- **Identifies genuine evaluation weaknesses in prior object-detection backdoor work.** The paper clearly demonstrates that existing methods rely on flawed metrics (ASR alone for RMA, mAP for ODA) and do not test trigger scale/position robustness. The proposed TDR metric and instance-level ASR evaluation are principled improvements that should become standard in this subfield.
- **Technically sound and well-motivated attack formulation.** The log-barrier penalty is derived from an analysis of failure modes; it acts as a soft constraint that suppresses original-class logits on trigger-bearing objects while leaving clean predictions unaffected. The unification of RMA and ODA (treating background as a target class) is clever and grounded in the design of modern detectors.
- **Comprehensive experimental evaluation.** Experiments cover two datasets (including a real-world physical transfer benchmark), four architectures (FCOS, Faster RCNN, DINO, YOLOv5), multiple trigger positions and scales, and an analysis of poisoning ratios. The results consistently show BadDet+ outperforming baselines across both RMA and ODA settings on the key metrics (ASR, TDR, mAP preservation).
- **Exposes the insufficiency of data-poisoning alone.** An important meta-contribution: the paper shows that even with 100% poisoning, existing attacks either fail to achieve consistent backdoor behavior or do so only by sacrificing clean accuracy. This justifies the stronger threat model and motivates the penalty-based approach.
- **Defense evaluation provides practical insights.** While limited to fine-tuning defenses, the experiments show that BadDet+ remains effective after FT/FT-SAM with 2-4% clean data, underscoring that object-detection backdoors require detection-specific defenses.

## Weaknesses

### Fatal
None.

### Major
- **On YOLOv5, BadDet+ underperforms BadDet in RMA (Table 4).** The paper acknowledges this but attributes it to the choice of λ=0.001; however, this suggests the unified penalty formulation is not equally effective across all architectures. Since YOLO is widely used in practice, this limitation weakens the claim of a single generalizable mechanism. The discussion in Appendix A.8 should be supplemented with a clearer explanation of why the penalty fails on this architecture and whether alternative formulations could address it.
- **Defense evaluation is narrow.** The paper evaluates only fine-tuning and FT-SAM, leaving pruning, test-time detection (e.g., TRACE), and input-level defenses for future work. While this is acknowledged, it limits the practical conclusions about robustness. Given that the paper emphasizes the need for detection-specific defenses, a broader empirical defense study would strengthen the paper significantly.

### Minor
- **The physical transfer results still show a substantial performance drop from synthetic to real (e.g., FCOS ODA Fixed: 93.77% → 59.59%).** While BadDet+ vastly outperforms baselines on PTSD, the absolute ASR on physical data is modest for some settings. The paper should discuss whether this gap is fundamental or could be reduced with further augmentation.
- **Hyperparameter sensitivity (λ and poisoning ratio) requires per-architecture tuning.** Appendix A.5 shows that the optimal λ varies across models (e.g., 1 for FCOS, 0.001 for YOLO). This is not a fatal flaw but reduces the plug-and-play nature of the method.
- **Only one trigger pattern (blue square) is used in main experiments.** Alternative triggers are tested only in the appendix. Given that the paper emphasizes trigger-scale and position robustness, more diverse trigger patterns in the main evaluation would be informative.

### Trivial
None.

## Nice-to-Haves
- A comparison with defense-aware adaptive attacks or a discussion of how BadDet+ could be detected would strengthen the paper's contribution as a benchmark.
- Including more recent object detection architectures (e.g., DETR variants beyond DINO) would increase generality.
- The theoretical analysis in Appendix A.7 could be condensed and moved to the main paper to provide a stronger conceptual foundation for the penalty.

## Novel Insights
Beyond the paper's own contributions, the key novel insight is that the failure of existing backdoor attacks in object detection stems not from the model's inability to learn the backdoor mapping, but from the persistence of original-class predictions alongside attack predictions. This observation leads to a reformulation of the attack as a constraint that explicitly suppresses original-class logits, rather than relying solely on poisoned labels. The insight that ODA can be naturally expressed as RMA with background as the target class is elegant and clarifies the relationship between these threat models.

## Suggestions
- Add a discussion on why YOLOv5 is less amenable to the penalty and whether a detector-specific variant of the penalty (e.g., accounting for YOLO's objectness score) could close the gap with BadDet.
- Include a small-scale comparison with at least one non-fine-tuning defense (e.g., a test-time backdoor detector or image compression) to give readers a broader sense of the attack's robustness.
- Clarify in the main text the trade-off between λ and clean mAP: for practitioners wanting to adopt BadDet+, provide concrete guidance on tuning λ for new architectures.

## Score and Decision
BadDet+ makes a clear, well-supported contribution to an important but underexplored area. It identifies evaluation flaws that have misled prior work, proposes principled metrics and a technically motivated attack, and validates it across diverse settings including physical transfer. The limitations (architecture-specific performance, narrow defense evaluation, synthetic-to-real gap) are acknowledged and do not invalidate the core contributions. The paper is a strong candidate for acceptance at ICLR.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>