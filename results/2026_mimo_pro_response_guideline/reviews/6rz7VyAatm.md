## Summary
This paper critiques existing backdoor attacks for object detection by identifying four concrete evaluation blind spots (ASR ignoring retained labels in RMA, mAP as misleading ODA proxy, no trigger scale/placement robustness, curated dataset dependence) and introduces BadDet+, a training-time log-barrier penalty that suppresses original-class predictions on trigger-bearing objects, unifying RMA and ODA under a single mechanism. Evaluation spans COCO and MTSD datasets, four architectures (FCOS, Faster RCNN, DINO, YOLOv5), multiple trigger positions, and physical-world validation on PTSD.

## Strengths
- **Diagnostic evaluation with concrete evidence (Section 3, Figure 1)**: The identification of four specific evaluation blind spots is well-argued with concrete examples. Figure 1 shows BadDet RMA producing dual detections (fire hydrant classified as both car and original class) and UBA producing phantom boxes and duplicate detections. The proposed TDR metric reveals that BadDet's reported 99%+ ASR for RMA masks 44–76% retained original-class detections (Table 2: TDR@50 ranges from 44.74 to 75.94 on COCO), demonstrating a failure mode prior evaluations systematically missed.

- **TDR metric with empirical validation (Section 5.2, Table 2)**: BadDet+ achieves comparable ASR@50 to BadDet (97.27–99.45% vs 99.26–99.48%) while reducing TDR@50 from 44–76% to 1.5–3.2% on COCO, showing the penalty genuinely replaces original-class predictions rather than merely adding target-class detections alongside them.

- **Unified formulation with cross-architecture design (Section 4, Equations 1-2)**: The log-barrier penalty cleanly unifies RMA and ODA with the insight that ODA is a special case where the target is background. The softmax-compatible variant (Eq. 2) for multi-class softmax detectors like Faster RCNN shows careful attention to cross-architecture applicability.

- **Comprehensive evaluation breadth (Tables 1-4)**: 2 datasets (COCO, MTSD), 4 architectures, multiple trigger positions (fixed high/low/both plus random), varying poisoning ratios, and physical-world validation on PTSD. BadDet+ achieves worst-case ASR@50 of 96.46 on COCO ODA (Table 1) and 83.68–97.75 on MTSD ODA (Table 3), substantially outperforming all baselines.

- **Poisoning ratio analysis motivating the stronger threat model (Section 5.3, Figure 3)**: Figure 3 systematically demonstrates that increasing the poisoning ratio for UBA, UBA Box, and BadDet does not reliably improve attack success without degrading clean mAP. BadDet+ forms a tighter cluster in the desirable high-ASR/high-mAP region. This provides strong empirical justification for the stronger threat model.

- **Honest limitation reporting (Conclusion, Table 4)**: The paper transparently acknowledges YOLO underperformance (Table 4, line 221: "On YOLO, BadDet+ underperforms BadDet"), the stronger threat model (lines 84-88), and narrow defense scope (Section 2.2, Conclusion). This transparency supports credibility.

## Weaknesses

### Fatal
None.

### Major
- **Asymmetric threat model weakens the core comparison**: BadDet+ modifies the training loss directly (Section 4: "augments the detector loss with a log-barrier penalty term"), while all baselines (BadDet, UBA, UBA Box, Align, Morph) use the standard data-poisoning paradigm. The paper acknowledges this ("stronger adversarial setting," lines 84-88) and justifies it by showing data poisoning is unreliable (Fig. 3). However, when data-poisoning baselines succeed on a given architecture, the gap narrows dramatically: UBA on DINO achieves ASR@50=97.89 (Table 1) matching BadDet+ at 97.60; for YOLO RMA, BadDet outperforms BadDet+ on all metrics (Table 4: ASR@50 96.57 vs 91.97, TDR@50 3.14 vs 7.54). A matched-conditions comparison (e.g., applying the loss penalty to a baseline method) would isolate whether gains come from the specific penalty design or simply from operating under a stronger threat model.

- **BadDet+ underperforms BadDet on YOLO for RMA, weakening the unified mechanism claim**: Table 4 shows BadDet outperforms BadDet+ on YOLOv5 across all RMA metrics on both MTSD and PTSD. The paper acknowledges "λ=0 is optimal for this architecture" (line 221), meaning the proposed penalty *actively harms* performance on one of four architectures. The conclusion's claim that BadDet+ is "a strong and representative benchmark" (line 260) overstates the case given this architecture-dependent failure.

### Minor
- **ASR definition ambiguity in Section 5.2**: Lines 163-164 first state "we generate a poisoned version of each test image by placing a trigger within the bounding box of every poisonable object," then clarify "for both ODA and RMA, we evaluate each poisonable object independently: for every object, we create a separate test instance in which only that object is poisoned." These describe different evaluation protocols. The independent evaluation (second sentence) is more rigorous, but the first sentence creates confusion about the actual protocol.

- **Defense evaluation scope relative to the conclusion**: The paper tests only FT and FT-SAM with 2-4% clean data, yet concludes (line 262) that "backdoor defenses in object detection cannot simply be transferred from image classification." This conclusion is too strong when only fine-tuning defenses were tested. The paper honestly scopes out other defenses (Section 2.2) but the conclusion then overreaches.

- **No error bars in main results**: Tables 1-4 report single-point estimates with no confidence intervals or standard deviations. Given training stochasticity (data poisoning selection, training randomness), reporting variance across multiple runs would strengthen confidence. The defense evaluation uses 10 runs (good), but the main attack evaluation does not.

- **Abstract promises theoretical analysis deferred entirely to appendix**: The abstract claims "a theoretical analysis showing that the proposed penalty acts selectively within a trigger-specific feature subspace," but this is entirely in Appendix A.7. Section 4 provides only informal "design rationale." The abstract's claim should be qualified.

### Trivial
- **τ and ρ hyperparameters lack sensitivity analysis in main text**: The confidence boundary τ and IoU threshold ρ (Eq. 1) are critical to the penalty's behavior — the log barrier only activates when the original-class logit exceeds τ. While λ sensitivity is studied in Appendix A.5, τ and ρ receive no main-text analysis.

## Nice-to-Haves
- Include the key result from Appendix A.7 in the main text to substantiate the abstract's theoretical claim.
- A brief architectural analysis of why the penalty harms YOLO (in main text, not just Appendix A.8).
- Adding one additional defense class (e.g., JPEG compression or Gaussian noise) to strengthen practical relevance claims.
- A matched-conditions comparison isolating whether gains come from penalty design or the stronger threat model.

## Removed Points
These points are flagged to be removed, treat them with caution.
- None removed from reviewers. All kept weaknesses have been verified against specific passages in the paper.

## Novel Insights
The paper's most valuable insight is that ASR as typically computed for RMA is deeply misleading — it counts misclassification as "success" even when the original class is still detected alongside the target class (Table 2: BadDet achieves 99%+ ASR but 44–76% TDR). The TDR metric exposes this failure mode and is a genuine diagnostic contribution that stands independently of BadDet+. The poisoning ratio analysis (Figure 3) provides a complementary finding: data-poisoning approaches for object detection are fundamentally unreliable, with increasing poisoning ratios either failing to improve attack success or degrading clean performance, motivating rethinking the standard threat model. These two insights alone would make the paper a valuable contribution to the object-detection security community.

## Suggestions
- Clarify the ASR evaluation protocol in Section 5.2 to resolve the ambiguity between "every poisonable object" and "independently."
- Include key theoretical insight from Appendix A.7 in the main text to substantiate the abstract's claim.
- Add variance reporting (error bars or confidence intervals) to main results tables.
- Reframe the conclusion to match the defense evaluation scope — soften the "cannot simply be transferred" claim to note it applies specifically to fine-tuning defenses.
- Add a matched-conditions comparison to isolate whether gains come from the penalty design or the stronger capability.

## Score and Decision

**Calibration anchors retrieved across all rounds:**

| Paper | Avg Score | Decision | Round | Comparison |
|-------|-----------|----------|-------|------------|
| PADetBench | 4.75 | Reject | 1 | Benchmarking physical attacks on OD; BadDet+ is stronger — it contributes both a novel method and diagnostic evaluation |
| LeBD (YOLO defense) | 3.25 | Reject | 1 | Backdoor defense for YOLO, limited novelty; BadDet+ has far broader evaluation |
| VSSC Triggers | 4.33 | Reject | 1 | Weak experimental support; BadDet+ has stronger evidence |
| Efficient Backdoor Attacks | 5.75 | Accept | 1,2 | Novel attack for data-constrained scenarios; BadDet+ has comparable breadth plus unique diagnostic contributions |
| Wicked Oddities | 6.00 | Accept | 1 | Clean-label backdoor with selection strategy; BadDet+ has comparable value plus TDR/diagnostic contributions |
| Backdooring VLMs | 6.33 | Accept | 1 | Backdoor on VLMs with OOD data; BadDet+ has comparable contribution depth |
| A Closer Look at Backdoor on CLIP | 5.25 | Reject | 2 | Empirical analysis; BadDet+ has more actionable contributions |
| Boosting Backdoor Attack | 5.50 | Reject | 2 | Sample selection for backdoor; BadDet+ has broader evaluation |
| LIME-Eval | 6.25 | Reject | 2 | Evaluation methodology critique; BadDet+ has both critique AND novel method |

**Round 1 bracket: 5.5–6.5.** BadDet+ is clearly above PADetBench (4.75, rejected) due to its method contribution and diagnostic framework, and comparable to "Efficient Backdoor Attacks" (5.75, accepted) and "Wicked Oddities" (6.00, accepted).

**Round 2 narrowed to 5.75–6.25.** Direct comparisons confirm BadDet+ is at least as strong as the 5.75 anchor (broader evaluation, TDR contribution) but below 6.33 (the asymmetric threat model and YOLO failure temper the contribution).

**Final score: 6.0** — A solid paper with genuine diagnostic contributions (TDR metric, blind spot identification) and a method that works on 3/4 architectures, tempered by the asymmetric threat model and YOLO failure. The diagnostic contributions alone make this a worthwhile accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>