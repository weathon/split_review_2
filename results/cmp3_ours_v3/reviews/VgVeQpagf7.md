Now I have a good calibration picture. Let me finalize the review.

**Round 1 Bracket:**

Based on the calibration anchors, I tentatively place this paper in the **5.5–6.5** range. It has stronger novelty than "Does Training with Synthetic Data Truly Protect Privacy?" (6.00, an empirical comparison paper) and is cleaner than "Advancing Differential Privacy through Synthetic Dataset Alignment" (2.50, which had unclear privacy accounting). It's comparable in contribution to "Differentially Private Synthetic Data via Foundation Model APIs 1: Images" (6.25) — a DP synthetic data generation method with strong experiments but some caveats.

Now producing the final review:

---

## Summary

This paper proposes SPS and SPS+, differentially private dataset distillation algorithms that generate private synthetic versions of sensitive data. The method extracts and privatizes intermediate activation statistics from a public pretrained model, then synthesizes images that match these statistics via KL-divergence minimization. On CIFAR-10/100, SPS+ (WRN34-10 Ensemble) achieves 96.2%/76.6% at ε=1, outperforming the DP-SGD baseline (94.8%/70.3%) — making it the first generation-based DP method to exceed DP-SGD on standard image classification benchmarks. The approach also demonstrates practical advantages in ensembling, federated learning, and continual learning without additional privacy cost.

## Strengths

- **First generation-based DP method to match/exceed DP-SGD on image classification (Tables 1, Figure 2).** This is the paper's headline result and it is genuine. SPS+ (WRN34-10 Ensemble) achieves 96.2%/76.6% on CIFAR-10/100 at ε=1 versus DP-SGD's 94.8%/70.3% — a 6.3 percentage point gap on CIFAR-100. Prior generation-based methods (Private Evolution at 89.13% on CIFAR-10 at ε=10) were far below DP-SGD, so crossing this threshold is a meaningful advance.

- **Practical advantages of the data-based approach are demonstrated concretely (Section 5.5–5.6).** The paper shows that the synthetic-data approach enables ensembling, federated learning, and continual learning without additional privacy cost — capabilities that require extra composition (or are infeasible) under DP-SGD. These are empirical demonstrations, not speculation.

- **Principled privatization strategy with tunable dimensionality (Section 3.2.2).** By privatizing aggregate activation statistics (~10⁵ dimensions) rather than per-iteration gradients (~10⁷ dimensions), the method directly improves the signal-to-noise ratio. The dimensionality can be controlled via D_G and D_C, offering a clean knob for privacy-utility trade-offs.

## Weaknesses

### Major

- **Theorem 4.1 contains a verifiable notational error.** The theorem states: *"The release of ṽ in eq. (4) for M models satisfies (α, ε)-RDP, where ε = Mα/(2δ²) for α > 1."* This is incorrect. The standard RDP for the Gaussian mechanism (noise σ = b₀‖v‖_max, sensitivity Δ = ‖v‖_max) gives ε(α) = α/(2b₀²) per query, so the composed guarantee should be ε = Mα/(2b₀²). The δ in the denominator is undefined here — the paper's δ is the (ε,δ)-DP parameter (set to 10⁻⁵), which does not appear in RDP expressions. The authors use the standard RDP accountant from Ahmed et al. (2025) for experimental privacy budgeting, so this error likely does not propagate to the reported ε values. Nevertheless, a formal theorem statement central to the paper's privacy guarantee is wrong as written and must be corrected.

### Minor

- **"Matches or exceeds DP-SGD in every setting" is overstated (Table 1).** At ε=8 on CIFAR-100, SPS+ (WRN28-10, single model) achieves 77.5% versus DP-SGD (WRN28-10) at 81.8%. Even SPS+ (WRN34-10 Ensemble) at 81.6% remains slightly below DP-SGD's 81.8%. The claim should be qualified: SPS+ excels at low ε and with ensembles, but at high ε on CIFAR-100 with matched architectures, it is below DP-SGD.

- **Headline numbers in the abstract compare ensemble results against single-model baselines without transparency.** The abstract reports SPS+ (WRN34-10 Ensemble) at 96.2%/76.6% against DP-SGD (WRN28-10, single model) at 94.8%/70.3%. While post-processing is a legitimate advantage, the abstract should explicitly note that the SPS+ results use ensembles and a larger architecture, so readers can interpret the comparison accurately.

- **Grouped pseudo-classes (GPC) mechanism lacks a rigorous explanation (Section 4.2).** The paper states GPC "only works due to dynamics of optimizing the loss function, specifically the Σ inversion in the KL-divergence, and the eigenvalue clipping of Σ" and "does not offer benefits for direct mean estimation." This is vague — the mechanism by which grouping classes reduces noise while still recovering individual-class information is not clearly explained. The paper should either provide a formal justification or explicitly characterize this as an empirical finding.

- **Computational cost of generation is not quantified in the main text.** The paper acknowledges cost is "relatively heavy" and defers to Appendix F.1, but gives no indication of GPU-hours or wall-clock time required to generate 50,000 synthetic images. This directly affects assessment of practical viability and should be summarized in the main paper.

### Trivial

- The clipping norm expression in Section 3.2.4 appears to be missing parentheses: "|v|_max = K_clip sqrt(LD_G^layer) + S|L_C|D_C^layer = K_clip sqrt(2LD_G^layer)" — the intended expression (given S = LD_G^layer/(|L_C|D_C^layer)) is presumably K_clip sqrt(LD_G^layer + S|L_C|D_C^layer).

## Nice-to-Haves

- Report SPS+ downstream accuracy with a standard optimizer (e.g., AdamW without GSAM) to isolate the contribution of the optimizer from the privatization method.
- Quantify the variance introduced by the random projections (M_l^G, M_l^C) and Gaussian noise in the synthetic data generation process itself, beyond the n=5 downstream fine-tuning runs.
- Discuss which hyperparameters (D_G, D_C, λ_C, K_clip, P) are most critical and how they were selected.

## Removed Points

These points from the input review are flagged to be removed. Treat them with caution:

- *"Section 3.2.4 — the derivation is not shown... the authors should verify privacy cost after rescaling"* — This speculation about the noise-redistribution derivation is not independently verifiable as an error; the paper states the procedure keeps the same privacy cost b₀ and the math is consistent after correcting the parentheses placement.
- *"Section 5.2 — CAMELYON17 comparison is non-ideal"* — The paper correctly reports the actual ε values for all methods; the ε mismatch is inherent to comparing methods with different privacy accounting. This is a standard comparison practice, not a weakness.
- *"Missing Parts — variance of synthetic data generation"* — This is a nice-to-have, not a weakness. Error bars on downstream accuracy (n=5) are already reported.
- *"Variance of synthetic data generation itself"* — Speculative concern, not a verified flaw.

## Novel Insights

None beyond the paper's own contributions. The harsh review generally corroborates the paper's claimed strengths and identifies presentation/verification issues that the authors can address during revision.

## Suggestions

1. **Fix Theorem 4.1.** Replace the erroneous δ² with b₀² and verify the corrected formula against the standard RDP accountant that is already used in experiments.
2. **Qualify the central claim.** Acknowledge the CIFAR-100 ε=8 regime explicitly in the abstract and Section 5.1.
3. **Add compute cost to main text.** Include a brief quantification of GPU-hours for synthetic data generation in the Limitations section (Section 6).
4. **Improve GPC explanation.** Provide a more rigorous explanation or clearly state that the technique is empirically motivated.
5. **Ensure abstract transparency.** Note that headline results use ensembles and a larger architecture when comparing against single-model DP-SGD baselines.

---

## Calibration Anchors

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| Exploring Data Distillation for Tabular Data | 3.33 | R1 (bracket) | Lower quality, writing issues, not as strong empirical results |
| Advancing DP through Synthetic Dataset Alignment | 2.50 | R1 (bracket) | Had unverifiable privacy accounting — more severe issue than this paper's theorem error |
| Privacy as a Free Lunch | 4.75 | R1 (bracket) | Mixed reviews, had contribution but presentation issues |
| Does Training with Synthetic Data Truly Protect Privacy? | 6.00 | R1+R2 (narrow) | Less novelty but solid, similar overall quality tier |
| DP Synthetic Data via Foundation Model APIs | 6.25 | R2 (narrow) | Similar paper type (DP synthetic data generation), strong results with minor caveats |
| RAPID: Retrieval Augmented Training of DP Diffusion Models | 6.00 | R2 (narrow) | Similar quality tier, accepted with some review concerns |
| Privacy-Preserving ICL with DP Few-Shot Generation | 8.00 | R1 (bracket) | Stronger paper — cleaner presentation, no formal errors, thorough evaluation |

**Round 1 bracket:** 5.5–6.5 based on comparison to anchors.
**Round 2 narrowing:** Compared to "DP Synthetic Data via Foundation Model APIs" (6.25) and "Does Training with Synthetic Data Truly Protect Privacy?" (6.00), this paper has stronger novelty (first to exceed DP-SGD) but carries a notable formal error in Theorem 4.1. These roughly balance out, placing it at 6.0.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>