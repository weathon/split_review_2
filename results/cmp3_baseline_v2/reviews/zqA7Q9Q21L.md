## Summary

This paper proposes R2PS, the first approach to worst-case robust real-time pursuit strategies under partial observability in pursuit-evasion games (PEGs). The authors theoretically extend dynamic programming (DP) solutions for Markov PEGs to handle asynchronous evader moves, introduce a belief preservation mechanism to manage partial observability, and embed this mechanism into the Equilibrium Policy Generalization (EPG) framework for cross-graph reinforcement learning. Experiments on real-world graphs show that the resulting GNN-based pursuer policy achieves strong zero-shot generalization to unseen structures, outperforming PSRO policies trained directly on the test graphs.

## Strengths

- **Addresses a practically important and under-explored problem**: Real-time pursuit strategies under partial observability with dynamic graph structures is relevant for security applications, and the paper correctly identifies the gap left by prior work that assumes perfect information.
- **Solid theoretical analysis of the DP algorithm**: Theorem 2 and Corollary 1 rigorously prove that the DP algorithm yields strictly optimal strategies under asynchronous evader moves, and Lemma 1 provides the minimax structure of the distance table. These results are non-trivial and well-established.
- **Comprehensive experimental evaluation**: Experiments cover 10 diverse real-world test graphs, compare against multiple evader strategies (Stay, DP_sync, DP_async, BR_async), include scalability tests with larger graphs, and provide ablation studies on belief update frequency and observation range. The consistent outperformance over PSRO trained directly on test graphs is a strong result.
- **Practical runtime advantage**: The O(n²m) inference complexity of the GNN policy versus O~(n^{m+1}) for DP recomputation is convincingly demonstrated, with sub-0.01 second inference times on GPU compared to minutes for DP.

## Weaknesses

### Major

- **Theoretical guarantees for the partially observable setting are very limited**: Lemma 2 only covers the trivial case where Pos is a singleton (i.e., full observability). The paper acknowledges that D(·) becomes an "optimistic estimator under partial observability," which means the core "worst-case robust" claim in the title and throughout the paper is not theoretically substantiated for the partially observable regime. The practical method is heuristic.
- **The belief preservation mechanism (7) assumes a uniform evader policy by default**, which can be highly inaccurate when facing an optimal or best-responding evader. The paper shows that using known opponent information improves results (Table 4), but in the primary setting where this knowledge is unavailable, the belief may be systematically misleading. The mechanism's robustness to mis-specified priors is not analyzed.

### Minor

- **Comparison with PSRO is favorable but somewhat asymmetric**: PSRO is trained on each test graph individually for only 10 iterations (10000 episodes/iteration), while R2PS uses extensive cross-graph pretraining (150 graphs × 30000 episodes + 150 graphs × 70000 episodes). The comparison would be stronger if PSRO were given more training budget or if a direct single-graph RL baseline were included.
- **The inference time comparison in Table 3 is confounded by hardware**: DP time is measured on CPU while RL time uses GPU. For a fair assessment of "real-time applicability," the comparison should either use the same platform or report CPU-only inference for the GNN policy as well.
- **The transition from equation (5) to equation (6) lacks justification**: Why belief averaging improves over the minimax position-based policy is explained only qualitatively ("pessimistic pursuit behaviors like staying at rest points"). A more rigorous analysis or an ablation showing when each is better would strengthen the paper.
- **The "first" claim ("first approach to worst-case robust real-time pursuit strategies under partial observability") is difficult to verify** and adds unnecessary risk if prior work exists. The contribution stands on its own merits without this claim.

### Trivial

- The pipeline diagram (Figure 1) is visually dense; the arrows and boxes are difficult to parse without careful study.

## Nice-to-Haves

- An analysis of the approximation ratio or regret of the belief-averaged policy relative to the optimal partially observable solution.
- Evaluation on graphs with larger node counts (5000+) to further stress-test scalability.
- A discussion of how the observation range of 2 was chosen and sensitivity to this hyperparameter during training.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Remove or soften the "worst-case robust" language throughout the paper, or provide formal worst-case guarantees under partial observability. The current framing overclaims relative to what is proven.
- Add a CPU-only inference time comparison for the GNN policy to complement the GPU results, enabling a direct like-for-like runtime comparison with DP.
- Include a baseline where a single-graph RL policy (e.g., MAPPO or SAC) is trained directly on each test graph under partial observability, so the zero-shot generalization benefit is isolated from the choice of RL algorithm.

## Score and Decision

Score: 6

Decision: Borderline Accept

The paper makes a meaningful contribution by extending EPG-style cross-graph RL to partial observability with a practical belief mechanism, provides solid theoretical results for the full-observability asynchronous-move case, and demonstrates convincing empirical performance. However, the gap between the "worst-case robust" claim and the heuristic nature of the partially observable extension, together with the limited theoretical grounding for the belief mechanism, prevent this from being a stronger acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>