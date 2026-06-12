## Summary

This paper applies Goal-Oriented Environment Inference (GOEI), a model-based reinforcement learning algorithm that extracts minimal "core" state representations from redundant observations, to the competitive card game "Hol's der Geier." The authors demonstrate that GOEI achieves near-Nash equilibrium performance using only 2.9% (452 states) of the original 15,542 possible observations, significantly outperforming Q-learning and several heuristic strategies. The paper analyzes which features of the game state are preserved versus discarded through the reduction process, and examines the sensitivity of GOEI to its hyperparameters.

## Strengths

- **Strong empirical demonstration of state reduction effectiveness**: The paper provides compelling evidence that GOEI can reduce the state space to a tiny fraction of the original observations (2.9%) while achieving performance indistinguishable from the Nash equilibrium. This is a non-trivial result in a game with complex dynamics and demonstrates the practical utility of the approach beyond simple abstract environments.

- **Clear experimental methodology**: The authors carefully separate environment inference from strategy optimization, training GOEI on fixed-strategy games (Rand vs. NE) and testing separately against the NE opponent. This design choice properly isolates the ability of GOEI to learn useful state representations from the confounding effects of policy improvement, making the results interpretable.

- **Detailed analysis of what information is preserved**: The mutual information analysis in Figure 3 provides concrete insights into which game features are retained versus discarded at each round. The finding that CT and RT are preserved in early rounds while SD becomes important only at the final round is intuitive and validates that GOEI learns sensible representations aligned with game-theoretic reasoning.

## Weaknesses

### Major

- **The opponent modeling assumption is restrictive and limits practical relevance**: The paper assumes the opponent selects cards based only on the current observation \(o_t\), independent of history across previous rounds or games (Section 3.1). This marginalizes the Markov property but is a strong assumption for any realistic competitive setting. In real play, opponents adapt based on past games, and this assumption essentially turns the problem into a sequence of independent decision problems rather than a true multi-agent learning scenario. The claim that GOEI is useful for "online learning to adapt to opponents" (Introduction) is not supported by experiments under this assumption.

- **Performance evaluation against NE opponent is insufficient to demonstrate generality**: The agents are trained on games between Rand and NE, then tested against the same NE opponent. While this tests whether GOEI learns the correct model of the environment under fixed opponent behavior, it does not test whether the learned state representations generalize to different opponent strategies. A more convincing evaluation would test against unseen strategies (e.g., \(\pi_0, \pi_1\), or other mixed strategies) to show the reduced representation captures genuinely "core" information rather than being specific to the NE opponent's action patterns.

- **Lack of comparison with alternative state abstraction methods**: The only baseline is Q-learning, which is a model-free method that does not attempt state reduction. The paper would be significantly strengthened by comparing GOEI to other state abstraction methods such as bisimulation metrics, MDP homomorphisms, or PAC-style state aggregation techniques. Without such comparisons, it is unclear whether GOEI's performance is due to the specific algorithmic design or simply because any reasonable state abstraction method would perform well in this game.

### Minor

- **The paper's claims about explainability are not fulfilled**: The introduction frames GOEI as addressing the need for explainability, and the discussion acknowledges that "we could not give a verbal explanation of the reduced state representation more concretely than Figure 3." This is an honest limitation, but the paper's motivation is partially misaligned with its contributions. The paper is fundamentally about state reduction for efficient learning, not about explainability per se.

- **The impact of the "2.9%" figure is somewhat inflated**: The claim of reduction to 2.9% (452/15,542) aggregates across all rounds, but the most significant reduction happens at round 4 (408/11,028 = 3.7%). At round 2, the reduction is more modest (8/300 = 2.7%), and the NE strategy itself has 247 states at round 2. The extreme compression at round 4 is less surprising because the game is nearly deterministic by then.

### Trivial

- The paper would benefit from a more detailed description of the variational Bayesian inference procedure, particularly how the Dirichlet process handles state creation during training.

## Nice-to-Haves

- Testing GOEI in an interactive online learning setting where the policy updates and environment inference happen jointly, as the authors acknowledge this is a limitation.
- Cross-validation against other opponent strategies to verify that reduced states capture general-purpose decision-relevant information.
- Comparison with a simple state aggregation method (e.g., discretization based on score difference bins) to establish a lower bound on what naive reduction achieves.

## Novel Insights

The paper provides a concrete demonstration that explicit state reduction via variational Bayesian inference on a Dirichlet process mixture can achieve near-optimal performance in a non-trivial competitive game while using orders of magnitude fewer states than the full observation space. The key insight is that the mutual information analysis reveals a non-obvious pattern: the reduced representation preserves complex combinations of features rather than any single interpretable feature, suggesting that "core" states are latent constructs that do not map simply to human-understandable concepts. This is a sobering finding for the claim that state reduction directly improves explainability—the representation is smaller but not necessarily more interpretable.

## Suggestions

- Add experiments testing GOEI's learned policies against a variety of opponent strategies (e.g., all \(\pi_k\) strategies, as well as the random strategy) to demonstrate that the reduced state representation captures generalizable decision-relevant information rather than features specific to the NE opponent.

- Include at least one alternative state abstraction baseline, such as simply clustering observations by their expected future return (bisimulation) or using a naive aggregation of the five features into coarser bins. This would contextualize GOEI's performance.

- Clarify the practical implications of the opponent modeling assumption. If the goal is to eventually deploy GOEI in truly adaptive multi-agent settings, discuss what modifications would be needed to relax this assumption.

## Score and Decision

The paper presents a well-executed empirical study of state reduction in a specific competitive game, with clean experimental design and informative analysis. The results demonstrate the potential of GOEI for efficient representation learning, which is a meaningful contribution to the reinforcement learning community. However, the restrictive opponent modeling assumption, lack of comparison with other state abstraction methods, and insufficient generalization testing temper the overall impact. The contribution is solid but not groundbreaking—it validates an existing method (GOEI) in a new, more realistic domain with careful analysis.

**Score**: 6

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>