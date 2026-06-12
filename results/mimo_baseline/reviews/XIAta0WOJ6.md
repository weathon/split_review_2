## Summary

This paper studies stochastic bilevel optimization under nonconvex-strongly-convex settings and proposes F²SA-p, a family of fully first-order methods that replaces the forward-difference hyper-gradient estimator of F²SA with pth-order finite differences. The key insight is reinterpreting F²SA's penalty formulation as a forward difference approximation, which naturally extends to higher-order schemes. The authors prove an improved SFO complexity of Õ(pε^{-4-2/p}) for pth-order smooth problems and establish an Ω(ε^{-4}) lower bound showing near-optimality when p = Ω(log ε⁻¹/log log ε⁻¹).

## Strengths

- **Novel and elegant reinterpretation.** The connection between F²SA's penalty formulation and finite-difference approximation of the hyper-gradient (Eq. 8-9) provides a clean conceptual framework. This directly addresses the conjecture by Chayti & Jaggi (2024) about extending finite-difference connections beyond symmetric approximations and meta-learning to general bilevel optimization.

- **Progressive complexity improvement.** The paper achieves a meaningful interpolation from Õ(ε⁻⁶) (p=1) toward Õ(ε⁴) (p→∞), with tight analysis. For p=2, the method requires the same number of lower-level solves as F²SA (2 solves) yet achieves Õ(ε⁻⁵) under second-order smoothness—essentially "free" improvement when the smoothness assumption holds. The tighter bound on ∂³/(∂ν∂x²)ℓ_ν(x) Lipschitzness (O(κ⁵) vs. O(κ⁶)) via the limiting-point argument in Remark 3.2 is also a nice technical contribution.

- **Clean lower bound construction.** The Ω(ε⁻⁴) lower bound uses a fully separable bilevel construction (f depends only on x, g is a simple quadratic in y) that avoids the pitfalls of prior work (Daggru et al. 2024 had non-Lipschitz derivatives in y; Kwon et al. 2024a violated joint smoothness in x). This construction is straightforward and clearly satisfies all assumptions in Definition 2.2.

- **Well-structured paper.** The progression from problem setup → finite-difference reinterpretation → algorithm → complexity → lower bound → experiments is logical and well-executed. The discussion of open problems (condition number gap, p=1 gap) is honest and informative.

## Weaknesses

### Fatal
None.

### Major

- **Condition number dependence gap.** The upper bound depends on κ^{9+2/p}, while recent lower bounds (Ji 2025: Ω(κ^{5/2}ε⁻⁴); Chen & Zhang 2025: Ω(κ⁴ε⁻⁴)) show this is far from tight. For the highly-smooth regime where near-optimality in ε is claimed, the result is only near-optimal up to a potentially large κ-dependent factor. While the paper honestly acknowledges this (Table 1, line "Open problems"), it limits the practical significance of the near-optimality claim.

- **Weak experimental validation.** The experiments evaluate only a single problem (learn-to-regularize on 20 Newsgroup) with a small number of outer-loop iterations (T=1000). From Figure 1, the loss curves for F²SA-3, -5, -8, -10 are nearly indistinguishable, and the difference from F²SA itself is modest. No ablation on the effect of p on per-iteration cost is presented, and no experiments test sensitivity to the hyperparameter ν. The claim that F²SA is "the only method scaled to 32B LLM training" suggests practical relevance is important, yet the experiments are limited to logistic regression.

### Minor

- **Near-optimality condition is restrictive.** Requiring p = Ω(log ε⁻¹/log log ε⁻¹) smoothness to match the Ω(ε⁻⁴) lower bound means near-optimality only applies in a regime where the problem is extremely smooth. For typical ML problems where only p=2 or p=3 smoothness holds, the gap to the lower bound remains ε^{-0.5} to ε^{-0.67}.

- **Comparison baseline imbalance.** The paper compares against HVP-based methods (stocBiO, MRBO, VRBO) which use strictly stronger oracles. While useful as reference points, the comparison is not apples-to-apples, and the main comparison (F²SA vs. F²SA-p) shows relatively modest practical differences.

### Trivial
None.

## Nice-to-Haves

- Experiments on a broader set of problems (e.g., meta-learning, hyperparameter tuning for neural networks) to demonstrate the generality of the approach.
- Per-iteration runtime comparisons, since F²SA-p with p≥3 requires solving more lower-level problems per iteration, and the practical tradeoff between per-iteration cost and convergence speed matters.
- Experiments with larger T (more iterations) to better observe asymptotic convergence behavior.

## Novel Insights

The central novel insight is that the penalty formulation of bilevel optimization (Eq. 3) can be viewed as a finite-difference approximation of the hyper-gradient (Eq. 9), and that replacing forward difference with higher-order central differences yields a principled family of algorithms with provably better complexity under correspondingly stronger smoothness assumptions. This bridges numerical differentiation techniques from numerical analysis with stochastic bilevel optimization theory, providing a unified framework where the smoothness order p directly determines both the approximation quality and the resulting complexity. The observation that p=2 (central difference) offers near-free improvement over p=1 (forward difference) — requiring only 2 lower-level solves like F²SA but gaining Õ(ε⁻⁵) instead of Õ(ε⁻⁶) under second-order smoothness — is a practically valuable design principle.

## Suggestions

- Include per-iteration cost analysis in experiments to show wall-clock advantages, not just iteration-count advantages.
- Add experiments with larger iteration counts or on problems where higher-order smoothness is more pronounced (e.g., polynomial regression tasks) to better demonstrate the practical benefit of larger p.
- Discuss more concretely when Assumption 2.5 is expected to hold in practice beyond logistic regression with softmax parameterization.

## Score and Decision

The paper makes a clean, theoretically sound contribution that meaningfully advances our understanding of complexity in stochastic bilevel optimization. The finite-difference reinterpretation is elegant, the algorithm family is natural, and the matching lower bound provides good closure. The main limitations are the large condition number gap and limited experiments, but these do not invalidate the core contributions.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept