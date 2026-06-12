## Summary

This paper presents a method for learning discrete POMDP parameters (transition and observation matrices) from action-observation sequences collected under a random exploration policy, without knowledge of the state space. The key insight is to connect Predictive State Representations (PSRs), which learn transition/observation matrices up to an unknown similarity transform, with tensor decomposition methods to estimate that transform. The method recovers POMDP parameters up to a "full-rank observability partition"—groups of states that share the same observation distribution across all actions with full-rank transition matrices—and demonstrates that explicit observation and transition likelihoods can be leveraged for reward specification to direct planner behavior.

## Strengths

- **Novel theoretical bridge between PSRs and tensor decomposition**: The paper makes a genuine contribution by extending the Carlyle & Paz (1971) / Balle et al. (2014) result on PSR similarity transforms and reformulating tensor decomposition methods (Anandkumar et al., 2012; Azizzadenesheli et al., 2016) to estimate the unknown basis. This relaxes the per-action uniqueness assumption of prior tensor methods, allowing all full-rank actions to contribute jointly to the similarity transform estimation.

- **Well-motivated practical value**: The paper convincingly argues that explicit transition and observation likelihoods enable operations that black-box PSRs cannot support, such as specifying reward functions post-learning to direct agent behavior. The reward specification experiments (Figure 4) on the noisy and directional hallway domains provide concrete evidence that this flexibility matters—particularly in the noisy domain where observation-based reward assignment fails but state-based assignment using learned observation models succeeds.

- **Clear running example and theoretical exposition**: The Sense-Float-Reset domain effectively illustrates the nontrivial challenges (singular transition matrices, ambiguous observations across states) and the concept of full-rank observability partitions. Theorem 1 is clearly stated with a concrete worked example (Figure 2) showing how partition-level likelihoods are computed.

## Weaknesses

### Fatal

None.

### Major

- **Very limited experimental scale**: All experiments use POMDPs with only 2–4 states. The Hankel matrix construction requires enumerating action-observation sequences up to a certain length, making the approach potentially expensive for larger systems. Without any medium-scale experiments (e.g., 10–50 states), it is difficult to assess whether the method is practical beyond pedagogical examples. The scalability concern is acknowledged as future work but deserves more than acknowledgment given the method's reliance on matrix decompositions of potentially very large Hankel matrices.

- **Weak baselines**: The EM baseline is a simple HMM-style EM algorithm with the number of states set by the truncated SVD. This is a reasonable baseline but does not represent current best practices in POMDP learning (e.g., model-based deep RL approaches, or more sophisticated spectral methods). The comparison would be more compelling with additional baselines that better represent the state of the art.

- **Limited domain diversity**: The standard POMDP benchmarks used (Tiger, T-Maze, Sense-Float-Reset) are very small and toy-like. The novel hallway domains are designed specifically to highlight the method's reward specification advantage. More diverse benchmarks—including POMDPs from established libraries with varying characteristics—would strengthen the generalizability claims.

### Minor

- **Convergence rate analysis missing**: While the experiments show convergence with sufficient data, there is no theoretical or empirical analysis of sample complexity. How much data is needed as a function of the number of states, actions, and observations? This is important for practical applicability.

- **Theorem 1 assumes infinite data**: The main theoretical result is stated in the infinite data regime. While finite-data extensions are deferred to Appendix B.1, the gap between theory and experiments could be better bridged with at least a brief discussion of practical convergence rates.

- **Reward specification experiments on limited domains**: The noisy/directional hallway domains are 3-state problems. The claim that "explicit observation and transition likelihoods can be leveraged to specify planner behavior" would be more convincing with demonstrations on larger, more realistic problems.

### Trivial

None.

## Nice-to-Haves

- A runtime comparison between the proposed method, PSR, and EM across different problem sizes would help practitioners assess tradeoffs.
- A discussion of how to select the SVD truncation threshold in practice and its sensitivity would be useful.
- An analysis of the method's behavior when the ergodicity or full-rank assumptions are slightly violated (robustness analysis).

## Novel Insights

The paper's central novel insight is that the similarity transform ambiguity in PSRs can be resolved by jointly diagonalizing observation matrices derived from *all* full-rank actions simultaneously, rather than requiring per-action uniqueness as in prior tensor decomposition approaches (Azizzadenesheli et al., 2016; Guo et al., 2016). When states share observation distributions across all full-rank actions, the method gracefully degrades to learning transitions between partitions of states rather than failing entirely. This partition concept provides a natural spectrum between full state recovery (when all observation distributions are unique) and coarser abstractions, offering a useful theoretical framework for understanding the limits of observability in POMDP learning.

## Suggestions

- Include at least one experiment with a moderately-sized POMDP (10+ states) to demonstrate scalability beyond toy problems, even if with a longer data budget.
- Add a brief sample complexity analysis (empirical if not theoretical) showing how data requirements scale with POMDP size.
- Expand the baselines to include at least one more competitive spectral or neural method for POMDP learning.
- Consider demonstrating the reward specification capability on a robotics-inspired domain (e.g., the cabinet domain mentioned in the introduction) to connect back to the motivating application.

## Score and Decision

The paper presents a genuine theoretical contribution connecting PSR learning with tensor decomposition for POMDP parameter recovery, addressing a real gap in the literature between black-box predictive models and explicit likelihood models. The partition concept is well-motivated and the reward specification experiments demonstrate practical value. However, the experimental evaluation is limited to extremely small synthetic domains with weak baselines, making it difficult to assess real-world impact. The theoretical contribution warrants acceptance, but the limited empirical evidence tempers enthusiasm.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept