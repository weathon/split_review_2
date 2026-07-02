## Summary

This paper proposes Forest-based Graph Learning (FGL), a new paradigm for semi-supervised node classification that models message propagation as transportation over spanning trees. The key insight is that a spanning tree is the minimal subgraph connecting all nodes, thus achieving global coverage with low per-structure cost, breaking the inherent trade-off between cost-effectiveness and global receptive field. The framework includes: (1) a pre-processing step that augments the graph to ensure connectivity and increase homophily; (2) a tree sampler that uses a learned edge-homophily estimator to bias sampling toward homophilous spanning trees; (3) a general tree aggregator that performs quadratic node-pair interactions in linear time; and (4) a tree fuser that integrates multiple trees. Theoretical analysis establishes an asymptotic relationship between the accuracy of the edge-homophily estimator and the quality of the induced tree distribution. Experiments on nine benchmark datasets show competitive or state-of-the-art performance while maintaining higher efficiency than many baselines.

## Strengths

- **Novel and principled paradigm**: The idea of using spanning trees as the structural primitive for long-range propagation is elegant. The paper provides a clear analysis of the cost-coverage trade-off (Eq. 1) and identifies trees as a natural compromise between local and global structures.
- **Rigorous theoretical foundation**: Theorem 2 establishes monotonicity, upper bound, and asymptotic tightness linking the edge-score ratio to the expected homophily ratio of sampled trees, directly justifying the homophily-guided sampling strategy.
- **Efficient and general tree aggregator**: The derivation of a general tree aggregator based on combine/disentangle properties (Theorem 1) is novel. The resulting linear-time implementation with potential parallelization across trees is a significant engineering contribution.
- **Comprehensive and convincing experiments**: The paper evaluates on 9 datasets covering both homophilous and heterophilous graphs, compares against 26 baselines spanning classic GNNs, deep GNNs, Graph Transformers, and Mamba, and reports both performance and wall-clock efficiency. Ablation studies clearly isolate the contributions of each component.
- **Strong empirical results**: FGL achieves the best average rank (1.22) and top performance on most datasets, with notable gains on heterophilous graphs (e.g., Texas +13% over next best). Efficiency is demonstrated with 2–5× speedups over strong baselines like GCNII and DIFFormer.

## Weaknesses

### Fatal
None.

### Major
- **The pre-processing step (adding k-NN edges from pseudo-labels) is crucial but insufficiently ablated**: The method adds synthetic edges to ensure connectivity and increase homophily. The paper does not isolate the effect of this augmentation—how much of the performance gain comes from the pre-processing itself (which could be combined with many baselines) versus the forest-based paradigm? An ablation removing the pre-processing or using a simpler connectivity fix (e.g., connecting isolated components) would clarify the source of improvement.
- **Theory-practice gap in the homophily estimator analysis**: Theorem 2 assumes ground-truth edge scores (p for homophilous, q for heterophilous). In practice, scores come from a learned estimator trained on pseudo-labels. The paper states "as edge-homophily estimates improve, the induced tree distribution biases towards higher-homophily trees" but does not provide finite-sample guarantees or quantitative bounds on the impact of estimation error. The connection between the idealized theorem and the practical algorithm needs more rigorous treatment.

### Minor
- **Limited demonstration of the aggregator's generality**: The paper claims the tree aggregator works for any message aggregator satisfying Properties (I) and (II), but only implements a linear weighted-sum variant. No experiments with non-linear aggregators (e.g., RNN-style, SSM-style) are provided, leaving the generality claim unverified.
- **Missing some recent scalable baselines**: The baseline set is extensive, but omits some efficient GNNs like RevGNN, GCN-LPA, or GNN-AK. For large-scale datasets (Flickr, Arxiv), comparisons with scalable methods like ClusterGCN (already included) and GraphSAINT are included, but a few more would strengthen the efficiency claims.
- **Efficiency metrics could be more comprehensive**: The per-epoch time comparison does not include pre-processing time (pseudo-label training, k-NN construction) or the overhead of homophily estimator training. The total training time might be higher than suggested. Additionally, memory usage is not reported beyond the OOM indications.
- **Sensitivity to hyper-parameters**: The paper studies the number of trees and the estimator quality, but does not analyze sensitivity to the pre-processing k (number of nearest neighbors), the local module parameters (β₁, β₂, K_L), or the residual weight γ. Understanding the robustness to these choices would be helpful.

### Trivial
- Some figures (e.g., Figures 4, 5, 6) appear to be hand-drawn or low-resolution, which is a presentation issue but does not affect content.

## Nice-to-Haves
- Ablate the pre-processing step by removing k-NN edge addition or replacing it with a simpler strategy (e.g., connecting all isolated components to the closest node).
- Provide finite-sample analysis or at least empirical characterization of how estimation accuracy (e.g., AUROC of edge homophily prediction) translates into tree quality and downstream performance.
- Demonstrate a non-linear tree aggregator (e.g., using a GRU or Mamba-style recurrence) to support the claimed generality.
- Report total training time including pre-processing and estimator training for a fair comparison.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
- Add an ablation that removes the pre-processing augmentation (i.e., use the original graph with a connectivity fix such as adding a virtual node) to isolate the benefit of the forest-based paradigm from the benefit of synthetic edges.
- Include a supplementary experiment on a larger dataset (e.g., OGBN-Products or OGBG-PCQM4Mv2) to demonstrate scalability under the claimed linear complexity.
- Clarify in the main text that Theorem 2 applies under the simplifying assumption of perfect edge-label knowledge, and discuss how the practical estimator approximates this ideal.

## Score and Decision

Score: 8
Decision: Accept

This paper makes a substantial contribution by introducing a fundamentally new paradigm for graph learning that effectively addresses the long-standing trade-off between global coverage and cost. The idea is novel, theoretically motivated, and empirically validated across diverse graphs. The tree aggregator is a technically sound contribution that achieves linear-time global propagation. The experiments are thorough and show strong performance with practical efficiency gains. The weaknesses—primarily the incomplete ablation of pre-processing and the theory-practice gap in the homophily analysis—are addressable and do not invalidate the core contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>