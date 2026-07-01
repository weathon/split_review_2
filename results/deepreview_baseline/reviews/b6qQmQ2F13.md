## Summary

This paper investigates memory-accuracy trade-offs for reasoning models under fixed memory budgets, considering model size, weight precision, token budget, parallel scaling, and KV cache compression. Through systematic experiments across model families (Qwen3, DeepSeek-R1-Distill, OpenReasoning-Nemotron) and benchmarks (AIME25, GPQA-Diamond, LiveCodeBench, MATH500), the authors find that the optimal memory allocation strategy is scale-dependent: for models with effective size below 8-bit 4B, memory is better spent on larger weights, while for larger models, increasing the generation budget is more efficient. The paper also shows that task type matters (math/code need higher precision than knowledge tasks) and that KV cache compression (eviction for small models, quantization competitive for large) is essential beyond weight-only quantization.

## Strengths

- **Timely and practical problem**: The paper addresses a critical deployment challenge for reasoning models, where KV cache can dominate memory due to long generations, and shows that conventional wisdom from non-reasoning models does not transfer.
- **Systematic and comprehensive study**: Over 1,700 experimental configurations across multiple model families, weight precisions, token budgets, parallel scaling, and KV compression methods provide robust empirical evidence.
- **Clear, actionable findings**: The five main findings are well-supported and provide concrete guidelines for practitioners (e.g., scale-dependent allocation, task-dependent precision, when to use parallel scaling, and when eviction beats quantization).
- **Generalization across model families**: Key results are validated on DeepSeek-R1-Distill and OpenReasoning-Nemotron, not just Qwen3, increasing confidence in the conclusions.
- **Pareto frontier analysis**: The use of Pareto-optimal configurations to compare strategies is appropriate and clearly visualizes the trade-offs.

## Weaknesses

### Fatal
None.

### Major
- **Inconsistent threshold definitions**: Finding 1 uses "8-bit 4B" as the threshold for scale-dependent allocation, while Finding 5 uses "8-bit 8B" for the eviction vs. quantization decision. The paper does not explain why different thresholds arise for different decisions, which could confuse practitioners trying to apply the guidelines. This inconsistency needs clarification or justification.

### Minor
- **Limited latency/throughput analysis**: The paper focuses on memory-accuracy trade-offs but only briefly mentions latency in an appendix. The claim that increasing effective size is "strictly dominant" for small models relies on the assumption that latency is dominated by token budget, which may not hold in all deployment scenarios (e.g., real-time applications with strict latency constraints). A more thorough discussion of latency implications in the main text would strengthen the practical recommendations.
- **Single eviction and quantization methods**: The study uses R-KV for eviction and HQQ for quantization. While these are reasonable choices, results may not generalize to all KV compression methods. The paper acknowledges this in limitations, but the strength of the claims (e.g., "eviction is better than quantization for small models") would benefit from verification with at least one additional method per category.
- **No theoretical explanation for threshold**: The 8-bit 4B effective size threshold is purely empirical. While this is acceptable for an empirical study, providing intuition or a theoretical rationale for why this particular scale emerges would deepen the contribution.

### Trivial
- The paper uses "effective size" to mean weight memory footprint, but occasionally uses "scale" interchangeably; this is clear in context but could be more consistent.

## Nice-to-Haves

- A decision flowchart or table summarizing the recommended strategy based on effective size, task type, and memory budget would be a practical addition for practitioners.
- Analysis of how the threshold might shift with different architectures (e.g., MoE models, different attention mechanisms) would be interesting future work.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the memory-optimal strategy for reasoning models is fundamentally different from non-reasoning models because the KV cache becomes a dominant memory consumer. This shifts the optimization problem from "how to compress weights" to "how to allocate memory between weights and generation." The finding that small models benefit more from higher-precision weights while large models benefit from longer generations is non-trivial and suggests that the scaling behavior of reasoning models has a phase transition around a certain effective size. The task-dependent sensitivity to weight precision (math/code needing higher precision than knowledge tasks) is also a novel observation that challenges the universal 4-bit prescription.

## Suggestions

- Clarify the relationship between the two thresholds (8-bit 4B vs. 8-bit 8B) and explain why different decisions have different inflection points. If the thresholds are consistent under a unified framework, make that explicit; if they differ, explain the rationale.
- Include a brief latency discussion in the main paper (even a paragraph) to qualify the "strictly dominant" claim for small models, noting that the conclusion holds when latency is proportional to token budget.

## Score and Decision

**Score**: 8

**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>