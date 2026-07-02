## Summary
# Final Review Report

## Summary

This paper studies differentially private (DP) domain discovery, where each user holds a subset of items from an unknown domain and the goal is to output an informative subset of items while preserving DP. The paper makes three primary contributions:

1. **Reframing via missing mass:** It proposes evaluating DP set union algorithms by missing mass (fraction of total item frequency not recovered) rather than cardinality (number of unique items recovered). Under this lens, the paper proves that the Weighted Gaussian Mechanism (WGM) has near-optimal ℓ₁ missing mass on Zipfian data (Theorem 3.3) and a distribution-free ℓ∞ missing mass guarantee (Theorem 3.6).

2. **New unknown-domain algorithms:** Using WGM as a domain-discovery primitive, the paper designs two-stage algorithms for unknown-domain top-k selection and k-hitting set, obtaining new utility guarantees (Theorems 4.3 and 4.5) that do not require distributional assumptions.

3. **Empirical evaluation:** Experiments on six real-world datasets at (1,10⁻⁵)-DP show that WGM-based methods are competitive with or outperform existing baselines for set union, top-k, and k-hitting set.

The paper is well-structured, with clear theoretical contributions: it provides the first absolute (rather than relative) utility guarantees for DP set union, and extends these to two downstream tasks. The theoretical analysis includes both upper and lower bounds, demonstrating near-optimal scaling with ε and N for the core set union problem.

However, the paper also has several limitations. The experimental evaluation has statistical weaknesses (only 5 trials, no variance reporting), the comparison baselines for k-hitting set are not fully privacy-preserving, and there are typographical errors in key theorem statements (e.g., (1-1/ε) instead of (1-1/e) in Theorem 4.5). The novelty claims cannot be fully verified without external literature search (disabled in this run).

## Strengths
**S1 — Novel missing-mass framing with theoretical foundation.** The paper's core conceptual contribution — reframing DP set union from cardinality to missing mass — is well-motivated and yields a clean analytical framework. The missing mass objective captures item frequency information that cardinality discards, making it more informative for downstream applications. The theoretical analysis is rigorous: Theorem 3.3 provides a high-probability upper bound on ℓ₁ missing mass under Zipfian data, Theorem 3.5 gives a nearly matching lower bound (matching in ε and N dependence), and Theorem 3.6 extends to a distribution-free ℓ∞ bound.

**S2 — First absolute utility guarantees for DP set union.** As the paper correctly notes, prior work provides only relative utility guarantees (comparing algorithms against each other). Theorem 3.3 and Corollary 3.4 represent the first absolute bounds showing how the missing mass depends on dataset parameters (C, s, N, max_i|W_i|) and privacy parameters (ε, δ). This is a genuine step forward for the theory of DP set union.

**S3 — Clean extension to downstream tasks.** The meta-algorithm (WGM for domain discovery + known-domain algorithm for the target task) is conceptually clean and practically relevant. Theorems 4.3 and 4.5 provide the first utility guarantees for unknown-domain top-k and k-hitting set, respectively. The ℓ∞ missing mass bound (Theorem 3.6) elegantly enables these extensions without requiring distributional assumptions on the downstream data.

**S4 — Economical and reproducible algorithm.** The WGM is simple, requiring only subsampling, weighted histogram construction, and Gaussian thresholding. Unlike sequential/adaptive methods (Policy Gaussian, Policy Greedy), WGM is trivially parallelizable and scalable. The paper provides code and dataset processing scripts in the supplement.

**S5 — Practical relevance.** Domain discovery is a real bottleneck in industrial DP systems (Plume, OpenDP). The paper connects its theoretical contributions to practical deployment contexts, and the empirical evaluation uses six real-world datasets from diverse domains (Reddit, Amazon Games, MovieLens, Steam, Amazon Magazine, Amazon Pantry).

## Weaknesses
### W1 — Typographical errors in key theorem statements (Major)

Theorem 4.5 contains two critical typographical errors that affect interpretability. The approximation factor is written as $(1 - 1/\epsilon)$, where $\epsilon$ is the privacy parameter. This is clearly a typo for $(1 - 1/e)$ (the standard $(1-1/e)$ approximation factor for greedy submodular maximization). For $\epsilon < 1$, $(1 - 1/\epsilon)$ would be negative, making the bound meaningless. Additionally, the error bound on line 138 has $q^\epsilon$ in the denominator where it should be $q^*$. These errors must be corrected before publication.

**Location:** Page 7 — Section 4.2, Theorem 4.5 statement and subsequent discussion.
**Fix required:** Replace $(1 - 1/\epsilon)$ with $(1 - 1/e)$ in Theorem 4.5, and replace $q^\epsilon$ with $q^*$ in line 138.

### W2 — Insufficient statistical rigor in experiments (Major)

All experimental results (Figures 1-3) report averages over only 5 trials without standard deviations, standard errors, confidence intervals, or statistical significance tests. The set union results claim WGM is "within 5%" of policy mechanisms, but with only 5 trials and no variance reporting, this gap could be within the noise of the measurements. The paper also does not report how the random subsampling step (Algorithm 1, step 1) affects the variance of the results across different subsampling seeds.

**Location:** Pages 7-9 — Section 5, Experiments.
**Fix required:** (1) Report mean $\pm$ standard deviation over at least 5 seeds (ideally 10-20). (2) Add paired bootstrap confidence intervals for the difference between WGM and the strongest baseline. (3) Report the effect of subsampling randomness by fixing or varying the subsampling seed.

### W3 — Unfair baseline comparisons for k-hitting set (Major)

The k-hitting set experiments compare against a non-private greedy algorithm and a "private" algorithm that assumes public knowledge of $\bigcup_i W_i$ (which is private in the unknown-domain setting). As the paper acknowledges, neither baseline is a valid private algorithm for the unknown domain. While the paper honestly discloses this limitation, presenting the results as "our method performs comparably with both baseline methods" could mislead readers into thinking the method is more competitive than it is. A proper unknown-domain private baseline (e.g., WGM followed by random selection of k items) should be the primary comparison.

**Location:** Page 8 — Section 5.3, k-hitting set experiments.
**Fix required:** (1) Make the WGM+random-selection baseline the primary fair comparison. (2) Add a proper DP baseline that uses the same privacy budget composition. (3) Explicitly state that both existing baselines violate the unknown-domain privacy model and are included only as upper/lower bound references.

### W4 — Near-optimality claim not fully qualified (Moderate)

The paper claims WGM has "near-optimal ℓ₁ missing mass" on Zipfian data. The upper bound (Corollary 3.4) and lower bound (Theorem 3.5) match in their $\epsilon$ and $N$ dependence, but the upper bound contains additional terms ($\max_i|W_i|/\sqrt{q^*}$) that do not appear in the lower bound. The "near-optimal" claim applies only to the $\epsilon$ and $N$ scaling, not to all parameters. This qualification should be stated explicitly.

**Location:** Pages 4-5 — Sections 3.2 and 3.3, Theorem 3.5 discussion.
**Fix required:** Add a sentence explicitly stating that the near-optimality is with respect to $\epsilon$ and $N$ dependence, and that the dependence on $\max_i|W_i|$ and $\Delta_0$ may not be tight.

### W5 — Missing motivation and intuition for key mechanism choices (Moderate)

The WGM weighted histogram uses $1/\sqrt{|\tilde{W}_i|}$ normalization, but the paper does not explain why this specific weight is chosen. The weight directly controls the $\ell_2$ sensitivity of the histogram, which determines the required noise level $\sigma$ and threshold $T$. Without this intuition, readers cannot assess why WGM works. Similarly, Theorem 3.2's privacy condition is stated as opaque CDF inequalities without explanation of how they lead to the claimed asymptotic rates.

**Location:** Pages 3-4 — Section 3.1, Algorithm 1 and Theorem 3.2.
**Fix required:** Add 1-2 sentences explaining the weighting intuition (each user's total $\ell_2$ contribution is at most 1), and provide a brief sketch of how the CDF conditions in Theorem 3.2 simplify to $\sigma = \Theta(\epsilon^{-1}\sqrt{\log(1/\delta)})$.

### W6 — Abstract lacks self-contained motivation (Minor)

The abstract jumps directly into technical results without establishing the stakes. It does not follow the recommended problem → significance → gap → method → result structure. Readers unfamiliar with DP set union may not understand why reframing from cardinality to mass is valuable.

**Location:** Page 1 — Abstract.
**Fix required:** Restructure as: S1 (problem and stakes) → S2 (gap in prior work) → S3 (method: missing mass reframing) → S4 (key theoretical results) → S5 (empirical validation).

### W7 — Related Work organized chronologically rather than thematically (Minor)

The DP set union related work paragraph lists papers in chronological order, making it hard for readers to understand the key design dimensions (single-item vs multi-item, adaptive vs non-adaptive, cardinality vs mass). The "first to prove absolute utility guarantees" novelty claim cannot be externally verified in this review run.

**Location:** Page 1 — Section 1.1, DP Set Union paragraph.
**Fix required:** Reorganize around comparison axes (single-item vs multi-item, cardinality vs mass, adaptive vs non-adaptive). Qualify the "first" claim as "to our knowledge, the first absolute utility guarantee for the missing mass objective."

### W8 — Composition approach uses basic composition without discussion (Minor)

The meta-algorithm (Algorithm 2) splits the privacy budget equally between WGM and the downstream algorithm using basic composition. Tighter composition theorems (e.g., Rényi DP, zCDP) could yield better constants. While this does not affect asymptotic guarantees, it is a practical limitation.

**Location:** Page 5 — Section 4, Algorithm 2 discussion.
**Fix required:** Acknowledge that basic composition is chosen for simplicity and that tighter composition could improve constants.

## Score
**Final Score: 6/10**

**Rationale:** The paper's core theoretical contributions — the missing-mass reframing and the first absolute utility guarantees for DP set union — are genuinely novel and fill a gap in the DP literature. The upper and lower bounds are nearly matching in their ε and N dependence, and the extensions to unknown-domain top-k and k-hitting set are clean and useful. The empirical evaluation on six real-world datasets demonstrates practical relevance.

However, the score is limited by several factors:
- **Typographical errors in Theorem 4.5** ($(1-1/\epsilon)$ instead of $(1-1/e)$, $q^\epsilon$ instead of $q^*$) undermine confidence in the theoretical presentation and must be corrected.
- **Weak experimental statistics** (only 5 trials, no variance reporting) make it difficult to assess the statistical reliability of the empirical claims.
- **Unfair baselines for k-hitting set** (non-private greedy and a known-domain method that is not a valid unknown-domain algorithm) weaken the empirical contribution.
- The **near-optimality claim** is not fully qualified for all parameters.
- **External literature verification** was not available in this review run, so novelty claims could not be independently validated.

With the major typographical errors fixed and strengthened experimental reporting, the paper's score could improve to approximately 7.5/10. The theoretical core is solid; the main revision targets are in the presentation and experimental sections.