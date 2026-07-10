## Summary

The paper proposes HOMIL, a MIL framework for WSI classification that extends ABMIL by adding second-order (covariance) statistics alongside the standard first-order (attention-weighted mean) aggregation, and improves efficiency via DBSCAN-based adaptive clustering. The method is evaluated on two WSI benchmarks (CAMELYON16, TCGA-NSCLC) against nine baselines.

## Strengths

- **Clean statistical framing.** The paper observes that ABMIL's attention-weighted sum is equivalent to a first-order moment estimate (§3.1), and argues that covariance (second-order moment) captures complementary feature variability and inter-feature relationships that a mean vector discards. This framing is pedagogically useful and clearly motivates the method.

- **DBSCAN-based adaptive clustering delivers genuine efficiency gains.** The compression ratios (0.18 on CAMELYON16, 0.16 on TCGA-NSCLC, line 254) and runtime comparison (310s vs. 7200s for MambaMIL and 10800s for HMIL on CAMELYON16) demonstrate meaningful computational benefits. This is arguably the paper's strongest and most clearly supported contribution.

- **Consistent top-line point estimates across both datasets.** In Tables 1 and 2, HOMIL achieves the highest point estimates on all three metrics (ACC, AUC, F1). The ablation study (Table 3) confirms that both the clustering module and the second-order moment module contribute positively relative to the ABMIL baseline.

## Weaknesses

### Major

- **No statistical significance testing to support the central accuracy claim.** The abstract states HOMIL "significantly improves the state-of-the-art performance" (line 9), but no statistical test (paired t-test, Wilcoxon, or confidence interval analysis) is reported. With only 5-fold cross-validation, the reported standard errors produce overlapping confidence intervals between HOMIL and several baselines. For instance, on CAMELYON16, HOMIL ACC=96.98±2.43% vs. ABMIL ACC=94.72±2.18% — with 5 folds, these CIs overlap substantially. The paper's strongest claims about accuracy improvement are therefore not supported by the evidence as presented.

- **HMIL baseline on CAMELYON16 shows an anomalous ACC/AUC relationship.** On CAMELYON16 (Table 1), HMIL achieves ACC=96.19% but AUC=94.44% — ACC exceeding AUC by ~1.75 points for binary classification is unusual and suggests an incorrect decision threshold, different class imbalance handling, or an implementation issue. Since the authors state all methods use "a unified codebase" (line 200), this raises questions about the fairness of the HMIL comparison. This matters because on TCGA-NSCLC HOMIL's margin over HMIL is only ~0.3-0.4% in ACC and F1.

### Minor

- **The covariance vectorization via 1D convolution (§4.3.3) is presented without justification or ablation of its design choices.** The parameters m=64 and T=4 (line 238) are stated but never ablated or compared against simpler alternatives (e.g., taking the diagonal, eigenvalues, or row-wise mean of the covariance matrix). This component contributes ~1% ACC improvement (Table 3, w/o SOM vs. full model), yet its design is opaque and appears arbitrary.

- **The covariance-like matrix C = Σ g̃_k g̃_k^T (line 152) lacks the standard 1/(K-1) normalization factor**, meaning its entries scale linearly with the number of clusters K. Since K varies across slides depending on DBSCAN parameters and tissue content, this introduces a confound that makes the second-order representation harder to interpret, even if the model can learn to compensate via learned fusion weights.

- **The DBSCAN modification for non-core points is non-standard and under-specified.** The paper states "non-core points form single-element clusters" (line 122-123), meaning every noise point becomes a singleton cluster. It does not specify whether standard DBSCAN's border/noise distinction is preserved, and the potential impact on the claimed "adaptive granularity" for rare pathological regions is not discussed.

### Trivial

None.

## Nice-to-Haves

- Show qualitative evidence of what the covariance captures (e.g., which covariance entries are most discriminative, correlations with interpretable tissue properties).
- Diagnose the HMIL ACC/AUC anomaly on CAMELYON16 more precisely (is it a threshold issue, an implementation artifact, or valid behavior?).
- Provide an ablation on the covariance vectorization hyperparameters (m, T) and compare against simpler alternatives.

## Removed Points

- The critic's claim that HMIL's TCGA-NSCLC results (ACC=92.89%, AUC=93.59%) are also anomalous is factually incorrect — AUC > ACC here is normal behavior. Removed as factually wrong.
- The critic's speculation that the unified codebase might have bugs specifically affecting HMIL is unfounded. The ACC/AUC anomaly is real and worth noting; the cause is unknown.
- The critic's section-by-section notes about the figure caption vs. text describing Conv1D differently is a parser artifact / minor caption inconsistency — removed as a formatting-level issue.
- The critic's criticism that the fusion attention over two vectors is "over-engineered" is a trivial design preference, not a weakness — removed.
- The critic's comment about missing appendix/sensitivity analysis being deferred to appendix — removed per hard rule about appendix references.

## Novel Insights

None beyond the paper's own contributions. The observation that fusion weights show the model relying more on first-order than second-order information is already presented by the authors in Figure 2(b) and §5.5.

## Suggestions

1. **Add paired statistical significance testing** (e.g., paired t-test across folds, or report effect sizes with CIs) comparing HOMIL against each baseline. This is the single most impactful improvement.
2. **Diagnose the HMIL ACC/AUC anomaly** on CAMELYON16, or replace that baseline with a correctly configured version.
3. **Ablate the covariance vectorization** — vary m and T, and compare against simpler alternatives (diagonal, eigenvalues, flattened+linear layer).
4. **Clarify the DBSCAN noise-point handling** and discuss whether the unnormalized covariance sum is intentional.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>