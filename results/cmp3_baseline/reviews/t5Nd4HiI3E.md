## Summary

This paper studies preference optimization for Large Reasoning Models (LRMs), where the statistically correct marginal objective over reasoning traces is intractable and single-trace surrogates suffer from high gradient variance. The authors propose Bias–Variance Optimized Preference Optimization (BVPO), which mixes a high-variance trace-based gradient estimator with a low-variance empty-trace gradient estimator via convex combination. Theoretically, they prove variance reduction, MSE optimality of the mixing weight, and tighter SGD convergence bounds. Empirically, BVPO improves alignment by up to 7.8 points on AlpacaEval 2 and 6.8 points on Arena-Hard, while also improving average math reasoning performance by up to 4.0 points across six benchmarks.

## Strengths

- **Timely and important problem.** Aligning LRMs with human preferences is a critical and underexplored problem. The paper clearly identifies trace-induced gradient variance as a key bottleneck and provides a principled solution.
- **Novel and principled method.** BVPO is simple, drop-in compatible with existing preference optimization algorithms, and grounded in bias–variance theory. The idea of mixing a trace-based estimator with an empty-trace estimator to reduce variance is elegant.
- **Strong theoretical analysis.** The paper provides rigorous proofs of conditional variance reduction (Theorem 1), MSE-optimal mixing (Theorem 2), and a direct connection between MSE minimization and SGD convergence bounds (Theorems 3 and 4). This establishes a clear statistical-to-algorithmic optimality link.
- **Consistent and substantial empirical gains.** BVPO outperforms DPO and SimPO across three LRM sizes on both alignment benchmarks (Arena-Hard, AlpacaEval 2) in both Thinking and NoThinking modes. The improvements are large (up to 7.8 points) and consistent.
- **Reasoning preservation and improvement.** The paper demonstrates that alignment with general conversational data does not degrade reasoning; BVPO even improves average math reasoning performance by up to 4.0 points. This is an important practical finding.

## Weaknesses

### Major

- **Lack of detail on the practical choice of α.** The paper derives a closed-form optimal α (Theorem 2) but does not specify how α is set in the experiments. Is it tuned as a hyperparameter? Estimated from data? The practical implementation is crucial for reproducibility and for understanding whether the theoretical optimality is realized. Without this detail, the connection between theory and practice is unclear.
- **No ablation on the mixing weight α.** The paper does not study sensitivity to α, nor does it compare the empirically best α to the theoretically predicted one. Such an ablation would strengthen the paper and validate the theoretical claims.
- **No comparison with multi-trace variance reduction.** The paper motivates the problem by noting that marginalization over traces is intractable, but a natural alternative to reduce variance is to average over multiple sampled traces (e.g., Monte Carlo with K > 1). The paper does not compare BVPO against this simpler baseline, which would help isolate the benefit of the empty-trace estimator.

### Minor

- **Limited model diversity.** Experiments are conducted only on DeepSeek R1 distill models (1.5B, 7B, 8B). While these are representative open LRMs, the paper would benefit from at least one additional model family (e.g., a Qwen-based reasoning model or a different distillation) to demonstrate generality.
- **Reasoning improvement not deeply analyzed.** The paper reports that BVPO improves math reasoning, but does not analyze why. Is it due to reduced gradient variance preventing catastrophic forgetting? Or does the empty-trace loss act as a regularizer? A brief analysis or hypothesis would strengthen the narrative.
- **Potential bias from the empty-trace estimator.** The empty-trace estimator conditions on a fixed empty trace, which may be far from the model's natural distribution. While the theory accounts for bias, the paper does not empirically characterize the bias of \(g_e\) or how it changes during training.

### Trivial

- The paper uses "empty-trace" to mean disabling reasoning trace generation. The term is clear but could be more precisely defined (e.g., "no-thinking mode" as used in experiments).

## Nice-to-Haves

- An ablation study showing performance as a function of α, ideally with the theoretically optimal α marked.
- A comparison with a multi-trace baseline (e.g., averaging over 2–4 sampled traces) to contextualize the benefit of the empty-trace estimator.
- Analysis of the bias of \(g_e\) over the course of training (e.g., norm of bias vector).
- Experiments on at least one additional LRM family (e.g., a Qwen3-based reasoning model without DeepSeek distillation).

## Novel Insights

The paper's core insight is that the high variance of trace-based gradients in LRM alignment can be effectively mitigated by mixing with a low-variance, biased estimator derived from an empty trace. The theoretical contribution—showing that the MSE-optimal mixture directly tightens SGD convergence bounds—provides a principled justification for this approach that goes beyond heuristic variance reduction. The empirical finding that alignment on general conversational data can improve math reasoning is also noteworthy and suggests that variance reduction may help preserve or enhance capabilities acquired during earlier RL stages.

## Suggestions

- Clearly specify how α is chosen in the experiments (e.g., tuned on a validation set, or estimated via the closed-form formula using empirical moments). If tuned, report the range of α values considered and the final chosen value.
- Add an ablation study varying α (e.g., α ∈ {0, 0.25, 0.5, 0.75, 1.0}) on at least one model to show sensitivity and validate the theoretical optimality.
- Include a baseline that averages over multiple traces (e.g., K=4) to demonstrate that the empty-trace mixture is more effective than simple multi-sample averaging.
- Discuss the practical estimation of the optimal α: what moments are needed and how they can be approximated during training.

## Score and Decision

**Score:** 8

**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>