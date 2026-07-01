## Summary

This paper addresses the problem of learning the parameters of a discrete POMDP—transition and observation matrices—from action-observation sequences when the state space is unknown. The authors connect Predictive State Representation (PSR) learning with tensor decomposition methods to recover a similarity transform that maps the PSR parameters back to the original POMDP basis. The recovery is guaranteed up to a *full-rank observability partition*: states that share identical observation distributions across all full-rank actions are grouped together. The method is evaluated on several small POMDP benchmarks and shows convergence to correct partition-level parameters, competitive planning performance, and the ability to leverage explicit observation/transition likelihoods for reward specification after learning.

## Strengths

- **Addresses a significant and well-motivated problem.** Learning POMDP parameters from raw interaction without state supervision is a core challenge for autonomous agents operating in partially observable environments. The motivation from robotics (e.g., learning hidden locking mechanisms) is clearly stated and relevant.
- **Novel technical synthesis.** The paper bridges two previously separate lines of work—spectral learning of PSRs and tensor decomposition methods for POMDPs—to relax the distinct-observation-per-state assumption required by prior tensor methods. The theoretical result (Theorem 1) formally characterizes what can be recovered up to a full-rank observability partition, which is a clean and useful characterization.
- **Theoretical grounding.** The connection to the classical Carlyle & Paz (1971) result and the new Theorem 1 provide solid foundations. Lemma 1 on random weighted sums for joint diagonalization is appropriately stated and used.
- **Experimental validation with careful comparisons.** Experiments on multiple domains (Tiger, T-Maze, Sense-Float-Reset) show the method converges to correct observation and transition likelihoods as data increases, outperforming EM (which gets stuck in local minima) and matching PSR performance in planning. The reward specification experiment (Figure 4) convincingly demonstrates the practical advantage of having explicit state-level likelihoods: when observation-based reward assignment fails due to ambiguous observations, state-based reward assignment (only possible because the model provides partition-level observation probabilities) succeeds.

## Weaknesses

### Fatal
None.

### Major
1. **Strong reliance on the existence of full-rank actions.** The method critically requires at least one action whose transition matrix is full-rank. The paper gives a plausible justification (action failure models in robotics) and discusses that the reset action in Sense-Float-Reset is singular and thus not used. However, this assumption excludes many real-world POMDPs. For example, any POMDP where all actions are deterministic (permutation matrices) would have rank-deficient transition matrices (typically rank < number of states). The paper acknowledges this in Section 4.1.1 but does not provide any relaxation or fallback, making the method inapplicable to a large class of environments.

2. **Recovery is only up to a (possibly coarse) partition.** Theorem 1 states that the algorithm recovers the model up to the full-rank observability partition. When the partition is nontrivial (multiple states per partition), the learned model only describes transitions *between partitions*, not between individual states. The paper argues this is still useful for planning, but the experiments only test domains where the partition is either trivial (all states distinguishable) or very fine (e.g., Sense-Float-Reset has 2 partitions: the two leftmost states vs. the rest). In domains with large partitions, the loss of state-level resolution could severely degrade planning performance, especially for tasks that depend on fine-grained state distinctions. This limitation should be discussed more explicitly.

3. **Experimental evaluation is limited to small-scale domains.** All tested POMDPs have at most 5 states. The computational cost of constructing and factorizing the Hankel matrix grows quickly with state space size and history length. While the paper mentions future work on scaling, the lack of any experiment on moderately larger domains (e.g., 10–20 states) leaves open the question of whether the method is practical beyond toy problems. The Hankel matrix is built from action-observation subsequences, and with limited data, its estimation quality degrades; the paper does not characterize this trade-off.

4. **Reliance on a uniform random exploration policy and ergodicity.** The method assumes data is collected under a memoryless uniform random policy and that the induced Markov chain is ergodic. In many realistic settings, a uniform random policy may be inefficient or infeasible for large action spaces. The paper mentions a passive sensing action to break periodicity, but this is not always available. The method does not address how to handle data collected under a different policy.

5. **The comparison with EM is somewhat limited.** EM is evaluated with a single initialization (number of states determined by SVD truncation, standard EM iterations). It is well known that EM for HMMs/POMDPs is highly sensitive to initialization. The paper does not attempt multiple random restarts or informed initialization strategies for EM, which might make the comparison more balanced. While the authors are not obligated to make EM perform well, the current presentation risks overselling the spectral method by comparing against a relatively weak baseline.

### Minor
- The concept of the *final vector* $m_\infty$ and its role in recovering partition-level likelihoods is explained somewhat tersely (Section 4.3). The step of multiplying by a random block-diagonal rotation matrix $R$ to avoid zeros is mentioned but not justified in detail. A more thorough explanation would improve accessibility.
- The paper uses the term "full-rank actions" to refer to actions whose transition matrices are full-rank. This could be confused with actions that have full-rank observation matrices; clarifying this early would help.
- The y-axis scaling in Figure 3 is tailored to show convergence, but some plots (e.g., Trans. matrix error for T-Maze) show negative values for some methods, which is unusual for an $L_1$ error metric (likely it is actually log-scale or something else). This is a minor labeling issue.
- The paper refers to "the final vector" but does not always use consistent notation; in Section 4.3 there is "P m_0" where it seems "m_\infty" is intended (a formatting artifact).

### Trivial
- On page 7, line "$\text{diag}(P m_0)$" should likely involve $P'$ and $m_\infty$ based on the surrounding description; this is likely a parser artifact but could confuse readers.

## Nice-to-Haves
- A discussion of sample complexity bounds (e.g., how many interaction steps are needed to estimate the Hankel matrix accurately for a given state space size) would strengthen the practical contribution.
- Experiments on a larger domain (e.g., a 10-state grid-world POMDP) would significantly increase confidence in scalability.
- An ablation study showing the effect of the number of history/test subsequences used to form the Hankel matrix on estimation quality.
- A comparison against deep recurrent model-based approaches (e.g., Dreamer, RSSM) that also learn latent dynamics, to contextualize the spectral method's data efficiency vs. expressiveness.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the similarity transform ambiguity in PSRs can be resolved up to an *aggregation* of states that are observationally indistinguishable across all full-rank actions. This clarifies a precise boundary: you get a coarsened POMDP where each "meta-state" corresponds to such an equivalence class. This is a natural and principled notion of partial identifiability in POMDP learning. The fact that this partition-level model suffices for planning (as shown in experiments) is a useful practical observation: full identifiability is not always necessary for downstream tasks.

## Suggestions
1. **Discuss the practical prevalence of full-rank actions more concretely.** Provide examples beyond the "action failure" model, or cite real-world POMDPs from robotics that satisfy this condition. If possible, offer a relaxation (e.g., using actions whose transition matrices have rank close to the number of states).
2. **Run at least one experiment on a POMDP with 10+ states** to demonstrate scalability. Even a simple chain POMDP with noisy observations would suffice.
3. **Provide a more balanced comparison with EM** by including a version with multiple random restarts (or spectral initialization for EM), to show that the spectral method is genuinely more robust, not just better than a poorly-initialized EM.
4. **Clarify the random rotation step** in Section 4.3. Why is it needed, and how is it constructed? Include a small example or pseudocode.
5. **Explicitly discuss the implications of partition-level recovery** for planning. When would a coarse partition be insufficient? Provide guidance for practitioners.

## Score and Decision

The paper makes a solid technical contribution by connecting PSRs and tensor methods to recover explicit POMDP parameters up to a well-defined partition. The theoretical characterization is clean, and the experiments on small domains support the claims. However, the strong assumptions (full-rank actions, ergodicity, uniform exploration) and the limited scale of evaluation prevent this work from being a strong accept. The method currently applies to a restricted class of POMDPs and has not been demonstrated to scale. The contribution is valuable but incremental: it improves on prior tensor methods but still inherits many of their limitations. I lean toward a borderline accept because the core idea is novel and the experiments are carefully done, but the practical impact is uncertain.

MY FINAL SCORE: 6.0
MY FINAL DECISION: Accept