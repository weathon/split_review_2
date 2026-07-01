## Summary

This paper studies differentially private domain discovery, where each user holds a subset of items from an unknown domain. It provides the first *absolute* utility guarantees (ℓ₁ and ℓ∞ missing mass bounds) for DP set union using the Weighted Gaussian Mechanism (WGM), proves near-matching lower bounds under Zipfian assumptions, and extends the framework to unknown-domain variants of top-k selection and k-hitting set. Experiments on six real-world datasets show the WGM-based methods are empirically competitive with existing approaches.

## Strengths

1. **First absolute utility guarantees for DP set union.** As the authors correctly note (Section 1.1), existing guarantees are relative (comparing one algorithm to another). Theorems 3.3 and 3.6 prove absolute bounds on missing mass — a genuine theoretical contribution to a problem where provable guarantees were previously lacking.

2. **Upper and lower bounds that nearly match.** The lower bound (Theorem 3.5) has the same functional dependence on ε, N, and Zipfian parameters (C, s) as the upper bound (Corollary 3.4), up to a factor involving max_i|W_i|/√q^* that becomes sub-polynomial under Lemma 3.1. This pins down the essential difficulty of the problem.

3. **Clean modular architecture.** The meta-algorithm (Algorithm 2) that splits the privacy budget between WGM-based domain discovery and a known-domain mechanism is simple and allows the authors to leverage existing results. The generalization from ℓ₁ to ℓ∞ missing mass (Theorem 3.6) is elegant and enables distribution-free guarantees for downstream tasks.

## Weaknesses

### Fatal

None.

### Major

1. **Figure 3 baseline-label mismatch makes k-hitting set experiments uninterpretable.** Section 5.3 states the baselines are "the non-private greedy algorithm and the private non-domain algorithm from Mitrovic et al. (2017) after taking ∪_i W_i to be a public known-domain" — i.e., two baselines. However, the Figure 3 caption lists *four* methods: 'Ours', 'DP-Top-k', 'DP-Top-k with Pay-What-You-Get', and 'Random Selection'. Neither 'DP-Top-k' nor 'Random Selection' is mentioned in the text's baseline description, and it is unclear how they relate to the described baselines. Additionally, the caption labels the y-axis "Number of missed users" while the text says "number of users hit." This discrepancy is severe enough that a reader cannot determine what was actually compared. This must be resolved for the experiments to be verifiable.

### Minor

1. **Omission of Chen et al. (2025) from set union experiments.** The paper cites Chen et al. (2025) as having "proved that the resulting algorithm dominates the WGM (albeit by a small margin, empirically)" yet does not include it as a baseline in the set union experiments. While Chen et al. studied cardinality rather than missing mass, including this comparison would strengthen the claim that WGM's missing mass is already near-optimal. The paper would benefit from either adding this baseline or explaining why the comparison is inapplicable to the missing mass objective.

2. **The "5%" claim in set union results is underspecified.** Section 5.1 states "the WGM obtains MM within 5% of that of the policy mechanisms" without specifying whether this is a relative gap (percentage of the baseline's value) or an absolute difference (5 percentage points). Given that the y-axis values range differently across datasets (e.g., ~0.04–0.40 on Reddit vs ~0.00–0.25 on Movie Reviews), this distinction matters for interpretation.

3. **Practical setting of Δ₀ requires public knowledge of a private quantity.** Corollary 3.4 recommends setting Δ₀ = max_i|W_i|, but max_i|W_i| is itself private. Lemma 3.1 provides an upper bound (CN)^{1/s}, but C and s are also unknown. The paper does not discuss a practical heuristic for this circular dependency. This does not affect the theoretical results but limits deployability.

4. **The "distribution-free" label for Theorem 3.6 is slightly imprecise.** The bound still depends on max_i|W_i|, which is a property of the dataset. The result is more accurately described as "no distributional assumption beyond boundedness of individual contributions" rather than fully distribution-free.

### Trivial

- The text and caption for Figure 3 use complementary metrics ("users hit" vs "missed users") without clarifying the relationship. This should be consistent.

## Nice-to-Haves

- **Synthetic validation of theoretical bounds.** Including a small-scale experiment on synthetic Zipfian data comparing empirical MM to the bound from Corollary 3.4 would help calibrate how tight the bounds are in practice.
- **More ε regimes.** The main experiments use only (ε, δ) = (1, 10⁻⁵); Appendix F adds (0.1, 10⁻⁵). Adding one more value (e.g., ε = 0.5 or 2) would improve robustness.
- **Add Chen et al. (2025) as a set union baseline.** As noted in Minor #1, this would close an obvious empirical gap.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **C3: The (1 − 1/ε) factor in Theorem 4.5.** The harsh critic flagged that the parsed text shows (1 − 1/ε) where the privacy parameter ε would make the factor vacuous at ε=1. This is almost certainly a parser artifact (the standard result uses Euler's number e, not ε). Per the hard rules, formatting/parser artifacts must be removed. The authors should confirm the original submission is correct.
- **ℓ_p generality overstatement.** The critic noted that p values other than 1 and ∞ are mentioned but unused. This is a scope observation, not a weakness; the paper does not claim to analyze them.
- **Privacy budget split (δ not explicitly mentioned).** A minor presentation note that does not affect correctness.
- **Top-k experiments admit near-0 MM on large datasets.** The paper is being honest about its experimental findings; this is not a weakness.

## Novel Insights

None beyond the paper's own contributions. The reviewer's central insight — that the experimental presentation has a concrete mismatch that must be fixed — is a verification concern, not an additional finding about the results.

## Suggestions

1. **Fix the Figure 3 baseline discrepancy.** Align the text's baseline description with the figure's legend, or vice versa. Clarify whether the y-axis measures "users hit" or "missed users" and make the text and caption consistent.
2. **Specify whether the "5%" claim in Section 5.1 is relative or absolute.**
3. **Add a brief discussion** of how practitioners might approximate Δ₀ without public knowledge of max_i|W_i|, or at minimum acknowledge the limitation.
4. **Consider adding Chen et al. (2025) as a baseline** in the set union experiments, or add a sentence explaining why it is omitted (e.g., "their method optimizes cardinality, not missing mass, so a direct comparison is not apples-to-apples").

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>