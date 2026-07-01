## Summary

This paper proposes PA-TFNP (Physics-Aware Tensor Field Neural PDE), a framework for climate and weather prediction that combines rotation-equivariant tensor field neural operators on the sphere with physics-informed components including spherical-transform-based gradient operators, physically consistent boundary conditions, and diffusion terms derived from atmospheric primitive equations. The model is evaluated on global and regional weather forecasting tasks using the ERA5 dataset, reporting improvements over ClimODE and other baselines, with claimed gains of 78.92% on hourly data.

## Strengths

- **Geometric awareness through rotation-equivariant architecture**: The use of Tensor Field Networks (TFNs) to handle spherical geometry is a principled approach that addresses the distortion issues near poles that plague standard CNNs on latitude-longitude grids. The paper provides a clear motivation for why rotational equivariance matters for global weather data.

- **Physically motivated boundary conditions**: The introduction of Neumann and average padding strategies for the poles, combined with circular padding for longitude, is a simple yet effective fix for the boundary artifacts observed in ClimODE. The qualitative results in Figure 2c support this improvement.

- **Comprehensive experimental evaluation**: The paper evaluates across multiple settings (global long-term, global short-term, regional, monthly averaged) and provides ablation studies separating the contributions of the tensor field network from the physics-aware components.

## Weaknesses

### Fatal
None.

### Major

- **The claimed 78.92% improvement is misleading and unsupported by the reported results**: The abstract states PA-TFNP "outperforms ClimODE by 78.92% on global hourly data." However, examining Figure 3 (second row, hourly data), the RMSE values for ClimODE and PA-TFNP are on the same order of magnitude (e.g., for z at 6h, ClimODE ~100 vs PA-TFNP ~80). A 78.92% improvement would require PA-TFNP's RMSE to be roughly 1/5 of ClimODE's, which is not reflected in the plots. The paper does not specify which metric or lead time this number corresponds to, making the claim unverifiable and potentially exaggerated.

- **Missing critical baselines and comparisons**: The paper compares only against ClimODE, ClimaX, and a basic Neural ODE. It does not compare against modern, high-performing weather models such as GraphCast, Pangu-Weather, FourCastNet, or Aurora, which are cited in the related work section. While these models may use different architectures, the claim of "state-of-the-art" performance requires comparison with the actual SOTA. The paper also does not report computational cost comparisons (training time, inference speed, parameter counts) against these baselines.

- **The tensor field network implementation appears to be a simple bilinear layer, not a proper TFN**: Equation (3) defines f_TFN as a pointwise bilinear operation (I ⊗ I) with a learned weight tensor W. This is a simple quadratic feature interaction, not a proper Tensor Field Network as defined by Thomas et al. (2018), which involves spherical harmonics, Clebsch-Gordan coefficients, and explicit rotation of features in SO(3) representations. The paper does not describe how rotational equivariance is actually achieved—there is no mention of spherical harmonics, irreducible representations, or how the network transforms under rotations. The claim of "rotation-equivariant tensor-field neural operators" is not substantiated by the provided formulation.

- **The "spherical transform" gradient is just a latitude-corrected finite difference**: Equation (3) is a standard central difference with a cos(φ) correction factor for the longitudinal component. This is a well-known technique in geoscience and is not a "numerically rigorous gradient operator based on spherical transforms" as claimed. There is no spherical harmonic transform, no spectral method, and no rigorous treatment of the spherical Laplacian. The paper overstates the novelty of this component.

- **The physics-aware modifications are ad-hoc and not rigorously justified**: The modified primitive equation introduces a spatially varying diffusion coefficient α(x), a time-dependent blending factor β_t, and a physical operator f_phys with learnable viscosity and drag coefficients. While these are physically motivated, the paper does not provide theoretical justification for the specific functional forms (e.g., why β_t = 1 - exp(-t/τ_0)?), nor does it analyze whether the resulting PDE system preserves important physical properties like conservation laws or energy stability.

### Minor

- **The regional forecasting results are mixed**: For t2m (2m temperature) in Australia, PA-TFNP performs significantly worse than ClimODE at 6h, 12h, and 18h (RMSE 2.42 vs 0.80 at 6h). The paper acknowledges this but does not provide a satisfactory explanation. This suggests the physics-aware components may hurt performance in certain settings.

- **The monthly averaged results (Table 2) show PA-TFNP is not consistently better than TFNP**: For month 2, TFNP outperforms PA-TFNP on t (2.42 vs 2.44) and u10 (2.40 vs 2.32 for PA-TFNP, but ClimaX achieves 1.92). The benefits of the physics-aware components are not uniformly positive.

- **Limited analysis of the diffusion and blending components**: The paper introduces learnable parameters α(x), ν, γ, and τ_0 but does not analyze their learned values, spatial patterns, or sensitivity. This makes it difficult to assess whether the model is learning meaningful physics or simply overfitting.

### Trivial
- The paper states "All experiments were conducted using a single RTX 4090 GPU" but does not report training time, inference speed, or memory usage, which are important for practical deployment.

## Nice-to-Haves

- An analysis of the learned diffusion coefficient α(x) and its spatial pattern would strengthen the claim that the model captures physically meaningful processes.
- Comparison with spectral methods (e.g., spherical harmonic transforms) for computing gradients would clarify the claimed novelty of the gradient operator.
- A discussion of conservation properties (mass, energy) of the proposed PDE system would strengthen the physical fidelity claims.

## Novel Insights

None beyond the paper's own contributions. The combination of rotation-equivariant networks with physics-informed PDE modifications for weather forecasting is a reasonable direction, but the individual components (latitude-corrected finite differences, padding strategies, diffusion terms) are well-established techniques. The paper's main insight—that geometric awareness and physical constraints can improve neural weather models—is not novel in itself, though the specific combination may be.

## Suggestions

1. **Clarify or correct the 78.92% improvement claim**: Specify exactly which metric, lead time, and variable this corresponds to, or remove the claim if it cannot be substantiated.
2. **Provide a proper implementation of Tensor Field Networks** with spherical harmonics and SO(3) equivariance, or rename the component to avoid misleading claims about rotational equivariance.
3. **Add comparisons with modern SOTA models** (GraphCast, Pangu-Weather, FourCastNet) on at least one setting to support the "state-of-the-art" claim.
4. **Report computational costs** (parameters, training time, inference speed) for all models.
5. **Provide ablation studies** isolating the effect of each proposed component (boundary conditions, spherical gradient, physics features, diffusion, blending) to justify the design choices.

## Score and Decision

The paper addresses an important problem and has a reasonable motivation, but it suffers from several significant issues: the core technical claims about rotation-equivariant tensor field networks are not substantiated by the provided formulation, the reported performance gains are not clearly supported by the data, and the experimental evaluation lacks comparisons with actual state-of-the-art models. The physics-aware modifications, while sensible, are not rigorously justified or analyzed. The paper overstates its contributions relative to what is actually demonstrated.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>