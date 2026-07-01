## Summary

This paper proposes a control-theoretic framework for stabilizing gradient descent. The authors formulate GD as a second-order ODE, analyze stability under different curvature regimes, and propose adding a PD controller to achieve local asymptotic stability. They then attempt to convert this into a discrete algorithm (Controlled Gradient Descent, CGD) by integrating the controller to obtain a modified gradient update. Empirical results are shown on 2D synthetic functions.

## Strengths

1. **Clean mathematical framing of the curvature-stability connection (Section 4).** The derivation from the second-order ODE (Eq. 2) through the Jacobian (Eq. 3) to the characteristic equation det(λ²I + λH) = 0 is clearly presented and technically sound for the linearized second-order system (up to the caveat noted in Minor Weakness 2 below).

2. **Table 1 is a clear synopsis.** It succinctly communicates the claimed contrast between GD (Lyapunov stable at best, never asymptotically stable under strong convexity) and the controlled system (claimed asymptotically stable regardless of curvature).

## Weaknesses

### Fatal
None.

### Major

1. **The derivation from the continuous controller to the discrete algorithm (Eq. 5) contains a mathematical error that breaks the claimed connection between theory and method.** The paper computes ∫u dt = ∫(−K₁θ − K₂·dθ/dt)dt and replaces ∫θ dt with ½θ². However, ∫θ dt is the accumulated parameter trajectory over time — it depends on the full path θ(t), not the instantaneous value θ. The equality ∫θ dt = ½θ² holds only if θ(t) varies linearly with t (dθ/dt = constant), which is not true for gradient descent. This means Algorithm 1 does not rigorously follow from the theoretical analysis of the controlled second-order system. The claimed "variational interpretation" (Abstract) is unsubstantiated by the derivation as presented.

2. **The controller shifts the equilibrium away from the loss minimizer — a fundamental conceptual mismatch.** The controlled system (Eq. 4) with u = −K₁θ − K₂·dθ/dt has dynamics d²θ'/dt² = −H(θ)·dθ/dt − K₁θ − K₂·dθ/dt. At equilibrium (dθ/dt = 0, d²θ/dt² = 0), this yields −K₁θ = 0, hence θ = 0 — the origin, not the loss minimizer θ*. The paper states (line 198) that the system is stable around [θ*; 0], but this is inconsistent with the defined controller. In Algorithm 1, the modified gradient ∇L(θ) − K₁θ² − K₂θ = 0 does not generally have the original minimizer as a fixed point. The paper never acknowledges or addresses this equilibrium shift.

3. **The experimental evaluation misclassifies the curvature of its own test functions.**  
   - The "convex but not strongly convex sphere" L(θ) = θ₁² + θ₂² has Hessian 2I (positive definite), making it **strongly convex** — the textbook example.  
   - The "strongly convex quartic" L(θ) = θ₁⁴ + θ₂⁴ has Hessian diag(12θ₁², 12θ₂²), which at the minimum θ = 0 is the **zero matrix** (not positive definite), making it convex but not strongly convex.  
   These mislabelings (confirmed on lines 269–271) are factual errors that directly contradict the paper's own curvature-based stability framework and undermine trust in the empirical evaluation.

4. **The experimental scope is far too narrow to support the paper's broader claims.** The paper frames its contribution as relevant to "neural network training" (Algorithm 1 caption, Abstract) and "general non-convex and non-smooth" settings (Introduction), yet the experiments are exclusively on 2D synthetic functions (quadratics and quartics). There are no experiments on any neural network (even a small MLP), no high-dimensional problems, no stochastic gradients, and no comparisons to standard optimizers (momentum, Adam, Nesterov, or even vanilla GD with better-tuned learning rates). The gap between the claimed generality and the demonstrated evidence is large.

### Minor

5. **The stability analysis applies to a continuous-time second-order system, not to discrete GD.** The paper acknowledges this gap in the limitations (Section 8), but the entire theoretical contribution (Theorem 2, Theorem 3, Table 1) characterizes the continuous second-order ODE — a system that differs from the discrete first-order GD algorithm. There is no theorem connecting the continuous analysis to the discrete algorithm's behavior. The paper's claims about GD's stability (Table 1) are about a derived continuous system, not about the actual discrete GD, which limits their direct relevance.

6. **The Jacobian analysis for the convex-but-not-strongly case (Section 4.2.2) relies on linearization at a point where the Hessian has zero eigenvalues.** Standard dynamical systems theory (center manifold theorem) indicates that linearization alone is inconclusive when eigenvalues lie on the imaginary axis with degenerate Jordan blocks. The "unstable" conclusion is plausible but the linearization argument does not by itself conclusively establish instability for the full nonlinear system in this regime.

### Trivial

7. Line 124 reads "convex but not strongly concave"; this should be "concave."

## Nice-to-Haves

- The hyperparameter ablation (Section 7.1) tests only k₁ = k₂ with three values (0.05, 0.1, 0.2). An independent sweep over k₁ and k₂, or a test of the theoretical condition H(θ)+K₂ ≻ 0, would be more informative.
- The learning rate experiments (Section 7.2) only use the sphere loss. Testing on other curvature types would strengthen the empirical case.

## Removed Points

- *Criticism about no justification for PD controller form*: Removed — PD control is standard in control theory and the paper adopts it straightforwardly. No further justification is required given the paper's framing.
- *Criticism about no discussion of computational cost*: Removed — the element-wise operations (-K₁θ² - K₂θ) are trivially cheap and the paper's concern is convergence behavior, not wall-clock optimization of cheap operations.
- *Criticism that Table 1 is misleading*: Merged into Minor Weakness 5 — the continuous-discrete gap is acknowledged by the paper; the table accurately represents the continuous analysis.
- *Criticism about missing neural network experiments being fatal*: Kept as Major Weakness 4 but downgraded from "fatal" because the paper's primary contribution is framed as theoretical.

## Novel Insights

None beyond the paper's own contributions. The control-theoretic framing of GD stability is the paper's main idea, and the reviewers' analyses do not add substantively novel insights beyond identifying problems with the execution.

## Suggestions

1. **Fix the derivation (Eq. 5).** Replace the invalid ∫θ dt = ½θ² step with a correct mathematical argument. Alternatively, design the controller directly at the discrete level by analyzing the eigenvalues of the discrete update's Jacobian.

2. **Address the equilibrium shift.** Either (a) prove that the fixed point of ∇L(θ) − K₁θ² − K₂θ = 0 is near the original minimizer θ* under reasonable conditions, or (b) modify the controller to use (θ − θ*) instead of θ — though this requires knowing θ* a priori. Without this, it is unclear what problem CGD actually solves.

3. **Correct the curvature misclassifications.** Label the sphere loss (θ₁² + θ₂²) as strongly convex and the quartic (θ₁⁴ + θ₂⁴) as convex but not strongly convex, and discuss how these cases align with (or differ from) the theoretical predictions.

4. **Add at least one small-scale neural network experiment** (e.g., MLP on MNIST) and comparisons to standard baselines (SGD with momentum, Adam) to support the claimed relevance to neural network training.

---

**Calibration Anchors (from /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/):**

| Path | Avg Score | Round | Comparison to This Paper |
|------|-----------|-------|------------------------|
| 1NYhrZynvC.md — Exact linear-rate GD | 2.50 | Round 1 | Similar severity: had flawed theoretical claims (false global convergence guarantee) and limited experiments. Both are rejected. |
| NbbsRnPBoS.md — Faster GD in deep linear nets | 2.33 | Round 1 | Similar: very narrow scope, trivial observations. The current paper has a more interesting framing but also verifiable errors. |
| 9mOs2Bxd3Q.md — Extending stability analysis to adaptive optimizers | 3.50 | Round 2 | Similar theoretical ambitions with a verified mathematical error (incorrect eigenvalue decomposition). Rejected; current paper has more errors. |
| OZZYqfplS3.md — Predictive coding stability | 4.00 | Round 1 | Stronger theoretical analysis (no mathematical derivation errors), but continuous-discrete gap concerns. Current paper is weaker. |
| cCcaJzPAnb.md — Universal Concavity-Aware Descent | 3.80 | Round 2 | More rigorous proofs but incomplete empirical validation. Current paper has more fundamental theoretical issues. |

**Round 1 Bracket (from queries covering 1.5–8.5+):** The paper clearly falls in the Reject range. Strong-reject anchors (scores ≤ 1.5) were mostly off-topic or very weak papers. The relevant anchors cluster in 2.33–4.00, all rejected. This paper is at the lower end of this band due to verifiable mathematical errors (Eq. 5 integration, equilibrium mismatch) and factual errors (curvature mislabeling).

**Round 2 Narrowing:** Fine search in the 2.0–4.0 range confirmed the paper belongs near 3.0 — comparable to the exact-linear-rate GD paper (2.50) and the deep linear networks paper (2.33), but with a more interesting framing that prevents a score of 1 or 2. The 3.5–4.0 anchors (adaptive stability, concavity-aware descent) had fewer self-contradictions and more complete theoretical execution.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>