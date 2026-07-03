## Summary

This paper studies differentially private domain discovery, reframing DP set union in terms of missing mass rather than cardinality. It proves that the Weighted Gaussian Mechanism (WGM) achieves near-optimal ℓ₁ missing mass on Zipfian data (Theorem 3.3 / Corollary 3.4, with matching lower bound Theorem 3.5), provides a distribution-free ℓ∞ guarantee (Theorem 3.6), and extends these results to unknown-domain variants of top-k and k-hitting set via a clean meta-algorithm (WGM for domain discovery followed by a known-domain algorithm). Experiments on six datasets show the WGM-based methods are competitive with or outperform existing baselines.

## Strengths

- **First absolute utility guarantees for DP set union.** Prior work (Desfontaines et al., 2022; Chen et al., 2025) proved guarantees relative to other algorithms. This paper gives the first absolute (non-relative) bounds on missing mass as an explicit function of dataset parameters (C, s, N), privacy parameters (ε, δ), and the WGM hyperparameter Δ₀ (Theorem 3.3, Corollary 3.4). This fills a recognized gap in the literature.

- **Matching lower bound on ε and N dependence for Zipfian data.** Theorem 3.5 shows that the factor (1/(εN))^{(s-1)/s} in Corollary 3.4 is unavoidable for any (ε, δ)-DP algorithm satisfying Assumption 1, establishing near-optimality in those parameters.

- **Distribution-free ℓ∞ guarantee enables modular application.** Theorem 3.6 bounds ℓ∞ missing mass for any dataset (no Zipfian assumption required). This feeds into the meta-algorithm (Algorithm 2) to obtain guarantees for unknown-domain top-k (Theorem 4.3) and k-hitting set (Theorem 4.5) without distributional assumptions — a structural advantage over the ℓ₁ bound that requires Zipfian data.

- **Improvement over prior k-hitting set guarantees.** Theorem 4.5 yields additive error in terms of log(M) where M = |∪ᵢWᵢ| rather than log(|𝒳|) as in Mitrovic et al. (2017). When |𝒳| ≫ M (typical in unknown-domain settings), this is a strict improvement.

- **Empirical validation across six datasets.** The WGM-based methods perform competitively with or outperform baselines, including in settings where baselines have an informational advantage (known domain, non-private). For Steam Games and Amazon Magazine datasets, the WGM-based method even outperforms the known-domain private greedy baseline.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The "within 5%" claim (line 281) needs clarification.** The paper states WGM "obtains MM within 5% of that of the policy mechanisms." The figure captions suggest WGM substantially outperforms policy methods on Reddit (y-axis spans 0.15–0.40) and Movie Reviews (y-axis spans 0.00–0.25). It is unclear whether "within 5%" means 5 percentage points, 5% relative difference, or something else. Since the paper's own result is stronger if WGM substantially outperforms the baselines, the text should be precise about the comparison being made.

- **No error bars or variance reported for the set union experiments (Figure 1).** Only 5 trials are run and no measure of variance is reported for Figure 1. (Figure 3 does report standard error.) Readers cannot assess the stability of the reported MM values across trials for the paper's central experiment.

- **The "Uniform" baseline in Figure 2 is not introduced in the main text (Section 5.2).** The text describes only the limited-domain baselines (k̃ ∈ {k, 5k, 10k, ∞}); the Uniform baseline appears only in the figure legend without explanation in the body.

### Trivial
None.

## Nice-to-Haves

- **More practical guidance on Δ₀ selection.** The paper notes (line 147) that "the error due to subsampling can dominate" but could offer more concrete guidance for practitioners who lack public knowledge of max_i|W_i|.
- **Confidence intervals for set union results.** With only 5 trials, bootstrap confidence intervals or additional trials would increase confidence in the reported averages.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Figure 3 caption mismatch (baselines listed as "DP-Top-k" etc.):** The OCR-extracted figure description lists different methods than the paper text (line 309) describes. This is a PDF-extraction artifact from the image alt-text; the actual paper correctly identifies baselines as non-private greedy and Mitrovic et al. (2017). Removed as a formatting artifact.
- **k-hitting set baselines not fully private / unfair comparison:** The paper explicitly acknowledges (line 309) that the known-domain baseline "is not a valid private algorithm in the unknown domain setting." The asymmetry favors the baselines (they have more information or weaker privacy), not the author's method. Removed per rule about asymmetry favoring baselines.
- **(1 - 1/ϵ) approximation factor in Theorem 4.5:** This is almost certainly a LaTeX/PDF-rendering artifact (e vs. ϵ). The standard greedy approximation factor for submodular maximization is (1 - 1/e). Removed as a formatting artifact.
- **Gap between upper and lower bounds for top-k/k-hitting set not closed:** The paper explicitly acknowledges this in Section 6 (Future Directions). Not a weakness of the paper as presented.
- **"Near-optimal" language imprecision:** The paper carefully qualifies near-optimality as applying to ε and N dependence (line 149), which is accurate. The remaining gap involves C and s, which is honestly acknowledged through the explicit bounds.
- **Top-k only evaluated on small datasets:** The paper explains (line 293) all methods achieve near-0 MM on large datasets, making the comparison uninformative — a reasonable experimental design choice.
- **No dedicated limitation section:** The paper's Future Directions section (Section 6) discusses open problems and limitations.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the "within 5%" claim** (line 281) — specify whether this refers to absolute percentage points or relative difference, and note the variation across datasets.
2. **Add error bars or confidence intervals to Figure 1** to match the standard error reported for Figure 3.
3. **Introduce the Uniform baseline** in Section 5.2 for completeness.

## Score and Decision

**Bracket reasoning:** The calibration tool was unavailable, so scoring is based on direct evaluation. This paper makes a genuine theoretical contribution (first absolute utility guarantees for DP set union, with matching lower bounds) that fills a recognized gap. The weaknesses are minor reporting/experimental-precision issues that do not threaten the core claims. The theory is well-structured, the ℓ∞→top-k/k-hitting-set pipeline is modular and clean, and the experiments (while secondary) show the methods work in practice. This places the paper clearly above "borderline accept" (6) but below "strong accept" (10) because the experiments could be more rigorous, the paper applies existing mechanisms rather than proposing new ones, and the presentation has minor imprecisions. A score of 7.5 reflects a solid theoretical contribution with clean execution and well-calibrated claims.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>