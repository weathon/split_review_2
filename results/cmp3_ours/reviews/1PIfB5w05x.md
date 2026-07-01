## Summary

This paper studies sparse support recovery under heterogeneous Gaussian noise, where measurements come from two sources: a few high-quality samples (low noise variance) and many low-quality samples (high noise variance). It provides sufficient conditions for information-theoretic recovery in both agnostic and informed settings, defines the "Price of Quality" to quantify the sample-size trade-off between data sources, and extends LASSO recovery phase-transition results (Wainwright, 2009) to the heterogeneous-noise agnostic setting. Key findings: (1) in the agnostic setting, under the derived sufficient condition, one high-quality sample is never worth more than two low-quality samples; (2) in the informed setting, the price of quality can be arbitrarily large; (3) LASSO recovery depends only on the average noise level, not the individual variances.

## Strengths

- **Theorem 3 (LASSO phase transition) is a technically nontrivial extension of Wainwright (2009).** The paper correctly identifies that Σ ≠ σI breaks standard isotropic-noise arguments and overcomes this using QR decomposition followed by Haar-measure analysis of the resulting orthogonal matrix. This is a genuine technical contribution with a clean conclusion (only σ_avg² matters), and the proof approach is clearly described.
- **The Price of Quality concept (γ = α₁/α₂) provides an interpretable framework for comparing data sources.** The contrast between agnostic (bounded γ) and informed (unbounded γ) settings is conceptually clear and practically meaningful. The asymptotic analysis across different SNR regimes makes the results actionable.
- **The paper is transparent about its limitations.** Remark 3.2 explicitly discusses the Chernoff-bound relaxation, acknowledges the sufficient condition is not sharp, and identifies the cubic equation whose exact solution would tighten the bound. Remark 4.2 explains why the informed-LASSO setting is not addressed.

## Weaknesses

### Fatal

None.

### Major

- **Mathematical inconsistency between equations (9), (12), and (22).** Equation (9) (the sufficient condition) has the first log term's denominator as 2σ₂². Equation (12) (the Price of Quality derived from it) has denominator 2σ₁⁴ instead — these are not the same quantity. The generalization (22) uses 2σ_max⁴ = 2σ₂⁴, which again differs from both. The asymptotic analysis in (14) is mathematically consistent with γ having denominator 2σ₂² (as in (9)) or 2σ₂⁴ (as in (22)), but NOT with γ having denominator 2σ₁⁴ as written in (12). Specifically, (14) gives γ ≃ 2 − σ₁²/σ₂² using the form with σ₂², but with σ₁⁴ as in (12) the correct low-SNR asymptotic would be γ ≃ (2σ₂²−σ₁²)σ₂²/σ₁⁴, which reduces to 2−σ₁²/σ₂² only when σ₁² = σ₂². As presented, the paper is internally inconsistent at a critical juncture — a reader cannot verify the central interpretive quantity (the Price of Quality) against its own definition and the subsequent asymptotic analysis. This must be resolved before the paper can be considered coherent.

### Minor

- **The γ ≤ 2 claim, while correctly qualified, is given more prominence than its technical status warrants.** The abstract, introduction, and conclusion all state "under our sufficient condition, one high-quality sample is never worth more than two low-quality samples." Remark 3.2 does explain the relaxation, so the paper is not misleading, but the qualifier could be easily missed. The claim characterizes a specific sufficient condition derived from a relaxed Chernoff bound, not necessarily a fundamental property of the problem.
- **The relationship between n* in Theorems 1–2 (n* = 2s log(p/s)) and the known information-theoretic threshold n_INF = 2s log(p/s)/log s from (2) is not discussed.** The paper cites n_INF as the known threshold but uses the smaller n* in its own sufficient conditions. There is no contradiction (sufficient conditions need not match the fundamental limit), but the discrepancy merits an explicit comment to avoid confusion.
- **Remark 3.4 presents the generalization to arbitrary invertible Σ via equations (22)–(23) as factual extensions rather than conjectures.** The text says "the proof strategy suggests that these results extend," but the equations are stated without hedging. Given that the two-group case required nontrivial analysis, a clearer distinction between proven results and suggested extensions is warranted.
- **The proof sketch for Theorem 3(i) (necessity) is sparse in the main text.** While the full proof is in the appendix, the main text does not clarify whether the necessity direction requires the same QR/Haar technique used for sufficiency or follows Wainwright's original argument unchanged. A brief clarifying sentence would improve reader confidence.

### Trivial

None.

## Nice-to-Haves

- A synthetic numerical illustration (e.g., the sufficient region (n₁, n₂) from Theorem 1 vs. Theorem 2 for concrete σ₁², σ₂² values) would increase interpretability without requiring experiments.
- A conjecture or brief discussion about what the informed-LASSO threshold might look like would make the treatment more symmetric.
- A discussion connecting heterogeneous-noise recovery to the Overlap Gap Property framework, though beyond the paper's scope, could provide useful context.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Critical Issue 3 from the harsh review (LASSO necessity proof gap):** The critic argued the necessity direction of Theorem 3 lacks proof detail. However, the full proof is in Appendix D, which was stripped by the parser. Per guidelines, criticisms rooted in missing appendix content are removed.
- **Pure formatting/style nitpicks and grammar issues:** Removed per guidelines (these are parser artifacts, not author errors).
- **The claim that the paper "lacks any discussion of the OGP":** This is scope creep; the paper focuses on information-theoretic and LASSO thresholds, not the OGP.
- **The critic's speculation that the equation inconsistency might be a "parser/OCR artifact":** The inconsistency is present in the paper text regardless of cause. The weakness is retained, but the speculation about its origin is removed.

## Novel Insights

None beyond the paper's own contributions. The harsh review correctly diagnoses that equation (12) is inconsistent with both (9) and the asymptotic analysis (14) — this is a concrete, verifiable mathematical error, not a matter of interpretation.

## Suggestions

- Fix the inconsistency between equations (9), (12), (22), and the asymptotic analysis. The most likely resolution is that (12) should have 2σ₂² (or 2σ₂⁴ if consistent with (22)) in the denominator rather than 2σ₁⁴.
- Add a brief remark comparing n* in Theorems 1–2 to the known n_INF threshold from equation (2) to preempt reader confusion.
- Add a sentence in the main text clarifying whether the necessity direction of Theorem 3(i) requires the same QR/Haar technique as sufficiency.
- Soften Remark 3.4 to clearly label equations (22)–(23) as suggested extensions rather than proven results.

## Score and Decision

**Calibration anchors (all papers retrieved across rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Shuffled Regression (gVVoZtiQlt) | 5.00 | R1 | Rejected. Unrealistic assumptions + heuristic derivations. Current paper is more rigorous but has a concrete error. |
| Shuffled Regression (sIcPMMhl9W) | 5.80 | R1 | Same paper, higher avg from more reviewers. |
| In-Context Sparse Recovery via Transformers (NHhjczmJjo) | 7.00 | R1 | Accepted. Clean theory + experiments. Current paper is more niche and has an error. |
| Sparsistency for iOT (wpXGPCBOTX) | 6.75 | R1 | Accepted. Polished theory paper; current paper has comparable depth but a concrete flaw. |
| Slicing MI Bounds (Piod76RSrx) | 5.50 | R2 | Rejected. Solid theory but limited novelty. Comparable to current paper in rigor. |
| Misspecified Q-Learning (nIEjY4a2Lf) | 6.00 | R2 | Accepted. Clean theoretical bounds. Current paper has comparable theoretical ambition but an equation error. |

**Round-1 bracket:** [4.5, 6.0] → **Narrowed to:** 5.5.

A score of 5.5 reflects that the paper makes genuine theoretical contributions (Theorem 3, Price of Quality framework) but contains a verifiable mathematical inconsistency in a central equation that must be resolved before the paper can stand as a coherent piece of work. The core problem is fixable, and with the error corrected the paper could merit a higher score.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>