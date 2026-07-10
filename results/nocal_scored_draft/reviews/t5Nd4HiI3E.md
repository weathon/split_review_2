Now let me write the final consolidated review.

## Summary

This paper studies preference optimization for Large Reasoning Models (LRMs), where the statistically correct marginal objective (summing over all reasoning traces) is intractable. The authors identify that the standard single-trace Monte Carlo approximation introduces high gradient variance from trace sampling. They propose BVPO (Bias–Variance Optimized Preference Optimization), which mixes a high-variance trace-based gradient estimator \(g_t\) with a low-variance "empty-trace" gradient estimator \(g_e\) (obtained by disabling trace generation) via convex combination. The paper derives an MSE-optimal mixing coefficient, proves variance reduction and tighter SGD convergence bounds, and shows consistent empirical wins over DPO and SimPO across three LRM scales on Arena-Hard, AlpacaEval 2, and math reasoning benchmarks.

## Strengths

- **Timely and well-motivated problem.** The paper identifies a genuine gap: aligning LRMs that produce long reasoning traces with human preferences is largely unexplored. The trace-answer factorization and the intractability of the marginal \(\pi_\theta(y|x)=\sum_r\pi_\theta(r,y|x)\) are clearly laid out in Section 3.2, and the source of trace-induced gradient variance is concretely explained.

- **Clean, internally consistent theoretical framework.** The paper proves that the combined estimator reduces conditional variance from trace sampling (Theorem 1), derives the MSE-optimal mixing coefficient with a dominance guarantee (\(\text{MSE}(g_c(\alpha^*)) \leq \min\{\text{MSE}(g_t),\text{MSE}(g_e)\}\), Theorem 2), and connects this statistical optimality to tighter SGD convergence bounds (Theorems 3–4). The theory is mathematically sound under the stated assumptions.

- **Consistent empirical wins in the fairest comparison setting.** In Thinking mode (the fair comparison where all methods use traces), BVPO improves over the best baseline on Arena-Hard by +5.1 (7B), +3.6 (1.5B), and +2.3 (8B) points, and on AlpacaEval 2 LC win rate by +5.1, +1.4, and +1.6 points respectively. These are non-trivial, consistent gains across all three model scales. Math reasoning improvements (Table 2) are modest but also consistently positive.

## Weaknesses

### Major

- **NoThinking comparisons are not a fair test of the gradient estimator.** BVPO is trained on a mixture of trace-based data (\(\mathcal{D}_t\)) and empty-trace data (\(\mathcal{D}_e\)), while the DPO and SimPO baselines are trained only on trace-based data. When evaluated in NoThinking mode (traces suppressed), BVPO has a built-in training-distribution advantage — it was explicitly trained on empty-trace data, while the baselines were not. The abstract and introduction prominently highlight gains of "up to 6.8 points on Arena-Hard" without distinguishing that this figure comes from the NoThinking comparison. The Thinking mode comparisons are fair, and the gains there are real but more modest (+2.3 to +5.1 on Arena-Hard). The paper should present Thinking mode as the primary comparison and clearly caveat the NoThinking results as reflecting a different property (training on empty-trace data benefits non-reasoning deployment).

### Minor

- **The \(\alpha\) value used in experiments is not stated, and the theoretical optimal \(\alpha\) is not directly computable.** The main text's experiment section (Section 5.1) does not report what mixing coefficient \(\alpha\) was used or how it was selected. Theorem 2 derives a closed-form optimal \(\alpha\), but every term in that formula depends on the true marginal gradient \(\mu = \nabla_\theta \mathcal{L}_m(\theta)\), which is itself intractable. The paper does not clarify whether \(\alpha\) was tuned as a hyperparameter, set heuristically, or approximated from the closed form — creating a gap between the theoretical optimality claims and the empirical implementation. (Experimental details may reside in the stripped appendix.)

- **No variance or uncertainty reporting despite variance reduction being the paper's central motivation.** The paper reports no standard deviations, confidence intervals, or results from multiple random seeds. For a paper whose core claim is about reducing gradient variance, this is a conspicuous gap — the experiments demonstrate better final metrics but provide no direct evidence of reduced training variance.

- **Missing ablation isolating the effect of mixing.** The paper does not report results for \(\alpha=0\) (pure empty-trace estimator) or \(\alpha=1\) (pure trace-based estimator, using the trace-based loss from Section 3.2). Without these, it is difficult to attribute BVPO's gains specifically to the mixing of the two estimators rather than to the empty-trace training data alone or to some interaction.

- **The empty-trace estimator can have substantial bias.** While the paper acknowledges \(g_e\) has "potentially higher bias," the magnitude can be large — e.g., the R1-0528-Qwen3-8B base model drops from 48.7 to 37.5 on AlpacaEval 2 when traces are disabled (Table 1). This raises the question of how much MSE improvement the mixing provides over \(g_t\) alone, which is not quantified.

### Trivial

None.

## Nice-to-Haves

- Report the \(\alpha\) value(s) used and describe how they were selected (tuned, heuristic, or approximated from Theorem 2).
- Include variance-relevant evidence: training loss curves, gradient norm variance across batches, or results from multiple seeds.
- Add ablations for \(\alpha=0\) and \(\alpha=1\) to isolate the effect of mixing.
- Clarify in the abstract and introduction that the headline "up to 6.8 points on Arena-Hard" is from the NoThinking setting where the comparison is not apples-to-apples.

## Removed Points

These points are flagged to be removed; treat them with caution.
- **Issue about the "no systematic treatment" claim being overstated:** The paper qualifies this claim ("to the best of our knowledge") and cites relevant technical reports. This is standard framing, not a material overclaim.
- **Section-by-section comments calling the empty-trace trick "trivial" or the convex combination "simple":** Method simplicity is a potential virtue, and these are subjective aesthetic judgments, not substantive weaknesses.
- **Characterization of the \(\alpha\) gap as "structural/fatal":** The theoretical optimal-\(\alpha\) formula is mathematically valid under its stated assumptions. That it depends on unobservable quantities is a limitation common to many theoretical optimality results; the experimental \(\alpha\) choice could be addressed in the (stripped) appendix. This is a Minor reporting gap, not a fatal flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Restructure the presentation of results to make Thinking mode the primary comparison and clearly separate NoThinking results as measuring the benefit of training on empty-trace data for non-reasoning deployment scenarios.
- Report the \(\alpha\) value and selection method used in experiments to bridge the theory–practice gap.
- Add variance-related metrics (e.g., training loss variance across batches or multiple-seed results) to directly support the core claim of training stabilization.
- Include ablations for the individual components (\(\alpha=0\) empty-trace-only; \(\alpha=1\) trace-only with the Section 3.2 loss) to isolate the mixing effect.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>