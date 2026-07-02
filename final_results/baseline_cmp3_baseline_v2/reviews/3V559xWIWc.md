## Summary

This paper identifies a training-inference misalignment in tree-based speculative decoding (SpD): existing draft model training objectives treat the draft as a linear sequence, while inference uses a tree of candidate tokens. The authors propose two complementary solutions. TALF (Tree-Aware Loss Function) trains the draft model by aggregating cross-entropy losses over all nodes of a tree pre-constructed by the target model, thereby aligning training with tree-based inference. SALF (Stopping at Low Further Gains) is a principled early-stopping criterion for dynamic tree construction during inference that reduces drafting overhead while preserving tree quality. Combined, SALF&TALF achieve 15.6–39.4% and 6.5–24.4% end-to-end speedups over the state-of-the-art EAGLE-2 and HASS across multiple LLMs and benchmarks.

## Strengths

- **Clear problem identification with supporting evidence.** The paper demonstrates quantitatively (Figure 2) that prior draft models (EAGLE, HASS) perform substantially worse on lower-ranked candidate tokens, which constitute a non-negligible fraction of nodes in a draft tree. This directly motivates TALF.
- **Sound and well-motivated method.** TALF is a natural extension: if inference uses trees, training should optimize over trees. The use of the target model to generate a fixed tree during training is practical and avoids costly per-epoch re-generation. SALF is a simple but effective heuristic with a provable monotonicity guarantee (Theorem 1), and it demonstrably trades off tree quality for drafting overhead.
- **Comprehensive and well-designed experiments.** The evaluation covers three LLM families (Llama-2, Llama-3, DeepSeek-R1-Distill) across five benchmarks under both greedy and temperature=1 decoding. Ablation studies (Table 2) isolate the individual contributions of SALF and TALF, and parameter sensitivity analyses (Tables 3, 4) explore the impact of top-k and SALF threshold.
- **Consistent and practically meaningful improvements.** Across all settings, SALF&TALF outperform both baselines, with mean speedups of 1.16–1.39× over EAGLE-2 and 1.07–1.24× over HASS. The gains are larger for stronger target models (DeepSeek) where draft alignment is harder.
- **Reproducibility.** Code and detailed experimental setup are provided.

## Weaknesses

### Fatal
None.

### Major
1. **The training tree is fixed and precomputed by the target model.** The paper acknowledges this limitation (to avoid repeated expensive target model calls) but does not analyze whether the fixed tree structure leads to a distribution shift relative to the trees encountered during inference (which are built by the draft model). While the strong empirical results suggest this is not a critical problem, the potential gap deserves discussion or an ablation (e.g., using a held-in train set vs. a different distribution for tree generation).

2. **Comparison to HASS training may be imperfectly controlled.** For Llama-2 and Llama-3, the authors start from an EAGLE-trained checkpoint and then do additional training with HASS or TALF for three epochs. This could give TALF an advantage because it starts from a better initialization. For DeepSeek, they train each method from scratch for the same wall-clock time, which is fairer but still relies on the claim that HASS training is slower (due to sequential processing). The paper should report the actual training cost (e.g., GPU-hours) and show that TALF is at least as efficient as HASS to reach a given performance.

3. **The “optimal tree search” baseline may not match SpecExec.** The paper claims that Algorithm 2 without SALF (the red blocks) guarantees finding the highest-probability nodes. However, SpecExec’s optimal tree construction method (Svirschevski et al., 2024) uses a different algorithm (marginal probability decomposition). The paper should clarify whether the implemented baseline is exactly the same as SpecExec’s method or a simplified version, and discuss any differences. The speedup comparison against SpecExec (as a published method) is missing, though the paper does compare against EAGLE-2 and HASS.

### Minor
1. **Theorem 1 is relatively straightforward.** The decreasing sum of probabilities of top-B nodes at each depth follows intuitively from the fact that children’s probabilities are multiplicative and the product is ≤ the parent’s probability. The formal proof is appreciated but the claim is not surprising; this does not detract from the usefulness of SALF.

2. **Default SALF threshold th=0.6 is suboptimal on DeepSeek.** Table 4 shows that th=0.5 yields a higher mean speedup (2.62× vs. 2.59×). The paper acknowledges this and suggests future work on dynamic thresholding, but the default choice could be better justified or tuned per model.

3. **No quantitative verification of generation quality.** While speculative decoding with rejection sampling is theoretically lossless, it would be reassuring to report task accuracy (e.g., HumanEval pass@1, GSM8K accuracy) to confirm that the speedups do not come from altered output distributions.

### Trivial
- The ordering of SALF and TALF in the title (alphabetical) is slightly confusing given that SALF is discussed second.
- Some figure captions are long and repeat the in-text description; this is a formatting issue, not a content problem.

## Nice-to-Haves

- An analysis of how much training time is spent on target-model tree generation vs. draft model training, to help practitioners assess the overhead.
- A comparison with other recent dynamic tree construction methods (e.g., AdaEagle, Sequoia) beyond just beam search and optimal search.
- A study on sensitivity to the tree depth and branching factor (N, k) for SALF, similar to the threshold analysis.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that tree-based speculative decoding demands a training objective that explicitly accounts for branching alternatives, because draft errors on lower-ranked tokens propagate to deeper nodes and reduce effective acceptance length. The paper convincingly shows that sequence-level distillation (even with feature feedback like HASS) is insufficient and that a tree-level loss (TALF) yields calibrated probability estimates on all branches. This principle likely generalizes to other structured prediction tasks where beam search or tree-structured exploration is used.

## Suggestions

- Clarify whether the “optimal tree search” baseline (Algorithm 2 without SALF) is equivalent to the method in SpecExec, or provide a direct comparison to the original SpecExec implementation.
- Include a small-scale experiment where TALF is trained with a dynamically grown tree (updated each epoch) to measure the impact of the fixed-tree approximation.
- Report task-specific accuracy (e.g., pass@1 for HumanEval, accuracy for GSM8K) for all methods to confirm no quality degradation.

## Score and Decision

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>