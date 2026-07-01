## Summary

This paper introduces a systematic deletion framework to probe how much LLMs genuinely depend on chain-of-thought (CoT) reasoning in physics problem solving. By intercepting CoT traces mid-generation, deleting tokens under three strategies (end, random, physics-aware), and measuring downstream effects on accuracy, answer length, and information overlap, the authors find that models remain accurate under heavy deletions (40-60%) by "cramming" reconstructed steps into final answers. The work reveals that current accuracy-based evaluations are insufficient for scientific domains and argues for evaluation methods that assess reasoning faithfulness.

## Strengths

- **Novel methodological contribution**: The deletion-based probing framework is a simple yet effective approach for evaluating reasoning dependence that goes beyond standard accuracy metrics. Intercepting CoT mid-generation and systematically removing tokens provides a controlled way to test whether models genuinely use their reasoning traces.

- **Domain-appropriate evaluation**: Physics is a well-chosen testbed because its structured nature (equations, units, terminology) enables precise quantification of information overlap and recovery, making the faithfulness analysis more rigorous than in open-ended domains.

- **Comprehensive experimental design**: The paper evaluates three different deletion strategies (end, random, physics-aware) across three models and three datasets, providing a thorough characterization of cramming behavior and its consistency across settings.

## Weaknesses

### Major

- **Limited novelty relative to existing work**: The core finding that models can produce correct answers while not faithfully using CoT traces is well-established in prior work (Turpin et al., 2023; Lanham et al., 2023; Lyu et al., 2023), which the paper itself cites. The paper's primary contribution is applying deletion-based probing to physics, but the qualitative patterns observed (cramming, robustness to deletion, surface-level recovery) largely confirm rather than extend existing understanding. The paper does not demonstrate how its findings lead to new insights about model mechanisms or how they could inform concrete improvements to model design or evaluation.

- **Weak faithfulness analysis**: The information overlap metrics (Jaccard similarity and Manhattan distance on bag-of-words) are too coarse to meaningfully assess reasoning faithfulness. Lexical overlap does not capture whether reconstructed content is logically correct, uses appropriate equations, or follows valid derivations. A model could reproduce the same vocabulary while making fundamentally different reasoning errors, and these metrics would not distinguish this from faithful recovery. The paper acknowledges this limitation but does not address it.

- **No mechanistic analysis**: The paper explicitly states it does not analyze latent representations, attention patterns, or decoding dynamics. This is a significant limitation because the central claim about "cramming" as compensatory behavior remains speculative without internal evidence. The observed increase in answer length could arise from multiple mechanisms (e.g., the model simply generating more text when given less context, or different sampling dynamics with shorter prompts), and the paper does not rule out simpler explanations.

### Minor

- **Evaluation using Claude-4 Sonnet as judge**: Using another LLM to score physics solutions introduces potential biases and reliability concerns. The paper does not provide validation of the judge model's accuracy or calibration against human evaluation.

- **Limited model diversity**: All three models are recent reasoning-focused LLMs. Including a non-reasoning model as a baseline would strengthen the claim that observed behaviors are specific to reasoning-oriented architectures.

### Trivial

- The paper refers to "Magistral" in the abstract and body but "Magistrall" in Section 2.2, suggesting a minor inconsistency.

## Nice-to-Haves

- A baseline comparison with non-reasoning models (e.g., standard instruction-tuned LLMs without CoT training) would help isolate whether cramming is a general phenomenon or specific to reasoning-focused models.
- Human evaluation of a subset of reconstructed answers would strengthen the faithfulness analysis.
- Analysis of whether cramming produces correct or incorrect reconstructions would be more informative than lexical overlap alone.

## Novel Insights

None beyond the paper's own contributions. The paper's empirical findings—that models remain accurate under moderate CoT deletion and exhibit cramming behavior—are consistent with and largely confirm existing work on CoT faithfulness. The application to physics is novel but does not yield qualitatively new insights about model reasoning.

## Suggestions

- Strengthen the faithfulness analysis by evaluating whether reconstructed content is *correct* (e.g., checking if regenerated equations are mathematically valid and appropriate for the problem), not just lexically similar.
- Include a non-reasoning baseline model to demonstrate that cramming is not a general property of all LLMs but specifically relates to reasoning-focused training.
- Provide mechanistic evidence for cramming, such as analyzing whether the model's internal representations show evidence of information preservation during deletion.

## Score and Decision

The paper presents a clean experimental framework and applies it to an underexplored domain (physics), but the core findings largely replicate established results about CoT faithfulness. The methodological contribution is incremental, and the faithfulness analysis is too coarse to support strong claims about reasoning dependence. The paper would benefit from deeper analysis and stronger evidence for its central claims.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>