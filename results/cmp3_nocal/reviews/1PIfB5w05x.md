## Summary

This theoretical paper studies sparse recovery when observations come from two sources with different noise variances (high-quality, low-noise; low-quality, high-noise). It establishes sufficient conditions for information-theoretic support recovery in both an agnostic setting (decoder unaware of per-sample noise levels) and an informed setting (decoder knows which samples are which), introducing a "Price of Quality" γ that quantifies how many low-quality samples replace one high-quality sample. It further extends the LASSO recovery threshold (Wainwright, 2009) to heterogeneous noise in the agnostic setting, showing the threshold depends only on total sample size and average noise — a striking contrast with the information-theoretic result.

## Strengths

1. **Well-motivated and novel problem formulation.** The mixed-quality data model (Section 1.1.2, lines 43–48) captures a realistic scenario — combining a small number of high-quality human annotations with many lower-quality LLM or weak-annotator labels — that has received applied attention but, to my knowledge, not sparse-recovery theory analysis. The clean separation into agnostic and informed settings isolates two practically relevant regimes.

2. **The "Price of Quality" γ is an interpretable and effective framing.** The linear trade-off (5) compresses a multidimensional sample-complexity condition into a single scalar. The finding that γ ≤ 2 in the agnostic setting (Eqs 13–14) while it can be arbitrarily large in the informed setting (Eqs 19–21) is genuinely informative and non-obvious.

3. **Theorem 3 (LASSO robustness) is a genuine technical extension.** Extending Wainwright (2009) to heterogeneous noise requires handling the breakdown of the Wishart structure for X_S^T X_S when Σ ≠ σI. The paper's use of QR decomposition and Haar measure on the orthogonal group (lines 304–305) is a legitimate technical contribution, and the result — that the LASSO threshold depends only on total sample size and average noise — is surprising and directionally opposite to the information-theoretic result.

4. **Intellectual honesty about scope.** The paper consistently flags which results are sufficient vs. necessary (Remark 3.2, lines 193–204; discussion after Theorem 2, line 251), acknowledges where extensions are non-trivial (Remark 4.2, lines 330–331), and discusses limitations of the binary-signal assumption (Remark 3.1). This candor builds trust in the claims that are made.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The γ ≤ 2 claim is tied to a sufficient condition whose tightness in the heterogeneous case is unquantified.** The headline result — that one high-quality sample is never worth more than two low-quality samples in the agnostic setting — is uniformly hedged with "under our sufficient condition" (abstract line 9, introduction line 81, conclusion line 336). However, Remark 3.2 (lines 193–195) explains that the sufficient condition (9) uses a relaxation of the Chernoff bound optimization (the exact optimization leads to a cubic equation), and the looseness of this relaxation in the heterogeneous-noise setting is not characterized. In the homogeneous-noise special case, the relaxation is known to be harmless (line 195), but the heterogeneous case introduces an extra parameter (σ₁² vs σ₂²), and whether the γ ≤ 2 bound holds for the optimized (non-relaxed) condition is not established. The paper would be strengthened by either (a) showing that optimizing the cubic equation does not change γ, or (b) stating more prominently in the abstract and conclusion that the bound is only known under a relaxation whose gap is open.

2. **The LASSO guarantee assumes knowledge of σ_avg² to set λ_p, which the agnostic decoder does not have.** Theorem 3 shows that if λ_p satisfies condition (28) — which involves σ_avg² = (n₁σ₁² + n₂σ₂²)/n — then LASSO recovers the signed support. Proposition 4.1 constructs an explicit λ_p (31) that works, but this construction requires knowing σ_avg². The paper defines the agnostic setting as the decoder lacking access to observation-level noise variances (line 47) and does not address how a decoder would obtain σ_avg² or whether standard data-driven λ-selection (e.g., cross-validation) would achieve the same guarantees. This is not a fatal flaw — the theorem is an existence result — but it narrows the gap between the agnostic and informed settings more than the framing suggests, and a brief remark would help.

### Trivial

1. **Equation (12) contains a typo that propagates to Equation (14).** In the definition of γ for the agnostic setting (line 177), the denominator of the first logarithm is 2σ₁⁴ instead of 2σ₂², inconsistent with the sufficient condition (9) it derives from. The asymptotic expansions in (13) and (14) are consistent with the σ₂² version, confirming the σ₁⁴ is a typo. Equation (14) also writes σ₁⁴ in its first expression, which is internally inconsistent with the simplification to 2 − σ₁²/σ₂² that follows (this simplification is correct only when σ₁⁴ is replaced by σ₂²). These errors would confuse a reader trying to verify the derivations.

## Nice-to-Haves

- A brief discussion of whether data-driven λ-selection for the LASSO (e.g., cross-validation) can recover the guarantees of Theorem 3 without explicit knowledge of σ_avg² would bridge the theory/practice gap noted in Weakness 2.
- Quantifying the gap between the relaxed sufficient condition (9) and the optimized Chernoff bound (as discussed in Remark 3.2) would strengthen the paper's main quantitative claim, though the authors note this is nontrivial (cubic equation).

## Removed Points

These points from the input review were removed per the filtering guidelines:

- **Missing verb in lines 147–149**: Removed per the hard rule on formatting/grammar — this is a PDF-extraction artifact.
- **Lack of experiments/simulations**: Removed — the reviewer acknowledged this is a missed opportunity, not a flaw; for a pure theory paper at ICLR, experiments are not a required standard.
- **Alternative agnostic estimators not discussed**: Removed — the paper explicitly scopes the agnostic setting as the decoder "applies standard sparse-recovery methods without noise estimation or reweighting" (line 48) and already discusses alternative approaches (including variance-aware procedures) in Remark 3.2 (lines 196–204).
- **Section-by-section observations** (Section 1.1.2 clarity, Remark 3.3 scope clarification, Theorem 3 regularity condition flag, abstract/intro phrasing comparisons): Removed — these are granular presentation observations that do not constitute substantive weaknesses affecting the evaluation.
- **"Strengthening the Paper on Its Own Terms" suggestions**: The substantive points (quantify the sufficient-condition gap, discuss data-driven LASSO) are already reflected in Minor Weaknesses 1 and 2 above; the remaining advice is acknowledged but does not rise to the level of a separate weakness.
- **Generic/superficial strength framings**: Removed — the retained strengths are cited to specific content in the paper.

## Novel Insights

None beyond the paper's own contributions. The key observation from the review process — that the γ ≤ 2 claim depends on a sufficient condition whose gap relative to the sharp threshold is uncharacterized in the heterogeneous case — is a limitation the paper itself identifies in Remark 3.2; no external reviewer observation transcends what the authors already state.

## Suggestions

1. Correct the typo in Equation (12) (and the corresponding expression in Equation (14)): change σ₁⁴ to σ₂² in the denominator of the first log term.
2. Strengthen the hedging in the abstract and conclusion to more clearly communicate that the γ ≤ 2 bound is known only under a sufficient condition that involves a relaxation whose gap is uncharacterized in the heterogeneous case — e.g., "under our sufficient condition (which relies on a relaxation whose tightness is not established)" instead of "under our sufficient condition."
3. Add a brief remark after Theorem 3 or Proposition 4.1 discussing how a decoder in the agnostic setting could choose λ_p without explicit knowledge of σ_avg², or explicitly note that the result is an existence guarantee.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>