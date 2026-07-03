Based on my thorough verification of each reviewer claim against the actual paper text, I now produce the final consolidated review.

---

## Summary

This paper provides the first theoretical treatment connecting certified machine unlearning with continual learning under an ℓ₂-regularized framework. It decomposes post-unlearning excess risk into unlearning loss and continual learning (CL) excess risk, adapts gradient-based (natural forgetting) and Hessian-based certified unlearning methods to this setting, and provides (ε,δ)-certified guarantees with explicit bounds. A key analytical contribution shows how unlearning request order affects the Hessian-based method's approximation error, leading to a storage-reducing hybrid algorithm.

## Strengths

1. **Clean decomposition of post-unlearning excess risk (Eqs. 5–7).** The paper identifies that post-unlearning excess risk can be written as the sum of unlearning loss and CL excess risk, and observes a tension: preventing forgetting (which benefits CL) inversely increases unlearning loss. This surfaces a design trade-off absent from prior work on either problem in isolation.

2. **Extension of CL excess-risk bounds from linear to nonlinear convex models (Theorem 3.1).** Prior theoretical work (Lin et al., 2023) was limited to linear models. Theorem 3.1 provides an upper bound for L-Lipschitz, μ-strongly convex, M-smooth losses, capturing dependence on task heterogeneity, sample sizes, and the regularization parameter ρ = λ/(μ+λ).

3. **Analysis of how unlearning request order affects Hessian-based performance (Proposition 5.1, Lemma 5.4).** The paper shows that well-ordered unlearning sequences (tasks unlearned at time tᵢ were trained after the previous unlearning time) simplify the correction, enabling a hybrid that reduces storage from O(td²+2td) to storage proportional to the max gap between consecutive unlearning times.

4. **Explicit storage cost comparison across all three algorithm variants.** Zero for Alg. 1, O(td²+2td) for Alg. 2, hybrid costs proportional to the inter-unlearning gap — clear and comparable.

## Weaknesses

### Fatal
None.

### Major

1. **Theory–experiment mismatch on strong convexity.** Assumption 2.1 requires ℓ to be μ-strongly convex, and the paper's theoretical machinery (ρ = λ/(μ+λ), Hessian invertibility, convergence rates in Theorem 3.1, Theorem 4.1, Proposition 5.1) depends on this being defined. The experiments use softmax + cross-entropy loss on a linear model, which is not strongly convex. The paper acknowledges this at line 288 but merely asserts it "relaxes" the assumption without providing any analysis to justify extending the theory to the non-strongly-convex setting. As a result, the experiments do not operate under the conditions required by the theory, and the reported empirical quantities cannot be directly linked to the theoretical bounds.

2. **Claimed advantage of Hessian-based method is contradicted by experimental results.** The abstract states the Hessian-based algorithm "largely outperforms the gradient-based algorithm" and the conclusion claims it "achieves lower unlearning loss." However, Figure 2(b) shows the natural forgetting algorithm (Alg. 1) has substantially *lower* approximation error (≈0.08–0.10) than the Hessian-based algorithm (≈0.20–0.24) across all λ values tested. Section 5 (line 258) states the Hessian-based method's advantage is a *tighter second-order upper bound* — but the abstract and conclusion phrase this as a general empirical superiority claim, creating a contradiction with the plotted data that is not discussed.

3. **Thin experimental validation.** The experiments use one dataset (MNIST), one model class (linear softmax), no error bars or multiple trials, and only three λ values in the main comparison table (Table 1). The unlearning sequence (Table 2) is in the appendix. The decomposition of post-unlearning excess risk — the paper's conceptual centerpiece — is never empirically decomposed into its two components. No comparison against existing continual learning-unlearning methods is provided. For a paper whose headline contribution includes experimental validation, these limitations significantly weaken the evidence.

### Minor

1. **Anomalous result in Table 1.** At λ=30, the Hessian-based algorithm achieves 71.59% test accuracy while the "perfect retraining" baseline achieves 71.05% — the unlearned model outperforms the supposed upper bound. Without error bars or discussion, this undermines confidence in the evaluation.

2. **Mathematical imprecision in the λ→0 claim (line 168).** The paper states that γ_t(S_{1:t}) "approaches zero for λ = 0 and ρ → 0." From Eq. (9), γ_t = (L/λ) Σ ρ^{...}. As λ→0, ρ = λ/(μ+λ)→0, producing an indeterminate form (∞×0). A proper limiting analysis shows terms with exponent 1 converge to L/μ (non-zero), not zero. The claim is overstated.

3. **Scalability of Hessian storage.** The full Hessian-based algorithm requires O(td²+2td) storage. For networks of practical size (d≥10⁶) this is infeasible. While Section 5.3 proposes a hybrid reduction, it still requires full Hessians over intervals. The paper does not discuss approximate alternatives (diagonal, Kronecker-factored) that might mitigate this.

### Trivial
None.

## Nice-to-Haves

- Empirically measure the two components of the post-unlearning excess risk separately to verify the additive decomposition.
- Discuss the limitation (currently briefly mentioned) that Algorithm 1's internal model still contains deleted data more prominently.

## Removed Points

These points were flagged for removal; treat them with caution.
- **Criticism of "first theoretical investigation" claim vs. related work:** The paper cites system works as lacking theoretical guarantees, which is a reasonable distinction. Not a valid weakness.
- **Parser artifacts in Theorem 3.1 equation** (ρ^{τ_j-τ_j}, zero-norm terms): PDF extraction errors, not paper flaws.
- **Missing Table 2:** The appendix was stripped by the parser; the original submission contains it.
- **Algorithm 1's internal state containing deleted data:** The paper acknowledges this at line 170 and points to Appendix C.2. Already addressed.
- **Proposition 5.2 undefined notation:** Parser extraction artifact.
- **Demand for comparisons to unrelated works outside paper's scope.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Align experiments with theory.** Either modify the experiments to satisfy strong convexity (e.g., use ridge regression or add explicit ℓ₂ regularization to the loss) OR extend the theoretical analysis to cover non-strongly-convex losses.

2. **Resolve the Hessian-advantage contradiction.** Clarify whether the claimed advantage refers to tighter theoretical bounds or lower empirical unlearning loss. If the former, adjust the abstract/conclusion accordingly. If the latter, explain why Figure 2(b) shows the opposite and test on settings (e.g., recent-task unlearning) where the Hessian-based method is expected to excel.

3. **Provide statistically rigorous experiments:** multiple random seeds, error bars, additional datasets, and comparisons against existing continual learning-unlearning baselines.

4. **Fix the λ→0 analysis** or remove the imprecise claim.

5. **Discuss the anomalous λ=30 result** and justify why the unlearning method can exceed retraining.

## Score and Decision

This paper has genuine theoretical contributions — the risk decomposition, extension of bounds to nonlinear convex models, and the analysis of order-dependent Hessian correction are all meaningful advances. However, three structural issues prevent acceptance: (1) the theory relies on strong convexity while experiments violate this assumption without justification; (2) the central claim that the Hessian-based method "outperforms" is contradicted by Figure 2(b) where it has 2–3× higher approximation error; and (3) the experimental evaluation is too thin (one dataset, one model, no error bars) to convincingly validate the theory. The paper requires major revisions to align claims with evidence.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>