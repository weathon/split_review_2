## Summary

This theory paper investigates the relationship between adaptive optimizers (Adam, Shampoo) and Normalized Steepest Descent (NSD) methods (Muon, Lion) through the lens of smoothness assumptions. It extends adaptive smoothness theory to nonconvex settings, provides a unified convergence analysis via a novel matrix inequality (Lemma 3.3) that handles noncommutative preconditioner sets, and introduces adaptive variance as an analogue for gradient noise. The paper proves two key separations: (1) adaptive smoothness enables Õ(1/T²) acceleration under Nesterov momentum, unattainable under standard ℓ∞ smoothness; (2) adaptive variance yields dimension-free rates for NSD, impossible under standard variance.

## Strengths

- **Novel matrix inequality (Lemma 3.3).** The paper identifies a genuine technical bottleneck: extending convergence proofs from diagonal to general (noncommutative) preconditioner sets requires handling noncommuting matrices. Lemma 3.3 bounds Σ‖Vₜ⁻¹gₜ‖²_H via the operator norm of an S_T matrix, explicitly accounting for the noncommutativity cost (an extra log d factor). The reliance on a new inequality relating differences of positive definite matrices to differences of their logarithms (Lemma C.1) is likely to have independent utility.

- **Clean separation results (Sections 4.2–4.3).** Two concrete comparisons give substance to the "stronger assumption → better rate" framing: (a) under adaptive smoothness, accelerated adaptive optimizers achieve Õ(1/T²) vs. Ω(1/T) under standard ℓ∞ smoothness (Theorem 4.3 vs. Guzmán & Nemirovski 2015); (b) under adaptive variance, NSD with momentum achieves dimension-independent convergence vs. unavoidable Ω(√d) dependence under standard variance (Theorems 4.5 vs. 4.6–4.7).

- **Unified meta-algorithm (Algorithm 1).** The framework captures AdaGrad, Adam, AdaGrad-Norm, and one-sided Shampoo by varying only the preconditioner set ℋ, making the analysis modular and covering previous results as special cases (e.g., the log d factor disappears for diagonal ℋ, recovering Xie et al. 2025a).

- **Transparent assumption hierarchy.** Proposition 2.5 cleanly establishes L_{‖·‖_ℋ}(f) ≤ Λ_ℋ(f) ≤ d·L_{‖·‖_ℋ}(f), and the analogous comparison for variance (Proposition B.11) is noted. The paper does not hide the fact that stronger assumptions drive the better rates.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Gap between stated theorem bounds and claimed clean rate.** Theorem 3.2's bound is (1/√T)(ξ + √d ε^{3/4} √ξ) where ξ = Õ(Δ₀/η + η·Λ_ℋ(f) log² d). The prose then claims a clean rate Õ(log d · √(Δ₀ Λ_ℋ(f)/T)). The √d ε^{3/4} √ξ term is not absorbed into this rate without additional reasoning about ε being negligibly small. While it is standard practice to state clean asymptotic rates in optimization theory, the paper should make the transition from the detailed bound to the clean rate more explicit, or state the clean rate as the primary theorem with the detailed expression as a remark.

2. **Astronomically small constants in the lower bound (Theorem 4.7).** The lower bound contains e^{-25} ≈ 1.39 × 10^{-11}. This means the bound only rules out better-than-Ω(√d) convergence for impractically small target accuracies. The asymptotic Ω(√d/√T) scaling is what matters theoretically, but the proof artifact invites skepticism. A brief explanation of whether this constant can be tightened or is an artifact of the construction would improve the paper.

3. **Hyperparameter transformations stated without derivation.** The paper asserts (line 174) that the EMA variant produces identical iterates to the weighted variant with η^W = η^E/√(1-β) and ε^W = ε^E/(1-β). These transformations are critical for connecting Algorithm 1 to practical Adam but are stated without justification or derivation (presumably in the stripped appendix). A brief justification in the main text, or a clear reference to the appendix, would help.

4. **The acceleration narrative could more prominently emphasize the assumption-class comparison.** The paper is transparent about Proposition 2.5 showing Λ_ℋ(f) ≥ L_{‖·‖_ℋ}(f), and the prose accurately describes the results. However, the abstract and introduction frame the acceleration result as a direct benefit of adaptive smoothness without equally emphasizing that the comparison spans different function classes (those satisfying adaptive smoothness vs. those satisfying only standard smoothness). This is a framing precision issue, not a technical error, but it could lead casual readers to over-interpret the result as a claim about algorithm superiority on the same problem.

### Trivial
None.

## Nice-to-Haves

- An experiment on synthetic functions where Λ_ℋ(f) and L_{‖·‖_ℋ}(f) are known would strengthen the practical relevance of the separation results, though this is not required for a theory paper.
- A brief discussion of the limitations of the well-structured preconditioner assumption (Definition 2.1) and whether common practical approximations (e.g., block-diagonal preconditioners with arbitrary block sizes) satisfy it.
- Clarifying the regime in Theorem 4.3 where the Õ(1/T²) acceleration is visible (i.e., when Λ_ℋ(f)D²/T² dominates σ_ℋD/√T).

## Removed Points

**Removed Weaknesses**
1. "Adaptive variance comparison has ambiguous practical significance" — removed. This is a theory paper; proving results under well-specified assumptions is standard. Asking whether real problems satisfy adaptive variance is outside scope.
2. "The connection to Adam's actual update is loose (the Vₜ update is expensive)" — removed. The paper acknowledges this is an analysis framework, not an implementation recipe, which is standard for theory papers.
3. "No empirical illustration" — moved to Nice-to-Haves. Not required for a theory paper.
4. "No discussion of when the well-structured preconditioner assumption holds" — moved to Nice-to-Haves. The paper does list concrete examples.

**Removed Strengths**
None of the listed strengths were removed; all are specific and evidenced.

## Novel Insights

The harsh critic raises an insightful meta-level observation: the paper's "separation" results (acceleration under adaptive smoothness, dimension-free rates under adaptive variance) are structurally comparisons between *different assumption classes*, not between algorithms on the same problem. The paper is honest about this (Proposition 2.5), but the narrative arc — "adaptive smoothness is stronger → it enables better rates!" — creates a rhetorical structure where the stronger assumption is cast as an advantage, when logically a stronger assumption always makes proofs easier. The paper would be more precise by explicitly stating: "The value of the adaptive smoothness framework is not that it gives better rates for the same problems, but that it explains why adaptive methods can provably exploit geometry that NSD methods cannot access through standard smoothness alone." This is what the paper does technically, but the prose could be sharper.

## Suggestions

- Restate Theorem 3.2 with the clean asymptotic rate Õ(log d · √(Δ₀ Λ_ℋ(f)/T)) as the primary claim, and relegate the full detailed bound to a remark or appendix.
- Add a brief remark in Section 4.2 specifying the regime (T ≪ (Λ_ℋ(f)/σ_ℋ)²) where the Õ(1/T²) acceleration is visible before the stochastic O(σ_ℋ/√T) term dominates.
- Explain the e^{-25} constant in Theorem 4.7: is it a proof artifact, or is there a fundamental reason it cannot be tightened to a reasonable value?
- Provide a short derivation of the hyperparameter transformations linking the EMA and weighted variants, or a clear appendix reference.

## Score and Decision

**Calibration Anchors:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| On the Convergence of Adam under Non-uniform Smoothness | 4.25 | R1 | Similar topic (Adam theory under alternative smoothness), but had proof errors and inconsistent assumptions. Weaker than the reviewed paper. |
| Convergence of Adafactor under Non-Convex Smooth Optimization | 5.00 | R1 | Similar style (adaptive optimizer convergence analysis), but relied on restrictive boundedness assumptions. Comparable but the reviewed paper has more novel technique (matrix inequality). |
| OPTAMI: Global Superlinear Convergence of High-order Methods | 6.25 | R1 | Accepted theory paper with practical library; had structural concerns but real contributions. Slightly stronger due to empirical validation and released library. |
| Adaptive Methods through the Lens of SDEs | 7.00 | R1 | Accepted theory+experiments paper; had broader scope and empirical support. Stronger overall package. |

**Round 1 Bracket:** 5.5 – 7.0

**Final Score:** 6.0 — Solid theory paper with genuine technical contributions (novel matrix inequality, clean separation results, unified framework). Weaknesses are presentational and minor rather than structural. The paper is above the rejection threshold but falls short of the strongest papers in the band due to being pure theory without any empirical validation and having minor presentational gaps.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>