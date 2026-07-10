Now let me write the final consolidated review.

## Summary

This paper studies Kernel Density Estimation (KDE) in high dimensions and presents a data-structure using asymmetric Locality-Sensitive Hashing (LSH) to obtain the first known query-time vs. space tradeoffs for KDE. The key insight is that in the Charikar et al. (2020) KDE framework, the distance scale that determines the maximum query time is different from the scale that determines the space bound — creating an opening for asymmetric LSH (which allows different space and query exponents ρ_s, ρ_q) to outperform symmetric LSH. The paper obtains a query exponent of 0.05 with space exponent 4.15, and for the linear-space regime (δ=0) achieves query exponent 0.1865, improving the prior data-independent bound of 0.25 and coming within ≈0.013 of the best data-dependent bound.

## Strengths

- **A genuine and well-motivated technical insight.** The paper identifies that different distance scales govern query time and space in the Charikar et al. (2020) framework (Section 4, threshold function θ(δ) and the two regimes). This observation correctly creates an opening for asymmetric LSH to improve over symmetric LSH, rather than merely applying a known tool to a new problem.

- **First time-space tradeoffs for KDE.** Theorem 16 establishes a parametric tradeoff curve ξ(δ) for any δ ≥ 0, going beyond any single operating point. Prior work (Charikar & Siminelakis 2017; Charikar et al. 2020) targeted specific regimes; the paper's claim (line 41) of the first such tradeoff is justified.

- **The linear-space result (δ = 0) is a nontrivial improvement.** The query exponent 0.1865 improves on the prior data-independent bound of 0.25 (Charikar et al., 2020) and comes within ≈0.013 of the best known data-dependent bound of 0.173, using a data-independent construction. This is a legitimate theoretical advance.

- **The paper confronts a limitation directly.** Section 1.2 contains a substantive discussion of why constant-query-time KDE is not achievable with current ANN technology (the plateau at ≈0.05 for δ ≥ 3.15), giving the reader a clear picture of where the method's capabilities end.

## Weaknesses

### Major

- **The headline quantitative results depend on undocumented numerical optimization.** The paper states "The exact optimum does not seem simple to obtain analytically, and we therefore resort to numerics" (line 77), and the optimization in Equation (10) is the basis for all reported exponents (0.05, 0.1865, 4.15, and the function ξ(δ) in Figure 1). However, the paper provides no information about the numerical method used — no discretization scheme, optimization algorithm, error bounds, convergence criteria, or sensitivity checks. For a theory paper at a top venue where quantitative exponents are headline results, readers cannot verify whether the reported values are accurate to three significant digits or are rough approximations. This is fixable but needs to be addressed.

### Minor

- **Numerical inconsistency between reported values across the paper.** Theorem 1 (line 35) states query exponent 0.051 and space exponent 4.15, while Theorem 17 (line 263) states query exponent 0.05 and space exponent 4.1. The abstract (line 9) says 0.05 and 4.15. These small discrepancies (0.051 vs 0.05; 4.15 vs 4.1) should be reconciled or explained, especially given that the numerical method used to obtain them is undocumented.

### Trivial

None.

## Nice-to-Haves

- A table comparing the different regimes (symmetric LSH data-independent, data-dependent, this work linear-space, this work polynomial-space) with exponents would further clarify the contribution.
- A brief remark on whether asymmetric and data-dependent LSH could be combined for further improvement would be valuable.

## Removed Points

These points were flagged in the input review but are removed per the filtering guidelines:
- **Lemma 31 / appendix not accessible**: The hard rules require removing criticisms about missing appendix content; the parser strips these sections from all papers and this is not an author error.
- **Notation issue with p_j = min(1/2^{J+n}, 1)**: Likely a PDF-extraction artifact; formatting artifact criticisms are removed per guidelines.
- **Andoni et al. (2017) citation scope**: Both Andoni et al. (SODA '17) and Razenshteyn (2017) cover asymmetric LSH tradeoffs; the citation is correct.
- **"Much simpler analysis" claim not substantiated**: This is a subjective framing claim, not a technical weakness.
- **Missing related work / combining data-dependent LSH**: Scope creep beyond the paper's stated contribution.

## Novel Insights

None beyond the paper's own contributions. The review confirms that the core insight — that different distance scales govern query time vs. space in the Charikar et al. (2020) framework, making asymmetric LSH beneficial — is correctly identified and yields the first KDE tradeoff curve.

## Suggestions

- Document the numerical optimization used to obtain the exponents in Theorem 17 and Figure 1: describe the algorithm, discretization granularity, convergence criteria, and ideally a sensitivity analysis showing stability of reported values.
- Reconcile the 0.051/4.15 (Theorem 1) vs 0.05/4.1 (Theorem 17) discrepancy or explain that they come from different rounding conventions.

## Score and Decision

The paper makes a genuine theoretical contribution with a well-motivated technical insight, first-of-their-kind tradeoffs, and a concrete improvement in the linear-space regime. The main weakness — undocumented numerical optimization — is significant but fixable and does not undermine the analytical framework (Theorem 16). The numerical inconsistency is minor.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>