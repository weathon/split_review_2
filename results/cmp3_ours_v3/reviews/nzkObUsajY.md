Now let me write the final consolidated review with calibration-informed scoring.

## Summary

This paper proposes a "dual" ANN-to-SNN conversion framework for LLMs that eliminates the need to train a conversion-friendly ANN. Instead, it starts from a training-free quantized LLM (PrefixQuant), introduces an Integer Spiking (IS) neuron with multi-hierarchical thresholds to approximate the quantization function, and uses a parameter-efficient layer-wise calibration (optimizing only ~0.107K parameters per layer) to reduce unevenness error. Experiments on LLaMA-2-7B and LLaMA-3-8B at W6A6 show the calibration substantially recovers accuracy lost during uncalibrated conversion.

## Strengths

1. **Practical re-framing of the conversion pipeline.** The core idea — using a training-free quantized LLM as the starting point rather than training a conversion-friendly ANN — addresses a real bottleneck. Training a QCFS-based LLM from scratch is prohibitive for large models, and the paper's pipeline avoids this (Section 3.2, Figure 1). This is a genuinely practical insight.

2. **Parameter-efficient calibration recovers large accuracy losses.** The layer-wise calibration optimizes only IS neuron thresholds and initial membrane potentials (~0.107K params per layer), not the full weights (~202M per layer for LLaMA-2-7B). Table 4 shows this achieves comparable or better accuracy than full weight calibration (67.65 vs 66.39 Avg Acc) while using ~6 orders of magnitude fewer parameters.

3. **Calibration substantially closes the conversion gap.** The gap between uncalibrated "Conversion" and calibrated "Ours" in Table 2 is large — e.g., on LLaMA-2-7B at T=2, uncalibrated Avg Acc is 59.99 vs calibrated 67.65, a recovery of 7.66 points. This demonstrates the calibration is doing meaningful work.

## Weaknesses

### Fatal
None.

### Major
1. **No comparison against any existing spiking LLM method.** The paper cites SpikeZIP (You et al., 2024) in the introduction as "the dominant approach" for ANN-to-SNN conversion, yet Table 2 compares only against *quantization* methods (PrefixQuant, DuQuant). The "Conversion" rows are an ablation of the authors' own pipeline (uncalibrated IS neurons), not a prior SNN method. Since the paper's title asks "How to Get Spiking LLMs?" and claims to propose a method for doing so, the absence of experimental comparison against other ways of *obtaining spiking LLMs* (SpikeZIP, SpikeGPT, or any converted SNN baseline) leaves the paper's central claim untested. The reader cannot evaluate whether the proposed SNN outperforms, matches, or underperforms existing spiking LLM approaches.

2. **No energy analysis despite this being the central motivation for SNNs.** The paper invokes "brain-inspired efficiency and low power consumption" (abstract), "potentially reduces the energy consumption of LLMs" (contribution 3), and "power demands of dense matrix multiplication" (Section 2.1). Yet it contains no measurement, estimate, or theoretical calculation of energy consumption, synaptic operations, or firing rates. Without this, the paper reduces to showing that an SNN approximates a quantized ANN with accuracy loss — the *reason* to use an SNN (energy efficiency) is never evaluated. This is a structural gap: the motivation is energy, but the experiments measure only accuracy.

3. **No ablation comparing the IS neuron against a standard IF neuron in the same pipeline.** The IS neuron with multi-hierarchical thresholds is presented as a key technical innovation, but there is no experiment comparing IS-based conversion against IF-based conversion using the same quantization starting point and the same calibration procedure. Without this, it is impossible to determine whether the IS neuron design is necessary — the calibration may be doing all the work regardless of the neuron model.

### Minor
1. **Performance degrades with more timesteps, and the explanation is incomplete.** For calibrated models, Avg Acc drops as T increases (LLaMA-2-7B: 67.65 at T=2 → 66.03 at T=8; LLaMA-3-8B: 69.03 → 63.76). The paper attributes this to "growing unevenness error" but does not provide a detailed layer-wise analysis or demonstrate that this can be mitigated. In conventional ANN-to-SNN conversion, more timesteps improve approximation; the observed degradation is counterintuitive and deserves deeper investigation.

2. **Theorem 3 (Lipschitz-based error bound) is not connected to the experiments.** The bound is a standard Lipschitz propagation result that provides no specific insight about the IS neuron or the dual conversion. It is not computed, tracked, or validated against empirical MSE or accuracy results. The theory and experiments are thus disengaged.

3. **Calibration optimization details are missing.** The paper does not specify the number of calibration samples, optimizer, learning rate, or number of optimization steps used for the layer-wise calibration. These details are needed for reproducibility.

4. **Only tested at W6A6 with a single quantizer (PrefixQuant).** The method's sensitivity to bit-width (e.g., W4A4, W8A8) and to alternative quantizers (e.g., DuQuant, QuaRot) is unexplored. Since the entire pipeline depends on the quantized starting point, this limits generality.

5. **Perplexity is systematically worse than the quantized baseline and this is not discussed.** For LLaMA-2-7B at T=2, PrefixQuant achieves PPL 5.76 while the calibrated SNN achieves 7.39, and at T=4 the gap widens to 9.71. The paper discusses accuracy prominently but does not adequately address the perplexity degradation, which matters for language modeling quality.

### Trivial
1. The term "dual" is used throughout (title, abstract, Section 3.2) but never clearly defined. The pipeline has two stages (quantization → SNN conversion + calibration), but "dual" in a mathematical sense is not justified. A more descriptive framing would improve clarity.
2. SpikeZIP is cited in the introduction as the exemplar of ANN-to-SNN conversion for LLMs but is not discussed in Section 2.2 (Related Work), creating an internal inconsistency.

## Nice-to-Haves
- Compare against SpikeZIP or another spiking LLM conversion method on the same models and tasks.
- Add firing-rate estimates and energy consumption estimates using a standard SNN energy model.
- Ablate the IS neuron against standard IF neurons in the same pipeline.
- Provide a deeper error analysis showing which layers accumulate the most unevenness error as T increases.
- Test at additional bit-widths (W4A4, W8A8) and with alternative quantizers.
- Include calibration hyperparameters (optimizer, learning rate, number of steps, calibration dataset size) for reproducibility.

## Removed Points
- "The 'ANN-to-SNN conversion' baseline mentioned in the text is not actually present in Table 2." — Factually wrong: the "Conversion" rows in Table 2 are the uncalibrated conversion baseline, and "Weight" in Table 4 is the full-parameter calibration baseline. Both are present.
- "At T=1, the 'SNN' is not really spiking" as a criticism — This is a known property of conversion methods at T=1 (the quantized model), not a unique flaw of this paper.
- "The paper would benefit from being restructured and positioned more honestly" — Subjective framing critique, not an actionable weakness.
- Various formatting and presentation nitpicks — These are parser artifacts, not author errors.

## Novel Insights
The reviews surface three well-identified gaps (missing spiking LLM baselines, missing energy analysis, missing IS-vs-IF ablation) that collectively weaken the paper's claims but do not invalidate the core approach. The most useful insight is that the paper's framing and evaluation are misaligned: the paper's title and motivation focus on spiking LLMs, but the experiments only compare against quantization techniques. The core idea — using PTQ as a training-free bridge — is genuinely novel and practical, but the evaluation does not yet validate the claimed contribution of a viable spiking LLM.

## Suggestions
1. Add a comparison against at least one existing spiking LLM method (e.g., SpikeZIP) on the same tasks and models.
2. Include energy consumption estimates or, at minimum, firing-rate statistics to connect the SNN's behavior to its claimed energy advantage.
3. Add an ablation replacing the IS neuron with a standard IF neuron within the same pipeline to isolate the IS's contribution.
4. Provide calibration optimization details (optimizer, learning rate, steps, data).
5. Perform a bit-width sensitivity analysis (W4A4, W8A8) and test with at least one alternative quantizer.
6. Explicitly discuss the perplexity gap between the SNN and the quantized baseline.

## Score and Decision

**Calibration anchors (all retrieved rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| SpikeLLM (`ZadnlOHsHv`) | 7.00 | R1 (5.5–7.5) | More comprehensive spiking LLM paper with energy analysis, scales to 70B. Current paper is weaker. |
| Spatio-Temporal Approx (`XrunSYwoLr`) | 7.00 | R1 (5.5–7.5) | Training-free SNN conversion for ViT, strong theory + energy analysis. Current paper targets harder LLM problem but evaluation is less thorough. |
| SpikeBERT (`6c4gv0E9sF`) | 6.33 | R1 (5.5–7.5) | Language spikformer via KD; rejected (split 8,8,3). Current paper is comparable in quality but has different gaps. |
| QAC (`D4sQzdMvcG`) | 5.75 | R2 (5.0–6.5) | Mixed-timestep conversion with calibration; rejected for limited scope. Similar pattern of strengths/weaknesses to current paper. |
| Error-Free ANN-to-SNN (`GTzP2GC7NR`) | 5.75 | R1 (5.5–7.5) | Conversion with BN bias shift; rejected (requires retraining). Current paper has more novel core idea but similar evaluation limitations. |
| Canonic Signed Spike (`mtmqwhQiaG`) | 5.25 | R1 (3.5–5.5) | Coding scheme for SNNs; rejected. Comparable contribution level. |
| Bridge SNN/ANN (`G3vceNrP4o`) | 4.00 | R1 (3.5–5.5) | Distillation for image restoration; rejected. |
| SpikeZIP (`u438df0Uce`) | 3.60 | R1 (3.5–5.5) | QANN-to-SNN for image models; rejected (lack of novelty). Current paper is stronger (more novel idea for a harder problem). |

**Round 1 bracket:** 4.0–6.5 (after examining anchors from all bands, the paper sits between SpikeZIP/SpikeBERT/SpikeLLM)

**Round 2 narrowing:** 5.0–6.0 (comparing against QAC at 5.75 and Error-Free at 5.75, the current paper has a more novel core idea but similar evaluation gaps)

**Final score:** 5.5. The paper has a genuinely novel and practical core idea (using PTQ as a bridge for SNN conversion, eliminating costly training of conversion-friendly ANNs), and the calibration method is clearly effective at recovering accuracy. However, three substantial evaluation gaps — no comparison against existing spiking LLM methods, no energy analysis despite energy being the central motivation, and no ablation of the IS neuron against IF — prevent the paper from validating its core claims about producing a viable spiking LLM. The paper is below the acceptance bar but has a clear path to improvement.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>