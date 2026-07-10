Now let me produce the final consolidated review.

## Summary

This paper introduces FedMPDD, a federated learning algorithm that encodes each client's gradient by computing directional derivatives along multiple random vectors (projections). Clients transmit m scalars (plus a seed) instead of the full d-dimensional gradient, compressing communication from O(d) to O(m). The server reconstructs an estimate of the gradient, and the paper argues that the low-rank nature of the projection provides inherent privacy against gradient inversion attacks. The core idea of using multi-projected directional derivatives for joint compression and privacy is motivated and the paper provides a theoretical convergence analysis (Theorem 2) along with empirical evaluations on MNIST and CIFAR-10.

## Strengths

- **Lemma 1 gives a clean, verifiable calculation** (line 134): the relative reconstruction error of (d-1)/m for the multi-projected estimator provides a concrete quantitative link between the number of projections m and the information loss, which the paper repurposes as a privacy metric.

- **The multi-projection averaging extension (FedMPDD) over a single projection (FedPDD) is a well-motivated fix** for the dimension-dependent variance issue. The paper correctly identifies that the single-projection estimator has a √d magnitude scaling (line 96: 𝔼[∥ĝ∥²] = d∥g∥²) and shows that averaging m projections reduces this.

## Weaknesses

### Fatal

- **The JL-based norm preservation claim (lines 108–112) is mathematically incorrect and invalidates Theorem 2.** The paper states that the mapping (1/m)UU^T satisfies the JL lemma, implying m = O(log d/ε²) projections suffice to approximately preserve gradient norm. However, the JL lemma applies to the dimensionality-reducing projection (1/√m)U^T g ∈ ℝ^m, **not** to the reconstruction (1/m)UU^T g ∈ ℝ^d. The estimator's expected squared norm is 𝔼[∥ĝ∥²] = (1 + (d-1)/m)∥g∥², giving a norm scaling of √(1+d/m)∥g∥ for m ≪ d — far larger than (1+ε)∥g∥. Standard random matrix theory (covariance estimation of subgaussian vectors) shows that the correct scaling is m = Ω(d/ε²), not logarithmic. This means the claimed convergence guarantee in Theorem 2 does not follow from the arguments given, and the logarithmic communication savings claimed in the theory are unsupported.

### Major

- **The fundamental privacy-utility tension is acknowledged but not resolved.** Lemma 1 gives reconstruction error as (d-1)/m, which the paper uses as a privacy metric (large error = good privacy). But the same estimator drives optimization. For m ≪ d (the regime where privacy and communication savings are both meaningful), the reconstruction error is enormous (e.g., d=300K, m=600 gives relative error ≈ 500), and the estimator's norm is inflated by roughly √(d/m). Without the (incorrect) JL argument, the paper provides no explanation of how such an estimator can converge at the same rate as FedSGD. Theorem 2's convergence bound depends on the JL distortion parameter ε, and once the JL argument is removed, the analysis collapses.

### Minor

- **Abstract vs. Theorem 2 convergence rate inconsistency.** The abstract (line 9) claims O(1/K) convergence matching FedSGD, while Theorem 2 (line 114) and the introduction (line 32) both state O(1/√K). In the standard non-convex setting assumed by the paper, SGD converges at O(1/√K), not O(1/K). This is a factual error in a headline claim.

- **Empirical claim contradicts the theory.** The paper states (line 226) that "smaller values of m can actually achieve comparable or even faster convergence to the target accuracy" while also stating "increasing m accelerates convergence." The latter is consistent with Theorem 2; the former contradicts it. The paper offers only a hand-wavy explanation (the "nullspace effect"), without reconciling this with the theory.

- **Privacy claims overstate what is established.** Remark 2 (line 148) states that "privacy is guaranteed if T × m < d." This condition ensures the gradient is not uniquely determined by *linear* measurements, but does not account for nonlinear inversion attacks (e.g., using image priors) that can succeed with far fewer than d measurements. The language of "guarantee" overstates what is actually proven.

- **No error bars or variance reporting.** Tables 1 and 2 report single numbers without standard deviations or confidence intervals, despite the method's inherent randomness from random projections and client sampling.

### Trivial

- **LDP baselines** use a few discrete noise levels (var=0.1, 0.5, 1, 10) without systematic ε-calibration; intermediate noise levels could reveal a different trade-off.

## Nice-to-Haves

- The paper would benefit from comparison against methods explicitly designed for joint compression and differential privacy (e.g., Amiri et al. 2021, Agarwal et al. 2018), which are cited but not evaluated. This would strengthen the positioning that FedMPDD offers a unique combination of properties.

- A sensitivity analysis sweeping m systematically (beyond what appears in the appendix) would help clarify where the privacy–utility–communication trade-off breaks.

## Removed Points

These points are flagged to be removed; treat them with caution:
- Critic's claim that Section 1 oversimplifies the landscape about structured/sketched methods using fresh randomness: removed because the cited methods predominantly use fixed subspaces or hash functions, so the paper's characterization is broadly accurate.
- Critic's claim about the rank-1 argument in Equation (3) being "misleading" about privacy: removed because the paper's main algorithm is FedMPDD (multi-projection), not FedPDD; Lemma 1 provides the formal bound for the multi-projection case.
- Critic's generic strength about the problem being motivated by a real problem: removed as too generic.
- Critic's point about missing sensitivity analysis for m: removed because the paper states m was chosen from theory and references appendix results across a range of m values.
- Critic's point about no wall-clock time: removed because Remark 1 discusses computational cost and references appendix data.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Replace the JL argument entirely** with a direct variance-based convergence analysis. Lemma 1 already gives 𝔼[∥ĝ−g∥²] = ((d-1)/m)∥g∥²; use this to honestly derive how m must scale with d for a meaningful convergence guarantee. This will reveal whether the claimed communication savings are supported.
2. **Fix the abstract** to state O(1/√K) (consistent with Theorem 2) or specify if a different (e.g., strongly convex) setting is assumed.
3. **Reconcile the empirical observation** about smaller m giving faster convergence with the theory, or clearly flag it as an unexplained phenomenon.
4. **Add error bars** to experimental results given the method's randomness.
5. **Tone down the privacy language** to reflect that the guarantee is about gradient ambiguity rather than formal privacy protection against all attacks.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>