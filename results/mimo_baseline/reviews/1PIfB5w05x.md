## Summary

This paper studies sparse signal recovery when observations come from two sources with different noise levels (high-quality and low-quality data). The authors establish sufficient conditions for information-theoretic support recovery in both agnostic and informed settings, introduce the "Price of Quality" concept quantifying how many low-quality samples replace one high-quality sample, and prove that LASSO recovery in the agnostic setting depends only on the average noise level, revealing a striking robustness of algorithmic recovery to data heterogeneity.

## Strengths

- **Novel and well-motivated problem formulation.** The mixed-quality data setting directly addresses a practical scenario (e.g., combining LLM-labeled with expert-labeled data, multi-site clinical trials) that lacks a rigorous sparse-recovery foundation. The paper is the first to systematically study the trade-off between high- and low-quality samples for sparse recovery, filling a genuine gap.

- **Clean, interpretable results with striking contrasts.** The "Price of Quality" framework yields elegant conclusions: in the agnostic setting, one high-quality sample is never worth more than two low-quality samples (equations 13–14); in the informed setting, this price can grow arbitrarily large (equations 19–21). This contrast has clear practical implications—it quantifies the value of knowing per-sample noise variances.

- **Elegant LASSO robustness result (Theorem 3).** The finding that LASSO recovery thresholds in the agnostic setting depend only on the average noise level $\sigma_{\text{avg}}^2$ is surprising and theoretically clean. The proof technique—using Gram-Schmidt/QR decomposition and Haar measure properties to handle the non-scalar noise matrix—is a genuine technical contribution to extending Wainwright (2009) to the heterogeneous setting.

- **Tight results where possible, honest about limitations.** The informed setting results are obtained via exact Chernoff exponent optimization and are sharp. The agnostic sufficient condition involves a relaxation for tractability, and the paper explicitly acknowledges this in Remark 3.2, even suggesting where the bound could be tightened. The paper also clearly delineates what is proven tight versus what remains open.

- **Good exposition.** Proof sketches are provided in the main text with clear references to appendix material. The results are organized logically, the notation is clean, and the interpretation of each result in terms of different SNR regimes aids understanding.

## Weaknesses

### Fatal
None.

### Major

- **Agnostic sufficient condition is not proven tight.** The paper's most practically relevant bound—the price of quality ≤ 2 in the agnostic setting—rests on a sufficient condition obtained via a Chernoff bound relaxation (equation 37 becomes cubic, and the authors simplify for closed-form results). Without a matching necessary condition, one cannot rule out that this bound of 2 is an artifact of the proof technique rather than a fundamental limit. The informed case results are tight, and the paper acknowledges this gap (Remark 3.2, Remark 3.3), but the agnostic setting is arguably the more interesting/practical one. This limits the strength of the paper's headline claim about the price of quality being uniformly bounded.

- **No experimental validation.** While this is a theory paper, even brief numerical simulations confirming the phase transitions in sample-size space, verifying the price-of-quality behavior across SNR regimes, or comparing the sufficient condition with empirical recovery rates would substantially strengthen confidence in the results and their practical relevance. This is especially important given that the agnostic condition is only sufficient.

### Minor

- **LASSO analysis limited to agnostic setting.** The paper does not extend the LASSO analysis to the informed case (Remark 4.2 discusses the technical obstacle—the loss of Wishart structure). This means the natural question of whether informed LASSO would exploit quality differences at the algorithmic level remains unanswered, leaving an asymmetry in the paper's treatment of the two settings.

- **Binary signal assumption for information-theoretic results.** While well-justified in Remark 3.1 and standard in the literature, the restriction to binary signals $\beta^* \in \{0,1\}^p$ for Theorems 1–2 means the results apply to a restricted signal class. The extension to general sparse signals with varying magnitudes could reveal additional structure in how signal magnitude interacts with data quality.

### Trivial
None.

## Nice-to-Haves

- A brief discussion or numerical exploration of the tightness gap in the agnostic condition, perhaps by comparing the relaxed Chernoff bound with the exact cubic solution for specific parameter regimes.
- Extension to the case where the number of quality levels $K > 2$, which arises naturally in multi-site studies or crowdsourcing with multiple annotator skill levels. Remark 3.4 hints at this via the generalization to arbitrary $\Sigma$, but explicit analysis would be valuable.
- Comparison with practical heuristics (e.g., the $1/Y_i^2$ reweighting estimator mentioned in Remark 3.2) via simulations.

## Novel Insights

The paper's most genuinely novel insight is the fundamental asymmetry between information-theoretic and algorithmic thresholds in how they respond to data heterogeneity. The information-theoretic threshold adapts to quality differences (with the price of quality ranging from bounded to unbounded depending on the decoder's knowledge), while the LASSO algorithmic threshold is completely blind to heterogeneity and depends only on average noise. This suggests that computational tractability imposes a "lossy compression" on the data quality information: the algorithm cannot exploit per-sample quality differences even when they exist. This finding connects to a broader theme noted in the paper (Section 5) about algorithmic thresholds being more "robust" to modifications of the standard sparse recovery setup, alongside prior observations about sparse designs.

## Suggestions

- Consider adding a small simulation study validating the theoretical predictions, particularly the price-of-quality trade-off curves and the LASSO phase transition, across the three SNR regimes analyzed.
- For the agnostic information-theoretic result, it would be valuable to numerically solve the exact Chernoff exponent (cubic equation 37) and compare the resulting threshold with the relaxed bound, to quantify the tightness gap in concrete cases.
- Clarify whether the LASSO result's independence from individual noise levels has implications for practice—for instance, does it suggest that practitioners need not worry about calibrating sensor noise when using LASSO, even if the sensors are heterogeneous?

## Score and Decision

This is a well-executed theory paper that introduces a novel and practically motivated problem, provides clean and interpretable results across multiple settings, and makes genuine technical contributions. The contrast between agnostic and informed settings yields surprising insights, and the LASSO robustness result is elegant. The main limitation is that the agnostic sufficient condition—the paper's most practically relevant bound—is not proven tight, which tempers the strength of the headline "price of quality ≤ 2" claim. The absence of experimental validation is also notable for a paper with such clear practical motivations. However, these limitations are clearly acknowledged and do not invalidate the contributions. The informed results and LASSO results are tight, and the problem formulation itself opens a valuable research direction.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept