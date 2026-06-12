## Summary

The paper proposes Physics-Aware Tensor Field Neural PDE (PA-TFNP), a forecasting framework that combines rotation-equivariant tensor-field neural operators, numerically rigorous spherical gradient operators with physically consistent boundary conditions, and diffusion terms derived from atmospheric primitive equations. The authors claim state-of-the-art performance on global and regional weather prediction tasks, outperforming ClimODE by 78.92% on global hourly data.

## Strengths

- The paper identifies important limitations in current data-driven weather models: lack of geometric fidelity on the sphere, boundary artifacts at poles, and absence of physically grounded diffusion.
- The idea of blending neural predictions with physics-based operators via a time-dependent coefficient (β_t) is conceptually reasonable for improving long-term stability.
- The inclusion of physics-derived features (wind magnitude, lapse rate, vorticity) is well motivated by atmospheric science.

## Weaknesses

### Fatal

- **The core claimed contribution—rotation-equivariant tensor-field neural operators—is not correctly implemented or described.** Equation (3) defines f_TFN as a pointwise bilinear operation: f_TFN(I[i, c_out]) = Σ_{c1,c2} W[c_out, c1, c2] (I[i, c1] · I[i, c2]). This is a simple elementwise quadratic transformation applied independently per spatial location i, with no local aggregation, no spherical harmonic decomposition, and no message passing between grid points. This does not match the cited literature (Thomas et al., 2018; Weiler et al., 2018) which uses steerable representations and equivariant convolutions. The paper provides no proof or empirical demonstration that this bilinear pointwise operation achieves rotation equivariance on the discretized sphere. The architectural claim contradicts the actual mathematical description, invalidating a central contribution of the paper.

- **The claimed 78.92% improvement over ClimODE is unsupported and inconsistent with presented results.** The RMSE plots in Figure 3 show both models producing errors of similar magnitude (e.g., ~1–2 m/s for winds, ~50–100 m²/s² for geopotential). A 78.92% improvement would mean PA-TFNP achieves RMSE roughly 21% of ClimODE’s, which is clearly not reflected in any subfigure. The paper does not explain how this percentage is computed (e.g., relative to a normalized baseline, averaged across variables in some unconventional way), nor does it provide the raw numbers for verification. This constitutes a misleading performance claim that undermines the paper’s credibility.

### Major

- **Insufficient comparison to state-of-the-art models.** The baseline set is limited to ClimODE, ClimaX, and a simple Neural ODE. Widely recognized state-of-the-art weather models such as GraphCast (Lam et al., 2023), Pangu-Weather (Bi et al., 2023), FourCastNet (Kurth et al., 2023), and Aurora (Bodnar et al., 2024) are not included. Claiming “state-of-the-art performance” without comparing to the strongest published baselines is a significant omission.

- **The experimental resolution (5.625° and 11.25°) is extremely coarse** for modern weather forecasting. Most operational and research models operate at resolutions of 0.25°–1°. Operating at such coarse resolution limits the practical relevance of the results and may mask instabilities that would appear at higher resolution.

- **Parameter counts are not reported** despite claiming “comparable number of parameters.” Without these numbers, the fairness of the comparison cannot be assessed.

### Minor

- The paper does not discuss cases where baselines outperform PA-TFNP (e.g., in Table 2, ClimaX achieves lower RMSE than PA-TFNP for u10 and v10 at months 1 and 2). Such selective reporting weakens the empirical narrative.
- The ablation study comparing ClimODE vs TFNP conflates architectural changes (tensor field + attention) with rotation equivariance, making it an improper ablation for isolating the effect of equivariance.

## Nice-to-Haves

- Clarify the exact implementation of the tensor field network: if it is indeed a pointwise bilinear layer, rename it accordingly and remove misleading references to spherical harmonic expansions. If a genuine equivariant convolution was intended, provide the correct formulation and prove its equivariance.
- Include comparisons to strong recent baselines (GraphCast, Pangu-Weather) at comparable resolutions and provide parameter counts for all models.
- Report raw numerical RMSE values with confidence intervals for all experiments and justify the 78.92% improvement claim with traceable calculations.
- Evaluate at higher operational resolutions (e.g., 1°) to demonstrate real-world applicability.

## Novel Insights

None beyond the paper's own contributions. The physics-inspired modifications (diffusion terms, blended neural-physical tendencies) are reasonable engineering additions but do not constitute a fundamentally new insight for the community.

## Suggestions

- Resolve the discrepancy between the claimed rotation-equivariant architecture and the actual pointwise bilinear operation described in Equation (3). Either provide the correct equivariant formulation with theoretical guarantees, or retract the equivariance claim and reposition the contribution.
- Remove or fully justify the unsupported 78.92% improvement figure. Provide the raw RMSE values used to compute any percentage improvements.
- Add comparisons to modern data-driven weather models (GraphCast, Pangu-Weather, Aurora) to substantiate state-of-the-art claims.
- Report parameter counts and training/inference computational cost for all compared methods.

## Score and Decision

MY FINAL SCORE: 3.0</score>
MY FINAL DECISION: Reject</decision>