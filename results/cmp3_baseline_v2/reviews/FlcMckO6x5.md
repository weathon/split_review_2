## Summary
This paper provides a theoretical and algorithmic framework for separable neural networks (SepNNs). It proves universal approximation theorems for multivariate SepNNs (CP, TT, Tucker forms), characterizes their Neural Tangent Kernel (NTK) regimes under both infinite and fixed rank, and proposes an efficient Separable Preconditioned Gradient Descent (SepPGD) method that alleviates spectral bias with O(nD) complexity for n^D grid samples. Experiments on kernel ridge regression, implicit neural representations, and physics-informed neural networks validate the proposed methods.

## Strengths
- **Comprehensive theoretical analysis**: The paper provides the first universal approximation theorem for multivariate SepNNs beyond the bivariate case, covering CP, TT, and Tucker decompositions with a clean proof using Stone-Weierstrass theorem. This fills an important gap in the literature.
- **Novel NTK characterization**: The derivation of both deterministic (infinite width + infinite rank) and random (infinite width + fixed rank) NTK regimes for SepNNs is technically sound and provides new insights into spectral bias of these architectures. Lemma 1's decomposition of the SepNN NTK into factor MLP NTKs is elegant.
- **Efficient and principled preconditioning**: The SepPGD method is well-motivated theoretically (Lemma 2 showing equivalence to classical NTK-based PGD with Kronecker-structured preconditioners) and achieves dramatically lower computational complexity (O(nD) vs O(n^D) for standard PGD), which is a significant practical contribution.
- **Strong empirical validation**: Experiments across KRR, image/surface representation, and PINNs consistently show SepPGD converges faster than baselines in wall-clock time, and the visual results (e.g., PSNR 33.30 vs 26.48 for SepNN) demonstrate meaningful quality improvements.

## Weaknesses

### Fatal
None.

### Major
1. **Limited novelty of the approximation theory**: While the universal approximation theorem for multivariate SepNNs is new, the proof technique (Stone-Weierstrass + universal approximation of MLPs) is a standard combination. The result, while important to establish, is not surprising given that separable approximations (like tensor decompositions) are known universal approximators for continuous functions. The paper acknowledges that the bivariate case was previously established in (Cho et al., 2023), and the extension to D>2 using CP/TT/Tucker is incremental.
2. **The SepPGD algorithm's practical advantages are overstated**: The complexity comparison in Table 1 (O(nD) vs O(n^D)) is valid only when the preconditioner is applied exactly as described. However, in practice, the SepPGD requires computing M_d (Equation 8), which involves outer products of dimensionality n^{D-1}. The paper acknowledges this in footnote 3 but dismisses it as "orders of magnitude less expensive." For D≥3, this term dominates and the true complexity is O(n^{D-1} + nD), not purely O(nD). A more precise complexity analysis is needed.
3. **The connection between SepPGD and spectral bias alleviation is not rigorously proven beyond D=2**: Lemma 2 only establishes equivalence for D=2. The paper states "it is believed that the result... can be readily extended to multivariate cases D>2" but provides no proof or sketch. Similarly, the claim that SepPGD "provably adjusts the NTK spectrum" is only argued heuristically for the D=2 case. For a paper claiming provable alleviation, this gap is significant.

### Minor
1. **Limited comparison with non-NTK preconditioning methods**: The paper only compares SepPGD against MSK (itself an NTK-based method) and standard gradient descent. There are many other preconditioning techniques (e.g., Adam, L-BFGS, KFAC) that are widely used for INRs and PINNs. The absence of these comparisons makes it unclear whether SepPGD's advantage is specific to the NTK-based approach or could be achieved with simpler optimizers.
2. **The experimental setup for PINNs is limited**: The paper tests only three PDEs (diffusion, Klein-Gordon, Helmholtz) on grid samples. Real-world PINN applications often involve complex geometries, non-grid collocation points, and coupled PDE systems. The paper does not demonstrate how SepPGD performs in these more realistic settings.
3. **Scalability of eigenvalue decomposition for factor NTKs**: The preconditioner construction requires eigenvalue decomposition of D n×n matrices, which is O(D n^3). While this is better than O(n^{3D}) for standard PGD, for large n (e.g., >10^4), this becomes prohibitive. The paper does not discuss approximations (e.g., random sketching, Lanczos) that would be needed for truly large-scale applications.

### Trivial
- The paper uses "stochasticity among factors" in the introduction when it likely means "expressivity" or "interaction."
- Figure 1's caption is duplicated (appears three times on page 4).

## Nice-to-Haves
- Analysis of how SepPGD interacts with different activation functions (the experiments use mostly ReLU/tanh; sine activations are common for INRs).
- A convergence theorem for SepPGD in the NTK regime (similar to how (Geifman et al., 2024) provides one for standard PGD).
- Ablation study on the rank R and its effect on SepPGD's effectiveness.

## Novel Insights
The key insight is that the separable structure of SepNNs enables a factorization of the preconditioning problem: instead of constructing one large n^D × n^D preconditioner, the SepPGD constructs D small n × n preconditioners for each factor network. This is possible because the NTK of a CP SepNN decomposes additively over dimensions (Lemma 1), and the Kronecker structure of grid data allows the preconditioner application to be computed efficiently via tensor operations. This observation bridges the gap between NTK-based preconditioning (which is computationally prohibitive for multidimensional problems) and separable architectures (which are efficient but suffered from spectral bias).

## Suggestions
1. Provide a more precise complexity analysis for SepPGD that separates the cost of constructing M_d (O(n^{D-1} R)) from the actual gradient computation (O(nD)).
2. Add experiments with Adam/L-BFGS baselines for fairness, and show for a subset of experiments that SepPGD is not simply inheriting gains from any preconditioning.
3. Include a theoretical or empirical analysis for D>2 (or at minimum for D=3) to substantiate the claim that Lemma 2 extends.
4. Add a discussion of when n is too large for O(D n^3) eigenvalue decomposition to be feasible, and suggest practical approximations.

## Score and Decision

### Score: 6.5 (borderline accept)

The paper makes solid theoretical contributions (universal approximation, NTK regimes for SepNNs) and proposes a practically motivated algorithm with clear efficiency advantages. The weaknesses—overstated O(nD) complexity claim, limited proof for D>2 cases, and narrow experimental comparisons—are substantial but not fatal. The paper contributes new knowledge to the community (NTK characterization of SepNNs, efficient preconditioning for separable architectures) and the results are reproducible. However, it falls short of the standard for a strong accept due to the gap between the claimed theoretical guarantees (especially for D>2) and what is actually proven.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>