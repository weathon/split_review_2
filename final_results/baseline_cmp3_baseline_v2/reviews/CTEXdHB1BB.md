## Summary

This paper introduces CANON (Conditional Advantage Estimation), a reinforcement learning method for large reasoning models that regroups sampled responses based on a metric (e.g., entropy, response length) and computes inter-group and intra-group advantages. The key idea is to amplify the impact of a target metric without presupposing whether higher or lower values are beneficial, allowing the model to naturally discover which metric trends lead to better performance. Experiments on math reasoning and complex logic reasoning tasks across three LLMs show that CANON outperforms prior advantage estimation methods like GRPO and DR.GRPO, and when applied to response length, achieves a superior Pareto frontier in the performance-efficiency trade-off.

## Strengths

- **Novel and well-motivated approach**: The conditional regrouping idea is a clever way to incorporate human priors about training metrics (entropy, length) without imposing directional biases (higher-is-better or lower-is-better). This addresses a real limitation of prior reward/advantage shaping methods that require careful hyperparameter tuning.
- **Theoretical grounding**: Theorems 1 and 2 provide formal justification that CANON selectively amplifies the advantage attributable to the grouping metric while not amplifying independent factors. The connection showing DR.GRPO as a special case (μ=0.5) is elegant.
- **Comprehensive empirical evaluation**: Experiments span six math reasoning benchmarks and three complex logic reasoning subsets, across three different LLMs (Qwen2.5-Math-7B, Qwen2.5-Math-1.5B, Llama3.1-8B). The method is compared against a wide range of baselines including ReMax, REINFORCE++, RLOO, GRPO, DR.GRPO, and entropy-specific methods.
- **Practical contributions**: CANON-Eff demonstrates a clear Pareto improvement in the performance-efficiency trade-off, achieving 2.63× higher performance at low token budgets and reducing token consumption by 45.5% at the same performance level. The analysis of training dynamics (Figure 2, Figure 6) provides useful insights into how inter-group and intra-group advantages play different roles during training.

## Weaknesses

### Fatal
None.

### Major
- **Radar chart inconsistency**: Figure 3 reports numerical values (e.g., Llama-8B DR.GRPO math=22.6, logic=18.9) that do not match the corresponding entries in Table 2 (Llama-8B DR.GRPO math=22.0, logic=14.9). The radar chart values appear to be different from the main results, and the scaling is unclear. This undermines confidence in the reported comparisons and needs clarification or correction.
- **Scheduling strategies appear ad-hoc**: The paper tries multiple scheduling strategies (First-Inter-Later-Intra, Cosin-First-Inter-Later-Intra, etc.) and selects the best per model. While the motivation (inter-group early, intra-group later) is reasonable, the specific cosine annealing schedule and the model-specific selection risk overfitting to the evaluation benchmarks. The paper does not provide a principled rule for choosing the schedule a priori.

### Minor
- **Theoretical scope**: Theorem 1 shows that the inter-group advantage ratio >1 only when groups are equal-sized. The method always enforces equal groups, so this is fine, but the theorem's condition "if |C_q^+| is a constant" is somewhat opaque. The proof is in the appendix (not visible), but the main text could be clearer about the practical implications.
- **Metric choice is a hyperparameter**: The paper explores entropy and length, but does not discuss how to select the metric or whether the method is sensitive to this choice. For practitioners, guidance on metric selection would be valuable.
- **Limited statistical analysis**: The paper reports point estimates without confidence intervals or significance tests. Given the modest gains in some settings (e.g., 1.9 points on math), it would be helpful to know whether these differences are statistically reliable.

### Trivial
- The paper uses "DR.GRPO" as a baseline but DR.GRPO is itself a variant of GRPO; the relationship could be stated more clearly.

## Nice-to-Haves

- An ablation study that varies the group size (not just equal split) to empirically validate Theorem 1's prediction about amplification.
- A discussion of limitations: e.g., the method requires a meaningful metric to group by, and the scheduling introduces an additional hyperparameter (though the paper shows it can be set based on training accuracy).
- Release of the constructed 35k dataset for Llama3.1-8B to facilitate reproducibility.

## Novel Insights

Beyond the paper's own contributions, the key insight is that splitting sampled responses by a metric and computing separate baselines (inter-group vs. intra-group) naturally creates a contrastive signal that can either exploit or explore along that metric dimension without manual direction specification. This is a principled alternative to reward shaping that avoids the brittleness of hand-crafted penalties. The observation that inter-group advantage favors exploitation (lower entropy, shorter length) while intra-group advantage favors exploration (higher entropy, more reflection) is well-supported by the training dynamics and provides a clear intuition for why scheduling between them works.

## Suggestions

- Clarify the radar chart discrepancy: explain whether the values are normalized, averaged differently, or if there is an error. Ensure consistency with Table 2.
- Provide a simple rule for setting the scheduling strategy (e.g., use training accuracy as a natural schedule, as in First-Inter-Later-Intra) rather than model-specific tuning.
- Add confidence intervals or standard deviations for key results (e.g., Table 1 main entries) to assess statistical significance.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>