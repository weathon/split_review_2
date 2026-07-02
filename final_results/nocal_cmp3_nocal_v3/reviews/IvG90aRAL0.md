## Summary

This paper proposes quantum variants of the Frank-Wolfe algorithm for projection-free sparse convex optimization in both the vector domain (ℓ₁-ball, simplex, latent group norm) and the matrix domain (nuclear norm ball). For the vector case, it gives quantum algorithms achieving query complexity Õ(√d/ε) and O(1/ε) using a function value oracle, reducing a factor of O(√d) and O(d) over classical algorithms. For the matrix case, it presents two complementary approaches—QTSVE and QPM—with per-update-step time complexities of Õ(rd/ε²) and Õ(√rd/ε³), claiming at least an O(√d) speedup over classical methods. The paper is a theoretical contribution with no experimental evaluation.

## Strengths

- **Addresses a genuinely open question.** Quantum acceleration of the Frank-Wolfe linear subproblem—the bottleneck in high-dimensional FW optimization—is not a saturated area, and the paper provides the first systematic treatment across multiple constraint types (ℓ₁-ball, simplex, nuclear norm ball, latent group norm).

- **Two complementary approaches for the matrix case.** QTSVE and QPM target different regimes (low-rank vs. high-rank gradient matrices), and the paper explicitly discusses the trade-off between them, showing awareness that no single quantum subroutine dominates in all settings.

- **Honest about assumptions.** The paper states its quantum access models (function value oracle for the vector case; quantum matrix access via a specific data structure for the matrix case) and explicitly notes where it follows the classical convention of excluding gradient evaluation time.

## Weaknesses

### Major

- **Inconsistency between Table 2 and the theorem statements in the main text.** This is the most concrete and verifiable flaw.  
  *Theorem 3*: Table 2 (line 88) gives Õ(σ₁²(M) d / ((σ₁(M)−σ₂(M)) ε²) + T\_∇), while the theorem text (line 241) gives Õ(r σ₁³(M_t) d / ((σ₁(M_t)−σ₂(M_t)) ε²)). The exponent of σ₁ differs (2 vs. 3) and the rank factor r is missing from the table.  
  *Theorem 4*: Table 2 (line 89) gives Õ(√(σ₁²(M) d) / ((1−σ₁(M)γ′\_{min}) ε³) + T\_∇), while the theorem text (line 294) gives Õ(√r σ₁⁴(M_t) d / ((1−σ₁(M_t))³ γ\_{min}²·⁵)). The expressions are structurally different—different powers of σ₁, different denominator forms, and the √r factor is absent from the table.  
  A reader consulting the table to compare against classical baselines will reach different conclusions than one reading the theorems. These must be reconciled.

- **Parameter-setting circularity in the matrix-case theorems.** Theorem 3 (line 241) sets δ_t = C₁/(2(t+2)σ₁(M_t)) and ε_t ≤ (σ₁(M_t)−σ₂(M_t))/2. Theorem 4 (line 290) sets k_t = 2C₀σ₁(M_t) ln d / ε and δ_t, δ′_t that depend on σ₁(M_t) and γ′\_{min}. These parameters depend on σ₁(M_t), σ₂(M_t), and γ′\_{min}—precisely the quantities the quantum subroutines are designed to discover. The paper references "Remark 2" for parameter choosing, but the main text does not explain how these can be set without prior knowledge of the spectrum, nor does it provide an adaptive scheme. If a practical implementation must estimate these quantities, the stated complexity bounds may not be achievable without additional overhead.

### Minor

- **The state-preparation claim is potentially misleading.** The paper states (lines 167–168) that the state-preparation overhead is "completely decoupled from the potentially large dimension d." This refers only to gate complexity per iteration. The qubit count remains O(d) (Table 1), and the total space complexity still scales with dimension. Clarifying this distinction would prevent misinterpretation.

- **The matrix-case speedup analysis does not address the cost of loading the gradient into the quantum data structure.** The paper properly scopes its analysis to the update-direction computation and follows the classical convention of excluding gradient evaluation time (line 217). However, Assumption 4 requires the gradient to be stored in a specific quantum-accessible data structure, and the cost of loading a dense d×d matrix into this structure (O(d² log d) preprocessing) is not discussed. While excluding gradient evaluation is standard, the data-structure loading cost is a quantum-specific overhead that does not have an exact classical analogue and should be acknowledged when interpreting total per-iteration cost.

- **The claimed "at least O(√d) speedup" for the matrix case is stated without qualification about the regimes where it holds.** The speedup factor depends on spectral properties (singular value gaps, rank r, overlap γ′\_{min}) that vary across problem instances. For example, QTSVE's complexity depends on p = σ₁²/∑σᵢ², which can be as small as 1/d when singular values decay slowly, weakening the advantage. The paper should more precisely characterize when each speedup materializes.

### Trivial

- The latent group row in Table 1 (line 67) contains garbled notation (e.g., O(∑\_{g∈[g]} g)) that makes the classical baseline unverifiable. This should be fixed.

## Nice-to-Haves

- Theorems 3 and 4 would be strengthened by either (a) an adaptive parameter-estimation scheme that pays bounded overhead, or (b) a proof that worst-case bounds using known quantities (L, D) suffice, even if looser.
- A brief discussion of when the quantum function-value oracle (Assumption 3) is realistic for practical objectives (e.g., Lasso, SVM dual) would help ground the vector-case contributions.
- Including a one-sentence explanation of the qubit counts in the main text would aid readability.

## Removed Points

- **"Matrix-case speedup claim compares a sub-component, not full cost"** — The paper explicitly scopes to update-direction computation (line 217: "analysis focuses on the update direction computation") and Table 2's header reads "Complexity of the Update Computing." Both classical and quantum entries include T\_∇ additively, so the comparison is fairly scoped. The concern is addressed in Minor weakness 2 above but does not warrant "structural" or "critical" status.
- **"Vector-case gradient error analysis has circular parameter choices"** — The reviewer's detailed algebraic derivation merges constants C_t, C_T, and C_f in ways that cannot be verified without the full proof (Appendix B.3, stripped by the parser). The notation could be clarified, but the claim of a fatal circularity is speculative from the main text alone.
- **"Abstract overstates generic speedup"** — The abstract distinguishes the main result (function value oracle) from the Lipschitz-continuous + Jordan algorithm variant. This is adequately handled.
- **"QTSVE worst-case analysis under slow singular value decay"** — The reviewer's own calculation extrapolates from stated formulas but does not identify an error in the paper. The claim would need to be checked against the full proof.
- **Various section-by-section observations** that are commentary rather than verifiable weaknesses (e.g., "preliminaries are clean," "algorithm description is clear").

## Novel Insights

None beyond the paper's own contributions. The reviews identify specific gaps in presentation (table/theorem inconsistency, parameter-setting circularity) but do not surface a fundamentally new analytical insight about the paper's core claims.

## Suggestions

1. **Reconcile Table 2 and the theorem statements.** This is the single most impactful fix. Every entry in Table 2 should match the corresponding theorem exactly. If the table simplifies (e.g., omits r or uses different σ₁ exponents to show a cleaner comparison), the relationship between the simplified and exact forms should be explained in a footnote.
2. **Address the parameter-setting problem.** Add a paragraph in Section 4 discussing how σ₁(M_t), σ₂(M_t), and γ′\_{min} can be estimated or bounded adaptively, or show that worst-case bounds suffice.
3. **Add a brief discussion of the data-structure loading cost.** Even a sentence acknowledging that loading a dense gradient into the Assumption-4 data structure costs O(d² log d) would give readers a complete picture of total per-iteration cost.
4. **Clarify the "completely decoupled from d" statement** by noting that it refers to gate complexity per iteration, not qubit count.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>