## Summary

This paper proposes Controlled Gradient Descent (CGD), which adds a control-theoretic correction term (−K₁θ² − K₂θ) to the standard GD update. The authors formulate GD as a second-order dynamical system, analyze its stability under different curvature regimes (strongly convex → Lyapunov stable; convex-but-not-strongly → unstable; concave → unstable), design a controller that guarantees local asymptotic stability for the continuous-time controlled ODE, and attempt to derive a discrete algorithm from this controller. Experiments are conducted on 2D synthetic functions.

---

## Strengths

- **The core observation is genuinely interesting.** The paper correctly identifies that in the continuous-time second-order formulation (Eq. 2), GD dynamics are at best Lyapunov stable (never asymptotically stable) under strong convexity, and unstable under weaker convexity assumptions. This is a non-trivial observation that existing convergence analyses do not foreground.

- **Theorem 3 (and Lemma 4) is mathematically correct in the continuous-time setting.** Given the controlled second-order ODE with K₁ ≻ 0 and H+K₂ ≻ 0, the quadratic eigenvalue problem implies all eigenvalues have negative real parts, hence local asymptotic stability of the controlled continuous-time system.

- **The framing of stability types (Lyapunov vs. asymptotic) is a useful lens** for thinking about GD convergence. Distinguishing between "stays near the optimum" and "actually converges to the optimum" is conceptually valuable and connects cleanly to control-theoretic machinery.

---

## Weaknesses

### Fatal

- **The derivation from the controlled ODE to the algorithm (Section 6, Equation 5) contains a genuine mathematical error.** The paper writes: ∫u dt = –(1/2)K₁θ² – K₂θ where u = –K₁θ – K₂·dθ/dt. Computing the time integral gives ∫u dt = –K₁∫θ(t) dt – K₂θ(t). The claim that ∫θ(t) dt = (1/2)θ(t)² is not a general identity — it confuses the time integral ∫θ(t) dt with the parameter-space integral ∫θ dθ. This means the proposed algorithm (Algorithm 1: g_t = ∇L(θ_t) – K₁θ_t² – K₂θ_t) does **not** follow from the theoretical controller design. The paper's central claim — that CGD is *derived from* control-theoretic stabilization — is unsupported. Without this bridge, the paper offers an ad-hoc algorithm alongside a theory that applies to a different system, not to the discrete update being proposed.

### Major

- **The experimental test functions are misclassified relative to the paper's own curvature definitions.** (a) L(θ)=θ₁²+θ₂² (line 271) is labeled "convex but not strongly convex sphere" but has Hessian 2I ≻ 0, which by the paper's own Lemma 1 makes it **strongly convex**. (b) L(θ)=θ₁⁴+θ₂⁴ (line 259) is labeled "strongly convex quartic" but its Hessian diag(12θ₁², 12θ₂²) is zero at the minimum θ*=0, so it does NOT satisfy ∇²L ≽ mI for any m>0 and is not strongly convex. The experiments therefore do not actually test the instability patterns predicted by Theorem 2 for the claimed curvature classes; the mapping from theory to experimental validation is broken.

- **The empirical evaluation is extremely limited** — only 2D synthetic functions with full-batch GD. There are no experiments on neural network training (even small-scale), no stochastic mini-batch experiments, no comparison to any existing stabilization method (momentum, Adam, weight decay, etc.). The paper claims to "stabilize gradient descent" and have "higher tolerance on learning rate" but provides essentially no empirical validation beyond trivial toy cases. This is a severe evidential gap for a paper presenting a new optimization algorithm.

### Minor

- **The continuous-time stability analysis does not directly support the discrete-time claims about learning-rate tolerance.** The paper claims CGD "increases the 2/sharpness threshold" but the eigenvalue analysis is in continuous time and does not formally imply convergence bounds for discrete GD with a specific step size η. The paper acknowledges this discretization gap in the limitations section, but the empirical claims about learning-rate tolerance go beyond what the theory supports.

- **The "variational interpretation" promised in the abstract** is never provided or explained anywhere in the paper body.

- **The ablation study (Section 7.1) only tests k₁ = k₂**, so it does not demonstrate the independence of the two hyperparameters — they could have compensating effects.

### Trivial

- Line 124 states the system is "unstable if the loss function L is convex but not strongly concave" — this is a typo; the corresponding Section 4.2.3 is about the **concave** case.

---

## Removed Points

These points from the input review were filtered:
- Concern about Jordan block reasoning in Section 4.2.2 lacking rigor — depends on appendix material stripped by the parser; the paper's sketch is a standard argument.
- Demand for comparison to weight decay literature — a minor omission that does not affect the core critique.
- Concern about global condition K₂ ≻ –H(θ) for all θ being impractical — acknowledged in Remark 2; inherent to the design, not a flaw per se.
- Note about missing runtime comparison — trivial omission.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Fix the bridge from theory to algorithm.** The integration in Section 6 is mathematically wrong. There are two honest ways forward: (a) discretize the controlled second-order ODE directly (e.g., via a symplectic integrator or by treating it as a coupled first-order system) without attempting the invalid analytic integration; or (b) design the controller in the discrete setting from the start, using discrete-time control theory. A clean derivation would salvage the paper's core thesis.

2. **Correct the misclassified test functions** so they actually match the curvature classes claimed in Theorem 2. Replace L(θ)=θ₁²+θ₂² (which is strongly convex) with a genuinely semi-definite objective, and relabel or replace the quartic (which is not strongly convex at its minimum).

3. **Conduct experiments on at least one non-trivial problem** (e.g., MLP on MNIST) with comparisons to standard GD, momentum, and Adam. Without this, the "stabilizing gradient descent" claim in the title remains unsupported.

---

## Score and Decision

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>