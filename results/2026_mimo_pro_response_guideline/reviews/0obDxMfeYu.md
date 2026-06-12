## Summary
This paper proposes Medix, a median-centric framework for OOD detection that filters candidate outlier samples from unlabeled wild data using element-wise median (EWM) of gradient deviations, then trains a binary OOD detector on filtered outliers plus labeled InD data. The paper provides theoretical bounds on misclassification rates and reports improvements over 20 baselines on CIFAR-10/100.

## Strengths
- **Well-motivated design via preliminary experiment (Figure 1, Section 3.1):** The paper demonstrates a monotonic increase in L2-norm deviation between the InD mean gradient and the EWM of wild data gradients as OOD contamination increases, directly motivating the optimization formulation in Equation 4. This gives a principled empirical basis for the filtering approach.
- **Two-sided theoretical guarantees (Theorems 4.1, 4.2):** Complementary upper bounds on both inlier misclassification (InD flagged as outlier) and outlier misclassification (OOD retained as inlier), decomposing cleanly into contamination, concentration, and separation effects. This provides genuine insight into when and why median-based filtering works, and constitutes a contribution over prior work where Du et al. (2024a) was the only prior theoretical foundation for the wild setting.
- **Consistent improvements over all baselines (Tables 1, 2):** Medix achieves average FPR95 of 0.80% vs WOODS's 3.40% on CIFAR-10 and 5.42% vs 6.74% on CIFAR-100, winning on every individual OOD dataset and metric when comparing against wild-data methods. Tested against 20 baselines across 11 InD-OOD pairs, demonstrating comprehensive evaluation.
- **Relaxes batch-level mixing assumption (Section 6):** Unlike WOODS and Du et al. (2024a), which require batch-level InD/OOD mixing, Medix operates at the dataset level without requiring structured batch composition—a practically meaningful relaxation.

## Weaknesses

### Fatal
None.

### Major
- **Theory-algorithm gap: theorems analyze the idealized EWM estimator, not the deployed greedy algorithm.** Theorems 4.1 and 4.2 (Section 4, lines 134–148) bound misclassification rates of the element-wise median filtering rule under a Huber contamination model. However, the actually deployed Algorithm 1 (lines 105–120) is a greedy leave-one-out procedure that iteratively removes samples. The theorems do not analyze the approximation quality of this greedy scheme relative to the optimization problem in Eq. 4, nor bound cumulative error from iterative removal. The paper's claim that the theorems provide "provable guarantees for the robustness of Medix's filtering stage" (Section 4) overstates the connection, since the guarantees apply to the idealized median rule rather than the algorithm actually deployed.

- **Theoretical bounds are vacuous at the sole experimental operating point.** At π = 0.5, the contamination terms equal 0.5 in both theorems: π/[2(1−π)] = 0.5/1 = 0.5 for Theorem 4.1, and (1−π)/(2π) = 0.5/1 = 0.5 for Theorem 4.2. These bounds guarantee at most ~50% misclassification—trivially true for any binary classifier. The paper states bounds are "controlled as long as the contamination ratio π < 0.5" (line 138), yet all experiments use π = 0.5 (line 170). Experiments at π ∈ {0.2, 0.3, 0.4} where the bounds are informative would validate the theoretical predictions and substantially strengthen the contribution.

- **Misleading improvement framing via cross-regime comparison.** The abstract prominently claims "outperforming [KNN+] by an average of 40.98% in terms of FPR95" (line 27). KNN+ is an InD-only method without access to wild data, while Medix uses both InD and wild data. The fair same-regime comparison against WOODS shows more modest improvements: 1.32% FPR95 on CIFAR-100 and 2.60% on CIFAR-10 (lines 27, 234). These are genuine but modest, and the 40.98% figure obscures this. Similarly, "Medix reduces the FPR95 by 52.31% on PLACES365 compared to KNN+" (Section 5.3) compares against a method without wild data access.

### Minor
- **Algorithm 1 loop condition appears inconsistent with its text description.** The pseudocode reads "while t ≤ T or |δ_max| > ε" (line 110), meaning the loop continues until *both* conditions fail. The text description says the algorithm "repeats until there is no significant drop in δ_i or a maximum number of iterations is reached" (lines 95–96), which implies termination when *either* condition fails—suggesting "and" rather than "or." This may affect reproducibility if someone implements the pseudocode literally.

- **Hyperparameters tuned on the reported test metric.** ε and k are selected "with the objective of maximizing OOD performance" (line 178), meaning they optimize the very metric being reported on the test data. A held-out validation split would avoid potential optimistic bias. While common in the field, this is worth acknowledging.

### Trivial
None.

## Nice-to-Haves
- Sensitivity to π: testing at multiple contamination levels to validate theoretical predictions and demonstrate robustness across realistic scenarios.
- Ablation of filtering quality vs. detector quality to attribute improvement specifically to the filtering stage.
- Brief main-text discussion of computational cost of the greedy algorithm (deferred to Appendix A.6).
- Fixing the loop condition in Algorithm 1 to match the textual description.

## Removed Points
These points are flagged to be removed, treat them with caution.
- Criticism about missing Appendix content: the paper references appendices (A.1–A.7, C.3) that are stripped from the parsed version but exist in the original submission.
- Nitpick about EWM treating gradient dimensions independently: the paper provides EWM vs. geometric median comparison in Appendix A.1, and the empirical results demonstrate EWM's effectiveness.

## Novel Insights
The core novel observation is using element-wise median of gradient deviations as a robust statistic for separating InD and OOD samples in wild data, with two-sided theoretical analysis decomposing error into contamination, concentration, and separation effects. This median-centric perspective on OOD filtering is a genuine contribution to the wild-data OOD detection literature. The relaxation of batch-level mixing is also a practically relevant advance, though the experiments only test at a single contamination ratio.

## Suggestions
- Add experiments with π < 0.5 (e.g., 0.2, 0.3, 0.4) to validate the theoretical bounds at operating points where they are informative.
- Bridge the theory-algorithm gap, even with a simple argument showing that the greedy approximation preserves error bounds up to a multiplicative or additive factor.
- Reframe the comparison to lead with the WOODS comparison (1–3% improvement) and discuss the KNN+ comparison as demonstrating the value of using wild data.
- Fix the loop condition in Algorithm 1 to match the textual description.

## Calibration Report

**Anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| l5ouuojPGe.md | 3.00 | 1 | Thresholding for NN monitoring — weaker method, lower relevance |
| KK29oh8jZs.md | 3.00 | 1 | OOD synthetic datasets — lower empirical contribution |
| 3ZdGSTxKuy.md | 2.00 | 1 | Atypical video OOD — weaker method |
| i28ZjVxl81.md | 2.50 | 1 | OOD on tabular data — limited scope |
| Cdhxv0Oz1v.md | 4.20 | 1 | GradRect for OOD — gradient-based but no wild setting, weaker results |
| RWZzGkFh3S.md | 4.50 | 1 | Outlier gradient analysis — different task |
| qDFpNXnuYK.md | 5.00 | 1 | Early training OOD — empirical study, rejected |
| jjjxp9Wgjp.md | 4.25 | 1 | Pseudo-labels for OOD — rejected |
| VAmVEghgoC.md | 4.50 | 2 | NC-OOD — similar motivation, rejected |
| Zww4Xqmk38.md | 4.75 | 2 | Tree-based OOD — different method, rejected |
| zUrdd5NRLH.md | 5.00 | 2 | GROD PAC theory — rejected |
| am7BPV3Cwo.md | 5.75 | 2 | Imbalanced OOD — closest comparator, rejected |
| VTYg5ykEGS.md | 6.50 | 1 | ImageNet-OOD benchmark — accepted, different type |
| w0jk3L3IjV.md | 5.67 | 1 | Detection-generalization paradox — rejected |
| mUXdysoxEP.md | 6.75 | 1 | Feature separation OOD — accepted, novel + theory |
| hlijRgXTDK.md | 4.75 | 2 | Pathologies of OOD — critical analysis, rejected |
| bcWwhF8cTZ.md | 5.50 | 2 | Gradient norm for OOD — rejected |
| sZZ3R0lV9f.md | 5.25 | 2 | MixDiff OOD — constrained access, rejected |
| kwCHcaeHrf.md | 5.50 | 2 | SPADE provable OOD — accepted |
| 9qpdDiDQ2H.md | 5.25 | 2 | MetaOOD auto selection — accepted |
| ym0ubZrsmm.md | 5.33 | 2 | Image background for OOD — accepted |

**Round 1 bracket:** 5.0–6.0. The paper is clearly above the 4.0–4.5 rejects (weaker methods, less rigorous evaluation) and comparable to the 5.5–5.75 range where rejected papers with theoretical frameworks and CIFAR evaluations sit. It falls below the 6.5+ accepted papers which had cleaner theory-empirical alignment.

**Final score:** 5.5 — The paper has genuine contributions (novel median-based filtering, two-sided theoretical analysis, consistent empirical improvements, practical relaxation of assumptions) but is held back by misleading comparison framing, a real gap between the theoretical analysis and the deployed algorithm, and vacuous theoretical bounds at the sole experimental operating point.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>