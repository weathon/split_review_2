## Summary

This theory paper studies sparse support recovery when observations come from two sources with different noise levels (mixed-quality data). It establishes the first sufficient conditions for information-theoretic recovery in both agnostic and informed settings, introducing a "Price of Quality" concept that quantifies the trade-off between high- and low-quality samples. On the algorithmic side, it extends LASSO recovery guarantees to the heterogeneous-noise agnostic setting, proving that the LASSO threshold depends only on the average noise level — a non-trivial robustness result.

## Strengths

1. **Well-motivated problem with clear practical relevance.** The setting of combining few high-quality (low-noise) samples with many low-quality (high-noise) samples — e.g., human-labeled vs. LLM- or weakly-labeled data — is directly relevant to modern data pipelines. The paper formalizes this in the canonical sparse recovery framework, which cleanly isolates the effect of noise heterogeneity.

2. **Clean conceptual framing: the Price of Quality.** Expressing the high/low-quality trade-off as an exchange rate γ between the two sample types is effective and intuitive. The contrast between the agnostic setting (γ bounded) and the informed setting (γ can grow arbitrarily large) captures a genuine and meaningful difference that yields actionable practical guidance.

3. **The LASSO robustness result is technically substantive.** Theorem 3 shows that the LASSO's sample-size threshold is independent of how noise variance is distributed across samples — only the average σ²_avg matters. The proof adaptation (QR decomposition and Haar measure on the orthogonal group to handle the Σ matrix, Section 4) is non-trivial: the paper honestly explains that the presence of Σ destroys the Wishart structure used in the classical proof (Wainwright, 2009), requiring genuinely new techniques.

4. **Honest about limitations.** The paper explicitly acknowledges that Theorem 1 is not sharp (Remark 3.2), that the agnostic estimator may not be optimal, and that the informed algorithmic setting is not addressed (Remark 4.2). It also sketches generalizations to signed support recovery and non-diagonal noise covariance (Remark 3.4). This stands in positive contrast to papers that overstate their contributions.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Price of Quality is defined relative to a non-sharp sufficient condition.** The paper's marquee concept (γ) is derived from a sufficient condition explicitly acknowledged to be loose (Remark 3.2: "The potential looseness arises from a relaxation in the Chernoff bound"). The numerical bound γ < 2 in the agnostic setting is therefore a property of the bounding technique, not necessarily of the true information-theoretic limit. The paper uses careful qualifiers ("under our sufficient condition") throughout the body, and the abstract says "for this sufficient condition to hold," so this is not a case of misrepresentation. However, the conceptual framing — the Price of Quality as a named, quantified entity — could lead readers to over-interpret these quantitative bounds as fundamental. A matching lower bound (which the paper does not provide) would be needed to confirm whether γ < 2 is a property of the problem or of the relaxation.

2. **No necessity established for the information-theoretic thresholds.** The paper provides sufficient conditions but not matching lower bounds (except for the LASSO, where Theorem 3 gives both directions). This means the gap between the sufficient conditions and the true thresholds is unknown. The paper acknowledges this and marks it as future work (Remark 3.3, Section 5), but it limits the closure of the information-theoretic analysis. The Price of Quality in particular cannot be definitively interpreted as a fundamental quantity without a necessity result.

3. **The informed algorithmic setting is not addressed.** The paper studies the informed setting information-theoretically but not algorithmically, leaving a gap. The paper acknowledges this (Remark 4.2) and honestly explains why the proof does not easily extend (loss of Wishart structure), but a heuristic discussion or conjecture about what one would expect would strengthen the narrative and make the paper feel more complete.

### Trivial

1. **Signal-to-noise ratio definition depends on a later assumption.** SNR₁ = s/σ₁² and SNR₂ = s/σ₂² are defined in Section 2 (lines 129–130), but their justification relies on the binary signal assumption (β* ∈ {0,1}ᵖ) introduced in Section 3. A reader encounters these definitions before the necessary context, which could cause momentary confusion.

## Nice-to-Haves

- A simulation study (even synthetic, Gaussian design) showing where the LASSO phase transition occurs relative to Theorem 3's prediction would make the results more vivid and help practitioners interpret the theory. Not required for a theory paper but would strengthen it.
- A brief discussion of what one might conjecture about the informed algorithmic setting (e.g., whether the LASSO with rescaled loss would outperform the agnostic LASSO, and by how much) would fill the gap noted in Remark 4.2.
- The relationship to the existing heteroscedastic regression literature (heteroscedastic LASSO, weighted LASSO, variance-adaptive methods) could be developed further, though the paper's focus on sparse support recovery (rather than estimation or prediction) differentiates it from that literature.

## Removed Points

- **Issue about equation (12) having a possible formatting artifact (σ₁⁴ vs σ₂²).** The asymptotic analysis in (14) is internally consistent and this is almost certainly a parser artifact from the PDF extraction; the original PDF likely renders this correctly. Removed per the formatting-artifact rule.
- **Issue that the agnostic estimator (8) is not the only choice.** The paper already acknowledges this explicitly in Remark 3.2 ("might not constitute the best approach... the decoder might re-weight the loss"). This is a strawman — the paper addresses it.
- **Issue that Theorem 3's contribution is "descriptive rather than prescriptive."** Extending a known result to a strictly more general setting with a non-trivial proof technique (QR decomposition + Haar measure) is a genuine contribution. The finding — that the LASSO threshold is robust to noise heterogeneity — is the point.
- **Several generic strengths from the input** (e.g., "well-motivated problem" without specific evidence) were removed or collapsed into the four concrete strengths listed above.
- **Speculation about readers misinterpreting the abstract.** The paper includes the qualifier "for this sufficient condition to hold" in the abstract itself. The reviewer's concern about potential misinterpretation is speculative and not a flaw in the paper's presentation.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's key insight — that the Price of Quality's boundedness claim may be an artifact of the Chernoff-bound relaxation rather than a property of the problem — is valid and is reflected in Weakness 1 above. Beyond that, the review surface no novel synthesis not already present in the paper.

## Suggestions

1. **Add an explicit caveat in the conclusion** about the epistemological status of the Price of Quality in the agnostic setting, stating plainly that tightening the bound is an open problem and that the quantitative values (γ < 2) may change with tighter analysis. The paper already does this implicitly but a dedicated sentence would help.
2. **Consider adding a matching lower bound** for the information-theoretic thresholds (or at least a quantitative characterization of the gap) to strengthen the Price of Quality analysis.
3. If space permits, **add a small simulation study** with synthetic Gaussian data to empirically verify the LASSO phase transition predicted by Theorem 3.

## Calibration

Round 1 bracket: 5.5–7.5.

Anchor papers used:
- **Sparsistency for inverse optimal transport** (avg 6.75, Accept) — Theory paper deriving sufficient conditions for sparse recovery; mixed reviews on experiments but clean theory. Comparable contribution style and rigor.
- **Lasso Bandit with Compatibility Condition** (avg 6.33, Accept) — Theoretical weakening of assumptions; incremental improvement noted by reviewers. Slightly weaker contribution than the current paper.
- **In-Context Sparse Recovery with Transformers** (avg 7.00, Accept) — Theory + strong experiments; some gap between theory and practice noted. Slightly stronger due to empirical validation.
- **Shuffled Regression Phase Transition** (avg 5.80, Reject) — Non-rigorous approximations, poor presentation. Clearly weaker than the current paper, which is rigorous and well-presented.
- **Optimal Sketching for Residual Error** (avg 6.75, Accept) — Tight bounds, clean theory. Comparable in contribution quality and presentation.

The current paper is clearly above the 5.80 reject (which used non-rigorous approximations), comparable to the 6.75 theory papers, and slightly below the 7.00 paper that included empirical validation. Final score: **6.5**.

## Score and Decision

**MY FINAL SCORE:** <score>6.5</score>
**MY FINAL DECISION:** <decision>Accept</decision>