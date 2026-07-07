Here is the final review.

---

## Summary

This paper studies sparse recovery (support recovery of a high-dimensional sparse signal) when observations come from two heterogeneous-quality sources: a smaller set of high-quality (low-noise) measurements and a larger set of low-quality (high-noise) measurements, with both Gaussian design and additive Gaussian noise. The authors derive sufficient conditions for information-theoretic support recovery in an "agnostic" setting (decoder does not know per-sample noise levels) and an "informed" setting (decoder knows noise levels), introducing the "Price of Quality" γ — the number of low-quality samples needed to replace one high-quality sample. They also extend Wainwright's LASSO signed-support phase transition to the heterogeneous-noise agnostic setting, showing the algorithmic threshold depends only on total sample size and average noise level, while the regularization condition depends on σ²_avg.

## Strengths

1. **Novel problem formalization with practical motivation.** The paper is the first to study sparse recovery under explicitly heterogeneous (mixed-quality) noise, formalizing a problem that arises naturally when combining expert labels with crowd-sourced/weak labels. The agnostic vs. informed distinction is well-motivated by real scenarios (loss of provenance vs. logged calibration data), and the Gaussian-design framework inherited from Wainwright (2009), Gamarnik & Zadik (2022), and Reeves et al. (2019) is appropriate for a first treatment.

2. **The "Price of Quality" concept is genuinely interpretable.** Quantifying the trade-off between data qualities as a single coefficient γ — how many low-quality samples replace one high-quality sample — is a clean conceptual contribution that translates a complex sufficient condition into an actionable number and makes comparisons across settings concrete.

3. **The LASSO result (Theorem 3) is a nontrivial technical extension.** Extending Wainwright's signed-support phase transition to the heterogeneous-noise setting requires overcoming the loss of Wishart structure caused by Σ ≠ σI. The QR decomposition + Haar measure approach (referenced in the proof sketch) is a genuine technical adaptation, and the finding that the threshold depends only on n = n₁ + n₂ (independent of σ₁², σ₂²) while the regularization condition depends only on σ²_avg is a clean, non-obvious result.

4. **Transparent about limitations.** Remark 3.2 forthrightly acknowledges the agnostic condition is not sharp and discusses the cubic-equation relaxation. Remark 3.3 notes that establishing full necessity in the heterogeneous setting remains future work. Remark 4.2 explains why the informed LASSO analysis is deferred. This candor clarifies the paper's scope.

## Weaknesses

### Major

1. **The Price of Quality comparison conflates problem structure with proof-artifact tightness.** The agnostic γ is derived from a sufficient condition (Theorem 1) obtained by relaxing a cubic Chernoff equation (Remark 3.2 explicitly states the condition is "not expected to be information-theoretically sharp" and arises from a relaxation). The informed γ is derived from an exactly optimized Chernoff bound (Remark 3.3). The paper's central interpretive claim — that γ is small (≤2) in the agnostic setting but can be arbitrarily large in the informed one — therefore mixes two differences: (a) a genuine difference between the agnostic and informed problems, and (b) a difference in how tightly the two sufficient conditions approximate the true thresholds. If the agnostic condition were tightened (e.g., by solving the cubic equation in (37)), the agnostic γ could increase, potentially narrowing the gap. The paper consistently adds the qualification "under our sufficient condition" for the agnostic bound (abstract line 9, introduction line 81, conclusion line 336), but the overall narrative draws the agnostic/informed comparison without noting that the two γ values come from proof strategies with different degrees of tightness. A reader cannot assess how much of the γ gap is fundamental versus an artifact of the relaxation. This does not invalidate any mathematical result, but it weakens the paper's central conceptual message.

### Minor

2. **The LASSO "agnostic" setting requires noise-level knowledge for tuning λ_p.** Theorem 3(ii) requires λ_p to satisfy (28), which depends on σ²_avg = (n₁σ₁² + n₂σ₂²)/n. The paper defines the agnostic setting as one where the decoder "lacks access to observation-level noise variances" (line 47) and "ignores ... the noise levels (σ₁², σ₂²)" (line 147). A decoder who cannot compute σ²_avg cannot verify (28). The impossibility direction (i) is genuinely agnostic, but the sufficiency direction assumes optimal tuning that requires unavailable knowledge. The theorem's theoretical contribution (extending Wainwright's phase transition to heterogeneous noise) remains valid, but the "agnostic" framing overstates what the decoder can achieve without any noise-level information.

3. **Theorem 3 requires n₁, n₂ = ω(s), which limits applicability to the motivating scenario.** The paper's motivating examples (Section 1.1.2) describe "a small collection of high-quality measurements" and "a larger collection of lower-quality measurements." If high-quality data is genuinely scarce — e.g., n₁ = O(1) or grows slower than s — the LASSO phase transition result does not apply. The assumption is stated (line 284) but its restrictiveness for the mixed-quality use case is never discussed.

### Trivial

4. **Probable typo in Equation (12).** The Price of Quality in the agnostic setting is written with σ₁⁴ in the denominator of the first log argument: γ = log(1 + δ(2σ₂² − σ₁²)s/(2σ₁⁴)) / log(1 + δs/(2σ₂²)). The sufficient condition (9) from which γ is derived uses 2σ₂² in both denominator terms. The asymptotic analysis in (14) only yields the claimed result γ ≃ 2 − σ₁²/σ₂² under the σ₂² form; the σ₁⁴ expression gives a different and non-matching expression. This is a copy-editing error.

## Nice-to-Haves

- A numerical experiment for a small (p, s) instance confirming that the sufficient conditions predict actual MLE/LASSO behavior would increase impact and help readers calibrate the looseness of the sufficient conditions. This is standard in adjacent theory papers (e.g., the shuffled regression papers retrieved during calibration include numerical validation).
- Showing whether the agnostic γ ≤ 2 bound survives tightening of the Chernoff relaxation — even a numerical check for a few (σ₁², σ₂², s, δ) combinations — would significantly strengthen the paper's central conceptual claim.

## Removed Points

- **Criticism about missing derivation/context for Eq. (2).** The paper cites Reeves et al. (2019) after the formula. This is a minor expository preference.
- **Criticism about the binary-signal assumption justification in Remark 3.1.** The paper already provides a reasonable justification. The request for tighter exposition about SNR scaling is already addressed in the remark.
- **The word "sharp" in line 340.** The paper qualifies this with "within the Gaussian design framework," and Remark 3.3 acknowledges necessity is future work. The qualification is sufficient.
- **Section-by-section notes about Remark 3.2, Remark 4.2, and the conclusion.** These are observations about what the paper already says, not actionable criticisms.
- **Request for a quantitative demonstration (numerical simulation).** Moved to Nice-to-Haves. Purely theoretical papers are within scope for ICLR, though numerical support would strengthen impact.

## Novel Insights

The most valuable insight from the reviews is that the paper's central narrative comparison — agnostic γ ≤ 2 vs. informed γ → ∞ — rests on two sufficient conditions with demonstrably different degrees of tightness (one relaxed, one exactly optimized). The paper acknowledges the relaxation in Remark 3.2 but does not connect it to the subsequent γ comparison, leaving the reader unsure whether the agnostic/informed γ gap would survive a tightening of the agnostic bound. Beyond this point, no novel insight emerges beyond the paper's own contributions.

## Suggestions

- In the narrative sections (introduction and conclusion), explicitly state that the agnostic and informed γ values come from sufficient conditions with different degrees of tightness (relaxed vs. exact Chernoff optimization), so the gap may partially reflect proof methodology rather than a purely fundamental difference.
- Add a brief discussion of the n₁, n₂ = ω(s) assumption and what it means for the motivating scenarios where high-quality data may be very scarce relative to sparsity.
- Clarify in Section 4 that while Theorem 3's sufficiency direction requires knowing σ²_avg for λ_p tuning, in practice this could be estimated from data (e.g., via cross-validation), and the theoretical result establishes what is possible with optimal tuning.
- Fix the σ₁⁴ → σ₂² (or the appropriate consistent expression) typo in Equation (12).

---

## Calibration Notes

**Round 1 bracket: 5.5 – 7.0.** Anchors consulted:

| Anchor | Avg Score | Round | Itemized | Comparison to this paper |
|--------|-----------|-------|----------|--------------------------|
| Phase Transition of Shuffled Regression (gVVoZtiQlt) | 5.00 | R1 | Yes | Less rigorous; contains heuristic approximations without justification (-5, -4 weights). This paper is fully rigorous (Chernoff bounds, union bounds, exact moment control) and transparent about limitations. |
| Phase Transition of Shuffled Regression (sIcPMMhl9W) | 5.80 | R1 | Yes | Similar topic area but relies on non-rigorous Gaussian approximations from statistical physics (-3, -4 weights for lack of rigor). This paper's proofs are mathematically rigorous. |
| Exact Community Recovery under Side Information (zhFyKgqxlz) | 5.75 | R1 | Yes | Similar structure (information-theoretic thresholds + algorithmic), but reviewers found standard proofs (-3) and unclear novelty (-4). This paper has more clearly novel contributions (first heterogeneous-noise analysis) and more transparent limitations. |
| Sparsistency for inverse OT (wpXGPCBOTX) | 6.75 | R1 | Yes | Rigorous theory paper with strong contributions (+4 weights) but weak experiments (-4). Comparable in theory quality; this paper has a cleaner conceptual contribution (Price of Quality) but also no experiments. |
| Weak-to-strong generalization (4vzGQcVUG8) | 6.50 | R1 | Yes | Rigorous theory for weak supervision with important problem (+4). Similar in being a theory paper with details deferred to appendix. Comparable quality tier. |
| Learn-to-Optimize ICL Sparse Recovery (NHhjczmJjo) | 7.00 | R1 | Yes | Strong theory (+4) but had simulation fairness concerns (-3). This paper is purely theoretical so avoids that weakness, but also lacks empirical validation. |

**Final score placement:** This paper sits between the 5.75–6.75 range. It shares the "rigorous theoretical contribution" (+3/+4) weight of the higher-scored anchors (sparsistency at 6.75, weak-to-strong at 6.50) and lacks the fatal flaws (non-rigorous approximations, incorrect equations, unclear novelty) that pulled down the 5.00–5.80 anchors. However, the interpretive concern about the Price of Quality comparison (Major weakness 1) is a real weakness that the higher-scored papers did not share, and the purely theoretical nature without experiments limits impact relative to the 7.00 anchor. These factors place it at **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>