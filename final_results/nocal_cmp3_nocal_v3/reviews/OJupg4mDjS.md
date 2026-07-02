## Summary

This paper addresses Geodesic Principal Component Analysis (GPCA) in Wasserstein space, proposing two algorithms: one for centered Gaussian distributions (lifting the problem from \(S_d^{++}\) to \(GL_d\) via Bures-Wasserstein quotient geometry) and a more general algorithm called GPCAGEN for absolutely continuous probability measures (using Otto's parametrization of geodesics with MLP-parameterized diffeomorphisms and scalar functions). The Gaussian case is theoretically well-grounded and supported by experiments; the general case is methodologically novel but lacks convincing quantitative validation.

## Strengths

- **Clear identification of a genuine gap.** The paper correctly observes that exact GPCA (equation 1) in Wasserstein space has not been solved for higher-dimensional absolutely continuous measures. Prior work either linearizes (TPCA), handles only 1D (Bigot et al. 2017; Cazelles et al. 2018), or replaces geodesics with generalized geodesics (Seguy & Cuturi 2015). The gap is real and well-articulated (Section 1, Related Works).

- **Elegant Gaussian formulation.** The lifting of the GPCA problem from \(S_d^{++}\) to \(GL_d\) (Proposition 3, Section 3) is mathematically principled. Replacing the Bures-Wasserstein distance with the Frobenius norm on horizontal subspaces is a clean application of known quotient geometry, and the optimization over \(SO_d\) variables is explained clearly. Proposition 4 (quantifying TPCA/GPCA distortion under equal eigenvalues) is a nice theoretical result.

- **Clever parametrization for the general case.** Using Otto's parametrization (Proposition 2) to represent geodesics as \((\text{id} + t\nabla f)_\#(\varphi_\#\rho)\) with \(f\) not required to be convex is a genuine methodological insight. This avoids input convex neural networks (ICNNs), which are known to be restrictive, while maintaining the ability to enforce the diffeomorphism constraint via Hessian eigenvalue monitoring.

## Weaknesses

### Fatal

None.

### Major

- **GPCAGEN lacks quantitative evaluation on real data.** The paper's headline algorithm for general a.c. measures is evaluated almost entirely through visual inspection and qualitative interpretation. For the 3D point cloud experiments (chairs, lamps) and landscape images: (i) no value of the GPCA objective (equation 1) is reported, so there is no evidence that the learned geodesics minimize the claimed criterion; (ii) no quantitative metric (e.g., projection cost, explained variance, classification accuracy on the learned components) is provided; (iii) claims that a component "captures the distinction between hanging lamps and standing lamps" or "reflects variations in thickness" are visual interpretations, not measurements. The paper needs quantitative evidence that GPCAGEN actually solves the problem it claims to solve.

- **No quantitative comparison to baselines.** The paper explicitly states (Section 5.2, "Baselines") that "A direct numerical comparison between the two methods is therefore not meaningful" regarding TPCA, but does not attempt any quantitative comparison. The GPCA objective (equation 1) could be evaluated for both TPCA's and GPCAGEN's components using a common evaluation framework (e.g., evaluating both methods' components on the same discrete approximations, or using Sinkhorn divergences uniformly). Similarly, the "PCA on latent vectors" baseline mentioned in the appendix is dismissed without quantitative comparison. Without such comparisons, there is no evidence that GPCAGEN improves on, matches, or even approximates the correct solution of the GPCA problem.

### Minor

- **The term "exact" is potentially overclaimed for GPCAGEN.** The abstract defines "exact" as "not relying on a linearization of the Wasserstein space." However, GPCAGEN involves multiple approximations: Sinkhorn divergence \(S_\varepsilon\) replacing \(W_2^2\) (entropic bias), MLP parametrization of \(\varphi\) and \(f\) (limited expressivity — arbitrary diffeomorphisms cannot be guaranteed), mini-batch sampling, approximate eigenvalue computation from \(m\) samples, and soft regularization penalties for orthogonality and intersection (hard constraints are not enforced). While the paper specifies what it means by "exact," the cumulative approximations make this label potentially misleading. The Gaussian GPCA (Section 3) legitimately earns the "exact" descriptor because the lifting to \(GL_d\) with the Frobenius norm is theoretically equivalent; the two cases should be more carefully distinguished.

- **No ablation or sensitivity analysis for GPCAGEN hyperparameters.** The regularization coefficients \(\lambda_I\) and \(\lambda_O\) are set to 1.0 in all experiments with no sensitivity study. The achieved orthogonality (value of the inner product in \(\mathcal{O}\)) and intersection error (value of \(\mathcal{I}\)) are never reported, so there is no diagnostic evidence that the key geometric constraints (orthogonal intersection of components) are actually satisfied. An ablation showing the effect of removing either term would strengthen the paper considerably.

- **The Gaussian experiments somewhat undercut the practical motivation for GPCA.** On random covariance matrices, GPCA improves on TPCA by "less than 1%" on average (Section 5.1). In the pathological case where GPCA and TPCA differ substantially (same eigenvalues, different orientations), the paper admits GPCA "may be seen as worse-behaved as TPCA, as some of the Gaussian distributions will project onto the first geodesic component boundaries, yielding a poor separation." This raises a question about practical value that the paper does not resolve.

### Trivial

- The MNIST experiment embeds images into \(\mathbb{R}^4\) by adding artificial color channels — a non-standard representation. Standard image distributions (e.g., pixel intensities as a 2D density) would be more informative.
- The synthetic experiment mentioned in Section 5.2 ("We conduct a preliminary experiment on a synthetic dataset with known geodesics...") is referenced in the main text without any cross-reference to results or an appendix figure, making it impossible for the reader to assess.

## Nice-to-Haves

- A runtime or convergence analysis for GPCAGEN would be helpful, as the method involves training two MLPs with Sinkhorn divergences per data point.
- A discussion of the Sinkhorn regularization parameter \(\varepsilon\) and its effect on the bias-variance tradeoff would improve reproducibility (currently deferred to the appendix).
- A brief discussion of whether local minima are a concern for the non-convex GPCA objective (equation 15) would be informative.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"The synthetic experiment results do not appear anywhere"** — REMOVED: results may exist in the appendix (which is stripped by the parser). The main text mentions the experiment was conducted, and the paper states experiments are deferred to appendices.
- **"The weather dataset experiment lacks quantitative cluster analysis"** — REMOVED: subsumed by the broader criticism about lack of quantitative evaluation; Figure 14 is in the appendix.
- **"Sinkhorn ε is not discussed"** — REMOVED: deferred to Appendix E per the paper's stated organization.
- **"No runtime or convergence analysis"** — MOVED to Nice-to-Haves (not a standard requirement for this type of paper).
- **"No discussion of the unimodality/multimodality of the GPCA objective"** — REMOVED: speculative; non-convexity is implicit from the MLP parametrization.
- **"Hessian eigenvalue monitoring could miss out-of-sample violations"** — REMOVED: speculative concern not demonstrated with evidence.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report the GPCA objective value (equation 1) achieved by GPCAGEN on each real dataset. Compare it to the value achieved by TPCA's components evaluated under the same metric (e.g., using a discrete approximation of the geodesics or a consistent evaluation framework).

2. Complete and report the synthetic experiment with known ground-truth geodesics, including recovery error between learned and true components.

3. Report the achieved orthogonality (value of \(\mathcal{O}\)) and intersection error (value of \(\mathcal{I}\)) for the second components on each dataset. Without this, it is unclear whether the second component is meaningfully orthogonal.

4. Run a sensitivity analysis on \(\lambda_I\) and \(\lambda_O\) for at least one dataset, showing how the objective value, orthogonality, and intersection error trade off.

5. Distinguish the exactness claims more carefully between the Gaussian case (truly exact lifting to \(GL_d\)) and GPCAGEN (approximate but not linearized).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>