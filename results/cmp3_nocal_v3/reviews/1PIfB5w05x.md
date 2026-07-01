Now I have all the evidence needed. Let me write the final consolidated review.

## Summary

This paper studies sparse support recovery when observations come from two sources with different noise levels (high-quality with small variance σ₁², low-quality with larger variance σ₂²). It provides sufficient conditions for information-theoretic recovery in both an agnostic setting (the decoder does not know per-sample noise levels) and an informed setting (the decoder knows them), introducing the *Price of Quality* γ — the number of low-quality samples needed to replace one high-quality sample. On the algorithmic side, it extends the LASSO recovery threshold analysis (Wainwright, 2009) to heterogeneous noise, showing the threshold depends only on total sample size and average noise variance. The paper is a theory contribution with clear framing and technically sound proofs.

## Strengths

1. **Clean conceptual framing (Price of Quality, γ).** The paper condenses the trade-off between high- and low-quality samples into a single interpretable quantity γ. The contrast between bounded γ in the agnostic setting (≤2) and unbounded γ in the informed setting cleanly conveys why knowing per-sample quality matters.

2. **Clear delineation of agnostic vs. informed settings (§1.1.2).** The paper carefully distinguishes what the decoder knows in each setting, leading to genuinely different mathematical structures — Theorem 1 (condition (9)) vs. Theorem 2 (condition (16)) — that are not conflated.

3. **Technical extension of LASSO analysis to heterogeneous noise (Theorem 3, §4).** The proof generalizes Wainwright (2009) by handling a non-scalar Σ via QR decomposition and Haar-measure analysis of the resulting orthogonal matrix. This is a non-trivial technical contribution that overcomes the breakdown of standard Wishart/inverse-Wishart arguments.

4. **Honest about limitations.** The paper explicitly acknowledges (Remark 3.2) that the agnostic sufficient condition involves a Chernoff relaxation and is not expected to be sharp, and that the exact optimization would yield a tighter characterization.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Inconsistency in equations (12) and (14).** The Price of Quality γ is defined from the sufficient condition (9), where the coefficient of n₁ is log(1 + δ(2σ₂² − σ₁²)s/(2σ₂²)). However, equation (12) writes σ₁⁴ in place of σ₂² inside the numerator's log. Equation (14) also uses σ₁⁴ but simplifies to 2 − σ₁²/σ₂² — a simplification that is mathematically inconsistent with σ₁⁴ (it would yield 2σ₂⁴/σ₁⁴ − σ₂²/σ₁² instead) but correct if σ₂² is used throughout. The expansions (13)–(14) and the claimed bound γ < 2 are all consistent with σ₂² as the intended denominator. This is a presentation error that creates a clear inconsistency between equations (9), (12), and (14) as written, and must be corrected.

2. **The headline γ < 2 bound derives from a relaxed sufficient condition whose looseness is unquantified.** The paper is transparent about this (Remark 3.2 states the condition "is not expected to be information-theoretically sharp" and involves a Chernoff relaxation), and consistently qualifies the claim as "under our sufficient condition." However, the abstract and introduction feature γ < 2 as a key finding, and the potential gap between the relaxed bound and the true information-theoretic threshold is not bounded or even discussed beyond a qualitative acknowledgment. A reader could reasonably infer γ < 2 is a fundamental property rather than an artifact of the proof technique. The paper would be strengthened by any quantification of this gap, even a heuristic one.

### Trivial
None.

## Nice-to-Haves

- **Numerical simulations** would help calibrate confidence in the tightness of the bounds, especially for the agnostic information-theoretic condition where the relaxation introduces unknown looseness. Many related papers (Wainwright, 2009; Reeves et al., 2019) include phase-transition plots. This is not required for a theory paper but would be a valuable addition.
- A brief discussion of whether the sufficient conditions can be interpreted as practical recipes (e.g., using plug-in estimates of σ₁², σ₂², and s) or are best understood as asymptotic scaling laws would help practitioners.

## Removed Points

- **"Formula error in the Price of Quality definition" framed as a fatal/mathematical error.** → Demoted to Minor (inconsistency, not a mathematical error in the underlying reasoning; the intended expression is clear from context and the expansions).
- **"LASSO 'striking robustness' is overstated"** → Removed. This is a matter of interpretive taste rather than a technical weakness. The paper's phrasing is standard for highlighting a non-obvious theoretical finding, and the technical proof is a genuine contribution.
- **"Agnostic estimator may not be optimal"** → Removed. The paper acknowledges this in Remark 3.2. Not a weakness — it is a correctly scoped limitation.
- **"Absence of simulations"** → Moved to Nice-to-Haves. The reviewer correctly notes it is "not required for a pure theory paper."
- **"No discussion of practical use"** → Moved to Nice-to-Haves. Outside the paper's stated scope.
- **"No comparison with weighted least squares baseline"** → Removed. The paper mentions this possibility in Remark 3.2; extending the analysis to such estimators is explicitly scoped as future work.
- **"Extension to non-singular noise without proof"** → Removed. Equations (22)–(23) are clearly stated as suggested extensions from the proof strategy, not as proven theorems.

## Novel Insights

None beyond the paper's own contributions. The harsh review correctly identified the equation inconsistency in (12)/(14) and validated that the expansions (13)/(14) are consistent with the corrected expression — this is a useful editorial observation but not a novel technical insight beyond what the paper itself provides.

## Suggestions

- Correct equation (12) to use σ₂² in the denominator (consistent with equation (9)) and fix equation (14) accordingly. The expansions (13)–(14) are correct under the corrected expression.
- Add a sentence or a short footnote quantifying (or at least bounding) the potential looseness of the agnostic sufficient condition, or explaining why such a bound is difficult to obtain. This would preempt the concern that γ < 2 is an artifact of the relaxation.

## Score and Decision

<score>8</score>
<decision>Accept</decision>