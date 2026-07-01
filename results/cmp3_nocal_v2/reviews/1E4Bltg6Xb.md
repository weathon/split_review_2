## Summary

This paper proposes DFR, a hierarchical Dynamics Feature Representation framework for RL-based dynamic path planning (DPP). DFR compresses global road network traffic into a compact state representation via two stages: (1) a "policy attention" mechanism that selects a subgraph based on top-k shortest paths by distance, and (2) n-hop neighborhood extraction around the agent's current node, intersected with the policy attention subgraph. Experiments on three urban road networks show that DFR reduces planning time by 46–86% versus the full-graph "All Dynamics" (AD) baseline while maintaining or slightly improving path quality. The ablation study provides a thorough exploration of the two hyperparameters.

## Strengths

1. **Computational efficiency gains are substantial and well-documented.** The Compactness Rate (CR) data in Section 5.3 shows DFR compresses the input to under 6% of original dimensionality at reasonable settings (e.g., CR below 5.7% for n=4, k≥0.4). Planning time reductions of 85.59%, 46.08%, and 79.32% versus the AD baselines (Section 5.2, line 202) are large and practically meaningful.

2. **Thorough hyperparameter ablation.** The full heatmap grid across k ∈ {0.2, 0.4, 0.6, 0.8, 1.0, -1.0} and n ∈ {1, 2, 3, 4, -1} (Section 5.3) jointly visualizes GAP, SR, and CR, which is more informative than one-at-a-time ablations.

3. **Clean problem framing.** Sections 1 and 4.1 clearly articulate the tension between global (complete but expensive) and local (efficient but potentially suboptimal) state representations in RL-based DPP — a genuine and well-motivated problem.

## Weaknesses

### Fatal
None.

### Major

1. **The evaluation does not isolate whether DFR's specific two-step design matters versus any tractable compression of matched dimensionality.** The "All Dynamics" (AD) baselines feed the full graph's edge weights into an MLP. Crucially, the DQN architecture includes a **64-unit embedding layer** as the first layer (Section 5.1, line 183), which projects the high-dimensional input down to 64 dimensions before the hidden layers. So the AD baseline *can* process the input — the concern is whether it learns effectively from a noisy, high-dimensional projection. Since the paper's central claim is that DFR's *specific* hierarchical refinement (distance-based subgraph → n-hop intersection) resolves the completeness-efficiency trade-off, the evaluation needs comparisons against other compression strategies at comparable output dimensionality — e.g., (a) n-hop alone without policy attention, treated as a proper baseline, (b) a random edge subset of matched size, or (c) a GCN bottleneck with matched output dimension. The ablation data (Section 5.3) already hints that n-hop alone (k=-1.0 rows) achieves SR of 0.901 with n=3 — close to the best overall SR of 0.905 at (k=0.4, n=4) — suggesting the policy attention step's marginal benefit may be modest. Without compression baselines, the reader cannot tell whether DFR's particular design is validated or whether any moderate compression would suffice.

2. **The distance-based subgraph selection's failure modes are unexamined.** The "policy attention" step selects the subgraph based on static shortest paths by distance, while the optimization objective is travel time under congestion. The paper justifies this (line 149) by stating "distance naturally serves as one of the most fundamental constraints." However, when congestion patterns cause the shortest-distance path to be heavily congested while a longer-distance route is fast, the top-k distance-based paths may systematically exclude the dynamically optimal routes. The paper provides no analysis of when this mismatch occurs, how frequently it happens under the experimental congestion model, or whether the method degrades gracefully. This is an evidential gap for a core design choice.

### Minor

1. **No statistical variance over training runs.** All main results (Figure 5) are reported as point estimates without standard deviations over independent random seeds. RL experiments are high-variance, and single-run results can be misleading. The planning time numbers include ± (line 202), but these are over planning queries, not independent training runs. Without variance over seeds, the reader cannot assess whether the reported improvements are statistically significant.

2. **Internal inconsistency in reported numbers.** The text (line 253) states that at (k=0.4, n=4) the SR is 0.908, but the ablation table (line 232) shows SR=0.905 for that cell. This discrepancy should be corrected.

3. **The temporal dynamics model is underspecified.** The congestion factor β ∈ [0.1, 1.5] (line 159) is the sole source of dynamics, but the paper does not state how β evolves over time — is it i.i.d. per timestep, a random walk, an AR process? The entire motivation depends on dynamics having exploitable temporal structure; the absence of this description limits reproducibility.

4. **PSR grounding is invoked as post-hoc justification rather than a design principle.** The Predictive State Representation discussion (lines 129–135) asserts that DFR's output preserves decision-relevant information, but it does not derive *why* the specific choices of Ψ (distance-based subgraph) and Φ (n-hop intersection) satisfy PSR conditions. The framework is referenced but not used to guide or constrain the design.

5. **Graph sizes (nodes, edges) are only in figure captions, not stated in the text.** The reader has to infer the scale of the problem from Figure 4's legends. These should be explicitly stated in Section 5.1.

### Trivial

1. **"Policy attention" is an inflated term for a hard-coded graph pruning heuristic.** The paper acknowledges this (line 41: "hard, pre-computed attention"), but the term "attention" carries an implication of adaptivity and learned weighting that this mechanism does not have. It selects the same subgraph regardless of current congestion. "Distance-based subgraph pruning" would be more precise.

## Nice-to-Haves

- A diagnostic experiment where the optimal dynamic path systematically *differs* from the static shortest path (e.g., induced congestion on the shortest-distance route) to test whether the policy attention step can still capture the optimal route.
- A computational overhead breakdown: offline precomputation time, per-timestep feature extraction time, RL inference time, total planning time with and without DFR.
- Comparison against a random edge subset of matched dimensionality to test whether the structure of DFR's selection matters.
- Reporting results over at least 5 random seeds with means and standard deviations for key metrics.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Critical Issue #1's claim that the AD baseline "cannot process" the input.** Removed because the paper specifies a "64-unit embedding layer" as the first layer of the DQN (line 183), which projects the high-dimensional input down to 64 dimensions before the hidden layers. The network can process the input; the real concern (kept in Major #1) is about missing compression baselines, not network incapability.
- **Criticism that using RL to learn π_d* is unnecessarily complex.** Removed as a minor implementation choice that does not affect the paper's validity; using RL instead of Dijkstra for shortest paths is unusual but not a weakness.
- **Criticism that the "policy attention" framing is a fundamental deception.** Downgraded to Trivial because the paper explicitly states it is "hard, pre-computed attention" (line 41), showing transparency.
- **Suggestion to compare against traditional methods.** Removed because the paper explicitly scopes out this comparison (line 165) and the justification is reasonable for a paper focused on state representation within the RL paradigm.
- **Request for self-adaptive tuning of k and n.** The paper already acknowledges this as future work in the conclusion (line 257).
- **Criticism about "n-hop alone is doing most of the work."** This is a valid observation (moved into Major #1) but the reviewer's framing as a separate fatal weakness is excessive; it is better addressed as part of the missing-baselines concern.

## Novel Insights

The reviews surface one observation not fully discussed in the paper: the ablation data shows that the n-hop step alone (policy attention disabled, k=-1.0) achieves SR values close to the best joint configuration (e.g., SR=0.901 at k=-1.0, n=3 vs. SR=0.905 at k=0.4, n=4). This suggests the marginal benefit of the policy attention step is modest, and that most of the performance gain may come from the n-hop neighborhood decomposition. The paper does not discuss this pattern or its implication for the claimed contribution. Separately, the CR=121.042% for the (k=-1.0, n=-1) baseline is a curious artifact — if CR is defined as "reduced dimension / original dimension," the no-compression baseline should be 100%, not 121%. The paper should clarify this definition.

## Suggestions

1. Add comparisons against simpler compression baselines matched to DFR's output dimensionality (random edge subset of matching size, n-hop alone as a proper baseline, GCN bottleneck).
2. Run experiments over at least 5 random seeds and report mean ± std for GAP, SR, and CR.
3. Correct the SR discrepancy (0.908 vs. 0.905 in the ablation) and clarify the CR definition to explain why the AD baseline gives 121%.
4. Specify the temporal process for β (how congestion evolves between timesteps).
5. Include a diagnostic experiment where distance-optimal and time-optimal paths diverge to test the policy attention step's robustness.
6. Report graph sizes (node and edge counts) explicitly in the main text.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>