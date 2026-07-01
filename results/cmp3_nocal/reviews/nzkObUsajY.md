Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper proposes an ANN-to-SNN conversion framework for LLMs that bypasses the conventional requirement of training a conversion-friendly ANN. Instead, it starts from an off-the-shelf quantized LLM (PrefixQuant), replaces the quantization function with a multi-hierarchical threshold Integer Spiking (IS) neuron, and applies a layer-wise calibration that tunes only thresholds and initial membrane potentials (~0.1K parameters per layer). Experiments on LLaMA-2-7B and LLaMA-3-8B show the calibrated SNN achieves accuracy close to the source quantized model.

## Strengths

1. **Practical problem identification.** The paper correctly identifies that conventional ANN-to-SNN conversion requires training a conversion-friendly ANN (e.g., with QCFS activations), which is prohibitive for LLMs. Leveraging off-the-shelf quantized LLMs as the conversion source bypasses this cost. Figure 1 clearly contrasts the two pipelines, and this motivation is well-articulated throughout.

2. **Genuinely striking parameter efficiency.** Table 4 shows that tuning only thresholds and initial membrane potentials (~0.1K parameters per layer) achieves accuracy competitive with full weight fine-tuning (~200M parameters). Even at T=2 (the setting with actual SNN dynamics), the calibration recovers a large fraction of the performance lost in the uncalibrated conversion (e.g., LLaMA-2-7B: 59.99 → 67.65 for Ours T=2 vs. PrefixQuant 68.70; LLaMA-3-8B: 48.83 → 69.03 vs. PrefixQuant 70.24).

3. **Theoretical error decomposition.** The paper formally analyzes three types of conversion error (clipping, quantization, unevenness) and provides a Lipschitz-based bound (Theorem 3) that justifies the layer-wise calibration objective. While the bound itself is structurally standard, the framing within the dual-conversion setting and the explicit identification of unevenness error as dominant (Figure 3) is useful.

## Weaknesses

### Major

1. **Performance degrades with more time steps, inverting the expected SNN behavior.** In conventional ANN-to-SNN conversion, accuracy improves as the time window T grows because firing rates better approximate the target activations. Here, the opposite occurs:

   | Model | T=1 (calibrated) | T=2 | T=4 | T=8 |
   |-------|------------------|-----|-----|-----|
   | LLaMA-2-7B Avg. Acc. | 68.79 | 67.65 | 67.04 | 66.03 |
   | LLaMA-2-7B PPL | 5.61 | 7.39 | 9.71 | 12.03 |
   | LLaMA-3-8B Avg. Acc. | 71.67 | 69.03 | 67.21 | 63.76 |
   | LLaMA-3-8B PPL | 6.66 | 9.07 | 11.67 | 18.93 |

   (Table 2 in the paper)

   The paper attributes this to "growing unevenness error" but offers no analysis of why the calibration, which directly targets unevenness error, fails to arrest the trend. At T=8, the perplexity of 12.03 (LLaMA-2) and 18.93 (LLaMA-3) would make the model impractical for generation. The method works best at T=1 — which, while still technically an SNN, lacks temporal spike dynamics. The fact that SNN behavior only exists at settings where the model performs worse than its minimal-T variant is a fundamental limitation that the paper does not resolve.

2. **The central motivation (energy-efficient SNN deployment) is asserted but never measured.** The abstract, introduction, and conclusion all frame the contribution around "brain-inspired efficiency and low power consumption" and "potentially reduc[ing] the energy consumption of LLMs." Yet the paper contains zero energy measurements, no FLOP counts, no MAC vs. spike-accumulation comparison, no spike-rate analysis, and no latency benchmarks. Experiments are run on A100 GPUs without even simulating the event-driven advantage. Contribution 3 states the work "potentially reduces the energy consumption of LLMs" — but a paper that motivates itself through a claimed benefit and never measures it leaves its central thesis unevidenced. This goes beyond a missing ablation; the evidence for the paper's stated raison d'être is absent.

3. **No comparison against any prior SNN-based LLM method.** The paper is about ANN-to-SNN conversion for LLMs and cites SpikeZIP (You et al., 2024) as "recent advances" and SpikeGPT (Zhu et al., 2023) as a direct-training alternative, but evaluates neither. Every baseline in Table 2 is a *quantization* method (PrefixQuant, DuQuant). The only "conversion" baseline is the uncalibrated version of the authors' own method. To establish that this conversion approach advances the state of the art in spiking LLMs, at least one prior SNN-based LLM method should be included (or a clear explanation of why comparison is infeasible). As designed, the experiments only show that the converted SNN roughly preserves the accuracy of the quantized source — a conversion fidelity claim, not a comparative advance over existing SNN approaches.

### Minor

4. **The "comparable to SOTA quantization" claim conflates the T=1 and T>1 settings.** The headline claim holds at T=1 (LLaMA-2-7B: 68.79 vs. PrefixQuant 68.70; LLaMA-3-8B: 71.67 vs. 70.24). At T=2 (the lowest setting with actual SNN temporal dynamics), the gap widens to ~1–1.2 points in accuracy, and perplexity jumps significantly (e.g., LLaMA-3-8B: 6.66 → 9.07). At T=8, the accuracy gap reaches ~5–6 points. The paper should specify which time-step regime the claim refers to.

5. **The central theoretical equivalence (Theorem 2) is acknowledged to be inexact, with the approximation error unquantified.** Theorem 2 shows exact equivalence only when LT = 2ⁿ - 1. Remark 1 states this "rarely holds for arbitrary integer choices of L and T if T ≠ 1" and resorts to an approximate equivalence (≈) with no bound on the approximation error. The interval conditions on Iᵏ(t) in Theorems 1 and 2 are also never verified for real LLM activations. The paper is transparent about this gap, but the gap is real: the theory provides a veneer of rigor that only applies in a regime the implementation cannot satisfy.

6. **The IS neuron's novelty relative to prior M-HT work is not articulated.** Section 3.2.2 introduces the IS neuron as a "modified Integer Spiking (IS) neuron—also referred to as the Multi-Hierarchical Threshold (M-HT) neuron" citing Sun et al. (2022), Wang & Zhang (2023), Li & Zeng (2022), and Hao et al. (2024). The word "modified" is used but the specific modification(s) relative to the cited M-HT neuron are never stated. Given that the IS neuron is central to the conversion, the delta from prior M-HT should be explicit.

7. **The weight calibration comparison (Section 4.4) is not against the most informative baseline.** Comparing 0.107K calibration parameters against full weight fine-tuning on 202M parameters is staged to make calibration look favorable — full fine-tuning on a tiny calibration set would be expected to overfit. A parameter-efficient method like LoRA (which also uses a small number of parameters) would be a more meaningful comparison.

8. **Calibration data budget is unspecified.** The paper does not state how many calibration samples were used, how they were selected, or how sensitive the method is to calibration set size. This is standard information for post-training calibration methods and affects practical deployment.

### Trivial

9. **The term "dual" is used throughout but never explicitly defined.** From context, it appears to refer to the two-stage pipeline (quantization then conversion) as a mirror of the conventional two-stage pipeline (training then conversion). A brief definition would improve clarity.

## Nice-to-Haves

- A brief discussion of why direct SNN training methods (e.g., SpikeGPT) are not compared or are not suitable would help contextualize the contribution within the broader SNN literature.
- Reporting variance or confidence intervals for the zero-shot accuracies would strengthen statistical credibility, though single-run reporting is the norm in this sub-area.

## Removed Points

These points from the input review are not included in the weaknesses above, with justifications:

- **"Section 1 lines 37–38: unevenness error claim is opposite of conventional understanding."** This criticism assumes standard IF-neuron dynamics, but the paper uses a fundamentally different neuron model (IS/M-HT) with multi-level thresholds. The conventional understanding of unevenness error in IF-based conversion does not directly transfer. The broader concern (performance degrades with T) is already captured in Major weakness #1. Removed to avoid conflating two different neuron models.

- **"Section 3.2.3: substantial portion of architecture inherited from SpikeZIP without evaluation of whether approximations are faithful."** The paper transparently cites and adopts these operations from You et al. (2024). Re-evaluating adopted prior work is not standard practice. Removed.

- **"No standard deviation or statistical significance."** Single-run reporting is the established norm in LLM benchmarking on these tasks. Removed.

- **"At T=1, the SNN has no temporal dynamics — it is functionally a quantized ANN with a different activation function."** This overstates the case. An SNN with T=1 still uses threshold-based spiking neurons (Eqs. 8–10), discrete spike outputs, and the IS neuron dynamics; it is not "functionally a quantized ANN." The valid concern (performance degrades with T) is already captured in Major weakness #1. Removed the exaggerated framing.

- **"Section 4.3: performance does vary non-trivially."** The accuracy range is ~2.2 points (65.46–67.65) across very different group sizes (1 to 256). The claim "does not vary significantly" is a reasonable characterization of this variation for the intended purpose; the best performer is also the default configuration. Removed as borderline and does not harm the core claim.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the gap between the paper's SNN framing and its actual evidence base, but this is a critical evaluation rather than a novel observation about the method.

## Suggestions

1. **Add at least one SNN baseline.** The most natural candidate is SpikeZIP (You et al., 2024), which the paper already cites and whose spiking-compatible operations it adopts. Even a rough comparison on identical models and tasks would establish where this method sits relative to prior SNN-based LLM approaches.

2. **Measure energy or efficiency directly.** At minimum, report theoretical synaptic operations (synops) or spike-accumulation vs. multiply-accumulate counts for the SNN at different T settings. Without this, the energy-efficiency motivation remains speculative.

3. **Diagnose and address the T-degradation.** The paper should analyze whether the calibration actually reduces unevenness error at T>1, or whether the multi-threshold IS neuron introduces new sources of temporal error that grow with T. If the method is inherently limited to low-T operation, this should be forthrightly stated as a limitation rather than attributed to a standard error type that behaves differently here.

4. **Specify the calibration data budget.** Report the number of calibration samples, selection method, and ablation over calibration set size.

5. **Qualify the "comparable to quantization" claim.** State explicitly which T setting the claim refers to, and acknowledge that performance degrades as T increases.

## Score and Decision

The paper identifies a genuine practical bottleneck and proposes a clean conceptual solution with impressive parameter efficiency. However, the evaluation contains three major gaps: (1) accuracy degrades with time steps, inverting the expected SNN behavior and limiting practical utility; (2) the entire energy-efficiency motivation is asserted and never measured; and (3) no prior SNN-based LLM baselines are included. These gaps collectively mean the paper's core claims are insufficiently supported by the evidence presented. The paper presents a promising direction but requires substantially stronger evaluation before its contribution can be assessed.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>