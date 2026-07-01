## Summary

This paper introduces R2PS, the first approach to worst-case robust real-time pursuit strategies in graph-based pursuit-evasion games under partial observability. The authors extend a dynamic programming (DP) algorithm to handle asynchronous evader moves and propose a belief preservation mechanism to handle partial observability. They embed this mechanism into the Equilibrium Policy Generalization (EPG) framework to train a graph neural network (GNN) policy via cross-graph reinforcement learning. The resulting policy generalizes zero-shot to unseen real-world graphs and outperforms Policies Solved by Reinforcement learning (PSRO) policies trained directly on test graphs under various evader strategies.

## Strengths

- **Addresses an important underexplored setting:** The paper tackles worst-case robustness under partial observability in graph-based pursuit-evasion games, which has practical security applications and was not addressed by prior work like EPG (perfect information) or Grasper (no cross-graph generalization).
- **Sound theoretical extension of DP:** The authors prove that the DP algorithm can be extended to asynchronous-move evaders while maintaining optimality, and they propose a principled belief preservation mechanism for partial observability. Lemma 1 and Theorem 2 provide rigorous justification.
- **Strong empirical results:** The RL policy achieves consistently higher zero-shot success rates than PSRO policies trained directly on test graphs across multiple real-world maps, against various evader opponents including the strictly optimal asynchronous DP evader. Ablation studies (belief update frequency, known opponent information, observation range) convincingly demonstrate the benefits of the proposed components.
- **Real-time applicability demonstrated:** The inference time complexity is O(n²m), and the paper shows concrete timing comparisons (e.g., <0.01s vs. >2 minutes for DP recomputation), confirming practical real-time feasibility.

## Weaknesses

### Fatal

None.

### Major

- **Comparison limited to PSRO:** The baseline comparison only includes PSRO, which is not specifically designed for partial observability or cross-graph generalization. A more comprehensive evaluation against other partial-observability PEG methods (e.g., POSG solvers with abstraction, or other POMDP-based RL approaches) would strengthen the claim of being the first robust real-time approach under partial observability.
- **No treatment of observation noise or stochasticity:** The partial observability model is deterministic (evader detected exactly if within range). Real-world sensors often have false positives/negatives. The paper does not discuss how the belief mechanism would degrade under noisy observations, which limits practical impact.

### Minor

- **Heuristic belief update without theoretical guarantees:** The belief update uses a uniform evader policy when unknown. While ablation shows it still works, there is no theoretical guarantee that this belief approximates the true state distribution, unlike POMDP belief updates. The paper does not analyze convergence or error bounds of the belief under this heuristic.
- **Claim of being "first" is marginally overstated:** Although the combination is novel, there exist works on POMDP-based pursuit-evasion and on generalization in games; the paper could more carefully delineate what exactly is first (e.g., first to combine worst-case robustness, partial observability, and cross-graph RL for graph-based PEGs).

### Trivial

None.

## Nice-to-Haves

- An analysis of how the belief preservation mechanism performs under different initial distance distributions beyond the fixed condition used in experiments.
- A discussion of how the approach might scale to larger numbers of pursuers (m > 2) in terms of both DP and RL feasibility.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add a comparison with at least one partial-observability baseline, even if simplified (e.g., a POMCP-lite approach adapted to the PEG setting) to better situate the empirical contribution.
- Include a brief discussion of how sensor noise could be incorporated into the belief update, perhaps via probabilistic detection models, and whether the method could still perform robustly.

## Score and Decision

Score: 6

Decision: Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>