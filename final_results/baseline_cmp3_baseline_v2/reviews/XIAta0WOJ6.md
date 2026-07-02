## Summary

This paper proposes F²SA-p, a class of fully first-order stochastic bilevel optimization methods that use p-th order finite-difference approximations of the hyper-gradient. Under higher-order smoothness assumptions on the lower-level function, the method achieves an SFO complexity of Õ(pε^{-4-2/p}), improving on the best known Õ(ε^{-6}) for first-order smooth problems. The authors also provide an Ω(ε^{-4}) lower bound via a separable construction, showing near-optimality when p is sufficiently large.

## Strengths

- **Novel perspective and clean algorithmic extension:** The paper reinterprets the existing F²SA method as a forward-difference hyper-gradient approximation, which naturally motivates the use of higher-order finite differences. This connection is elegant and leads to a principled family of algorithms (F²SA-p) that seamlessly generalize prior work.

- **Improved complexity under higher-order smoothness:** The Õ(pε^{-4-2/p}) upper bound is a clear improvement over Õ(ε^{-6}) for first-order smooth problems, and the gap shrinks as p grows. This is a non-trivial theoretical advance in stochastic bilevel optimization.

- **Nearly optimal in the highly smooth regime:** The Ω(ε^{-4}) lower bound (matching the single-level SGD lower bound) demonstrates that F²SA-p is nearly optimal up to logarithmic factors when p = Ω(log(1/ε)/log log(1/ε)). This provides a meaningful theoretical benchmark.

- **Tightened analysis for existing methods:** For p=1 the analysis improves the κ dependence from κ^{12} to κ^{11} compared to the best known F²SA analysis. For p=2, Lemma 3.2 tightens a previous Lipschitz bound from O(κ⁶) to O(κ⁵), which is of independent interest.

## Weaknesses

### Major

- **Higher-order smoothness assumption is strong:** Assumption 2.5 requires up to (p+1)-th order derivatives of g and p-th order derivatives of f to be Lipschitz in y. While examples like softmax-based regularizers satisfy this, many practical bilevel problems (e.g., those using neural networks with ReLU activations) do not. The paper acknowledges this but does not discuss how restrictive this assumption is or provide empirical evidence on problems where it fails. The experiments use a logistic regression example (which is smooth) but not a non-smooth one, although a brief MLP experiment is mentioned in the appendix.

- **Experimental validation does not confirm the theoretical rates:** The experiments compare algorithms on a fixed number of iterations (1000) and report final test loss/accuracy. This does not verify the predicted scaling with ε (e.g., different p values should lead to different convergence rates). The advantages of higher p values might be due to better hyperparameter tuning rather than the complexity improvements claimed. A plot of the hyper-gradient norm vs. iterations or cost would be more informative.

- **Per-iteration cost grows with p:** For even p the algorithm solves p lower-level problems per outer iteration; for odd p it solves p+1. While these can be parallelized, the total SFO complexity upper bound Õ(pε^{-4-2/p}) hides a factor p even when the ε dependence dominates. The paper does not discuss the practical impact of this linear scaling on wall-clock time, especially when mini-batches are large.

### Minor

- **Hyper-parameter tuning is complex:** The theoretical parameter choices (Equation 10) involve many constants (ν, η_x, η_y, S, K, T) that depend on unknown problem parameters (κ, σ, L_1, etc.). The paper searches hyperparameters on a log scale, but the practicality of setting these in a black-box manner is questionable.

- **Lower bound construction is fully separable:** The lower bound uses a construction where g(x,y) ≡ g(y) and f is independent of y. This is a valid worst-case instance, but it does not capture the coupling that makes bilevel optimization challenging. A non-separable lower bound that distinguishes bilevel from single-level would strengthen the result.

## Nice-to-Haves

- It would be valuable to test F²SA-p on problems with varying degrees of smoothness (e.g., using a neural network with different activation functions) to understand when higher p helps in practice.
- A comparison of wall-clock time (accounting for parallel execution of inner loops) would help practitioners assess the trade-off between better rates and increased per-iteration cost.
- A discussion or experiment showing the empirical convergence of ‖∇φ(x)‖ as a function of SFO calls for different p would greatly strengthen the empirical validation.

## Novel Insights

Beyond the paper's own contributions, the key insight is that the F²SA family can be viewed through the lens of finite-difference approximation of a derivative with respect to the penalty parameter ν. This observation connects bilevel optimization to classical numerical analysis and opens the door to using higher-order finite-difference formulas (central difference, etc.) to improve the error in hyper-gradient estimation. The proof that the necessary higher-order Lipschitz constants scale polynomially in κ (Lemma 3.2) is technically non-trivial and tightens prior bounds for p=2.

## Suggestions

- For a more convincing empirical evaluation, consider plotting the norm of the hyper-gradient (or a surrogate) versus the number of SFO calls for different p values, using the same initial random seed and standardized hyper-parameter selection.
- Add a discussion (or a figure) on how the total computational cost (including the parallel factor p) translates to wall-clock time, and whether the theoretical gains materialize under practical parallelization constraints.

## Score and Decision

**Score:** 8

**Decision:** Accept