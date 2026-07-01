## Summary

This paper studies differentially private domain discovery, focusing on the set union problem and its applications to top-k selection and k-hitting set. The authors prove utility guarantees for the Weighted Gaussian Mechanism (WGM) in terms of missing mass, showing near-optimal bounds on Zipfian data and distribution-free ℓ∞ guarantees. They then use WGM as a precursor for known-domain algorithms, obtaining utility guarantees for unknown-domain variants of top-k and k-hitting set, and demonstrate empirically that their methods are competitive with or outperform existing baselines.

## Strengths

- **First absolute utility guarantees for DP set union**: The paper provides, to the best of the authors' knowledge, the first provable absolute utility guarantees for DP set union, which is a significant theoretical contribution given the widespread use of set union in industrial DP frameworks.

- **Clean theoretical framing via missing mass**: Reframing the problem in terms of missing mass (ℓ₁ norm) rather than cardinality is a natural and insightful choice that enables tighter analysis and connects naturally to downstream tasks. The generalization to ℓₚ norms is elegant.

- **Near-optimal lower bounds**: Theorem 3.5 provides a matching lower bound showing that the dependence on ε and N in the upper bound is tight, which substantially strengthens the theoretical contribution.

- **Practical applicability**: The WGM-based approach is simple, scalable, and the experiments demonstrate it performs competitively with more complex sequential methods, making the theoretical guarantees practically relevant.

## Weaknesses

### Fatal
None.

### Major

- **The ℓ∞ missing mass guarantee (Theorem 3.6) appears to rely on Zipfian assumptions despite claiming to be distribution-free**: The theorem statement says "Let W be any dataset" and claims a distribution-free bound, but the proof (referenced to Appendix C.2.3) likely uses the same structure as Theorem 3.3 which explicitly requires Zipfian assumptions. The bound contains max_i |W_i| which for arbitrary datasets could be arbitrarily large, making the guarantee vacuous without additional structure. This needs clarification.

- **The lower bounds (Theorems 3.5, Corollaries 4.4, 4.6) rely on Assumption 1 (soundness) which is a design choice, not a fundamental limitation**: The lower bounds show that any algorithm satisfying Assumption 1 must incur certain loss, but algorithms that violate Assumption 1 (e.g., by allowing false positives) could potentially achieve better missing mass. The paper does not discuss this limitation of the lower bounds or whether the assumption is truly necessary for meaningful domain discovery.

- **The top-k and k-hitting set guarantees depend on M = |∪_i W_i|, which is private information**: The bounds in Theorems 4.3 and 4.5 contain log(M) terms, but M is the true number of unique items in the dataset, which is itself private. The algorithms do not need to know M to run, but the utility guarantee depends on it, making it difficult to interpret the bound before seeing the data.

### Minor

- **The experimental comparison for set union is limited**: The paper only compares WGM against Policy Gaussian and Policy Greedy, but does not compare against the adaptive weighting method from Chen et al. (2025), which is cited as a recent improvement. Including this baseline would strengthen the empirical evaluation.

- **The top-k experiments only show results on "small" datasets**: The paper states that all methods achieve near 0 missing mass on large datasets, but does not show these results or discuss what "near 0" means quantitatively. This makes it difficult to assess whether the methods are meaningfully different on large datasets.

- **The k-hitting set baselines are not fully private**: The paper acknowledges that the known-domain private greedy baseline is not valid in the unknown domain setting, but still uses it as a comparison. A more appropriate baseline would be a fully private unknown-domain algorithm, even if it requires constructing one from existing components.

### Trivial
None.

## Nice-to-Haves

- An empirical comparison against the adaptive weighting method of Chen et al. (2025) for set union.
- A discussion of how to set Δ₀ in practice without public knowledge of max_i |W_i|.
- An analysis of the computational cost of the WGM compared to the policy-based methods.

## Novel Insights

The paper's key insight is that reframing DP set union in terms of missing mass (rather than cardinality) enables provable utility guarantees for the simple WGM, which was previously only evaluated empirically. This is a genuinely useful perspective because it connects the set union problem to downstream tasks like top-k and k-hitting set in a principled way. The observation that the ℓ∞ missing mass bound can be used to derive guarantees for these downstream tasks without requiring Zipfian assumptions is particularly clever. The lower bound showing that the ε and N dependence is tight for Zipfian data provides a clear characterization of the fundamental difficulty of the problem.

## Suggestions

- Clarify whether Theorem 3.6 truly holds for arbitrary datasets or requires additional assumptions, and if it does hold, explain why the bound does not become vacuous for worst-case data.
- Discuss the implications of Assumption 1 for the lower bounds—specifically, whether algorithms that allow false positives could circumvent these lower bounds, and whether such algorithms would be practically useful.
- Include experiments on large datasets for top-k and k-hitting set, even if the results are "near 0," to demonstrate that the methods do not break down on these datasets.
- Consider adding a baseline that combines WGM with a different known-domain top-k algorithm (e.g., the joint exponential mechanism from Gillenwater et al. 2022) to show the generality of the approach.

## Score and Decision

The paper makes a solid theoretical contribution by providing the first absolute utility guarantees for DP set union and extending them to downstream problems. The lower bounds are a nice addition. The experiments are reasonable but not exhaustive. The main concerns are the clarity of the ℓ∞ guarantee and the reliance on Assumption 1 for lower bounds. Overall, this is a well-executed paper with clear practical relevance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>