Now let me write the final consolidated review.

## Summary

This paper proposes PA-TFNP, a neural PDE framework for weather and climate forecasting that combines spherical-aware gradient operators, physically consistent boundary conditions at the poles, and physics-derived diffusion terms. The model is built on the ClimODE baseline and adds a "Tensor Field Network" component for rotation-equivariant processing, along with boundary padding strategies and physics-informed features (wind magnitude, lapse rate, vorticity).

## Strengths

- **Clear problem identification (+8.9).** The paper correctly identifies two genuine issues with neural weather models on latitude-longitude grids: geometric distortions near the poles caused by non-uniform Euclidean distances on the sphere, and boundary artifacts from improper treatment of the poles (Sections 3.2–3.3).

- **Valid spherical gradient correction (+9.2).** Equation (3) provides a principled central-difference scheme with the cos φ latitude correction factor and Earth's radius R, combined with circular padding in longitude and Neumann/average padding at the poles. This is a concrete improvement over ClimODE's naive flat-Earth gradients.

- **Honest limitations section (+4.5).** The paper acknowledges that rotation-equivariance offers limited benefit for regional forecasting and that a single diffusion equation applied uniformly to all variables is physically inappropriate (Section 5).

## Weaknesses

### Fatal
None.

### Major

- **TFN architectural claim unsupported (-9.7).** The "Tensor Field Network" described in Section 3.2 (equation on line 75) is a **per-location bilinear (quadratic) layer** — a pointwise operation applied independently at each grid cell *i*. It has no spatial structure, no spherical harmonic filters, no Clebsch-Gordan decomposition, and no steerable kernel basis. These are the defining characteristics of a Tensor Field Network as introduced by Thomas et al. (2018), Weiler et al. (2018), and Kondor et al. (2018) — the very papers the authors cite. The claimed rotation-equivariant processing that is central to the paper's title, abstract, and contributions list is not supported by the provided formulation. The attention mechanism *f_att* provides the only spatial interaction. This is not a missing ablation; it is a mismatch between the claimed method and its description that undermines the paper's core thesis.

- **'State-of-the-art' claim unsupported by evaluation (-9.8).** The paper compares against NODE, ClimaX, and ClimODE only, yet its own related work section cites GraphCast (Lam et al., 2023, *Science*), Pangu-Weather (Bi et al., 2023, *Nature*), FourCastNet, Aurora, and NeuralGCM as relevant. Claiming "state-of-the-art performance in global and regional weather prediction" (abstract, conclusion) without comparison against these published benchmarks — or at minimum acknowledging the gap — is not justified.

- **Headline improvements unverifiable (-6.3).** The abstract claims PA-TFNP "outperforms ClimODE by 78.92% on global hourly data" and "38.12% on daily data" (also line 156), but **no global RMSE table is provided** in the main paper. Only regional tables (Tables 1, 2) and qualitative Figure 3 plots are given. The paper does not explain how these aggregate percentages are computed (averaged over which variables? at which lead times?), making these headline numbers impossible to verify or reproduce from the presented results.

- **Missing component-level ablations (-4.2).** The TFNP vs PA-TFNP comparison (Figure 4) shows overall benefit but does not ablate individual innovations — spherical gradient vs flat gradient, boundary padding vs none, TFN vs no TFN, physics features vs none, diffusion terms vs none. Without this, it is impossible to determine which component drives the observed improvements.

### Minor

- **Very coarse experimental resolutions (-4.6).** Global experiments use 5.625° (~625 km) and 11.25° (~1250 km). Modern operational models run at 0.25° (~30 km) or finer. The paper does not acknowledge this limitation or justify the chosen resolutions relative to operational forecasting standards, despite framing its results as relevant to "climate and weather prediction."

- **Inconsistent performance across settings (-2.4).** PA-TFNP underperforms ClimODE on t2m at 6h, 12h, and 18h for Australia and South America (Table 1, e.g., t2m at 6h for Australia: 2.42 vs 0.80). In monthly forecasting (Table 2), TFNP (without physics) sometimes beats PA-TFNP — for z at month 2 (527.07 vs 562.39) and t at month 2 (2.42 vs 2.44). The paper acknowledges some of these issues, but they nonetheless caveat the overall claims.

- **Only RMSE reported (-1.1).** The Anomaly Correlation Coefficient (ACC), a standard metric in atmospheric science, is absent, making cross-comparison with the broader literature difficult.

- **Parameter counts not reported (-0.4).** The abstract states PA-TFNP uses a "comparable number of parameters" to ClimODE, but no actual parameter counts are given.

### Trivial
None.

## Nice-to-Haves

- Clarify what the TFN component actually is — either present a genuine TFN implementation (with irreducible representations, steerable kernels, Clebsch-Gordan products) or rename/reframe the component to avoid misleading terminology.
- Add component-level ablations isolating: spherical vs flat gradient, boundary padding vs none, TFN vs no TFN, physics features vs none, diffusion terms vs none.
- Add at least one modern baseline comparison (e.g., GraphCast at the same coarse resolution) or temper the "state-of-the-art" claim.
- Report the Anomaly Correlation Coefficient (ACC) alongside RMSE.
- Report parameter counts and training hyperparameters.

## Removed Points

These points from the input review are removed, treat them with caution:
1. Claim that 78.92% improvement is "inflated" — removed as speculative; the numbers are unverifiable but not proven wrong.
2. Figure caption repetition complaint — removed as a formatting/parsing artifact.
3. "Each variable having its own velocity field is not physics" — removed as a critique of the inherited ClimODE framework, not a flaw of this paper.
4. "Circular dependency in modified primitive equation (z used in velocity equation)" — removed as a misunderstanding; this is a standard coupled PDE system in atmospheric physics.
5. Missing Appendix references — removed per guidelines (appendix stripped by parser).
6. "Boundary conditions are standard in geophysics" — removed; the paper does not claim novelty of individual padding schemes but their application in this neural PDE context.
7. Missing training hyperparameters — removed per guidelines (deferred to appendix, parser-stripped).
8. "Overgeneralization about physics-agnostic methods" — removed as a typical introduction framing, not a substantive weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe or redesign the "Tensor Field Network" component — either implement a genuine TFN with rotation-equivariant steerable kernels, or rename the per-point bilinear layer to avoid the misleading architectural claim.
2. Provide a table of global RMSE values so the 78.92% and 38.12% claims can be verified, with a transparent explanation of how aggregate percentages are computed.
3. Add at least one modern baseline (e.g., GraphCast at the same coarse resolution) or temper the "state-of-the-art" framing throughout.

## Score and Decision

The paper has genuine engineering value in its spherical-gradient correction and boundary treatment — both clear improvements over the ClimODE baseline. However, the paper's central architectural claim (rotation-equivariant Tensor Field Network) is unsupported by the provided formulation, the headline quantitative results are unverifiable, and the "state-of-the-art" framing is not justified by the narrow evaluation against ClimODE alone. Taken together, these issues mean the paper in its current form cannot be accepted.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>