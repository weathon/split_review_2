## Summary

This paper introduces TD-JEPA, a zero-shot unsupervised RL method that uses a temporal-difference latent-predictive loss to learn state and task encoders, a policy-conditioned predictor, and latent-space policies from offline reward-free data. The key algorithmic innovation is replacing the Monte Carlo latent-prediction loss (which requires on-policy rollouts) with a TD bootstrapping loss that can be estimated from static offline datasets. The paper provides theoretical analysis (under idealizations) connecting the learned representations to successor measure factorization, and evaluates the method across 13 datasets in ExoRL and OGBench.

## Strengths

- **The TD-based latent-predictive loss (Eq. 9) is a genuine algorithmic innovation.** The insight that Bellman bootstrapping makes multi-step policy-conditioned latent prediction compatible with off-policy offline data is clearly motivated (Section 3.1, from Eq. 5 to Eq. 7/9), and addresses a real gap: prior latent-predictive methods require on-policy rollouts (Eq. 5) or are limited to single-step / behavioral-policy assumptions.

- **The theoretical analysis (Theorems 1–4) is substantial for this subfield.** It establishes gradient-matching connections between the latent-predictive loss and successor measure approximation losses, provides a non-collapse guarantee (Theorem 2), and derives a policy evaluation error bound (Theorem 4) that connects to zero-shot RL. While idealized, this goes beyond what most representation-learning-for-RL papers offer.

- **The empirical evaluation is broad and well-structured:** 13 datasets across locomotion, navigation, and manipulation, with both proprioceptive and pixel observations, organized to answer distinct questions (zero-shot comparison, prediction-target ablation, symmetric vs. asymmetric encoders, fast adaptation). The probability-of-improvement analysis (Figure 2) is a useful complement to per-suite averages.

- **TD-JEPA's advantage in pixel-based domains is clear and meaningful.** On DMC_RGB (628.8 ± 5.5), it substantially outperforms the next-best BYOL-γ* (582.4 ± 9.8). Learning from pixels is the harder setting, and showing a decisive advantage there is the paper's strongest empirical result.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The theoretical guarantees and the practical algorithm operate under meaningfully different conditions, and the paper does not discuss how robust the results are when assumptions are violated.** Theorems 1–4 assume a tabular setting with orthonormal representations (A1: φᵀφ = ψᵀψ = I), uniform state distribution (A2), and symmetric transition matrices (A3). Theorem 2's non-collapse guarantee additionally requires a "continuous-time relaxation" where optimal predictors are computed *before* each gradient step on the representations (line 161) — fundamentally different from the simultaneous SGD in Algorithm 1. The paper acknowledges these are idealizations ("for an idealized version," line 34; "simplified tabular setting," line 140) and notes the assumptions are standard in related work (line 157), but it never discusses what happens under joint SGD training or when assumptions are violated. The practical algorithm's mechanisms for avoiding collapse may differ from the theoretical story.

2. **The headline empirical advantage is concentrated in pixel-based DMC; the "matches or outperforms" framing in the abstract is broader than the full results support.** On OGBench_RGB, BYOL-γ* (41.58) ties or slightly exceeds TD-JEPA (41.34). On OGBench proprioception, FB (39.04) and HILP (37.98) match or exceed TD-JEPA (37.98). The paper's own discussion (line 271: "TD-JEPA is only slightly preferable to FB and HILP from proprioception") is more measured. A method that excels in the harder pixel regime is still valuable, but the abstract's wording could more accurately reflect that the advantage is concentrated in that setting.

3. **The asymmetric encoder (distinct φ and ψ) provides at best marginal benefits, yet Section 3.2 invests a full subsection motivating the design.** Figure 3 (right) and the text (line 287) concede this variant "performs comparatively rather well" and the advantage is only "more often than not." If the asymmetric architecture is not clearly beneficial, the method's core contribution reduces to the symmetric TD loss (Eq. 7). This does not weaken the paper, but the presentation over-invests in a design choice with weak empirical support.

4. **Several baselines (BYOL*, BYOL-γ*, ICVF*) were re-implemented with novel zero-shot wrappers designed by the authors.** The paper is transparent about this (line 251), and the comparison with standard zero-shot methods (FB, HILP, Laplacian, RLDP) is unaffected. However, the combination of author-designed wrappers, added improvements (explicit state encoders, line 277), and hyperparameter tuning by the proposing authors creates potential for unknown asymmetries. The paper does not report whether the tuning budget per baseline was equal or whether the re-implemented baselines' results were validated against published numbers.

### Trivial
None.

## Nice-to-Haves
- Reporting training-time compute (GPU hours, wall time) and comparison with baselines would aid practical adoption.
- A sensitivity analysis for the orthonormality regularization coefficient λ and latent dimensionalities d_φ, d_ψ would increase confidence in the method's robustness.
- Testing the theory's predictions on small tabular domains (e.g., measuring successor measure reconstruction error) could validate the theoretical connection or reveal where it breaks.

## Removed Points
These points are flagged to be removed; treat them with caution.

- **Claim about "existing methods are typically limited to single-task, one-step, or on-policy" (line 9) being misleading for FB**: The paper uses "typically," not "all." FB is discussed in the same paragraph and in Related Work as a contrastive multi-policy method. No misrepresentation. (Strawman)
- **Eq. 9 vs. Eq. 7 notation difference**: The notation change from φ(s') target (Eq. 7) to ψ(s') target (Eq. 9) is a natural consequence of the asymmetric design described in the text. (Formatting nitpick)
- **λ hyperparameter not discussed in main text**: Implementation details in the appendix are standard practice for this field. (Reproducibility nitpick)
- **OGBench BC regularization not described in main text**: The paper cites the source and points to the appendix (line 249). (Already addressed by paper)
- **Action-dependence of theory**: The paper explicitly states the simplification (line 140): action-conditioned transitions are replaced with policy-conditioned ones. (Misunderstands paper)
- **Compute cost**: Reasonable suggestion but not a weakness. (Moved to Nice-to-Haves)

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Explicitly delineate what the theory guarantees about the idealized objective versus what is hypothesized about the practical algorithm. This would strengthen credibility without weakening the contribution.
2. Recalibrate the abstract to state directly that TD-JEPA's strongest and most consistent advantages are in pixel-based domains, and that it is broadly competitive (rather than uniformly superior) in proprioceptive settings.
3. Report the symmetric (shared encoder) variant as a simpler default, and reposition the asymmetric design as an optional extension with modest expected benefit.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>