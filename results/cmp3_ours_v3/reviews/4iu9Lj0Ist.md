Now let me finalize the review with proper calibration.

## Final Review

Let me write the complete review.

**Summary of calibration anchors:**

| Anchor | Score | Decision | Topic | Comparison to this paper |
|--------|-------|----------|-------|-------------------------|
| C3TrHWanh5 | 6.0 | Accept | Hessian-free certified unlearning | Stronger experiments, no internal contradictions |
| HVFMooKrHX | 6.6 | Accept | Utility/complexity of unlearning | Stronger theory, no claim-experiment conflicts |
| CGfWyU28Pd | 4.5 | Reject | Fine-tuning theory for unlearning | Comparable: theory with weak experiment connection |
| nSYycd5tEC | 4.0 | Reject | Replay theory for continual learning | Weaker theoretical framing but no claim contradictions |
| GicZtgSlJW | 5.0 | Reject | Constrained optimization for CL | More mixed reviews wider variance |

**Round 1 bracket: 3.5–5.5** (below accepted papers due to internal claim-evidence conflict, but above bottom due to genuine theoretical novelty)

**Final score: 4.5** — The theoretical framework (problem formulation, risk decomposition, extension of bounds to nonlinear convex models) is genuinely novel and well-motivated. However, the paper claims "Hessian-based largely outperforms gradient-based" while the only direct experimental comparison (Fig 2b) shows the opposite (2–3× worse approximation error), and this contradiction is unacknowledged. The experiments also violate the theory's core strong-convexity assumption while being presented as "validation." These issues prevent acceptance in the current form but are addressable.

---

## Summary

This paper establishes a theoretical framework connecting certified machine unlearning with continual learning. It defines a two-stage process (continual learning on new tasks, then unlearning on deletion requests), decomposes post-unlearning excess risk into unlearning loss plus continual-learning excess risk, and adapts two certified unlearning approaches (gradient-based natural forgetting and Hessian-based) with theoretical guarantees. The theoretical framework is the paper's main contribution.

## Strengths

1. **Novel problem formulation.** The observation that certified unlearning algorithms assume static datasets while real systems train continually is well-motivated. The two-stage model (Fig. 1) cleanly captures the interaction between sequential task learning and intermittent deletion requests, formalizing constraints (e.g., tasks can only be deleted once) that make the problem well-posed.

2. **Clean decomposition of post-unlearning excess risk (Eqs. 5–7).** Separating the total error into unlearning loss (from the unlearning algorithm) and excess risk (from continual learning) is conceptually insightful and reveals a genuine trade-off: a continual learning algorithm that prevents forgetting (large λ) may increase unlearning loss. This framing is used throughout the analysis and is the paper's most elegant conceptual contribution.

3. **Two adapted algorithms with complementary storage-accuracy profiles.** The natural forgetting algorithm (Alg. 1) adds noise directly with zero additional storage, while the Hessian-based algorithm (Alg. 2) provides second-order corrections at O(td²+2td) cost. The combination method in Section 5.3—applying Hessian corrections to recent tasks and natural forgetting to older ones—is a practical compromise.

4. **Extension of excess-risk bounds to nonlinear convex models.** Theorem 3.1 extends prior ℓ₂-regularized continual learning bounds (previously limited to linear models) to general convex, L-Lipschitz, M-smooth, μ-strongly-convex losses.

## Weaknesses

### Major

1. **Claim-evidence contradiction: the experiments contradict the paper's central comparative claim.** The abstract states "Our analysis shows that our Hessian-based adaption algorithm largely outperforms the gradient-based algorithm," and Section 5.2 states "[Alg. 2] achieves a lower post-unlearning excess risk than Alg. 1." However, **Figure 2(b)—the only direct experimental comparison between the two algorithms—shows the opposite**: the natural forgetting algorithm (Alg. 1) has an approximation error / unlearning loss of ~0.08–0.10, while the Hessian-based algorithm (Alg. 2) has an error of ~0.20–0.24, i.e., 2–3× **worse** across all λ values. The paper does not acknowledge or explain this discrepancy anywhere in the text. Furthermore, Table 1 reports post-unlearning accuracy only for Hessian-based unlearning with no equivalent row for Alg. 1, so even the combined metric cannot be compared. This is not a missing ablation—it is a coherence failure between the paper's thesis and its own evidence. 

   *Mitigation note*: The phrase "analysis shows" could refer to the theoretical bounds (second-order vs. first-order). But the experiments are explicitly presented as validation ("We validate these theoretical findings with experiments"), and when the only experimental comparison contradicts the claim, the validation claim is unsupported. The paper must either explain why the experiments are not intended as comparative validation, or reconcile the discrepancy.

2. **Experiments do not test the theory because they violate a core theoretical assumption.** The entire theoretical framework (Assumption 2.1, Theorem 3.1, Theorem 4.1, Proposition 5.1, Corollary 5.3) assumes the loss function is **μ-strongly convex**. The experiments (Section 6) use a linear model with softmax output and cross-entropy loss, which is **not strongly convex**. The paper acknowledges this at line 288 ("we relax its assumption of μ-strong convexity here in order to show the more general results under a non-strongly convex setting") but still presents the experiments as validating the theory. Since the theoretical guarantees are derived under strong convexity, experiments that explicitly violate this condition cannot serve as validation of those guarantees. At minimum, the paper needs a formal argument (or reference) that the bounds degrade gracefully under this relaxation.

3. **Insufficient experimental evaluation for the strength of the claims.** The experiments consist of one dataset (MNIST), one model (a linear classifier—far from the "nonlinear convex models" the theory addresses), no standard deviations or multiple trials, and no baseline comparisons (not even a simple "retrain from scratch" runtime comparison). Table 1 shows the unlearning accuracy (71.59% at λ=30) *exceeding* the "perfect retraining" accuracy (71.05% at λ=30), which suggests the results are dominated by noise or an implementation artifact rather than providing meaningful signal. For a paper making "first theoretical foundation" claims and drawing strong comparative conclusions, this level of empirical support is inadequate.

### Minor

4. **No comparison on the combined post-unlearning excess risk metric.** The paper's own decomposition identifies post-unlearning excess risk as the metric that matters. Table 1 reports it only for Alg. 2, omitting Alg. 1. Without a direct comparison on this combined metric, the central comparative claim cannot be evaluated.

5. **Proposition 5.2's second-order bound has a recursive dependence that is not analyzed.** The bound in (15) depends on the *squared* norm of model differences from *previous* unlearning steps: for the bound to imply convergence, one must show the base error is < 1, which the paper does not establish. Without this, the claimed theoretical advantage of the Hessian-based algorithm's second-order bound over the natural forgetting algorithm's first-order bound is not rigorous.

6. **"Zero storage" claim for Alg. 1 is imprecise.** Alg. 1 stores the current model parameters (d dimensions). While minimal compared to Alg. 2's quadratic storage, calling it "zero storage" is misleading.

### Trivial

7. None. The paper is generally well-written for a theory paper.

## Nice-to-Haves

- A comparison with a simple "retrain from scratch" baseline would contextualize the benefits of both algorithms.
- Error bars or multiple trials are essential given the noise suggested by Table 1 (unlearning accuracy exceeding retraining).
- A discussion of how theoretical parameters (L, μ, M, ‖wᵢ*−wⱼ*‖) might be estimated or bounded in practice would strengthen the practical relevance.
- A concrete example showing the Hessian update for a simple case (e.g., two tasks, one unlearning request) would improve readability of Section 5.

## Removed Points

- **Indexing errors in Theorem 3.1 bound**: The reviewer noted potential issues like "ρ^{τ_j − τ_j}" and "‖w_{τ_j}^* − w_{τ_j}^*‖" which would be ρ⁰=1 and zero respectively. These may be PDF parsing artifacts from the automated extraction; the original submission likely has correct indices. Removed per the parser-artifact rule.
- **"First theoretical investigation" claim**: The reviewer suggested this could be tempered since the paper itself cites related work. This is a scope judgment, not a verifiable error. Removed as not a concrete weakness.
- **Section-by-section presentation notes**: Many were minor observations about notation density or missing appendix details that are either presentation preferences or parser-stripped content. Removed per filtering rules.
- **Strong convexity assumption critique for the Hessian-bound paper (C3TrHWanh5)**: The reviewer's comparison to this anchor is noted but does not constitute a weakness of the current paper.
- **"Missing related works" concerns**: Removed per instructions — I cannot verify existence of external works.

## Novel Insights

The most penetrating observation from the reviews concerns the recursive nature of Proposition 5.2's second-order bound: the "tighter" bound depends on squared error terms from earlier steps, creating a circular dependency where the claimed improvement may not hold without establishing that the base error is below 1. This is a genuine theoretical subtlety the paper does not address and would merit investigation even in a revised version. The second novel insight is the referee's observation that Figure 2(b) not only fails to validate the Hessian-based claim but actively undermines it—a finding that reframes the paper's narrative from "validated theory" to "untested or contradicted comparative claims."

## Suggestions

1. **Resolve the Fig. 2(b) contradiction.** Either the figure is incorrect (correct it), or the theory predicts something different from what is measured (explain why—perhaps the bound is looser for Alg. 2 on this specific unlearning sequence, or the approximation error conflates factors). A paper whose central comparative claim is directly contradicted by its own data cannot stand without explanation.

2. **Run experiments under strongly convex losses** (e.g., ℓ₂-regularized logistic regression, or linear regression with MSE) so the theoretical assumptions are satisfied and the bounds can actually be tested. This is the most direct way to give experiments a genuine connection to the theory.

3. **Include Alg. 1 results in Table 1** so the combined post-unlearning excess risk can be compared between the two methods.

4. **Expand the experimental evaluation** to include at least one more dataset, error bars over multiple runs, and a simple baseline (e.g., comparison to retraining cost).

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>