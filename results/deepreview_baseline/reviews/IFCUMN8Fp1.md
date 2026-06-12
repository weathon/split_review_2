## Summary

This paper proposes a spectral method for learning the parameters of a discrete POMDP (transition and observation matrices) from action-observation sequences collected under a uniform random policy. The approach builds a Hankel matrix from data, computes a rank factorization to obtain a linear Predictive State Representation (PSR), and then applies tensor decomposition and joint diagonalization techniques to estimate the similarity transform that recovers explicit POMDP parameters up to a *full-rank observability partition*—groups of states that have identical observation distributions across all full-rank actions. Experiments on small POMDP benchmarks (Tiger, T-Maze, Sense-Float-Reset, and custom hallway domains) show that the learned partition-level models converge to ground-truth likelihoods and achieve planning performance comparable to PSRs, while additionally enabling reward specification based on explicit transition/observation probabilities.

## Strengths

- **Clear theoretical contribution bridging PSRs and tensor methods.** The paper extends known results (Carlyle & Paz, Balle et al.) to formally characterize what can be recovered: observation and transition matrices up to a partition of states sharing identical observation distributions across all full-rank actions (Theorem 1). This relaxes the stronger per-action uniqueness assumption of earlier tensor-decomposition approaches.
- **Principled algorithm with finite-sample considerations.** The method uses joint diagonalization (He et al., 2024) to aggregate information across all full-rank actions, reducing ambiguity from repeated eigenvalues. The paper provides practical steps for handling finite data, including thresholding for rank determination and processing to ensure partition-level belief sums are proper likelihoods.
- **Empirical validation of convergence and planning utility.** Experiments show that the learned observation and partition-level transition errors decrease with more data, and that planning performance (using PO-UCT) is comparable to that obtained with the ground-truth model or a linear PSR. The reward-specification experiments on the noisy hallway domain convincingly demonstrate a concrete advantage of having explicit transition/observation matrices over black-box PSR predictions.
- **Well-motivated problem and honest discussion of assumptions.** The paper grounds the learning problem in a realistic robotics scenario (e.g., actions with failure probabilities) and explicitly discusses when the required assumptions (full-rank actions, ergodicity) are likely to hold, rather than simply asserting them.

## Weaknesses

### Major

- **Scalability is unaddressed.** All experiments use very small state spaces (2–4 states). The method depends on enumerating all length-limited histories/tests to form the Hankel matrix, which grows combinatorially. The paper acknowledges that scaling to larger problems remains future work, but without any evidence or analysis (e.g., on a 10-state domain or with a larger observation space), it is unclear whether the approach is practical beyond toy benchmarks.
- **Strong reliance on the existence of full-rank actions.** The method can only recover observation distributions for actions whose transition matrices are full-rank, and the final model is only defined up to partitions induced by these actions. If no action is full-rank (e.g., all transitions are deterministic or singular), the algorithm cannot proceed. While the paper argues that failure-prone actions are full-rank, it does not characterize how common or generalizable this condition is across POMDP domains of interest.
- **Planning performance is not clearly superior to PSRs.** Figure 3 shows that the total reward obtained by the learned POMDP model is essentially the same as that obtained by the PSR baseline, across all tested domains. The paper’s main claimed advantage is the ability to specify rewards after learning, but the planning results themselves do not demonstrate a performance improvement. The reward-specification experiments (Figure 4) do show an advantage for Ours_state in the noisy domain, but only after many interactions (10^6–10^7). The practical benefit may be limited to settings where the planner can exploit explicit state-reward mappings, which is a narrow use case.

### Minor

- **The uniform random exploration policy is restrictive.** The theory and estimation of the Hankel matrix assume a memoryless policy (here uniform). In many applications, random exploration may be inefficient or infeasible (e.g., safety constraints). The paper does not discuss how to adapt the method to different exploration strategies or to off-policy data.
- **Hyperparameter sensitivity.** The algorithm requires choosing thresholds for SVD truncation, the length of histories/tests used to form the Hankel matrix, and the number of random weights for joint diagonalization. The paper does not provide guidance on how to set these parameters robustly, nor does it analyze sensitivity in the experiments.
- **Comparison baseline is limited.** The only non-spectral baseline is EM, which is known to suffer from local optima. A comparison to a more recent spectral method (e.g., Balle et al.’s spectral learning of weighted automata) or to a deep recurrent model (e.g., a state-space model) would provide a more complete picture of the method’s strengths.

## Nice-to-Haves

- A sample complexity or PAC-style bound for the learned parameters would significantly strengthen the theoretical contribution.
- An experiment on a moderately larger POMDP (e.g., 8–10 states) would help assess scalability.
- A discussion of how to handle actions that are not full-rank (e.g., using only a subset of actions for observation recovery) would broaden applicability.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Add a small-scale scalability experiment (e.g., on a 6- or 8-state version of Sense-Float-Reset) with the same algorithm to show the trend in model error and computational cost as state count increases.
- Provide a more detailed analysis of the finite-sample error of the joint diagonalization step (e.g., how the error in the estimated Hankel matrix propagates to the similarity transform estimate).
- Discuss the possibility of using importance weighting to relax the uniform exploration assumption, or cite existing work on off-policy spectral learning.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>