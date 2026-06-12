## Summary

This paper investigates how compression methods (quantization, distillation, and pruning) affect the reasoning capabilities of Large Reasoning Models (LRMs), specifically DeepSeek-R1 and its distilled variants. The authors conduct extensive benchmarking across four reasoning datasets and employ mechanistic interpretability techniques (difference of means and attribution patching) to identify which specific weight matrices are most critical for reasoning. Their key findings include: (1) weight count impacts knowledge memorization more than reasoning, (2) the MLP up projection in the final layer of distilled LRMs is among the most important components, and (3) current quantization methods overly compress final-layer modules and MLP gate projections, where protecting just 2% of weights can improve accuracy by 6.57%.

## Strengths

- **Comprehensive empirical evaluation**: The paper benchmarks an impressive breadth of compression methods (dynamic quantization, AWQ, GPTQ, GPTAQ, ANY4/3, distillation, SparseGPT, AlphaPruning) across multiple model sizes (7B-671B) and four diverse reasoning datasets, providing the most thorough assessment of compressed LRMs in the literature.

- **Novel mechanistic interpretation methodology**: Adapting difference of means and attribution patching to compute fine-grained weight importance scores for individual linear modules (rather than just layer-level analysis) is a principled and valuable contribution that addresses the fundamental question of locating critical weights for compression.

- **Actionable findings with empirical validation**: The discovery that the final-layer MLP up projection is critical, and that protecting just 2% of weights can yield 6.57% average accuracy improvement over state-of-the-art quantization, provides clear, practical guidance for future compression research.

- **Generalizability claims supported**: The paper demonstrates that key findings generalize across both R1 and non-R1 model families (Llama and Qwen), strengthening the broader impact of the work.

## Weaknesses

### Fatal
None.

### Major
- **Limited behavioral annotation validation**: The annotation of four reasoning behaviors (backtracking, uncertainty estimation, example testing, adding knowledge) relies entirely on GPT-4o with only 120 instances total (30 per dataset). While Appendix G mentions robustness, this is a small annotation set for drawing fine-grained causal conclusions about weight importance, and GPT-4o's ability to reliably identify these specific reasoning behaviors is not rigorously validated against human annotations.

- **Inconsistent alignment between behavioral analysis and key claims**: The paper's most significant findings (importance of final-layer up_proj, excessive compression of gate projections) are presented as general observations about reasoning, but the behavioral breakdown shows these patterns vary significantly across the four reasoning behaviors (e.g., 32_up importance shift is minimal for uncertainty estimation but large for backtracking). The paper does not adequately reconcile this variation with the claim that these are unified "reasoning capabilities."

- **Pruning analysis is superficial**: Despite including pruning in the claimed scope, the pruning experiments are limited to 50% sparsity in the main table and SparseGPT/AlphaPruning analysis is relegated to Appendix I. Given that pruning shows severe degradation (50% sparsity collapses performance on AIME), the paper's claim that pruning effects appear "very similar to quantization effect" requires stronger evidence.

### Minor
- **The interpretability framework's assumptions need clarification**: The decision to set all increases in relative importance to zero (Section 2.3) is justified as "since it is more informative to track cases where the RI decreases," but this choice fundamentally shapes all subsequent visualizations and could mask important compensatory dynamics in compressed models.

- **Selective protection experiment is limited**: The validation in Section 5.2 only tests protection of final-layer MLP modules on one model (R1-Distill-Llama-8B) with one quantization method (AWQ). Testing on additional models and quantization methods would strengthen the generalizability of the claim that "protecting just 2% of all weights... can raise average accuracy by 6.57%."

### Trivial
None.

## Nice-to-Haves
- Including a baseline of random weight protection to demonstrate that the identified important weights are genuinely special would strengthen the causal claims.
- Providing human annotation validation for the behavioral labeling, even on a small subset, would increase confidence in the interpretability pipeline.
- A practical recommendation section summarizing which compression method to use under different resource constraints and task types would increase practical utility.

## Novel Insights

The paper's key insight emerges from the intersection of mechanistic interpretability and model compression: that weight importance in compressed LRMs is not uniformly distributed, and current state-of-the-art quantization methods systematically over-compress the very components (final-layer MLP projections and gate projections) that distillation makes most critical for reasoning. This reveals a fundamental misalignment between what compression algorithms optimize for (per-layer error minimization) and what actually matters for preserving reasoning capability. The finding that distillation essentially rewires the model to concentrate reasoning capability in specific late-layer components, which compression methods then inadvertently damage, suggests that compression-aware fine-tuning or mixed-precision strategies could yield substantial improvements without additional parameters.

## Suggestions
- Expand the selective protection validation to include at least one additional quantization method (GPTQ) and one additional model (R1-Distill-Qwen-7B) to strengthen the generalizability of the quantitative improvement claims.
- Provide a more detailed analysis of whether the four reasoning behaviors show consistent or divergent patterns of weight importance, and discuss how this affects the paper's unified conclusions about "reasoning capabilities."

## Score and Decision
MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>