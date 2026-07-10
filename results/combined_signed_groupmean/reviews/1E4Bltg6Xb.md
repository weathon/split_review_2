## Summary

This paper proposes a Dynamics Feature Representation (DFR) framework for RL-based Dynamic Path Planning (DPP) in urban road networks. DFR uses a two-stage hierarchical refinement: (1) a "policy attention" mechanism that pre-trains a distance-based policy to select top-k shortest paths, forming a task-relevant subgraph, and (2) n-hop neighborhood extraction that further decouples this subgraph into node-local features for the RL agent. Experiments on three OSM-derived urban road networks compare DQN/PPO/GCN+DQN agents with and without DFR, along with a parameter ablation.

## Strengths

- **Well-motivated problem.** The paper correctly identifies the real trade-off in RL-based DPP between the informational completeness of global dynamics and the computational efficiency of local dynamics. Sections 1 and 4.1 articulate this tension clearly.

- **Clean three-level hierarchical refinement structure.** The decomposition (global dynamics → task-relevant subgraph via policy attention → node-local features via n-hop neighborhoods, Eq. 5) is conceptually appealing and well-communicated. The intuition—first identify what is globally relevant to the task, then decouple it locally for the agent's current position—is sensible.

- **Useful ablation study on k and n.** The systematic sweep over both parameters (Figure 6, Section 5.3) is the paper's strongest contribution. The heatmaps show how the two design choices interact, and the CR heatmap honestly shows the naive baseline uses ~121× the feature dimensionality, making the compression claim concrete and quantifiable.

## Weaknesses

### Major

- **Missing critical baselines.** The evaluation compares DFR+RL only against AD+RL (full graph dynamics). Without comparisons against other principled compression techniques (random subgraph selection matched for dimensionality, spectral sparsification, PCA of edge weights, or multi-layer GCN embeddings), it is unclear whether DFR's specific design choices matter or whether *any* dimensionality reduction would produce similar benefits. The AD baseline is a weak comparator: feeding thousands of edge weights into a 64-unit MLP is unlikely to work well, so outperforming it is a low bar. This gap undermines the paper's central claim that DFR resolves the completeness-efficiency trade-off better than existing approaches.

- **Weak GCN baseline.** The GCN+DQN baseline uses only a single graph convolutional layer (line 183: "GCN+DQN uses a graph convolutional layer for feature extraction"), which aggregates information from immediate neighbors only — effectively a 1-hop local view. A multi-layer GCN (2-3 layers) would be a more meaningful and competitive comparison, and would better test the paper's claim that GNN approaches are impractical without DFR.

- **PSR grounding is asserted but never substantiated.** Section 4.2 invokes Predictive State Representations as a theoretical foundation, claiming that W''_t serves as a predictive representation and that DFR "guarantees that the resulting representations are compact, temporally predictive, and theoretically sufficient" (lines 129-135). No formal argument, proof, or empirical test is provided to demonstrate that the representation satisfies PSR's conditions for predictive sufficiency. The PSR framing is rhetorical rather than substantive.

### Minor

- **"Policy attention" terminology overclaims the mechanism.** The method is static subgraph extraction via top-k shortest paths from a pre-trained distance policy — there are no learned attention weights, no query-key-value operations, and no differentiable end-to-end mechanism. The paper acknowledges this ("hard, pre-computed attention" in Section 2), but the term "policy attention" in the title and contribution statement creates misleading expectations for what is essentially distance-based graph pruning.

- **Main results reported only via radar charts without numerical tables.** Figure 5 uses radar charts that make exact GAP and SR values unreadable. While percentage planning-time reductions are reported textually (85.59%, 46.08%, 79.32%), the underlying GAP and SR values for all six methods across three subgraphs are not provided in a table. The ablation does provide numbers, but the main result supporting the headline claim does not.

- **Distance-based sparsification may be blind to dynamics it aims to capture.** The policy attention selects subgraphs based on static distance, not dynamic travel time. When congestion makes longer-distance routes faster, the top-k shortest-distance paths may systematically exclude the optimal travel-time route. The paper provides no analysis or ablation studying how often this failure mode occurs.

- **Ablation conducted on only one subgraph.** The systematic k/n parameter sweep (Section 5.3) is performed only on Subgraph 1 (Nanjing). Given the paper has three datasets, the ablation should be replicated on at least one additional subgraph to establish generality.

- **"Dynamic Dijkstra" ground truth is underspecified.** Line 175 states ground-truth paths are computed by the "dynamic Dijkstra algorithm" but does not clarify whether this is (a) a full-knowledge oracle replanning with access to future dynamics, (b) a deterministic algorithm assuming current weights persist, or (c) something else. This affects how GAP should be interpreted.

- **No variance reporting for main GAP and SR results.** Planning time is reported with ± values, but the core path-quality metrics (GAP, SR) are not accompanied by error bars, standard deviations, or confidence intervals across random seeds.

### Trivial

None.

## Nice-to-Haves

- Adding comparison against random (non-distance-based) subgraph selection would test whether distance is the right prior for sparsification.
- Training curves at intermediate checkpoints (beyond the final epoch) would strengthen the convergence claim in the abstract.
- A self-adaptive tuning mechanism for k and n, already mentioned as future work, would improve practical applicability.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:
- "No local-only baseline" — the ablation study (Figure 6) includes k=-1 conditions (no policy attention, only n-hop), which is a de facto local-only comparison. This exists in the ablation but not the main results.
- "Planning time comparison DFR vs AD is unfair" — the comparison is inherent to the paper's thesis; DFR is designed to reduce dimensionality so shorter planning time is expected.
- Requests for real-world traffic traces — scope creep beyond the paper's stated experimental design using OSM data with a synthetic congestion model.
- Notation inconsistency between v_i/v_j and v^t/v_g — a minor readability preference, not a substantive weakness.
- "GNN approaches impractical" claim not backed by runtime — this is a high-level motivation, not a central empirical result requiring proof.

## Novel Insights

None beyond the paper's own contributions. The key structural critiques (missing baselines, PSR overclaim, radar chart opacity) are useful for revision but are standard review observations.

## Suggestions

1. Add comparisons against alternative compression techniques (random subgraph, spectral sparsification, PCA of edge weights) at matched dimensionality to isolate whether DFR's distance-based subgraph selection drives improvement.
2. Use a multi-layer GCN (2-3 layers) as a stronger GNN baseline.
3. Report GAP, SR, and CR in a numerical table alongside the radar charts, with variance estimates across seeds.
4. Either substantiate the PSR connection with formal arguments or remove it.
5. Replicate the k/n ablation on at least one additional subgraph.
6. Add a control condition using random subgraph selection or distance-sparsification with initial dynamic weights to test sensitivity to the distance prior.
7. Clarify the "dynamic Dijkstra" algorithm specification.

## Score and Decision

**Calibration:** The paper was anchored against 19 retrieved reviews across two rounds. Closest peers: (a) *Structured Predictive Representations in RL* (4.80) — shares unsubstantiated theoretical claims and limited baselines, but has stronger presentation and experimental breadth; (b) *MetroGNN* (5.00) — similar weaknesses but compares against multiple baselines; (c) *Coverage Path Planning with RL* (4.75) — comparable ablation quality. Our paper's three decisive negative impact items (missing baselines -9.81/-9.98, weak GCN -9.94, PSR overclaim -10.00) outweigh the strong ablation contribution (+9.95), placing it below these anchors. The paper is clearly above the 3.00-level anchors (Dynamic TSP) which lack real-world data and thorough ablations, but has evaluation gaps too wide for acceptance at ICLR.

**Decision: Reject**

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>