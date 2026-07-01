## Summary

This paper studies uncertainty quantification for surrogate models of time-dependent PDEs via conformal prediction. It proves that in the function-space setting, solution distributions at different times are mutually singular (Theorem 4.1), making standard CP impossible. For discretized linear PDEs with Gaussian initial conditions, it derives the closed-form Gaussian distribution of the solution (Theorem 4.2), which enables closed-form likelihood-ratio weights for weighted conformal prediction. Experiments on synthetic linear PDEs and one real-world dataset demonstrate coverage properties against naive CP and LSCI baselines.

## Strengths

- **Theorem 4.1 (mutual singularity in function space) is a clean, non-obvious theoretical result.** It rigorously demonstrates that even for a simple PDE (heat equation), the total variation distance between solution distributions at arbitrarily close times is maximal (d_TV = 1), proving that function-space CP is theoretically impossible and grounding the practical necessity of discretization in a formal argument rather than computational convenience.

- **The identification that linear PDEs with Gaussian ICs yield closed-form Gaussian densities for the discretized solution (Theorem 4.2) is mathematically sound and directly enables the CP weighting scheme.** The derivation of μ_t and Σ_t via the method of lines is correct, and the use of these densities for likelihood-ratio weights connects PDE structure to CP machinery in a clean, principled way.

- **The critique of existing CP approaches for time-dependent PDEs (trajectory-level exchangeability, LSCI's unverifiable local exchangeability) is accurate and well-supported** by the backward heat equation example (Figure 2), which concretely demonstrates why prior methods fail.

## Weaknesses

### Fatal

None.

### Major

1. **Scope and framing overreach relative to the actual method.** The title ("Time-Dependent PDEs"), abstract ("a broad class of PDE problems"), and contributions ("without limiting assumptions on their time-dependent behavior") all suggest broad applicability. In reality, the method requires: (a) a *linear* PDE (Theorem 4.2 requires the spatial operator ℒ_x to be linear and the finite-difference matrix **A** to be independent of time), (b) Gaussian (or location-scale) initial conditions, and (c) knowledge of the analytical PDE form to construct **A**. The linear-PDE restriction is noted once in the Discussion, but the Gaussian IC requirement is never acknowledged as a limitation. Most practically important PDEs (Navier-Stokes, Burgers, reaction-diffusion with nonlinear sources) are excluded. This framing mismatch makes the paper less informative for readers trying to assess whether the method applies to their problem.

2. **Missing theoretical justification for the weighted CP validity in this particular PDE setting.** The paper frames the weighting as a covariate-shift problem (Section 3.1) but computes weights from the density of the *solution* u_t — which is the target variable, not a covariate. For weighted CP with importance weights to provide exact coverage, one needs the conditional distribution of the score given the weighted variable to be invariant between calibration and test (i.e., p(score | u_t) should be the same at times t and t+δ). The paper does not state this condition, does not argue why it should hold for surrogate model errors, and does not test it empirically. While the assumption may be plausible, its absence from the theoretical development is a gap that could affect whether the coverage guarantees are valid in the intended setting.

3. **Minimal real-world validation in the main paper.** The real-world experiment (pulsed thermography, the only evaluation on data not generated from the paper's own assumptions) receives only one sentence in Section 5. All details are relegated to the appendix. At minimum, a summary table or figure showing coverage on real data should appear in the main paper.

### Minor

4. **Infinite bands in the most challenging regimes limit practical usefulness.** Table 1 shows that for a = −0.0075 (timestep 15), WCP produces 86.4% infinite bands; for a = −0.01, it produces 100% infinite bands at timesteps 15 and 20. The method "achieves target coverage" by refusing to predict — which is mathematically honest but means no useful uncertainty interval is provided exactly when the dynamics are most unstable. This trade-off deserves more prominent discussion, including practical guidance on when finite intervals can be expected.

5. **Empirical coverage sometimes falls below the target in moderate regimes.** At a = −0.005, timestep 20, WCP reports coverage 0.85 (below the 0.9 target) with only 0.2% infinite bands — the paper's explanation about "higher stochastic noise due to small remaining sample size" does not apply here, since 99.8% of samples remain. While the formal guarantee holds in expectation over the weighted procedure, this empirical deviation warrants explanation.

6. **No comparison against a direct Gaussian-interval baseline.** Since Theorem 4.2 provides the exact Gaussian (μ_t, Σ_t) of the *true solution*, one could construct Gaussian prediction intervals from this distribution directly. Although such a baseline would measure uncertainty in the solution rather than in the surrogate (so it is not a direct competitor), including it would clarify what value the CP machinery adds beyond the known Gaussian.

### Trivial

7. Table 1 reports only the mean bandwidth; reporting the distribution (e.g., standard deviation or percentiles) would be more informative, since the score is a maximum over space.

## Nice-to-Haves

- The function-space analysis (Theorem 4.1 and surrounding discussion, several paragraphs) is interesting but the paper itself admits it is "not necessarily problematic for practical CP on surrogate models." It could be condensed to make room for the real-world experiment.
- For unstable PDE regimes where WCP gives infinite bands, providing guidance in terms of the TV distance or density-ratio magnitude between calibration and test distributions would help practitioners anticipate when the method will produce finite intervals.

## Removed Points

These points from the input review were removed with justification:

- **"CP is redundant because the Gaussian distribution is already known"** — REMOVED. This misreads the paper's goal: the Gaussian describes the *ground-truth solution distribution*, while CP quantifies uncertainty in the *surrogate model's* errors, whose distribution is unknown. The known Gaussian is used only to compute importance weights. The paper could be clearer about this distinction (see Weakness #6), but the core criticism is invalid as a fatal flaw.
- **"LSCI was adversarially configured to over-coverage"** — REMOVED. The paper's stated choice to "push LSCI to over-coverage" means making bands wider (more conservative), which is generous to LSCI rather than adversarial. This gives LSCI the best chance to perform well.
- **"Reproducibility details are thin (discretization scheme, grid resolution)"** — REMOVED per policy: the appendix (which would contain these details) is stripped by the PDF-to-text parser and exists in the original submission.
- **"The weight formula is ambiguous about whether weights are computed for calibration and test points collectively"** — REMOVED. The paper states "for all u_i belonging to the calibration set together with the target test point," which is clear.
- **Various formatting/style nitpicks and "the paper should include X" without specific anchor** — REMOVED.

## Novel Insights

The key insight from combining the review perspectives is that the paper's real contribution is a *template* for making conformal prediction work for time-dependent surrogate models when the underlying physical process has tractable distributional structure. The specific instance (linear PDEs + Gaussian ICs) has limited scope, but the blueprint — (1) prove mutual singularity in function space to justify discretization, (2) exploit the PDE's closed-form distribution for importance weights, (3) apply weighted CP to the surrogate's residuals — is extensible to other tractable families (e.g., linearized approximations of nonlinear PDEs, Gaussian process emulators, SDEs with known transition densities). The mutual singularity theorem (Theorem 4.1) is the most conceptually novel piece and is well-deployed to motivate the discrete approach.

## Suggestions

1. Revise the title and abstract to reflect the actual scope — e.g., "Weighted Conformal Prediction for Linear Time-Dependent PDEs with Gaussian Initial Conditions."
2. Explicitly state and justify the conditional invariance assumption needed for weighted CP in this setting: that the surrogate model's error distribution given the solution u is (approximately) invariant across time. If theory is unavailable, provide an empirical test on held-out calibration data.
3. Move the real-world experiment (at minimum a summary table) from the appendix into the main paper.
4. Add a baseline that constructs intervals from the known Gaussian (μ_t, Σ_t) directly and clarify why CP adds value beyond it.
5. Discuss the practical implications of infinite-band behavior more prominently, including guidance for practitioners on when the method is likely to produce useful finite intervals.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>