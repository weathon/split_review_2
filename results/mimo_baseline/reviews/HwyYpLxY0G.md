## Summary

This paper proposes Aligned Scoring Rules (ASR) for textual information elicitation, optimizing over the space of separate (single-dimensional) proper scoring rules to minimize mean squared error between the proper scoring rule and a reference score (e.g., instructor score or LLM-Judge score). Building on Wu & Hartline (2024)'s reduction from textual to numerical elicitation via LLM oracles, the paper formulates the alignment problem as a convex optimization that preserves properness while achieving significantly better alignment with human preferences than prior methods on peer grading datasets.

## Strengths

- **Well-motivated problem with clear gap**: The paper identifies a genuine limitation in prior work—Wu & Hartline (2024) achieves properness but not alignment with preferences—and provides a principled optimization framework to address it. The framing of converting non-proper reference scores into proper ones is compelling.

- **Elegant convex optimization**: By restricting to separate scoring rules with know-it-or-not reports, each dimension has only 6 variables with linear constraints, yielding a convex program (Corollary 3.4) that is computationally tractable. This is a clean and interpretable design choice.

- **Substantial empirical improvements**: ASR dramatically outperforms baselines. For instructor score alignment, ASR achieves MSE of 1.73 vs. 3.74 (best constant) and 9.54/18.36 (EGPT variants), with Pearson correlation of 0.717 vs. 0.294/0.213. The near-identity linear fit (Figure 4) demonstrates effective alignment.

- **Interpretability**: The separate scoring rule structure allows identification of important rubric points through the learned convexity of each single-dimensional scoring function, which is valuable for understanding what the mechanism rewards.

- **Maintains properness guarantees**: The method inherits all provable properness and adversarial robustness properties from the Wu & Hartline (2024) reduction while adding alignment.

## Weaknesses

### Fatal

None.

### Major

- **Evaluation methodology unclear**: The paper does not describe a train/test split or cross-validation procedure. With only 22 assignments (516 total reviews), if the ASR is evaluated on the same data used for optimization, the near-identity regression and strong MSE improvements could be substantially due to overfitting. This is critical because the optimization directly targets MSE on the training distribution. Without held-out evaluation, the reported numbers may not generalize.

- **Limited scale and generalizability**: The entire evaluation rests on 516 reviews from two undergraduate algorithm classes. The know-it-or-not assumption (Assumption 2.2) is motivated specifically by this peer grading setting and may not hold in other textual elicitation domains. It is unclear how the method performs on richer textual settings where agents express graded uncertainty.

- **Missing weight optimization in separate aggregation**: Program 2 sums S_i uniformly without weights, yet Definition 2.7 allows weighted averaging. Different summary points may carry different importance for alignment. The paper does not discuss whether optimizing weights w_i alongside the scoring rules could improve performance, nor does it justify the uniform weighting choice.

### Minor

- **No upper-bound comparison**: The paper does not compare against a non-proper scoring function (e.g., a direct regression on features) to quantify the cost of maintaining properness. Understanding this trade-off would strengthen the paper's positioning.

- **LLM-Judge as reference**: The Pearson correlation between instructor score and LLM-Judge score is 0.554 (moderate). Aligning to this somewhat noisy signal means the ASR is optimizing toward an imperfect proxy. The paper could discuss how noise in the reference affects the quality of the learned proper scoring rule.

- **Specificity of LLM oracles**: The entire framework depends on the quality of summarization and question-answering oracles. While properness is maintained even with imperfect oracles, alignment quality depends on accurate state identification. The paper does not ablate the oracle quality.

### Trivial

None.

## Nice-to-Haves

- A clear description of train/test methodology (e.g., leave-one-assignment-out cross-validation) with corresponding standard errors.
- Comparison with weighted separate scoring rules or max-over-separate scoring rules as additional baselines.
- An ablation on the number of summary points m and its effect on alignment quality.

## Novel Insights

The paper's core novel insight is that optimizing over the space of proper scoring rules via convex programming can simultaneously maintain truthfulness and align with exogenous human preferences. This bridges the gap between mechanism design (properness) and machine learning (alignment to preferences), demonstrating that the properness constraint does not preclude effective alignment—the optimal proper scoring rule achieves near-identity fitting to reference scores. The convexity of the separate scoring rule space is key to making this tractable.

## Suggestions

- Clearly describe the train/test evaluation protocol with cross-validation across assignments, reporting mean and standard deviation of metrics.
- Consider optimizing weights w_i in the separate aggregation to capture differential importance of rubric points.
- Add a non-proper upper-bound baseline to quantify the properness cost.

## Score and Decision

The paper presents a clean and well-motivated optimization framework for aligning proper scoring rules with human preferences. The convex formulation is elegant and the empirical results are strong in magnitude. However, the lack of described train/test methodology combined with a small dataset (516 reviews) raises serious questions about whether the reported improvements generalize. Without clarity on evaluation protocol, the near-perfect alignment shown in Figure 4 is as likely to reflect overfitting as genuine alignment quality. The contribution is incremental over Wu & Hartline (2024), and the strong know-it-or-not assumption limits applicability. The paper is borderline, with the evaluation concerns tipping the balance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>