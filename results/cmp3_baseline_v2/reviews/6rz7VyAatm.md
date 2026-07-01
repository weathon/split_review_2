## Summary

This paper introduces BadDet+, a penalty-based backdoor attack framework for object detection that unifies region misclassification attacks (RMA) and object disappearance attacks (ODA) under a single mechanism. The authors identify several evaluation blind spots in prior object detection backdoor work, including reliance on ASR alone (which ignores retained labels in RMA), use of mAP as a proxy for ODA success, and lack of robustness checks for trigger scaling and placement. BadDet+ augments the detector loss with a log-barrier penalty that suppresses true-class predictions for trigger-bearing objects, achieving stronger synthetic-to-physical transfer than prior work across COCO and MTSD/PTSD benchmarks.

## Strengths

- **Comprehensive diagnosis of evaluation flaws in prior work**: The paper systematically identifies four key limitations in existing object detection backdoor evaluations (ASR ignoring retained labels, mAP as a poor ODA proxy, lack of trigger scaling/placement robustness checks, and dependence on curated datasets). This diagnostic contribution is valuable for the community.

- **Principled unified formulation**: The log-barrier penalty framework elegantly unifies RMA and ODA under a single mechanism by treating background as a special target class. The theoretical analysis showing selective activation within a trigger-specific feature subspace provides a solid foundation.

- **Strong empirical results across diverse settings**: BadDet+ achieves consistently high ASR@50 (96%+ in most cases) while dramatically reducing TDR@50 compared to BadDet (e.g., from 75.94% to 2.78% on FCOS COCO RMA). The evaluation spans 2 datasets, 4 architectures, multiple trigger positions, and includes physical-world validation on PTSD.

- **Rigorous evaluation protocol**: The introduction of TDR as a complementary metric for RMA, instance-level ASR for ODA, and systematic testing of trigger scaling/placement robustness sets a higher standard for future work in this area.

## Weaknesses

### Fatal
None.

### Major
- **Limited defense evaluation scope**: The paper only evaluates against fine-tuning-style defenses (FT and FT-SAM) with very small clean subsets (2-4% of MTSD). While the authors acknowledge this limitation, the claim that BadDet+ is "robust" is only supported against a narrow set of defenses. The paper would benefit from at least evaluating against one additional defense category (e.g., input sanitization, pruning, or test-time detection) to strengthen the robustness claims.

- **YOLO results contradict the main narrative**: On YOLOv5 for RMA (Table 4), BadDet+ underperforms BadDet in both ASR@50 (91.97% vs 96.57%) and TDR@50 (7.54% vs 3.14%). The authors note that "λ=0 is optimal for this architecture," which effectively means BadDet+ provides no benefit over the baseline on this architecture. This is a significant caveat that weakens the claim of a "unified" and "consistently effective" approach.

- **The threat model assumption is strong**: BadDet+ assumes control over the training process (loss manipulation), not just data poisoning. While the authors argue this is realistic (third-party ML services, cloud training), this is a substantially stronger threat model than standard data-poisoning backdoors. The paper would benefit from a clearer discussion of when this threat model is and is not applicable in practice.

### Minor
- **The poisoning ratio analysis (Figure 3) is somewhat difficult to interpret**: The scatter plots with color-coded poisoning ratios are dense and the key patterns (BadDet+ forming tighter clusters) are not immediately obvious. A clearer visualization or tabular summary would improve readability.

- **The paper does not evaluate computational overhead**: The log-barrier penalty requires computing IoU between all predicted and ground-truth boxes for poisoned samples. The computational cost relative to standard training is not discussed, which would be useful for practitioners considering adoption.

### Trivial
- The paper uses "MTSd" and "MTSD" inconsistently in tables and text (should be MTSD).

## Nice-to-Haves

- Evaluation against at least one additional defense (e.g., TRACE test-time detection, or a pruning-based approach) would substantially strengthen the robustness claims.
- A sensitivity analysis for the IoU threshold ρ and confidence boundary τ would help practitioners understand how to set these hyperparameters.
- Discussion of whether BadDet+ can be extended to targeted ODA (removing objects of a specific class) would be a natural extension.

## Novel Insights

The key insight is that the failure modes of existing object detection backdoors stem from the detector's continued ability to assign high confidence to the original class on trigger-bearing objects, rather than from an inability to predict the target class. This observation motivates a penalty-based approach that directly suppresses original-class logits, which is fundamentally different from prior data-poisoning approaches that only modify training labels. The theoretical analysis showing that the log-barrier penalty acts selectively within a trigger-specific feature subspace without degrading normal predictions provides a principled explanation for why this approach works. The finding that data-poisoning alone is fundamentally unreliable for object detection backdoors (even at 100% poisoning ratios) is an important negative result that justifies the stronger threat model.

## Suggestions

1. Add at least one additional defense evaluation (e.g., test-time detection or input sanitization) to strengthen the robustness claims, or explicitly reframe the defense claims as "robust to fine-tuning-based defenses" rather than general robustness.

2. Address the YOLO limitation more thoroughly—either explain why BadDet+ fails on this architecture (e.g., architectural differences in how YOLO handles classification vs. regression) or propose a modification that works across all architectures.

3. Include a computational cost analysis (training time overhead) for the log-barrier penalty computation.

## Score and Decision

The paper makes a solid contribution by identifying and addressing evaluation blind spots in object detection backdoor research, introducing a principled unified framework, and providing extensive empirical validation. The main limitations are the narrow defense evaluation and the YOLO caveat. The paper is technically sound, clearly written, and provides value to the community as a stronger benchmark for future defense work. However, the strong threat model assumption and limited defense evaluation prevent it from being a top-tier contribution.

MY FINAL SCORE: 7.0</score>
MY FINAL DECISION: Accept</decision>