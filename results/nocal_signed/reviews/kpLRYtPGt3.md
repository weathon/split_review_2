Based on the impact-weighted analysis, the strengths are overwhelmingly positive (multiple items at +9+), and the weaknesses are moderate-to-minor. The paper's core contribution is novel, well-theorized, and empirically validated across diverse architectures. The weaknesses are addressable in revision.

## Summary

This paper introduces Neon (Negative Extrapolation from Self-Training), a post-processing method that improves pretrained generative models by reversing the degradation caused by brief fine-tuning on the model's own synthetic data. The key insight is that self-training degradation is not random noise but a structured signal anti-aligned with the real-data population gradient, so extrapolating away from the degraded parameters — via a simple parameter merge θ_Neon = (1+w)θ_r − wθ_s — reduces the true-data risk. The authors prove this theoretically (linking mode-seeking inference samplers to anti-alignment) and demonstrate it empirically across diffusion, flow matching, autoregressive, and few-step models, achieving a headline FID of 1.02 on ImageNet-256 with xAR-L at 0.36% additional compute.

## Strengths

- **Genuinely novel and counterintuitive idea (Sections 1, 3):** The core insight — that self-training degradation is not random noise but a structured, inverted signal that can be reversed via negative extrapolation — is creative and non-obvious. The paper shows that model collapse can be harnessed rather than just avoided.
- **Architectural universality with a unified method (Sections 4.1–4.3):** Neon is demonstrated across diffusion (EDM-VP), flow matching, autoregressive (VAR, xAR), and few-step (IMM) models. This breadth is uncommon in the generative model improvement literature, where prior methods are typically tied to one architecture family.
- **Impressive headline results (Section 4.2):** The xAR-L improvement from FID 1.28→1.02 on ImageNet-256 with only 0.36% additional compute is concretely impressive. Near-optimal performance even with 1k synthetic samples is striking.
- **Rigorous theoretical framework (Section 3.1):** The paper provides a formal account via anti-alignment, connecting inference-sampler properties (mode-seeking via monotone reweighting) to gradient geometry. Theorems 1 and 2 give sufficient conditions under which Neon provably reduces the true-data risk.
- **Honest analysis of the precision-recall trade-off (Figure 4, Section 4.1):** The paper clearly shows that Neon trades precision for recall and explains why this yields net FID improvement, with mechanism consistent with the theoretical analysis.
- **Cross-architecture transfer (Section 4.4):** Showing that synthetic data from a flow matching model can improve a diffusion model (and vice versa) validates the claim that the degradation signal captures a generic bias rather than an architecture-specific artifact.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Asymmetric comparison with prior methods (Section 2).** The related work correctly identifies limitations of DDO, SIMS, and Discriminator Guidance (architecture-specific, inference modifications), but does not acknowledge that these methods require no additional fine-tuning, while Neon does (even if brief). The framing as "Neon requires no auxiliary models, no inference modifications, no likelihood computations" omits Neon's own trade-off. The methods could be framed as complementary rather than Neon being strictly superior.

- **FID evaluation details are underspecified (Section 4).** The paper does not state which reference set (e.g., ImageNet training set split, specific preprocessing) is used for FID computation. This matters because minor protocol differences can shift FID by 0.05–0.1 on ImageNet-256, and the paper makes a SOTA claim (FID 1.02). The referenced Appendix C was stripped from the review copy, but these details should be accessible in the main text or a reliably present appendix section.

- **Theoretical sufficient condition not empirically calibrated (Theorem 1).** The sufficient condition involves quantities (η₀, η₁, cos φ) that are not empirically measured or estimated for any studied model. The theory provides valuable intuition and proof-of-concept, but does not generate testable predictions or quantitative bounds verifiable against the experiments.

- **The 1k-sample claim could be clearer (Section 4.2).** The statement that "even with just 1k samples, the xAR models achieve near-optimal performance" refers to FID after tuning w via grid search, which requires real reference data. When presented as a selling point for data-scarce settings, this dependency should be explicitly noted.

### Trivial

- **Hyperparameter w tuning tension with framing.** The paper states Neon "requires no additional real training data, no access to the original training data" (Abstract, Contributions [C1]), yet w (and γ) is tuned via FID-based grid search requiring real reference statistics. The merge operation itself is truly data-free, but hyperparameter selection requires some real data. This is a framing/overstatement issue rather than a methodological flaw — the paper should qualify the claim, or demonstrate that a fixed w works robustly across settings. (This does not invalidate the method; the impact on practical deployability is bounded.)

## Nice-to-Haves

- Demonstrate that a fixed value of w (e.g., w=1 or a plateau midpoint from Figures 3–4) works near-optimally across all settings without per-dataset tuning.
- Provide a direct experimental comparison with at least one prior method (e.g., DDO for autoregressive models, SIMS for diffusion) under matched conditions.
- Report FID with confidence intervals over multiple seeds and report wall-clock time or GPU-hours for the full Neon pipeline.
- Include an explicit FID reference statistics specification in the main text.

## Removed Points

These were surfaced in the input review but are removed per filtering rules:

1. "SOTA claim may have shifted by July 2026" — Speculative; not grounded in paper content.
2. "UCGM comparison should re-evaluate under same pipeline" — Citing another paper's reported number is standard practice.
3. "DDO and SIMS require no additional training whatsoever" — Overstated; DDO requires reference models, SIMS requires inference-time computation. Rephrased accurately above.
4. Formatting/style nitpicks and missing-appendix complaints — Parser issues or standard removal criteria.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the hyperparameter-tuning tension as the central unresolved question, which the paper itself does not directly address.

## Suggestions

1. Qualify the data-access claim: explicitly state that the Neon merge operation is data-free, but hyperparameter tuning requires a small real validation set for FID-based evaluation. Better yet, test whether a fixed default w works across settings.
2. Provide explicit FID reference details (dataset split, preprocessing, number of real samples) in the main text.
3. Acknowledge the fine-tuning requirement when comparing with inference-only methods (DDO, SIMS) to present a balanced trade-off.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>