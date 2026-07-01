## Summary

This paper proposes quantum variants of the Frank-Wolfe algorithm for projection-free sparse convex optimization. For the vector domain (ℓ₁-ball, simplex, latent group norms), it achieves Õ(√d/ε) query complexity via finite-difference gradient approximation combined with quantum maximum finding. For the matrix domain (nuclear norm), it proposes two approaches—quantum top singular vector extraction (QTSVE) and quantum power method (QPM)—with claimed time complexities of Õ(rd/ε²) and Õ(√(rd)/ε³) for the update step.

## Strengths

- **Clean vector-case result (Theorems 1, 2).** Combining finite-difference gradient approximation (Lemma 3) with quantum maximum finding (Lemma 4) yields Õ(√d) per-iteration query complexity versus classical O(d) for ℓ₁-ball and simplex constraints. Algorithm 2 and the convergence analysis are clearly presented.
- **Well-structured error propagation.** Lemma 2 bounds the ℓ₂ finite-difference error, converted to ℓ_∞ error for the max-finding subroutine, with parameter choices σ_t = C_t/(√d L(t+2)) that accumulate correctly across T iterations to achieve the target ε.
- **Novel subroutine for latent group norms (Theorem 6).** Computing dual norms coherently across groups in quantum superposition and identifying the dominant group via quantum maximum finding goes beyond the simple coordinate-max case and represents a non-trivial algorithmic contribution.

## Weaknesses

### Fatal

None.

### Major

1. **Inconsistency between Theorem statements and Table 2 complexity expressions.** The complexity expressions for the matrix-case algorithms differ substantially between the theorem statements and Table 2, making the core quantitative claims unverifiable:
   - **Theorem 3 (line 241):** Õ(r σ₁³(M_t) d / ((σ₁-σ₂)ε²)) — **Table 2 QTSVE (line 88):** Õ(σ₁²(M)d / ((σ₁-σ₂)ε²) + T∇). These differ in the presence of the rank factor r and the exponent of σ₁ (³ vs ²).
   - **Theorem 4 (line 294):** Õ(√r σ₁⁴(M_t)d / ((1-σ₁)³ γₘᵢₙ²·⁵)) — **Table 2 QPM (line 89):** Õ(√(σ₁²(M)d) / ((1-σ₁ γ'ₘᵢₙ)ε³) + T∇). These differ in the exponent of σ₁ (⁴ vs ¹), the denominator form ((1-σ₁)³ vs (1-σ₁γ'ₘᵢₙ)), and critically, Theorem 4's expression does not contain ε explicitly while Table 2 has ε³. A reader cannot determine which expression is correct, which undermines the paper's central quantitative claims for the matrix case.

2. **Matrix-case speedup claim is misleading for QTSVE.** The abstract (line 9) and contributions (line 48) state that the matrix-case algorithms achieve "at least a factor of O(√d) over the best classical algorithm." However, comparing QTSVE against the Lanczos method (the state-of-the-art classical method, also listed in Table 2) shows both have O(d) dimension scaling (Lanczos: O(d/ε), QTSVE: O(d/ε²)), with QTSVE having worse ε-dependence. The √d speedup materializes only when comparing against the Power Method (O(d²)), not against the best classical method. QPM does achieve √d vs d scaling over Lanczos, but with ε⁻³ vs ε⁻¹ deterioration and a denominator (1-σ₁γ'ₘᵢₙ) that could negate the advantage in worst cases. The claims should be restated per-algorithm with these tradeoffs acknowledged.

### Minor

3. **QPM's γ'ₘᵢₙ dependence is a potential weakness not discussed.** Lemma 9 (line 286) and Theorem 4 (line 294) require a lower bound γ'ₘᵢₙ on ‖(M^T M)^i z‖ for all i ∈ [k]. This quantity can be exponentially small in k if the starting vector has negligible overlap with the dominant eigenvector, potentially making the cost prohibitive. The classical power method avoids this by normalizing at each step—the Rayleigh quotient converges regardless of intermediate norms. This meaningful difference between the quantum and classical versions is not discussed.

4. **Tomography cost means the O(d) factor comes from classical post-processing.** Both QTSVE and QPM require Õ(d log d / δ²) cost for ℓ₂-norm quantum state tomography (Lemma 6, line 233) to extract d-dimensional classical vectors u, v. This is the same O(d) output cost as the classical Lanczos method. The quantum advantage is in the number of matrix accesses or operations, not in avoiding O(d) output cost. This should be explicitly acknowledged.

5. **Data structure overhead for the matrix case is not discussed.** Assumption 4 (line 221) requires a specific data structure with Õ(1) query time (Kerenidis & Prakash 2020b). For a gradient matrix M that changes each iteration, rebuilding this data structure costs O(d²) time per iteration—the same as reading the matrix classically. While treated as preprocessing in the quantum algorithms literature, this overhead merits explicit acknowledgment.

### Trivial

6. **Notation issue in Theorems 1 and 2.** The theorems (lines 187, 195) use C_T and C_t without defining either. These presumably refer to the curvature constant C_f, but the notation is inconsistent.

## Nice-to-Haves

- Numerical validation on synthetic data (even small-scale simulations) would increase credibility. While the paper is theoretical, such validation is common in the quantum algorithms literature.
- A more detailed discussion of the qubit and gate cost for the Jordan's gradient estimation approach (Theorem 5) would help assess practical feasibility.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Problem choice is well-motivated" (Strength 1 from input):** Removed per rule — this is a generic strength about the importance of the problem, not a specific contribution of this paper.
- **"Gradient evaluation cost may dominate" (Issue 3 from input):** Removed — the paper explicitly follows the standard convention (Jaggi 2013) of excluding gradient evaluation time and includes +T∇ for both classical and quantum methods in Table 2, making the comparison apples-to-apples. The concern is speculative and the paper is transparent about this modeling choice.
- **"No empirical validation" (from Missing Parts):** Moved to Nice-to-Haves — this is not a standard requirement for theory papers.
- **"Parser artifact in latent group table" (from Missing Parts):** Removed — this is a parser artifact affecting table formatting, not an author error.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the inconsistency between Theorem 3/4 and Table 2 by deriving one coherent expression per quantum algorithm, verified against the lemma-level analysis.
2. Restate the matrix-case speedup claims per-algorithm: acknowledge that QTSVE has the same dimension scaling as Lanczos, and discuss the ε and eigengap tradeoffs for QPM explicitly.
3. Add a discussion of the γ'ₘᵢₙ dependence in QPM and its potential to become exponentially small.
4. Clean up the C_T / C_t notation in Theorems 1 and 2.

## Score and Decision

**Score:** 4.0
**Decision:** Reject (borderline)

The vector-case results (Theorems 1, 2, 6) are solid contributions and the error propagation analysis is well-structured. However, the matrix-case results—which form half of the paper's claimed contributions—have verifiable problems: the inconsistency between theorem statements and Table 2 makes the central quantitative claims unverifiable, and the speedup claims are misleading when compared against the best classical method (Lanczos). These issues are significant enough that the paper cannot be accepted in its current form. A revised version fixing these issues could be a strong submission.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>