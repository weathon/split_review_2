## Summary

This paper introduces SCaSML (Simulation-Calibrated Scientific Machine Learning), a framework that improves pre-trained surrogate models for solving high-dimensional PDEs at inference time without retraining. The core idea is to derive a "Structural-preserving Law of Defect"—a new PDE that exactly describes the error of a surrogate model—and solve it using Multilevel Picard (MLP) Monte Carlo simulation. The authors prove that the final error is bounded by the product of surrogate and simulation errors, and demonstrate 20-80% error reduction on PDEs up to 160 dimensions across multiple surrogate types (PINNs, Gaussian Processes).

## Strengths

- **Novel and well-motivated framework**: The idea of using defect correction to combine the speed of learned surrogates with the rigor of Monte Carlo simulation at inference time is genuinely novel. The connection to inference-time scaling in LLMs provides an intuitive and timely motivation.

- **Theoretical contribution with provable guarantees**: Theorem 2.5 and Corollary 2.6 provide a clean theoretical result showing that the final error is the product of surrogate and simulation errors, yielding an improved convergence rate of O(m^{-γ-1/2+o(1)}). This is a non-trivial and useful theoretical contribution.

- **Strong empirical validation across diverse problems**: The experiments cover linear convection-diffusion, viscous Burgers, Hamilton-Jacobi-Bellman, and diffusion-reaction equations, with dimensions up to 160. The method works with both PINN and GP surrogates, demonstrating versatility. The 20-80% error reduction is practically meaningful.

- **Clear exposition of the core idea**: The derivation of the Structural-preserving Law of Defect (Fact 2.3) is clearly presented, and the warm-up with linear PDEs helps build intuition. The distinction from classical defect correction methods is well-articulated.

## Weaknesses

### Major

1. **Computational cost is not adequately addressed**: The method adds significant runtime (e.g., 13-87 seconds for SCaSML vs. 0.3-3.7 seconds for the surrogate alone in Table 1). The paper frames this as "elastic compute" but does not provide a systematic cost-benefit analysis. For many practical applications, a 10-100x increase in runtime for a 20-80% error reduction may not be worthwhile. The paper needs a clearer discussion of when this trade-off is favorable.

2. **The MLP baseline comparison is misleading**: In Table 1, the "naive MLP" often performs worse than the surrogate alone (e.g., LCD 10d: MLP 2.27E-01 vs SR 5.20E-02). This suggests the MLP implementation may be suboptimal or under-tuned. A fair comparison would require tuning the MLP to a similar computational budget as SCaSML. The current comparison makes SCaSML look better than it might be against a properly tuned pure simulation method.

3. **Limited ablation on the surrogate quality**: The theory predicts that better surrogates lead to better SCaSML performance (product of errors). However, the experiments only show one surrogate quality level per problem. A systematic study varying surrogate accuracy (e.g., training PINNs for different numbers of iterations) and measuring how SCaSML's improvement scales would strengthen the empirical validation of Theorem 2.5.

### Minor

1. **The "first physics-informed inference time scaling framework" claim is overstated**: While the specific combination is novel, the general idea of using Monte Carlo to correct learned PDE solvers has precedent (e.g., control variate methods in stochastic simulation). The paper should more carefully delineate its novelty relative to existing hybrid approaches.

2. **The scaling law verification (Figure 4) is limited**: Only the GP surrogate is shown for the viscous Burgers equation. The empirical verification of the improved scaling law would be stronger with results across multiple problem types and surrogate architectures.

3. **The Hutchinson estimator for Laplacian is mentioned but not analyzed**: The paper uses Hutchinson's method for the HJB problem but notes it caused instability for the diffusion-reaction problem. The conditions under which this approximation is valid and its impact on the theoretical guarantees are not discussed.

### Trivial

- The notation is inconsistent in places (e.g., $\tilde{u}$ is used for both the surrogate and the defect in different sections).

## Nice-to-Haves

- A comparison with other inference-time refinement methods (e.g., iterative solvers, Newton-type corrections) would help contextualize the advantages of the Monte Carlo approach.
- A discussion of the memory footprint of SCaSML vs. the surrogate alone would be useful for practitioners.
- The paper could benefit from a simple 1D or 2D example with visualizations of the defect correction process to build intuition.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the error of a learned PDE solver can be exactly characterized by a PDE of the same structural class as the original problem. This structural preservation is non-trivial and enables the use of established Monte Carlo solvers for the correction step. The observation that the surrogate handles low-frequency components while Monte Carlo efficiently handles high-frequency residuals (due to spectral bias) provides a principled explanation for why the hybrid approach works. The product-form error bound (Theorem 2.5) is a clean theoretical result that quantifies the synergy between learned and simulation-based methods.

## Suggestions

1. Add a systematic ablation study varying surrogate accuracy (e.g., training for different numbers of iterations) and measuring SCaSML's improvement to validate Theorem 2.5 empirically.
2. Include a cost-benefit analysis (e.g., error vs. total compute time) for each problem to help practitioners understand when SCaSML is worthwhile.
3. Tune the "naive MLP" baseline more carefully or use a state-of-the-art MLP implementation for fair comparison.
4. Add a discussion of the limitations: when would SCaSML not help (e.g., when the surrogate is already very accurate, or when the defect PDE is as hard as the original)?

## Score and Decision

The paper presents a novel, well-motivated framework with solid theoretical guarantees and strong empirical results across diverse high-dimensional PDEs. The main concerns are the computational cost trade-off and the fairness of the MLP baseline comparison, but these do not invalidate the core contribution. The paper makes a genuine contribution to the field of scientific machine learning.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>