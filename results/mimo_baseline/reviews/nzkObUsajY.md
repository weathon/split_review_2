## Summary

The paper proposes a dual ANN-to-SNN conversion framework for obtaining spiking LLMs without training a conversion-specific ANN. The approach starts from a statically quantized LLM (PrefixQuant), replaces quantization functions with Integer Spiking (IS) neurons that mimic quantization behavior, and applies a parameter-efficient layer-wise calibration to reduce unevenness error. Experiments on LLaMA-2-7B and LLaMA-3-8B demonstrate that calibration substantially improves converted SNN performance, approaching the underlying quantized ANN baseline.

## Strengths

- **Novel framework concept.** The idea of directly converting a quantized LLM into an SNN without retraining a conversion-friendly ANN is a practical and meaningful contribution. By framing IS neurons as quantization-function approximators, the paper elegantly bridges two active research areas (LLM quantization and ANN-to-SNN conversion), as illustrated clearly in Figures 1 and 2.

- **Theoretical grounding.** The paper provides a concrete analysis of conversion error types (clipping, quantization, unevenness) and derives an upper bound on total conversion error (Theorem 3) that motivates the layer-wise calibration strategy. The theoretical framework (Theorems 1–3) is clearly presented and connects directly to the proposed method.

- **Parameter efficiency of calibration.** Table 4 demonstrates that the calibration method achieves comparable or better accuracy than full weight fine-tuning while using ~0.107K parameters per layer versus ~200M, a compelling efficiency result. Table 3 further shows robustness across different group sizes, supporting the claim of strong adaptability.

- **Clear improvement over naive conversion.** Table 2 convincingly shows that without calibration, the converted SNN suffers catastrophic degradation (e.g., avg accuracy drops from 70.24 to 48.83 on LLaMA-3-8B at T=2), while calibration recovers most of this gap (to 69.03). This cleanly demonstrates the importance of addressing unevenness error.

## Weaknesses

### Fatal

None.

### Major

- **No energy or latency analysis.** The paper's core motivation is energy-efficient LLM deployment on edge devices. However, it provides zero empirical evidence of energy savings, latency reduction, or hardware-level comparisons. Claims about SNNs offering "brain-inspired efficiency and low power consumption" remain entirely unsubstantiated in the experiments section. Without this, the practical value of the contribution is unclear—the paper essentially reduces to a quantization method with SNN dynamics, and it is not demonstrated that the SNN formulation actually provides a deployment advantage over the underlying quantized ANN.

- **Narrow experimental evaluation.** Only two models (LLaMA-2-7B, LLaMA-3-8B) with one quantization setting (W6A6) and five zero-shot reasoning tasks are evaluated. The paper does not evaluate on generation tasks, instruction-tuned variants, larger models, or different bit-widths. This limits the generalizability of the conclusions and is insufficient for a contribution targeting LLMs broadly.

- **DuQuant baseline results appear identical across models.** In Table 2, DuQuant yields exactly the same accuracy values (67.88, 72.64, 40.53, 53.07, 77.15, 62.25) for both LLaMA-2-7B and LLaMA-3-8B, differing only in PPL. This is highly suspicious for two different model families and raises concerns about experimental correctness.

### Minor

- **The IS neuron is borrowed from prior work.** The paper explicitly credits the Multi-Hierarchical Threshold neuron to Sun et al. (2022), Wang & Zhang (2023), Li & Zeng (2022), and Hao et al. (2024). The primary novelty lies in the framework and calibration rather than the neuron design itself, which limits the technical contribution.

- **Calibration procedure underspecified in main text.** The paper states that thresholds and initial membrane potentials are optimized to minimize conversion error but does not describe the optimization method, number of calibration samples, learning rate, or training schedule in the main paper. Key reproducibility details are deferred entirely to an unavailable appendix.

- **Comparison with existing spiking LLM methods absent.** The paper mentions SpikeGPT and SpikeBERT in the introduction but does not compare against them, even qualitatively. SpikeZIP is also cited as a relevant conversion method but is not included as a baseline. This limits the ability to situate the contribution within the spiking LLM landscape.

- **T=1 results for "Conversion" and PrefixQuant are identical**, which is expected but makes the "Ours" row at T=1 subtly different from PrefixQuant without explanation. The difference (e.g., 76.22 vs 75.70 HellaSwag on LLaMA-2-7B) is small but unexplained given that T=1 should correspond to standard quantization.

## Nice-to-Haves

- Energy profiling or at least an analytical model estimating computational cost (e.g., spike operations vs. MAC operations) on representative hardware
- Evaluation on at least one downstream task (e.g., language generation, instruction following) to demonstrate the method's utility beyond zero-shot classification
- Comparison with SpikeZIP or other conversion-based spiking LLM methods
- Results on larger models (13B, 70B) to demonstrate scalability

## Novel Insights

The paper's genuinely novel insight is that the mathematical relationship between symmetric quantization functions and multi-threshold spiking neurons (formalized in Theorem 2) provides a principled bridge between LLM quantization and ANN-to-SNN conversion. This reframes SNN conversion not as an approximation of ReLU activations but as an emulation of quantization operations, which is a conceptually different (and potentially more efficient) paradigm. The observation that unevenness error dominates over clipping/quantization error in this dual conversion setting (Figure 3) further motivates the calibration focus and is a useful empirical finding for the community.

## Suggestions

1. **Add energy/latency measurements.** Profile the actual energy consumption and inference latency of the spiking LLM on neuromorphic or edge hardware (or at minimum via simulation), directly comparing against the quantized ANN baseline. This is essential to validate the paper's primary motivation.

2. **Clarify and expand baselines.** Include SpikeZIP as a baseline for direct comparison. Address the suspicious DuQuant numbers. Expand to additional models and quantization settings.

3. **Provide calibration details in the main text.** Include a brief but complete description of the calibration procedure (optimizer, learning rate, data samples, convergence criteria) so the method is understandable without the appendix.

4. **Discuss practical tradeoffs.** The paper notes that T=1 is ideal but explores T=2,4,8. It should explicitly discuss the tradeoff between time steps (energy cost) and accuracy, providing guidance for practitioners choosing T.

MY FINAL SCORE: 4.0
MY FINAL DECISION: Reject