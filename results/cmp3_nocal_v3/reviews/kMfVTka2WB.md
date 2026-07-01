## Summary

The paper proposes Covariance-Adjusted SVM (CSVM), a method that uses class-specific covariance information (via Cholesky decomposition) to adjust the margin allocation in SVM classification. The core mathematical observation — that the margin ratio between two classes in a per-class-whitened SVM depends on their covariance matrices (equation 14) — is a clean formalization of an intuitive idea. The paper also presents an iterative self-training algorithm (SM Algorithm) to estimate population covariance when test labels are unknown.

---

## Strengths

1. **Equation (14) — the margin ratio formula — is a clear mathematical observation.** The derivation showing that under per-class whitening, the margin allocated to each class is proportional to its covariance structure (specifically the ratio √(θᵀΣ₋₁⁻¹θ) / √(θᵀΣ₁⁻¹θ)) is algebraically sound and captures a genuine intuition: classes with higher dispersion should receive a larger margin. This is the paper's most defensible contribution.

2. **The paper tackles a real practical question.** Standard SVM treats all classes symmetrically in margin allocation, ignoring within-class covariance structure. Recognizing that class dispersion should influence the decision boundary is a worthwhile goal, and the paper's attempt to formalize this via Mahalanobis distance has internal consistency.

---

## Weaknesses

### Fatal
None. No single error invalidates the paper's core claims beyond repair; the margin ratio formula is mathematically correct and the method is implementable.

### Major

1. **The "non-Euclidean space" framing is conceptually confused and overclaims.** The paper repeatedly asserts that the input space is "non-Euclidean" and that SVM is "invalid" there (Lemma 2.1, Abstract, Introduction). This is not correct: ℝ^d with the standard L₂ norm is Euclidean by definition. Mahalanobis distance is equivalent to Euclidean distance after a linear (whitening) transformation — a fact the paper itself acknowledges in equation (1). The paper is arguing for a different *metric* on the same space, not a different space. The claim that "KKT boundary conditions are valid only in Euclidean vector spaces" is stated without proof and is not a standard property of KKT conditions (which depend on convexity and differentiability, not the metric). This inflated framing weakens the paper's credibility; the actual insight (margin should account for class covariance) does not depend on calling the input space non-Euclidean.

2. **Inconsistency between Lemma 2.2 and the SM Algorithm.** Lemma 2.2 claims that in the input space, "there will be N linear classifiers" for N classes. For binary classification, this means two classifiers. However, the SM Algorithm (Section 3) produces a *single* linear classifier: Step (d) performs linear SVM on the original training data to obtain one classifier (θ_inputᵀx + θ₀ = 0), and Step (e) adjusts only its intercept. The paper never explains why the theory predicts two classifiers but the algorithm produces one, nor does it reconcile this disconnect.

3. **The experimental evaluation is too weak to support the claimed improvements.**
   - **(a) No measure of variance or statistical significance.** All metrics (accuracy, precision, recall, F1) are reported as single numbers across all five datasets — no confidence intervals, standard deviations, or repeated runs. The claimed improvements over linear SVM are often tiny (e.g., Pulsar accuracy: 0.981 vs. 0.979; Diabetes accuracy: 0.786 vs. 0.760), and without variance estimates these differences are indistinguishable from sampling noise, especially on a single 80/20 split.
   - **(b) No hyperparameter tuning for baselines.** The baselines include SVM-RBF, SVM-Poly, and SVM-Sigmoid, all of which are sensitive to kernel parameters (γ, degree) and the regularization parameter C. No grid search, cross-validation, or hyperparameter selection procedure is reported. Using default parameters systematically disadvantages the kernel baselines and makes the comparison unfair.
   - **(c) No comparison against the most relevant prior work.** The Introduction criticizes MCVSVM (Zafeiriou et al. 2007), MD-TSVM (Peng & Xu 2012), MD-BLSSVM (Ke et al. 2018), and other covariance-aware SVM methods for having "gaps" and "dimensional inconsistencies." Yet the paper never compares CSVM against *any* of these methods empirically. This is the most directly relevant comparison class, and its absence is a decisive gap. Without it, the reader cannot assess whether CSVM offers any improvement over existing covariance-adjusted SVM approaches.
   - **(d) No ablation studies.** The CSVM method has multiple components: per-class whitening, Cholesky decomposition, the margin-ratio adjustment, the iterative self-training loop. No ablation isolates which component drives the results. The improvements over linear SVM could be entirely due to the whitening step (standard preprocessing) with no contribution from the novel margin-ratio adjustment or SM iteration.

4. **The criticism of prior work is unsubstantiated.** The Introduction states that "analysis of the optimization problems formulated in those studies revealed gaps in application of appropriate vector spaces and dimensional inconsistencies." This claim is never elaborated anywhere in the paper — no specific gap or inconsistency is identified for any cited work. Section 4 similarly claims to "address the limitations of previous studies done in variance adjusted SVM" but provides no concrete comparison or demonstration. Asserting errors in prior work without demonstration is a scholarly lapse.

5. **The SM Algorithm's behavior is unanalyzed.** The algorithm iteratively adds test data (with predicted labels) to the training set to recompute covariance — essentially self-training. The paper acknowledges this is "heuristic" but provides:
   - No analysis of how mislabeled test data corrupts the covariance estimate (error propagation).
   - No discussion of convergence conditions (the criterion is that labels "stop moving," but they could stabilize on wrong labels).
   - No comparison against a simpler non-iterative baseline (e.g., CSVM using only training-data covariance, without iteration). So it is impossible to tell whether the iteration helps or hurts.

### Minor

1. **The claim that "the literature is divided on the reasons for [whitening improving SVM performance]" (Section 4) is unsupported by any citation.** The paper asserts this as a motivation but provides no reference for the claimed disagreement, weakening the stated novelty.

2. **No dataset characteristics are reported.** The paper lists five dataset names but gives no information about their size, number of features, class balance, or preprocessing applied. This makes the results harder to interpret.

3. **No handling of singular covariance matrices is discussed.** If the number of training examples per class is smaller than the number of features, the sample covariance matrix will be singular and Cholesky decomposition will fail. This is a practical concern the paper does not address.

4. **The geometric interpretation of the "margin" in equation (9) is unclear.** The quantity 1/√(θᵀΣ⁻¹θ) is the Euclidean margin in the *transformed* space expressed in original coordinates. The paper treats it as a margin in the input space without justifying why this quantity has a meaningful geometric interpretation there.

### Trivial
None.

---

## Nice-to-Haves

- **Derive a single unified optimization problem** that incorporates both class covariances jointly, rather than deriving two separate problems (equations 10–13) and then reconciling them heuristically via the SM Algorithm. Resolving the two-classifier vs. one-classifier inconsistency would significantly strengthen the theoretical framing.
- **Validate the SM Algorithm against simpler alternatives:** (a) CSVM with training-data-only covariance (no iteration), (b) CSVM with pooled/global whitening instead of per-class whitening, and (c) the full iterative SM Algorithm. This would isolate where the gains come from.
- **Compare against MCVSVM, MD-TSVM, MD-BLSSVM, and other covariance-aware SVM methods** before or alongside comparisons against generic RBF/Poly/Sigmoid kernels. This is the most directly relevant comparison class and the paper already claims to improve upon them.

---

## Removed Points

- *"No code or reproducibility information"* — Removed per Hard Rules: reproducibility nitpicks about artifacts impractical to include in a submission are to be removed.
- *"No alternative optimality conditions discussed"* — Removed as scope creep; the paper does not claim to need alternative optimality conditions, and demanding them is outside the paper's stated scope.
- *"KKT conditions claim is stated without proof"* — This is kept in spirit under Major weakness #1 (the non-Euclidean framing confusion), where the unsupported KKT claim is discussed.
- *Some generic section-by-section notes* — Several notes in the input review (about equation numbering, aesthetic presentation, etc.) were filtered as they do not constitute substantive weaknesses.

---

## Novel Insights

None beyond the paper's own contributions. The input review identifies the core conceptual confusion (non-Euclidean framing) and the inconsistencies between theory and algorithm, but these are critiques that reveal the paper's limitations rather than novel observations about the subject matter.

---

## Suggestions

1. **Drop the "non-Euclidean space" rhetoric.** Reframe the contribution as a *class-weighted margin adjustment* or *metric-learning approach to SVM* that uses per-class covariance to allocate margins. The mathematics (equation 14) stands on its own without this framing.
2. **Reconcile Lemma 2.2 with the actual algorithm.** Either revise the lemma to match what the algorithm does (one adjusted classifier), or modify the algorithm to produce two classifiers and justify when two are needed.
3. **Add error bars and statistical tests** (e.g., repeated stratified cross-validation with standard deviations) to the experimental results. Most reported improvements are small and could be noise.
4. **Compare against the prior covariance-aware SVM methods** that the paper criticizes. This is essential to establish whether CSVM actually addresses their limitations.
5. **Include ablation experiments** isolating the effect of (a) whitening alone, (b) margin ratio adjustment without iteration, and (c) full SM iteration.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>