Now let me finalize the review.

## Summary

The paper studies preference optimization for Large Reasoning Models (LRMs), where the intractable marginal objective over reasoning traces is replaced with a single-sample trace-based gradient. The authors identify that this introduces high gradient variance and propose BVPO, which mixes the trace-based gradient with a low-variance "empty-trace" gradient (obtained by disabling trace generation) via a convex combination. They provide theoretical analysis showing variance reduction, an MSE-optimal mixing coefficient, and tighter SGD convergence bounds, and demonstrate consistent improvements over DPO and SimPO on Arena-Hard, AlpacaEval 2, and six math reasoning benchmarks across three LRM sizes.

## Strengths

1. **Clean, well-motivated idea.** The paper identifies a genuine underexplored problem — trace-induced gradient variance in LRM alignment — and proposes a transparent, implementable solution (convex combination of two gradients). Section 3.2 clearly contrasts the intractable marginal objective ℒ\_m with the practical trace-based proxy ℒ\_t, making the problem framing pedagogically effective and the mismatch easy to understand.

2. **Coherent theoretical chain.** The theory builds logically from variance reduction (Theorem 1: any α∈(0,1) reduces conditional variance from trace sampling), through MSE-optimal mixing (Theorem 2 and Corollary 1: α* guarantees MSE no worse than the better component), to SGD convergence bounds (Theorems 3–4: linking MSE to the error floor of convergence). Each step follows from the previous one, and the connection between bias–variance and optimization error is well-explained.

3. **Consistent empirical gains, especially on smaller models.** BVPO beats DPO and SimPO across all three model sizes and both Thinking/NoThinking modes in Table 1. Gains on the 7B and 1.5B models are substantial (5–8 points on alignment metrics). The math reasoning results in Table 2 provide useful evidence that alignment does not degrade, and may even improve, reasoning ability.

4. **Drop-in simplicity.** BVPO requires only a convex combination of two losses with a single hyperparameter α, and is agnostic to the underlying preference optimization algorithm — straightforward for adoption in existing pipelines.

## Weaknesses

### Fatal
None.

### Major

- **Missing critical baseline: empty-trace DPO (ℒ\_e alone).** The paper compares BVPO (mixing ℒ\_t and ℒ\_e) against DPO (ℒ\_t alone) and SimPO but never reports performance of training with ℒ\_e alone (the empty-trace loss in isolation). Without this ablation, BVPO's improvement mechanism is ambiguous: the gains could come from (a) the claimed variance-reduction from mixing g\_t and g\_e, or (b) simply adding an extra training signal (ℒ\_e) that provides preference information without the noise of trace sampling. If ℒ\_e alone already outperforms DPO, the variance-reduction narrative is weakened. If ℒ\_e alone performs poorly, it would strengthen the variance-reduction claim. This is the single most important ablation the paper omits.

### Minor

- **No uncertainty quantification on any result.** For a paper whose thesis is variance reduction, the absence of any error bars, confidence intervals, or statistical significance testing across all tables (Tables 1 and 2) is conspicuous. Given the small margins on some comparisons (e.g., BVPO 62.3 vs DPO 61.0 average on 7B math — a 1.3 point gap), it is unclear which differences are reliable and which may reflect noise. Reporting variance across training seeds would substantially strengthen the empirical claims.

- **Gap between optimal-α theory and experiments.** The theoretical framing centers on α\* (the MSE-optimal mixing coefficient, Theorem 2), but α\* depends on quantities that require knowing the true marginal gradient μ, which the paper itself states is intractable. The paper provides no practical procedure for estimating α\*, and the optimality guarantees of Theorems 2–4 do not directly translate to the reported results. Theorem 1 (variance reduction for any α∈(0,1)) remains practically useful, but the stronger optimality claims are disconnected from the experimental implementation. Clarifying whether α was tuned, set to a fixed value, or estimated would help close this gap.

- **No direct measurement of gradient variance.** The paper's core motivation is that trace-based gradients have high variance and BVPO reduces it. But no experiment measures gradient variance directly (e.g., trace of gradient covariance over sampled traces for fixed (x, y⁺, y⁻) pairs). The paper references Appendix B for log-probability variance, but gradient variance is a distinct quantity. A direct measurement would be the most natural empirical validation of the central claim.

### Trivial
None.

## Nice-to-Haves

- Reporting the actual α value(s) used in experiments (may already be in the stripped appendix).
- A small-scale direct measurement of gradient variance (e.g., ‖g\_t − μ̃‖² approximated with multiple Monte Carlo samples).

## Removed Points

These points were flagged in the harsh review but are removed per policy:

1. **"The paper never states what value of α was used."** — The experiments section states "Additional experimental details are provided in Appendix C" (line 281). The appendix is stripped by the PDF parser; this information exists in the original submission.

2. **"g\_e is not a proper estimator of the marginal gradient; the bias–variance framing is misleading."** — The paper explicitly defines bias vectors b\_t and b\_e in Section 4.2, acknowledges both are biased (line 95: "the trade-off is a potentially higher bias"), and the theory treats both as biased estimators of μ. The statistical framing is correct and the concern reflects a misreading.

3. **"Closed-form choice is misleading because α\* depends on μ."** — The expression for α\* (Theorem 2) is indeed a closed-form expression in terms of the relevant moments. The practical computability issue is already captured in the retained Minor weakness above. The abstract's phrasing is technically accurate.

## Novel Insights

None beyond the paper's own contributions. The reviewer observations largely confirm the paper's framing and identify gaps the authors should address, but do not reveal structural limitations beyond what the authors have already scoped.

## Suggestions

1. **Add the ℒ\_e-alone baseline.** This is the single most informative ablation for interpreting BVPO's mechanism. The mechanism claim is currently unverifiable without it.
2. **Report variance across seeds or runs.** At minimum, run each method 2–3 times with different random seeds and report mean ± std for the main tables.
3. **Clarify the practical choice of α.** State the value(s) used, whether it was tuned on a validation set, or estimated via some approximation. If the appendix already contains this, ensure it is prominent in the main paper.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>