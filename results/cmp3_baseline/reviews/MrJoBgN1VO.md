## Summary

This paper formalizes the **Program-to-Geometry** task, where LLMs must interpret procedural drawing code (e.g., Asymptote) and perform geometric reasoning. The authors introduce **GeoGramBench**, a curated benchmark of 500 problems organized by a three-level taxonomy (Primitive Recognition, Local Relation Composition, Global Abstract Integration) that reflects geometric complexity rather than reasoning steps. An extensive evaluation of 19 frontier LLMs reveals that even the strongest models achieve less than 50% accuracy on the highest abstraction level, exposing critical limitations in symbolic-to-spatial reasoning.

## Strengths

- **Well-motivated and underexplored task.** The Program-to-Geometry setting is a natural and important capability for LLMs, bridging procedural code and spatial reasoning. The paper convincingly demonstrates that existing benchmarks do not isolate this skill, and that models suffer significant accuracy drops when code is present.
- **Rigorous benchmark construction.** The authors carefully address answer leakage (direct and indirect), perform decontamination, and use human expert verification. The taxonomy is empirically motivated by showing that geometric complexity, not reasoning steps, drives difficulty in this task.
- **Comprehensive evaluation.** 19 models spanning closed-source and open-source, from 1.5B to 235B parameters, are evaluated with consistent protocols. The results are clearly presented and reveal consistent patterns (e.g., all models below 50% on Abstract level, angle/volume as hardest subtypes).
- **Useful behavior analysis.** The qualitative analysis of model responses (RQ1–RQ3) provides concrete insights into how models parse code, struggle with composition, and fail to benefit from long CoT reasoning. The identified failure patterns (algebraic bias, no auxiliary constructions, orientation confusion) are actionable.

## Weaknesses

### Major

- **Behavior analysis is largely qualitative and anecdotal.** The analysis of failure patterns and CoT behavior is based on manual review of representative examples rather than systematic annotation or quantitative metrics. While insightful, the claims about “pronounced preference for algebraic methods” or “rarely introduce auxiliary lines” lack rigorous support. A more structured error analysis (e.g., categorizing failure types across all model outputs) would strengthen the conclusions.
- **Benchmark size is moderate (500 problems).** While the authors argue this is the largest dedicated benchmark for this task, 500 problems is still relatively small for fine-grained subtype analysis (e.g., some subtypes have very few examples). The distribution is also heavily skewed toward the Abstract level (55.3%), which may affect reliability of per-subtype comparisons.
- **Taxonomy validation could be stronger.** Figure 2 attempts to validate the taxonomy by showing that accuracy on P_TC problems correlates with geometric complexity but not reasoning complexity. However, the graph is somewhat confusing (the legend and axes are unclear), and the analysis is only done on MATH-500 (42 code problems). A more thorough validation across the full benchmark would be desirable.

### Minor

- **The claim of “first large-scale benchmark” is slightly overstated.** Existing benchmarks like MATH-500 and AIME24 contain procedural code subsets, and works like Muennighoff et al. (2025) have studied this setting. The paper acknowledges this but could more precisely position GeoGramBench as the first *dedicated* and *systematically curated* benchmark for Program-to-Geometry.
- **The evaluation uses 8 samples per problem with temperature 0.6.** While this is reasonable, the paper does not discuss the sensitivity of results to sampling strategy or whether majority voting would change conclusions. A brief ablation would be helpful.

### Trivial

- None.

## Nice-to-Haves

- A systematic error taxonomy with quantitative frequencies across models would greatly strengthen the behavior analysis.
- Including a small set of human performance estimates would help calibrate the difficulty of the benchmark.
- Releasing the benchmark with multiple code languages (e.g., both Asymptote and matplotlib) could increase generality.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that geometric complexity—rather than reasoning step count—is the primary bottleneck in Program-to-Geometry tasks. This challenges the common assumption that harder problems are simply those requiring more reasoning steps. The finding that even strong reasoning models (GPT-o1, DeepSeek-R1) plateau below 50% on the Abstract level suggests that current LLMs lack a fundamental capacity for constructing and manipulating internal spatial representations from symbolic code, a limitation that CoT reasoning alone cannot overcome.

## Suggestions

- Provide a more quantitative error analysis, e.g., by having human annotators label failure types on a random subset of model outputs, and report frequencies.
- Clarify the taxonomy validation by showing accuracy vs. geometric complexity on the full GeoGramBench (not just MATH-500) and by reporting inter-annotator agreement for the taxonomy labels.
- Discuss the potential impact of the skewed distribution (55% Abstract) on the overall conclusions and consider adding more Primitive/Compositional problems in future versions.

## Score and Decision

**Score:** 7.5  
**Decision:** Accept  

The paper makes a solid contribution by formalizing an underexplored task, constructing a careful benchmark, and providing a broad evaluation with actionable insights. The weaknesses (qualitative behavior analysis, moderate size) are not fatal and can be addressed in future work. The benchmark is likely to be a useful resource for the community.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>