Now I'll produce the final review.

## Summary

This paper proposes a dual ANN-to-SNN conversion framework for obtaining spiking LLMs. Instead of training a conversion-friendly ANN (conventional practice), the approach starts from a pre-quantized LLM and converts it to an SNN using an Integer Spiking (IS) neuron with multi-hierarchical thresholds designed to approximate the quantization function. A layer-wise calibration technique that optimizes only thresholds and initial membrane potentials (0.107K parameters per layer) reduces conversion error. Experiments on LLaMA-2-7B and LLaMA-3-8B show the method achieves accuracy within ~1% of quantized baselines while using orders of magnitude fewer learnable parameters than full weight fine-tuning.

## Strengths

1. **Well-motivated problem.** The observation that conventional ANN-to-SNN conversion requires training a conversion-friendly ANN, which becomes prohibitive at LLM scale, is a real and underexplored bottleneck. Targeting this problem is worthwhile.

2. **Parameter efficiency of calibration is genuinely striking (Table 4).** Calibrating only thresholds and initial membrane potentials (0.107K parameters per layer) achieves comparable or better accuracy than fine-tuning all weights (202M parameters). On LLaMA-2-7B, calibration achieves 67.65% vs weight fine-tuning's 66.39% average accuracy — better results with 6 orders of magnitude fewer parameters. This is the paper's most concrete and persuasive result.

3. **Using pre-quantized LLMs as the conversion source is a sensible direction.** It sidesteps the expensive re-training step that prior ANN-to-SNN conversion methods require and leverages the existing ecosystem of post-training quantization techniques.

## Weaknesses

### Major

1. **Performance degrades with more timesteps, undermining the claim of a viable spiking model.** In conventional ANN-to-SNN conversion, more timesteps improve approximation quality. Here the results show the reverse: LLaMA-2-7B accuracy drops monotonically from 68.79 (T=1) → 67.65 (T=2) → 67.04 (T=4) → 66.03 (T=8). The uncalibrated "Conversion" rows show catastrophic degradation (39.82% at T=8). At T=1, the "SNN" is functionally equivalent to a quantized ANN with multi-level activation — each neuron emits at most L spikes in a single timestep with no meaningful temporal dynamics. The paper attributes this to "growing unevenness error" but does not resolve it. The method is therefore most useful precisely in the regime (T=1) where it is least distinguishable from a quantized ANN, and accuracy drops when temporal dynamics are introduced.

2. **No energy efficiency measurements despite this being the primary motivation.** The paper repeatedly motivates SNNs through "brain-inspired efficiency and low power consumption" (abstract, introduction, contribution 3). Yet it provides zero measurements of energy consumption, spike counts, operations, or any proxy for power usage. For a method whose accuracy is slightly below quantization baselines, the absence of evidence for any energy advantage is a critical gap — the reader cannot assess whether the trade-off is worthwhile.

3. **Missing comparison against existing spiking LLM methods.** The paper cites SpikeZIP (You et al., 2024) as a representative advance in spiking LLMs but never compares against it in experiments. The only SNN baselines are the authors' own uncalibrated conversions; all other baselines (PrefixQuant, DuQuant) are quantization techniques. If the contribution is a better approach to building spiking LLMs, comparison to prior spiking LLM work is essential for assessing relative merit.

### Minor

4. **IS neuron approximation error is acknowledged but uncharacterized.** Theorem 2 establishes exact equivalence to the quantization function only when LT = 2^n - 1. Remark 1 concedes this equality "rarely holds for arbitrary integer choices of L and T if T ≠ 1" and resorts to "≈" with L = ceil(2^{n-1}/T). No bound is given on the deviation when equality fails. Since the IS neuron is the core mechanism enabling the conversion, characterizing this gap (even with a worst-case bound) would substantially strengthen the theoretical foundation.

5. **The "training-free" framing is imprecise.** The paper describes the framework as "training-free" (line 101), but Section 3.4 defines an optimization problem min_{θ^k, v^k(0)} ||∑ ŷ^k(t) - y^k|| solved by running forward passes on calibration data. While this is lightweight and only tunes 0.107K parameters per layer, it is technically a form of optimization. The claim would be more precise as "eliminates the need to train a conversion-friendly ANN" (which the paper also states) rather than "training-free."

6. **Theorem 3 is a standard Lipschitz perturbation bound without specific connection to the proposed design.** The error bound follows Lipschitz continuity assumptions standard in this literature (the paper cites Bu et al., 2022; Hao et al., 2023a). The theorem does not incorporate any property specific to the IS neuron, the dual conversion framework, or the calibration method. Remark 3's inference that this "implies that Layer-wise calibration of these errors can effectively mitigate the overall conversion error" is reasonable but is a generic consequence of any per-layer error bound, not a result specific to the proposed approach.

### Trivial

None.

## Nice-to-Haves

- A characterization of the IS neuron approximation error when LT ≠ 2^n - 1 (e.g., a bound on |Σ ŝ^k(t)θ^k − X_q^k| in terms of L and T).
- Energy estimates: total spike counts per forward pass, or estimated energy using published per-operation costs for neuromorphic hardware.
- Comparison against SpikeZIP or another spiking LLM baseline.
- Analysis of whether T > 1 provides any measurable benefit over T=1 (e.g., increased spike sparsity, temporal computation advantages, or improved calibration stability).

## Removed Points

These points from the input review were removed with justification:

- **"Three intervals condition cannot be guaranteed"** (from Critical Issue 1): REMOVED — factually incorrect. Theorem 1 and 2 state the intervals are "mutually exclusive and exhaustive," meaning they partition ℝ. The condition is automatically satisfied for any input I^k(t). The reviewer misread this as an unachievable constraint.

- **"SNN underperforms quantization methods"** (Critical Issue 6): REMOVED — overstated by the reviewer. The gap vs PrefixQuant is ~1% on average for Ours at T=2. For LLaMA-3-8B at T=1, Ours (71.67) actually outperforms PrefixQuant (70.24). The claim of "comparable performance" is reasonable for this margin.

- **"Theoretical foundation is unobtainable"** (part of Critical Issue 1): REMOVED — the paper transparently acknowledges the approximation in Remark 1. While characterizing the gap would strengthen the paper, the acknowledgment itself is honest, and the practical approximation L = ceil(2^{n-1}/T) is standard for integer-constrained systems. The reviewer's framing that this "undermines the entire method" is too severe given that the paper already uses and discloses the approximation.

- **Generic strengths removed** (none — all three listed strengths are specific and evidence-backed).

## Novel Insights

None beyond the paper's own contributions. The most informative result not foregrounded by the paper is that optimizing only 0.107K scalar parameters per layer (thresholds and initial membrane potentials) recovers nearly all accuracy lost during ANN→QANN→SNN conversion, while full weight fine-tuning with 202M parameters yields worse accuracy on LLaMA-2-7B (66.39 vs 67.65). This suggests conversion error is dominated by mismatches in neuronal response scales and offsets rather than weight values — a finding that could inform future conversion method design.

## Suggestions

1. Provide a theoretical bound for the IS neuron approximation error when LT ≠ 2^n - 1.
2. Report spike counts or estimated energy consumption for the converted SNNs.
3. Include SpikeZIP or another spiking LLM as a baseline.
4. Discuss the T > 1 regime more honestly — either demonstrate a benefit of temporal spiking dynamics or acknowledge that the method is primarily a quantized ANN with SNN-compatible activation at T=1.

## Score and Decision

**Calibration anchors (all retrieved from the human-review corpus):**

| Path | Avg Human Score | Round | Comparison to this paper |
|------|----------------|-------|------------------------|
| SpikeZIP (u438df0Uce.md) | 3.60 | Bracketing | ANN-QANN-SNN conversion for CNNs; rejected for lack of novelty and weak analysis. Current paper is more novel (targets LLMs, IS neuron) and addresses a harder problem. |
| EfficientSkip (7DY2DFDT0T.md) | 2.50 | Bracketing | Sparse LLM conversion; rejected. Not directly comparable. |
| S-TLLR (vlQ56aWJhl.md) | 5.00 | Bracketing | STDP-based SNN training; rejected. Not directly comparable. |
| Temporal Misinfo (sgke1JuVlc.md) | 5.00 | Bracketing | ANN-SNN conversion with probabilistic neurons; high reviewer variance (8,6,3,3). |
| Canonic Signed Spike (mtmqwhQiaG.md) | 5.25 | Bracketing | Spike coding for efficient SNNs; rejected. |
| When SNN meets ANN (GTzP2GC7NR.md) | 5.75 | Bracketing | ANN-to-SNN for CNNs (ImageNet); rejected for novelty concerns. More thorough evaluation than current paper but targets an easier problem. |
| SpikeBERT (6c4gv0E9sF.md) | 6.33 | Bracketing | Spiking BERT via knowledge distillation; rejected. |
| Spatio-Temporal Approx (XrunSYwoLr.md) | 7.00 | Bracketing | Training-free SNN conversion for ViT; accepted. Solid theory and evaluation. |
| SpikeLLM (ZadnlOHsHv.md) | 7.00 | Bracketing | First spiking LLM with saliency-based spiking; accepted. More thorough evaluation (energy, larger models, more baselines) than current paper. |

**Round 1 bracket:** The paper sits clearly above SpikeZIP (3.60) because it targets a harder, more timely problem (LLMs) with a more novel approach. It sits below When SNN meets ANN (5.75) due to less thorough evaluation (no energy measurements, missing SNN baselines, unresolved T-degradation). Narrowed plausible range: 4.0–5.0.

**Round 2 narrowing:** The paper is below SpikeLLM (7.00) which had energy estimates, comparisons at 70B scale, and broader baseline coverage. The paper is above SpikeZIP (3.60) which was criticized for lack of novelty — the current paper's IS neuron design and parameter-efficient calibration are demonstrably novel. The most natural anchor is mid-way between SpikeZIP and When SNN meets ANN: 4.5.

**Final score: 4.5.** The paper has genuine merits (well-motivated problem, elegant parameter-efficient calibration, sensible use of pre-quantized models) but has significant gaps (performance degradation with more timesteps undermines the spiking claim, no energy measurements despite energy being the primary motivation, missing comparison against existing spiking LLM work, uncharacterized approximation error). These weaknesses are structural and would require substantial new experiments and analysis to resolve.

**Decision: Reject.** The paper identifies a worthwhile problem and has one genuinely striking result (Table 4), but the core claim of producing a *spiking* LLM is not adequately supported — the method excels at T=1 (where it is functionally a quantized ANN) and degrades at T>1 (where meaningful spiking dynamics would emerge). The absence of energy measurements and missing SNN baselines further weaken the case. These are significant enough to warrant rejection in the current form.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>