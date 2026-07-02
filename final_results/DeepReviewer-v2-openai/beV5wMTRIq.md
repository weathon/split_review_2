## Summary
# Final Review Report

## Summary

This paper proposes PA-TFNP (Physics-Aware Tensor Field Neural PDE), a hybrid forecasting framework that combines neural operators with physics-inspired PDE components for climate and weather prediction. The method builds on ClimODE's Method-of-Lines + Neural ODE formulation and adds three core innovations: (i) a rotation-equivariant tensor-field network (TFN) replacing CNNs for the neural operator $f_\eta$, (ii) a latitude-corrected finite-difference gradient operator with physics-informed boundary padding (Neumann and average padding), and (iii) learnable diffusion and blended physical momentum terms derived from the atmospheric primitive equations.

The paper evaluates PA-TFNP against ClimODE, ClimaX, and a vanilla NODE on the ERA5/WeatherBench dataset across global, regional, and monthly settings. The results show consistent RMSE reductions for thermodynamic variables (geopotential height z, temperature t, 2m temperature t2m) particularly at longer lead times, with the headline claim of 78.92% improvement over ClimODE on hourly global data.

**Strengths:** The spherical rotation-equivariant operator is a sound motivation for addressing polar distortion. The latitude-corrected gradient and boundary padding are practically useful refinements to the finite-difference scheme. The ablation study (TFNP vs PA-TFNP) usefully isolates the effect of the physics augmentation.

**Key weaknesses identified in this audit:**
1. The TFN formulation (Eq. 4) is a per-point bilinear channel mixer, not a proper rotation-equivariant tensor field network as claimed — a critical architectural discrepancy.
2. The spherical gradient operator (Eq. 3) has inconsistent latitude-longitude spacing and is missing a factor of 2 in the central difference denominator; the polar singularity ($\cos\phi = 0$ at poles) is unaddressed.
3. The 78.92% improvement claim is poorly specified and appears inconsistent with individual variable gains; the comparison lacks several strong neural weather baselines (GraphCast, Pangu-Weather, FourCastNet, NeuralGCM).
4. PA-TFNP is 2–3$\times$ worse than ClimODE for t2m at short lead times, with no causal analysis or mitigation.
5. The conclusion overclaims generalization to other scientific domains and uses "state-of-the-art" without sufficient comparative evidence.

Due to Retrieval-Disabled Mode, external literature verification was not possible in this run; novelty and positioning judgments are deferred for manual verification. The above findings are based entirely on manuscript-internal audit.

## Strengths
**1. Well-motivated spherical geometry awareness.** The paper correctly identifies that CNN-based neural PDE operators on flattened latitude-longitude grids suffer from polar distortion and are not rotation-equivariant. The motivation for using spherical tensor-field representations is scientifically sound and addresses a genuine limitation in existing neural weather models. This geometric inductive bias is the paper's most distinctive conceptual contribution.

**2. Practical boundary-condition refinement.** The introduction of physical padding strategies (Neumann and average padding) for finite-difference stencils on the sphere, combined with circular padding in longitude, is a practically useful contribution. Figure 2 qualitatively demonstrates reduced boundary artifacts compared to ClimODE, and the approach is simple to implement in existing neural PDE frameworks.

**3. Clean ablation design.** The two-level ablation (TFNP vs ClimODE isolates rotation-equivariant TFN; PA-TFNP vs TFNP isolates physics augmentation) provides clear attribution of which component contributes what. The TFNP-based results showing improved polar-region accuracy support the rotation-equivariance claim qualitatively.

**4. Comprehensive evaluation across settings.** The paper evaluates at three distinct horizons (short-term 6-42h, medium-term 5-day, seasonal 2-month) and two regions (global, regional). This multi-scale evaluation demonstrates the method's stability across resolution and lead time regimes, which is stronger evidence than a single-setting benchmark.

**5. Transparent limitation discussion.** The limitations section honestly acknowledges that rotation-equivariance offers limited benefit for regional forecasting and that variable-specific equation modifications are needed. This self-awareness strengthens the paper's credibility, even though the limitations section could be more comprehensive.

**6. Competitive computational cost.** All experiments use a single RTX 4090 GPU, which is modest by modern standards. The "comparable parameter count" claim, while lacking exact numbers, suggests the method does not achieve gains through brute-force scaling — a desirable property for adoption in resource-constrained settings.

## Weaknesses
The weaknesses are presented in descending order of severity, following the Ranked Error Board established during audit.

### Critical

**W1. TFN architecture does not implement claimed rotation-equivariant tensor field network.**
*Page 3 - Section 3.2 (TFNP formulation)*

The paper claims to use a Tensor Field Network (TFN) from Thomas et al. (2018) to achieve rotation equivariance. However, the presented formulation in Eq. (4) is a per-point bilinear channel mixer:
$$f_{TFN}(I[i, c_{out}]) = \sum_{c_1, c_2} W[c_{out}, c_1, c_2] (I[i, c_1] \cdot I[i, c_2])$$

This operation has no spatial neighborhood aggregation, no spherical harmonic expansion, no Clebsch-Gordan tensor products, and no SO(3) group convolution — all core mechanisms that define a Tensor Field Network. The described operation is a simple pointwise quadratic transformation that is not rotation-equivariant in any non-trivial geometric sense.

**Impact:** This is a core claim of the paper (Contribution C1). If the TFN is not actually rotation-equivariant, the paper's central technical contribution is unsupported, and the claimed gains may originate from other factors (e.g., the latitude-corrected gradient, attention mechanism, or simply increased parameter count). The qualitative polar-region improvement shown in Figure 6 could be equally explained by the spherical gradient correction rather than the TFN.

**Required action (Must):** Either (a) provide the full TFN implementation including spherical harmonic features, neighbor aggregation, and equivariance proof, or (b) rename the operation to "bilinear channel mixing" and provide a separate justification for rotation handling (e.g., through data augmentation or spherical interpolation). The latter would significantly reduce the claimed contribution.

---

**W2. Spherical gradient operator (Eq. 3) contains numerical errors and an unaddressed polar singularity.**
*Page 5 - Section 3.3 (Spatial Derivative Approximation)*

Equation (3) defines the gradient approximation as:
$$\nabla q_i((\phi, \lambda), t) \approx \left( \frac{q_i((\phi + h, \lambda), t) - q_i((\phi - h, \lambda), t)}{Rh\pi/180}, \frac{q_i((\phi, \lambda + w), t) - q_i((\phi, \lambda - w), t)}{Rh\pi \cos \phi/180} \right)$$

Three issues are identified:

(i) **Missing factor of 2:** Central difference for uniform spacing $h$ should be $(q(\phi+h) - q(\phi-h)) / (2h)$. The denominator uses $Rh\pi/180$ instead of $2Rh\pi/180$. The same applies to the longitudinal term.

(ii) **Inconsistent spacing variable:** The longitudinal (second) component uses $h$ (latitude spacing) in the denominator instead of $w$ (longitude spacing). The correct form should use $w$ in place of $h$ for the $\lambda$-derivative.

(iii) **Polar singularity unaddressed:** At $\phi = \pm 90^\circ$, $\cos\phi = 0$, causing division by zero in the longitudinal gradient. The text claims "all points within the domain are treated as interior points" but does not explain how this singularity is handled.

**Impact:** The gradient operator is used throughout the PDE solve. Errors in Eq. (3) will propagate through the entire advection-diffusion computation, potentially corrupting the forecast. The polar singularity means the model cannot compute valid gradients at the poles as described.

**Required action (Must):** Correct Eq. (3) to:
$$\nabla q_i((\phi, \lambda), t) \approx \left( \frac{q_i((\phi + h, \lambda), t) - q_i((\phi - h, \lambda), t)}{2R \cdot h\pi/180}, \frac{q_i((\phi, \lambda + w), t) - q_i((\phi, \lambda - w), t)}{2R \cos\phi \cdot w\pi/180} \right)$$
and add an explicit handling of the polar singularity (e.g., set longitudinal gradient to zero at $\phi = \pm 90^\circ$).

---

### Major

**W3. 78.92% improvement claim is opaque and potentially misleading.**
*Page 1 - Abstract; Page 6 - Section 4.1*

The abstract claims "outperforming ClimODE by 78.92% on global hourly data." The same number appears in Figure 3's caption without specifying: (a) which metric (RMSE? MAE? a composite?); (b) whether this is an average across all 5 variables or a single best variable; (c) whether it is averaged over all lead times or at a specific horizon. Individual variable RMSE plots in Figure 3 show more modest variable-specific gains (typically 15–40% for z and t, and mixed for t2m). A gain of 78.92% in RMSE would mean PA-TFNP's error is ~21% of ClimODE's, which is an order-of-magnitude larger improvement than what the individual plots suggest.

Furthermore, the comparison omits several strong neural weather baselines (GraphCast, Pangu-Weather, FourCastNet, NeuralGCM) that are cited in the introduction. Without these comparisons, "state-of-the-art" claims are unsupported.

**Required action (Must):** Provide a precise breakdown of what 78.92% represents: the exact formula, the variables and lead times included in the average, and individual gains per variable. Replace "state-of-the-art" with bounded comparative claims. Add at least one cross-paper comparison with a recent neural weather model under comparable settings.

---

**W4. PA-TFNP is 2–3$\times$ worse than ClimODE for 2-meter temperature at short lead times, with no causal analysis.**
*Page 7 - Section 4.2, Table 1*

For t2m at 6h, PA-TFNP achieves RMSE 2.42 (Australia) vs ClimODE's 0.80, and 1.73 vs 1.33 (South America). This pattern persists at 12h and 18h. The paper dismisses this as "underperforms at earlier lead times" without analysis.

**Impact:** t2m is the most operationally relevant variable for end users. A model that is 3$\times$ worse on t2m is not practically usable, regardless of gains on other variables. The lack of root-cause analysis (e.g., bias/variance decomposition, spectral analysis, error spatial maps) means reviewers cannot evaluate whether this is a fundamental limitation or a fixable calibration issue.

**Required action (Must):** (a) Replace euphemistic language with direct reporting of the failure magnitude. (b) Add diagnostic analysis: is the error bias or variance? Is it concentrated in specific regions (coastal, mountainous)? Does the learnable diffusion oversmooth the surface field? (c) Report results with a t2m-specific configuration (e.g., reduced diffusion coefficient) if that resolves the issue.

---

**W5. Related work section lacks critical comparative positioning.**
*Page 1 - Section 2*

The Related Work section does not describe how ClimODE (the primary baseline) works, what its limitations are, and how PA-TFNP specifically addresses them. The Physics-Informed ML paragraph dismisses most related work as "smaller-scale fluid systems" while citing NeuralGCM [Kochkov et al., 2024] — which operates at global scale — without discussing its relevance. The Deep Learning for Forecasting paragraph lists methods without analyzing their limitations relative to the proposed approach.

**Required action (Must):** Add a dedicated paragraph on ClimODE describing its MOL+NeuralODE formulation and its specific limitations (flat-grid distortion, no rotation-equivariant operators, missing boundary conditions). Discuss NeuralGCM's hybrid approach and clarify differences. Reorganize the section by comparison axes (e.g., grid typology, physics integration method, equivariance properties) rather than paper-by-paper summaries.

---

**W6. Modified primitive equation lacks reproducibility-critical hyperparameters and unit scaling.**
*Page 5 - Section 3.3 (Modified Primitive Equation)*

The blended momentum equation uses $\beta_t = 1 - \exp(-t/\tau_0)$ but $\tau_0$ is not reported. The learnable diffusion coefficient $\alpha(\mathbf{x})$ is a $d \times H \times W$ tensor with no spatial regularization, risking noisy localized values. The geopotential gradient $-\nabla \Phi$ uses $\Phi = z$ directly without unit scaling (geopotential height has units $m$ or $m^2/s^2$, while wind tendency needs $m/s^2$).

**Required action (Must):** Report $\tau_0$ and its sensitivity. Add spatial regularization for $\alpha(\mathbf{x})$. Normalize geopotential by gravitational acceleration $g_0 = 9.81$ m/s² so that $-\nabla(z / g_0)$ has correct units.

---

**W7. Selective reporting in monthly forecasting results.**
*Page 8 - Section 4.3, Table 2*

The text states "PA-TFNP consistently outperforms other benchmarks" but Table 2 shows ClimaX has lower RMSE than PA-TFNP for u10 at both Month 1 (1.80 vs 1.83) and Month 2 (1.92 vs 2.32), and for v10 at Month 2 (1.71 vs 1.91). Similarly, TFNP outperforms PA-TFNP for t at Month 2 (2.42 vs 2.44). These counterexamples are not acknowledged, giving an incomplete picture.

**Required action (Must):** Add a fair assessment: "For wind components, ClimaX achieves competitive or superior RMSE in the monthly setting, suggesting the physics augmentation provides limited benefit for dynamic variables at seasonal timescales."

---

### Minor

**W8. Conclusion overclaims generalization and SOTA status.**
*Page 8 - Section 5*

"We anticipate that the mathematical principles introduced here will generalize across a broad range of scientific computing domains" is speculative and unsupported. The paper only evaluates weather forecasting on ERA5.

**Action (Nice-to-have):** Remove or significantly soften to: "The approach may extend to other PDE-constrained geophysical prediction tasks, though this remains to be demonstrated."

---

**W9. Duplicate equation numbering.**
*Page 2 - Section 3.1*

The system ODE approximation and the integral solution both carry the label "(2)." The loss function reference to "Sections 3.7 and 3.8 of (Verma et al., 2024)" is not self-contained.

**Action (Nice-to-have):** Fix numbering; add a concise description of the loss function in the main text.

---

**W10. Title is overly generic.**
*Page 1*

"Physics-Aware Tensor Field Neural PDE for Climate and Weather Prediction" describes the method but not the problem or result.

**Action (Nice-to-have):** Consider a more specific title: "Rotation-Equivariant Tensor Field Neural PDE for Global Weather Forecasting with Latitude-Corrected Spherical Gradients."

## Score
**Final Score: 4/10**

**Scoring rationale:**

The paper presents a well-motivated approach for incorporating spherical geometry and physics-aware operators into neural PDE-based weather forecasting. However, the score is significantly constrained by two critical issues that undermine the core technical claims:

1. **Architecture-claim mismatch (critical):** The tensor-field network formulation presented in Eq. (4) is a per-point bilinear channel mixer, not a proper rotation-equivariant TFN. The claimed rotation-equivariance property is not substantiated by the provided equations. This affects Contribution C1 — the paper's most distinctive selling point.

2. **Gradient operator errors (critical):** Equation (3) contains a missing factor of 2, inconsistent spacing variables, and an unaddressed polar singularity. These errors affect the core physics-aware computation (Contribution C2).

Additionally, major weaknesses in result reporting (opaque 78.92% claim, missing t2m analysis, selective reporting in monthly results) and reproducibility (missing hyperparameters, unit scaling) further reduce confidence.

**Score breakdown:**
- **Research value & novelty:** 4/10 — The spherical rotation-equivariance motivation is sound and the latitude-corrected gradient is a practical improvement, but the TFN implementation does not match the novelty claim, and the most distinctive algorithmic contribution is not correctly described. External literature verification was not performed in this run (Retrieval-Disabled Mode), so novelty versus the strongest baselines remains unverified.
- **Validity & soundness:** 3/10 — Two critical mathematical errors (TFN formulation, gradient operator) directly affect core claims. Until these are resolved, the validity of the reported results cannot be fully assessed.
- **Empirical evidence:** 4/10 — The evaluation is multi-scale and partially informative, but the t2m degradation, selective reporting in monthly results, and opaque aggregate improvement metric reduce evidentiary quality.
- **Reproducibility:** 3/10 — Missing hyperparameter ($\tau_0$), loss function defined only by external reference, unregularized diffusion coefficient, and unit scaling issues prevent independent reproduction.
- **Presentation & clarity:** 5/10 — The writing is generally clear and the figures are informative, but the related work lacks comparative positioning, the conclusion overclaims, and the organizational narrative could be tighter.

**Expected revision impact:** If the TFN formulation is corrected or honestly recharacterized, the gradient operator is fixed, and the reporting issues are addressed, the paper could achieve a score in the 6-7/10 range — reflecting a solid but incremental contribution in neural PDE-based weather forecasting.