## Summary

This paper proposes a method for constructing lower prediction bounds (LPBs) for counterfactual survival times under general right-censoring. The core idea is to transform the counterfactual coverage problem into a covariate-shift problem between the marginal covariate distribution and the distribution conditional on being uncensored under a given treatment, then apply weighted conformal prediction. The authors provide a finite-sample bound on coverage in terms of weight estimation error (Theorem 4.1) and an asymptotic doubly robust guarantee (Theorem 4.2). Experiments on synthetic and real clinical data compare against prior PAC-type methods.

## Strengths

1. **Clean reduction to weighted conformal prediction.** The derivation in equation (1) that connects the counterfactual miscoverage probability to a weighted expectation over uncensored treated observations is technically sound under the stated assumptions (SUTVA + ignorability with T ⟂⟂ C | X) and elegantly maps a non-standard problem onto a well-studied framework.

2. **Theoretical bound with weight-estimation error (Theorem 4.1).** The bound P(T(w) ≥ LPB) ≥ 1 − α − (1/2)E[|ω̃ − ω|] usefully characterizes how errors in estimating γ(x) = P(W=w, e=1|X) propagate into the coverage gap. This is explicit and connects implementation difficulty (estimation of a nuisance function) to statistical guarantees in a way prior PAC-type guarantees did not.

3. **Doubly robust property (Theorem 4.2).** Establishing that asymptotic coverage holds if either the weights or the quantile function is consistently estimated adds a layer of robustness that is valuable in practice, where one but not both models may be well-specified.

## Weaknesses

### Fatal
None.

### Major

1. **Per-test-point τ-optimization is not covered by the theoretical guarantee.** The paper states that coverage holds "for any τ ∈ (0,1)" (line 162) then optimizes τ*(x) per test point to maximize the LPB (line 164). This τ*(x) depends on both the test covariate x and the calibration data (through c(τ)). Standard conformal prediction theory does not automatically extend to data-dependent per-point choice of the non-conformity score function. The paper provides no argument — theoretical or empirical — that coverage is preserved under this optimization. This is a genuine gap: the method as actually implemented and evaluated (Table 1, Figure 1-3) uses the optimized τ*, but the theorem only guarantees coverage for fixed τ. This does not invalidate the core reweighting contribution, but it means the practical procedure lacks the stated theoretical backing. The authors could fix τ = α, use a separate validation set for τ selection, or provide a uniform-convergence proof that the argmax preserves the bound.

### Minor

2. **"Exact" guarantee language overstates what is proved.** The abstract claims "an LPB to be obtained via quantile regression with an exact miscoverage guarantee" and the contributions claim "a distribution-free exact guarantee." However, Theorem 4.1 provides a bound: P ≥ 1 − α − (1/2)E[|ω̃ − ω|], which is exact only when the weight estimation error is zero. The introduction does qualify "provided that the weight function can be well estimated" (line 28), but the abstract and contribution list do not. This contrast with the PAC-type guarantees of prior work is meaningful and worth highlighting, but the language should be calibrated to what is actually proved (e.g., "approximately exact" or "distribution-free bound with explicitly quantified error from weight estimation").

3. **Calibration data limitation not quantitatively characterized.** Algorithm 1 discards all censored observations (step 3 keeps only uncensored treated observations). In high-censoring regimes (e.g., 60% censoring) with rare treatments, the effective calibration sample per arm can shrink drastically (e.g., 20% treatment × 40% uncensored = 8% of total data). The Discussion acknowledges this qualitatively (line 288), but the paper does not characterize the regimes — in terms of censoring rate, treatment proportion, and sample size — where coverage begins to degrade. Given that this is structurally required by the method (the non-conformity score needs observed T), this characterization would help practitioners understand applicability boundaries.

4. **No uncertainty quantification for coverage estimates.** Coverage rates are reported as point estimates across 50 trials (Figure 1) or 10 trials (Table 1, Figure 2) without standard errors or confidence intervals. Given the modest effective sample sizes per treatment arm, the variance of the estimated coverage is material and should be reported.

5. **Coverage dip in setting 6 unexplained.** The paper notes that "the average coverage rate of our method slightly falls below 1−α in setting 6" (line 238) but does not analyze why. Is this setting characterized by higher censoring, smaller sample size, treatment imbalance, or worse weight estimation? Understanding this would clarify whether the gap is due to randomness, a systematic pattern, or a limitation of the weight estimation method.

6. **Limited evaluation across α levels.** The main synthetic experiments (Figure 1) only test α = 0.1. Table 1 explores other α values but on only one setting with only 10 trials. Given that coverage guarantees across different nominal levels are central to the paper's claims, broader evaluation is warranted.

7. **Real-data analysis provides only face validity.** The real dataset has 541 patients with 124 features; with a 50/10/30/10 split and 4 treatment arms, some subgroups likely have very few test patients per trial. An MLP with 3 hidden layers on this sample size risks overfitting. The analysis is descriptive — it observes that LPB correlates with known prognostic factors in expected directions — which is a useful sanity check but does not validate counterfactual accuracy (ground truth counterfactuals are inherently unobservable).

### Trivial

8. **Non-monotonic τ* values in Table 1.** The optimized τ* values (0.16, 0.16, 0.26, 0.21) are not monotonic in α, which is unexpected if τ* tracks the quantile of interest. The paper's explanation ("the quantile regression model is well trained") is insufficient.

9. **Coverage plots (Figure 1) use compressed y-axis (0.86–0.94).** This visually exaggerates small coverage differences.

## Nice-to-Haves

- **Empirical comparison with Qi et al. (2024) and Candès et al. (2023):** The paper compares only against Davidov et al. (2025) baselines ("Focus," "Fused"). Including Qi et al. (best-guess imputation) would strengthen the benchmark, and including Candès et al. in a Type-I censoring sub-experiment would help assess relative performance in that restricted setting.
- **Ablation: fixed τ = α vs. optimized τ*(x):** Running a controlled comparison between fixed and optimized τ would empirically check whether the optimization inflates miscoverage.
- **Clarify how γ(x) = P(W=w, e=1|X) is estimated:** The paper says "fit Random Forest classifiers" (line 234/258) but does not specify whether this is a single joint model or a product of two models (P(W=w|X) × P(e=1|X,W=w)). The distinction matters for the doubly robust property.

## Removed Points

The following criticisms from the harsh review were removed:
- **"Section 3 equation notation confusing"** — The paper explicitly states this describes Gui et al. (2024)'s Type-I censoring scenario; the notation is appropriate for that context.
- **"Lemma A.1 not stated in main text"** — The appendix is stripped by the parser; the paper's existing text provides the intuition for the inequality direction.
- **"Theorem 4.2 regularity conditions may fail in practice"** — Every asymptotic theorem has regularity conditions; this observation is generic and applies to virtually all doubly robust results.
- **"Figure caption duplication"** — This is a PDF parsing artifact, not an author error.
- **"No comparison against Candès et al. in the paper's main setting"** — Candès et al. is designed for Type-I censoring; the paper targets general censoring, making a direct comparison in the main experiments methodologically mismatched. A comparison in a Type-I sub-experiment is noted as a nice-to-have.
- **"Missing discussion of how to estimate γ(x)"** — The paper states Random Forest; the missing implementation detail (single joint model vs. product) is a minor clarification.
- **"Only α=0.1 in main experiments"** — This is already listed as Minor (point 6); the critic's framing was slightly stronger than warranted since the paper does include some variation in Table 1.

## Novel Insights

None beyond the paper's own contributions. The harsh review correctly identified the τ-optimization gap, which is a genuine oversight not discussed in the paper itself. No additional structural insights emerged from the review that the authors themselves did not surface.

## Suggestions

1. **Address the τ-optimization gap directly.** The cleanest fix is to either (a) fix τ = α and justify why this suffices, (b) use a separate validation set to select a single τ, or (c) prove that the argmax over τ does not inflate the miscoverage probability (e.g., via a union bound or by showing the coverage bound holds uniformly). Without one of these, the main experimental results lack a matching theoretical guarantee.
2. **Calibrate "exact" language** in the abstract and contribution list to match Theorem 4.1's bound, e.g., "distribution-free bound with explicitly quantified error from weight estimation."
3. **Add error bars or confidence intervals** to all reported coverage rates.
4. **Characterize the effective sample size** as a function of censoring rate and treatment proportion, and show where coverage empirically degrades.
5. **Explain the setting 6 coverage dip** and whether it reflects a systematic limitation.
6. **Add a comparison against Qi et al. (2024)** in the synthetic experiments to broaden the baseline set.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>