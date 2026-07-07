## Summary

This paper proposes Covariance-Adjusted SVM (CSVM), a method that incorporates class-specific covariance information into SVM via Cholesky whitening. The authors argue that standard SVM's Euclidean-distance-based margin ignores class-conditional covariance structure, and they derive a modified optimization problem where the margin becomes a function of intra-class covariances. An iterative algorithm (the SM algorithm) is proposed to estimate population covariances without test labels. Experiments on five datasets compare CSVM against standard SVM kernels and PCA/ZCA whitening.

## Strengths

- **The core idea is well-motivated.** The observation that standard SVM's maximum-margin framework ignores class-specific covariance structure is valid, and incorporating covariance information via Cholesky whitening is a natural approach. The algebraic derivation in Section 2 (Eqs. 1-14) is internally coherent.

- **The SM algorithm targets a real practical bottleneck.** Population covariance is unknown for test data, and the iterative self-training approach is a creative (if problematic in its current form) attempt to estimate it.

## Weaknesses

### Fatal

None.

### Major

- **The evaluation conflates supervised and semi-supervised learning, invalidating the experimental comparison.** The SM algorithm (Section 3, steps f–h) iteratively: labels test data using the current classifier, adds the predicted test labels to the training set, recomputes covariance matrices, and retrains. This is a self-training / semi-supervised procedure. The paper never uses the term "semi-supervised," does not compare against semi-supervised SVM methods (e.g., TSVM, S3VM), and does not analyze the risk of confirmation bias. If the reported results (Tables 1-4) use the SM algorithm, the comparison against supervised-only baselines (linear SVM, RBF SVM, etc.) is invalid because CSVM has seen test data during training while the baselines have not. If the results use only training-set covariances without the SM algorithm, then the SM algorithm is never actually tested. The paper is ambiguous on this point. In either case, the evaluation as presented does not support the claimed contribution. **This is the most serious issue.**

- **No comparison against the most relevant prior work.** The paper cites MCVSVM (Zafeiriou et al., 2007), MD-TSVM (Peng & Xu, 2012), the maxi-min margin machine (Huang et al., 2004), and weighted Mahalanobis kernels (Wang et al., 2007) — all covariance-aware SVM variants sharing the same motivation. None appear in the experimental comparison. Without this, the reader cannot assess whether CSVM improves over existing covariance-aware methods, which is the core claim.

- **No uncertainty quantification and marginal improvements.** All results (Tables 1-4) are point estimates from a single 80-20 split, with no standard deviations, confidence intervals, or significance tests. The margins are small (e.g., Pulsar accuracy 0.981 vs 0.979; Diabetes AUC 0.74 vs 0.74; OSHA — CSVM is never best on any metric). The abstract's claim of "marked improvement" is unsupported by the evidence presented.

- **The "two classifiers" claim (Lemma 2.2) is not operationalized.** The paper derives two separate optimization problems (Eqs. 10-13) and asserts that a binary problem yields two classifiers in the input space. However, the SM algorithm produces a single classifier (steps d-e), and the paper never explains how two hypothetical classifiers are reconciled into a single decision rule for a test point whose label is unknown. This is a gap between the theoretical claim and the actual method.

- **The SM algorithm's logic is confusing.** Step (c) runs SVM in Euclidean space to get θ, then step (d) runs a separate linear SVM in the input space to get θ_input and θ₀, then step (e) adjusts θ₀. It is unclear why the Euclidean-space SVM (which uses the whitened, correctly-transformed data) does not directly give the final classifier, and why a separate input-space SVM is needed.

### Minor

- **The "non-Euclidean space" framing is overstated.** The input space is ℝⁿ; the Mahalanobis distance corresponds to a different inner product ⟨x,y⟩ = xᵀΣ⁻¹y, which still yields a Euclidean inner product space. The claim that KKT conditions "are not valid in the input space" (Lemma 2.3) conflates the appropriateness of a particular distance metric with the validity of the optimization framework. The practical method (whitening + SVM) is standard linear algebra; the geometric framing does not add substance and risks misleading readers.

- **Dataset characteristics (sample size, number of features, class imbalance) are not reported.** Without these, readers cannot assess whether the datasets pose the kind of problem (class-specific covariance differences) that the method is designed to exploit.

- **Hyperparameters for kernel SVMs (RBF γ, polynomial degree, C values) are not specified.** The reader cannot verify whether the baselines were reasonably tuned.

- **The gap between population covariance Σ (theory) and sample covariance S (algorithm) is not discussed.** When the training sample is small relative to the number of features, the sample covariance estimate degrades. This limitation is neither analyzed nor tested.

### Trivial

None.

## Nice-to-Haves

- Clarify unequivocally whether the SM algorithm was used to produce the reported results.
- Report results with standard deviations over multiple train-test splits (e.g., 5-fold or 10-fold cross-validation).
- Compare against MCVSVM, MD-TSVM, and other covariance-aware SVMs cited in the paper.
- Add convergence analysis for the SM algorithm (iteration count, initialization sensitivity, degeneracy risk).

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Harsh critic's point about Step (d) "Why train an input-space SVM at all?"** — This is a reasonable observation about algorithm design but is subsumed by the stronger "two classifiers not operationalized" criticism above.
- **Harsh critic's point about "dimensional inconsistencies" critique of prior work being unsubstantiated (Section 1)** — While true that the paper does not name specific prior papers with errors, the reviewer positioned this as a minor section note rather than a core weakness.
- **Harsh critic's point about lack of ROC curves** — The paper does include ROC AUC values, and the plots are embedded images in the PDF. The AUC values are reported in the tables. This criticism is not factually wrong but is less significant than the other issues.
- **Several generic "strengths" from the input** (e.g., "the problem is important," "the core instinct is right") — dropped because they are too generic or conflict with verified weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Acknowledge the semi-supervised nature of the SM algorithm** and compare against proper semi-supervised baselines (TSVM, S3VM, self-training SVM). This single change would resolve the most serious evaluation flaw.
- **Drop or significantly soften the "non-Euclidean space" framing.** Present the method as: class-specific Cholesky whitening as preprocessing, followed by linear SVM in the whitened space. The contribution is a practical preprocessing technique, not a geometric insight.
- **Add error bars, cross-validation, and most critically, comparisons against existing covariance-aware SVMs** (MCVSVM, MD-TSVM, etc.). These are the methods CSVM should outperform to justify its contribution.

## Score and Decision

**Round 1 bracket:** 1.5 – 3.0.

**Anchors consulted:**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| Sparse Covariance Neural Networks (ZDoaLbOFaP) | 3.00 | R1 | Yes | Better theoretical grounding and clearer evaluation; scored 3 despite incremental novelty concerns. Our paper has more fundamental evaluation issues. |
| Bridging PCA and Neural Networks (qcyn7ESaM8) | 2.50 | R1 | Yes | Similar severity of weaknesses (clarity, unfocused experiments) but does not have an evaluation contamination issue. |
| Neural Bounds on Bayes Error (Hh0Cg4epYY) | 2.33 | R1 | Yes | Described as incomplete/insufficiently detailed; comparable tier. |
| Covariance+Hessian Eigenanalysis (anek0q7QPL) | 5.00 | R1 | Yes | Much stronger empirical methodology and clearer framing; not comparable. |
| Language Models + Mahalanobis Distance (ClixrtIHUJ) | 5.25 | R1 | Yes | Strong empirical results and clear evaluation; not comparable. |

**Weighted-item comparison:** The paper's heaviest negative item (−9.71, semi-supervised contamination) and second-heaviest (−8.23, missing baselines) are comparable in magnitude to the heaviest negatives in the score-2.5–3.0 anchors (e.g., Bridging PCA's −10.23 and −10.52, Sparse CovNN's −8.17 and −7.64). However, the Bridging PCA and Sparse CovNN papers compensate with positive weights in the +4–+5 range, while this paper's positives are modest (+3.32, +2.42). Combined with the evaluation contamination issue — which is more fundamental than presentation or novelty concerns — the paper sits below the 2.5–3.0 anchors.

**Final calibration:** The paper has a salvageable core idea (class-specific whitening + SVM) and coherent algebra, but the evaluation is compromised by the semi-supervised contamination issue, and the paper omits its most relevant baselines. These are fixable in principle, but in the current form the evidence does not support the claimed contribution. This places the paper in a clear reject range, around 2.0.

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>