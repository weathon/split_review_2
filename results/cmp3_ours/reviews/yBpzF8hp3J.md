## Summary

This paper provides the first absolute utility guarantees (in terms of missing mass) for differentially private set union, analyzing the Weighted Gaussian Mechanism (WGM). It proves near-optimal ℓ₁ missing mass bounds under Zipfian data assumptions, a distribution-free ℓ∞ bound, and extends these to unknown-domain variants of top-k and k-hitting set by using WGM as a domain-discovery precursor. Experiments on six real-world datasets show WGM is competitive with more complex policy-based mechanisms on missing mass.

## Strengths

- **First absolute utility guarantees for DP set union (Section 3).** Prior work gave only relative guarantees (comparing algorithm A to algorithm B) or focused on the single-item-per-user setting. The missing-mass framing is more informative than cardinality-based analysis because it naturally weights items by frequency. The paper correctly identifies and fills this gap (lines 15–16, 31).

- **Distribution-free ℓ∞ bound (Theorem 3.6).** This bound does not require the Zipfian assumption and serves as the foundation for the unknown-domain top-k and k-hitting set guarantees. It is clean and broadly applicable.

- **Lower bounds that match in key parameters (Theorem 3.5, Corollaries 4.4, 4.6).** The lower bound for set union shows near-optimal dependence on ε and N (up to a factor that is small under the Zipfian condition). The lower bounds for top-k and k-hitting set honestly reflect the fundamental cost of operating in the unknown domain.

- **Empirical finding that WGM is competitive with more complex policy mechanisms on missing mass (Figure 1).** Prior work using cardinality had ranked mechanisms differently (e.g., sequential methods outputting ~2× more items). Figure 1 shows WGM outperforms Policy Gaussian and Policy Greedy on missing mass at moderate-to-high Δ₀ values, which is a non-obvious and noteworthy result.

## Weaknesses

### Major
None.

### Minor

- **The k-hitting set guarantee (Theorem 4.5) requires clarification on how the domain restriction interacts with the approximation factor.** The algorithm runs the private greedy mechanism on domain *D* (WGM's output), not the full item universe. The standard (1−1/e) approximation for submodular maximization applies relative to the optimal solution restricted to *D*. Relating this to Opt(W,k) requires showing that the coverage lost from items not in *D* is absorbed into the additive error. The additive error term in Theorem 4.5 contains `k·max_i|W_i|/(ε√q^*)` — which is *k* times the ℓ∞ bound — suggesting this is handled. However, this reasoning is non-trivial and is not sketched in the main paper; the authors should clarify this step.

- **The set union and top-k experiments (Figures 1–2) report only means over 5 trials without error bars or variance.** Only the k-hitting set experiments (Figure 3) report standard error. For the empirical claim that WGM is "competitive with or outperforms existing baselines" to be fully credible, the authors should report the variance across trials or explain why it is negligible. Five trials without any dispersion measure is a standard rigor concern.

- **The most directly contemporary baseline — Chen et al. (2025), described as dominating WGM — is not included in the set union experiments.** The paper cites Chen et al. (2025) as having "proved that the resulting algorithm dominates the WGM (albeit by a small margin, empirically)" (line 29) but compares WGM only against Policy Gaussian and Policy Greedy. The omission is acknowledged in the Future Work section (line 315), but the paper should either include this baseline or explain why it is not directly comparable (e.g., different evaluation metric).

### Trivial
- Theorem 4.5 states the approximation factor as `(1 - 1/ε)` (line 253) which is clearly meant to be `(1 - 1/e)` (Euler's number ≈ 2.718). As written, for ε ≤ 1 the factor could be negative, which is meaningless. The authors should correct this.
- Line 261 writes `q^ε` when it should be `q^*` (the definition from lines 131, 145, etc.). This appears to be a formatting artifact.

## Nice-to-Haves
- Provide concrete numerical values for σ, T, and λ used in the experiments, or at least describe how they were instantiated from the asymptotic guarantees.
- Add a brief proof sketch in the main paper of how the ℓ∞ bound on missing mass (Theorem 3.6) translates into the coverage guarantee for k-hitting set (Theorem 4.5), to make the argument self-contained.

## Removed Points
These points are flagged to be removed; treat them with caution.
- **Concern about the k-hitting set guarantee being a "structural issue" or potentially incorrect** — removed. The additive error term in Theorem 4.5 already contains `k·max_i|W_i|/(ε√q^*)` = k × (ℓ∞ bound), which is precisely the quantity needed to absorb coverage lost from items not in D. Whether the proof succeeds is a question for the appendix (which exists in the original submission), not a verifiable flaw from the main paper. The concern is retained only as a Minor clarity weakness.
- **Criticism that the ℓ∞ bound suppresses explicit β dependence** — removed; this is standard for Õ notation and not a meaningful weakness.
- **Missing related works** — removed per policy.
- **Undisclosed hyperparameters and reproducibility nitpicks** — removed per policy.
- **Formatting/typo criticisms** — removed per policy, though the substantive content of `1/ε` → `1/e` is noted in Trivial.
- **Strength about addressing an important problem** — removed as generic.

## Novel Insights

None beyond the paper's own contributions. The main insight from the reviews is that the additive error structure in Theorem 4.5 already has the right form to absorb the restricted-domain issue the harsh critic raised, but this should be made explicit in a proof sketch.

## Suggestions

1. **Clarify Theorem 4.5** — add a remark (or 2–3 sentence proof sketch) showing how the (1−1/e) approximation on restricted domain D combines with the ℓ∞ missing mass bound to yield the stated bound in terms of Opt(W,k).
2. **Add error bars or confidence intervals to Figures 1–2**, or state that variance across the 5 trials was negligible.
3. **Either include the Chen et al. (2025) baseline** in the set union experiments, or add a sentence explaining why it is not directly comparable.
4. **Correct the formatting errors** in Theorem 4.5 (`1/ε` → `1/e`) and line 261 (`q^ε` → `q^*`).

---

### Calibration Anchors

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| `bEgDEyy2Yk` | 1.00 | R1 | Unrelated paper (reject) — far below this paper's quality |
| `uxFme785fq` | 2.50 | R1 | DP + BLB paper (reject) — less contribution, thin experiments |
| `S6Dn3uyM2p` | 4.60 | R1 | DP MinHash (reject) — comparable to mid-range but rejected |
| `yfZJdCijo6` | 5.25 | R1 | Max coverage streams (reject) — related problem but rejected |
| `uqWM9hBDAE` | 7.33 | R1 | Missing mass estimation (accept) — stronger experiments |
| `yLhJYvkKA0` | 6.67 | R1 | DP hierarchical clustering (accept) — similar structure, comparable contribution |
| `fbqOEOqurU` | 7.00 | R1 | DP matrix mechanism optimality (accept) — deeper theory, no experiments |
| `txV4dNeusx` | 6.25 | R1 | DP privacy amplification (accept) — similar rigor level |
| `hkSjjs4o5d` | 6.50 | R1 | DP clustering for well-clustered graphs (accept) — similar theory+experiments |
| `hVTaXJ0I5M` | 6.75 | R2 | Privately counting partial orders (accept) — comparable contribution |
| `JQQDePbfxh` | 6.50 | R2 | DP mechanism design (accept) — comparable quality |
| `2cF3f9t31y` | 6.50 | R2 | Private data selection (accept) — comparable |

**Round 1 bracket:** 6.0 – 7.5  
**Round 2 narrowing:** The paper's theoretical contribution (first absolute guarantees for DP set union) is genuine and well-executed. The empirical evaluation has minor gaps (no error bars in two of three experiment sets, one omitted baseline) but the main empirical claim is supported. The k-hitting set clarity concern is addressable. The paper sits comfortably alongside accepted DP theory+experiments papers scoring 6.5–7.0.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>