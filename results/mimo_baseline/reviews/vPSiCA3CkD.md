## Summary

This paper develops Accelerated GRAAL, a gradient method that combines Nesterov momentum with adaptive stepsize selection based on local curvature estimation. The key technical innovation is an "additional coupling step" that decouples the computation of the momentum parameter α_k from the adaptive stepsize η_k, enabling the stepsize to grow at a geometric rate—matching the adaptation speed of non-accelerated GRAAL. The method achieves near-optimal iteration complexity O(√(L‖x₀−x*‖²/ε) + log(1/(η₀L))) for L-smooth convex functions and the same rate up to additive constants under the more general (L₀, L₁)-smoothness assumption, without requiring line search or hyperparameter tuning.

## Strengths

- **Novel resolution of a genuine technical challenge.** The paper identifies a fundamental tension: Nesterov acceleration requires knowing α_k before computing η_k, but the curvature estimator needs the gradient at a point defined using α_k. The coupling step (line 7, eq. (15)) with the specific choice β_k = η_k/(α_kH_k) elegantly resolves this, and the proof that β_k ∈ (0,1] in Lemma 1 relies on a clean induction. This is a substantive algorithmic contribution.

- **Strong theoretical results with clear comparative advantage.** Corollary 2 achieves near-optimal complexity with only a logarithmic additive factor depending on the initial stepsize, and Corollary 3 extends this to (L₀, L₁)-smoothness. The detailed comparison in Section 3.2 convincingly demonstrates that AC-FGM and AdaNAG have sublinear stepsize growth that fundamentally limits their adaptivity—their complexities degrade by factors of 1/√(η₀L) or η₀L when the initial stepsize is misspecified.

- **First adaptive accelerated method for (L₀,L₁)-smoothness.** Table 1 clearly positions Algorithm 1 as the first method achieving near-optimal iteration complexity under (L₀,L₁)-smoothness while being fully adaptive. The prior near-optimal methods (Vankov et al., Tyurin) require either a relaxation oracle or parameter tuning.

## Weaknesses

### Fatal
None.

### Major

- **Lack of any empirical evaluation.** The paper makes strong theoretical claims about adaptivity advantages, particularly the geometric growth of stepsizes versus the sublinear growth in AC-FGM and AdaNAG. However, no experiments are provided to demonstrate these advantages in practice. For a paper whose primary contribution is an adaptive algorithm, showing actual stepsize evolution trajectories and comparing convergence on concrete problems would substantially strengthen the claims. While theory-only papers appear at ICLR, the absence of even a single synthetic experiment to validate the claimed behavior is a missed opportunity.

- **The (L₀,L₁)-smoothness additive constant (L₁D)³ versus (L₁D)^{5/3} for Vankov et al. (2024) is non-trivial.** While the paper correctly frames both as "near-optimal" (matching the √(L₀D²/ε) rate up to additive constants), the gap between exponents 3 and 5/3 can be substantial when L₁D is large. The paper does not discuss whether this gap is inherent to the adaptive setting or could potentially be improved.

### Minor

- **The choice of parameters θ, γ, ν satisfying eq. (19) is left implicit.** While the paper states such parameters "exist" and "it is easy to verify," providing at least one concrete triple would aid implementation. The condition involves four coupled inequalities on three parameters, and practitioners may find it non-trivial to satisfy.

### Trivial
None.

## Nice-to-Haves

- A simple experiment comparing Algorithm 1 against AC-FGM and AdaNAG on a logistic regression or similar convex ML problem, particularly visualizing stepsize trajectories to demonstrate the claimed geometric vs. sublinear growth difference.
- An explicit parameter choice (e.g., θ = ..., γ = ..., ν = ...) verified to satisfy eq. (19), or a discussion of how sensitive the method is to this choice.

## Novel Insights

The paper's central novel insight is that the tension between Nesterov acceleration (requiring predetermined schedule parameters) and adaptive stepsize selection (requiring curvature information that depends on those parameters) can be resolved by introducing an auxiliary averaging variable x̄_k controlled by a coupling coefficient β_k. By choosing α_k based on previous stepsizes and the cumulative sum H_{k-1} rather than on a fixed schedule like 2/(k+2), the method inherits the fully adaptive nature of GRAAL while gaining Nesterov acceleration. This insight—that the coupling step effectively absorbs the information mismatch—is genuinely new and goes beyond what prior work (AC-FGM, AdaNAG) attempted by simply predefining α_k.

## Suggestions

- Include at least a small synthetic experiment (e.g., quadratic or logistic regression) demonstrating the claimed advantages, particularly the stepsize behavior and convergence comparison with AC-FGM and AdaNAG.
- Provide explicit parameter values satisfying eq. (19), potentially with a brief verification, to lower the barrier for implementation.

## Score and Decision

The paper makes a genuine and technically sophisticated contribution to adaptive optimization theory. The coupling step is an elegant solution to a real algorithmic challenge, and the theoretical analysis is thorough with clear positioning against prior work. The main weakness—lack of experiments—is significant for a paper about practical adaptivity but is standard for theory-oriented optimization papers. The (L₁D)³ vs (L₁D)^{5/3} gap is a real limitation but does not invalidate the contribution, as adaptivity is the primary claimed advantage over Vankov et al.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: Accept