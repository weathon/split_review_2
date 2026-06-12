## Summary

This paper introduces CANON (Conditional Advantage Estimation), a method for RLVR in large reasoning models that regroups sampled responses into two groups based on a target metric (e.g., entropy or response length), then computes inter-group advantages (identifying which metric trend leads to better performance) and intra-group advantages (selecting better responses within each trend). The key insight is that this approach amplifies the influence of a given metric without presupposing a directional preference (higher-is-better vs. lower-is-better), with DR.GRPO shown as a special case at μ=0.5. Experiments across three models, six math benchmarks, and three logic tasks demonstrate consistent improvements over prior methods.

## Strengths

- **Elegant formulation with theoretical grounding**: The paper cleanly shows that DR.GRPO is a special case of CANON (Eq. 7), and Theorems 1–2 establish that equal group sizes maximize the advantage signal (Theorem 1) and that CANON selectively amplifies only the target metric without amplifying independent confounders (Theorem 2). This provides principled justification rather than ad-hoc engineering.

- **Comprehensive and consistent experimental evidence**: CANON-Dynamic outperforms DR.GRPO across all three model architectures (Qwen2.5-Math-7B, Qwen2.5-Math-1.5B, Llama3.1-8B) and both task types (math and high-complexity logic reasoning). On entropy-based grouping, CANON-Inter achieves 1.9 points higher on math tasks while CANON-Intra achieves 5.2 points higher on the most challenging logic subset. These consistent trends across diverse settings strengthen confidence in the method.

- **Strong efficiency results with Pareto frontier analysis**: CANON-Eff achieves 2.63× higher performance at low token budgets and 45.5% token reduction at the same performance level compared to DR.GRPO. The systematic Pareto frontier analysis (Figure 4c) across multiple α values and baseline hyperparameters demonstrates robust stability, unlike Length Reward(+) which collapses from 54.8 to 22.5 with a small coefficient change.

- **Insightful analysis of different advantage roles**: The training dynamics (Figure 2) clearly show that CANON-Inter drives fast convergence and entropy reduction (exploitation), while CANON-Intra promotes exploration and eventually achieves positive rethinking gains (Figure 2f). This provides genuine mechanistic understanding of why scheduling between the two is beneficial.

## Weaknesses

### Fatal

None.

### Major

- **Scheduling strategy selection is non-trivial and undermines the "avoiding handcrafted priors" claim**: The paper tries four scheduling strategies and selects the best one per model (Section 5.2), with different models requiring different strategies (cosine annealing for Qwen-7B and Llama-8B vs. accuracy-based for Qwen-1.5B). This requires tuning schedule type, cosine parameters, and min/max μ values—arguably comparable hyperparameter burden to the reward shaping methods the paper critiques. The paper partially acknowledges this but doesn't provide systematic guidance for practitioners.

- **CANON-Dynamic performance on math tasks is not consistently better than CANON-Inter**: Table 2 shows that for Qwen2.5-Math-7B, CANON-Dynamic (56.7 on math) underperforms CANON-Inter (57.6 from Table 1), and for Llama-8B, CANON-Dynamic (22.6) is slightly worse than DR.GRPO (22.6, same). The claim of "superior and more comprehensive performance" is partially undermined by these cases where the scheduling introduces trade-offs rather than pure gains.

### Minor

- **Only two metrics explored**: The framework is general and could be applied to other signals (reasoning step count, self-consistency, tool usage). Demonstrating at least one non-obvious metric would strengthen the generality claim.

- **The radar chart in Figure 3 appears to use normalized/schematic values** rather than the actual performance numbers from Table 2, which could mislead readers about the magnitude of improvements.

- **Different training data for Llama3.1-8B** (35k samples from a different mixture vs. 45k from OpenR1-Math-220k) makes cross-model comparisons less clean, though the authors acknowledge this is due to capability differences.

### Trivial

None.

## Nice-to-Haves

- A comparison of CANON with more sophisticated advantage estimation methods from the broader RL literature (e.g., methods that use learned baselines or adaptive normalization) would contextualize the contribution more broadly.
- Analysis of how CANON interacts with different group sizes G (the paper uses G=16 throughout) would provide practical guidance.
- Ablation on the number of groups (the paper uses exactly 2) would clarify whether finer-grained splitting could help.

## Novel Insights

The paper's key novel insight—that advantage estimation can be decomposed into inter-group and intra-group components, where the inter-group component naturally discovers the beneficial direction of a metric without human-specified directional priors—is genuinely valuable. The observation that inter-group advantage favors exploitation (fast convergence, entropy reduction) while intra-group advantage promotes exploration (higher entropy, positive rethinking gains), and that both are needed at different training stages, provides a principled framework for understanding the exploration-exploitation tradeoff in RLVR. The result that DR.GRPO is a uniform mixture of these two advantages (Eq. 7) offers a new lens for understanding existing methods.

## Suggestions

- Provide practical guidelines or automatic mechanisms for scheduling strategy selection rather than per-model tuning, e.g., a validation-based adaptive scheduler or rules of thumb based on model capability and task difficulty.
- Include ablations on the number of groups (beyond binary splitting) to test whether finer-grained metric-aware regrouping provides additional benefits.
- Validate on a broader set of base models (e.g., larger models or non-math-tuned models) to assess whether the entropy/length insights transfer across model families and scales.

## Score and Decision

The paper presents a clean, theoretically motivated method that consistently improves over DR.GRPO across diverse settings. The core CANON formulation is elegant, and the inter/intra advantage decomposition offers genuine insight into RLVR training dynamics. The main concern is the practical complexity of CANON-Dynamic's scheduling, which somewhat undermines the simplicity argument, and the inconsistent gains of the dynamic version over fixed-μ variants. However, even the fixed-μ CANON variants show clear improvements, and the efficiency results are compelling.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept