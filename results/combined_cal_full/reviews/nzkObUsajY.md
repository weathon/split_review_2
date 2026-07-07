Now I have all the information needed. Let me write the final review.

## Summary

This paper proposes a dual ANN-to-SNN conversion framework for LLMs, where the conversion goes through a post-training quantized (PTQ) intermediate representation rather than requiring a specially trained conversion-friendly ANN. The key contributions are: (1) an Integer Spiking (IS) neuron with multi-hierarchical thresholds designed to approximate the quantization function, enabling conversion from any PTQ-quantized LLM; (2) a parameter-efficient layer-wise calibration that optimizes only thresholds and initial membrane potentials (0.107K parameters vs 202M for full weight calibration); and (3) an explicit decomposition of conversion errors (clipping, quantization, unevenness) with evidence that unevenness error is dominant.

## Strengths

- **Eliminates need for a conversion-friendly trained ANN (Sections 1, 3.2).** Conventional ANN-to-SNN conversion requires training or fine-tuning the source ANN with a specialized activation (QCFS, ReLU, etc.), which is prohibitively expensive for LLMs. By instead starting from a PTQ-quantized LLM and designing IS neurons that directly approximate the quantization function, the paper sidesteps this cost. This is a genuine architectural insight.

- **Parameter-efficient calibration (Section 3.4, Table 4).** The calibration optimizes only thresholds and initial membrane potentials — 0.107K parameters per layer for LLaMA-2-7B, compared to 202.375M for full weight fine-tuning. Remarkably, this tiny calibration outperforms full weight calibration on average accuracy (67.65% vs 66.39% for LLaMA-2-7B, T=2). This result is striking and worth highlighting.

- **Explicit decomposition of conversion errors (Section 3.3).** The paper distinguishes three types of error (clipping, quantization, unevenness) and provides empirical evidence (Figure 3) that unevenness error is the dominant factor. This decomposition is useful for the community even if the analysis has limitations.

## Weaknesses

### Fatal

None.

### Major

- **No energy, latency, or spike statistics reported despite energy-efficiency being the paper's core motivation.** The paper repeatedly motivates SNNs through energy efficiency (Abstract: "brain-inspired efficiency and low power consumption"; Introduction: "significantly reduced energy consumption"; Contribution 3: "potentially reduces the energy consumption of LLMs"), yet provides zero evidence on firing rates, spike counts, energy estimates, or latency. The IS neuron with L-level thresholds and T time-steps can theoretically generate many spikes per inference, making it unclear whether the converted SNN would actually be more energy-efficient than the quantized ANN baseline. Without any spike statistics or energy estimates, the paper's central motivation is unevidenced. This is not a missing experiment; it is the core claim left unvalidated.

- **The accuracy-perplexity results do not fully support the claim of "performance comparable to state-of-the-art quantization techniques."** For LLaMA-2-7B at T=2, average accuracy is 67.65 vs PrefixQuant's 68.70 (a modest ~1% gap), but perplexity is 7.39 vs 5.76 — a 28% relative degradation — and the gap grows with T (9.71 at T=4, 12.03 at T=8). While accuracy looks reasonable, perplexity degradation is substantial and under-discussed in the paper's narrative framing. Since perplexity on WikiText-2 is a standard generative quality metric, this gap raises questions about whether generation quality is preserved.

### Minor

- **The theoretical analysis is largely generic rather than specific to the proposed method.** Theorem 3 provides a standard Lipschitz-based error propagation bound that would apply to any ANN-to-SNN conversion with Lipschitz layers. The Lipschitz constants ρ^k are never computed, estimated, or bounded. The paper claims "theoretical analysis demonstrates that our calibration method substantially lowers the final conversion error" (Abstract) and "theory-backed layer-wise calibration" (Contribution 2), but Theorem 3 does not specifically analyze the IS neuron design, the multi-hierarchical thresholds, or the dual conversion framework. The calibration method is motivated primarily by the empirical observation in Figure 3, not by the theorem's bound.

- **Performance decreases with increasing time-steps T** (Table 2: T=2→T=4→T=8 all show degradation for both LLaMA-2-7B and LLaMA-3-8B). This is unusual — for conventional ANN-to-SNN conversion, more time-steps improve approximation. The paper attributes this to growing unevenness error but does not provide a mechanistic explanation for why more time-steps make unevenness error worse. This raises questions about the practical utility of the method at larger T.

### Trivial

None.

## Nice-to-Haves

- Measure and report spike statistics (average firing rate per layer, spike count per inference) and provide a concrete energy estimate relative to the QANN baseline. This directly addresses the paper's own motivation.
- Provide a dedicated analysis of how non-linear operations (Softmax, LayerNorm, SiLU, attention) are handled in the SNN and how they interact with the IS neuron framework, rather than delegating entirely to prior work.
- Test at lower bit widths (W4A4, W4A8) to understand the method's range of viability, since the theoretical equivalence condition (LT = 2^n - 1) becomes harder to satisfy at lower bit widths.
- Provide a mechanistic explanation for why performance degrades with increasing time-steps T, ideally with supporting analysis or ablations.

## Removed Points

These points from the input review were removed after cross-checking against the paper:

1. **Non-linear operations delegated to prior work (original Issue 2):** The harsh critic claimed this "hollows out" the spiking LLM claim. However, the paper explicitly states "we adopt the spiking-compatible operations proposed in You et al. (2024)" and notes "Additional implementation details are provided in the Appendix" (stripped by the parser). Adopting prior work for non-core components is standard practice, and the core contribution (IS neuron design + calibration) is unaffected.

2. **Calibration optimizes total error, not unevenness specifically (original Issue 5):** The calibration target min ||Σ_t ŷ^k(t) - y^k|| directly minimizes the unevenness error as defined in Definition 1 (||Σ_t ŷ^k(t) - \bar{y}||). The paper's claim that it reduces "conversion error, particularly unevenness error" is accurate since the objective is exactly the unevenness error.

3. **"Training-free" framing is misleading:** The paper never claims the entire pipeline is training-free. Section 3.2 says "training-free quantization technique" (referring to PrefixQuant), and Table 1 says "Training Tailored ANN: No" — which is accurate. The calibration step is described as "parameter-efficient," not training-free.

4. **No error bars:** For zero-shot evaluation with lm-evaluation-harness, single-run reporting without error bars is standard practice in the LLM quantization literature.

5. **Missing related work:** Not verifiable. The paper cites relevant prior work (SpikeGPT, SpikeZIP, You et al. 2024).

6. **Formatting/style nitpicks and parser artifacts:** These are parser errors, not author errors.

7. **Missing appendix content:** The parser strips the appendix from all papers; the original submission contains it.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Recenter the paper's contribution on the IS neuron design and parameter-efficient calibration, and qualify the energy-efficiency claims with a clear statement that energy benefits are theoretical and unmeasured.
2. Address the perplexity degradation head-on — explain why the method preserves multiple-choice accuracy but degrades perplexity, and under what conditions this trade-off is acceptable.
3. Add a small-scale energy analysis (even theoretical MAC vs. spike-based AC comparisons using estimated firing rates from a small calibration set) to validate the core motivation.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8QTpYC4smR.md` | 1.00 | R1 | No | Survey paper; unrelated quality |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/u438df0Uce.md` (SpikeZIP) | 3.60 | R1 | Yes | Most directly related — same ANN-QANN-SNN paradigm. Our paper has more novelty (IS neuron) and better calibration results, so scores higher |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/mtmqwhQiaG.md` (Canonic Signed Spike) | 5.25 | R1 | No | Similar-level contribution (novel encoding/neuron) but more complete evaluation; our paper is comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/GTzP2GC7NR.md` (When SNN meets ANN) | 5.75 | R1 | Yes | Stronger theoretical treatment of conversion; our paper has comparable empirical novelty but weaker theory-evaluation connection |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/D4sQzdMvcG.md` (QAC) | 5.75 | R2 | No | Similar quantization-aware conversion concept; comparable scope |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/mJ4mgYjDru.md` (QIF Neuron) | 4.60 | R2 | Yes | Similar pattern — novel neuron design with limited evaluation; our paper targets harder LLM problem |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6c4gv0E9sF.md` (SpikeBERT) | 6.33 | R2 | Yes | Spiking language model; stronger evaluation but overclaimed results similar to our paper |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XrunSYwoLr.md` (Spatio-Temporal Approx.) | 7.00 | R1 | Yes | Higher quality: stronger theory, addresses nonlinearities directly. Our paper has better parameter efficiency but weaker evaluation |

**Round 1 bracket:** 4.5–6.0, narrowed from comparison of weighted items.

**Weighted-item comparison grounding:** The paper's strongest positive weights (+5.01 parameter-efficient calibration, +4.37 error decomposition, +4.34 eliminating conversion-friendly ANN) are comparable to the mid-range anchors (Canonic Signed Spike at 5.25, QIF Neuron at 4.60). However, the negative weight on generic theoretical analysis (-6.29) is severe and comparable in magnitude to the strongest negatives on SpikeZIP (-8.01, -9.55). The missing energy evidence (-5.24) is also a heavy negative. These combined negatives push the paper below Spatio-Temporal Approximation (7.00) and SpikeBERT (6.33), settling it alongside the mid-range anchor papers at ~5.0.

The IS neuron design is a genuine contribution, and the calibration's parameter efficiency is striking (0.107K beating 202M on accuracy). However, the paper claims energy benefits it never measures, overstates its theoretical backing, and under-discusses the perplexity degradation. On balance, this is a paper with a solid core idea that needs stronger evaluation to meet its own claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>