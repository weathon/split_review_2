## Summary

This paper proposes Quantized Zeroth-order Optimization (QZO), a method that combines zeroth-order optimization with model quantization to enable memory-efficient fine-tuning of large language models. QZO eliminates gradients and optimizer states by using zeroth-order optimization, and reduces weight memory via quantization, by perturbing continuous quantization scales rather than discrete quantized weights. The method also introduces directional derivative clipping (DDC) to stabilize training, and demonstrates up to 18x memory reduction compared to full-precision fine-tuning, enabling fine-tuning of Llama-2-13B on a single 24GB GPU.

## Strengths

- **Novel and practical approach to extreme memory reduction**: The core idea of perturbing quantization scales rather than discrete weights is a clever solution to the fundamental incompatibility between zeroth-order optimization and quantized weights. This enables a unified framework that simultaneously reduces memory for weights, gradients, and optimizer states, achieving an impressive 18x memory reduction over 16-bit fine-tuning.

- **Strong empirical results across multiple architectures and tasks**: QZO consistently outperforms quantized zero-shot baselines and performs on par with MeZO (which uses 16-bit models) across OPT-6.7B, Llama-2-7B, and Llama-3.1-8B on five NLP benchmarks. The method also shows effectiveness under extreme 2-bit quantization on Llama-2-13B, demonstrating practical utility for resource-constrained settings.

- **Comprehensive ablation and analysis of DDC**: The paper provides both theoretical justification (variance reduction proof) and empirical validation (Figure 2 and 3) for the directional derivative clipping mechanism, showing it is essential for training stability and relatively robust to the choice of clipping threshold.

- **Orthogonality to existing quantization methods**: QZO is compatible with both scalar-based (GPTQ) and codebook-based (AQLM) post-training quantization methods, making it a versatile plug-and-play solution.

## Weaknesses

### Major

- **Limited comparison to parameter-efficient fine-tuning (PEFT) methods**: The paper compares QZO primarily against full fine-tuning and MeZO, but does not include comparisons with widely-used PEFT methods like LoRA or QLoRA (Dettmers et al., 2023) that also achieve significant memory reduction. Since QZO fine-tunes only quantization scales (~50M parameters vs 6.7B), it is essentially a parameter-efficient method, and the community would benefit from understanding how it compares to established PEFT approaches in terms of both memory and performance.

- **No evaluation on more challenging or larger-scale tasks**: The experiments are limited to relatively small datasets (1,000 training examples) and simple tasks. The paper does not evaluate on more complex generation tasks (e.g., instruction following, summarization on larger datasets) where the limitations of zeroth-order optimization might be more apparent. This makes it difficult to assess the practical utility of QZO for real-world fine-tuning scenarios.

- **Missing analysis of computational overhead**: While the paper reports FLOPs and memory, it does not provide wall-clock time comparisons. Zeroth-order methods require two forward passes per step, and QZO's perturbation of quantization scales may introduce additional overhead. Without timing data, it is unclear whether the memory savings come at a prohibitive computational cost.

### Minor

- **The theoretical contribution of DDC is limited**: The variance reduction proof (Eq. 7-8) is straightforward given the definition of clipping (d'^2 ≤ d^2). The unbiasedness claim (Theorem 1) is also expected since clipping is applied to the scalar directional derivative, not the gradient estimate itself. The theoretical analysis does not provide deeper insights into why DDC works or how to optimally set C.

- **The diffusion model experiments are mentioned but not fully presented**: The paper states that QZO was applied to Stable Diffusion 3.5 Large with results in Appendix F, but the appendix is not included in the provided content. This makes it impossible to evaluate this claim.

## Nice-to-Haves

- Comparison with QLoRA or other quantized PEFT methods would significantly strengthen the paper's positioning.
- Wall-clock time measurements and convergence speed comparisons would help practitioners assess the practical trade-offs.
- Analysis of how the choice of quantization group size affects QZO's performance would be informative.

## Novel Insights

The key insight is that zeroth-order optimization can be applied to quantized neural networks by perturbing the continuous quantization scale parameters rather than the discrete weights themselves. This is non-trivial because standard SPSA requires continuous perturbations, and the paper correctly identifies that the quantization scale serves as a natural continuous parameter through which gradients can be estimated. The observation that this reduces trainable parameters by ~99% (from 6.7B to 50M) while maintaining competitive performance is a valuable finding for the memory-efficient training community.

## Suggestions

- Add comparisons with QLoRA and other PEFT methods to contextualize QZO's performance within the broader memory-efficient fine-tuning landscape.
- Report wall-clock training time alongside FLOPs to give a complete picture of computational efficiency.
- Include experiments on larger datasets (e.g., full training sets rather than 1,000 examples) to demonstrate scalability.

## Score and Decision

The paper presents a novel and practical solution to a well-motivated problem (memory-efficient LLM fine-tuning), with solid empirical validation across multiple models and tasks. The core technical contribution (perturbing quantization scales) is clever and clearly explained. The main limitations are the lack of comparison to established PEFT methods and the restricted evaluation scope. However, the paper's contribution is genuine and the results are convincing within its stated scope.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>