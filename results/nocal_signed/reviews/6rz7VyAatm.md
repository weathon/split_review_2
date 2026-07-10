Now let me produce the final review.

## Summary

This paper identifies several evaluation blind spots in backdoor attacks for object detection (ASR ignoring retained labels in RMA, mAP as a confounded ODA proxy, trigger scaling/placement issues), introduces the True Detection Rate (TDR) metric to complement ASR, and proposes BadDet+, a unified penalty-based attack framework. BadDet+ augments the detector loss with a log-barrier penalty that suppresses original-class predictions on trigger-bearing objects, unifying RMA and ODA under a single mechanism. The paper provides extensive evaluation across 2 datasets, 4 architectures, and a physical-world benchmark (PTSD), showing that BadDet+ produces more reliable backdoor behavior than prior data-poisoning-only methods.

## Strengths

- **Diagnostic analysis of evaluation blind spots (Section 3, concretely demonstrated in Table 2).** The paper correctly identifies that prior RMA evaluation uses ASR alone while ignoring retained labels (duplicate detections of the original class), and ODA evaluation uses mAP which is a confounded proxy. The introduction of TDR as a complementary metric for RMA is a simple but useful diagnostic contribution. Table 2 makes the point concretely: BadDet's RMA achieves ~99% ASR@50 but ~75% TDR@50 on FCOS — ASR alone dramatically overstates attack success.

- **Physical-world validation on PTSD (Tables 3 and 4).** Prior work had noted poor synthetic-to-physical transfer for object-detection backdoors. BadDet+ achieves meaningfully higher ASR@50 on the real-world PTSD benchmark across four architectures compared to all baselines (e.g., FCOS PTSD ODA: 59.59–62.25 vs. Morph's 15.22, UBA's 15.37). This is non-trivial experimental work that adds credibility to the attack's real-world relevance.

- **Principled log-barrier formulation (Section 4.1, Equations 1–2).** The penalty is clean: it activates only when a predicted box overlaps a trigger-bearing ground-truth box and assigns high confidence to the original class. The softplus/log-barrier form provides a natural "penalty wall" that is inactive below threshold τ and sharply increasing above it. The unified treatment of ODA as RMA with background as the target class is conceptually elegant and emerges naturally from treating background as another class in the detector's output space.

- **Extensive and honest scoping.** The paper evaluates across multiple architectures (FCOS, Faster RCNN, DINO, YOLOv5), two datasets (COCO, MTSD), multiple trigger placements, and physical-world transfer. The limitations paragraph (line 262) and scope section (line 58) are unusually detailed and honest for this type of paper.

## Weaknesses

### Fatal
None.

### Major

- **Comparison conflates threat-model advantage with method advantage (Issue 1).** BadDet+ assumes a strictly stronger threat model — it modifies the training loss during optimization (L = L_det + λP_atk). The baselines (BadDet, UBA, Align, Morph) only poison the training data and train normally. The paper acknowledges this asymmetry (lines 84–88, 262) but then presents Tables 1–4 as head-to-head comparisons, and the Abstract states that BadDet+ "outperforms existing RMA and ODA baselines" without qualifying the threat-model difference. The results primarily show that having access to the training loss is more powerful than data-poisoning-only — which is expected. The separate diagnostic contribution showing data-poisoning insufficiency (Fig. 3) is convincing and does not rely on this comparison. The head-to-head tables should clearly flag the different threat-model assumptions, and the Abstract's "outperforms" claim should be scoped accordingly.

- **ODA ASR definition has the same blind spot the paper criticizes in prior RMA work (Issue 2).** For ODA, ASR is defined (line 164) as "the proportion of these objects for which the original class y_i is not detected." This means any detection that is not the original class — including detections of a *different non-background class* — counts as a successful disappearance. But an object detected as the wrong class has not disappeared; it has been misclassified. The paper's own critique of prior RMA evaluation (Section 3: ASR overstates success when disappearance of the true label is not actually achieved) applies symmetrically to its own ODA ASR metric. The paper should either define ODA ASR as requiring that *no* detection (of any class) is associated with the object, or justify why misclassifications are acceptable for ODA but not for RMA.

### Minor

- **Isolated-object evaluation protocol limits ecological validity (Issue 3).** The paper evaluates ASR by creating separate test instances where exactly one object is poisoned per image (line 164). This avoids interactions between multiple triggered objects via NMS and global context. In a real attack, an adversary would place triggers on multiple objects in the same scene, and NMS interactions between nearby triggered objects could affect behavior. A multi-object evaluation would strengthen claims about practical attack effectiveness.

- **BadDet+ fails to outperform the baseline BadDet on YOLOv5 for RMA (Issue 4).** In Table 4, BadDet+ achieves ASR@50 of 91.97 vs. BadDet's 96.57 and TDR@50 of 7.54 vs. BadDet's 3.14 on YOLOv5 RMA Fixed. The paper states that λ = 0 is optimal for this architecture (line 221), meaning the core contribution (the log-barrier penalty) provides no benefit and actually hurts on 1 of 4 architectures tested. This is a meaningful scope restriction that is acknowledged in the conclusion (line 262) and Appendix A.8 (stripped) but could be surfaced more prominently (e.g., in the Abstract or Introduction).

### Trivial

- Hyperparameter τ (confidence boundary) is defined in Equations (1)–(2) and discussed conceptually but its numerical value and selection procedure are not reported in the main text.
- Computational cost of the IoU-based penalty (Equation 1) is not discussed in the main text. The paper references a computational analysis in Appendix A.6 (stripped) but wall-clock overhead relative to standard training should be stated in the main body.

## Nice-to-Haves

- Add a multi-object evaluation scenario where multiple poisoned objects appear in the same image, to test NMS interference effects.
- Report the numerical value of τ and τ' in the main text.
- Surface the YOLO RMA limitation in the Abstract so readers can calibrate expectations from the start.

## Removed Points

These points from the input review were removed, treat them with caution:
1. **Code availability concern (footnote 1).** Removed per policy: criticisms questioning the release status of cited resources are not permissible.
2. **Defense analysis is too narrow (Issue 5).** Removed: The paper explicitly scopes its defense evaluation (line 58: "deliberately restricted to fine-tuning-style defenses") and does not claim to have evaluated all defenses. The conclusion that fine-tuning alone is insufficient is supported by the evidence. The call for detection-specific defenses is a reasonable forward-looking statement.
3. **Generic strengths** (about the paper addressing an "important problem") removed — not specific or grounded enough to retain.

## Novel Insights

None beyond the paper's own contributions. The key insight — that existing backdoor attack evaluations in object detection suffer from confounded metrics and that a log-barrier penalty can unify RMA and ODA — is already well articulated in the paper itself.

## Suggestions

1. Restructure the comparison in Tables 1–4 to clearly label which threat model each method operates under, and qualify the "outperforms" claim in the Abstract to acknowledge the stronger threat model assumed by BadDet+.
2. Fix the ODA ASR definition to require that no detection (of any class) is associated with the object, making the ODA evaluation symmetric with the RMA TDR critique.
3. Report the value of τ and τ' in the main text.
4. Add a brief statement about training-time overhead in the main text.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>