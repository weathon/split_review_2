Now I have all the information needed to produce the final consolidated review.

---

## Summary

This paper establishes a theoretical framework for certified machine unlearning in continual learning settings, based on an ℓ₂-regularized continual learning algorithm. It adapts gradient-based and Hessian-based certified unlearning methods to this setting, providing theoretical bounds on post-unlearning excess risk decomposed into unlearning loss and continual learning excess risk. The Hessian-based method uses a three-term correction to handle interference among multiple unlearning requests, while the gradient-based method leverages natural forgetting with zero storage overhead.

## Strengths

- **Clean analytical decomposition of post-unlearning excess risk.** Equations (5)–(7) decompose the overall risk into unlearning loss + continual learning excess risk, cleanly surfacing the tradeoff that minimizing forgetting (for good continual learning) can make unlearning harder. This framing is well motivated and is the paper's central conceptual contribution.

- **The Hessian-based update rule (eq. 13) addresses a genuinely nontrivial technical challenge** — interference among unlearning requests where unlearning task A disrupts the correction previously applied for task B. The three-term correction in Algorithm 2 is a sensible and technically sound design. The analysis of how well-ordered vs. disordered unlearning sequences affect approximation error (Propositions 5.1, Lemma 5.4) is a meaningful theoretical insight.

- **The forgetting-enhanced Hessian method (Section 5.3)**, which combines Hessian-based unlearning for recent tasks with natural forgetting for older tasks to reduce storage to the maximum gap between consecutive unlearning times, is a practically motivated design choice that follows naturally from the theory.

- **Theorem 4.1's bound** showing that each unlearned task contributes error proportional to ρ^{t-s-n} reflects the intuitive idea that older, more-forgotten tasks are easier to unlearn, and the clean mathematical form supports the paper's conceptual framing.

## Weaknesses

### Fatal

None.

### Major

- **Theorem 3.1 (equation 8) contains subscript errors that render parts of the bound degenerate as printed.** Specifically: `ρ^{τ_j - τ_j}` = `ρ^0` = 1 (almost certainly intended to be `ρ^{τ_j - τ_i}`), and `‖w_{τ_j}^* - w_{τ_j}^*‖` = 0 (almost certainly intended to involve different indices). Similarly `‖w_{τ_i}^* - w_{τ_i}^*‖` later in the same line is identically zero. Since this is the main excess risk bound that underpins all downstream results, the error must be corrected.

- **The experiments violate the core theoretical assumption (Assumption 2.1).** The paper uses a linear model with softmax output and cross-entropy loss, which is not μ-strongly convex. The authors acknowledge this (line 288: "we relax its assumption of μ-strong convexity here"), but the consequence is that the experiments operate outside the regime covered by any of the paper's theorems. Since the theoretical bounds depend critically on strong convexity (μ → 0 gives ρ = 1, collapsing the forgetting-based decay in all bounds), the experiments cannot validate the theory's quantitative predictions.

- **The paper's central comparative claim about unlearning loss is contradicted by its own experimental results.** The contributions list (line 37) states the Hessian-based method "achieve[s] lower unlearning loss than gradient-based methods," and the abstract claims experiments "validate these theoretical findings." However, Figure 2(b) shows the opposite: the Hessian-based algorithm has 2–3× higher unlearning loss (≈0.20–0.24) compared to the natural forgetting algorithm (≈0.08–0.10) across all λ values. No accuracy comparison between the two methods' post-unlearning models is provided to substantiate the claim of superior overall performance.

- **No error bars, standard deviations, or confidence intervals are reported for any experimental result.** Every reported accuracy is a single point estimate. Given the small scale (30 tasks on MNIST) and the fact that different task splits and unlearning sequences would produce variance, the lack of statistical reporting makes it impossible to assess whether observed differences (e.g., the 71.59% vs 71.05% at λ=30) are meaningful or simply noise.

### Minor

- The hyperparameter values ε and δ used in the DP noise mechanism are not specified. Since the noise standard deviation depends critically on these values, the experimental setup cannot be reproduced from the paper as written.
- No comparison of test accuracy between the natural forgetting algorithm (Alg. 1) and Hessian-based algorithm (Alg. 2) for post-unlearning models is provided. Table 1 only reports Hessian-based vs. retraining, so the reader cannot evaluate the central comparative claim about which algorithm achieves better final accuracy.
- The experimental section is limited to one dataset (MNIST) and one model (linear with softmax), making it difficult to assess the generality of the findings.

### Trivial

None.

## Nice-to-Haves

- Include at least one experiment that satisfies the strong convexity assumption (e.g., ℓ₂-regularized logistic regression) to provide a genuine validation of the theoretical bounds.
- Clarify in the text when the "well-ordered" condition in Lemma 5.4 would realistically arise in practice.

## Removed Points

These points were raised in the input review but are removed or downgraded after verification against the paper:

1. **"Hessian-based unlearning beats perfect retraining — a theoretical impossibility"** → Removed. The 0.54% difference (71.59% vs 71.05%) is almost certainly noise from a single run; it is not a theoretical impossibility. The real concern (no error bars) is already captured as a Major weakness.
2. **"The bound in Proposition 5.1 is nearly unreadable"** → Removed. This is a subjective presentational judgment, not a substantive flaw.
3. **Claims about "no related work section" and missing appendix content** → Removed per hard rules; the parser strips appendices (they exist in the original submission).
4. **"The experiments contradict the paper's central claim that Hessian 'largely outperforms'"** → The paper's theoretical claim is about its analysis; the experiments use a non-strongly-convex setting where the theory does not directly apply. However, the claim that Hessian "achieves lower unlearning loss" (contributions, line 37) is factually contradicted by Figure 2(b), which is already captured as a Major weakness above.

## Novel Insights

None beyond the paper's own contributions. The observation that the empirical unlearning loss results invert the claimed ranking is accurate but is already captured in the weaknesses section above. No genuinely novel synthesis emerged that the paper does not already articulate.

## Suggestions

1. Fix the subscript errors in Theorem 3.1 (equation 8) so that the bound is interpretable from the main text. Cross-check all index variables.
2. Add error bars (multiple random seeds with different task splits and unlearning sequences) to all reported experimental values.
3. Include a direct accuracy comparison between the natural forgetting and Hessian-based algorithms on post-unlearning models to support the claimed ranking.
4. Report the specific ε and δ values used and any other unlisted hyperparameters.
5. Clarify in the text that the claimed advantage of the Hessian method refers to the theoretical bounds under strong convexity, and explain why the empirical unlearning loss pattern differs in the non-strongly-convex setting tested.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>