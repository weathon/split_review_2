Now I have the calibrated favorability signals. Let me construct the final review.

## Summary

This paper proposes Covariance-Adjusted SVM (CSVM), which uses class-specific Cholesky whitening transformations to map data from "statistical (non-Euclidean) space" to Euclidean space, formulates SVM in that space, and derives covariance-dependent margin ratios. An iterative algorithm (SM Algorithm) is proposed to estimate population covariance from sample data. The method is tested on 5 datasets with comparisons against standard SVM kernels and PCA/ZCA whitening.

## Strengths

- **The connection between Mahalanobis distance and Euclidean distance via Cholesky decomposition (Equation 1) is mathematically sound** — the identity (X−μ)ᵀΣ⁻¹(X−μ) = [Ψ⁻¹(X−μ)]ᵀ[Ψ⁻¹(X−μ)] where Σ = ΨΨᵀ is a standard and correct relationship that properly motivates using whitening as a vector-space transformation.

- **The motivation that standard SVM's Euclidean geometry ignores class-specific dispersion, and that wider margins should be allocated to more dispersed classes, is a sensible starting point** that has been explored in prior work (MCVSVM, Mahalanobis-distance SVMs) and is worth examining.

## Weaknesses

### Fatal
None.

### Major

- **Unclear/confused optimization derivation in Section 2 (Equations 10–13):** The paper presents two separate optimization problems minimizing different quadratic forms (½θᵀΣ_{y=1}⁻¹θ vs. ½θᵀΣ_{y=-1}⁻¹θ) while sharing the same optimization variables (θ, θ₀). The paper neither specifies how to resolve this conflict into a single well-posed objective, nor clarifies whether the two problems are meant to produce separate classifiers (Lemma 2.2 claims two classifiers yet uses identical variables for both). This makes the theoretical foundation in Section 2 incoherent as a basis for the algorithm that follows.

- **Geometric inconsistency in the class-specific whitening framework:** Equation (3) defines two different transformations (Ψ_{y=1}⁻¹ and Ψ_{y=-1}⁻¹) for data of each class. Step 2(c) of the SM Algorithm then runs SVM on the concatenated transformed data. While both transformations map to Rⁿ with the standard dot product (they are not in "different vector spaces" in a literal sense), the fundamental problem is that the resulting decision boundary θᵀΨ_{y}⁻¹X + θ₀ = 0 requires knowing which class-specific transformation to apply — but the class label is what the classifier is supposed to predict. The SM Algorithm avoids this circularity in practice by using a separate standard linear SVM (θ_input) on the original data and only using the whitened SVM to compute a bias adjustment (steps 2(d)–(f)), but the theoretical derivation in Section 2 never acknowledges or resolves this inconsistency, and the relationship between the two classifiers is not theoretically justified.

- **No ablation isolating the source of improvements:** CSVM differs from standard SVM in at least three ways: (a) class-specific whitening vs. none, (b) covariance-dependent margin ratio adjustment, and (c) iterative self-training (SM Algorithm). There is no experiment isolating which component drives the improvements. The reported gains could plausibly come entirely from the self-training loop or from overfitting, rather than from the covariance-adjustment theory that is the paper's central contribution.

- **Weak experimental evaluation without variance reporting:** Every metric in Tables 1–4 is a point estimate from a single 80/20 split. No standard deviations, confidence intervals, or statistical tests are reported. The improvements over baselines are marginal (accuracy differences of 0.002–0.026), and on OSHA the method is *worse* than RBF SVM (0.752 vs. 0.760). Without variance estimates, these tiny differences could easily be within the noise of a single split.

- **Unfair baseline comparisons:** The paper applies "SVM-Linear, SVM-RBF, SVM-Sigmoid, SVM-Poly" without mentioning any hyperparameter search. RBF SVM has critical hyperparameters (C, γ); polynomial kernels have degree and coef0. If these were used at default values, the comparison is unfair — comparing a custom method against off-the-shelf baselines used suboptimally. No dataset characteristics (size, dimensionality, class balance) are reported, making it difficult to assess whether the datasets are trivially easy or whether results generalize.

### Minor

- **Overstated framing:** The introduction claims SVM "should not be valid in the input space as it is Non-Euclidean," which is too categorical. SVM with a linear kernel works in the input space regardless of whether the Euclidean metric is the best choice; the metric choice affects performance but does not make standard SVM "invalid." This framing overstates the mathematical necessity of the proposed approach.

- **Disconnect between theoretical claims and empirical evidence:** The paper claims that experiments validate Lemmas 2.1, 2.2, and 2.3 (concerning KKT conditions, number of classifiers, and covariance-dependent margins), but the experiments only report aggregate accuracy/precision/recall/AUC numbers. None of these directly test whether KKT conditions are invalid in input space or whether two unique classifiers exist for binary problems.

### Trivial
None.

## Nice-to-Haves

- Provide dataset characteristics (size, dimensionality, class balance).
- Report results with multiple train/test splits or cross-validation with standard deviations.
- Tune baseline hyperparameters (C, γ for RBF; degree for polynomial) via grid search or report the settings used.
- Add an ablation study: (1) linear SVM alone, (2) pooled-whitening + linear SVM, (3) class-specific whitening + SVM (without self-training), (4) full CSVM with SM Algorithm.
- Either reconcile the theoretical derivation (Section 2) with the algorithm (Section 3), or clearly separate them, noting that the SM Algorithm is a heuristic that diverges from the theoretical framing.

## Removed Points

- **Self-training literature citation complaint:** REMOVED per hard rules (criticisms about missing related works are not permitted).
- **Claim about "incommensurate vector spaces" / "different inner product structures":** REMOVED as partially inaccurate — both Ψ₁⁻¹ and Ψ₂⁻¹ map to Rⁿ with the standard Euclidean dot product; the real issue is about classification rule ambiguity, not incompatible spaces.
- **Reproducibility nitpicks about undisclosed implementation details:** REMOVED per hard rules.
- **Generic strengths about importance of the problem:** REMOVED as superficial.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The most productive direction would be to abandon the class-specific transformation framework and instead use a single whitening transformation derived from the pooled within-class covariance matrix, which places all data in a single Euclidean space and makes the SVM formulation well-posed. The self-training component (SM Algorithm) should then be clearly separated from the whitening component, with ablations comparing pooled whitening + linear SVM, class-specific whitening in a common pooled space, and the iterative self-training procedure.

## Score and Decision

This paper has a sensible motivation but suffers from multiple serious issues: the optimization derivation in Section 2 is mathematically incoherent, the class-specific whitening framework introduces a circularity in the classification rule that is not resolved, the experimental evaluation is far too weak to support the claims (no variance, tiny margins, no hyperparameter tuning for baselines, no ablation study), and there is a clear disconnect between the theoretical claims and the empirical evidence presented. The paper should not be accepted in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>