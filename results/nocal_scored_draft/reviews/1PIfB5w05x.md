Here is the final consolidated review.

---

## Summary

This paper studies sparse recovery (support estimation) when observations come from two sources with different noise variances — a small set of high-quality measurements and a larger set of low-quality ones. It introduces a conceptual "Price of Quality" γ (the number of low-quality samples needed to replace one high-quality sample) and derives sufficient conditions for support recovery using the MLE in both an agnostic setting (decoder ignores noise levels) and an informed setting (decoder knows per-sample variances). It also extends Wainwright (2009) to show that the LASSO threshold in the agnostic heterogeneous-noise setting depends only on the average noise variance and matches the homogeneous-noise threshold — a nontrivial technical generalization using QR decomposition and Haar measure on the orthogonal group.

## Strengths

- **Novel problem formulation.** The paper formalizes mixed-quality (heterogeneous-noise) data for sparse recovery with a clean distinction between agnostic and informed settings, motivated by real-world scenarios (web-scale data without provenance vs. multi-site clinical trials with calibration logs).
- **Conceptual contribution: Price of Quality.** The notion of γ — the number of low-quality samples needed to replace one high-quality sample — is well-defined and interpretable. The finding that γ < 2 (agnostic) vs. γ unbounded (informed) cleanly captures the value of knowing per-sample noise levels.
- **Non-trivial technical contribution in Theorem 3.** Generalizing Wainwright (2009) to heterogeneous noise where Σ is not a scalar multiple of the identity is genuinely nontrivial. The paper's QR decomposition + Haar measure on the orthogonal group solution shows real technical depth. The result — that the LASSO threshold depends on noise only through σ²_avg — is clean and surprising.
- **Sharp contrast between information-theoretic and algorithmic thresholds.** The finding that the algorithmic condition treats all samples equally regardless of quality while the information-theoretic condition distinguishes between them is a structurally interesting asymmetry.

## Weaknesses

### Major

- **Inconsistency between equations (9) and (12).** In (9) the coefficient of n₁ is log(1 + δ(2σ₂² − σ₁²)s/(2σ₂²)), but in (12) the numerator of γ is log(1 + δ(2σ₂² − σ₁²)s/(2σ₁⁴)). The denominator changed from 2σ₂² to 2σ₁⁴ with no explanation. The Price of Quality γ is defined as the ratio of the coefficients in the sufficient condition (9), so γ should follow directly from (9) — but it does not as written. This inconsistency needs resolution. If it is a typo, it requires correction before the analysis can be trusted. The asymptotic result in (14) (γ → 2 − σ₁²/σ₂²) is consistent with the (9) coefficients but not with (12) as written.

- **Over-claim on 'information-theoretic' status and contradictory sharpness claim.** Sections 3.1 and 3.2 present results as establishing "sampling complexity of sparse recovery... information-theoretically," but Theorem 1 and Theorem 2 are sufficient conditions for specific estimators (unweighted and rescaled MLE), not fundamental information-theoretic limits. The paper acknowledges this partially in remarks (3.2, 3.3) but the abstract, introduction, and conclusion continue to use "information-theoretic" as the primary descriptor without consistent qualification. More troublingly, the conclusion (line 340) states "the informed information-theoretic threshold... [is] sharp," while Remark 3.3 explicitly states "Establishing full necessity in the heterogeneous setting remains an interesting direction for future work." These are contradictory. A threshold cannot be called "sharp" when necessity has not been proven.

### Minor

- **The γ < 2 bound is a property of a specific loose sufficient condition.** The paper is transparent about this (qualifying with "under our sufficient condition"), but the prominence of the claim in the abstract, introduction, and conclusion risks over-interpretation as a fundamental bound on the exchange rate between data qualities. If the sharp condition were available, the structure and numerical values could differ.
- **The agnostic and informed results use different estimators (unweighted MLE vs. rescaled MLE),** so part of the observed gap in γ may reflect estimator misspecification rather than the fundamental value of knowing noise levels. The paper acknowledges this in Remark 3.2, where it mentions alternative agnostic estimators (e.g., Y_i²-weighted reweighting), but does not adjust the overarching narrative accordingly.

### Trivial

None.

## Nice-to-Haves

- A small-scale simulation study (2–4 figures) showing empirical phase transitions for the LASSO and comparing the sufficient condition (9) to empirical MLE performance would strengthen confidence that the theoretical findings are predictive rather than artifacts of bounding techniques. Given the looseness concerns, this would be particularly valuable for a theory paper.

## Removed Points

- *"Missing validation" criticism:* Moved to Nice-to-Haves — this is a theory paper where experiments are not standard practice.
- *"LASSO necessity direction (26) does not involve noise at all":* This is presented as a finding, not a weakness — the paper correctly notes it is consistent with Wainwright (2009).
- *"No discussion of computational complexity":* Scope creep — the paper is about sample complexity, not computational resource analysis.
- *"Paper does not discuss the case where n₁ or n₂ is zero":* Trivial omission.
- *Any reproducibility concern rooted in doubting that a cited entity exists:* Hard-rule removal — all cited references are assumed to exist.

## Novel Insights

The key insight from synthesizing the reviews is that the paper has two separable contributions of different strength. The LASSO result (Theorem 3) is technically solid, cleanly proven, and yields a surprising finding (robustness to heterogeneity that depends only on average noise). The Section 3 MLE-based analysis introduces a useful conceptual framework (Price of Quality), but the specific numerical values (γ < 2) rest on a sufficient condition with known looseness and a visible equation-level inconsistency that must be resolved. The framing gap — calling estimator-specific sufficient conditions "information-theoretic" — inflates the apparent contribution of Section 3 beyond what is actually proven. This is a case where the strongest result (Theorem 3) could be given more prominence and the MLE analysis reframed as complementary estimator-specific analysis rather than fundamental limits.

## Suggestions

1. Resolve the (9)/(12) inconsistency — verify the denominator and correct whichever equation is wrong.
2. Rename Section 3 to "Sufficient Conditions for MLE-Based Support Recovery" and remove or consistently qualify "information-theoretic" in the abstract and conclusion. The LASSO result can stand alone and should be given more prominence.
3. Reconcile the conclusion's "sharp" claim for the informed threshold with Remark 3.3's statement that necessity is not established.
4. Add a brief numerical illustration (even a single synthetic-data figure) showing the phase transition behavior, to give readers confidence that the sufficient conditions are predictive.
5. Consider re-centering the paper around the LASSO result (Theorem 3) as the primary contribution, with the Section 3 MLE analysis presented as complementary.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>