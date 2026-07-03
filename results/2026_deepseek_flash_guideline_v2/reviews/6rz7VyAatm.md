The calibration tool is unavailable due to a persistent file access issue. I will proceed based on my thorough reading of the paper and the submitted reviews.

---

## Summary

The paper identifies several evaluation blind spots in existing object-detection backdoor attack literature (Section 3), proposes a new attack method (BadDet+) that augments the detector loss with a log-barrier penalty to unify region misclassification (RMA) and object disappearance (ODA) under a single formulation, and evaluates across four detector architectures on COCO and MTSD with physical-world validation on PTSD. It also introduces the True Detection Rate (TDR) metric to expose duplicate-detection failures in RMA that prior ASR-only evaluations miss.

## Strengths

- **TDR metric directly exposes a critical blind spot in prior RMA evaluations.** Table 2 shows that BadDet achieves 99.45% ASR@50 on FCOS but TDR@50 of 75.94% — meaning ~75% of "successful" attacks by ASR still produce correct-class detections alongside the target. This failure mode was invisible to prior evaluation protocols. BadDet+ reduces TDR@50 to 2.78% while matching ASR@50. This metric is a simple but important contribution to the evaluation toolkit.

- **Unified log-barrier penalty formulation that jointly handles RMA and ODA.** Equations (1)-(2) provide a single mechanism where ODA is treated as RMA with background as the target class. The softmax-compatible variant (Eq. 2) for detectors like Faster R-CNN is a thoughtful addition. This unification is cleaner than treating RMA and ODA as requiring separate training procedures.

- **Demonstrates substantially stronger synthetic-to-physical transfer than prior work.** On PTSD (real traffic sign images, Table 3), BadDet+ achieves ASR@50 of 59.59–85.16% across architectures under Fixed placement. The closest competitor, Morph, reaches at most 54.87% (DINO), and UBA reaches at most 38.05%. This is the strongest evidence of real-world backdoor effectiveness and directly addresses the generalization gap previously highlighted by Doan et al. (2024).

- **Systematic diagnosis of four evaluation blind spots in prior work (Section 3).** The paper catalogues: (i) ASR ignoring retained labels in RMA, (ii) mAP as a poor proxy for ODA success, (iii) absence of trigger scaling/placement robustness checks, and (iv) dependence on curated datasets — and either provides empirical demonstrations or designs controlled baselines to rule out trivial fixes. This diagnostic analysis stands as a valuable contribution independent of the proposed method.

- **Broad evaluation across 4 detector architectures on 2 datasets plus physical-world validation.** Tables 1–4 cover FCOS, Faster R-CNN, DINO, and YOLOv5 on COCO and MTSD, with PTSD for physical validation. This breadth exceeds prior object-detection backdoor evaluations, which typically test one or two architectures.

## Weaknesses

### Fatal
None.

### Major

1. **Threat-model asymmetry in the headline comparative claims.** The abstract states BadDet+ "outperform[s] existing RMA and ODA baselines," but baselines (BadDet, UBA, Align, Morph) are data-poisoning-only attacks — they modify training data but train with the standard detector loss. BadDet+ additionally modifies the training loss via the log-barrier penalty, operating under a strictly stronger threat model (attacker controls training, not just data). While the paper acknowledges this threat-model difference (lines 84–88, conclusion), it does not qualify the "outperforms" claim accordingly. A λ=0 ablation (BadDet+ using standard detector loss, keeping 50% poisoning and otherwise identical training) is missing across all architectures except YOLO (where λ=0 was found optimal). Without this ablation, it is impossible to isolate whether the gains come from the penalty or from the higher poisoning ratio (50%) and training configuration. This asymmetry does not invalidate the method but makes the comparative framing misleading.

2. **YOLO RMA failure undermines the generality claims.** On YOLOv5 RMA (Table 4), BadDet+ underperforms BadDet on both ASR@50 (91.97 vs. 96.57) and TDR@50 (7.54 vs. 3.14) — strictly worse on both metrics. The paper notes that "λ = 0 is optimal for this architecture" (i.e., the penalty should be turned off), but offers no analysis or hypothesis for *why* YOLO behaves differently from the other three architectures. YOLO is one of only four architectures tested; a 25% failure rate is a nontrivial limitation that directly contradicts "consistently effective" language used elsewhere.

### Minor

1. **The YOLO failure is noted but not analyzed.** The paper should at minimum provide an architectural hypothesis (e.g., YOLO's different loss formulation, single-stage vs. two-stage characteristics, or labeling conventions) to guide future work and clarify the method's boundary conditions.

2. **Hyperparameters ρ (IoU threshold) and τ (confidence boundary) are introduced in Equations 1–2 but not stated in the main text.** Their values are presumably in the appendix (which is stripped), but their absence from the main text makes it harder to assess the method at a glance.

3. **Defense evaluation is limited to FT and FT-SAM.** The paper acknowledges this scope explicitly, but the claimed role as a representative "benchmark" (line 260) is limited without testing more diverse defenses (e.g., pruning, input sanitization). This is a scope limitation, not a flaw of the method.

4. **Poisoning-ratio analysis (Figure 3) compares BadDet+ (which uses loss manipulation) against data-poisoning-only baselines** at varying poisoning ratios, but never tests BadDet+ without the penalty at those same ratios. This makes the figure's demonstration of data-poisoning insufficiency somewhat circular — it shows that data-poisoning-only methods fail, but the method used to argue for the stronger threat model is never tested in a data-poisoning-only mode.

### Trivial
None.

## Nice-to-Haves

- A brief discussion of computational overhead from the IoU computations in the penalty term would improve practical usability.
- At least one defense method specifically designed for object detection (beyond generic fine-tuning) would strengthen the benchmark claim, though the authors note this is out of scope for this paper.

## Removed Points

These points were raised by the reviewers but are removed from the main assessment with justification:

- **"Missing ablation of BadDet+ without penalty term"** — Merged into Major weakness 1 (threat-model asymmetry) since the two issues are connected.
- **"Theoretical analysis deferred entirely to Appendix A.7"** — This is standard practice for conference papers; the main text (lines 92, 114) references the appendix clearly.
- **"No discussion of computational cost"** — The paper references a computational analysis in Appendix A.6 (line 114), so the discussion exists, just deferred.
- **"Values of ρ and τ not stated"** — Demoted to Minor (not stated in main text; appendix presumably contains them).
- **"Defense evaluation should include more methods"** — The paper explicitly and repeatedly scopes this out; kept as Minor since it limits the benchmark claim.
- **"Could the metric be measuring a proxy?"** — The TDR metric is well-defined (Section 5.2) and directly measures the claimed failure mode; this is a speculative concern without evidence.
- **"Data-poisoning claim not exhaustive"** — The claim is specifically about the schemes tested; the paper qualifies this implicitly by testing only existing methods.

## Novel Insights

The harsh critic's observation that the threat-model asymmetry is not merely a minor oversight but a structural problem with the paper's comparative framing is genuinely insightful. The paper compares a method with training-time loss manipulation against data-poisoning-only baselines, and the missing λ=0 ablation prevents assessing whether the penalty itself drives the gains. Additionally, the YOLO RMA failure (BadDet+ strictly worse than BadDet on both ASR and TDR) is not just a caveat — for YOLO, the "improvement" claimed by BadDet+ over data-poisoning attacks evaporates completely, reducing to the baseline. This boundary condition is more significant than the paper's brief mention suggests.

## Suggestions

1. **Run the λ=0 ablation** — Train BadDet+ with 50% poisoning but standard detector loss (λ=0) on FCOS, Faster R-CNN, and DINO. This would isolate the penalty's contribution and address the primary comparison concern.
2. **Investigate and explain the YOLO RMA failure** — Provide an architectural analysis (loss function differences, label assignment, or architectural properties) that explains why YOLO requires the penalty to be turned off.
3. **Qualify comparative claims** — In the abstract and results, explicitly note that comparisons are across different threat models (data-poisoning-only vs. training-time loss manipulation), or reframe as "under the stronger threat model of training-time loss manipulation, BadDet+ achieves..."
4. **State ρ and τ values in the main text** for reproducibility.

## Score and Decision

Given that the calibration tool is unavailable, I calibrate based on my own judgment informed by the paper's content.

**Bracket reasoning:** This paper has genuine, independently valuable diagnostic contributions (Section 3, TDR metric) that would be useful even without the proposed method. The method itself shows strong results on 3 of 4 architectures with physical-world validation — exceeding prior work in scope. However, the threat-model asymmetry in comparisons and the unexplained YOLO failure are significant concerns that prevent this from being a clear accept (score 8+). The paper is above borderline reject (score <5) because the diagnostic contributions are real and the method demonstrably works better on most architectures. The paper sits in the **borderline accept to accept** range (roughly 6–7).

**Final score:** 6.5 — The paper makes genuine contributions (diagnosis, TDR metric, unified formulation, physical validation) that are somewhat weakened by a comparison framing that conflates two threat models and an unexplained failure on one of four architectures. These issues are fixable and do not invalidate the core contributions.

**Decision:** Accept — The diagnostic contributions (Section 3) and TDR metric are independently valuable. The method is well-motivated and shows strong results under its stated threat model. The major weaknesses are about framing and missing analysis, not about the validity of the claims. With the suggested revisions (λ=0 ablation, YOLO analysis, qualified claims), the paper would be clearly strong.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>