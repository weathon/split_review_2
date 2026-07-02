## Summary

The paper proposes PA-TFNP, a physics-informed extension of ClimODE for weather/climate forecasting. The claimed innovations are: (1) a rotation-equivariant tensor-field neural operator on the sphere, (2) a spherical-transform gradient operator with physical boundary conditions, and (3) diffusion dynamics derived from atmospheric primitive equations. The method is evaluated on ERA5 at resolutions of 5.625° and 11.25°, comparing against ClimODE, ClimaX, and a basic Neural ODE.

## Strengths

- **Spherical gradient correction (Eq. 3) is physically meaningful.** Accounting for the varying Euclidean distance of longitudinal differences at different latitudes via the 1/cos(φ) factor corrects a genuine oversight in ClimODE's naive finite differences on a lat-lon grid.

- **Boundary padding strategies address a real failure mode.** The Neumann and average padding schemes at the poles (Section 3.3, Figure 2) directly target the boundary artifacts visible in ClimODE near the poles. The motivation is well-reasoned and the fix is clearly described.

## Weaknesses

### Fatal

None.

### Major

- **The Tensor Field Network is mis-specified and does not deliver rotation equivariance as claimed.** The paper claims a "rotation-equivariant tensor-field neural operator" (abstract) citing Thomas et al. (2018) and Weiler et al. (2018). However, Eq. (75) reveals a **per-point bilinear layer** applied independently at each spatial location *i*:

  $$f_{TFN}(I[i, c_{out}]) = \sum_{c_1} \sum_{c_2} W[c_{out}, c_1, c_2] (I[i, c_1] \cdot I[i, c_2]), \quad \forall i \in [N]$$

  There is no spatial convolution, no message passing between grid points, no spherical harmonics, and no Clebsch-Gordan tensor products — the defining components of a Tensor Field Network in the cited literature. The input is simply reshaped from raw atmospheric grid data into N × C_in with no featurization into irreducible representations of SO(3). A per-point bilinear map does not provide rotation equivariance in any meaningful sense for spherical data. This is not a minor naming issue: the paper's central architectural novelty — rotation-equivariant processing on the sphere — is not supported by the formulation presented.

- **Unsupported "state-of-the-art" claims and narrow evaluation.** The abstract and conclusion claim "state-of-the-art performance," yet the paper only compares against ClimODE, ClimaX, and a basic Neural ODE. Major baselines cited in the related work — GraphCast (Lam et al., 2023), Pangu-Weather (Bi et al., 2023), FourCastNet (Pathak et al., 2022), and NeuralGCM (Kochkov et al., 2024) — are never evaluated against. The evaluation at 11.25° (32×16 = 512 grid points for the entire globe) is far below the resolutions at which these models operate. The SOTA claim cannot be justified from the evidence presented.

- **Overclaimed physics enforcement.** The introduction states that existing models "struggle to enforce fundamental conservation laws, such as mass or energy conservation, and lack mechanisms to maintain incompressibility" (lines 14–15), and the conclusion claims the model incorporates "divergence-free conditions" (line 227). However, the method (Section 3.3) implements **none of these** — no conservation law, no divergence-free constraint, no incompressibility enforcement is present anywhere in the architecture or loss function. The actual physics-aware components are sensible (boundary padding, spherical gradient correction, three physics-derived features, a learnable diffusion term, and a time-dependent blending between neural and physical tendencies), but they do not constitute enforcement of conservation laws. The gap between claimed and actual physics is substantial.

- **Regional results contradict the unqualified "consistently outperforms" claim.** The contributions list (line 21) states the model "consistently outperforms the latest benchmark models across diverse climate and weather-prediction tasks" without qualification. Table 1 shows this is false as stated. PA-TFNP is substantially worse than ClimODE on *t2m* at Australia 6h (2.42 vs 0.80), Australia 12h (2.98 vs 1.10), South America 6h (1.73 vs 1.33), and South America 12h (2.37 vs 1.04), and also worse on several *u10* and *v10* entries at short lead times. The paper acknowledges *t2m* underperformance in text (line 190), but the unqualified contribution-level claim is inconsistent with the data.

### Minor

- **The "78.92% improvement" figure is undefined.** The abstract and Figure 3 caption state that "PA-TFNP outperforms ClimODE by 78.92% on global hourly data" but no definition is given for what this percentage represents — average RMSE reduction across variables? Improvement on a single variable? At what lead time? Cannot be verified or interpreted.

- **"Finer resolution" is mislabeled.** Section 4.1 (line 148) describes 11.25° as "a finer resolution" compared to 5.625°. In fact, 11.25° (32×16 grid, 512 points) is 2× coarser per dimension than 5.625° (64×32, 2048 points).

- **Insufficient ablation.** The ablation (Section 4.4) only compares TFNP vs PA-TFNP. There is no isolation of individual components: spherical gradient vs. naive FD, bilinear layer vs. standard CNN, each physics-derived feature, or the attention mechanism. Performance gains cannot be attributed to specific design choices.

- **Missing computational cost and parameter counts.** The abstract claims "comparable number of parameters" to ClimODE, but no actual parameter counts, training time, inference time, or FLOPs are reported.

### Trivial

- The blending parameters τ₀, ν, and γ are not reported, making the hybrid dynamics component irreproducible.

## Nice-to-Haves

- Comparison against a CNN-based version of the same framework would test whether the bilinear layer provides any benefit over standard architectures.
- Statistical significance tests for regional results (many entries show large standard deviations overlapping between methods).

## Removed Points

- **"The problem framing is directionally correct"** (strength) — Generic framing praise, not a concrete strength of the paper's contributions.
- **"Section 4.2 claim of 'consistently outperforms all baselines across all lead times' is false"** (from reviewer's Weakness 4) — The paper actually qualifies this to z and t variables in Section 4.2 (line 160: "particularly for the geopotential height (z) and temperature (t) variables, where it consistently outperforms all baselines across all lead times"), which is accurate for those two variables. The unqualified claim in the contributions list is retained as a Major weakness above.
- **Missing appendix content** — Parser-stripped sections are assumed present in original submission.
- **Missing related works** — Cannot verify as per policy.
- **Formatting/grammar nitpicks** — Parser artifacts.
- **Speculative concerns about confounders** — Not grounded in specific paper content.

## Novel Insights

The reviews surface two observations beyond the paper's own contributions. First, the paper's central architectural claim — a rotation-equivariant tensor-field neural operator — is shown to be unsupported by the mathematical formulation, which is a per-point bilinear layer rather than a proper equivariant architecture. This is not a superficial naming issue: it calls into question whether the model actually provides any equivariance benefit or simply gains capacity from quadratic feature interactions. Second, the pattern of overclaiming (conservation laws, divergence-free conditions, SOTA performance, "consistently outperforms") is systematic rather than isolated, running through the abstract, introduction, contributions list, and conclusion, while the evidence supports weaker claims.

## Suggestions

1. **Fix the TFN description.** Either implement a proper TFN with steerable filters on the sphere, or (more practically) describe the bilinear layer as a per-point quadratic feature interaction layer and remove or correctly qualify the rotation-equivariance claims.
2. **Tone down physics claims.** Replace "conservation laws," "incompressibility," and "divergence-free conditions" with accurate descriptions of what the model actually does.
3. **Define the headline metric transparently.** State what "78.92%" means — which variables, which lead times, numerator and denominator.
4. **Add ablations** isolating the spherical gradient correction, boundary padding, bilinear layer, and each physics-derived feature.
5. **Correct the resolution labeling** (11.25° is not finer than 5.625°).

## Calibration Report

**Round 1 bracket:** 2.0 – 3.5

**Anchors retrieved:**
| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| WeatherODE (UFzE9njwMG) | 3.60 | R1, R2 | Similar Neural ODE weather paper at 5.625°, but has a coherent architecture and more baselines. Our paper is weaker. |
| PASSAT (o6tO1rUcQe) | 3.50 | R2 | Physics-assisted weather model at 5.625° with spherical GNN; compares against GraphCast/Pangu. Stronger evaluation than our paper. |
| PACE (7fuddaTrSu) | 3.00 | R1, R2 | Physics-informed climate emulator with similar overclaiming issues. Comparable quality. |
| Atmospheric Radiation Param. (otXB6odSG8) | 3.00 | R1, R2 | Neural ODE for climate; solid but narrow. Our paper has more issues but broader scope. |
| CoDiCast (j1jtyGdD4O) | 3.50 | R2 | Diffusion for weather; more sophisticated method. |
| ClimGen (sELO2DCCC1) | 3.75 | R2 | Climate forcing-response; reasonable but limited scope. |
| Physics-Guided Learning (QMkYEau02q) | 4.25 | R1 | Better-executed physics-informed weather work. |
| CirT (YslOW2SO6S) | 6.00 | R1 | Strong geometry-informed model with thorough SOTA comparison. Well above our paper. |
| Pangu-Weather (Cjz9Xhm7sI) | 8.00 | R1 | Exceptional work. Not comparable. |

**Final calibration:** Our paper sits below WeatherODE (3.60) and PASSAT (3.50) due to the TFN mis-specification and weaker evaluation, and is comparable to PACE (3.00) and Atmospheric Radiation Parameterization (3.00). The legitimate contributions (boundary padding, spherical gradient) are incremental and outweighed by the architectural misrepresentation and overclaimed physics enforcement.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>