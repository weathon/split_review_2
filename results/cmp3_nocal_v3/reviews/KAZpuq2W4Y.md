## Summary

This paper proposes HOMIL, a multi-instance learning framework for whole-slide image classification that augments the standard attention-weighted first-order (mean-based) aggregation with second-order statistics (a covariance matrix computed on DBSCAN-clustered patch features), plus a Conv1D-based vectorization to fuse both representations. The core motivation—that first-order moments discard inter-feature variability—is clearly articulated, and the use of adaptive clustering (DBSCAN) to reduce computational cost while preserving diagnostic information is practically appealing.

## Strengths

- **Well-motivated and clearly framed core idea.** The paper identifies a genuine limitation of first-order-only MIL aggregation (loss of variability and inter-feature relationships across patches) and connects it naturally to statistical moments (Section 3.2). The connection between ABMIL and first-order moments (Section 3.1) provides a clean conceptual framing.

- **Credible computational efficiency advantage.** On CAMELYON16, HOMIL (310s across 5 folds) is faster than ABMIL (455s) and dramatically faster than transformer/state-space baselines (MambaMIL: 7200s, HMIL: 10800s), while achieving the best reported metrics. On TCGA-NSCLC the trend holds (3685s vs ABMIL's 4056s, vs MambaMIL's 25200s). Table 3 confirms the clustering module drives this efficiency gain.

- **Ablation study provides internal validation.** Table 3 systematically removes the clustering module (CM) and second-order moment module (SOM), showing that both components contribute positively and that removing both (→ ABMIL) yields the lowest performance. This gives some evidence that the design choices are functional.

## Weaknesses

### Fatal

None.

### Major

- **Imprecise and potentially misleading mathematical terminology.** The paper repeatedly calls the second-order statistic an "attention-weighted covariance matrix" (lines 108, 147). However, the formula given on line 152 is $\mathbf{C} = \sum_{k=1}^K \tilde{\mathbf{g}}_k \tilde{\mathbf{g}}_k^\top$ (where $\tilde{\mathbf{g}}_k = \mathbf{g}_k - \mathbf{v}^{(1)}$), which contains **no attention weights** in the outer-product sum—the attention weights $a_k$ are only used to produce the centering vector $\mathbf{v}^{(1)}$. This is an **attention-centered** scatter matrix, not an attention-**weighted** covariance. A careful reader implementing from the formula would get a different operation from what the text claims. Additionally, the abstract (line 9) states the method "compute[s] the covariance matrix of the patch representation vectors across the entire slide," but the actual method computes it on *cluster* representations, not raw patches. While none of these imprecisions invalidate the method, they erode confidence in whether the paper accurately describes what it implements.

- **Statistical significance of the claimed improvements is not established.** The paper reports standard error (SE = SD/√5) across 5 folds. On nearly every comparison with the strongest baselines, the SE ranges overlap substantially:
  - CAMELYON16 ACC: HOMIL **96.98±2.43** vs MambaMIL **96.48±1.37** — ranges [94.55, 99.41] vs [95.11, 97.85].
  - CAMELYON16 AUC: HOMIL **99.23±0.62** vs S4MIL **99.02±0.87** — ranges [98.61, 99.85] vs [98.15, 99.89].
  - TCGA-NSCLC ACC: HOMIL **93.24±2.47** vs HMIL **92.89±1.45** — ranges [90.77, 95.71] vs [91.44, 94.34].
  - TCGA-NSCLC AUC: HOMIL **97.41±1.24** vs MambaMIL **96.68±0.97** — ranges [96.17, 98.65] vs [95.71, 97.65].

  No statistical significance tests (paired t-test, Wilcoxon, or McNemar) are reported, and with only 5 folds and overlapping error bars, the paper's claim of "state-of-the-art" performance improvements cannot be distinguished from noise. The paper should either provide significance evidence or temper its claims and reframe the contribution around the demonstrated efficiency-accuracy tradeoff.

### Minor

- **Figure 1 caption is inconsistent with the method text.** The caption describes $\mathbf{v}^{(1)}$ and $\mathbf{v}^{(2)}$ as having dimensions $n \times d$ (per-instance features produced by Conv1D layers). In the method text, however, $\mathbf{v}^{(1)}$ (line 141) is a single $d$-dimensional vector produced by an attention-weighted sum of cluster features, and $\mathbf{v}^{(2)}$ (line 168) is a $d$-dimensional vector from the covariance vectorization. The caption describes a different pipeline from the text; this needs reconciliation.

- **The ablation reveals an undiscussed failure case.** Table 3 shows that the "w/o CM" variant (second-order moments on all patches, no clustering) achieves AUC **98.14**, which is *lower* than plain ABMIL's **98.88**. This means that adding second-order moments to raw patch-level features actively hurts performance, and the second-order moment only helps when combined with clustering. The paper does not discuss this interaction, which raises questions about whether the benefit comes from the statistical moment itself or from the specific interaction with clustering.

- **Conv1D covariance vectorization is an ad-hoc design choice with no justification or ablation.** The paper compresses the $d\times d$ matrix to a $d$-dimensional vector via a two-stage Conv1D + double max-pooling scheme (Section 4.3.3, Step 3). No rationale is given for why this specific architecture (kernel width $m=64$, $T=4$ kernels, double max-pooling) was chosen, nor is it ablated against simpler alternatives (e.g., flatten+linear, diagonal-only, eigenvalue decomposition). Without this analysis, it is unclear whether the vectorization preserves meaningful covariance structure or is merely a dimension-matching trick.

- **PCA fitting procedure is underspecified.** The paper reduces patches to $d'=32$ via PCA (Section 4.1, Step 2) but does not state whether PCA is fit on the training set of each fold independently or on all slides globally. A global fit would leak information across folds and compromise the 5-fold cross-validation. This needs clarification.

- **DBSCAN modification from standard practice is unstated.** Line 122 says "non-core points form single-element clusters," which differs from standard DBSCAN (which labels non-core, non-reachable points as *noise*). The paper does not explain how this modification is implemented or how noise points are handled (assigned to nearest cluster? forced as singletons?). This affects the total number of clusters $K$ and thus the scale of $\mathbf{C}$.

- **"Scatter matrix" vs "covariance."** Both formulas (lines 73, 152) are unnormalized sums of outer products (scatter matrices), not proper covariance matrices (which divide by $n$ or $n-1$). Since $K$ varies across slides (compression ratios 0.18 and 0.16), the scale of $\mathbf{C}$ is slide-dependent purely due to counting. While the learnable Conv1D kernels may adapt, the paper does not acknowledge or justify this choice.

### Trivial

None.

## Nice-to-Haves

- **Evaluation on additional datasets, particularly multi-class ones.** The paper only evaluates on two binary classification tasks (metastasis detection, lung cancer subtyping). Many WSI MIL papers include datasets like TCGA-BRCA (multi-class) or CRC (colorectal). Adding at least one multi-class or additional binary dataset would strengthen generalizability claims.

- **Ablation of the Conv1D vectorization** against simpler baselines (flatten + linear projection, diagonal-only, eigenvalue features) to verify that the complex scheme preserves meaningful covariance structure.

- **Report the standard deviation (SD) in addition to SE** for a clearer picture of fold-to-fold variance.

## Removed Points

The following points raised in the input review were removed:

- **"ABMIL becomes a special case" claim is overstated (Section-by-Section note):** The reviewer argued the parameterization differs. However, when $K=n$ and each cluster is a singleton, HOMIL's first-order aggregation ($a_k = \text{softmax}(\mathbf{w}_a^\top \tanh(\mathbf{W}_a \mathbf{g}_k + \mathbf{b}_a))$) and ABMIL's attention ($a_i = \exp(\mathbf{w}^\top \tanh(\mathbf{Vh}_i))/\sum\cdots$) are functionally the same class (single-layer attention network). The extra bias term is a minor difference. This is an overly strict reading; the claim is reasonable.

- **HMIL baseline has unusually large SE and low AUC relative to ACC (Section-by-Section note):** While this observation is factually correct (HMIL on CAMELYON16: ACC 96.19±4.18, AUC 94.44±1.89), it is a property of the baseline's behavior, not a weakness of the paper's method. The paper is not responsible for explaining anomalies in other methods.

- **"Surpasses S4MIL in AUC (99.02%)" overclaim (Section-by-Section note):** This is a minor phrasing issue subsumed by the broader statistical significance weakness above. It is redundant when the main significance concern is stated.

- **Baseline hyperparameter tuning not specified:** The paper states a unified codebase and reports settings for HOMIL. Whether baselines used the same settings or were individually tuned is a reasonable question, but the unified codebase practice is standard, and this is a relatively minor detail.

## Novel Insights

None beyond the paper's own contributions. The main insight—that second-order statistics on clustered patch representations can improve MIL for WSIs while maintaining computational efficiency via adaptive clustering—is the paper's own contribution. The reviews do not surface any novel perspectives beyond what the paper already presents.

## Suggestions

1. **Clarify the mathematical terminology.** Either add the attention weights $a_k$ to the covariance sum (making it truly attention-weighted) and re-run experiments, or replace "attention-weighted covariance matrix" with "covariance of attention-centered features" or similar precise language throughout. Normalize by $K$ or $K-1$ to get a proper covariance, or justify why the unnormalized form is preferable.

2. **Report statistical significance.** Apply a paired test (e.g., Wilcoxon signed-rank or paired t-test across folds) to compare HOMIL against the top 2-3 baselines, or use bootstrapping. If the improvements are not statistically significant, acknowledge this and reframe the contribution around the efficiency-accuracy balance rather than claiming state-of-the-art.

3. **Reconcile the Figure 1 caption with the method text.** Clarify the dimensions and processing steps for $\mathbf{v}^{(1)}$ and $\mathbf{v}^{(2)}$.

4. **Discuss the "w/o CM" ablation finding.** Explain why second-order moments on raw patches hurt performance relative to ABMIL, and why clustering resolves this.

5. **Ablate or justify the Conv1D vectorization** against simpler alternatives to demonstrate its necessity.

## Score and Decision

**Score:** 6 — The paper's core idea (second-order moments + adaptive clustering for MIL) is well-motivated and the efficiency advantages are clearly demonstrated. However, the imprecise mathematical description ("attention-weighted covariance matrix" that isn't actually attention-weighted, "covariance matrix" that is a scatter matrix) and the lack of established statistical significance for the claimed performance gains prevent a higher score. These issues are addressable in revision and do not invalidate the method, but they meaningfully weaken the paper in its current form.

**Decision:** Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>