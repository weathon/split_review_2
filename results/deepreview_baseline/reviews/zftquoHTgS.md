## Summary

This paper identifies and characterizes the "underthinking" problem in Long Chain-of-Thought (LongCoT) reasoning models, where models prematurely abandon promising reasoning paths by switching thoughts too frequently without sufficient exploration. The authors propose SmartSwitch, a plug-and-play, training-free inference framework that uses a Process Reward Model (PRM) to detect prematurely abandoned high-potential thoughts and intervenes by backtracking and injecting a "deepen prompt" to encourage further exploration. Experiments on challenging mathematical reasoning benchmarks (AIME24/25, AMC23, MATH-500, GaoKao2023en) show consistent accuracy improvements across multiple model families and sizes (1.5B to 32B), while also reducing response length and inference time.

## Strengths

- **Clear problem identification and characterization**: The paper provides both qualitative examples and a quantitative metric (Underthinking Frequency) to demonstrate the prevalence and severity of the underthinking problem across multiple LongCoT models, establishing a strong motivation for the work.
- **Practical and well-designed framework**: SmartSwitch is training-free, model-agnostic, and plug-and-play, making it immediately applicable to existing models without additional training costs. The two-module design (Perception + Intervention) is intuitive and grounded in metacognitive strategies from human problem-solving.
- **Strong empirical results**: The method shows substantial and consistent accuracy gains across all tested models and benchmarks (e.g., +16.7% on AIME25 for 1.5B model, +10.0% on AIME25 for QwQ-32B). Notably, it also reduces response length and inference time, demonstrating that deeper exploration of promising paths can replace wasteful shallow switching.
- **Thorough ablation studies**: The paper systematically ablates key design choices including the PRM model, process division strategy, score mapping strategy, and score threshold, providing clear evidence for each design decision.

## Weaknesses

### Major

- **Reliance on external PRM and linguistic cues**: The framework's effectiveness is fundamentally bounded by the quality of the external PRM (Universal-PRM-7B) and the heuristic thought-switch detection via linguistic cues. The paper acknowledges this as a limitation but does not provide analysis of failure cases where the PRM misjudges a thought's potential or where switches occur without explicit linguistic markers. This raises questions about robustness in more diverse or less structured reasoning domains.
- **Limited evaluation scope**: The evaluation is confined to mathematical reasoning benchmarks. While mathematics is a valid testbed, the paper claims the framework is broadly applicable, yet provides no evidence on other complex reasoning domains (e.g., programming, scientific QA, legal analysis) where LongCoT is also used. The generalizability claim is therefore unsupported.
- **Hyperparameter sensitivity**: The ablation on the score threshold (Table 8) shows extreme sensitivity: performance peaks sharply at exactly 0.70 and drops significantly at 0.68, 0.69, and 0.71 across all models. This suggests the framework may require careful per-model or per-domain tuning, which undermines the plug-and-play claim and raises concerns about practical deployment without extensive calibration.

### Minor

- **The "deepen prompt" is fixed and generic**: The intervention uses a single, fixed prompt ("Wait, this seems like a promising idea..."). The paper does not explore whether different prompts or dynamically generated prompts could yield better results, nor does it analyze how the model's behavior changes in response to this specific prompt versus alternatives.
- **Comparison with TIP is limited**: The comparison with TIP (Wang et al., 2025) is only on one model (1.5B) and one benchmark (AIME24). A more comprehensive comparison across model sizes and benchmarks would strengthen the claim that SmartSwitch is superior to existing underthinking mitigation methods.

### Trivial

- The paper uses "thought" and "process" somewhat interchangeably in places, though the ablation on process-to-thought mapping clarifies the distinction.

## Nice-to-Haves

- An analysis of cases where SmartSwitch fails (e.g., when the PRM incorrectly scores a low-potential thought as high, leading to wasted intervention) would help characterize the framework's limitations.
- A study on the optimal number of interventions per problem and whether this interacts with model size or problem difficulty would be useful for practitioners.
- Discussion of how the framework might be extended to detect implicit thought switches (without explicit linguistic cues) would strengthen the future work section.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Evaluate SmartSwitch on at least one non-mathematical LongCoT reasoning benchmark (e.g., GPQA, LiveCodeBench) to support the claim of general applicability.
- Provide an analysis of the PRM's scoring accuracy on the specific reasoning traces used, including examples of false positives and false negatives, to help readers understand the framework's reliability.
- Investigate whether the sharp threshold sensitivity (Table 8) is an artifact of the specific PRM or a fundamental property of the approach, and discuss strategies for automatic threshold selection.

## Score and Decision

The paper makes a clear, well-motivated contribution by identifying and addressing the underthinking problem in LongCoT reasoning. The SmartSwitch framework is practical, training-free, and shows strong empirical gains with the added benefit of improved efficiency. However, the reliance on an external PRM with demonstrated hyperparameter sensitivity, the limited evaluation scope (mathematics only), and the heuristic nature of thought-switch detection temper the overall impact. The paper is solid and valuable but has clear limitations that prevent it from being a top-tier contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>