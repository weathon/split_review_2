## Summary

This paper proposes quantum algorithms to accelerate the Frank-Wolfe (FW) linear subproblem for both vector-domain constraints (ℓ₁-ball, simplex, latent group norms) and matrix-domain constraints (nuclear norm). For the vector case, it achieves O(√d/ε) query complexity using a function-value oracle, giving a quadratic improvement over the classical O(d) cost of scanning gradient components. For the matrix case, it presents two approaches—QTSVE-based (Theorem 3, Õ(rd/ε²)) and QPM-based (Theorem 4, Õ(√rd/ε³))—that target different rank regimes. This is the first systematic treatment of quantum-accelerated FW for both domains under general smooth convex functions.

## Strengths

- **First systematic study of quantum FW for both vector and matrix domains.** Prior work (Chen & de Wolf, 2023) was restricted to linear regression with closed-form gradients; this paper considers general smooth convex functions accessed via a function-value oracle, broadening the setting significantly.

- **Two complementary quantum approaches for the matrix case with explicit tradeoffs.** The QTSVE-based algorithm (Theorem 3) and the QPM-based algorithm (Theorem 4) target different regimes (high-rank vs. low-rank gradient matrices), with distinct dependencies on rank, precision, and spectral properties. This is a more nuanced treatment than offering a single approach.

- **Error propagation analysis connecting quantum subroutine errors to FW convergence guarantees (Section 3.1).** The paper tracks how gradient approximation error (from finite-difference estimation) propagates through the linear subproblem and into the overall FW convergence bound via Hölder's inequality. This is technically nontrivial and gives the analysis credibility.

## Weaknesses

### Fatal
None.

### Major

- **The quantum data structure construction cost is unaccounted for in the matrix-case complexity.** The quantum algorithms for the matrix domain (Theorem 3, Theorem 4) require quantum access to the gradient matrix via Assumption 4, which presupposes a specific data structure. The construction (or per-iteration reconstruction) of this data structure has cost O(d² log d) (Kerenidis & Prakash, 2020b). Since the gradient M_t changes each FW iteration, this overhead is incurred every round. The complexity bounds in Table 2 and Theorem 3/4 include T_∇ (gradient evaluation time) but not this data-structure cost. For dense matrices, the O(d²) overhead per iteration could dominate the claimed Õ(d) or Õ(√rd) update cost, eroding the practical speedup. The paper is transparent about focusing on the update step (Section 4, Remark 3), but this gap significantly affects how the total per-iteration cost compares with the classical baseline.

- **The QPM complexity bound (Theorem 4) depends on a poorly characterized parameter γ′_{\min}.** The time complexity is Õ(√r σ₁⁴(M_t)d / ((1−σ₁(M_t))³ γ′_{\min}²·⁵)), where γ′_{\min} is the lower bound of ‖(M_t^⊤ M_t)^i b‖ over all i ∈ [k]. The paper states this "depends on the relation of the singular value distribution of the gradient matrix and the direction of the initial vector" (Table 2 caption) and does not bound it in terms of standard spectral quantities (e.g., spectral gap, condition number). The classical power method's analysis involves the spectral gap (σ₁−σ₂) but requires no analogous parameter. The γ′_{\min}^{−2.5} dependence makes the claimed advantage over classical methods less clean, and the practical regime where this bound translates to a genuine speedup is unclear.

### Minor

- **The vector-case speedup claim compares quantum query complexity against classical computational cost, which are different resource measures.** The quantum O(√d) counts calls to the function-value oracle U_f (each requiring coherent arithmetic and state preparation), while the classical O(d) counts comparisons of already-computed gradient entries—a fundamentally cheaper operation. The paper's abstract states the algorithms "outperform the optimal classical methods in dependence on the dimension d" without noting this asymmetry. While this framing is standard in quantum algorithms theory, it gives a misleading impression of the nature and magnitude of the advantage.

- **The claimed speedup for Algorithm 3 (line 243) depends on parameter relationships that may not hold.** The factor reduction over the classical power method is stated as O(dε / rσ₁²(M)), which requires dε ≪ rσ₁²(M) for the quantum method to be faster. The paper does not discuss when this condition is satisfied in practice, nor does it provide guidance for when practitioners should prefer one method over the other.

### Trivial

- Table 1 and Table 2 contain formatting artifacts (e.g., missing ℓ₁ notation in Table 1, garbled denominators in Table 2) that are likely parser-induced but should be verified in the final version.

## Nice-to-Haves

- A worked resource estimate (using standard fault-tolerant quantum cost models) quantifying crossover points in d and ε where the quantum algorithm's total cost—including state preparation, tomography, and data-structure overhead—drops below the classical baseline, would substantially strengthen the paper's claims.
- Characterizing γ′_{\min} in terms of standard spectral quantities (condition number κ or spectral gap Δ) would make the QPM bound more interpretable and comparable to the classical analysis.
- A brief discussion of the cost of rebuilding the quantum-access data structure each iteration for the matrix case would give a more complete picture of the total complexity.

## Removed Points

- **"Gradient computation is excluded from the comparison"** (part of Critical Issue 2): Removed because Table 2 explicitly includes T_∇ in all complexity expressions. The quantum and classical methods both include T_∇, so this specific sub-claim is factually incorrect.
- **State preparation inverse operation / coherent control across iterations**: Removed because these are speculative concerns not concretely identified in the paper.
- **Non-uniform case success probability p (Lemma 4) not specified**: Removed because this is a question, not a demonstrated weakness.
- **Literature cross-check against Chen et al. (2025a)**: Removed because the paper itself acknowledges this concurrent work.
- **Formatting and table rendering issues**: Removed per rules (parser artifacts, not author errors).
- **Missing related works**: Removed per rules (cannot verify external literature from the paper alone).
- **General speculation about constant factors and log overheads**: Removed because these are generic concerns that apply to nearly all quantum algorithms papers and are not specific to this work.

## Novel Insights

None beyond the paper's own contributions. The input review surfaces a useful framing distinction between oracle-query speedup and practical speedup, and correctly identifies the QRAM data-structure cost as a concrete gap in the matrix-case analysis—but these are elaborations of standard concerns in quantum algorithms, not genuinely novel observations.

## Suggestions

- Add a brief discussion (or a short table) of the per-iteration data-structure reconstruction cost for the matrix case, and state explicitly how it compares to the classical matrix-storage cost.
- Bound γ′_{\min} in terms of the spectral gap (σ₁−σ₂) and the condition number κ for the QPM case, or at least discuss when γ′_{\min} is expected to be small/large.
- Clarify in the abstract and introduction that the vector-case speedup is in query complexity to a function-value oracle, and note that the classical O(d) baseline is for gradient-component comparison (a cheaper per-operation cost).

## Score and Decision

This paper makes a technically competent and novel contribution—it is the first systematic study of quantum-accelerated Frank-Wolfe algorithms for both vector and matrix domains. The algorithms are correctly specified, the convergence analysis is sound, and the treatment of two complementary matrix-case approaches is a genuine strength.

However, the significance of the claimed speedups is materially less than the abstract and comparison tables suggest. For the matrix case, both quantum approaches require a specialized quantum-access data structure whose per-iteration construction cost (O(d²)) is not accounted for, and the QPM bound depends on a non-standard parameter γ′_{\min} whose behavior is not characterized. For the vector case, the speedup is measured in query complexity against a classical baseline that performs a simpler operation (component comparison). These gaps do not invalidate the paper's technical correctness, but they substantially reduce the practical import of the results as framed.

The paper would be a strong contribution to a theory-focused venue. For ICLR, where the bar for significance includes the gap between theoretical speedup and practical import, the paper falls short in its current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>