## Summary
This paper introduces R2PS, the first approach to worst-case robust real-time pursuit strategies under partial observability in graph-based pursuit-evasion games. The authors theoretically extend a dynamic programming algorithm to handle asynchronous evader moves and partial observability via a belief preservation mechanism, then embed this into the Equilibrium Policy Generalization (EPG) reinforcement learning framework to train a GNN-based pursuer policy that generalizes zero-shot to unseen graph structures. Experiments demonstrate that the learned policy outperforms PSRO baselines trained directly on test graphs, achieving real-time inference with worst-case robustness.

## Strengths
- **Novel problem formulation**: The paper is the first to address worst-case robust real-time pursuit strategies under partial observability with graph structure generalization, filling a clear gap in the literature where prior work (EPG, Grasper) assumed perfect information.
- **Theoretical contributions**: The authors provide rigorous proofs that the DP algorithm maintains optimality under asynchronous evader moves (Theorem 2, Corollary 1) and that the belief preservation mechanism reduces to the optimal perfect-information policy when observability is unlimited (Lemma 2).
- **Strong empirical results**: The cross-graph RL policy consistently outperforms PSRO policies directly trained on test graphs across diverse real-world maps (Table 2), including against the strictly optimal asynchronous-move evader and best-responding adversaries.
- **Practical real-time capability**: The inference time complexity of O(n²m) with GPU acceleration (under 0.01 seconds for large graphs) is orders of magnitude faster than recomputing DP policies, enabling real-time application in dynamically changing environments.

## Weaknesses
### Fatal
None.

### Major
- **Limited evaluation of the belief preservation mechanism's theoretical guarantees**: While Lemma 2 shows the policy reduces to the optimal case when Pos is a singleton, there is no theoretical characterization of how the belief-averaged policy degrades under partial observability. The paper relies on empirical results to justify the approach, but the gap between the "optimistic estimator" (as acknowledged) and the true optimal policy under partial observability is not formally bounded.
- **Missing comparison with alternative partial observability approaches**: The paper does not compare against any existing partially observable RL methods (e.g., recurrent PPO, memory-based architectures, or POMDP solvers) that could serve as baselines for the partial observability aspect specifically. The only baseline is PSRO, which is a game-theoretic method not designed for partial observability.
- **The training set construction is somewhat ad-hoc**: The synthetic training set (150 Dungeon maps + 150 random urban locations) lacks systematic justification for why this particular distribution enables zero-shot generalization. There is no analysis of training set diversity, coverage of graph properties, or ablation on training set composition.

### Minor
- **The belief update mechanism (Equation 7) assumes a uniform evader policy by default**, which may be suboptimal when the evader follows a non-uniform strategy. While Table 4 shows that using the known opponent policy improves results, the paper does not discuss how sensitive the approach is to this assumption in practice.
- **The success rate metric (capture within 128 timesteps) is somewhat arbitrary** and may not fully capture the quality of pursuit strategies, especially for graphs with large diameters where 128 steps may be insufficient even for optimal play.

### Trivial
- The paper uses "Lancet et al." in the PSRO citation (should be "Lanctot et al."), but this is a minor formatting issue.

## Nice-to-Haves
- A theoretical bound on the suboptimality gap of the belief-averaged policy under partial observability would strengthen the paper significantly.
- Comparison with a POMDP-based approach or a recurrent neural network policy trained with PPO under partial observability would better isolate the contribution of the belief preservation mechanism.
- Analysis of how the number of training graphs affects zero-shot generalization performance would help practitioners understand the data requirements.

## Novel Insights
The key insight is that the distance table from the DP algorithm, which encodes optimal worst-case capture times under perfect information, can be repurposed as a "value function" for partial observability through belief averaging. This bridges the gap between exact game-theoretic solutions and practical RL-based approaches: the DP provides a strong reference signal for policy learning, while the belief mechanism handles the information asymmetry. The finding that training against asynchronous-move optimal evaders across diverse graphs yields policies that outperform per-graph PSRO training is non-trivial and suggests that cross-graph training induces a form of regularization that improves robustness.

## Suggestions
- Add a theoretical analysis (even a simple bound) characterizing how the belief-averaged policy's performance degrades as a function of the belief uncertainty (e.g., size of Pos or entropy of the belief distribution).
- Include a baseline that uses a standard partially observable RL method (e.g., recurrent PPO with GRU) trained on the same training graphs, to isolate the benefit of the DP-guided training and belief mechanism.
- Provide an ablation study on the number of training graphs to help understand the data efficiency of the cross-graph generalization.

## Score and Decision
The paper makes a clear contribution by being the first to address worst-case robust real-time pursuit under partial observability with graph generalization, supported by theoretical analysis and strong empirical results. The weaknesses are not fatal and can be addressed in future work or discussion. The paper is well within the acceptance range for ICLR.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>