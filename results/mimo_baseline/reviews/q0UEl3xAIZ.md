## Summary

This paper applies Goal-Oriented Environment Inference (GOEI), a previously proposed model-based RL algorithm, to a competitive card game "Hol's der Geier" to validate its ability to learn minimal state representations ("core states") in a more realistic environment. GOEI reduces the observation space from 15,542 possible observations to 452 states (2.9%) while achieving performance nearly indistinguishable from the Nash equilibrium against a NE opponent, significantly outperforming tabular Q-learning.

## Strengths

- **Rigorous evaluation against a known optimal solution.** The use of a game with a computable Nash equilibrium provides a clear, objective benchmark. The reward rate of ≈0 against the NE opponent (Table 1, median -0.010) is a strong quantitative result that demonstrates the sufficiency of the reduced state representation.

- **Substantial state reduction with interpretable analysis.** The mutual information analysis (Figure 3) meaningfully characterizes what information is preserved versus discarded across rounds, showing that score difference becomes important only in later rounds while hand card information is largely compressed away. This goes beyond simply reporting state counts.

- **Systematic parameter exploration.** The paper sweeps over α and β parameters (Figure 4, Table 1) and provides reasonable interpretations of their effects (β controlling sparsity of transitions, α controlling exploration of new states), giving practitioners useful guidance.

## Weaknesses

### Fatal

None.

### Major

- **Artificially separated training and evaluation undermines the core claim.** GOEI is trained on games between fixed Rand vs. NE strategies, then tested against NE. The agent never learns from its own gameplay, and the training distribution is static. This sidesteps the fundamental challenge of online RL where strategy changes alter the data distribution. The paper acknowledges this limitation (Section 5), but it is severe: the claim that GOEI "effectively excludes information irrelevant to game outcomes" is only demonstrated under this artificial setup, not under interactive learning where the relevant information might differ.

- **Insufficient baselines.** The only comparison is against tabular Q-learning, which is known to struggle with large observation spaces. Missing are comparisons with: (1) deep RL methods (DQN, PPO) that handle large state spaces through function approximation; (2) other state abstraction methods (bisimulation metrics, homomorphic MDPs); (3) even simple feature-based approaches that use domain knowledge to hand-craft reduced features. Without these, it is impossible to assess whether GOEI's state reduction is genuinely superior to alternative approaches.

- **Modest environment complexity.** Despite the paper's framing as a "realistic, difficult environment," this is a 5-card, 2-player, 4-round game with ~15K total observations. The game has a small, finite action space and a known analytical solution. The gap between this and environments where state reduction would be truly impactful (e.g., imperfect-information games with continuous or very large state spaces) is substantial.

### Minor

- **Statistical claims need support.** The paper states GOEI's performance is "indistinguishable" from NE (reward rate ≈0), but the median is -0.010 with quartiles [-0.012, -0.009]. No statistical test is provided to support indistinguishability, and the gap, while small, is systematic.

- **Incremental contribution over prior work.** GOEI was already proposed and validated in Takahashi et al. (2024) on an abstract environment. This paper's contribution is essentially a validation on a slightly more complex game, with the same algorithm and no methodological novelty.

- **Scalability is unclear.** The paper notes memory constraints (12GB GPU) limited experiments to the 5-card version and vaguely suggests "introducing an appropriate upper bound" for larger versions, but provides no analysis of computational scaling.

### Trivial

- The claim that the game is "difficult for humans to understand" (Section 1) is unsupported and likely overstated for a simple 5-card game.

## Nice-to-Haves

- An interactive learning experiment where GOEI updates its model while simultaneously playing against the NE opponent would substantially strengthen the paper's claims.
- Comparison with at least one deep RL baseline (e.g., DQN with a small network) to contextualize the state reduction benefit.
- Analysis of the learned state mappings themselves—what do the 8 states at round 2 actually represent in game-theoretic terms?

## Novel Insights

The paper's most interesting finding is that the information preserved by GOEI shifts across rounds: current and remaining table cards matter early, while score difference becomes important only at the final round. This round-dependent information structure is a genuine observation that aligns with game-theoretic intuition but is empirically demonstrated through the mutual information analysis. However, this insight is somewhat expected given the game's structure and does not constitute a deep novel contribution beyond the paper's own validation exercise.

## Suggestions

- Replace the tabular Q-learning baseline with a deep RL method to make the comparison meaningful for the claimed contribution (handling large observation spaces).
- Run at least one experiment with interactive learning, even if performance degrades, to understand the practical limitations.
- Provide confidence intervals or statistical tests for the "near-optimal" performance claim.

## Score and Decision

The paper presents a clean validation of GOEI on a non-trivial game with a known optimal solution, and the state reduction results are impressive in magnitude. However, the artificially separated training setup, the absence of meaningful baselines, and the incremental nature of the contribution over the prior GOEI paper significantly limit the paper's impact. The results are promising but insufficient to establish that GOEI provides a practical advantage over existing approaches.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject