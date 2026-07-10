Now let me compose the final review.

## Summary

This paper proposes Aligned Scoring Rules (ASR), which optimizes proper scoring rules for textual information elicitation to align with human preferences (e.g., instructor scores) while maintaining provable truthfulness. The key technical contribution is a convex optimization formulation (Program 2) that minimizes MSE between a separate scoring rule and a reference score subject to properness constraints. The method builds on the ElicitationGPT framework of Wu & Hartline (2024) and is evaluated on peer grading datasets.

## Strengths

- **Well-motivated problem.** The paper correctly identifies a genuine gap: proper scoring rules for text (Wu & Hartline, 2024) guarantee truthfulness, but nothing in the framework ensures the scores align with human judgments. Fixing this without breaking properness is a real and interesting technical challenge.

- **Clean theoretical formulation.** Program 2 — minimizing MSE between a separate scoring rule and a reference score subject to properness constraints — is convex (Corollary 3.4), with only 6 variables per dimension and linear constraints. The paper correctly identifies that this particular hypothesis space (separate scoring rules) preserves convexity, whereas alternatives (max-over-separate) would not. This is a genuine technical contribution.

- **Large quantitative margins over baselines (if evaluation is sound).** In Table 1, ASR achieves Pearson correlation of 0.717 and Spearman of 0.622 against instructor scores, versus 0.294/0.301 for EGPT(AV) and 0.213/0.207 for EGPT(MV). These margins are substantial — provided the evaluation is reliable.

## Weaknesses

### Fatal
None.

### Major

- **No train/test split or cross-validation in the experimental evaluation.** The paper never states whether the results in Table 1 are computed on training data, held-out data, or any cross-validation scheme. The constant baseline is defined using "training data D" (line 358) and the optimization uses gradient descent "over samples" (line 256), but there is no description of any evaluation on held-out data. ASR is explicitly optimized to minimize MSE against reference scores — comparing an optimized model to fixed, non-optimized baselines without any separation between training and evaluation means the quantitative results cannot be interpreted as evidence of generalization. With ~516 reviews across 22 assignments, overfitting is a genuine risk that the paper does not discuss or address.

- **Scale mismatch makes MSE comparisons against EGPT baselines uninterpretable.** The V-shaped scoring rule (EGPT) outputs scores bounded in [0, 1/2] (Definition 2.4) while reference scores are on [0, 10]. The paper states that the reference score is "normalized to [0, 1]" (line 227) for the optimization formulation, but the reported Constant MSE of 3.741 is mathematically impossible if both predictions and targets are in [0, 1] (maximum possible MSE is 1), indicating the evaluation uses the original [0, 10] scale without stating this clearly. Direct MSE comparison between methods operating on fundamentally different output scales conflates alignment quality with scale differences. Pearson and Spearman correlations are scale-invariant and avoid this issue, but the MSE column in Table 1 is not reliably interpretable across methods, and the paper's claim of outperformance "on all metrics" is only partially supported.

### Minor

- **Error bars and variance measures are absent.** All metrics in Table 1 are point estimates. With only 22 assignments (~516 reviews), reporting variance across assignments or bootstrap resamples would let readers assess whether the reported differences are meaningful or driven by a few favorable assignments.

- **The "nearly-identity" linear fit claim (Section 5.3) lacks quantitative support.** The paper states the regression parameters "align closely with s = S" but provides no slope, intercept, or R² values. This claim is presented as a key result but cannot be verified from the paper as written.

- **Quality of the language oracles is not empirically evaluated.** The properness guarantees (Theorems 3.2–3.3) rely on the QA oracle being non-inverting (Definition 3.1), but no accuracy or error-rate measurements for the LLM-based summarization or QA pipelines are reported. This makes it difficult to assess how close the deployed system comes to the theoretical guarantees.

- **The paper does not quantify what alignment is lost by enforcing properness.** A natural comparison would be against an unconstrained predictor (e.g., linear regression on the same features) to measure the cost of truthfulness — a quantity that would be genuinely informative for mechanism designers considering this approach.

### Trivial

- The paper claims interpretability via learned scoring rule weights but only references an appendix case study. Some discussion of learned weights in the main text would substantiate this claim.

## Nice-to-Haves
- Regularization (e.g., toward the V-shaped rule as a prior) would be a natural addition to address overfitting concerns.
- A discussion of how many parameters (what is m, the number of summary dimensions?) were actually optimized would help readers assess model complexity.

## Removed Points

These points are flagged to be removed, treat them with caution:

- *"The related work connections to differentiable economics feel slightly aspirational"* — subjective opinion, not a concrete weakness.
- *"The Know-it-or-not assumption substantially narrows applicability"* — the assumption is clearly stated and motivated by observed data patterns; this is an appropriate scoping choice for the application domain, not a flaw.
- *"The dataset is small and not publicly benchmarked"* — concerns about cited data availability are removed per hard rules.
- *Various presentation/style nitpicks* — removed per the formatting-artifact rule (parser artifacts).
- *Criticisms about missing appendix content* — the appendix was stripped by the parser, not omitted by the authors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add proper cross-validation.** Leave-one-assignment-out (22 folds) is a natural choice for this dataset. Report mean and standard error of MSE/Pearson/Spearman across folds. This directly addresses the most serious weakness.

2. **Clarify the evaluation scale.** State explicitly whether MSE is computed on normalized [0,1] scores or original [0,10] scores. To enable fair cross-method MSE comparison, rescale all methods' outputs to a common range before computing MSE.

3. **Quantify the "nearly-identity" claim.** Report the slope, intercept, and R² for the linear regression in Figure 4.

4. **Add an unconstrained baseline.** Compare ASR to an unconstrained regression model predicting reference scores from the same features to quantify the cost of enforcing properness.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>