## Summary

This paper proposes methods for Geodesic Principal Component Analysis (GPCA) on collections of probability distributions using the Wasserstein metric. It introduces an exact GPCA algorithm for centered Gaussian distributions by lifting computations to the space of invertible matrices via the Bures–Wasserstein geometry, and presents GPCAGEN for general absolutely continuous measures by parametrizing geodesics using neural networks based on Otto’s geometric formulation. The work aims to fill the gap for exact GPCA beyond linearized tangent PCA (TPCA), and provides experimental illustrations on synthetic data, weather, MNIST, 3D point clouds, and landscape images.

## Strengths

- **Theoretically well-motivated approach**: The paper carefully builds on the Otto–Wasserstein and Bures–Wasserstein geometries, providing a principled lifting of the GPCA problem to flat spaces (GL_d for Gaussians, diffeomorphisms for general measures). This geometric grounding is a clear strength.
- **Avoids linearization artifacts**: By directly minimizing the GPCA objective without resorting to tangent-space linearization, the method can capture curvature-induced structure that TPCA misses, as demonstrated in the pathological Gaussian example of Figure 4.
- **Flexible parametrization for general measures**: The use of neural networks (MLPs) to represent diffeomorphisms and velocity fields, combined with the Sinkhorn divergence, offers a practical way to handle continuous distributions without needing input-convex networks or discrete approximations.
- **Qualitative interpretability**: The recovered principal components on real datasets (weather clusters, chair/armchair distinction, lamp type variation, brightness/color separation) suggest that the method captures meaningful modes of variation.

## Weaknesses

### Fatal
None.

### Major
1. **Lack of quantitative evaluation against baselines**: The experiments for general a.c. measures are purely qualitative. Although the authors note that a direct numerical comparison with TPCA is “not meaningful,” they do not provide any quantitative metric (e.g., reconstruction error, explained variance, out-of-sample projection error) that would allow the reader to assess whether GPCAGEN actually outperforms simpler alternatives or recovers ground-truth structure better. Without such evaluation, the empirical value of the method remains unsubstantiated.

2. **Overclaiming “exact” GPCA for general measures**: The GPCAGEN method uses Sinkhorn divergence (a regularized approximation of W₂), neural network function approximators, and penalty-based regularization for orthogonality/intersection. These introduce multiple sources of approximation and hyperparameter sensitivity (λ_I, λ_O). Calling the solution “exact” is misleading and undercuts the theoretical rigor claimed in the Gaussian case. The paper should clearly distinguish between an exact formulation and a practically implemented approximation.

3. **Insufficient discussion of computational cost and scalability**: Training separate neural networks for each principal component, estimating Hessian eigenvalues, and computing Sinkhorn divergences repeatedly is likely expensive. The paper provides no timing information, convergence curves, or discussion of how the method scales with data dimension d, number of samples m, or number of components. This makes it difficult to assess the practicality of GPCAGEN for realistically sized problems.

### Minor
- The orthogonality enforcement for the second component in GPCAGEN relies on a regularization term with weight λ_O. The paper does not analyze how the choice of λ_O affects the solution or whether exact orthogonality is achieved in practice. A sensitivity analysis or a measure of the achieved orthogonality would strengthen the claims.
- The MNIST experiment (interpolating digits with color) seems somewhat contrived and does not clearly demonstrate that the method generalizes beyond the constructed example. A more natural dataset of shape variations (e.g., fashion MNIST or EMNIST letters) would be more convincing.
- The paper states that GPCAGEN “operates directly on continuous distributions,” but in practice it uses finite sample batches and the Sinkhorn divergence on empirical measures. The disconnect between the theoretical continuity and the practical discretization is not discussed.

### Trivial
- The abstract repeats the title verbatim, which is unusual and could be shortened.
- Some parts of Figure 1 caption are repeated multiple times (likely a PDF parsing artifact).

## Nice-to-Haves

- A reproducibility statement specifying the hardware, software, random seeds, and number of runs for the experiments would be valuable.
- An ablation study showing the effect of the Sinkhorn regularization parameter ε on the quality of the recovered components.
- A demonstration on higher-dimensional data (e.g., 64×64 images as distributions) to test scalability, or a discussion of limitations in that regime.

## Novel Insights

None beyond the paper’s own contributions. The geometric lifting for GPCA is not entirely new (similar ideas exist in prior work for tangent PCA and for Gaussian distributions), but the paper’s specific combination—using Otto’s parametrization with neural networks to solve the exact GPCA problem for general a.c. measures—is novel. The paper also offers a quantitative link between curvature and the GPCA/TPCA discrepancy for Gaussians (Proposition 4), which provides useful intuition.

## Suggestions

1. Provide a quantitative comparison on a toy dataset where the ground-truth principal geodesic is known (e.g., a set of distributions generated along a known geodesic with added noise). Report the reconstruction error (projection residual) and the angle between the recovered and true geodesic direction.
2. Compare GPCAGEN to a discretized version of TPCA on the same continuous distributions: sample each ν_i to a fixed number of points, run tangent PCA on the discrete OT maps, and compare the resulting principal components (e.g., by projecting the continuous ν_i onto the learned geodesic and computing the sum of squared residuals).
3. Include a convergence plot for the Gaussian GPCA optimization (or mention that it converges reliably) and report wall-clock training time for the GPCAGEN experiments.
4. Clarify in Section 4 that the proposed method yields an *approximate* solution to exact GPCA due to the use of neural networks and Sinkhorn divergence, and discuss the trade-offs relative to an exact solver.

## Score and Decision

The paper addresses an important problem and provides a well-grounded geometric framework. However, the experimental evaluation is insufficient to demonstrate that the proposed method (especially GPCAGEN) is practically effective—quantitative validation is missing, and the claim of “exact” GPCA for general measures is overstated given the approximations involved. The contribution is promising but not yet convincingly validated. I therefore recommend a borderline reject.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>