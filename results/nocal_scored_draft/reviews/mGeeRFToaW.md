Now I have all the evidence needed. Let me write the final consolidated review.

## Summary

This paper proposes QZO (Quantized Zeroth-order Optimization), a method for fine-tuning quantized LLMs that combines memory-efficient zeroth-order optimization with post-training model quantization. The key technical insight is to perturb the continuous quantization scale (rather than the discrete quantized weights) for gradient estimation, along with a directional derivative clipping (DDC) mechanism to stabilize training. QZO achieves ~3× memory reduction over MeZO and ~18× over AdamW fine-tuning while attaining comparable accuracy to MeZO on most benchmarks.

## Strengths

- **The core insight — perturbing continuous quantization scales rather than discrete quantized weights for ZO gradient estimation (Section 3.2.1) — is genuinely clever and well-motivated.** It cleanly resolves the precision mismatch problem without requiring dequantization/requantization at each step.

- **Memory savings are substantial and clearly documented (Figure 1, Table 1).** QZO with 4-bit weights achieves 4.8–6.3 GB peak memory on 7B-class models vs. 14.8–20.5 GB for MeZO and 26–31.9 GB for SGD fine-tuning — a ~3× reduction over MeZO and ~18× over AdamW fine-tuning.

- **QZO is orthogonal to existing PTQ frameworks;** it works with both scalar-based (GPTQ, 4-bit) and codebook-based (AQLM, 2-bit) quantization without modifying the quantization scheme itself.

- **The DDC ablation (Figures 2–3) is clean and convincing.** Figure 2 shows training collapses to NaN within ~20 steps without DDC but remains stable with DDC. Figure 3 shows the method is robust to the clipping threshold C for C ≥ 75.

## Weaknesses

### Fatal
None.

### Major

- **The theoretical analysis of DDC (Section 3.2.2) is not sound as stated.** Theorem 1 claims the clipped gradient estimate `d'·z` is an unbiased estimate of ∇L, but clipping is a non-linear operation; generally `E[clip(d,-C,C)·z] ≠ E[d·z]`, especially when `|d| > C` with non-negligible probability. This is the standard bias of gradient clipping. Furthermore, the variance derivation in Eq. 8 uses `(E[||∇̂L||])²` (squared expected norm) instead of `||E[∇̂L]||²` (norm squared of the expectation) in the variance decomposition, and replaces the former with `(∇L)²` without justification. The empirical evidence for DDC (Figures 2–3) is solid and stands independently, but the theoretical framing needs correction — the paper should either prove unbiasedness under appropriate conditions (large enough C where clipping is rare), acknowledge the bias and analyze MSE instead, or reframe as a heuristic explanation.

### Minor

- **Missing comparison to QLoRA** (Dettmers et al., 2023, cited in references), the most widely known method for fine-tuning quantized LLMs. QLoRA is never compared against experimentally. A practitioner deciding between approaches would need to see how QZO compares in both memory and accuracy.

- **Missing empirical comparison to prior ZO+quantization methods** (Feng et al., 2024; Zhou et al., 2025; Bar & Giryes, 2025), which are discussed in Related Work but not benchmarked. The claim that QZO is "inherently more efficient and flexible" remains speculative without direct comparison.

- **No error bars, confidence intervals, or standard deviations** are reported for any result (Tables 1, 3). ZO methods have inherent gradient variance, and many comparisons show small gaps (e.g., Llama-3-8B SST-2: 93.0 vs 92.5). Without variance estimates, it is impossible to assess whether these differences are systematic or within noise.

- **The large performance gap on CB (CommitmentBank) for Llama-3-8B** (QZO 69.6 vs MeZO 91.1 — a 21.5-point gap) is not discussed. This is the largest discrepancy in Table 1 and deserves comment.

- **The comparison to MeZO confounds two effects simultaneously**: ZO on scales only vs. ZO on all parameters. QZO fine-tunes ~5×10⁷ parameters (~0.75% of total) while MeZO fine-tunes all 6.7×10⁹ parameters. The paper is transparent about this (Table 2), but a controlled experiment separating the quantization effect from the parameter-count effect (e.g., MeZO restricted to scale parameters only) would strengthen the conclusions.

- **No wall-clock training time** is reported alongside FLOPs (Table 2). Actual runtime would be useful for practitioners.

### Trivial
None.

## Nice-to-Haves
- A controlled experiment where MeZO fine-tunes only the same scale parameters as QZO would cleanly separate the effect of quantization from the effect of fewer trainable parameters.
- Reporting results with error bars (at least 3 runs with standard deviation) would increase confidence.

## Removed Points
None.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Fix the DDC theoretical analysis: either prove unbiasedness under appropriate regularity conditions (large C where clipping events are rare), or acknowledge the bias and reframe the analysis using MSE (bias² + variance).
2. Add at least one controlled experiment: compare to QLoRA on at least one model/dataset configuration, and consider a version of MeZO restricted to fine-tuning only the scale parameters.
3. Compare against at least one prior ZO+quantization method to substantiate the claimed superiority.
4. Report results with error bars from multiple runs.
5. Discuss the CB outlier and any other notable failure cases.
6. Report wall-clock training time.

## Score and Decision

The paper presents a genuinely clever core idea (perturbing quantization scales rather than discrete weights) with clearly demonstrated memory savings and convincing empirical evidence that the method works. The DDC ablation is clean and the empirical results are promising across multiple model families and quantization schemes.

However, the theoretical analysis of DDC contains errors (an unjustified unbiasedness claim and a flawed variance derivation) that need correction. The evaluation is also weakened by the absence of several natural baselines (QLoRA, prior ZO+quant methods) and the lack of statistical significance reporting. These issues are addressable but limit the paper's contributions as presented.

**Score: 6.0** — borderline accept. The paper's core empirical contribution is real, but the theoretical claims need fixing and the evaluation needs strengthening.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>