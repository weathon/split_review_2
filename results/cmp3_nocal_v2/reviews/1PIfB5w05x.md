Here is the final consolidated review.

---

## Summary
This theoretical paper studies sparse support recovery when observations come from mixed-quality sources (low-noise "high quality" and high-noise "low quality"). It provides sufficient conditions for recovery in both an agnostic setting (the decoder ignores per-sample variances) and an informed setting (variances are known), and analyzes the LASSO in the agnostic setting. The central conceptual contribution is the "Price of Quality" (γ) — the number of low-quality samples needed to replace one high-quality sample under the sufficient condition — which is bounded by 2 in the agnostic setting but can grow arbitrarily large in the informed setting. The LASSO analysis shows the algorithmic threshold depends only on total sample size and average noise variance, matching the homogeneous-noise case.

## Strengths
- **Well-motivated problem formulation.** The paper correctly identifies that the sparse recovery literature overwhelmingly assumes homogeneous noise, despite many practical settings (LLM-assisted labeling, citizen science, multi-site clinical trials) where data quality varies. The distinction between agnostic and informed decoders is natural and useful.
- **The Price of Quality is a clean conceptual contribution.** The idea of quantifying the trade-off via a single coefficient γ, and the result that γ ≤ 2 in the agnostic setting, is interpretable and potentially impactful for practitioners thinking about data acquisition. The paper consistently qualifies this as holding "under our sufficient condition" (lines 81, 336).
- **The LASSO analysis is a non-trivial technical extension.** Extending Wainwright (2009) to heterogeneous noise requires overcoming the loss of Wishart structure — the QR/Haar-measure approach is a principled solution. The result that the phase transition depends only on σ²_avg is clean and practically relevant.
- **Transparent about limitations.** Remark 3.2 openly discusses the looseness of the agnostic sufficient condition, the relaxation used in the Chernoff bound, and even suggests an alternative estimator (reweighting by Yᵢ²) that is not analyzed. Remark 4.2 explains why the informed LASSO extension is difficult. This candor is commendable.

## Weaknesses

### Fatal
None.

### Major
1. **The Section 3 framing conflates "information-theoretic limit" with "performance of a specific estimator that ignores heterogeneity."** Section 3 opens by stating the goal is to determine "whether it is possible, information-theoretically, to recover the support" (line 139), and the abstract and introduction use the same language. However, Theorem 1 analyzes estimator (8) — the naive ℓ₂-minimizer motivated by the MLE under *homogeneous* noise — and the paper acknowledges (Remark 3.2) that this estimator "might not constitute the best approach to recover the support" when noise is heterogeneous and that the condition is not information-theoretically sharp. Despite these caveats, the "information-theoretic" framing invites readers to interpret the Price of Quality bounds (γ < 2) as fundamental limits, when they are contingent on estimator choice and on the looseness of a sufficient condition. This is a meaningful gap between the paper's framing and what is actually proved.

2. **The looseness of the agnostic sufficient condition is not quantified.** The paper notes (Remark 3.2) that condition (9) involves a relaxation of the optimal Chernoff bound (solving a cubic equation (37) would tighten it). However, the gap between the relaxed condition and the optimal bound is never quantified — no numerical illustration, no lower bound, no necessity result. Since the headline γ < 2 result (14) is derived from this relaxed condition, it is unclear whether this bound is tight or could be much smaller than the true Price of Quality. The paper's practical interpretation of γ as a meaningful quantity rests on this unquantified gap.

### Minor
1. **δ-dependence of γ is undiscussed.** Both γ expressions (12) and (18) depend on δ, the error tolerance parameter. The asymptotic analyses (13)-(14) and (19)-(21) treat δ as a fixed constant, but the paper does not discuss whether γ is sensitive to δ in regimes of interest or how γ behaves as δ → 0. This weakens the interpretability of the γ bounds.

2. **No empirical validation.** The paper is purely theoretical, with no simulations demonstrating that the sufficient conditions are predictive of actual recovery behavior. Given that the sparse recovery theory literature routinely includes Monte Carlo phase diagrams (Wainwright 2009; Gamarnik & Zadik 2022), and that the paper's practical relevance is a central motivation, the absence of even a simple simulation limits the paper's ability to support claims of practical applicability.

3. **LASSO regularization parameter requires unknown σ²_avg in the agnostic setting.** Condition (28) on λₚ depends on σ²_avg = (n₁σ₁² + n₂σ₂²)/n. In the agnostic setting, the decoder does not know σ₁² or σ₂². The paper states an existence result but does not address how to choose λₚ in practice when the per-sample variances are unknown.

4. **Dangling thread on the reweighted estimator.** Remark 3.2 mentions an alternative estimator reweighting by 1/Yᵢ² but offers no analysis. This creates a natural question — would such an estimator achieve a higher Price of Quality in the agnostic setting? — that the paper leaves unresolved.

### Trivial
- The notation in the SNR definitions (line 129), `𝔼[‖yᵢ − xᵢᵀβ*‖₂²]_{i=1}^{n₁}`, is slightly ambiguous about whether it denotes a per-observation expectation or a sum. The resulting expression s/σ₁² is correct but the notation could be clearer.

## Nice-to-Haves
- A compact table summarizing key assumptions (Gaussian design, exact s-sparsity, binary/bounded-away-from-zero signal, two noise levels) and their roles would improve readability.
- A discussion of the computational gap between the combinatorial estimator (8) (NP-hard) and the polynomial-time LASSO would strengthen the information-theoretic vs. algorithmic narrative.
- Quantifying the gap between the relaxed Chernoff bound and the optimal bound for a specific numerical case (e.g., a contour plot showing how much (9) differs from the exact solution of (37)) would help readers assess whether γ < 2 is robust.
- A practical suggestion for choosing λₚ in the agnostic setting (e.g., cross-validation or plug-in estimates of σ²_avg) would round out the LASSO contribution.

## Removed Points
- **Criticism about the n_INF formula (Section 1.1.1) only matching known thresholds under specific SNR conditions:** This concerns how the paper characterizes cited work (Reeves et al., 2019), not the paper's own contributions. Removed per rule against second-guessing cited results.
- **Criticism about the binary-signal assumption not being formally justified:** The paper provides justification via rescaling (Remark 3.1). Removed — the paper already addresses this.
- **Criticism that Remark 3.3 "oversells" the sharpness of informed thresholds:** This is a characterization dispute about cited work. Removed as not affecting the paper's own contributions.
- **Formatting/style nitpicks** (ambiguous SNR notation labeling as "harder to parse than necessary," tangential conclusion paragraph criticism): Removed per formatting/style rule.

## Novel Insights
Beyond the paper's own contributions, the most useful insight from the review is that the agnostic setting conflates "information-theoretic" analysis with the performance of a specific estimator that ignores heterogeneity. This framing critique identifies a concrete path to strengthen the paper: either establish minimax lower bounds, or explicitly reframe Section 3. The looseness critique further sharpens the concern that the headline γ < 2 bound may not be robust.

## Suggestions
1. Reframe Section 3 to clearly state that Theorem 1 analyzes the performance of the naive ℓ₂ estimator (8) under heterogeneous noise, rather than claiming to establish fundamental information-theoretic limits. Alternatively, add a minimax lower bound or necessity result to justify the "information-theoretic" framing.
2. Quantify the gap between the relaxed condition (9) and the optimal Chernoff bound — even a simple numerical illustration for one parameter configuration would help readers assess whether γ < 2 is an artifact of the relaxation.
3. Add a simulation study (e.g., Monte Carlo recovery probabilities for moderate p, s, comparing the sufficient condition thresholds against empirical phase transitions).
4. Discuss the δ-dependence of γ, particularly whether the γ < 2 bound degrades as δ → 0.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>