Now I'll compose the final review.

## Summary

The paper proposes a Dynamics Feature Representation (DFR) framework for RL-based dynamic path planning in urban road networks. DFR progressively refines high-dimensional global traffic dynamics into compact, decision-relevant features through a two-stage hierarchy: (1) a "policy attention" mechanism that extracts a subgraph based on top-k shortest paths by distance, and (2) an n-hop neighborhood method that further decouples this into node-local features. Experiments on three realistic urban graphs with DQN, PPO, and GCN+DQN show that DFR improves performance and reduces planning time compared to using full-graph dynamics.

## Strengths

- **Well-motivated problem framing (Section 1, Section 4.1).** The trade-off between global dynamics (complete but expensive) and local dynamics (efficient but potentially non-Markovian) is a real issue in RL-based routing. The paper correctly identifies that insufficient state representation can undermine the Markov property, leading to unstable training. This framing is clear and sensible.

- **Model-agnostic framework.** DFR is applied on top of DQN, PPO, and GCN+DQN, and results are reported separately, allowing the reader to see that DFR helps across different RL algorithms. This is the right experimental design for a representation method.

- **Thorough ablation on k and n (Section 5.3, Figure 6).** The ablation explores a reasonable grid of (k, n) values and reports three metrics (Mean GAP, SR, CR) jointly, giving a fairly complete picture of how these hyperparameters interact. The observation that k has a "more complex and less predictable impact" than n (line 253) is a useful empirical finding.

## Weaknesses

### Fatal
None.

### Major

- **Distance-based subgraph selection vs. time-minimization objective is not empirically validated.** The policy attention mechanism selects paths based on static distance (lines 141–149), while the RL agent optimizes for traffic time under congestion. The paper argues that "distance naturally serves as one of the most fundamental constraints" (line 149) but provides no empirical evidence that distance-based selection preserves time-optimal routes. No comparison is made against alternatives such as time-aware path selection or even random subgraph selection of the same dimensionality, which would be needed to validate the claim that DFR identifies "task-relevant" dynamics.

- **No error bars or statistical reporting on core metrics.** The main results (Figure 5) and ablation heatmaps (Figure 6) report only point estimates. There is no mention of how many random seeds were used, no standard deviations, and no confidence intervals. RL is sensitive to random seeds (ε-greedy exploration, random experience replay, random source/goal sampling). The only place ± is reported is planning time (line 202). This is a significant gap for an empirical paper claiming performance improvements.

- **PSR theoretical grounding is asserted without formal support.** Section 4.2 (lines 129–135) invokes Predictive State Representations and claims this "guarantees that the resulting representations are compact, temporally predictive, and theoretically sufficient" (line 135). However, the paper provides no formal construction, no proof that W''_t satisfies the PSR property, and no empirical test of whether the representation captures sufficient statistics for prediction. The PSR reference is ornamental; the paper claims theoretical rigor it does not deliver.

- **AD baseline confounds representation quality with model capacity.** The AD (All Dynamics) baseline feeds the full high-dimensional edge-weight vector into the same small MLP (64-unit layers) that DFR uses for its compressed representation. The paper itself acknowledges that "the combination of a relatively small network and high feature dimensionality limits the model's ability to fully exploit dynamic information" (line 200). This confounds two variables: representation quality and model capacity. A proper control would use a larger-capacity encoder or a learned compression for the AD baseline to isolate the benefit of DFR's specific representation design.

### Minor

- **CR metric is ambiguous at the critical baseline point.** At (k=-1.0, n=-1) — the configuration where DFR is disabled — CR = 121.042% (Figure 6). If DFR is off, the "reduced" dimension should equal the original (100%), not exceed it. The paper does not explain what the "original dimension" refers to across configurations, making the metric uninterpretable at the key comparison point.

- **"Policy attention" is a misnomer.** The mechanism (lines 141–149) is a hard, static subgraph selection based on distance-computed shortest paths — it has no attention weights, no query-key-value computation, and no soft selection. While the paper acknowledges it is "hard" (line 41), the name invites confusion with actual attention mechanisms.

- **Pre-training π_d^* via RL is unnecessarily complex.** The paper trains an RL policy to find shortest paths by static distance (line 147). Dijkstra's algorithm solves this exactly and in closed form; using RL introduces an unnecessary approximation step and computational cost for no benefit.

- **Inconsistency in MDP formulation.** The MDP is described as "deterministic" (line 65), but the transition function T maps to [0, 1] (line 67), suggesting a stochastic formulation.

### Trivial
None.

## Nice-to-Haves

- Compare against a random-subgraph baseline of the same dimensionality to isolate whether DFR's specific selection matters beyond dimensionality reduction.
- Clarify how the congestion factor β evolves over time in the dynamics model.
- Report the numerical triangle areas from Figure 5 for transparency.

## Removed Points

These points are flagged to be removed; treat them with caution.

- Claim that the distance-vs-time mismatch is "not acknowledged" — the paper does acknowledge this in lines 147–149, though the empirical validation is lacking.
- The "strawman" framing of AD baseline — the paper uses the same architecture fairly across conditions; the capacity confound is a real weakness but the comparison is not a strawman.
- Typo/formatting nitpicks — parser artifacts.
- Criticism of the GNN practicality claim — the paper cites a reference and this is a standard limitation.
- Missing related work — cannot be verified without external sources.
- Missing appendix content — parser-stripped, not an author error.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run all experiments over at least 5 random seeds and report means with standard deviations.
2. Add a baseline with time-aware path selection (using current-step edge weights) to empirically validate that distance-based selection does not exclude time-optimal routes.
3. Add a random-subgraph baseline of the same dimensionality as DFR's output.
4. For the AD baseline, use a larger-capacity encoder or a learned compression to control for model capacity.
5. Either provide a genuine PSR construction linking DFR features to sufficient statistics, or drop the PSR "guarantee" language and use PSR only as motivation.
6. Clarify the definition of "original dimension" so that CR is interpretable at all configurations.
7. Replace RL-based pre-training of π_d^* with exact Dijkstra computation for simplicity.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>