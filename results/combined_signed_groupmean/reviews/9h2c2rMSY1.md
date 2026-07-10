## Summary

The paper addresses conformal prediction (CP) for time-dependent PDE surrogate models, where exchangeability fails because solution distributions drift over time. The authors prove that in function space, distributions at different times are mutually singular (Theorem 4.1), motivating a turn to discretized settings. For discretized linear PDEs with Gaussian initial conditions, they observe that the solution distribution remains Gaussian (Theorem 4.2), which allows closed-form likelihood ratios for weighted conformal prediction (WCP). Experiments on a family of linear PDEs and a real-world thermography example show the method can maintain coverage where baselines fail. The core idea — using known PDE dynamics to compute importance weights — is conceptually sound and well-motivated.

## Strengths

- **Identifies a genuine and important problem (impact: +6.63).** The paper correctly identifies that exchangeability fails for time-dependent PDE surrogate models, which is a real barrier to applying conformal prediction in scientific ML. The motivating examples (Figures 1 and 2) effectively illustrate the problem.

- **Clean theoretical framing of the function-space obstacle (impact: +9.96).** Theorem 4.1 (mutual singularity of measures at different times for the heat equation) is a crisp, rigorous demonstration of why infinite-dimensional settings are intractable for CP, cleanly motivating the turn to discretized settings. This is a genuine theoretical contribution.

- **Weighted CP is conceptually the right framework (impact: +9.35).** Using the known PDE dynamics (linear-Gaussian structure) to compute density ratios in closed form is a sound idea that no prior work has exploited. The approach is principled and leverages a natural structure.

- **Computational efficiency (impact: +0.03).** The method is orders of magnitude faster than the LSCI baseline (seconds vs ~40 minutes for 5000 samples), which is a practical advantage.

## Weaknesses

### Fatal
None.

### Major

- **Coverage deficit contradicts the claim of exact guarantees (impact: -10.00).** In Table 1, for the most stable case tested (a = -0.005), WCP reports coverage of **0.88** at timestep 15 and **0.85** at timestep 20 against a 90% target, with n_∞ at 0.0% and 0.2% respectively — essentially all samples receive finite bands. The paper's explanation ("When n_∞ approaches roughly 90%, WCP shows a slight drop in empirical coverage") does **not** apply here, since n_∞ is near zero. This is a systematic 2–5 percentage point undercoverage in the most benign regime, directly contradicting the paper's central claims of "exact coverage guarantees" (abstract) and "consistently meets its coverage guarantees" (Section 5, Results). Weighted CP with correctly specified likelihood ratios should provide exact coverage; the fact that it does not here needs explanation. The paper must either explain why this occurs (numerical errors in matrix exponentials? discretization error in the Gaussian assumption?) or adjust its claims.

- **Scope is restricted to linear PDEs while the framing overstates generality (impact: -9.98).** Theorem 4.2 requires a linear spatial differential operator with linear boundary conditions and Gaussian (or location-scale) initial conditions. Many practically important PDEs — Navier-Stokes, shallow-water equations, reaction-diffusion with nonlinear terms — are nonlinear. While the discussion section acknowledges this, the abstract claims the method applies to "a broad class of PDE problems" and the introduction claims "exact coverage guarantees for PDEs without limiting assumptions on their time-dependent behavior," both of which overstate the scope. The experiments test only one PDE family that is linear by construction, with no nonlinear benchmarks (not even Burgers' equation).

### Minor

- **Infinite bands in unstable regimes limit practical utility (impact: -9.79).** In Table 1, for a = -0.0075, n_∞ reaches 86.4% at timestep 15 and 100% at timestep 20; for a = -0.01, n_∞ reaches 35.4% at timestep 10 and 100% by timestep 15. While the paper frames this as honest uncertainty reporting, the method is uninformative precisely when uncertainty quantification is most needed. The paper does not report coverage *including* infinite bands (which would trivially be 1.0), making it hard to assess overall utility.

- **Theorem 4.2 is a standard result, not a novel contribution (impact: -9.39).** The statement that the solution to du/dt = Au + r(t) with Gaussian initial condition remains Gaussian is a textbook result from linear systems theory (an affine transformation of a Gaussian is Gaussian). The paper would benefit from more modest framing of this point.

- **Weak real-world validation in the main text (impact: -9.68).** The real-world example (pulsed thermography) receives only one sentence: "Our method achieves target coverage over all tested time steps." No coverage numbers, bandwidths, n_∞, or comparisons appear in the main text. Details are deferred to the appendix. For evaluating a real-world claim, the main text should include at least a summary of key results.

- **Single surrogate model with an unverified claim (impact: -9.97).** The paper uses only one base model (geometry-informed neural operator) and claims "the choice of surrogate model is not important for downstream analysis" without any ablation. Different surrogate models have different error structures that could affect CP residuals; this claim needs empirical support.

## Nice-to-Haves

- Report coverage metrics both with and without infinite bands to give a complete picture.
- Include a discussion of the computational cost of computing the matrix exponential exp(tA) for high-dimensional discretizations.
- Ablate with at least one additional surrogate model (e.g., standard FNO, PINN) to test the claim that model choice is unimportant.
- Include an adaptive conformal inference baseline (e.g., Gibbs & Candès 2021) for a stronger comparison, though this is outside the paper's stated focus on exact finite-sample guarantees.
- Add a sensitivity analysis for approximately linear dynamics or approximately Gaussian initial conditions.

## Removed Points

These points from the input review are flagged to be removed — treat them with caution:

- *LSCI baseline tuning criticism*: The harsh critic claimed pushing LSCI to over-coverage is a "strange experimental choice" that is unfair. This is a misunderstanding — pushing LSCI to be more conservative gives it an advantage; if it still undercovers, this strengthens the comparison. **Removed as factually incorrect.**
- *Unspecified Gaussian parameters*: The critic claimed the paper "does not specify how the Gaussian parameters (μ_t, Σ_t) are obtained." This is factually incorrect — Theorem 4.2 provides explicit closed-form formulas. **Removed.**
- *Weight interpretation (u_i in Equation 1)*: The critic questioned whether u_i refers to predicted or true values. The context and the weighted CP framework make clear that u_i refers to the PDE solution values at calibration/test points, used as covariates. **Removed.**
- *Missing adaptive conformal inference baseline*: Requesting Gibbs & Candès (2021). The paper's focus is on exact finite-sample guarantees using PDE-specific structure. Omission is acceptable given the stated scope. **Removed as scope creep.**
- *Missing computational cost analysis*: Requesting O(n³) analysis of matrix exponential. A reasonable nice-to-have but not a core weakness; empirical cost comparison with LSCI is provided. **Demoted to nice-to-have.**
- *Missing sensitivity to approximate Gaussian dynamics*: Requesting analysis for approximately linear dynamics. A reasonable future direction but within stated scope limitations. **Removed as scope creep.**
- *Pure formatting/style nitpicks and missing-appendix references*: Removed per filtering rules (the parser strips appendix content; the original submission includes it).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Address the coverage deficit.** The 0.88/0.85 coverage for a=-0.005 (n_∞≈0%) directly contradicts the "exact guarantees" claim. Investigate whether this is due to numerical errors in computing matrix exponentials, discretization errors in the Gaussian assumption, or finite-sample effects. If the cause is identifiable, describe it and propose remediation; if not, adjust the claims accordingly.
2. **Report coverage including infinite bands.** Present two numbers: coverage over all test points (treating infinite bands as coverage=1) and the fraction of test points with finite bands. This gives a complete picture of the method's operational behavior.
3. **Tone down scope claims.** Replace "broad class of PDE problems" and "without limiting assumptions" with language that accurately reflects the method's assumptions (linear PDEs, Gaussian/location-scale initial conditions).
4. **Include real-world results in the main text.** At minimum, provide coverage, bandwidth, and n_∞ for the thermography experiment in a table or figure.
5. **Ablate the surrogate model.** Test at least one additional surrogate model (e.g., standard FNO, DeepONet, PINN) to support the claim that model choice is unimportant.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `aJ3tiX1Tu4.md` (Wasserstein-Regularized CP) | 6.67 | R1 | Yes | Stronger theory (novel Wasserstein decomposition), cleaner evaluation; our paper is weaker |
| `4vPVBh3fhz.md` (PAC Prediction Sets Under Label Shift) | 6.40 | R1 | Yes | Stronger contributions (novel algorithm with PAC guarantees); our paper is weaker |
| `33XGfHLtZg.md` (Conformal Risk Control) | 7.00 | R1 | Yes | Significantly stronger in both theory and experiments |
| `cF6OoaYcRa.md` (Calibrated Physics-Informed UQ) | 4.50 | R2 | Yes | Closely related (CP for PDE surrogates); our paper is stronger (has theory, baselines, more experiments) |
| `k2gGy2hpfx.md` (Adapting Prediction Sets) | 3.67 | R2 | Yes | Heuristic method with no guarantees; our paper is much stronger |
| `RcNzwKrjTo.md` (CP with Trust Scores) | 5.00 | R2 | No | Relevant but not directly comparable |
| `fzZfju8y0g.md` (In-Context Neural PDE) | 3.40 | R1 | No | Different focus (neural PDE solvers, not CP) |
| `Nfd7z9d6Bb.md` (Probabilistic CP) | 6.00 | R1 | No | Stronger CP theory, but different setting |
| `Dtxc7mlKRg.md` (Class-Conditional CP) | 4.60 | R3 | No | Different domain (classification imbalance) |
| `GQhlM0Mavg.md` (OOD Detection and CP) | 5.00 | R3 | No | Different focus |
| `PRKFRzOEq8.md` (CP from Noisy Labels) | 5.40 | R3 | No | Different setting |

**Bracket (Round 1):** Between 4.5 and 6.0.

**Narrowing (Round 2):** Our paper is clearly stronger than the 4.50 anchor (Calibrated Physics-Informed UQ) — we provide theory, baselines, and more extensive experiments. But it is weaker than the 6.40–6.67 anchors (PAC Prediction Sets, Wasserstein-regularized CP) — those papers have genuinely novel theory and cleaner evaluations, while our paper's central claim is undermined by the coverage deficit and Theorem 4.2 is a standard result.

**Final score:** 4.5. The paper identifies a real problem and proposes a conceptually sound approach, but the coverage deficit in the most benign test case directly contradicts the central claim of "exact coverage guarantees," and the method's scope (linear PDEs only) is narrower than the abstract and introduction suggest. These issues, combined with the modest theoretical novelty of Theorem 4.2, place the paper in the borderline-reject range.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>