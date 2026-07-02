## Summary

This paper theoretically compares adaptive optimizers (Adam, Shampoo) and Normalized Steepest Descent (NSD) methods (SignGD, Lion, Muon) through the lens of smoothness and variance assumptions. It extends the notion of adaptive smoothness to nonconvex optimization, proving that adaptive optimizer convergence is governed by adaptive smoothness. The paper further shows that adaptive smoothness enables Nesterov acceleration to achieve an O(T^{-2}) rate under non-Euclidean geometry—a rate provably unattainable under standard smoothness. Finally, it introduces an adaptive gradient variance assumption and demonstrates that it yields dimension-free convergence guarantees for NSD, which are impossible under standard variance.

## Strengths

- **Clear conceptual separation.** The paper draws a crisp distinction between standard smoothness (governing NSD) and adaptive smoothness (governing adaptive optimizers), and shows that adaptive smoothness is strictly larger yet enables better rates—a non-obvious trade-off that advances the theoretical understanding of adaptivity.
- **Novel nonconvex analysis for general preconditioner sets.** Theorem 3.2 provides the first unified convergence guarantee for adaptive optimizers with arbitrary well-structured preconditioner sets in the nonconvex setting, going well beyond the diagonal case. The key technical Lemma 3.3, a new matrix inequality, is both necessary and potentially of independent interest.
- **Acceleration under adaptive smoothness.** Theorem 4.3 shows that adaptive optimizers with Nesterov momentum achieve an accelerated O(T^{-2}) rate under adaptive smoothness, while citing a known lower bound (Guzmán & Nemirovski, 2015) showing that Ω(T^{-1}) is optimal under standard ℓ∞ smoothness. This establishes a concrete optimization benefit of the stronger adaptive smoothness.
- **Adaptive variance and dimension-free bounds.** The introduction of adaptive variance (Definition 4.1) and the proof that it enables dimension-free nonconvex rates for NSD (Theorem 4.5), complemented by a matching lower bound under standard variance (Theorem 4.7), is a clean and impactful theoretical contribution.

## Weaknesses

### Fatal
None.

### Major

- **No empirical validation.** The paper is purely theoretical. While theory papers do not require experiments, the strong claims about “benefits” (acceleration, dimension-free rates) would be significantly strengthened by simple illustrative examples or numerical verification on synthetic problems that clearly exhibit the separation between adaptive and standard smoothness. Without any experiments, it is difficult to assess whether the theoretical bounds are tight or whether they reflect practically relevant phenomena.

- **Practical realizability of adaptive variance.** The adaptive variance (Definition 4.1) requires uniform control over all x and t of the expected squared gradient deviations in the H⁻¹ norm, minimized over H. This is a strong assumption; the paper claims it is weaker than bounded covariance (Proposition B.10), but the uniform supremum over x and t makes it potentially hard to verify in practice. A discussion of realistic problem classes where this assumption holds would improve the paper.

### Minor

- **Convergence rates with log factors.** The stated rates contain multiple logarithmic factors and involve constants like ‖S_T‖_op that are only bounded up to absolute constants. The practical dependence on problem parameters (d, ϵ, β) is somewhat obscured. A cleaner corollary with explicit leading-order terms would aid readability.

- **Accelerated algorithm requires domain knowledge.** Algorithm 2 uses a projection to stay within a ‖·‖_ℋ-ball of radius D, but choosing D may require prior knowledge of the distance to optimum. The paper addresses this in the appendix but the main text presentation could be clearer about the added complexity.

### Trivial

- The lower bound in Theorem 4.7 has unusual constants (e^{-25 - 1/4}) that appear to be parser artifacts; the exact form is difficult to parse.

## Nice-to-Haves

- A small synthetic experiment demonstrating the acceleration gap (adaptive vs. standard smoothness) on a convex problem with ℓ∞ geometry would substantially increase the impact of Section 4.2.
- A brief discussion of whether the log d factors in the nonconvex bound for general ℋ are tight, perhaps by comparison to known lower bounds for AdaGrad/Adam.

## Novel Insights

The paper articulates a fundamental duality between the supremum of primal norms induced by a preconditioner set and the infimum of the corresponding dual norms (Lemma 2.2), and uses this to explain why adaptive optimizers and NSD exploit the same geometry through different smoothness assumptions. The insight that averaging is ineffective in dual spaces (leading to the dimension-dependent obstacle) and that adaptive variance circumvents this by aligning the noise measure with the preconditioner geometry is a genuinely novel synthesis.

## Suggestions

- Include a brief toy experiment (e.g., a convex function with ℓ∞ smoothness where Adam with Nesterov acceleration beats SignGD with momentum) to validate the accelerated rate claim.
- Clarify the relationship between adaptive variance and the bounded covariance assumption more explicitly in the main text (currently only in Proposition B.10 of the appendix).

## Score and Decision

Score: 8

Decision: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>