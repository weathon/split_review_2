## Summary

This paper proposes Quantized Zeroth-order Optimization (QZO), a method that enables fine-tuning of quantized neural networks by perturbing the continuous quantization scale rather than the discrete weights, thereby avoiding the precision gap between discrete weights and continuous gradients. QZO eliminates gradients and optimizer states via zeroth-order optimization and compresses weights via post-training quantization, achieving up to 18× memory reduction compared to full-precision fine-tuning. The method also introduces directional derivative clipping (DDC) to stabilize training, with theoretical and empirical evidence of variance reduction. Experiments on several LLMs (OPT-6.7B, Llama-2-7B, Llama-3.1-8B, Llama-2-13B) across five NLP benchmarks show that QZO performs on par with MeZO (which uses 16-bit models) while using 3× less memory, and works even under extreme 2-bit quantization.

## Strengths

- **Novel and practical idea**: Perturbing the quantization scale instead of discrete weights is a clever and principled way to combine zeroth-order optimization with quantized models, directly addressing the precision gap challenge.
- **Significant memory reduction**: QZO reduces total memory cost by 18× compared to full-precision fine-tuning with AdamW, enabling fine-tuning of Llama-2-13B on a single 24GB GPU. This is a concrete and impactful contribution for resource-constrained practitioners.
- **Orthogonality to PTQ methods**: The method is compatible with both scalar-based (GPTQ) and codebook-based (AQLM) post-training quantization, as demonstrated experimentally, making it widely applicable.
- **Theoretical and empirical analysis of DDC**: The paper provides a theoretical argument that directional derivative clipping reduces gradient estimate variance, and ablation studies confirm its necessity for stable training and robustness to the clipping threshold.
- **Comprehensive evaluation**: Experiments cover multiple LLM families (OPT, Llama-2, Llama-3.1), multiple tasks (classification and generation), and both 4-bit and 2-bit quantization, with consistent positive results.

## Weaknesses

### Fatal
None.

### Major
- **Missing comparison with QLoRA and other quantized fine-tuning methods**: QLoRA (Dettmers et al., 2023) is a widely used approach for fine-tuning quantized LLMs that also achieves significant memory savings. The paper does not compare QZO with QLoRA or similar methods (e.g., LoRA, adapter-based fine-tuning on quantized models). Such a comparison is essential to contextualize QZO’s memory-performance trade-off and to justify its practical advantage. Without it, the claim of “maximum reduction in memory usage” is not fully supported against existing strong baselines.
- **Upper-bound baseline uses SGD, not AdamW**: The paper states that fine-tuning experiments use SGD due to budget constraints, but AdamW is the standard optimizer for LLM fine-tuning and typically yields better performance. This weakens the “upper-bound” claim and makes the comparison with MeZO (which also uses SGD-based ZO) less informative. The paper should either use AdamW for the upper bound or clearly acknowledge this limitation and discuss its impact.

### Minor
- **Theoretical derivation of DDC variance reduction is not fully rigorous**: The derivation in Eq. (8) attempts to show that Var[clipped] ≤ Var[unclipped], but the step from the inequality of second moments to the inequality of variances is not fully justified without additional assumptions about the first moments. The argument would benefit from a clearer statement or a more standard proof.
- **No wall-clock time comparison**: The paper reports FLOPs reduction but does not report actual training time. Since QZO requires two forward passes per step, the wall-clock time may be comparable to MeZO despite fewer FLOPs. Reporting training time would strengthen the computation-efficiency claim.
- **Limited hyperparameter sensitivity analysis**: Only the clipping threshold C is ablated. The sensitivity to learning rate, perturbation scale ε, and batch size is not explored, which would be useful for practitioners.

### Trivial
- The paper uses “upper-bound” and “lower-bound” loosely; the zero-shot baselines are not strict lower bounds (e.g., a poorly quantized model could be worse than zero-shot).

## Nice-to-Haves

- A comparison with QLoRA or other parameter-efficient fine-tuning methods on quantized models would greatly strengthen the paper.
- Reporting training time (e.g., hours to convergence) alongside FLOPs would give a more complete picture of computational efficiency.
- An ablation on the number of trainable parameters (e.g., fine-tuning only scales vs. also fine-tuning unquantized components) would clarify the design choices.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Add a comparison with QLoRA (or similar) on at least one model and dataset to demonstrate the relative memory-performance trade-off.
- Replace the SGD fine-tuning upper bound with AdamW, or explicitly discuss why SGD is used and how it affects the comparison.
- Clarify the theoretical derivation of DDC variance reduction, either by providing a more rigorous proof or by stating the necessary assumptions.
- Report wall-clock training time for QZO and MeZO on a representative setting.

## Score and Decision

**Score**: 6  
**Decision**: Accept

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>