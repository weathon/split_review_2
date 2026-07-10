Now I have all the information needed. Let me compile the final review.

## Summary

This paper proposes Quantized Zeroth-Order Optimization (QZO), which enables fine-tuning of quantized LLMs by perturbing the continuous quantization scales Δ (rather than the discrete quantized weights θ̄) for gradient estimation via SPSA. Combined with a Directional Derivative Clipping (DDC) method for training stability, QZO achieves ~3× memory reduction over MeZO and enables fine-tuning Llama-2-13B on a single 24GB GPU. The method is demonstrated across model families (OPT, Llama-2, Llama-3.1) and quantization schemes (GPTQ 4-bit, AQLM 2-bit).

## Strengths

- **Genuinely clever core idea (§3.2.1).** The key insight — perturbing the continuous quantization scale Δ rather than the discrete weights θ̄ — directly solves the fundamental problem that quantized weights cannot be perturbed continuously and continuous gradients cannot update discrete weights. This cleanly sidesteps the de-quantize/re-quantize loop that prior methods require.

- **Practical memory savings clearly documented (Table 1).** The 3× reduction over MeZO (14.8GB → 5.0GB for Llama-2-7B; 20.5GB → 6.3GB for Llama-3.1-8B) is a practically meaningful improvement. Fine-tuning Llama-2-13B on a single 24GB GPU (Table 3, 5.78GB) is a tangible achievement.

- **Orthogonality to quantization methods (§3.2.1, §4).** QZO is demonstrated with both GPTQ (4-bit scalar-based) and AQLM (2-bit codebook-based quantization), showing the idea is not tied to a specific quantization scheme. This significantly raises the impact potential.

- **Surprisingly strong results given the limited tunable parameters (Table 2).** QZO updates only ~50M parameters (the quantization scales) out of ~7B total, yet achieves performance within striking distance of MeZO (which tunes all 7B weights). This is a genuinely interesting finding about the expressiveness of scaling factors.

- **Computational efficiency documented (Table 2).** QZO uses orders of magnitude fewer FLOPs than MeZO (e.g., 2.26×10¹⁶ vs 1.13×10¹⁸ for Llama-2-7B) because it only perturbs the quantization scales rather than all weights.

## Weaknesses

### Fatal
None.

### Major

- **The variance reduction proof in §3.2.2 (Eq. 8) is mathematically invalid as written.** The derivation uses the formula Var[∇̂'] = E[||∇̂'||²] − E[||∇̂'||]² (square of the *expected norm*), but the correct variance formula for a random vector is E[||X||²] − ||E[X]||² (*squared norm of the expectation*). These are not the same quantity (by Jensen, E[||X||]² ≥ ||E[X]||²). The derivation then replaces E[||∇̂||]² with (∇L)², which would only be valid for ||E[∇̂]||², not E[||∇̂||]². These errors mean the chain of inequalities in Eq. 8 does not establish what the paper claims. Crucially, the paper's *correct* Eq. 7 (showing E[||∇̂'||²] ≤ E[||∇̂||²], i.e., reduction in the second moment) is sufficient to motivate DDC, and the empirical ablation (Figure 2) is convincing on its own. But the paper should not claim a proven variance reduction based on this derivation. This is fixable: replace the flawed variance argument with the second-moment argument, or correct the derivation.

### Minor

- **Missing empirical comparison to the most directly relevant prior methods (§2).** The Related Work section identifies Feng et al. (2024), Zhou et al. (2025), and Bar & Giryes (2025) as prior work combining ZO with quantization, and claims QZO is "inherently more efficient and flexible." Yet none of these methods appear in the experimental evaluation. While the design-based argument (no need to quantize perturbations or re-quantize weights) is reasonable, at least one empirical comparison would substantially strengthen the paper and ground this claim.

- **No variance/error bars for any experimental result (§4).** QZO is a stochastic optimization method, yet every result in Tables 1 and 3 is reported as a single point. The comparison between QZO and MeZO shows an inconsistent pattern across datasets (e.g., QZO wins on SST-2 for Llama-2-7B but loses on OPT-6.7B), and without error bars it is unclear whether these differences are meaningful. While single-run reporting follows the convention of the MeZO baseline paper, multi-seed results would greatly increase confidence, especially for a stochastic method.

### Trivial
None.

## Nice-to-Haves

- A comparison to QLoRA would be informative but is outside the paper's stated scope (ZO methods for quantized models, not parameter-efficient fine-tuning via backpropagation).
- The paper could clarify the relationship between DDC and standard gradient clipping (they are mathematically distinct operations) for reader convenience.

## Removed Points

*"Fine-tuning framing is overstated"* — REMOVED. The paper is transparent about its mechanism (abstract: "perturbs the continuous quantization scale"; §3.2.1: "perturb the scaling component Δ while keeping the discrete weights θ̄ fixed"). The title "Fine-Tuning Quantized Neural Networks" accurately describes the process; the specific mechanism is clearly explained.

*"DDC is just standard gradient clipping"* — REMOVED. DDC clips the scalar directional derivative d, scaling the gradient vector by clip(d,−C,C)/d. This is mathematically distinct from gradient norm clipping. Theorem 1 and the ablation adequately justify the approach.

*"Comparison to QLoRA"* — MOVED to Nice-to-Haves. QLoRA uses a different paradigm (low-rank adapters + backprop) and is outside the paper's comparison scope.

*Various section-by-section observations, formatting concerns, and speculation about missing appendix content* — REMOVED per filtering rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix Eq. 8.** Either correct the variance formula and derivation, or (more simply) replace the variance argument with the already-correct second-moment argument in Eq. 7, which suffices to explain DDC's stabilizing effect.
2. **Add one empirical comparison** against at least one of the cited prior ZO-for-quantized-models methods (Feng et al., Zhou et al., or Bar & Giryes) on a representative model/dataset pair.
3. **Report multi-seed results** (± std) for a representative subset of experiments to establish statistical reliability.

## Score and Decision

This paper presents a genuinely clever and practical contribution: perturbing quantization scales instead of discrete weights is a simple, elegant solution to a real problem, and the empirical results across models and quantization schemes are convincing. The weaknesses are real but addressable — the flawed variance derivation does not undermine the core contribution (the paper can fall back on the correct Eq. 7 and the strong ablation), and the missing comparison to prior methods is a gap but not a fatal omission given the strength of the MeZO comparisons.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>