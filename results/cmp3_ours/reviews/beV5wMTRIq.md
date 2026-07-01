## Summary

PA-TFNP extends the ClimODE neural-ODE framework for weather forecasting with three physics-motivated modifications: (1) a spherical-gradient correction that accounts for latitude-dependent longitudinal spacing; (2) padding-based boundary conditions at the poles and periodic longitude; and (3) diffusion terms, physics-derived features (wind magnitude, lapse rate, vorticity), and a hybrid neural-physics velocity blending inspired by the primitive equations. The model is evaluated on global, regional, and monthly forecasting tasks against ClimODE, ClimaX, and a vanilla Neural ODE baseline.

## Strengths

1. **Spherical gradient correction (Equation 3).** The latitude-dependent longitudinal scaling factor 1/(R h π cos φ / 180) correctly addresses a known deficiency in naive finite-difference gradients on lat-lon grids. This is a clean, well-motivated improvement over ClimODE's default scheme and is the paper's most defensible technical contribution. [Line 114]

2. **Physical boundary padding.** The two padding strategies (circular in longitude, Neumann/average at the poles) are physically grounded. Circular padding correctly handles the periodic longitudinal domain, and the pole treatments plausibly reduce edge artifacts — the qualitative error maps in Figure 2c support this. [Lines 100–108]

3. **Physics-derived features and hybrid blending.** The addition of wind magnitude, lapse rate, vorticity, and the time-dependent blending of neural predictions with a physics-based operator is a sensible approach to improving long-term stability. The ablation (Figure 4) shows PA-TFNP outperforming TFNP at extended horizons, which is consistent with the stated goal. [Lines 118–138]

## Weaknesses

### Fatal

None.

### Major

1. **The "Tensor Field Network" formulation does not implement rotation equivariance as claimed.** This is the paper's most serious problem. The Abstract and Section 3.2 claim "rotation-equivariant tensor-field neural operators" and that the approach is "inherently rotation equivariant," citing Thomas et al. (2018), Weiler et al. (2018), and Kondor et al. (2018) — the foundational papers on TFNs and steerable CNNs, which use spherical harmonics, Clebsch-Gordan tensor products, and steerable filter convolutions. However, the actual formulation (Equation 4) is:

   $$f_{TFN}(I[i, c_{out}]) = \sum_{c_1=1}^{C_{in}} \sum_{c_2=1}^{C_{in}} W[c_{out}, c_1, c_2] (I[i, c_1] \cdot I[i, c_2]), \quad \forall i \in [N].$$

   This is a **per-point bilinear self-interaction**: for each grid point i, it computes pairwise products of input channels at that same point and linearly recombines them. There is no spatial convolution, no spherical-harmonic basis, no Clebsch-Gordan decomposition, no steerable filtering, and no message passing between points. The weight tensor W is shared across spatial locations, making the operation translationally uniform on the grid — but this is permutation equivariance (treating each grid point identically), not rotation equivariance on the sphere. The terms "spherical harmonics," "irreducible representations," and "steerable filters" never appear in the paper. The claimed advantage over CNNs ("cannot capture rotation-equivariant properties") is not theoretically justified by the architecture as described. [Lines 61–77]

   **Impact**: This undermines the paper's primary architectural contribution. The experimental improvements cannot be attributed to rotation-equivariant processing without evidence that the architecture implements it.

2. **Headline improvement figures lack definition and supporting data.** The abstract and Figure 3 claim "outperforming ClimODE by 78.92% on global hourly data" and "38.12% on daily data." These are very large claimed improvements, but: (a) the paper never states how these percentages are computed (per-variable average? RMSE reduction averaged over all lead times? relative to which configuration?); (b) no numerical RMSE tables are provided for the global experiments — only line plots; (c) standard deviations and confidence intervals are absent for the global results. The absence of raw numerical data for the experiment that produces the headline claim is a significant omission. [Lines 9, 156]

3. **Insufficient baseline comparison for "state-of-the-art" claims.** The global experiments compare only against ClimODE. The paper's own Related Work (Section 2) discusses GraphCast, Pangu-Weather, FourCastNet, and Aurora as "state-of-the-art neural forecasting approaches," yet none appear in the experiments. Claiming "state-of-the-art performance" while comparing against a single baseline (ClimODE) is an overclaim. Even if exact reproduction at equivalent resolution is constrained, the absence of any of these stronger baselines prevents the reader from assessing where PA-TFNP actually stands. [Lines 142–150]

4. **Mixed results undercut the narrative of uniform superiority.** Table 1 shows several settings where PA-TFNP underperforms ClimODE substantially:
   - **t2m at 6h Australia**: PA-TFNP = 2.42 ± 0.70 vs. ClimODE = 0.80 ± 0.13 (~3× higher RMSE)
   - **t2m at 12h Australia**: PA-TFNP = 2.98 ± 1.50 vs. ClimODE = 1.10 ± 0.22
   - **v10 at 6h South America**: PA-TFNP = 1.68 ± 0.39 vs. ClimODE = 1.30 ± 0.21
   - PA-TFNP's standard deviations on t2m are 2–5× larger than ClimODE's, suggesting substantially higher variance.

   In the monthly forecasting (Table 2), the base TFNP outperforms PA-TFNP on geopotential at month 2 (527.07 vs. 562.39) and temperature at month 2 (2.42 vs. 2.44). ClimaX outperforms both TFNP and PA-TFNP on u10 and v10 at month 2. These results do not support the blanket claim of "superior performance through strict physical fidelity." [Lines 166–215]

### Minor

1. **Incomplete specification of learned components.** The diffusion coefficient α(x) is described as "learnable" but how it is parameterized (per-grid-point parameter? small network?) is not specified. The blending time constant τ₀ in β_t = 1 − exp(−t/τ₀) is never defined or discussed. [Lines 126–134]

2. **No computational cost reporting.** The abstract claims the model "demands significantly fewer computational resources," but no wall-clock training time, inference speed, parameter counts, or memory usage are reported anywhere. Only the GPU type (RTX 4090) is noted. [Line 144]

3. **Selective uncertainty reporting.** In Table 1, NODE and ClimaX results are reported without standard deviations, while ClimODE and PA-TFNP include them, making it impossible to assess whether differences with NODE and ClimaX are significant. [Lines 166–189]

### Trivial

None.

## Nice-to-Haves

- A stepwise ablation isolating the individual contributions of each physics-aware component (spherical gradient, boundary padding, diffusion, physics features, velocity blending) rather than the bundled TFNP vs. PA-TFNP comparison in Figure 4.
- Clarification of the monthly-averaged forecasting protocol: how are two-month averages computed from forecasts at what temporal resolution?

## Removed Points

These points were flagged for removal with brief justification:

- *"ClimODE was published in ICLR 2024 and is likely not the strongest available baseline"* — Speculative. However, the concrete absence of GraphCast/Pangu-Weather/FourCastNet as experimental baselines is kept as a Major weakness.
- *"No appendix available"* — The parser strips appendices from all papers; not a valid weakness.
- *"Missing hyperparameters, data split years, etc."* — Paper defers to Verma et al. (2024) and Appendix B; missing implementation details from a stripped appendix are not a valid weakness per review guidelines.
- *"The average padding hardcodes 64"* — 64 is the number of longitude points at 5.625° resolution (360/5.625 = 64); not a design flaw.
- *"The t2m results show a trade-off between local variance and longer-horizon stability"* — The paper already acknowledges this interpretation explicitly in Section 4.2.
- *"f_phys = −∇Φ + νΔu − γu has no guarantee of physical meaningfulness"* — f_phys is a standard simplified momentum equation; the paper uses it as a correction term blended with neural predictions, not a standalone replacement.
- *Formatting nitpicks about figure descriptions, parser artifacts.*
- *Strengths about "the problem being important" or generic claims* — Removed as insufficiently specific to the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Address the TFN claim.** Either provide evidence that the bilinear layer in Equation (4) is part of a larger rotation-equivariant pipeline (e.g., by showing how it connects to spherical harmonics or steerable filters, consistent with the cited TFN papers), or revise the claims to accurately describe what is implemented (e.g., "pointwise bilinear feature interaction" rather than "rotation-equivariant tensor-field operator").

2. **Define and support the headline figures.** Provide the formula for the 78.92% and 38.12% improvement figures, along with the underlying numerical RMSE data with uncertainty for the global experiments.

3. **Add stronger baselines or temper claims.** Include at least one well-established baseline (e.g., GraphCast or Pangu-Weather at comparable resolution) or drop the "state-of-the-art" claim in favor of a more nuanced comparison.

4. **Report per-component ablations.** The current TFNP vs. PA-TFNP ablation bundles boundary conditions, spherical gradients, physics features, diffusion, and velocity blending together. A stepwise ablation would clarify which component drives the improvements.

5. **Provide computational cost metrics.** Report parameter count, training time, inference speed, and memory usage to substantiate the efficiency claim.

## Score and Decision

**Calibration anchors used (listed for transparency):**

| Anchor Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| WeatherODE | UFzE9njwMG.md | 3.60 | 1 | Neural ODE weather model, ~40% improvement claims, similar baseline scope. This paper has the same limitations plus a more serious claim-implementation gap. |
| PASSAT | o6tO1rUcQe.md | 3.50 | 2 | Physics-assisted spherical GNN for weather. Reviewers flagged that physical components showed minimal impact in ablation — analogous to this paper's TFN claim gap. |
| PhyDL-NWP | QMkYEau02q.md | 4.25 | 1 | Physics-guided weather forecasting. Stronger evaluation but still lacking SOTA baselines. |
| PACE | 7fuddaTrSu.md | 3.00 | 1 | Physics-informed climate emulator with Neural ODE. Had clarity and support issues. |
| CirT | YslOW2SO6S.md | 6.00 | 1 | Geometric innovation with proper SOTA baselines (GraphCast, Pangu-Weather). Accepted — clearly superior evaluation. |

**Bracket determination:** Round 1 bracketing placed the paper between 2.5 and 4.5 based on similarity to WeatherODE (3.60) and PASSAT (3.50). Round 2 examination of PASSAT more closely confirmed the pattern: a paper with a genuine motivation and some good ideas, but a central claim that is not supported by the presented evidence and insufficient baselines.

**Final score rationale:** The paper has real, well-motivated ideas (spherical gradient correction, boundary padding, physics-derived features). However, the core architectural claim — rotation-equivariant processing via a Tensor Field Network — is not supported by the mathematical formulation provided (Equation 4 is a per-point bilinear layer, not a rotation-equivariant operator in the sense of the cited TFN papers). Combined with insufficient baseline diversity, undefined headline improvement metrics, mixed empirical results, and missing supporting data, the paper does not currently substantiate its claims. These are fixable issues, but in its present form the evidence does not support acceptance.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>