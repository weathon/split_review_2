## Summary

This paper addresses the problem of Geodesic Principal Component Analysis (GPCA) on collections of probability measures using the Wasserstein metric. It proposes two exact GPCA algorithms: one for centered Gaussian distributions that lifts computations to the space of invertible matrices via the Bures-Wasserstein geometry, and another for general absolutely continuous measures (GPCAGEN) that parametrizes geodesics using neural networks based on Otto's Riemannian structure. The methods are demonstrated on synthetic examples, weather data, MNIST, 3D point clouds, and landscape images.

## Strengths

- **Novel theoretical framework for exact GPCA**: The paper provides a principled lifting of the GPCA problem to the total space of Otto's fiber bundle, both for Gaussians (Proposition 3) and general measures (Proposition 2). This avoids the distortion inherent in tangent-space linearization and yields true geodesic components.
- **Neural network parametrization without convexity constraints**: GPCAGEN uses Otto's parametrization to represent geodesics via arbitrary smooth functions, avoiding the need for input-convex neural networks. The Hessian eigenvalue monitoring is a practical way to enforce the diffeomorphism condition.
- **Theoretical analysis of TPCA vs GPCA distortion**: Proposition 4 quantifies when linearization fails, showing that distortion is largest for covariance matrices near the boundary of the SPD cone. This provides useful guidance for practitioners.
- **Diverse experimental validation**: The paper tests on multiple domains (Gaussian covariances, MNIST, 3D point clouds, images) and shows that GPCAGEN recovers interpretable modes of variation that align with intuitive structure (e.g., chair vs armchair, brightness variation).

## Weaknesses

### Fatal
None.

### Major
- **Overclaimed "exact" nature of GPCAGEN**: The paper repeatedly claims to solve the "exact" GPCA problem, but the neural network approach relies on several approximations: Sinkhorn divergence instead of true Wasserstein distance, finite-sample estimation of Hessian eigenvalues, and regularization-based enforcement of orthogonality. The method is approximate, and this should be clearly stated.
- **Insufficient quantitative evaluation**: The experiments are almost entirely qualitative. There is no quantitative comparison to baselines (e.g., TPCA, linearized Wasserstein PCA) on metrics such as reconstruction error, explained variance, or downstream task performance. The paper dismisses direct numerical comparison with TPCA as "not meaningful" without justification. For a method paper, rigorous quantitative validation is essential.
- **No discussion of computational cost or scalability**: The neural network approach requires training MLPs and estimating Hessian eigenvalues at each iteration. The paper does not report training times, convergence behavior, or how the method scales with dimension or number of data points. This limits practical assessment.

### Minor
- **Orthogonality constraint via regularization**: The second component uses regularization terms with coefficients λ_I and λ_O, set to 1.0 in all experiments. There is no ablation study on these hyperparameters, and the regularization does not guarantee exact orthogonality. The sensitivity of results to these choices is unexplored.
- **Limited baseline comparison for GPCAGEN**: The only baseline shown (TPCA in Appendix A.2) is qualitative and uses discrete measures, which the paper argues is not directly comparable. However, alternative baselines such as autoencoder-based PCA or kernel PCA on distributions are not considered.

### Trivial
- The paper mentions "outlier detection" in Appendix A.3 but does not describe the experiment in the main text.

## Nice-to-Haves

- A quantitative comparison on a synthetic dataset with known ground-truth geodesics, reporting reconstruction error or variance explained for both GPCA and TPCA.
- An ablation study on the regularization coefficients λ_I and λ_O to show robustness.
- A discussion of limitations, particularly the computational cost and the approximate nature of the neural network approach.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the Otto-Wasserstein geometry provides a natural framework for GPCA that avoids the need for convex functions in geodesic parametrization. The connection between the Bures-Wasserstein geometry and the horizontal lift to GL_d is elegantly exploited to turn a non-convex optimization over geodesics into a more tractable problem. The observation that GPCA and TPCA can differ dramatically for covariance matrices near the boundary of the SPD cone (Proposition 4) is a valuable caution for practitioners using tangent-space methods.

## Suggestions

- Clarify in the abstract and introduction that GPCAGEN is an approximate method, not exact, due to the use of Sinkhorn divergence and finite-sample Hessian estimation.
- Add a quantitative experiment on a synthetic dataset where the true geodesic components are known, comparing reconstruction error of GPCAGEN and TPCA.
- Report training time and convergence behavior for the neural network approach, and discuss scalability to higher dimensions or larger datasets.

## Score and Decision

**Score**: 6

**Decision**: Accept

The paper makes a solid theoretical contribution by providing a principled framework for exact GPCA in Wasserstein space, with a novel neural network parametrization that avoids convexity constraints. The experimental validation is diverse but lacks quantitative rigor, which prevents a higher score. The overclaim of "exact" is a concern but does not invalidate the core contribution. The paper is well-written and addresses an important problem in geometric data analysis.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>