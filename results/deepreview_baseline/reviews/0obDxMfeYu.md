## Summary
This paper introduces Medix, a median-centric framework for out-of-distribution (OOD) detection that leverages unlabeled "in-the-wild" data. The method first filters potential outliers from mixed unlabeled data using element-wise median (EWM) of gradients, then trains a binary OOD detector using the identified outliers and labeled in-distribution data. The authors provide theoretical guarantees bounding both inlier and outlier misclassification rates, and demonstrate empirical superiority over 20 baselines across multiple benchmarks.

## Strengths
- **Novel theoretical contribution**: The paper provides provable bounds on misclassification rates for both inliers and outliers in the filtering stage, which is rare in the OOD detection literature. The analysis decomposes errors into contamination, concentration, and separation effects, offering clear insight into when the method works.
- **Strong empirical results**: Medix achieves state-of-the-art performance across all evaluated InD-OOD pairs, with particularly impressive gains on CIFAR-100 (average FPR95 of 5.42% vs. 6.74% for WOODS). The improvements are consistent and substantial, with low variance across runs.
- **Well-motivated approach**: The median-based filtering is intuitively appealing due to its robustness to outliers, and the authors provide empirical motivation (Figure 1) showing monotonic relationship between OOD contamination and gradient deviation.

## Weaknesses

### Major
- **Computational scalability concern**: Algorithm 1 requires computing the EWM after removing each sample individually (line 6), which is O(m²) per iteration where m is the wild dataset size. For large-scale wild datasets (e.g., millions of samples), this becomes prohibitively expensive. The paper mentions computational efficiency in Appendix A.6 but does not provide wall-clock time comparisons against baselines like WOODS.
- **Limited evaluation on large-scale, realistic settings**: While Appendix A.4 evaluates on ImageNet-scale data, the main experiments are limited to CIFAR-10/100 with relatively small wild datasets (25,000 samples). The method's practicality for real-world deployment where wild data could be orders of magnitude larger is unclear.
- **Sensitivity to the contamination ratio π**: The theoretical guarantees require π < 0.5 for the inlier bound to be meaningful, but real-world wild data could easily exceed this threshold. The paper does not systematically evaluate performance as π approaches or exceeds 0.5.

### Minor
- **The comparison with KNN+ is somewhat misleading**: The paper claims "40.98% improvement" over KNN+, but this is an absolute FPR95 reduction (from 46.40% to 5.42%), not a relative improvement. The framing could be clearer.
- **The synthetic experiment (Figure 2) uses an extreme OOD distribution** (mean at [20, 2√3] vs. InD means near origin), making the separation artificially easy. A more challenging setup with closer OOD distributions would be more informative.

### Trivial
- The notation in Algorithm 1 uses both $\bar{V}_{\text{in}}$ and $\bar{\nabla}_{\text{in}}$ interchangeably, which could cause confusion.

## Nice-to-Haves
- An analysis of how the method performs when the sub-Gaussian assumption is violated (e.g., heavy-tailed gradient distributions) would strengthen the practical claims.
- A comparison with more recent OOD detection methods that also use unlabeled data (e.g., from 2024-2025) would make the evaluation more current.

## Novel Insights
The key insight is that the element-wise median of gradients provides a robust reference point for distinguishing in-distribution from out-of-distribution samples in unlabeled mixtures, with theoretical guarantees that hold as long as OOD contamination is below 50%. This is a principled alternative to heuristic thresholding approaches and provides a clear connection between robust statistics and OOD detection.

## Suggestions
- Provide wall-clock runtime comparisons against WOODS and other baselines to demonstrate practical feasibility.
- Evaluate performance across a wider range of contamination ratios π (e.g., 0.1, 0.3, 0.5, 0.7) to understand the method's limitations.
- Consider a more efficient approximation of the leave-one-out procedure (e.g., influence function-based approximations) to improve scalability.

## Score and Decision
The paper makes a solid contribution with novel theoretical analysis and strong empirical results. The main concern is computational scalability for large-scale applications, but this does not invalidate the core contribution. The method is well-motivated, the theory is sound, and the empirical validation is thorough within the chosen experimental setup.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>