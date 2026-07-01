## Summary

The paper introduces Medix, a two-stage framework for out-of-distribution (OOD) detection that uses unlabeled wild data. In the first stage, a greedy algorithm iteratively removes wild samples that cause the largest drop in the L2 distance between the element-wise median (EWM) of the remaining wild gradients and the mean InD gradient, thereby isolating candidate outliers. In the second stage, a binary OOD detector is trained on the labeled InD data and the identified outliers. Theoretical bounds on inlier and outlier misclassification rates are provided, and experiments on CIFAR-10 and CIFAR-100 show that Medix outperforms 20 baselines across multiple OOD test sets, often by a wide margin.

## Strengths

- **Novel median-based filtering idea.** Using the element-wise median of gradients as a robust reference for outlier detection in unlabeled wild mixtures is creative and well motivated. The preliminary experiment (Figure 1) clearly shows the monotonic trend that the algorithm exploits.
- **Theoretical guarantees.** Theorems 4.1 and 4.2 provide interpretable upper bounds on both inlier and outlier misclassification rates, decomposing the error into contamination, concentration, and separation terms. Such rigorous analysis is rare for this problem setting and adds credibility.
- **Strong empirical results on standard benchmarks.** Medix achieves the best average FPR95 and AUROC among all compared methods on both CIFAR-10 (e.g., 0.80% FPR95 vs. WOODS 3.40%) and CIFAR-100 (5.42% vs. WOODS 6.74%). The improvements over WOODS, while modest in absolute terms, are consistent across all five OOD test sets.
- **Clear exposition and thorough baseline comparison.** The paper compares against 20 baselines, including both InD-only and wild-data methods, and clearly separates the results.

## Weaknesses

### Major

1. **Computational cost of Algorithm 1 is prohibitive without further justification.** The greedy leave-one-out approach recomputes the element-wise median *per sample removal* at each iteration. A naive implementation would have complexity roughly \(O(T \cdot |S|^2 \cdot d)\), where \(|S|\) can be tens of thousands. The paper defers efficiency evaluation to an appendix that is not provided in the main text. No runtime numbers or complexity analysis are given, making it impossible to judge whether the method scales to realistically sized problems (e.g., ImageNet-scale). This is a serious practical limitation.

2. **The theoretical bounds apply to an “EWM filtering rule” that is not exactly the algorithm run in practice.** Theorems 4.1 and 4.2 analyze a rule that classifies points based on their gradient deviation from the median, but Algorithm 1 iteratively removes the *k* samples that *most reduce the distance* between the median and the InD mean. The connection between the theoretical misclassification bounds and the actual greedy procedure is not formally established. This gap weakens the theoretical claim.

3. **Limited evaluation scope.** Only CIFAR-10 and CIFAR-100 are used as InD datasets. While these are standard, the paper claims wide applicability. Without results on larger-scale datasets (e.g., ImageNet) or more diverse InD distributions, it is unclear whether the strong performance generalises. The “large-scale” study mentioned in the appendix is hidden from the main paper.

4. **Contamination proportion \(\pi\) is fixed at 0.5 in all main experiments, and sensitivity to \(\pi\) is not shown.** The theoretical bound degrades as \(\pi\) approaches 0.5 (the contamination term in Theorem 4.1 diverges). In practice, wild data may contain a majority of OOD samples (\(\pi > 0.5\)). The paper does not evaluate this regime, which limits the confidence in the method’s robustness under realistic shifts.

### Minor

- The improvement over the strongest wild-data baseline (WOODS) is modest (1.32% average FPR95 on CIFAR-100, 2.60% on CIFAR-10). The much larger gains (40.98%) claimed in the abstract compare Medix against KNN+, a method that uses only InD data, which is an apples-to-oranges comparison.
- The greedy algorithm requires two hyperparameters (\(k\) and \(\epsilon\)) that are tuned per dataset. The paper reports robustness in an appendix, but the main text does not include a sensitivity analysis.
- The objective in Eq. (4) is a combinatorial search; the greedy heuristic is not guaranteed to find the optimal subset. No discussion of approximation quality is given.

### Trivial

- Some baseline abbreviations are inconsistent (e.g., “ReaT” → “ReAct”, “Cimpoei” → “Cimpoi” in references). These do not affect evaluation.

## Nice-to-Haves

- A computational complexity analysis (big-O) and actual wall-clock time comparisons against competing methods would greatly strengthen the paper.
- Experiments with varying contamination levels \(\pi\) (e.g., 0.1, 0.3, 0.5, 0.7) would validate the theoretical bound and demonstrate practical robustness.
- A theoretical or empirical link between the filtering error and the final OOD detection performance would make the pipeline self-contained.

## Novel Insights

The key insight is that the element-wise median of gradients, being robust to outliers, can serve as a stable reference for distinguishing InD from OOD samples in unlabeled wild data. The theoretical decomposition into contamination, concentration, and separation effects is novel and provides a principled understanding of when such median-based filtering works. The observation that the median remains stable as long as the OOD proportion is below 50% is practically useful.

## Suggestions

- Include a detailed analysis of the time and memory complexity of Algorithm 1 in the main paper. Provide runtime comparisons with WOODS and other baselines on the CIFAR benchmarks.
- Explicitly state the relationship between the theoretical bound (which analyzes a one-step median rule) and the iterative greedy algorithm. Clarify under what conditions the bounds apply to the output of Algorithm 1.
- Add experiments with different contamination ratios \(\pi\) (e.g., 0.3, 0.5, 0.7) to show the method’s behaviour beyond the default setting.
- Consider rephrasing the 40.98% improvement claim to clearly separate comparisons with InD-only methods vs. wild-data methods.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>  
MY FINAL DECISION: <decision>Accept</decision>