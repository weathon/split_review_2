## Summary

This paper applies the previously proposed Goal-Oriented Environment Inference (GOEI) algorithm to a competitive card game, Hol's der Geier. The authors show that GOEI can reduce the state representation to 2.9% of the original observation space while achieving a near-optimal strategy (reward rate close to zero against the Nash equilibrium opponent). The paper compares GOEI with Q-learning and simple heuristic strategies, and analyzes which features of the observations are preserved in the reduced state representation.

## Strengths

- **Clear problem motivation**: The paper addresses the important challenge of state abstraction in reinforcement learning, which is relevant for both efficiency and explainability.
- **Impressive state reduction**: GOEI reduces the state space from 15,542 observations to 452 states (2.9%) while maintaining near-optimal performance, which is a striking empirical result.
- **Principled approach**: The use of variational Bayesian inference with Dirichlet processes provides a theoretically grounded method for automatic state abstraction without requiring a predefined number of states.
- **Informative analysis**: The mutual information analysis (Figure 3) gives insight into which features are preserved or discarded at different rounds, helping to understand what the reduced representation captures.

## Weaknesses

### Fatal
None.

### Major

1. **No algorithmic novelty**: GOEI is an existing method published in Neural Networks (2024). The paper contributes only an application to a new domain. For a top venue like ICLR, the contribution is incremental and lacks methodological innovation.

2. **Limited comparison baselines**: The only learning-based baseline is tabular Q-learning. The paper does not compare against other state abstraction methods (e.g., bisimulation metrics, MDP homomorphisms, deep learning-based representation learning, or other model-based RL approaches). Without such comparisons, it is unclear whether GOEI's performance is due to its specific design or simply to the fact that it performs state abstraction.

3. **Small-scale environment**: The game uses only 5 cards, resulting in a total observation space of ~15K states. While this is larger than the abstract environment in the original GOEI paper, it is still a very small problem by modern RL standards. Scalability to larger games (e.g., 15-card version) is not demonstrated, and the paper acknowledges memory limitations (12GB GPU) that would likely prevent scaling.

4. **Fixed opponent training**: The agent is trained on games between two fixed strategies (Rand vs. NE) rather than in an interactive online setting where the opponent adapts. The authors acknowledge this limitation, but it significantly reduces the realism and practical relevance of the evaluation. The claim that GOEI is suitable for online learning is not supported by the experiments.

5. **Statistical rigor of "near-optimal" claim**: The best median reward rate is -0.010 (Table 1). The paper states this is "indistinguishable from the optimal one (≈0)", but no statistical test (e.g., confidence interval on the difference from zero) is provided. Given the quartile ranges (e.g., -0.012 to -0.009), the performance may be statistically significantly different from zero.

### Minor

- The state reduction is not uniformly better than the Nash equilibrium's own state representation: at round 4, GOEI uses 408 states while NE uses only 69 states. The paper highlights the overall 2.9% reduction but does not discuss this discrepancy.
- The paper does not report computational cost (runtime, memory usage) of GOEI, which is important for assessing practical applicability.
- The explainability goal is only partially addressed: the mutual information analysis is informative, but the paper does not provide a concrete interpretation of what the reduced states represent (e.g., a decision tree or rule extraction).

### Trivial
None.

## Nice-to-Haves

- Comparison with other state abstraction methods (e.g., bisimulation, MDP homomorphisms, or deep representation learning) would strengthen the evaluation.
- Testing on a larger version of the game (e.g., 7 or 10 cards) or on a different game would demonstrate generality.
- An interactive learning experiment where the opponent also learns would be more realistic and informative.

## Novel Insights

None beyond the paper's own contributions. The main insight—that GOEI can achieve strong state reduction in a competitive card game—is a useful empirical validation of an existing method, but does not provide new theoretical or algorithmic understanding.

## Suggestions

- Add statistical tests (e.g., bootstrap confidence intervals) to support the claim that the reward rate is indistinguishable from zero.
- Include comparisons with at least one other state abstraction method (e.g., bisimulation-based abstraction or a deep learning baseline).
- Report runtime and memory usage to help readers assess scalability.
- Discuss why the state reduction at round 4 is less compact than the NE representation and whether this is a limitation.

## Score and Decision

The paper is a well-executed application of an existing method to a new domain, but it lacks the novelty and breadth of evaluation expected for a top venue like ICLR. The contribution is incremental, the environment is small, and the comparisons are limited. The paper would be more suitable for a specialized reinforcement learning or game theory workshop or conference.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>