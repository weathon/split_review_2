Now I have all the information needed to construct the final review. Let me produce it.

## Summary

This paper proposes a dual ANN-to-SNN conversion framework for LLMs that avoids training a conversion-friendly ANN by starting from an already-quantized LLM (obtained via training-free PTQ). The method replaces quantization functions with a novel Integer Spiking (IS) neuron — a multi-level threshold neuron shown theoretically to approximate symmetric quantization — and applies parameter-efficient layer-wise calibration of thresholds and initial membrane potentials to reduce conversion error (particularly "unevenness error" from temporal spike dynamics). Experiments on LLaMA-2-7B and LLaMA-3-8B show that calibration with only 0.107K parameters per layer recovers accuracy after conversion, with results at T=1 and T=2 approaching those of the quantized baseline.

## Strengths

- **The core idea addresses a real bottleneck.** Conventional ANN-to-SNN conversion requires training a specialized conversion-friendly ANN (e.g., with QCFS activation), which is prohibitively expensive at LLM scale. Starting from an off-the-shelf quantized LLM (obtained via training-free PTQ) removes this bottleneck entirely (Section 3.2, Figure 1). This is a clean, practically motivated design insight.

- **The IS neuron design is theoretically grounded in the quantization function it replaces.** Theorems 1 and 2 (Section 3.2.2) establish conditions under which the multi-level spiking neuron's cumulative output exactly equals or approximates the symmetric quantization function. This principled connection between spiking dynamics and quantization justifies the neuron design as more than a heuristic.

- **Parameter efficiency of calibration is genuinely impressive and well-demonstrated.** Table 4 shows that calibrating per-layer thresholds and initial membrane potentials (0.107K parameters per layer) matches or exceeds full weight fine-tuning (202M parameters) on accuracy for LLaMA-2-7B (67.65 vs. 66.39 Avg. Acc.). This is a concrete, nontrivial empirical finding that gives the method practical appeal.

## Weaknesses

### Fatal
None.

### Major

- **No comparison against any existing spiking LLM method.** The paper evaluates only against quantization methods (PrefixQuant, DuQuant). The related work (Section 2.2) discusses SpikeGPT, SpikeBERT, and SpikeZIP as existing spiking approaches, and the method itself uses SpikeZIP's spiking-compatible operations for nonlinearities (line 150). Yet none appear in the experiments. The paper positions itself as building a "spiking LLM" via ANN-to-SNN conversion, but a reader cannot assess how it compares to other spiking LLMs in accuracy or efficiency. If existing methods cannot scale to 7B+ models, this should be stated explicitly as a justification for comparing only against quantization methods; as presented, the omission appears as an oversight that leaves the paper's claimed domain unaddressed by its evaluation.

- **No energy consumption estimates despite energy efficiency being the central motivation.** The abstract, introduction, and conclusion all motivate the work by SNNs offering "brain-inspired efficiency and low power consumption" and "potentially reduc[ing] the energy consumption of LLMs" (lines 9, 49). There are zero energy measurements, zero synaptic operation counts, zero FLOPs comparisons, and no discussion of how spiking operations translate to energy savings on any hardware platform. The central promised benefit is entirely unsupported by evidence.

- **SNN performance degrades monotonically with increasing time steps — the SNN cannot exploit temporal integration.** Across both models, accuracy decreases as T increases (LLaMA-2-7B: 68.79 at T=1 → 66.03 at T=8; LLaMA-3-8B: 71.67 at T=1 → 63.76 at T=8). The best configuration by a clear margin is T=1, where the IS neuron emits a single multi-level output with no temporal dynamics — effectively a quantized activation function, not a spiking network exhibiting event-driven behavior across time. This is the opposite of conventional ANN-to-SNN conversion, where firing rates converge to activations as T increases. The paper acknowledges the degradation and attributes it to "growing unevenness error" (Section 4.2), but this describes the symptom rather than resolving it. If higher T — where event-driven efficiency advantages would materialize — produces strictly worse results, the method's practical operating regime is limited to ultra-low latency where the spiking advantages are minimal.

### Minor

- **Potential data integrity concern with DuQuant results.** The DuQuant accuracy numbers are identical across LLaMA-2-7B and LLaMA-3-8B in Table 2 (67.88, 72.64, 40.53, 53.07, 77.15, 62.25 on all five tasks), with only PPL differing (5.53 vs 6.27). Identical accuracy across five independent tasks for different model families is highly unlikely and suggests a copy-paste error in the table.

- **Calibration procedure is underspecified.** The paper optimizes per-layer thresholds and initial membrane potentials (line 188) but does not describe what calibration dataset is used, how many forward passes or optimization steps are required, what optimizer is used, or the total computational cost of calibration relative to the baselines. This directly affects reproducibility and also the paper's "training-free" framing (line 101) — the conversion itself is training-free, but the calibration step involves optimization whose cost is undisclosed.

- **Imprecision in Theorem 3 / calibration target.** The calibration target is min ||∑_t ŷ^k(t) − y^k|| (line 188), and the text says it "reduc[es] the gap between the source ANN and the converted SNN." However, Theorem 3 decomposes total error into SNN-vs-QANN and QANN-vs-ANN components. The calibration target should minimize the SNN-vs-QANN term, not directly the SNN-vs-ANN gap. The text conflates the two, creating potential confusion about what the calibration actually achieves.

- **IS neuron novelty relative to prior M-HT neurons is unclear.** The paper describes it as "a modified Integer Spiking (IS) neuron — also referred to as the Multi-Hierarchical Threshold (M-HT) neuron" (line 122) but does not clearly differentiate which modification distinguishes the IS neuron from prior M-HT neurons. Given the importance of the neuron design to the paper's contribution, the novelty should be explicitly stated.

### Trivial

- **Missing "Ours T=8" row for LLaMA-2-7B in Table 2.** The table shows Conversion T=8 for 2-7B (line 227) and then jumps to "3-8B | Ours T=8" (line 228) with no intervening Ours T=8 row for 2-7B. If this is a parser artifact it should be clarified; if the experiment was not run, the omission should be explained.

- **Figure 3 uses mismatched scales** (left y-axis log-scale 0.02–3.5, right y-axis linear -8 to 2) making visual comparison between the two curves misleading.

## Nice-to-Haves

- An ablation study disentangling the contributions of threshold calibration vs. membrane potential calibration would help understand which component does most of the work.
- Testing with other quantization backends (e.g., QuaRot, DuQuant) or bit-widths (e.g., W4A4) would strengthen claims of generality.
- Clarifying whether the DuQuant identical numbers are a formatting error would resolve a distracting concern.

## Removed Points

These points from the input review were flagged for removal; treat them with caution:

- **"Framing oversells"** — removed as a subjective presentation concern, not a factual weakness. The paper's performance claims are supported at T=1 and partially at T=2.
- **"Generalizability to other quantization formats"** — removed as speculative; the paper evaluates under one consistent setting and does not claim generality beyond it.
- **"Uncalibrated SNN is catastrophically bad"** — removed because the paper deliberately uses calibration to recover from poor uncalibrated performance; this is the design, not a weakness. The related underspecification point is retained separately.
- **"More ablation studies needed"** — weakened to nice-to-have; the paper does ablate group size (Table 3) and compare against weight calibration (Table 4).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the T-dependent degradation or explicitly reframe the method** for low-latency (T=1 or T=2) operation, and discuss whether those regimes still deliver the energy benefits that motivate spiking networks. If higher T cannot be improved, the paper should be upfront that this is a low-latency-only conversion method.

2. **Add comparison against at least one existing spiking conversion method**, or explicitly explain why no such comparison is feasible at 7B+ scale. The paper currently leaves its claimed domain of "spiking LLM" methods unaddressed by its evaluation.

3. **Provide energy estimates** — even standard analytical estimates based on synaptic operations, as commonly reported in the SNN literature — to support the paper's central motivating claim.

4. **Specify the calibration procedure** (dataset, optimizer, steps, compute cost) to enable reproducibility and assessment of the "training-free" claim.

5. **Clarify the IS neuron's modifications** over prior M-HT neurons to establish novelty more clearly.

6. **Reconcile the duplicated DuQuant accuracy numbers** in Table 2.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>