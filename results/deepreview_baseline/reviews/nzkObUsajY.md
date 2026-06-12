## Summary

This paper proposes a dual ANN-to-SNN conversion framework for large language models (LLMs) that eliminates the need to train a conversion-friendly ANN. Instead, it starts from a statically quantized LLM and replaces the quantization function with a multi-hierarchical threshold integer spiking (IS) neuron. A parameter-efficient layer-wise calibration method that adjusts only thresholds and initial membrane potentials is introduced to reduce conversion errors, particularly unevenness error. Theoretical bounds on conversion error are provided, and experiments on LLaMA-2 and LLaMA-3 models show that the method recovers performance close to the quantized baseline for low time steps (T=1,2), though performance degrades at larger T.

## Strengths

- **Novel conversion paradigm**: The dual conversion framework avoids the expensive step of training a conversion-friendly ANN, which is a practical bottleneck for scaling SNN conversion to LLMs. This is a clear advance over conventional ANN-to-SNN pipelines.
- **Parameter-efficient calibration**: The layer-wise calibration only optimizes thresholds and initial membrane potentials (0.107K parameters per layer), achieving substantial error reduction with minimal overhead. Table 4 shows it outperforms full weight fine-tuning in average accuracy while using orders of magnitude fewer parameters.
- **Theoretical grounding**: The paper provides a formal analysis of conversion errors (clipping, quantization, unevenness) and derives an upper bound on the total conversion error (Theorem 3), which motivates the calibration objective. The connection between the IS neuron and the quantization function is established in Theorem 1 and 2.

## Weaknesses

### Major

1. **Performance degradation at larger time steps limits practical energy benefits**: The key motivation for SNNs is low-power event-driven computation, which typically requires multiple time steps to achieve good accuracy. However, the method’s accuracy drops sharply as T increases (e.g., LLaMA-2-7B average accuracy: T=2 → 67.65, T=4 → 67.04, T=8 → 66.03; perplexity rises from 7.39 to 12.03). This means the SNN must operate at very low latency (T=1 or T=2) to be competitive, which may not provide the energy efficiency advantage over the quantized ANN baseline (which already runs with low-bit integer arithmetic). The paper does not report any energy consumption or efficiency measurements, making it difficult to assess the practical benefit of the spiking model.

2. **Incomplete comparison with existing spiking LLM methods**: The paper compares only against quantization methods (PrefixQuant, DuQuant) and does not compare with other SNN conversion methods for LLMs (e.g., SpikeZIP You et al., 2024) or direct training approaches (e.g., SpikeGPT). Since the paper claims to be a “seed effort toward building a spiking LLM,” it should at least discuss how it relates to or outperforms existing spiking LLM works. The absence of such comparison weakens the claim of novelty and effectiveness.

3. **Confusing results for T=1**: In Table 2, “Conversion T=1” (uncalibrated) yields exactly the same numbers as PrefixQuant, which is expected because T=1 conversion should be exact if the IS neuron matches the quantization function. However, “Ours T=1” (calibrated) gives slightly different numbers (e.g., LLaMA-2-7B: 68.79 vs 68.70). This suggests that calibration changes the model even for T=1, which contradicts the theoretical equivalence. The paper does not explain this discrepancy, raising questions about the correctness of the calibration procedure or the implementation.

### Minor

- **Reliance on a specific quantization method**: The framework is built on PrefixQuant (static quantization). It is unclear whether the approach generalizes to other quantization schemes (e.g., dynamic quantization, different bit widths) or whether the IS neuron design is tightly coupled to the specific quantization function of PrefixQuant.
- **Lack of details on spiking-compatible operations**: The paper mentions adopting “spiking-compatible operations” from You et al. (2024) for nonlinear layers (LayerNorm, SiLU, Softmax, etc.) but does not describe them in the main text, relying on an appendix that is stripped. This makes the architecture description incomplete and hinders reproducibility.
- **Theoretical bounds may not be tight**: The Lipschitz assumption (Assumption 1) for QANN layers is plausible but not verified empirically. The bound in Theorem 3 involves products of Lipschitz constants that could grow exponentially with depth, potentially making the bound loose. The paper does not discuss the practical tightness of the bound.

### Trivial

- Figure 3 is described as a “dual-axis plot” but the axis labels and scales are confusing (left y-axis log scale for ANN vs QANN, right y-axis linear for ANN vs SNN). The caption and text could be clearer.

## Nice-to-Haves

- Report energy consumption estimates (e.g., synaptic operations, spike counts) to substantiate the claimed energy efficiency advantage of the spiking LLM over the quantized ANN baseline.
- Include comparisons with other SNN conversion methods for LLMs (e.g., SpikeZIP) and direct training methods (e.g., SpikeGPT) to better position the contribution.
- Provide an ablation study showing the contribution of each component (IS neuron design, calibration, different error types) to the final performance.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Clarify the T=1 calibration results: explain why calibration changes the model when T=1 should be theoretically exact, or correct the experimental setup if there is an error.
- Add energy efficiency measurements (e.g., estimated power consumption or spike counts) to demonstrate the practical advantage of the spiking model over the quantized ANN.
- Include comparisons with existing spiking LLM methods to strengthen the novelty and effectiveness claims.

## Score and Decision

**Score**: 5.0  
**Decision**: Reject  

The paper presents a novel and well-motivated framework for converting LLMs to SNNs without training a conversion-friendly ANN, and the parameter-efficient calibration is a clever idea. However, the practical impact is significantly limited by the severe performance degradation at larger time steps (T>2), which undermines the energy efficiency motivation. The lack of energy measurements and incomplete comparison with existing spiking LLM methods further weaken the contribution. While the theoretical analysis is a plus, the experimental results do not convincingly demonstrate that the method is a viable path toward deployable spiking LLMs.

MY FINAL SCORE: 5.0</score>
MY FINAL DECISION: Reject</decision>