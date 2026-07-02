Now I have enough calibration. Let me write the final review.

## Calibration Summary

### Anchor Papers Retrieved

**Strong reject band (score < 1.5):** Papers on GFlowNets, scientific discourse visualization, minimax paths, financial networks — all avg 1.0. These are fundamentally flawed or trivial. Our paper is clearly above this band.

**Reject band (1.5-3.5):** Paper on solving unbalanced OT via transform coefficients (avg 2.6), Schrödinger bridge via stochastic action (avg 3.4). Our paper has stronger theory and more rigorous presentation.

**Borderline band (3.5-5.5):** Dynamic Rep of OT via Ensemble Systems (4.0, rejected), Relative-Translation Invariant Wasserstein (3.8, rejected). Our paper has stronger theory but comparable experimental limitations to these.

**Middle band (5.5-7.5):** Wasserstein Flow Matching (6.33, rejected — mixed reviews: 5,8,6), OT Barycenter via Nonconvex Minimax (6.2, rejected), Expected Sliced Transport Plans (6.67, accepted), Wasserstein Proximal (6.0, rejected), Neural Networks on Symmetric Spaces (6.0, accepted). Our paper has comparable or stronger theoretical novelty to most of these, but weaker experimental validation than the accepted ones and some rejected ones.

**Strong accept band (7.5-8.5):** Comparing neural dynamics via OT (8.0, accepted), Flow Matching on General Geometries (8.0, accepted). These have both strong theory and thorough experiments.

### Round 1 bracket
The paper sits between 4.5 and 6.5. The theoretical contribution (Otto fiber bundle lifting for GPCA) is genuinely novel and the Gaussian case is rigorous — pushing it above the 4.0 reject-level papers. However, the complete absence of quantitative validation for GPCAGEN prevents it from reaching the clean accept level of the 6.67 or 8.0 anchors.

### Round 2 narrowing
Comparing against the 6.0-6.33 anchors:
- Wasserstein Flow Matching (6.33, rejected): had quantitative results and baselines but theoretical grounding concerns; our paper has stronger theory but weaker experiments → similar tier
- OT Barycenter (6.2, rejected): theory-practice gap (modified algorithm doesn't match theory) → similar to our GPCAGEN approximation issue
- Neural Networks on Symmetric Spaces (6.0, accepted): comprehensive experiments across diverse benchmarks but more incremental theory → our theory is stronger, experiments weaker

Anchor comparison favors a score of 5.0-6.0. I calibrate at **5.5** — a borderline paper whose theoretical framework is genuinely valuable but whose general-case method (GPCAGEN) lacks the experimental validation needed for acceptance.

---

## Summary
This paper addresses Geodesic PCA (GPCA) in Wasserstein space by lifting the problem from the curved space of probability measures to flat spaces via Otto's fiber bundle formalism. For Gaussian distributions, the lifting goes to GL_d (invertible matrices) enabling a clean optimization. For general absolutely continuous measures, lifting to Diff(Ω) enables neural parametrization of geodesics using MLPs (GPCAGEN) without requiring input-convex neural networks. The paper provides theoretical results (Propositions 3-5) and experiments on both Gaussian and general settings.

## Strengths
- **Principled geometric lifting framework (Sections 3-4).** Reformulating the curved GPCA problem in Wasserstein space as optimization over flat spaces (GL_d for Gaussians, Diff(Ω) for general measures) is mathematically elegant and genuinely novel. The fiber bundle perspective is well-developed with Propositions 1-3 providing the theoretical backbone.
- **Rigorous Gaussian GPCA (Section 3, Propositions 3-5).** The Gaussian case is mathematically complete: the objective is lifted to GL_d (Proposition 3), orthogonality and intersection constraints are handled explicitly (equations 12-13), and the univariate consistency result (Proposition 5) is a nice theoretical contribution. Proposition 4, quantifying the distortion between TPCA and GPCA for same-eigenvalue covariance matrices, is concrete and useful.
- **Otto's parametrization avoids ICNNs (Section 4).** Parameterizing Wasserstein geodesics using arbitrary MLPs for φ and f (rather than input-convex neural networks for u in the McCann formulation) is a practical methodological contribution with potential reuse beyond GPCA. The trade-off (monitoring Hessian eigenvalues instead of enforcing convexity architecturally) is acknowledged.

## Weaknesses

### Major
- **GPCAGEN lacks quantitative validation (Section 5.2).** The paper claims "a preliminary experiment on a synthetic dataset with known geodesics to verify that our algorithm, GPCAGEN, accurately recovers the two first principal components" (line 238) but provides zero quantitative metrics: no recovery error, no optimized objective values before/after training, no convergence curves, and no comparison against any baseline on quantitative metrics. All experiments (MNIST, 3D point clouds, landscape images) are purely qualitative visual interpretations ("the first component captures X, the second captures Y"). The paper dismisses numerical comparison with TPCA as "not meaningful" (line 264) without first establishing that GPCAGEN actually solves the problem it claims to solve. Without any quantitative evidence, the paper has not demonstrated that GPCAGEN works — only that it can learn *some* geodesics that can be visually interpreted post-hoc.

### Minor
- **Gaussian GPCA's practical significance is self-limiting (Section 5.1).** The paper's own experiments show that GPCA and the simpler TPCA differ by less than 1% in the objective for generic Gaussian data (line 208). In the only setting where they differ significantly (same eigenvalues, different orientations), the paper acknowledges GPCA "can yield undesirable effects" and "poor separation" (lines 232, 282). This undercuts the practical value of the Gaussian contribution — the paper does not identify a clear regime where GPCA's extra complexity is beneficial over the much simpler TPCA.
- **GPCAGEN soft constraints are not validated (Section 4, equations 186-192).** The orthogonality penalty 𝒪 involves division by ‖g‖²‖h‖² (numerically unstable when gradient fields have near-zero norm). The intersection penalty ℐ enforces exact matching in Diff(Ω) via a quadratic penalty on ℝᵈ displacements. The paper states λ_I=λ_O=1.0 "works as expected in all experiments" (line 256) but provides no ablation, no sensitivity analysis, and no reporting of whether the constraints are actually satisfied at convergence. For the second component to be meaningful, these constraints must hold.
- **"Exact" framing could mislead for GPCAGEN (abstract, line 28).** The paper qualifies "exact" as "not relying on linearization," which is technically true. However, the practical GPCAGEN implementation replaces W₂² with Sinkhorn divergence S_ε, uses minibatch sampling, enforces diffeomorphism constraints via approximate eigenvalue monitoring over a finite sample set, and uses soft penalties for constraints. The distinction between the ideal problem and the practical approximation could be drawn more carefully to avoid misleading readers unfamiliar with these details.

### Trivial
None.

## Nice-to-Haves
- Report the Sinkhorn regularization parameter ε and discuss its influence on results.
- Include an ablation study of the soft penalty weights λ_I, λ_O.
- Report GPCAGEN's computational cost (number of MLPs, optimization time per experiment).

## Removed Points
- Criticism about missing appendix content (outlier detection experiment in Appendix A.3) — removed per instructions (appendices stripped by parser, exist in original submission).
- Criticism about the projection operator p_{A,X} being an "unacknowledged gap" — removed because the paper explicitly discusses this operator and the necessity of clipping (line 116).
- Criticism about GPCAGEN orthogonality constraints being "stronger than necessary" — speculative, not verified as a concrete problem.
- Generic scope-creep criticisms and broad "the evaluation lacks rigor" framing — removed for lacking specific anchors in the paper.
- Formatting nitpicks about figure descriptions and typos — removed per instructions (parser artifacts, not author errors).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Quantitatively validate GPCAGEN**: (a) Synthetic ground-truth experiment — generate data from a known Wasserstein geodesic, measure angular error between recovered and true geodesic direction as a function of n (number of distributions) and m (samples). (b) Sanity check against Gaussian GPCA — generate Gaussian data and verify GPCAGEN approximately recovers the same components. (c) Report the optimized Sinkhorn-based loss before/after training for all experiments.
2. **Qualify the "exact" label** for GPCAGEN to clearly distinguish the ideal problem formulation from the practical computational approximations.
3. **Report constraint satisfaction** for the second GPCAGEN component — show final ℐ and 𝒪 values at convergence.
4. **Address the Gaussian GPCA tension** — either identify a practical regime where GPCA clearly outperforms TPCA, or reframe the contribution as primarily theoretical.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>