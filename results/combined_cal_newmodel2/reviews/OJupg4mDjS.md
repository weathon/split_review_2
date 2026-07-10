Now I have all the data I need. Let me compile the final review.

**Round 1 bracket:** Based on the calibration search, the paper sits between the 3.5-5.5 band. The most directly comparable anchors are "Relative-Translation Invariant Wasserstein Distance" (3.80), "Intrinsic Riemannian Classifiers on SPD Manifolds" (5.00), and "Probabilistic Geometric Principal Component Analysis" (7.33). All of these papers have quantitative experimental validation, which the current paper's main method (GPCAGEN) completely lacks.

**Narrowing to final score:** Compared to the RW paper (3.80), which has theoretical contributions + algorithmic contributions + quantitative experiments (even if limited), our paper has stronger theory but zero quantitative results for the main method. The RW paper's most negative weakness items (favorability -1.01, -0.74) are less severe than our paper's most negative items (favorability -2.30, -3.03). This places our paper below 3.80. Compared to the SPD classifiers paper (5.00), which has extensive quantitative experiments across multiple benchmarks, our paper is much weaker empirically. A score of 3.5 reflects: strong theory that prevents a 1-2 score, but a fatal empirical gap that prevents a 4+ score.

---

## Summary

This paper tackles Geodesic PCA (GPCA) in Wasserstein space, proposing two algorithms: one for Gaussian distributions using a GL_d lifting (Sections 2–3) and one for general absolutely continuous measures using neural-network-parametrized Otto geodesics (GPCAGEN, Section 4). The Gaussian derivation is mathematically clean, and the Otto parametrization avoiding input-convex neural networks is a practical contribution. However, the paper's central empirical claim—that GPCAGEN solves the GPCA problem—is supported entirely by qualitative visualizations with no quantitative metrics, baselines, or controlled validation. This is a decisive evidential gap for a method paper.

## Strengths

- **Mathematically principled lifting to GL_d for Gaussian GPCA (Proposition 3).** The exploitation of the quotient geometry S_d^{++} = GL_d / O_d to convert geodesic optimization into a Euclidean problem in the total space is clean and correct. The resulting formulation (equation 12) is well-suited for numerical optimization, and Proposition 3 is a sound theoretical contribution.

- **Proposition 4 quantifies TPCA distortion in a non-zero-curvature setting.** The expression showing distortion grows with (a−b)/(a+b) for same-eigenvalue, different-orientation covariance matrices is a concrete, interpretable theoretical result that gives genuine insight into when tangent linearization fails.

- **Proposition 5 resolves a nontrivial question for univariate Gaussians.** Showing that univariate GPCA restricted to the Gaussian submanifold gives the same result as GPCA in the full a.c. space closes a natural gap in the literature.

- **Otto parametrization avoids ICNNs (equation 9).** Using the id + t∇f formulation instead of input-convex neural networks is a practical contribution that eliminates hard architectural constraints at the cost of monitoring Hessian eigenvalues. This expands the toolset for Wasserstein-geometry learning.

## Weaknesses

### Major

- **GPCAGEN has no quantitative evaluation.** The paper's central empirical claim—that the neural algorithm solves the GPCA problem—is supported only by qualitative visualizations (Figures 5, 6, 7). The paper mentions a synthetic experiment "with known geodesics" (line 238) but reports no reconstruction error, variance-explained fraction, geodesic recovery accuracy, or final loss values. For a method paper proposing a novel neural-network-based algorithm, this is a decisive evidential gap: the reader cannot assess whether the method converges reliably, recovers known ground-truth geodesics, or satisfies orthogonality constraints.

- **No meaningful quantitative baseline comparison for GPCAGEN.** The paper dismisses a direct comparison with TPCA as "not meaningful" (line 264) and mentions an autoencoder+PCA baseline without reporting any numbers (line 268). Neither standard Euclidean PCA on sample embeddings, nor TPCA on discretized measures, nor the GPCA algorithm restricted to Gaussian approximations is quantitatively compared. Without baselines, the experiments cannot demonstrate that GPCAGEN provides any advantage over simpler approaches.

### Minor

- **The Gaussian GPCA experiments undercut rather than support the claimed contribution.** The paper reports (line 208) that GPCA improves over TPCA by less than 1% on average for generic covariance matrices. In the only case where they differ substantially (same eigenvalues, different orientations), the paper states that "GPCA may be seen as worse-behaved than TPCA" (line 232). The paper never resolves this tension: it neither identifies a realistic scenario where the GPCA-specific solution is preferable nor reframes the contribution accordingly.

- **The "exact" label is imprecise for GPCAGEN.** The paper defines "exact" as not relying on linearization (abstract, line 28), which is fair for the Gaussian algorithm. But GPCAGEN uses Sinkhorn divergence (an entropically regularized approximation of W₂²), minibatch sampling, finite-capacity MLP function approximation, and approximate Hessian eigenvalue estimation from finite samples. Calling this "exact" is misleading; it is a neural approximation of the exact GPCA problem and should be described as such.

- **The Hessian eigenvalue monitoring (Algorithm 1, line 5) addresses only a pointwise sufficient condition for invertibility of id + t∇f at sampled points, but the actual condition for being a diffeomorphism is global (injectivity), which eigenvalue positivity alone does not guarantee.** Additionally, eigenvalues estimated from minibatch samples may not capture the true spectral extremes of the learned function. These limitations are acknowledged in passing but their implications for the reliability of the learned geodesics are not discussed.

### Trivial

None.

## Nice-to-Haves

- Report runtime and scalability information for GPCAGEN, which requires training MLPs with 4×128 hidden units, computing second-order derivatives for Hessian eigenvalues, and running Sinkhorn per iteration for each data point.
- Acknowledge the gap between the pointwise Hessian eigenvalue condition (which is sufficient but not necessary) and the global diffeomorphism condition.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Missing Sinkhorn ε, batch size m, and λ sensitivity analysis:** The paper explicitly states these details are in Appendix E, which is stripped by the parser. Removed per rule that parser-stripped appendix content should not be flagged as missing.
- **Missing optimization details for Q_i ∈ SO_d:** Paper defers to Appendix D.2. Removed for same reason.
- **Critique about unfair comparison favoring baselines:** Not applicable; asymmetry (if any) favors baselines, not the author's method.
- **Missing related work on Seguy & Cuturi 2015 acknowledgment:** Minor citation precision point that does not affect core claims.
- **Generic formatting/style nitpicks:** Removed per rule.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Quantitative validation on controlled synthetic data.** Create a dataset where true principal geodesics are known (e.g., by interpolating between two known distributions along a true Wasserstein geodesic, then perturbing). Report angular error between recovered and true geodesics, RMS Wasserstein distance between recovered and true distributions along each component, and the final loss value. This single experiment would directly validate the core claim.

2. **Report convergence and constraint-satisfaction metrics:** orthogonality measure ⟨∇f₁, ∇f₂⟩_{L²(ρ)} after training, final Sinkhorn divergence values, and standard deviation across random initializations.

3. **Resolve the Gaussian GPCA tension** by either (a) identifying a realistic use case where the GPCA-specific solution is genuinely preferable to TPCA, or (b) reframing the contribution: exact GPCA provides a computational framework that validates TPCA as a good approximation in most settings, rather than positioning "exact" as inherently superior.

## Score and Decision

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>