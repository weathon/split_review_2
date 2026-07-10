Now I'll write the final consolidated review.

## Summary

This paper proposes Controlled Gradient Descent (CGD), a modification to GD's update rule motivated by control-theoretic analysis of a second-order ODE formulation of gradient flow. It analyzes GD stability at the ODE level via Hessian eigenvalue structure and Jordan block theory (Sections 3–5), then attempts to convert the controlled ODE into a discrete algorithm (Section 6). Experiments are conducted on 2D toy losses.

## Strengths

- **The second-order ODE reformulation of gradient flow and the eigenvalue/Jordan-block stability analysis (Sections 3–4) are mathematically clean.** The derivation of d²θ/dt² = -H(θ)·dθ/dt from gradient flow is correct, and the analysis connecting Hessian eigenvalues to Lyapunov vs. unstable behavior through Jordan block structure (zero eigenvalues with vs. without nontrivial blocks) is a valid theoretical contribution at the continuous-time level.

- **The controller design at the continuous ODE level (Section 5) is theoretically sound.** The quadratic eigenvalue problem analysis (Lemma 4, Theorem 3) correctly shows that the controlled second-order ODE is locally asymptotically stable under K₁≻0 and H+K₂≻0, regardless of curvature.

## Weaknesses

### Fatal

- **The derivation from the controlled ODE to Algorithm 1 contains an elementary calculus error.** Equation (5) evaluates ∫θ dt as (1/2)θ² (element-wise square), implying ∫θ(t) dt = θ(t)²/2. This is only true if dθ/dt = 1 — not for a general parameter trajectory θ(t) during training. This invalidates the bridge between the continuous-time theory and the proposed discrete algorithm.

- **Algorithm 1 does not match Equation (5) even on its own terms.** The ODE-derived velocity is dθ'/dt = -∇L - (1/2)K₁θ² - K₂θ. Discretizing this directly (forward Euler) would give the update θ_{t+1} = θ_t - η∇L - η(1/2)K₁θ² - ηK₂θ. However, Algorithm 1 computes θ_{t+1} = θ_t - η∇L + ηK₁θ² + ηK₂θ — the signs on both controller terms are flipped and the K₁ coefficient differs by a factor of 1/2. Consequently, **Theorem 3's stability proof for the controlled ODE does not apply to Algorithm 1**, and the paper's central claim that CGD stabilizes GD is unsupported by the theory it invokes.

### Major

- **No neural network experiments despite claiming "Neural Network Training" in Algorithm 1's title** and being motivated by EoS phenomena observed in real neural networks. All experiments are restricted to 2D toy losses (quadratic ellipses, spheres, quartics). This is insufficient to support claims about stabilizing gradient descent as a practical method.

- **Misclassification of the sphere loss function.** The paper classifies L(θ) = θ₁² + θ₂² as "convex but not strongly convex" (Section 7.1). Its Hessian is 2I (uniformly positive definite), which by the paper's own Lemma 1 makes it **strongly convex**. This factual error mischaracterizes the experimental setting.

### Minor

- **No comparison to standard stabilizing methods.** The paper compares only against vanilla GD, with no baselines such as momentum (which also arises from second-order dynamics), gradient clipping, or adaptive methods — all standard approaches relevant to training stability.

- **No practical guidance for choosing K₁ and K₂.** The theoretical condition K₁≻0 and H+K₂≻0 involves the Hessian, which varies during training, but the paper provides no method for estimating or setting these matrices in practice.

- **The nonlinear θ² term is outside the stability proof.** Even ignoring the derivation error, the stability analysis relies on linearization around equilibrium and does not account for the nonlinear θ² term introduced in Algorithm 1.

### Trivial

- Figure 1's text describes a "divergent trajectory of GD" while the caption states GD "reaches the Optimum (star)" — an internal inconsistency.

## Nice-to-Haves

- Comparing against momentum would be particularly informative since momentum also derives from second-order dynamics.
- If the algorithm derivation were corrected, the resulting method would likely involve momentum-like variables and Hessian-vector products, rather than element-wise parameter squares.

## Removed Points

- "Strongly concave case in Table 1 not supported by evidence": The paper's Theorem 3 claims stability regardless of curvature, which covers the concave case theoretically. The lack of concave experiments is already subsumed by the broader experimental-evidence weakness. Removed as redundant.
- "No statistical significance reported" and "Minimal ablation": These are addressed by the existing weaknesses about experimental scope.

## Novel Insights

The reviews reveal that the paper has two distinct contributions that are disconnected: (1) a valid theoretical analysis of second-order GD dynamics and ODE-level control (Sections 3–5), and (2) a proposed algorithm (CGD) that does not implement the controlled ODE due to a calculus error and sign/coefficient mismatches. The theoretical ODE analysis could potentially be salvaged by re-deriving the discrete algorithm properly (e.g., as a momentum-like system with Hessian-vector products via symplectic or semi-implicit Euler discretization), but the current Algorithm 1 is not supported by the theory it invokes.

## Suggestions

1. Re-derive the discrete algorithm from the controlled ODE by properly discretizing the first-order system [θ; v] dynamics rather than attempting to integrate out the velocity with an incorrect indefinite integral.
2. If claiming relevance to neural network training, include experiments on actual neural networks, even a simple MLP on a standard benchmark.
3. Correct the curvature classification of L(θ) = θ₁² + θ₂² (it is strongly convex) throughout the paper.
4. Include comparisons to momentum and at least one adaptive method or gradient clipping baseline.
5. Provide practical guidance for choosing K₁ and K₂, or acknowledge this as an open problem.

## Score and Decision

The paper presents an interesting theoretical analysis at the ODE level, but the central contribution — the CGD algorithm — is disconnected from this theory by a fundamental derivation error. The stability proofs proven for the controlled ODE do not apply to the algorithm as presented, and the experiments are insufficient to compensate. The paper should not be accepted in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>