Now I have strong calibration anchors. Let me produce the final review.

## Summary

This paper proposes a "dual ANN-to-SNN conversion" framework for LLMs that avoids the prohibitive cost of training a conversion-friendly ANN. Starting from an off-the-shelf quantized LLM (PrefixQuant), it replaces the quantization function with a novel Integer Spiking (IS) neuron with multi-hierarchical thresholds, then applies a parameter-efficient layer-wise calibration that optimizes only thresholds and initial membrane potentials (~0.1K parameters per layer). Experiments on LLaMA-2-7B and LLaMA-3-8B demonstrate that the calibrated SNN recovers most of the accuracy lost during conversion, operating at T=2 to T=8 time steps — far lower than conventional conversion.

## Strengths

- **Practical starting point (weight=9.26).** The paper correctly identifies that training a conversion-friendly ANN from scratch for LLMs is prohibitively expensive. By leveraging off-the-shelf quantized LLMs (PrefixQuant) as the source, the method sidesteps this bottleneck. This is a sensible practical choice that makes the approach feasible at LLM scale (Section 3.2, Table 1).

- **Parameter-efficient calibration (weight=9.30).** The calibration method (Section 3.4) is genuinely lightweight — it optimizes only thresholds and initial membrane potentials while freezing weights, using 0.107K parameters per layer versus 202M for full weight tuning (Table 4). The ablation in Table 3 shows performance is reasonably robust across different group sizes. This is a well-designed, minimal intervention that recovers a significant fraction of the accuracy lost during conversion.

- **IS neuron design bridges quantization and spiking (weight=9.34).** The Integer Spiking (IS) neuron with multi-hierarchical thresholds is designed to approximate the quantization function, providing a principled bridge from quantized ANNs to SNNs (Theorem 1–2, Section 3.2.2). This design choice makes the "dual conversion" (quantized LLM → SNN) theoretically grounded.

- **Low-latency conversion (weight=8.80).** The method operates at T=2 to T=8 time steps, which is substantially lower than conventional ANN-to-SNN conversion (often requiring >50 time steps). If the spiking model's energy benefit holds, this low latency is important for practical deployment (Section 3.2, Table 1).

## Weaknesses

### Fatal
None.

### Major

- **No comparison against existing SNN methods (weight=-3.04).** The paper cites SpikeZIP (You et al., 2024) and adopts its spiking-compatible operations for nonlinear layers (Section 3.2.3, line 150), but the experiments compare only against pure quantization methods (PrefixQuant, DuQuant), the uncalibrated conversion, and full-weight fine-tuning. There is no comparison against SpikeZIP or any other SNN conversion method. This makes it impossible to assess the paper's contribution relative to prior SNN work. Adding this comparison — even a limited reimplementation at the same scale — is essential to establish where the proposed method stands in the SNN literature.

- **No energy evaluation (weight=-0.07).** The paper motivates spiking LLMs with "brain-inspired efficiency and low power consumption" (Abstract, line 9) and claims the approach "potentially reduces the energy consumption of LLMs" (contributions, line 49), yet contains zero energy measurements, spike-rate statistics, synaptic operation counts, or any quantitative estimate of power consumption. Since the baselines (PrefixQuant, DuQuant) also reduce computational cost, the paper cannot substantiate why one would prefer a spiking version. Adding at least a spike-rate analysis and estimated synaptic operations per forward pass would substantially strengthen the paper.

### Minor

- **Performance gap versus quantization baseline at practical time steps.** For LLaMA-2-7B at T=2 (the most practical setting), the calibrated SNN achieves 67.65 Avg. Acc. vs. 68.70 for PrefixQuant, with PPL degrading from 5.76 to 7.39 (Table 2). The gap widens at T=4 (67.04, 9.71 PPL) and T=8 (66.03, 12.03 PPL). The abstract's claim of "performance comparable to state-of-the-art quantization techniques" is most accurate at T=1, where the SNN degenerates to a non-spiking state. The paper acknowledges this degradation but should more precisely scope the claim.

- **Theoretical results are weaker than claimed.** Remark 1 concedes that the core equivalence condition *LT = 2ⁿ − 1* "rarely holds for arbitrary integer choices of L and T" (line 142), meaning Theorem 2's exact equivalence does not apply in practical settings. Theorem 3's error bound involves products of per-layer Lipschitz constants that could grow exponentially with depth (32 layers for LLaMA-2-7B), but the paper neither bounds nor estimates these constants, making the bound potentially vacuous.

- **Perplexity variation in Table 3 not fully discussed.** The paper states performance "does not vary significantly across different parameter sizes" (line 247), but PPL swings from 6.89 (group size 16) to 9.17 (group size 64) — a meaningful difference that warrants explanation.

- **Conclusion overstates results.** The conclusion claims "showcasing substantial improvements in accuracy" (line 275) without clarifying that these improvements are relative to the *uncalibrated* conversion baseline, not the quantized LLM source model.

### Trivial
None.

## Nice-to-Haves
- Report calibration data requirements (number of calibration samples used).
- Include results at T=16 or T=32 to establish whether the degradation trend flattens or continues.
- Add a second perplexity benchmark (e.g., C4) to broaden the evaluation.
- Provide an ablation comparing IF neurons vs. IS neurons at identical settings.

## Removed Points

These points from the input review were removed after cross-checking against the paper; they should be treated with caution:

1. **Figure 3 MSE negative values (right axis -8 to 2).** Removed as a formatting artifact from automatic PDF extraction — MSE cannot be negative and the original figure has correct labels. This is a parser error, not an author error.

2. **DuQuant results identical for both model sizes (Table 2).** Removed. The accuracy numbers are identical for LLaMA-2-7B and LLaMA-3-8B in the DuQuant rows, but PPL differs (5.53 vs. 6.27). Without external verification, this could be a reproduced result from the DuQuant paper; it is not a confirmed error.

3. **"Training-free" terminology criticism.** Removed. The paper clearly distinguishes between the conversion being training-free (no weight training needed for the neuron replacement) and the calibration being a separate parameter-optimization step. The usage is standard in the literature.

4. **α^k(t) notation confusion.** Removed. The paper explains that α^k(t) is user-set (Section 3.2.2, line 130) and Theorem 2 provides a concrete setting. This is sufficiently clear for a conference paper.

5. **Calibration data budget not reported / additional perplexity datasets / ablation on IS neuron design.** Removed per filtering guidelines — these are either nice-to-haves or minor implementation details that do not affect the paper's validity.

6. **Request for larger T (T=16, T=32).** Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews surface well-known issues in the ANN-to-SNN conversion literature (missing energy evaluation, lack of SNN baselines, theory-practice gaps) rather than providing novel diagnoses of the paper.

## Suggestions

1. **Add an SNN baseline comparison.** Compare against SpikeZIP (You et al., 2024) or a reimplementation of its conversion approach at the same model scale (LLaMA-2-7B). This is the most important addition for establishing the paper's contribution to the SNN literature.

2. **Add energy estimation.** Report spike rates per layer, estimate synaptic operations per forward pass, and compare estimated energy to the quantized ANN baseline using standard SNN energy models. This addresses the gap between the paper's motivation and its evidence.

3. **Clarify the scope of "comparable" in the abstract.** Specify that the method achieves results comparable to quantization methods at T=1 and approaches comparable performance at T=2–4 with acceptable degradation, rather than claiming unqualified comparability.

4. **Estimate or bound the Lipschitz constants in Theorem 3** to make the theoretical bound meaningful, or reframe the theorem as a qualitative motivation for layer-wise calibration rather than a tight quantitative guarantee.

5. **Acknowledge the PPL swing in Table 3** and discuss why group size 16 achieves the best PPL (6.89) while the default configuration (group size -1) has a higher PPL (7.39).

## Score and Decision

### Calibration summary

**Round 1 — Bracketing (score bands):**
All calibration queries used "ANN-to-SNN conversion spiking neural networks" across 6 score brackets. The most relevant anchors retrieved were:

| Anchor | Score | Decision | Relevance |
|--------|-------|----------|-----------|
| SpikeZIP | 3.60 | Reject | Highly relevant — cited by the paper, same QANN→SNN paradigm |
| Temporal Misinformation & Conversion | 5.00 | Reject | Relevant — ANN-SNN conversion error analysis |
| Canonic Signed Spike Coding | 5.25 | Reject | Relevant — SNN coding for conversion |
| Bridge Gap SNN/ANN for Image Restoration | 4.00 | Reject | Less relevant (image restoration task) |
| When SNN meets ANN | 5.75 | Reject | Relevant — error-free conversion, CNN scale |
| QAC | 5.75 | Reject | Relevant — mixed-timestep conversion, quantization-aware |
| **Spatio-Temporal Approximation** | **7.00** | **Accept (itemized)** | **Highly relevant — training-free Transformer→SNN conversion** |
| QP-SNN | 6.75 | Accept | Relevant — quantized/pruned SNN |
| **SpikeLLM** | **7.00** | **Accept (itemized)** | **Most relevant — scales SNN to LLMs (7B–70B)** |

**Round 2 — Narrowing (score 5.5–7.5):**
Confirmed Spatio-Temporal Approximation (7.00) and SpikeLLM (7.00) as the closest top-end anchors. SpikeBERT (6.33, Reject) also retrieved as a language-task SNN paper.

**Anchor item-weight comparison:**
- **SpikeLLM (7.0, Accept):** Strengths weighted 10.04–11.80; weaknesses: missing energy eval (weight=2.57, positive/mild), missing baselines (weight=-0.28, barely negative). This paper parallels the current one in addressing spiking LLMs but had stronger novelty claims ("first spiking LLM"), evaluation across 7B–70B, and a more complete comparison suite.
- **Spatio-Temporal Approximation (7.0, Accept):** Strengths weighted 8.82–10.90; most negative weakness weight=-1.08. First training-free Transformer→SNN conversion.
- **SpikeZIP (3.6, Reject):** Multiple strongly negative innovation weights (-3.01, -3.17, -4.55, -4.22). The current paper has much better novelty signals.

**This paper's item weights:** Strengths 8.80–9.34 (comparable to the 7.0 anchors). Weaknesses: -3.04 (no SNN baseline — more negative than any single weakness in the 7.0 anchors) and -0.07 (no energy evaluation — mild). All other weaknesses scored positive.

**Final placement:** The paper sits above SpikeZIP (3.6) and When SNN meets ANN (5.75) by a wide margin, but below SpikeLLM (7.0) which had broader model scaling, more comprehensive comparisons, and stronger novelty positioning. The missing SNN baseline comparison is the primary factor keeping the score below the 7.0 anchors. The paper's practical contribution, parameter-efficient calibration, and IS neuron design justify a score above 5.5. Final score: **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>