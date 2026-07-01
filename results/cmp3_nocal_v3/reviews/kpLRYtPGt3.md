## Summary

This paper introduces Neon, a post-hoc method that improves generative image models by fine-tuning them briefly on their own synthetic data, then extrapolating *away* from the degraded checkpoint (θ_Neon = θ_r − w(θ_s − θ_r)). The core insight — that self-training degradation is not random noise but a structured signal anti-aligned with the true data gradient — is theoretically grounded via connections between mode-seeking samplers and gradient anti-alignment. Empirically, Neon is evaluated across four model families (diffusion, flow matching, autoregressive, few-step) and three datasets, achieving a state-of-the-art FID of 1.02 on ImageNet-256 (xAR-L) with only 0.36% additional compute.

## Strengths

1. **Simplicity and counterintuitive clarity of the core idea.** The method reduces to a single parameter merge (Eq. 2): fine-tune on self-generated data, then extrapolate backward. The paper articulates this cleanly, and the contrast between the simplicity of the procedure and the sophistication of the theoretical justification is a genuine strength.

2. **Theoretical grounding linking samplers to anti-alignment.** The paper provides formal analysis (Theorems 1 and 2) explaining *why* self-training degrades models and *why* reversing that degradation improves them. The connection between mode-seeking inference samplers (temperature < 1, top-k, CFG) and anti-aligned synthetic/population gradients is a genuine insight that predicts the phenomenon, not a post-hoc rationalization.

3. **Broad empirical validation.** Experiments span diffusion/EDM, flow matching, autoregressive (VAR, xAR), and few-step (IMM) models across ImageNet, CIFAR-10, and FFHQ at multiple resolutions. The universality claim is well supported, and the SOTA result on ImageNet-256 (xAR-L achieves FID 1.02, surpassing UCGM's 1.06) is genuinely impressive.

4. **Well-designed ablations.** Section 4.4 directly addresses the most obvious concerns: does Neon require a near-optimal base model? (No — Figure 9 shows broad applicability.) Does it require high-quality synthetic data? (No — Figure 10 shows robustness across CFG scales 1–3.) Is the signal transferable across architectures? (Yes — Figure 8.) The CIFAR-10C null result is a clean control confirming the mechanism.

5. **Practical efficiency.** The compute overhead is genuinely minimal (< 1% in most cases, as low as 0.005% for IMM), making this a practical method, not a theoretical curiosity.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **Theorem 1 contains an inconsistent subscript in the statement.** Line 110 defines alignment as s := ⟨r_d, P r_s⟩, but Theorem 1 (line 134) states "s = ⟨r_s, P r_s⟩." Since P is positive-definite, ⟨r_s, P r_s⟩ ≥ 0, contradicting the concept of anti-alignment that the theorem aims to establish. The rest of the paper's reasoning is internally consistent and relies on the anti-alignment of r_d and r_s (the definition on line 110). This is a typographical error in the theorem statement rather than a conceptual flaw, but it must be corrected.

2. **Coupled optimization of Neon weight w and CFG scale γ in autoregressive experiments partially conflates the source of improvement.** For autoregressive models (Section 4.2), the paper jointly optimizes over (w, γ) and reports the best FID against baselines at their original γ settings. The paper provides partial disentanglement — Figure 6 shows that for VAR-d16, γ-only re-optimization (γ=1.25, w=0) gives FID 3.01 vs. the original baseline 3.30, while adding w gives 2.01 — indicating w contributes the bulk of the gain. However, the headline comparisons (e.g., xAR-L: 1.28 → 1.02) would benefit from an explicit controlled experiment holding γ fixed at the baseline-optimal value and reporting the Neon-only improvement, to fully separate the two effects.

3. **Precision-recall tradeoff acknowledged but not discussed as a limitation.** Figure 4 shows that Neon monotonically decreases precision while increasing recall (inverted-U), with net FID improvement. The paper frames this as "redistributing probability mass" (a positive interpretation) but does not candidly discuss that for applications where generation precision is critical (e.g., avoiding false positives, faithful reproduction of specified content), the precision loss at the FID-optimal w* may be unacceptable. Reporting which downstream uses would prefer different points on this tradeoff would strengthen the paper's characterization of its own method.

4. **No confidence intervals or multiple-run variance reported for headline FID numbers.** The paper reports single FID values (Table A.1 referenced). FID has non-negligible variance across random seeds, and while the reported improvements are large enough to likely be significant, the lack of uncertainty quantification weakens the precision of the SOTA claim, especially for the narrow margins (e.g., 1.02 vs. UCGM's 1.06 on ImageNet-256).

### Trivial

None.

## Nice-to-Haves

- **The theory's sufficient condition for anti-alignment (Theorem 1) is a local guarantee.** The condition ‖ε‖_H_d < (m η₀)/(M(1+η₁))(−cos φ) involves quantities defined in terms of the sampler and true distribution that are not directly observable. The paper acknowledges and tests this empirically (Figure 9), showing Neon works across a spectrum of model qualities. This is not a flaw — the theory provides the right structural insight — but a direct measurement of the gradient angle s (e.g., via cosine similarity between θ_s−θ_r and a proxy for the true gradient) in a realistic neural network would further concretize the anti-alignment claim.

- **Wall-clock compute comparison.** The paper reports additional compute as a percentage of training budget, which is useful, but does not report wall-clock time or GPU-hours, which would be more actionable for practitioners.

- **Transferability experiment (Section 4.4) is CIFAR-10 only.** A demonstration of cross-architecture transfer on ImageNet-scale models would strengthen the claim; this is a natural direction for future work.

## Removed Points

- **"The precision-recall tradeoff is only shown for one model (EDM-VP on CIFAR-10, Figure 4)"** — REMOVED because this is factually incorrect. Figure 6 explicitly shows precision-recall trade-offs for VAR-d16 (an autoregressive model) on ImageNet-256, including heatmaps of FID, precision, and recall as functions of w and γ, plus asymptotic precision-recall curves. The paper also references Appendix D ("See Appendix D for all models").

## Novel Insights

Beyond the paper's own contributions, the review surfaces one genuinely novel observation: the analog between Neon and an effective data multiplier. The paper shows (Figure 9) that a model trained on only 30k real samples + Neon nearly matches a model trained on the full 50k dataset, suggesting Neon can compensate for ~40% reduction in real training data. This positions Neon not just as a post-hoc polish but as a potential tool for data-scarce regimes — a point that could be made more prominent.

## Suggestions

1. Correct the subscript in Theorem 1: s = ⟨r_d, P r_s⟩ (not ⟨r_s, P r_s⟩), consistent with the definition on line 110.
2. Add a controlled experiment for autoregressive models: hold γ fixed at the baseline-optimal value, vary only w, and report the Neon-only FID gain separately alongside the joint (w, γ) improvement.
3. Add a brief discussion of the precision-recall tradeoff as a limitation, noting applications where precision loss matters.
4. Report FID confidence intervals or variance across seeds for the headline results.
5. Include wall-clock compute time or GPU-hours alongside the percentage-of-training-budget figures.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>