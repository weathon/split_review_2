## Summary

This paper proposes a robust evaluation framework for heterogeneous treatment effect (HTE) estimators using relative error. The key theoretical contribution is relaxing the requirement in Gao (2025) that both propensity score and outcome regression models be consistent — the proposed method only requires propensity score consistency, relieving reliance on outcome model extrapolation which is prone to misspecification. The authors derive conditions for robust relative error estimation, design novel loss functions (weighted least squares + balance regularizers) embedded in a Dragonnet-style neural network, provide asymptotic guarantees, and extend the framework to a new HTE learning method via pair-wise aggregation.

## Strengths

1. **Well-motivated theoretical target.** The paper correctly identifies and formalizes a genuine limitation in Gao (2025): Condition 2 requires both propensity score and outcome models to be consistent (as a product). Since outcome models rely on cross-group extrapolation that is often inaccurate, relaxing this requirement is both well-motivated and practically relevant. The paper's framing of this issue (Section 3) is clear and persuasive.

2. **The core theoretical derivation is crisp.** The Taylor expansion in Section 4.1, deriving the conditions (Eq. 4) under which first-order nuisance estimation error terms vanish, is the paper's cleanest contribution. The logical chain — Taylor expansion → score conditions → weighted least squares loss design — is coherent, and the insight that a carefully weighted loss can make first-order terms vanish even with misspecified outcome models is genuinely clever.

3. **Informative ablation study.** Table 5 cleanly separates the contributions of the three loss terms. Removing L\_const causes a large degradation in both HTE accuracy and relative error selection accuracy; removing L\_ce causes a moderate decline. This supports the paper's central claim that the balance constraints (L\_const) are a key innovation.

4. **Strong empirical validation of the evaluation framework.** Figures 1–2 and Table 2 provide compelling evidence that the proposed method achieves near-nominal coverage while maintaining high selection accuracy across multiple estimator pairs on IHDP and Twins. This is the paper's strongest empirical contribution.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Ambiguity about the neural network training protocol for the HTE estimator (Table 1).** The paper states that candidate HTE estimators are "trained on a training set" and the test set is used for evaluation (Section 2.1, line 48; Section 6.1). However, it does not explicitly state what data the proposed neural network is trained on when producing the "Ours" results in Table 1. The neural network's loss function (L\_wls + λ₁L\_ce + λ₂L\_const) depends on observed outcomes Y\_i and candidate estimator predictions, all of which are available on both training and test splits. This needs clarification: if the neural network is trained on the test set while baselines are trained only on the training set, the comparison is not apples-to-apples. If it is trained on the training set (the more natural reading), this should be stated explicitly. The in-sample vs. out-of-sample breakdown in Table 1 partially mitigates this concern (since an advantage from test-set training would appear only in in-sample metrics), but explicit clarification is necessary.

2. **Missing evidence for the claimed high variance of baseline relative-error estimators.** In the "Comparison with Gao's Method" (Section 6.2, Table 2), the paper states that linear regression and boosting nuisance estimators yield "variance so large that the confidence intervals frequently include zero." This claim is central to the motivation for the proposed method's advantage in selection accuracy, yet no evidence is provided — no confidence interval widths, no standard errors of δ̂, and no variance estimates. Reporting the average CI width or standard error for each method would substantiate this claim. *(Note: the reviewer's criticism that this "does not implement Gao's method" is not valid — the paper is transparent about using standard nuisance estimators in the relative error formula. The concern is only about missing variance evidence.)*

3. **Sensitivity analysis for propensity score tests noise rather than model misspecification.** Table 6 adds Gaussian noise to the true propensity score in simulated data. While this tests robustness to random perturbations, it does not test sensitivity to systematic model misspecification (e.g., logistic form when the true propensity is nonlinear in a different way). Since Theorem 1 assumes correct propensity score specification, understanding sensitivity to actual misspecification (not just noise) would strengthen the paper.

4. **Convergence rate assumptions for neural network estimators with non-standard losses.** Theorem 1 requires that γ̂, β̂₀, β̂₁ converge to their probability limits faster than n^{-1/4}. The paper argues this is mild, citing Chernozhukov et al. (2018). However, the neural network is trained with a non-standard loss (weighted least squares + balance constraints + cross-entropy), and the asymptotic behavior of neural network estimators under such composite losses is not fully covered by standard M-estimation theory. A brief discussion of this gap would improve the paper's rigor.

5. **O(K²) computational scaling of the HTE estimator.** As shown in Table 3, the runtime grows super-linearly with the number of candidate estimators (12.24s for K=5 vs 2.03s for TARNet). The paper notes this and suggests random subsampling of pairs, but provides no analysis or guidance for this strategy. This limits practical applicability when K is large.

### Trivial

- The ablation study (Table 5) describes the variant (L\_wls & L\_ce) as "a method of (Gao, 2025)" — but L\_wls is a novel contribution of this paper, not part of Gao (2025). This characterization is slightly misleading, though it does not affect the ablation's conclusions.

## Nice-to-Haves

- **Add an ensemble-of-baselines comparison for the HTE learning method.** The proposed estimator averages over all pairs of candidate estimators (Section 5). A natural baseline is a simple average of the candidate estimators' predictions (a standard ensemble). Without this, the paper's claim that the aggregation "surpasses the performance of any single candidate estimator" is only partially tested — it shows superiority over individuals but not over a simple ensemble.

- **Report CI widths or variance estimates for the baselines in Table 2** to substantiate the claim about high variance causing low selection accuracy.

## Removed Points

- *"The comparison with Gao (2025) does not actually implement Gao's method."* — Removed because the paper is transparent about what it does ("follow their choice of nuisance estimators"), and the reviewer's concern is based on an expectation not stated in the paper.
- *"Condition 2 characterization slightly overstates restrictiveness."* — Removed because the paper's statement that both estimators must be consistent is correct (if either is inconsistent, the product cannot be o_p(n^{-1/2})).
- *"Jobs dataset results deferred to appendix."* — Removed because it is a space constraint, and the paper acknowledges this.
- *"Missing sensitivity analysis for ρ and λ₁ in main text."* — Removed because the paper states these are in Appendix F.8 (parser-stripped content).
- *"The HTE estimator connection to the evaluation framework is undertheorized."* — Removed because Section 5 provides a concrete technical description of how the framework is extended; the reviewer's concern is subjective and the connection is sufficiently explained.
- *"Over-constrained system concern."* — Removed because the paper explicitly acknowledges this and describes the soft-relaxation solution.

## Novel Insights

The reviews surface a useful perspective: the paper's two contributions (evaluation framework and HTE learning) serve different purposes and operate under different experimental controls. The evaluation framework is the more rigorous contribution, validated through coverage and selection accuracy metrics against meaningful comparisons. The HTE learning extension is empirically promising but would benefit from tighter experimental design (especially clarifying training protocol and adding an ensemble baseline). The risk of conflating the two contributions — where ambiguity in the HTE learning experiment could cast doubt on the evaluation framework — is worth the authors' attention.

## Suggestions

1. Explicitly state the training protocol for the neural network in the HTE estimation experiments (Table 1): what data split is used, and whether the same network is used for both relative error evaluation and HTE estimation.
2. Add average confidence interval widths (or standard errors of δ̂) for the baselines in Table 2 to substantiate the variance claim.
3. Add a simple ensemble baseline (average of candidate estimator predictions) to the HTE learning comparison.
4. Include a sensitivity analysis for propensity score *model misspecification* (e.g., misspecified functional form) in addition to the noise-based analysis in Table 6.
5. Acknowledge the gap between standard M-estimation theory and the non-standard neural network loss used in the paper.

## Score and Decision

**Summary assessment:** The paper makes a genuine theoretical contribution to HTE evaluation — the derivation of conditions for robust relative error estimation that relax outcome model consistency requirements is well-structured and the empirical validation of the evaluation framework (coverage, selection accuracy) is convincing. The concerns identified (experimental protocol ambiguity, missing variance evidence, sensitivity analysis scope) are addressable and do not undermine the core contribution. The HTE learning extension is more preliminary but does not detract from the main contribution. On balance, the paper warrants acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>