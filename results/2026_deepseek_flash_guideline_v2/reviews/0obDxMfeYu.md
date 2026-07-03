The calibration database appears to be inaccessible. I'll proceed with my best judgment based on the paper content and reviews, applying the scoring guidelines carefully.

Let me finalize the review.

## Summary

This paper introduces Medix, a two-stage OOD detection framework that uses the element-wise median (EWM) of gradient vectors to filter outlier candidates from unlabeled wild data, then trains a binary OOD detector on the identified outliers plus labeled InD data. The paper provides provable bounds on inlier/outlier misclassification rates (Theorems 4.1, 4.2) and reports state-of-the-art results across 11 InD-OOD pairs against 20 baselines.

## Strengths

- **Two-sided theoretical guarantees (Theorems 4.1, 4.2).** The paper derives upper bounds on both inlier and outlier misclassification rates for median-based filtering, decomposed into interpretable contamination, concentration, and separation effects. Among wild-data OOD methods, only Du et al. (2024a) provides a theoretical foundation, making this a distinctive contribution.

- **Strong empirical results across diverse benchmarks.** On CIFAR-100 (Table 2), Medix achieves an average FPR95 of 5.42% vs 6.74% for WOODS and 46.40% for KNN+, with all results averaged over five runs. On CIFAR-10 (Table 1), average FPR95 is 0.80% vs 3.40% for WOODS. Medix uses only 25k labeled InD samples (half the full training set), making comparisons with InD-only methods conservative.

- **Relaxation of the batch-level mixing assumption (Section 6).** The paper correctly identifies that prior wild-data methods (WOODS, Du et al.) assume structured per-batch InD/OOD ratios, which is unrealistic for large outsourced datasets. Medix operates at the dataset level without requiring batch-level structure — a genuine methodological advancement.

- **Empirically grounded motivation (Figure 1).** The preliminary experiment demonstrating monotonic increase in gradient deviation as OOD contamination rises directly motivates the optimization in Eq. 4 and the algorithm's stopping criterion.

## Weaknesses

### Fatal
None.

### Major

- **Theory-algorithm disconnect.** Theorems 4.1 and 4.2 analyze a statistical "EWM filtering rule" without referencing Algorithm 1's core parameters (*k*, *T*, *ε*) or the iterative greedy leave-one-out removal procedure. The bounds contain no terms involving the number of points removed per iteration, the convergence threshold, or the sequential dependencies introduced by repeated subset selection. The paper claims (C2, C3) that the theory certifies Medix's performance, but no approximation or regret guarantees connect the greedy algorithm to the analyzed rule. This gap undermines a central contribution — the paper's theoretical support does not directly apply to the method being evaluated.

- **Evaluation protocol conflates wild OOD with test OOD.** The wild mixture is constructed from the *same* OOD dataset used for testing (Section 5.1: "when using PLACES365 as an OOD test set, we construct a wild mixture by combining CIFAR with PLACES365 as wild data and test on PLACES365 as the OOD set"). This means the method observes samples from the test OOD distribution during training (unlabeled), which is not the standard open-world scenario where test OOD distributions are unseen. The paper mentions an "unseen OOD" experiment in Appendix A.4 but defers it; this evaluation should anchor the results given its greater practical relevance.

- **Missing baseline results for claimed comparators.** CONJ (Peng et al., 2024) and DRL (Zhang et al., 2024) are listed as baselines in Section 5.1, and the conclusion claims Medix "outperforms state-of-the-art methods such as WOODS and DRL." Yet neither CONJ nor DRL appears in the main result tables (Tables 1, 2). A comparative claim requires substantiating data.

### Minor

- **Synthetic experiment is uninformative.** The OOD mean is placed 40 standard deviations from the nearest InD mean ([20, 2√3] vs nearest InD center [0, 2√3], σ=0.5). This trivial separation does not demonstrate robustness. A 12.5% false-positive rate among detected outliers in such a setting (Figure 2) is underwhelming.

- **Theoretical bounds are loose.** At π=0.5, Theorem 4.1's contamination term is 0.5 (50% inlier misclassification rate). While these are upper bounds, the looseness limits the practical insight the theory provides.

- **Computational cost unreported in main text.** Algorithm 1's leave-one-out loop (lines 5–7) has O(m²·d) per-iteration cost. The paper defers efficiency to Appendix A.6 without reporting runtime or FLOP counts in the main text, making it difficult for readers to assess practical deployability.

- **Hyperparameter selection may leak test information.** The paper states that *k* and *ε* are selected to "maximize OOD performance" (Section 5.2), potentially creating validation leakage if tuned per InD-OOD pair.

### Trivial
None.

## Nice-to-Haves

- Include Du et al. (2024a) as a direct baseline in the main tables, given it is the most closely related prior work in the same wild-data setting.
- Move the "unseen OOD" experiment (Appendix A.4) to the main paper.

## Removed Points

These points were raised by the reviewers but are removed from the main weaknesses for the reasons stated:

- **"The optimization problem in Eq. 4 is not well-motivated."** — Removed. The paper explicitly motivates it with Figure 1, which demonstrates the monotonic relationship.
- **"Comparison against InD-only methods is unfair."** — Removed. The tables clearly separate method categories, and the paper acknowledges the data advantage. This is standard practice.
- **"Pseudo-label quality dependence not discussed."** — Removed. Addressed in Appendix A.5 (shows resilience to noisy labels).
- **"Batch-level vs dataset-level mixing claim needs clarification."** — Removed. Clearly explained in Section 6.
- **"The 40.98% improvement over KNN+ is misleading."** — Removed. Tables separate methods by category; readers can assess the appropriate comparison.
- **"Gradient independence assumption unrealistic."** — Removed as a major concern but noted as a minor weakness (common in ML theory; many papers make similar assumptions).
- **"CONJ/DRL unreleased/unverifiable."** — Removed. Per hard rules, the paper cites these works; they are assumed to exist.

## Novel Insights

The most consequential insight from the reviews is the gap between the theoretical analysis and the implemented algorithm. The theorems characterize an idealized EWM decision rule under i.i.d. assumptions but never analyze the actual iterative greedy procedure with its sequential removal dynamics. This means the paper's claim of having "theoretical guarantees for Medix" is only partially supported — the bounds apply to a simplified version of the method. Combined with the evaluation protocol where wild OOD matches test OOD, these two issues significantly narrow the gap between what the paper claims and what it demonstrates.

## Suggestions

1. **Align theory with algorithm.** Either modify Algorithm 1 to correspond to the analyzed EWM filtering rule (e.g., replace greedy removal with a one-shot median-based decision), or provide approximation/regret guarantees that bound the greedy procedure's suboptimality relative to the idealized analysis.
2. **Restructure the evaluation around unseen OOD.** Make the setting where P_out^test ≠ P_out the primary experiment and move the matched-setting results to secondary.
3. **Report computational cost in the main text.** Provide wall-clock time or FLOP estimates for Algorithm 1 with realistic dataset sizes.
4. **Include CONJ and DRL results** in the main tables, or remove the comparative claims from the conclusion and Section 5.1.

## Score and Decision

This paper tackles a meaningful problem and proposes a conceptually interesting approach. The empirical results are strong, and relaxing the batch-level mixing assumption is a genuine contribution. However, the theory does not analyze the actual algorithm (undermining C2), and the evaluation protocol (wild OOD = test OOD) limits the practical relevance of the claimed superiority. Additionally, comparative claims are made against baselines that never appear in the tables. These issues are individually addressable but collectively prevent acceptance in the current form.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>