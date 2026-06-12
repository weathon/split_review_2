## Summary

This paper proposes a Covariance-Adjusted Support Vector Machine (CSVM) that performs class-wise Cholesky decomposition of covariance matrices to transform data from "non-Euclidean" input space to Euclidean space before SVM classification. The authors derive that in the input space, the SVM margin for each class depends on its intra-class covariance, and propose an iterative "SM Algorithm" to estimate population covariance-adjusted classifiers from training data. Experiments on five binary classification datasets claim improvements over standard SVM kernels and PCA/ZCA whitening approaches.

## Strengths

- **Interesting core premise.** The idea that class-specific whitening (rather than global whitening) before SVM can improve performance is practically reasonable and well-motivated by the observation that different classes may have different covariance structures. This is a legitimate insight worth exploring.

- **Comprehensive baseline comparison.** The paper compares against linear SVM, RBF, sigmoid, polynomial kernels, and PCA/ZCA whitening + SVM across five datasets spanning healthcare, astronomy, and other domains, providing a broad empirical picture.

- **Consistent direction of improvement.** CSVM achieves the highest accuracy, recall, and F1 on 4 of 5 datasets and highest precision on 3 of 5 datasets, with highest AUC on 3 of 5 datasets. The results are consistently favorable rather than cherry-picked.

## Weaknesses

### Fatal

- **The SM Algorithm uses test data labels during training, invalidating the fair comparison.** In steps 2(f)–2(g) of the SM Algorithm, test data points are labeled based on the current classifier and then *added to the training set* to re-estimate covariance matrices. This is a form of semi-supervised self-training that uses the test set during model fitting. All baselines (standard SVM, PCA/ZCA + SVM) use only training data. The reported improvements over baselines therefore reflect a fundamentally different information regime (test data leakage), not a fair methodological comparison. This undermines the entire experimental validation.

### Major

- **Central theoretical claims are overstated and conflated.** The paper states that "KKT boundary conditions are not valid in the input space" (Lemma 2.3) and that "max-margin classification is valid only in Euclidean space." KKT conditions are mathematical properties of a convex optimization problem and hold whenever the problem is well-posed and constraint qualifications are met—this is independent of any notion of the data's "natural geometry." The data vectors live in R^n, the optimization is convex, and KKT conditions apply. The paper conflates "the optimization objective may not be well-motivated" with "the optimization is mathematically invalid," which are fundamentally different claims.

- **The two-classifier result (Lemma 2.2) is not properly resolved.** The paper derives that each class gets its own optimization problem and hence its own classifier, but a single hyperplane cannot simultaneously be the solution to two different optimization problems. The SM Algorithm attempts to reconcile this by computing a single classifier with an adjusted bias, but the adjustment procedure (step 2(e)) is vaguely specified ("adjusts θ₀ to θ₀' so that the modified classifier divides the margin in ratio...") without a concrete formula or proof that such an adjustment exists or is unique.

- **Evaluation methodology is weak.** No cross-validation (single 80/20 split), no statistical significance tests, and no variance/confidence intervals are reported. With only one random split, the results could easily be due to randomness. Given the marginal improvements in several cases (e.g., Diabetes accuracy 0.786 vs. 0.760, OSHA where CSVM doesn't win on accuracy), significance testing is essential.

### Minor

- **No comparison with modern methods.** Comparing only against SVM variants is insufficient to establish practical value. Random forests, gradient boosting, and other ensemble methods are strong baselines that should be included.

- **Singular covariance matrices not addressed.** The method requires inverting class covariance matrices via Cholesky decomposition. No discussion is provided for high-dimensional settings (p > n) or cases where covariance matrices are singular/near-singular.

- **Convergence of SM Algorithm not analyzed.** The paper offers no proof or empirical evidence that the iterative algorithm converges, nor does it specify what "convergence" means precisely (label stability threshold is mentioned but not quantified).

- **Marginal improvements on several datasets.** On the OSHA and Diabetes datasets, CSVM's advantage over linear SVM or whitening approaches is very small (e.g., Diabetes AUC: 0.74 for all methods), suggesting the method may not generalize well.

### Trivial

- The notation switches between Ψ and C for the Cholesky factor between Sections 2 and 3 without explanation.

## Nice-to-Haves

- Ablation study separating the effect of class-wise whitening from the iterative SM Algorithm to understand each component's contribution.
- Analysis of sensitivity to the initial covariance estimate and convergence behavior across iterations.
- Discussion of computational complexity in quantitative terms (wall-clock time comparisons).

## Novel Insights

The paper's most genuinely novel contribution is the argument for class-specific whitening rather than global whitening before SVM, grounded in the observation that different classes have different covariance structures and thus need different transformations. The theoretical framework connecting Mahalanobis distance to vector space transformations is a useful pedagogical perspective. However, the practical benefit over global whitening appears small in the experiments, and the iterative self-training component—which is where the real improvement likely comes from—is not a novel technique, being essentially a form of semi-supervised pseudo-labeling.

## Suggestions

1. **Fix the experimental protocol.** Either (a) remove test data from the SM Algorithm and evaluate it as a purely supervised method, or (b) properly frame it as semi-supervised and compare against semi-supervised baselines with the same test data access.
2. **Add cross-validation and significance testing.** Report mean ± std over multiple folds/splits.
3. **Moderate the theoretical claims.** Replace statements about KKT conditions being "invalid" with statements about the optimization objective not accounting for covariance structure. The KKT conditions hold for the optimization as formulated; the question is whether the formulation is appropriate.
4. **Specify the bias adjustment formula.** Step 2(e) of the SM Algorithm needs a concrete, implementable formula.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>