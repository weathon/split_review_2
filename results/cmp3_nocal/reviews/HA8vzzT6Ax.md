Now let me write the final consolidated review.

## Summary
This paper revisits the trade-off between watermark strength and speculative sampling efficiency for LLMs. It introduces a quantitative measure of watermark strength (expected KL divergence / mutual information), characterizes the Pareto frontier as a constrained optimization problem, and proposes Algorithm 1 — a mechanism that makes the draft-token acceptance decision pseudorandom. The paper proves (Theorem 4.1) that this approach simultaneously achieves maximal watermark strength and maximal speculative sampling efficiency under degenerate decoders, and provides experiments on Gumbel-max and SynthID watermarks showing improved detectability without efficiency loss.

## Strengths

1. **A precise, well-motivated quantitative definition of watermark strength (Def. 3.1).** The expected KL divergence (equivalently mutual information I(w; ζ)) is a natural choice. The paper shows it governs the p-value decay rate of the UMP test (Theorem 3.1), is bounded by the entropy of the original distribution (Theorem 3.2), and attains its maximum exactly when tokens are deterministic functions of pseudorandom numbers. This moves decisively beyond the binary "preserved or not" framing of prior work.

2. **Theorem 4.1 genuinely breaks the theoretical trade-off.** The proof that Algorithm 1 simultaneously achieves maximal watermark strength (Ent(P)) and maximal sampling efficiency (1 − TV(Q, P)) is clean and correct under its stated assumptions. The core insight — that the residual randomness of the acceptance coin-flip is what forces the trade-off, and that making it pseudorandom restores determinism in ζ — is simple once stated but not obvious beforehand.

3. **Clean characterization of the Pareto frontier (Section 3.2).** The formulation of the trade-off curve as a constrained optimization problem (Def. 3.2), the reduction to SSE via Lemma 3.1, and the explicit derivation for linearly watermarked classes give the field a usable framework. Figure 1 provides a concrete visualization that immediately shows where existing schemes fall relative to the theoretical optimum.

4. **Honest separation between watermark strength and practical detectability (Remark 3.1, Section 4.2).** The paper does not conflate the theoretical guarantee (Theorem 4.1c) with the harder practical problem of detection. It explicitly acknowledges that two schemes with equal watermark strength can differ in detection efficiency, and develops specific detectors (Ars-τ, Bayes-MLP) to address the practical challenge.

## Weaknesses

### Fatal
None.

### Major

1. **Temperature sensitivity of experimental evidence.** The paper tests detectability only at temperatures 0.5 (Gumbel-max) and 0.7 (SynthID), stating this is "to make the results more pronounced" (line 259). At lower temperatures, the target distribution is sharper (lower entropy → lower maximal watermark strength) and the acceptance thresholds min{1, P_w/Q_w} become more extreme, making acceptance decisions more deterministic even without the pseudorandom intervention. The claim that Algorithm 1 "improves detectability" is therefore supported only in the low-temperature regime, not at temperature 1.0 (a widely used default). The omission of temperature 1.0 results is a meaningful gap in the experimental evidence. This does not weaken the theoretical results, but it limits the empirical support for the practical claim of improved detectability.

2. **Gap between Theorem 4.1's assumption and the SynthID experimental setup.** Theorem 4.1 (lines 217-218) states: "Assume the decoder S is unbiased and achieves the largest watermark strength (hence it is degenerate by Thm. 3.2)." This applies to Gumbel-max (which is degenerate) and to SynthID only in the limit m → ∞. However, the experiments use SynthID with m = 30 (line 257), which the paper itself notes is not at maximal strength (line 172: "the watermark strength drops below that of Gumbel-max"). The theoretical guarantee therefore does not directly cover the SynthID experimental setting. While the Gumbel-max experiments are covered, the paper would benefit from either extending the analysis to non-degenerate decoders or providing a bound that relates achieved watermark strength to the degree of degeneracy.

### Minor

3. **Asymmetric calibration in detection comparison.** Ars-τ selects its threshold τ via grid search on a held-out validation set, optimizing for TPR at the target FPR (lines 233-235). The baseline Ars-Prior estimates its probability p from observed acceptance rates (lines 235-237). Because Ars-τ's threshold is directly optimized for the evaluation metric while Ars-Prior's p is merely estimated, the comparison may conflate the benefit of pseudorandom acceptance with the benefit of having a validation-set-optimized threshold. A cleaner comparison would calibrate both methods analogously.

4. **No quantification of distance from theoretical efficiency maximum.** The AATPS bar chart (Fig. 2, left) shows Algorithm 1 matches standard speculative sampling, which is the relevant comparison. However, the paper does not report how close the measured AATPS is to the theoretical maximum 1 − TV(Q, P), making it difficult to assess whether any efficiency gap remains.

### Trivial
None.

## Nice-to-Haves

- **Non-speculative watermarking baseline.** Comparing Algorithm 1's detectability against standard (non-speculative) watermarking detectability on the same model would directly quantify how much of the trade-off is recovered in practice. The Oracle curve is an upper bound, but a direct baseline comparison would be more informative.
- **Statistical significance tests.** The paper reports 95% confidence intervals, but does not test whether the difference between Ars-τ and Ars-Prior is statistically significant at specific token lengths. A simple test would strengthen the evidence.
- **Quantification of bonus-step frequency.** Footnote 3 notes that bonus steps are rare for K > 1, but provides no empirical quantification. Reporting the measured frequency would strengthen this claim.

## Removed Points

These points from the input review are flagged for removal; treat them with caution:

1. **Oracle detection rule criticism** (not achievable in practice): Removed because the paper already explicitly states (line 263) that it is "an ideal detector that always selects the correct test statistic" and acknowledges the gap to it — the paper is not claiming the Oracle is achievable.
2. **Theorem 4.1(b) deserves more justification in main text**: Removed because proofs are deferred to the appendix (standard conference practice), and the case for keeping the main text concise is reasonable.
3. **Non-speculative watermarking comparison as a weakness**: Demoted to Nice-to-Have. The paper's scope is the trade-off *within* speculative sampling; non-speculative comparison is useful additional context but not a core evaluative requirement.
4. **Only two model pairs**: Removed as a generic criticism (68M-7B and 2B-7B spans a reasonable range for this type of study).
5. **Results in appendix tables**: Removed because appendix content is part of the paper; the parser strips these sections but they exist in the original submission.

## Novel Insights

None beyond the paper's own contributions. The key insight — that making the acceptance coin-flip pseudorandom rather than truly random resolves the degeneracy that forces the trade-off — is the paper's own, and the reviews do not surface additional novel perspectives.

## Suggestions

1. Run the main detectability experiment at temperature 1.0 for both Gumbel-max and SynthID. If the improvement holds, report it; if it shrinks, report the temperature sensitivity as a meaningful boundary condition.
2. Provide theoretical analysis or bounds for Algorithm 1 when applied to non-degenerate watermarks (e.g., SynthID with finite m), bridging the gap between Theorem 4.1 and the experimental setup.
3. Equalize the calibration procedures between Ars-τ and Ars-Prior (e.g., also tune Ars-Prior's p via grid search on the same validation set) to isolate the benefit of pseudorandom acceptance from the benefit of threshold optimization.

## Score and Decision

<score>8</score>
<decision>Accept</decision>

The paper makes a genuine theoretical contribution (the quantitative measure, Pareto characterization, and the mechanism to break the trade-off are all significant), the experimental validation is adequate as supporting evidence for a primarily theoretical paper, and the authors are transparent about limitations. The identified weaknesses (temperature sensitivity, degeneracy gap, calibration asymmetry) are real but addressable and do not undermine the core theoretical claims.