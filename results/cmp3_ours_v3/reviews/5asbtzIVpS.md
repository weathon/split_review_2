Now let me produce the final consolidated review.

## Summary

The paper proposes FGL, a paradigm that replaces standard message passing on a full graph with message passing on a forest of sampled spanning trees. The method comprises four components: (1) pre-processing that augments the graph by adding k-NN edges based on pseudo-labels, (2) a homophily-biased spanning tree sampler using Wilson's algorithm, (3) a linear-time two-recursion tree aggregator, and (4) a tree fuser combining global and local information. The authors provide a theoretical result (Theorem 2) linking homophily estimator quality to tree distribution quality and report strong results on heterophilous node classification benchmarks with favorable per-epoch efficiency.

## Strengths

1. **Genuinely novel paradigm (Section 4, Figure 2).** The core idea — replacing standard message passing on a full graph with message passing on a forest of sampled spanning trees — is creative and well-motivated via the cost-per-structure × number-of-structures analysis (Eq. 1). A spanning tree is indeed the minimal subgraph achieving global coverage, offering a principled middle ground between deep local models (many low-cost structures) and shallow global models (few high-cost structures). This is a genuinely different conceptual approach to the global-receptive-field problem in GNNs.

2. **Rigorous theoretical result connecting homophily estimation to tree quality (Theorem 2, Section 4.6).** Theorem 2 establishes a monotonicity result (better edge-homophily estimates → higher expected tree homophily) and an upper bound tied to the graph's structural limitations, with asymptotic tightness. This is a genuine theoretical contribution that goes beyond what most GNN method papers offer — it does not just name-drop theory but actually proves a non-trivial relationship between estimator quality and sampling distribution.

3. **Strong empirical results on heterophilous graphs (Table 1).** On Texas (91.89%, +13 pts over SGFormer at 78.92%), Cornell (83.24%, +6.5 pts over GraphMamba/Graphormer), and Wisconsin (86.27%, +5.9 pts over GraphMamba at 80.39%), the gains are substantial. The average rank of 1.22 across 9 datasets is genuinely impressive.

4. **Practical efficiency (Table 2).** The method is often the fastest or among the fastest per epoch, especially on larger graphs (0.246s on ArXiv vs. GCNII's 2.843s). This aligns with the claimed linear complexity.

5. **Informative ablation study (Table 3).** The progressive improvements from conditions (3)→(4)→(5) tell a coherent story about the value of homophily-guided sampling and multi-tree fusion, helping isolate the contributions of different components.

## Weaknesses

### Major

1. **Pre-processing step creates an uneven comparison with baselines.** Section 4.1 describes augmenting the graph by computing pseudo-labels from a model trained on labeled nodes, then adding k-NN edges between nodes with similar pseudo-labels. This increases the graph's homophily ratio, which the paper acknowledges "has been shown to improve performance in semi-supervised node classification." The baselines in Table 1 operate on the *original* graph without this augmentation. The ablation study (Table 3) does not include a "full FGL without pre-processing" condition, so the contribution of the forest-based paradigm cannot be disentangled from the graph augmentation. Concretely, on Texas, even the local-submodule-only variant with pre-processing (row (1) in Table 3: 82.88%) outperforms the best baseline SGFormer (78.92%), suggesting pre-processing alone provides substantial benefit that baselines were not given. While pre-processing is a legitimate component of the framework, the headline comparisons conflate two distinct effects (graph augmentation + forest aggregation).

### Minor

2. **"Quadratic node-pair interactions" overstates expressivity.** The abstract and contributions (lines 9, 36) state the tree aggregator "realizes quadratic node-pair interactions." On a tree, every pair of nodes does interact through products of edge weights along the unique path, so O(n²) interactions technically occur. However, these are *path-constrained* interactions — they are products of edge-level attention weights along a fixed tree path, not the unconstrained pairwise dot-products of full quadratic attention. The phrasing invites readers to infer attention-level expressivity at linear cost, which is imprecise.

3. **Missing ablation: without pre-processing.** The ablation study (Table 3) varies tree sampling strategies and submodule choices but never removes the pre-processing step. Adding a condition "FGL on the original graph (no k-NN augmentation)" would directly quantify how much of the performance gain comes from the forest-based aggregation vs. the graph modification. This is the most important missing experiment for interpreting the results.

4. **Per-epoch timing understates total training cost.** Table 2 reports only per-epoch timing, excluding the one-time costs of: (a) training the pseudo-label model to convergence, (b) computing k-NN for all nodes (which can be O(n²d) naively), and (c) running Wilson's algorithm N_T times. The complexity analysis in Section 4.5 mentions "pre-training epoch" costs but the timing comparison does not include these. A full end-to-end timing comparison would be more informative.

5. **Generality claim for non-linear aggregators is unverifiable in the main text.** Section 4.3 claims the tree aggregator can accommodate "non-linear variants (Sec. A.6)," but the appendix is not accessible in this version and the actual implementation uses only linear weighted sums. Without seeing the appendix, this claim lacks support in the main paper.

6. **Gains on larger datasets are modest compared to small heterophilous ones.** On Arxiv (+2.7% over GCN) and Flickr (+3% over DiFFormer), the gains are far smaller than on Texas (+13 pts), Cornell (+6.5 pts), and Wisconsin (+5.9 pts). The paper does not discuss this discrepancy. One plausible explanation is that the pre-processing step has proportionally more impact on very small graphs, which would further reinforce the need for the ablation suggested in point 3.

### Trivial

7. **The k value for k-NN edge addition is not reported.** Section 4.1 does not specify how many nearest neighbors are added per node, which affects both reproducibility and understanding of how much the graph structure is modified.

8. **Avg. Rank computation is unclearly documented.** Table 1 reports "Avg. Rank" but does not state whether missing entries (OOM for GT, SAN, Graphormer, TDGNN on Arxiv/Flickr) are excluded or assigned a penalty rank.

## Nice-to-Haves

- Run FGL without the pre-processing step to isolate the forest paradigm's contribution.
- Provide baselines evaluated on the same augmented graph to control for the effect of graph modification.
- Report end-to-end training time including pre-processing and tree sampling.
- Report the k value and discuss sensitivity to this hyperparameter.
- Measure the diversity of sampled trees (e.g., average pairwise Jaccard similarity).

## Removed Points

These points from the input review were removed with justification:

1. **"The two-recursion pattern lacks novelty (belief propagation)."** The paper frames the two recursions as a *key observation* enabling efficient tree aggregation within their GNN framework, not as a novel algorithmic discovery about trees in general. The contribution is applying this known tree-processing pattern to GNNs with specific linear aggregators, which is legitimate.

2. **"Diversity principle not operationalized."** The paper uses independent sampling from Wilson's algorithm, which naturally provides diversity. The reviewer acknowledges this is "partially justified."

3. **"Abstract's cautious language vs. actual results."** Not a weakness; the paper's claims are appropriately scoped.

4. **Missing related works.** Removed per policy — cannot verify existence of external references.

5. **Formatting/presentation nitpicks.** Parser artifacts, not author errors.

6. **Missing appendix content.** Removed per policy — appendix exists in original submission.

7. **Speculation about pre-processing's impact across graph sizes.** The reviewer's explanation for the Arxiv/Flickr vs. Texas/Cornell discrepancy is plausible but speculative as a criticism; the observation itself is retained as weakness 6.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add an ablation condition running the full FGL pipeline on the original graph *without* pre-processing (k-NN edge addition). This is the single most important experiment for interpreting the results.

2. Report end-to-end training time including pre-processing (pseudo-label model convergence + k-NN computation) and tree sampling (Wilson's algorithm), not just per-epoch training time.

3. Replace "quadratic node-pair interactions" with more precise phrasing, e.g., "enables each node to aggregate information from all other nodes along tree paths in linear time."

4. Report the k value for k-NN augmentation, the rationale for choosing it, and its sensitivity.

5. Clarify how Avg. Rank in Table 1 handles missing entries (OOM).

## Score and Decision

**Calibration anchors (all rounds):**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bEgDEyy2Yk.md` (avg 1.0, round 1): Unrelated dense graph paper; clearly worse than FGL.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/VyMW4YZfw7.md` (avg 3.0, round 1): "Simplifying GNN Performance" — limited novelty, narrow experiments; weaker than FGL.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GEZACBPDn7.md` (avg 5.25, round 1): "KDGCN" — graph classification under label scarcity, limited scope.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ctXZJLBbyb.md` (avg 5.8, round 1): "Understanding Heterophily" — theory-heavy, limited practical recommendations; rejected despite decent score.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/oSdrJyb4UH.md` (avg 6.0, round 2): "Monophilic Neighbourhood Transformers" — neighborhood transformer for heterophily, rejected with scores 5,8,5; FGL has stronger novelty and theory.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Abr7dU98ME.md` (avg 6.5, round 1): "Forward Learning of GNNs" — forward-forward for GNNs, missing important experiments; comparable novelty to FGL.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/y21ZO6M86t.md` (avg 7.25, round 2): "PolyGCL" — spectral polynomial filters for contrastive learning; cleaner evaluation than FGL.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/viftsX50Rt.md` (avg 8.0, round 1): "General Graph Random Features" — strong theory, clean experiments, all 8s; stronger than FGL.

**Round 1 bracket:** [5.5, 7.0]. FGL is stronger than the 3.0–5.8 papers due to its novel paradigm and theoretical result, but the evaluation concern (pre-processing) prevents it from reaching the 7+ band where papers like PolyGCL sit with cleaner evaluations. It sits naturally alongside the 6.0–6.5 papers: comparable novelty to "Forward Learning of GNNs" (6.5) and "Monophilic Neighbourhood Transformers" (6.0) but with a more significant evaluation gap that needs addressing.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>