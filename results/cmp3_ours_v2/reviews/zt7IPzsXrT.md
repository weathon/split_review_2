Now I have a solid calibration. Let me write the final review.

## Summary

This paper proposes ScaPre, a framework for large-scale concept unlearning in diffusion models. It combines three components: (1) a spectral trace regularizer (Eq. 3) with SVD-based gating to suppress conflicting weight updates across multiple concepts, (2) a Bures-distance geometry alignment (Eq. 5) to preserve global structure, and (3) an Informax Decoupler (Eq. 6–7) that uses mutual information to identify concept-relevant parameters and restrict updates to targeted subspaces. The core optimization yields a closed-form Sylvester equation (Eq. 9), with a proximal refinement for the geometry term. Experiments on Imagenette (10 classes), ImageNet-Diversi50 (50 classes), and ImageNet-Confuse5 (fine-grained disentanglement) show strong unlearning performance while maintaining generation quality, with 120-second runtime for 50 concepts.

## Strengths

- **Strong empirical results with large performance margins.** On ImageNet-Confuse5 (Table 4), ScaPre achieves 84.3% Overall Acc vs. 50.3% next-best (SP/ESD) — a qualitative regime change in fine-grained disentanglement. On ImageNet-Diversi50 (Table 3), ScaPre achieves 65.30 UQ vs. next-best 56.35 (ESD). These results are supported by individual raw metrics (Avg Acc, CLIP score, Preserve Acc) that independently tell the same story.

- **Efficiency claim is credible and well-supported.** The 120-second runtime for 50 concepts (Sec. 5.5) is demonstrated alongside direct comparisons of execution time and memory usage across methods (Figure 3). No additional data or auxiliary modules are required, which is a practical advantage for real-world deployment.

- **Method components are grounded in specific, identified failure modes.** The spectral trace regularizer targets conflicting weight updates (S penalizes high-variance directions; R via SVD gates overlapping concept embeddings); the Bures distance preserves covariance structure rather than raw weight differences; the Informax Decoupler targets parameter-level precision. This design-by-failure-mode approach is principled.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **Informax Decoupler notation is ambiguous (Sec. 4.2).** The paper writes *aᵢ(s) = W_{i,s}* and calls this "the activation of channel i on input feature s." If W_{i,s} denotes a static weight element of the projection matrix, then the mutual information between this constant and the label y would be zero, making the decoupler a null operation. The intended reading (activation = dot product of row i with feature s) is clear from context — otherwise the empirical results would be impossible — but the notation is nonstandard and needs to be corrected. The paper should also specify the number of samples K used for MI estimation and how the adaptive threshold τᵢ is set.

- **"Closed-form" framing overstates the simplicity of the full pipeline.** The core solution (Eq. 9) is indeed a closed-form Sylvester equation, but the complete pipeline includes: computing second-order statistics S by aggregating features across all target concepts (Eq. 4), performing SVD and sigmoid gating for R, running forward passes to estimate MI for each channel (Sec. 4.2), and a post-hoc proximal refinement on the Bures geodesic (Sec. 4.3). This goes well beyond the plug-and-chug matrix inversion of UCE or RECE. The paper should qualify "closed-form" to reflect the data-dependent preprocessing and geometric post-hoc step.

- **UQ metric is normalised across the method set in each table.** As defined in Sec. 5.2, UQ uses the mean and standard deviation of metrics *across the methods being compared*, making UQ values incomparable across tables and sensitive to which methods are included. This is a weakness of the composite metric, though it does not undermine the paper's conclusions because all individual raw metrics (Avg Acc, CLIP score, Preserve Acc) are reported in full and independently support the same claims.

- **Key hyperparameters not reported in the main text.** The spectral trace coefficient λ (Eq. 3), the geometry alignment coefficient β (Eq. 8), the number of samples K for MI estimation, the adaptive threshold τᵢ, and the "partway" fraction along the Bures geodesic are not specified in the main paper. These may appear in the appendix but should be stated in the main text for reproducibility.

- **"SP" abbreviation used in all tables is not defined in the main text.** The related work section (Sec. 2.2) mentions "Sculpting Memory (Li et al., 2025a)" but never introduces "SP" as its abbreviation.

### Trivial

None.

## Nice-to-Haves

- The paper would benefit from reporting variance across runs or seeds, as generative model evaluations can have substantial variability.
- A scatter plot of Unlearn Accuracy vs. CLIP score (one point per method, with Pareto frontier) would be more informative than the composite UQ.

## Removed Points

These points were raised in input but removed per the filtering rules:

- "Adversarial robustness and explicit content results deferred to the appendix" — Removed: the parser strips appendices from all papers; they exist in the original submission.
- "Figure 1 claim is vague" — Removed: visual comparisons are standard supporting evidence, not a substantive weakness.
- "Transition from Eq. 8 to Eq. 9 is underspecified" — Removed: the paper points to Appendix B.1 for the derivation, which is standard practice.
- "Missing variance / seed reporting" — Removed: single-run evaluation is the norm for this kind of benchmark; requesting multi-run statistics is a nice-to-have, not a weakness.
- "Number of images per prompt not reported" — Removed: these details belong in the experimental setup, likely in the (stripped) appendix.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. In Sec. 4.2, replace the ambiguous notation *aᵢ(s) = W_{i,s}* with something like *aᵢ(s) = (Wᵢ)ᵀ s* or *aᵢ(s) = row_i(W) · s* to make clear that this is an activation that depends on the input. Also report K (sample size) and the rule for setting τᵢ.
2. Add a brief table of hyperparameter values (λ, β, K, geodesic fraction) to the main text, ideally in Sec. 5.1 or a footnote.
3. Tone down the "closed-form" framing: replace "closed-form solution" with "efficient closed-form core with data-dependent preprocessing."
4. Define "SP" explicitly in the related work section.

## Score and Decision

**Bracket (Round 1):** 5.5–7.5, based on comparison with accepted concept-unlearning papers (ConceptPrune 5.75, Growth Inhibitors 6.00, Optimal Targets AGE 6.33, SFD 6.50). ScaPre's empirical results are stronger than the lower end of this band, and its weaknesses are minor and addressable.

**Anchors consulted:**
- RealEra (avg 3.40, Reject) — much weaker than ScaPre in evaluation breadth and technical depth
- CORE (avg 4.00, Reject) — simpler method; ScaPre is more technically sophisticated with better results
- EraseDiff (avg 5.60, Reject) — comparable domain, less comprehensive evaluation
- ConceptPrune (avg 5.75, Accept) — training-free editing; ScaPre has broader evaluation and stronger large-scale results
- Growth Inhibitors (avg 6.00, Accept) — concept suppression; ScaPre has stronger multi-concept handling
- Optimal Targets AGE (avg 6.33, Accept) — strong analysis paper; ScaPre offers comparable quality with a different contribution
- Score Forgetting Distillation (avg 6.50, Accept) — different technical approach; similar overall quality

**Narrowing:** ScaPre's empirical margins (10–30x gap on key metrics) and well-targeted method components place it above the mid-6s anchors. The weaknesses are all minor and addressable; none threaten the core contribution. The paper is clearly above the accept threshold for this venue.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>