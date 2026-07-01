Now let me finalize the review with proper calibration.

## Summary

This paper proposes quantum Frank-Wolfe algorithms for projection-free sparse convex optimization in both vector and matrix domains. For the vector domain (ℓ₁-ball, simplex), it achieves Õ(√d/ε) query complexity using a function-value oracle, giving a quadratic speedup over classical O(d). For latent group norms, a Õ(√|G|) speedup is claimed. For the matrix domain (nuclear norm constraints), two quantum methods are proposed—one based on quantum singular value estimation (QTSVE) and one based on a quantum power method (QPM)—with claimed time complexities of Õ(rd/ε²) and Õ(√rd/ε³) for computing the update direction.

## Strengths

1. **Clean speedup in the vector ℓ₁/simplex case (Theorems 1–2).** The integration of quantum max-finding (Durr & Hoyer) on finite-difference gradient estimates to avoid scanning all d coordinates is well-motivated and technically sound. The error propagation analysis (finite-difference accuracy → max-finding tolerance → Frank-Wolfe convergence) is properly structured. The sparsity of FW iterates (at most t nonzeros after t iterations) justifies efficient state preparation decoupled from dimension d.

2. **Systematic treatment across multiple constraint types.** The paper provides two approaches per domain (function-value-oracle-based and Jordan-gradient-based for vectors; QTSVE and QPM for matrices) and extends to latent group norm constraints, offering breadth beyond prior quantum FW work that only handled linear regression with closed-form gradients.

3. **First quantum treatment of the matrix FW linear subproblem.** The paper correctly identifies that the nuclear-norm FW subproblem reduces to extracting top singular vectors, and adapts existing quantum primitives (QSVE, quantum matrix-vector multiplication) to this setting. The acknowledgment of concurrent independent work (Chen et al. 2025a) is appropriate.

## Weaknesses

### Major

1. **Uncharacterized parameter γ′\_{min} in the QPM complexity (Theorem 4).** The stated per-round complexity is Õ(√r σ₁⁴(M_t) d / ((1−σ₁(M_t))³ γ\_{min}^{2.5})), where γ′\_{min} = min_i ‖(M_t^⊤ M_t)^i b‖ is the lower bound of the power iteration vector norm across all iterations. This is not a problem-instance constant — it depends on the random draw of the initial vector b and the iteration depth k. The abstract and introduction advertise a clean Õ(√rd/ε³) complexity, but the theorem's expression does not contain ε explicitly, and the ε-dependence is absorbed into γ′\_{min} in a way that is not obvious from the stated formula. Without a concrete high-probability lower bound on γ′\_{min} (e.g., via standard randomized power-method analysis showing Ω(1/√d) overlap with the top singular vector), the complexity statement is a function of an unobservable quantity and cannot be meaningfully compared to classical bounds. **Evidence:** Lines 289–294 state Theorem 4 with γ′\_{min} in the denominator; line 9 and line 48 state the abstract's Õ(√rd/ε³) without this dependence.

2. **Missing analysis of quantum data-structure initialization and update (Assumption 4).** The matrix-case algorithms assume the gradient matrix M is stored in a quantum-accessible data structure (Assumption 4, lines 221–222) that supports Õ(1) queries, referencing Kerenidis & Prakash (2020b). The paper does not discuss how this data structure is initialized or, crucially, how it is updated across FW iterations when the gradient changes. The classical baselines (power method, Lanczos) require O(d²) per matrix-vector multiplication and do not need a special data structure. If the quantum data structure must be rebuilt from scratch each iteration, the O(d²) cost would dominate the claimed per-round complexities of Õ(rd/ε²) and Õ(√rd/ε³). The paper states it "follows the classical convention of excluding gradient evaluation time" (line 217), but the classical power method does not require storing the gradient in a specialized data structure — this is an extra requirement specific to the quantum approach.

3. **Inconsistent QPM complexity expressions.** Table 2 (line 89) states the QPM update complexity as Õ(√(σ₁²(M)d) / ((1−σ₁(M)γ′\_{min})ε³) + T_∇), while Theorem 4 (line 294) states it as Õ(√r σ₁⁴(M_t)d / ((1−σ₁(M_t))³ γ\_{min}^{2.5})). These expressions differ in their functional form—the former has √d in the numerator and a single power of (1−σ₁γ′\_{min}) in the denominator, while the latter has d and (1−σ₁)³ γ\_{min}^{2.5} in the denominator. The abstract claims Õ(√rd/ε³), which matches neither expression exactly. This inconsistency creates confusion about which complexity bound is authoritative.

### Minor

4. **Latent group norm comparison involves different aggregate quantities (Table 1).** The classical complexity is O(Σ_g |g|) (total features across all groups) while the quantum complexity is O(√|G|·|g|_max) (square root of number of groups times largest group size). These are different aggregates; the claimed O(√|G|) speedup assumes |g|_max is not significantly larger than the average group size. If one group dominates (|g|_max ≈ Σ|g|), the quantum complexity could be larger. This nuance is not discussed.

5. **Spectral gap dependence in matrix-case theorems.** The complexities of Theorems 3 and 4 include (σ₁−σ₂) or (1−σ₁) in denominators, but the paper does not discuss how to estimate this gap a priori or at what additional cost it can be obtained. This is a common limitation in spectral methods but limits the practical applicability of the stated bounds.

### Trivial

None.

## Nice-to-Haves

- Provide a rigorous high-probability lower bound on γ′\_{min} in terms of d, ε, and spectral gap, using standard randomized power-method analysis.
- Discuss how the quantum data structure in Assumption 4 is initialized and updated per FW iteration, including any cost amortization.
- Reconcile the inconsistent complexity expressions for QPM across the abstract, Table 2, and Theorem 4.
- Consider extending the function-value oracle model (used in the vector case) to the matrix case for a unified treatment, as mentioned in line 217.

## Removed Points

- **QTSVE non-uniform max-finding criticism:** Removed because the paper already accounts for the non-uniform amplitude distribution via Lemma 7, where the complexity includes a factor 1/√p = ‖M‖_F/σ₁. This propagates through Theorem 3 via the rank-dependent expression ∥M∥_F²/σ₁ ≤ rσ₁. The paper explicitly notes this (line 181) and Appendix B.2 provides a proof.
- **Qubit scaling concern:** Removed as a near-term hardware critique not relevant to asymptotic complexity analysis, which is the paper's proper frame.
- **Formatting/table-garbling complaints:** Removed as parser artifacts.
- **Generic strength about "important problem":** Removed as non-specific.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Bound γ′\_{min} rigorously in Theorem 4, or restate the complexity with ε explicit and γ′\_{min} resolved.
2. Add discussion of how the quantum data structure for the gradient matrix is maintained across FW iterations, including per-iteration cost.
3. Unify the QPM complexity expressions in the abstract, Table 2, and Theorem 4.
4. Qualify the abstract's Õ(√rd/ε³) claim with the caveat that it depends on the uncharacterized parameter γ′\_{min} in the full theorem.
5. Add a note about the latent group norm comparison caveat (dominant group scenario).

## Score and Decision

**Calibration anchors (all retrieved):**
- `XABvLUXQ45` (avg 4.80, Reject): Quantum sparse online learning. Weaker novelty; the current paper has a cleaner vector-case contribution but similar gaps in completeness.
- `XaARrKTNh3` (avg 5.25, Reject): Catalyst framework for QLSP. Solid theory; reviewer noted incremental contribution.
- `rUx0zQFwD1` (avg 5.33, Reject): Quantum LP via Gibbs sampling. Technical improvement but presentation issues.
- `pB1FeRSQxh` (avg 6.00, Accept): Near-optimal quantum max-loss. Clean results with matching lower bounds; more complete than the current paper.

**Round 1 bracket:** [4.8, 6.0]. The paper's vector case is cleaner than the 4.80 anchor, but the matrix case gaps are significant enough to prevent reaching the 6.00 level.

**Final reasoning:** The vector case (Theorems 1–2) is a genuine, well-reasoned contribution that yields a clean O(√d) query complexity speedup. However, the matrix case — presented as a core contribution and a key differentiator from prior work — has two unresolved issues: (1) the QPM complexity (Theorem 4) depends on an uncharacterized parameter γ′\_{min} that is never bounded in terms of accessible quantities, making the advertised Õ(√rd/ε³) unsupported; (2) the quantum data structure cost for storing/updating the gradient matrix across FW iterations is not accounted for. The inconsistent QPM expressions (abstract vs. Table 2 vs. Theorem 4) compound these concerns. A revised version that addresses these gaps could merit acceptance, particularly if the matrix-case claims are either tightened or scoped more carefully.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>