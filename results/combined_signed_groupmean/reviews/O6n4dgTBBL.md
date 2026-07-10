Now let me write the final review.

## Summary

This paper proposes a control-theoretic framework for analyzing gradient descent, formulating GD as a second-order ODE and proving stability/instability under different Hessian curvature regimes (Theorem 2). It introduces a controller u = -K₁θ - K₂(dθ/dt) designed to stabilize the continuous second-order ODE (Theorem 3), then attempts to convert this controller into a discrete algorithm (Algorithm 1) that adds -K₁θ² - K₂θ terms to the gradient. Experiments are conducted on three 2D toy problems.

## Strengths

- **Novel framing.** Formulating gradient descent dynamics as a second-order ODE and applying control-theoretic stability analysis (Lyapunov stability via linearization, quadratic eigenvalue problems) is a genuinely non-standard perspective. The connection between Hessian eigenvalues and the Jacobian eigenvalues of the second-order system (Section 4.2) is a clean observation that could, if properly developed, offer fresh insight into GD stability.

- **Continuous-time ODE analysis is internally consistent.** The mathematical analysis of the continuous second-order ODE (Theorem 2's classification under different Hessian definiteness conditions, and Theorem 3's stability proof for the controlled ODE via the quadratic eigenvalue problem (Lemma 4)) is correctly executed for the continuous system. Under the stated conditions (K₁≻0, H+K₂≻0), the conclusion that the controlled second-order ODE is locally asymptotically stable follows from standard theory.

## Weaknesses

### Fatal

- **The derivation from the continuous-time controller to the discrete algorithm (Equation 5) contains a basic calculus error that invalidates the bridge between theory and algorithm.** The paper claims that ∫θ dt = ½θ², but ∫θ(t) dt is not equal to θ(t)²/2 in general (this would require dθ/dt = 1, which is never stated or justified). Therefore, Algorithm 1 — which adds a -K₁θ² - K₂θ term to the gradient — does not actually implement the controller whose stability was proven in Theorem 3. The paper analyzes one system (continuous controlled ODE with linear feedback u = -K₁θ - K₂θ̇) and implements a different one (discrete update with a quadratic θ² term). The central advertised contribution — a theoretically grounded stabilized GD algorithm — is not supported by the mathematics presented. (Verified at line 224: `dθ'/dt = ... = dθ/dt - ½K₁θ² - K₂θ`.)

### Major

- **The experimental example labeled "convex but not strongly convex sphere" (L(θ) = θ₁² + θ₂²) is actually strongly convex.** Its Hessian is diag(2, 2) = 2I, which is positive definite. By the paper's own Lemma 1, this makes the function strongly convex. The paper claims to validate stability across "strongly convex," "convex (not strongly)," and "concave" regimes (Table 1), but all three toy examples (ellipse, sphere, quartic) fall in the strongly convex family. No experiment is conducted on a genuinely non-strongly-convex or concave function, so the core theoretical claim about different curvature regimes (Theorem 2) is empirically unvalidated. (Verified at lines 269, 271.)

- **The experimental validation is far too weak to support the paper's claims.** Despite being titled "Controlled Gradient Descent for Neural Network Training" (Algorithm 1) and claiming "higher tolerance on learning rate," the experiments are limited to three 2D synthetic functions with at most 100 iterations. There are no neural network experiments, no comparisons to standard optimizers (SGD with momentum, Adam, RMSprop, normalized GD, or SAM), and no results on any benchmark dataset. The learning-rate tolerance claim is demonstrated only on a single 2D quadratic problem. For a paper presenting a practical algorithm, this constitutes a severe evidence gap.

- **The novelty claim is overstated.** The paper states (Section 1.1): "To date, no theoretically characterized algorithm exists that guarantees stabilized convergence of GD in general setting." This is inaccurate — momentum methods (Polyak heavy ball, Nesterov acceleration), normalized gradient descent, gradient clipping, and adaptive methods all provide convergence guarantees under various general settings. The paper also does not discuss the relationship between its -K₂θ damping term and classical momentum, which similarly adds a parameter-dependent term to stabilize dynamics. (Verified at line 36.)

### Minor

- **The paper analyzes a continuous ODE (gradient flow) and draws conclusions about discrete GD without a rigorous discretization analysis.** While the paper acknowledges this gap in Section 8, it nevertheless proceeds to treat continuous results as if they directly imply discrete behavior (e.g., the abstract's claim that GD "can diverge even in simple convex settings" is supported only by continuous ODE analysis and toy experiments). No discrete stability analysis or rate analysis is provided.

- **The quartic loss L(θ) = θ₁⁴ + θ₂⁴ has a degenerate Hessian at the minimum** (H = 0 at θ=0, since ∂²/∂θ²(θ⁴) = 12θ²), making the linearization at equilibrium entirely zero. The local Jacobian analysis from Theorem 2 does not directly apply to this degenerate case, which the paper does not discuss.

- **The ablation study on controller hyperparameters is extremely limited**, testing only three values (k₁=k₂=0.05, 0.1, 0.2) with K₁=K₂ always. This provides minimal insight into the sensitivity of the method to the two hyperparameters independently.

### Trivial

None.

## Nice-to-Haves

- Replace Equation 5 with a properly justified discretization of the controlled second-order ODE (e.g., via symplectic or implicit Euler integration), or directly analyze a discrete control law from the start.
- Add at least one genuinely non-strongly-convex example (e.g., L(θ) = θ₁² with a flat second dimension) and one genuinely concave example.
- Validate on at least one practical neural network task with comparisons to standard optimizers.
- Tone down the novelty claim about "no theoretically characterized algorithm exists."

## Removed Points

These points from the input review were removed after verification against the paper:

- **Criticism about missing appendix / code / reproducibility details**: REMOVED — the appendix is removed by the parser, not omitted by the authors.
- **Concern about "no error bars or multiple trials"**: REMOVED — not a standard expectation for 2D toy problems.
- **Concern about the Jordan block analysis needing more detailed verification**: REMOVED — the reviewer acknowledged this is standard mathematics.
- **Claim about the sphere (η=0.995) experiment being inconsistent with theory**: REMOVED — the paper describes "slow convergence or marginal instability" (not outright instability), and (1-2η) = -0.99 is technically oscillatory convergent.
- **Criticism about not comparing to momentum as a separate point**: MERGED into the overstated novelty weakness.
- **Computational cost not discussed**: REMOVED — the reviewer acknowledges it's negligible O(d).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. The Equation 5 derivation error is structural, not cosmetic. Fixing it requires either: (a) deriving the discrete update from the controlled ODE via a valid numerical integrator (e.g., symplectic Euler) and analyzing the resulting discrete stability, or (b) abandoning the claim that Algorithm 1 is theoretically grounded in the control analysis and repositioning the paper as a purely empirical method with separate analysis.
2. Correctly classify all experimental functions and include at least one genuinely non-strongly-convex and one genuinely concave case.
3. Validate the method on at least one neural network task (e.g., MNIST with a small MLP or CNN) with comparisons to standard optimizers.

## Score and Decision

**Bracketing (Round 1)**: The fatal mathematical error (-10.00 impact) places the paper in the 1.0–3.5 reject range. The interesting framing (+7.10) prevents a strong-reject (1) score, but the severity of the error keeps it below the typical reject (3).

**Narrowing (Round 2)**: The closest anchor is 1NYhrZynvC ("Exact linear-rate gradient descent," avg 2.50), which has a similar pattern of a mathematical derivation error combined with insufficient experiments. Our paper's framing strength (+7.10 vs. that anchor's max +0.51) provides a modest upward nudge, but the fatal error is decisive.

**Final placement**: The paper's continuous ODE analysis is mathematically sound, and the control-theoretic framing is genuinely novel. However, the bridge from theory to algorithm (Equation 5) contains a basic calculus error that invalidates the central advertised claim. The score 2.5 reflects a paper with an interesting idea but a fatal flaw in core execution.

MY FINAL SCORE: <score>2.5</score>
MY FINAL DECISION: <decision>Reject</decision>