## Summary

This paper establishes a theoretical framework connecting certified machine unlearning with ℓ₂-regularized continual learning. It proposes two algorithms—a gradient-based "natural forgetting" method (Alg. 1) and a Hessian-based correction method (Alg. 2)—and analyzes their post-unlearning excess risk via a decomposition into unlearning loss and continual learning excess risk. The key contribution is providing the first theoretical excess-risk bounds for this combined continual-learning-unlearning setting.

## Strengths

- **Clean problem decomposition.** The separation of post-unlearning excess risk into unlearning loss (6) and continual learning excess risk (7) is a conceptually useful framing that clarifies the inherent trade-off between preserving past knowledge and forgetting upon deletion requests. This decomposition is the paper's most original contribution and provides a clear lens for future work.

- **Extension of continual learning excess-risk bounds.** Theorem 3.1 extends the ℓ₂-regularized continual learning analysis of Lin et al. (2023) from linear models to general μ-strongly convex losses. If the proof is correct (the appendix is not available for verification), this is a nontrivial theoretical generalization.

- **Adaptation of certified unlearning to a realistic constraint.** The paper correctly identifies that existing certified unlearning methods assume full access to past training data, which is incompatible with continual learning's storage constraints. Adapting noise-based certified unlearning to this setting is a well-motivated problem.

## Weaknesses

### Fatal

- **The central comparative claim is contradicted by the paper's own experimental evidence.** The abstract states: *"Our analysis shows that our Hessian-based adaption algorithm largely outperforms the gradient-based algorithm"* (line 9). The contributions section says the Hessian-based method achieves *"lower unlearning loss than gradient-based methods"* (line 37). The conclusion repeats: *"the Hessian-based method achieves lower unlearning loss"* (line 318). However, Figure 2(b) and its accompanying description (lines 300–301) show the exact opposite: the natural forgetting (gradient-based) algorithm achieves an unlearning loss (approximation error) of approximately 0.08–0.10, while the Hessian-based algorithm achieves 0.20–0.24 across all λ values shown. The gradient-based method's unlearning loss is lower by a factor of 2–3× at every point. The paper provides no comparison between the two algorithms on the combined post-unlearning excess risk metric either (Table 1 only shows Hessian-based vs. retraining). This is not a minor framing issue—it is a direct contradiction between the paper's headline claim and the evidence presented to support it. A paper cannot claim Method A "largely outperforms" Method B on metric X while showing that B outperforms A on metric X.

### Major

- **The experiments do not validate the theory's core assumptions.** The entire theoretical analysis (Theorems 3.1, 4.1, Propositions 5.1, 5.2) rests on Assumption 2.1 requiring μ-strong convexity of the loss. The experiments use cross-entropy loss on a softmax linear model, which is *not* strongly convex. The paper states it *"relaxes"* this assumption (line 288), but provides no modified analysis, no argument about why the bounds still hold, and no quantification of how the lack of strong convexity affects the guarantees. Since the theory depends on ρ = λ/(μ+λ) and related quantities that require μ > 0, it is unclear whether any of the proven bounds apply to the experimental setting.

- **The claim of extending theory to "nonlinear convex models" has no empirical support.** The paper claims to extend results *"from linear to nonlinear convex models"* (abstract, line 35). But the experiments exclusively use a linear model (softmax regression). A theoretical extension without a single empirical demonstration on a nonlinear model is at best incomplete and weakens the evidence for the paper's broader contribution.

### Minor

- **No comparison against any practical baseline.** The only baseline is "perfect retraining." There is no comparison against fine-tuning on remaining tasks without an unlearning mechanism, existing heuristic continual unlearning methods (which the paper cites), or even a "do nothing" baseline showing what accuracy the model achieves if unlearning is ignored. Without these, the practical significance of the proposed methods cannot be assessed.

- **No statistical rigor.** All experimental results are reported as single numbers with no error bars, confidence intervals, or standard deviations over multiple trials. Given the variance inherent in random task splits, unlearning sequences, and noise sampling, any observed difference could be noise. This is particularly problematic for interpreting Table 1, where the "perfect retraining" baseline at λ = 30 is *below* the Hessian-based method (71.05% vs. 71.59%), which the paper labels a *"loose accuracy upper bound"* (line 296)—indicating the baseline itself may not be reliably constructed.

- **Apparent notational issue in Theorem 3.1 bound.** Equation (8) contains the term ρ^{τ_j - τ_j} ‖w*_{τ_j} − w*_{τ_j}‖, which evaluates to ρ^0 × 0 = 0 regardless of the data. The expression is likely intended to be ‖w*_{τ_i} − w*_{τ_j}‖ or similar, but as written in the main text it is degenerate. (The appendix, which is stripped, may contain the correct expression.)

### Trivial

- The Hessian-based method's O(td²) storage cost is acknowledged but the paper's own "forgetting enhanced" modification receives only a three-sentence sketch (lines 276–282) with no experimental validation.

## Nice-to-Haves

- A comparison of both algorithms on the combined post-unlearning excess risk metric (not just unlearning loss).
- Empirical verification of the unlearning guarantee (e.g., membership inference attacks or canary tests) to confirm that the noise injection actually removes data influence.
- Experiments on a nonlinear model (e.g., a small MLP) to support the claimed extension to nonlinear convex models.
- Directly varying the unlearning request sequence to demonstrate the claimed sensitivity of the Hessian-based method to request order.

## Removed Points

The following points from the input review were removed with justification:

- *"No unlearning certification is actually verified"* — removed per Hard Rule: the paper provides theoretical certification; empirical verification via MIAs is not standard for theoretical certified unlearning papers, and the paper does not claim to provide such verification.
- *"The formulation assumes the algorithm internally maintains a secret model"* — removed because the paper explicitly acknowledges this limitation (lines 169–170).
- *"Bounds depend on unknown quantities (‖w*_τ_i‖, etc.)"* — removed as a generic criticism that applies to most learning-theoretic bounds; not specific enough to constitute a weakness.
- *"Section 4: for ρ close to 1 bounds decay slowly"* — removed as a description of the bound's behavior, not a flaw.
- *"With the appendix stripped I cannot verify..."* — removed per Hard Rule; this is a reviewer process limitation, not a paper weakness.
- *"Missing related works"* — removed per Hard Rule.
- *"The claim of being the first theoretical investigation"* — removed as it is not a weakness.
- *"Second-order bound is circular"* — softened to Minor; the bound (15) depends on prior model differences, which is a recursive dependence but not strictly circular. The original framing was overwrought.

## Novel Insights

None beyond the paper's own contributions. The problem formulation (decomposing post-unlearning excess risk into unlearning loss + continual learning excess risk) is the most novel element, and this was already identified in the Strengths section. The reviewer's observation that Figure 2(b) directly contradicts the paper's central comparative claim is a factual finding, not a conceptual insight.

## Suggestions

1. **Resolve the central contradiction.** Either (a) correct the claim about Hessian-based outperformance to match the experimental evidence, or (b) show that the claim refers to post-unlearning *excess risk* (not unlearning loss) and provide experimental comparisons on that metric for both algorithms.

2. **Run controlled baselines.** At minimum, compare against simple fine-tuning on remaining tasks and a "no unlearning" baseline.

3. **Add error bars.** Report means and standard deviations over at least 5 random seeds, given the multiple sources of randomness.

4. **Acknowledge the gap between theory and experiments.** Either run experiments under μ-strongly convex losses (e.g., ℓ₂-regularized logistic regression on a binary task) to match Assumption 2.1, or provide an argument for why the bounds approximately apply to the non-strongly-convex setting used.

## Score and Decision

The paper tackles a genuinely important problem and its problem formulation is clean. However, the fatal contradiction between the central comparative claim and the experimental evidence (Figure 2(b) shows the gradient-based method achieving 2–3× lower unlearning loss while the text claims the opposite) cannot be ignored. Combined with the theory-experiment gap on strong convexity, the lack of meaningful baselines, and the absence of statistical rigor, the paper cannot be accepted in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>