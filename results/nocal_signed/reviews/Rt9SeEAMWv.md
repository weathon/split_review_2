## Summary

This paper introduces *random set stability*, a new framework extending algorithmic stability to data-dependent random sets produced by stochastic optimization algorithms. It derives worst-case generalization bounds that avoid intractable mutual information (IT) terms present in prior topological/fractal bounds (Simsekli et al., 2020; Birdal et al., 2021; Andreeva et al., 2024), replacing them with a stability parameter β_n and a Rademacher complexity term. The framework elegantly unifies classical stability bounds (J=1) and Rademacher complexity bounds for fixed hypothesis sets (J=n). Theorems 4.3 and 4.4 provide IT-free versions of existing intrinsic dimension and topological bounds.

## Strengths

- **Meaningful technical advance over prior work.** The paper correctly identifies that the mutual information terms in existing topological/fractal generalization bounds are intractable, poorly understood, and can be infinite. Removing them is a well-motivated and genuine contribution.
- **Clean conceptual framework.** The random set stability framework (Assumption 3.1) naturally extends algorithmic stability to data-dependent random sets while explicitly incorporating algorithmic randomness U, improving on Foster et al. (2019). Lemma 3.2 bridges to classical uniform argument stability, showing the assumption is satisfiable under standard conditions.
- **Elegant unification of classical bounds.** Lemma 3.4 and its corollaries show that the parameter J interpolates between algorithmic stability bounds (J=1, Corollary 3.5) and Rademacher complexity bounds for fixed hypothesis sets (J=n, Corollary 3.6), situating the framework within the broader learning theory landscape.
- **Theorems 4.3 and 4.4 genuinely remove IT terms.** The resulting bounds are expressed purely in terms of β_n and a complexity measure of the random set — a meaningful advance over Andreeva et al. (2024). This is the paper's strongest contribution.
- **Transparent about limitations.** Section 6 honestly states that only expected bounds are provided, only Euclidean-based topological complexities are covered, and the trade-off of a slower convergence rate.

## Weaknesses

### Fatal

None.

### Major

- **Structural disconnect between theory and experiments.** The headline theoretical contribution is the IT-free topological bounds (Theorem 4.4), which incorporate complexity measures E^α and PMag. Yet Table 1 does not compute these bounds. Instead, it evaluates a coarse bound derived from Massart's lemma: 2√(2log(T)/J) + 2Jβ_n, which uses *only* the iteration count T and the stability parameter β_n, completely ignoring the topological complexity measures. A bound of this form could be derived without any topological machinery. The correlation plots (Figures 2, 3) linking topological complexity to the generalization gap are informative but do not fill this gap — correlating with the generalization error is not the same as validating that the bound in Theorem 4.4 is tight or informative. The paper's two threads (theory and experiment) remain disconnected, and the abstract slightly oversells what was empirically shown.

- **The O(n^{-1/3}) rate is significantly slower than classical rates, with no analysis of tightness.** When β_n = O(1/n) (the standard rate from Hardt et al. (2016) for convex, smooth, Lipschitz losses), the bound in Theorem 4.4 scales as O(n^{-1/3}) — and slightly worse still (roughly O(n^{-1/3}√(log n))), because K_{n,α} = 2(2L_{S,U}√n/B)^α grows with n inside the log term. The paper acknowledges the slower rate as "a deliberate trade-off" (line 231) but provides no theoretical or empirical argument that this rate is tight, or that the trade-off is worthwhile relative to the intractable IT terms. This undercuts the framing of achieving "the best of both worlds" (line 73).

### Minor

- **The claim of being "the first to fully estimate a bound on the worst-case error" (line 280) overstates what was done.** The estimated bound (a) omits the topological complexity measures central to the paper's claimed contribution, and (b) uses an optimistically estimated β_n. The claim should be tempered to match what was actually computed.

- **The estimation of β_n is optimistic.** As the paper acknowledges (line 254), the supremum over the entire data space Z is replaced with a maximum over 500 held-out points, making the reported empirical bounds *underestimates* of the true bound. The paper is transparent about this, but it means we do not know whether the true bound would be 10×, 100×, or more above the actual generalization error.

### Trivial

None.

## Nice-to-Haves

- Compute the actual topological bounds (Theorem 4.4) for at least a small subset of configurations to directly validate whether the topological complexity measures tighten the bound.
- Provide a bound on the estimation error of β_n (e.g., via a union bound) to convert the optimistic estimate into a rigorous upper bound.
- Include a discussion of whether the O(n^{-1/3}) rate can be improved under additional assumptions.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Rademacher complexity data dependence "glossed over":** The paper *does* address this — Section 4 discusses the independence structure and introduces Assumption 4.1. The critic's claim that the paper "glosses over" it is inaccurate.
- **Divisibility condition n = JK:** The paper uses "without loss of generality" framing. This is a minor technical point within standard practice.
- **Random set stability definition complexity:** A presentational judgment, not a substantive weakness. Lemma 3.2 shows the condition is satisfiable.
- **Missing Lipschitz constant estimation in experiments:** The paper explicitly states this is avoided due to computational cost (line 260). A design choice, not an oversight.
- **Decreasing Pearson correlations for large n (Figure 3):** The paper already discusses this, citing similar observations in prior work (Birdal et al., 2021; Andreeva et al., 2024).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Compute the actual topological bounds (Theorem 4.4) for at least a subset of configurations to directly show whether the topological complexity measures tighten the bound.
2. Bound the estimation error of β_n (e.g., via a union bound over the held-out points) to turn the current optimistic estimate into a rigorous upper bound.
3. Temper the "first to fully estimate" claim to accurately reflect what was empirically computed.
4. Add a discussion of tightness of the O(n^{-1/3}) rate.

## Score and Decision

The paper makes a genuine theoretical contribution: random set stability is a clean framework, the removal of IT terms is meaningful, and the unification of classical bounds is elegant. The theoretical half is strong. However, the empirical evaluation does not actually validate the paper's headline topological bounds — Table 1 computes a simplified bound that ignores the topological complexity measures entirely. This disconnect, combined with an overclaimed novelty statement and the slower convergence rate without tightness analysis, prevents an unqualified recommendation. The theoretical contribution is solid enough to warrant acceptance, with the expectation that the empirical framing be adjusted to match what was demonstrated.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>