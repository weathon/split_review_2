## Summary

This paper reframes DP set union utility in terms of *missing mass* (fraction of total item mass recovered) rather than cardinality (number of unique items). Under this metric, it proves near-optimal guarantees for the Weighted Gaussian Mechanism (WGM) on Zipfian data (Theorem 3.3, Corollary 3.4) with matching lower bounds (Theorem 3.5), plus a distribution-free ℓ∞ bound (Theorem 3.6). The WGM is then applied as a domain-discovery precursor for unknown-domain variants of top-k selection and k-hitting set, yielding new utility guarantees via a clean two-stage meta-algorithm. Experiments on six real-world datasets show WGM-based methods are competitive with or outperform existing baselines.

## Strengths

- **Reframing DP set union via missing mass (Section 3).** The paper convincingly shows (via the singleton-dataset argument) that cardinality-based guarantees are essentially impossible without distributional assumptions, while missing-mass guarantees are tractable and informative. This reframing is what enables the theoretical contributions.

- **First absolute utility guarantees for DP set union under missing mass (line 31).** The upper bound (Theorem 3.3 / Corollary 3.4) and matching lower bound (Theorem 3.5) give a clean picture of achievable utility on Zipfian data, with matching dependence on ε and N up to the Zipfian parameters C and s. This is a genuine theoretical contribution.

- **Distribution-free ℓ∞ bound (Theorem 3.6).** The observation that the same proof technique yields a distribution-free ℓ∞ missing-mass bound without any Zipfian assumption is elegant. This bound then provides the foundation for downstream guarantees (top-k, k-hitting set) without requiring distributional assumptions.

- **Clean meta-algorithm for downstream problems (Algorithm 2).** The two-stage approach — spending half the privacy budget on WGM-based domain discovery and half on a known-domain mechanism — is simple, well-motivated, and provably effective via the ℓ∞ bound. The extension to k-hitting set (Theorem 4.5) is a genuine new result for the unknown-domain variant where prior work only handled known domains.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Theorem 4.5 approximation factor error (line 253).** The theorem states the approximation factor as `(1 − 1/ε)`. For the standard greedy approximation for submodular maximization (cf. Mitrovic et al., 2017), this should be `(1 − 1/e)` ≈ 0.632. For typical privacy parameters (ε ≤ 1), `(1 − 1/ε)` would be zero or negative, which is nonsensical. This appears to be a typo (ε ↔ e) that must be corrected.

- **Imprecise "within 5%" claim (line 281).** The paper states that WGM obtains missing mass "within 5% of that of the policy mechanisms." However, based on the figure description (lines 283–287), the gap for Reddit appears to be roughly 7 percentage points (WGM ~0.15 vs Policy Greedy ~0.22), exceeding a 5pp interpretation. The paper should state whether the claim refers to absolute percentage points or relative difference, and verify it against the actual plotted numbers.

- **Missing contemporary baseline (Chen et al., 2025).** The paper cites Chen et al. (2025) as the most recent work on DP set union and notes that their adaptive-weighting algorithm "dominates the WGM (albeit by a small margin, empirically)" (line 29). Yet this algorithm is not included as an experimental baseline. Its absence makes it difficult for readers to assess whether the paper's theoretical guarantees translate to practical advantages over the strongest known approach.

- **k-hitting set figure labels do not match text baselines (Section 5.3).** The text describes baselines as "the non-private greedy algorithm and the private non-domain algorithm from Mitrovic et al. (2017)" (line 309). However, Figure 3's caption lists "DP-Top-k", "DP-Top-k with Pay-What-You-Get", and "Random Selection." These do not correspond to the text-described baselines, making the experimental comparison difficult to interpret as reported.

- **Missing variance reporting for set union experiments (Section 5.1).** Set union results are reported as averages over only 5 trials without confidence intervals or standard errors, while the k-hitting set experiments (Section 5.3) include standard error. This inconsistency and the lack of variance measures for the main comparison weaken confidence in the "within 5%" claim.

### Trivial
None.

## Nice-to-Haves

- An ablation study of different privacy budget splits between WGM and the downstream mechanism would strengthen practical guidance.
- A discussion of realistic scenarios where data deviates from Zipfian structure (e.g., near-uniform or multimodal frequency distributions) would strengthen the paper's credibility.

## Removed Points

These points were flagged by the harsh critic but are removed under the filtering rules:

- **Missing appendix / proofs / content:** These are parser artifacts — the original submission contains the appendices.
- **ℓp generalization not fully used (only p=1, p=∞):** Minor observation, not a weakness — the paper focuses on the relevant cases.
- **Lower bound C-dependence on N:** The authors are transparent about this (lines 135, 147); not a flaw.
- **Formatting/style nitpicks:** Removed per policy.
- **Demand for privacy budget split ablation:** Moved to Nice-to-Haves.
- **Speculation about parser artifacts (e.g., figure captions garbled):** Not the authors' error.
- **Strengths that are generic or not grounded (e.g., "addressed an important problem"):** Removed.

## Novel Insights

None beyond the paper's own contributions. The review confirms the core theoretical contribution (first absolute utility guarantees for DP set union under missing mass) as genuine and well-supported. The main concerns are with experimental presentation and completeness, not with the theoretical core.

## Suggestions

1. Correct Theorem 4.5: change `(1 − 1/ε)` to `(1 − 1/e)`.
2. Clarify the "within 5%" claim: specify whether it refers to absolute percentage points or relative difference, and verify against the actual plotted data.
3. Either include Chen et al. (2025) as a baseline, or explain clearly why it cannot be included (e.g., implementation complexity, with a comparison against their reported numbers if possible).
4. Resolve the k-hitting set figure label mismatch to match the text-described baselines.
5. Add confidence intervals or standard errors to the set union results for consistency with the k-hitting set reporting.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>