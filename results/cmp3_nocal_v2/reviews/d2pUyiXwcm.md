## Summary

This paper proposes SCaSML, a framework that uses classical defect correction to derive a PDE describing the error of a pre-trained surrogate model (PINN or GP), then solves that error PDE with a Multilevel Picard (MLP) Monte Carlo method to refine the surrogate's prediction at inference time without retraining. The authors prove a product-form error bound and demonstrate consistent error reductions (6.6%–66%, depending on setting) across high-dimensional semi-linear parabolic PDEs up to 160 dimensions.

## Strengths

- **Consistent empirical improvement across all test problems.** Table 1 shows SCaSML achieves lower relative L² error than the base surrogate in every single row — across PINN and GP surrogates, across dimensions 10–160, and across all four PDE families (LCD, VB, LQG, DR). The improvement is not uniform (6.6%–66%), but the direction is universal, providing meaningful evidence that the defect-correction idea is empirically effective.

- **The hybrid approach succeeds where pure MLP simulation fails catastrophically.** For the LQG (HJB) problem, the naive MLP solver produces >500% relative L² error, while SCaSML improves on the surrogate (LQG 100d: 7.97% → 5.53%). This demonstrates genuine value from the hybrid design in a challenging regime.

- **The core mathematical derivation is correct and the theoretical analysis is principled.** The derivation of the defect PDE (Fact 2.3) is algebraically sound, and the key observation — that the error PDE preserves the semi-linear structural form needed for MLP solvers — is correctly identified. Theorem 2.5 gives a clean product-form bound, and the asymptotic complexity result (Corollary 2.6) follows from standard MLP analysis.

- **The paper acknowledges the control-variate interpretation** (line 328) and correctly explains why classical defect correction's iterative error expansion does not apply to neural network surrogates (lines 125–129).

## Weaknesses

### Major

- **The headline "20–80% error reduction" does not hold uniformly across the reported experiments, and the cost-performance trade-off is often unfavorable.** Checking the actual per-problem reductions against Table 1:

  | Problem | Reduction range | Max cost ratio |
  |---------|----------------|---------------|
  | DR (100–160d) | **6.6%–10.9%** | 234× |
  | LQG (100–160d) | 11.7%–30.8% | 88× |
  | VB-PINN (20–80d) | 16.2%–66.1% | 12× |
  | LCD (10–60d) | 20%–56.9% | 134× |

  For DR 160d: 7% reduction at **234× the runtime** of the surrogate alone. The abstract and introduction repeatedly state "20–80%" as a uniform characterization (lines 9, 33), which is misleading — six of sixteen settings fall below 20%. The paper's own Section 3.4 acknowledges 6.6% for DR, but the summary language does not reflect this range. A practitioner reading only the abstract would substantially overestimate the method's benefit in the cases where the trade-off is weakest.

- **The "naive MLP" baseline is compared under substantially different hyperparameter regimes, weakening the claim that SCaSML outperforms pure simulation.** Specifically, the clipping thresholds differ by factors of 100–1000 between naive MLP and SCaSML (LQG: 10 vs 0.1; DR: 10 vs 0.01; VB: 1.0 vs 0.01), and both methods use only n=2 levels — a shallow hierarchy for high-dimensional MLP. The paper justifies the different clipping thresholds (lines 250–251: the defect PDE has smaller magnitude solutions), which is reasonable in principle. However, the reader cannot determine from the presented evidence whether the naive MLP's catastrophic failure on LQG (563% error) and poor performance on DR would persist with properly tuned clipping and more levels. A sensitivity study (e.g., showing naive MLP performance under multiple clipping values and level counts) would be needed to conclude that SCaSML is genuinely superior to a well-configured pure simulation approach, rather than just better than an undertuned one.

### Minor

- **The "2m computational budget" intuition conflates quantities that are not comparable, and the framing overstates the simplicity of the cost analysis.** The paper writes (line 105): "If the surrogate achieves error ~m⁻ᵞ using *m* training points... By averaging over *m* new Monte Carlo paths... total budget of 2*m* function evaluations." The *m* collocation points used during training are not "function evaluations" comparable to *m* Monte Carlo path simulations — training involves thousands of gradient steps on those points, while each Monte Carlo path involves simulating an SDE with surrogate evaluations at every step. The actual runtime ratios in Table 1 (20–234×, not 2×) show this is not a 2× overhead. The formal analysis (Theorem 2.5, Corollary 2.6) uses the standard MLP complexity notation and does not rely on this "2m" framing, but the intuitive account in both Section 2.1 and Section 2.4 gives a misleading picture of the true cost.

- **Some novelty claims are overstated.** The derivation in Fact 2.3 is a straightforward algebraic manipulation (substitute *u* = *û* + *ũ*, subtract the surrogate's PDE). The observation that semi-linear structure is preserved is correct but follows directly from the algebraic form. Calling this "the first derivation that preserves the semi-linear structure" (line 31) is implausible given the simplicity of the algebra. Similarly, "the first physics-informed inference-time scaling framework" (line 328) is defensible as new terminology but the underlying mechanism (surrogate-as-control-variate for Monte Carlo) is well-established in computational statistics. The paper itself acknowledges the control-variate connection (line 328), which partially mitigates this, but the "first" claims should be toned down.

- **Error bars (standard deviations / confidence intervals) are not reported for the main results in Table 1.** Given the stochasticity of both PINN training and MLP sampling, point estimates alone do not convey the reliability of the reported error reductions. The paper mentions statistical significance tests (p ≪ 0.001) in the appendix, but the main table would benefit from variance information.

### Trivial

- None (the paper is clearly written; the formatting artifacts in the extracted text are parser issues, not author errors).

## Nice-to-Haves

- A compute-normalized comparison (e.g., SCaSML + weaker surrogate vs. stronger surrogate at equal total budget) would directly test the "elastic compute" claim. The paper mentions fixed-budget comparisons in Appendix G.7, which addresses this in part.
- An ablation separating the benefit of (a) the surrogate-informed defect PDE vs. (b) simply averaging Monte Carlo samples would clarify the source of the improvement.
- A runtime breakdown showing what fraction of SCaSML's cost is spent on surrogate gradient evaluations vs. SDE simulation.

## Removed Points

- **"Theorem and algorithm are partially mismatched"** (criticizing the global sup bound vs. pointwise evaluation). Removed because this misreads the theorem: Theorem 2.5 bounds the *statistical error* of the MLP estimator at any point (t,x) — the sup over (t,x) of the L² (over randomness) error is a standard MLP guarantee, not a claim about dense evaluation over the whole domain. The bound applies per query point.
- **Criticism that "2m" framing fundamentally undermines the convergence analysis.** Removed as overstatement. The formal analysis (Theorem 2.5, Corollary 2.6) uses standard MLP complexity notation (N, M, d, ε) and does not rely on the "2m" simplification. The "2m" framing appears only in the intuitive explanation. The point about cost conflation is kept as a Minor weakness above, appropriately scaled.
- **"The improvement is not as substantial as the headline suggests"** — kept as a Major weakness with specific numbers from Table 1. The generalized framing about "not substantial" was replaced with a precise accounting of which settings fall below 20%.

## Novel Insights

None beyond the paper's own contributions. The reviewer's identification of the cost-performance disparity in specific DR settings is a useful quantitative check, but the relevant data is fully present in Table 1 — the reviewer added no information not already in the paper.

## Suggestions

- Revise the abstract and introduction to report the *range* honestly (e.g., "6–66% reduction, with settings above and below 20%") rather than the misleading "20–80%."
- Add standard deviations or confidence intervals to Table 1.
- Include a sensitivity study for the naive MLP baseline across multiple clipping thresholds and level counts, so readers can assess whether the poor naive MLP performance is due to insufficient tuning.
- Tone down the "first" claims: acknowledge that the derivation is algebraically straightforward and that the method relates to control-variate Monte Carlo, which is known in computational statistics.
- Clarify in the main text (not just the appendix) that the "2m" intuition is a pedagogical simplification and that actual wall-clock costs are reported in Table 1.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>