## Summary

This paper argues that the standard assumption behind diffusion models — that they learn statistical quantities like the score, posterior, or velocity field — is incorrect in high dimensions. The argument rests on a "weighted sum degradation" phenomenon: in high-dimensional sparse spaces, the conditional expectation E[X₀|Xₜ] (the fitting target) becomes dominated by a single training sample rather than being a smooth weighted average. The paper then proposes a "Natural Inference" framework that reframes sampling as autoregressive x₀-prediction without statistical concepts, claiming to unify DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, and DEIS.

## Strengths

1. **Clean derivation of the unified objective (Section 2, Equations 3–12).** The paper shows algebraically that the objectives of Markov-chain DDPM, score-based SDE models, and flow matching all reduce to learning E[X₀|Xₜ]. This is a useful pedagogical synthesis, presented with clear steps and explicit coefficient mappings.

2. **Frequency-domain perspective on the training objective (Section 3.3, Figures 2–4).** The explanation that training can be understood as frequency-dependent denoising/inpainting — where the model prioritizes reconstructing low frequencies first because they have higher SNR — provides an intuitive lens on why coarse-to-fine generation emerges. This is conceptually the most insightful part of the paper, though similar ideas have been discussed by Dieleman (2024), whom the paper cites.

## Weaknesses

### Fatal

None.

### Major

1. **The central claim that degradation "prevents learning" does not follow from the mathematical observation.** The paper shows that in high dimensions, under the empirical data distribution, the conditional expectation E[X₀|Xₜ] is dominated by a single nearest-neighbor training sample (Tables 1–2). The paper then concludes that this "hinders the model's ability to effectively learn essential statistical quantities" (Abstract) and that the model "cannot effectively learn the underlying probability distributions" (Conclusion, line 306).

   The logical gap: E[X₀|Xₜ] is the optimal target for MSE minimization *regardless of its shape*. If this function happens to be approximately a nearest-neighbor lookup under the empirical distribution, then learning that function *is* learning the correct conditional expectation. The peakedness of E[X₀|Xₜ] is a property of the data distribution, not evidence that learning fails. The paper's framing of the target as "inaccurate" (line 167) is self-contradictory — it is definitionally the correct target for the MSE objective. The conclusion that the model "cannot effectively learn" statistical quantities is an interpretation that does not follow from the premises presented. The paper conflates "the learned function has a particular (peaked) shape" with "the model cannot learn."

2. **No experimental validation of the central claim.** The paper makes a strong, falsifiable claim — that diffusion models trained in high dimensions do not learn the score/posterior/velocity field — yet provides zero experimental evidence. The paper never:
   - Compares a trained model's predictions to the true score or conditional expectation on any tractable distribution.
   - Shows that the degradation rates in Tables 1–2 correlate with degraded generation quality (e.g., by comparing models at different dimensions or noise schedules).
   - Provides any generated samples from the framework it describes.
   - Evaluates whether the Natural Inference framework matches or improves upon standard sampling methods quantitatively.
   
   Tables 1–2 demonstrate that degradation *occurs*, but never test whether it *matters* for model behavior. The central thesis is asserted rather than demonstrated.

3. **The Natural Inference framework (Section 4) is a reformulation presented as a discovery, without new methods or testable predictions.** The framework expresses xₜ as a linear combination of previous x₀ predictions and noise terms. This is a valid algebraic reframing, but:
   - It is not an "alternative mechanism" — the model still predicts x₀ from xₜ. Describing this as "learning the posterior mean" versus "predicting the clean image" is a change in vocabulary, not a change in what the network computes.
   - The claimed unification of DDPM, DDIM, DPM-Solver, etc., is described via placeholder coefficient matrices (cᵢʲ, bᵢʲ) that are never instantiated for any specific method in the main text. The main text reports that the sum of signal coefficients "approximately equals" √ᾱₜ (line 284) but does not specify the approximation error, the conditions under which it holds, or where the derivations can be verified without the appendix.
   - The framework leads to no new algorithms, improved results, or testable predictions. The paper acknowledges this ("exploring these possibilities could be a direction for future work," line 302), which undercuts the claim of substantive contribution.

### Minor

1. **Overstated novelty.** The paper claims "the first rigorous analysis" of the diffusion objective in high dimensions (line 31). Yet the paper itself acknowledges that Karras et al. (2022, Appendix B) presented a "similar conclusion" about the posterior distribution (line 125), and Dieleman (2024) is cited for the frequency-domain perspective. While the paper's analysis may be more detailed, the "first" claim is not appropriately calibrated to what the paper acknowledges as prior work.

2. **Arbitrary threshold without sensitivity analysis.** The degradation analysis uses p > 0.9 as the threshold (line 139). No sensitivity analysis is provided to show how results change with different thresholds. The paper also asserts that "the actual degradation ratio should be higher than the statistics show" (line 165) due to limited sampling, but provides no quantification of this effect.

3. **The relationship between the degradation analysis (Section 3.2) and the frequency perspective (Section 3.3) is not established.** These two lenses on the training objective are presented independently. The paper does not explain whether the degradation phenomenon follows from the spectral properties of natural images, or whether the two perspectives make consistent predictions about model behavior.

### Trivial

None.

## Nice-to-Haves

- An experiment that either validates the degradation claim (train on a tractable synthetic distribution with known ground-truth score and measure learning accuracy as a function of dimension) or falsifies it (showing that even under severe degradation, the model learns the correct conditional expectation).
- Concrete coefficient mappings for at least one specific sampling method (e.g., DDPM or DDIM) in the main text rather than only in the appendix.
- Generated samples to demonstrate that the Natural Inference perspective is actionable.

## Removed Points

These points from the input review are excluded or demoted. Treat them with caution:

- **"Central claim rests on a logical error that invalidates the main thesis"** (framed as *fatal*): Demoted to Major. The mathematical observation about E[X₀|Xₜ] being peaked is valid; the error is in the *interpretation* (equating peakedness with inability to learn). This is a significant overclaim but not a complete invalidation — the derivations in Sections 2 and 3.1 remain correct, and the frequency perspective has independent value.
- **Criticism about "per-sample estimation variance":** Removed because the paper's argument concerns the true conditional expectation (not the Monte Carlo estimate), so the critic's framing slightly mischaracterizes the paper. The core criticism (conclusion doesn't follow) is retained and rephrased in Weakness #1.
- **"Self Guidance is a straightforward extension":** Removed as an opinion, not a concrete weakness.
- **Criticism about derivations deferred to a parser-stripped appendix:** Removed per policy. The observation that the main text alone is insufficient for verification is retained.
- **Section-by-section notes about the abstract not returning to its framing question:** Removed as subjective.
- **"No generated samples" and "no quantitative comparison to existing methods":** Folded into Weakness #2 rather than listed separately.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the paper's contribution.** The strongest version of this paper would present the degradation phenomenon and the Natural Inference framework as *complementary perspectives* on how diffusion models work, not as evidence that the standard interpretation is wrong. The observation that E[X₀|Xₜ] is highly peaked in high dimensions is mathematically interesting; the paper should discuss what this implies about the nature of the learned function and generalization, rather than claiming the model "cannot learn."

2. **Add at least one experiment.** Either validate the degradation claim by testing whether a model trained under degraded conditions actually fails to match the true conditional expectation on a synthetic distribution, or falsify it by showing that degradation is harmless. Without such an experiment, the paper's central thesis is unsupported.

3. **Provide concrete coefficient mappings** for at least one sampling method in the main text so readers can verify the claimed unification without the appendix.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>