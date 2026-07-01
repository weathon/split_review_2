Now let me write the final calibrated review.

**Bracket for Round 1:** Based on the comparative analysis, the paper sits between 5.5 and 6.5. The diagnostic contribution (Section 3 + TDR metric) is genuinely valuable and unconditional, placing it above 4–5 range papers. However, the asymmetric threat-model comparison framing, YOLO failure, and overclaimed "invariance" language prevent it from reaching the 7+ range. The closest comparable papers are "Efficient Backdoor Attacks" (5.75, Accept), "Wicked Oddities" (6.0, Accept), and "Backdooring VLMs with OOD" (6.33, Accept) — all accepted papers with substantive contributions but bounded weaknesses similar to ours.

**Final calibration refinement:** Our paper's diagnostic contribution is stronger than those of the 5.75–6.0 papers, but the framing issue is more prominent. Score settles at 6.0.

---

## Summary

This paper identifies critical evaluation blind spots in existing object-detection backdoor attacks — specifically, ASR ignoring retained labels in RMA, mAP as a poor proxy for ODA, lack of robustness checks for trigger scaling/placement, and dataset dependence. It proposes BadDet+, which augments the detector loss with a log-barrier penalty that suppresses true-class predictions for trigger-bearing objects, unifying RMA and ODA under a single formulation. The paper also introduces TDR (True Detection Rate) as a complementary metric for RMA. Evaluation across COCO and MTSD/PTSD with four architectures (FCOS, Faster R-CNN, DINO, YOLOv5) shows strong attack performance, though under a stronger threat model (loss manipulation) than the data-poisoning-only baselines.

## Strengths

1. **Diagnosis of evaluation blind spots in prior work (Section 3).** The identification of four specific failures — ASR ignoring retained labels in RMA, mAP as a poor proxy for ODA, lack of robustness checks for trigger scaling/placement, and dependence on curated datasets — is concrete, well-illustrated (Figure 1), and backed by clear reasoning about why each failure mode inflates reported attack success. This diagnostic is an independent, unconditional contribution.

2. **The TDR metric (Section 5.2).** The True Detection Rate directly captures the duplicate-detection failure mode that ASR misses. Table 2 shows this cleanly: BadDet achieves ASR@50 > 99 on all three COCO architectures but TDR@50 ranges from 44.74 to 75.94, meaning the original class label is still detected alongside the target in most cases. BadDet+ drops TDR@50 to 1.54–3.18 while matching ASR. The metric is simple, interpretable, and directly motivated by the identified failure mode.

3. **Clean formulation unifying RMA and ODA (Section 4/4.1).** The observation that ODA is a special case of RMA with background as the target class is conceptually clean and leads to a single penalty term (Equations 1–2) covering both settings. The IoU-gating condition further restricts the penalty to predictions overlapping the triggered object, which is appropriate.

4. **Evaluation breadth.** Two datasets (COCO, MTSD), four architectures (FCOS, Faster R-CNN, DINO, YOLOv5), multiple trigger positions (fixed and random), plus physical-world transfer to PTSD. This is more comprehensive than any prior work on OD backdoors.

5. **Poisoning ratio analysis (Figure 3).** The demonstration that increasing the poisoning ratio for existing methods either fails to close the gap or does so only by degrading clean mAP provides genuine justification for considering a stronger threat model.

## Weaknesses

### Fatal

None.

### Major

1. **Asymmetric threat model in headline comparisons (Tables 1–4, abstract).** BadDet+ assumes the attacker can modify the training loss function, while baselines (BadDet, UBA, Align, Morph) assume the attacker can only modify training data. The paper is transparent about this in Section 4 ("our design assumes a stronger adversarial setting in which the training process can be controlled"), but the headline presentation conflates the two. The abstract states BadDet+ "outperforming existing RMA and ODA baselines" without signaling the different assumptions, and Tables 1–4 present all methods uniformly without visual distinction. The real finding is "method A under stronger assumptions > methods B–E under weaker assumptions." This does not invalidate the contribution, but the comparison should be reframed as an ablation/justification study demonstrating what the additional capability buys, rather than a conventional head-to-head win.

2. **BadDet+ underperforms BadDet on YOLO for RMA (Table 4).** On YOLOv5 for MTSD RMA, BadDet achieves ASR@50 = 96.57 (Fixed) and TDR@50 = 3.14, while BadDet+ achieves ASR@50 = 91.97 and TDR@50 = 7.54. The paper acknowledges λ = 0 is optimal for this architecture — meaning the proposed penalty is actively harmful. This contradicts the abstract's claim of "consistent applicability across RMA and ODA" and reveals the method is not architecture-agnostic. The failure is mentioned in a single sentence and warrants greater prominence, ideally with root-cause analysis (e.g., whether single-stage architecture, loss structure, or YOLO's handling of background is responsible).

3. **"Position- and scale-invariant" claim is overstated.** The abstract lists "position- and scale-invariant behavior" as a key advantage. However, results show meaningful degradation between Fixed and Random placements even for BadDet+ (e.g., FCOS ODA on MTSD drops from 93.77 to 83.68; DINO RMA on MTSD TDR rises from 2.00 to 5.39). The behavior changes substantially between conditions; BadDet+ is more *robust* than baselines, not *invariant*. This is a clear overclaim and should be corrected throughout.

### Minor

1. **Narrow defense evaluation (Section 5.3, Figure 2).** Only FT and FT-SAM with 2–4% clean data are tested — deliberately weak defenses. The paper scopes this out explicitly in both the Related Work and Conclusion sections, so this is not a hidden flaw. However, the framing in Section 5.3 ("BadDet+ sustains strong performance after both FT and FT-SAM") could create an impression of broader robustness than supported. The paper's own disclaimers mitigate this concern; mentioning the narrow scope earlier in Section 5.3 would help.

2. **Single-run results without variance in main tables (Tables 1–4).** The main attack results report single runs without variance. The defense evaluation (Figure 2) correctly reports ten runs with different random subsets, but the core results lack this rigor. Given acknowledged sensitivity to λ (Appendix A.5) and poisoning ratio, reporting variance across seeds would strengthen confidence.

3. **UBA Box and Align Random are author-designed variants, not established baselines.** The paper creates these as "simple fixes" to address limitations of UBA and Align. While reasonable, these are not existing methods with established parameters. The paper does not discuss whether the modifications change the underlying threat model for these methods.

### Trivial

None.

## Nice-to-Haves

- A brief informal sketch of the theoretical analysis (Appendix A.7) in the main text would help readers assess its substance.
- The YOLO failure mode warrants dedicated analysis — understanding whether single-stage architecture, loss structure, or YOLO's background handling causes the degradation would strengthen the contribution.
- Statistical variance (e.g., across seeds) for the main Tables 1–4 would improve confidence in the results.

## Removed Points

- **"Section 3 claim about poisoning ratio supported only by Figure 3, not a dedicated table"** — REMOVED because Figure 3 explicitly shows the quantitative relationship (mAP Ratio vs. ASR@50/TDR@50) and Appendix A.3 provides numeric breakdown. The criticism is about presentation format, not absence of evidence.
- **Various formatting/presentation observations from the Harsh Critic's "Section-by-Section Notes"** — REMOVED as editorial nitpicks that are either already addressed by the paper or not substantive weaknesses.
- **"Trigger design discussion" suggestion** — REMOVED as speculative; no evidence trigger salience interacts with the penalty in a problematic way.

## Novel Insights

The most valuable cross-review insight is that the paper's two contributions (diagnostic/evaluation protocol vs. attack method) operate under different evidentiary standards. The diagnostic contributions (Section 3, TDR metric, evaluation protocol) are unconditional and stand independently — they identify real blind spots regardless of what attack method one uses. The attack contribution (BadDet+) is conditional on the stronger threat model. The paper currently presents these as a unified package ("we identified limitations... so we propose BadDet+"), which conflates an evaluation critique solvable through better metrics with a method that addresses it only under different assumptions. Separating these explicitly would sharpen both contributions. The YOLO failure further suggests that the penalty formulation may interact with detection paradigms in ways not yet understood — this itself is a useful direction for follow-up.

## Suggestions

1. Reframe the comparison tables to visually distinguish methods operating under different threat models, or reposition the primary comparison as an ablation showing what loss manipulation adds beyond data poisoning.
2. Soften "position- and scale-invariant" to "position- and scale-robust" throughout the paper.
3. Elevate the YOLO RMA limitation from a passing mention to a discussed limitation with potential root-cause analysis (e.g., ablation in the appendix on why λ=0 is optimal for YOLO).
4. Add variance reporting (across seeds) to the main results tables.
5. Include a one-paragraph informal sketch of the theoretical result in the main text.

## Score and Decision

**Calibration anchors (retrieved across rounds):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| LeBD: Run-time Defense Against Backdoor in YOLO | 3.25 | R1 | Weaker paper — narrow scope, single architecture |
| Certified Copy: Resistant Backdoor Attack | 3.00 | R1 | Weaker paper — limited evaluation, unclear contribution |
| Backdoor in Seconds via Model Editing | 4.75 | R1 | Similar structural issues (unfair threat-model comparison) but our diagnostic contribution is stronger |
| Efficient Backdoor Attacks (data-constrained) | 5.75 | R1/R2 | Comparable — both have practical threat model, clear motivation. Our paper has broader evaluation but framing issues |
| Wicked Oddities: Selective Clean-Label Poisoning | 6.00 | R1/R2 | Comparable — both accepted with bounded weaknesses. Our diagnostic contribution is stronger |
| Backdooring VLMs with OOD Data | 6.33 | R1/R2 | Comparable accepted paper — our evaluation breadth is larger, but our framing issues are more prominent |
| Detecting Backdoor Samples in CLIP | 6.00 | R2 | Comparable accepted paper — similar score range |
| Fusion Is Not Enough (3D OD attacks) | 6.25 | R2 | Comparable — accepted attack paper for object detection |

**Round 1 bracket:** 5.5–6.5 (based on comparison to Efficient Backdoor Attacks at 5.75, Wicked Oddities at 6.0, and Backdooring VLMs at 6.33). The diagnostic contribution is strong enough to place this above 4–5 papers, but the asymmetric threat-model framing and YOLO failure prevent reaching 7+.

**Final score determination:** The paper's diagnostic contributions (Section 3, TDR metric, evaluation protocol) are a genuine, unconditional asset to the field. The BadDet+ method is clean and effective under its stated assumptions. The main limitations — asymmetric comparison framing, YOLO failure, overclaimed invariance — are real but bounded and addressable through revisions. Score settles at 6.0, reflecting a borderline accept with required revisions.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>