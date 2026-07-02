## Summary

The paper introduces High-Entropy Sum (HES), a training-free metric that sums the entropy of the top 0.5% highest-entropy tokens in a reasoning sample to quantify reasoning quality. HES is validated across SFT, RFT, and RL training paradigms, showing that selecting data based on HES consistently matches or surpasses full-dataset performance while using significantly less data. The metric is simple, efficient, and generalizes across models, datasets, and domains (math, code, STEM).

## Strengths

- **Simple yet effective metric**: HES is intuitive (focusing on high-entropy "forking" tokens) and requires no additional training or external reward models, making it practical for large-scale data curation.
- **Comprehensive empirical validation**: The paper evaluates HES across three major training paradigms (SFT, RFT, RL), multiple models (Qwen3-8B, DeepSeek-R1-Distilled-7B/1.5B), multiple datasets, and multiple domains (math, code, STEM). The experiments are thorough and well-controlled.
- **Consistent and significant improvements**: In SFT, training on the top 20% HES data matches full-dataset performance, and the top 80% consistently surpasses it. In RL, HES-based positive selection with random negatives outperforms full-batch training despite using half the data. These results are robust across settings.
- **Cross-model transferability**: HES computed using a small proxy model (0.6B) transfers effectively to larger models (8B), demonstrating cost-effective data curation.
- **Clear ablation and sensitivity analysis**: The paper systematically ablates different entropy-based metrics, selection strategies, and hyperparameters (data ratio, high-entropy token ratio), providing strong evidence for the design choices.

## Weaknesses

### Fatal
None.

### Major
- **Limited theoretical grounding**: The paper relies on an intuitive connection between high-entropy tokens and reasoning quality, but does not provide a formal justification or analysis of why HES works. The claim that "higher HES indicates higher quality" is empirically supported but not theoretically explained. This limits the depth of the contribution.
- **RL experiments are narrow**: The RL experiments are conducted only on a 1.5B model with a single dataset (DeepScaleR). While the results are positive, the generalizability of the HES-based RL strategy to larger models and more diverse RL settings (e.g., different reward structures, longer training) is not demonstrated. The paper's claim of a "unified" framework would be stronger with broader RL validation.

### Minor
- **Comparison to more advanced data selection methods**: The paper compares HES against simple baselines (random, length, difficulty, average entropy) but does not compare against more sophisticated training-free metrics (e.g., perplexity-based filtering, self-supervised difficulty estimation) or lightweight gradient-based methods. While the paper argues these are costly, a brief comparison or discussion would strengthen the positioning.
- **Choice of top 0.5% is somewhat arbitrary**: The sensitivity analysis shows that smaller ratios (0.005) work best, but the paper does not explore why 0.5% is optimal or whether this ratio generalizes across models and tasks. A more principled justification or adaptive selection would be beneficial.

### Trivial
- The paper occasionally uses "Highest-HES (0.6B)" and "Highest-HES (1.7B)" in tables without explicitly stating these are proxy models; this is clarified in the text but could be confusing at a glance.

## Nice-to-Haves

- A theoretical analysis (e.g., connection to information gain or decision-theoretic measures) would elevate the paper from an empirical contribution to a deeper understanding.
- Extending RL experiments to larger models (e.g., 7B) and more diverse tasks (e.g., code generation RL) would strengthen the claim of universality.
- A comparison to a lightweight learned reward model (e.g., a small classifier trained on HES-like features) could further contextualize the benefits of HES.

## Novel Insights

The key insight is that focusing on the *sum* of the highest-entropy tokens (rather than average or total entropy) captures the cumulative complexity of critical decision points in reasoning paths, and that this signal is robustly correlated with training value across paradigms. The finding that pruning the lowest-HES data improves performance (even surpassing full-dataset) is a practical and non-obvious result. The asymmetric RL strategy (high-HES positives + random negatives) is also a novel and effective design.

## Suggestions

- Provide a brief theoretical discussion (e.g., why cumulative high-entropy tokens might correlate with reasoning complexity, perhaps via a connection to the number of "forks" or decision points).
- Add RL experiments on at least one additional model size (e.g., 7B) or task domain to demonstrate broader applicability.
- Clarify in the main text that the 0.5% threshold is a hyperparameter and discuss its sensitivity more explicitly (the sensitivity analysis is in the paper but could be highlighted).

## Score and Decision

Score: 8  
Decision: Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>