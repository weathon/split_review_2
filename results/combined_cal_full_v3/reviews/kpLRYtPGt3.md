Based on the calibration comparison with accepted papers (Shortcut Models at 8.00, Improved Consistency Models at 7.00, T-Stitch at 7.00), Neon's strengths are comparable or higher (8.24–10.45 vs 7.35–10.29 for Shortcut Models), and its weaknesses (0.95–7.33) are within the range seen in accepted papers (T-Stitch had items as low as 0.84). I'll assign **7.5**.

## Summary

This paper introduces Neon, a post-hoc parameter merging technique for improving pre-trained generative image models. The method is remarkably simple: (1) briefly fine-tune the model on its own self-generated synthetic data (which degrades it), then (2) reverse this degradation via negative extrapolation: θ_Neon = (1+w)θ_r − wθ_s. The key insight is that degradation from self-training is not random noise but a structured signal anti-aligned with the real-data gradient, so reversing it corrects the model. The paper provides theoretical analysis (Theorems 1–2), showing that mode-seeking inference samplers induce this anti-alignment under formal assumptions, and evaluates Neon across diffusion, flow matching, autoregressive (xAR, VAR), and few-step (IMM) models on ImageNet, CIFAR-10, and FFHQ.

## Strengths

- **A genuinely counterintuitive and novel idea.** The central insight — that self-training degradation is not noise but a structured, anti-aligned signal, and that reversing it via negative extrapolation yields improvement — is surprising and non-obvious. This makes the paper genuinely interesting rather than incremental.

- **Remarkable simplicity.** The method is a single equation: θ_Neon = (1+w)θ_r − wθ_s. It requires no auxiliary networks, no inference-time modifications, no likelihood computations, and no additional real data. This contrasts favorably with prior approaches like DDO, Discriminator Guidance, and SIMS.

- **Genuinely broad empirical validation** across diffusion (EDM-VP), flow matching, autoregressive (xAR, VAR), and few-step (IMM) models on three datasets (ImageNet, CIFAR-10, FFHQ). The method delivers meaningful FID improvements in every setting — e.g., xAR-L on ImageNet-256 achieves **1.02 FID** (from 1.28) with 0.36% extra compute; EDM-VP on FFHQ-64 achieves **1.12 FID** (from 2.39) with 0.85% extra compute.

- **Cross-architecture transfer (Section 4.4)** is a non-trivial finding: synthetic data from a flow matching or IMM model can improve an EDM-VP model. This is practically useful when inference on the target model is expensive.

- **Thoughtful ablation studies** testing sensitivity to synthetic data quality (Figure 10), base model quality (Figure 9), and synthetic dataset size (Figure 3). The CIFAR-10C control (null result with corrupted real images) is an excellent sanity check that rules out the trivial hypothesis that any out-of-distribution data would suffice.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The theory provides intuition but the gap between its sufficient conditions and the practical regime is large.** The analysis (Section 3.1) is rigorous within its formal model but relies on several unverified assumptions: local convexity/directional smoothness of the risk, the A-MONO curvature-density coupling assumption for diffusion/flow models (footnote 2), and the short-fine-tuning Taylor approximation. The sufficient condition in Theorem 1 (small model error ‖ε‖) is far from necessary — the method works even for models trained on as few as 30k CIFAR-10 samples (Figure 9) where model error is presumably large. The paper's claim (C2) that the theory "guarantees the effectiveness of negative extrapolation" is accurate within the formal setting, but the gap between the sufficient condition and practice limits the theory to a working hypothesis rather than a verified guarantee for deep networks. This does not undermine the empirical results.

- **For autoregressive models, the (w, γ) joint tuning introduces ambiguity in attributing gains.** The paper shows for VAR-d16 that independent γ optimization (without Neon) yields FID 3.01 vs. joint optimization yielding 2.01, demonstrating synergy. However, for the headline xAR-L result (1.28→1.02), the paper does not provide a "base model + re-tuned γ" baseline. The fraction of gain attributable to Neon versus finding a CFG scale not explored in the original paper is not fully separable. This is a limited concern — the diffusion/flow experiments (which don't use CFG) independently support the core Neon claim with no such confound.

- **Compute accounting focuses exclusively on training overhead.** The paper states Neon requires "< 1% additional compute" (abstract specifies "additional training compute"), which refers only to the fine-tuning budget. The one-time cost of generating synthetic data is not reported. For the xAR-L result, generating 750k ImageNet-256 samples from an autoregressive model with sequential decoding has non-trivial inference cost. The paper should report both components transparently. This is a presentation gap rather than a methodological flaw — the training overhead claim is accurately characterized.

- No limitations section is included. Several limitations worth acknowledging: the improvement comes from a precision-recall tradeoff (may not benefit precision-critical applications); the method is demonstrated only for image generation; the theory's assumptions are not verified for the deep networks used.

### Trivial
None.

## Nice-to-Haves

- Include head-to-head comparisons with prior methods (SIMS, DDO, Discriminator Guidance) on matched settings.
- Explore iterative application of Neon (θ_r → θ_Neon → generate new synthetic data → fine-tune → merge again).
- Provide practical guidance on w selection when no real validation data is available.
- Directly test the anti-alignment hypothesis at the gradient level (compute inner product of r_d and r_s) for a small-scale experiment.

## Removed Points
None.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
The paper would benefit from reporting both sampling and fine-tuning compute costs, providing the re-tuned CFG-only baseline for xAR-L, and adding a brief limitations section. These are straightforward to address and would strengthen an already compelling paper.

## Score and Decision

**Calibration Anchors Considered:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OlzB6LnXcS.md` (Shortcut Models) | 8.00 | R1 | Yes | Similar novelty level; Neon has broader architectural validation but is a post-hoc method rather than a new model family |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/WNzy9bRDvG.md` (Improved Consistency Models) | 7.00 | R1 | Yes | More incremental (improving existing method); Neon is more novel |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2mqb8bPHeb.md` (T-Stitch) | 7.00 | R2 | Yes | Simpler idea, training-free acceleration; Neon has deeper contribution |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JORAfH2xFd.md` (Iterative Retraining) | 6.75 | R2 | Yes | Strong theory, weaker experiments; Neon has stronger empirical validation |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lNtio1tdbL.md` (ATM) | 3.00 | R1 | Yes | Fundamentally flawed; Neon is much stronger |

**Round 1 Bracket:** 7.0–8.0 (based on comparison with Shortcut Models at 8.00 and Improved Consistency Models at 7.00)

**Round 2 Narrowing:** Papers at 7.00–7.50 (T-Stitch at 7.00, various 7.33–7.50 papers) have comparable strength profiles. Neon's very high strength favorability (8.24–10.45) is on par with Shortcut Models (8.71–10.29), while the main weakness (theory gap at 0.95 favorability) is comparable to T-Stitch's theoretical gaps at 0.84. Neon's core contribution — the counterintuitive insight that reversing self-training degradation improves models — combined with broad empirical validation across 4 model families, places it above purely incremental work (Improved Consistency Models at 7.00) and closer to the Shortcut Models benchmark (8.00). The weaknesses are minor and addressable.

**Final Score: 7.5** — Between borderline accept and accept. The paper introduces a genuinely novel, simple, and broadly validated method. The identified weaknesses (theory-practice gap, attribution ambiguity for AR models, compute accounting) are real but do not threaten the core claim, which is independently supported by CFG-free experiments.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>