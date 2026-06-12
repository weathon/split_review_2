## Summary

This paper introduces a systematic deletion framework to probe how much LLMs genuinely depend on chain-of-thought (CoT) reasoning traces in physics problem solving. By intercepting CoT mid-generation, deleting tokens under three strategies (end, random, physics-aware), and measuring downstream effects on accuracy, answer length, and information overlap, the authors find that models remain accurate under heavy deletions (40-60%) by "cramming" reconstructed steps into final answers. The work reveals that CoT traces are both informative and redundant, raising concerns about reasoning faithfulness in scientific domains and arguing for evaluation methods beyond accuracy.

## Strengths

- **Novel and well-motivated methodology**: The deletion-based probing framework is a creative and principled approach to studying CoT dependence. Intercepting generation mid-stream and manipulating the scratchpad before decoding is a clean experimental design that directly addresses the faithfulness question, going beyond prior work that only observes final outputs.

- **Domain choice is appropriate and impactful**: Physics provides a stringent testbed with structured equations, units, and terminology that enable precise quantification of information recovery. The connection to AI-for-Science is timely and well-argued, as reliability of reasoning traces is critical for scientific applications.

- **Comprehensive experimental design**: The paper systematically varies deletion strategies (end, random, physics-aware), deletion fractions (0-100%), prompting styles (low/medium/high reasoning), and evaluates three diverse open-source models across three benchmarks of varying difficulty. The "cramming" phenomenon is convincingly documented through multiple converging metrics (accuracy, answer length, information overlap).

- **Clear and actionable findings**: The observation that accuracy remains stable under 40-60% deletion while models reconstruct missing content in final answers is a robust and non-obvious result. The implications for early stopping, prompt design, and the need for faithfulness-aware evaluation are practical and well-supported.

## Weaknesses

### Fatal
None.

### Major

- **The evaluation of answer correctness relies on Claude-4 Sonnet as a judge, but this introduces a circular dependency**: The paper uses Claude-4 Sonnet both to evaluate answer quality (scoring 0-1) and to identify physics-related tokens for the "physics-aware" deletion strategy. This raises concerns about whether the evaluation judge shares the same failure modes as the models being evaluated. If Claude-4 Sonnet also exhibits "cramming" behavior or is insensitive to missing reasoning steps, the scoring may systematically overestimate correctness under deletion. The paper does not validate the judge's reliability against human expert evaluation or ground-truth answer keys.

- **The information overlap analysis conflates lexical similarity with genuine reasoning faithfulness**: Jaccard similarity and Manhattan distance on bag-of-words capture surface-level token reuse but do not measure whether the *logical structure* of reasoning is preserved. A model could reproduce the same equations and terms while using them in a fundamentally different or incorrect derivation. The paper acknowledges this limitation but does not provide any structural or semantic analysis (e.g., dependency graphs, step ordering) that would strengthen the faithfulness claim.

- **The "cramming" interpretation is plausible but underdetermined by the evidence**: The increase in final answer length under deletion could reflect genuine reconstruction of missing reasoning, but it could also reflect the model generating more verbose or hedging language when uncertain, or simply producing longer outputs because the generation budget is reallocated from the scratchpad to the answer. Without internal analyses (e.g., probing hidden states, attention patterns, or decoding dynamics), the paper cannot distinguish between these alternatives. The authors acknowledge this limitation but do not attempt any mechanistic analysis that would strengthen the cramming hypothesis.

### Minor

- **The calibration study (Section 3.1) is underspecified**: The paper states that "approximately 5 prompts are sufficient to reduce the relative error bar below 10%" based on bootstrapped results over 50 questions with 5 re-runs. However, the details of the bootstrapping procedure, the confidence interval computation, and the justification for the 10% threshold are not provided. This makes it difficult to assess whether the calibration is adequate for the main experiments.

- **The paper does not report statistical significance or effect sizes for the key comparisons**: While error bars are shown in figures, there is no formal hypothesis testing (e.g., whether the accuracy drop at 40% deletion is statistically significant across models and datasets). Given the variability in the results, this would strengthen the claims.

- **The "Less Reasoning" conditions (Low/Medium) are not clearly distinguished from the deletion experiments**: The paper establishes that explicit reasoning improves accuracy, but the relationship between prompting style and deletion robustness is not explored. Do models prompted with "Low Reasoning" exhibit different cramming behavior under deletion? This would be a natural extension.

### Trivial
None.

## Nice-to-Haves

- A human evaluation study on a subset of the data to validate the Claude-4 Sonnet judge's scoring, especially for cases where the model produces correct answers with incorrect or missing reasoning.
- Analysis of whether the "cramming" behavior is specific to physics or generalizes to other structured reasoning domains (e.g., math word problems, logic puzzles, code generation).
- Investigation of whether larger models (e.g., 70B+ parameters) exhibit more or less cramming, to test the scaling hypothesis mentioned in the limitations.

## Novel Insights

Beyond the paper's own contributions, the most striking insight is that the "cramming" phenomenon reveals a fundamental tension in how LLMs use CoT: the scratchpad serves as both a *workspace* for intermediate computation and a *communication channel* to the user. When the workspace is disrupted, the model can shift computation to the communication channel (the final answer), effectively treating the answer as a fallback scratchpad. This suggests that CoT faithfulness is not just about whether the trace is accurate, but about whether the model has a stable *division of labor* between reasoning and output generation. The paper's deletion framework could be adapted to study this division of labor more broadly, potentially revealing architectural or training factors that determine how models allocate computation across generation stages.

## Suggestions

- Validate the Claude-4 Sonnet judge against human expert evaluation on a random subset of 50-100 answers, reporting agreement rates and systematic biases. If the judge is unreliable, consider using exact answer matching or a simpler rubric.
- Add a structural faithfulness metric beyond bag-of-words overlap, such as whether the key equations in the CoT are correctly reproduced in the final answer (e.g., using symbolic matching or dependency parsing).
- Report results with confidence intervals and statistical tests (e.g., paired bootstrap tests comparing accuracy at 0% vs. 40% deletion) to quantify the reliability of the observed patterns.
- Include an ablation where the deletion is applied *after* the CoT is fully generated but before the answer is decoded, to confirm that the effects are due to missing information rather than disruption of the generation process itself.

## Score and Decision

The paper presents a novel, well-executed methodology for probing CoT faithfulness in a scientifically important domain. The findings are robust across models, datasets, and deletion strategies, and the "cramming" phenomenon is a genuine contribution to understanding how LLMs use reasoning traces. The major weaknesses—reliance on an unvalidated judge model and the surface-level nature of the overlap analysis—are significant but not fatal, as the core claims about accuracy stability and answer length increase under deletion do not depend on the judge's absolute correctness. The paper is clearly written, the experiments are thoughtfully designed, and the implications for AI-for-Science are compelling. I recommend acceptance with the expectation that the authors address the judge validation and structural faithfulness analysis in the final version.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>