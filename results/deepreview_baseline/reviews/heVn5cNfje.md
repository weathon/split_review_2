## Summary

The paper proposes **High-Entropy Sum (HES)** , a training-free metric that measures reasoning-path quality by summing the entropy of the top 0.5% highest-entropy tokens—targeting critical forking points in long-CoT reasoning. The authors validate HES across SFT, RFT, and RL: in SFT, training on just the top 20% of HES-ranked data matches full-dataset performance; in RFT, HES-based selection outperforms random baselines; in RL, pairing highest-HES successful trajectories with random failures surpasses the full-batch baseline using half the data. A unified data-selection framework built on HES improves training efficiency and obviates costly external reward models.

## Strengths

- **Simple, principled, and computationally efficient metric.** HES is intuitive (focusing on high-uncertainty forking points), requires no training, and can be computed from a single model forward pass on existing data. This is a clear practical advantage over reward-model–based or gradient-based alternatives.
- **Comprehensive empirical validation.** The paper demonstrates HES across three major training paradigms (SFT, RFT, RL), on diverse benchmarks (math, code, STEM), with multiple models (Qwen3-8B, DeepSeek-R1-Distilled-7B/1.5B), and in different dataset sizes. The consistent improvements over random and heuristic baselines (length, difficulty, average entropy) make the findings convincing.
- **Unified framework with actionable insights.** HES provides a single metric that works for data pruning, rejection sampling selection, and RL positive-sample curation. The observation that the bottom 20% of HES-scored data is actively harmful (SFT) and that random negative sampling is better than curated negative sampling (RL) are valuable, non-obvious findings.
- **Small-to-large model transferability.** Using a 0.6B proxy model to select data for an 8B model yields nearly identical performance, dramatically reducing inference costs; this is a strong practical contribution.

## Weaknesses

### Fatal
None.

### Major

1. **Lack of statistical significance or variance estimates.** No experiment reports multiple seeds or confidence intervals. The RL improvement (21.30 vs 20.63 average) is modest and not uniform across benchmarks (e.g., HMMT25 decreases). Without uncertainty quantification, it is unclear whether these gains are statistically reliable.

2. **Arbitrary choice of the top-0.5% threshold.** While sensitivity analysis shows that 0.5% (0.005 ratio) works best, the paper provides no theoretical or empirical justification for why this specific percentile is principled. The metric’s success depends on this hyperparameter, yet the reasoning for its selection is missing.

3. **Potential failure mode for concise correct reasoning.** HES assumes that higher entropy at forking points correlates with higher quality. A correct but very confident, low-entropy solution (e.g., a simple elegant derivation) would get a low HES score and be discarded as low-quality, even though it is perfectly valid training data. The paper does not discuss this limitation or test scenarios where low-entropy correct paths are beneficial.

### Minor

- The RL experiments use only one model size (1.5B) and a single training run per configuration. Extending to larger models or reporting multi-seed averages would strengthen the claims, especially given the modest improvements.
- The comparison with “difficulty” baselines (pass@32, number of correct answers) is somewhat weaker because those metrics require additional evaluations, making them less “training-free” than HES. This is acknowledged but could be discussed more explicitly.

### Trivial

- The paper uses the acronym “HES” for both the metric and the overall framework, occasionally causing slight confusion in the text.
- Some figure captions in the provided material are repetitive due to extraction artifacts (these are parser issues and do not affect the paper’s quality).

## Nice-to-Haves

- A theoretical analysis or intuitive explanation of why the *sum* of high-entropy tokens is more discriminative than their *average* (the paper shows this empirically but does not explore the reason).
- A case study showing examples of high- and low-HES reasoning paths to illustrate what the metric captures qualitatively.

## Novel Insights

Beyond the paper’s own contributions, the most interesting insight is that *cumulative uncertainty at a few critical steps* carries more information about reasoning quality than average uncertainty or total uncertainty. This suggests that the distribution of entropy along a reasoning path is highly non-uniform, and conventional global metrics (average, total sum) dilute the signal. The paper also provides the surprising finding that negative samples in RL should be diverse rather than curated for simplicity—a nuance that challenges the straightforward application of any selection metric to negative data.

## Suggestions

- Report results with 3–5 random seeds for the RL experiments and indicate standard deviations. This is critical for convincing the reader that the modest gains are not noise.
- Provide a more principled justification for the 0.5% percentile, e.g., by analyzing the entropy distribution of typical reasoning paths and showing that this cutoff reliably isolates forking points.
- Discuss the limitation of HES for low-entropy correct solutions and propose potential mitigation (e.g., using HES only for pruning low-quality data, not for discarding all low-entropy content).

## Score and Decision

Score: 8  
Decision: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: Accept