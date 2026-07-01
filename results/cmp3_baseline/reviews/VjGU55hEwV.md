## Summary

The paper introduces RLIE, a framework that combines LLM-based natural language rule generation with logistic regression to produce a set of weighted, interpretable rules for binary classification. The method comprises four stages: rule generation by an LLM, probabilistic weighting and selection via elastic-net regularized logistic regression, error-driven iterative refinement, and a systematic evaluation of inference strategies. Experiments on six real-world text classification datasets show that RLIE achieves strong performance against several LLM-based baselines, and that direct prediction using the learned linear combiner surprisingly outperforms strategies that feed the rules, weights, or reference predictions back into an LLM.

## Strengths

- **Novel integration of LLM rule generation with probabilistic combination.** RLIE is the first framework to explicitly couple LLMs with regularized logistic regression for learning a collaborative set of weighted natural language rules. This bridges the gap between the expressive power of LLMs and the principled aggregation of classical rule-based methods.
- **Insightful hierarchical evaluation of inference strategies.** The paper systematically compares four ways to use the learned rules (linear-only, LLM+rules, +weights, +linear prediction) and provides the counterintuitive result that the simplest linear combiner is most effective. This finding offers practical guidance and deepens the understanding of LLMs’ limitations in probabilistic reasoning.
- **Consistent empirical performance.** Across six datasets, RLIE with DeepSeek-V3 ranks first or second in both Accuracy and Macro-F1 compared to a range of competitive baselines (zero-shot, ICL, IO Refinement, HypoGeniC), demonstrating robustness and generalizability.
- **Clear, detailed methodology.** The four-stage pipeline is well-motivated and described with sufficient detail (coverage filtering, ternary judgments, elastic-net regularization, iterative refinement with hard-example mining) to enable reproduction.

## Weaknesses

### Fatal

None.

### Major

- **Small dataset sizes and lack of uncertainty reporting.** Each dataset is partitioned into only 200/200/300 samples, and the reported results in Tables 1 and 2 do not include standard deviations despite the paper claiming “at least three repetitions.” Without variance information, it is impossible to assess the statistical significance of the observed performance gaps, which are often modest (a few percentage points). This weakens the reliability of the main results and the claims of superiority.
- **Potential overfitting concerns.** With only 200 training samples and an iterative refinement process driven by hard examples from the same training set, the learned rule set may overfit to the small data. Although early stopping on a 200-sample validation set is used, the validation set itself is small, and no analysis of rule generalization (e.g., performance on held-out folds or larger datasets) is provided.
- **Limited comparison of LLM backbones for baselines.** The baselines (IO Refinement, HypoGeniC) are only evaluated with DeepSeek-V3, while RLIE is tested on three different backbones (including larger ones). This makes the horizontal comparison partially confounded by model choice. A fairer evaluation would also run baselines on the same varied backbones to isolate the effect of the RLIE framework.

### Minor

- **The claim of “superior over all performance” is slightly over-stated.** While RLIE generally performs best, the gains on some datasets (e.g., Reviews, Retweets) are small, and on Dreddit the LLM+Full strategy matches or slightly exceeds the linear-only result. The conclusion that linear-only is “best across the board” is supported, but the margin of superiority is not always large.
- **The evaluation of LLM injection strategies depends on prompt design.** The prompts used for inference (E2–E4) are in the appendix but not discussed in the main text. Suboptimal instruction could partially explain the degraded performance when rules/weights are provided. The paper acknowledges this implicitly but does not ablate over different prompt formulations or verify that the LLM correctly follows the intended reasoning protocol.
- **The rule capacity limit H=10 and other hyperparameters are dataset-agnostic.** No sensitivity analysis is performed to show how the choice of H, coverage threshold γ, or number of hard examples k affects performance. These choices may not transfer to different data regimes.

### Trivial

- The red “Update” arrow in Figure 1 is described but the figure itself is not fully accessible in the text; the caption repeats verbatim.
- The Ethics and Reproducibility sections are present but somewhat generic.

## Nice-to-Haves

- Conduct experiments on larger splits (e.g., thousands of samples) to verify that the RLIE framework scales and does not overfit.
- Include standard deviations and statistical significance tests (e.g., paired bootstrap) for all main results.
- Run baselines (IO Refinement, HypoGeniC) on multiple LLM backbones (e.g., Qwen3-235B) to enable a cleaner comparison.
- Perform an ablation study on the number of refinement iterations and the coverage threshold to analyze the contribution of each component.

## Novel Insights

Beyond the paper’s own contributions, the most striking insight is that LLMs, despite their vast pre-trained knowledge, are not naturally good at integrating explicit probabilistic signals (rule weights and reference predictions) into their reasoning. The linear-only strategy, which uses a simple logistic regression model on ternary rule judgments, consistently outperforms LLM-augmented inference. This aligns with the idea of a “division of labor”: LLMs are strong at semantic interpretation at the single-rule level but weak at controlled, global probabilistic aggregation. This finding reinforces the value of neuro-symbolic designs where classical statistical methods handle combination and calibration while LLMs handle local, flexible tasks.

## Suggestions

- Report standard deviations in all result tables and use statistical tests to support claims of improvement.
- Include an additional experiment on a larger benchmark (e.g., HypoBench’s non-language tasks or a public text classification dataset with >1000 examples) to demonstrate scalability.
- Add a sensitivity analysis for key hyperparameters (rule capacity, coverage threshold, number of hard examples) and discuss how they might be chosen in practice.

## Score and Decision

**Score:** 6.0

**Decision:** Accept

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>