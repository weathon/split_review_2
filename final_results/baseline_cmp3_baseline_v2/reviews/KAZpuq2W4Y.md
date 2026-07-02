## Summary

This paper proposes HOMIL (Higher-Order Multi-Instance Learning), a framework that extends attention-based MIL for whole-slide image classification by incorporating second-order statistics (covariance matrix of patch features) alongside the conventional first-order mean aggregation. To improve computational efficiency, it uses DBSCAN to adaptively cluster patches, grouping abundant normal tissue coarsely while keeping rare pathological regions fine-grained. Experiments on CAMELYON16 and TCGA-NSCLC show moderate improvements over several baselines, with an ablation study confirming the contribution of each component.

## Strengths

- **Clear motivation**: The paper convincingly argues that first-order moments alone (mean pooling) miss variability and inter-feature relationships in heterogeneous WSIs, making second-order statistics a natural extension.
- **Practical efficiency idea**: Using density-based clustering (DBSCAN) to adaptively reduce the number of instances from thousands of patches to a much smaller set of cluster representations is a practical way to reduce computational cost while preserving diagnostic structure.
- **Ablation study**: The controlled removal of the clustering module and the second-order moment module provides direct evidence of each component’s contribution, showing that both are needed for the best performance.
- **Reproducibility-oriented setup**: All baselines are evaluated in a unified codebase with consistent feature extraction, 5-fold cross-validation with patient-level splits, and reporting of standard errors.

## Weaknesses

### Fatal

None.

### Major

1. **Lack of statistical significance testing**: The reported gains over strong baselines are modest (e.g., CAMELYON16 ACC: 96.98% vs MambaMIL 96.48%, AUC: 99.23% vs ABMIL 98.88%). Standard errors overlap for many comparisons (e.g., HOMIL ACC 96.98±2.43 vs MambaMIL 96.48±1.37), but the paper provides no significance tests (e.g., paired t-test, Wilcoxon, or confidence intervals). Without this, it is impossible to determine whether the improvements are actually meaningful rather than noise from cross-validation folds.

2. **Questionable fairness of runtime comparisons**: The paper states that “Time denotes total computational time across 5 folds (seconds),” with a footnote “including clustering for HOMIL, or training+inference only for other methods.” This is ambiguous: if clustering time is included only for HOMIL, but preprocessing (patch feature extraction) is shared, that may be acceptable. However, the large runtime differences between HOMIL (310s) and expensive baselines like TransMIL (5175s) or MambaMIL (7200s) raise concerns about implementation optimization. The paper does not control for identical batch sizes, sequence lengths, or training procedures beyond a “unified codebase.” The efficiency claim is therefore not rigorously supported.

3. **Incremental novelty**: Using second-order moments (covariance) as a bag-level representation is a direct extension of existing first-order MIL architectures. The covariance compression via 1D convolution is ad-hoc and lacks theoretical justification. DBSCAN clustering for adaptive granularity in WSIs has been explored in prior work (e.g., clustering patches for efficient MIL). The combination, while reasonable, does not present a fundamentally new insight.

4. **Limited experimental scope**: Only two binary classification datasets are used (metastasis detection and lung cancer subtyping). Many WSI benchmarks (e.g., TCGA-RCC, TCGA-BRCA, multi-class subtyping, survival prediction) are not tested. The method’s generalization beyond binary settings and to tasks requiring finer-grained prediction is unknown.

5. **Methodological unclarity in second-order aggregation**: The paper titles Section 4.3.3 “attention-weighted covariance matrix,” but the covariance in Eq. (9) is an unweighted sum of outer products of centered features. The only use of attention is in centering with the first-order representation v^(1). This is technically an “attention-centered” covariance, not an “attention-weighted” covariance. The distinction matters because many prior covariance-pooling methods use explicit weighting.

### Minor

- The paper claims “higher-order moments” but only uses up to second order; the title and abstract might slightly overstate the scope.
- The Conv1D compression of the covariance matrix (Section 4.3.3) is described with an unusual two-stage max-pooling over kernel outputs and then over kernels. The rationale for this specific design (as opposed to standard global covariance pooling or eigen-decomposition) is not explained.

### Trivial

None.

## Nice-to-Haves

- Include multi-class WSI classification (e.g., TCGA kidney or breast cancer subtyping) to demonstrate broader applicability.
- Provide an analysis of how cluster sizes vary across slides and how DBSCAN hyperparameters affect the trade-off between granularity and accuracy (beyond a one-paragraph appendix reference).
- Compare against a variant that uses a weighted covariance (explicitly multiplying by attention weights) to clarify whether attention-weighting the covariance itself helps.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

1. **Add statistical significance testing**: Report p-values or confidence intervals for the primary metrics (ACC, AUC, F1) between HOMIL and the top-2 baselines. Bootstrapped differences or paired 5-fold tests would strengthen the claims.
2. **Clarify runtime measurements**: Explicitly state what is included in the timing for each method (e.g., training only, inference only, preprocessing). Ensure that all methods are run under identical hardware and software configurations with comparable optimization efforts (same learning rate schedule, batch size, etc.). Provide per-epoch timing as a secondary metric.
3. **Justify or simplify covariance compression**: Replace the ad-hoc Conv1D scheme with a standard approach (e.g., vectorizing the upper triangle of the covariance matrix, or performing eigenvalue decomposition and taking the top-d eigenvalues), or provide a clear motivation for why the proposed convolution+max-pooling is beneficial.
4. **Consider additional benchmarks**: Evaluate on multi-class datasets (e.g., TCGA-RCC with 3 subtypes, or TCGA-BRCA with 5 subtypes) to show that the method scales beyond binary classification.

## Score and Decision

Score: 4 (borderline reject)

Rationale: The paper addresses a relevant problem and the framework is clearly motivated, but the core claims of “significant” improvement and “superior computational efficiency” are not convincingly supported due to the absence of statistical significance testing and potentially unfair runtime comparisons. The methodological novelty is modest and the experimental scope is limited to two binary tasks. The paper is well-written and has a solid ablation study, but the evidence is not strong enough to warrant acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>