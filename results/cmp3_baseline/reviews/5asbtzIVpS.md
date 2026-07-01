## Summary

The paper introduces Forest-based Graph Learning (FGL), a novel paradigm where message passing on a graph is performed over a forest of spanning trees rather than the original dense graph. This allows global information propagation with linear complexity, breaking the tradeoff between cost and receptive field. The framework includes a homophily-aware tree sampler, a linear-time tree aggregator derived from two recursions, and a tree fuser. Theoretical analysis shows that improving edge-homophily estimates biases the tree distribution toward higher-homophily trees. Experiments on nine semi-supervised node classification benchmarks show competitive or state-of-the-art results with significantly higher efficiency.

## Strengths

- **Novel and principled paradigm**: The insight that spanning trees are the minimal globally-connected subgraphs, and that a forest can capture complementary topological pathways, is genuinely original and well-motivated. The formulation reframes the efficiency–receptive-field dilemma in a clear cost equation.
- **Strong theoretical grounding**: Theorem 2 establishes a rigorous asymptotic relationship between homophily estimator accuracy and the quality of the induced tree distribution, directly justifying the tree sampling strategy. The proof is claimed in the appendix.
- **Extensive empirical validation**: Experiments cover nine diverse datasets (homophilous and heterophilous), 26 baselines from GNNs, Deep GNNs, Graph Transformers, and Mamba-based methods. FGL achieves the best average rank (1.22) and substantial gains (e.g., 16.1% relative over DIFFormer, 24.5% over GCN).
- **Excellent efficiency**: Both time and space complexities are linear in nodes, edges, and hidden dimension. Practical runtime (Table 2) shows FGL is faster than most competitive baselines, often by 2–5×, and scales to large graphs (ArXiv, Flickr) where many GTs run out of memory.
- **Comprehensive ablation studies**: The ablations isolate the contributions of the global submodule, local submodule, homophily-guided tree sampling, and multi-tree fusion. Each component is shown to be beneficial, and the experiment on homophily estimator variants (Table 4) directly supports the theoretical claim.

## Weaknesses

### Fatal
None.

### Major
- **Unsubstantiated claim of generality for the tree aggregator**: The paper states that any message aggregator satisfying Properties (I) and (II) can be used (e.g., linear attention, linear RNNs, SSMs), but the actual implementation and experiments only use a simple weighted-sum aggregator. No concrete examples or experimental results are provided for alternative aggregators. This over-claims generality without evidence and may mislead readers about the framework’s actual flexibility.

### Minor
- **Pre-processing adds edges based on pseudo-labels**: The augmentation step uses k-nearest-neighbors among pseudo-labels derived from a model trained on the same labeled set. While this is a reasonable self-training technique, it introduces a dependency that is not fully analyzed—e.g., sensitivity to pseudo-label quality, or risk of reinforcing label noise. The paper could discuss this more thoroughly.
- **Gap between idealized theory and practice**: Theorem 2 assumes edge scores take only two values (p for homophilous, q for heterophilous), but the actual homophily estimator produces continuous attention scores. The asymptotic result provides intuition, but the mapping from learned attention to the binary scoring model is heuristic. The paper does not bridge this gap.
- **Choice of tree count**: The optimal number of trees (6–10) is determined empirically and varies across datasets. While the results are good, the paper does not provide a principle for selecting this hyperparameter aside from grid search.

### Trivial
None.

## Nice-to-Haves

- Provide experiments using a different aggregator (e.g., a linear RNN or SSM) in the tree aggregator to support the claimed generality.
- Analyze the sensitivity of the pre-processing step to the quality of pseudo-labels (e.g., by varying the training fraction).
- Offer a more direct link between the continuous attention scores and the binary scoring model used in Theorem 2 (e.g., by thresholding or probabilistic interpretation).

## Novel Insights

Beyond the paper’s own contributions, the key insight—that spanning trees are the minimal structures achieving global coverage and that a forest of such trees can efficiently encode long-range information—reframes how one can think about graph learning architectures. The connection to bagging (implicit in the forest analogy) and the use of tree-specific recursions to achieve quadratic pairwise interactions in linear time are conceptually elegant. This perspective may inspire new approaches that replace full-graph attention with tree-structured message passing in other domains (e.g., point clouds, molecule generation).

## Suggestions

1. **Temper or substantiate the generality claim**: Either provide at least one concrete alternative aggregator implementation (e.g., using a linear RNN) with experimental results, or explicitly state that the current work focuses on the weighted-sum version and leave other aggregators as future work.
2. **Discuss the gap between theory and practice**: Add a paragraph explaining how the continuous attention scores relate to the binary p/q model, e.g., via a softmax interpretation or by showing that score ratios approximate homophily bias.
3. **Provide guidance on selecting the number of trees**: Show a simple rule-of-thumb (e.g., \(N_T \approx \log n\) or based on empirical saturation) to reduce hyperparameter search.

## Score and Decision

MY FINAL SCORE: <score>8.5</score>
MY FINAL DECISION: <decision>Accept</decision>