## Summary

This paper addresses the question of whether GRAAL's curvature-adaptive stepsize rule can be combined with Nesterov acceleration while preserving both geometric stepsize growth and provable convergence. The authors identify a structural incompatibility between the standard acceleration framework and the adaptive stepsize, resolve it via an additional coupling step, and prove near-optimal iteration complexity for both \(L\)-smooth and \((L_0, L_1)\)-smooth convex functions. The key result is the first accelerated method for the \((L_0, L_1)\)-smooth class that avoids line search, hyperparameter tuning, or relaxation oracles.

## Strengths

- **Non-trivial algorithmic construction (Section 2.1):** The paper identifies a genuine obstruction — the inequality (14) from Kovalev & Borodich's acceleration framework is incompatible with an adaptive stepsize rule — and resolves it with an explicit construction: the additional coupling step (15) with \(\beta_k = \eta_k/(\alpha_k H_k)\) and the choice \(\alpha_k = (1+\gamma)\eta_{k-1}/(H_{k-1}+(1+\gamma)\eta_{k-1})\). This is a clean solution to a real technical problem.

- **Geometric stepsize growth (Section 3.2):** The paper correctly identifies that AC-FGM's restriction \(\eta_{k+1} \leq (1+1/k)\eta_k\) fundamentally limits adaptivity. Algorithm 1's ability to grow stepsizes geometrically \((\eta_{k+1} \leq (1+\gamma)\eta_k)\) is a genuine improvement that the paper formalizes and proves sufficient for near-optimal convergence.

- **First adaptive accelerated method for \((L_0, L_1)\)-smooth functions (Section 4, Table 1):** Existing accelerated methods (Li et al., 2023; Gorbunov et al., 2024; Vankov et al., 2024; Tyurin, 2025) all require either line search, parameter tuning, or a relaxation oracle. Algorithm 1 is the first to provably avoid these while achieving near-optimal complexity. This is the paper's strongest claim and is well-documented in Table 1.

- **Honest comparison with competing methods (Sections 3.2, 4.2):** The paper transparently reports that Algorithm 1 has worse additive constants (\((L_1\mathcal{D})^3\) vs. \((L_1\mathcal{D})^{5/3}\) from Vankov et al. and \((L_1\mathcal{D})^2\) from Tyurin), and explains the structural reason (geometric vs. sublinear stepsize growth) rather than claiming universal superiority.

## Weaknesses

### Fatal
None.

### Major

1. **Underspecified parameter condition in Theorem 1 (eq. 19):** The second inequality  
   \(1+2\gamma + \frac{2\gamma\theta^2}{(1+\theta)^2} \leq \frac{\theta}{(1+\theta)^2} + \frac{\theta^2}{\lambda_k}\)  
   contains \(\lambda_k\) on the right-hand side — the same iteration-dependent curvature estimate from Algorithm 1 (line 145). The paper states "it is easy to verify that such parameters exist" (line 185) but provides no explicit valid triple \((\theta,\gamma,\nu)\) in the main text, nor does it explain whether \(\lambda_k\) should be interpreted as a worst-case bound, a specific iteration value, or a separate parameter. Since \(\lambda_k \geq 1/L\) (Lemma 3) has no universal upper bound in the main text, it is unclear whether the condition can be satisfied by problem-independent constants, or whether it instead requires knowledge of \(\lambda_k\) values that depend on the objective. The appendix (which the parser strips) likely resolves this, but the main text as written is ambiguous on a point central to whether the algorithm is well-defined.

### Minor

1. **No empirical verification:** The paper presents Algorithm 1 as a practical contribution motivated by the "attractive results, both theoretically and experimentally" of GRAAL and AdGD, yet contains zero experiments — not even a synthetic convex quadratic to verify that the stepsize dynamics (geometric growth, the \(H_{k-1}\) cumulative sum in the stepsize rule, the \(\beta_k\) computation from \(\eta_{k+1}\)) behave as claimed. While the paper is primarily theoretical, and theory-only papers appear at ICLR, a minimal empirical illustration would substantially strengthen confidence that the algorithmic mechanics work outside idealized proof conditions.

2. **No conclusion or limitations discussion:** The paper ends abruptly after Section 4.2 (line 339). There is no discussion of limitations — e.g., the per-iteration cost of computing \(\lambda_k\) via the Bregman divergence (Option II), the restriction to convex objectives, the need to store past iterates for extrapolation, or guidance for choosing the universal constants \(\theta,\gamma,\nu\) across problem classes. This makes the paper feel structurally incomplete.

### Trivial
None.

## Nice-to-Haves

- Provide explicit valid parameter values \((\theta,\gamma,\nu)\) satisfying eq. (19) in the main text, together with an explanation of whether the \(\lambda_k\) dependence is resolved by a worst-case bound or by the iteration-specific dynamics.
- Include a simple numerical experiment (e.g., minimizing a convex quadratic with a deliberately bad \(\eta_0\)) to illustrate geometric stepsize growth vs. AC-FGM's sublinear growth.
- Add a conclusion/discussion section covering limitations (convex-only, computational overhead of \(D_f\) evaluation, robustness of universal constants) and future directions (stochastic or nonconvex extensions).

## Removed Points

These points from the input review are removed, with justification:

- **AdaGrad characterization as "oversimplified":** The reviewer claimed the paper's statement that AdaGrad's stepsize is non-increasing is too strong because modern variants can increase stepsizes. The paper explicitly defines AdaGrad's stepsize in eq. (5) as \(\eta_k = \eta \cdot (\sum \|\nabla f(x_i)\|^2)^{-1/2}\), which is indeed non-increasing. The characterization is correct for the standard variant discussed. *Removed: criticism is factually inaccurate.*

- **AC-FGM/AdaNAG complexity claims deserve more scrutiny:** The reviewer questioned whether the paper's interpretation of Li & Lan (2025, Corollary 1) and Suh & Ma (2025) is correct. The paper attributes eqs. (28) and (29) to specific cited results. Without access to those cited works, this criticism is speculative — it questions a cited reference's correctness. *Removed: speculative; the paper cites specific results.*

- **The "Solution: additional coupling step" lacks explanation:** The reviewer claimed the paper doesn't explain how the additional coupling step resolves the circular dependency. Lines 155-163 explain that \(\alpha_k\) uses \(\eta_{k-1}\) (not \(\eta_k\)), breaking the dependency. *Removed: the paper already addresses this.*

- **Formatting/style nitpicks:** Various minor notes about presentation. *Removed per Hard Rules.*

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- In the main text of Theorem 1, either provide explicit numerical values for \((\theta,\gamma,\nu)\) that satisfy eq. (19) together with a brief verification, or clarify that the \(\lambda_k\) in (19) is to be replaced by the uniform lower bound from Lemma 3 (or Lemma 6) to obtain a condition on the constants alone.
- Add a brief experimental section showing Algorithm 1's stepsize growth on a simple convex quadratic, compared to AC-FGM, to directly illustrate the claimed adaptive advantage.
- Add a conclusion section discussing limitations, practical parameter guidance, and possible extensions.

## Score and Decision

**Calibration Report:**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| GQ1Tc3vHbt.md — Optimizing (L₀,L₁)-Smooth Functions by Gradient Methods | 6.50 (Accept) | Round 2 | Yes | Same function class; has simple experiments + conclusion; slightly weaker algorithmic novelty but better presentation |
| YwJkv2YqBq.md — Nesterov acceleration in benignly non-convex landscapes | 6.75 (Accept) | Round 1 | Yes | Theory-heavy optimization with Nesterov; has experiments and clear limitations discussion |
| nuX2yPejiL.md — Stochastic Polyak Step-sizes and Momentum | 7.00 (Accept) | Round 1 | Yes | Strong theory + experiments; better empirical validation |
| CuupjjjT3U.md — Parameter-Free Adaptive Gradient Methods | 4.00 (Reject) | Round 1 | Yes | Weak novelty, insufficient experiments, theory-practice disconnect |
| uu2CorJCUi.md — Adaptive Curvature Step Size | 4.80 (Reject) | Round 1 | Yes | Theory was actually wrong (non-convergence); fatally flawed |
| 1JPfHljXL4.md — Adaptive Learning Rate Scheduling | 5.80 (Reject) | Round 3 | Yes | Strong experiments but limited theoretical novelty |
| SrGP0RQbYH.md — Adaptive backtracking | 6.25 (Accept) | Round 1 | No | Related adaptive method with experiments and conclusion |

**Bracketing:** Round 1 placed the paper between 5.5 and 7.5, with the topically closest anchor (GQ1Tc3vHbt, 6.50) in the Accept band. Round 2 narrowed by comparing weighted items: the paper shares the anchor's heavy-weight strengths (theoretical contribution to \((L_0,L_1)\)-smooth optimization, clear algorithmic construction), but lacks the anchor's experiments and conclusion section. The anchor's item-weighted profile shows its "simple experiments" weakness had relatively low negative impact (weight ~3-6), while its "writing/presentation issues" had moderate impact. The paper under review has a stronger algorithmic novelty (solving the GRAAL+acceleration open problem) but worse main-text clarity on the parameter condition and no conclusion section.

**Final score: 6.0** — borderline accept. The contribution is genuine (first adaptive accelerated method for \((L_0,L_1)\)-smooth functions, non-trivial algorithmic resolution of a structural obstruction), but the underspecified parameter condition in the main text and the absence of a conclusion/limitations discussion weaken the presentation. The paper would be a solid accept with explicit parameter values and a conclusion section.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>