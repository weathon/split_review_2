Now I have all the information needed for the final review.

## Summary

This paper introduces Neon, a post-hoc parameter-merging technique that improves pre-trained generative models by reversing self-training degradation. The key insight is that self-training degradation is structured (not random): mode-seeking inference samplers induce anti-alignment between synthetic and real-data population gradients, so extrapolating *away* from the degraded model's weights reduces true-data risk. The method requires only brief fine-tuning on self-generated samples, a simple parameter merge (θ_Neon = (1+w)θ_r − wθ_s), <1% additional compute, and no new real data or auxiliary models. Experiments span diffusion (EDM), flow matching, autoregressive (xAR, VAR), and few-step (IMM) models on CIFAR-10, FFHQ, and ImageNet. The headline result — xAR-L reaching FID 1.02 on ImageNet-256 with 0.36% extra compute — is a genuine SOTA advance.

## Strengths

- **Genuinely novel and counterintuitive core idea.** The observation that the degradation from self-training is not random noise but a *structured* signal anti-aligned with the true-data gradient — and that reversing it via a simple parameter merge can improve model quality — challenges common intuition about model collapse. The 2D Gaussian toy study (Figure 2) makes this geometric intuition concrete.
- **Well-developed theoretical framework (Theorems 1 and 2).** The paper provides a formal analysis linking mode-seeking inference samplers (low-temperature, top-k, CFG) to anti-alignment between synthetic and real-data gradients. The theoretical conditions are spelled out clearly (cos φ < 0 under monotone reweighting, the sufficient condition boxed inequality). This is significantly more rigorous than most self-training / model-collapse papers.
- **Impressive experimental breadth.** The method is tested across four fundamentally different model families (diffusion, flow matching, autoregressive, few-step) on three datasets. The consistency of improvement across all architectures strongly supports the claim that the mechanism is general.
- **Computational efficiency is genuinely impressive.** <1% additional compute, working with as few as 1k synthetic samples, no auxiliary models, no inference-time overhead — these claims are well-substantiated across all experiments.
- **Headline result is a genuine advance.** xAR-L achieving FID 1.02 on ImageNet-256 (surpassing UCGM's 1.06) with only 0.36% additional compute is a striking result.
- **Thoughtful ablation design.** The CIFAR-10C negative control (no improvement) is particularly well-designed — it demonstrates that Neon is not simply "any out-of-distribution data helps." The synthetic-data-quality sensitivity experiment (Figure 10) shows robustness across a wide CFG range.

## Weaknesses

### Fatal
None.

### Major
- **Figure 4 contains a verifiable caption error and an unresolved discrepancy with the paper's central claim.** (a) The caption (line 193) states "w = −1 corresponds to the model directly trained on synthetic data, i.e., θ_Neon = θ_r." Plugging w=−1 into Equation 2 gives θ_Neon = θ_s (the synthetic model), not θ_r — this is a clear typo. (b) More substantively, the figure description states the FID minimum for EDM-VP on CIFAR-10 is at w ≈ −0.5, which is the interpolation regime between base and degraded models (θ_Neon = 0.5θ_r + 0.5θ_s), while the caption claims "w > 0 corresponds to the negative extrapolation regime where Neon demonstrates its improvement capability." The paper does discuss that optimal w* decreases with fine-tuning (line 203), which could explain this for the larger training budgets. However, the contrast with the autoregressive results (VAR-d16 optimal w ≈ 1.0, Figure 6) is striking and unresolved: diffusion models peak at negative w (interpolation) while autoregressive models peak at positive w (extrapolation). Since the paper's title and claimed mechanism center on *negative extrapolation* (w > 0), the authors must clarify whether the diffusion results operate through a different mechanism and whether the naming "negative extrapolation" accurately describes the regime that produces improvements.

### Minor
- **The base model quality ablation (Figure 9) overstates its case.** The paper claims "Neon can compensate for a 40% reduction in real training data" and "offers substantial improvements across the entire quality spectrum." However, the figure description shows the EDM and EDM+Neon lines starting at nearly identical FID values (~1.87 at |D|=30k) and crossing around |D|=40k to similar endpoints (~1.85). The absolute improvement from Neon at 30k samples is ~0.02 FID, which is within the noise floor of FID (typical Monte Carlo variance ±0.05–0.1 at 50k samples), and no error bars or multiple trials are reported. This experiment does not provide strong evidence that Neon "compensates" for data reduction.
- **No error bars or confidence intervals on any FID numbers.** FID is a stochastic metric with Monte Carlo variance. Given that some improvements are small (e.g., ~0.02 FID in the data-reduction experiment, or the ~0.05 FID differences between self and cross-architecture transfer), it is unclear which results are statistically significant.
- **Missing empirical comparison against the most relevant baselines.** The paper discusses DDO, SIMS, and Discriminator Guidance as related methods but provides no head-to-head comparison on shared benchmarks using the same base models. The "SOTA" claim (FID 1.02) is verifiable against published checkpoints, but the community cannot assess whether Neon's improvement is larger or smaller than what DDO would achieve on the same xAR-L model.
- **The gap between single-step theory and multi-step practice is acknowledged but unverified.** The theory models fine-tuning as a single gradient step (θ_s = θ_r − αPr_s + O(α²)), while experiments use many steps. The paper's argument that the averaged displacement concentrates on the gradient direction when T is large and αT is small involves competing conditions that may not hold with standard reduced-LR recipes. Direct empirical verification that θ_s − θ_r is approximately collinear with the synthetic gradient at θ_r would substantially strengthen the link between theory and experiments.
- **The cross-architecture transfer claim is slightly overstated for the IMM case.** IMM synthetic data improves EDM-VP from FID 1.97 to 1.80 (a 0.17 improvement vs. self-transfer's 0.59 improvement). Calling this "highly effective" (line 241) is generous for the IMM transfer case, though the flow transfer (to ~1.45–1.59) is more convincing. The paper also does not test the reverse direction (e.g., using EDM data to improve flow models).

### Trivial
- Figure 4 caption typo: w = −1 should map to θ_Neon = θ_s, not θ_r.

## Nice-to-Haves
- **Direct anti-alignment measurement:** Computing the cosine similarity between (a) the empirical gradient on a held-out real validation set and (b) the displacement vector θ_s − θ_r (or the synthetic gradient at θ_r) and showing it is consistently negative would directly validate the claimed mechanism and bridge theory and experiment.
- **Investigation of the w* sign discrepancy:** Explaining why diffusion models peak at negative w (interpolation) while autoregressive models peak at positive w (extrapolation) would either strengthen the theory or reveal its limits. This might stem from different loss functions (MSE vs. cross-entropy) or fine-tuning dynamics.
- **Multi-step collinearity check:** Demonstrating empirically that the multi-step displacement vector θ_s − θ_r is approximately collinear with the initial synthetic gradient at θ_r would address the theory-practice gap.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "No access to original training data is misleading": The paper's claim is technically correct (only model weights needed, not the data itself).
- "Can't evaluate A-MONO assumption (appendix stripped)": Parser strips appendices from all papers; this is not an author error.
- "Missing appendix content": Same as above.
- "Cross-architecture reverse direction not tested": While valid, this is a scope limitation, not a flaw in what was done. Included in Minor as an asymmetric evidence concern.
- "Generic strengthening the paper suggestions": Moved to Nice-to-Haves where appropriate.

## Novel Insights

None beyond the paper's own contributions. The central insight — that self-training degradation is a structured, anti-aligned signal that can be reversed via a simple parameter merge — is the paper's own novel contribution, not something derived from the reviews.

## Suggestions

1. **Fix Figure 4** — Correct the w=−1 mapping to θ_s (not θ_r) and explicitly discuss the optimal w values for diffusion vs. autoregressive models, explaining why diffusion peaks at interpolation and AR at extrapolation.
2. **Add error bars** — Report FID with standard errors (e.g., bootstrapped over evaluation samples or multiple evaluation runs) for at least the key results.
3. **Temper the data-reduction claim** — Acknowledge that the FID improvement at 30k in Figure 9 is within the evaluation noise floor.
4. **Add direct anti-alignment measurements** — Computing cosine similarity between θ_s − θ_r and the real-data gradient would strongly validate the theoretical mechanism.
5. **Add empirical verification of multi-step collinearity** — Show that the multi-step fine-tuning displacement approximates the single-step synthetic gradient direction.

## Score and Decision

**Round 1 bracket (from calibration):** 5.5–7.5. Based on comparison with anchors: stronger than "Self-Consuming Generative Models Go MAD" (6.67, accepted) and "On the Stability of Iterative Retraining" (6.75, accepted), comparable to "Improved Techniques for Training Consistency Models" (7.00, accepted) and "Discrete Distribution Networks" (7.00, accepted), but not at the level of "Strong Model Collapse" (8.00, rejected — pure theory, different type).

**Final score: 7.0.** This paper presents a genuinely novel idea with non-trivial theoretical grounding and the most architecturally diverse experimental evaluation in the self-training improvement literature. The weaknesses (Figure 4 caption inconsistency, overstated ablation, missing baselines comparison, theoretical gap) are real but addressable and do not undermine the core contribution. The paper belongs at a strong conference venue.

**Anchors retrieved:**
- et5l9qPUhm.md ("Strong Model Collapse") — 8.00, Round 1, itemized — Pure theory paper establishing strong model collapse bounds; different paper type (no new method, no experiments on generative models).
- WttfQGwpES.md ("A Theoretical Perspective on STLs") — 6.67, Round 1, itemized — Theoretical framework for self-consuming loops; no new method, limited empirical validation.
- 1v7SRWsYve.md ("MAP Model Merging") — 6.33, Round 2, itemized — Model merging via Pareto fronts; similar in having a new method with theory, but substantially less experimental breadth.
- JORAfH2xFd.md ("On the Stability of Iterative Retraining") — 6.75, Round 1&2, itemized — Theoretical analysis of retraining on synthetic data; similar topic, but more limited empirical scope and some reviewer concerns about assumptions.
- 6p74UyAdLa.md ("Dynamic Negative Guidance") — 6.25, Round 1, itemized — Negative guidance for diffusion; similar concept of reversing degradation, but limited to diffusion and lacks theoretical depth.
- ShjMHfmPs0.md ("Self-Consuming Generative Models Go MAD") — 6.67, Round 2&3, itemized — Empirical/analytical study of model collapse loops; thorough but proposes no improvement method.
- WNzy9bRDvG.md ("Improved Consistency Models") — 7.00, Round 3, itemized — Method paper with strong empirical improvements; comparable in quality, similar strength of evidence.
- xNsIfzlefG.md ("Discrete Distribution Networks") — 7.00, Round 3, itemized — Novel generative model method; lower quantitative results, limited to small datasets.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>