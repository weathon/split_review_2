## Summary

This paper presents the first systematic study of quantum acceleration for the Frank-Wolfe (FW) linear subproblem under both vector-domain constraints (ℓ₁ ball, simplex, latent group norm) and matrix-domain constraints (nuclear norm). For the vector case, it achieves O(√d/ε) query complexity via quantum maximum finding on finite-difference gradient approximations. For the matrix case, it proposes two quantum subroutines—quantum top singular vector extraction (QTSVE) and quantum power method (QPM)—achieving time complexities of Õ(rd/ε²) and Õ(√rd/ε³) respectively for computing the update direction, improving dimension dependence over classical methods at the cost of worse precision dependence.

## Strengths

1. **First quantum treatment of the matrix-case FW linear subproblem (Section 4).** Prior quantum FW work (Chen & de Wolf, 2023) only addressed the vector case with closed-form gradients. Extending quantum speedups to nuclear-norm constraints requires fundamentally different subroutines (top singular vector extraction), and the paper provides two concrete approaches (QTSVE and QPM) with complete complexity analyses (Theorems 3, 4). This is a genuine extension beyond known results.

2. **Systematic treatment across two domains under a unified framework with transparent tradeoffs.** The paper covers vector (ℓ₁ ball, simplex, latent group norm) and matrix (nuclear norm) settings under the same FW framework, and is honest about where speedups apply and where tradeoffs exist. The matrix-case methods are explicitly analyzed as trading better dimension dependence for worse precision dependence (Section 4, Tables 1–2, and the explicit comparison ratios in lines 243, 296). The body does not oversell the matrix results as unconditional improvements.

3. **Novel subroutine for latent group norm constraints (Section 3.2 / Theorem 6).** Computing the linear subproblem over latent group norms requires finding the group with the largest ℓ₂ norm of the gradient subvector. The paper's approach—computing dual norms coherently across all groups in quantum superposition and identifying the dominant group via quantum maximum finding—is a clean algorithmic contribution that goes beyond the simpler ℓ₁ case.

## Weaknesses

### Major

1. **Abstract oversimplifies matrix-case complexities, omitting critical problem-dependent parameters.** The abstract states time complexities of "Õ(rd/ε²)" and "Õ(√rd/ε³)" and claims "reducing at least a factor of O(√d) over the best classical algorithm" without qualification. However, the full theorem statements reveal significantly more complex expressions:

   - Theorem 3 (QTSVE): Õ(r σ₁³(M)d / ((σ₁(M)−σ₂(M)) ε²))
   - Theorem 4 (QPM): Õ(√r σ₁⁴(M)d / ((1−σ₁(M))³ γ_min^{2.5}))

   Table 2 correctly includes σ₁, spectral gap (σ₁−σ₂), and γ'_min terms—but the abstract drops all of these. This is consequential because the spectral gap can be arbitrarily small, and the claimed "O(√d) speedup" depends on these parameters being benign. The body is transparent about this (lines 243, 296, and Table 2), but the abstract creates a misleading first impression. The authors should revise the abstract to either include these dependencies or clearly state that the simplified expressions assume constant spectral gap and singular values.

### Minor

2. **Gap between Lemma 4 (classical-index output) and its use in Algorithm 3 (coherent state preparation).** Lemma 4 is described as finding an index i* (classical output after measurement). Algorithm 3 (line 9) uses it to obtain the quantum state |u_top⟩|v_top⟩|σ₁⟩ for subsequent tomography. The paper notes this application and defers to Appendix B.2/B.8 (line 181–182) for the extension to non-uniform input states. However, the main text does not clarify how the standard index-output quantum maximum finding procedure is adapted to produce the needed coherent quantum state. A brief clarification would help.

3. **Oracle model mismatch in the vector case could be discussed more thoroughly.** The vector-case speedup compares classical gradient evaluation (O(d) floating-point operations) against O(√d) queries to a quantum function-value oracle U_f (Assumption 3). This comparison is standard and valid within quantum query complexity, but the paper does not discuss how practical overheads—reversible circuit size, quantum state preparation costs, and error-correction overhead—could affect the practical relevance of the claimed √d advantage. A brief paragraph on the regime where this advantage survives practical overheads would strengthen the paper's credibility.

### Trivial

None.

## Nice-to-Haves

- A short discussion of the crossover regime where the quantum matrix methods become competitive (given their worse ε-dependence) would help practitioners understand when the speedup applies.
- Clarify in the main text how the index-output quantum maximum finding procedure (Lemma 4) is adapted for coherent state preparation in Algorithm 3.
- Brief discussion of whether the function value oracle U_f can be implemented with overhead that does not scale with d for relevant function classes.

## Removed Points

The following points from the input reviews were removed with justification:

1. **Gradient estimation ℓ₂→ℓ∞ error concern (Critical Issue 3 in Harsh Critic).** The reviewer claimed that Lemma 2's ℓ₂ bound does not directly bound the per-coordinate error needed for Lemma 4. This is factually incorrect: ‖v‖∞ ≤ ‖v‖₂, so the ℓ₂ bound directly implies a per-coordinate error bound of the same magnitude. The paper's parameter choice σ_t = C_t/(√d L(t+2)) correctly controls this.

2. **Different complexity measures in Tables 1 and 2.** The paper explicitly justifies this (line 217): the matrix case analysis focuses on update direction computation assuming pre-computed gradient (Remark 3), following classical convention (Jaggi 2013). Adequately explained.

3. **Parser-artifact complaints** (unbalanced parentheses, redundant symbols). These are PDF extraction artifacts, not paper problems.

4. **Missing related works, appendix content.** Removed per policy.

5. **Generic practicality concerns that apply broadly to all quantum algorithms papers.** These are not specific weaknesses of this paper.

## Novel Insights

The input review's most valuable observation is the gap between the abstract's simplified matrix-case complexities and the full theorem statements—a real presentation problem that extends beyond standard "big-O hides constants" to omit problem-dependent parameters (spectral gap, singular values) that can dominate the complexity in worst-case regimes. This is a fixable issue but one that meaningfully affects how readers perceive the contribution. Beyond this, no novel insights beyond the paper's own contributions emerge from the review.

## Suggestions

1. **Revise the abstract and introduction** to include the singular-value and spectral-gap dependence for the matrix-case complexities, or state clearly that the simplified expressions assume constant spectral gap and singular values. Qualify the "O(√d) speedup" claim as holding in dimension-dependence only.
2. **Add a brief note in the main text (Section 4)** explaining how quantum maximum finding (classical-index output) is adapted to preserve the quantum state for subsequent tomography in Algorithm 3.
3. **Add a brief discussion** of the practical crossover regime where quantum methods become competitive given their worse ε-dependence in the matrix case.

---

**Calibration Anchors:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Quantum Algorithm for Sparse Online Learning | 4.80 | R1 | Similar quantum speedup paper, but weaker contribution (narrower regime) and poorer presentation; our paper is stronger |
| Catalyst Framework for QLSP | 5.25 | R1 | Similar theoretical quantum improvement; comparable contribution level |
| Quantum Speedups in LP via Multi-Gibbs | 5.33 | R1 | Similar quantum optimization paper; our paper has better presentation |
| Near-Optimal Quantum Algorithm for Minimizing Max Loss | 6.00 | R1,R2 | Stronger theoretical contribution (tight lower bounds); comparable quality |
| Quantum D²-sampling with Applications | 6.50 | R2 | Stronger practical component; comparable quantum algorithm contribution |

**Round 1 bracket:** 5.0–6.5. The paper has a genuine novel contribution exceeding the 4.80–5.33 anchors, but lacks the tight lower bounds of the 6.00 anchor and has a clear presentation weakness in the abstract.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>