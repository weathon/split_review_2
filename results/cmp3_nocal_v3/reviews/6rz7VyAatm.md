Here is the final consolidated review:

---

## Summary

This paper introduces BadDet+, a backdoor attack framework for object detection that unifies region misclassification (RMA) and object disappearance (ODA) via a log-barrier penalty term added to the training loss. The paper also contributes a critical evaluation of existing object-detection backdoor evaluation protocols, identifying blind spots in ASR-based RMA evaluation (duplicate detections) and mAP-based ODA evaluation, and proposes TDR as a complementary metric. Empirical results on COCO, MTSD, and the real-world PTSD benchmark show that BadDet+ achieves high attack success while nearly eliminating dual detections on most architectures.

## Strengths

1. **Well-diagnosed evaluation blind spots (Section 3).** The observation that ASR overstates RMA success because it ignores *retained* original-class detections (duplicate detections) is genuinely insightful and clearly demonstrated (Figure 1a). The critique of mAP as a proxy for ODA success — where phantom boxes from zero-area training artifacts depress mAP independently of actual disappearance — is also well-taken. These are non-trivial observations that the object-detection backdoor community has missed. The TDR metric (Section 5.2) is a clean fix for the RMA evaluation gap that has standalone value regardless of the proposed attack.

2. **Strong empirical results on the RMA TDR metric (Tables 2 and 4).** On COCO, BadDet+ reduces TDR@50 to 1.54–3.18% across architectures, compared to BadDet's 44.74–75.94%. On MTSD (FCOS, Faster R-CNN, DINO), the pattern holds: 2.00–6.75% vs. 5.77–85.74%. The near-elimination of dual detections on most architectures is a nontrivial technical achievement.

3. **Physical-world validation (MTSD → PTSD).** The paper evaluates on PTSD, a real-world traffic sign dataset, and shows that BadDet+ maintains meaningful ASR@50 (59–85% across architectures for ODA, 67–90% for RMA) while baselines largely collapse. This is a demanding and honest test that most prior work has not passed.

4. **Poisoning-ratio analysis (Figure 3).** The systematic demonstration that increasing poisoning ratio alone does not fix the failure modes of data-poisoning attacks is valuable. It substantiates the paper's claim that data-poisoning-only approaches have inherent limitations, which provides motivation for considering stronger threat models.

## Weaknesses

### Fatal

None.

### Major

1. **Asymmetric threat model comparison conflates method advantage with attack-surface advantage.** The paper compares BadDet+ (which manipulates the training loss directly) against baselines operating under a strictly more constrained data-poisoning-only threat model. While the paper acknowledges this asymmetry in Section 4 ("our design assumes a stronger adversarial setting") and the conclusion, the abstract claims BadDet+ "outperforms existing RMA and ODA baselines" and the core experimental tables (1–4) are structured as a direct head-to-head comparison without consistently caveating the asymmetry. The baselines are denied access to loss manipulation, so the observed gains conflate the advantage of having a second attack channel with the advantage of the specific penalty design. The paper's own poisoning-ratio analysis (Figure 3) convincingly argues that data-poisoning-only approaches are fundamentally limited — which is a valid motivation for the stronger threat model — but the presentation should more clearly separate two distinct claims: (a) data-poisoning-only is insufficient, and (b) adding loss manipulation via BadDet+ effectively overcomes this. The abstract and introduction should reflect this framing more honestly rather than presenting BadDet+ as a direct outperformer of data-poisoning attacks under equal footing.

### Minor

2. **YOLO RMA results contradict the "consistent applicability" claim.** On YOLOv5m6 for RMA (Table 4), BadDet+ underperforms BadDet: lower ASR@50 (91.97 vs. 96.57 Fixed) and higher TDR@50 (7.54 vs. 3.14 Fixed). The paper states "λ = 0 is optimal for this architecture" (line 221), effectively acknowledging the penalty provides no benefit. The abstract's claim of "consistent applicability across RMA and ODA" is contradicted by RMA on YOLO — one of four architectures tested and among the most widely used in deployment contexts. The paper acknowledges this in the body (lines 221–222) and conclusion, but this should qualify generality claims in the abstract.

3. **Overclaim on "position- and scale-invariant behavior."** The abstract lists "position- and scale-invariant behavior" as a key advantage. However, results show meaningful drops from Fixed to Random trigger positions: e.g., on MTSD ODA (Table 3), BadDet+ ASR@50 drops from 93.77 to 83.68 (FCOS) and 94.90 to 89.38 (Faster R-CNN). On PTSD ODA, the Fixed-to-Random drop for DINO is 85.16 to 76.75. BadDet+ is *more robust* to placement variation than baselines (which often collapse entirely), which is a genuine strength, but "invariant" implies negligible variation and is not supported by the data. Given that the paper's own Section 3 correctly criticizes prior work for testing only fixed trigger positions, precision on this claim matters.

4. **Defense evaluation is thin for the robustness claims made.** The paper tests only fine-tuning (FT) and FT with SAM on 2–4% of clean data, and explicitly scopes other defenses as "out of scope" (Section 2.2, line 58). However, the claim that BadDet+ "still pose[s] a significant threat" after fine-tuning is qualified only qualitatively ("ASR@50 remains above 0.4") without a table of exact post-defense values with standard deviations, despite the defense using ten runs. This makes the robustness claim difficult to evaluate precisely.

5. **PTSD table presentation is ambiguous.** In Table 3, the PTSD ASR@50 cells contain two numbers (e.g., "59.59 62.25" for BadDet+ FCOS ODA Fixed) without explanation of what the two values correspond to. The experimental setup description (lines 129–130) does not clarify this, making the table difficult to interpret.

### Trivial

6. **No variance reporting in main attack tables.** The main results (Tables 1–4) report only point estimates without standard deviations or confidence intervals, even though the defense section uses ten runs.

7. **Hyperparameter λ varies by three orders of magnitude** (1 for FCOS/Faster R-CNN/DINO, 0.001 for YOLO), with sensitivity analysis deferred to the appendix. A brief discussion in the main text would help assess how brittle the method is to this choice.

## Nice-to-Haves

- **Compare against alternative penalty functional forms.** The paper does not compare the log-barrier penalty against simpler alternatives (e.g., hinge-like penalty or cross-entropy term penalizing correct-class predictions). An ablation isolating whether the specific log-barrier form matters would strengthen the method contribution.
- **Add a standard defense calibration point.** Including at least one standard defense known to be somewhat effective (e.g., pruning low-activation neurons or spectral signature filtering) would calibrate how strong BadDet+ actually is relative to known countermeasures, making the robustness claim more meaningful.

## Removed Points

These points from the harsh critic's review were removed with justification:

1. **RMA mechanism underspecified** — REMOVED. The paper explains the mechanism: data poisoning changes ground-truth labels to the target class; the penalty suppresses the original-class logit; the standard classification loss then steers the model toward the (relabeled) target class (Section 4, lines 80–82). The mechanism is adequately described.
2. **Missing appendix content** — REMOVED per instructions. Appendix sections referenced in the paper are stripped by the parser but exist in the original submission.
3. **Reproducibility nitpicks about undisclosed implementation details** — REMOVED per instructions.
4. **Formatting and style nitpicks** — REMOVED per instructions.
5. **Speculation about TDR confidence thresholds** — REMOVED. The critic's question about what counts as "detected" is a reasonable clarification request but does not rise to a weakness; the paper defines TDR using IoU@50, which is standard practice.
6. **Asking for baselines to also have loss-manipulation access** — REMOVED. The critic acknowledges the strengthened UBA/Align variants are "fair and appropriate." Asking for those baselines to also receive loss manipulation would change the fundamental comparison framing in a way the authors explicitly justify as out-of-scope.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Restructure the abstract and introduction to present BadDet+ as a *demonstration of what becomes achievable when training-time loss manipulation is allowed* — not as a direct outperformer of data-poisoning attacks under equal footing. Frame the three contributions (evaluation critique → demonstrating data-poisoning-only is insufficient → BadDet+ as a stronger-threat-model demonstration) as distinct contributions.
2. Add exact post-defense ASR@50 values with standard deviations to the defense analysis (Figure 2), even if only in a supplementary table.
3. Clarify the two-number format in the PTSD rows of Table 3.
4. Replace "position- and scale-invariant" with "more robust to position and scale variation" and qualify "consistent applicability" to acknowledge the YOLO RMA exception.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>