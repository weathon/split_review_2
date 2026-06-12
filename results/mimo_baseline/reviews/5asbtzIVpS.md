## Summary
This paper proposes Forest-based Graph Learning (FGL), a novel paradigm that reinterprets graph message passing as information transport over a forest of spanning trees. The framework includes a homophily-guided tree sampler (supported by Theorem 2 on asymptotic distribution quality), a linear-time tree aggregator (Theorem 1 with recursive combine/disentangle operations), and a tree fuser for integrating multi-tree messages. Extensive experiments on nine benchmarks demonstrate competitive or superior performance against 26 baselines while maintaining high efficiency.

## Strengths
- **Genuinely novel paradigm**: The core insight—treating graphs as fusions of spanning trees rather than dense structures—offers a principled middle ground between deep local models and shallow global models. The cost analysis in Eq. 1 elegantly motivates why spanning trees are the optimal structure for balancing per-structure cost and number of structures.
- **Non-trivial theoretical contributions**: Theorem 2 rigorously establishes that improving the edge-homophily estimator provably shifts the induced tree distribution toward higher-homophily trees, with monotonicity and asymptotic tightness results. Theorem 1 provides the recursive framework enabling linear-time computation of what would otherwise be quadratic node-pair interactions on trees.
- **Strong empirical performance**: The method achieves best or near-best results across all nine benchmarks, with average rank 1.22. The gains are particularly large on heterophilous datasets (Texas: 91.89%, Wisconsin: 86.27%, Cornell: 83.24%), with substantial margins over prior methods.
- **Comprehensive ablations**: Table 3 systematically validates each component. Table 4's homophily estimator comparison directly supports Theorem 2 empirically. Figure 6 demonstrates that the guided sampling achieves significantly higher tree-level homophily ratios than random sampling across all datasets.
- **Efficiency**: Table 2 shows practical speedups of 2-5× over efficient baselines like DiFFormer and GCNII, and orders-of-magnitude improvements over heavy methods like GOAT and ANS-GT, while achieving better accuracy.
- **Generality of the tree aggregator**: The combine/disentangle properties (Eq. 4) subsume many aggregation functions (linear attention, RNNs, SSMs), making the framework broadly applicable.

## Weaknesses
### Fatal
None.

### Major
- **Large margins on small heterophilous datasets deserve deeper scrutiny**: On Texas (183 nodes), FGL achieves 91.89% vs. the next best 78.92% (SGFormer)—a 12.97% absolute gap. Wisconsin and Cornell show 5-6% gaps. These datasets are known to have high variance due to small size and specific data splits (Pei et al., 2020a). While the paper reports 10 initializations, standard deviations are deferred to the appendix (Table 10), and the reader cannot assess stability. The magnitude of these gaps is unusual for well-studied benchmarks and warrants stronger evidence (e.g., statistical significance tests, reporting standard deviations prominently).
- **Disentangling pre-processing contribution**: The k-NN graph augmentation based on pseudo-labels (Sec. 4.1) modifies the graph structure substantially. For heterophilous datasets, this essentially creates a feature-similarity-based graph via an MLP. Comparing (C) the two-stage estimator alone (Table 4) achieves strong heterophilous results (e.g., Cornell 78.38, Texas 83.78, Wisconsin 82.75) without any tree-based component. This suggests the pre-processing is a major contributor, and the ablation in Table 3 does not include "FGL without pre-processing augmentation" to isolate the forest component's contribution from the graph augmentation.

### Minor
- **Efficiency comparison excludes pre-training cost**: Table 2 reports per-epoch training time but the two-stage estimator requires additional pre-training epochs. For a complete efficiency picture, total training time (including estimator pre-training) should be reported.
- **Tree aggregator simplification**: The actual implementation (Eq. 7-8) uses weighted sums, which is a specific instantiation of the general framework. The gap between the general theory and practical implementation could be discussed more explicitly—do the non-linear variants (mentioned in Sec. A.6) offer meaningful improvements?

### Trivial
None.

## Nice-to-Haves
- Report standard deviations alongside main results in Table 1 for immediate readability.
- Include an ablation variant "FGL without k-NN augmentation" to isolate the forest contribution.
- Add statistical significance tests (e.g., paired t-test) given the large margins on small datasets.
- Provide total wall-clock training time including the pre-processing/estimator training stage.

## Novel Insights
The paper's reinterpretation of graph message passing as transport on spanning trees is a genuinely fresh perspective in the GNN literature. The connection between edge-homophily estimation quality and tree distribution quality (Theorem 2) is a clean theoretical result that provides actionable design guidance. The observation that a small number of spanning trees (6-10) suffices to capture most of the graph's structural information for classification is a practically valuable finding. Additionally, the identification that spanning trees are the *minimal* structures achieving global coverage—thus simultaneously minimizing per-structure cost and number of structures—is an elegant structural insight that could inspire follow-up work on graph rewiring and sparse attention.

## Suggestions
- Add a "w.o. pre-processing augmentation" row to Table 3 to clearly separate the forest contribution from the graph augmentation.
- Include total training time (pre-training + fine-tuning) in Table 2 alongside per-epoch time.
- Add standard deviations to the main results table rather than deferring entirely to the appendix.
- Consider exploring whether the strong heterophilous performance partially stems from the augmented graph being essentially a k-NN graph on features, which naturally captures similarity structure. An analysis comparing against pure k-NN graph baselines on heterophilous datasets would strengthen the contribution.

## Score and Decision
The paper presents a genuinely novel paradigm with solid theoretical grounding and comprehensive empirical validation. The core idea is well-motivated, the theoretical results are clean, and the experiments cover diverse settings. However, the unusually large margins on small heterophilous datasets and the inability to clearly disentangle the forest contribution from the pre-processing augmentation temper confidence in the reported results. These are addressable concerns rather than fundamental flaws.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>