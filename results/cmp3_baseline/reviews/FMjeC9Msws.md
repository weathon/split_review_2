## Summary

This paper presents a large-scale empirical study (over 400,000 GPU-hours) on scaling reinforcement learning (RL) for large language models (LLMs). The authors propose a sigmoidal compute-performance scaling law for RL training, characterize how various design choices affect asymptotic performance (`A`) and compute efficiency (`B`), and derive a practical recipe (SCALERL) that scales predictably. They demonstrate that SCALERL achieves state-of-the-art validation performance on math reasoning tasks and exhibits clean extrapolation to 100,000 GPU hours, bringing a degree of predictability to RL training that parallels pre-training scaling laws.

## Strengths

- **Massive and systematic empirical study**: The paper conducts over 400,000 GPU-hours of controlled experiments, enabling reliable statistical comparisons of design choices under a unified scaling framework. This is significantly larger and more rigorous than prior ablation studies in RL for LLMs.
- **Novel predictive scaling framework**: The sigmoidal curve (Equation 1) provides a practical tool for extrapolating RL performance from small-scale runs to large compute budgets. This is a concrete methodological contribution that can help the community identify promising algorithms before committing to expensive large-scale runs.
- **Clear separation of asymptotic performance and efficiency**: The framework cleanly separates whether a design choice improves the ceiling (`A`) or merely speeds up convergence (`B`). This insight (e.g., FP32 precision improves asymptote, while PipelineRL mainly improves efficiency) is actionable for practitioners.
- **Leave-one-out ablations at 16,000 GPU-hours**: Each component of SCALERL is validated by reverting it in a full-scale run, confirming that the combination yields net gains. The extrapolations from 8k to 16k GPU-hours are verified, supporting the predictive claim.
- **Consistent cross-axis scaling**: The paper shows that the predictive framework extends across model size, generation length, batch size, and multi-task training, lending credibility to the generality of the approach.

## Weaknesses

### Fatal
None.

### Major
1. **Domain specificity**: The experiments are almost entirely on verifiable math tasks (Polaris‑53k). While a brief multi-task math+code result is shown, the paper does not convincingly demonstrate that the sigmoidal scaling law or the SCALERL recipe transfers to other important RL for LLM domains (e.g., multi-step reasoning with dense rewards, agentic tasks, instruction following). The claim of a general scaling methodology is thus supported only within a narrow domain.

2. **Empirical rather than principled justification of the sigmoidal functional form**: The choice of a sigmoidal curve is motivated primarily by empirical fit stability compared to power laws. There is no theoretical argument for why RL performance should follow this form (e.g., why it saturates rather than continuing to improve on a log scale). This weakens the scientific contribution; the framework is a useful description but not an explanatory model.

3. **Potential unfairness in cross-recipe comparison (Figure 2)**: The baseline methods (DeepSeek GRPO, DAPO, etc.) are re-implementations based on public descriptions. It is unclear whether these recipes were given comparable hyperparameter tuning or optimization of auxiliary components (e.g., batch size, learning rate schedule, off-policy setup). The paper may underestimate the scalability of these methods if they were not configured optimally for the specific compute regime.

4. **Limited exploration of divergence and training stability**: The paper mentions that some design choices become unstable beyond a certain compute scale (Appendix A.16) but does not systematically analyze how scaling affects training stability or what failure modes occur. This is an important practical aspect of scaling that is largely left to future work.

### Minor
1. The evaluation metric (pass rate on a held-out validation set of 1000 prompts with 16 generations each) is reasonable but depends on the quality of the validation set and the generation count. The paper does not study how these choices affect the fitted scaling curves.

2. The ablation on "generations per prompt" (Section 5) holds the total batch fixed, which mixes the effect of generation count and prompt count. The conclusion that it is a “second-order choice” may not hold at different batch sizes or reward densities.

### Trivial
None.

## Nice-to-Haves
- A theoretical sketch (even heuristic) of why saturating curves emerge for bounded metrics like pass rate, linking to the diminishing gradient signal as the policy improves.
- A study of whether the sigmoidal fits hold for unbounded metrics (e.g., reward) or for evaluation on out-of-distribution tasks (beyond AIME‑24).
- Code release for the full SCALERL training pipeline, not just the curve-fitting code.

## Novel Insights
The paper’s key insight is that, despite the “art” reputation of RL for LLMs, RL training follows predictably saturating scaling curves when measured on in-distribution validation performance. This allows researchers to forecast the asymptotic payoff of a recipe from early, smaller-scale runs and to distinguish design choices that shift the ceiling from those that only affect convergence speed. The empirical finding that careful precision management (FP32 logits) substantially raises the asymptote is a concrete, novel surprise that was not widely appreciated in prior work.

## Suggestions
- Validate the scaling framework on at least one additional, non-math domain (e.g., code reasoning or instruction tuning) with a comparable budget, even if at smaller model scale, to strengthen claims of generality.
- For the cross-recipe comparison, provide evidence that each baseline was tuned (e.g., learning rate sweep, batch size adjustment) to perform well at the scales tested, or disclose the tuning effort dedicated to each.
- Investigate whether the sigmoidal form holds when performance is measured on a held-out test set (downstream generalization) rather than in-distribution validation, and discuss any discrepancies.

## Score and Decision

Score: 7.0  
Decision: Accept

The paper makes a substantial empirical contribution with high practical relevance. The predictive scaling framework fills a clear gap in the community and is supported by a body of experiments at an unusually large scale. The weaknesses (domain specificity, empirical functional form, potential unfairness in comparisons) are notable but not fatal; they reduce the strength of the claims but do not invalidate the core contribution. The paper will likely have significant impact on how RL research for LLMs is conducted.

MY FINAL SCORE: <score>7.0</score>  
MY FINAL DECISION: <decision>Accept</decision>