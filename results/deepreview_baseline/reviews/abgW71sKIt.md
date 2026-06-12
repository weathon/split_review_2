## Summary

This paper investigates why existing output-matching objectives for 1-bit post-training quantization of large language models often underperform. It identifies three key issues: (1) layer-wise output matching does not guarantee block-level loss reduction, (2) quantization errors accumulate across layers and cause the alignment target to drift, and (3) naive output matching degrades token-to-token interactions and attention patterns. Based on these insights, the paper proposes a method that applies output matching selectively (only to the last layer of each block), explicitly accounts for accumulated errors by using the full-precision input as the target, and introduces an Attention Matrix Preservation (AMP) mechanism to protect attention structure. Experiments across OPT and LLaMA model families and multiple benchmarks show consistent improvements over prior 1-bit PTQ methods.

## Strengths

- **Systematic analysis of why output matching fails in 1-bit PTQ**: The paper provides clear diagnostics—block-level loss comparison, error accumulation across depth, and token-similarity drift—that go beyond empirical observation and offer genuine explanatory value.
- **Well-motivated and targeted technical solutions**: Each of the identified issues is directly addressed: selective block-level application for the block-level problem, the output error objective for accumulated errors, and AMP for attention degradation. The design choices are clearly linked to the analysis.
- **Strong and consistent empirical results**: Across OPT (1.3B to 30B) and LLaMA-2/3 models, the method outperforms existing 1-bit PTQ baselines (BiLLM, PB-LLM, ARB-RC, ARB-X) on perplexity and zero-shot QA, with many improvements being substantial (e.g., >10 perplexity points on many settings). The ablation studies confirm the individual contributions of the output error objective and AMP.

## Weaknesses

### Fatal

None.

### Major

- **The derivation of the AMP objective (Equation 9) is mathematically unsound.** The paper writes:  
  \[
  \mathcal{L}_{AMP} = \left\| (\hat{X}\hat{W}\hat{W}^\top\hat{X}^\top) \odot (XWW^\top X^\top) \right\|
  \]  
  and then rewrites it as  
  \[
  \text{Tr} \left[ \hat{X}\hat{W}\hat{W}^\top\hat{X}^\top XWW^\top X^\top \right].
  \]  
  This is not correct: the Frobenius norm of an element-wise product is \(\sqrt{\sum (a_{ij}b_{ij})^2}\), not the sum of element-wise products (i.e., \(\text{Tr}[A^\top B]\)). The paper appears to conflate the two operations. As a result, the subsequent AMP optimizer (using gradients of this incorrectly defined objective) is not justified by the text. While the empirical results suggest that AMP helps, the presented mathematics does not support what is being optimized. This must be clarified or corrected to ensure the method is correctly understood and reproducible.

- **The selective layer-wise strategy is under-specified and potentially ambiguous.** The paper states that output alignment is applied only to "the last fully connected layer of each block." In a standard Transformer block, this could refer to either the second linear layer of the attention output or the output projection of the feed-forward network. The authors should explicitly state which layer within each block is targeted and provide the rationale. Moreover, the preliminary analysis in Figure 1 indicates that some layers actually **increase** block-level loss under output matching—does the method avoid those layers, or is "last layer" always safe? The paper does not discuss this.

- **A notable failure case is not analyzed.** On the PTB dataset for LLaMA-2-7B, the proposed method achieves perplexity 3166, which is much worse than ARB-X (681) and PB-LLM (657). The paper mentions this exception in passing but offers no explanation. Given that this is a significant degradation on a standard benchmark, an analysis (e.g., why PTB differs from C4/WikiText2) is necessary to understand the method’s limitations.

### Minor

- The paper claims "Our method consistently outperforms previous state-of-the-art quantization approaches across all benchmarks" but then acknowledges the PTB exception. The phrasing should be adjusted for accuracy.
- The AMP mechanism uses the sign of the gradient to create a hard mask that decides whether to use the closed-form solution or keep the current value. This is a strong heuristic; some justification (e.g., why sign is used instead of a continuous update) would be helpful.
- The derivation of the closed-form solution for \(\alpha_r\) involves solving \((\hat{S} \odot C) \alpha_r = \text{Diag}(SW \text{diag}(\alpha_c)B^\top)\) and then using the pseudoinverse. The paper notes numerical instability but does not discuss whether this affects the quality of the solution in practice.

### Trivial

None.

## Nice-to-Haves

- An analysis comparing the proposed output error objective with a block-wise (end-to-end) output matching would strengthen the claim that selective block-level application is sufficient.
- Ablation over different choices of which layer to quantize with output matching (e.g., all layers, first layer, last layer) would make the selective strategy more convincing.

## Novel Insights

Beyond the specific technical contributions (output error objective, AMP), the paper offers a principled understanding of why output alignment can backfire in 1-bit LLM quantization. In particular, the observation that naive output matching degrades token similarity matrices—and that architectures using RMSNorm (like LLaMA) are especially vulnerable because they depend on directional alignment—is a valuable design insight that could inform future work on quantization-aware training or other compression techniques. The analysis of block-level loss inconsistency (layer-wise improvement not translating to block-level improvement) is also a clean conceptual contribution.

## Suggestions

1. **Fix the AMP derivation.** Clearly define the quantity being maximized—likely the Frobenius inner product (dot product) of the two token-similarity matrices, i.e., \(\text{Tr}[(\hat{X}\hat{W}\hat{W}^\top\hat{X}^\top)^\top (XWW^\top X^\top)]\), not the norm of the element-wise product. Correct the equations and the subsequent gradient derivation accordingly.
2. **Provide a detailed explanation of the selective strategy.** Specify which layer(s) within a block receive output alignment and justify why the "last fully connected layer" is the correct choice based on block-level loss analysis.
3. **Analyze the PTB failure case.** Investigate whether the issue stems from distribution mismatch, numerical instability, or a property of the dataset, and discuss potential remedies or limitations.

## Score and Decision

The paper makes a valuable contribution by systematically identifying failure modes of output matching in 1-bit PTQ and proposing targeted fixes that yield consistent gains. The empirical validation is strong and covers a wide range of models and tasks. However, the mathematical error in the AMP derivation is a significant flaw that undermines the correctness of that component as presented. This issue is likely fixable, but in its current form it weakens the paper’s technical rigor. Given the overall strength of the analysis and results, the paper is close to acceptance but requires clarification of the AMP formulation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>