## Summary
This paper proposes two algorithms for exact Geodesic Principal Component Analysis (GPCA) in Wasserstein space: one for centered Gaussian distributions by lifting computations to the flat space of invertible matrices GL_d, and another (GPCAGEN) for general absolutely continuous probability measures using neural network parameterization of geodesics via Otto's fiber bundle formulation. The key contribution is solving the exact GPCA minimization problem (equation 1) rather than relying on linearized tangent space approximations (TPCA).

## Strengths
- **Clear identification and filling of a gap**: The paper precisely states that an exact GPCA method for d-dimensional probability measures is missing and provides two concrete algorithms addressing this, with rigorous mathematical grounding.
- **Elegant lifting strategy for Gaussian case**: The Bures-Wasserstein quotient geometry (GL_d → S_d^{++}) is leveraged cleanly in Proposition 3, replacing geodesic optimization with horizontal line segments and explicit projection times—a significant computational and conceptual simplification.
- **Rigorous quantification of GPCA vs TPCA distortion**: Proposition 4 provides an explicit formula showing the distortion ratio depends on |a−b|/(a+b), giving concrete geometric conditions under which linearization fails. The pathological same-eigenvalue circle example (Figure 4) convincingly demonstrates the practical impact.
- **Proposition 5**: Showing that GPCA in the full space of a.c. distributions stays in the Gaussian submanifold for univariate Gaussians is a useful theoretical result confirming the consistency of the Gaussian restriction.
- **Meaningful real-world demonstrations**: The 3D point cloud and landscape image experiments show interpretable modes of variation (chandeliers vs floor lamps, brightness variation), and the synthetic MNIST experiment with known orthogonal geodesics validates the method's ability to recover true components.

## Weaknesses
### Fatal
None.

### Major
- **Lack of quantitative evaluation for GPCAGEN**: The paper acknowledges that direct numerical comparison between GPCAGEN and TPCA "is not meaningful" due to discrete vs continuous setting, but this leaves the general method without any quantitative validation beyond the single synthetic MNIST experiment. The real-world experiments are purely qualitative. Metrics such as variance explained, projection residual values, or reconstruction error comparisons with alternative approaches (e.g., latent-space PCA) would substantially strengthen the empirical claims.
- **No computational cost analysis**: Training two MLPs per component while jointly optimizing n projection times and computing Sinkhorn divergences at each iteration is computationally intensive. No wall-clock times, convergence curves, or complexity analysis are provided. This is a practical concern for adoption.
- **Orthogonality/intersection constraints are soft**: The regularization terms λ_I and λ_O are set to 1.0 uniformly with no ablation. Since these are soft constraints, it is unclear how well they are actually satisfied in practice or how sensitive results are to their values. The paper defers this to the appendix but it is central to the method's correctness for higher-order components.

### Minor
- **Sensitivity to reference measure ρ**: The paper uses ρ = standard Gaussian without discussing how the neural network optimization depends on this choice. While the theory is reference-independent, the practical optimization landscape is not.
- **Higher-order components undeveloped**: The methodology for components beyond the second is mentioned only briefly ("computed similarly"), yet the definition involves increasingly complex intersection constraints that merit more detail and experimental validation.
- **Stronger constraint than needed in Diff(Ω)**: Enforcing ξ₁(t₁) = ξ₂(t₂) in Diff(Ω) rather than only π(ξ₁(t₁)) = π(ξ₂(t₂)) in Prob(Ω) is acknowledged but could miss valid solutions.

### Trivial
None.

## Nice-to-Haves
- A summary table comparing the two proposed methods (scope, computational complexity, key equations) would improve readability.
- Sensitivity analysis for the reference measure choice ρ.
- Convergence diagnostics showing how well the soft intersection/orthogonality constraints are satisfied during training.

## Novel Insights
The paper provides several genuinely novel observations beyond its methodological contributions: (1) the explicit quantification of GPCA-vs-TPCA distortion (Proposition 4) reveals that the eigenvalue ratio |a−b|/(a+b) governs when linearization breaks down, with matrices near the SPD cone boundary suffering the most—this is a valuable guideline for practitioners choosing between the two methods; (2) the demonstration that the first GPCA component need not pass through the Wasserstein barycenter (unlike TPCA which always does by construction) is a striking geometric phenomenon that parallels similar findings in spherical geometry and has practical implications for interpretability; (3) the observation that Otto's parametrization avoids the need for input convex neural networks by working with general smooth functions f (with the convexity constraint handled via Hessian eigenvalue monitoring) opens a practical middle ground between strict architectural constraints and unconstrained parameterization.

## Suggestions
- Add quantitative evaluation metrics for GPCAGEN experiments (projection residuals, variance captured) and comparison with at least one alternative pipeline.
- Report training times and convergence behavior.
- Include an ablation study on regularization coefficients λ_I and λ_O, and report actual intersection distances and orthogonality violations.
- Discuss sensitivity to the reference measure ρ with at least one experiment varying this choice.

## Score and Decision
The paper presents a mathematically rigorous and novel framework for exact GPCA in Wasserstein space. The Gaussian case is elegant with strong theoretical results (Propositions 4 and 5). The general case (GPCAGEN) is promising but lacks the quantitative evaluation needed to fully substantiate its claims. The gap identification is clear, the mathematical framework is coherent, and the experiments are illustrative despite their qualitative nature. The theoretical contributions alone make this a valuable addition to the optimal transport literature.

MY FINAL SCORE: 6.5
MY FINAL DECISION: Accept