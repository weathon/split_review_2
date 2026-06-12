## Summary

This paper proposes a conformalized survival counterfactual prediction method that constructs exact marginally valid lower prediction bounds (LPBs) for counterfactual survival times under different treatments in the general right-censored data setting. The key innovation is a reweighting scheme that transforms the problem into a weighted conformal inference problem, enabling exact marginal coverage guarantees (rather than PAC-type guarantees from prior work) via counterfactual quantile regression with density ratio weighting.

## Strengths

- **Addresses a genuine gap in the literature.** Prior works (Gui et al., 2024; Davidov et al., 2025) achieved only PAC-type coverage guarantees for LPBs in the general right-censored setting. The paper convincingly argues that exact marginal coverage is preferable in high-stakes clinical scenarios where rare/extreme cases matter, and provides a principled approach to achieve it.

- **Well-grounded theoretical framework.** The weighted conformal prediction approach, building on Lei & Candès (2021), is theoretically sound. Theorem 4.1 provides a finite-sample bound with an explicit error term from density ratio estimation (Eq. 4), and Theorem 4.2 establishes the doubly robust property, ensuring valid coverage when either the weight function or the quantile estimator is consistently estimated.

- **Comprehensive empirical evaluation.** The synthetic experiments span six settings mimicking real clinical trials, include robustness tests against outliers (Figure 3), multi-treatment scenarios (Figure 2), sensitivity analyses to regression algorithms and weight functions (Appendix E.4, E.5), and sample size convergence (Appendix E.1). The real-world lung cancer dataset application yields clinically interpretable results consistent with domain knowledge (e.g., VMAT outperforming IMRT, stage/KPS associations with survival).

- **Clever LPB optimization procedure.** The observation that coverage holds for any τ allows maximizing the LPB over τ to obtain the most informative bound, which is a practical and elegant design choice.

## Weaknesses

### Fatal
None.

### Major

- **The "exact" guarantee is overstated in the introduction.** Theorem 4.1's coverage guarantee is $1 - \alpha - \frac{1}{2}\mathbb{E}[|\hat{\omega}(X) - \omega(X)|]$, which includes a density ratio estimation error term. This is only "exact" when the density ratio is perfectly estimated. The paper should more carefully distinguish between the exactness of the conformal calibration procedure (conditional on estimated weights) versus the population-level guarantee. The current framing risks misleading readers about the nature of the guarantee.

- **Limited real-world validation.** The clinical application uses a single dataset of 541 lung cancer patients with four treatment regimens. The results are presented descriptively (Figures 4-5) without formal statistical testing or comparison with clinical baselines beyond prior literature citations. For a method paper targeting clinical decision-making, stronger validation (e.g., multiple clinical datasets, clinical expert validation, or comparison with established clinical prediction models) would significantly strengthen the claims.

### Minor

- **Weight instability not addressed.** When the positivity assumption is nearly violated (very small γ(x)), the weights ω(x) = 1/γ(x) can become extremely large, destabilizing the weighted conformal procedure. The paper acknowledges data imbalance in the Discussion but provides no practical guidance or diagnostics for detecting and handling such cases.

- **Computational cost of τ optimization.** The LPB optimization requires searching over τ ∈ (0,1) for each test point, which involves recomputing the weighted conformal quantile for each candidate τ. The paper does not discuss computational complexity or practical runtime.

- **Typo in Algorithm 1.** Line 7 uses $\mathcal{I}_2^{(w)}$ which should be $\mathcal{I}_{\text{cal}}^{(w)}$ based on the formulas in Section 4.1.

### Trivial
None.

## Nice-to-Haves

- A discussion of when the weighted conformal approach may break down in practice (e.g., extreme censoring rates, treatment imbalance) with practical diagnostics.
- Computational comparison of runtime against baselines, especially for the τ optimization step.
- Sensitivity analysis to the training/calibration split ratio.

## Novel Insights

The paper's most novel insight is the reformulation of the survival counterfactual coverage problem as a density ratio estimation problem under covariate shift. By recognizing that the distribution shift from the full population P_X to the conditional population P_{X|W=w,e=1} can be handled through importance weighting, the paper elegantly bridges conformal prediction under covariate shift (Lei & Candès, 2021) with causal survival analysis. This connection, combined with the observation that coverage holds for any τ (enabling post-hoc optimization for informativeness), represents a meaningful conceptual contribution to the conformal causal inference literature.

## Suggestions

- Explicitly discuss the limitations of the "exact" guarantee and provide practical guidance for when the density ratio estimation error term is expected to be small (e.g., based on propensity model fit diagnostics).
- Add at least one additional real-world clinical dataset to strengthen generalizability claims.
- Include a practical diagnostic for weight instability (e.g., effective sample size after weighting).
- Fix the notation inconsistency in Algorithm 1, Step 7 ($\mathcal{I}_2^{(w)}$ vs. $\mathcal{I}_{\text{cal}}^{(w)}$).

## Score and Decision

The paper makes a solid methodological contribution by providing the first exact marginal coverage guarantee for conformalized survival counterfactual prediction in the general right-censored setting. The theoretical framework is sound and the experimental evaluation is reasonably thorough. However, the "exact" guarantee is somewhat overstated, and the real-world validation is limited to a single dataset. The contribution is incremental but genuine—combining existing tools (weighted conformal prediction, causal survival analysis, density ratio estimation) in a principled way to achieve a stronger guarantee than prior work.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept