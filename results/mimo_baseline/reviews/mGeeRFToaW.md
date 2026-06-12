## Summary
The paper proposes Quantized Zeroth-Order Optimization (QZO), a method that enables fine-tuning of quantized LLMs by perturbing continuous quantization scale parameters (rather than discrete weights) for zeroth-order gradient estimation, combined with directional derivative clipping (DDC) to stabilize training. QZO eliminates gradients and optimizer states while compressing model weights, achieving ~18× memory reduction compared to 16-bit full-parameter fine-tuning, and performs comparably to MeZO (which operates on unquantized models with 3× more memory).

## Strengths
- **Clean and well-motivated problem formulation.** The paper clearly identifies the fundamental incompatibility between ZO optimization and quantized weights (discrete weights cannot be perturbed in continuous space; continuous gradients cannot update discrete weights) and proposes an elegant solution by perturbing the quantization scale instead. This is a simple yet effective insight.
- **Significant and well-documented memory savings.** The 18× memory reduction is demonstrated through rigorous memory profiling across three model families (OPT-6.7B, Llama-2-7B, Llama-3.1-8B), with QZO enabling fine-tuning of Llama-2-13B on a single 24GB GPU. Table 2 also shows ~1% of MeZO's FLOPs, demonstrating both memory and compute efficiency.
- **Orthogonality to existing quantization methods.** QZO is demonstrated with both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) quantization, showing broad applicability. The 2-bit results on Llama-2-13B (Table 3) demonstrate effectiveness under extreme quantization.
- **Thorough ablation of DDC.** Figure 2 convincingly shows that without DDC, training collapses at step 22, and Figure 3 provides a useful sensitivity analysis of the clipping threshold, showing stable performance for C ≥ 75.

## Weaknesses
### Fatal
None.

### Major
- **Missing comparison with QLoRA.** QLoRA (Dettmers et al., 2023) is the most widely adopted method for memory-efficient fine-tuning of quantized models and is cited in the references. Omitting this comparison is a significant gap, as practitioners would need to know the accuracy-memory tradeoff between QZO and QLoRA. QLoRA likely uses more memory but may achieve substantially better accuracy, and this tradeoff is central to the paper's value proposition.
- **Upper-bound baseline uses SGD instead of AdamW.** The paper acknowledges this (footnote 2) but the comparison is weakened since AdamW typically outperforms SGD significantly for LLM fine-tuning. The performance gaps (e.g., 61.7 vs. 79.8 on RTE for OPT-6.7B) may be partly attributable to the weak baseline rather than inherent limitations of QZO.
- **Large performance gaps on some tasks remain unexplained.** On RTE with OPT-6.7B, QZO achieves 61.7 vs. 79.8 for fine-tuning (a 18-point gap), and on CB with OPT-6.7B, 67.9 vs. 73.2. The paper does not analyze which tasks are harder for QZO and why, or discuss when QZO's memory-accuracy tradeoff is favorable versus alternatives.

### Minor
- **Limited scale of evaluation.** All experiments use 1,000 training examples. It is unclear whether QZO's relative performance holds with larger training sets, which is the typical fine-tuning scenario.
- **Hyperparameter sensitivity analysis is limited to C.** The sensitivity to learning rate (fixed at 10⁻⁷), perturbation scale ε (fixed at 10⁻³), and batch size is not explored, making it difficult for practitioners to tune QZO on new tasks.
- **The 2-bit results (Table 3) lack a MeZO comparison**, making it impossible to assess whether the gains come from the quantization-aware optimization or simply from fine-tuning in general.

### Trivial
None.

## Nice-to-Haves
- Comparison with QLoRA and other PEFT methods (e.g., LoRA) to fully characterize the Pareto frontier of memory vs. accuracy
- Experiments on larger models (e.g., 70B) where memory savings would be most impactful
- Analysis of gradient estimation quality (e.g., cosine similarity between QZO gradient estimates and true gradients)
- More diverse tasks such as instruction following or code generation

## Novel Insights
The key novel insight is that perturbing the continuous quantization scale (rather than the discrete weights) provides a natural bridge between zeroth-order optimization and quantized models. This avoids the need for de-quantization/re-quantization cycles and noise quantization that prior approaches require, making the method simpler and more broadly applicable to different quantization schemes. The DDC mechanism, while straightforward, provides a practical solution to a real instability problem in ZO training of quantized models.

## Suggestions
- Add QLoRA as a baseline to provide a complete picture of the memory-accuracy tradeoff landscape
- Include at least some AdamW fine-tuning results (even on a subset of tasks) to strengthen the upper-bound comparison
- Provide guidance on hyperparameter selection (learning rate, ε, C) based on model size and task characteristics

## Score and Decision
The paper presents a clean, well-motivated method with substantial practical value (18× memory reduction). The core idea is elegant and the experiments are reasonably thorough. However, the missing QLoRA comparison is a significant gap for a paper targeting memory-efficient fine-tuning, and the SGD-only upper bound weakens the accuracy claims. These issues prevent a stronger recommendation but do not invalidate the contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept