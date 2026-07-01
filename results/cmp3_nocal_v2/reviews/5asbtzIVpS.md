Now I have all the verification needed. Let me write the final consolidated review.

## Summary

This paper introduces Forest-Based Graph Learning (FGL), a new paradigm for semi-supervised node classification that reinterprets message passing as transportation over spanning trees. The core insight is that a spanning tree is the minimal subgraph achieving global connectivity, and a forest (set of trees) can capture complementary topological pathways. The method comprises: (1) a pre-processing step that augments the graph with k-NN edges from pseudo-labels; (2) a homophily-guided tree sampler with theoretical guarantees (Theorem 2); (3) a general linear-time tree aggregator (Theorem 1); and (4) a tree fuser. Empirical results across 9 benchmarks with 26 baselines show FGL achieves an average rank of 1.22, with notable gains on heterophilous datasets, while maintaining strong efficiency.

## Strengths

1. **Well-motivated structural insight.** The paper's observation—that spanning trees are the minimal subgraphs achieving global connectivity—provides a clean conceptual framework for analyzing the cost/coverage trade-off in graph learning. The formalization in Eq. 1 (Total cost = cost per structure × number of structures) identifies a real design tension and directly motivates the choice of tree as an intermediate structure. (Section 1, Eq. 1, Figure 1)

2. **Non-trivial theoretical result.** Theorem 2 establishes a monotonic relationship between the edge-score ratio Δ = p/q and the expected homophily of sampled trees, with an asymptotically tight upper bound determined by the graph's homophilous connected components. This goes beyond hand-waving to provide formal justification for why refining the homophily estimator provably improves the tree distribution. (Section 4.6)

3. **Strong empirical results.** In Table 1, FGL achieves the best accuracy on 7 of 9 datasets and is runner-up on the other 2, with an average rank of 1.22 (next best is SGFormer at 7.22). The gains on heterophilous datasets are substantial (e.g., Texas: +13 pts over SGFormer). (Table 1)

4. **Genuine efficiency advantage.** The method achieves practical linear complexity. Table 2 shows FGL is the fastest among all methods with competitive performance (0.005 sec/epoch on Cora, 0.246 on ArXiv), with measured runtime backing the complexity claims. (Table 2, Section 4.5)

5. **General tree aggregator framework.** Theorem 1 and the associated recursions (Eqs. 4-6) provide a principled way to adapt any message aggregator satisfying Combine/Disentangle properties to operate on a tree in linear time. The framework itself is a useful conceptual contribution beyond the particular instantiation tested. (Section 4.3)

## Weaknesses

### Fatal
None.

### Major

1. **Pre-processing contribution is not isolated from the forest paradigm contribution.** The ablation study (Table 3) removes the Global Submodule (tree aggregation) but retains the pre-processed/k-NN augmented graph. On several heterophilous datasets, this "w.o. Global Submodule" variant already exceeds all baselines (e.g., Texas: 82.88 vs. best baseline SGFormer 78.92; Wisconsin: 83.92 vs. SGFormer 80.00). The paper never runs an ablation that applies the full method (tree sampler + aggregator + fuser) on the *original un-augmented* graph. This makes it impossible to determine how much of the headline performance advantage relative to baselines comes from the forest-based paradigm versus from the engineered graph augmentation. The paper's central claim—that the forest-based paradigm breaks the cost/coverage trade-off—is partially confounded with the pre-processing step. (Table 3, Section 4.1)

   *This is an addressable weakness: the authors could run the missing ablation or reframe the contribution to transparently acknowledge the pre-processing as a critical pipeline component rather than a technicality.*

### Minor

2. **Standard deviations relegated to appendix for small high-variance datasets.** The paper reports only means in the main Table 1, with standard deviations in Appendix Table 10. On the smallest datasets (Texas, Cornell, Wisconsin: n ≈ 183–251), the headline improvements are very large (e.g., Texas: +13 pts), but the main paper provides no way to assess whether these gaps are statistically robust. Given that these are the datasets where the most striking claims are made, the main table should include standard deviations or effect-size indicators. (Table 1, line 240)

3. **Generality of the tree aggregator is claimed but untested beyond one instantiation.** Section 4.3 asserts that "many popular auto-regressive sequence models and first-order GNN aggregators can be adopted" (listing linear attention, linear RNNs, SSMs). However, only a single weighted-sum instantiation is tested. This over-claims relative to the evidence. The paper would benefit from either testing one additional aggregator or toning down the generality claim. (Section 4.3, lines 110–114, 130)

4. **Theory-practice gap in the homophily estimator analysis.** Theorem 2 analyzes a setting where edges have binary scores (p for homophilous, q for heterophilous). In the actual method, the homophily estimator produces continuous attention scores via Eq. 3. The paper does not establish that Theorem 2 extends to continuous scores, nor does it characterize the mapping from attention weights to the p/q parameterization. The empirical correlation in Figure 5 provides some support, but the theoretical framing in the abstract is stronger than what Theorem 2 formally proves. (Section 4.6 vs. Section 4.2, Eq. 3)

5. **Heterophily mechanism not fully explained.** The paper shows dramatically larger gains on heterophilous graphs than homophilous ones (Cora: +0.12 pts; Texas: +12.97 pts), but does not provide a mechanistic explanation for this asymmetry. The intuitive story that "spanning trees enable long-range propagation" applies equally to both regimes. The paper mentions that pre-processing increases homophily ratio, which helps heterophilous graphs more, but a deeper analysis of *why* the tree-based aggregation specifically amplifies gains on heterophilous graphs would strengthen the narrative. (Table 1 vs. Table 3, Section 4.1)

### Trivial

6. **Undefined variable K in complexity analysis.** The complexity expression O((n + m)Kd) (Section 4.5, line 160) uses K without definition. From context it appears to relate to N_T or a parallelism constant, but this should be explicit.

## Nice-to-Haves

- **Isolate the pre-processing contribution.** Run the full FGL pipeline on the original (non-augmented) graph, with connectivity minimally ensured (e.g., a virtual node). If the paradigm is doing the work, performance should remain strong. Either outcome is informative.
- **Provide statistical significance measures** (p-values or confidence intervals) for the comparisons against the best baselines on the small heterophilous datasets.
- **State the k value for k-NN augmentation and whether it is tuned per dataset** in the main paper, as this is a key hyperparameter.

## Removed Points

The following points from the input review are excluded with justification:

- **Wilson's algorithm complexity concern ("nearly O(n)" claim):** The paper acknowledges "nearly O(n) time per-tree." Wilson's algorithm complexity depends on the graph, and the paper's phrasing ("nearly") is appropriately qualified. This is a minor technical quibble that does not substantively affect the paper.
- **"Missing limitations section":** While a limitations discussion would strengthen any paper, its absence is a standard presentation choice, not a weakness specific to evaluating this paper's claims.
- **"Missing related works about tree-based methods":** Per policy, I cannot verify or flag missing related work without external sources.
- **"Pre-processing details missing from main text" (k value):** Accepted partially (moved to Nice-to-Haves as a suggestion). But the critic's framing as a critical omission overstates the issue; this detail is likely in the appendix (Section K) per the paper's statement, and the method is clearly described at a high level.
- **"Theoretical analysis in abstract oversells":** This is folded into Weakness #4 above at the Minor level, not treated as a separate point.
- **The critic's claim that "w.o. Global Submodule" on Wisconsin is "above all baselines except SGFormer":** This contains a factual error—the variant at 83.92 actually *exceeds* SGFormer (80.00). The overall point (that the variant outperforms baselines) is correct and retained in Weakness #1; the erroneous detail is excised.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a significant methodological question about the entanglement of the pre-processing step with the core paradigm, but this is a critique of the evidence, not a novel insight about the approach itself.

## Suggestions

1. **Conduct and report the missing ablation** (full FGL on the original, non-augmented graph) to cleanly separate the contribution of the forest-based paradigm from the contribution of the k-NN graph augmentation. This is the single most impactful fix.
2. **Move standard deviations to the main results table**, or at minimum annotate the key comparisons on small heterophilous datasets with effect-size or significance information.
3. **Add a brief mechanistic discussion** explaining why heterophilous graphs benefit disproportionately from the tree-based paradigm, beyond the pre-processing effect.

## Score and Decision

The paper introduces a genuinely novel paradigm with solid theoretical backing and impressive empirical results. The main weakness—the confounded pre-processing contribution—is significant but addressable: the tree aggregation component demonstrably adds value on top of pre-processing (e.g., +9 pts on Texas), and the homophily-guided sampling consistently outperforms uniform sampling. The paper would substantially benefit from a cleaner ablation design, but the core contributions (forest-based paradigm, general tree aggregator, theoretical analysis) are real and well-supported.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>