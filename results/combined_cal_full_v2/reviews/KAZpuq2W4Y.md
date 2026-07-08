Now I have all the information needed to produce the final consolidated review.

## Summary

This paper proposes HOMIL (Higher-Order Multi-Instance Learning), a framework for whole-slide image (WSI) classification that extends standard attention-based MIL (ABMIL) by adding second-order statistical information (a covariance-like matrix of patch/cluster features) to the usual first-order (attention-weighted mean) representation, and uses DBSCAN clustering to reduce computational cost by adaptively grouping similar patches. Experiments on CAMELYON16 and TCGA-NSCLC show HOMIL achieves the best point estimates across ACC, AUC, and F1 while being computationally efficient.

## Strengths

- **Clear statistical framing of the problem (Sections 3.1–3.2).** The paper clearly motivates why attention-weighted averaging in MIL corresponds to a first-order moment and why this discards variability and inter-feature correlation information. This provides a clean conceptual hook for adding second-order information.

- **DBSCAN as an adaptive clustering method is well-motivated for WSIs (Section 4.2).** The observation that DBSCAN naturally produces large clusters for homogeneous normal tissue and small clusters for sparse, heterogeneous pathological regions aligns with known WSI structure. Compression ratios of 0.18–0.16 are substantial, and runtime comparisons show HOMIL is competitive with or faster than several baselines.

- **Clean ablation study separating the two proposed components (Table 3).** The ablation isolates the contributions of the Clustering Module (CM) and the Second-Order Moment module (SOM), showing each individually improves over ABMIL and the full model performs best. This level of ablation is appropriate.

## Weaknesses

### Major

- **The "covariance matrix" is an unnormalized scatter matrix, not a covariance matrix, and this undermines the paper's central statistical framing.** The paper's method (Section 4.3.3, line 152) defines $\mathbf{C} = \sum_{k=1}^K \tilde{\mathbf{g}}_k \tilde{\mathbf{g}}_k^\top$, and the background (Section 3.2, line 73) similarly defines $\Sigma = \sum_{i=1}^n (\mathbf{h}_i - \mu)(\mathbf{h}_i - \mu)^\top$. Neither includes the standard $1/n$ or $1/(K-1)$ normalization factor that defines a covariance matrix versus an unnormalized scatter matrix. Because $\mathbf{C}$ is a sum over $K$ clusters — and $K$ varies across slides since DBSCAN produces different numbers of clusters per slide — the magnitude of $\mathbf{C}$ scales with cluster count, conflating feature structure with cluster count. The paper repeatedly calls this "the covariance matrix" (abstract, lines 19, 71, 75, 77, 108, 147, 150, 154, 260, 291) and frames adding second-order moments as its core contribution, but the math does not match the statistical framing. (The method may still work in practice — the downstream Conv1D + learned fusion could adapt to the scale — but the paper's central claimed contribution is imprecisely specified.)

- **No statistical significance testing for claimed improvements.** The paper reports results as mean ± standard error over 5-fold cross-validation and claims HOMIL "significantly improves" performance (abstract). However, with SE = SD/√5, the reported SEs imply large standard deviations relative to the observed improvements. For example, on CAMELYON16 ACC: HOMIL 96.98 ± 2.43 (SE) vs. ABMIL 94.72 ± 2.18 (SE) — a 2.26% difference that is well within one pooled SE (~3.26%). On TCGA-NSCLC the same pattern holds. No confidence intervals, bootstrap tests, or paired significance tests are provided. The point estimates favor HOMIL, but the evidence is insufficient to support claims of statistical significance. The paper should either provide rigorous significance testing or temper its claims.

### Minor

- **The Conv1D-based covariance vectorization lacks justification (Section 4.3.3).** The compression from a $d \times d$ matrix to a $d$-dimensional vector uses 1D convolution with $T=4$ kernels of size $m=64$, followed by two successive max-pooling operations. The paper provides no rationale for why this specific scheme is appropriate for covariance structure, why $m=64$ and $T=4$, or what property of the covariance matrix is preserved. This contrasts with the paper's framing as a principled statistical generalization of MIL.

- **The HMIL baseline shows anomalously low AUC.** On TCGA-NSCLC, HMIL achieves AUC 93.59% — substantially lower than mean pooling (96.85%), max pooling (96.97%), and ABMIL (96.58%). On CAMELYON16, HMIL's AUC (94.44%) is also the lowest among all methods. Since all baselines are "implemented in a unified codebase" (line 200), this raises a concern about faithful implementation of the HMIL baseline, which could affect the fairness of comparisons.

- **PCA fitting protocol in cross-validation is unspecified (line 101).** The paper does not state whether PCA dimensionality reduction is fit within each cross-validation fold or globally on the full dataset. If PCA is fit on all data before splitting, information leaks across folds.

- **Notation inconsistency in the convolution equation (line 162).** The equation uses $k_{i,j}$ which appears to index a different kernel per row $i$ of the covariance matrix, but the text describes "a set of $m$-dimensional kernels $\{\mathbf{k}_t\}_{t=1}^T$" ($T=4$). The inconsistency between the equation and text hurts reproducibility.

### Trivial

None.

## Nice-to-Haves

- Normalize the covariance-like matrix by $K$ (or $K-1$) to make it a true covariance matrix, or at minimum discuss why the unnormalized form is used and how the downstream network handles the varying scale.
- Add paired statistical tests (e.g., Wilcoxon signed-rank across folds, bootstrapped confidence intervals) or tone down claims of "significant improvement."
- Clarify the PCA fitting protocol in cross-validation.
- Provide rationale or an ablation for the Conv1D kernel size ($m=64$) and number of kernels ($T=4$).
- Resolve the notation inconsistency in the convolution equation and clarify whether kernels are shared across rows.
- Improve the figure caption for Figure 1 to match the method text.

## Removed Points

These points from the input review were removed with justification:

- **Figure 1 inconsistency as a "critical issue":** The harsh critic claimed the figure caption describes a Conv1D pipeline on instance features that conflicts with the method text. While the caption is somewhat ambiguous, the figure also mentions cluster feature aggregation and the overall pipeline is described at a high level. The caption could be clearer, but this is a presentation issue, not a "critical" implementation inconsistency. Demoted to the Nice-to-Haves section.

- **Loss curve flatness as a weakness:** The observation that training/validation loss remains flat for 30 epochs before dropping is noted but the paper discusses the convergence behavior in Section 5.5, and this is not a method flaw.

- **Questions about hyperparameter tuning protocol:** These are generic concerns applicable to most deep learning papers and not specific enough to be a distinct weakness.

- **Formatting/style nitpicks and speculation about missing appendix content:** Removed per instructions.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Fix the covariance computation.** Include proper normalization or justify why the unnormalized form is used and discuss the handling of varying $K$.
- **Strengthen the experimental evidence.** With 5-fold CV, report standard deviations (not just standard errors) and run a paired bootstrap or Wilcoxon signed-rank test to validate whether improvements are statistically detectable.
- **Clarify the PCA protocol.** State explicitly whether PCA is fit per-fold or globally.
- **Simplify or justify the covariance vectorization.** The current Conv1D + double max-pooling scheme needs justification — or could be replaced with a simpler approach.
- **Investigate HMIL baseline implementation.** The anomalously low AUC suggests the unified codebase implementation may not be faithful.

## Calibration Report

### Anchors Retrieved

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| Mamba-HMIL (0yVP49SDg0) | 3.25 | Bracket | Yes | Similar WSI MIL domain; Mamba-HMIL had more severe reviewer criticism (lack of novelty, poor motivation) and more extreme negative item weights (down to -5.09). HOMIL is stronger due to clearer motivation and cleaner ablation. |
| Covariance Pooling Riemannian (q1t0Lmvhty) | 6.00 | Bracket | Yes | Covariance-theory paper accepted with all 6s. Much stronger theoretical contribution and rigorous evaluation. HOMIL is substantially weaker on theoretical precision and empirical rigor. |
| Causal MIL (6xrDPHhwD3) | 6.00 | Bracket | Yes | WSI MIL paper with mixed reviews (5,8,3,8); accepted. Had similar evaluation setup (CAMELYON16 + TCGA-NSCLC). HOMIL lacks the extensive justification and causal framing of this paper. |
| SMIL (lo9HMoGNwQ) | 4.50 | Narrow | Yes | Sequential MIL paper, rejected (5,5,5,3). Comparable quality: clear motivation but limited novelty/evidence. HOMIL has better-motivated architecture but similar evidential gaps. |
| PointMIL (T7ZVzuObcj) | 5.50 | Narrow | Yes | MIL for point clouds, rejected. Had similar pattern of clear motivation but limited methodological depth. HOMIL's weaknesses (covariance normalization, significance testing) are more central to its claims. |
| Dual-Metric (i4ouG6Kc8M) | 2.50 | Bracket | No | Histopathology SSL paper; substantially weaker evaluation. |
| Masked Mamba (V9UsZBbTvZ) | 3.00 | Bracket | No | Histopathology SSL paper; lower quality. |
| Annotation by Clicks (6NO5UVWvo6) | 4.50 | Narrow | No | Medical segmentation; not directly comparable. |
| Unitention (HBFzStNrS9) | 5.25 | Narrow | No | General classification; not directly comparable. |

### Score Placement

The bracket search placed HOMIL between anchors scoring 3.25 (Mamba-HMIL) and 6.00 (Causal MIL, Covariance Pooling). The narrow search refined to 4.50–5.50. Comparing **weighted-item profiles**:

- HOMIL shares the **strong motivation and clean ablation** pattern with SMIL (4.50) — both have high-weighted strengths (8.88–9.80 vs SMIL's 9.32, 8.28) — but HOMIL's weaknesses have more negative weights (0.06 for significance, 1.97 for covariance) than SMIL's weakest items (-4.34, -2.14). However, HOMIL is **stronger than Mamba-HMIL (3.25)**, which had extreme negative weights (-5.09, -4.04, -3.92) that HOMIL lacks.

- The covariance normalization issue (weight 1.97) and the significance gap (weight 0.06) are the primary drags. These are both **fixable but central** — the first undermines the claimed statistical rigor of the core contribution, and the second leaves the empirical support unsubstantiated.

The final score of **4.5** places HOMIL in the borderline-reject zone: the core idea has clear merit and is well-motivated, but the paper in its current form has two major weaknesses that prevent acceptance. The covariance normalization is a mathematical imprecision in the central contribution, and the lack of significance testing means the claimed improvements are not empirically validated.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>