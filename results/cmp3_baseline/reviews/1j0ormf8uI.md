## Summary
This paper introduces a conformal prediction procedure for constructing lower prediction bounds (LPB) for counterfactual survival times under different treatments with general right-censored data. By reformulating the problem as a covariate shift through a reweighting scheme and applying weighted conformal prediction, the method achieves exact marginal coverage guarantees (up to weight estimation error) and doubly robustness. Experiments on synthetic and real lung cancer data demonstrate validity and informativeness over PAC-type baselines.

## Strengths
- **Novel combination of weighted conformal prediction and survival counterfactuals**: The paper is the first to achieve exact marginal coverage for counterfactual LPB under general right-censored data, whereas prior works either handled Type-I censoring only or provided PAC-type guarantees.
- **Clean theoretical analysis**: Theorems 4.1 and 4.2 provide a coverage guarantee that quantifies the effect of weight estimation error and a doubly robustness property, respectively. The results are distribution-free and maintain the non-parametric spirit of conformal prediction.
- **Strong empirical validation**: On synthetic data across six settings with varying treatment/censoring rates, the method attains near-nominal coverage while producing less conservative LPB than focused/fused baselines. The real-data application on non-small cell lung cancer patients shows that the LPB aligns with known clinical factors (stage, KPS, radiomic features) and differentiates treatment regimens (e.g., VMAT vs IMRT) in expected ways.

## Weaknesses
### Fatal
None.

### Major
- **Derivation of the key weighting transformation is not fully self-contained**: Equation (1) relies on an inequality step (iii) that references Lemma A.1 in the appendix. The main text does not provide enough reasoning to verify the direction and tightness of the inequality, which is central to the method’s validity. While the appendix likely fills this gap, the presentation in the main text should be clearer.
- **Unclear adaptation of baselines to the counterfactual setting**: The paper compares against methods from Davidov et al. (2025) that were originally designed for survival analysis without counterfactual outcomes. It is not explicitly described how these baselines are extended to the counterfactual scenario, raising concerns about the fairness and reproducibility of the comparison.
- **Guarantee is not exact in finite samples**: Theorem 4.1 includes an additive error from weight estimation, so the coverage is only approximately exact when weights are imperfect. The abstract and introduction emphasize “exact” marginally valid LPB, which could mislead readers without careful qualification.

### Minor
- **Calibration set size can be very small**: The weighted conformal step uses only uncensored observations with the given treatment. Under high censoring rates or imbalanced treatments, the effective calibration size may be too small to reliably estimate the weighted quantile. The paper does not discuss this limitation or provide guidance on minimum sample sizes.
- **Some notation inconsistencies**: In equation (1), both \(\bar{q}_\alpha\) and \(\hat{q}_\tau\) appear without clear distinction. The variable \(\alpha\) is overloaded (coverage level and other uses).

### Trivial
None.

## Nice-to-Haves
- A sensitivity analysis for the weight estimation quality (e.g., misspecification of the classifier for \(\gamma(x)\)).
- A discussion of how to select the \(\tau\) optimization strategy (global vs per-test point) and its computational cost.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Expand the derivation in Section 4.1 to include an intuitive explanation of each step in equation (1) and the role of Lemma A.1, so that the main text is more self-contained.
- Clearly state how each baseline (focus, fused, naive, uncal) is adapted to the counterfactual prediction task, and ensure that the implementation details are identical across methods (e.g., same quantile regression estimator, same weight estimation).
- Add a discussion on practical scenarios where the calibration set becomes too small and propose fallback strategies (e.g., pooling over treatments or imputing censored outcomes).

## Score and Decision
Score: 6  
Decision: Accept

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>