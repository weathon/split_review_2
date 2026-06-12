## Summary
This paper proposes HOMIL, a multi-instance learning framework for whole-slide image classification that extends standard attention-based MIL (ABMIL) by incorporating second-order statistical moments (covariance matrices) alongside first-order moments. The method uses DBSCAN clustering to adaptively group similar patches, reducing computational cost while preserving diagnostic information. Experiments on CAMELYON16 and TCGA-NSCLC datasets show improvements over several MIL baselines in accuracy, AUC, and F1 score, with competitive computational efficiency.

## Strengths
- **Clear statistical motivation**: The paper provides a well-articulated statistical perspective on MIL aggregation, framing ABMIL as first-order moment estimation and convincingly arguing why second-order moments (covariance) could capture complementary information about feature variability and inter-feature relationships that mean-based aggregation misses.
- **Practical computational design**: The DBSCAN-based adaptive clustering is a sensible approach that naturally aligns with WSI characteristics—large clusters for abundant normal tissue, small clusters for rare pathological regions. The reported compression ratios (0.18 and 0.16) and runtime improvements over many baselines demonstrate practical value.
- **Consistent empirical improvements**: The method achieves the best or near-best results across all three metrics (ACC, AUC, F1) on both datasets, with improvements over ABMIL of 2-3% in ACC and F1. The ablation study cleanly isolates the contributions of clustering and second-order moments.

## Weaknesses
### Fatal
None.

### Major
- **Incomplete baseline comparison**: The paper omits several important and recent MIL methods for WSI classification, including DSMIL (Li et al., 2021), DTFD-MIL (Zhang et al., 2022), and ILRA-MIL (Xiang et al., 2023). These methods also address limitations of first-order aggregation and are standard baselines in the WSI-MIL literature. Without comparison, it is unclear whether the gains are genuinely novel or matched by existing approaches.
- **No statistical significance testing**: The paper reports means and standard errors but does not perform any statistical significance tests (e.g., paired t-test, Wilcoxon) to determine whether improvements over baselines are statistically significant. Given the standard errors overlap for several comparisons (e.g., CAMELYON16 AUC: HOMIL 99.23±0.62 vs. S4MIL 99.02±0.87), the claimed improvements may not be reliable.
- **Missing details on second-order representation**: The covariance matrix vectorization via 1D convolution with max-pooling is described but not well motivated. Why is this particular compression scheme chosen over simpler alternatives (e.g., flattening the upper triangle, eigenvalue decomposition, or using the trace)? The choice of kernel size m=64 and T=4 kernels appears arbitrary with no ablation or sensitivity analysis provided for these parameters.
- **Limited evaluation scope**: Only two datasets are used, both binary classification tasks (metastasis detection and lung cancer subtyping). The method is not evaluated on multi-class classification, survival analysis, or other common WSI tasks. Additionally, both datasets are from the same staining type (H&E), and generalization to other stains (e.g., IHC) is not explored.

### Minor
- **The claim that ABMIL becomes a special case when second-order moments are omitted and each cluster contains a single patch** is technically correct but somewhat trivial—any clustering-based method reduces to the per-patch case with singleton clusters.
- **The fusion mechanism** (attention over two moment vectors) is simple but the paper does not analyze whether the learned fusion weights are interpretable or consistent across different slides/tasks.
- **The sensitivity analysis** is mentioned as being in the appendix, which is not available for review. This is a minor concern given the paper's overall clarity.

### Trivial
- The paper states "DBSCAN adaptively adjusts granularity" but DBSCAN's granularity is controlled by fixed hyperparameters (ε and minPts), not truly adaptive in a learned sense. This is a minor wording issue.

## Nice-to-Haves
- An analysis of which types of feature correlations captured by the covariance matrix are most informative for classification (e.g., visualization of the learned covariance structure).
- Evaluation on multi-class datasets (e.g., TCGA kidney cancer subtypes) to test scalability beyond binary tasks.
- A comparison with a simpler second-order baseline that computes the covariance matrix without clustering, to isolate the benefit of clustering from the benefit of second-order moments.

## Novel Insights
The key insight is that treating MIL aggregation as moment estimation opens a principled path to enriching slide-level representations beyond the mean. While second-order statistics have been used in other domains (e.g., texture analysis, style transfer), their application to MIL for WSI classification is relatively underexplored. The paper's observation that DBSCAN's density-adaptive clustering naturally matches the distribution of normal vs. pathological tissue is also a practical insight that could inform future work on adaptive-resolution WSI processing.

## Suggestions
1. Add comparisons with DSMIL, DTFD-MIL, and ILRA-MIL to establish state-of-the-art positioning.
2. Perform statistical significance testing (e.g., paired bootstrap or 5-fold paired t-test) between HOMIL and the top-3 baselines on each dataset.
3. Provide an ablation study on the covariance vectorization parameters (kernel size m, number of kernels T) and justify the chosen values.
4. Evaluate on at least one multi-class dataset (e.g., TCGA-RCC or TCGA-BRCA subtype classification) to demonstrate generalizability.

## Score and Decision
The paper presents a well-motivated and practically sound extension to MIL for WSI classification, with clear empirical gains on two datasets. However, the omission of several important baselines and lack of statistical significance testing weaken the strength of the claims. The contribution is solid but incremental—the core idea (using second-order moments) is not entirely novel in the broader representation learning literature, though its application to WSI-MIL is underexplored. The paper would benefit from addressing the major weaknesses before acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>