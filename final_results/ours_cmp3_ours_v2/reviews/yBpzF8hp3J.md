Now I have sufficient calibration context. Let me produce the final review.

## Summary

This paper studies differentially private domain discovery problems (set union, top-k, and k-hitting set) under the lens of "missing mass" rather than cardinality. The authors prove that the Weighted Gaussian Mechanism (WGM) achieves near-optimal ℓ₁ missing mass guarantees on Zipfian data (Theorem 3.3) and a distribution-free ℓ∞ bound (Theorem 3.6), then extends these results to obtain utility guarantees for unknown-domain variants of top-k and k-hitting set. Experiments on six real-world datasets show WGM-based methods are competitive with or outperform existing baselines.

## Strengths

1. **First absolute (not relative) utility guarantees for DP set union (Theorem 3.3, Corollary 3.4).** Prior work (Desfontaines et al., 2022; Chen et al., 2025) only provides relative or dominance-based guarantees. The paper correctly identifies this gap, proves explicit bounds, and gives a near-matching lower bound (Theorem 3.5) up to logarithmic factors. This is a genuine theoretical advance.

2. **Clean framing shift from cardinality to missing mass (Definition 2.2, Section 2.3).** The paper motivates why ℓ₀ cardinality is problematic in sparse domains (each user having a unique item forces MM≈1) and why ℓ₁ missing mass is more informative for real-world Zipfian data. The ℓₚ generalization enables the distribution-free ℓ∞ bound used downstream.

3. **Distribution-free ℓ∞ guarantee (Theorem 3.6).** Unlike Theorem 3.3 which requires Zipfian (C, s>1) data, the ℓ∞ bound holds for any dataset. This is what makes the top-k and k-hitting set extensions work without distributional assumptions — a clean technical result that does real work in the paper.

4. **Empirical competitiveness of the simple WGM.** Despite being simpler and more scalable than the policy-based sequential mechanisms, WGM matches or outperforms them on missing mass across three large datasets (Figure 1). On top-k (Figure 2), WGM-then-peeling consistently beats the Durfee & Rogers (2019) limited-domain baseline across all k on all three small datasets.

## Weaknesses

### Fatal
None.

### Major

- **Zipfian assumption for the main ℓ₁ missing mass bound (Theorem 3.3) is not verified on the experimental datasets.** Theorem 3.3 requires (C,s)-Zipfian data with s > 1, yet the set union experiments (Section 5.1, Figure 1) run on Reddit, Amazon Games, and Movie Reviews without any check that these datasets satisfy this condition. The paper gives no guidance on how to estimate C and s from data, nor does it discuss what happens when data is only approximately Zipfian. The practical relevance of Theorem 3.3 to the experiments thus rests on an unverified premise. (Caveat: the distribution-free ℓ∞ bound and all downstream top-k/k-hitting set results do not depend on this assumption, which partially mitigates the concern but does not eliminate it for the headline set union result.)

### Minor

- **The claim "WGM obtains MM within 5% of that of the policy mechanisms" (Section 5.1) is imprecisely quantified.** On Reddit, WGM's MM (~0.15) is substantially lower (better) than Policy Gaussian (~0.35) — a gap of ~0.20 on a scale with range ~0.25. Similarly on Movie Reviews, WGM (~0.02) is much better than Policy Gaussian (~0.15). The "within 5%" phrasing does not accurately describe the observed gaps on two of the three large datasets. (Note: this understates WGM's advantage — WGM actually outperforms the policy mechanisms on these datasets — but the imprecision is still worth correcting.)

- **The k-hitting set experiments (Section 5.3, Figure 3) compare against baselines the paper itself acknowledges are not valid private unknown-domain algorithms.** The paper states: "the latter baseline is not a valid private algorithm in the unknown domain setting since, in reality, ⋃ᵢ Wᵢ is private" (lines 308–309). While the paper is transparent about this limitation, comparing against a non-private baseline and an improperly-private baseline weakens the empirical signal.

- **Limited statistical reporting.** Only 5 trials with no error bars or confidence intervals shown in Figures 1–2 (standard errors are mentioned only for Figure 3). The reader cannot assess whether observed differences between methods are statistically reliable.

- **No sensitivity analysis for the privacy budget across main experiments.** All experiments use ε=1, δ=10⁻⁵ (with a brief appendix for ε=0.1). Showing how MM scales with ε would directly illustrate the ε-dependence in the theoretical bounds and is standard practice in DP papers.

### Trivial

- The main theoretical bounds (Theorem 3.3, Corollary 3.4, Theorem 3.6) use tilde notation that suppresses dataset-specific constants (C, N, Δ₀, etc.), making practical interpretability low. This is common in theory papers but worth noting.

## Nice-to-Haves

- A log-log frequency-rank plot for each dataset would show whether the (C,s)-Zipfian model is a reasonable description of the data, bridging the theory-experiment gap for the set union results.
- Including the adaptive-weighting baseline from Chen et al. (2025) as a comparison on the MM objective would be informative, since the paper argues that cardinality and MM are meaningfully different metrics.
- A sensitivity study of Δ₀ for the top-k and k-hitting set downstream tasks (currently only shown for set union).

## Removed Points

The following points from the input review are removed:

- **"Lower bounds rely on Assumption 1, making them conditional, not fundamental"** — REMOVED: The paper transparently states "Assumption 1 is standard across works in the unknown domain setting" (line 75) and all lower bounds correctly state "satisfying Assumption 1." This is standard practice in the field, not a flaw.

- **"Section 2.3 ℓₚ generalization unused except for p=1 and p=∞"** — REMOVED: The ℓₚ framing is a conceptual tool. The paper uses p=1 (main results) and p=∞ (Theorem 3.6). This is a natural framing choice, not a weakness.

- **"Small vs large datasets asymmetry"** — REMOVED: The paper explicitly explains why large datasets are not informative for top-k/k-hitting set (near-zero MM for all methods). This is a reasoned methodological choice.

- **"Only 5 trials for DP mechanisms"** — REDUCED from stronger criticism to Minor: 5 trials without error bars is a valid concern but the critic's framing as a major issue overstated the problem. Demoted to the Minor tier above.

- **Critic's claim that "within 5%" claim shows WGM is worse than policy mechanisms** — CORRECTED: The critic misread Figure 1. WGM achieves LOWER (better) MM than policy mechanisms on Reddit and Movie Reviews. The imprecision is in the quantification, not in the claimed direction of advantage.

- **Formatting/style nitpicks and missing appendix references** — REMOVED per hard rules; these are parser artifacts.

## Novel Insights

The most interesting observation that emerges from synthesizing the reviews is the structural asymmetry between the paper's two main theoretical results: Theorem 3.3 (ℓ₁ MM bound) requires a Zipfian assumption that is never validated on the experimental data, while Theorem 3.6 (ℓ∞ MM bound) is distribution-free and powers all the downstream applications (top-k, k-hitting set). The paper could potentially reframe its contribution around the ℓ∞ bound as the more robust and widely applicable result, with the Zipfian ℓ₁ bound as an additional refinement for datasets known to follow power laws — this would better align the theoretical framing with what the experiments actually support. The practical message would then be: "for set union, WGM has a distribution-free ℓ∞ guarantee (bounded maximum missing mass) and on Zipfian data the stronger ℓ₁ guarantee drops in."

## Suggestions

1. Verify (or at minimum discuss) whether the experimental datasets approximately satisfy the Zipfian condition used in Theorem 3.3. A log-log frequency-rank plot in the appendix would suffice.
2. Replace the "within 5%" qualitative claim with a table of actual MM values (with standard errors) for all datasets.
3. Report standard errors or confidence bands in Figures 1 and 2, not just Figure 3.
4. Run a sensitivity experiment varying ε beyond the brief ε=0.1 appendix to directly illustrate the theoretical ε-dependence.
5. Acknowledge more explicitly in the discussion that the set union ℓ₁ bound (Theorem 3.3) is the only result requiring the Zipfian condition, and that the remaining contributions (ℓ∞ bound, top-k, k-hitting set) do not depend on it.

## Score and Decision

**Calibration anchors:**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/yLhJYvkKA0.md (Hierarchical Clustering DP) | 6.67 | R1 (5.5-7.5) | Similar: theory + experiments DP paper with explicit assumptions, accepted. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/hkSjjs4o5d.md (Well-Clustered Graphs DP) | 6.50 | R1 (5.5-7.5) | Similar: DP algorithm under structural assumptions, experiments on real data, accepted. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/hVTaXJ0I5M.md (Counting Partially Ordered Data) | 6.75 | R2 (5.5-7.5) | Similar: DP theory + experiments, limitations in runtime validation noted but accepted. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fbqOEOqurU.md (Matrix Mechanism Optimality) | 7.00 | R2 (5.5-7.5) | Stronger: pure theory paper with tight bounds, less experimental burden. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/O7wTfBLSFn.md (Private Wasserstein) | 5.00 | R2 (3.5-5.5) | Weaker: formal privacy model issues, unclear contribution, rejected. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JG9PoF8o07.md (Generalized Gaussian Mechanism) | 4.25 | R2 (3.5-5.5) | Weaker: limited novelty, straightforward generalization, rejected. |

**Round 1 bracket:** 5.5–7.5 (based on initial calibration search).

**Narrowing rationale:** The paper is clearly stronger than the mid-band anchored papers (Private Wasserstein at 5.00, GGM at 4.25), which had fundamental issues with either privacy modeling or novelty. It is comparable to the accepted DP theory+experiments papers (Hierarchical Clustering at 6.67, Well-Clustered Graphs at 6.50, Partial Orders at 6.75). Like those papers, it has a genuine theoretical contribution with experimental support that has limitations but doesn't undermine the core claims. The Zipfian verification gap is the paper's most significant weakness — it's real but bounded in impact since the ℓ∞ bound and downstream results don't require it. The paper is slightly below the Matrix Mechanism paper (7.00) because that paper had tight matching bounds and fewer empirical limitations.

**Final score: 6.5**

**Final decision: Accept**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>