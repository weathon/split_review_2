## Summary

This paper introduces R-HORIZON, a method for constructing long-horizon reasoning tasks by composing multiple single-hop problems with explicit arithmetic dependencies. The authors build a benchmark spanning mathematics, code, and agent tasks, evaluate 26 large reasoning models, and find substantial performance degradation as reasoning horizon increases. They further use R-HORIZON to create training data for reinforcement learning with verified rewards, showing that training on composed problems improves performance on both multi-horizon and standard single-problem benchmarks while promoting more efficient reasoning.

## Strengths

*   **Timely and important problem.** The paper identifies a genuine gap in current evaluation and training paradigms for LRMs: models are tested on isolated problems, but real-world tasks often require sequential interdependent reasoning. Addressing this gap is of clear value to the community.
*   **Comprehensive evaluation.** The benchmark covers 6 diverse datasets (math: MATH500, AIME, AMC; code: LiveCodeBench; agent: WebShaper) and evaluates 26 models across various scales and families. This large-scale empirical study provides a reliable picture of current model limitations.
*   **Insightful analysis.** Beyond accuracy numbers, the paper analyzes error types, effective reasoning length, reflection patterns, and thinking budget allocation. These analyses reveal specific failure modes (e.g., localized reflection, limited reasoning boundaries, uneven token allocation) that go beyond simple performance reporting and offer actionable insights.
*   **Demonstrated practical benefit.** The RLVR experiments show that training with R-HORIZON composed data improves performance on both composed tasks (e.g., +17.4 on AIME24 n=2) and standard benchmarks (+7.5 on AIME24), while also reducing overthinking and improving token budget allocation. This shows the method's utility for training better LRMs.
*   **Scalable and low-cost approach.** The query composition method is simple, does not require human annotation, and can be applied to existing datasets, making it easy for others to adopt.

## Weaknesses

### Fatal
None.

### Major
1.  **Limited methodological novelty.** The core idea of concatenating problems with arithmetic dependencies is straightforward and shares conceptual similarity with prior work (NEST, GSM-Infinite, as cited by the authors). The paper's primary contributions are empirical: the comprehensive benchmark, evaluation, and RL training findings. While these are valuable, the method itself offers little new technical insight, which tempers the overall originality.
2.  **Expected accuracy metric is flawed.** Equation (4) defines expected accuracy as the product of individual pass rates, implicitly assuming independence of sub-problem correctness. However, the composed problems have explicit dependencies, so this product is not a theoretically sound expected accuracy; it is merely a rough heuristic. The "gap" shown in Figure 1 conflates the effect of dependencies with the degradation from limited reasoning length. A more principled baseline (e.g., passing the first problem answer as context to the next) would strengthen the "degradation beyond expectations" claim.
3.  **Limited generalization of RLVR findings.** The reinforcement learning experiments are conducted on only one base model (R1-Qwen-7B) with one RL algorithm (GRPO from Skywork-OR1). It is unclear whether the benefits of composed training data extend to other model sizes, architectures, or RL frameworks (e.g., PPO, RLOO). A single data point limits confidence in the generality of the training conclusions.
4.  **Ambiguity in some analysis definitions.** The "error position" in Section 5.1 is described as the position of the first error in tokens, but the paper states "error range is (4-6k tokens)" without clarifying whether this is the average token position of the *first* error across all composed problems. The reflection detection method ("wait", "but...") is not formally specified, making replication difficult. The "effective" ratio in rollout efficiency (Figure 10) is also not clearly defined in the main text.

### Minor
1.  **Incomplete use of proposed composition types.** The paper introduces three composition types (Directly Compose, Sequential Compose, Graphic Compose) but the main evaluation and training experiments use only the Sequential Compose variant for math. The code and agent constitution methods are relegated to the appendix and use different composition patterns. A more unified evaluation across all three types would strengthen the claim that "R-HORIZON supports the concatenation of three types."
2.  **Potential source of degradation from prompt format.** The composed problems explicitly state the dependency (e.g., "v_{i+1} = f_i(a_i)"). The observed degradation could partly stem from models struggling with the modified prompt structure rather than the multi-horizon reasoning per se. An ablation comparing "directly composed" (no dependency) with "sequentially composed" (with dependency) would help isolate the source of difficulty. The paper has an ablation in Appendix D but it only compares directly composed vs. dependent; the result shows direct composition also degrades, but the additional drop from dependencies is relatively small for some models. This should be discussed more prominently.
3.  **Missing discussion of limitations.** The paper does not explicitly discuss its limitations, such as potential data contamination (seed problems may be memorized) or the fact that the dependency construction relies on integer answers, restricting its applicability to problems with non-integer or non-numeric answers.

### Trivial
None.

## Nice-to-Haves
- Include an analysis of how performance on R-HORIZON correlates with performance on other complex reasoning benchmarks (e.g., MATH, GSM8k) to further validate the benchmark's diagnostic value.
- Provide a more formal definition of reflection detection (e.g., keyword list or parser rules) to enable reproducibility.
- Add experiments with at least one more base model (e.g., Qwen-32B) for the RLVR training to demonstrate generalization.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel observation is that training on interdependent multi-step problems not only improves performance on such tasks but also significantly boosts single-problem accuracy while simultaneously reducing overthinking (shorter responses with better budget allocation). This suggests that the reason for overthinking on isolated problems is not merely that the model is encouraged to think longer, but rather that the model lacks the ability to appropriately *stop* thinking and proceed to the next logical step. Composed problems naturally teach this "proceed" behavior, yielding both efficiency gains and accuracy improvements. This insight has implications for training strategies: simply adding more single-problem RL data may exacerbate overthinking, whereas exposing models to sequential dependencies may be a more effective regularization.

## Suggestions
- Clarify the definition of "expected accuracy" and consider providing a more meaningful baseline, such as the accuracy when the correct previous answer is given as a hint.
- Formalize the reflection detection process (e.g., provide a list of trigrams or a regex pattern) for reproducibility.
- Add a brief discussion of limitations (e.g., integer-answer constraint, potential data contamination, dependency construction scope) in the conclusion.
- Consider including an ablation comparing the effects of "directly composed" vs. "sequentially composed" tasks in the main paper, as the current Appendix D suggests direct composition alone causes significant degradation, which is an important nuance.

## Score and Decision

The paper addresses a timely and important problem, provides a comprehensive evaluation with insightful analysis, and demonstrates practical training improvements. The core method is simple, but the empirical contribution is substantial. The weaknesses (limited novelty of the construction method, questionable expected accuracy metric, narrow RLVR scope) are significant but do not invalidate the overall value of the work. The paper brings sufficient new knowledge and a useful benchmark/training paradigm to the community.

**Score:** 8

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>