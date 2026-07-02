## Summary

This paper revisits the ranking stage of recommender systems and challenges the prevailing two-stage (Multi-)Generator–Evaluator paradigm. The authors prove theoretically that a single, sufficiently large generator-only model can achieve strictly smaller approximation error to the optimal ranking policy than any finite mixture of generators with an evaluator, and that this error decreases with model size (scaling law). They then derive a group-relative optimization principle that uses a reward model trained on real user feedback to construct a reference policy, enabling effective training of a large generator-only ranker. The proposed framework, **GoalRank**, is validated through extensive offline experiments on public benchmarks and large-scale online A/B tests, showing consistent improvements over state-of-the-art baselines and clear scaling behavior.

## Strengths

- **Theoretical foundation.** The paper provides a formal proof (Theorem 1) that a single larger generator can strictly outperform any finite multi-generator–evaluator system in terms of KL approximation error to the optimal policy, and that the error vanishes as model size grows. This gives a principled justification for moving away from the two-stage paradigm.
- **Novel optimization principle.** The group-relative optimization (Section 3.2) is a clean and practical idea: using a reward model to construct a reference policy via group-level normalization, then training the generator to minimize KL divergence to that reference. The derivation from an evidence upper bound is well motivated.
- **Extensive and convincing experiments.** The paper includes offline experiments on three datasets (ML-1M, Amazon-Book, Industry) with strong improvements (e.g., +17% H@6 on ML-1M, +25% H@6 on Industry), scaling experiments showing clear scaling laws for GoalRank but not for baselines, ablation studies on group size and reward model bias, and large-scale online A/B tests on a platform with over half a billion daily active users. The online results show statistically significant gains across all business metrics.
- **Reproducibility and practical relevance.** The authors commit to releasing code, and the online deployment demonstrates that the method works in a real industrial setting. The ablation on reward model bias (Table 3) shows robustness, which is important for practical adoption.

## Weaknesses

### Fatal
None.

### Major
- **Theoretical comparison is somewhat asymmetric.** Theorem 1 compares a *larger* single generator (width ≥ kα + n) against a mixture of *smaller* generators (width ≤ α). While the result is valid, it is not surprising that a larger model can approximate the optimal policy better than a constrained mixture. The key insight is that the two-stage structure itself imposes a limitation that can be overcome by scaling a single model, but the paper does not compare against a single generator of the same total parameter count as the multi-generator system. A more informative comparison would be: given a fixed total parameter budget, does a single large generator outperform a mixture of smaller ones? The paper’s scaling experiments (Figure 3) partially address this by showing that GoalRank scales better than MG-E, but the MG-E baseline increases the number of generators rather than the size of each generator, so the comparison is not directly on total parameters.
- **Group construction relies on auxiliary policies.** The training process uses an auxiliary set of ranking policies (including heuristic methods and lightweight neural models) to construct the list groups $\mathcal{B}_u$. While this is a practical solution, it introduces additional complexity and dependencies. The paper does not fully analyze how the choice of auxiliary policies affects performance, nor does it compare against a variant that constructs groups purely from the generator itself (e.g., via stochastic sampling or beam search). This weakens the claim that GoalRank is a pure “generator-only” framework, as the training signal depends on external policies.
- **Reward model details are deferred.** The reward model $\hat{r}$ is a critical component, but its training procedure, architecture, and data are only briefly mentioned (with reference to Appendix B, which is not available in the main text). The ablation on bias (Table 3) is helpful, but without understanding the reward model’s quality and potential biases, it is hard to assess how generalizable the method is to other domains or feedback signals.

### Minor
- **Offline evaluation setup is somewhat artificial.** The ground truth is defined as the last six interactions in a user’s history, and the task is to predict that order. This does not fully capture the true ranking objective (maximizing future user engagement), though the online A/B tests mitigate this concern.
- **Improvements on Amazon-Book are modest.** While still positive, the gains on Amazon-Book (e.g., +4.07% H@6, +3.32% N@6) are much smaller than on ML-1M and Industry, suggesting that the method may be less effective in certain settings. The paper does not discuss why.

### Trivial
- The acronym “GoalRank” is a bit forced from “Group-Relative Optimization for a Large Ranker,” but this is not a substantive issue.

## Nice-to-Haves
- A comparison against a single generator of equivalent total parameter count to the multi-generator system would strengthen the theoretical claim.
- An analysis of how the choice of auxiliary policies in group construction affects final performance, or a variant that uses only the generator’s own outputs (e.g., via diverse beam search) to form groups.
- More details on the reward model’s architecture and training in the main paper, or a sensitivity analysis to different reward model designs.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the two-stage Generator–Evaluator paradigm, while intuitive, imposes a structural bottleneck: the evaluator can only select among a finite set of candidate lists, and the generator’s capacity is limited. By scaling a single generator and training it with a group-relative objective derived from a reward model, one can effectively bypass this bottleneck and achieve better approximation to the optimal policy. This suggests that the community may have been over-relying on multi-stage pipelines when a sufficiently large end-to-end model could be more effective.

## Suggestions
- In the theoretical analysis, consider comparing against a single generator with the same total parameter budget as the multi-generator system, to make the advantage more concrete.
- Provide an ablation where groups are constructed without auxiliary policies (e.g., using stochastic sampling from the generator itself) to demonstrate that the method can be truly generator-only.
- Include a brief description of the reward model in the main paper (e.g., architecture, training data, loss function) to improve self-containedness.

## Score and Decision

**Score:** 8  
**Decision:** Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>