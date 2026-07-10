Here is my final consolidated review:

---

## Summary

This paper proposes QZO (Quantized Zeroth-order Optimization), a method for fine-tuning already-quantized LLMs using zeroth-order optimization. The core technical contribution is Q-SPSA (Section 3.2.1), which perturbs the continuous quantization scale Δ while keeping discrete quantized weights θ̄ fixed—circumventing the problem that quantized weights cannot be smoothly perturbed for ZO gradient estimation. QZO eliminates gradients and optimizer states (via ZO) while compressing weights (via PTQ), achieving 4.8–6.3 GB memory for 7B-class models. The method is orthogonal to both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) quantization. A directional derivative clipping (DDC) mechanism is introduced to stabilize training.

## Strengths

- **Genuinely novel core idea (Section 3.2.1).** Perturbing the continuous quantization scale Δ while keeping discrete weights θ̄ fixed is a clean, non-obvious solution to the incompatibility between ZO perturbation and quantized weights. This is not an incremental modification of MeZO—it addresses a distinct constraint that prior ZO methods do not handle.

- **Orthogonality to existing PTQ methods (Section 3.2.1, Table 1, Table 3).** QZO works with both scalar-based quantization (GPTQ, 4-bit) and codebook-based quantization (AQLM, 2-bit) without modification to the quantization procedure itself. This is a meaningful practical advantage.

- **Clear memory profiling (Figure 1, Table 1).** QZO achieves 4.8–6.3 GB for 7B-class models vs. 14.8–20.5 GB for MeZO and 26–32 GB for SGD fine-tuning. The 3× reduction over MeZO is cleanly attributable to weight quantization (16-bit → 4-bit). Fine-tuning Llama-2-13B in 5.78 GB on a single RTX 4090 (Table 3) is practically significant.

- **Parameter and FLOP efficiency (Table 2).** QZO fine-tunes only ~50M parameters (the quantization scales) rather than ~6.7B weights. FLOPs are dramatically lower than MeZO (which requires two full forward passes per step on all parameters) and sometimes lower than first-order fine-tuning.

- **Empirically convincing DDC ablation (Figure 2, Section 4.3).** Without DDC, training collapses to NaN by step 22; with DDC, it stabilizes. The sensitivity study on C (Figure 3) shows a stable operating range (C ≥ 75). This evidence stands independently of the theoretical analysis.

## Weaknesses

### Fatal
None.

### Major

- **DDC variance-reduction proof is mathematically flawed (Section 3.2.2, Eq. 8).** The derivation uses a non-standard variance definition (Var[∇̂] = E[‖∇̂‖²] − E[‖∇̂‖]² instead of the standard E[‖∇̂−E[∇̂]‖²]) and then makes an unjustified substitution in the last line of Eq. 8, replacing E[‖∇̂‖]² with ‖E[∇̂]‖² = (∇_Δ L)². By Jensen's inequality, E[‖X‖] ≥ ‖E[X]‖, so this substitution is invalid and the claimed inequality does not follow from the derivation. Additionally, Theorem 1's unbiasedness claim for the clipped estimate is questionable—clipping the directional derivative d introduces bias unless the distribution of d is symmetric and its support lies within [−C, C], which is not generally guaranteed. However, the *empirical* demonstration (Figure 2) is strong and stands independently. The paper would be better served by correcting or retracting the flawed proof and presenting DDC as an empirically motivated technique.

- **No experimental comparison against QLoRA (Dettmers et al., 2023).** QLoRA is the most widely used method for fine-tuning 4-bit quantized LLMs. It is cited in the references (line 311) but never appears in the experiments. QLoRA fine-tunes 4-bit base models with low-rank adapters, achieving memory in a similar range (~4–6 GB by rough estimate). Without this comparison, readers cannot assess whether QZO offers practical advantages over the established approach for the same use case. The paper should include QLoRA as a baseline (at minimum for memory usage and one or two tasks) or provide a clear argument for why it is not comparable.

- **No experimental comparison against prior ZO+quantization methods cited in Section 2 (Feng et al., 2024; Zhou et al., 2025; Bar & Giryes, 2025).** The paper claims QZO is "inherently more efficient and flexible" than these approaches but provides no empirical evidence. Since these works target the exact same problem setting (combining ZO with quantization), their absence from the experiments is a significant omission.

### Minor

- **No statistical uncertainty reported.** ZO methods are inherently noisy (Eq. 5 is a single-sample Monte Carlo approximation), yet no standard deviations, confidence intervals, or multiple-seed runs are reported for any result in Tables 1-3. This is especially problematic for interpreting outliers like the Llama-3.1-8B CB result, where QZO (69.6) trails MeZO (91.1) by 21.5 points—a gap that goes undiscussed in the paper.

- **2-bit experiments are thin (Table 3).** Only one model (Llama-2-13B), one quantization method (AQLM), and only QZO vs. Zero-Shot-Q are compared. Improvements on RTE (53.1→54.5) and BoolQ (69.2→70.2) are small enough that without error bars, it is unclear whether QZO is doing meaningful fine-tuning on those datasets.

- **FLOPs numbers show unexplained variation (Table 2).** QZO on OPT-6.7B uses 8.19×10¹³ FLOPs while QZO on Llama-2-7B uses 2.26×10¹⁶ FLOPs (~276× more) despite similar numbers of trainable parameters (~50M). The paper provides no explanation for this discrepancy.

- **No ablation on learning rate or perturbation scale ε.** Both are critical hyperparameters for ZO optimization. Only the clipping threshold C is ablated (Figure 3).

### Trivial
None.

## Nice-to-Haves

- An ablation on the learning rate and perturbation scale ε would strengthen the empirical characterization.
- An explanation of the large FLOPs variation across model architectures in Table 2 would improve clarity.
- Discussion of the outlier results (e.g., Llama-3.1-8B CB: QZO 69.6 vs. MeZO 91.1) would improve the paper's presentation.

## Removed Points

These points were identified in the input review but excluded from the main evaluation for the following reasons:

1. **Framing inconsistency (18× vs 3× claim):** The critic argued the 18× claim is misleading. However, the paper transparently presents *both* the 18× reduction over AdamW (with FSDP) and the ~3× reduction over MeZO in the same figure/table. Both comparisons are valid—the 18× figure is a legitimate comparison showing the maximum possible reduction. **Removed** because the claimed inconsistency does not hold on closer inspection.

2. **Missing related works:** Not included per policy (cannot confirm existence of works not cited by the paper).

3. **Formatting and style nitpicks:** Not included per policy.

## Novel Insights

None beyond the paper's own contributions. The reviews raised the missing-baseline concern (QLoRA, prior ZO+quantization methods) and identified a genuine mathematical flaw in the DDC variance proof, but neither constitutes a novel insight about the method.

## Suggestions

1. **Add QLoRA as a baseline.** This is the single highest-leverage improvement. Even one table showing memory usage and accuracy for QZO vs. QLoRA on SST-2 and one other task would substantially strengthen the evaluation.
2. **Include at least one prior ZO+quantization comparison** (e.g., Bar & Giryes 2025's ZOQO) to substantiate the claim that QZO is more efficient and flexible.
3. **Fix or retract the variance proof (Eq. 8).** The empirical DDC ablation is sufficient motivation on its own. The flawed theoretical derivation should be corrected or removed. If a theoretical claim is desired, provide a clean proof using the standard variance definition.
4. **Report results with multiple seeds (≥3) and include standard deviations.** For a noisy ZO method, this is essential to assess whether differences between methods are statistically meaningful.
5. **Discuss the outlier results** (e.g., Llama-3.1-8B CB where QZO trails MeZO by 21.5 points).
6. **Add ablation on learning rate and perturbation scale ε.**
7. **Explain the large FLOPs variation** across models in Table 2.

## Score and Decision

**Calibration Anchor Summary:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| SensZOQ (ZO+quantization, Accept) | 5.80 | R1 | Yes | Closest anchor; similar gaps but QZO has more novel core idea |
| LOZO (ZO with low-rank, Accept) | 7.00 | R1 | Yes | Stronger theory but less novel core idea vs. QZO |
| SubZero (ZO subspace, Reject) | 4.25 | R1 | Yes | Less novel, QZO is clearly above |
| LeZO (ZO layer-sparse, Reject) | 4.00 | R1 | Yes | Less novel, QZO is clearly above |
| 3-Stage Quantized FT (Reject) | 5.40 | R1 | Yes | Mixed reviews; QZO has cleaner contribution |
| LQ-LoRA (quantized FT, Accept) | 6.75 | R2 | No | Different approach (decomposition-based); not directly comparable |

**Round 1 bracket:** 5.0–7.0 (based on comparison with SensZOQ at 5.80 and LOZO at 7.00).

**Round 2 narrowing:** QZO's weighted strengths are all 9.22–9.97 (very high), vs. SensZOQ's strongest strength at 10.26 and its most negative weakness at −6.01 (novelty). QZO's most negative weaknesses are −0.68 (missing prior ZO+quant comparison) and −0.02 (DDC proof flaw)—much milder than SensZOQ's novelty concern. QZO's core idea is more novel than SensZOQ's, which was its main weakness. However, QZO's missing baselines (QLoRA, prior ZO+quant) and the flawed theoretical proof prevent it from reaching the LOZO tier (7.0). Placing it above SensZOQ (5.80) but below LOZO (7.00) yields a score of 6.0.

**Decision rationale:** The paper has a genuinely novel core contribution (Q-SPSA) supported by clean memory profiling and a convincing ablation. However, the evaluation is incomplete—the absence of QLoRA (the dominant method for the same use case) and other ZO+quantization baselines, combined with a mathematically flawed variance proof and a lack of statistical uncertainty reporting, prevents full acceptance at a top venue. The paper is solidly in borderline-accept territory, contingent on addressing these gaps.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>