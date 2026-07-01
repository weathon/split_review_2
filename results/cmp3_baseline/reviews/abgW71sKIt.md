## Summary

This paper analyzes why naive output-matching objectives fail for 1-bit post-training quantization (PTQ) of LLMs, identifying three key issues: (i) layer-wise output matching does not guarantee block-level loss reduction, (ii) activation errors accumulate across layers, degrading the alignment target, and (iii) indiscriminate output matching disrupts token interactions and attention mechanisms. Building on these insights, the authors propose a selective block-level output alignment strategy that directly minimizes the true output error (using full-precision inputs) and introduces an Attention Matrix Preservation (AMP) mechanism to maintain token similarity structure. The method yields consistent perplexity and zero-shot accuracy improvements over existing 1-bit PTQ baselines on OPT and LLaMA models.

## Strengths

- **Thorough diagnostic analysis**: The paper clearly identifies and experimentally demonstrates three concrete failure modes of layer-wise output alignment in 1-bit LLM quantization—block-level discrepancy, error accumulation, and attention degradation—which provide valuable understanding for the community.
- **Sound technical solution**: The proposed reformulation of the quantization objective to minimize the true output error (using full-precision inputs rather than quantized activations) is principled, and the closed-form update derivations for parameters are well-presented.
- **Consistent empirical gains**: Across a range of model scales (1.3B to 30B for OPT, 7B/13B/8B for LLaMA) and multiple benchmarks (perplexity on three datasets, zero-shot QA), the method outperforms existing 1-bit PTQ approaches including weight-matching (ARB-RC) and output-matching (ARB-X) baselines.

## Weaknesses

### Fatal
None.

### Major

1. **Modest improvement over ARB-RC in many settings**: While the method beats ARB-X clearly, the advantage over ARB-RC (which uses only weight alignment) is often small—for example, on OPT-30B C4 perplexity 13.15 vs. 13.34 (ARB-RC), WikiText2 10.94 vs. 11.19, and PTB 16.75 vs. 16.88. This raises questions about how much of the gain comes from the output alignment formulation versus other design choices (e.g., selective application, AMP). A more direct ablation isolating the effect of output vs. weight alignment under the same selective/AMP framework would strengthen the claims.

2. **Problematic results on LLaMA-2-7B PTB**: The method obtains perplexity 3166 on PTB, which is dramatically worse than all baselines (e.g., ARB-X: 681.24, ARB-RC: 763.19, PB-LLM: 657.24). The paper mentions this anomaly but dismisses it by saying "the large perplexity indicates that the metric cannot provide a meaningful evaluation." This is unconvincing—if the metric is unreliable, it should be reported with caution or excluded, and the cause of this failure should be explained (e.g., numerical instability, outlier sensitivity, or a bug). This single result casts doubt on the robustness of the method.

3. **Heuristic nature of AMP**: The Attention Matrix Preservation mechanism (Eq. 9–11) is defined as maximizing the Frobenius inner product between quantized and full-precision token similarity matrices, then using the *sign of the gradient* as a binary mask for parameter updates. This design is ad hoc: (i) the token similarity matrix already appears implicitly in the output error objective; adding an explicit AMP term may double-count or conflate objectives, (ii) the binarized masking ("accept the closed-form update only when its gradient sign is positive") lacks theoretical justification and may introduce hard discontinuities. A simpler regularization or soft penalty approach could be more principled.

### Minor

- The selective layer-wise strategy (applying output alignment only to the last fully connected layer of each block) is empirically motivated but not deeply justified. Given that this is a key component (Algorithm 1, Appendix E), the paper would benefit from an ablation comparing different choices (e.g., all layers, first layer, random layer) to validate the claim that the last layer has the most direct impact.
- The zero-shot QA results (AveQA) show only marginal improvements (e.g., ARB-RC: 55.01, Ours: 55.06 for OPT-13B; ARB-RC: 57.11, Ours: 57.70 for OPT-30B). These differences are within standard error; reporting significance or confidence intervals would be more informative.

### Trivial

None.

## Nice-to-Haves

- An analysis of how the number of calibration samples affects performance, since the method is data-aware and uses full-precision inputs which may require more or different data.
- A discussion of whether the proposed Output Error objective requires storing full-precision activations (and thus more memory), and how this compares to the Activation-conditioned Error in practice.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that **output alignment for 1-bit quantization fails not because it is a poor objective but because it is applied naively**: (a) layer-wise optimality does not guarantee block-level optimality in transformer architectures, (b) conditioning on quantized activations introduces a moving target that deviates from the true full-precision behavior, and (c) the directional structure of token representations is more fragile than the Euclidean distance, making attention mechanisms particularly susceptible to quantization artifacts. This nuanced understanding could guide future PTQ design for extreme bit-widths.

## Suggestions

1. **Investigate and explain the LLaMA-2-7B PTB anomaly**: If the PTB evaluation for LLaMA-2-7B yields a perplexity of 3166, check for numerical instability (e.g., log-probability overflow, division by near-zero perplexity) or data preprocessing mismatch. Report results with and without the PTB entry, or replace it with a stable metric such as accuracy on a subset.
2. **Provide a cleaner ablation for output vs. weight alignment**: Design an experiment where the only variable is the alignment objective (Weight Error, Activation-conditioned Error, Output Error) while keeping the selective layer policy and AMP fixed. This would directly show the benefit of the proposed objective over ARB-X’s objective.
3. **Simplify or justify the AMP update rule**: Consider using a soft regularization term added to the main objective (e.g., λ * L_AMP) rather than hard masking via gradient signs. Report the sensitivity to λ.

## Score and Decision

Score: 6 (borderline accept). The paper provides a well-motivated analysis and a technically sound method that improves upon existing 1-bit PTQ approaches. However, the improvements are modest in many settings, and the anomalous PTB result for LLaMA-2-7B weakens confidence in robustness. The contribution is solid but not strong enough for a higher score.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>