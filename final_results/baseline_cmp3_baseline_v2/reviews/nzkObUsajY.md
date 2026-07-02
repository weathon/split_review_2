## Summary

This paper proposes a dual ANN-to-SNN conversion framework for large language models that eliminates the need to train a conversion-friendly ANN. The method starts from a statically quantized LLM, introduces an Integer Spiking (IS) neuron with multi-hierarchical thresholds to approximate the quantization function, and applies a parameter-efficient layer-wise calibration technique to reduce conversion errors, particularly unevenness error. Experiments on LLaMA-2-7B and LLaMA-3-8B demonstrate that the calibrated SNN achieves performance comparable to state-of-the-art quantization methods.

## Strengths

- **Novel problem framing**: The paper identifies a practical and important challenge—converting pre-trained LLMs to SNNs without expensive retraining—and proposes a clean solution that leverages existing quantized LLMs as an intermediate representation. This is a well-motivated approach that addresses a genuine bottleneck in deploying spiking LLMs on edge devices.

- **Theoretical grounding**: The paper provides formal theorems (Theorem 1 and Theorem 2) establishing conditions under which the proposed IS neuron can approximate the quantization function, and Theorem 3 provides an upper bound on the conversion error. The theoretical analysis of clipping, quantization, and unevenness errors is clearly articulated and connected to the proposed calibration method.

- **Parameter efficiency**: The layer-wise calibration method that only optimizes thresholds and initial membrane potentials (0.107K parameters per layer) achieves performance comparable to full weight fine-tuning (202M parameters per layer), as shown in Table 4. This is a significant practical advantage for large-scale models.

- **Comprehensive evaluation**: The paper evaluates on two model families (LLaMA-2-7B and LLaMA-3-8B) across multiple time steps (T=1,2,4,8) and five zero-shot reasoning tasks, with perplexity on WikiText2. The ablation study on learnable parameter sizes (Table 3) demonstrates robustness.

## Weaknesses

### Major

- **Missing energy efficiency analysis**: The paper claims SNNs offer "brain-inspired efficiency and low power consumption" and that the work "potentially reduces the energy consumption of LLMs," but provides no energy consumption measurements, theoretical FLOPs comparison, or even spike rate analysis. For a paper whose core motivation is energy-efficient edge deployment, the absence of any energy-related evaluation is a significant gap. The claim that SNNs are more energy-efficient than quantized ANNs is not substantiated.

- **Limited model scale and comparison scope**: The evaluation is limited to 7B and 8B parameter models. The paper does not demonstrate scalability to larger models (e.g., 13B, 30B, 70B) where the computational advantages of the proposed method would be most relevant. Additionally, the comparison baselines are limited to quantization methods (PrefixQuant, DuQuant) and do not include other SNN conversion methods for LLMs (e.g., SpikeZIP) or direct SNN training approaches.

- **Theoretical-practical gap in Theorem 2**: Remark 1 acknowledges that the exact equivalence condition $LT = 2^n - 1$ "rarely holds for arbitrary integer choices of L and T," meaning the IS neuron only approximately mimics the quantization function. The paper does not quantify how large this approximation error is in practice or how it varies with different choices of L and T. The practical implications of this gap are not explored.

- **Unclear practical advantage over quantized ANNs**: The paper shows that the calibrated SNN achieves performance comparable to quantized LLMs (e.g., PrefixQuant W6A6). However, it does not clearly articulate what advantage the SNN version provides over the quantized ANN version. If the quantized ANN already runs efficiently on edge devices, what additional benefit does converting to an SNN provide? The paper needs to address this more directly.

### Minor

- **Unevenness error analysis**: While the paper identifies unevenness error as the dominant source of degradation and shows that calibration helps, the analysis of why unevenness error increases with larger T (as observed in Table 2) is superficial. A deeper investigation into the mechanism would strengthen the paper.

- **Calibration data and cost**: The paper does not specify how much calibration data is used, how many calibration steps are required, or the computational cost of the calibration process. This information is important for practitioners to assess the practical overhead.

### Trivial

- The paper uses "dual" in the title and throughout but never explicitly defines what makes the conversion "dual" beyond being a two-stage process. The term is used more as a stylistic choice than a technical distinction.

## Nice-to-Haves

- An energy consumption comparison between the quantized ANN and the converted SNN (e.g., estimated synaptic operations, theoretical energy cost) would significantly strengthen the paper's core motivation.
- Evaluation on larger LLaMA models (13B, 30B) would demonstrate scalability.
- Comparison with other SNN conversion methods for LLMs (e.g., SpikeZIP) would provide a more complete picture.

## Novel Insights

The key insight is that quantized LLMs, which are already widely studied for efficient deployment, can serve as a natural bridge to SNN conversion. By designing an IS neuron that approximates the quantization function, the paper avoids the expensive step of training a conversion-friendly ANN. The observation that unevenness error, rather than clipping or quantization error, dominates the conversion gap, and that calibrating only thresholds and initial membrane potentials is sufficient to address this, is a practically valuable finding.

## Suggestions

1. Add an energy efficiency analysis comparing the quantized ANN and the converted SNN, including estimated synaptic operations, theoretical energy consumption, or actual runtime measurements on edge hardware.
2. Clarify the practical advantage of the SNN over the quantized ANN—under what conditions would a practitioner prefer the SNN version?
3. Quantify the approximation error from the inexact equivalence in Theorem 2 and discuss how it affects practical performance.
4. Report the calibration data requirements and computational cost.

## Score and Decision

The paper addresses a timely and important problem with a well-motivated approach, provides theoretical grounding, and demonstrates empirical results on models of practical interest. However, the absence of any energy efficiency analysis—which is central to the paper's motivation—is a significant gap that prevents the paper from being fully convincing. The paper would benefit from addressing this before acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>