## Summary

This paper proposes a conformal prediction method for constructing lower prediction bounds (LPBs) for counterfactual survival times under different treatments in general right-censored data. The key innovation is a reweighting calibration procedure that transforms the problem into weighted conformal inference, achieving exact marginal coverage guarantees (rather than PAC-type guarantees from prior work). The method is theoretically supported by distribution-free coverage guarantees and a doubly robustness property, and is validated on synthetic and real clinical lung cancer datasets.

## Strengths

- **Addresses an important and timely problem**: Providing reliable uncertainty quantification for counterfactual survival predictions under general right-censoring is crucial for clinical decision-making, and the paper tackles a clear gap—prior methods only offered PAC-type guarantees or were limited to Type-I censoring.
- **Technically sound and novel approach**: The reweighting scheme that converts the counterfactual coverage problem into a weighted conformal prediction problem is clever and well-motivated. The theoretical analysis (Theorem 4.1) provides a distribution-free exact coverage guarantee with a bound on the error from weight estimation, and Theorem 4.2 establishes doubly robustness.
- **Comprehensive empirical evaluation**: Experiments cover six synthetic settings with varying censoring/treatment rates, robustness to outliers, multi-treatment scenarios, and a real clinical dataset with four radiochemotherapy regimens. The method consistently achieves coverage close to nominal while producing competitive LPBs.
- **Clear exposition and practical relevance**: The method is clearly described (Algorithm 1), the connection to weighted conformal prediction is well explained, and the real-data analysis demonstrates clinically meaningful patterns (e.g., VMAT vs IMRT, stage-dependent LPBs).

## Weaknesses

### Fatal
None.

### Major
- **Theoretical guarantee is asymptotic for doubly robustness**: Theorem 4.2 provides an asymptotic guarantee, which is weaker than the finite-sample guarantee in Theorem 4.1. The conditions for doubly robustness (A1 or A2) involve limits and assumptions (e.g., bounded density, convergence of weighted errors) that may be difficult to verify in practice. The paper does not empirically demonstrate the doubly robust property.
- **Sensitivity to weight estimation is under-explored**: The method requires estimating ω(x) = 1/γ(x) where γ(x) = P(W=w, e=1|X=x). While Theorem 4.1 quantifies the effect of weight estimation error via an L1 bound, the experiments only use random forest for weight estimation. There is no systematic study of how different weight estimators or misspecification levels affect coverage in finite samples.

### Minor
- **The claim of being "first" to achieve exact coverage for general right-censored data** is plausible but slightly strong. The paper should more carefully acknowledge that the exact guarantee relies on the strong ignorability assumption and the reweighting scheme, which is a non-trivial extension but builds directly on Lei & Candès (2021).
- **Coverage is slightly below nominal in Setting 6** (Figure 1). The paper notes this but attributes it to "remarkably close." While not a fatal flaw, it suggests the method may be sensitive to certain data configurations (e.g., high censoring or treatment imbalance).
- **Real data experiment has limited sample size** (541 patients) and the LPB values are small (0.3–0.65 years). The clinical interpretability of these LPBs and whether they are practically meaningful for treatment selection is not discussed.
- **No comparison with alternative conformal survival methods** that might also achieve exact coverage under different assumptions (e.g., Candès et al. 2023 for Type-I censoring). The baselines are all PAC-type methods, which is appropriate but limits the scope of comparison.

### Trivial
None.

## Nice-to-Haves

- A finite-sample analysis of the doubly robust property (even under stronger assumptions) would strengthen the theoretical contribution.
- An ablation study varying the quality of the weight estimator (e.g., using misspecified models) to empirically validate the robustness.
- Discussion of computational complexity and scalability, especially for larger datasets or higher-dimensional covariates.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Clarify in the main text that the doubly robustness result (Theorem 4.2) is asymptotic and discuss the practical implications of the required conditions.
- Add an experiment where the weight function is intentionally misspecified (e.g., using a linear model when the true relationship is nonlinear) to demonstrate robustness.
- Discuss the practical significance of the LPB values in the real data experiment (e.g., what does a 0.5-year LPB mean for treatment decisions?).

## Score and Decision

**Score**: 8

**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>