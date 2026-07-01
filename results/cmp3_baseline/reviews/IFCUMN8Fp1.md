## Summary

This paper addresses the problem of learning the parameters (transition and observation matrices) of a discrete POMDP from action-observation sequences, without knowledge of the state space. The authors connect Predictive State Representations (PSRs) with tensor decomposition methods to recover the similarity transform that maps the PSR’s learned representation back to the original POMDP parameters. The key theoretical result is that the method recovers the POMDP up to a partition of states that share the same observation distributions across all full-rank actions. Experiments on small POMDPs show that the learned models achieve planning performance comparable to PSRs and ground truth, and that explicit likelihoods enable reward specification that is not possible with black-box PSRs.

## Strengths

- **Novel connection between PSRs and tensor methods.** The paper provides a principled way to recover the similarity transform that maps a linear PSR to the original POMDP basis, leveraging joint diagonalization across all full-rank actions. This is a clean theoretical contribution that bridges two previously separate lines of work.
- **Clear theoretical result (Theorem 1).** The theorem precisely characterizes what can be recovered (up to the full-rank observability partition) and is supported by a proof sketch and appendix. The result is honest about the limitations (partition-level recovery when states share observation distributions).
- **Demonstrated advantage of explicit likelihoods.** The reward-specification experiments (Figure 4) convincingly show that having explicit transition and observation models enables the planner to be directed toward states with ambiguous observations, which is not possible with a black-box PSR. This is a practical benefit that motivates the approach.
- **Sound experimental methodology.** The experiments compare against PSRs, EM, and ground truth across multiple domains, with error bars over 100 seeds. The planning evaluation uses a standard solver (PO-UCT) with appropriate roll-out strategies for each model type.

## Weaknesses

### Fatal
None.

### Major
- **Requirement of full-rank actions is restrictive.** The method can only recover observation distributions for actions whose transition matrices are full-rank. While the paper argues that many robotic actions can be modeled as full-rank (e.g., actions with failure probabilities), this excludes a significant class of POMDPs where all actions have singular transitions. The paper does not discuss how to handle domains with no full-rank actions.
- **Experiments are limited to very small POMDPs (2–4 states).** The method’s scalability to larger state spaces is not addressed. The Hankel matrix construction and SVD become computationally expensive as the number of histories/tests grows, and the joint diagonalization step may suffer from numerical issues in higher dimensions. Without evidence on larger problems, the practical impact is unclear.
- **Weak baseline comparison.** The only non-spectral baseline is EM, which is known to converge to local optima and performs poorly. A more informative comparison would include a spectral method with EM refinement, or a recent deep recurrent model (e.g., a recurrent state-space model). The paper’s claims about the advantage of explicit likelihoods would be stronger if compared against a method that also learns explicit parameters (e.g., EM with correct state count).
- **No finite-sample guarantees.** The theoretical result (Theorem 1) is asymptotic (infinite data). The paper mentions finite-sample parameters in Appendix B.1 but provides no rigorous sample complexity bound or convergence rate. This limits the theoretical contribution to a consistency result.

### Minor
- **Dense presentation.** Sections 3 and 4 are notation-heavy and could benefit from more intuitive explanations or illustrative examples. The connection between the Hankel matrix factorization and the similarity transform is not immediately accessible.
- **Figure quality.** The figures (especially Figure 3) are small and the text is hard to read. The captions are long and contain redundant information.
- **Missing discussion of computational complexity.** The paper does not analyze the time or memory cost of constructing the Hankel matrix, performing SVD, or computing the joint diagonalization. This is relevant for assessing scalability.

### Trivial
None.

## Nice-to-Haves

- An ablation study on the effect of the random weights in the joint diagonalization (Lemma 1) would strengthen the empirical validation.
- A discussion on how to automatically determine the threshold for singular value truncation (to estimate the number of states) would be useful for practitioners.
- A comparison to a method that uses spectral initialization followed by EM (e.g., the approach of Hsu et al. 2012) would provide a stronger baseline.

## Novel Insights

The paper’s key insight is that the similarity transform between a PSR and the original POMDP can be estimated by jointly diagonalizing observation matrices derived from full-rank actions, and that this recovers the POMDP up to a natural partition of states that are observationally equivalent under all full-rank actions. This elegantly explains why some POMDPs are learnable up to state partitions rather than individual states, and provides a practical algorithm for doing so. The connection to the classic result of Carlyle & Paz (1971) is well leveraged.

## Suggestions

- Provide a finite-sample analysis or at least a discussion of sample complexity, even if heuristic. This would significantly strengthen the theoretical contribution.
- Test the method on a larger POMDP (e.g., 10–20 states) to demonstrate scalability, or discuss the expected computational bottlenecks and how they might be addressed (e.g., via matrix completion or randomized SVD).
- Compare against a stronger baseline, such as a spectral method with EM refinement, to better isolate the benefits of the proposed similarity transform recovery.

## Score and Decision

MY FINAL SCORE: 6.0<score>6.0</score>
MY FINAL DECISION: Accept<decision>Accept</decision>