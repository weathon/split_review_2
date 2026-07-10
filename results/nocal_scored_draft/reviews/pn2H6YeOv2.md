Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper tackles replay-free continual learning for vision-language models by reframing forgetting as alignment-geometry drift. It proposes Pi-CCA, which summarizes the cross-modal alignment structure of CLIP-like dual encoders via a compact CCA certificate (top-k canonical correlations + sketched subspaces) and constrains adaptation to preserve this certificate using only mini-batch statistics. The method achieves state-of-the-art performance among replay-free methods on four benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL) and includes a thorough ablation study confirming the contribution of each loss component.

## Strengths

- **Well-motivated problem reframing (Section 1, lines 20-23).** The paper correctly identifies that prior VL-CL methods regularize proxy signals (similarities, logits, weights) rather than the alignment geometry itself, providing a clear conceptual motivation for the CCA-based approach.

- **Principled use of CCA with sketch-based compression (Section 3.2).** Using the whitened cross-covariance SVD to define alignment invariants is a natural choice for dual-encoder models like CLIP, and the random orthonormal sketches with h ≪ d achieve constant memory independent of embedding dimension — a genuine practical virtue.

- **Consistent empirical results across four benchmarks (Tables 1 and 2).** Pi-CCA achieves the best results among replay-free methods on MTIL, X-TAIL, VLCL, and ConStruct-VL with consistent (if modest) margins. It even edges out GIFT (a synthetic-replay method) on VLCL and ConStruct-VL without storing or generating data.

- **Thorough component ablation study (Table 3).** Each term (spectral, subspace, prompt-invariance, covariance EMA, certificate EMA) is systematically ablated with meaningful performance drops (up to 2.8 p.p. on MTIL Last, up to 2.7 p.p. on VLCL I2T R@1), confirming that all designed components contribute.

- **Task-order robustness evaluation (Figure 5).** Testing on 20 independently shuffled task sequences with narrow IQRs provides strong evidence of low order sensitivity — a robustness check that should be standard but often is not.

## Weaknesses

### Fatal
None.

### Major

- **Figure 3 reports correlation statistics that are not credible for real empirical data.** The paper claims to sweep "realistic perturbations" across at least 7 dimensions (certificate size, EMAs, invariance strength, whitening, pairing, LoRA capacity/LR, sketch type) yet reports Pearson r = 1.00 and Spearman ρ = 1.00 for three of four panels (0.99/1.00 for the fourth). Spearman ρ = 1.00 means ranks are perfectly preserved and Pearson r = 1.00 means every point lies exactly on the regression line — these values are not plausible for real experimental data with multiple varied conditions. The caption also mentions "realistic scatter" while reporting perfect correlation, which is contradictory. This undermines the paper's "geometry → performance" causal claim (Section 4.3, line 232), presented as a key piece of mechanistic validation. The authors should replace Figure 3 with an honest scatter plot from actual multi-condition runs with correctly computed correlation statistics.

### Minor

- **Initial certificate source is underspecified (Section 3.2, line 89).** The paper states the reference CCA quantities come from "a diverse anchor prompt set" without specifying what data is used to compute them — whether this is a held-out subset of CLIP's pre-training data, the first task's data, or something else. Since the entire method constrains drift relative to this initial reference, this ambiguity affects reproducibility and makes it unclear whether the method is genuinely replay-free.

- **Table 1 (MTIL/X-TAIL) lacks error bars or variance estimates.** Margins over the second-best baseline are small (e.g., +0.7 p.p. on X-TAIL Avg, +1.6 p.p. on MTIL Avg). Since Table 2 reports ± ranges of 1.0–1.6 p.p. for similar methods, it is unclear whether the improvements in Table 1 are within run-to-run noise. Standard deviations or confidence intervals should be reported for all main results.

- **Default value of ξ in Equation (8) is not stated.** The spectral loss combines sorted-pairing MSE with a Ky-Fan-k sum alignment term weighted by ξ ∈ [0,1], but no default value is given. The ablation tests only λ₁=0 (removing the entire term) without examining sensitivity to ξ within the spectral term.

- **Computational overhead of the prompt-invariance loss is not quantified.** L_pi requires M=4 forward passes through the text encoder per sample (plus per-perturbation SVD), yet the paper never reports the per-step wall-clock time overhead relative to baseline methods. This makes it difficult to assess the practical cost of the prompt-robustness mechanism.

### Trivial
None.

## Nice-to-Haves

- A controlled comparison isolating the "geometry-first vs. proxy-only" principle: hold backbone and LoRA constant, compare Pi-CCA against a version that replaces the CCA losses with a distillation/logit-matching proxy from prior work, and a version without sketch compression (full CCA).
- Report wall-clock time and peak memory for at least 2–3 baseline methods alongside Pi-CCA's in the Pareto analysis (Figure 2), so readers can assess the real-world efficiency tradeoff.

## Removed Points

- **"Modest margins over GIFT" and "EMA drift means the certificate is a moving target."** The former is not a weakness — beating a synthetic-replay method without generators is a strength, even narrowly. The latter is a deliberate design choice ("controlled plasticity," line 133), not a flaw; the α=0 ablation is tested, and the remaining concern (α sensitivity not fully explored) is already captured in the minor weaknesses above.
- **"Pareto analysis should include cross-method comparison."** This is a legitimate suggestion but more of a nice-to-have than a weakness; it has been moved to Nice-to-Haves.
- **Speculative claims about fabricated data.** The critic speculates that Figure 3 data may be fabricated. This cannot be verified from the paper text alone and there are other possible explanations (e.g., very few data points). The weakness is kept in a verifiable form (the correlation values are not credible) without the unverifiable fabrication accusation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Replace Figure 3** with real scatter plots from multi-condition runs with honestly computed correlation statistics. If the relationship is strong but not perfect (e.g., r ≈ 0.85–0.95 with genuine scatter), that is still a valuable and publishable result.
2. **Specify the initial certificate source** in Section 3.2 with one sentence (e.g., "computed from the first task's training set" or "from a held-out subset of the pre-training data").
3. **Add standard deviations or confidence intervals to Table 1** (or at minimum state the number of seeds and whether differences are statistically significant).
4. **Report the default value of ξ** used in all experiments.
5. **Quantify the computational overhead** of L_pi: report per-step wall-clock time for Pi-CCA vs. 2–3 baseline methods with comparable settings.

## Score and Decision

The paper presents a conceptually clean, principled method with consistent benchmark results and thorough ablations — these are genuine strengths. However, Figure 3 reports correlation statistics (Pearson r = 1.00, Spearman ρ = 1.00 across multiple perturbation conditions) that are not credible for real empirical data, which undermines the paper's supporting mechanistic analysis. This issue is significant but does not invalidate the core method or benchmark contributions. The paper would benefit from a corrected analysis and several minor clarifications.

**Score: 5.0**  
**Decision: Reject** (borderline; the correlation evidence needs correction, but the method and main results are otherwise solid and would warrant re-review after fixing Figure 3 and clarifying the certificate source.)

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>