## Summary

This paper analyzes the stability of gradient descent from a continuous-time, control-theoretic perspective. The authors formulate GD as a second-order ODE, show that its stability depends on the curvature of the loss function (stable only under strong convexity), and propose a controller term that guarantees local asymptotic stability regardless of curvature. The controller is implemented as a gradient guidance term, and experiments on low-dimensional synthetic problems demonstrate that the proposed Controlled Gradient Descent (CGD) stabilizes training and tolerates larger learning rates compared to standard GD.

## Strengths

- **Novel perspective on GD stability**: Framing gradient descent as a second-order dynamical system and analyzing stability via the eigenvalues of the linearized system's Jacobian is a creative and potentially insightful approach. The paper correctly identifies that the sign structure of Hessian eigenvalues directly impacts stability, and the connection to control theory is well-motivated.
- **Clear theoretical claim with strong contrast**: Theorem 3 and Table 1 present a clear, unambiguous theoretical result: the proposed controller guarantees local asymptotic stability even when GD is only Lyapunov stable (strongly convex) or unstable (convex but not strongly, concave). This is a mathematically precise claim that, if correct, would constitute a genuine contribution.
- **Empirical validation on synthetic problems**: The experiments (Figures 1–3) convincingly show that on the tested low-dimensional objectives, CGD converges while GD oscillates or diverges. The ablation on controller hyperparameters (k1, k2) shows robustness within the tested range, which is a practical strength.

## Weaknesses

### Fatal

**1. The derivation from the continuous-time controller to the discrete-time algorithm (Equation 5 and Algorithm 1) is mathematically incorrect, invalidating the core algorithmic contribution.**

The paper defines the controller in the continuous-time second-order system (Eq. 4) as u = -K1θ - K2(dθ/dt). To implement this in discrete gradient descent, the authors attempt to "recover the gradient dθ'/dt by taking an integration" and arrive at:

dθ'/dt = dθ/dt - (1/2)K1θ² - K2θ   (Equation 5)

This is wrong in two ways:
- The integral of -K1θ with respect to t is not -(1/2)K1θ². The integral ∫θ dt is not (1/2)θ²; that would be the integral of θ with respect to θ, not with respect to time t. This conflates integration over time with differentiation with respect to θ.
- Even if the integration were performed correctly, there is no principled justification for treating the resulting "dθ'/dt" as the new gradient to be used in a discrete Euler step. The mapping from a continuous-time controlled ODE to a discrete optimizer is a discretization problem, not an integration problem.

Because Algorithm 1 is the paper's main deliverable, this error is fatal. The algorithm does not implement the controller that was proven to be stable, so the central claim ("our controlled gradient descent stabilizes training") is not supported by the analysis.

**2. The experimental evaluation only tests cases where the Hessian is diagonal, isotropic, or has simple structure (2D ellipses, spheres, quartics), which is insufficient to validate the algorithm for general non-convex, non-smooth landscapes that the paper claims to address.**

The paper explicitly states in the abstract and introduction that the goal is to handle "general loss function of neural network" and "various curvature setting." However, the experiments are limited to three quadratic objectives with at most 2 parameters. There is:
- No experiment on a non-convex function (all tested losses are convex)
- No experiment with more than 2 parameters
- No experiment on a neural network or any realistic deep learning task
- No comparison to existing stabilizers (e.g., momentum, Adam, gradient clipping, spectral normalization)

The paper claims "Empirical evaluations on synthetic problems confirm our controlled gradient descent improves stability, tolerates larger learning rates, and converges more reliably than standard GD." This claim is vastly over-extrapolated from the evidence.

### Major

**3. The continuous-time analysis of GD stability (Theorem 2) contains inconsistencies and does not address the known stability results from discrete-time analysis.**

The paper claims that GD is unstable for "convex but not strongly convex" and "concave" cases. However, it is well-established that gradient descent on a convex (but not strongly convex) function like θ₁² + θ₂² with a sufficiently small learning rate converges (e.g., Nesterov, 2013). The paper's instability conclusion arises from the continuous-time 2nd-order reformulation, which introduces an extra zero-eigenvalue Jordan block that does not exist in the discrete GD dynamics. The authors acknowledge in the Limitations section that "a gap remains between continuous-time differential equations and the actual discrete gradient descent updates," but this is a severe gap: the instability they claim for convex functions is an artifact of their reformulation, not a property of GD.

**4. The central experimental result (Figure 3) contains a critical contradiction with the paper's own Table 1 and Theorem 2.**

For the convex sphere loss L(θ) = θ₁² + θ₂² (sharpness = 2), Table 1 says GD is "unstable" (X). Yet Figure 3(a) shows GD converging at η=0.99 (below the stability threshold), and Figure 3(b) shows GD converging at η=1.0 (at the threshold). The only case where GD diverges is η=1.01 (Figure 3(c)), which is above the classical 2/sharpness bound. This contradicts the paper's claim that GD is unstable for convex functions even *below* the stability threshold. The actual behavior is consistent with the well-known discrete analysis: GD is stable for η < 2/sharpness, unstable otherwise.

### Minor

**5. The related work discussion omits key connections.** The paper does not discuss Gradient Flow in the context of dissipative Hamiltonian systems, nor does it connect to Polyak's heavy-ball momentum (which also modifies the second-order dynamics). The pseudo-Hessian or modified loss perspective is not explored.

**6. The notational inconsistency in the integration step (Equation 5) between vector derivatives and element-wise squares is confusing.** The expression θ² is defined as element-wise square, but K₁ is a matrix; K₁θ² is not a standard operation. This sloppiness suggests the derivation was not carefully checked.

### Trivial

None beyond those already noted.

## Nice-to-Haves

- If the derivation can be corrected, it would strengthen the paper to show that CGD is equivalent to or closely approximates an existing known optimizer (e.g., adding a quadratic penalty to the loss, which would make the corrected algorithm a proximal method or a regularized GD).
- Extending the empirical evaluation to at least one small-scale neural network (e.g., a 2-layer MLP on MNIST) would significantly improve the paper's practicality claims.

## Novel Insights

None beyond the paper's own contributions, because the claimed contributions contain a fatal error. The idea of analyzing GD stability via second-order ODEs is not new (the paper itself cites related work that does this), and the proposed algorithm is not correctly derived from the analysis.

## Suggestions

1. **Fix the derivation in Section 6.** The mapping from the controlled ODE to the discrete update rule must be done via a correct discretization (e.g., using a numerical integrator like the symplectic Euler method or the Lie-Trotter splitting), not by an erroneous integration. If the algorithm cannot be derived correctly, the paper should either present the algorithm as a *heuristic* motivated by the continuous analysis (and state this explicitly) or reformulate the controller directly in the discrete setting.

2. **Address the gap between continuous and discrete stability.** The paper should either prove that the controlled ODE's stability implies stability of the discretized algorithm under some conditions (e.g., small enough step size), or acknowledge that the continuous analysis is only a proxy and cannot guarantee discrete stability.

3. **Expand experimental validation.** At a minimum, test on a non-convex function (e.g., the Rosenbrock function or a non-convex quadratic with indefinite Hessian) and on a higher-dimensional problem (e.g., d=10, 50). Include comparison to momentum, Adam, and gradient clipping.

## Score and Decision

This paper proposes an interesting theoretical framing but Fatal Weaknesses 1 and 2 undermine both the algorithmic contribution and the empirical claims. The core derivation from the controlled ODE to the proposed algorithm is mathematically incorrect, and the experiments do not support the claimed generality. Without a corrected derivation and substantially broader empirical validation, the paper cannot be accepted.

MY FINAL SCORE: <score>1</score>
MY FINAL DECISION: <decision>Reject</decision>