## Summary

The paper proposes HOMIL (Higher-Order Multi-Instance Learning), a framework for whole-slide image classification that extends attention-based MIL (ABMIL) by incorporating a second-order moment (covariance matrix) of patch features alongside the usual first-order (mean) aggregation. To improve computational efficiency, DBSCAN adaptive clustering groups similar patches into clusters of variable granularity—coarse clusters for abundant normal tissue, fine clusters for rare pathological regions. The first- and second-order representations are fused via learned attention weights and used for slide-level classification. Experiments on CAMELYON16 and TCGA-NSCLC show modest improvements in accuracy, AUC, and F1 over strong baselines, with reduced runtime compared to heavy sequential models.

## Strengths

- **Clinically relevant problem and intuitive motivation.** Capturing both mean and covariance of patch features is a natural extension of first-order MIL, and the paper clearly argues why second-order statistics can capture complementary information beyond an attention-weighted average.
- **Adaptive clustering for efficiency.** Using DBSCAN to create coarse clusters for normal tissue and fine clusters for pathological regions is well-motivated for gigapixel WSIs, and the runtime gains (310s on CAMELYON16 vs. 455s for ABMIL) are demonstrated.
- **Unified experimental setup.** All baselines are implemented in the same codebase with the same pre-extracted CONCH features, and 5-fold patient-level cross-validation is used, which reduces confounding factors in comparisons.

## Weaknesses

### Major
- **Inconsistency in the covariance matrix formulation.** The paper claims to compute an “attention-weighted covariance matrix” (Section 4.3.3), but the formula given is **C = Σ_k (g_k – v^{(1)})(g_k – v^{(1)})^T** without any attention weights. This is an unweighted covariance. If the implementation actually uses attention weights, the paper is incorrect; if it does not, the method doesn’t match the claim. This core inconsistency casts doubt on the correctness of the second-order aggregation.
- **Lack of statistical significance testing.** The reported improvements over strong baselines (e.g., +0.35% AUC on CAMELYON16, +0.83% AUC on TCGA-NSCLC) are small relative to the reported variability (standard errors overlap substantially). Without any statistical test (e.g., paired t-test, confidence intervals, McNemar’s test), the claimed “significant improvement” is not supported. On both datasets, the difference between HOMIL and the best baseline lies well within one standard error.
- **Ad-hoc and poorly motivated covariance vectorization.** The method compresses the d×d covariance matrix to a d-dimensional vector via row-wise 1-D convolution with multiple kernels followed by two stages of max-pooling. This approach is not justified theoretically or empirically; simpler alternatives (e.g., flattening + MLP, eigenvalue decomposition, or diagonal of the covariance) are not considered. The chosen convolution seems arbitrary and may lose information.

### Minor
- **Ambiguity in reported variability.** The tables use notation “mean_{SE} (%),” but it is unclear whether the subscript is standard deviation or standard error. Given only 5 folds, standard error would be very small, which is inconsistent with the large percentage values shown. This should be clarified.
- **Limited analysis of clustering sensitivity.** The paper mentions a sensitivity analysis in the appendix (which is stripped), but the main text provides no discussion of how DBSCAN parameters (ε, minPts) affect performance or clustering granularity. The method’s robustness to these choices is not demonstrated in the main paper.

### Trivial
- The claim that ABMIL becomes a special case of HOMIL is somewhat loose: ABMIL uses attention on patches, while HOMIL without clustering and SOM would use attention on per-patch “clusters” (each cluster of size 1). While similar, the formulation is not identical unless additional assumptions are made.

## Nice-to-Haves

- **Qualitative analysis of what the second-order moments capture.** A visualization of the covariance structure or attention maps showing which clusters contribute most to second-order statistics would strengthen the story.
- **Comparison with other second-order aggregation methods** (e.g., bilinear pooling, second-order pooling via Gram matrices) to better contextualize the contribution.
- **Statistical significance tests** (e.g., bootstrap confidence intervals or paired permutation tests) would clarify whether improvements are reliable.

## Novel Insights

None beyond the paper’s own contributions. The combination of DBSCAN-based adaptive clustering with second-order moments for MIL is a reasonable engineering contribution, but no deeper theoretical or conceptual insight emerges from the paper.

## Suggestions

1. Clarify the covariance formulation: if attention weights are used, show the corrected formula; if not, rename the component and explain why unweighted covariance is still effective.
2. Add statistical significance tests (e.g., 95% confidence intervals for differences or paired non-parametric tests) to support claims of improvement.
3. Simplify or better motivate the covariance vectorization step; at a minimum, compare with a flatten+MLP alternative on one dataset.
4. Clarify the variability metric (SD vs. SE) and report standard deviation to help readers interpret result stability.

## Score and Decision

**Score**: 4 – borderline reject. The paper addresses an important problem and has a sensible core idea, but the major inconsistency in the covariance formulation and the lack of statistical significance for the reported gains undermine confidence in the results. The method improvements are modest, and the weaknesses are not fully resolved in the current form.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>