## Summary

The paper studies preference optimization for Large Reasoning Models (LRMs) which generate intermediate reasoning traces. Because marginalizing over all possible traces is intractable, practitioners use single-trace Monte Carlo estimates, leading to high gradient variance. The authors propose Bias–Variance Optimized Preference Optimization (BVPO), which mixes a high-variance trace-based gradient estimator with a low-variance estimator obtained by disabling trace generation (the "empty-trace" estimator). The mixing weight is chosen to minimize mean squared error relative to the true marginal gradient. The paper provides theoretical variance reduction and convergence results, and empirically shows improvements over DPO and SimPO on AlpacaEval 2 and Arena-Hard, while also preserving or enhancing math reasoning performance.

## Strengths

- **Novel and important problem.** Aligning LRMs that externalize reasoning traces is a timely and understudied challenge. The paper clearly identifies trace-induced gradient variance as a key bottleneck, which is a genuine practical issue.
- **Simple and principled approach.** The idea of combining two gradient estimators with an MSE-optimal convex combination is elegant, grounded in classic bias–variance trade-off reasoning, and easy to implement as a drop-in modification.
- **Solid empirical results across multiple models and benchmarks.** BVPO consistently outperforms DPO and SimPO in both *Thinking* and *NoThinking* modes on two alignment benchmarks, and improves or maintains reasoning on six math benchmarks. The experiments cover model sizes from 1.5B to 8B parameters.
- **Theoretical contribution connecting MSE to SGD convergence.** Theorems 3 and 4 link the statistical optimality of the mixed estimator (MSE minimization) to improved convergence bounds for SGD, providing a formal justification for why the method works.

## Weaknesses

### Fatal
None.

### Major

1. **Missing specification of how the mixing weight α is chosen in practice.** The paper derives an optimal α based on unknown expectations, but never states how α is actually set during experiments. Is it a fixed hyperparameter tuned on a validation set? Estimated online? Using a plug-in estimator? Without this detail, the claimed optimality guarantee is not realized in the reported results, and reproducibility is compromised. This is the most critical weakness.

2. **The empty-trace estimator is a heuristic with limited justification.** Computing gradients by conditioning on an empty trace (r=∅) yields a biased estimator of the marginal gradient; the paper acknowledges this but provides no analysis of when this proxy is reasonable. For example, if the model’s answer distribution changes drastically when forced to skip reasoning, the empty-trace gradient may be a poor estimator, and the optimal α might be 1 (reducing to standard trace-based DPO). A discussion of practical failure modes or a diagnostic for the validity of the empty-trace assumption would strengthen the paper.

3. **No error bars or significance tests.** All empirical results are reported as single point estimates. Given the inherent randomness in LLM training and evaluation (e.g., sampling traces, GPT‑4-based judges), it is unclear whether the reported gains are statistically significant. This is especially important for the math reasoning benchmarks where improvements are small (e.g., 1–2 points).

### Minor

- The theoretical results (Theorem 1–4) are straightforward applications of standard bias–variance decomposition and SGD convergence analysis. The novelty lies in applying these tools to the LRM alignment setting, not in the techniques themselves.
- The paper claims to be “the first systematic study of aligning LRMs,” but the related work section is brief and does not discuss whether any existing alignment work on reasoning models exists beyond technical reports. A more careful literature positioning would strengthen the novelty claim.
- The method requires constructing two separate preference datasets (with and without traces), which effectively doubles the data-collection and generation effort. While the paper calls BVPO a “drop-in” method, this additional overhead is worth noting.

### Trivial

- The notation for the empty-trace gradient \(g_e\) and its relationship to the marginal gradient could be clarified. In particular, it is not obvious that conditioning on \(r=\emptyset\) and then computing the DPO loss produces a gradient that estimates \(\nabla_\theta \mathcal{L}_m\) (with bias).

## Nice-to-Haves

- Ablation study on the mixing coefficient \(\alpha\) (e.g., \(\alpha=0,0.25,0.5,0.75,1.0\)) to show empirical sensitivity and validate that the chosen \(\alpha\) improves over both endpoints.
- Comparison to other variance-reduction techniques in RL (e.g., control variates, GAE) adapted to the LRM setting.
- Experiments on larger LRMs (e.g., 32B or 70B scale) to test scalability.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

1. **Clarify \(\alpha\) selection.** State explicitly how \(\alpha\) was chosen for each experiment (fixed value, cross-validated, estimated using sample moments, etc.). If a fixed value was used, report it and provide a sensitivity analysis. If a plug-in estimator is used, describe the procedure and whether it is evaluated on a held-out set.
2. **Add error bars or confidence intervals.** For the main alignment and reasoning results, report standard deviations across multiple runs or a bootstrapped confidence interval, or at least note the evaluation protocol (e.g., greedy decoding, number of seeds).
3. **Discuss limitations of the empty-trace proxy.** Provide a theoretical or empirical condition under which the empty-trace gradient is a sensible estimator of the marginal gradient (e.g., when reasoning traces are mostly uninformative or when the model can still produce high-quality answers without explicit traces). A concrete failure case would make the paper more complete.

## Score and Decision

**Score:** 6

**Decision:** Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>