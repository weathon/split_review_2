## Summary

This paper studies conformal prediction (CP) for time-dependent PDE surrogate models, where exchangeability fails due to temporal distribution shifts. The authors prove that in infinite-dimensional function spaces, solution distributions at different times are mutually singular (Theorem 4.1), motivating a finite-dimensional approach. Their main technical contribution is Theorem 4.2, which derives closed-form Gaussian densities for discretized linear PDEs with Gaussian initial conditions, enabling weighted conformal prediction (WCP) with exact coverage guarantees. Experiments on synthetic PDEs and a real-world pulsed-thermography problem demonstrate that WCP maintains coverage where naive CP and LSCI fail.

## Strengths

1. **Clean, correct derivation of closed-form density ratios via linear-Gaussian structure (Theorem 4.2).** The paper establishes that under linear dynamics and Gaussian initial conditions, the discretized PDE solution is Gaussian at every time point, providing exact closed-form likelihood ratio weights for weighted CP. This is the paper's technical engine and is mathematically sound.

2. **Empirical demonstration that naive CP and LSCI collapse in unstable regimes.** Figure 3 and Table 1 show that as the PDE parameter `a` becomes more negative (more unstable), naive CP and LSCI coverage drops dramatically (e.g., to 0% at timestep 20 for a=−0.01), while WCP maintains coverage much closer to the 90% target. The visual contrast is compelling and supports the paper's core narrative.

3. **Directly addresses a genuine, underappreciated problem.** Non-exchangeability in time-dependent PDEs is a real obstacle for CP in scientific ML, and most prior work sidesteps it. The paper provides both a theoretical diagnosis (Theorem 4.1 showing why function-space approaches fail) and a concrete solution for an important subclass of problems.

## Weaknesses

### Fatal
None.

### Major

1. **Unexplained undercoverage in the experimental results, contradicting the central empirical claim.**  
   In Table 1, for `a = −0.005` at timestep 20, WCP achieves only 0.85 coverage against a 0.90 target, yet only 0.2% of samples receive infinite bands (n_∞). The paper's stated explanation — "with very few samples remaining, the empirical coverage is subject to higher stochastic noise" — does not apply here because 99.8% of samples have finite bands. Similar mild undercoverage appears at other configurations without correspondingly high n_∞ (e.g., `a = −0.0075`, timestep 10: 0.88 coverage, n_∞ = 0.0%). No confidence intervals or standard errors are reported anywhere in the paper, making it impossible to assess whether these deviations from 0.90 are statistically significant or indicative of a systematic issue. The paper claims WCP "consistently meets its coverage guarantees" (line 289), but the data in the same table undermine this claim. This is a substantive evidential gap that needs to be addressed.

### Minor

1. **Scope inflation in the abstract and introduction.** The abstract claims the method applies to "a broad class of PDE problems" and the introduction says "exact coverage guarantees for PDEs without limiting assumptions on their time-dependent behavior." In practice, Theorem 4.2 requires: (i) a linear spatial differential operator, (ii) Gaussian (or location-scale) initial conditions, (iii) the PDE must be known analytically, and (iv) the initial distribution parameters must be known. This is a meaningful but delimited subclass. The discussion section correctly characterizes it as "the class of linear PDEs," but the abstract and introduction would benefit from upfront qualification rather than leaving the reader to discover the restrictions.

2. **Remark 4.5 on transferring coverage to the continuous solution is too vague to be actionable.** The remark states that "bands on the discretized solution can be transferred to the original solution by leveraging numerical error guarantees of the scheme" but provides no concrete bound, condition, or worked example. Since the function-space diagnosis (Theorem 4.1) establishes that the continuous problem is intractable, the relationship between discretized and continuous coverage is a natural point of concern, and the paper leaves this connection dangling.

3. **Real-world experiment is undersold in the main text.** The pulsed-thermography example receives exactly one sentence (line 293) with only a qualitative claim ("Our method achieves target coverage over all tested time steps"). No coverage numbers, bandwidths, or error bars appear in the main paper. If this experiment is worth mentioning to demonstrate practical applicability, it deserves at least one quantitative result in the main text.

4. **No discussion of robustness to misspecified PDE parameters or initial distribution.** The weights depend on knowing the matrix A, μ₀, and Σ₀ exactly. In practice, these quantities would be estimated (e.g., thermal diffusivity in the real-world example). Weighted CP is sensitive to weight misspecification, but the paper does not discuss how errors in these estimates would propagate into coverage or how practitioners could account for uncertainty in the PDE model itself.

### Trivial

- Theorem 4.1 (mutual singularity in function space) is formally correct and serves a diagnostic role, but it does not directly inform the weighted CP method or bound the error from discretization. It contextualizes the problem statement but is somewhat peripheral to the paper's actual contribution.

## Nice-to-Haves

- Report coverage with confidence intervals (e.g., binomial CIs or standard errors) for all experimental results. This would directly address the main weakness about the unexplained 0.85 coverage value.
- Compare against trajectory-level exchangeability as a baseline (Moya et al., 2025; Gray et al., 2025). While trajectory-level CP answers a different question (coverage over full trajectories rather than per-time-step), including it would contextualize the paper's contribution relative to the most closely related alternative.
- Provide a proper timing benchmark with controlled hardware, rather than the current anecdotal comparison (40 minutes for LSCI vs. seconds for WCP on one machine).
- Discuss the impact of weight misspecification on coverage guarantees and potential mitigation strategies.

## Removed Points

These points are flagged to be removed; treat them with caution:

- *Missing trajectory-based baseline as a "critical methodological gap" (Critic's Issue #3)*: Trajectory-level CP provides coverage guarantees over full trajectories, not per-time-step. Since the paper addresses the strictly harder problem of per-time-step coverage under distribution shift, trajectory-based CP is not a direct comparison baseline for the same task. Demoted from "critical weakness" to a nice-to-have.

- *"WCP requires knowledge unavailable in surrogate model settings" (Critic's Issue #5, main thrust)*: The paper explicitly states the assumption that the PDE is known analytically and can be solved numerically (line 126). This is a stated limitation of the approach, not an unacknowledged flaw. The robustness-to-misspecification sub-point is retained as Minor weakness #4 above.

- *Criticism that Theorem 4.1 is "a single example, not a general result"*: The paper explicitly states (line 154) that this is "representative of a broader phenomenon" and cites Hairer (2023) on mutual singularity of measures in infinite dimensions. The generalization claim is present.

- *Claim that "no experiments showing method works under non-Gaussian location-scale distributions"*: Remark 4.3 explicitly references appendix A.8 for additional experiments with location-scale distributions. The appendix is stripped by the parser; the experiments exist in the original submission.

- *"Computational comparison is anecdotal"*: This is standard for ML papers; a more rigorous comparison would strengthen the paper but omitting one is not a weakness.

- *Criticism that the paper should discuss "whether the [Theorem 4.1] choice is forced by the analysis"*: Already addressed by the paper's citation of Hairer (2023) and the statement that this is a broader phenomenon.

- *Criticism about "missing related works"*: Not verifiable without external sources; removed per policy.

- *"Pure formatting/style nitpicks" and "typos, grammar, punctuation" complaints*: These are parser artifacts, not author errors; removed per policy.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a tension between the paper's clean theoretical development (which is valid for its stated subclass) and its empirical evidence (which contains a partially unexplained coverage gap). This tension—between elegant theory and messy practice—is worth noting but does not constitute a novel insight about the paper's problem domain.

## Suggestions

1. **Add confidence intervals to all coverage numbers in Table 1 and Figure 3.** This is the single most impactful change the authors can make. It would clarify whether the 0.85 coverage value represents a meaningful deviation or is within expected variability, and it would significantly strengthen the paper's empirical credibility.

2. **Calibrate the abstract and introduction to match the actual scope.** Replace "broad class of PDEs" with a more precise description (e.g., "linear PDEs with known dynamics and Gaussian initial conditions") and move the "without limiting assumptions" claim to the discussion section or qualify it explicitly.

3. **Provide a concrete bound or reference for Remark 4.5** or remove the remark. As written, it promises a connection it does not deliver.

4. **Include at least one quantitative result from the real-world experiment** in the main text (e.g., coverage at the final time step).

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>