Now I'll produce the final consolidated review with the score anchored at 5.5.

## Summary

This paper addresses the problem that time-dependent PDEs produce distribution drift that breaks the exchangeability assumption required by standard conformal prediction (CP). The authors prove that in infinite-dimensional function spaces, CP is fundamentally impossible (Theorem 4.1, mutual singularity), but on finite-dimensional discretizations, the solution to a linear PDE with Gaussian initial condition remains Gaussian with analytically tractable mean and covariance (Theorem 4.2). This closed-form Gaussian structure enables likelihood-weighted CP with exact coverage guarantees. Experiments on a parameterized family of second-order linear PDEs (varying a, b, c coefficients) compare the proposed WCP against naïve CP and LSCI, showing that WCP maintains target coverage while baselines undercover.

## Strengths

- **Well-motivated problem.** The paper correctly identifies that time-dependent PDEs produce distribution drift that breaks standard CP exchangeability. The backward-heat-equation illustration in Figure 2 concretely demonstrates the failure mode, and the real-world examples (weather forecasting) ground the motivation.

- **Theorem 4.2 provides a clean theoretical foundation.** The result that a discretized linear PDE with Gaussian initial condition yields a Gaussian solution with analytically tractable mean and covariance is the core enabler. The connection between this classical fact and weighted CP — enabling closed-form likelihood ratios without density estimation — is the paper's genuine insight.

- **Empirical validation is reasonably thorough.** The paper tests multiple PDE parameterizations (varying a, b, c coefficients), compares against both naïve CP and LSCI, and includes a real-world thermography example (appendix). WCP consistently outperforms baselines in maintaining coverage, demonstrating that the theoretical guarantees translate to practice.

## Weaknesses

### Major

- **Scope overclaiming in abstract and contributions.** The abstract claims "exact coverage guarantees" for "a broad class of PDEs," and Contribution 2 claims "exact coverage guarantees for PDEs without limiting assumptions on their time-dependent behavior." In reality, Theorem 4.2 requires a *linear* spatial differential operator ℒ_x, linear boundary conditions, and a Gaussian (or location-scale) initial condition. The Discussion (§6) does honestly state "the class of linear PDEs," but the abstract and introduction (lines 8–9, 44–46) do not reflect this restriction. The phrase "without limiting assumptions on their time-dependent behavior" is doubly misleading: the limitation is linearity, not time-dependent behavior.

- **Empirical coverage deviates from the 90% target in cases the paper's own explanation does not cover.** Table 1 shows WCP coverage of 0.88, 0.85 (a=-0.005, steps 15, 20), 0.89, 0.88, 0.84 (a=-0.0075, steps 5, 10, 15), and 0.89, 0.88 (a=-0.01, steps 5, 10). In several of these cases n_infinity is 0.0% (a=-0.005/step-15, a=-0.0075/step-5, a=-0.0075/step-10), meaning no samples were excluded. The paper's defense that the drop occurs "when n_infinity approaches roughly 90%" (line 289) does not explain these cases. With 5000 test samples, the deviation at a=-0.005/step-20 (0.85 vs 0.90) is about 12 standard errors below target. This is a genuine gap between the "exact coverage" claim and the evidence.

- **Gap between the theoretical derivation and the empirical procedure regarding surrogate residuals.** Theorem 4.2's Gaussian result applies to the PDE *solution*, but CP scores are computed on *residuals* (surrogate model prediction error). The density-ratio weights (Equation 1) use the Gaussian density of the solution u_t. Whether the surrogate model's residuals inherit the same Gaussian dynamics — and whether the weighted CP coverage guarantee remains valid when weights are based on the solution distribution rather than the residual distribution — is never discussed or justified. This is a significant gap.

### Minor

- **Theorem 4.1 is presented as Contribution 1 but has no practical connection to the method.** The paper itself states (line 156–157) that the function-space mutual singularity result "is not necessarily problematic for practical CP on surrogate models." Presenting it as a main contribution inflates the paper's theoretical heft without informing the actual solution. It would be better presented as background motivation for why discretization is necessary.

- **Missing trajectory-based exchangeability baselines.** The Related Work (§2) identifies trajectory-based methods (Moya et al., 2025; Gray et al., 2025) as "the most straightforward option," but the experiments compare only against naïve CP and LSCI. While the paper's setting (deployment beyond the calibration horizon) limits direct applicability, their absence weakens the empirical story, especially for time horizons within the calibration window.

- **No uncertainty estimates on reported coverage values.** Table 1 and Figure 3 report mean coverage without standard errors, confidence intervals, or variance estimates. With 5000 test samples, these are trivial to compute and would substantially strengthen the reliability assessment.

- **LSCI baseline uses a non-standard configuration.** The paper sets LSCI's number of band samples to 5000 to "push LSCI to over-coverage" (line 279). While this is generous to LSCI rather than adversarial, the non-standard configuration makes the comparison harder to interpret against LSCI's recommended settings.

### Trivial

None.

## Nice-to-Haves

- Report overall coverage including infinite-band samples (where infinite bands count as covering) — this would likely show WCP as conservative above 90%, which is more honest and useful for safety-critical applications.
- Provide a rigorous error analysis for transferring bands from the discretized solution to the original PDE solution (Remark 4.5 is currently handwavy).
- Discuss the computational cost of matrix exponentials exp(tA) for large spatial grids (2D/3D).

## Removed Points

These points were flagged for removal from the input review (with justification):

1. *"The dismissal of trajectory-based methods applies equally to WCP"* — REMOVED as factually incorrect. WCP handles any time horizon through the known PDE model; trajectory methods cannot extrapolate beyond the training horizon.
2. *"The assumption that 𝒜 = 𝒰_t for all t should be stated upfront"* — REMOVED because it IS stated upfront (line 104).
3. *"LSCI configuration stacks the deck against the baseline"* — REMOVED because making LSCI more conservative favors the baseline, not the authors.
4. *"Theorem 4.2 derivation is elementary"* — REMOVED as a stylistic opinion, not a weakness.
5. *"Missing implementation details about exp(tA) computation"* — REMOVED as appendix content removed by parser, not verifiable.
6. *"Real-world example relegated to appendix"* — REMOVED as common practice, not a weakness.

## Novel Insights

The most penetrating observation from the review process is the mismatch between the density-ratio weighting (which uses the PDE solution's Gaussian distribution) and the actual object of conformal prediction (surrogate model residuals). This is a genuine theoretical gap that the paper never addresses: WCP's weights are derived from the PDE solution distribution, but the coverage guarantee requires the weights to be likelihood ratios of the *data points* being exchangeability-adjusted, which in CP for regression is the joint distribution of features and response. A deeper connection between the Gaussian solution dynamics and the residual distribution would substantially strengthen the theory.

A second valuable observation is that the empirical coverage deviations (0.85–0.89) occur precisely where the paper's stated defense (n_infinity approaching 90%) does not apply — suggesting that the underlying issue may be finite-sample weighted quantile estimation error or numerical precision in the covariance computation, rather than small remaining sample size. This warrants investigation.

## Suggestions

1. Temper the scope claims in the abstract and introduction to honestly reflect "linear PDEs with Gaussian/location-scale initial conditions."
2. Investigate and explain the coverage deviations in Table 1 where n_infinity is low (0–35%).
3. Discuss or theoretically justify the transfer from PDE solution Gaussianity to surrogate model residual distribution in the weighted CP framework.
4. Add trajectory-based exchangeability methods as baselines for time horizons within the calibration window.
5. Report standard errors or confidence intervals for all coverage estimates.
6. Report overall coverage including infinite-band samples.
7. Move Theorem 4.1 from "Contributions" to background/setup.

**Calibration Summary:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Calibrated Physics-Informed UQ | cF6OoaYcRa | 4.50 | R1 | Yes | Weaker theory, simpler method; our paper is stronger |
| In-Context Neural PDE | fzZfju8y0g | 3.40 | R1 | Yes | Different task (solving PDEs vs UQ); less relevant |
| Regression CP under Bias | v8RDgaEtE2 | 2.50 | R1 | Yes | Different topic; weaker empirical support |
| Valid CP for Dynamic GNNs | i3T0wvQDKg | 5.80 | R1 | Yes | Similar CP-for-dynamics framing; cleaner experiments |
| CONTRA (Normalizing Flow CP) | pOO9cqLq7Q | 6.25 | R1 | Yes | Stronger presentation; fewer overclaim issues |
| Non-Exchangeable Conformal Risk Control | j511LaqEeP | 6.00 | R2 | Yes | Broader theory; incremental from prior work |
| KOWCPI (Weighted CP Time Series) | oP7arLOWix | 6.00 | R2 | Yes | Clean framing; good experiments |
| Wasserstein-Regularized CP | aJ3tiX1Tu4 | 6.67 | R2 | Yes | Stronger theory; more thorough experiments |
| CopulaCPTS | ojIJZDNIBj | 6.25 | R2 | Yes | Solid but limited novelty |
| Quantifying Past Error Matters (ECI) | RD9q5vEe1Q | 5.50 | R3 | Yes | **Closest anchor** — similar overclaim issues, accepted |

The round-1 bracket was **[4.5, 6.0]**. Within this bracket, the closest anchor is "Quantifying Past Error Matters" (5.50), which shares a similar profile: a solid core methodological contribution with some overclaiming and presentation roughness. Our paper has stronger theoretical grounding (Theorem 4.2) than that anchor but has more significant empirical gaps (coverage deviations, missing baseline comparisons). The strengths carry positive weights (8.65–10.58), while the most negative-weighted weakness is only -0.88 (Theorem 4.1 as contribution). Compared to the CPI-UQ anchor (4.50, rejected), our paper has clearly better theory and more extensive experiments. Placing it at 5.5 reflects a paper whose core contribution is genuine and valuable, but whose framing and experimental incompleteness prevent it from reaching the clear-accept tier.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>