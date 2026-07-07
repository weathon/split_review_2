Now I have all the data I need. Let me write the final consolidated review.

---

## Summary

This paper introduces two methods for computing exact Geodesic PCA (GPCA) in the Wasserstein space of probability measures: one for centered Gaussian distributions (leveraging Bures-Wasserstein geometry to lift computations to GL_d) and one for general absolutely continuous measures (GPCAGEN, using a neural parametrization of geodesics via Otto's formulation that avoids input-convex neural networks). The Gaussian contribution is theoretically well-developed (Propositions 3, 4, 5) and quantitatively validated. The GPCAGEN contribution offers an elegant theoretical framing but is evaluated only qualitatively.

## Strengths

- **Strong theoretical grounding of Gaussian GPCA via Bures-Wasserstein geometry (Section 3).** The paper correctly leverages the fiber bundle structure to transform the non-convex geodesic optimization into a tractable form in GL_d. Proposition 3 provides a principled formulation, and Proposition 4 gives a precise quantification of distortion between TPCA and GPCA for same-eigenvalue covariance matrices. These are genuine theoretical contributions.

- **Otto-Wasserstein parametrization for general measures (Section 4).** Parameterizing geodesics via (id + t∇f)_#(φ_#ρ) rather than through McCann's convex function parametrization is a genuinely clever contribution. It avoids the hard-to-train input-convex neural networks (ICNNs) and replaces convexity constraints with monitoring Hessian eigenvalues — a practical insight that is useful beyond GPCA.

- **Proposition 5 (univariate Gaussian closure).** Proving that GPCA stays within the Gaussian family for univariate Gaussians is a clean theoretical result, and the paper is honest about this being an open question in higher dimensions.

## Weaknesses

### Fatal
None.

### Major

- **GPCAGEN experimental evaluation is entirely qualitative.** The paper's headline contribution (GPCAGEN for general a.c. measures, Section 4) is evaluated solely through visual inspection across all experiments. The MNIST geodesic experiment (Figure 5) is described as a "sanity check" where ground truth is known — two orthogonal geodesics with known spatial and chromatic components — yet no quantitative error metric is reported: not the angle between the learned components (should be 90°), not the Wasserstein reconstruction error, not the mean squared error between learned and ground-truth parameters. The 3D point cloud experiments (Figure 6) and landscape image experiments are also purely qualitative. The paper calls these "preliminary experiments" and "illustrations," which is honest but insufficient for a method that stacks Sinkhorn divergence (an approximation of W₂²), Monte Carlo sampling with finite batches, neural network function approximators, approximate eigenvalue bounds for t_min/t_max, and soft regularization constraints. Without any quantitative validation, the reader cannot determine whether the optimization actually solves Eq. (1) or merely produces visually plausible interpolations from a convenient initialization.

- **No quantitative baseline comparison for GPCAGEN.** The paper acknowledges (line 264) that TPCA is the "obvious baseline" but states that "a direct numerical comparison between the two methods is therefore not meaningful" because TPCA acts on discrete measures. The autoencoder+PCA baseline is dismissed as "computationally expensive" without quantitative evidence. This means the paper provides no empirical evidence that GPCAGEN performs comparably to or better than existing approaches on the problems they are designed for. A qualitative comparison in the appendix (Figure 16) showing TPCA "artifacts" on discrete measures does not substitute for a meaningful quantitative comparison — especially since these are different regimes (discrete vs. continuous) and the artifacts are expected.

### Minor

- **Gaussian GPCA results limit practical motivation.** The paper's own experiments (line 208) show GPCA improves cost by <1% over TPCA on average for random Gaussian covariances (100 trials), and the case where they differ substantially (same eigenvalues, different orientations) is described as potentially yielding "undesirable effects" (poor separation, projections at component boundaries). This leaves unclear the practical scenario where Gaussian GPCA would be preferred over the simpler, cheaper TPCA. The paper is transparent about this, but it weakens the narrative that GPCA is the "more geometrically coherent approach" that should replace TPCA.

- **Lack of controlled quantitative experiment with known ground truth for GPCAGEN.** The MNIST experiment has a known ground-truth structure (two orthogonal geodesics with known spatial and chromatic components), yet the paper reports no metrics on how accurately these are recovered. Reporting the angle between learned components, the Wasserstein reconstruction error, or the fraction of variance explained by the first k components would be the most straightforward way to validate the method.

### Trivial
None.

## Nice-to-Haves

- A controlled quantitative experiment on the MNIST synthetic setup reporting reconstruction errors, orthogonality angle, or fraction of variance explained.
- Reporting the objective function value (Eq. 1) for learned GPCAGEN components and comparing to a TPCA baseline on discretized versions of the same distributions.
- Sensitivity analysis with respect to the Sinkhorn parameter ε, batch size m, network architecture, and regularization weights λ_I, λ_O.
- Convergence diagnostics (loss curves, multiple random seeds, solution consistency) and computational cost characterization (training time, scaling with n and d).

## Removed Points

- Weather dataset "no actual result shown": The paper states Figure 14 (in appendix) shows the projection results. REMOVED (factually inaccurate).
- Algorithm 1 ambiguity: The algorithm's loop structure (iterating over i, updating based on each ν_i) is clear standard SGD. REMOVED (not a genuine ambiguity).
- Orthogonality constraint handling: The paper discusses this design choice in detail with explicit rationale (lines 184-196). REMOVED (addressed in paper).
- Missing hyperparameter guidance (Sinkhorn ε, batch size m, learning rate): The paper refers to Appendix E. Per rule on stripped appendix sections. REMOVED.
- Hessian eigenvalue estimation criticism: The paper acknowledges this as an approximation and describes the method. REMOVED (standard implementation detail).
- "Exact" framing criticism: The paper explicitly defines "exact" as "not relying on a linearization of the Wasserstein space" (line 28). The computational approximations are orthogonal to this geometric definition. REMOVED (strawman — paper addresses the concern directly).

## Novel Insights

The most interesting tension in the paper arises from its own Gaussian GPCA results: the method improves cost by <1% over TPCA generically, and the regime where it differs is described as potentially pathological. This means the paper's carefully developed Gaussian theory — while mathematically elegant — does not clearly establish a practical advantage over the simpler existing method. Meanwhile, the GPCAGEN method's Otto parametrization is theoretically principled, but the paper offers no experimental evidence that its complex neural optimization actually recovers correct geodesics or outperforms alternatives. The paper would be substantially strengthened by bridging this gap between theoretical elegance and empirical validation.

## Suggestions

1. Add quantitative evaluation on the MNIST synthetic setup with known ground truth: report the angle between the two learned geodesic components (should be 90°), the Wasserstein reconstruction error per component, and the fraction of variance explained.
2. Report the objective function value (Eq. 1) for all learned GPCAGEN components. Compare to a TPCA baseline on discretized versions of the same distributions, even while acknowledging the limitations of the comparison.
3. Add at least one ablation study showing how solution quality changes with the Sinkhorn parameter ε, batch size m, or regularization weights λ_I, λ_O.
4. Provide basic convergence diagnostics: loss curves over training, solution consistency across random seeds, and computational cost as n and d scale.

## Score and Decision

**Anchors used for calibration (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| HB4lr0ykTi.md (Wasserstein Flow Matching) | 6.33 | R1 | Yes | Similar profile: Wasserstein method with theoretical contribution and experimental concerns. WFM had better experimental validation (quantitative baselines). My paper has stronger theory but much weaker experiments. |
| CrOHzVtWmH.md (Rel-Transl Inv. Wasserstein) | 3.80 | R1 | Yes | Similar weakness profile: lacked quantitative ground-truth experiments. My paper has stronger theoretical contributions. |
| 3P87ptzvTm.md (Optimal Multiple Transport) | 5.00 | R1 | Yes | OT method paper with incremental improvement concerns. My paper has more novel theory but weaker experiments. |
| rY8xdjrANt.md (OT Barycenter via Nonconvex) | 6.20 | R1 | Yes | Theory-practice gap (different algorithms for analysis and implementation). My paper's theory is cleaner but experiments are weaker. |
| mkDam1xIzW.md (Probabilistic Geometric PCA) | 7.33 | R2 | Yes | Geometric PCA on manifolds with proper EM derivation and some quantitative experiments. Better validated than my paper. |
| Uj0h13lVrR.md | 1.00 | R1 | No | Strong reject — not comparable to this paper. |
| 9WG1ga39Dq.md (Consistent OT) | 3.00 | R1 | No | Lower quality, less relevant. |

**Round 1 bracket:** 4.0–6.5. **Narrowing:** Comparison with WFM (6.33), OT Barycenter (6.20), and Probabilistic Geometric PCA (7.33) shows that papers with theoretical contributions but experimental limitations can score 5–7 if they have at least some quantitative validation. My paper lacks this for its headline method. The RW distance paper (3.80) shows the lower bound for papers with similar experimental gaps. My paper has stronger theory, placing it above 3.80.

**Final score:** 5.0. The two major weighted weaknesses (-7.73, -7.38) are heavy enough to substantially pull down the very strong theoretical strengths (+5.60, +5.66). The Gaussian GPCA contribution is well-supported, but the GPCAGEN contribution — presented as the paper's central advance — lacks the quantitative validation needed at ICLR. The paper's theoretical ideas are genuine and the approach is principled, but the experimental evidence does not yet establish that the method works as claimed.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>