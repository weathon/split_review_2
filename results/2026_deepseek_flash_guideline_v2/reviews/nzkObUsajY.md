The calibration database is not accessible. I will proceed with calibration based on my general knowledge of reviewer standards. Let me finalize my review.

## Final Consolidated Review

## Summary

This paper proposes a "dual" ANN-to-SNN conversion framework for LLMs that eliminates the need to train a conversion-friendly ANN. Instead of the conventional pipeline (train ANN → convert to SNN), it starts from a statically quantized LLM (PrefixQuant), replaces quantization functions with Integer Spiking (IS) neurons equipped with multi-hierarchical thresholds, and applies a lightweight layer-wise calibration (freezing weights, optimizing only thresholds θ^k and initial membrane potentials v^k(0)). Experiments on LLaMA-2-7B and LLaMA-3-8B show the calibrated SNN matches the quantized ANN at T=1 and comes within ~1–1.5% average accuracy at T=2 using only ~0.1K learnable parameters per layer.

## Strengths

1. **Eliminates costly conversion-specific ANN training.** The paper validates its central claim through Table 2: on LLaMA-2-7B at T=1, the method achieves 68.79% Avg. Acc., matching PrefixQuant's 68.70% — without any task-specific ANN training for conversion. This is a clean, well-supported result that distinguishes the approach from conventional two-stage conversion methods.

2. **Extreme parameter efficiency in calibration.** Table 4 shows the layer-wise calibration uses 0.107K learnable parameters per layer on LLaMA-2-7B — a ~1.9 million× reduction compared to full weight fine-tuning (202.375M) — yet achieves higher average accuracy (67.65% vs. 66.39%). This directly validates the claim of "minimal computational and memory overhead."

3. **Formal theoretical connection between IS neurons and quantization.** Theorem 2 provides a principled link: under appropriate conditions (LT = 2^n − 1, with v^k(0) = θ^k/2, α^k(t) = 2^{n−1}/T), the IS neuron's summed output Σ_t s^k(t)θ^k exactly mimics a symmetric quantization function X_q^k. This gives the conversion a clean theoretical foundation.

4. **Comprehensive error decomposition.** The paper identifies and defines three distinct error sources (clipping, quantization, unevenness) in the dual conversion setting, and provides empirical evidence that unevenness error dominates — directly motivating the calibration design.

## Weaknesses

### Fatal
None.

### Major

1. **Performance degrades with more timesteps, limiting the practical value of SNN temporal dynamics.** As T increases from 1 to 8, Avg. Acc. declines monotonically (68.79 → 67.65 → 67.04 → 66.03 for LLaMA-2-7B; a similar pattern for LLaMA-3-8B). The paper acknowledges this and attributes it to "growing unevenness error." The implication is that the best-performing configuration (T=1) is not meaningfully a spiking network — Theorem 2 shows the IS neuron at T=1 with appropriate settings is essentially the quantization function itself. At T>1, where temporal dynamics exist, performance is consistently worse. This tension between the "spiking LLM" framing and the observed behavior is not adequately discussed or mitigated.

2. **No comparison against existing spiking LLM methods.** The paper cites SpikeZIP (You et al., 2024) and SpikeGPT (Zhu et al., 2023) in related work but compares only against quantization methods (PrefixQuant, DuQuant). While comparison to quantization baselines is meaningful (the method builds on quantized LLMs), the absence of any SNN baseline makes it impossible to assess whether this method advances the state of the art within its own subfield.

### Minor

1. **Energy efficiency is a prominent motivation but entirely unmeasured.** The abstract and introduction position SNNs as offering "brain-inspired efficiency and low power consumption, making them ideal for edge deployment," and contribution 3 notes the method "potentially reduces the energy consumption of LLMs." No energy estimates, FLOP comparisons, or synaptic operation counts are provided. While this gap is common in methods papers and the energy benefit follows from the SNN paradigm, the paper's framing makes energy efficiency sufficiently central that some estimate (even theoretical) would strengthen the paper considerably.

2. **The "comparable performance" claim in Table 4 vs. weight calibration is imprecise.** On LLaMA-2-7B, the PPL gap is 7.39 vs 6.37 (a meaningful difference), though Avg. Acc. favors the proposed method (67.65 vs 66.39). The accuracy/perplexity trade-off is not discussed.

3. **Figure 3 caption describes a y-axis ranging from −8 to 2 for what is labeled "MSE loss," but MSE cannot be negative.** This is confusing and undermines the interpretability of the figure. Clarification is needed.

4. **Imprecise enumeration of benchmarks.** The text states "five zero-shot reasoning tasks, including PIQA..., ARC..., HellaSwag..., and WinoGrande" — only four items are named. (ARC has two variants, explaining the count, but the listing is sloppy.)

### Trivial
None.

## Nice-to-Haves

- An analysis of calibration data requirements (number of samples, sensitivity to distribution).
- Testing on larger models (13B, 70B) would strengthen the scalability narrative.
- Clarification of whether α^k(t) is learned during calibration or fixed a priori (the paper says it is "set by users" but does not specify how it is set in practice beyond the theoretical condition in Theorem 2).

## Removed Points

These points were removed from the inputs; treat them with caution:

1. **"Energy efficiency is the paper's raison d'être" (Harsh Critic, Critical Issue 1)** — Downgraded from Fatal to Minor (Weakness #1). The paper's primary contribution is the conversion methodology; the energy benefit is a well-established property of SNNs in the broader literature, not a claim unique to this paper. The paper says "potentially reduces energy consumption," which appropriately hedges. However, because the framing heavily emphasizes edge deployment, some estimate would be valuable.

2. **"Theorem 3's Lipschitz constants are never computed"** — Removed. This is a standard feature of Lipschitz-based analyses in neural network papers; the bound is intentionally qualitative. This is not a specific flaw of this paper.

3. **"The 'training-free' claim is misleading because of the calibration step"** — Removed. The paper explicitly scopes this: Section 3.2 describes the quantization and conversion as "training-free," while Section 3.4 describes calibration as a separate learning step. The distinction is clear.

4. **"α^k(t) role is not explained"** — Removed. Theorem 2 shows α^k(t) = 2^{n−1}/T for exact equivalence, and Remark 1 specifies α^k(t) = 2^{n−j−1} for practical implementation. This is explained.

5. **"Table 3 trend shows significant variation"** — Removed. The range from 67.65 to 65.46 (~2 pp across 5 tasks) is modest and the paper's characterization as "not vary[ing] significantly" is reasonable.

6. **"No analysis of calibration data requirements"** — Moved to Nice-to-Haves. This would strengthen the paper but is not a core flaw.

## Novel Insights

None beyond the paper's own contributions. The key insight — using a quantized LLM as the intermediate representation for ANN-to-SNN conversion and connecting quantization functions to multi-threshold spiking neurons — is genuinely novel and is the paper's main contribution. No additional novel observations emerge from the reviews.

## Suggestions

1. **Address the timestep degradation directly.** Either (a) investigate whether the degradation is fundamental or can be mitigated with better calibration, or (b) explicitly scope the method as a low-timestep (T ≤ 2) conversion approach and discuss the implications for SNN temporal dynamics.
2. **Include at least one spiking LLM baseline** (SpikeZIP or SpikeGPT) in the comparison to establish standing within the SNN subfield.
3. **Provide energy estimates** (theoretical synaptic operations, FLOP comparison) to substantiate the edge-deployment motivation.
4. **Clarify the Figure 3 axis labeling** (MSE cannot be negative) and fix the benchmark enumeration.
5. **Discuss the accuracy/perplexity trade-off** between the proposed calibration and weight-based calibration in Table 4.

## Score and Decision

Based on my assessment, the paper presents a genuinely novel idea with clean theoretical backing and strong empirical validation of its parameter efficiency. However, the timestep degradation issue and the absence of spiking baselines are significant limitations that prevent it from being a strong accept. The paper would benefit from a major revision addressing these concerns.

**MY FINAL SCORE:** <score>5.5</score>
**MY FINAL DECISION:** <decision>Reject</decision>