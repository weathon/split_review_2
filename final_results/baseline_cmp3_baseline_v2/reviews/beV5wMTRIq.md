## Summary

The paper proposes PA-TFNP, a neural PDE framework for climate and weather forecasting that combines a tensor field neural operator (claimed to be rotation-equivariant), a spherical-transform-based gradient operator with physically consistent boundary conditions, and diffusion terms inspired by the atmospheric primitive equations. The model is evaluated on global and regional weather prediction tasks using the ERA5 dataset and compared primarily against ClimODE, reporting improvements of up to 78.92% in RMSE.

## Strengths

- **Addresses geometric distortions on the sphere**: The paper correctly identifies that standard CNNs on latitude-longitude grids cause distortions near the poles and that a rotation-equivariant architecture could mitigate this issue.
- **Incorporates physically motivated components**: The inclusion of spherical-gradient corrections, proper boundary conditions, and diffusion/drag terms is a principled step toward bridging data-driven and physics-based modeling.
- **Clear ablation on physics-awareness**: The comparison between TFNP and PA-TFNP (Figure 4) shows that adding the physics-informed components improves long-term stability, supporting the value of the proposed modifications.

## Weaknesses

### Fatal

1. **The claimed rotation-equivariant tensor field network is not correctly formulated.**  
   The definition of \(f_{TFN}\) in Section 3.2 (Equation (3)) is a pointwise bilinear operation over channels:  
   \[
   f_{TFN}(I[i, c_{out}]) = \sum_{c_1,c_2} W[c_{out},c_1,c_2]\,(I[i,c_1]\cdot I[i,c_2]).
   \]  
   This operation does not involve any spatial interactions or spherical harmonics, and it is applied independently to each grid point \(i\). Such a pointwise operation is not rotation-equivariant in the sense required for spherical fields—it simply mixes channels at the same location. No mechanism (e.g., spherical harmonic filtering, Clebsch-Gordan tensor products, or message passing on the sphere) is provided that would actually make the representation transform covariantly under rotations of the sphere. The paper’s central claim of “rotation-equivariant tensor-field neural operators” is therefore unsupported by the described implementation, invalidating a core contribution.

### Major

1. **Insufficient comparison with state-of-the-art neural weather models.**  
   The paper compares only with ClimODE, ClimaX, and a vanilla Neural ODE. No comparisons are made with widely recognized and more powerful models such as FourCastNet, Pangu-Weather, GraphCast, or Aurora. Given that the paper claims “state-of-the-art performance,” the absence of these baselines makes this claim unsubstantiated.

2. **Significant performance degradation on a key variable.**  
   For 2-meter temperature (\(t2m\)) in regional forecasting (Table 1), PA-TFNP is dramatically worse than ClimODE at multiple lead times (e.g., 6h Australia: 2.42 vs. 0.80). The paper dismisses this as a “trade-off,” but such a large error on a primary meteorological variable contradicts the overall narrative of superior accuracy and undermines the credibility of the results.

3. **No isolation of individual contributions.**  
   The ablation study (Figure 4) only compares TFNP (the base tensor-field model) with PA-TFNP (which adds all physics components simultaneously). The effects of the spherical gradient correction, the boundary-condition padding strategies, and the additional physics features are not disentangled. Consequently, it is impossible to attribute gains to any specific design choice.

4. **Missing essential experimental details.**  
   The paper does not state the number of parameters, training time, inference time, or the exact architecture of the Tensor Field Network (e.g., number of layers, feature dimensions). Without this information, the claim of “comparable number of parameters” to ClimODE cannot be verified, and the method cannot be reliably reproduced.

### Minor

- The performance improvements of 38.12% (daily) and 78.92% (hourly) are reported without explaining how these percentages are computed (e.g., average over which variables or lead times).
- The attention component \(f_{att}\) is mentioned but never described or ablated; its contribution to the overall model is unclear.
- The “modified primitive equation” (Section 3.3) adds diffusion and drag terms in a heuristic manner; the connection to the actual atmospheric primitive equations is only superficial.
- Some variable names and formatting errors (e.g., “Koehkov” instead of “Kochkov”) are present, though minor.

## Nice-to-Haves

- An ablation isolating the spherical gradient (+boundary conditions) from the physics features would strengthen the analysis.
- Including state-of-the-art baselines (even at the coarse resolutions used) would validate the claim of state-of-the-art.
- A quantitative evaluation of rotational equivariance (e.g., measuring equivariance error under random rotations) would support the core claim.

## Novel Insights

None beyond the paper’s own contributions. The idea of using tensor-field networks for weather forecasting is a plausible direction, but the paper does not demonstrate that its specific implementation achieves true rotation equivariance or that it significantly outperforms strong modern baselines.

## Suggestions

1. Provide a correct and detailed description of the rotation-equivariant architecture. If a proper TFN (with spherical harmonics and equivariant tensor products) is used, the paper must describe it mathematically and cite the relevant works (Thomas et al., Weiler et al., Kondor et al.) correctly. If the current pointwise bilinear operation is intended to be the full network, then the claim of equivariance must be retracted or justified with a different argument.
2. Benchmark against at least one widely used modern model (e.g., FourCastNet, GraphCast) at the same spatial resolutions to substantiate the state-of-the-art claim.
3. Ablate the spherical gradient, boundary conditions, and physics features separately (three ablations plus the full model) to identify which component drives the improvement.
4. Report parameter counts, training/inference times, and full architecture details.

## Score and Decision

Given the fatal flaw in the formulation of the core rotation-equivariant component and the lack of comparison with modern baselines, the paper does not meet the threshold for acceptance in its current form.

**Score**: 3

**Decision**: Reject

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>