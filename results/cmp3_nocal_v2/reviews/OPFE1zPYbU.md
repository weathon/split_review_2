## Summary

This paper argues that in high-dimensional spaces, the fitting target of diffusion model objectives—the posterior mean E[x₀|xₜ]—concentrates on single training samples (a phenomenon called "weighted sum degradation"), which the authors claim prevents the model from learning statistical quantities like the posterior, score, or velocity field. The paper then proposes a "Natural Inference" framework that unifies existing sampling methods (DDPM, DDIM, Euler, DPM-Solver, etc.) as linear combinations of x₀ predictions, offering a statistical-concept-free view of inference.

## Strengths

- **The degradation phenomenon is clearly formulated and empirically demonstrated.** Section 3.2 derives Equation (15) showing that E[x₀|xₜ] is a distance-weighted sum over training samples, and Tables 1–2 provide striking quantitative evidence that for early timesteps (t<600) in ImageNet-256/512 latent spaces, the posterior mass concentrates (>0.9 probability) on a single sample nearly 100% of the time. The separation between "any degradation" and "degradation to the originating X₀" is a useful analytical distinction.

- **The unification of sampling methods under a linear-combination framework is mathematically clean and nontrivial.** Section 4.3 shows that DDPM, DDIM, Euler, DPM-Solver, DPM-Solver++, and DEIS can all be expressed as lower-triangular linear combinations of x₀ predictions with coefficient matrices. This reparameterization provides a concrete way to compare solver structures, even if primarily an organizational contribution.

- **The presentation of the training objective equivalences (Section 2) is clear and technically competent.** The reduction of Markov-chain, score-based, and flow-matching objectives to learning E[x₀|xₜ] (Equations 3–12) is correctly derived and well-organized.

## Weaknesses

### Fatal
None.

### Major

1. **The core logical claim—that degradation prevents learning statistical quantities—contradicts the paper's own mathematical framework and is not supported by the evidence presented.**

   The paper argues: (a) training reduces to learning E[x₀|xₜ] (Section 2, correct); (b) in high dimensions, E[x₀|xₜ] is concentrated on single training samples (Section 3.2, supported); therefore (c) "the model cannot effectively learn the essential statistical quantities of the underlying data distribution, including the posterior, score, and velocity field" (lines 24–25, 31, 306).

   Step (c) does not follow from (b). A model trained to minimize E[‖f_θ(xₜ) − x₀‖²] converges to E[x₀|xₜ] regardless of whether the posterior is concentrated. Concentration implies low posterior variance, which makes the stochastic gradient estimator *more* accurate, not less. Furthermore, the paper's own Section 2 derivation (Equations 8–9) shows that the score ∂log p(xₜ)/∂xₜ is an *affine function* of E[x₀|xₜ]: ∂log p(xₜ)/∂xₜ = (√ᾱₜ/(1−ᾱₜ))·E[x₀|xₜ] − (1/(1−ᾱₜ))·xₜ. So if the model learns E[x₀|xₜ]—even a concentrated version—it mathematically *is* learning the score (this is essentially Tweedie's formula, which the paper never discusses). The paper's central thesis that "diffusion models do not learn these statistical quantities" is therefore internally inconsistent with its own derivations in Section 2.

   *What the evidence actually supports* is a more modest claim: the posterior mean E[x₀|xₜ] is highly concentrated on individual training samples, which suggests the model's effective behavior is local denoising/nearest-neighbor regression rather than smooth global distribution modeling. This reinterpretation is interesting, but the paper states it as a failure of learning rather than a characterization of what is learned.

2. **The Natural Inference framework is presented as a key contribution but is not evaluated for usefulness.**

   The paper claims three advantages for the framework: it unifies existing sampling methods (supported), it is "more visual and interpretable" (line 300), and it may enable "other, potentially more optimal parameter configurations" (line 302). The latter two claims are unsupported. No visualization of the inference process is shown and analyzed in the main text (Figures 15–16 are referenced but parser-stripped). No new sampling method is derived from the framework. No experiment demonstrates that searching the coefficient space leads to better generation. The framework remains a clean reparameterization of existing methods, but the paper does not show that it enables anything beyond description. For a paper whose title promises to "rethink" diffusion models, the lack of any empirical demonstration that the rethinking leads to new capabilities or insights is a significant weakness.

### Minor

1. **No sensitivity analysis for the degradation threshold.** The degradation measurement (Tables 1–2) uses a single threshold of 0.9 posterior probability on a single sample. How robust are the reported rates to thresholds of 0.8 or 0.99? This matters because the paper's main argument hinges on these numbers.

2. **The frequency-domain perspective (Section 3.3) is not novel.** The observation that diffusion models generate from low to high frequencies (coarse-to-fine) is well established in the literature (Dieleman, 2024, is cited but the paper does not discuss what it adds beyond this existing perspective). The claim that the objective can be understood as "filtering higher-frequency components" (line 193) is a known reframing, not a novel finding of this paper.

3. **No generative quality evaluation.** The paper presents no FID, IS, or any generation quality metric. For a paper making strong claims about *how* diffusion models operate (that they do not learn statistical quantities), some acknowledgment of whether this perspective is consistent with known generative capabilities is reasonable. For instance: if degradation prevents learning statistical quantities, why do diffusion models generate high-quality samples? The paper's implicit answer ("they do local denoising/information enhancement") could be tested by analyzing whether model predictions are indeed local.

4. **No discussion of limitations.** The conclusion (Section 5) states the paper's claims without acknowledging limitations of the analysis, alternative interpretations, or scope of the claims. For a position paper challenging an established view, this omission is notable.

5. **"First rigorous analysis" overstatement (line 31).** The analysis in Section 3.2 relies on a Dirac-delta approximation to the data distribution (treating it as purely discrete over training samples, Equation 14) and a threshold-based empirical measurement. While the analysis is thoughtful, the "first rigorous" framing overstates what is ultimately an approximate empirical characterization.

6. **Self Guidance (Section 4.1) connection to the rest of the paper is not developed.** The analogy between CFG, unsharp masking, and Self Guidance is clever, but the paper does not concretely connect this to the degradation analysis or use it to derive any actionable insight. The claim that linear combinations in Natural Inference "can be interpreted as a composition of multiple Self Guidance operations" (line 266) is stated but not developed into a concrete analysis.

### Trivial
None.

## Nice-to-Haves

- **Sharpen the framing.** Instead of "models cannot learn statistical quantities," frame the contribution as: "The posterior mean E[x₀|xₜ] is concentrated on individual training samples, implying the model's effective behavior is local denoising rather than global distribution modeling. This does not invalidate the mathematical equivalence to score matching, but changes how we interpret what is learned." This would make the argument logically consistent with the evidence.

- **Derive at least one new sampling method** from the Natural Inference framework (e.g., a non-standard coefficient configuration) and evaluate it, even qualitatively. This would demonstrate the framework's generative potential.

- **Include a traceable example in the main text** showing how one method (e.g., DDIM with 4 steps) maps to the coefficient matrices, so the reader can follow the framework without going to the appendix.

- **Add sensitivity analysis** for the 0.9 degradation threshold and discuss the implications of the Dirac-delta approximation on the strength of conclusions.

## Removed Points

- *"The 'due to limited sampling during training' note is confusing"* — The paper's meaning is actually clear: mini-batch sampling during training would produce even higher degradation rates than the full-dataset measurement. Removed.

- *"Computational cost of the degradation measurement is not discussed"* — An implementation detail not material to the paper's claims. Removed.

- *"Missing related work on spectral bias"* — Unable to verify the existence or precise relevance of suggested citations; rule forbids raising missing related works. Removed.

- *"Framework explanation relies on the appendix"* — The appendix exists (parser-stripped); reliance on supplementary material for detailed derivations is standard. Demoted from consideration.

- *Various section-by-section presentation nitpicks* (e.g., "the connection to the rest of the paper is unclear" without concrete anchor points) — addressed in the minor weaknesses above where specific and verifiable.

- *Strengths about the problem being "important" or "timely"* — generic, removed.

## Novel Insights

The harsh critic's analysis surfaces a genuine logical inconsistency in the paper: the model *is* trained to learn E[x₀|xₜ], which IS a statistical quantity and IS mathematically equivalent to the score via Tweedie's formula (as implicitly shown in the paper's own Equation 9). The paper's claim of a "fundamentally different mechanism" is not supported because the mathematical equivalence between denoising and score matching holds regardless of whether the posterior is concentrated. What the evidence actually supports—and what would be an interesting contribution if properly scoped—is that E[x₀|xₜ] is a degraded, localized quantity in high dimensions, which has implications for how we interpret what diffusion models learn, even if it does not break the standard mathematical framework.

## Suggestions

1. Reframe the core claim to be logically consistent: the degradation phenomenon reveals that E[x₀|xₜ] is concentrated on single training samples (local nearest-neighbor denoising), not that the model "cannot learn" statistical quantities.
2. Either validate the Natural Inference framework with a concrete new method or discovery, or scope it as a unification/reparameterization without claiming practical advantages.
3. Add a discussion of Tweedie's formula to directly address the relationship between E[x₀|xₜ] and score learning.
4. Include sensitivity analysis for the degradation threshold and some generative quality metrics to contextualize the analysis.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>