## Summary
The paper introduces NEON (Negative Extrapolation frOm self-traiNing), a deceptively simple post-hoc method that improves generative models by fine-tuning on self-generated synthetic data and then reversing the resulting gradient update via a parameter merge (Eq. 2). The core theoretical contribution is proving that mode-seeking inference samplers (e.g., temperature scaling, top-k, CFG) create a predictable anti-alignment between synthetic and real-data population gradients, so that negative extrapolation from the degraded model moves parameters toward lower true-data risk. The method achieves state-of-the-art FID of 1.02 on ImageNet-256 (xAR-L) with only 0.36% additional compute and works across diffusion, flow matching, autoregressive, and few-step generator architectures.

## Strengths
- **Simplicity and practicality.** Neon reduces to three lines: generate synthetic data, briefly fine-tune on it, and apply a linear parameter merge. No auxiliary models, no inference modifications, no likelihood computation. This is a striking advantage over prior work (Discriminator Guidance, SIMS, DDO) that requires additional networks or inference-time changes.
- **Strong theoretical foundation.** The anti-alignment analysis (Theorems 1–2) provides a principled explanation for why this counterintuitive procedure works. The proof that mode-seeking samplers guarantee cos φ <  (Theorem 2) cleanly connects the theory to standard inference practices (temperature < 1, top-k, CFG). The Taylor expansion in Eq. 4 gives a precise characterization of the optimal w* and the conditions under which Neon reduces risk.
- **Comprehensive empirical validation.** The method is tested across four fundamentally different model families (EDM diffusion, flow matching, xAR/VAR autoregressive, IMM few-step generators) on three datasets (CIFAR-10, FFHQ-64, ImageNet-256/512), with consistent improvements. The new state-of-the-art FID of 1.02 on ImageNet-256 with xAR-L is a strong headline result.
- **Well-designed ablation studies.** Cross-architecture transfer (Section 4.4), base model quality robustness (Figure 9 showing Neon compensates for 40% data reduction), and synthetic data quality sensitivity (Figure 10) all strengthen confidence in the method's generality and robustness.
- **Mechanistic insight via precision-recall analysis.** Figure 4 clearly demonstrates that Neon redistributes probability mass from over-represented to under-represented modes, providing an interpretable mechanism rather than just a benchmark improvement.

## Weaknesses
### Fatal
None.

### Major
- **W sign convention inconsistency.** In the diffusion/flow experiments (Figure 4), the optimal w appears to be around −0.5, while in the autoregressive experiments, the optimal w is positive (~1.0). The paper's main definition (Eq. 1–2) defines Neon with w > 0 for negative extrapolation, yet the diffusion experiments seem to operate in the w < 0 regime (interpolation toward θ_s). The text in Section 3.1 discusses "diversity-seeking samplers" requiring −1 < w < 0 but frames these as rare. If the diffusion experiments actually require w < 0 for optimal performance, the generality of the "negative extrapolation" narrative is weakened. The authors should clarify whether these negative optimal w values represent a different phenomenon and how it relates to Theorem 2's guarantees.
- **Joint hyperparameter optimization obscures the method's simplicity claim.** For autoregressive models, the paper jointly optimizes (w, γ) — the merge weight and CFG scale — and explicitly notes that co-optimization is "crucial" (Section 4.2, Figure 6). This adds non-trivial search cost beyond the simple parameter merge described in the abstract and contributions. The sensitivity analysis in Figure 10 helps but applies to xAR-B specifically; similar robustness guarantees for the joint (w, γ) search would strengthen the practicality claims.
- **Limited comparison depth with prior work.** While Neon is compared qualitatively against DDO, Discriminator Guidance, and SIMS in Section 2, the empirical comparison in the main text focuses on FID improvements over base models rather than head-to-head comparisons with these methods. Table A.1 is referenced but not shown. A direct comparison on at least one benchmark (e.g., CIFAR-10 EDM) would substantially strengthen the contribution claims.

### Minor
- **The U-shaped relationship with |S| (Section 3.1, "Finite |S| effects")** is discussed theoretically but the experimental validation is limited — Figure 3 shows the relationship between FID and B for different |S| values, but the U-shape in |S| for fixed B is not clearly demonstrated across all settings.
- **The FID-optimal inference settings are used to generate synthetic data,** meaning the synthetic data quality is tuned for the baseline evaluation metric. It would be informative to understand how the synthetic data quality for the *purpose of Neon* relates to the synthetic data quality for standard evaluation — these may have different optima.
- **No discussion of failure modes or limitations.** When does Neon fail? The method seems to always help in the experiments shown, but an honest characterization of when it would not (e.g., highly diverse samplers, very poor base models) would be valuable.

### Trivial
None.

## Nice-to-Haves
- A visualization of actual generated samples before and after Neon for non-ImageNet datasets (CIFAR-10, FFHQ) would complement the ImageNet samples in Figure 1.
- Empirical investigation of whether Neon benefits compound across multiple rounds (i.e., applying Neon to a Neon-improved model).
- Analysis of Neon's effect on sample diversity beyond FID — e.g., Coverage, LPIPS diversity scores, or class-conditional distribution analysis.

## Novel Insights
The paper's central theoretical insight — that mode-seeking inference samplers create a systematic anti-alignment between synthetic and real-data gradients, making the degradation direction a useful signal for improvement — is genuinely novel and well-motivated. This reframes model collapse/self-training degradation not as a failure mode but as a structured, harnessable corrective signal. The connection between sampler bias (mode-seeking behavior) and gradient anti-alignment (Theorem 2) provides a clean mechanistic explanation that goes beyond empirical observation. The cross-architecture transfer result (Section 4.4, Appendix B.8) is also a noteworthy finding: that models learning similar representations exhibit similar overconfidence patterns, enabling one model's degradation signal to correct another's biases.

## Suggestions
- Clarify the w sign convention systematically across all experiments. If the diffusion/flow experiments require w < 0 (interpolation), this should be stated explicitly rather than discovered by the reader from Figure 4's axis labels.
- Add a direct empirical comparison with at least one prior method (e.g., DDO on diffusion models) on the same base model and dataset to quantify Neon's advantages.
- Provide explicit hyperparameter search costs for the joint (w, γ) optimization to give a complete picture of the total computational overhead.

## Score and Decision
The paper presents a simple, theoretically grounded, and empirically validated method with broad applicability across generative model architectures. The theoretical contribution (anti-alignment under mode-seeking samplers) is elegant and well-connected to the empirical results. The empirical results are strong and comprehensive, with the new ImageNet-256 SOTA being a compelling headline. The main concerns — the w sign convention issue for diffusion models and the need for joint hyperparameter search — are notable but do not invalidate the core contribution. The method's extraordinary simplicity (< 1% additional compute, no auxiliary models, simple parameter merge) combined with strong results makes this a high-impact contribution.

MY FINAL SCORE: 8.0
MY FINAL DECISION: Accept