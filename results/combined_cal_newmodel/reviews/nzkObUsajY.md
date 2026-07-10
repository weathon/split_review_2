Now let me compose the final consolidated review.

## Summary

This paper proposes a pipeline for converting quantized LLMs (via training-free PTQ) into spiking neural networks. The key idea is to replace the quantization function in PrefixQuant with a multi-level Integer Spiking (IS) neuron, then apply a lightweight layer-wise calibration that adjusts only thresholds and initial membrane potentials (~0.107K parameters per layer). Experiments on LLaMA-2-7B and LLaMA-3-8B show substantial recovery of accuracy compared to the uncalibrated conversion (e.g., 59.99% → 67.65% on LLaMA-2-7B at T=2), approaching the quantized ANN baseline.

## Strengths

- **Practical pipeline design (Section 3.2, Figure 1).** The core idea — starting from a training-free PTQ quantized LLM (PrefixQuant), replacing the quantization function with an Integer Spiking (IS) neuron, and then applying lightweight calibration — is pragmatically motivated. It avoids the expensive step of training a conversion-friendly ANN from scratch, which is the main barrier to applying ANN-to-SNN conversion to LLMs. [favorability=13.22]

- **Parameter efficiency of calibration (Section 4.4, Table 4).** The calibration method uses ~0.107K learnable parameters per layer and achieves accuracy competitive with full weight fine-tuning (67.65 vs 66.39 avg. acc. on LLaMA-2-7B). While perplexity is worse (7.39 vs 6.37), the accuracy difference is small and the parameter savings are dramatic. This is the strongest empirical result in the paper. [favorability=10.41]

- **Substantial recovery from uncalibrated conversion (Table 2).** On LLaMA-2-7B at T=2, uncalibrated conversion achieves 59.99% avg. acc.; calibration recovers this to 67.65%, approaching the quantized baseline of 68.70%. Similar recovery is shown across T=4 and T=8. This demonstrates that the calibration addresses a real degradation. [favorability=11.74]

- **The paper targets a challenging and timely problem** — converting LLMs to SNNs for potential edge deployment — and proposes a sensible pipeline that avoids training a conversion-specific ANN, which is a practical barrier in existing methods. [favorability=12.57]

## Weaknesses

### Fatal
None.

### Major

- **Missing comparison against existing spiking LLM methods.** The paper cites SpikeZIP (You et al., 2024) as "the dominant approach" in ANN-to-SNN conversion for LLMs (line 35), yet never compares against it or any other spiking LLM method experimentally. The baselines used (PrefixQuant, DuQuant) are quantization methods that produce standard ANNs, not SNNs. The 'Conversion' baseline in Table 2 is an ablation of the proposed method itself (uncalibrated version), not an external baseline. Without a comparison against other spiking LLM approaches, the paper cannot substantiate the claim that it advances the state of the art in spiking LLMs specifically. [favorability=-0.14]

- **Multi-level spikes undermine the energy-efficiency motivation, with no analysis provided.** The IS neuron (Eq. 9) outputs spikes valued 0, 1, 2, …, L, where L can be large (e.g., L=63 for T=1 with n=6 bits). The standard energy-efficiency argument for SNNs relies on binary spikes enabling MAC-to-AC conversion. Multi-level spikes require multi-bit arithmetic, negating this core advantage. The paper motivates SNNs as offering "low power consumption" and "brain-inspired efficiency" for edge deployment throughout the introduction and abstract, but provides no spike statistics, energy estimates, or discussion of how multi-level spiking affects hardware efficiency. A central premise of the paper is therefore unsubstantiated. [favorability=-0.02]

### Minor

- **The theoretical analysis does not provide actionable guarantees.** Theorem 2 claims equivalence between the IS neuron and symmetric quantization under the condition LT = 2^n - 1, but Remark 1 admits this condition "rarely holds for arbitrary integer choices of L and T if T ≠ 1." The paper then resorts to approximation with no error bound. Theorem 3 bounds conversion error in terms of per-layer Lipschitz constants ρ^k, but these constants are never computed, estimated, or bounded — the bound is purely existential. The calibration method (minimizing per-layer MSE) stands on its own empirical merit without requiring this theoretical scaffolding. [favorability=0.17]

- **Anomalous scaling behavior in Table 3.** As the group size decreases from 256 to 1 (and per-layer learnable parameters increase from 0.194K to 23.399K), average accuracy drops monotonically from 67.40 to 65.46. The best result (67.65) is achieved with the *smallest* parameter count (0.107K at group size -1). This is the opposite of what one would expect if calibration genuinely learns to correct conversion errors. The paper attributes this to "strong adaptability" without investigating possible causes such as overfitting on the calibration set, optimization instability, or the default thresholds being already near-optimal. [favorability=1.25]

- **Narrow evaluation scope.** The evaluation uses only five zero-shot reasoning tasks (PIQA, ARC, HellaSwag, WinoGrande) and only one quantization setting (W6A6). Standard LLM evaluation also includes benchmarks like MMLU and GSM8K. Only W6A6 is tested; lower bit-widths (W4A4, W4A8) are unexplored. No inference latency or calibration overhead (samples, steps, wall time) is reported, despite claiming "low-latency" (Table 1). [favorability=1.36]

- **Figure 3 y-axis error.** The caption describes the right y-axis as ranging from -8 to 2 (linear scale) representing MSE loss. MSE cannot be negative, so this is either an error in the axis description or the metric is not MSE. [favorability=0.76]

### Trivial
None.

## Nice-to-Haves

- **Test on larger models (e.g., LLaMA-2-13B)** to support the scalability claim. The paper currently evaluates only the smallest members of each family.
- **Test on additional quantization settings** (W4A4, W4A8) to understand sensitivity to quantization scheme.
- **Provide calibration overhead details** (number of samples, optimization steps, wall time).
- **Provide inference latency measurements** to substantiate the "low-latency" claim in Table 1.

## Removed Points

These points were flagged in the input review but are removed with justification:

- *"Missing comparison with existing SNN methods for LLMs"* → Kept as Major weakness (verified against paper; SpikeZIP cited but not compared).
- *"No energy or efficiency measurements"* → Merged into the "multi-level spikes" Major weakness.
- *"Missing scalability to 13B/70B models"* → Removed as scope creep. The paper calls itself "a seed effort" and 7B/8B evaluation is a reasonable starting point.
- *"Eq. 10 notation confusing"* → Removed. Notation like s^k(t) = s^k(t) - α^k(t) is non-standard but common in dynamical systems; not a substantive weakness.
- *"Missing appendix content / deferred implementation details"* → Removed. Parser strips appendix sections; they exist in the original submission.
- *"Theory doesn't do the work claimed"* → Reframed as Minor weakness about actionable guarantees, not a fatal flaw.
- *"Only W6A6 tested"* → Merged into narrow evaluation scope (Minor).
- *Generic formatting/style nitpicks* → Removed per parser artifact policy.

## Novel Insights

The reviews surface the core tension in this paper: the pipeline is practically motivated and the parameter efficiency is genuinely impressive, but the two major gaps (missing SNN comparison, no energy analysis) prevent it from making a convincing case that it advances spiking LLMs specifically. The paper's strongest contribution is the practical calibration scheme (0.107K parameters per layer achieving accuracy within ~1% of the quantized ANN), which is a genuine engineering result — but this stands as a method for recovering accuracy after PTQ-to-SNN conversion, not yet as a validated spiking LLM system.

## Suggestions

1. **Compare against at least one existing spiking LLM method** (e.g., SpikeZIP) to contextualize the contribution within the SNN literature.
2. **Provide spike statistics and energy analysis:** Report the distribution of spike values (fraction >1), the effective energy cost relative to the quantized ANN baseline, or at minimum discuss the trade-offs of multi-level spiking explicitly.
3. **Investigate the anomalous Table 3 behavior** — explain why more calibration parameters lead to worse performance.
4. **Report calibration overhead** (number of samples, optimization steps, wall time) and inference latency.
5. **Fix the Figure 3 y-axis description** (MSE cannot be negative).

---

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| SpikeZIP (u438df0Uce.md) | 3.60 | R1 | Yes | Most directly related (ANN-QANN-SNN). Current paper is stronger: avoids training QANN, targets LLMs, better empirical LLM results. |
| QAC (D4sQzdMvcG.md) | 5.75 | R1 | Yes | Similar concept with calibration but on smaller CV models. Stronger theory, similar empirical quality. |
| When-SNN-meets-ANN (GTzP2GC7NR.md) | 5.75 | R2 | Yes | Conversion with modified neurons. Stronger writing and theory, but limited novelty concerns. |
| SpikeBERT (6c4gv0E9sF.md) | 6.33 | R2 | Yes | Spiking language model via direct training (not conversion). Different approach, mixed reviews (8,8,3). |
| Spatio-Temporal (XrunSYwoLr.md) | 7.00 | R1 | Yes | Stronger accepted paper: training-free SNN conversion for Transformers. More thorough evaluation. |
| CSS Coding (mtmqwhQiaG.md) | 5.25 | R1 | Yes | SNN coding scheme. Different focus, similar issues with missing energy analysis. |

**Round 1 bracket:** between 3.6 and 5.75.
**Round 2 narrowing:** The paper's two Major weaknesses (favorability ~0) are more severe than the worst items in the 5.75 cluster, but the paper's strengths are clearly superior to the 3.6 SpikeZIP anchor. The paper sits squarely between these two bands.

**Final score rationale:** The paper's practical pipeline and parameter-efficient calibration are genuine contributions. However, the two Major gaps — missing comparison against the spiking LLM methods it cites, and the unanalyzed tension between multi-level spikes and the energy-efficiency motivation — are not minor omissions. They cut to whether the paper's contribution is validated against the correct baselines and whether its motivating premise is supported. The paper makes an honest step toward spiking LLMs but is not yet complete enough for acceptance.

<score>4.0</score>
<decision>Reject</decision>