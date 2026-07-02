## Summary

This paper argues that diffusion models in high dimensions cannot truly learn statistical quantities (scores, posterior means, velocity fields) due to a "weighted sum degradation" phenomenon: the posterior p(x₀|xₜ) becomes concentrated on a single training sample, collapsing the fitting target E[x₀|xₜ] to a nearest-neighbor. The paper also proposes a "Natural Inference" framework re-expressing various sampling methods (DDPM, DDIM, Euler, DPM-Solver, DEIS) as linear combinations of x₀ predictions. Quantitative evidence in Tables 1–2 shows this posterior concentration is indeed severe in the latent spaces of ImageNet-256 and ImageNet-512.

## Strengths

- **Provocative question.** The paper identifies a genuine puzzle: diffusion models are theoretically supposed to learn statistical quantities (score functions, posterior means) that suffer from the curse of dimensionality, yet they work well in high-dimensional settings. The disconnect between theory and practice explored in Section 1 is worth investigating.

- **Quantitative illustration of posterior concentration.** Tables 1 and 2 provide concrete calculations showing that in the latent spaces of ImageNet-256 and ImageNet-512, p(x₀|xₜ) is often dominated by a single training sample at low-to-moderate timesteps. The trends (concentration increases with dimensionality, stronger for flow matching than VP mixing) are internally consistent.

- **Correct technical observation about unification.** The observation that many samplers (DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, DEIS) can be expressed as linear combinations of x₀ predictions (Section 4) is technically correct.

## Weaknesses

### Major

1. **The paper fails to engage with the established theory that directly contradicts its central claim.** The paper argues that diffusion models "do not learn scores, posteriors, or velocity fields" (line 17, line 306), but never addresses the well-established results showing that denoising (predicting x₀ from xₜ) is equivalent to score matching:
   - **Denoising Score Matching** (Vincent 2011): training a model to denoise is provably equivalent to learning the score of the marginal distribution p(xₜ).
   - **Tweedie's Formula**: the posterior mean E[x₀|xₜ] is directly related to the score via E[x₀|xₜ] = (xₜ + (1−ᾱₜ)∇log p(xₜ))/√ᾱₜ, meaning learning E[x₀|xₜ] *is* learning the score.
   
   The paper itself correctly notes (lines 71–85) that the score can be expressed in terms of E[x₀|xₜ], and (lines 101–105) that the objective is equivalent to predicting x₀. To support its central claim, the paper would need to explain where and why these equivalences break down in high dimensions. It does not do so. This is not a reference-counting issue—it is a failure to engage with theory that, if correct, fully undermines the paper's thesis.

2. **No experimental validation of the central claim.** The paper makes fundamental claims about how diffusion models operate—that they cannot learn statistical quantities and that their apparent success relies on a different mechanism—yet provides zero experimental evidence:
   - No generation quality metrics (FID, IS, CLIP score) are reported.
   - No experiments showing that models trained under high "degradation" perform poorly or exhibit specific failure modes.
   - No ablation isolating the effect of the "degradation" phenomenon.
   - No demonstration that the "Natural Inference" perspective leads to better inference, debugging, or new algorithms.
   - No analysis relating the computed degradation rates (Tables 1–2) to actual model performance on those datasets.
   
   A theoretical paper can succeed without experiments if its reasoning is rigorous, but here the reasoning has a significant gap (point 1), making the lack of evidence critical.

3. **The logical connection from posterior concentration to the paper's conclusion is not established.** The paper shows that the optimal target E[x₀|xₜ] (Eq. 15) is a weighted sum over training samples, and that in high dimensions this weighted sum is often dominated by a single sample (Tables 1–2). The paper then asserts that this "hinders the model's ability to effectively learn essential statistical quantities" (line 9). However, the actual training objective (Eq. 103) is min_θ ∫∫ p(x₀, xₜ) ‖f_θ(xₜ) − x₀‖² dx₀ dxₜ, where every training pair uses a single x₀ as the target. The model learns the posterior mean E[x₀|xₜ] through generalization across many (xₜ, x₀) pairs, not by directly computing the weighted sum in Eq. 15. The paper acknowledges the equivalence between these two forms (lines 101–105) but then argues as if the degradation of the analytic form implies a problem with the training procedure, without explaining why. The observation of posterior concentration is real, but the paper does not establish why this prevents the model from learning useful representations—especially given that diffusion models demonstrably generate novel, high-quality samples.

4. **The "Natural Inference" framework is a valid re-description, not a novel framework.** Section 4 shows that various sampling methods can be expressed as linear combinations of x₀ predictions at different timesteps. This is mathematically correct, but it is a consequence of the linear structure of the backward differential equations, not a novel insight. The framework does not generate new predictions, improve existing methods, or provide analytical leverage that the existing formulations lack. The "Self Guidance" concept (Section 4.1) notes that linear interpolation between earlier and later x₀ predictions improves quality, which follows directly from later predictions being more accurate. The paper claims this framework is "free from any reliance on statistical concepts" (line 32), but this is a change in vocabulary, not a change in the underlying mathematics. The unification claim is descriptively accurate but not generative of new understanding.

### Minor

5. **The "train-test matching" motivation is a non-sequitur.** Line 209 states that because training predicts x₀, inference should also be understood as predicting x₀. But this is already how diffusion models work at inference time—each step evaluates the model on a noisy xₜ to produce a prediction. The paper's own derivation confirms this. There is no inconsistency that "Natural Inference" resolves.

6. **Threshold choice (0.9) for degradation is arbitrary.** The threshold for determining "weighted sum degradation" (line 139: p(x₀ = X₀'|xₜ = Xₜ) > 0.9) is not justified. The paper does not analyze sensitivity to this choice or show that it correlates with any measurable phenomenon.

7. **Unsupported speculation about actual degradation.** Line 165 states "the actual degradation ratio should be higher than the statistics show" due to limited sampling during training. This speculation is presented without analysis or evidence.

8. **No engagement with memorization literature.** Given that the paper's analysis suggests diffusion models may function through nearest-neighbor-like mappings, the lack of engagement with the memorization literature in generative models (e.g., Carlini et al. 2023, Somepalli et al. 2023) limits the paper's ability to contextualize its findings.

### Trivial

None.

## Nice-to-Haves

- If the paper were reframed as primarily making an empirical observation (posterior concentration) and a pedagogical re-description (Natural Inference), while dropping the unsupported claim that diffusion models do not learn statistical quantities, it could be a useful contribution. The observation in Tables 1–2 is genuinely interesting and could inform future work.
- Adding experiments that connect the degradation phenomenon to model behavior (FID scores, memorization metrics) would substantially strengthen the paper.
- Engaging with Tweedie's formula and denoising score matching would clarify where the paper's perspective aligns with or differs from established theory.

## Removed Points

These points from the input review were removed with brief justification:

- **"Fundamental logical error" (harsh critic #1, characterized as Structural):** Downgraded to Major weakness (point 3). The paper does correctly state the equivalence between the two objective forms (lines 101–105). The error is not in the mathematics but in the conclusion drawn from it—the paper fails to explain how posterior concentration invalidates the score-matching equivalence. This is a logical gap, not a fundamental mathematical error.
- **"The paper does not engage with the theory it claims to refute" (harsh critic #2, characterized as Structural):** Kept as Major weakness (point 1). "Structural" was too strong—the paper could potentially be compatible with score-matching theory if properly argued. The real problem is the absence of engagement.
- **"Natural Inference is not a new framework" (harsh critic #4, characterized as Methodological gap):** Kept as Major weakness (point 4). It is a valid re-description, which is a limitation but not "fatal."
- **"Train-test matching is a non-sequitur" (harsh critic #5):** Downgraded to Minor (point 5).
- **Section-by-section notes:** Collapsed into relevant weaknesses where they add substance.
- **"Strengthening the Paper on Its Own Terms" suggestions:** Incorporated into Nice-to-Haves.
- **Formatting/style nitpicks and missing-appendix complaints:** Removed per hard rules (parser artifacts).

## Novel Insights

None beyond the paper's own contributions. The reviews identify a key issue—that the paper's central claim is incompatible with established denoising score matching theory unless the paper shows where the equivalence breaks down—but this is a critique, not a novel insight about the paper's content.

## Suggestions

1. **Engage with denoising score matching theory and Tweedie's formula**: show where the equivalence between denoising and score learning breaks down in high dimensions, or acknowledge that the paper's perspective is compatible with this theory.
2. **Add experiments**: measure generation quality (FID) under varying degrees of posterior concentration; test whether the "Natural Inference" perspective enables new algorithms or improved performance.
3. **Clarify the scope of the claim**: if the paper intends to challenge existing theory, provide a mathematical argument for why the equivalences fail; if it intends to offer a complementary perspective, state this explicitly and drop the stronger claims.
4. **Analyze sensitivity** of the degradation metric to the 0.9 threshold.
5. **Connect the degradation phenomenon** to the memorization literature.

## Score and Decision

**Calibration anchors (retrieved from deepreview_13k_calibration):**

| Anchor Paper | Avg Human Score | Round | Comparison |
|---|---|---|---|
| "On the onset of memorization to generalization transition in diffusion models" | 3.40 | Bracketing | Similar topic (how diffusion models work), similar level of theoretical analysis but with toy model experiments; rejected for insufficient practical connection. Current paper has less experimental support. |
| "High variance score function estimates help diffusion models generalize" | 4.00 | Narrowing | Similar question about diffusion model generalization; has more theoretical depth; rejected. Current paper is weaker in theoretical rigor. |
| "On the Relation Between Linear Diffusion and Power Iteration" | 4.00 | Narrowing | Theoretical perspective on diffusion models with experiments; rejected. Current paper has no experiments. |
| "Rethinking Diffusion Posterior Sampling" | 6.67 | Bracketing | Similar "rethinking" framing with strong experimental support and proposed improvements; accepted. Current paper has vastly less experimental validation. |
| "GUD: Generation with Unified Diffusion" | 5.75 | Narrowing | Unification framework with experiments; rejected. Current paper's unification claim is a re-description without experiments. |

**Round-1 bracket:** 2.0 – 4.5 (based on comparison with similar-theory/no-experiments papers in the 3.4–4.0 range that were rejected).

**Narrowing rounds confirmed:** The paper shares the weaknesses of rejected papers in the 3.0–4.0 range (theoretical gaps, insufficient experimental support, overclaimed contributions) without matching the rigor of accepted rethinking papers (which provide extensive experiments). The posterior concentration observation (Tables 1–2) is genuinely interesting but does not salvage the paper's core argument.

**Final score:** 3 (Reject). The paper asks an interesting question and provides an empirically verified observation about posterior concentration, but its central claim that diffusion models do not learn statistical quantities is not properly justified—it fails to engage with the established equivalence between denoising and score matching, draws an unsupported logical leap from posterior concentration to "cannot learn," and provides no experimental validation. The "Natural Inference" framework is a descriptively accurate re-description but generates no new predictions or capabilities. The paper would need substantial revision—specifically, engagement with contradictory theory and experimental validation—to be publishable.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>