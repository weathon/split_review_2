## Summary
# Final Review Report

## Summary

This paper addresses the problem of evaluating heterogeneous treatment effect (HTE) estimators under relaxed assumptions on nuisance parameter estimation. Building on the relative error framework of Gao (2025), the authors propose a method that achieves $\sqrt{n}$-consistent and asymptotically normal estimation of the relative error between two HTE estimators even when the outcome regression models are misspecified, provided the propensity score is correctly specified at a rate faster than $n^{-1/4}$. The key technical contributions include: (i) deriving a set of moment conditions (Eq. 4) that enable robustness to outcome model misspecification, (ii) designing a weighted least-squares loss $\mathcal{L}_{\text{wls}}$ and balance regularizers $\mathcal{L}_{\text{const}}$ within a Dragonnet-style neural architecture, and (iii) extending the evaluation framework to a learning method for HTE estimation via pair-averaging. Empirical results on IHDP, Twins, and Jobs datasets show that the proposed method achieves targeted 90% confidence interval coverage for relative error and improves HTE estimation accuracy over 11 baseline methods. The paper addresses a practically important gap in the causal inference literature and provides a theoretically grounded approach to estimator evaluation. However, the manuscript contains several critical formula errors, notational inconsistencies, and missing implementation details that must be addressed before the contributions can be fully verified.

## Strengths
1. **Theoretically grounded relaxation of outcome model consistency**: The paper correctly identifies a practical limitation of Gao (2025)'s relative error framework—its reliance on consistent outcome regression models—and provides a principled theoretical derivation of weaker sufficient conditions. The key insight that the propensity score model alone can drive consistency of the relative error estimator, even under outcome model misspecification, is a meaningful contribution to the HTE evaluation literature.

2. **Novel loss design with balance regularization**: The weighted least-squares loss $\mathcal{L}_{\text{wls}}$ and the balance regularizer $\mathcal{L}_{\text{const}}$ represent an interesting integration of causal inference principles (covariate balancing, IPW weighting) into neural network training. The ablation study (Table 5) provides empirical evidence that both components contribute to the overall performance, with $\mathcal{L}_{\text{const}}$ being particularly important.

3. **Comprehensive empirical evaluation**: The paper evaluates both the relative error estimation quality (coverage, selection accuracy) and the downstream HTE estimation performance across three benchmark datasets with 11 baseline methods. The coverage rate analysis (Figures 1-2) and the comparison with conventional nuisance estimators (Table 2) convincingly demonstrate the practical benefits of the proposed approach.

4. **Extension to HTE estimation**: Leveraging the evaluation framework for direct HTE estimation via pair-averaging is a natural and useful extension. The empirical results in Table 1 show consistent improvements over strong baselines including Dragonnet, DCFR, and ESCFR across both IHDP and Twins datasets.

5. **Sample splitting not required**: The paper explicitly notes that their methodology does not require sample splitting, unlike Gao (2025). This is a practical advantage that simplifies the workflow and potentially improves statistical efficiency in small-sample settings.

## Weaknesses
### W1. Critical formula error in the absolute error estimator (Page 2, Section 3)

The paper's derivation of the absolute error estimator $\hat{\phi}(\hat{\tau})$ contains a self-cancelling expression that makes the formula identically zero. The term $\hat{\tau}(X_i) - \hat{\tau}(X_i)$ appears twice in the estimator, where the second occurrence should be a different quantity (likely a nuisance-based CATE estimate $\tilde{\tau}(X_i)$). This error is non-trivial because readers cannot verify the claimed semiparametric efficiency of the absolute error estimator, and it undermines confidence in the theoretical development throughout the paper. **Severity: Major. Fixability: Easy** — replace the inner $\hat{\tau}$ with a properly defined distinct quantity.

### W2. Notational collapse in the Taylor expansion (Page 4, Section 4.1)

The Taylor expansion that forms the theoretical backbone of the proposed method suffers from a serious notational inconsistency. Both terms in the expansion use the same symbol $\tilde{\gamma}$ (line 69), making the difference zero by construction. The intended expression should involve $\hat{\gamma}$ (or $\tilde{\gamma}$) versus $\bar{\gamma}$ (probability limit). This error propagates through the derivation of Eq. (3) and Eq. (4), making it impossible to verify the key theoretical conditions. Additionally, the notation $\tilde{\mu}_a$ and $\bar{\mu}_a$ are used without clear separation between estimators and their probability limits. **Severity: Major. Fixability: Moderate** — requires rewriting all three notational levels (true parameter, probability limit, sample estimate) consistently.

### W3. Missing theoretical justification for the loss functions (Page 5, Sections 4.2-4.3)

Several critical theoretical gaps affect the loss function design:

- **W3a**: The weighted least-squares loss $\mathcal{L}_{\text{wls}}$ multiplies the squared residuals by $(\hat{\tau}_1(X_i) - \hat{\tau}_2(X_i))$, which can be negative. A negative weight would make the loss non-convex and potentially unbounded below, yet the paper provides no discussion of this issue or how optimization handles it.
- **W3b**: The balance regularizer $\mathcal{L}_{\text{const}}$ uses non-standard notation "$\max\{\cdot \mid -\xi, 0\}$" that is not defined. The variable $\hat{r}_1, \hat{r}_2$ (lines 88-89) are used instead of $\hat{\tau}_1, \hat{\tau}_2$ without definition, creating inconsistency with Eq. (4).
- **W3c**: Theorem 1 requires convergence faster than $n^{-1/4}$ to probability limits, but the working models are linear in a learned representation $\Phi(X)$. The paper does not specify conditions on $\Phi$ (e.g., bounded eigenvalues, sparsity) that ensure this rate when $\Phi$ is high-dimensional.

**Severity: Major. Fixability: Moderate** — requires explicit discussion of the weight sign issue, correction of notation, and statement of regularity conditions.

### W4. Unclear training protocol for the aggregated HTE estimator (Page 7, Section 5)

The enhanced HTE estimator averages over all $K(K-1)/2$ pairs of candidate estimators. However, the paper does not specify whether each pair requires a separate neural network or whether parameters are shared. Training $O(K^2)$ networks would be computationally prohibitive for moderate $K$, while parameter sharing would require careful architectural design. The running time analysis (Table 3) shows super-linear scaling ($K=5$ requires 12.2 seconds), but no guidance is given on how many pairs are needed for stable performance. **Severity: Major. Fixability: Moderate** — requires clarifying the training protocol and providing scaling recommendations.

### W5. Comparison with Gao's method confounds architecture and loss effects (Page 8, Section 6.2)

The paper compares the proposed method against standard nuisance estimators (Linear Regression, Boosting) as "Gao's method." This conflates two differences: (a) the neural architecture vs. simple models, and (b) the proposed losses vs. standard losses. The ablation study (Table 5) partially addresses this, but the comparison would be more informative if it controlled for architecture (e.g., Dragonnet + standard losses vs. Dragonnet + proposed losses). **Severity: Moderate. Fixability: Easy** — add a controlled architecture comparison.

### W6. Experimental validation limitations (Page 7-8, Section 6)

- **W6a**: IHDP has severe treatment imbalance (139 treated vs. 608 control) that could affect IPW-based estimates, but this is not discussed.
- **W6b**: No statistical significance tests are provided for the main HTE comparison (Table 1). Given that some improvements are modest (e.g., Twins: 0.284 vs. 0.290), significance testing is essential.
- **W6c**: The sensitivity analysis for propensity score misspecification (Table 6) fixes the t-head while retraining the rest, which means the representation learning layers are no longer optimized jointly, confounding the interpretation.

**Severity: Moderate. Fixability: Moderate** — add imbalance discussion, significance tests, and cleaner sensitivity analysis.

### W7. Conclusion introduces untested future directions (Page 9, Section 7)

The conclusion mentions ITE estimation and joint distribution of potential outcomes as desirable future work without any prior analysis or evidence in the paper. Adding unsupported claims in the conclusion weakens the paper's focus and could confuse readers about what has been achieved. **Severity: Minor. Fixability: Easy** — remove or bound the ITE discussion to a single sentence referencing the existing limitations section.

### W8. Contribution claims too vague (Page 1, Introduction)

The three contribution bullets (lines 17-19) are generic and do not specify the precise technical advance, the verified properties, or the boundary conditions. Readers cannot distinguish the contribution from Gao (2025) based on these bullets alone. **Severity: Minor. Fixability: Easy** — rewrite with specific technical achievements as suggested in the annotation.

### W9. Table 1 column formatting (Page 7-8)

Table 1 appears to have duplicated column headers and misaligned data columns, making it difficult to interpret which columns correspond to which dataset and metric. Ten data columns are shown where eight are expected. **Severity: Minor. Fixability: Easy** — correct the LaTeX table specification.

### Novelty Assessment (Deferred)

Due to Retrieval-Disabled Mode (external paper search unavailable for this run), a full literature-based novelty assessment cannot be completed. The paper builds on Gao (2025) and the Dragonnet framework (Shi et al., 2019a), with the main claimed novelty being the relaxation of outcome model consistency requirements. Based on internal evidence, the contribution appears to be an incremental but non-trivial extension of the relative error framework. A definitive novelty verdict requires manual literature verification against concurrent work on doubly robust evaluation and balance-based regularization in causal inference.

## Score
**Final Score: 6/10**

**Scoring rationale**: The score prioritizes research value and novelty as primary dimensions, consistent with the required policy.

- **Research value (7/10)**: The paper addresses a genuine practical problem—evaluating HTE estimators when outcome regression models may be unreliable—and provides a principled framework with theoretical guarantees. The extension to HTE learning is a useful byproduct. However, the value is somewhat limited by the strong reliance on correct propensity score specification, which may be violated in practice.

- **Novelty (5/10)**: The core idea (relaxing outcome model consistency via moment conditions derived from loss design) is a meaningful but incremental extension of Gao (2025). The loss function design and balance regularization add novelty, but the overall framework follows established patterns in doubly robust causal inference and balance-based learning. A definitive novelty verdict requires external literature verification (deferred in this run).

- **Validity/Soundness (5/10)**: The paper's theoretical development has critical notational errors (W1, W2) and missing regularity conditions (W3c) that prevent verification of the core claims. The experimental design has several shortcomings (W4, W6). These issues are fixable with moderate revision effort.

- **Reproducibility (4/10)**: The loss functions contain undefined notation (W3b), the training protocol is incompletely specified (W4), and the neural network implementation details are mostly relegated to the appendix (which is not available in the submitted text). A reader cannot confidently reproduce the method from the main paper alone.

**Score summary**: The paper has a solid technical core and addresses an important problem, but is held back by (a) critical formula errors that undermine theoretical verification, (b) missing implementation details that prevent reproducibility, and (c) experimental limitations that weaken the empirical claims. The weaknesses are fixable and the paper has clear potential for acceptance after major revision.

**Post-Revision Target**: [7, 8]/10 — achievable if the formula errors are corrected, notation is clarified, training protocol is specified, and additional robustness experiments (significance tests, cleaner ablation) are added.