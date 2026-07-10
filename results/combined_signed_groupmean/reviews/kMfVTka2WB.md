## Summary

This paper proposes Covariance-Adjusted SVM (CSVM), which uses class-specific Cholesky whitening to decorrelate each class's data before SVM training, then reverses the transformation to obtain class-dependent margin constraints in the original space. The paper additionally introduces the SM Algorithm, a self-training procedure that iteratively estimates population covariances from sample covariances by pseudo-labeling test data. Experiments on five datasets compare CSVM against standard SVM kernels and PCA/ZCA whitening.

## Strengths

- **Clean derivation connecting Mahalanobis distance to Cholesky-based whitening (Section 2, Eq. 1-3).** The paper correctly shows that Mahalanobis distance can be rewritten as Euclidean distance after applying the inverse Cholesky factor of the covariance matrix. This is mathematically sound and provides a clear pedagogical link between the two distance metrics.

- **Identifies a genuine operational problem.** The paper correctly recognizes that class-conditional whitening at test time requires label information, creating a chicken-and-egg problem. The SM Algorithm's attempt to address this via iterative self-training targets a real difficulty, even if the proposed solution has significant limitations.

- **Transparent about limitations.** Section 6 explicitly acknowledges that the SM algorithm is a heuristic, discusses the computational complexity trade-off, and admits that perfect classification is not achieved. This candor is commendable.

## Weaknesses

### Major

- **Fundamental inconsistency between the theoretical derivation and the practical algorithm.** Lemma 2.2 states that a binary classification problem requires *two* distinct linear classifiers in the input space — one per class — and Lemma 2.3 states that KKT conditions are invalid in the input space. Yet the SM Algorithm (step d-f) trains a *single* standard linear SVM on the original input-space data (which relies on KKT conditions) and adjusts only its bias term. The paper never explains how two classifiers would be combined for prediction, nor does it reconcile the claim that KKT conditions are invalid with the algorithm's use of standard SVM in input space. This disconnect between theory (Section 2) and practice (Section 3) undermines the paper's claimed contributions.

- **Class-specific whitening places data into incompatible coordinate systems.** Equation (3) defines distinct transformations for each class: X^{Euclidean}_{y=1} = Ψ_{y=1}^{-1} X^{Input}_{y=1} and X^{Euclidean}_{y=-1} = Ψ_{y=-1}^{-1} X^{Input}_{y=-1}. Since Ψ_{y=1}^{-1} and Ψ_{y=-1}^{-1} are generally different matrices, the "Euclidean space" representations of the two classes live in different bases. An inner product between a class-1 point transformed by L₁^{-1} and a class-2 point transformed by L₂^{-1} is not a standard Euclidean inner product — it involves a cross-covariance term L₁^{-T}L₂^{-1}. Step (c) of the SM Algorithm performs SVM jointly on such incompatible representations without addressing this issue. The algorithm effectively sidesteps the problem by using a separate input-space SVM for the actual classifier (step d), but this creates a gap between the claimed theory and what is actually implemented.

- **Conceptual framing is misleading and the theoretical contributions are overstated.** The paper claims the "input space is Non-Euclidean" and that SVM principles are "valid only in Euclidean spaces" (Lemma 2.1). In reality, ℝ^d with the standard inner product is definitionally a Euclidean space; non-spherical data covariance does not change the geometry of the space. Whitening is standard preprocessing (feature decorrelation/standardization), not a geometric discovery. Lemma 2.3 further asserts that "KKT boundary conditions are not valid in the input space" — this is mathematically incorrect: KKT conditions apply to any convex optimization problem regardless of data covariance structure. The paper presents standard operations as novel theoretical findings.

- **The SM Algorithm is underspecified in critical details.** Step (e) says "Adjust θ_0 to θ'_0" to achieve a specific margin ratio but provides no procedure, formula, or algorithm for computing θ'_₀ from the given ratio. The convergence criterion is "changes in test data labels are below a certain threshold" — no threshold is specified. There is no analysis of fixed points, convergence guarantees, or sensitivity to initialization.

### Minor

- **Theoretical derivation assumes hard-margin SVM (ξ_i = 0, stated in Eqs. 6-7 and 10-13),** but real-world datasets are almost never linearly separable. The empirical evaluation presumably uses soft-margin SVM (otherwise many datasets would not be separable). The paper does not discuss how slack variables would be incorporated into the CSVM formulation, creating a gap between theory and experiments.

- **Experimental evaluation is weak in several respects.** (a) Results report point estimates from a single 80/20 split with no standard deviations, confidence intervals, or cross-validation, making it impossible to assess whether small differences (e.g., 0.981 vs 0.979 accuracy on Pulsar) are significant. (b) Gains are modest and inconsistent — on OSHA data CSVM is not the best on any metric, on Diabetes the AUC (0.74) ties with three other methods. (c) No comparison with the most directly relevant prior work, Minimum Class Variance SVM (MCVSVM, Zafeiriou et al. 2007), which the paper cites and which also incorporates within-class scatter into SVM.

### Trivial

None.

## Nice-to-Haves

- Extend the theoretical derivation to soft-margin SVM.
- Add the missing prediction rule for the two-classifier formulation from Lemma 2.2.
- Include MCVSVM (Zafeiriou et al. 2007) as a baseline.
- Provide a convergence analysis or at least empirical convergence plots for the SM Algorithm.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"Core premise conflates data distribution with space geometry (fatal)."* — This criticism is factually correct (the paper's framing is indeed non-standard), but the paper's actual mathematical operations (Cholesky whitening + SVM) are standard and correct regardless of terminology. The overstated framing is a presentation problem, not a mathematical error that invalidates the core contribution. It has been merged into the "Conceptual framing is misleading and overstated" Major weakness above.

- *"No modern baselines (random forests, gradient boosting, neural networks)."* — Scope creep. The paper is about SVM-based methods, and requiring comparisons against entirely different classifier families is outside the stated scope.

- *"No reproducibility details (random seed, hyperparameters, solver)."* — The appendix section (which would contain implementation details) is stripped by the parser and exists in the original submission.

## Novel Insights

None beyond the paper's own contributions. The input review accurately identifies a genuine mathematical issue — the incompatibility of coordinate systems under class-specific Cholesky whitening — that the paper does not address, and documents a clear disconnect between the theoretical lemmas and the practical algorithm.

## Suggestions

1. Resolve the theory-algorithm disconnect: either derive the SM Algorithm from the theoretical framework, or reframe the theoretical claims to match what the algorithm actually does (one adjusted linear classifier, not two).
2. Address the incompatible-coordinate-system issue: specify how SVM is performed on data transformed by different class-specific matrices, or reformulate the approach using a single pooled whitening transform.
3. Provide a concrete formula for computing θ'_₀ from the margin ratio in the SM Algorithm.
4. Add standard deviations or confidence intervals to experimental results and include MCVSVM as a baseline.
5. Extend the hard-margin derivation to the soft-margin case.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| u1cQYxRI1H.md (IC-Light) | 0.50 | R1 | No | Unrelated topic (diffusion illumination); strong accept |
| 5lUdTogEL3.md (Lifelong ReID) | 1.00 | R1 | No | Unrelated topic |
| bEgDEyy2Yk.md (Minimax Path) | 1.00 | R1 | No | Unrelated topic |
| ZDoaLbOFaP.md (Sparse Cov VNN) | 3.00 | R1 | Yes | Most relevant anchor. Had strong experiments (+10.00) and sound theory (+9.55) but minor novelty. Our paper has weaker experiments (single split, no error bars) and internal theory-algorithm inconsistencies — below this anchor. |
| qcyn7ESaM8.md (PCA Class Bias) | 2.50 | R1 | No | Somewhat related (PCA + class structure) |
| anek0q7QPL.md (Cov+Hessian Eigenanalysis) | 5.00 | R1 | Yes | Related topic (covariance + classification). Had stronger empirical evidence (+9.83) despite unclear contributions. |
| Q1kPHLUbhi.md (Self-Sup Cov Est) | 6.25 | R1 | Yes | Different profile — strong theory-experiment balance, accepted. Not comparable. |
| ZINaxJyoQr.md (Barlow Twins Norm) | 1.50 | R2 | Yes | Most distant. Had no experiments and tackled a non-existent problem. Our paper has more substance (correct derivation, some experiments) — above this anchor. |
| 2NwHLAffZZ.md (Weak Correlations) | 2.33 | R2 | No | Unrelated topic |

**Bracketing:** Round 1 established a plausible range of 2.0–3.5. Comparing item-level impact scores:
- Our paper shares the "minor novelty / unclear contribution" profile of Sparse Cov VNN (3.00) but lacks its strong experiments (+10.00 vs our weak point estimates) and sound theory (+9.55 vs our internal inconsistencies).
- Our paper has more substance than the 1.5-level anchors (which were essentially empty/incomplete).
- The fatal-scoring items in our draft (theory-algorithm disconnect at -10.00, incompatible coordinate systems at -9.98, overstated claims at -10.00) are verifiable from the paper text and place it decisively below the 3.00 anchor.

The paper has a correct but standard mathematical core (Cholesky whitening + SVM), but this core is presented with misleading framing, the theoretical derivation does not match the practical algorithm, the algorithm itself contains an unresolved mathematical issue (incompatible coordinate systems), and the experimental support is weak. These are structural problems that revisions could only partially address.

**Final Score: 2.0**  
**Decision: Reject**

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>