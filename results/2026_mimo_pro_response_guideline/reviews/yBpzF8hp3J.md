Now let me write the final calibrated review.

## Summary

This paper studies differentially private domain discovery across three problems: set union, top-k selection, and k-hitting set. The central contribution is reframing DP set union in terms of "missing mass" — the fraction of total item-frequency mass not captured by the output set — rather than cardinality. Under this objective, the paper proves near-optimal utility guarantees for the Weighted Gaussian Mechanism (WGM) on Zipfian data (matching upper and lower bounds in Theorems 3.3/3.5) and a distribution-free ℓ∞ missing mass guarantee (Theorem 3.6). It then uses WGM as a domain-discovery precursor in a two-step pipeline (Algorithm 2) to obtain utility guarantees for unknown-domain top-k (Theorem 4.3) and k-hitting set (Theorem 4.5). Experiments on six real-world datasets validate that WGM-based methods are competitive with or superior to existing baselines.

## Strengths

- **First absolute utility guarantees for DP set union (line 31).** Prior work by Desfontaines et al. (2022) and Chen et al. (2025) proved only relative guarantees (one algorithm vs. another). This paper establishes absolute bounds on missing mass for a problem central to industrial DP frameworks. This fills a genuine gap in the literature.

- **Near-optimality of WGM via matching upper and lower bounds.** Theorem 3.3 proves an ℓ₁ missing mass upper bound of Õ(C^{1/s}/(s−1) · (max_i|W_i|/(N√q*))^{(s−1)/s} · (T+σ)^{(s−1)/s}), and Theorem 3.5 proves a matching Ω(C^{1/s}/(s−1) · (1/(εN))^{(s−1)/s} · ln(1+(e^ε−1)/(2δ))^{(s−1)/s}) lower bound, establishing that the ε and N dependence is essentially tight. This is the paper's strongest theoretical claim.

- **Distribution-free ℓ∞ missing mass guarantee (Theorem 3.6).** Unlike Theorem 3.3, this does not require Zipfian data, providing MM_∞(W,S) ≤ Õ(max_i|W_i|/(εN√q*)). This is the enabling result for the downstream utility guarantees for top-k and k-hitting set without distributional assumptions.

- **Novel ℓ_p generalization of missing mass (Equation 1, lines 63–67).** The definition MM_p(W,S) := ‖(N(x)/N)_{x ∈ ∪W_i \ S}‖_p unifies p=1 (traditional missing mass), p=∞ (maximum missing frequency), and p=0 (cardinality). This is a clean conceptual contribution connecting the paper to prior cardinality-based work.

- **Simple WGM competitive with computationally intensive baselines (Section 5.1, Figure 1).** Despite being significantly simpler and more scalable than Policy Gaussian and Policy Greedy mechanisms, WGM obtains MM within 5% of these baselines. This contrasts with prior cardinality-based evaluations where sequential methods appeared much better, suggesting the missing mass perspective reveals WGM's true competitiveness.

- **Modular two-step meta-algorithm (Algorithm 2) with matching lower bounds for all three problems.** The pipeline (WGM for domain discovery → known-domain algorithm) is practical and provides a reusable template. Matching lower bounds (Theorem 3.5, Corollaries 4.4, 4.6) establish that the upper bounds cannot be substantially improved.

## Weaknesses

### Fatal

None.

### Major

- **Vacuous theoretical guarantee for k-hitting set at practical privacy parameters.** Theorem 4.5 (line 253) gives Hits(W,S) ≥ (1 − 1/ε) · Opt(W,k) − err. The multiplicative factor (1 − 1/ε) becomes zero when ε = 1 and negative when ε < 1. The experiments (line 273) use (ε,δ) = (1, 10⁻⁵) and (0.1, 10⁻⁵), so the theoretical guarantee is vacuous at both tested privacy levels. While the empirical results (Figure 3) are strong and this is a known limitation of DP submodular maximization analyses, the paper should explicitly acknowledge this limitation and discuss the regime where the guarantee is meaningful (ε > 1). Without this caveat, the theory-evidence alignment claimed for this result is incomplete.

- **Missing experimental comparison with Chen et al. (2025).** Line 29 describes Chen et al. (2025) as having "proved that the resulting algorithm dominates the WGM (albeit by a small margin, empirically)." This is the state-of-the-art for DP set union — the most natural baseline given the paper's positioning of WGM as near-optimal. Its absence from experiments is conspicuous. The authors' characterization of the gap as "small" based on prior work is secondhand evidence. Including this comparison would significantly strengthen the paper, especially if WGM matches or nearly matches this algorithm under missing mass.

### Minor

- **5 trials without confidence intervals for set union and top-k experiments.** The k-hitting set experiments (Section 5.3) include standard error across 5 trials, but the set union (§5.1) and top-k (§5.2) experiments report only averages. Error bars in Figures 1 and 2 would strengthen the empirical claims and maintain consistency.

- **Non-trivial upper-lower bound gaps for top-k and k-hitting set.** The upper bound for top-k (Theorem 4.3) involves terms max_i|W_i|/(ε√q*) and √k·log(M)/ε, while the lower bound (Corollary 4.4) is Ω̃(k/(εN)). The paper acknowledges this in Section 6 as future work, but a more explicit decomposition of where the looseness enters (WGM step vs. known-domain algorithm composition) would help readers assess room for improvement.

### Trivial

None.

## Nice-to-Haves

- Verifying whether the experimental datasets exhibit Zipfian behavior (e.g., rank vs. frequency on log-log axes) would connect the theory to experiments more tightly.
- A small supplementary table with exact MM numbers for the "within 5%" claim (line 281) would make set union results more precise.
- Brief discussion of how often top-k outputs fewer than k items in practice (Definition 4.1, line 191).

## Removed Points

These points are flagged to be removed, treat them with caution.
- Generic strengths about "important problem" were removed as they lack specificity. The Strength Finder's claims about importance of the problem domain were subsumed by the more concrete strengths listed above.

## Novel Insights

The paper's most novel insight is the reframing of DP set union from cardinality to missing mass, which reveals that the simple WGM is near-optimal (matching upper/lower bounds) — a fact invisible under the traditional cardinality metric where sequential methods appeared much better. The ℓ_p generalization (Equation 1) unifies this with prior work (p=0 gives cardinality) and enables the distribution-free ℓ∞ bound that powers the downstream applications. The modular meta-algorithm (WGM → known-domain algorithm) provides a reusable template for extending known-domain DP algorithms to the unknown-domain setting, with the k-hitting set result improving over Mitrovic et al. (2017) by replacing log(|X|) with log(M) when |X| ≫ M.

## Suggestions

- Add an experimental comparison with Chen et al. (2025) for set union — this is the single most impactful addition.
- Explicitly state that the (1 − 1/ε) factor in Theorem 4.5 requires ε > 1 for a non-vacuous guarantee, and discuss practical implications.
- Add error bars (standard error) to Figures 1 and 2 to match the reporting standard used in Figure 3.
- Consider adding a brief Zipfian fit for experimental datasets to connect theory and experiments.

## Calibration Report

**Anchors retrieved across all rounds:**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| bEgDEyy2Yk | 1.00 | 1 | Code implementation paper, completely unrelated — reject anchor |
| P49gSPmrvN | 1.00 | 1 | Visualization method, no theory — reject anchor |
| 5lUdTogEL3 | 1.00 | 1 | Person re-ID, unrelated — reject anchor |
| TbOcySs6g8 | 2.50 | 1 | DP synthetic data, weak contribution — reject anchor |
| uxFme785fq | 2.50 | 1 | DP + BLB, incremental — reject anchor |
| WhIuLQWCWS | 3.00 | 1 | DP federated k-means, limited novelty — reject anchor |
| S6Dn3uyM2p | 4.60 | 1 | DP One Permutation Hashing, lacks utility analysis — reject anchor |
| fj5SqqXfn1 | 5.00 | 1 | Privacy accounting pitfalls — reject anchor |
| yfZJdCijo6 | 5.25 | 1 | Maximum coverage streaming — reject anchor |
| yLhJYvkKA0 | 6.67 | 1 | DP hierarchical clustering, theory + experiments — Accept anchor |
| hVTaXJ0I5M | 6.75 | 1 | Privately counting partially ordered data — Accept anchor |
| fbqOEOqurU | 7.00 | 1 | Optimality of matrix mechanism, DP matching bounds — Accept anchor |
| EUSkm2sVJ6 | 7.60 | 1 | Dataset usage inference — Accept anchor |
| oZtt0pRnOl | 8.00 | 1 | DP in-context learning — Accept anchor |
| A3YUPeJTNR | 8.00 | 1 | Waiting for accurate predictions — Accept anchor |

**Round 1 bracket:** Between 6.5 and 7.5. The paper is clearly above the reject anchors (4.60–5.25) which lack utility analysis or have incremental contributions. It is comparable to the Accept anchors at 6.67–7.00, which are DP theory papers with matching bounds. The paper under review has stronger practical relevance (industry-relevant problem, 6 datasets, 3 problems) than the 7.00 anchor ("Optimality of Matrix Mechanism" which was criticized for significance of generalization). However, the two major weaknesses (vacuous k-hitting set theory, missing Chen et al. baseline) prevent a score above 7.0.

**Final score: 7.0** — The paper makes strong, well-supported contributions to DP domain discovery with the first absolute utility guarantees, matching bounds, and a clean modular framework. The two major weaknesses are addressable and non-fatal.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>