## Summary

This paper argues that traditional support vector classification is valid only in Euclidean spaces, and that in the “non-Euclidean” input (statistical) space the max-margin principle must be adjusted according to each class’s intra-class covariance. The authors propose to first transform each class separately to Euclidean space via Cholesky decomposition of its covariance matrix, solve the SVM problem there, and then reverse-transform to the original space, yielding class-specific margins. They also present an iterative algorithm (SM algorithm) that estimates population covariance from training data and adapts the decision boundary. Experiments on five datasets show modest improvements in accuracy, precision, recall, F1, and AUC compared to linear and kernel SVMs as well as PCA/ZCA whitening.

## Strengths

* The paper tackles a conceptually relevant question: whether and how intra-class covariance should influence the SVM decision boundary when the data metric is not Euclidean.
* The vector-space transformation interpretation (statistical → Euclidean via Cholesky) provides a clear geometric picture that connects Mahalanobis distance to whitening.
* The experiments span multiple domains (healthcare, astronomy, quality, safety), and the reported metrics (accuracy, precision, recall, F1, AUC) give a reasonably comprehensive view of performance.

## Weaknesses

### Fatal

1. **Disconnect between theoretical derivation and the algorithm used in experiments.** The theoretical derivation (Lemma 2.2, equations 8–13) yields two separate classifiers in input space (one per class). The SM algorithm, however, starts with a **single** linear SVM on the original training data and then merely adjusts the intercept to obtain the margin ratio. The derivation does not actually motivate the algorithm. The paper never explains how two class-specific classifiers would be combined for prediction, and the algorithm does not reflect the derived optimization problems.

2. **Unfair experimental comparison (self-training vs. no self-training).** The SM algorithm is an iterative self-training procedure that adds test data (labeled by the current classifier) back into the training set to recompute covariances and retrain. Standard SVM, PCA/ZCA whitening, and kernel SVMs are evaluated without any self-training. The observed performance gains could be entirely due to this semi‑supervised bootstrap, not to covariance adjustment. The paper provides no control experiment (e.g., self-training with a standard linear SVM) to isolate the effect.

3. **No statistical rigor.** All results are reported from a single 80/20 train‑test split (no cross‑validation, no multiple runs, no error bars or confidence intervals). Given the modest performance margins (e.g., +0.018 accuracy on Breast Cancer, +0.002 on Pulsar), significance cannot be assessed. The claim of “marked improvement” is not supported.

### Major

4. **Fundamental misunderstanding of KKT conditions in modified optimization.** The paper states that “KKT boundary conditions are not valid in the input space” because the margin now depends on all data points through the covariance (Lemma 2.3). This is incorrect: changing the objective function does **not** invalidate KKT conditions; it simply changes the specific Lagrangian and complementary slackness. The paper provides no rigorous argument for invalidation.

5. **Vague and heuristic SM algorithm.** The convergence criterion (“changes in test data labels are below a certain threshold”) is not quantified. No analysis of convergence, runtime, or sensitivity to initial conditions is provided. The algorithm risks propagating errors, especially if the initial linear SVM is poor.

6. **Lack of crucial experimental detail.** It is unclear whether the reported CSVM results were obtained using the full SM algorithm (iterating over test data) or a one‑shot transformation with training‑data covariance. The regularization parameter *C*, kernel hyperparameters for RBF/sigmoid/polynomial, and the soft‑margin vs. hard‑margin choice are not specified. This severely undermines reproducibility.

### Minor

* The paper claims to address “gaps” in prior variance‑adjusted SVM work (e.g., Zafeiriou et al., Huang et al.) but provides no concrete comparison – neither theoretical nor experimental – to those methods.
* Several equations contain minor inconsistencies or missing parentheses (e.g., equation 14 could be more clearly written), and the text sometimes switches between “SVC” and “SVM” without distinction.

### Trivial

* None beyond the formatting issues already noted.

## Nice‑to‑Haves

* A controlled experiment comparing standard SVM + self‑training vs. CSVM (with and without self‑training) would disentangle the effect of covariance adjustment.
* Statistical significance tests (e.g., McNemar’s test or bootstrap confidence intervals) should be added to all performance comparisons.
* The mathematical derivation could be clarified by showing how the two class‑specific classifiers are reconciled into a single decision rule.

## Novel Insights

None beyond the paper’s own contributions. The idea that class‑conditional whitening changes the margin ratio is already implicit in existing minimum‑class‑variance SVM and Mahalanobis‑kernel methods; the paper’s vector‑space framing is a different perspective but does not yield an algorithm that is clearly superior or theoretically sound.

## Suggestions

1. **Re‑run experiments with proper controls.** Include a “standard linear SVM + self‑training” baseline. Use cross‑validation or repeated random splits with reported means and standard deviations.
2. **Align the algorithm with the theoretical derivation.** If two class‑specific hyperplanes are derived, explain how they are used to label test data, or revise the theory to match the single‑classifier algorithm.
3. **Provide convergence guarantees or at least empirical analysis** for the SM algorithm (e.g., number of iterations needed, effect of the threshold on final accuracy).
4. **Compare directly against prior variance‑adjusted SVM methods** (e.g., MCVSVM, Mahalanobis TSVM) to demonstrate superiority.

## Score and Decision

**Score:** 3.0

**Decision:** Reject

The paper presents an interesting conceptual idea, but the theoretical derivation does not support the implemented algorithm, the experimental comparison is confounded by self‑training, and the results lack statistical rigor. These fatal and major weaknesses prevent the paper from making a reliable contribution.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>