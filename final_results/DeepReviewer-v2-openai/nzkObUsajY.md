## Summary
# Final Review Report

## Summary

This paper proposes a dual ANN-to-SNN conversion framework for large language models (LLMs) that avoids training a dedicated conversion-friendly ANN. The key idea is to start from a statically quantized LLM (using PrefixQuant) and replace the quantization function with a novel Integer Spiking (IS) neuron equipped with multi-hierarchical thresholds. A parameter-efficient layer-wise calibration method that adjusts only thresholds and initial membrane potentials (0.107K parameters per layer) is introduced to reduce conversion errors—particularly unevenness error—with minimal overhead. Theoretical analysis provides an error bound based on a Lipschitz assumption, and experiments on LLaMA-2-7B and LLaMA-3-8B under W6A6 quantization show that the calibrated SNN recovers accuracy from the catastrophic degradation seen in uncalibrated conversion.

The work addresses a relevant problem (energy-efficient LLM deployment on edge devices) and proposes a clean technical pipeline. However, the paper has several significant weaknesses: (1) the central claim of energy efficiency is never validated with actual measurements; (2) the theoretical guarantees rely on restrictive assumptions (Lipschitz continuity for quantized layers with discontinuous operations) and the exact equivalence between IS neurons and quantization is practically unachievable; (3) the experimental evaluation lacks statistical significance testing, variance reporting, and baseline fairness controls; (4) critical implementation details for non-linear operations are deferred to the appendix; and (5) several claims are overstated relative to the evidence provided.

## Strengths
1. **Problem significance and timeliness.** The paper addresses a genuine challenge: deploying LLMs on edge devices with limited power and compute. Converting pre-trained LLMs to SNNs without retraining is a promising direction that could significantly impact practical deployment, and the paper correctly identifies the key bottleneck (training a conversion-friendly ANN is prohibitively expensive at LLM scale).

2. **Clean conceptual framework.** The "dual conversion" idea—using a quantized LLM as the intermediate representation and designing an IS neuron that approximates the quantization function—is conceptually elegant. The pipeline (Pretrained ANN → Quantized ANN → Calibrated SNN) avoids the expensive retraining step required by prior conversion methods.

3. **Parameter-efficient calibration.** The layer-wise calibration method that optimizes only thresholds and initial membrane potentials (0.107K parameters per layer) is a strong contribution. Table 4 demonstrates that this tiny parameter budget achieves accuracy comparable to full weight fine-tuning (202M parameters), which is practically valuable and methodologically interesting.

4. **Comprehensive error analysis.** The paper identifies and formally characterizes three error sources (clipping, quantization, unevenness) in the dual conversion setting, building on established conversion error analysis. Definition 1 explicitly formalizes unevenness error, which is a useful contribution to the SNN conversion literature.

5. **Empirical recovery from catastrophic degradation.** The calibration dramatically recovers accuracy from the severely degraded uncalibrated SNN (e.g., from 59.99% to 67.65% on LLaMA-2-7B at T=2). This demonstrates that the proposed calibration is practically effective.

## Weaknesses
### Major Weaknesses

**W1. Energy efficiency claims are entirely unvalidated.**
The paper's central motivation is that SNNs offer "brain-inspired efficiency and low power consumption" for edge deployment, yet no energy consumption, power usage, inference latency, or FLOP comparison is measured anywhere in the manuscript. The only quantitative evidence is accuracy/perplexity scores on zero-shot reasoning tasks. Without any energy measurement, the paper does not substantiate its core value proposition. This is a critical gap because: (a) the SNN uses T=2-8 time steps, which means it performs 2-8x more forward passes than the quantized ANN baseline; (b) the energy advantage of SNNs depends on spike sparsity, which is not measured; (c) the quantized ANN (W6A6) may already be quite efficient on modern hardware. *Fix: Add at least one of: GPU power profiling, estimated energy per inference (synaptic operations count), or latency comparison under identical hardware.*

**W2. Theoretical guarantees are weaker than claimed.**
The conversion error bound (Theorem 3) assumes Lipschitz continuity for all QANN layers, but quantized layers involve floor operations (discontinuous), clipping (non-differentiable boundaries), and self-attention (softmax with exponential). The Lipschitz constants ρ^k are never bounded or estimated. For 32-layer LLaMA-2-7B, the bound contains products of up to 31 ρ^τ terms, which can grow exponentially unless every ρ^k < 1—an unverified condition. Furthermore, Theorem 2's exact equivalence between IS neuron output and the quantization function requires LT = 2^n - 1 (e.g., L·T = 63 for W6A6), which the paper acknowledges is "rarely" satisfiable. The paper uses approximation (≈) but provides no error bound for the approximation. *Fix: Estimate empirical Lipschitz constants for each layer; provide the approximation error bound as |∑ŝ^kθ^k - X_q^k| ≤ λ^k·max(1, L·T - (2^n-1)).*

**W3. Missing statistical significance and variance reporting.**
All results in Tables 2-4 are single-point accuracy numbers without variance estimates, confidence intervals, or significance tests. Differences between the calibrated SNN and quantized baseline are often small (0.1-1.5 accuracy points). Without multi-seed reporting, a reviewer cannot determine whether these differences are systematic or due to run-to-run variation. *Fix: Run all experiments with ≥3 random seeds (calibration data subset, initialization), report mean±std, and include a paired bootstrap significance test against the quantized baseline.*

**W4. Critical implementation details are missing.**
Section 3.2.3 delegates the handling of all nonlinear operations (LayerNorm, SiLU, Softmax, activation-activation multiplication) to "spiking-compatible operations proposed in You et al. (2024)" without summarizing what approximations these operations introduce. Since these nonlinearities are central to modern LLM architectures, a reviewer cannot assess whether the conversion is sound without understanding the approximations made. Additionally, the layer-wise calibration objective (Section 3.4) is stated without specifying optimizer, learning rate, number of steps, calibration dataset size, or how gradients are handled through the non-differentiable IS neuron firing. *Fix: Provide a table mapping each nonlinear operation to its spiking equivalent with the approximation type and error. Specify calibration hyperparameters.*

**W5. Performance degrades consistently as T increases, limiting practical utility.**
The calibrated SNN's accuracy drops steadily with more time steps (e.g., LLaMA-2-7B: 68.79% at T=1 → 67.65% at T=2 → 67.04% at T=4 → 66.03% at T=8). Since SNN energy efficiency typically requires more time steps to achieve better performance, this inverse scaling is problematic. The paper attributes this to "growing unevenness error" but provides no analysis of why calibration cannot compensate at higher T. This directly limits the practical applicability for edge deployment where energy-accuracy tradeoffs matter. *Fix: Analyze why calibration fails at higher T (e.g., per-layer error accumulation analysis, or propose a time-step-dependent calibration scheme).*

### Minor Weaknesses

**W6. Figure 3 is misleading.** The dual-axis plot uses a log scale (left, for ANN→QANN error) and a linear scale with negative values (right, for ANN→SNN error). MSE is non-negative by definition, so the negative values on the right axis indicate the plotted quantity is not MSE or the axis is mislabeled. The incompatible scales make visual comparison unreliable. *Fix: Use a single-axis log-scale line plot for both curves, or a side-by-side bar comparison.*

**W7. Overclaiming in conclusion and contributions.** Contribution C3 ("seed effort") and the conclusion's "substantial improvements in accuracy" overstate what is demonstrated. The calibrated SNN is consistently worse than the quantized baseline, not better. "Substantial improvements" refers only to the recovery from a catastrophically degraded uncalibrated SNN. *Fix: Rephrase to "recovers most of the accuracy lost during conversion" and avoid claiming improvements over the quantized baseline.*

**W8. Related work lacks analytical depth.** Section 2.2 on ANN-to-SNN conversion reads as a catalog without comparison axes relevant to LLMs (retraining requirement, neuron type, demonstrated scale, time steps needed). *Fix: Add a table comparing prior methods on these LLM-relevant axes.*

**W9. PPL anomaly in Table 3.** The perplexity for group_size=64 in Table 3 (9.17) is substantially higher than all other configurations (6.89-7.39). This unexplained outlier raises reproducibility concerns. *Fix: Report multi-seed results; explain or fix the outlier.*

**W10. Reproducibility statement is placeholder.** The statement says "source code will be publicly released after publication," which does not help reviewers. *Fix: Provide calibration pseudo-code or detailed hyperparameter settings in the appendix.*

## Score
Final Score: 5/10

**Rationale:** The paper proposes an interesting and conceptually clean approach for converting quantized LLMs to SNNs without retraining. The parameter-efficient calibration (0.107K parameters per layer) achieving accuracy comparable to full weight fine-tuning is a genuinely valuable finding. However, the paper has several critical weaknesses that prevent a higher score:

- **Primary gap (W1):** The central motivation—energy-efficient edge deployment—is entirely unvalidated. Without any energy measurement, the core value proposition rests on an assumption.
- **Theoretical overclaim (W2):** The equivalence between IS neurons and quantization functions is approximate under realistic settings, and the error bound depends on unverified Lipschitz constants.
- **Evidence insufficiency (W3, W5):** No statistical testing or variance reporting, and performance degrades with more time steps, undermining practical utility.
- **Reproducibility (W4):** Critical details about nonlinear operation handling and calibration optimization are missing.

These weaknesses are fixable with additional experiments and clearer writing. If the authors add energy measurements, statistical significance testing, and calibration details, the paper could reach 6-7/10.

**Post-Revision Target:** [6, 7]/10, contingent on addressing W1, W3, and W4 as minimum requirements.

**Novelty/comparison verdict (deferred):** External literature search was unavailable in this run. Novelty claims (C1: training-free dual conversion framework, C2: theory-backed layer-wise calibration, C3: spiking LLM seed effort) require manual verification against prior SNN conversion and spiking LLM literature. The contributions appear technically novel within the stated scope but should be verified against concurrent works such as SpikeZIP (You et al., 2024) and related SNN calibration methods.