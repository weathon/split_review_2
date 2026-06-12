## Summary

This paper proposes Quantized Zeroth-order Optimization (QZO), which combines zeroth-order optimization with post-training quantization to fine-tune large language models with drastically reduced memory. QZO works by perturbing the continuous quantization scale parameters (rather than discrete quantized weights) to estimate gradients, and introduces Directional Derivative Clipping (DDC) to stabilize training. Experiments on 7B-13B LLMs with 4-bit and 2-bit quantization show QZO achieves up to 18× memory reduction compared to 16-bit fine-tuning while often performing on par with MeZO (which uses unquantized models).

## Strengths

- **Clear and practical contribution**: The idea of perturbing quantization scales instead of discrete weights is intuitive, well-motivated, and genuinely addresses a core difficulty in combining ZO with quantization. The resulting memory savings (e.g., fine-tuning Llama-2-13B on a single 24GB GPU) are impressive and practically valuable.
- **Solid experimental evaluation**: The paper tests across three model families (OPT, Llama-2, Llama-3.1), multiple model sizes (7B–13B), five diverse NLP benchmarks (classification and generation), and two quantization paradigms (scalar-based GPTQ at 4-bit, codebook-based AQLM at 2-bit). Memory profiling and compute statistics are reported.
- **Theoretical grounding**: Theorem 1 establishes unbiasedness of the clipped gradient estimate, and the variance reduction argument (Equation 7–8) provides a clean theoretical justification for DDC. The ablation study (Figure 2–3) convincingly demonstrates DDC's practical necessity and the effect of the clipping threshold.
- **Good ablation and analysis**: The DDC ablation (Figure 2) clearly shows training collapse without clipping. The sensitivity analysis on the clipping threshold (Figure 3) provides useful guidance for practitioners.

## Weaknesses

### Fatal
None.

### Major
- **Performance gap on several tasks undermines the "on par with MeZO" claim**: On CB with Llama-3.1-8B, QZO achieves 69.6 vs. MeZO's 91.1 (a 21.5 point gap). On BoolQ with the same model, QZO scores 78.2 vs. MeZO's 83.4. These are not small variations. The claim "performing on par with MeZO" is stated in the abstract and introduction, but the evidence is mixed. The paper should either qualify this claim or discuss why certain tasks show larger gaps.
- **No comparison to parameter-efficient fine-tuning methods like LoRA or QLoRA**: Given the paper's focus on memory-efficient fine-tuning, it would be highly informative to compare QZO against LoRA (which also reduces memory but uses backpropagation) and QLoRA (which combines quantization with low-rank adapters). This would help position QZO's memory-performance trade-off relative to widely-used alternatives. The current comparison only includes full fine-tuning and MeZO, leaving a gap in context.
- **Wall-clock training time is not reported**: Table 2 reports FLOPs, but actual training speed is critical for practical adoption. Since QZO still requires two forward passes per step (like MeZO), throughput may be low. Reporting actual training time (e.g., hours per dataset) would strengthen the practicality claims.

### Minor
- **Limited capacity of fine-tuning only scales**: QZO fine-tunes only the quantization scales (~1% of parameters). While this is a deliberate design choice for memory efficiency, it inherently limits the model's ability to adapt to complex tasks. The paper acknowledges this but does not investigate whether fine-tuning additional components (e.g., some full-precision weights jointly) could improve performance without significantly increasing memory.
- **The 2-bit experiment uses a different setting (joint fine-tuning of unquantized parts)**: The Llama-2-13B experiments modify QZO to also update unquantized components via SPSA. This is a reasonable extension, but it means the 2-bit results are not a pure test of scale-only fine-tuning, making the comparison less clean.

### Trivial
None.

## Nice-to-Haves
- An analysis of how the number of trainable scales (i.e., quantization group size) affects performance and memory trade-offs.
- A discussion of potential extensions to other domains like fine-tuning vision transformers or multimodal models with quantization.

## Novel Insights
The core insight—that zeroth-order optimization can be applied to quantized neural networks by perturbing the continuous quantization scale rather than the discrete weight values—is genuinely novel and elegantly circumvents the precision mismatch problem. The additional observation that clipping the directional derivative reduces gradient variance (theoretically and empirically) provides a generally useful technique for ZO-based training beyond the quantized setting.

## Suggestions
1. Qualify the "on par with MeZO" claim to reflect the variation across tasks, or provide an analysis of why certain tasks (e.g., CB) see larger degradation.
2. Include a comparison with LoRA/QLoRA in terms of both memory usage and performance on a subset of tasks to help readers understand relative trade-offs.
3. Report wall-clock training time (e.g., hours per full fine-tuning run on a fixed GPU) alongside FLOPs.
4. Consider an ablation where a small fraction of full-precision weights are also updated via SPSA alongside the scales, and evaluate the performance-memory trade-off.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>