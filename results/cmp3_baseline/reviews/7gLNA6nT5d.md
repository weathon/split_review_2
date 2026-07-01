## Summary

This paper proposes integrating n-gram induction heads into transformers for in-context reinforcement learning (ICRL), building on Algorithm Distillation (AD). The authors claim that n-gram attention patterns reduce the amount of data required for generalization, ease hyperparameter sensitivity, and can be extended to pixel-based observations via vector quantization. Experiments on Dark Room, Key-to-Door, and Miniworld environments show improvements over the AD baseline in low-data and low-diversity settings.

## Strengths

- The motivation is well-grounded: prior work shows that transformers exhibit simplicity bias and that induction heads (including n-gram patterns) are central to in-context learning. Hardcoding these patterns is a sensible way to accelerate training and improve data efficiency.
- The paper addresses a practical bottleneck in ICRL—the high cost of collecting diverse learning histories—and proposes a model-centric solution rather than a data-centric one.
- The evaluation protocol using Expected Maximum Performance (EMP) with random hyperparameter search is appropriate for demonstrating robustness and ease of tuning.
- The extension to visual observations via vector quantization is a reasonable first step toward applying n-gram matching in continuous state spaces.

## Weaknesses

### Major

1. **Incomplete experimental evidence.** The paper repeatedly refers to figures and appendices that are not present in the provided content (e.g., Figure 2, Figure 4, Appendix B, Appendix C, Appendix D). The core claims about data efficiency (27× reduction) and hyperparameter sensitivity rely on these missing details. Without seeing the actual curves and the justification for the 27× factor, the results cannot be properly evaluated.

2. **Weak baseline comparison.** The paper only compares against Algorithm Distillation (AD). Other ICRL methods (e.g., Lee et al. 2023, retrieval-augmented approaches) are not considered, making it unclear whether the proposed n-gram heads offer a general advantage or are specific to AD. The contribution would be stronger with a broader set of baselines.

3. **Limited task complexity.** Experiments are confined to simple grid-world environments (Dark Room, Key-to-Door) and a small 3D environment (Miniworld). The paper does not demonstrate scalability to more challenging domains (e.g., XLand-Minigrid, Meta-World) where data efficiency and hyperparameter sensitivity are more critical. The conclusion acknowledges this limitation, but it significantly weakens the impact.

4. **Unclear hyperparameter search details.** The paper states that hyperparameter assignments are varied over “core transformer hyperparameters that do not change the parameter count,” but the exact search space is relegated to the missing Appendix C. Without this information, the results are not reproducible, and the claim that n-gram layers reduce sensitivity is not fully substantiated.

### Minor

5. **Discrepancy in ablation results.** Table 1 shows EMP values around 0.7 for n-gram length and position ablations, while Figure 5 reports near-optimal returns (~0.96) for the n-gram method on Miniworld-Dark. The paper does not explain this gap, leaving the reader unsure whether the n-gram layer is consistently beneficial or only under specific conditions.

6. **Lack of computational cost analysis.** The paper does not discuss the additional memory or time overhead of the n-gram attention mechanism compared to standard multi-head attention. This is important for practitioners considering the method.

7. **Ambiguity in n-gram matching for discrete observations.** The paper describes two approaches (matching full transitions or just states) but does not specify which is used in each experiment or whether the choice affects performance.

### Trivial

- The paper contains repeated figure captions and some unclear phrasing (e.g., “transitivity of the in-context ability” likely meant “transient nature”), but these are minor and do not affect the scientific evaluation.

## Nice-to-Haves

- An analysis of when n-gram matching fails (e.g., in stochastic environments or with partial observability) would strengthen the paper.
- A comparison of the n-gram layer with other architectural modifications that improve in-context learning (e.g., different attention biases or gating mechanisms) would help contextualize the contribution.

## Novel Insights

None beyond the paper’s own contributions. The idea of hardcoding n-gram induction heads is borrowed from Akyürek et al. (2024) and applied to ICRL; the main novelty is the application domain and the use of VQ for visual observations. The paper does not provide new theoretical understanding of why n-gram heads help in RL specifically.

## Suggestions

- Provide the missing figures and appendices in the main paper or supplement. The 27× data efficiency claim must be clearly justified with a direct comparison to the original AD results.
- Include at least one additional ICRL baseline (e.g., Lee et al. 2023 or a retrieval-augmented method) to demonstrate generalizability.
- Report the computational overhead (FLOPs, memory) of the n-gram layer relative to standard attention.
- Clarify the hyperparameter search space and the exact n-gram matching strategy used in each experiment.

## Score and Decision

**Score:** 4  
**Decision:** Reject

The paper addresses an interesting and relevant problem, and the proposed approach is well-motivated. However, the experimental evidence is incomplete due to missing figures and appendices, the baseline comparison is too narrow, and the evaluation is limited to simple environments. These issues prevent the paper from making a convincing case for acceptance at a top venue like ICLR.

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>