## Summary

This paper proposes STBP, a novel framework for continual spatio-temporal forecasting that integrates a general-purpose spatio-temporal backbone with a scalable contextual pattern bank. The backbone uses frequency-domain analysis and linear graph attention to capture stable representations and dynamic spatial correlations, while the pattern bank is incrementally expanded to adapt to new data distributions and mitigate catastrophic forgetting. Experiments on three real-world datasets demonstrate significant improvements over existing methods in forecasting accuracy and scalability.

## Strengths

- **Strong empirical results**: STBP achieves substantial improvements over state-of-the-art baselines across all three datasets, with MAE reductions of 21.44%, 21.93%, and 2.35% on PEMS-Stream, CA-Stream, and AIR-Stream respectively. The gains are particularly impressive on the large-scale traffic datasets.
- **Well-motivated problem formulation**: The paper clearly identifies the limitations of existing STGNNs and CSTF methods, correctly arguing that current approaches either rely on static assumptions or adopt backbones with limited modeling capacity. The four key challenges outlined (§1) provide a structured framework for evaluating contributions.
- **Careful ablation study**: The ablation experiments isolate the contributions of each component—the backbone, DLGA module, and contextual pattern bank—demonstrating that each is necessary for the overall performance. The variants are appropriately designed to test specific hypotheses.
- **Efficiency analysis**: The paper addresses scalability concerns directly, showing that linear attention reduces computational complexity and that STBP maintains competitive training times despite its more sophisticated backbone. The toy dataset experiment validating O(N) vs O(N^2) complexity is particularly useful.

## Weaknesses

### Fatal
None.

### Major
- **Unclear novelty relative to existing CSTF literature**: Several components of STBP closely follow or adapt existing ideas. The contextual pattern bank with prompt-based guidance (§4.2) appears conceptually very similar to EAC's (Chen & Liang, 2025) dynamic prompt pool, which also expands and compresses over time. The linear attention mechanism for graph attention is a direct application of Katharopoulos et al. (2020). The frequency-domain network for handling distributional drift (§4.3) follows established principles in signal processing and has been explored in prior STGNN work (e.g., Xia et al., 2023). The paper would benefit from a clearer articulation of which aspects are genuinely novel versus engineering combinations of existing techniques.
- **Missing details on experimental protocol**: The paper does not specify how many incremental periods exist for each dataset, what the total number of nodes is at each stage, or how the "streaming" nature of the data is constructed from the original datasets. Without this information, it is difficult to assess the severity of the continual learning challenge posed by each dataset or to reproduce the results. The description "all datasets are split into training, validation, and test sets using a fixed ratio of 6:2:2" (§5.1) reads as if it describes a standard offline split, not a streaming setup.
- **Limited baseline coverage for the AIR-Stream dataset**: The gap between STBP and the best baseline on AIR-Stream (2.35% MAE reduction) is much smaller than on the traffic datasets (~21%). The paper attributes this to the different domain but does not analyze why the improvement is so much smaller, nor does it discuss whether the AIR-Stream dataset presents a fundamentally easier or harder continual learning scenario.

### Minor
- **The term "general spatio-temporal backbone" is somewhat misleading**: The backbone is designed specifically for this particular framework and is not demonstrated to be generally useful across different tasks or datasets outside of STBP. The claim that it is "general" (§4.3) because it is independent of node count and adjacency matrix is true but applies to any MLP-based or transformer-based architecture, not uniquely to this design.
- **The t-SNE visualization analysis (§4.2, Figure 3) is qualitative and somewhat subjective**: While the clustering appears meaningful, the paper does not quantitatively evaluate how well the pattern bank captures node relevance and heterogeneity (e.g., via clustering metrics like silhouette score or comparison to ground-truth node categories).

### Trivial
- None.

## Nice-to-Haves
- An analysis of how the number of incremental periods or the size of node expansion per period affects performance would strengthen the scalability claims.
- A discussion of failure cases—situations where STBP performs worse than baselines—would provide a more balanced evaluation.

## Novel Insights

None beyond the paper's own contributions. The key insight—that freezing a general-purpose backbone and only updating a small set of task-specific parameters can balance stability and plasticity in continual learning—is well-established in the broader continual learning literature (e.g., prompt tuning, adapter modules) and has been applied to CSTF by EAC. The paper's main contribution is demonstrating that a more capable backbone (with frequency-domain processing and linear attention) combined with this strategy yields better results than simpler backbones used in prior CSTF work.

## Suggestions

1. Provide explicit details on the streaming setup: number of incremental periods per dataset, node count at each period, and the exact construction of the incremental graph sequence.
2. Clarify how the contextual pattern bank differs conceptually from EAC's prompt pool and what specific advantages the proposed design offers over EAC's compression/expansion mechanism.
3. Add quantitative evaluation of the pattern bank clustering (e.g., silhouette score, NMI) to support the qualitative t-SNE analysis.
4. Include an analysis of per-period performance to show not just average improvement but also stability across stages (e.g., whether STBP degrades less than baselines on later periods).

## Score and Decision

This paper addresses a relevant and timely problem, executes a thorough experimental evaluation, and achieves strong empirical results. However, the novelty is somewhat incremental—the main contribution appears to be engineering a stronger backbone for existing CSTF strategies rather than introducing a fundamentally new approach to continual learning. The combination is effective and well-evaluated, which warrants acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>