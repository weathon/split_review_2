Now let me produce the final consolidated review.

## Summary

This paper proposes two aggregation algorithms — Optimal Weight (OW) and Inverse Surprising Popularity (ISP) — for combining answers from multiple LLMs by leveraging first-order (accuracy) and second-order (correlation) information. The authors formalize LLM answer aggregation as a Bayesian decision problem, prove OW is Bayesian-optimal under conditional independence (Theorem 1), establish the ordering ISP ≻ MV ≻ SP in expectation with explicit gap formulas (Theorem 2), and validate the methods on synthetic data, UltraFeedback, MMLU, and a real healthcare dataset (ARMMAN). The paper makes a principled theoretical contribution to an important practical problem.

## Strengths

- **Clean theoretical framing.** The paper formalizes LLM answer aggregation as a Bayesian decision problem, proves that OW (log-odds weighting) is Bayesian-optimal under conditional independence (Theorem 1), and establishes the ordering ISP ≻ MV ≻ SP in expectation with explicit closed-form gap formulas (Theorem 2). The connection to the Bradley-Terry model (Corollary 1) is a nice insight that bridges aggregation theory with widely-used LLM post-training methodology.

- **Honest characterization of SP's limitations.** Section 4.1 clearly shows that the surprisingly popular rule — a known method from the human-judgment literature — is actually *worse* than majority voting in the LLM setting, and provides clear intuition: LLMs lack the systematic biases that SP exploits in human subjects. This empirical observation is then productively used to motivate ISP as a principled fix, making the paper's design choices well-grounded.

- **Consistent empirical advantage over MV.** Across three real-world datasets (UltraFeedback, MMLU, ARMMAN) with three proposed methods (OW-L, OW-I, ISP), all methods beat majority voting with statistical significance (t-statistics of 12.53, 23.39, 3.22). The per-question comparison in Table 4 shows the improvement is not from a handful of questions. Across all 16 model ensembles, OW-L outperforms MV in 97.92% of cases, and MV never achieves the best performance in any ensemble.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **σ_K definition inconsistency between the overview and the technical section.** The Overview of Results (line 25) defines σ_K(x) = x²/(K-1+x²), while the technical Section 3 (line 73) defines σ_K(x) = e^x/(K-1+e^x). These are different functions with different inverses — the first gives √((K-1)x/(1-x)), the second gives log(x(K-1)/(1-x)), which is the log-odds form consistent with Corollary 1 and the Bradley-Terry connection. The correct definition is used throughout the technical content and Algorithm 1, so the error is confined to one sentence in the overview, but it will confuse readers forming their initial understanding of the method. This should be corrected.

- **Theoretical guarantees are tied to conditional independence, which is acknowledged as imperfect for LLMs.** Theorems 1–3 are proved under Assumption 1 (conditional independence given ground truth). The paper acknowledges (line 63) that "this assumption may not hold perfectly in the LLM setting" and states that results extend to a more general setting (Appendix C). However, the empirical results do not directly quantify how much performance degrades as inter-model correlation increases. This does not invalidate the contribution — the empirical validation on real data provides evidence that the methods work despite assumption violations — but it means the theory should be understood as providing principled motivation rather than a deployed guarantee.

- **On MMLU, aggregation underperforms the single best model.** The best aggregation method (OW-L at 90.37%) is below the single best model (91.02%). The paper honestly labels Single Best as a "clairvoyant oracle," which is fair, but this result on a widely-used benchmark limits the strength of the claim that aggregation "can extend the boundary of model capabilities" (which the paper carefully qualifies to only UltraFeedback and ARMMAN).

- **OW-L and OW-I produce identical results in Tables 3 and 4.** Across all three datasets, OW-L and OW-I show identical accuracy numbers to two decimal places (73.66%, 90.37%, 85.78%) and identical per-question discrepancy counts. This coincidence warrants an explanation — are the methods empirically equivalent on these particular ensembles, or is this a rounding artifact?

### Trivial

None.

## Nice-to-Haves

- Comparing against confidence-weighted voting (which the paper cites as related work by Chen et al., 2023a; Fu et al., 2025) would strengthen the empirical positioning.
- Reporting confidence intervals or standard deviations across the 16 ensembles in Tables 2 and 3 would be informative.
- A brief discussion of ISP's computational cost (O(N²×K²) for estimating pairwise conditional probabilities) would help readers assess practical scalability.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Appendix not available for review:** Removed per policy — the parser strips appendices from all papers; they exist in the original submission.
- **Algorithm 1 LaTeX formatting issue:** Removed per policy — formatting artifacts from PDF parsing are not author errors.
- **Line 164 presentation issue:** The critic noted a tautological equality in the inequality chain. This is a presentation-level issue that does not affect any claim in the paper and is removed as a trivial artifact.
- **Overstated claims about "extend the boundary of model capabilities":** Removed — the paper carefully qualifies this claim as applying to UltraFeedback and ARMMAN specifically (line 301), and does not claim it holds on MMLU.
- **Missing confidence-weighted voting baseline, missing variance/confidence intervals, missing computational cost discussion:** Moved to Nice-to-Haves as standard suggestions rather than weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Fix the σ_K definition in the Overview of Results (line 25) to match the technical definition in Section 3 (line 73).
- Add a brief explanation for why OW-L and OW-I produce identical numbers in Tables 3 and 4 — is this a property of the data or a rounding coincidence?
- Consider adding a brief discussion of how the conditional independence assumption empirically manifests: does ISP's advantage over MV grow or shrink when models are more correlated?

## Score and Decision

**Calibration Protocol**

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/WVWZ6SnM4t.md` (RoundTable) | 4.75 | R1 | Yes | More critical weaknesses (lowest favorability: -4.92); strengths comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lXFGpwtkRl.md` (MoAA) | 4.80 | R1 | Yes | Much more critical weaknesses (lowest: -5.26); strengths comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/XZ71GHf8aB.md` (Auction) | 6.25 | R1 | Yes | Several very negative weaknesses (lowest: -3.33); strengths comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rfdblE10qm.md` (BT Theory) | 8.00 | R1 | Yes | Clean weakness profile (~4-6 range), much deeper theoretical contribution |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Yol6nUVIJD.md` (ReConcile) | 6.00 | R2 | Yes | More critical weaknesses (lowest: -2.56); similar strength level |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Dl6nkKKvlX.md` (DMoA) | 6.25 | R2 | Yes | Several very negative weaknesses (lowest: -3.86); strengths comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JtGPIZpOrz.md` (Multiagent FT) | 6.67 | R2 | Yes | More critical weaknesses (lowest: -1.53); strengths comparable |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/K3n5jPkrU6.md` (Scaling) | 7.00 | R2 | Yes | More critical weaknesses (lowest: -1.63); more ambitious scope |

**Round 1 bracket:** 6.0–7.0. The paper's strengths (favorabilities 6.93–12.13) are comparable to anchors in this band, while its weaknesses (all ≥ 4.71 favorability) are substantially milder than any anchor at 6.0–6.67, all of which have multiple weaknesses below 0 or even negative.

**Round 2 narrowing:** Comparing against Dl6nkKKvlX (6.25) and Yol6nUVIJD (6.00): those papers have weaknesses with favorability below 0 (DMoA: -3.86, ReConcile: -0.97, -2.56), while this paper's lowest weakness is 4.71. Comparing against JtGPIZpOrz (6.67) and K3n5jPkrU6 (7.00): those papers also have damaging weaknesses (-1.53, -1.63) that this paper lacks. However, this paper's contribution is narrower (modest empirical gains, theory under acknowledged limiting assumption) than the more ambitious contributions at 7.0+. The paper sits above the 6.0–6.25 papers (cleaner profile) but does not reach the ambition level of 7.5+ papers. The final score of 6.5 reflects this positioning: a solid paper with clean theory and consistent empirical validation, where all weaknesses are minor rather than fundamental.

**Final score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>