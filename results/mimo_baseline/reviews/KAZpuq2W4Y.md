## Summary

This paper proposes HOMIL, a multi-instance learning framework for whole-slide image classification that enriches slide-level representations by combining first-order moments (attention-weighted mean of patch features) with second-order moments (covariance matrices of patch features). To manage computational cost, DBSCAN clustering adaptively groups patches into variable-sized clusters—fine-grained for rare pathological regions and coarse-grained for abundant normal tissues. Experiments on CAMELYON16 and TCGA-NSCLC demonstrate improvements over nine MIL baselines in accuracy, AUC, and F1 while maintaining competitive or superior runtime efficiency.

## Strengths

- **Clean statistical motivation**: The paper provides a clear and intuitive statistical interpretation of ABMIL as a first-order moment estimator and motivates the addition of second-order moments to capture feature variability and inter-feature correlations. This framing is elegant and makes the contribution easy to understand.

- **Comprehensive baselines and fair comparison**: The paper compares against nine MIL baselines (ABMIL, CLAM-SB, CLAM-MB, TransMIL, S4MIL, MambaMIL, HMIL, plus simple pooling) implemented in a unified codebase with consistent 5-fold cross-validation splits, which demonstrates experimental rigor.

- **Strong computational efficiency**: HOMIL achieves total 5-fold runtimes of 310s on CAMELYON16 and 3685s on TCGA-NSCLC, outperforming or matching most baselines (e.g., TransMIL at 48710s, HMIL at 32400s on TCGA-NSCLC) while achieving top accuracy. The adaptive clustering reduces patch counts to ~16-18% of the original, validating the efficiency gains.

- **Ablation study confirms component synergy**: The ablation on CAMELYON16 shows that both the Clustering Module and Second-Order Moment module contribute positively: removing CM increases runtime by 71% and drops ACC by 1.26%; removing SOM drops ACC by 1.0%; and removing both (ABMIL) yields the worst results.

## Weaknesses

### Fatal

None.

### Major

- **Mismatch between claimed and implemented covariance computation**: The paper claims to compute an "attention-weighted covariance matrix" (Section 4.3.3), yet the actual formula $\mathbf{C} = \sum_{k=1}^K \tilde{\mathbf{g}}_k \tilde{\mathbf{g}}_k^\top$ assigns equal weight to all clusters. A true attention-weighted covariance would be $\mathbf{C} = \sum_{k=1}^K a_k \tilde{\mathbf{g}}_k \tilde{\mathbf{g}}_k^\top$. While centering uses the attention-weighted mean $\mathbf{v}^{(1)}$, the covariance sum itself is uniform. This is a substantive discrepancy that affects interpretation—important clusters should dominate the covariance, but currently all clusters contribute equally.

- **Unclear statistical significance of improvements**: The reported standard errors frequently overlap between HOMIL and the strongest baselines. On CAMELYON16: HOMIL ACC 96.98±2.43% vs. MambaMIL 96.48±1.37%; on TCGA-NSCLC: HOMIL ACC 93.24±2.47% vs. HMIL 92.89±1.45%. Without formal significance testing (e.g., paired t-test, DeLong test for AUC), it is difficult to determine whether the improvements are statistically meaningful or within noise.

- **Limited experimental scope**: Only two datasets are evaluated, and the ablation study is conducted on only one (CAMELYON16). More diverse benchmarks (e.g., colorectal cancer subtyping, multi-class settings with >2 classes) and ablations on both datasets would substantially strengthen the generalizability claims.

### Minor

- **The covariance vectorization via 1D convolution is somewhat ad hoc**: The paper applies row-wise 1D convolution with max-pooling to compress the 512×512 covariance matrix into a 512-dimensional vector. While functional, this choice lacks theoretical grounding and the interaction between kernel size (m=64), number of kernels (T=4), and the resulting information loss is not analyzed. Alternative approaches (e.g., eigendecomposition, matrix power normalization, or log-Euclidean mapping) might preserve more structural information.

- **The "w/o SOM" variant shows mixed results**: On CAMELYON16, clustering without second-order moments yields AUC 98.51%, which is actually *lower* than ABMIL's 98.88%. This suggests that clustering alone (with only first-order aggregation on clusters) can hurt AUC relative to per-patch attention, a nuance worth discussing.

- **The second-order moment contribution diminishes during training**: Figure 2(b) shows $\alpha^{(2)}$ decreasing from ~0.5 to ~0.4 while $\alpha^{(1)}$ increases to ~0.6. While the paper interprets this positively, it also raises the question of whether the second-order component provides marginal benefit that might not generalize robustly.

### Trivial

- The paper references a sensitivity analysis in an appendix that is not included here, which is expected given parser limitations.

## Nice-to-Haves

- Providing p-values or confidence intervals for the key comparisons against the strongest baselines
- Evaluating on at least one more dataset or a multi-class setting
- Analyzing what types of covariance patterns the model learns (e.g., which feature dimensions co-vary most)
- Comparing the unweighted vs. attention-weighted covariance formulation as an additional ablation

## Novel Insights

The paper's key insight—that the standard attention-weighted mean pooling in MIL corresponds to a first-order moment estimator and can be extended with second-order statistics—is genuinely useful as a conceptual framework, even though higher-order pooling has been explored in other vision tasks (e.g., bilinear pooling). The observation that DBSCAN's density-adaptive clustering naturally aligns with WSI characteristics (large clusters for normal tissue, small clusters for rare pathology) is a practical and well-motivated design choice that offers computational benefits beyond just the statistical moment contribution.

## Suggestions

- **Fix the covariance formulation**: Either implement the attention-weighted covariance $\mathbf{C} = \sum_{k=1}^K a_k \tilde{\mathbf{g}}_k \tilde{\mathbf{g}}_k^\top$ to match the textual description, or clearly explain why the unweighted version is preferred and provide an ablation comparing both.

- **Add statistical significance tests**: Report p-values (e.g., from paired cross-validation tests) for HOMIL vs. the top-2 baselines on each metric/dataset combination.

- **Extend the ablation to TCGA-NSCLC**: The ablation findings on CAMELYON16 may not transfer directly; showing component contributions on the more complex dataset would strengthen the paper.

## Score and Decision

The paper presents a clean, well-motivated extension of MIL with second-order statistics and adaptive clustering. The experimental results are positive and the efficiency gains are notable. However, the discrepancy between the claimed attention-weighted covariance and the actual unweighted implementation is a significant concern, the improvements over the strongest baselines lack statistical significance validation, and the evaluation is limited to two datasets with ablation on only one. These issues place the paper in the borderline category—the contribution is reasonable but needs additional evidence and clarification to be fully convincing.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject