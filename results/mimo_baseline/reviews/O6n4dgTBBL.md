## Summary

This paper reformulates gradient descent as a second-order ODE derived from gradient flow, analyzes its stability under different curvature conditions (strongly convex, convex but not strongly convex, concave), and proposes a control-theoretic controller term that guarantees local asymptotic stability. The controller is then converted into a modified gradient descent algorithm (CGD) with an additional gradient guidance term, validated on low-dimensional synthetic problems.

## Strengths

- **Systematic stability taxonomy across curvatures:** The paper provides a clear classification (Table 1) of when the second-order ODE formulation of GD is Lyapunov stable, unstable, or asymptotically stable, organized by curvature regime. The Jordan form analysis in Sections 4.2.1–4.2.3 is technically correct and well-presented.

- **Clean application of quadratic eigenvalue problem theory:** The use of Lemma 4 (Tisseur & Meerbergen, 2001) to establish asymptotic stability of the controlled system via the QEP structure Q(λ) = λ²I + λ(H+K₂) + K₁ is elegant and correct, given the stated assumptions on K₁ and K₂.

- **Clear exposition and organization:** The paper follows a logical progression from motivation → preliminaries → analysis → controller design → algorithm → experiments, making it easy to follow the technical development.

## Weaknesses

### Fatal

- **Incorrect derivation of Algorithm 1 from the controlled ODE (Equation 5):** The paper derives the discrete algorithm by "integrating" the controlled second-order ODE. Specifically, it claims that ∫θ(t)dt = (1/2)θ(t)², which is mathematically incorrect. The integral ∫θ(t)dt is the antiderivative of θ with respect to time and cannot be simplified to (1/2)θ² without assuming dθ/dt = θ (i.e., θ(t) = θ₀e^t), which does not hold in general. This error invalidates the entire derivation of Algorithm 1 from the control-theoretic formulation. The paper's central narrative—that a theoretically motivated controller on the second-order ODE yields a principled algorithm—breaks down at this step. Algorithm 1 is effectively an ad-hoc modification (adding -K₁θ² - K₂θ to the gradient) without valid theoretical backing from the ODE analysis.

### Major

- **Second-order ODE analysis does not directly characterize GD stability:** The second-order ODE d²θ/dt² = -H(θ)·dθ/dt is obtained by differentiating the first-order gradient flow, which enlarges the state space to include arbitrary initial velocities. The gradient flow itself is constrained to dθ/dt = -∇L(θ). For example, continuous-time gradient flow on convex functions always converges, yet the paper's second-order analysis finds instability—this is an artifact of the reformulation, not a property of GD. The paper does not establish that instability of the second-order system implies instability of the original gradient descent dynamics, undermining the motivating claims.

- **Continuous-time analysis with discrete-time algorithm:** All theoretical guarantees are for continuous-time dynamics, while Algorithm 1 is a discrete iterative method. The paper acknowledges this gap in the limitations but does not address it. The stability threshold η < 2/sharpness is fundamentally a discrete-time phenomenon (as noted by Cohen et al., 2021), yet the paper's analysis operates entirely in continuous time where no such threshold exists.

- **Experiments limited to 2D toy problems:** All experiments use simple 2D quadratic and quartic functions. There are no experiments on neural networks, standard ML benchmarks, or any problem with more than 2 parameters. This severely limits the evidence for practical relevance, especially since the θ² term in Algorithm 1 could behave very differently in high-dimensional, non-convex settings.

### Minor

- **The -K₁θ² term in Algorithm 1 is unusual and potentially problematic:** This element-wise squared term acts as a non-convex regularizer (contributing a cubic term K₁θ³/3 to the effective loss). For negative parameter values, this creates a repulsive force away from zero, which is counterintuitive for regularization. The paper does not discuss or justify this behavior.

- **Choosing K₂ requires Hessian knowledge:** Definition 4 requires H(θ) + K₂ ≻ 0 for all θ, which in practice requires knowledge of the Hessian's spectral properties. Remark 2 suggests K₂ = k₂I but does not specify how to choose k₂ to satisfy the condition, especially for non-convex losses where H can have arbitrary negative eigenvalues.

### Trivial

- Minor notation inconsistency: the paper uses both λ for eigenvalues of the Jacobian J and λ_i for eigenvalues of the Hessian H, which can cause confusion in Section 4.

## Nice-to-Haves

- A discrete-time stability analysis that directly characterizes when the proposed Algorithm 1 converges, with explicit conditions on η, K₁, K₂.
- Experiments on at least one neural network training task to demonstrate practical viability.
- A comparison with existing stabilization methods like SAM, gradient clipping, or momentum-based methods.

## Novel Insights

The observation that the second-order ODE reformulation of gradient flow reveals different stability properties depending on curvature (with convex-but-not-strongly-convex being unstable due to Jordan block structure) is an interesting theoretical observation. However, its relevance to actual gradient descent behavior is questionable given the gap between the second-order ODE and the original first-order dynamics. The eigenvalue-shifting mechanism of the controller (replacing H with H+K₂ and adding K₁) is a standard control-theoretic technique rather than a novel insight specific to optimization.

## Suggestions

- Fix the derivation in Equation 5. If the goal is to derive a practical algorithm, either (a) work directly in discrete time from the start, or (b) use a proper discretization of the controlled ODE (e.g., via symplectic integrators or careful Euler discretization with stability analysis).
- Clearly distinguish between properties of the second-order ODE and properties of gradient descent. The paper's claims about GD instability in convex settings should be carefully qualified.
- Replace the θ² term with a better-motivated modification, or provide stronger justification for why this particular form arises from the control framework.

## Score and Decision

The paper presents an interesting high-level idea of applying control theory to stabilize optimization, and the stability analysis of the second-order ODE is technically sound. However, the fatal error in deriving Algorithm 1 from the controlled ODE (incorrect integration in Equation 5) invalidates the paper's core contribution. Combined with the significant gap between the continuous-time second-order analysis and the discrete algorithm, and experiments limited to 2D toy problems, the paper is not ready for acceptance.

MY FINAL SCORE: <score>2</score>
MY FINAL DECISION: <decision>Reject</decision>