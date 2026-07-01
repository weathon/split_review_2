## Summary

This paper proposes to analyze gradient descent through a second-order control-theoretic lens. It derives a second-order ODE from gradient flow, analyzes its stability under different curvature regimes (strongly convex, convex-but-not-strongly, concave), and designs a continuous-time feedback controller (u = -K₁θ - K₂(dθ/dt)) intended to guarantee asymptotic stability regardless of curvature. The paper then attempts to convert this continuous controller into a discrete update rule (Algorithm 1) by integrating and adding a gradient modification term -K₁θ² - K₂θ.

## Strengths

- **The core conceptual framing — using second-order dynamics and control-theoretic stabilization for optimization — is intellectually interesting.** The specific use of the quadratic eigenvalue problem (Lemma 4, Tisseur & Meerbergen 2001) to prove asymptotic stability of the controlled continuous-time system (Theorem 3) is mathematically sound as a standalone technical step.

- **The stability classification of the second-order system (Section 4.2)** based on the characteristic polynomial det(λ²I + λH) and the eigenvalue/Jordan-block analysis is internally consistent within its own formal framework.

- **The paper identifies a genuine practical concern:** that gradient descent can exhibit unstable or oscillatory behavior in non-strongly-convex regions and that learning-rate bounds alone do not guarantee stable convergence across all curvature regimes.

## Weaknesses

### Fatal

- **Equation 5 contains a mathematical error that invalidates the derivation of Algorithm 1 from the continuous theory.** The paper writes:

  > dθ'/dt = ∫ d²θ'/dt² dt = ∫ d²θ/dt² dt + ∫ u dt = dθ/dt - ½K₁θ² - K₂θ

  where u = -K₁θ - K₂(dθ/dt). The term ∫ u dt = -K₁∫θ dt - K₂θ. The paper implicitly claims ∫θ dt = ½θ², which is **false**: the integral of θ(t) with respect to *time* is not θ(t)²/2 (that would be ∫θ dθ, integration with respect to θ itself, not t). This is not a minor typo — it is the single step that bridges the continuous-time controller (defined on the second derivative) to the discrete algorithm (which modifies the gradient/first derivative). Because this step is unsound, **Algorithm 1 does not follow from the theoretical analysis in Sections 3–5**. The paper's primary deliverable is a discrete optimizer, but its derivation is mathematically invalid. This flaw is structural and cannot be fixed by adding experiments or tightening prose.

### Major

- **The second-order system being analyzed is not equivalent to gradient descent in its stability properties.** Starting from gradient flow (dθ/dt = -∇L(θ)), the paper differentiates to obtain d²θ/dt² = -H(θ)·dθ/dt, then analyzes this 2n-dimensional system. Under strong convexity, the original n-dimensional gradient flow has Jacobian -H(θ*) with all eigenvalues negative → asymptotically stable. The paper's 2n-dimensional reformulation introduces n spurious zero eigenvalues, leading it to conclude the system is only "Lyapunov stable" (not asymptotically) under strong convexity. This weaker conclusion is an artifact of the reformulation, not a discovery about gradient descent. The paper then designs a controller to fix this self-created problem.

- **The experiments are far too weak to support the paper's claims.** All experiments are on 2D toy problems (quadratic and quartic). There are: (a) **no neural network experiments** despite Algorithm 1 being titled "for Neural Network Training"; (b) **no comparisons against standard optimizers** (momentum, Adam, Nesterov, or any other method); (c) **no error bars or statistical significance** — all results are single-run trajectories; (d) **no study of high-dimensional behavior** where K₁, K₂ would be d×d matrices. For the empirical claims in the abstract ("improves both stability and convergence behaviors," "higher tolerance on learning rate"), this evidence is insufficient.

- **Factual errors in the experimental setup undermine confidence.** The paper labels L(θ) = θ₁² + θ₂² as "convex but not strongly convex sphere" (line 269, line 271). This function has Hessian = 2I, which is positive definite everywhere — it **is** strongly convex. Conversely, the paper labels L(θ) = θ₁⁴ + θ₂⁴ as "strongly convex quartic" (line 259, line 269). This function has Hessian = diag(12θ₁², 12θ₂²) which is zero at the origin, so it is **not** globally strongly convex. These are basic classification errors that affect how the experiments relate to the theoretical claims in Table 1.

- **The claimed "variational interpretation" (abstract) is never discussed in the paper body.** The abstract states the controller "admits a variational interpretation," but this claim appears nowhere in Sections 3–8. A contribution asserted in the abstract but absent from the main text is unsubstantiated.

### Minor

- **The paper overclaims the gap it fills.** The introduction states "to date, no theoretically characterized algorithm exists that guarantees stabilized convergence of GD in general setting" (line 36). This is too strong and is not remedied by the paper itself, which does not provide discrete-time convergence guarantees.

- **The condition H(θ) + K₂ ≻ 0 must hold for all θ.** In a general non-convex setting where H(θ) can have large negative eigenvalues, this would require K₂ to have correspondingly large positive eigenvalues. The paper provides no guidance on choosing K₂ in practice beyond setting it to k₂I, and does not address feasibility when the Hessian has arbitrarily negative curvature.

### Trivial

None.

## Nice-to-Haves

- The derivation from continuous controller to discrete algorithm could be fixed by discretizing the controlled second-order ODE directly (e.g., using a symplectic integrator or treating it as a second-order difference equation), rather than attempting the mathematically invalid integration in Equation 5.
- Experiments on at least a small neural network (e.g., MLP on MNIST) with comparisons against standard optimizers would be needed to substantiate the practical claims.
- The variational interpretation promised in the abstract should be developed or removed.
- The curvature classification of the test functions should be corrected.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticism about missing engagement with prior control-theoretic approaches (PID control for SGD, observer-based optimizers):** This is a missing-related-work claim. As per policy, this is removed because I cannot independently verify the completeness of the related work coverage.
- **Section-by-section note about "no engagement with prior control-theoretic approaches":** Same reasoning as above.

## Novel Insights

None beyond the paper's own contributions. The reviewer's main insight — that Equation 5's integration of θ(t) with respect to t does not yield θ²/2 — is a straightforward mathematical verification. The concern about the second-order analysis creating spurious stability artifacts is a structural observation about the paper's framing but does not constitute a novel discovery about optimization.

## Suggestions

1. **Fix or remove the derivation in Equation 5.** If the intention is to propose a heuristic modification of the gradient (adding -K₁θ² - K₂θ), this should be stated as a heuristic inspired by the continuous analysis, not as a mathematically derived consequence. Alternatively, derive a discrete algorithm by directly discretizing the controlled second-order ODE.
2. **Separate the analysis of the second-order system from claims about gradient descent's intrinsic stability.** Acknowledge that the stability artifacts (spurious zero eigenvalues) arise from the reformulation itself.
3. **Substantially expand the experiments** to include high-dimensional problems, comparisons with standard optimizers, and statistical replicates — or explicitly scope the paper as purely theoretical.
4. **Correct the factual errors** in the curvature labels of the test functions.
5. **Either develop the claimed variational interpretation or remove it from the abstract.**

## Score and Decision

This paper has a conceptually appealing premise but contains a fatal mathematical error (Equation 5) that invalidates the derivation of its central algorithmic contribution from the theory. The connection between the continuous controller and the discrete update rule is unsound. Combined with major weaknesses in the experimental evaluation and factual errors in the experimental design, the paper cannot be accepted in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>