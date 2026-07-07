## Summary

This paper proposes a "Covariance-Adjusted Support Vector Machine" (CSVM) that whitens each class's training data via class-conditional Cholesky decomposition before running SVM, then reverse-transforms the classifier. The paper claims that standard SVM is invalid in "non-Euclidean" input spaces and that incorporating class-specific covariance yields a margin ratio proportional to intra-class dispersion. A self-training heuristic (SM Algorithm) is proposed to iteratively estimate population covariance. Experiments compare CSVM against standard SVM kernels and PCA/ZCA whitening on five binary datasets.

## Strengths

- **Class-conditional covariance is a legitimate design concern.** The intuition that classes with higher variance warrant a larger margin allocation has support in the literature, and the paper correctly cites relevant work (MCVSVM, weighted Mahalanobis kernels, maxi-min margin machine, etc.).
- **The baseline set provides a basic sanity check.** Experiments include linear, RBF, sigmoid, and polynomial SVMs plus PCA and ZCA whitening across five datasets from different domains (healthcare, astronomy, quality, safety).

## Weaknesses

### Fatal
None individually — the issues below are collectively severe enough to warrant rejection, but each is in principle addressable. No single error makes the paper irretrievable.

### Major

1. **The core theoretical framing is based on a mathematical misunderstanding.** The paper repeatedly claims the input/statistical space is "non-Euclidean" (abstract, lines 15, 45) because it uses Mahalanobis rather than Euclidean distance. This is incorrect: ℝ^N with inner product ⟨u,v⟩_Σ = u^T Σ^{-1} v is still a finite-dimensional inner product space over ℝ — i.e., a Euclidean space. The paper conflates "using the identity-covariance Euclidean metric" with "being a Euclidean space." This error directly undermines:
   - **Lemma 2.1:** The claim that SVM principles are "valid only" after transformation is false — SVM works in ℝ^N under any inner product.
   - **Lemma 2.2:** The claim that N classes yield N classifiers is a design choice (using separate class-conditional covariances), not a mathematical necessity.
   - **Lemma 2.3:** The claim that "KKT boundary conditions are not valid" because all points contribute to Σ^{-1} is a factual error. KKT conditions are optimality conditions for any convex constrained optimization; using a covariance-weighted objective does not invalidate them.
   
   The algebra in equations (1)–(14) is correct as algebraic manipulation, but the interpretation that motivates the paper's claimed novelty does not follow. The paper's own statement (line 317) that experiments "validate the findings of lemma 2.1, 2.2 and 2.3" makes this a central issue.

2. **The SM Algorithm applies different linear transformations to each class, creating a geometrically ill-defined optimization.** Step 2(b) transforms Train₁ by C_{y=1}^{-1} and Train_{-1} by C_{y=-1}^{-1}. Step 2(c) then performs SVM on the union of these differently-transformed sets. After distinct linear maps, the dot product between a class-1 point and a class-(-1) point (both in "Euclidean space" per the algorithm) has no consistent geometric interpretation — it mixes two different whitening transformations. The resulting θ_Euclidean is then used in step 2(e) to compute a margin ratio involving S_{y=1}^{-1} and S_{y=-1}^{-1}, mixing quantities from incommensurate geometries. The theoretical derivation (Section 2) suggests two separate optimization problems (equations 10 and 12), but the algorithm produces one modified classifier by adjusting only the intercept. The connection between theory and algorithm is broken.

3. **The experimental evaluation lacks any statistical validity.** Results are from a single 80:20 train-test split (line 169). There are no standard deviations, confidence intervals, cross-validation, or significance tests. Reported improvements over the linear SVM baseline are small and well within the noise of a single split (e.g., Breast Cancer accuracy 0.974 vs 0.956; Diabetes 0.786 vs 0.760; Pulsar 0.981 vs 0.979). On OSHA, CSVM is outperformed by RBF SVM on accuracy (0.752 vs 0.760) and precision (0.747 vs 0.766). ROC AUC values are effectively tied on several datasets (OSHA: 0.72 for CSVM vs 0.72 for RBF; Diabetes: 0.74 for CSVM, linear, PCA, and ZCA). Without uncertainty quantification, these marginal differences cannot be interpreted as evidence of superiority.

4. **The paper claims to fix limitations of prior work but never compares against it.** The introduction lists MCVSVM (Zafeiriou et al., 2007), MD-BLSSVM (Ke et al., 2018), the maxi-min margin machine (Huang et al., 2004), weighted Mahalanobis kernels (Wang et al., 2007), and Mahalanobis TSVM (Peng & Xu, 2012). It asserts these have "gaps in application of appropriate vector spaces and dimensional inconsistencies" (line 21). Yet none of these methods appear in the experiments — the comparison is limited to standard kernels and PCA/ZCA whitening. The claim that CSVM "rectifies" prior gaps is therefore unsubstantiated.

### Minor

5. **Algorithm contradicts Lemma 2.2.** The lemma states a binary problem yields "two unique linear classifiers," but the SM Algorithm produces a single modified classifier (step 2(e) adjusts only one intercept θ₀). The paper does not explain how a two-classifier formulation would be used for prediction, nor why the algorithm reduces it to one.

6. **No ablation isolating the self-training effect.** The SM Algorithm iteratively adds test data to the training set (steps 2(f)–(g)). Any improvement could come simply from having more training data rather than from the covariance adjustment. An experiment comparing against the same self-training loop without class-conditional transformation is needed.

7. **No computational cost analysis despite raising the question.** Line 321 asks "is the increase in classification performance worth the computational complexity?" but the paper provides no runtime measurements or scalability experiments.

### Trivial

None.

## Nice-to-Haves

- Compare against the covariance-aware SVM methods cited in the introduction (MCVSVM, MD-BLSSVM, maxi-min margin machine, weighted Mahalanobis kernels, Mahalanobis TSVM) to substantiate the central claim of improvement.
- Report results over multiple random train-test splits (≥10) with standard deviations, or use k-fold cross-validation.
- Add an ablation: run the SM self-training loop using standard linear SVM (without class-conditional Cholesky transformation) to isolate the effect of covariance adjustment from the self-training data augmentation.
- Consider using a single pooled within-class covariance or a properly formulated joint optimization so that the SVM in the transformed space is geometrically well-defined.

## Removed Points

- **Missing hyperparameter documentation for baselines.** Per rules, pure documentation nitpicks are removed. However, the observation that the sigmoid kernel performs at 0.4–0.6 accuracy (suggesting untuned defaults) is a substantive experimental fairness concern that is partially reflected in Major weakness #3 (experimental rigor lacking details).
- **No comparison to semi-supervised SVMs (S3VM/TSVM).** The SM Algorithm is presented as a heuristic for covariance estimation, not as a general semi-supervised method. A comparison would strengthen the paper but its absence is not a core flaw.
- **Section-by-section editorial notes.** These are consolidated into the specific weaknesses above.
- **Vague framing criticism about "two classifiers" not being a theorem.** Captured in Major weakness #1 (mathematical misunderstanding of the lemmas' status).

## Novel Insights

None beyond the paper's own contributions. The core observation that within-class covariance should affect margin allocation is already present in the cited prior work (MCVSVM, weighted Mahalanobis kernels, maxi-min margin machine). The paper's attempted contribution — deriving this from a "non-Euclidean" framing — does not produce new valid insights because the foundational premise is incorrect.

## Suggestions

1. **Drop the "non-Euclidean space" framing entirely.** Present the method as learning a class-conditional Mahalanobis metric for SVM. The algebra works the same way; the misleading terminology is a liability, not a contribution.
2. **Use a single pooled within-class covariance (or formulate a proper joint optimization) instead of applying different transformations per class.** This would make the SVM in the transformed space geometrically coherent.
3. **Include the relevant prior covariance-aware SVM methods as experimental baselines.** Without this, the paper's main advertised advantage over prior work cannot be assessed.
4. **Report mean and standard deviation over multiple random splits or use cross-validation.** The current single-split results are statistically uninformative.

## Score and Decision

**MY FINAL SCORE:** <score>3.0</score>
**MY FINAL DECISION:** <decision>Reject</decision>