## Summary
This paper tackles the problem of Geodesic Principal Component Analysis (GPCA) in the Wasserstein space of probability measures. It introduces two algorithms: an exact method for centered Gaussian distributions that lifts optimization to the general linear group via the Bures-Wasserstein quotient geometry, and a neural-network-based method (GPCAGEN) for general absolutely continuous measures that parameterizes geodesics using Otto’s formulation. The paper demonstrates the utility of GPCA on several synthetic and real datasets, and provides theoretical results characterizing differences from tangent PCA.

## Strengths
- **Theoretically sound gap-filling.** The paper addresses the problem of exact GPCA in Wasserstein space, which previously lacked a general solution. The lifting to GL_d for Gaussians and the use of Otto’s geometry for general measures are principled and well-motivated.
- **Novel neural parametrization.** GPCAGEN avoids the need for input-convex neural networks by leveraging Otto’s parametrization of geodesics, which is a clever and original way to impose geodesic structure without hard architectural constraints.
- **Clear geometric exposition.** The quotient geometry (Bures-Wasserstein for Gaussians; Otto’s fiber bundle for general measures) is explained in a way that makes the algorithmic construction transparent. The connection between horizontal lifts and geodesic orthogonality is clearly drawn.
- **Theoretical comparison with TPCA.** Proposition 4 quantifies the distortion of linearization, and Proposition 5 shows that GPCA on univariate Gaussians stays in the Gaussian family, which is a useful consistency result.

## Weaknesses
### Fatal
None.

### Major
- **Weak empirical validation for GPCAGEN.** The experiments on general measures are mostly qualitative (visual inspection of geodesic interpolations and projection plots). There is no quantitative metric reported: e.g., reconstruction error, percentage of variance explained, or comparison of final cost values. The orthogonality constraint is enforced via soft penalties, but the paper never reports how well the constraints are satisfied (e.g., final orthogonality angle, intersection distance). Without these, it is hard to judge whether the optimization reliably recovers true principal geodesics.
- **No meaningful quantitative baseline comparison.** The paper correctly notes that TPCA acts on discrete measures and GPCAGEN on continuous measures, making direct numerical comparison “not meaningful.” However, this leaves the evaluation entirely qualitative. The alternative baseline (PCA on latent embeddings) is only briefly dismissed. A proper quantitative baseline (e.g., using a discretized version of GPCAGEN’s output to compare with TPCA on common samples) or a synthetic problem with known ground truth geodesics (beyond the MNIST construction) would strengthen the paper considerably.
- **Hyperparameter sensitivity and computational cost are not discussed.** GPCAGEN depends on several hyperparameters: Sinkhorn regularization ε, batch size m, regularization coefficients λ_I and λ_O, and the method for estimating t_min and t_max via Hessian eigenvalues. The paper sets λ_I=λ_O=1.0 “in all experiments” but provides no ablation or sensitivity study. The cost of computing Hessian eigenvalues for each sample across batches and the effect of approximation errors on the admissible interval are not analyzed.
- **Gaussian GPCA experiments are limited.** The synthetic examples (same orientation, same eigenvalues) are illustrative but the paper only reports average cost improvement over TPCA without showing reconstruction error or component quality on real data beyond the weather dataset (which appears only briefly in the appendix). The claim that GPCA and TPCA “generically yield very similar results” is based on 100 trials; the exact distribution of differences and the standard error are not given.

### Minor
- The paper’s definition of higher-order components (constrained to pass through the intersection of previous components) is standard for GPCA, but the paper does not discuss whether this nested constraint is always appropriate in Wasserstein space, given the non-flat geometry.
- The MNIST experiment constructs two known orthogonal geodesics and verifies that GPCAGEN recovers them. This is a sanity check rather than a discovery experiment; its contribution to demonstrating the method’s utility is limited.

### Trivial
- Figure 1 and Figure 2 contain duplicated captions in the extracted text (likely a parser artifact), which does not affect evaluation.

## Nice-to-Haves
- A synthetic benchmark with known principal geodesics (e.g., mixtures of Gaussians along a prescribed geodesic) where reconstruction error and explained variance can be quantitatively measured.
- An ablation on λ_I, λ_O, and Sinkhorn ε to show how constraint satisfaction and final cost trade off.
- Reporting the final orthogonality angle and intersection distance for the real experiments to demonstrate that constraints are satisfied.

## Novel Insights
The paper’s key insight is that exact geodesic PCA in Wasserstein space can be solved by lifting to the total space of Otto’s fiber bundle, where geodesics become straight line segments. For Gaussians this is computationally tractable; for general measures, the lift makes neural parametrization natural because the horizontal condition (gradients of functions) is easy to enforce. The observation that GPCA and TPCA can differ substantially near the boundary of the SPD cone (and that this difference is governed by the ratio (a-b)/(a+b)) is a concrete geometric lesson.

## Suggestions
1. Add quantitative metrics to the experiments: report the final value of the GPCA objective (equation 1), the orthogonality angle between components, and the average projection cost per data point.
2. Include a synthetic experiment with a known ground truth (e.g., measures lying exactly on a geodesic) to verify that GPCAGEN can recover the correct component and that the cost decreases monotonically with training.
3. Provide a sensitivity analysis for the key hyperparameters (λ_I, λ_O, Sinkhorn ε) or at least justify the chosen values.
4. For the Gaussian case, report the average cost improvement and the standard deviation over many runs, and also show an example where GPCA is worse (e.g., the pathological case where projection clips to boundaries).
5. Elaborate on the weather dataset example in the main paper to give a more complete demonstration of Gaussian GPCA on real data.

## Score and Decision
**Score:** 6  
**Decision:** Accept  

The paper makes a solid theoretical contribution and introduces a novel neural parametrization for an important problem. However, the empirical validation is too weak to support a higher score. With stronger quantitative experiments and sensitivity analysis, the paper could become a strong accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>