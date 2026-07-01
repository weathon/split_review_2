## Summary

This paper proposes a cross-validation method for graphon model selection called CV-imputation. The key idea is to randomly partition node pairs into folds, replace held-out edges with Bernoulli draws of a fixed mean \(\theta\), then train the graphon estimator on the imputed adjacency matrix and transform the estimate back to the original probability scale. The method avoids expensive matrix completion (needed by the existing ECV method) and is applied to tune hyperparameters of four popular graphon estimators. The authors provide an asymptotic theory showing that the CV score is parallel to the true squared-error loss, and demonstrate through synthetic and real-network experiments that CV-imputation selects better models and is substantially faster than the competing ECV method.

## Strengths

*   **Practical and efficient procedure:** The method is simple to implement, model-agnostic, and replaces a costly singular-value decomposition step with cheap random imputation. Experiments show consistent computational gains over ECV across multiple estimators and network sizes.
*   **Strong empirical validation:** The synthetic experiments cover four graphon structures (dense/sparse, low/high rank) and four estimation methods (NS, USVT, SAS, ICE). CV-imputation consistently yields lower estimation MSE than both ECV and default parameter choices. Real-data link-prediction tasks further confirm improved accuracy and speed.
*   **Theoretical grounding:** The authors prove (Theorem 1) that under a regularity condition on the optimism bias, the CV-imputation score is asymptotically parallel to the true loss function, so its minimizer converges to the optimal model. This provides formal justification beyond heuristic intuition.
*   **Agnostic to the estimator:** The method treats the graphon estimator as a black box, making it broadly applicable to any estimation approach that produces a probability matrix, not just the four considered.

## Weaknesses

### Fatal
None.

### Major

1. **Condition 1 is not well justified.** The core theoretical result relies on a polynomial bound on the maximum \(K\)-fold optimism bias \(Q_K(M) = O_p(K^{-\alpha})\). The only explicit example given is the trivial Erdős–Rényi model with a simple averaging estimator. For the complex estimators used in practice (NS, SAS, USVT, ICE), it is unclear whether such a condition holds with any \(\alpha>0\), and the paper offers no analysis or supporting references. The claim that the condition is “verifiable computationally” does not substitute for a theoretical justification.

2. **Asymptotic theory requires \(K\to\infty\), but experiments use fixed \(K\) (e.g., 5).** Theorem 1 mixes limits in both \(n\) and \(K\), yet all experiments fix \(K\) (presumably 5, as mentioned in the supplementary). The paper does not explain why the asymptotic result should meaningfully apply to a fixed, small number of folds, nor does it investigate the sensitivity of the method to the choice of \(K\).

3. **The imputation parameter \(\theta\) is a free tuning parameter.** The method introduces \(\theta\) (the mean of the imputed Bernoulli variables), which must be chosen by the user. The main text relegates all discussion of \(\theta\) selection to the supplementary material and does not study the sensitivity of the CV score to misspecification of \(\theta\) in the core experiments. Without a principled or data-driven way to choose \(\theta\), the method’s practical reliability is unclear.

4. **Limited baselines and comparisons.** The only cross-validation competitor is ECV (Li et al., 2020). Other plausible approaches for network hyperparameter tuning—such as node‑based splitting with bias correction, block cross‑validation, or information criteria—are neither discussed nor compared. This narrow comparison makes it hard to gauge the overall merit of CV‑imputation within the broader toolkit.

### Minor

*   The caption of Figure 3 contains a typo: it states “ECV is faster than CV-imputation” while the text and data clearly show the opposite.
*   The text occasionally overstates theoretical soundness given the reliance on an unverified Condition 1.

### Trivial

*   Minor grammatical informality (e.g., “innovatively splits data”).

## Nice-to-Haves

*   An ablation study varying \(K\) (e.g., \(K=3,5,10,20\)) would strengthen the practical recommendations.
*   A discussion or small experiment on the robustness of CV-imputation to different choices of \(\theta\) (e.g., \(\theta = 0.25, 0.5, 0.75\)) would greatly increase confidence in the method.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

1.  Provide a more thorough, albeit informal, discussion of when Condition 1 might be expected to hold for common graphon estimators (e.g., for bandwidth‑type parameters, the optimism bias might decay as the training fold approaches the full data). Empirical verification across several synthetic scenarios would also help.
2.  Add experiments with a small and moderate number of folds (e.g., \(K=5,10,20\)) to illustrate how the CV score behaves as \(K\) changes and to connect the theory to practice.
3.  Report the sensitivity of the results to the imputation mean \(\theta\) in the main paper, or propose a data-driven rule (e.g., setting \(\theta\) to the global edge density).
4.  Expand the baseline set to include at least one alternative CV strategy (e.g., a node‑based split with simple mean imputation or the method of Chen & Lei, 2018 for stochastic block models) to better contextualize the gains.

## Score and Decision

**Score:** 5.0  
**Decision:** Borderline Accept

The paper addresses a relevant and practical problem, proposes a clean and computationally attractive method, and provides extensive experiments that support its effectiveness. However, the theoretical contribution is weakened by an unverified key condition, and the limited baselines and lack of sensitivity analysis for the imputation parameter leave significant open questions. With reasonable revisions, especially clarifying the condition and adding robustness checks, this work would be a solid contribution.

MY FINAL SCORE: <score>5.0</score>  
MY FINAL DECISION: <decision>Reject</decision>