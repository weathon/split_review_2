## Summary

This paper introduces CANON (Conditional advaNtage estimatiON), a method for reinforcement learning with verifiable rewards (RLVR) in large reasoning models. CANON regroups sampled responses based on a target metric (e.g., entropy or response length) into two groups, then computes inter-group and intra-group advantages to amplify the impact of the metric without presuming its direction (higher-is-better or lower-is-better). The method is evaluated across three LLMs on math reasoning and complex logic reasoning tasks, showing improvements over prior advantage estimation methods like DR.GRPO, and achieving better Pareto frontiers in the performance-efficiency trade-off when applied to response length.

## Strengths

- **Novel and well-motivated approach**: The core idea of conditional regrouping to avoid hand-crafted directional priors is elegant. The paper clearly identifies a limitation of existing reward/advantage shaping methods (brittle hyper-parameter tuning, biased priors) and proposes a principled alternative that lets the data determine which metric trend is beneficial.

- **Strong empirical results across multiple models and tasks**: CANON demonstrates consistent improvements over strong baselines (DR.GRPO, RLOO, ReMax, etc.) on three different LLMs (Qwen2.5-Math-7B, Qwen2.5-Math-1.5B, Llama3.1-8B) across six math reasoning benchmarks and three complex logic reasoning subsets. The gains are non-trivial (e.g., 1.9 points on math, 5.2 points on the most challenging logic subset).

- **Theoretical grounding**: The paper provides theoretical analysis (Theorem 1 and 2) showing that CANON amplifies the advantage attributable to the grouping metric without amplifying independent factors, and that DR.GRPO is a special case of CANON when μ=0.5. This connects the proposed method to existing work and clarifies its behavior.

- **Practical impact on efficiency**: The weighted condition variant (CANON-Eff) achieves a superior Pareto frontier in the performance-token cost trade-off, with substantial token reductions (e.g., 45.5% at the same performance level) compared to baselines. This is a practically valuable contribution for deploying reasoning models under budget constraints.

## Weaknesses

### Major

- **Limited analysis of metric choice and sensitivity**: The paper focuses on entropy and response length as grouping metrics, but does not systematically explore how the choice of metric affects performance. Are there metrics that would hurt performance? How sensitive is CANON to the specific metric chosen? The paper claims CANON "amplifies the impact of the target metric without presuming its direction," but the metric itself is still a human choice that encodes a prior. A discussion of when a metric might be inappropriate would strengthen the paper.

- **Scheduling strategies are somewhat ad-hoc**: The CANON-Dynamic results rely on scheduling μ during training (e.g., First-Inter-Later-Intra, cosine annealing). While the paper shows these work well, the choice of scheduling strategy appears to be model-specific (different strategies for different model sizes). The paper does not provide clear guidance on how to select a scheduling strategy for a new model or task, which limits reproducibility and practical applicability.

- **The theoretical results are somewhat narrow**: Theorem 1 only establishes the condition for amplification when groups are equal-sized, and Theorem 2 shows independence for independent conditions. These are useful but do not fully characterize when CANON will outperform GRPO/DR.GRPO. The paper would benefit from a more complete theoretical understanding of the conditions under which the regrouping provides a better signal.

### Minor

- **The ablation on μ is limited**: Figure 5 shows entropy trends for different μ values, but the paper does not provide a systematic ablation of μ on final task performance. The analysis focuses on training dynamics rather than final accuracy, making it hard to assess the sensitivity of the method to this hyperparameter.

- **The comparison to "Direct Numerical Amplification" (Table 4) is somewhat weak**: The baseline of simply scaling the advantage by 2 is a strawman. A more informative comparison would be to other methods that also aim to amplify specific signals without directional priors, if any exist.

### Trivial

- The paper uses "DR.GRPO" as a baseline but DR.GRPO is itself a variant of GRPO. The relationship between these methods could be clarified earlier in the paper.

## Nice-to-Haves

- An analysis of what happens when the grouping metric is completely uncorrelated with task performance (e.g., a random metric). This would help validate the claim that CANON does not introduce harmful bias.
- A discussion of computational overhead: does the regrouping and dual advantage computation add significant cost compared to standard GRPO?
- A more detailed analysis of the "rethinking gain" metric used in Figures 2 and 6, including how it is computed.

## Novel Insights

The key insight of this paper is that by regrouping responses based on a metric and computing both inter-group and intra-group advantages, one can amplify the influence of that metric on policy updates without committing to a directional prior (higher-is-better or lower-is-better). This is a clever way to incorporate human knowledge about which metrics are relevant (e.g., entropy, length) while letting the data determine whether higher or lower values of that metric are beneficial. The finding that DR.GRPO is a special case of CANON with μ=0.5 provides a unifying perspective on existing advantage estimation methods. The observation that inter-group advantage favors exploitation (low entropy, high certainty) while intra-group advantage favors exploration (high entropy, more reflection) is a useful characterization that explains the scheduling results.

## Suggestions

1. Add a systematic ablation study of the μ hyperparameter on final task performance (not just training dynamics) to help practitioners understand sensitivity.
2. Provide clearer guidance on how to select a scheduling strategy for CANON-Dynamic, or propose a more principled adaptive scheduling method.
3. Discuss the limitations of the metric choice and when CANON might fail (e.g., if the metric is irrelevant or harmful).
4. Include an analysis of computational overhead compared to standard GRPO.

## Score and Decision

The paper presents a novel, well-motivated, and empirically strong method for advantage estimation in RLVR. The core idea is elegant, the experiments are thorough (three models, multiple tasks, multiple baselines), and the results are convincing. The theoretical analysis, while not exhaustive, provides useful grounding. The main weaknesses are the somewhat ad-hoc scheduling strategies and limited analysis of metric sensitivity, but these do not invalidate the core contribution. The paper is likely to be of significant interest to the ICLR community working on LLM reasoning and RL for language models.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>