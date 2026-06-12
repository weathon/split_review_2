## Summary

This paper introduces HARA (Hybrid Arithmetic-ReLU Networks Approximation), a unified framework that replaces diverse non-linear operators in Transformers (GELU, Softmax, LayerNorm, etc.) with a single canonical architecture composed of arithmetic primitives and a shallow ReLU network. The core algorithmic innovation is a dynamic-programming-based parameter initialization pipeline that systematically finds near-optimal parameters for the ReLU approximators, dramatically outperforming direct-training baselines. Hardware synthesis estimations project over 60% silicon area reduction for non-linear processing, and end-to-end evaluation across BERT, Swin, LLaMA, and Stable Diffusion shows negligible performance degradation (<0.1% change) with full 8-bit quantization compatibility.

## Strengths

- **Principled optimization pipeline with strong empirical validation**: The three-stage DP-based initialization pipeline (DP for optimal breakpoints → analytical PWL-to-ReLU conversion → fine-tuning) is algorithmically sound and demonstrably effective. Table 4 shows that DP-based initialization reduces MSE by 2-3 orders of magnitude over naive direct training, and the final fine-tuning stage further improves results by another order of magnitude. This is a genuine methodological contribution.

- **Comprehensive end-to-end evaluation across diverse architectures**: The paper validates on four architecturally diverse models spanning NLU (BERT on SQuAD v2.0), vision (Swin on ImageNet-1k), language generation (LLaMA 3.2-3B on WikiText-2), and text-to-image synthesis (Stable Diffusion 3.5 on SDCI), covering all major Transformer operator combinations (Table 2). Results consistently show <0.1% performance change, which is strong evidence for the framework's generality.

- **Clear problem motivation and hardware co-design framing**: The paper clearly articulates the "function-specific designs" and "suboptimal heuristic parameterization" gaps in existing work, and the unified architecture with reconfigurable URN blocks is a conceptually clean solution. The hardware synthesis estimation (Table 5) provides concrete projections of 62.3% area and 51.7% power savings.

- **Effective operator decomposition strategy**: The decomposition of Softmax and LayerNorm into chains of Pow2, Log2, and arithmetic operations (Equations 2-3) is mathematically elegant, reducing all complex non-linearities to just two primitive functions that can be approximated by the unified ReLU network.

## Weaknesses

### Fatal
None.

### Major

- **Hardware results are synthesis estimations, not physical implementations**: While the authors transparently acknowledge this limitation, the 60% area reduction claim is a central selling point of the paper. Without post-layout analysis or at least more detailed synthesis methodology (e.g., timing constraints, operating frequency, process corner assumptions), it is difficult to assess whether these projections would hold in practice. The comparison baseline (three separate specialized LUT-based units vs. one URN) also needs more justification—specifically, whether the specialized units were designed with comparable throughput/latency targets.

- **Missing computational cost and latency analysis**: The paper focuses on area and power but does not analyze latency or throughput implications. Softmax via HARA requires multiple sequential passes through the URN plus arithmetic operations (max, sub, sum, Pow2, Log2), which could introduce significant latency compared to a single dedicated Softmax unit. For edge deployment, latency is often as critical as area. A roofline or cycle-count analysis would substantially strengthen the hardware claims.

- **Fairness of baseline comparisons in Table 3**: The comparison with NN-LUT and RI-LUT is at the operator-level MSE only. Since these methods use different architectures (neural-network-generated LUTs vs. reconfigurable integer LUTs), the comparison should also account for equivalent hardware cost—i.e., how much area would NN-LUT or RI-LUT need to achieve similar MSE? As presented, HARA's advantage could partially stem from using a different (potentially more expensive) computational structure per approximation.

### Minor

- **The "(8,8,8)" configuration in Table 6 is under-specified**: The paper mentions "hidden dimension 8" but does not explain whether all operators use the same HD, whether this is optimal per operator, or how this configuration was selected. Given that Table 3 shows MSE varies significantly with HD, this choice deserves more discussion.

- **Fine-tuning stage details are sparse**: Stage 3 mentions using the Adam optimizer but provides no details on learning rate, number of epochs, training data (the full model's training data or synthetic samples?), or whether fine-tuning is done at the function-approximation level or end-to-end. This affects reproducibility.

- **Extensibility claims could be stronger**: The paper claims extensibility to new activation functions, but does not demonstrate this. A brief case study on a less common activation (e.g., GELU variants, Mish) would strengthen this argument.

### Trivial
None.

## Nice-to-Haves

- A latency analysis or at least a cycle-count comparison between HARA's multi-step Softmax/LayerNorm computation and dedicated hardware implementations.
- Sensitivity analysis of end-to-end model performance to hidden dimension of the ReLU network (e.g., HD=4 vs 8 vs 16) to guide hardware designers.
- A discussion of numerical precision requirements for the intermediate arithmetic operations in the Softmax/LayerNorm decomposition chains.

## Novel Insights

The paper's most novel insight is that the diverse non-linear operators in Transformers can be decomposed into a small set of primitive functions (Pow2, Log2, and arithmetic) that share a common approximation architecture, and that dynamic programming provides a principled, globally optimal strategy for fitting the ReLU approximators. The demonstration that this DP-based initialization is 2-3 orders of magnitude more accurate than direct training (Table 4) is a strong empirical finding that suggests the field's reliance on heuristic training for function approximation may be fundamentally misguided for high-fidelity requirements.

## Suggestions

- Add a latency/throughput analysis comparing HARA's multi-step computation for Softmax and LayerNorm against dedicated hardware implementations, since area savings alone do not capture the full picture for edge deployment.
- Provide more detail on the fine-tuning stage (learning rate, epochs, data source) for reproducibility, and consider releasing code.
- Include a comparison where NN-LUT and RI-LUT are given equivalent hardware budgets to assess whether HARA's accuracy advantage persists under resource parity.

## Score and Decision

The paper makes a clear and well-validated algorithmic contribution (DP-based initialization for unified ReLU approximation) and addresses an important practical problem (hardware-efficient Transformer deployment). The experimental validation is comprehensive across four diverse architectures. However, the central hardware claims rest on synthesis estimations without latency analysis, and some baseline comparisons lack resource-parity fairness. These issues prevent a higher score but do not invalidate the core contributions.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept