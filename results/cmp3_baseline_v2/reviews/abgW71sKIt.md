## Summary

This paper studies 1-bit post-training quantization (PTQ) for large language models. It identifies three key issues with naive output-matching quantization objectives: (1) layer-wise output alignment does not guarantee block-level loss reduction, (2) activation errors accumulate across layers and degrade alignment quality, and (3) output alignment can disrupt token interactions and attention mechanisms. The authors propose a selective, block-level output alignment strategy that accounts for accumulated errors and introduces an Attention Matrix Preservation (AMP) mechanism to maintain token similarity structure. Experiments on OPT and LLaMA models show consistent perplexity and zero-shot accuracy improvements over existing 1-bit PTQ methods including ARB-RC, ARB-X, BiLLM, and PB-LLM.

## Strengths

- **Thorough diagnostic analysis.** The paper provides clear empirical evidence (Figures 1 and 2) that layer-wise output matching does not always reduce block-level loss, that activation-conditioned errors diverge from true output errors as depth increases, and that quantization distorts token similarity matrices. This analysis is valuable for understanding limitations of existing PTQ objectives.
- **Novel AMP mechanism.** The attention matrix preservation objective is a well-motivated addition: the observation that RMSNorm-based models (LLaMA) are especially sensitive to token-direction changes, and the AMP design directly addresses attention degradation without requiring full attention-layer quantization.
- **Consistent improvements across multiple architectures and sizes.** The method outperforms all baselines on OPT (1.3B–30B) and LLaMA-2/3 models on C4, WikiText-2, and zero-shot QA benchmarks, with gains of 0.5–4.8 perplexity points over the next-best method (ARB-RC) in many settings.

## Weaknesses

### Fatal
None.

### Major

1. **Modest and sometimes inconsistent gains.** On larger models (OPT-30B, LLaMA-2-13B) the improvement over ARB-RC is often less than 1 perplexity point (e.g., OPT-30B WikiText-2: 10.94 vs 11.19; LLaMA-2-13B C4: 13.8 vs 14.77). For LLaMA-2-7B on PTB, the method yields 3166 perplexity, which is dramatically worse than ARB-RC (763) – the authors dismiss this as “not meaningful,” but this is a clear failure case that contradicts the claim of consistent improvement.

2. **Heuristic nature of AMP.** The AMP mechanism blends optimal closed-form solutions with current solutions using the sign of the gradient. No theoretical justification is given for why this mixing preserves attention patterns, nor is there an analysis of convergence or how the mask magnitude might affect optimization. The ablation shows it is critical (especially for LLaMA), but the design seems ad hoc.

3. **Selective layer application is under-justified.** The paper applies output alignment only to the last fully connected layer of each block, while using weight alignment for other layers. The justification (“it has the most direct impact on the block loss”) is stated without supporting evidence or ablation on which layer to select. This choice may be architecture-specific and not generalizable.

### Minor

- The effective bit width is 1.06–1.11 bits (due to row/column scaling), not exactly 1-bit. This is clearly stated and acceptable for the “1-bit” family, but the title could be more precise.
- The paper uses multiple closed-form updates and iterative optimization; runtime overhead is mentioned only briefly in the appendix (stripped). Without seeing it, it is hard to assess practical deployment cost.

### Trivial

- None.

## Nice-to-Haves

- An ablation comparing different layer-selection strategies within a block (e.g., attention vs. FFN, or multiple layers) would strengthen the selective alignment claim.
- A theoretical or empirical analysis of why AMP works (e.g., gradient alignment with attention preservation) would improve the paper.

## Novel Insights

None beyond the paper’s own contributions. The observation that output matching degrades token similarity in RMSNorm-based architectures is a useful practical insight that could guide future PTQ design.

## Suggestions

- Address the PTB failure case for LLaMA-2-7B: provide analysis or a simple fix (e.g., falling back to weight alignment for the problematic blocks).
- Provide an ablation on which layer(s) in a block to apply output alignment, to justify the “last FC layer” heuristic.
- Include convergence analysis or a stopping criterion for the iterative optimization.

## Score and Decision

**Score:** 4.0  
**Decision:** Reject  

**Reasoning:** The paper presents a solid diagnostic study and a technically reasonable method, but the empirical gains are often marginal and one significant failure case (LLaMA-2-7B PTB) undermines the consistency claims. The AMP mechanism, while effective, is introduced heuristically without rigorous justification. The selective layer choice is under-explored. Overall, the contributions are incremental relative to the strong baselines (especially ARB-RC), and the paper does not convincingly demonstrate that the proposed approach is a reliable step forward for 1-bit LLM quantization. A borderline reject is appropriate given the gap between the claimed improvements and the actual results.

MY FINAL SCORE: <score>4.0</score>  
MY FINAL DECISION: <decision>Reject</decision>