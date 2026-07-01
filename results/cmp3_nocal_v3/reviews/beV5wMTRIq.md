## Summary

This paper proposes PA-TFNP, a neural PDE forecasting framework for climate/weather prediction that extends ClimODE with three modifications: (1) a pointwise quadratic layer (called a "Tensor Field Network") with an attention mechanism, (2) a spherical gradient correction with physically consistent boundary conditions, and (3) physics-inspired diffusion and momentum correction terms. The work targets genuine limitations in ClimODE's naive finite-difference handling of spherical geometry.

---

## Strengths

1. **The spherical gradient correction (Eq. 3) is physically correct and addresses a genuine limitation of ClimODE.** Incorporating the `cos(φ)` factor in the longitudinal derivative is standard in geoscience but absent from ClimODE, and fixing it should reduce polar artifacts. This is a well-motivated, concrete improvement.

2. **The boundary-condition padding (Neumann and average padding) is a principled fix** for the unphysical behavior ClimODE exhibits near the poles in Figure 2c. Circular padding in longitude and Neumann/average padding in latitude are standard but missing from ClimODE, and their inclusion is a clear improvement.

3. **The paper reports standard deviations in Tables 1 and 2** rather than point estimates alone, which provides useful information about variability.

---

## Weaknesses

### Major

1. **The "Tensor Field Network" does not correspond to the cited literature.**  
   The paper defines its TFN (Eq. 3.2, line 75) as a pointwise quadratic transformation applied independently at each spatial location *i*:  
   `f_TFN(I[i, c_out]) = Σ Σ W[c_out, c_1, c_2] (I[i, c_1] · I[i, c_2])`  
   The input is reshaped to `N × C_in`, treating each grid point independently. This operation has no spatial convolution, no spherical-harmonic features, no Clebsch-Gordan tensor products, and no type-*l* representations — which are the defining characteristics of the Tensor Field Networks it cites (Thomas et al., 2018; Weiler et al., 2018; Kondor et al., 2018). Real TFNs achieve rotation equivariance through kernel constraints operating on spatial neighborhoods. The proposed operation is trivially rotation equivariant because it processes each grid cell independently — a property shared by *any* pointwise function. While the overall model includes an attention mechanism (`f_att`) that provides some spatial context, the named "Tensor Field Network" component itself is misrepresented relative to the cited works. This undermines the paper's central methodological claim (abstract, contribution list 1, Section 3.2).

2. **The paper's own tables contradict the claim that PA-TFNP "consistently outperforms" baselines.**  
   **Table 1** shows PA-TFNP **losing to ClimODE** on multiple variable/lead-time combinations:
   - **t2m** at 6h: ClimODE 0.80 vs PA-TFNP 2.42 (Australia), ClimODE 1.33 vs 1.73 (S. America)
   - **t2m** at 12h: ClimODE 1.10 vs PA-TFNP 2.98 (Australia), ClimODE 1.04 vs 2.37 (S. America)
   - **t** at 6h S. America: ClimODE 0.97 vs PA-TFNP 1.01
   - **u10** at 6h: ClimODE beats PA-TFNP in both regions
   - **v10** at 6h: ClimODE beats PA-TFNP in both regions

   **Table 2** similarly contradicts the claim:
   - **z, Month 2**: TFNP (527.07) beats PA-TFNP (562.39)
   - **t, Month 2**: TFNP (2.42) beats PA-TFNP (2.44)
   - **u10, Month 1**: ClimaX (1.80) beats PA-TFNP (1.83)
   - **u10, Month 2**: ClimaX (1.92) beats PA-TFNP (2.32)
   - **v10, Month 2**: ClimaX (1.71) beats PA-TFNP (1.91)

   The abstract and Figure 3 caption claim improvements of "78.92%" and "38.12%" over ClimODE, but these aggregate numbers are never derived or explained — no definition of the metric, variables included, lead times, or computation method is provided. Given that the tabular data show multiple cases where PA-TFNP performs worse, these headline numbers are uninterpretable and potentially misleading.

3. **The evaluation omits comparisons against the SOTA models the paper itself cites.**  
   The Related Works section (Section 2, line 31) discusses FourCastNet, Pangu-Weather, and GraphCast as "state-of-the-art neural forecasting approaches." Yet the experimental section compares only against ClimODE, ClimaX, and a plain NODE. The abstract claims "state-of-the-art performance" without having evaluated against any of these models. This is a severe evidential gap.

4. **Parameter counts and computational-resource claims are unsubstantiated.**  
   The abstract claims PA-TFNP achieves results "with a comparable number of parameters" to ClimODE, and Section 1 claims it "demand[s] significantly fewer computational resources." **No parameter counts, FLOPs, wall-clock times, or any efficiency metric are reported anywhere in the paper.** The only hardware mention is "a single RTX 4090 GPU" with no comparison against baseline runtimes on the same hardware. These claims are unverifiable.

### Minor

5. **The ablation study is too coarse to attribute improvements.**  
   The ablation (Section 4.4) compares only TFNP vs. PA-TFNP, which bundles together five distinct components: (a) boundary conditions, (b) spherical gradient correction, (c) physics-derived features (wind magnitude, lapse rate, vorticity), (d) diffusion term, (e) momentum correction with geopotential gradient, viscosity, and drag. There is no component-wise ablation. Without this, it is unclear which modifications drive the reported improvements.

6. **Spatial resolution is described incorrectly.**  
   Section 4.1 (line 148) describes the 5.625° grid as "coarse" and the 11.25° grid as "finer." In standard convention, 5.625° (≈ 2048 grid points) is *finer* than 11.25° (≈ 512 grid points). This is the opposite of what the text states. While this error does not affect the experimental results themselves, it suggests confusion about a basic experimental-design detail.

### Trivial

None.

---

## Nice-to-Haves

- **Individual ablations** of the five physics components would let readers understand which parts of PA-TFNP contribute most to the improvements.
- **Comparisons against at least one SOTA neural weather model** (e.g., FourCastNet at comparable resolution) would substantiate the "state-of-the-art" claim.
- **Reporting parameter counts and training cost** would support the efficiency claims made in the abstract and introduction.

---

## Removed Points

These are points from the input review that were removed per the filtering rules:

1. **"No code or data release is mentioned"** — Removed per hard rules on reproducibility nitpicks; code at submission time is not required.
2. **"Standard training details are missing"** — Removed because the paper states details follow Verma et al. (2024) and Appendix B; the appendix is stripped by the parser and assumed to exist in the original submission.
3. **"The TFN has no spatial interaction at all"** (as a claim about the whole model) — Weakened: the overall model includes an attention mechanism (`f_att`) that provides spatial context; the TFN component itself is pointwise, but the full `f_η = f_TFN + f_att` is not purely pointwise.
4. **"Motivation is sound"** (strength) — Too generic to keep as a substantive strength.
5. **"Reports standard deviations"** — Partially kept as strength 3; the reviewer correctly noted this, and it is concrete.

---

## Novel Insights

The key insight from cross-referencing the reviews is that the paper's claimed contributions operate at two different levels of validity: the spherical gradient correction and boundary-condition improvements are concrete, verifiable fixes to ClimODE's known limitations, while the "Tensor Field Network" framing is a misnomer for what is actually a pointwise quadratic layer. The evaluation tables show a more nuanced picture than the paper's narrative — PA-TFNP wins convincingly on some variables (geopotential, temperature at longer leads) but loses on surface temperature and wind at short leads. This pattern, if honestly presented, could be the basis for a useful discussion about when physics-aware corrections help and when they hurt.

---

## Suggestions

1. **Rename or redesign the "Tensor Field Network."** Either implement an actual rotation-equivariant operator with spatial kernels (as the cited TFN papers do), or rename the component to something honest (e.g., "pointwise quadratic layer" or "bilinear fusion layer") and reposition the rotation-equivariance claim to apply to the overall pipeline (spherical gradient + boundary conditions + model architecture) rather than the TFN component specifically.

2. **Derive the 78.92% and 38.12% numbers transparently.** Specify exactly over which variables, lead times, and metric these improvements are computed, and reconcile them with the tabular results that show PA-TFNP losing on several metrics.

3. **Report parameter counts** for all compared models and either provide a runtime comparison or remove the unsupported efficiency claims.

4. **Tone down the "consistently outperforms" language** to accurately reflect the results: PA-TFNP outperforms ClimODE on most variables at longer lead times but underperforms on some surface variables at short leads.

---

## Score and Decision

**MY FINAL SCORE:** <score>3</score>
**MY FINAL DECISION:** <decision>Reject</decision>