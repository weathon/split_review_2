## Summary

This paper identifies a training-inference mismatch in tree-based speculative decoding: existing draft model training objectives (e.g., EAGLE, HASS) are sequence-based, while inference relies on tree-structured drafts. To address this, the authors propose TALF (tree-aware loss function), which aggregates cross-entropy losses over all nodes of a dynamically constructed tree during training, aligning the draft model’s predictions with the target LLM across branches. They also introduce SALF (stopping at low further gains), a dynamic tree construction algorithm with a provably monotonic early-stopping criterion that reduces drafting overhead. Combined, SALF & TALF achieve 15.6–39.4% and 6.5–24.4% end-to-end speedups over EAGLE-2 and HASS across multiple LLMs and benchmarks.

## Strengths

- **Clear problem identification and motivation.** The paper convincingly demonstrates (Figure 2) that existing training methods underperform on lower-ranked tokens, which constitute a non-negligible fraction of the draft tree, and that this mismatch hurts tree-based SpD performance.
- **Principled and well-designed solution.** TALF directly incorporates the tree structure into the training objective, and SALF provides a theoretically grounded early-stopping criterion (Theorem 1) that balances draft quality and overhead. Both contributions are simple yet effective.
- **Thorough and fair evaluation.** Experiments cover three LLM families (Llama-2, Llama-3.1, DeepSeek-R1-distill), five diverse benchmarks, both greedy and non-greedy sampling, and include ablation studies isolating the benefits of each component (Table 2). The training budget is controlled for fair comparison.
- **Consistent and significant improvements.** SALF & TALF outperform strong baselines (EAGLE-2, HASS) across every model and task, with mean speedups of 1.16–1.39× and 1.07–1.24× respectively. The gains are larger for stronger target models, where alignment is harder.
- **Reproducibility.** The paper provides code, detailed hyperparameters, and a reproducibility statement, making it easy to verify and build upon.

## Weaknesses

### Minor

- **Fixed tree structure during TALF training.** The tree used for training is precomputed by the target model and fixed across epochs. While this avoids repeated target model invocations, it may not reflect the draft model’s own tree distribution during inference. The paper acknowledges this but does not discuss potential negative effects or alternative strategies (e.g., iterative refinement).
- **SALF threshold tuning.** The SALF threshold \(th\) is a hyperparameter that requires tuning (default 0.6). Although sensitivity analysis is provided (Table 4), the paper does not offer a principled way to set it a priori or adapt it dynamically, which could limit practical deployment.
- **No regression loss in TALF.** Unlike EAGLE and HASS, TALF omits the feature regression loss. While experiments show this works well, the paper does not provide an ablation or theoretical justification for why feature alignment is unnecessary when using tree-aware classification loss.
- **Limited discussion of limitations.** The paper does not explicitly discuss scenarios where SALF & TALF might underperform (e.g., very short generation lengths, extremely small draft models, or tasks with highly peaked distributions).

### Trivial

- The notation in Algorithm 2 uses \(\mathcal{G}\) for both the output tree and the initial set; this is clear in context but could be slightly confusing on first read.

## Nice-to-Haves

- An adaptive SALF threshold that adjusts based on the current drafting iteration or model confidence could further improve robustness.
- Exploring whether TALF can be combined with other training objectives (e.g., adding a lightweight regression loss) might yield additional gains.
- A comparison with other recent tree-based SpD methods (e.g., Sequoia, AdaEagle) would strengthen the positioning, though the paper already compares with the most relevant baselines.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Discuss the potential impact of using a fixed training tree versus a dynamically updated one, and whether the draft model’s own tree could be used in a self-distillation loop.
- Provide guidance on setting the SALF threshold based on the target model’s acceptance rate or drafting overhead, perhaps as a function of the draft model’s calibration.

## Score and Decision

**Score:** 8  
**Decision:** Accept

The paper makes a clear, well-motivated contribution to an important problem (LLM inference acceleration). The proposed methods are simple, principled, and empirically validated with consistent improvements over strong baselines. The evaluation is thorough and the writing is clear. Minor weaknesses do not detract from the overall quality and impact.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>