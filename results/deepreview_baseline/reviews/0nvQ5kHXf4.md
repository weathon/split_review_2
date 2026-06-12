## Summary

This paper introduces Weight-Activation Subspace Iteration (WASI), a method for efficient fine-tuning of transformer models under resource constraints. WASI jointly compresses both weight matrices and activation maps into low-rank subspaces using subspace iteration, leveraging the observation that the essential information in model parameters remains in a stable subspace throughout fine-tuning. The method achieves up to 62× memory reduction and 2× FLOPs reduction during training while maintaining competitive accuracy, with demonstrated speedups on a Raspberry Pi 5.

## Strengths

- **Novel unified framework**: WASI is the first method to jointly compress both weights and activations during training using subspace iteration, addressing the two primary memory bottlenecks in backpropagation simultaneously. This is a principled extension of prior work (ASI) that only compressed activations.

- **Strong empirical results**: The method demonstrates impressive memory savings (up to 62×) and computational reductions (up to 2×) while maintaining accuracy comparable to vanilla training across multiple vision transformer architectures and datasets. The on-device latency results on Raspberry Pi 5 (1.4× speedup) provide concrete evidence of practical utility.

- **Theoretical grounding**: The paper provides a clear motivation based on the stability of parameter subspaces during fine-tuning, supported by empirical validation (Figure 3a showing stable singular values across epochs). The explained variance threshold ε provides a principled way to control information loss.

- **Comprehensive evaluation**: Experiments cover multiple architectures (ViT, SwinT, TinyLlama), multiple datasets (CIFAR-10/100, CUB, Flowers, Pets, BoolQ), and include both simulated resource measurements and real on-device latency benchmarks.

## Weaknesses

### Fatal
None.

### Major

- **Incomplete comparison with LoRA-based methods**: The paper compares against SVD-LLM but does not directly compare against standard LoRA or its variants (e.g., LoRA+, AdaLoRA) for the vision transformer tasks. Since LoRA is the most widely used parameter-efficient fine-tuning method, its absence as a baseline weakens the claim that WASI is superior to "state-of-the-art methods." The paper mentions LoRA's drawbacks (adapter memory overhead, no inference speedup) but does not empirically demonstrate that WASI outperforms LoRA in the same settings.

- **Limited evaluation on language models**: The TinyLlama experiment (Figure 7) uses only ε=0.1 and fine-tunes only the last 5 layers, which is a very limited setting. The accuracy improvement over vanilla is marginal (~1%), and the comparison is only against vanilla training, not against LoRA or other LLM fine-tuning methods. This makes the claim of generality to language models weak.

- **Missing ablation studies**: The paper does not ablate the contribution of WSI (weight compression) vs. ASI (activation compression) separately. It would be valuable to know how much of the memory/FLOPs savings come from each component and whether the joint approach is necessary or if activation compression alone (ASI) is sufficient for most of the gains.

- **Unclear practical memory measurement**: The paper reports "memory usage" but does not clearly specify whether this is peak memory, total allocated memory, or something else. For on-device deployment, peak memory is the critical metric, and the paper should clarify this. Additionally, the 62× memory reduction claim seems to be for specific layers only (linear layers in MLP blocks), not the entire model, which could be misleading.

### Minor

- **The subspace stability assumption is only validated for one setting**: Figure 3a shows stability for one layer (W6) of ViT on Pets. It would be stronger to show this across multiple layers and datasets.

- **The dynamic programming strategy for rank selection is mentioned but not detailed**: The paper states that ASI is redesigned with a dynamic-programming strategy for rank selection (Appendix A.2), but the appendix is not included in the review. This makes it difficult to assess the novelty and correctness of this contribution.

- **The TinyLlama experiment uses a very low ε=0.1**: This is far below the range used for vision experiments (0.4-0.9), making direct comparison difficult. The paper should explain why such a low threshold was chosen.

### Trivial
- The paper claims "100× higher memory efficiency than SVD-LLM" in Section 4.3, but this appears to be a specific data point rather than a general claim, and the phrasing could be clearer.

## Nice-to-Haves

- Include LoRA as a baseline in the vision transformer experiments to strengthen the comparison against parameter-efficient methods.
- Provide an ablation study separating the contributions of WSI and ASI.
- Clarify the memory measurement methodology (peak vs. total) and report peak memory savings for the entire model, not just selected layers.
- Extend the TinyLlama experiments with a wider range of ε values and more layers to demonstrate generality more convincingly.

## Novel Insights

None beyond the paper's own contributions. The key insight—that both weights and activations can be jointly compressed using subspace iteration due to the stability of their low-rank subspaces during fine-tuning—is a natural extension of prior work (ASI for activations, SVD-based weight compression). The paper's main novelty is in combining these ideas into a unified framework and demonstrating its effectiveness for transformer models on edge devices.

## Suggestions

- Add LoRA and/or AdaLoRA as baselines in the main vision experiments (Figures 5 and 6) to provide a more complete comparison against parameter-efficient fine-tuning methods.
- Include an ablation study where WASI is compared against (a) WSI only (weight compression, no activation compression) and (b) ASI only (activation compression, no weight compression) to quantify the contribution of each component.
- Clarify the memory measurement: specify whether reported values are peak memory, average memory, or total allocated memory, and report savings for the entire model (not just linear layers) where possible.
- For the TinyLlama experiment, run with a wider range of ε values (e.g., 0.4-0.9) and fine-tune more layers to provide a more convincing demonstration of generality to language models.

## Score and Decision

The paper presents a novel and well-motivated method for resource-constrained training of transformers, with strong empirical results on vision tasks and promising on-device performance. However, the lack of comparison against LoRA-based methods and the limited evaluation on language models weaken the claims of generality and superiority over state-of-the-art. The paper is a solid contribution to the on-device learning and efficient training literature, but the weaknesses prevent it from being a top-tier paper.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>