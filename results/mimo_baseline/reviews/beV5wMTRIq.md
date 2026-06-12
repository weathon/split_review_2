## Summary

This paper proposes PA-TFNP, a weather/climate forecasting framework that replaces CNNs with rotation-equivariant tensor field neural networks operating on spherical data, adds physically consistent boundary conditions and spherical gradient operators, and incorporates diffusion dynamics derived from the atmospheric primitive equations. The method is evaluated on ERA5 data across global, regional, and monthly-averaged forecasting tasks, claiming substantial improvements over ClimODE.

## Strengths

- **Well-motivated architectural choice**: Replacing CNNs with tensor field networks to handle rotation equivariance on spherical data addresses a genuine geometric deficiency in grid-based approaches. The discussion of how equatorial-axis rotations cause distortions in rectangular projections (Figure 1) is compelling and the ablation in Figure 6 (referenced) showing reduced pole/equator errors supports this.
- **Reasonable physics integration**: The boundary condition strategies (Neumann and average padding), spherical gradient correction (Equation 3), and diffusion augmentation are principled modifications grounded in atmospheric physics. Figure 2c visually demonstrates that the boundary treatment reduces artifacts near the poles compared to ClimODE.
- **Consistent improvements over ClimODE in global forecasting**: Across both coarse (5.625°, 5-day) and fine (11.25°, 6–42h) resolution settings (Figure 3), PA-TFNP shows lower RMSE on most variables at most lead times.

## Weaknesses

### Fatal

None.

### Major

- **Extremely narrow baseline comparisons for the claimed contribution scope**: The paper claims "state-of-the-art performance in global and regional weather prediction" (Abstract), yet the global experiments (Section 4.1) only compare against ClimODE. Major recent systems—GraphCast, Pangu-Weather, FourCastNet, Aurora, GenCast—are entirely absent from the evaluation. The "state-of-the-art" claim cannot be supported with this limited comparison set. This is the paper's most significant weakness.

- **Large and inconsistent standard deviations undermine claimed gains**: In Table 1, PA-TFNP frequently exhibits substantially larger standard deviations than ClimODE (e.g., t2m at 12h in Australia: 2.98±1.50 vs 1.10±0.22; z at 24h: 205.8±59.5 vs 308.2±30.6). High variance in predictions raises questions about the reliability and reproducibility of the claimed improvements. The paper does not discuss or analyze this instability.

- **Mixed results without adequate discussion**: PA-TFNP underperforms ClimODE on t2m at early lead times in regional forecasting (Table 1), and ClimaX sometimes outperforms PA-TFNP on monthly u10 and v10 (Table 2). These mixed results are acknowledged only briefly ("may indicate a trade-off") without proper analysis or investigation of failure modes.

- **Unsubstantiated headline claim**: The abstract's "78.92% on global hourly data" improvement is presented prominently but the paper does not clearly define how this aggregate percentage is computed across variables, or justify why this single number is representative given the heterogeneous performance across variables.

### Minor

- **Insufficient parameter/compute analysis**: The abstract claims a "comparable number of parameters" but no actual parameter counts, FLOPs, or training time comparisons are provided. For a method paper at ICLR, this omission weakens the efficiency argument.
- **Tensor field network formulation is underspecified**: The f_TFN formulation (Equation 3 of the paper) is a simple bilinear operation, but the connection to proper steerable/TN architectures with irreducible representations (Thomas et al., 2018; Weiler et al., 2018) is not made explicit. It's unclear whether the network truly operates on spherical harmonics or simply uses pointwise tensor products on a grid.
- **Learnable physics parameters lack analysis**: The coefficients α(x), ν, γ are introduced but there is no analysis of learned values, spatial patterns, or whether they remain physically interpretable after training.

### Trivial

- The title says "Tensor Field Neural PDE" which conflates "neural PDE" with "neural ODE + spatial discretization via finite differences," which is technically what the method does (Method of Lines).

## Nice-to-Haves

- Compare against at least one recent SOTA model (GraphCast, Pangu-Weather, or Aurora) to validate the state-of-the-art claim.
- Provide a table of parameter counts, inference times, and training costs.
- Analyze the learned diffusion coefficients α(x) and physical parameters to demonstrate physical interpretability.
- Investigate the source of high variance in PA-TFNP predictions, particularly for t2m.

## Novel Insights

The observation that rotation-equivariant architectures can mitigate polar-region distortion artifacts in grid-based weather models is valuable, though it builds on well-known ideas from geometric deep learning. The specific demonstration that combining tensor field networks with physics-informed boundary treatments and diffusion yields improved long-term stability (Figure 4) provides a useful empirical data point for the community, though the novelty of each individual component is limited.

## Suggestions

- Add comparisons with GraphCast/Pangu-Weather/FourCastNet on at least one benchmark to substantiate the SOTA claim.
- Include a systematic ablation isolating the contribution of each component (TFN, boundary conditions, spherical gradients, diffusion, physics features) to understand relative importance.
- Analyze and discuss the high variance problem, which is arguably more important than mean performance for operational forecasting.

## Score and Decision

The paper addresses a meaningful problem with reasonable technical ideas, and the combination of rotation-equivariant networks with physics-aware modifications for spherical weather data is sensible. However, the experimental evaluation is insufficient: comparisons are limited almost exclusively to ClimODE, the standard deviations are troublingly high in many settings, results are mixed without thorough analysis, and the headline claims (state-of-the-art, 78.92% improvement) are not adequately supported. The individual contributions (better padding, spherical gradients, adding diffusion) are reasonable but incremental. The paper needs substantially broader evaluation and deeper analysis to support its claims.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject