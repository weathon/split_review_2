Now I have sufficient calibration data. Let me write the final consolidated review.

**Round 1 Bracket:** Based on the calibration search, the closest anchors are SpikeZIP (3.60, QANN-to-SNN conversion, penalized for novelty/evidence gaps) and When SNN meets ANN (5.75, error-free conversion, penalized for data issues). SpikeLLM (7.00) provides an upper bound — it has a similar motivation but provides energy estimates and stronger baselines. The current paper's strengths (genuinely novel pipeline, parameter efficiency) push it above SpikeZIP (3.60), but its critical missing evidence (no energy analysis, no SNN baselines, weak theory) keeps it well below SpikeLLM (7.00). **Bracket: 4.0–5.5.**

**Narrowing:** Comparing my draft's scored items against the anchors:

- The current paper shares SpikeLLM's weakness of missing baseline comparisons (-10.00 → comparable to SpikeLLM's -9.37) and goes further by lacking ALL energy analysis (-9.98) where SpikeLLM at least provided estimates.
- Unlike SpikeZIP, whose core idea was deemed non-novel and was penalized accordingly (-10.00 novelty), the current paper's core pipeline idea IS novel and scores as a high-magnitude strength (+9.12).
- The parameter efficiency strength (+8.67) and low-latency operation (+9.91) are distinct advantages not matched by any anchor in the 3–6 range.
- However, the weak theory weakness (-10.00) is a decisive negative that cannot be overcome by revision alone — the Lipschitz bound is generic, the constants are never computed, and Theorem 2's conditions are admitted to "rarely hold in practice."

The paper's **final score of 4.5** reflects: a genuinely novel core idea and impressive parameter efficiency (pulling toward 5.5+), weighed against three high-magnitude unaddressed gaps — no energy evidence, no SNN baselines, and substantively empty theory (pulling toward 3.5–4.0). This places it between SpikeZIP (3.60) and When SNN meets ANN (5.75), in the borderline reject range.

---

## Summary

This paper proposes a "dual" ANN-to-SNN conversion framework for LLMs that starts from an off-the-shelf quantized LLM (PrefixQuant), replaces the quantization function with a multi-level Integer Spiking (IS) neuron, and calibrates only thresholds and initial membrane potentials (0.107K parameters/layer). The core idea — eliminating the need to train a conversion-friendly ANN — is sound and addresses a genuine practical bottleneck. However, the paper suffers from three critical evidentiary gaps: (1) no energy measurements or estimates despite being motivated entirely by SNN energy efficiency, (2) no comparison with any prior SNN method (SpikeZIP is cited but never evaluated), and (3) theoretical analysis that does not provide numerically meaningful bounds.

## Strengths

- **The core idea is sensible and addresses a real practical bottleneck.** Eliminating the need to train a conversion-friendly ANN for LLM-to-SNN conversion is a genuine contribution. The pipeline of taking an off-the-shelf quantized LLM (PrefixQuant) and converting it via neuron replacement is cleaner than the conventional pipeline (Section 3.2, Figure 1).

- **The parameter efficiency of the calibration step is impressive.** Calibrating only thresholds and initial membrane potentials (0.107K parameters per layer) instead of full weight fine-tuning (202M parameters for LLaMA-2-7B) achieves comparable or better accuracy (Table 4).

- **The experiments cover multiple model families (LLaMA-2, LLaMA-3) and multiple time-steps (T=1,2,4,8),** and the gap between the uncalibrated "Conversion" baseline and the calibrated "Ours" variant is dramatic (e.g., LLaMA-2-7B T=2: 59.99% → 67.65%), confirming the calibration step matters.

- **The paper operates at low timesteps (T=2,4,8),** which is a genuine advance over conventional ANN-to-SNN conversion that typically requires 50+ timesteps to reach comparable performance (Section 3.2, Table 1).

## Weaknesses

### Major

- **No energy measurements or estimates of any kind.** The paper is motivated throughout by the energy efficiency of SNNs for edge deployment (Abstract, Introduction, Section 2.2), and Contribution 3 explicitly claims the method "potentially reduces the energy consumption of LLMs." Yet the only evidence offered is the general assertion that SNNs are energy-efficient. No operations count, no MAC vs. AC comparison, no neuromorphic hardware simulation, and no theoretical energy analysis is provided. For a paper whose entire framing rests on energy advantages over quantized ANNs, this is a missing central piece of evidence.

- **No comparison with any prior SNN conversion method for LLMs.** SpikeZIP (You et al., 2024) is cited in Section 2 as a "recent advance" in ANN-to-SNN conversion for LLMs, but it does not appear anywhere in the experimental comparison (Table 2). The only SNN results in the table are the authors' own "Conversion" (uncalibrated) and "Ours" (calibrated). A paper that proposes a new SNN conversion method for LLMs cannot omit all prior SNN work from its benchmark — this makes it impossible for a reader to assess the method's position in the subfield it claims to advance.

- **The theoretical analysis does not deliver numerically meaningful bounds.** Theorem 2 states exact equivalence between the IS neuron and the quantization function under conditions (including \(LT = 2^n - 1\)) that Remark 1 acknowledges "rarely hold in practice." The approximation error when conditions are violated is never quantified. Theorem 3 provides a generic Lipschitz-based error bound (Equation 11) that does not leverage any specific property of the IS neuron or conversion method, and the Lipschitz constants \(\rho^k\) are never computed. The claim of a "theory-backed" method (Contribution 2) is not substantiated by the analysis presented.

- **Figure 3 uses dual axes with mismatched scales** (left y-axis: logarithmic 0.02–3.5; right y-axis: linear –8 to 2) to compare ANN-vs-QANN error and ANN-vs-SNN error. The different scales make the visual comparison uninterpretable, undermining the claim that unevenness error "plays mainly character" (Section 3.3). A single-axis comparison or properly normalized metrics are needed to support this diagnostic claim.

### Minor

- **At T>1 the method underperforms the quantized ANN baseline it builds on** (PrefixQuant). For LLaMA-2-7B T=2: 67.65% vs 68.70% Avg Acc, PPL 7.39 vs 5.76; at T=8: 66.03% vs 68.70% Avg Acc, PPL 12.03 vs 5.76. While the accuracy gap is modest (~1–3 pp), the PPL degradation (more than doubling at T=8) is notable for a generation model. Performance degrades with increasing T, which the paper attributes to unevenness error without providing a mechanism to reverse or mitigate this trend.

- **The IS neuron fires at multiple discrete levels** (Equation 9: levels 0,1,...,L) rather than binary spikes. With L=16 at T=2 (W6A6), the neuron communicates one of 16 distinct values per timestep. The paper does not discuss how this multi-level design affects the energy-efficiency narrative relative to conventional binary-spike SNNs — e.g., whether the event-driven and AC-only computation benefits still hold to the same degree.

- **No ablation study isolating the contribution of the IS neuron design** versus using a standard Integrate-and-Fire (IF) neuron with the same calibration procedure. Since the calibration is the main driver of improvement over the uncalibrated baseline, a comparison with IF + calibration would clarify whether the multi-level IS neuron is necessary or whether the benefits come primarily from the calibration step.

- **The weight calibration baseline in Table 4 compares against full fine-tuning** of all 202M parameters (LLaMA-2-7B). A lightweight fine-tuning baseline (e.g., LoRA) would provide a more informative comparison for highlighting the parameter-efficiency advantage.

### Trivial

None.

## Nice-to-Haves

- Provide at least a rough analytical energy estimate (operations count, MAC vs AC per forward pass, accounting for multi-level spike communication) to support the energy-efficiency motivation.
- Include SpikeZIP or another SNN-LLM method as a baseline.
- Replace Figure 3 with a single-axis comparison or properly normalized metrics.
- Add an ablation comparing IS neuron vs. IF neuron under the same calibration procedure.
- Quantify the approximation error of Theorem 2 when \(LT \neq 2^n - 1\) (the practically relevant case).
- Discuss why perplexity degrades with increasing T and whether this is inherent to the approach.

## Removed Points

These points were flagged by the harsh critic but removed for the following reasons:

- **"The method does not produce a genuine spiking neural network"** — REMOVED. The IS neuron with multi-level outputs is a recognized spiking neuron variant cited from prior work (Sun et al., 2022; Wang & Zhang, 2023; Li & Zeng, 2022; Hao et al., 2024). While the energy implications differ from binary-spike SNNs, categorizing it as "not a genuine SNN" overstates the case. The (weaker) point about missing discussion of multi-level firing's effect on energy claims is retained as a Minor weakness above.

- **"T=1 results reveal the method adds nothing beyond the quantization baseline"** — REMOVED. T=1 functions as a sanity check showing the IS neuron can match the quantization function. The paper's temporal contribution is at T>1. Criticizing T=1 for "adding nothing" misunderstands the role of this baseline.

- **"The 'unevenness error' definition conflates different error sources"** — REMOVED. The logical decomposition is sound: the difference between ANN-vs-QANN error (clipping+quantization) and ANN-vs-SNN error (clipping+quantization+unevenness) does isolate unevenness error. The visualization issue is retained as a Minor weakness above.

## Novel Insights

The central insight from the reviewing process is that the paper's core contribution (a clean, training-free conversion pipeline from quantized LLMs to spiking models with parameter-efficient calibration) is genuinely valuable, but the paper systematically fails to provide the evidence that would turn this idea into a convincing submission. The gap is largest around energy — the paper's entire motivation is energy efficiency, yet it provides no energy analysis whatsoever. This is a more severe omission than typical "missing experiments" because the claimed advantage (energy-efficient spiking LLMs) cannot be evaluated by the reader in any form.

## Suggestions

1. **Add energy analysis.** Even a rough analytical estimate (operations per forward pass: MACs vs ACs, accounting for multi-level spike communication) would substantially strengthen the paper. This is the single most critical addition.
2. **Include SpikeZIP or another SNN-LLM baseline.** Without it, the paper cannot demonstrate its position in the SNN-for-LLM subfield.
3. **Add IF + calibration ablation** to isolate the benefit of the IS neuron design from the calibration procedure.
4. **Replace Figure 3** with a clean single-axis comparison.
5. **Quantify the approximation error** when \(LT \neq 2^n - 1\), or de-emphasize the theoretical equivalence claim.
6. **Discuss the perplexity degradation with T** and whether this is a fundamental limitation or addressable.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>