## Summary

This paper proposes Forest-based Graph Learning (FGL), a paradigm that replaces traditional local-neighborhood or global-attention message passing with aggregation over sampled spanning trees (a "forest"). The key insight is that spanning trees are the minimal subgraphs achieving global coverage, balancing the efficiency–receptive-field tradeoff. The method includes: (1) a pre-processing step that augments the graph with k-NN edges from pseudo-labels, (2) a homophily-guided tree sampler with theoretical guarantees (Theorem 2), (3) a general linear-time tree aggregator based on two recursions, and (4) a tree fuser. Experiments on nine benchmark datasets show competitive or superior accuracy against 26 baselines, with linear complexity.

## Strengths

- **Well-motivated core idea (Secs. 1, 4).** The framing of spanning trees as the minimal globally-connected subgraph, positioned as a principled middle ground between local-neighborhood aggregation and dense global attention, is genuinely insightful. The cost analysis (Eq. 1: total cost = per-structure cost × number of structures) provides a clean conceptual basis for why trees could break the typical efficiency-vs-receptive-field tradeoff. This is the paper's primary intellectual contribution.

- **Theoretical connection between homophily estimation and tree quality (Sec. 4.6, Theorem 2).** The paper establishes a nontrivial monotonicity result: as the score ratio Δ = p/q increases, the expected homophily of sampled trees increases monotonically, with an interpretable upper bound governed by the graph's homophilous connected components and an asymptotic tightness result. This moves beyond the intuitive notion that weighting homophilous edges higher produces homophilous trees.

- **Linear-time tree aggregator (Sec. 4.3).** The two-recursion design (bottom-up then top-down) on a tree, enabling each node's representation to incorporate information from all other nodes in O(n) time, is technically sound. The claimed generality—that any aggregator satisfying the Combine/Disentangle properties can be plugged in—provides a useful framework, even though only the linear variant is empirically tested.

## Weaknesses

### Fatal
None.

### Major

- **The pre-processing step (Sec. 4.1) creates a confound between graph augmentation and the forest-based paradigm, preventing clear attribution of results.** The method first trains a model on labeled nodes, uses it to generate pseudo-labels for all nodes, then adds k-NN edges to the graph based on pseudo-label similarity. The resulting augmented graph has higher homophily than the original—the paper explicitly acknowledges this as a benefit ("it increases the homophily ratio"). Every baseline in Table 1 operates on the *original* graph, while FGL operates on the *augmented* graph. Therefore any performance gain could partially or primarily arise from the graph augmentation rather than from the forest-based learning paradigm. The ablation studies (Table 3) do not isolate this effect: every variant—including "Uniform Tree Sampling" (row 3)—still uses the augmented graph. What is missing is a variant that runs the full method on the **original graph without augmentation**, or baselines that also receive the augmented graph. Without this control, the contribution of tree-based aggregation cannot be disentangled from the contribution of graph structure modification. This is especially concerning because improvement patterns are exactly what one would expect from augmentation alone: modest gains on already-homophilous graphs (Cora +0.12, Citeseer +0.18 over best baselines) but enormous gains on heterophilous graphs (Texas: 91.89 vs GCNII's 69.19, a 22.7-point gap) where injecting homophily provides far more room for improvement.

### Minor

- **The claim that "perfect estimation leading to perfect classification" is unsupported by the data.** The Interpretability Studies paragraph states: "Fig. 5 reveals that as the accuracy of homophily estimator increases, model performance consistently improves across all datasets, with perfect estimation (accuracy is 1) leading to perfect classification." However, Fig. 5 shows accuracy on the y-axis against edge score p on the x-axis, with p ranging only from 0.0 to 0.9. No data point exists at p = 1.0, and no evidence of 100% classification accuracy is displayed. Extrapolating the trend to "perfect classification" is an overclaim not supported by the presented data.

- **The data split specification for heterophilous datasets is imprecise.** The paper states: "other datasets strictly follow the standard public splits in (Kipf & Welling, 2017)." Kipf & Welling (2017) introduced standardized splits for Cora, Citeseer, and Pubmed only, not for Actor, Cornell, Texas, or Wisconsin. These four heterophilous datasets were popularized by Pei et al. (2020) and are typically evaluated under different split configurations. If the paper uses different splits from what baselines were originally tuned for, the comparison may not be calibrated correctly. This imprecision affects reproducibility without the (removed) appendix.

- **Standard deviations are deferred to the appendix (Tab. 10) rather than included in the main results table (Table 1).** Without error bars in the main body, the reader cannot assess whether the reported gains—especially the tiny margins on Cora (+0.11 over TDGNN) and Citeseer (−0.04 behind DIFFormer, yet still underlined as runner-up)—are statistically meaningful.

- **The labeled data is used in multiple stages of the pipeline, raising concerns about information cycling.** The pseudo-label model (Sec. 4.1) is trained on the labeled nodes; those pseudo-labels then guide the graph augmentation and train the homophily estimator (Eq. 3); and the final classifier also uses the same labeled nodes. While not conventional double-dipping, the labeled data influences both graph structure and multiple learning stages, which could lead to overfitting to the labeled set. The paper should clarify whether the pseudo-label training and augmentation are performed before the final train/test split and quantify pseudo-label accuracy.

### Trivial

- **The "quadratic node-pair interactions" framing (abstract, contribution list) is somewhat overstated.** The linear-time tree aggregator enables each node's representation to incorporate information from all other nodes, but interactions are mediated through the tree's branching structure—the aggregator computes O(n) outputs, not O(n²) pairwise scores. While all-pairs information flow is achieved, claiming "quadratic interactions" suggests direct pairwise computation that does not occur.

## Nice-to-Haves

- Include a variant of the full FGL pipeline on the *original* (unaugmented) graph to isolate the forest-based paradigm from the effect of graph augmentation.
- Compare against baselines that also receive the same augmented graph (via the same pseudo-label procedure) for a fairer comparison.
- Report the accuracy of the pseudo-labels to help assess the quality of the homophily estimator's supervision.
- Clarify the exact split sizes and random seeds used for heterophilous datasets.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **SGFormer efficiency comparison (Table 2 note).** The reviewer criticized the paper for dismissing SGFormer's faster speed, but on Cora FGL is faster (0.005 vs 0.010) and on Arxiv FGL trades minor speed (0.246 vs 0.114) for higher accuracy (56.47 vs 45.73). The paper's characterization is reasonable; this is not a weakness. *Removed.*

- **Theorem 1 to implementation gap (Sec. 4.3 note).** The reviewer claimed the relationship between general M⁺/M⁻ operators and the specific formulas is unclear. However, the paper explicitly states: "adopting f_Agg and M⁺ as weighted sums, M⁻ as weighted difference, and g as a linear transformation" — the mapping is direct. *Removed.*

- **Pre-processing cost not accounted for (Sec. 4.5 note).** The paper already states "Each pre-training epoch costs O((n+m)d) time and space." The cost is disclosed. *Removed.*

- **Abstract/Introduction Eq. 1 as "framework-level intuition" (Section note).** This is an observation about presentation, not a weakness. The paper presents Eq. 1 as motivation, not a formal cost model. *Removed.*

## Novel Insights

None beyond the paper's own contributions. The reviews surface the central experimental confound but do not reveal additional novel insights about the method itself.

## Suggestions

1. **Add the critical control experiment:** Run the full FGL pipeline on the original graph (skipping the k-NN edge addition in pre-processing). If performance holds, especially on heterophilous datasets, the paradigm claim would be strongly supported. If it degrades sharply, that is itself valuable scientific information about the role of graph augmentation.

2. **Give baselines the same augmented graph:** Re-run the strongest baselines (GCNII, DIFFormer, SGFormer) on the augmented graph to see whether FGL's advantage persists even when all methods receive the same input.

3. **Correct the data split claim** for heterophilous datasets and report exact split specifications in the main text.

4. **Include standard deviations in the main results table** (or at minimum indicate statistical significance of top results).

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>