Now I have all the information I need. Let me compile the final review.

## Summary

This paper proposes a dual ANN-to-SNN conversion framework for LLMs that eliminates the need to train a specialized conversion-friendly ANN. Instead, it starts from an off-the-shelf quantized LLM and introduces an Integer Spiking (IS) neuron with multi-hierarchical thresholds that approximates the quantization function. A parameter-efficient layer-wise calibration method (optimizing only 0.107K thresholds and membrane potentials per layer) reduces conversion error, particularly the unevenness error from temporal spike dynamics. Experiments on LLaMA-2-7B and LLaMA-3-8B at W6A6 precision show the calibrated SNN performs close to the source quantized LLM.

## Strengths

1. **Genuinely novel and practical core idea.** The insight of bypassing expensive retraining of a conversion-friendly ANN by starting from an already-available quantized LLM, and designing a spiking neuron that directly approximates the quantization function (Section 3.2), is clever and well-motivated. This directly addresses a real scalability bottleneck in conventional ANN-to-SNN conversion for LLMs.

2. **Clean theoretical grounding.** Theorems 1 and 2 (Section 3.2.2) characterize the IS neuron's behavior and specify conditions under which it mimics a symmetric quantization function. Theorem 3 provides a conversion error bound with layer-wise Lipschitz constants, and Remark 1 honestly acknowledges the practical gap when the exact equality LT = 2ⁿ − 1 does not hold.

3. **Genuinely parameter-efficient calibration.** The layer-wise calibration (Section 3.4) freezes all weights and only optimizes thresholds and initial membrane potentials (0.107K parameters per layer, Table 4), which is roughly 2 million times fewer than full weight fine-tuning (202M parameters). Table 3 shows stable performance across a range of group sizes, so the method is not brittle to this hyperparameter.

4. **Calibration substantially recovers from the uncalibrated SNN.** The gap between "Conversion" (uncalibrated) and "Ours" (calibrated) in Table 2 is dramatic — LLaMA-2-7B at T=2 goes from 59.99→67.65 Avg. Acc. and PPL from 12.42→7.39. This convincingly demonstrates that the layer-wise calibration addresses unevenness error as claimed.

## Weaknesses

### Fatal
None.

### Major

1. **No comparison against any existing SNN conversion method for LLMs.** The baselines (PrefixQuant, DuQuant) are quantization methods, not SNN methods. The paper cites SpikeZIP (You et al., 2024) as a "recent advance" in ANN-to-SNN conversion for LLMs and adopts its spiking-compatible operations, yet SpikeZIP never appears in any result table. The paper also mentions SpikeGPT and SpikeBERT without comparison. Because the paper's core contribution is a new *conversion framework*, the absence of any SNN-to-SNN comparison means the reader cannot assess whether this method produces better or worse spiking LLMs than existing alternatives. The evaluation only shows how much is lost in the QANN → SNN conversion, not whether the result is competitive as an SNN. This is a structural gap in the evaluation relative to the paper's stated contribution.

2. **Performance degrades meaningfully as temporal depth increases, undermining the spiking value proposition.** The paper claims "low-latency" (Table 1). At T=1, there is no temporal spike train and no event-driven computation — the "SNN" is effectively a reparameterized QANN. At T>1, where true spiking behavior emerges, performance degrades significantly:
   - LLaMA-3-8B: Avg. Acc. drops from 71.67 (T=1) → 69.03 (T=2) → 67.21 (T=4) → 63.76 (T=8); PPL rises from 6.66 to 18.93.
   - LLaMA-2-7B: Avg. Acc. drops from 68.79 (T=1) → 66.03 (T=8); PPL rises from 5.61 to 12.03.
   
   The paper attributes this to unevenness error but does not resolve it. If the best-performing configuration (T=1) lacks temporal spiking, and temporal configurations degrade with more time steps, the claimed energy-efficiency benefit (which depends on event-driven computation at T>1) is undermined by the accompanying accuracy loss. The paper does not quantify this trade-off.

### Minor

1. **No energy efficiency measurements despite being the paper's core motivation.** The abstract, introduction, and conclusion all motivate through energy efficiency ("brain-inspired efficiency and low power consumption," "potentially reduces energy consumption"). Yet the paper provides zero energy measurements, analytical models, or even theoretical operation counts (e.g., synaptic operations vs. MACs). This is a standard gap in the ANN-to-SNN literature, but given the paper's framing — where SNNs are presented as a solution to quantization's residual energy problem (Section 2.1: "significant energy consumption during LLM operation remains a barrier... even with low-bit quantized versions") — the absence of any empirical or analytical energy evidence is a concrete limitation.

2. **No ablation comparing the IS neuron against a standard IF neuron.** The IS neuron with multi-hierarchical thresholds is presented as a key design element, but the paper never compares against using a standard IF neuron (with appropriate rescaling) for the same conversion. Without this, it is unclear whether the IS neuron's design is responsible for the observed performance, or whether the calibration alone (which could be applied to any conversion) drives the improvements.

3. **The practical approximation gap from Remark 1 is not empirically characterized.** Remark 1 notes that the exact equivalence LT = 2ⁿ − 1 rarely holds when T ≠ 1, and the paper resorts to L = ⌈(2ⁿ − 1)/T⌉, meaning the IS neuron only approximately matches the quantization function. The actual effect of this approximation on conversion accuracy at T > 1 is never measured or ablated, leaving an unexplained gap between the theory and the empirical results.

4. **Inconsistent behavior between PPL and accuracy in the weight fine-tuning comparison (Table 4).** Weight fine-tuning achieves better PPL (6.37 vs. 7.39) but worse Avg. Acc. (66.39 vs. 67.65) than the proposed calibration for LLaMA-2-7B. The paper does not discuss this cross-metric inconsistency, which makes the comparison less clean than claimed and suggests the weight fine-tuning baseline may not have been properly tuned.

### Trivial
None.

## Nice-to-Haves

- Compare against at least one existing SNN conversion method for LLMs (e.g., SpikeZIP) to ground the evaluation in the SNN literature.
- Provide an analytical energy model (e.g., synaptic operations vs. multiply-accumulate operations) or even a theoretical FLOPs comparison to support the energy-efficiency claims.
- Ablate the IS neuron design against a standard IF neuron to isolate the contribution of the multi-hierarchical thresholds.
- Characterize the empirical effect of the L = ⌈(2ⁿ − 1)/T⌉ approximation at T > 1.
- Explain what the layer-wise calibration is correcting at T=1, where there is no temporal dimension and the IS neuron should theoretically match the quantization function exactly.

## Removed Points

These points from the input review are removed per filtering rules:

- **"Figure 3's scale appears physically impossible (negative MSE)"** — The figure is an embedded image; the axis labels are OCR output. MSE being negative is a parser artifact, not an author error.
- **"Code is not released"** — Hard rule: do not penalize papers that promise code release upon publication.
- **"Only W6A6 tested"** — The paper explicitly scopes to W6A6; testing one precision is within scope.
- **"Only 7B and 8B tested"** — These are already very large models for SNN research; demanding 13B/70B evaluation is scope creep for a paper of this type.
- **"Calibration details underspecified"** — These details may appear in the appendix (stripped by the parser). The main-text description is sufficient to understand the method.
- **"No comparison against direct training methods"** — The paper explains why direct training is not applicable at this scale; this is a reasonable scope limitation.
- **Missing related works** — Cannot verify without external sources; hard rule against this.
- **Formatting/style nitpicks** — Parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a comparison against at least one existing SNN conversion or spiking LLM method to ground the evaluation in the SNN literature. SpikeZIP is the natural candidate since the paper already adopts its spiking-compatible operations.
2. Provide some form of energy analysis (analytical operation counts, estimated synaptic operations vs. MACs, or even theoretical FLOPs) to support the energy-efficiency motivation that the paper leans on heavily.
3. Include an IF-neuron ablation to isolate the IS neuron's contribution from the calibration's contribution.
4. Characterize the empirical effect of the L = ⌈(2ⁿ − 1)/T⌉ approximation at T > 1.
5. Discuss the cross-metric inconsistency (PPL vs. accuracy) in the weight fine-tuning comparison of Table 4.

## Score Calibration

**Round 1 (bracketing):** Retrieved anchors across score bands for ANN-to-SNN conversion and spiking LLM topics.

**Anchor papers used:**

| Paper | Avg Score | Dec. | How it compares to the reviewed paper |
|---|---|---|---|
| SpikeZIP (u438df0Uce) | 3.60 | Reject | Same QANN→SNN conversion paradigm but criticized for lack of novelty; current paper is more novel (IS neuron, dual conversion) |
| SpikeLLM (ZadnlOHsHv) | 7.00 | Accept | First spiking LLM at up to 70B scale; comparable novelty, broader evaluation, but similar energy-efficiency gaps |
| Spatio-Temporal Approx. (XrunSYwoLr) | 7.00 | Accept | Training-free SNN conversion for transformers; similar theoretical contribution, but on ViT not LLM |
| When SNN meets ANN (GTzP2GC7NR) | 5.75 | Reject | ANN-to-SNN conversion with BN shift; limited novelty, no LLM evaluation |
| SpikeBERT (6c4gv0E9sF) | 6.33 | Reject | Language spikformer via distillation; mixed reviews (8,8,3), not conversion-based |
| QAC (D4sQzdMvcG) | 5.75 | Reject | Quantization-aware conversion; similar concept but for CNNs, limited scope |
| Canonic Signed Spike (mtmqwhQiaG) | 5.25 | Reject | New SNN coding scheme; no LLM application, criticized for energy concerns |
| Temporal Misinformation (sgke1JuVlc) | 5.00 | Reject | Probabilistic spiking neurons; mixed reviews, not at LLM scale |

**Round 1 bracket:** 4.0 – 7.0 (the paper has stronger novelty than the 3.6–5.75 papers but weaker evaluation than the 7.0 papers).

**Narrowing:** Compared against SpikeLLM (7.0) — the current paper has comparable novelty but tests only 7B/8B vs. up to 70B, has no SNN baselines vs. multiple baselines, and lacks energy analysis. Compared against Spatio-Temporal Approximation (7.0) — both are training-free with theory, but current paper's evaluation gaps (no SNN baselines, no energy analysis) are more significant. Compared against QAC/When SNN meets ANN (5.75) — current paper has stronger novelty and theory but similar evaluation weaknesses. **Final score: 5.5.** The paper has a solid core contribution and theoretical grounding, but the evaluation has structural gaps (missing SNN baselines, unmeasured energy claims, unexplained T>1 degradation) that prevent it from meeting the acceptance threshold.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>