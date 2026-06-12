## Summary

This paper introduces SCaSML (Simulation-Calibrated Scientific Machine Learning), a framework that improves pre-trained surrogate models for solving high-dimensional PDEs at inference time without retraining. The core idea is to derive a "Structural-preserving Law of Defect"—a new PDE that exactly describes the error of a surrogate model—and solve it using Multilevel Picard (MLP) Monte Carlo simulation. The authors prove that the final error is bounded by the product of surrogate and simulation errors, and demonstrate 20-80% error reduction on PDEs up to 160 dimensions using PINN and Gaussian Process surrogates.

## Strengths

- **Novel and well-motivated framework**: The idea of using defect correction to combine machine learning surrogates with Monte Carlo simulation at inference time is genuinely novel. The connection to inference-time scaling in LLMs provides an intuitive and timely motivation, and the separation of training (global approximation) from inference (targeted refinement) is practically appealing.

- **Theoretical guarantees**: The paper provides a rigorous convergence analysis showing that SCaSML achieves a faster convergence rate than either the surrogate or the Monte Carlo solver alone (Theorem 2.5, Corollary 2.6). The error bound being the *product* of surrogate and simulation errors is a clean and insightful result that formalizes the intuition behind the method.

- **Strong empirical validation**: Experiments span multiple challenging high-dimensional PDEs (up to 160 dimensions) with different surrogate types (PINN, GP), consistently showing error reduction. The inclusion of inference-time scaling studies (Figure 3b) and empirical verification of the improved scaling law (Figure 4) strengthens the claims.

- **Clear exposition of the core idea**: The derivation of the Structural-preserving Law of Defect is presented clearly, starting from the linear case and extending to semi-linear PDEs. The explanation of why Monte Carlo is well-suited for correcting the high-frequency residual left by spectral bias is insightful.

## Weaknesses

### Major

1. **Computational cost comparison is incomplete and potentially misleading**: The paper reports that SCaSML achieves lower errors than the surrogate, but at significantly higher computational cost (e.g., 13.31s vs 0.45s for LCD 10d, 61.82s vs 1.74s for VB-GP 20d). The key question is whether the same computational budget spent on training a larger/better surrogate or running more Monte Carlo samples directly would yield comparable or better results. The "elastic compute" argument is interesting, but the paper does not provide a fair comparison where total compute (training + inference) is held fixed. The claim that "a smaller base PINN can outperform a larger PINN under the same inference-time compute budget" is mentioned but not rigorously demonstrated with controlled experiments.

2. **Limited comparison to alternative hybrid approaches**: The paper compares SCaSML against the surrogate alone and a naive MLP solver, but does not compare against other natural baselines such as: (a) using the surrogate as a control variate in standard Monte Carlo, (b) training a larger surrogate with the same total compute, (c) ensemble methods, or (d) other inference-time refinement techniques like iterative PDE-constrained optimization. Without these comparisons, it's difficult to assess whether the specific defect-correction formulation is essential to the gains.

3. **Practical applicability concerns**: The method requires computing the residual of the surrogate model (which involves second-order derivatives of the neural network) and then running a full MLP simulation. For high-dimensional problems, computing the Hessian or even Hutchinson estimates of the Laplacian can be expensive. The paper acknowledges this for the diffusion-reaction equation (full Laplacian needed), but does not systematically analyze the computational overhead of computing the residual versus the simulation itself.

### Minor

4. **The "inference-time scaling" analogy is somewhat stretched**: While the paper draws inspiration from LLM inference-time scaling, the mechanism is fundamentally different. LLM inference scaling involves chain-of-thought reasoning or search, whereas SCaSML runs a separate Monte Carlo simulation. The analogy is useful for motivation but the paper could more clearly delineate the differences.

5. **Limited analysis of when the method might fail**: The method relies on the surrogate being reasonably accurate (Assumption 2.4). If the surrogate is very poor, the defect PDE may have large source terms, making the MLP simulation expensive or unstable. The paper does not discuss failure modes or provide guidance on when the method is beneficial versus when it's better to just run Monte Carlo directly.

6. **The MLP implementation details are relegated to the appendix**: While this is acceptable for a conference paper, the main text could benefit from a more self-contained description of how the MLP solver is adapted to the defect PDE, particularly how the modified nonlinearity $\tilde{F}$ is evaluated in practice.

### Trivial

7. The paper uses the notation "SCa²SM¹" inconsistently (sometimes "SCaSML"), which is a minor formatting issue.

## Nice-to-Haves

- A controlled experiment where total compute (training + inference) is held fixed, comparing SCaSML against training a larger surrogate or running more Monte Carlo samples directly.
- Comparison against a simple control variate baseline where the surrogate is used as a control variate in standard Monte Carlo.
- Analysis of the computational breakdown: what fraction of time is spent computing the residual vs. running the MLP simulation?
- Discussion of adaptive compute allocation: how to decide how many Monte Carlo samples to use at inference time for a given query.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the error of a machine-learned PDE solver satisfies a PDE of the *same structural form* as the original problem. This structural preservation is non-trivial and enables the use of existing Monte Carlo solvers for the correction step. The observation that the residual error inherits the high-frequency characteristics that Monte Carlo handles well (due to spectral bias of neural networks) provides a principled explanation for why the hybrid approach works. The product-form error bound is also a clean theoretical contribution that formalizes the intuition that a better surrogate makes the correction step easier.

## Suggestions

1. Add a controlled experiment comparing SCaSML against a larger surrogate trained with the same total compute budget (training + inference). This would directly address the "elastic compute" claim.
2. Include a baseline where the surrogate is used as a control variate in standard Monte Carlo, to isolate the benefit of the defect-correction formulation.
3. Provide a computational cost breakdown (e.g., pie chart) showing time spent on: (a) computing surrogate residual, (b) MLP simulation, (c) other overhead.
4. Discuss conditions under which SCaSML may not be beneficial (e.g., very inaccurate surrogate, very smooth solutions where spectral bias is not an issue).

## Score and Decision

The paper presents a novel, well-motivated framework with theoretical guarantees and strong empirical results on challenging high-dimensional problems. The main weakness is the lack of fair computational cost comparisons against alternative approaches, which makes it difficult to fully assess the practical significance of the method. However, the core idea is sound, the theory is rigorous, and the empirical results are convincing within the scope of the comparisons provided. The paper makes a genuine contribution to the field of scientific machine learning.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>