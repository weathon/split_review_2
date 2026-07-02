Now I have all the information I need. Let me produce the final review.

## Summary

This paper proposes a dual ANN-to-SNN conversion framework that starts from a statically quantized LLM (using PrefixQuant), replaces the quantization function with an Integer Spiking (IS) neuron with multi-hierarchical thresholds, and applies a lightweight layer-wise calibration that optimizes only thresholds and initial membrane potentials (~0.107K parameters per layer for a 7B model). The key advantage over conventional conversion is that it avoids training a conversion-friendly ANN, which is prohibitive for LLMs. Experiments on LLaMA-2-7B and LLaMA-3-8B at W6A6 precision show that calibration substantially improves the uncalibrated SNN, achieving accuracy within ~1–2% of the quantized baseline at T=2.

## Strengths

- **Well-motivated problem with practical significance.** The paper correctly identifies that conventional ANN-to-SNN conversion requires a specially trained conversion-friendly ANN, which is prohibitively expensive for LLMs. Starting from an already-quantized LLM is a sensible way to sidestep this cost. Figure 1 clearly contrasts the two pipelines.

- **Parameter-efficient calibration demonstrated with concrete numbers.** The layer-wise calibration optimizes only thresholds and initial membrane potentials, using 0.107K parameters per layer for the 7B model — orders of magnitude fewer than weight fine-tuning (202M parameters). Table 4 provides a clean head-to-head comparison showing that this tiny parameter set achieves higher accuracy (67.65 vs. 66.39) than a full-weight calibration baseline.

- **Clean error decomposition and visualization.** Section 3.3 decomposes conversion error into clipping, quantization, and unevenness errors following established conventions in the SNN literature. Figure 3 provides empirical evidence that unevenness error dominates, which directly motivates the calibration approach. Table 2 further validates this by showing the dramatic gap between uncalibrated ("Conversion") and calibrated ("Ours") results.

- **The calibration substantially improves uncalibrated SNN performance.** For LLaMA-3-8B at T=2, calibration lifts accuracy from 48.83 to 69.03 and reduces perplexity from 29.97 to 9.07 — a dramatic improvement that demonstrates the method's effectiveness.

## Weaknesses

### Fatal

None.

### Major

- **Missing energy/efficiency evaluation despite energy being a central motivation.** The paper frames SNNs as offering "brain-inspired efficiency and low power consumption" (abstract), claims the method "potentially reduces the energy consumption of LLMs" (Contribution 3), and explicitly argues that quantized LLMs still consume "significant energy" due to "the power demands of dense matrix multiplication, even with low-bit quantized versions" (Section 2.1). Yet the experiments contain zero energy measurements, no latency comparison, no synaptic operation counts, no FLOPs comparison, and no throughput measurement — not even a standard analytical estimate using established SNN energy models. Without this evidence, the paper's central motivation remains an unvalidated assertion. A method paper can be valuable without measuring energy, but the paper should not frame energy efficiency as a primary motivation without evaluating it.

- **No comparison against other SNN methods.** The paper compares only against quantization methods (PrefixQuant, DuQuant), not against other ANN-to-SNN conversion methods for LLMs. This is a critical omission because: (a) SpikeZIP (You et al., 2024) is cited as the source of the paper's spiking-compatible nonlinear operations but never appears as a baseline, and (b) without an SNN-to-SNN comparison, the reader cannot assess whether the dual conversion approach offers any advantage over existing conversion pipelines in terms of accuracy preservation. The Related Work section discusses SpikeGPT and SpikeBERT, but these also never appear in evaluation.

- **Performance degrades at T>1 without a demonstrated countervailing benefit.** At T=2, the method's average accuracy is competitive (e.g., LLaMA-3-8B: 69.03 vs. PrefixQuant's 70.24), but perplexity shows a larger gap (9.07 vs. 6.90 — a 31% increase). At T=4 and T=8, both accuracy and perplexity degrade substantially (e.g., LLaMA-3-8B perplexity rises to 11.67 at T=4 and 18.93 at T=8). The paper attributes this to "growing unevenness error" but does not explain why a practitioner would choose a higher-T SNN configuration. Since no energy benefit is quantified for larger T, there is no demonstrated trade-off that justifies the accuracy/perplexity loss.

- **DuQuant baseline results appear unreliable.** The DuQuant accuracy numbers are identical across LLaMA-2-7B and LLaMA-3-8B (67.88, 72.64, 40.53, 53.07, 77.15 for all tasks), with only perplexity differing (5.53 vs. 6.27). This is highly suspicious and suggests either a table compilation error or an evaluation setup issue. Additionally, DuQuant's ArcE score (53.07 vs. PrefixQuant's 74.41) is an anomalously large gap that is never discussed. The paper should clarify whether these numbers are correct and, if so, explain the discrepancy.

### Minor

- **"Comparable to quantization" claim overstates the perplexity results.** The paper repeatedly states performance is "comparable to state-of-the-art quantization techniques." While this is roughly true for average accuracy at T=1–2, the perplexity gaps are substantial — e.g., LLaMA-2-7B at T=2: 7.39 vs. PrefixQuant's 5.76 (28% relative increase), rising to 12.03 at T=8 (109% increase). Perplexity is a more sensitive quality metric than saturated accuracy benchmarks. The claim should be qualified to acknowledge this gap.

- **Theoretical analysis (Theorem 3) does not provide method-specific guarantees.** Theorem 3 is a standard Lipschitz-based error propagation bound showing that layer-wise errors accumulate according to products of Lipschitz constants. As Remark 2 acknowledges, this is "consistent with the classical Lipschitz continuity assumption." The bound does not depend on the IS neuron design, the calibration strategy, or any property of the proposed framework. Remark 3 — "Layer-wise calibration of these errors can effectively mitigate the overall conversion error" — is a tautology. The theory provides formal cover without analytical insight into why the proposed calibration is effective.

- **Remark 1 acknowledges a fundamental approximation gap.** The paper notes that the exact equivalence between the IS neuron and the quantization function (Theorem 2) "may not be perfectly achieved in practice" because the integer constraint \(LT = 2^n - 1\) rarely holds for \(T > 1\). This means the theoretical foundation is approximate precisely in the regime where the method is intended to operate as a multi-timestep SNN.

- **Calibration implementation details are deferred to the (stripped) appendix.** The paper states the calibration objective but does not specify in the main text the number of calibration samples, the dataset source, the optimization algorithm, or the convergence criteria. The appendix (referenced for the architecture description in Section 3.2.3) is unavailable in the submitted version.

### Trivial

None.

## Nice-to-Haves

- Comparison at lower bit widths (W4A4, W3A3) would test the method's generalizability across quantization levels.
- Testing on larger models (LLaMA-13B, 70B) would strengthen the scalability claim.
- Standard deviations or confidence intervals would be useful, though single-run evaluation on these benchmarks is standard practice.

## Removed Points

- **"At T=1, the SNN is not spiking."** Removed because the IS neuron at T=1 still produces discrete spike outputs (0, 1, ..., L). This is a spiking neuron with a single time step — a standard operating point in low-latency SNN literature. The reviewer conflated "no temporal dynamics" with "not spiking."

- **"The paper never explains why the spiking version is preferable."** The paper explicitly attributes T>1 degradation to growing unevenness error (Section 4.2: "We attribute this phenomenon to the growing unevenness error introduced by the larger time-step"). The reviewer's claim that this is unexplained is inaccurate.

- **"Weight calibration with meaningful fine-tuning would likely perform better."** This is speculation. The paper presents a direct comparison showing their 0.107K-parameter calibration outperforming a 202M-parameter weight calibration baseline under the same conditions. The reviewer offers no evidence that a different weight-tuning setup would reverse this result.

- **Criticisms about missing related work.** Removed per instructions — the reviewer does not have external sources to confirm existence of relevant work not cited by the authors.

- **Formatting/style nitpicks and reproducibility concerns about code release.** Removed per instructions (parser artifacts and standard practice concerns).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add an energy estimate — even a standard analytical model (e.g., counting synaptic operations vs. MACs using established SNN energy models) would validate the paper's central motivation. Without this, the paper reads as a representational exercise without demonstrated practical benefit.
2. Compare against at least one SNN baseline, ideally SpikeZIP (which the paper already builds on). This would ground the claim that the proposed conversion method is competitive as an SNN approach, not just as a reparameterization of quantization.
3. Clarify the DuQuant results — explain why the numbers are identical across model sizes and why the ArcE gap is so large versus PrefixQuant.
4. Qualify the "comparable to quantization" claim to explicitly acknowledge the perplexity gap.
5. Include calibration details (dataset, optimizer, convergence) in the main text.

## Score and Decision

This paper presents a genuinely novel approach to obtaining spiking LLMs without expensive conversion-specific training, and the parameter-efficient calibration is a concrete technical contribution. However, the evaluation has critical gaps: (a) the paper's central framing about energy efficiency is never evaluated, (b) no comparison against other SNN methods is provided, (c) the SNN's performance degrades at higher timesteps without a quantified benefit, and (d) the DuQuant baseline data appears unreliable. These omissions prevent the paper from convincingly demonstrating its claimed value proposition. The theoretical analysis is generic and does not provide method-specific guarantees. I cannot recommend acceptance without evidence for the paper's central claimed benefit.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>