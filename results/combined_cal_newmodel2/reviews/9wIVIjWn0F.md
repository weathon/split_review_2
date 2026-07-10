Now let me synthesize everything and write the final review.

**Round 1 bracket:** Based on the calibration anchors, this paper sits between the rejected papers at ~3.75-5.00 (PRO, Analytic TTA) and the accepted papers at 6.00-7.00 (ML-TTA, DOTA, RLCF, DeYO). The most negative favorability items in the paper (dimensionality mismatch at -0.83 and multi-label underspec at -2.29) are less severe than the "limited novelty" criticisms in papers scoring 3.75-5.00 (which had -5.12, -4.03, -3.45) but more negative than anything in accepted papers at 6.00+ (which had no negative favorability on their worst items). However, the paper's strengths have very high favorability (14.81, 11.29, 8.81), comparable to strong accepted papers.

**Narrowing:** Comparing against DOTA (6.00) — accepted but had a -2.45 weakness item for questionable human feedback — our paper has two items below 0 (dimensionality at -0.83, multi-label at -2.29) versus DOTA's one below-0 item. Our paper has underspecification issues that are verifiable from the paper text, making them harder to dismiss than DOTA's speculation about human-feedback value. The ML-TTA paper (6.25) had zero negative favorability items, placing it clearly above our paper. The closest match is PRO (3.75) which had -4.03 and -2.33 for lack of novelty — our paper has stronger novelty but worse specification issues.

**Final placement:** This paper is stronger than PRO (3.75) and Analytic TTA (5.00) due to its genuinely novel core idea and thorough evaluation, but weaker than ML-TTA (6.25) and DOTA (6.00) due to structural underspecification about how the regression tree handles variable-dimensionality inputs — a verifiable gap in the method description. The most plausible score is **5.0**.

Let me compile the final review.

**Anchor summary:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Active TTP | pdzHpQbGrn.md | 2.50 | 1 | Yes | Much weaker — marginal novelty and improvements |
| PRO | KZZbdJ4wff.md | 3.75 | 2 | Yes | Weaker — novelty concerns, but our paper has worse specification |
| Analytic TTA | UhKkWHkvfg.md | 5.00 | 2 | Yes | Similar score but different weaknesses; ours has better novelty but worse underspec |
| DOTA | yD2JMeKumt.md | 6.00 | 2 | Yes | Accepted; our paper's -2.29 and -0.83 items are more negative than DOTA's weakest item |
| ML-TTA | 75PhjtbBdr.md | 6.25 | 1 | Yes | Stronger; no negative favorability items, better specification |
| RLCF | kIP0duasBb.md | 6.67 | 1 | Yes | Stronger; well-received RL-based approach |
| DeYO | 9w3iw8wDuE.md | 7.00 | 1 | Yes | Stronger; principled motivation, thorough experiments |## Summary

This paper proposes Regression-based Test-Time Adaptation (RTA) for CLIP-based image classification. The core idea is to train a lightweight regression model (LightGBM) on pseudo-labeled data to predict the cross-entropy loss of each augmented view from its logits, then select views with the lowest predicted loss for ensembling — replacing standard entropy-based view selection. The method trains once offline on ImageNet validation data and then applies to arbitrary test distributions without further updates.

## Strengths

- **The "Ceiling TTA" analysis (Tables 1 & 2, Section 4.1) is genuinely informative.** By showing what performance is achievable with ground-truth labels for view selection, the paper establishes a clear upper bound (e.g., +19–35 points on ImageNet-A/ImageNet-R with 64 views, ViT-B/16). This quantifies the gap between current TTA and the oracle, a useful empirical observation for the field.

- **The evaluation is broad and consistent.** The paper covers five ImageNet variants, ten cross-domain datasets, three multi-label datasets, and two backbone architectures (RN50, ViT-B/16), with positive results across almost all settings. This is a thorough empirical effort.

- **The method is computationally efficient.** Training LightGBM once offline on ~1000 samples is lightweight, and inference at test time (a tree lookup) adds negligible cost. This is a practical advantage over methods requiring per-instance prompt tuning or cache updates.

## Weaknesses

### Major

1. **The regression model is trained on 1000-dimensional logits (ImageNet classes) but applied to logits of varying dimensionality at test time.** Algorithm 1 trains the tree on logits computed over ImageNet's 1000 classes. Algorithm 2 (steps 6–8) computes logits for `j = 1, …, L` where `L` varies by test dataset (e.g., 37 for Pets, 102 for Flowers, 80 for MSCOCO). The decision tree is then called as `f(s^{x_i^{test}})` (step 9) — but a tree trained on fixed 1000-dimensional inputs cannot accept 37- or 102-dimensional inputs. The paper provides no explanation of how this dimensionality mismatch is resolved: whether through padding, always using 1000 ImageNet class names, feature projection, or some other mechanism. This is a core structural omission that makes the method underspecified as written. The same issue applies to multi-label datasets, where the loss function and label structure differ fundamentally from single-label tasks (sigmoid vs. softmax), yet the paper never defines how the single-label-trained tree applies to binary predictions.

2. **The paper lacks an ablation comparing the learned regression function against simpler alternatives for view selection.** The key question is whether the regression model provides value beyond directly using max softmax probability (or negative entropy) as the selection criterion. The paper shows ground-truth cross-entropy loss far exceeds entropy (Tables 1 & 2), but the regression model trades on *predicting* LCE from logits. An obvious baseline would be: train the regression model, then instead of using its predictions, use raw max logit or max softmax probability to select views, keeping everything else fixed. Without this, it is unclear whether the gains come from the learned mapping or from other aspects (augmentation strategy, filtering ratio, number of views).

### Minor

3. **The regression model is trained only on high-confidence pseudo-labels (max softmax probability ≥ 0.8).** This means the training distribution consists almost entirely of logit patterns from confident/correct predictions, yet at test time the model must predict loss for all views, including uncertain, ambiguous, or OOD ones. The paper does not validate whether the regression model's loss ranking remains reliable on low-confidence logit patterns, where accurate view selection matters most.

4. **Improvements over prior TTA methods for the ViT-B/16 backbone are modest.** On ImageNet variants (Table 3), RTA achieves 65.84% OOD average vs. Zero's 65.03% (+0.81%). On cross-domain datasets (Table 4), RTA achieves 68.70% vs. BCA's 68.59% (essentially tied). BCA outperforms RTA on 5 of 10 cross-domain datasets (Pets, Flowers, DTD, EuroSAT, SUN). The more compelling gains are on RN50, the weaker backbone, suggesting diminishing returns with stronger vision encoders.

5. **All results are reported as point estimates without error bars, confidence intervals, or multiple-run variance.** Given that improvements over some baselines are <1%, statistical noise could change the conclusions.

6. **The training data source "ImageVal-12k" is mentioned but not defined.** It is presumably the ImageNet validation set, but its exact composition is not stated, harming reproducibility.

7. **The DMN baseline matches the base CLIP model exactly on all three RN50 multi-label datasets** (47.53, 75.91, 41.53 mAP). This suggests DMN may not have been properly applied or tuned for this setting, which weakens the baseline comparison.

### Trivial

8. **Table 4 (cross-domain, ViT-B/16) contains a duplicate row:** "TDA [CVPR 2024]" appears twice with different values (67.53 and 65.58 averages).

## Nice-to-Haves

- A sensitivity analysis for the pseudo-label confidence threshold (0.8) would strengthen the robustness claims.
- Feature importance analysis of the trained decision tree would provide insight into what the regression model actually learns.
- Testing on more specialized domains (e.g., medical or satellite imagery) would strengthen the claim of "arbitrary test distributions."

## Removed Points

- Criticisms about the "free lunch" phrasing being misleading: stylistic, not substantive. Removed.
- The claim that the method is not truly "independent of downstream tasks": the paper provides extensive empirical validation across many diverse datasets, supporting the claim within reasonable experimental bounds. Removed.
- Request to compare against Kim et al.'s method trained on ImageNet data: speculative what-if, not a concrete weakness. Removed.
- Sensitivity analysis for the confidence threshold: interesting but not a core flaw. Moved to Nice-to-Haves.
- Missing related works: cannot verify without external sources. Removed.
- Request for feature importance analysis: interesting but not essential. Moved to Nice-to-Haves.

## Novel Insights

The harsh critic's most useful insight — the dimensionality mismatch between the trained regression tree's input space and the variable-length logit vectors at test time — is a genuine and verifiable structural gap in the paper. This is not a minor presentation issue; it is core to whether the method is correctly specified. The critic also correctly identified that the multi-label handling is never defined, which is part of the same underspecification. These observations are more valuable than the standard "add more ablations" criticism because they reveal an actual incompleteness in the method description rather than a suggested improvement.

## Suggestions

1. **Explicitly state how the logit dimensionality mismatch is resolved.** If logits are always computed against 1000 ImageNet class names (even for non-ImageNet test datasets), state this clearly. If dimensionality reduction, padding, or feature selection is used, describe it formally. Without this, the method cannot be reproduced as written.

2. **Add an ablation replacing the regression model's predictions with max softmax probability (or negative entropy)** for view selection, keeping all other aspects of RTA fixed. This directly tests whether the learned mapping provides value beyond simpler measures.

3. **Validate the regression model's prediction quality on low-confidence samples** (confidence < 0.8) by comparing predicted vs. actual cross-entropy loss on a held-out set. Show that the ranking induced by the model remains reliable where it matters most.

4. **Define the multi-label setup explicitly:** state what loss function is used at test time and how the single-label-trained tree applies to multi-label binary predictions.

5. **Add variance estimates** (error bars or confidence intervals) for key results, especially those with <1% margins over baselines.

6. **Define "ImageVal-12k" explicitly** and fix the duplicate TDA row in Table 4.

## Score and Decision

**Calibration Anchors (all rounds):**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to this paper |
|--------|------|-----------|-------|-----------|--------------------------|
| Active TTP | pdzHpQbGrn.md | 2.50 | 1 | Yes | Much weaker — marginal novelty, marginal improvements |
| PRO | KZZbdJ4wff.md | 3.75 | 2 | Yes | Weaker — novelty concerns; our paper has better novelty but worse underspec |
| Analytic TTA | UhKkWHkvfg.md | 5.00 | 2 | Yes | Similar tier — our paper has better novelty but worse specification |
| DOTA | yD2JMeKumt.md | 6.00 | 2 | Yes | Accepted; our paper's -2.29 and -0.83 weakness items are more negative than DOTA's weakest item (-2.45 is close but DOTA had only one such item vs. our two) |
| ML-TTA | 75PhjtbBdr.md | 6.25 | 1 | Yes | Stronger; no negative-favorability weakness items, better specification |
| RLCF / CLIP Reward | kIP0duasBb.md | 6.67 | 1 | Yes | Stronger; well-received RL-based approach with broader task coverage |
| DeYO / "Entropy is not Enough" | 9w3iw8wDuE.md | 7.00 | 1 | Yes | Stronger; principled theoretical motivation, no specification gaps |

**Round 1 bracket:** 3.5–6.0. The paper is clearly above papers scoring 2.50–3.75 (which suffer from marginal novelty, a criticism that does not apply here) but below papers scoring 6.25+ (which have no negative-favorability weakness items).

**Round 2 narrowing:** The two negative-favorability items (dimensionality mismatch at -0.83, multi-label underspec at -2.29) place the paper below ML-TTA (6.25, zero negative items) and DOTA (6.00, one mildly negative item at -2.45). The absence of novelty concerns places it above PRO (3.75) and Analytic TTA (5.00). The closest anchor is Analytic TTA (5.00), but that paper's weakness (-5.12 for limited novelty) is more severe than this paper's underspecification issues, suggesting a slightly higher score.

The paper has a genuinely novel core idea and exceptionally broad evaluation — these are real strengths. However, the structural underspecification about how the regression tree handles variable-dimensionality logits is a verifiable gap that prevents full assessment of the method's correctness and reproducibility. If this issue is resolved and the method is clarified, the paper could be reconsidered.

**Final Score: 5.0** — borderline reject. The core idea is interesting and the evaluation is thorough, but the method's description contains a critical gap (dimensionality mismatch between training and inference) that must be clarified before the contribution can be fully assessed.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>