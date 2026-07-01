## Summary

This paper introduces Weight-Activation Subspace Iteration (WASI), a method for efficient fine-tuning of transformer models under resource constraints. WASI jointly compresses both model weights and activation maps into low-rank subspaces using SVD and subspace iteration, leveraging the observation that the essential information in both weights and activations resides in stable low-dimensional subspaces during fine-tuning. The method achieves up to 62× memory reduction and 2× FLOPs reduction compared to vanilla training, with approximately 1.4× speedup on a Raspberry Pi 5, while maintaining competitive accuracy across vision transformer models and even a small language model.

## Strengths

- **Novel unified framework**: WASI is the first method to jointly compress both weights and activations in a low-rank subspace during training, addressing both major memory bottlenecks in backpropagation simultaneously. This is a clear advance over prior work that focused on either weights (LoRA, SVD-LLM) or activations (ASI, AMC) separately.

- **Strong empirical results**: The paper demonstrates substantial memory savings (up to 62×) and computational reductions (up to 2×) with minimal accuracy loss across multiple architectures (ViT, SwinT, TinyLlama) and datasets. The on-device latency experiments on Raspberry Pi 5 provide compelling real-world validation.

- **Theoretical grounding**: The paper provides a clear motivation based on the stability of parameter subspaces during fine-tuning, supported by prior theoretical work (Aghajanyan et al., 2020; Li et al., 2018) and validated through their own experiments in Section 4.2.

- **Comprehensive evaluation**: The method is tested across multiple vision transformer architectures, multiple datasets, and even extended to a small language model (TinyLlama), demonstrating generality beyond the primary focus on vision transformers.

## Weaknesses

### Major

- **Limited comparison with parameter-efficient fine-tuning (PEFT) methods**: The paper compares WASI primarily against ASI, SVD-LLM, and vanilla training, but does not include comparisons with widely-used PEFT methods like LoRA, AdaLoRA, or DoRA. Given that LoRA is a dominant approach for efficient fine-tuning of transformers, the lack of direct comparison (especially on TinyLlama) weakens the claim that WASI is superior for resource-constrained training. The paper mentions LoRA's drawbacks (adapter overhead, no inference speedup) but does not empirically demonstrate WASI's advantages over it.

- **Missing details on the dynamic programming strategy for rank selection**: The paper mentions in Section 3.3 that WASI uses "a dynamic-programming strategy that determines r_i by minimizing memory usage under a target pre-tuning perplexity" but provides no details on how this works, what the optimization objective is, or how it compares to the fixed-budget approach of ASI. This is a non-trivial algorithmic contribution that is not adequately described.

- **Unclear how WASI handles non-linear layers and normalization layers**: The method focuses on linear layers in MLP blocks, but transformer models also contain attention layers, layer normalization, and other non-linear operations. The paper mentions "extended results with attention layers in Appendix B.3" but does not explain how WASI is applied to these components. This is a significant gap in the method description.

### Minor

- **The TinyLlama experiment is limited**: Only the last 5 layers are fine-tuned with a very low ε=0.1, and only one dataset (BoolQ) is used. This is insufficient to demonstrate that WASI generalizes well to language models. The accuracy range (64-66%) is also quite narrow, making it hard to assess meaningful differences.

- **The assumption of equal rank for weights and activations in Section 3.4 is unrealistic**: The analysis assumes the same optimal rank for both weights and activations, but in practice these are likely different. The analysis would be more informative if it considered separate ranks.

- **No discussion of training time overhead from subspace iteration**: While the paper reports FLOPs reductions, it does not discuss the actual wall-clock time overhead of performing subspace iteration (Algorithm 1) during training, which could be significant on resource-constrained devices.

### Trivial

- Figure 2 is difficult to parse with four overlapping curves and logarithmic scales; the caption is also overly long and contains redundant information.

## Nice-to-Haves

- A comparison with LoRA and its variants (e.g., AdaLoRA, DoRA) on the same vision transformer tasks would significantly strengthen the paper.
- An ablation study showing the contribution of weight compression vs. activation compression separately would help understand which component drives the gains.
- A discussion of how the method handles the attention mechanism (Q, K, V projections) would make the method more complete.

## Novel Insights

The key insight—that both weight and activation subspaces remain stable during fine-tuning and can be jointly exploited for compression—is genuinely novel and well-supported by the experiments. The observation that subspace iteration can be applied to weights (not just activations as in prior work) and that this does not degrade convergence is a non-trivial finding. The paper also provides a useful theoretical connection between the stability of parameter subspaces during fine-tuning and the feasibility of reusing low-rank decompositions across iterations.

## Suggestions

- Add a comparison with LoRA (or a variant like AdaLoRA) on at least one vision transformer task and the TinyLlama experiment. This is the most important missing baseline.
- Provide a clear description of the dynamic programming strategy for rank selection, including the optimization objective and algorithm.
- Clarify how WASI handles attention layers, normalization layers, and other non-linear components in transformers.
- Report actual wall-clock training time (not just FLOPs) for the simulation experiments to complement the Raspberry Pi results.

## Score and Decision

The paper presents a novel and well-motivated method with strong empirical results. The main weakness is the lack of comparison with widely-used PEFT methods like LoRA, which limits the ability to assess WASI's relative advantages. However, the core contribution—joint weight-activation subspace compression—is significant and the experiments are otherwise thorough. The paper is above the acceptance threshold but has room for improvement.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>