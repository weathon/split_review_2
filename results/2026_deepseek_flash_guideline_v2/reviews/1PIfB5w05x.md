Now I have all the verification I need. Let me compose the final consolidated review.

## Summary

This paper studies sparse recovery when observations come from mixed-quality sources (different noise variances). It establishes sufficient conditions for information-theoretic support recovery in both agnostic and informed settings, and proves a LASSO phase transition for the agnostic setting. The conceptual centerpiece is the "Price of Quality" γ — the exchange rate between high- and low-quality samples. Key findings: γ ≤ 2 in the agnostic setting, γ can be unbounded in the informed setting, and the LASSO threshold depends only on average noise (so high- and low-quality data contribute equally to algorithmic recovery).

## Strengths

- **Clean, interpretable Price of Quality framework (γ, Eq. 5/12/18):** The paper distills a complex multi-source trade-off into a single scalar. Characterizing γ across three SNR regimes yields concrete, intuitive predictions (γ < 2 in agnostic setting, γ → ∞ in informed setting). This directly addresses a practical need in settings like LLM-assisted labeling and citizen science.

- **Surprising LASSO robustness result (Theorem 3):** Proving that the LASSO recovery threshold n_ALG = 2s log(p-s) + s + 1 depends only on total sample size n = n₁+n₂ — and is *independent* of individual noise levels — is non-trivial and conceptually striking. This reveals a qualitative gap between information-theoretic and computational recovery under data heterogeneity.

- **Genuine technical extension of Wainwright (2009):** The LASSO proof overcomes a genuine obstacle: Σ is no longer a scalar multiple of identity, so classical inverse-Wishart arguments fail. The resolution via QR decomposition and Haar-measure properties (Section 4, Appendix D) is a substantive technical contribution.

- **Honest limitations discussion (Remark 3.2):** The paper explicitly acknowledges that Theorem 1's condition is not tight, identifies the source of looseness (relaxed Chernoff bound → cubic equation), and discusses alternative estimators. This transparency strengthens credibility.

- **Generalization to arbitrary noise structures (Remark 3.4):** Eqs. 22-23 extend results beyond the two-source model to any invertible Σ, showing the core results are not artifacts of the binary-quality setup.

## Weaknesses

### Fatal
None.

### Major

1. **Mathematical inconsistency in the Price of Quality expression and its low-SNR analysis.** The sufficient condition (9) has coefficient log(1 + δ(2σ₂² − σ₁²)s/(2σ₂²)) for n₁, implying γ = log(1 + δ(2σ₂² − σ₁²)s/(2σ₂²)) / log(1 + δs/(2σ₂²)). However, Eq. (12) writes the numerator as log(1 + δ(2σ₂² − σ₁²)s/(2σ₁⁴)) — with 2σ₁⁴ replacing 2σ₂². Moreover, the first-order simplification in the low-SNR₂ analysis (Eq. 14) claims that with 2σ₁⁴ in the denominator, γ ≃ 2 − σ₁²/σ₂². Direct algebra shows that (δ(2σ₂²−σ₁²)s/(2σ₁⁴)) / (δs/(2σ₂²)) = (2σ₂²−σ₁²)σ₂²/σ₁⁴, which simplifies to 2 − σ₁²/σ₂² *only* when σ₁² = σ₂² (a contradiction). Since γ and the bound γ < 2 are central claimed contributions, this needs clarification. **If the error is in the paper rather than a parser artifact, it undermines the quantitative claim that γ ≤ 2 in the low-SNR regime.** The authors should confirm the correct expression and either correct the derivation or explain the intended analysis.

### Minor

2. **Quantitative γ claims are properties of a loose sufficient condition.** The headline "one high-quality sample is never worth more than two low-quality samples" (abstract, intro, conclusion) is derived from a relaxed Chernoff bound that the paper itself acknowledges is not tight (Remark 3.2). While the paper qualifies these statements ("under our sufficient condition"), the prominence of the numerical claim — especially "never worth more than two" — risks readers taking it as a fundamental information-theoretic bound rather than an artifact of a particular proof technique. A tighter analysis or matching lower bound could yield a very different exchange rate.

3. **No lower bounds for information-theoretic recovery.** The homogeneous-noise setting has sharp necessary-and-sufficient thresholds, but here only sufficient conditions are provided. Without impossibility results, the paper cannot distinguish which aspects of the Price of Quality are fundamental and which are proof-induced. The paper acknowledges this, but it remains a limitation that weakens the strength of the claims.

4. **No algorithmic result for the informed setting.** Remark 4.2 explains why the LASSO proof does not extend, but this leaves half the problem space (informed + algorithmic) unaddressed. The paper's practical recommendation ("quantify uncertainty and rescale") would be strengthened by knowing whether a rescaled LASSO achieves a better threshold in the informed setting.

5. **No simulations or finite-sample illustrations.** The paper is purely theoretical. While acceptable for a theory paper, synthetic experiments would help gauge the looseness of the sufficient conditions and connect the abstract analysis to the claimed applications (LLM labeling, citizen science, medical imaging).

### Trivial

6. **Ambiguous SNR₁/SNR₂ definition (line 129).** The notation E[‖y_i − x_i^T β^*‖₂²]_{i=1}^{n₁} in the numerator would naturally be read as the expected sum of squared residuals (= n₁σ₁²), not the intended signal energy (= n₁s). The final result s/σ₁² is correct, but the intermediate notation is sloppy.

## Nice-to-Haves

- Tighten the agnostic sufficient condition by solving the cubic Chernoff equation mentioned in Remark 3.2, even numerically or asymptotically.
- Provide a matching impossibility (lower bound) for the information-theoretic threshold.
- Validate the Price of Quality with finite-sample simulations.
- Extend the LASSO analysis to the informed setting.

## Removed Points

These points from the inputs were filtered:

- **"LASSO framing undersells a limitation" (Harsh Critic point 3):** The paper accurately states that the sample size conditions (26,27) do not depend on noise levels. The regularization parameter conditions (28) do depend on σ_avg², which the paper explicitly states and does not hide. Not a valid weakness.

- **"No missing related works":** Removed per instructions (cannot verify without external sources).

- **Formatting nitpicks about SNR definition:** The notation at line 129 is slightly imprecise but the meaning is clear; demoted to Trivial.

- **"Potential inconsistency between (9) and (12)" framed as a parser-artifact concern:** Kept but upgraded to Major because the mathematical simplification in (14) is demonstrably incorrect regardless of parser issues—this goes beyond formatting.

- **Strawman about "fatal if true" speculation:** The Harsh Critic's speculation about the eq (9)/(12) issue being "fatal" is removed because the actual issue is mathematical inconsistency that could be resolved or explained by the authors.

- **Strength Finder's generic/delusional strengths:** Removed generic praise about "important problem" etc. Only kept concrete, specific strengths grounded in the paper's actual content.

## Novel Insights

None beyond the paper's own contributions. The key insight — that information-theoretic and algorithmic thresholds respond differently to data heterogeneity (γ bounded vs. equal contribution) — is the paper's own discovery, not something synthesized from the reviews.

## Suggestions

1. **Clarify the mathematical inconsistency:** Correctly state the γ expression — either from (9)'s coefficients (with 2σ₂²) or justify the 2σ₁⁴ version in (12). Fix the simplification in (14) which does not follow from (12) as written. If the bound γ < 2 survives correction, show the correct derivation; if not, revise the claim.

2. **Add a more prominent caveat** in the abstract and introduction that the γ ≤ 2 bound is a property of a *relaxed* sufficient condition, not a proven fundamental limit, to prevent reader over-interpretation.

3. **Consider adding even a small-scale simulation study** to illustrate the looseness of the sufficient conditions and the empirical exchange rate between sample qualities.

## Score and Decision

Given the calibration database is not accessible, I score based on first-principles evaluation against ICLR standards.

The paper addresses a well-motivated, novel problem with genuine technical contributions (especially Theorem 3). The writing is clear and limitations are honestly stated. However, the mathematical inconsistency in the γ derivation (Eqs. 9, 12, 14) is a concrete concern about the paper's central quantitative claim that needs author clarification. The lack of lower bounds and simulations limits the strength of the info-theoretic results. 

On balance, this is a solid theoretical paper with real contributions and some notable limitations. The LASSO result alone (Theorem 3) is a significant extension, and the Price of Quality framework is useful even as a sufficient-condition analysis. With the mathematical issue resolved, the paper merits acceptance.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>