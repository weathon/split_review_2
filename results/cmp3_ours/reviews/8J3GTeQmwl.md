## Summary

This paper proposes a cross-validation method for graphon model selection that avoids the computational cost of matrix-completion-based approaches. The core idea is to replace held-out edges in each CV fold with i.i.d. Bernoulli(θ) draws, creating a training distribution that undergoes a known affine shift (Eq. 5) that can be inverted (Eq. 6) to recover an unbiased predictor. The method is model-agnostic (works with NS, SAS, USVT, ICE estimators), supported by an asymptotic theory (Theorem 1) showing the CV score is parallel to the true loss, and is computationally more efficient than the competing ECV method. Experiments on synthetic and real networks validate the approach.

## Strengths

1. **Clever and principled core idea.** The random Bernoulli imputation scheme with affine correction (Section 3, Lemma 1, Eqs. 5–6) is a genuinely creative way to handle the bias introduced by edge splitting in network CV. The observation that the training distribution undergoes a known affine shift that can be analytically inverted avoids expensive matrix completion while remaining theoretically clean. The O(n²) per-fold cost vs. O(n³) for matrix-completion-based methods is a substantial practical advantage.

2. **Appropriate asymptotic justification.** Theorem 1 establishes that the CV-imputation score is asymptotically parallel to the true loss L(M) up to a model-independent constant Λ, which is exactly the property needed to justify model selection via CV. The proof structure is coherent with the method's design.

3. **Model-agnostic and broadly applicable.** The method works directly with any graphon estimator (NS, SAS, USVT, ICE) without modification, and the experiments cover four distinct estimation methods across four graphon types (low-rank, full-rank, dense, sparse). The computational advantage over ECV is substantial and well-documented (Table 2: 56.9s vs. 258.7s for PolBlog; 240.9s vs. 6021.1s for Yeast).

## Weaknesses

### Major

1. **ECV is tested on problems that violate its stated assumptions.** The paper explicitly notes (lines 27, 119) that ECV requires P to be low-rank, yet applies it to Graphon 2, which is described as full-rank. The resulting performance gap on Graphon 2 (e.g., CV-imputation MSE 2.13 vs. ECV 3.82 for NS) may partly reflect this assumption violation rather than genuine superiority of the proposed method. The paper should either restrict ECV comparisons to settings where its assumptions hold, or clearly acknowledge this mismatch and discuss how much of the gap is attributable to it.

2. **The 100% method-selection accuracy claim (n=200) is stated without uncertainty quantification.** The paper claims (line 181) that at n=200, "our method achieves a 100% accuracy rate in selecting the best candidate model" across 100 replications. Over four graphons with multiple estimators, this means the method never once selected a suboptimal model—a result that is suspiciously perfect. No confidence intervals, selection margins, or analysis of how close runner-up models were is provided. This claim should either be supported with more detailed analysis or presented more cautiously.

### Minor

3. **Key tuning parameters (θ and K) are not stated in the main text.** The Bernoulli imputation mean θ is referenced as a tuning parameter (line 63) and deferred to Section S.4 in the appendix. The number of folds K is never numerically specified anywhere in the main text. Experimental results cannot be reproduced from the main text alone without these values. The paper should state K explicitly and include a sensitivity analysis for θ or provide a principled default.

4. **Unexplained anomalies in the ECV comparison table.** Table 1 contains patterns that warrant discussion: (a) ECV with NS on Graphon 1 has mean 9.15 and SD 19.25—the standard deviation more than doubles the mean, suggesting catastrophic failures on some replicates that are not acknowledged; (b) ECV with USVT produces results numerically identical to Default USVT on three of four graphons (0.60, 5.06, 1.18), implying ECV provides no useful tuning for USVT in those settings.

5. **CV-imputation can select models that are worse than default tuning.** For Graphon 3 with the NS estimator, Default NS (M=1) achieves MSE 0.74 ± 0.04 while CV-imputation achieves 0.79 ± 0.07. The paper's text correctly notes that CV-imputation beats ECV (which is true: 0.79 vs. 3.07), but does not discuss cases where tuning via CV-imputation hurts relative to an untuned default. Acknowledging when and why tuning can fail would strengthen the paper's credibility.

6. **Condition 1 (polynomial decay of optimism bias) is not grounded in the experimental settings.** The paper asserts (line 115) that Q_K(M) "can be verified computationally" and points to an appendix figure. However, the only concrete example given (Erdős–Rényi with simple averaging, α=1) is a special case. For the actual graphon models and estimators used in the experiments, there is no empirical or theoretical guarantee that Condition 1 holds or that α>0. While this gap is common in CV theory (many methods have assumptions that are not fully verified in practice), it should be acknowledged rather than minimized.

### Trivial

None.

## Nice-to-Haves

- A sensitivity analysis for θ over a reasonable range (e.g., {0.1, 0.25, 0.5, 0.75}) would demonstrate robustness of the method to this choice.
- A comparison of CV-imputation's selected M against the MSE-oracle's selected M would directly measure how close the method comes to the ideal, complementing the existing comparisons against ECV and defaults.
- The drug repurposing observation (ledipasvir for COVID-19, line 231) is appropriately framed as a suggestion supported by clinical literature, but it would be helpful to clarify that the CV method identifies a candidate link for further investigation rather than making a discovery claim.

## Removed Points

- Figure 3 caption contradiction ("In all cases, ECV is faster than CV-imputation" vs. body text saying the opposite). Removed because it is almost certainly a parser artifact—the body text (line 173) and Table 2 consistently show CV-imputation being substantially faster.
- Missing specification of θ in the main text was partially addressed: the paper states θ is discussed in Section S.4 (appendix), which was stripped by the parser. The core concern about K is retained since it is never numerically specified.
- The claim about bolded entries in Table 1 being misleading: removed because all CV-imputation rows are bolded consistently—this is a formatting choice to highlight the proposed method's results, not a claim of numerical superiority over defaults. The underlying concern about CV-imputation being sometimes worse than default is retained as Weakness #5.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. State the values of θ and K explicitly for all experiments in the main text, and include a brief sensitivity analysis for θ over a reasonable range.
2. Acknowledge the ECV assumption mismatch for full-rank Graphon 2, and either exclude those results from the primary comparison or clearly discuss how much of the gap reflects this mismatch.
3. Provide confidence intervals or selection-margin analysis for the 100% accuracy claim at n=200, or present it more cautiously.
4. Discuss the Table 1 anomalies (high ECV variance for NS on Graphon 1; ECV(USVT) matching defaults) in the text.
5. Add a brief discussion of cases where CV-imputation does not improve over default tuning, explaining when tuning helps and when it does not.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>