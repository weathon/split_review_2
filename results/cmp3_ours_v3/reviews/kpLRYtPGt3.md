## Summary

This paper introduces Neon (Negative Extrapolation from self-traiNing), a post-hoc parameter merge technique that improves image generation models by first fine-tuning on self-generated synthetic data (which degrades quality), then extrapolating *away* from the degraded checkpoint via θ_Neon = (1+w)θ_r − wθ_s with w > 0. The method requires no auxiliary models, no inference modifications, no likelihood computations, and no additional real data. Experiments across four model families (diffusion, flow matching, autoregressive, few-step generators) and three datasets (ImageNet, CIFAR-10, FFHQ) show consistent improvements, including a new ImageNet-256 SOTA of FID 1.02 (xAR-L) at only 0.36% additional compute. A theoretical framework based on anti-alignment of synthetic and real-data population gradients under mode-seeking samplers explains the mechanism.

---

## Strengths

1. **Genuinely simple and elegant method with remarkable universality.** The core idea — fine-tune on self-generated data, then extrapolate away — is remarkably concise. The method requires no auxiliary models, no inference modifications, no likelihood computations, and no additional real data. It works across diffusion, flow matching, autoregressive, and few-step generators, which is rare for a single technique in this space.

2. **Strong experimental breadth and consistent improvements.** The paper evaluates across four distinct model families and three datasets. The improvements are consistent across all settings. The SOTA result on ImageNet-256 (xAR-L: FID 1.02, surpassing UCGM's 1.06) is genuinely impressive, particularly at only 0.36% additional compute. The result that 4-step Neon nearly matches 8-step base model quality (FID 1.69 vs 1.98) has practical value for inference efficiency.

3. **Theoretical framework provides a credible mechanism.** The anti-alignment argument is well-posed: mode-seeking samplers (temperature < 1, CFG, top-k) create a systematic bias that pushes synthetic data gradients away from the population gradient direction. The formalization via Theorems 1 and 2 gives the method a conceptual foundation that goes beyond "it happens to work."

4. **Well-designed ablations.** The transferability experiment (Fig. 8), the base-model-quality study (Fig. 9), and the synthetic-data-quality sensitivity test (Fig. 10) each probe a meaningful failure mode. The CIFAR-10C null result is informative — it shows that not any out-of-distribution signal works, only the specific anti-aligned signal from generative model bias. The joint optimization of (w, γ) for autoregressive models (Fig. 6) is a genuinely informative practical finding.

5. **Minimal computational overhead.** The method consistently uses < 1% additional training compute (as low as 0.005% for few-step generators), and works effectively with as few as 1k synthetic samples. This makes it practical for real-world deployment.

---

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Figure 4 caption contains a factual error.** The caption states: "w = −1 corresponds to the model directly trained on synthetic data, i.e., θ_Neon = θ_r." Per the formula θ_Neon = (1+w)θ_r − wθ_s, plugging w = −1 gives θ_Neon = 0·θ_r − (−1)·θ_s = θ_s (the synthetic-data fine-tuned model), not θ_r. This is a clear typo in a key explanatory figure's caption, which could confuse readers. (Line 193, page 6.)

2. **The "4× more real data" claim from the toy example is substantially stronger than what real experiments support.** The caption of Figure 2 claims that Neon achieves "similar improvements to fine-tuning the base model with 4× more real data." This claim is from the 2D Gaussian toy example. The real-data ablation in Figure 9 shows a more modest effect: a model trained on 30k real samples + Neon nearly matches a model trained on 50k real samples — a 40% reduction, not 4×. The toy example's quantitative claim is not representative of the real improvement magnitude and could mislead readers. The main text should explicitly note this discrepancy.

3. **No explicit statement of optimal w regime for diffusion models.** The paper clearly establishes w > 0 as the operating regime (equation (1) defines w > 0, the caption of Figure 4 says "w > 0 corresponds to the negative extrapolation regime where Neon demonstrates its improvement capability"). However, the body text (line 203) only says "As fine-tuning progresses, the optimal w^* decreases" without stating the actual optimal values for the EDM-VP/CIFAR-10 case. The optimal w for autoregressive models is explicitly given (w^* ≈ 1.0 for VAR-d16), but it is not stated for diffusion/flow models. Given that the theory predicts w^* > 0, the paper should explicitly verify this.

4. **Key theoretical quantities are not empirically estimated in any experiment.** The theory relies on Hessian spectra (m, M), gradient bias η₀, Jacobian mismatch η₁, and cos φ, but none of these are measured or estimated for any real model. The theory therefore functions as a qualitative existence argument rather than a quantitative predictor. This is not a fatal flaw — many good ML papers have theory that motivates rather than predicts — but it means the experiments carry the entire weight of the evidence, and the theory cannot be tested against counterexamples.

5. **FID is reported as a point estimate without confidence intervals or variance.** For small synthetic datasets (e.g., 1k samples), the fine-tuning step could have non-negligible variance. Reporting results across multiple seeds for the fine-tuning step would strengthen the reliability claims.

### Trivial

- The cost of generating the synthetic dataset S (particularly for the large |S| = 750k case in the xAR-L experiment) is not explicitly stated alongside the fine-tuning compute overhead. While the fine-tuning budget is carefully reported, the inference cost to generate S itself should be stated for completeness.

---

## Nice-to-Haves

- Adding a weight-decay baseline for synthetic-data fine-tuning would further isolate the mechanism and confirm that Neon's effect is specific to reversal of the gradient direction rather than any form of regularization.
- Estimating even one of the theory's key quantities (e.g., the alignment s = ⟨r_d, Pr_s⟩) via finite differences for one real model would meaningfully tighten the theory–experiment connection.
- Adding confidence intervals or multiple-seed results for the fine-tuning step would strengthen reliability claims.

---

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Discrepancy between Figure 4 and text about whether extrapolation or interpolation is optimal"**: This criticism is based on the parser's unreliable attempt to describe the embedded figure image (lines 189–191: "FID plot shows a U-shaped curve with a minimum at w ≈ −0.5"), not on the paper's own text. The paper's own caption explicitly states "w > 0 corresponds to the negative extrapolation regime where Neon demonstrates its improvement capability" (line 193). The parser-generated figure description may be hallucinated or misread axis labels; it should not be treated as a claim by the paper. The only verifiable issue is the caption typo (θ_Neon = θ_r vs θ_s), captured above.

- **"Does not compare against interpolation baseline (w ∈ (−1, 0))"**: The paper plots FID across a range of w values in Figure 4 (spanning w = −1 through w > 0), which inherently includes both interpolation and extrapolation regimes. The missing piece is merely an explicit statement of where the FID optimum lies for diffusion models, captured above.

- **"Does not compare against early-stopping baseline"**: Figure 3 shows FID vs fine-tuning budget B, with the minimum at B > 0, confirming that some fine-tuning beyond the base model (B = 0) is necessary. The paper does explore this dimension.

- **"Real data needed for w tuning (tension with 'no real data' claim)"**: The paper explicitly acknowledges the standard 10k/50k sample evaluation protocol (line 179) for hyperparameter selection. The method does not need real data *for training*, only for validation — which is standard practice.

- **"Criticism about missing appendix proofs/discussion"**: The appendix is stripped by the PDF parser; it exists in the original submission.

- **"Missing related work"**: Cannot be verified without external sources.

---

## Novel Insights

The harsh critic's observation that the Figure 2 "4× more real data" claim is from a toy example while the real experiments (Figure 9) show ~40% reduction is a genuine insight about a mismatch between the paper's framing and its empirical evidence. This is a presentational issue — the main text could inadvertently lead readers to overestimate the real-data savings — but it does not undermine the method's validity. Additionally, the critic correctly notes that the paper does not explicitly state whether the FID optimum for diffusion models lies at w > 0 or w < 0, despite plotting the full range. These are the two most actionable weaknesses.

---

## Suggestions

1. Fix the Figure 4 caption typo (θ_Neon = θ_s at w = −1).
2. Explicitly state the optimal w range for diffusion/flow models (e.g., "the FID optimum occurs at w ≈ X, confirming that w > 0 is the correct regime").
3. Clarify that the "4×" claim in Figure 2 is from a 2D toy and does not directly transfer to real model improvements; rephrase to avoid misleading readers.
4. Briefly estimate the cost of generating S in the computational overhead discussion.
5. (Optional but valued) Provide confidence intervals or multiple-seed results for the fine-tuning step.

---

## Score and Decision

**Round 1 Bracket:** 6.5 – 8.0

After reviewing the calibration corpus, the following anchors were used:

| Anchor Paper | Avg Score | Round | Comparison to Neon |
|---|---|---|---|
| LCSC (QowsEic1sc) | 6.00 | R1 | Checkpoint averaging for DM/CM; similar simplicity but limited to small datasets (CIFAR-10, ImageNet-64). Neon tests larger-scale models and achieves SOTA. |
| AFA Ensemble (e32cI4r8Eo) | 6.29 | R1 | Feature-level diffusion ensembling; limited to SD1.5 architecture, adds inference overhead. Neon is simpler and more universal. |
| Self-Consuming MAD (ShjMHfmPs0) | 6.67 | R2 | Analysis paper on model collapse, not a method. Limited to StyleGAN2/FFHQ and DDPM/MNIST. Neon contributes a solution with broader experiments. |
| Beyond Model Collapse (MQXrTMonT1) | 6.50 | R2 | Theoretical study on synthetic data selection. Neon is a concrete method with SOTA results. |
| DMM (t73rC2GJQJ) | 4.50 | R1 | Distillation-based merging for style transfer; limited scope. Substantially weaker than Neon. |

Neon is methodologically stronger than the 6.0–6.7 anchors: it has a genuinely novel method (not analysis), broader experimental scope (4 model families vs. 1–2), SOTA results on ImageNet-256, a simpler and more elegant approach, and only minor weaknesses. It does not quite reach the 8.0 level of papers like Würstchen (architecture/engineering breakthrough) or Strong Model Collapse (comprehensive theory). A score of **7.5** appropriately reflects this — clearly above the 6.0–6.7 range of solid accepted papers, but not at the exceptional 8+ tier.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>