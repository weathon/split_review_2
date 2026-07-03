## Summary

This paper proposes quantum algorithms for projection-free (Frank-Wolfe) convex optimization under sparsity-inducing constraints in both vector and matrix domains. For the vector domain (ℓ₁ ball, simplex, latent group norms), it achieves query complexity of O(√d/ε) using a function-value oracle — a quadratic improvement over the classical O(d). For the matrix domain (nuclear norm) it develops two algorithms based on quantum singular value estimation and a quantum power method, aiming for an O(√d) speedup over classical methods. The core techniques are quantum gradient estimation in superposition combined with quantum maximum finding for the FW linear subproblem.

## Strengths

1. **First quantum FW algorithms for the matrix domain (nuclear norm constraints).** The paper credibly claims to be the first to consider quantum acceleration of FW for the matrix domain (line 35–36). Prior quantum FW work (Chen & de Wolf, 2023) only covered vector domains with explicit closed-form gradients. Theorems 3 and 4 give concrete complexity bounds of Õ(rd/ε²) and Õ(√rd/ε³) for the update-direction computation.

2. **Clean O(√d) query advantage for the vector case.** Theorem 1 (line 187) provides an explicit per-round query complexity of O(√d log(C_f/ε)) using only a function-value oracle, with parameter settings (σ_t = C_t/(√d L(t+2))) specified. This is a quadratic improvement over the classical O(d) per iteration and is verifiable from the presented analysis.

3. **Two complementary matrix-domain algorithms for different gradient-rank regimes.** The QTSVE method (Theorem 3) targets high-rank gradients, while the QPM method (Theorem 4) reduces rank dependence at the cost of higher precision sensitivity (line 48–49). This demonstrates algorithmic design that accounts for problem-specific structure.

4. **Generalization to latent group norm constraints** with a subroutine that computes dual norms coherently across groups in quantum superposition, achieving O(√|G|) speedup (Theorem 6).

## Weaknesses

### Fatal
None. The vector-domain contribution is self-contained and unaffected by the matrix-domain issues. The matrix-case problems are significant but correctable with revisions.

### Major

1. **Inconsistency between Table 2 and Theorems 3/4 complexity expressions.** This is the most serious issue in the paper. Comparing the expressions directly from the paper:

   **QTSVE**: Table 2 reports σ₁²·d/((σ₁−σ₂)·ε²) + T_∇, while Theorem 3 gives r·σ₁³·d/((σ₁−σ₂)·ε²). These differ in the presence/absence of the rank r and the power of σ₁ (² vs ³).

   **QPM**: Table 2 reports √(σ₁²·d)/((1−σ₁γ'_min)·ε³) + T_∇ (= σ₁√d/((1−σ₁γ'_min)·ε³)), while Theorem 4 gives √r·σ₁⁴·d/((1−σ₁)³·γ_min²·⁵). These disagree on d-dependence (√d vs d), σ₁ power (1 vs 4), and denominator structure ((1−σ₁γ'_min) vs (1−σ₁)³·γ_min²·⁵).

   For a theory paper where these bounds are the sole evidence for the contribution, this internal inconsistency is debilitating. A reader cannot determine which expression is correct, and the speedup claims cannot be evaluated without resolving it.

2. **The claimed "at least O(√d) speedup" for the matrix case does not clearly follow from the stated bounds.** Using either version:
   - With Theorem 3's expression: classical/quantum ratio ≈ d·ε/(r·σ₁²). For r = Θ(1) this gives O(dε) speedup, not O(√d). For r = Θ(d) the ratio is O(ε/σ₁²) with no d-speedup at all.
   - With Table 2's expression: ratio ≈ d·ε/σ₁², giving O(dε) speedup — again not O(√d).
   
   The headline claim (abstract, line 48) thus overstates what the paper's own formulae support, making it unsupported as written.

3. **The σ_max ≤ 1 normalization in Lemma 8 is not addressed for Theorem 4.** The quantum power method subroutine (Lemma 8, line 282) explicitly requires σ_max ≤ 1. For M = ∇f(X_t) this is not guaranteed. The normalization required to meet this assumption propagates into Theorem 4's complexity bound, where the denominator (1−σ₁(M_t))³ assumes σ₁ is close to 1 after normalization — potentially making the bound very large or vacuous. This gap is not discussed.

### Minor

1. **Tomography cost derivation is opaque.** Lemma 6 (ℓ₂ tomography) costs O(d·log d/δ²) per copy. Theorem 3 sets δ_t = C₁/(2(t+2)σ₁(M_t)), so tomography cost scales as O(d·t²·σ₁²) per iteration. The paper does not trace how this combines with QSVE and maximum-finding costs to yield the final bound. The d factor in Theorem 3 presumably comes from tomography, but the derivation chain from Lemmas 5→7→Theorem 3 is not reconstructible from the main text.

2. **The γ'_min factor in Theorem 4 could be problematically small.** γ'_min is defined as the lower bound of ‖(M_tᵀM_t)ⁱb‖ over all power iterations. If the initial random vector has negligible overlap with the top singular vector (which can happen with constant probability when singular values are close), γ'_min could be exponentially small, making the 1/γ_min²·⁵ factor in Theorem 4's complexity astronomically large. The paper acknowledges "higher sensitivity on solution precision" (line 49) but provides no quantitative analysis.

3. **Notation inconsistencies for curvature constants.** The paper uses C_t (Theorem 1), C_T (Theorems 1, 2), C_f (Section 2.1), C_1 (Theorem 3, Algorithm 3), and C_L (Theorem 4, Algorithm 4) for what appear to be the same or similar curvature constants without clear definitions relating them. This makes the parameter settings difficult to evaluate from the main text.

4. **Abstract's ambiguous query complexity expression.** The abstract states O(√(d/ε)), which could be read as O(√d/ε) (which matches the paper's later claims, e.g., line 41: Õ(√d/ε)) or as O(√(d/ε)). These differ substantially and should be disambiguated.

### Trivial
None.

## Nice-to-Haves
- A worked example or concrete parameter regime showing when the matrix-domain speedup materializes (e.g., "for rank-O(1) gradients with eigengap Δ = Ω(1), the per-iteration complexity is Õ(d/ε²) vs classical O(d²/ε)").
- A brief derivation sketch in the main text showing how ℓ₂ tomography costs combine with QSVE/QPM to produce the final bounds.

## Removed Points
- Formatting corruption in Table 1 ("$O(\sum_{g \in [g]}  g )$") — this is a parser artifact from the PDF extraction, not an author error.
- Missing appendix content and proofs — the parser strips these sections; they exist in the original submission.
- Requests for experiments or empirical validation — outside the scope of a pure theory paper.
- The characterization of the tomography gap as "fatal" — the theorem bounds appear to include these costs; the issue is presentation transparency rather than a missing term.
- Claim about C_t/(√d L(t+2)) being problematic — C_t is bounded by the global curvature C_f, so the error propagation is standard FW analysis.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Reconcile Table 2 with Theorems 3 and 4.** Choose one correct expression for each algorithm, derive it transparently from the constituent subroutines (QSVE cost + maximum finding + tomography cost), and display it identically in both the table and the theorem statement. This is prerequisite for the paper to be evaluable.
2. **Qualify the speedup claim for the matrix case.** Replace the blanket "at least O(√d) speedup" with a precise statement as a function of r, σ₁, σ₂, ε, and d, along with the conditions under which the speedup holds. A theoretically honest bound is more valuable than an overstated one.
3. **Discuss the σ_max ≤ 1 normalization requirement** for the QPM subroutine and its effect on Theorem 4's complexity bound. Explain how M = ∇f(X_t) is normalized and how the normalization factor propagates.
4. **Unify curvature notation** under a single symbol (e.g., C_f) throughout the paper, or define each variant explicitly.
5. **Fix the abstract's ambiguous O(√(d/ε))** to O(√d/ε) if that is the intended expression.

## Score and Decision

**Score: 4** (borderline reject)

**Decision: Reject**

**Rationale:** The paper's vector-domain contribution (ℓ₁ ball, simplex) is correctly analyzed and achieves a genuine O(√d) query speedup that is verifiable from the presented formulae. This part of the paper is publishable. However, the matrix-domain contribution — which accounts for half the claimed novelty — suffers from three verifiable problems that prevent acceptance: (1) the complexity bounds in Table 2 and Theorems 3/4 are inconsistent with each other, (2) the headline "at least O(√d) speedup" claim does not cleanly follow from either version of the bounds, and (3) the σ_max ≤ 1 normalization requirement for the QPM subroutine is not addressed. For a theory paper where the entire evidence consists of these bounds, such internal inconsistency and overclaiming are disqualifying in the current form. The paper could be acceptable after major revisions that reconcile the expressions, correct the speedup claims, and discuss the normalization gap.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>