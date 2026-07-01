## Summary

This paper proposes a novel cross-validation method for graphon models called "graphon cross-validation with random imputation" (CV-imputation). The key idea is to randomly mask edges in each fold, impute them with Bernoulli noise, estimate the graphon on the modified training data, then predict the held-out edges after an affine transformation correction, yielding a computationally efficient and theoretically consistent model selection score. The method is evaluated on synthetic data with four graphon estimation methods (NS, USVT, SAS, ICE) and on several real-world networks, consistently outperforming the existing edge cross-validation (ECV) method in accuracy and speed.

## Strengths

- **Novel and practical solution to an important problem**: Tuning parameter selection in graphon estimation is crucial yet challenging due to the dependence structure of network data. The proposed imputation-based CV is simple, computationally cheap (avoiding O(n³) matrix completion), and broadly applicable across different graphon estimators.
- **Solid theoretical support**: Theorem 1 establishes that the CV-imputation score is asymptotically parallel to the true MSE up to a constant, guaranteeing that the minimizer of the score converges to the optimal model. The theoretical framework (Condition 1 on optimism bias) is well motivated and the result is clearly stated.
- **Extensive and convincing empirical evaluation**: Experiments cover four distinct graphon models (varying density and matrix rank), four state-of-the-art estimators, and multiple real networks (drug-disease, political blogs, coauthorship, PPI). CV-imputation consistently yields lower MSE or comparable AUC while being orders of magnitude faster than ECV (e.g., 51 seconds vs 771 seconds on NetSci, 241 vs 6021 on Yeast).
- **Model-agnostic design**: The method works with any graphon estimation approach (NS, SAS, USVT, ICE) without requiring specific structural assumptions, enhancing its practical utility.

## Weaknesses

### Fatal

None.

### Major

1. **Imputation parameter θ is not adequately addressed**: The Bernoulli imputation uses a fixed θ, which is a tuning parameter itself. The paper only mentions its selection is discussed in Section S.4 (appendix omitted), leaving the main text without guidance on how to choose θ or whether results are sensitive to it. This is a critical practical detail that could affect the method's reproducibility and performance.
2. **Condition 1 may be hard to verify in practice**: The asymptotic theory depends on an "optimism bias" condition requiring \(Q_K(M) = O_p(K^{-\alpha})\). While the paper claims it can be verified computationally, no concrete verification procedure is provided, and the given example (Erdős–Rényi with simple averaging) is too narrow. For complex graphons and estimators, the rate α might degrade or be nonzero, potentially weakening the theoretical guarantee.
3. **Mixed results on synthetic data**: For Graphon 3 with NS, the default selection (\(M=1\)) achieves a lower MSE (0.74) than CV-imputation (0.79) and ECV (3.07). The paper's headline claim that CV-imputation "consistently selects models with smaller MSE values compared to those chosen by ECV" is accurate, but comparing to defaults is less favorable. Additionally, ECV for Graphon 1/NS shows an anomalously large standard deviation (19.25), suggesting instability that is not discussed.
4. **Real-data evaluation limited to a single comparison point**: In the COVID-19 drug-disease network, only the CV-imputation–selected M=1.2 and ECV-selected M=0.4 are compared on the held-out test set. A more thorough evaluation would include the default M or other M values to confirm that CV-imputation truly finds the optimal parameter. The anecdotal ledipasvir discovery, while interesting, does not constitute a rigorous validation.

### Minor

- The paper states that NS and ICE are excluded for large networks due to computational cost, but the comparison at small n includes them. This is reasonable but limits the scope of scalability claims.
- Figure 5 shows accuracy for method selection reaching nearly 100% at n=200; while not impossible, this seems unusually high and may reflect the specific experimental setup (e.g., large gaps between estimator performances). A brief discussion of variability would be helpful.
- The bibliographic entry for Erdos and Renyi (1959) is incomplete.

### Trivial

- Some figure captions are repeated (e.g., Figure 1, Figure 2, Figure 3, Figure 4, Figure 5 each have two captions). This is likely a parsing artifact but should be cleaned.

## Nice-to-Haves

- A sensitivity analysis over θ and a practical recommendation for its value (e.g., the average edge density) would significantly strengthen the paper's applicability.
- Additional theoretical analysis linking Condition 1 to specific graphon classes (e.g., Hölder smoothness, block models) would make the asymptotic results more concrete.
- Including a baseline like "oracle" tuning (selecting M from the true MSE on the full data) would clarify how far from optimal CV-imputation typically operates.

## Novel Insights

The paper's central insight—that imputing missing edges with Bernoulli noise and then correcting via an affine transformation yields a valid and cheap CV procedure—is both elegant and practically valuable. It sidesteps the structural distortion caused by edge deletion while avoiding the heavy computational burden of matrix completion required by prior work. The theoretical demonstration that the CV score tracks the MSE up to a constant (independent of the model) is a clean result that justifies the approach.

## Suggestions

- Provide guidance on selecting the imputation parameter θ (e.g., use the network's average edge density or a small grid search over a few values) and show that results are robust to this choice in an ablation study.
- Clarify the high variance of ECV for Graphon 1/NS (Table 1) and whether CV-imputation also exhibits similar instability in that regime.
- In the real-data case study, include the default parameter or multiple parameter values to more convincingly show that CV-imputation finds the best model.

## Score and Decision

**Score:** 8

**Decision:** Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>