## Summary

This paper tackles the problem of certified machine unlearning within a continual learning framework where past data is inaccessible. It adapts gradient-based and Hessian-based certified unlearning methods to the continual learning setting, provides theoretical performance guarantees by decomposing post-unlearning excess risk into unlearning loss and continual-learning excess risk, and conducts experiments on MNIST.

## Strengths

- **Genuinely open problem, clean framing.** The paper identifies a well-motivated gap: certified unlearning under continual learning constraints where past datasets are unavailable. The decomposition of post-unlearning excess risk into an unlearning loss term plus a continual-learning excess risk term (equations 5–7) is a clear and useful conceptual contribution.

- **Nontrivial trade-off insight.** The observation that a continual learning algorithm that reduces forgetting (via larger λ) may simultaneously increase unlearning loss (Section 2.3) is specific to the continual-learning-unlearning setting and not present in prior certified unlearning work.

- **Zero-storage natural forgetting algorithm.** Algorithm 1, which injects noise calibrated by the forgetting effect inherent in ℓ₂-regularized continual learning, is elegantly simple and requires no additional storage — a genuine advantage.

## Weaknesses

### Fatal
None.

### Major

- **Central claim contradicted by own experimental evidence.** The conclusion (line 318) states "the Hessian-based method achieves lower unlearning loss," but Figure 2(b) shows the opposite: the Hessian-based algorithm has substantially higher approximation error (~0.20–0.24) compared to the natural forgetting algorithm (~0.08–0.10) across all λ values. Furthermore, Table 1 provides no accuracy comparison between the two algorithms for post-unlearning excess risk, so the broader claim that Hessian-based "largely outperforms" the gradient-based method is entirely unsupported by the experiments as presented.

- **Theory–experiment disconnect.** The theoretical guarantees (Assumption 2.1, Theorems 4.1, Corollary 5.3) require μ-strong convexity. The experiments use a linear model with softmax cross-entropy loss, which the paper acknowledges (line 288) is **not** strongly convex. Calling this a "relaxation" does not justify why the theoretical bounds should apply. The experiments therefore neither validate the theory nor are covered by it — they operate in a fundamentally different regime.

- **Suspicious perfect-retraining baseline.** At λ=30, the Hessian-based unlearning achieves 71.59% test accuracy while the "perfect retraining" baseline achieves 71.05% (Table 1). The paper itself states that the retrained model "serves as the loose accuracy upper bound" (line 296). The unlearned model should approximate the retrained model *plus* DP noise — systematically exceeding it suggests the baseline is incorrectly constructed or there is a setup issue.

- **Insufficient experimental validation.** The evaluation uses a single dataset (MNIST), a single model class (linear softmax), a single random seed (no error bars/standard deviations), and does not report the (ε, δ) values used for the DP noise mechanism. Without these, the certified unlearning claim cannot be assessed, and the empirical findings lack the statistical support needed to back the paper's central comparative claims.

### Minor

- **Theorem 3.1 bound contains self-difference terms.** Equation (8) includes terms such as ‖w\*_{τ_j} − w\*_{τ_j}‖ and ∑ ‖w\*_{τ_i} − w\*_{τ_i}‖, which evaluate to zero as written. This may be a PDF-parser subscript-garbling artifact, but it means the core theoretical bound cannot be independently verified from the main text alone.

### Trivial
None.

## Nice-to-Haves

- Run at least one experiment under the theory's own assumptions (strongly convex loss, e.g., ℓ₂-regularized logistic regression) to validate that the bounds are meaningful.
- Report the (ε, δ) values used for noise injection and add error bars via multiple random seeds.
- Compare both algorithms on post-unlearning excess risk (accuracy) side by side in Table 1.

## Removed Points

- Criticism about Table 2 being "not shown": This is a parser artifact — the appendix containing Table 2 was stripped by the extraction process, not omitted by the authors.
- Criticism about missing comparison to "Liu et al. 2022 or Cha et al. 2024": The paper explicitly positions itself as a theoretical foundation; the absence of heuristic baselines is not a fatal flaw for a primarily theoretical paper.
- "No demonstration that the certified unlearning guarantee actually holds" via indistinguishability measurement: This goes beyond standard practice for certified unlearning papers, which typically rely on the theoretical guarantee rather than empirical indistinguishability testing.
- Theorem notation issue: Kept as Minor weakness above (the reviewer's framing as a potentially fatal error was unwarranted given PDF-parser artifacts).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix the experimental setup so the perfect-retraining baseline is correctly constructed. Compare both algorithms on post-unlearning excess risk (accuracy).
2. Run at least one experiment that satisfies the theoretical assumptions (strongly convex loss) to validate the bounds.
3. Either correct or remove the claim that the Hessian-based method achieves lower unlearning loss, since it is contradicted by Figure 2(b). If the claim refers to post-unlearning excess risk, provide the evidence.
4. Add error bars, report (ε, δ) values, and include at least one more dataset to strengthen the evaluation.

## Score and Decision

The paper tackles a timely and genuinely important problem and offers a thoughtfully structured theoretical framework. However, the experimental section has fundamental problems: the central claim is contradicted by the paper's own Figure 2(b), the experiments operate in a regime where the theory's assumptions are violated, the perfect-retraining baseline produces suspicious results, and the evaluation is far too thin to support the conclusions drawn from it. These issues cannot be resolved with minor revisions — the experimental claims would need to be substantiated or the paper reframed as purely theoretical. In its current form, the paper cannot be accepted.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>