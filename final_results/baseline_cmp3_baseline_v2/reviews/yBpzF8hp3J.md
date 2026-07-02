## Summary

This paper provides the first absolute utility guarantees for differentially private set union, using the Weighted Gaussian Mechanism (WGM). The authors frame utility in terms of *missing mass* (ℓ₁ and ℓ∞) rather than cardinality, proving near-optimal ℓ₁ guarantees on Zipfian data and a distribution-free ℓ∞ guarantee. They then apply WGM as a domain-discovery precursor for unknown-domain variants of private top-k and k-hitting set, obtaining new utility bounds. Experiments on six real-world datasets show that WGM-based methods are competitive with or outperform existing baselines across all three problems.

## Strengths

- **First absolute utility guarantees for DP set union.** Prior work (Desfontaines et al., Chen et al.) only gave relative comparisons; this paper proves explicit high-probability bounds on missing mass, which is both theoretically novel and practically relevant for common Zipfian data distributions.
- **Distribution-free ℓ∞ guarantee (Theorem 3.6).** The ℓ∞ missing mass bound requires no distributional assumptions and is directly leveraged for downstream tasks (top-k, k-hitting set), making the approach broadly applicable.
- **Clean meta-algorithm and tight lower bounds.** The simple recipe (WGM for domain discovery, then standard known-domain mechanism) yields provable guarantees for top-k and k-hitting set. Lower bounds (Theorems 3.5, 4.4, 4.6) show the dependence on ε and N is tight for set union and nearly tight for the other problems.
- **Strong empirical validation.** Experiments on six diverse datasets show that WGM achieves missing mass within 5% of more complex sequential methods for set union, and outperforms existing limited-domain baselines for top-k and k-hitting set, including settings where the known-domain algorithm is given an unfair advantage.

## Weaknesses

### Fatal

None.

### Major

- **Asymptotic notation obscures practical interpretation.** The bounds in Theorems 3.3, 4.3, and 4.5 are stated with multiple suppressed log factors and dependencies (e.g., $\tilde{\mathcal{O}}_{\beta, C, N}$). It is difficult for a practitioner to extract concrete parameter recommendations (e.g., how to set $\Delta_0$ or T given a specific dataset and privacy budget). While common in theory papers, more explicit special cases would greatly improve usability.
- **Limited privacy budget variation in experiments.** All main experiments use $(\epsilon=1, \delta=10^{-5})$; appendix results for $\epsilon=0.1$ are mentioned briefly but not discussed in depth. Evaluating at a wider range (e.g., $\epsilon=0.1, 1, 5$) would strengthen the empirical story and validate theoretical scaling.

### Minor

- **Baseline for k-hitting set is not a valid unknown-domain algorithm.** The “private non-domain algorithm” (Mitrovic et al.) assumes public knowledge of $\bigcup_i W_i$, which is not available in the unknown-domain setting. The paper acknowledges this, but the comparison still appears somewhat unfair to the baseline; a completely private unknown-domain baseline (e.g., running WGM followed by random selection) would be more informative.
- **Choice of $\Delta_0$ in practice.** The analysis shows that setting $\Delta_0 \geq \max_i |W_i|$ is desirable, but $\max_i |W_i|$ is unknown in the unknown-domain setting. A brief discussion of how one might choose $\Delta_0$ (e.g., via public estimates or cross-validation) would be helpful.

### Trivial

None.

## Nice-to-Haves

- Provide simplified, readable bounds for the common case where $\Delta_0 = \max_i |W_i|$ is known publicly, and when $N$ is large relative to $\sigma$.
- Include experiments comparing WGM to the adaptive weighting method of Chen et al. (2025), which the paper mentions but does not evaluate.
- Show ablation results for different subsampling strategies beyond uniform without replacement.

## Novel Insights

Beyond the paper's own theoretical contributions, a genuinely novel observation is that the ℓ∞ missing mass bound for WGM is distribution-free and directly enables utility guarantees for downstream problems without requiring Zipfian assumptions. This decouples the domain-discovery analysis from the data distribution, which is conceptually clean and practically powerful. The lower bounds also reveal that the *assumption of outputting only observed items* (Assumption 1) is the fundamental source of the $\tilde\Omega(k/\epsilon)$ cost for top-k and k-hitting set, rather than the specifics of the algorithm.

## Suggestions

- In the main text, include a corollary that states a simplified bound for the common setting $\Delta_0 = \max_i |W_i|$ (e.g., Corollary 3.4 is already simplified; add an explicit numeric example if possible).
- Strengthen the experimental section by testing at least one additional privacy budget (e.g., $\epsilon=0.5$) and reporting results in the main paper, not just the appendix.
- For the k-hitting set experiments, replace the non-private greedy baseline with a fully private unknown-domain baseline (e.g., WGM followed by selecting the k most frequent items in the discovered domain) to provide a fairer comparison.

## Score and Decision

The paper makes a significant theoretical contribution by providing the first absolute utility guarantees for DP set union, introduces a powerful and simple meta-algorithm for unknown-domain problems, and supports its claims with convincing experiments. The weaknesses are minor relative to the contribution’s novelty and impact. I strongly recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>