## Summary

This paper proposes a Dynamics Feature Representation (DFR) framework for RL-based dynamic path planning in urban road networks. DFR uses a two-stage hierarchical refinement: (1) a "policy attention" mechanism that pre-trains a distance-oriented RL agent to identify top-k shortest paths and extracts a task-relevant subgraph, and (2) an n-hop neighborhood method that further decouples this subgraph into local features centered on the agent's current node. Experiments on three urban road networks compare DQN, GCN+DQN, and PPO with and without DFR.

## Strengths

1. **Well-motivated problem framing (Section 1, lines 13–19).** The paper correctly identifies the genuine tension in RL-based dynamic path planning: encoding full graph dynamics gives complete information but blows up input dimensionality, while purely local observations risk violating the Markov property. This framing grounds the contribution clearly.

2. **Interpretable hierarchical decomposition.** The two-stage refinement (task-level filtering via distance-based subgraph selection, then agent-level decoupling via n-hop neighborhoods) is a natural and conceptually clear design. The ablation study (Section 5.3, Figure 6) systematically varies both k and n, providing useful insight into their interaction and showing that performance saturates beyond a certain n threshold.

3. **Consistent empirical improvement across multiple algorithms and graphs.** DFR improves over the All-Dynamics (AD) baseline for DQN, GCN+DQN, and PPO on all three urban subgraphs (Figure 5), and reduces planning time substantially (85.6% for DQN, 46.1% for GCN+DQN, 79.3% for PPO).

4. **Honest acknowledgment of limitations.** Section 6 acknowledges that manual tuning of k and n limits practical applicability, and proposes self-adaptive parameter selection as future work.

## Weaknesses

### Major

1. **The core assumption of the policy attention mechanism is unvalidated (Section 4.3, lines 141–149).** The mechanism selects the top-k shortest paths based on static distance and assumes these paths contain the dynamics-relevant subgraph. The paper's only justification is that "distance naturally serves as one of the most fundamental constraints" (line 149). In a dynamic setting where the optimization objective is travel time under congestion (Equation 9), the optimal path under time-varying traffic can diverge arbitrarily from the shortest-distance path. The paper provides no analysis—theoretical or empirical—of how often the optimal dynamic path is actually contained within the distance-based subgraph. The method could still work well in practice (the empirical results suggest it does), but without this validation, we cannot assess whether the specific selection mechanism is the reason for the improvement, or whether any reasonable dimensionality reduction would suffice. **This is the most serious weakness in the paper.**

2. **The convergence-acceleration claim in the abstract (line 9) is unsupported.** The abstract claims DFR "accelerates convergence compared to baselines," but the only training curves shown (bottom of Figure 6) compare different DFR configurations to each other, not DFR to AD. No learning curves comparing DFR vs. Any-Dynamics convergence trajectory are presented anywhere in the paper. This claim should be substantiated with direct evidence or removed.

3. **Missing critical baselines.** The main comparison is DFR vs. AD (All Dynamics). For DQN+AD and PPO+AD, the state is the full graph's edge weights fed into an MLP—a very high-dimensional input that MLPs are known to handle poorly. While GCN+DQN+AD is a more reasonable baseline, the paper does not compare against equally low-dimensional alternatives such as: (a) a random subset of edges of the same dimensionality, (b) simple graph aggregation statistics (mean/variance per node), or (c) using only the n-hop neighborhood without the policy attention stage as a primary baseline (it is only presented in the ablation). Without these, it is unclear whether DFR's improvement comes from selecting the right edges or merely from reducing dimensionality to a level the MLP can process.

4. **No statistical significance for main results (Section 5.2).** The main metrics (Mean GAP, SR) are reported as single values without standard deviations, confidence intervals, or significance tests. Only planning time includes ± (line 202). Without variance estimates, it is impossible to assess whether the reported improvements are meaningful or within noise.

5. **Graph statistics and congestion dynamics are underspecified (Section 5.1).** The paper does not report the number of nodes, edges, or average degree of the three subgraphs, making it impossible to evaluate the claimed dimensionality reduction. Furthermore, the temporal evolution of the congestion factor β is not described—the paper says edge weights are "parameterized by a congestion factor β(v_i, v_j; t) ∈ [0.1, 1.5]" but does not specify the stochastic process that generates β over time.

### Minor

1. **The PSR theoretical grounding is asserted without justification (Section 4.2, lines 129–135).** The paper claims that W''_t serves as a predictive representation grounded in Predictive State Representations (PSR), but this connection is purely rhetorical. PSR requires that the representation predicts future observations conditioned on action sequences, and no argument or evidence is provided that the n-hop dynamics within a distance-based subgraph has this property. This section adds little and could be removed without affecting the paper.

2. **The distance-based RL pretraining is unnecessary (Section 4.3, line 147).** The paper trains an RL agent π_d* to find shortest paths under static distances. Dijkstra's algorithm provides exact shortest paths without any training, making this pretraining step computationally wasteful. While this choice does not affect the final method's validity, it is an odd design decision that the authors should justify.

3. **Ablation conducted on only one subgraph (Section 5.3).** The systematic sweep over k and n is performed only on Subgraph 1 (Nanjing). The trends may not generalize to the other two urban networks.

### Trivial

- The formalism in Section 3 is somewhat overwrought for what the method ultimately does—much of the notation (W_{:T}, the full dynamics sequence) is introduced with ceremony but never directly used in the method or evaluation.

## Nice-to-Haves

- Compare DFR against a same-dimensionality random subgraph selection to isolate whether the specific selection mechanism matters.
- Provide learning curves comparing DFR vs. AD convergence speed to support the convergence-acceleration claim.
- Validate the key assumption by measuring, on the experimental data, how often the optimal dynamic path falls within the top-k distance-based subgraph.
- Replace the RL-based shortest-path pretraining with Dijkstra's algorithm for efficiency.

## Removed Points

**"AD baseline is a straw man" (softened → Major #3).** The harsh critic characterized the AD comparison as a "structural flaw" and "straw man." This is too strong: the paper includes GCN+DQN+AD as a baseline that is more reasonable than raw-MLP-on-edge-weights, and DFR improves over that baseline too. The concern about missing alternative low-dimensional baselines is retained (Major #3), but the "straw man" framing is removed.

**"Policy attention is not attention" (removed).** The paper explicitly describes it as "hard, pre-computed attention" (line 41), acknowledging it is not soft/self-attention. The substantive concern (unvalidated assumption) is retained in Major #1; the semantic naming dispute is removed.

**"Related work is too generic" (removed).** Removed per rule: we cannot verify what related work exists outside the paper.

**"Radar charts are difficult to read" (removed).** Partially a presentation nitpick; the substance (numerical tables would help) is too minor to retain.

**Section-by-section notes about optimality preservation claims (Equations 6–8) (removed).** This is essentially a restatement of the unvalidated assumption concern already covered in Major #1.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Empirically validate that top-k distance-based shortest paths contain the optimal dynamic path on your datasets, and report the containment rate.
2. Add convergence curves comparing DFR vs. AD to support or retract the acceleration claim.
3. Add statistical significance measures (standard deviations or confidence intervals) for Mean GAP and SR.
4. Report basic graph statistics (node/edge counts, average degree) for each subgraph.
5. Include baselines with random subgraph selection of the same dimensionality.
6. Specify the congestion evolution model for reproducibility.
7. Justify the use of RL for the distance-based pretraining or replace it with Dijkstra's algorithm.
8. Either develop the PSR connection into a real theoretical analysis or drop it.

---

### Calibration Anchors

**Round 1 bracket: 3.0–5.5** (initially determined by comparing against strong reject, reject, and borderline accept bands).

**Anchors retrieved across bands:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `NIhRwzqhUz.md` (Dynamic TSP) | 3.00 | R1 | Similar topic (dynamic routing + RL); that paper had no ablation study and limited baselines. Our paper is stronger. |
| `Gs8jWk0F01.md` (Dynamic CVRP) | 2.20 | R1 | Similar topic (dynamic VRP + DRL); that paper had poor writing and unclear contributions. Our paper is stronger. |
| `z3L59iGALM.md` (Google Maps IRL) | 5.25 | R1 | Real-world deployment at scale with strong theory. Our paper is weaker. |
| `VeFmnRmoaW.md` (MetroGNN) | 5.00 | R1 | Urban transport + RL with GNN; limited novelty but strong empirical results. Our paper has similar scope but weaker baselines. |
| `YJxhZnGU1q.md` (Congestion Games) | 4.25 | R1 | Theoretical contributions with limited experiments. Not directly comparable. |
| `Pj3ErOxlLo.md` (NaviFormer) | 6.00 | R1 | Stronger methodology (Transformer for navigation). Our paper is weaker. |
| `NEu8wgPctU.md` (AdaWM) | 5.75 | R1 | World model for autonomous driving; stronger evaluation. |
| `ZiF1bJ9K6B.md` (Coverage Paths) | 4.75 | R2 | RL for coverage path planning; thorough feature representation analysis. Our paper has weaker evaluation rigor. |
| `r125wFo0L3.md` (Large Trajectory Models) | 5.00 | R2 | Motion prediction at scale; stronger methodology. |

**Narrowing:** The paper sits well above the 2–3 range (it has a clean framework, ablation study, and consistent results across 3 algorithms × 3 graphs) but below the 4.75–5.33 range (those papers have stronger evaluation rigor and more novel methodology). The unvalidated core assumption, missing baselines, and lack of statistical significance place it in the 3.5–4.5 band.

**Final score:** 4.0.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>