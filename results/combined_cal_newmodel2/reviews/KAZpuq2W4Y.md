Now I have all the calibration data I need. Let me compose the final review.

## Summary

This paper proposes HOMIL, a framework for Whole-Slide Image (WSI) classification that augments attention-based MIL with second-order moment (covariance) information and DBSCAN-based adaptive clustering. The key idea is to reinterpret MIL aggregation as moment estimation — first-order (attention-weighted mean) and second-order (covariance) — and to use density-based clustering to group similar patches, achieving computational efficiency while preserving diagnostic information. Experiments on CAMELYON16 and TCGA-NSCLC show competitive accuracy with substantially reduced runtime.

## Strengths

- **Clean conceptual framing (§3, §4).** The statistical reinterpretation of MIL aggregation as moment estimation (first-order = attention-weighted mean, second-order = covariance) is pedagogically effective and provides a clear intellectual throughline. This framing makes the motivation for adding second-order information intuitive and well-grounded.

- **Impressive computational efficiency gains from adaptive clustering.** On CAMELYON16, HOMIL completes 5-fold cross-validation in 310s versus 7,200s for MambaMIL and 10,800s for HMIL (Table 1). On TCGA-NSCLC, it takes 3,685s versus 25,200s and 32,400s respectively (Table 2). The DBSCAN-based clustering drives this cost-quality trade-off, which is the paper's strongest practical contribution.

- **Cleanly structured ablation study (§5.4, Table 3).** Isolating the Clustering Module and Second-Order Moment module separately, with clear per-variant metrics and runtimes, gives the reader a clear picture of each component's role. The "w/o CM" (98.14 AUC, 530s) versus "w/o SOM" (98.51 AUC, 217s) versus Full (99.23 AUC, 310s) comparison demonstrates both components' contributions.

## Weaknesses

### Major

- **No statistical significance testing for performance claims.** The abstract claims the method "significantly improves the state-of-the-art performance," but no significance tests are provided. On both datasets, HOMIL's gains over the strongest baselines fall within overlapping standard errors (e.g., CAMELYON16 AUC: 99.23±0.62 vs. S4MIL 99.02±0.87; TCGA-NSCLC ACC: 93.24±2.47 vs. HMIL 92.89±1.45; TCGA-NSCLC F1: 92.93±2.62 vs. HMIL 92.83±1.47). While HOMIL wins on all 6 metric-dataset pairs — a consistent pattern — the claim of "significant" improvement is not formally supported by the evidence presented. Given 5-fold CV, paired tests (t-test or Wilcoxon) across folds should be reported.

- **The "attention-weighted covariance matrix" claim is imprecise.** The paper states the covariance is "attention-weighted" (lines 108, 147), but the formula **C** = Σ_k (g_k − v^{(1)})(g_k − v^{(1)})^T (line 152) has attention weights only in the centering term v^{(1)} = Σ a_k g_k, not in the outer-product summation. A genuinely attention-weighted covariance would be Σ a_k (g_k − v^{(1)})(g_k − v^{(1)})^T. The centering is indeed attention-weighted (a non-trivial design choice), but the description overstates what is computed. This mismatch between description and implementation needs resolution and could affect results.

### Minor

- **Covariance vectorization design lacks justification and ablation.** The 1D convolution compression (§4.3.3) uses row-wise processing (despite the matrix being symmetric), m=64, T=4 kernels, and two successive max-pooling operations — all without rationale or sensitivity analysis. Given that second-order moments are the paper's central methodological contribution, it is unclear whether simpler alternatives (flatten+linear, diagonal-only variance, spectral methods) would work as well or better.

- **Fusion attention uses shared parameters for two statistically different representations (§4.3.4).** The parameters **W**, **w**, **b** are shared between v^{(1)} (a mean vector) and v^{(2)} (a compressed covariance vector), which have different statistical properties and likely different scales. No ablation compares shared vs. separate parameters, leaving it unclear whether this design choice is optimal or artificially constrains the fusion.

- **HMIL's AUC anomaly is not discussed.** In both Table 1 (CAMELYON16: 94.44%) and Table 2 (TCGA-NSCLC: 93.59%), HMIL's AUC is notably lower than its own ACC and F1 scores, and lower than much simpler methods like Mean Pooling (96.85% on TCGA-NSCLC). This unusual pattern may indicate an implementation issue or data skew that should be addressed, as HMIL is one of the strongest baselines in ACC/F1.

- **Background covariance formula is unnormalized (§3).** The covariance formula Σ = Σ_i (h_i − μ)(h_i − μ)^T (line 73) is the unnormalized scatter matrix, not the sample covariance (no 1/n or 1/(n−1) factor). This affects the scale of the second-order representation relative to the first-order one and the paper should be explicit about this design choice.

### Trivial

- **Minor discrepancy between Figure 1 and the text.** The figure caption describes Conv1D layers producing both v^{(1)} and v^{(2)} from instance features, while the main text (§4.3.2) specifies v^{(1)} = Σ a_k g_k (a weighted sum with no Conv1D). The figure's processing pipeline does not match the textual description.

## Nice-to-Haves

- Ablate the covariance vectorization against simpler alternatives (flatten+linear, diagonal-only variance) to justify the architectural complexity.
- Compare shared vs. separate parameters in the fusion attention.
- Report sensitivity to DBSCAN's minPts and PCA dimension d'=32 (referenced to appendix, but a brief note in the main text would help).
- Add per-class metrics or confusion matrices for clinical interpretability.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Criticism about PCA dimension for clustering (d'=32)**: The critic questions whether dimension reduction affects cluster quality, but this is a reasonable design choice with a straightforward motivation (efficiency). The paper references a sensitivity analysis in the appendix.
- **Criticism about baseline hyperparameter tuning**: The critic suggests baseline results may be suboptimal due to runtime differences (e.g., TransMIL at 48,710s on TCGA-NSCLC vs. 5,175s on CAMELYON16). While the runtime differences are large, they could reflect genuine model complexity differences across datasets. The paper states a unified codebase was used, which is a reasonable best-effort comparison.
- **Criticism about no per-class/per-slide analysis**: Scope creep for a paper focused on overall classification performance.
- **Criticism about the unnormalized covariance in §3**: This was merged into Minor (4th bullet) — the critic's point about the lack of normalization is valid and retained, but the more aggressive framing as a "significant problem" was removed.

## Novel Insights

The harsh critic's review surfaces one genuinely novel observation beyond the paper's own contributions: the discrepancy between the paper's description of the covariance as "attention-weighted" and the actual formula (where attention weights appear only in the centering, not the outer-product summation). This is a real methodological imprecision that the authors should address. The critic's observation about the significance testing gap is also important but more standard.

## Suggestions

1. **Clarify the covariance computation.** Either rename "attention-weighted covariance" to something like "covariance relative to the attention-weighted mean," or modify the formula to Σ a_k (g_k − v^{(1)})(g_k − v^{(1)})^T and re-run experiments. The current mismatch between description and implementation must be resolved.

2. **Add statistical significance testing.** Report paired t-tests or Wilcoxon signed-rank tests across folds comparing HOMIL against each baseline. If the improvements on TCGA-NSCLC are not significant, acknowledge this honestly and soften the "significantly improves" claim in the abstract.

3. **Ablate the covariance vectorization.** Compare the 1D-convolution approach against simpler alternatives: elementwise variance (diagonal-only), flatten+linear projection, or spectral methods. This would show whether the benefit comes from having *any* second-order information or from the specific architectural choices.

4. **Resolve the Figure 1 / text discrepancy.** Ensure the figure and text present the same processing pipeline.

## Score and Decision

**Calibration anchors consulted:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to this paper |
|--------|------|-----------|-------|-----------|--------------------------|
| Mamba-HMIL | 0yVP49SDg0.md | 3.25 (Reject) | 1 | Yes | Topically very similar MIL paper for WSI; rejected for lacking novelty and poor motivation. HOMIL has stronger conceptual framing and cleaner presentation — scores higher. |
| Pg-GAT | MOCEoNsjEx.md | 3.00 (Reject) | 1 | Yes | GNN-based WSI MIL; rejected for insufficient novelty. HOMIL's moment-estimation framing is more novel — scores higher. |
| Covariance Pooling | q1t0Lmvhty.md | 6.00 (Accept) | 1 | Yes | Theoretical paper on second-order statistics in DNNs. Different genre — indirect comparison. |
| MFC-MIL (Causal) | 6xrDPHhwD3.md | 6.00 (Accept) | 1,2 | Yes | MIL+WSI paper on same datasets; accepted despite significant method-description weaknesses. HOMIL's method is cleaner but its performance claims are weaker (overlapping error bars). |
| VLSA (Vision-Lang) | trj2Jq8riA.md | 5.67 (Accept) | 2 | Yes | Computational pathology MIL paper accepted at borderline. Similar weakness profile (marginal gains, missing significance tests, unjustified design choices). HOMIL has stronger strengths (higher favorability) but similar weakness severity. |

**Bracket reasoning (Round 1):** The paper is clearly stronger than the reject-level WSI MIL papers (3.0–3.25) due to its novel conceptual framing and practical efficiency gains. It is comparable to mid-level accepts (5.67–6.0) but slightly weaker in empirical support for its core claim. Initial bracket: 4.5–6.0.

**Narrowing (Round 2):** Comparing item-level favorability with VLSA (5.67, Accept): HOMIL's strengths have higher favorability (11–14 vs. 7–13) but its weakest weakness (0.03 for significance testing) is lower than VLSA's worst (-1.32). The covariance imprecision (4.60 favorability) is a drag that VLSA does not have. On balance, HOMIL sits slightly below VLSA. Final score: **5.0**.

**Score justification:** The paper has genuine contributions — a well-motivated conceptual framing of MIL as moment estimation, and practically valuable efficiency gains from adaptive clustering. However, the core empirical claim (that second-order moments improve performance) is not supported by significance testing — all gains fall within overlapping standard errors. Additionally, a central method description ("attention-weighted covariance") is imprecise relative to the actual formula. These issues prevent the paper from reaching accept-level confidence but are not fatal; they are addressable with clarifications and additional analysis.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>