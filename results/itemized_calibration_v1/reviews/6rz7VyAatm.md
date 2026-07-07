Now I have all the calibration data I need. Let me write the final consolidated review.

## Summary

This paper identifies several evaluation blind spots in existing object-detection backdoor research (duplicate detections ignored by ASR in RMA, mAP as a poor proxy for ODA, lack of trigger scale/position robustness testing, reliance on curated data). It proposes BadDet+, a unified backdoor attack framework using a log-barrier penalty that suppresses original-class predictions on trigger-bearing objects, unifying region misclassification (RMA) and object disappearance (ODA). The paper introduces a True Detection Rate (TDR) metric to measure whether the original class survives alongside the target prediction, and evaluates across COCO and MTSD/PTSD with four architectures and physical-world transfer.

## Strengths

1. **Well-diagnosed evaluation blind spots (Section 3).** The paper clearly identifies four genuine problems in prior work: (i) ASR in RMA ignores that the original label can survive alongside the target label; (ii) mAP is a poor proxy for ODA because artifacts like phantom boxes depress mAP without actual disappearance; (iii) existing attacks test only fixed trigger placements; (iv) some approaches rely on curated auxiliary datasets. These critiques are well-articulated, supported by examples, and have lasting value independent of the proposed method.

2. **The TDR metric (Section 5.2).** True Detection Rate directly addresses the RMA evaluation gap by measuring whether the original class prediction survives on a trigger-bearing object. The empirical results (Table 2) starkly illustrate the gap — BadDet achieves ASR@50 >99% across models but TDR@50 between 44% and 76%, meaning the model reports *both* original and target labels for most poisoned objects. This is a genuine methodological improvement.

3. **Convincing poisoning ratio analysis (Fig. 3).** The paper demonstrates that increasing the poisoning ratio for data-poisoning-only methods (UBA, UBA Box, BadDet) either fails to improve attack metrics or does so only while sharply degrading clean mAP. BadDet+ forms a tighter cluster in the desirable top-left region without needing 100% poisoning. This empirical evidence effectively motivates why data poisoning alone may be unreliable.

4. **Broad empirical scope.** Experiments cover two datasets (COCO, MTSD), four architectures (FCOS, Faster RCNN, DINO, YOLOv5), physical-world transfer (MTSD→PTSD), both fixed and random trigger placements, and a defense evaluation. This is an appropriate scope for establishing a benchmark.

## Weaknesses

### Fatal

None.

### Major

1. **Threat model credibility gap.** The paper criticizes prior work for unrealistic assumptions, then introduces a method requiring *training-time loss manipulation* — a stronger assumption than data poisoning. The justification (Section 4, "Threat Model") offers three scenarios: ML-as-a-service, cloud infrastructure, and pretrained weights. None cleanly supports custom loss modification: in MLaaS the customer provides data, not the loss function; the pretrained-weights scenario is a different attack vector entirely (direct weight backdooring). The argument that "data poisoning is unreliable therefore we need loss control" has a circular flavor: a threatening attack is defined as one that works, and the threat model is then defined as whatever is needed to make it work. The paper never concretely identifies a realistic scenario where an adversary would have loss-function control but nothing stronger. This does not invalidate the method — it is a useful demonstration of vulnerability under worst-case assumptions — but the paper frames it as a practical attack, which the evidence does not fully support.

2. **YOLOv5 RMA results contradict the "consistently strong" narrative.** On YOLOv5 (Table 4), BadDet+ underperforms the original BadDet for RMA: ASR@50 91.97 (Fixed) vs. BadDet's 96.57. The paper states "λ = 0 is optimal for this architecture," meaning the proposed penalty is counterproductive for YOLO. YOLO is one of the most widely deployed detectors in safety-critical systems (the paper's motivating application). The paper acknowledges this but defers discussion to an appendix rather than substantively engaging with *why* the penalty fails on this architecture. The claim in the conclusion that BadDet+ "consistently achieves high ASR@50 in both RMA and ODA settings" is inflated by this result.

### Minor

3. **ODA ASR conflates disappearance with misclassification.** The paper defines ODA ASR as "the proportion of these objects for which the original class y_i is not detected" (Section 5.2). This counts any non-detection of the original class as success — including cases where the object is detected as a *different* non-background class (misclassification), not true disappearance (no detection at all). Since BadDet+ unifies RMA and ODA under the same mechanism, the boundary between "repurposed to target class" and "disappeared" is blurred in the evaluation itself.

4. **Per-object independent test protocol deviates from prior work without justification.** The paper evaluates ASR by creating separate test instances where only one object per image is poisoned (Section 5.2). Prior work tests with all objects simultaneously poisoned. Testing one poisoned object at a time creates an easier detection task — the model sees mostly clean inputs with one anomaly — and the paper does not compare results under the prior all-objects-poisoned protocol to show whether conclusions hold under both settings.

5. **Narrow defense evaluation relative to conclusions drawn.** The paper evaluates only fine-tuning (FT) and FT-SAM with 2–4% clean data, then concludes that defenses "cannot simply be transferred from image classification" and that naive fine-tuning is insufficient. The natural baseline for the claimed threat model (attacker controls training) is full retraining from scratch on clean data. Without testing whether that simplest baseline defeats the attack, the claim that specialized defenses are needed is not fully supported. The paper is transparent about scope but overclaims the implication.

6. **Inconsistent claim about "worst-case ASR@50."** Section 5.3 states "BadDet+ achieves consistently strong results across all tested settings, with a worst-case ASR@50 of 96.46" — this is referring to COCO results specifically, but the conclusion generalizes the "consistently high ASR@50" claim broadly without the COCO qualifier, which is misleading given the YOLO ASR@50 of 91.97 on MTSD.

### Trivial

7. No ablation on the IoU threshold ρ (the penalty only activates when predicted-box IoU exceeds ρ; different detectors have different localization accuracy, and the paper does not study sensitivity to this parameter).

## Nice-to-Haves

- If the paper were reframed explicitly as a *worst-case vulnerability demonstration* (rather than a practical attack), the threat model issue would be largely resolved. This would be a clean, defensible framing.
- Testing the full retraining baseline (the most natural defense under the paper's threat model) would strengthen the defense claims.
- A direct comparison of the per-object protocol against the all-objects-poisoned protocol would clarify whether evaluation protocol drives the results.
- Engaging substantively with *why* the penalty fails on YOLO (rather than deferring to an appendix) could produce an interesting architectural insight.

## Removed Points (filtered or merged from input)

- **Theoretical analysis gap (abstract vs. main body).** The abstract promises a "theoretical analysis showing that the proposed penalty acts selectively within a trigger-specific feature subspace" referenced in Appendix A.7. The appendix was stripped by the PDF parser — this is a system artifact, not an author error.
- **Section 3 phantom box claim lacks systematic analysis.** The paper points to Appendix A.2.3 for empirical evaluation of this claim. Without access to the appendix, the claim cannot be evaluated, but the paper does reference supporting evidence.
- **Missing related works.** Cannot be verified without external sources.
- **Formatting/style nitpicks** (PTSD table formatting, figure readability). These are parser artifacts.
- **Reproducibility nitpicks** (undisclosed hyperparameters). Standard for papers of this type.

## Novel Insights

None beyond the paper's own contributions. The diagnostic analysis in Section 3 is the most novel conceptual contribution — the identification of duplicate-detection blind spots in RMA evaluation and the inadequacy of mAP for ODA are clearly demonstrated. The TDR metric is the operationalization of this insight. The log-barrier penalty formulation is a clean technical contribution but not conceptually surprising given the problem analysis.

## Suggestions

1. Reframe BadDet+ explicitly as a *demonstration of vulnerability under worst-case assumptions* (control over training loss) rather than a practical attack, and be honest about the conditions needed to reach this upper bound. This would resolve the threat-model credibility issue without changing any experiments.
2. Add a direct comparison of the per-object test protocol against the all-objects-poisoned protocol to verify that conclusions are not protocol-dependent.
3. Add an ablation on the IoU threshold ρ to show sensitivity.
4. Either include full retraining as a defense baseline, or soften the claim that defenses "cannot simply be transferred" to acknowledge that only fine-tuning-style defenses were tested.
5. Engage substantively with why the penalty fails on YOLO — this could be an interesting finding about architecture-specific backdoor dynamics rather than just a limitation.

## Score and Decision

**Calibration.** I retrieved anchors across score bands using `calibration_search` and itemized the five most thematically relevant:

| Anchor | Score | Round | Itemized | Comparison |
|--------|-------|-------|----------|------------|
| LeBD: Runtime Defense Against Backdoor Attack in YOLO | 3.25 | R1 | Yes | Much less substantive — a straightforward GradCAM→LayerCAM extension. The current paper has genuine diagnostic contributions, a novel metric, and far broader empirical scope. |
| Certified Copy: A Resistant Backdoor Attack | 3.00 | R1 | Yes | Limited novelty (representation similarity loss for evasion already proposed), poor presentation. Current paper is clearly stronger in both contribution and presentation. |
| Gradient Storm: Stronger Backdoor Attacks | 3.00 | R1 | Yes | Minor extension of Sleeper Agent to multi-trigger setting; limited datasets. Current paper has more substance. |
| Robust Backdoor Attack with VSSC Triggers | 4.33 | R1 | Yes | Performance not actually better than baselines; heuristic methodology. Current paper generally outperforms baselines (except YOLO) and has diagnostic contributions. |
| PADetBench: Benchmarking Physical Attacks against OD | 4.75 | R2 | Yes | Benchmark-only paper lacking a specific method contribution. Current paper has a concrete method (log-barrier penalty) plus diagnostic contributions. |
| Efficient Backdoor Attacks in Real-world Scenarios | 5.75 | R1/R2 | Yes | Stronger practical threat model (data-constrained), accepted despite novelty concerns. Current paper has comparable novelty but a weaker threat model justification. |
| VLOOD: Backdooring VLMs with OOD Data | 6.33 | R1/R2 | No | Better threat model realism and practical scenario; stronger overall execution. |

**Initial bracket:** [4.75, 5.5] — above benchmark-only papers like PADetBench (4.75) due to the specific method and diagnostic contributions, but below Efficient Backdoor (5.75) due to the weaker threat model justification.

**Final calibration.** The paper shares positive heavy-weight items with higher-scoring anchors (diagnostic analysis, broad empirical scope, well-motivated formulation) but also shares negative items (limited novelty concerns, threat model credibility issues) that hold it back. What distinguishes this paper from the 3–4 range is the genuine diagnostic contribution and the TDR metric — neither LeBD nor Certified Copy offers anything comparable. What keeps it below the 5.75–6.33 range is primarily the threat model credibility gap: the paper criticizes prior work for unrealistic assumptions while making an even stronger assumption (loss-function control) without adequately justifying it as realistic. Combined with the YOLO counterexample and evaluation protocol concerns, these prevent the paper from reaching the acceptance zone.

**Score:** 5.0  
**Decision:** Reject

The paper has real merit — the diagnostic analysis in Section 3 is valuable, the TDR metric is a genuine improvement, and the empirical scope is appropriate. However, the core framing of BadDet+ as a practical attack is undercut by a threat model (control over the training loss) that the paper does not adequately establish as realistic, while simultaneously criticizing prior work for unrealistic assumptions. The YOLO results and evaluation protocol issues further weaken the narrative. The paper would be substantially stronger if reframed as a worst-case vulnerability demonstration rather than a practical attack, and if the evaluation gaps (YOLO analysis, per-object protocol comparison, defense baselines) were addressed.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>