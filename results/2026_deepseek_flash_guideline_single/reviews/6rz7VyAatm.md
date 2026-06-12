Now I have a solid picture of the calibration anchors. Let me write the final review.

**Calibration Anchors Used:**

| Path | Avg Score | Round | Comparison to This Paper |
|------|-----------|-------|-------------------------|
| LeBD (7vKWg2Vdrs) | 3.25 | Round 1 | Weaker — confusing definitions and unexplained performance gaps; our paper's diagnostic contributions and formulation are stronger. |
| PADetBench (9rtlfjWMXI) | 4.75 | Round 1 | Comparable scope (object detection + evaluation protocol), but our paper has stronger diagnostic novelty and technical formulation. |
| VSSC Triggers (H6XiAoyugv) | 4.33 | Round 1 | Similar overclaiming issue (claims not fully supported by evaluation), but our paper's core contributions (Section 3, TDR, unified formulation) are more grounded. |
| Efficient Backdoor Attacks (vRyp2dhEQp) | 5.75 | Round 1 | Accepted. Stronger on realistic threat model but weaker on novelty (idea already explored). Our paper has stronger technical novelty but worse overclaiming. |
| VLOOD (tZozeR3VV7) | 6.33 | Round 1 | Accepted. Practical setting, clean contributions. Our paper has comparable strengths but more significant overclaiming issues. |
| Wicked Oddities (1Z3C49JQVf) | 6.00 | Round 1 | Accepted. Limited datasets, limited novelty. Our paper is similar in overall quality. |
| BDetCLIP (Uqxf2YH9LZ) | 5.75 | Round 1 | Rejected. Strong method but limited scope. Our paper is of comparable quality. |

**Round 1 bracket:** 4.0–6.0

**Final calibration:** The paper's diagnostic contributions (Section 3) and clean technical formulation are genuine assets. However, the contradictory robustness claim (intro claims "more robust under fine-tuning" but RMA defense results show the opposite) and the unqualified threat-model asymmetry are significant framing issues that push the score down from the ~5.75–6.0 range toward the middle. The paper sits between PADetBench (4.75) and Efficient Backdoor Attacks (5.75). Score 5.0 reflects a paper with real but somewhat overclaimed contributions, where the weaknesses are fixable but as written the paper's comparative/robustness framing overstates what the evidence supports.

---

## Summary

This paper identifies evaluation blind spots in existing backdoor attacks for object detection (ASR overstating RMA success by ignoring retained labels, mAP conflating multiple failure modes for ODA effectiveness, lack of trigger scaling/placement robustness, and dependence on curated datasets) and proposes BadDet+, a penalty-based attack framework that unifies region misclassification (RMA) and object disappearance (ODA) under a single log-barrier penalty mechanism. The method augments the detector training loss to suppress original-class logits on trigger-bearing objects, after which the standard classification loss produces the desired behavior (target class for RMA, background/no-prediction for ODA). Evaluation spans COCO and MTSD/PTSD across FCOS, Faster RCNN, DINO, and YOLO architectures.

## Strengths

- **Section 3 diagnoses genuine, non-obvious evaluation blind spots.** The observation that ASR overstates RMA success because backdoored models can produce *both* a target-class detection and an original-class detection is well-motivated with concrete examples (Figure 1). Similarly, the point that mAP is a confounded proxy for ODA effectiveness (reductions can come from duplicate detections, phantom boxes, or localization errors rather than actual disappearance) is a specific, grounded critique. Section 3 alone makes a methodological contribution to the field.

- **The TDR metric directly addresses one diagnosed blind spot.** TDR measures whether the original-class detection actually disappears, which is the dimension ASR alone misses. Tables 2 and 4 show the metric doing real work — BadDet achieves ASR@50 > 99 but TDR@50 of 44–76 (Table 2), cleanly exposing that the attack mostly adds a label rather than replacing one.

- **The log-barrier penalty formulation is clean and principled.** Treating ODA as RMA with background as the target class goes beyond rhetorical unification; it yields Equations 1–2 where a single penalty term suppresses original-class logits for trigger-bearing objects after which the standard classification loss produces the right behavior for both settings. The formulation adapts to both per-class-logit detectors (FCOS, YOLO, DINO) and softmax-based detectors (Faster RCNN) via the log-odds formulation in Equation 2.

- **Comprehensive evaluation along relevant dimensions.** Two datasets (COCO + MTSD/PTSD), four architectures spanning one-stage (FCOS, YOLO), two-stage (Faster RCNN), and DETR-style (DINO) detectors, multiple trigger positions (fixed high/low/both and random), physical-world transfer, and poisoning-ratio analysis (Figure 3). The creation of stronger baselines (UBA Box, Align Random) is methodologically sound.

## Weaknesses

### Major

- **Threat-model asymmetry in comparisons undermines the "outperforms" framing without consistent qualification.** BadDet+ assumes the attacker can modify the training loss (training-time loss manipulation, Section 4). All baselines (BadDet, UBA, Align, Morph) assume data-poisoning only — a strictly weaker threat model. The paper is transparent about this in Sections 4 and 6, but the abstract ("outperforming existing RMA and ODA baselines"), introduction ("yields more robust behavior compared to existing object-detection backdoor attacks under fine-tuning-based defenses"), and results tables present comparisons without consistently noting this asymmetry. The results are valid, but comparing attacks of different classes requires more careful framing.

- **The robustness claim is contradicted by the paper's own RMA defense evidence.** The introduction claims BadDet+ "yields more robust behavior compared to existing object-detection backdoor attacks under fine-tuning-based defenses." Yet Section 5.3 states: "For RMA, BadDet generally outperforms BadDet+ under both FT and FT-SAM." For RMA, the baseline (BadDet, data-poisoning only) retains higher ASR after fine-tuning than the proposed method. The paper reports this honestly but does not analyze *why* a method designed for robustness is *less* robust than its predecessor on one of the two attack types. The subsequent framing ("both BadDet and BadDet+ still pose a significant threat") does not resolve the tension with the stated claim. Since this claim appears in the contribution list, either an explanation or a scope restriction to ODA is needed.

- **YOLO results undermine the generalizability claim.** For RMA on YOLO (Table 4), BadDet+ underperforms BadDet in ASR@50 (91.97 vs. 96.57 for Fixed; 87.04 vs. 93.25 for Random) and TDR@50 (7.54 vs. 3.14). The paper's explanation — "λ=0 is optimal for this architecture" (line 222) — effectively concedes the penalty provides no benefit. This suggests the method's mechanism may be incompatible with YOLO's loss structure or label assignment, but the analysis is deferred entirely to Appendix A.8 (not available in the main body). The paper claims BadDet+ "generalizes effectively across datasets, architectures, and trigger placements" (line 242), but the YOLO result substantially limits this claim.

- **The isolated-object evaluation protocol is not justified.** Section 5.2 states that "for both ODA and RMA, we evaluate each poisonable object independently: for every object, we create a separate test instance in which only that object is poisoned." This means a scene with, e.g., 5 traffic signs is evaluated as 5 separate test images each with one poisoned sign, which differs from the natural scenario where multiple trigger-bearing objects co-occur and could interfere with each other's detection. The paper does not discuss whether this choice could inflate ASR or suppress interference effects. A controlled comparison or clear justification is needed.

### Minor

- **The claim of "position- and scale-invariant behavior" (abstract, item i) is asserted without supporting analysis.** The penalty in Equation 1 activates based on IoU between predicted boxes and trigger-bearing ground-truth boxes, which could still depend on where and at what scale the trigger appears within the object. Since trigger position is a key experimental variable, this claim warrants more explicit support.

## Nice-to-Haves

- The confidence boundary threshold τ is introduced in the formulation but its value is not stated in the main text. A note on its default setting would improve reproducibility.
- The defense evaluation (Figure 2) reports box plots from ten runs without precise numerical summaries or confidence intervals. Reporting key ASR/TDR values with intervals would strengthen the experimental claims.
- A brief YOLO-specific hypothesis in the main text (rather than deferring entirely to Appendix A.8) would help readers assess whether this is a fundamental limitation or a tuning issue.

## Removed Points

These points were identified by reviewers but removed per consolidation rules:

1. **Theoretical analysis deferred to appendix:** The paper references Appendix A.7 for a "more formal perspective." Since the appendix is stripped by the parser and this is a complaint about proofs residing only in the appendix, it is removed per policy. (Including a summary of the key theoretical result in the main text would strengthen the paper but this is a presentation preference, not a verifiable flaw.)
2. **Five-fold contribution list is granular:** Editorial presentation preference, not a substantive weakness.
3. **Table 3 PTSD formatting (e.g., "59.59 62.25"):** Parser artifact from the PDF table structure; the original submission does not have this issue.
4. **Suggestions about paper reorganization:** Removed as editorial/presentation comments.

## Novel Insights

The key insight distinguishing this review from the paper's own analysis is the observation that the threat-model asymmetry creates a systematic framing issue: while the paper is transparent about the stronger threat model in Sections 4 and 6, the abstract and introduction's comparative language ("outperforms") implicitly equates methods operating under different adversarial capabilities. Additionally, the defense evaluation partially *contradicts* the paper's robustness narrative (rather than simply limiting it) — the paper's own Section 6 frames the RMA defense underperformance as merely a scope limitation, but the introduction's explicit claim of "more robust behavior under fine-tuning-based defenses" is unsupported by the RMA evidence presented.

## Suggestions

1. Consistently qualify all comparisons between BadDet+ (training-time loss manipulation) and baselines (data-poisoning only) in the abstract, introduction, and table captions.
2. Reconcile or temper the robustness claim to match the RMA defense evidence — either analyze why BadDet+ underperforms BadDet under fine-tuning for RMA, or scope the robustness claim to ODA only.
3. Include a brief YOLO-specific analysis or hypothesis in the main text rather than deferring entirely to the appendix.
4. Justify the isolated-object evaluation protocol, or provide a controlled comparison showing it does not materially affect ASR values.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>