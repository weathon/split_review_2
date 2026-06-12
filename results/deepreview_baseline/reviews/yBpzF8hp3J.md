## Summary

This paper studies differentially private domain discovery, where each user holds a subset of items from an unknown domain, and the goal is to output an informative subset of items. The authors prove utility guarantees for the Weighted Gaussian Mechanism (WGM) for set union, showing near-optimal ℓ1 missing mass on Zipfian data and distribution-free ℓ∞ missing mass guarantees. They then apply WGM as a domain-discovery precursor for private top-k and k-hitting set problems, obtaining new utility guarantees for their unknown domain variants, and demonstrate empirically that their WGM-based methods are competitive with or outperform existing baselines.

## Strengths

- **First absolute utility guarantees for DP set union**: The paper provides, to the best of the authors' knowledge, the first provable absolute utility guarantees for DP set union, which is a significant theoretical contribution given that prior work only provided relative guarantees or empirical evaluations.

- **Clean theoretical framework with missing mass**: The reframing of DP set union in terms of missing mass (ℓ1 and ℓ∞ norms) rather than cardinality is elegant and enables both Zipfian-specific and distribution-free guarantees. The ℓ∞ missing mass guarantee (Theorem 3.6) is particularly valuable as it does not require distributional assumptions.

- **Novel application to downstream problems**: The application of WGM as a domain-discovery precursor for top-k and k-hitting set problems is well-motivated and yields new utility guarantees for their unknown domain variants. The theoretical results for these downstream problems are non-trivial extensions.

- **Strong empirical validation**: Experiments on six real-world datasets demonstrate that WGM-based methods are competitive with or outperform existing baselines for all three problems, including cases where the method outperforms baselines that assume public knowledge of the domain.

- **Lower bounds**: The paper provides matching or near-matching lower bounds for set union (Theorem 3.5) and lower bounds for top-k and k-hitting set, which strengthens the theoretical contribution.

## Weaknesses

### Fatal
None.

### Major

- **The ℓ∞ missing mass guarantee (Theorem 3.6) has a hidden dependence on the dataset through max_i |W_i|**: While the theorem is distribution-free, the bound depends on max_i |W_i|, which can be large. The authors acknowledge this but the practical implications are unclear. For datasets where some users have many items, the bound could be vacuous.

- **The top-k and k-hitting set results rely on the ℓ∞ bound, inheriting its limitations**: The guarantees in Theorems 4.3 and 4.5 depend on max_i |W_i| through the ℓ∞ bound. This means that for datasets with users having many items, the theoretical guarantees may be weak, even if empirical performance is good.

- **The lower bounds (Corollaries 4.4 and 4.6) are for worst-case datasets and may not reflect typical performance**: The lower bounds show that k/ε dependence is unavoidable for worst-case datasets, but the paper's upper bounds have additional terms involving max_i |W_i|. The gap between upper and lower bounds is acknowledged but not fully addressed.

### Minor

- **The Zipfian assumption (Definition 3.1) is somewhat restrictive**: While the authors argue that Zipfian distributions are common in practice, the main set union result (Theorem 3.3) requires s > 1, which excludes many real-world datasets with heavier tails. The ℓ∞ result (Theorem 3.6) is distribution-free but has a different form.

- **The experimental evaluation uses only (1, 10^{-5})-DP as the primary setting**: While additional experiments with (0.1, 10^{-5})-DP appear in the appendix, the main results are for a single privacy budget. More varied privacy budgets in the main text would strengthen the empirical claims.

- **The comparison to baselines for k-hitting set is somewhat limited**: The paper compares against non-private greedy and a private method that assumes public knowledge of the domain. A comparison to a method that uses a different domain discovery approach (e.g., thresholding with Laplace noise) would be more informative.

### Trivial
None.

## Nice-to-Haves

- An analysis of how the WGM parameters (σ, T, Δ₀) should be chosen in practice given only a privacy budget and no knowledge of the dataset would be useful for practitioners.
- A discussion of the computational complexity of the WGM compared to the policy-based baselines would help contextualize the empirical results.
- An ablation study showing the contribution of each component (subsampling, weighting, thresholding) to the overall missing mass would provide deeper insight.

## Novel Insights

The paper's key insight is that reframing DP set union in terms of missing mass (rather than cardinality) enables provable utility guarantees that were previously absent from the literature. The observation that the simple WGM achieves near-optimal ℓ₁ missing mass on Zipfian data is surprising given that more complex sequential methods were thought to be necessary. The application of ℓ∞ missing mass as a tool for bounding error in downstream problems (top-k and k-hitting set) is a novel technical contribution that may find broader application in DP algorithm design.

## Suggestions

- Consider providing a more detailed discussion of when the ℓ∞ bound is tight and when it is loose, perhaps with examples of datasets where max_i |W_i| is large but the bound is still meaningful.
- Add experiments with more varied privacy budgets (e.g., ε = 0.5, 2.0) to the main text to demonstrate robustness.
- Include a comparison to a simple baseline that uses Laplace noise instead of Gaussian noise for the thresholding step, to justify the choice of WGM.

## Score and Decision

The paper makes a significant theoretical contribution by providing the first absolute utility guarantees for DP set union, and demonstrates practical utility through strong empirical results. The theoretical framework is clean and the application to downstream problems is well-motivated. The weaknesses are relatively minor and do not invalidate the core contributions. The paper is clearly written and the results are well-supported.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>