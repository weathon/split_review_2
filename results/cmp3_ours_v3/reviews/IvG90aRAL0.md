## Summary

This paper proposes quantum Frank-Wolfe (conditional gradient) algorithms for projection-free sparse convex optimization, covering both vector-domain constraints (ℓ₁ ball, simplex, latent group norms) and matrix-domain constraints (nuclear norm ball). For the vector case, it achieves O(√d) quantum query complexity per iteration via Grover-style maximum finding over gradient components computed in superposition through finite-difference oracle queries. For the matrix case, it proposes two methods—quantum top singular vector extraction (QTSVE) and quantum power method (QPM)—with per-iteration complexities of Õ(rd/ε²) and Õ(√rd/ε³) respectively. The paper claims at least an O(√d) speedup over classical methods under favorable parameter regimes.

## Strengths

1. **Well-motivated problem domain.** The Frank-Wolfe method is the standard approach for structured constraints (ℓ₁ ball, nuclear norm ball) where projections are expensive, and the linear subproblem is the key bottleneck in high dimensions. The paper clearly positions its quantum acceleration of this step as a natural and relevant target, contrasting with prior work (Chen & de Wolf, 2023) that handles a narrower setting with an explicit closed-form gradient.

2. **Systematic treatment and honest accounting.** The paper covers both vector and matrix domains with multiple algorithmic variants and trade-offs, and reports not just query complexity but also qubit counts and gate counts (Tables 1 and 2). It flags where better query complexity comes at the cost of more qubits (Theorem 5's Jordan gradient estimation vs. Theorem 1's finite-difference approach)—good practice for a quantum algorithms paper.

3. **Error propagation analysis for the vector case.** The analysis connecting finite-difference gradient approximation error to FW convergence (the parameter setting σ_t = C_t / √(dL(t+2)) in Theorem 1) is a real analytical contribution beyond a trivial application of quantum max-finding. The extension to latent group norm constraints (Theorem 6) requires computing dual norms coherently in superposition, which is more technically involved than the ℓ₁ case.

## Weaknesses

### Major

1. **Matrix-case speedup is parametric and may collapse under unfavorable conditions.** The claimed "at least O(√d) speedup" (line 48) is conditional on problem-specific parameters that can be arbitrarily unfavorable. For QTSVE (Theorem 3), the complexity Õ(rσ₁³d/((σ₁−σ₂)ε²)) depends on the gradient rank r—if r ≈ d (dense gradient), this becomes O(d²), matching classical. The spectral gap σ₁−σ₂ can be arbitrarily small, making the denominator vanish. For QPM (Theorem 4), the complexity depends on γ′_min—the minimum value of ‖(M^⊤M)^i b‖ across all power iterations—which is hard to bound a priori and can be exponentially small in the worst case. The paper acknowledges the "sensitivity on solution precision" (line 49) but provides no probabilistic analysis or mitigation for γ′_min. The speedup is genuine only when r ≪ d and the spectral gap is sufficiently large, but this conditionality is not stated upfront and the blanket "at least O(√d)" framing overstates the robustness of the advantage.

### Minor

2. **Vector-case core results are a straightforward application of quantum maximum finding.** For the ℓ₁ ball and simplex, the linear subproblem reduces to finding argmax_i |∇f_i| over d items—exactly unstructured search. Applying quantum maximum finding (Durr & Hoyer, 1996) gives O(√d) queries, which is immediate to anyone familiar with both FW and quantum search. The paper's novelty for these specific cases is limited to the error propagation analysis (which is real but moderate in scope) and the finite-difference gradient estimation in superposition. The more novel vector result (latent group norms, Theorem 6) is deferred to the appendix.

3. **Oracle-model presentation asymmetry.** The paper compares classical "O(d) query complexity" (derived from Jaggi, 2013, which assumes a linear optimization oracle given the gradient) against quantum "O(√d) query complexity" measured in function-value oracle calls (Assumption 3). The O(√d) speedup does hold under a unified function-value oracle (classical would need O(d) function evaluations as the reviewer notes), but the paper does not make this alignment explicit. This does not invalidate the results but makes the comparison harder to parse cleanly.

### Trivial

4. **Tables could clarify oracle models.** Table 1 and 2 would benefit from footnotes explicitly stating which oracle model each complexity entry refers to.

## Nice-to-Haves

- A concrete worked example where the matrix-case conditions (small rank r ≪ d, bounded spectral gap) are known to hold simultaneously, to ground the theoretical speedup.
- A consolidated disclosure of all poly-log factors absorbed into Õ notation, to improve clarity of the final complexity statements.

## Removed Points

- **Criticism about Assumption 4 (QRAM) being unrealistic:** The paper states at line 217 that gradient evaluation time is excluded, following the classical convention (Jaggi, 2013). This is standard practice and acknowledged transparently. A reader familiar with the quantum algorithms literature will recognize the data structure from Kerenidis & Prakash (2020b) as the standard model. Removed because it mischaracterizes the paper's scope—the paper is not claiming the data structure comes for free; it is adopting the same convention as the classical baseline.

- **"Apples to oranges comparison" framed as structural/fatal:** The reviewer's own analysis acknowledges the speedup holds under a unified oracle model ("the O(√d) speedup holds"). The asymmetry is a presentation issue, not a structural flaw. Demoted to Minor.

- **Section-by-section notes about Lemma 2's ℓ₂ vs ℓ_∞ error and QSVE search space:** These are observations about presentation choices that the paper handles implicitly. Not genuine weaknesses.

- **"Missing numerical illustration":** Not expected for a pure theory paper in this community.

- **"Comparison with Chen et al. (2025a) should be deeper":** The paper provides a comparison on line 53. A deeper comparison would be desirable but its absence is not a weakness given the paper's scope.

## Novel Insights

None beyond the paper's own contributions. The merged review surfaces two calibrated concerns: (1) the matrix-case speedup is parametric in ways that a reader skimming the abstract will not appreciate, and (2) the vector-case contribution is narrower than its framing suggests, since the ℓ₁/simplex results are a direct application of a known quantum primitive. These are real constraints on the paper's overall significance but do not challenge the correctness of the results.

## Suggestions

1. **Restate the matrix-case speedup conditionally** in the abstract and contributions. Replace "at least O(√d) speedup" with "a speedup of at least O(√d) when the gradient matrix has rank r ≤ √d and a spectral gap bounded below by a constant." This would accurately reflect what the theorems show.

2. **Align the oracle-model comparison in Table 1.** Either measure both classical and quantum against the same function-value oracle, or add an explicit footnote explaining what each column counts.

## Score and Decision

**Calibration anchors (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Quantum Algorithm for Sparse Online Learning | 4.80 | 2 | Similar quantum speedup over dimension d; our paper has broader scope (vector + matrix) but the vector-case novelty is comparable |
| Quantum Speedups in Linear Programming | 5.33 | 2 | Incremental algorithmic improvement; our paper's speedup is more conditional but the systematic treatment is broader |
| Catalyst Framework for QLSP | 5.25 | 2 | Meta-algorithm with condition-number limitations; comparable level of parametric dependence |
| Near-Optimal Quantum Min-Max | 6.00 | 2 | Clean speedup with matching lower bound; stronger contribution overall than our paper |

**Round 1 bracket:** [4.5, 5.5]  
**Round 2 narrowing:** The paper sits between the 4.80 (Sparse Online Learning, Reject) and 5.33 (Quantum LP, Reject) anchors. It has broader scope than both but the matrix-case speedup is more conditional than either comparison paper's claims. The vector-case novelty is limited. I place it at 5.0.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>