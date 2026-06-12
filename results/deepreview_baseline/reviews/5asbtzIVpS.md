## Summary

This paper introduces Forest-based Graph Learning (FGL), a novel paradigm for semi-supervised node classification that reinterprets message passing on graphs as transportation over spanning trees. The key insight is that spanning trees are the minimal subgraphs achieving global coverage, enabling efficient long-range information propagation. The authors propose a framework consisting of: (1) a homophily estimator-based tree sampler that generates trees biased toward higher homophily, (2) a linear-time tree aggregator that realizes quadratic node-pair interactions, and (3) a tree fuser that integrates information across multiple trees. Theoretically, they establish an asymptotic relationship between edge-homophily estimation accuracy and tree distribution quality. Empirically, FGL achieves competitive or superior results against 26 baselines on 9 benchmark datasets while maintaining high efficiency.

## Strengths

- **Novel and well-motivated paradigm**: The paper identifies a fundamental limitation in existing graph learning approaches—the trade-off between cost-effectiveness and global receptive field—and proposes spanning trees as a principled intermediate structure. The analysis using "total cost = (cost per structure) × (number of structures)" provides clear intuition for why trees offer a sweet spot.

- **Strong theoretical foundation**: Theorem 2 establishes a rigorous asymptotic relationship between edge-homophily estimation accuracy and the quality of the induced tree distribution, showing monotonicity, upper bounds, and asymptotic tightness. This provides principled justification for the homophily-guided sampling approach.

- **Impressive empirical results**: The method achieves the best average rank (1.22) across 9 datasets, outperforming 26 baselines including state-of-the-art Graph Transformers and deep GNNs. The gains are particularly notable on heterophilous graphs (e.g., 91.89% on Texas vs. 78.92% for the next best SGFormer), where long-range dependencies are critical.

- **Efficiency**: The linear-time tree aggregator and overall linear complexity are well-demonstrated through both theoretical analysis and practical running time comparisons. The method is faster than most competitive baselines while achieving better performance.

## Weaknesses

### Major

- **Pre-processing step introduces potential label leakage**: The pre-processing step (Section 4.1) uses pseudo-labels to augment the graph by adding k-nearest neighbor edges. These pseudo-labels are generated using a model trained on the labeled nodes. This creates a potential information leakage issue: the augmented graph edges are constructed based on information derived from the labeled set, which could indirectly leak label information into the graph structure. The paper does not adequately address this concern or provide experiments controlling for this effect.

- **Limited analysis of the tree aggregator's generality**: While Theorem 1 claims the tree aggregator can work with any message aggregator satisfying Properties (I) and (II), the paper only implements a linear weighted-sum variant. The claim of generality is not empirically validated, and it's unclear how many practical aggregators actually satisfy these properties. The paper mentions linear attention, linear RNNs, and SSMs as examples but provides no experiments with these alternatives.

- **Ablation study design could be stronger**: The ablation study (Table 3) compares the full model against variants missing key components, but the comparison between (3) uniform tree sampling and (4) single homophily-guided tree is confounded—(3) uses multiple trees while (4) uses a single tree, making it difficult to isolate the effect of homophily guidance versus tree count.

### Minor

- **The tree fuser's local module (Eq. 9) is somewhat ad-hoc**: The local module uses a weighted combination of adjacency, attention, and identity matrices raised to power K_L (≤2). The motivation for this specific formulation and the hyperparameter choices (β₁, β₂, K_L) could be better justified.

- **The relationship between tree count and performance is not fully explored**: Figure 4 shows optimal performance at 6-10 trees, but the paper doesn't provide guidance on how to select this hyperparameter in practice or whether it depends on graph properties.

### Trivial

- The paper mentions "Codes are available at" but the URL is not provided in the extracted text.

## Nice-to-Haves

- An analysis of how the pre-processing augmentation affects the homophily ratio of the original graph versus the augmented graph would strengthen the motivation.
- A comparison with other tree-based graph methods (e.g., tree decomposition approaches) would help contextualize the contribution.
- Discussion of limitations: the method requires graph connectivity (addressed via pre-processing), and the tree sampling step adds overhead that could be analyzed more carefully.

## Novel Insights

Beyond the paper's own contributions, the key insight that spanning trees serve as the minimal globally-connected subgraph offers a fresh perspective on the graph learning efficiency-expressivity trade-off. The reinterpretation of message passing as transportation over trees provides a principled way to achieve global coverage without the quadratic cost of full attention or the depth requirements of stacked local models. The theoretical connection between edge-homophily estimation and tree distribution quality is also a valuable contribution that could inspire future work on structure-aware sampling in graphs.

## Suggestions

- Address the potential label leakage concern in the pre-processing step by either: (a) providing experiments that use only the original graph structure without augmentation, or (b) using a separate validation set for pseudo-label generation, or (c) clearly arguing why the current setup does not constitute leakage.
- Include experiments with at least one alternative tree aggregator (e.g., a simple RNN-based variant) to validate the claimed generality of Theorem 1.
- Add an ablation that controls for tree count when comparing homophily-guided versus uniform sampling (e.g., compare both with the same number of trees).

## Score and Decision

The paper presents a genuinely novel paradigm with strong theoretical grounding, impressive empirical results, and practical efficiency. The main concern about potential label leakage in the pre-processing step is significant but likely addressable. The contributions—a new learning paradigm, theoretical analysis, efficient algorithm, and strong experimental validation—are substantial and would bring significant value to the community.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>