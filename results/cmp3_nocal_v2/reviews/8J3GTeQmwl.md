## Summary

This paper proposes CV-imputation, a cross-validation procedure for graphon models that replaces held-out edges with Bernoulli(θ) draws and applies an affine correction to debias the resulting estimate. The method avoids the O(n³) matrix-completion overhead of prior edge-CV (ECV) approaches, replacing it with O(n²) Bernoulli imputation per fold. The authors provide asymptotic theory showing the CV score is parallel to the true MSE up to a constant-free term, and evaluate the method on four graphon types, four estimation methods, and three real networks.

## Strengths

1. **Clean and clever methodological core.** The idea of replacing held-out edges with Bernoulli(θ) draws and correcting via the affine relationship in Eq. 5–6 is elegant and well-motivated. Lemma 1 correctly identifies the distribution of the imputed training entries, and the connection between the imputed matrix's expectation and the true P is clearly stated.

2. **Genuine computational advantage.** The complexity analysis (Section 3) correctly identifies that ECV's per-fold SVD (O(n³)) is replaced by O(n²) Bernoulli imputation. Table 2 validates this with real-world speedups of 4.5×–24.9× (e.g., Yeast: 241s vs. 6,021s). This is a meaningful engineering contribution.

3. **Theoretical result targets the right quantity.** Theorem 1 shows the CV score V_K(M) is asymptotically parallel to L(M)+Λ where Λ is M-independent, establishing that minimizing V_K(M) is asymptotically equivalent to minimizing the true MSE. The use of Condition 1 (bounded optimism bias at rate K^{-α}) is honestly stated as a required assumption.

4. **Broad experimental scope.** The evaluation covers four graphon types (dense/sparse, low-rank/full-rank), four estimation methods (NS, SAS, USVT, ICE), three real networks, and a COVID-19 drug repurposing case study. Figure 4's convergence plots provide empirical support for the asymptotic parallelism predicted by Theorem 1.

## Weaknesses

### Fatal
None.

### Major

1. **Theory–experiment gap: Condition 1 is not established for any evaluated estimator.** Theorem 1's guarantees are conditional on Condition 1 (Q_K(M) = O_p(K^{-α})), but the paper does not show this condition holds for NS, SAS, USVT, or ICE — the four estimators used in all experiments. The paper claims Q_K(M) "can be verified computationally" (line 115) and references Appendix Figure S.3, but provides no summary or evidence in the main text. The single worked example (Erdős–Rényi with a simple averaging estimator, α=1) does not transfer to the complex non-linear estimators evaluated. This means the theoretical guarantees in Theorem 1 are not connected to the experiments as presented. **Why it matters:** A reader cannot tell whether the good empirical performance is explained by the theory or is coincidental. The paper would be substantially strengthened by either deriving α for at least one realistic estimator or presenting empirical verification of Condition 1's decay in the main paper.

2. **The affine correction (Eq. 6) is motivated by a linear relationship in expectation (Eq. 5) but is applied to non-linear estimators without explicit justification.** The paper presents Eq. 6 as an implication of Eq. 5, which is exact for the *expectation* P^{[-k]}. However, when a non-linear estimator P̂(M|A^{[-k]}) is substituted, there is no guarantee that applying the inverse affine transformation yields an unbiased or well-calibrated estimate of P. The theory sidesteps this via Condition 1 (which quantifies the gap between full-sample and split-sample estimates), but the paper never explicitly states that Eq. 6 is only a heuristic motivation for non-linear estimators and that the actual theoretical justification rests entirely on Condition 1. **Why it matters:** This creates confusion about what the method actually requires from the estimator. A reader might incorrectly assume the correction is exact.

### Minor

3. **Figure 3 caption contradicts the paper's central computational claim.** Lines 185 and 187 state "In all cases, ECV is faster than CV-imputation," while the main text (line 173), the complexity analysis, Table 2, and Figure 5 all claim the opposite. This is clearly a caption error — the overwhelming numerical evidence supports CV-imputation being faster — but a figure caption that directly contradicts the surrounding text is a blocking error for a reviewer trying to interpret the figure. The authors must correct this.

4. **The free parameter θ is incompletely specified in the main text.** Line 63 states θ "serves as a tuning parameter" and defers its selection to Section S.4 in the appendix. What value of θ was used in the synthetic and real experiments, how it was chosen, and how sensitive results are to its choice are all absent from the main paper. While deferred parameter details are common, θ directly affects the distribution of the training matrix A^{[-k]} and is central to the method's behavior. A reader without access to the appendix cannot fully evaluate the experiments.

5. **The conclusion overstates by claiming "lack of tuning requirements" (line 260) while θ is itself a tuning parameter (line 63).** This is a minor internal contradiction in the paper's framing.

6. **The COVID-19 ledipasvir repurposing claim overstates the CV method's role.** The paper states "Our findings suggest a potential repurposing of ledipasvir to treat COVID-19" (line 231). However, the CV method only *selects the tuning parameter* — the specific link prediction that surfaces ledipasvir is a function of the graphon estimator, not the CV scheme. This attribution should be dialed back to avoid overclaiming.

### Trivial
None.

## Nice-to-Haves

- Statistical significance testing or effect-size discussion for the Table 1 MSE comparisons, especially for cases where differences are modest (e.g., SAS on Graphon 1: 1.69 vs. 1.72).
- A brief discussion of whether the K→∞ asymptotic regime in Theorem 1 is meaningful for typical choices of K=5 or K=10.
- Sensitivity analysis for θ in the main paper (even a brief sentence on whether results are robust to its choice).

## Removed Points

- **"Missing comparison to node-based CV or AIC/BIC baselines":** Node-based CV is correctly identified in the Introduction as flawed due to independence violations; comparing against a known flawed baseline is not essential. AIC/BIC are not standard criteria for nonparametric graphon model selection and are outside the paper's scope.
- **"Accuracy metric in Figure 5 needs clarification":** Line 203 explicitly defines it as "the percentage of cases where the model with the smallest mean squared error (MSE) is selected from the top-tuned estimators." This is sufficiently clear.
- **"Figure 3 contradiction is a disqualifying error":** While the caption error is real, classifying it as fatal is overblown given that Table 2, Figure 5, the complexity analysis, and the main text all consistently point in one direction. The error is clearly in the caption text, not the data. Demoted to Minor.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the theory–experiment gap (Condition 1 unverified for real estimators) but do not produce a novel observation about the method or its domain beyond what the authors themselves discuss.

## Suggestions

1. **Fix the Figure 3 caption** — it currently says the opposite of what the data show.
2. **In the main paper, either (a) verify Condition 1 empirically** for at least one of the tested estimators (e.g., show Q_K(M) decaying as K increases on synthetic data), or **(b) explicitly state** that the theoretical results are conditional and that the method's practical success is supported by the convergence evidence in Figure 4 rather than by a verified Condition 1.
3. **State the θ value used in all experiments** in the main text (not just the appendix) and add a brief note on sensitivity.
4. **Acknowledge the linearity gap:** add a sentence clarifying that Eq. 6 is motivated by the linear relationship in expectation but the formal theory relies on Condition 1 rather than linearity.
5. **Tone down** the "lack of tuning requirements" claim and the ledipasvir attribution.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>