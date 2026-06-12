## Summary

The paper studies differentially private domain discovery, reframing set union in terms of *missing mass* (the fraction of total item-frequency missed) rather than the traditional cardinality objective. The authors prove that the simple Weighted Gaussian Mechanism (WGM) achieves near-optimal ℓ₁ missing mass on Zipfian data with matching lower bounds, and a distribution-free ℓ∞ missing mass guarantee. These bounds are then used to obtain new utility guarantees for unknown-domain variants of private top-k selection and k-hitting set via a simple two-step approach (WGM for domain discovery, then known-domain algorithm). Experiments on six real-world datasets validate strong empirical performance.

## Strengths

- **First absolute utility guarantees for DP set union.** As the authors correctly identify, prior work (Desfontaines et al., 2022; Chen et al., 2025) provides only relative comparisons between algorithms. This paper proves the first absolute bounds, with matching lower bounds (Theorem 3.5) showing the ε and N dependence is essentially tight. This fills a genuine gap in the literature.

- **Elegant missing mass framework with practical motivation.** The ℓ_p generalization of missing mass (Equation 1) is a clean conceptual contribution. The ℓ₀ recovery yields the cardinality objective studied by prior work, ℓ₁ is the natural frequency-weighted measure, and ℓ∞ yields a distribution-free guarantee useful for downstream tasks. This unifying view makes the theoretical development cohesive.

- **Clean two-step meta-algorithm with provable guarantees for downstream tasks.** The approach of running WGM for domain discovery (using half the privacy budget) then a known-domain algorithm (other half) is simple, scalable, and amenable to analysis. The resulting utility guarantees for top-k (Theorem 4.3) and k-hitting set (Theorem 4.5) are the first for these problems in the unknown-domain setting, and notably replace log(|𝒳|) dependence with log(M) where M = |∪W_i|.

- **Strong empirical validation.** On six diverse datasets, WGM-based methods are competitive with or outperform existing baselines. Notably for set union, WGM achieves missing mass within 5% of far more expensive sequential policy mechanisms. For top-k and k-hitting set, the method outperforms or matches baselines including some that are not fully private.

## Weaknesses

### Fatal
None.

### Major

- **Gap between upper and lower bounds for top-k and k-hitting set.** For top-k, the upper bound (Theorem 4.3) scales as O(k·max_i|W_i|/(εN√q*) + k^{3/2}log(M)/(εN)) while the lower bound (Corollary 4.4) is Ω̃(k/(εN)). The authors acknowledge this gap but do not discuss its likely source or whether the lower bound or upper bound is loose. This is the most significant theoretical shortcoming. A brief discussion of which bound is likely to be improvable would strengthen the paper.

- **The k-hitting set experimental baseline is not fully private.** The comparison includes a "known-domain" baseline that assumes public knowledge of ∪W_i, which violates the unknown-domain setting. While the authors acknowledge this, it makes the experimental comparison less conclusive for this problem. A more informative comparison might include natural baselines like running WGM then a random selection, to better isolate the value of the greedy peeling step.

### Minor

- **Zipfian assumption required for ℓ₁ guarantees.** Theorem 3.3 requires s > 1, and the paper notes that for s ≤ 1 the pathological worst-case dataset is a valid Zipfian dataset. While the ℓ∞ guarantee (Theorem 3.6) is distribution-free and partially mitigates this, the ℓ₁ missing mass is the more natural objective, and many real-world datasets may not be well-captured by Zipfian distributions (e.g., sparse heavy-tailed distributions). A brief empirical assessment of how well the Zipfian assumption fits the experimental datasets would be informative.

- **Choice of Δ₀ is not well-addressed.** The theoretical bounds depend on Δ₀ through q* = min{Δ₀, max_i|W_i|}, and the experiments sweep over Δ₀ ∈ {1, 50, 100, 150, 200, 300}. In practice, one typically doesn't know max_i|W_i|. The paper mentions using public knowledge of this quantity but doesn't provide guidance for the realistic case where it is unknown. Any data-dependent choice would itself require privacy accounting.

### Trivial
None.

## Nice-to-Haves

- A brief discussion of how the WGM's subsampling step interacts with the missing mass objective—specifically, whether adaptive subsampling strategies (as in Chen et al., 2025) could provably improve the missing mass guarantees.

- Empirical verification of how Zipfian the experimental datasets actually are (e.g., plotting frequency-ranked item distributions) to contextualize the applicability of Theorem 3.3.

- Sensitivity analysis of the two-step privacy budget split (currently 50/50 between WGM and the known-domain algorithm). An asymmetric split might improve performance for downstream tasks.

## Novel Insights

The paper's most novel insight is that missing mass, rather than cardinality, is the right objective for evaluating domain discovery algorithms, because it weights items by their frequency and yields bounds that are both distribution-free (in the ℓ∞ case) and tight (in the ℓ₁ case for Zipfian data). This reframing transforms the WGM—previously seen as a baseline dominated by sequential methods—into a near-optimal mechanism with the first absolute utility guarantees for DP set union. A second valuable observation is that ℓ∞ missing mass bounds, being distribution-free, enable utility guarantees for downstream problems (top-k, k-hitting set) without distributional assumptions, whereas ℓ₁ bounds require Zipfian structure.

## Suggestions

- Add a brief empirical plot of the frequency-rank distributions for the six datasets to assess the Zipfian assumption and help readers gauge applicability of the ℓ₁ results.

- For the top-k and k-hitting set lower bounds, provide a brief discussion of where the gap likely originates (is the upper bound's log(M) factor or the lower bound's lack of dependence on M and k the more likely source of slack?).

- Consider including a practical recommendation or simple heuristic for choosing Δ₀ when max_i|W_i| is unknown, even if it cannot be fully analyzed theoretically.

## Score and Decision

This is a well-executed theory paper that makes several meaningful contributions: the first absolute utility guarantees for DP set union, a clean missing mass framework with matching lower bounds, and extensions to top-k and k-hitting set in the unknown-domain setting. The theoretical development is thorough, the writing is clear, and the experiments support the claims. The main weakness is the gap between upper and lower bounds for the downstream tasks, which is common in theory papers and partially offset by the tightness results for set union.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: Accept