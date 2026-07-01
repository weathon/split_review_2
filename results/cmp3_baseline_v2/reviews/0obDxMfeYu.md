## Summary

This paper introduces Medix, a median-centric framework for out-of-distribution (OOD) detection that leverages unlabeled “in-the-wild” data. Medix first filters candidate outliers from a wild mixture by minimizing the L₂ distance between the element-wise median (EWM) of wild-sample gradients and the mean InD gradient, then trains a binary OOD detector on the identified outliers and labeled InD data. The authors provide theoretical bounds on both inlier and outlier misclassification rates, showing that median-based filtering remains robust as long as the OOD proportion is below 50%. Extensive experiments on CIFAR-10 and CIFAR-100 against 20 baselines demonstrate that Medix achieves state-of-the-art OOD detection performance.

## Strengths

- **Novel and principled approach.** Using the element-wise median of gradients to identify outliers from unlabeled wild data is a fresh idea that is well motivated by the robustness of the median to contamination. The greedy leave-one-out algorithm is a natural instantiation of the optimization objective.
- **Theoretical guarantees.** The paper provides provable bounds on both inlier and outlier misclassification rates (Theorems 4.1 and 4.2), decomposing errors into contamination, concentration, and separation effects. This is one of the few works offering rigorous theory for the unlabeled wild-data setting.
- **Strong empirical results.** Medix outperforms all 20 baselines on both CIFAR-10 and CIFAR-100 across five OOD test sets, often by large margins (e.g., average FPR95 of 0.80% on CIFAR-10 vs. 3.40% for WOODS). The results are reported with standard deviations over five runs, indicating reliability.
- **Comprehensive evaluation.** The paper compares against a wide range of methods, including those using only InD data and those using wild data, and includes ablation studies, sensitivity analysis, and additional experiments in the appendix.

## Weaknesses

### Fatal
None.

### Major
- **Computational cost of the filtering stage is not addressed.** Algorithm 1 requires, at each iteration, computing the EWM of the current set and then, for every remaining sample, the EWM of the set without that sample. This is O(m²·d) per iteration (where m is the wild-set size and d the gradient dimension), which can be prohibitive for large-scale wild data. The paper mentions efficiency in the appendix but does not provide runtime comparisons or complexity analysis in the main text. This is a significant practical concern.
- **The theoretical bounds are not directly linked to final OOD detection performance.** The theorems bound misclassification in the filtering stage, but the final OOD detector is trained on the filtered outliers. Error propagation from filtering to detector performance is not analyzed, leaving a gap between the theory and the reported results.
- **The method relies on the quality of the InD classifier’s gradients.** If the classifier is poorly calibrated or the gradients are not informative (e.g., due to overfitting or limited InD data), the filtering may degrade. The paper does not discuss this dependency or provide diagnostics.

### Minor
- **The improvement over WOODS is modest on CIFAR-100 (1.32% FPR95 average)**, though it is more substantial on CIFAR-10. The paper’s claim of “outperforming existing methods across the board” is supported, but the margin on the harder dataset is narrower.
- **The experimental setup fixes the contamination ratio π = 0.5.** While this follows prior work, the paper does not explore sensitivity to different π values in the main text (only in the appendix). The theoretical bound requires π < 0.5, so experiments with π near 0.5 are most relevant, but varying π would strengthen the evaluation.
- **Some baselines mentioned in the text (CONJ, DRL) do not appear in the main result tables.** They are listed in Section 5.1 but not included in Tables 1 and 2. The reader is left wondering whether they were omitted or deferred to the appendix without clear indication.

### Trivial
None.

## Nice-to-Haves

- A complexity analysis and wall-clock time comparison with WOODS and other wild-data methods.
- Experiments with varying contamination ratios π (e.g., 0.1, 0.3, 0.5, 0.7) to validate the theoretical bound’s prediction.
- An analysis of how filtering errors (ERR_in, ERR_out) correlate with final OOD detection metrics.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the element-wise median of gradients provides a stable reference point for outlier detection in unlabeled mixtures, with the contamination effect bounded by π/(2(1-π)) as long as OOD samples are not the majority. This is a clean theoretical justification for using a robust central tendency measure in a setting where the mean is easily skewed. The separation effect in Theorem 4.2 also quantifies how far OOD gradients must lie from the InD mean to be reliably detected, offering a design principle for feature spaces.

## Suggestions

1. **Address computational cost.** Provide a complexity analysis of Algorithm 1 and report runtime (or number of gradient evaluations) compared to WOODS. Consider discussing approximations (e.g., mini-batch EWM) to improve scalability.
2. **Connect theory to practice.** Show empirically how the theoretical bounds (ERR_in, ERR_out) relate to the final OOD detection performance (FPR95, AUROC) across different settings.
3. **Include experiments with varying π.** This would directly validate the contamination term in Theorem 4.1 and demonstrate robustness beyond the default π=0.5.
4. **Clarify baseline inclusion.** Either add CONJ and DRL to the main tables or explicitly state why they are omitted (e.g., different experimental protocol).

## Score and Decision

**Score:** 8  
**Decision:** Accept

The paper presents a novel, well-motivated method with solid theoretical backing and strong empirical results. The main concern is the computational cost of the filtering stage, which should be addressed in the final version, but it does not invalidate the core contribution. The work is a valuable addition to the OOD detection literature.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>