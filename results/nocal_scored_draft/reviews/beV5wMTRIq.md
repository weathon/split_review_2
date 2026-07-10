The scoring model confirms the severity pattern — the TFN issue and the three major problems all score 0.00 (strongly negative), while the two strengths score 1.00 (strongly positive). This supports my assessment: the paper has real engineering contributions but a fatal structural flaw in its central claim and multiple overclaiming issues.

Now I will produce the final review.

---

## Summary

This paper proposes PA-TFNP, a framework combining a tensor-field neural operator with spherical gradient corrections, physically consistent boundary conditions, and diffusion terms from atmospheric primitive equations for weather forecasting. The spherical gradient correction and boundary padding are legitimate engineering improvements over the ClimODE baseline. However, the paper's central mechanism — a Tensor Field Network providing rotation equivariance — is described in Eq. 4 as a per-point bilinear operation with no spatial interaction, which cannot deliver the claimed rotation equivariance. Combined with unsubstantiated headline improvement figures (78.92%), overclaimed SOTA status, and mixed physics-awareness results presented as unequivocally positive, the paper's core claims are not supported by the presented evidence.

## Strengths

- **Well-motivated problem framing (Sections 3.2–3.3).** The paper correctly identifies a concrete weakness in CNN-based neural PDE models applied to spherical weather data: geometric distortion near the poles and lack of rotation equivariance. The spherical gradient correction (Eq. 3) with the distance correction factor \(R\pi\cos\phi/180\) is numerically sound. The boundary-condition discussion (circular padding along longitudes, Neumann/average padding at poles) targets a real deficiency in the ClimODE baseline.

- **Sensible ablation design (Section 4.4).** The paper disentangles three axes of contribution — TFN vs CNN (TFNP vs ClimODE), physics-awareness (PA-TFNP vs TFNP), and the intermediate TFNP itself. Table 2 allows comparing all three variants, showing that most of the gain comes from replacing the CNN backbone, not the physics terms.

## Weaknesses

### Fatal

- **The Tensor Field Network as described (Eq. 4) does not implement rotation equivariance — the paper's central claim is unsupported by its own formulation.** Equation 4 defines
  \[
  f_{TFN}(I[i, c_{out}]) = I \otimes I = \sum_{c_1=1}^{C_{in}} \sum_{c_2=1}^{C_{in}} W[c_{out}, c_1, c_2](I[i, c_1] \cdot I[i, c_2]), \quad \forall i \in [N].
  \]
  This is a pointwise bilinear operation applied independently at each grid location \(i\) — it involves no spatial convolution, no interaction between neighboring grid points, no spherical-harmonic filter expansion, and no Clebsch-Gordan tensor products, which are the defining components of a Tensor Field Network (Thomas et al., 2018; Weiler et al., 2018). A per-point function cannot provide rotation equivariance for spatial data because rotating the spatial arrangement of inputs has no effect on an operation that processes each point independently. The paper either misrepresents its implementation or describes an architecture that cannot deliver the claimed equivariance. In either case, the headline claim of rotation-equivariant spherical tensor field operators is unsubstantiated as written. The ablation (Section 4.4) attributes pole-region improvements to "rotation-equivariant architecture," but these improvements could equally be explained by the boundary-condition padding and spherical gradient — both introduced in the PA-TFNP section, not the TFNP section — further confusing the attribution.

### Major

- **The headline improvement figures (78.92% on hourly data, 38.12% on daily data) are stated without derivation or supporting evidence.** The abstract and Figure 3 caption report these numbers, but no explanation is given of which metric, which variables, which lead times, or how they are aggregated. The tabulated results do not obviously support a 78.92% improvement: Table 1 shows improvements typically in the 10–35% range, with ClimODE actually outperforming PA-TFNP on t2m at early lead times and on u10/v10 at 6h across both Australia and South America. An improvement of nearly 80% over a strong baseline would be a remarkable result — it needs to be traceable to specific entries in a table or figure.

- **The paper claims "state-of-the-art" performance while comparing only against ClimODE, ClimaX, and NODE** — all baselines operating at the same coarse resolutions (5.625–11.25°). The Related Works section discusses GraphCast, Pangu-Weather, FourCastNet, and Aurora as more capable models at 0.25° resolution, yet none are compared against. Claiming SOTA without engaging the actual SOTA models overstates the contribution. Additionally, all experiments operate at very coarse resolutions (5.625° and 11.25°, corresponding to roughly 64×32 and 32×16 grids respectively), far coarser than operational forecasting resolutions (0.25°).

- **The physics-awareness contributions show mixed results that are not honestly discussed.** In Table 2, PA-TFNP underperforms the simpler TFNP on z (month 2: 562.39 vs 527.07) and t (month 2: 2.44 vs 2.42), and is tied on t2m (month 2: 2.95 vs 2.95). For u10 and v10 across both months, both TFNP and PA-TFNP are worse than ClimaX in several settings. The paper claims PA-TFNP "consistently outperforms the TFNP model at extended forecast horizons beyond 24 hours, across all scalar quantities" — this is contradicted by the paper's own numerical data. These counterexamples should be acknowledged and discussed rather than glossed over.

### Minor

- **The abstract claims "comparable number of parameters" to ClimODE, but no parameter counts are reported for any model in the paper.** This claim is unverifiable. No inference speed, FLOPs, or training time is reported despite the paper emphasizing efficiency as a contribution.

### Trivial

None.

## Nice-to-Haves

- Sensitivity analysis for the blending schedule \(\beta_t = 1 - \exp(-t/\tau_0)\), the diffusion coefficient \(\alpha(\mathbf{x})\), and viscosity/drag coefficients \(\nu, \gamma\) would improve the paper's depth.
- An empirical test of rotation equivariance (applying a known rotation to the input and checking that outputs are correspondingly rotated) would directly substantiate the equivariance claim.
- The paper would benefit from acknowledging the resolution gap and discussing plans for scaling to finer grids.

## Removed Points

These points were flagged by reviewers but are removed per filtering rules (see justification for each):

- Criticisms about missing training hyperparameters or implementation details likely deferred to the appendix: The paper states "Further details on dataset preprocessing and training settings remain consistent with those in (Verma et al., 2024) and Appendix B." The appendix is stripped by the parser, so these gaps are not verifiable as author omissions.
- "No statistical tests or confidence intervals for global experiments (Figure 3)": The Figure 3 caption states "Results are reported as mean ± standard deviation," contradicting this criticism — standard deviations are claimed to be reported.
- "Modified primitive equation is an exaggeration": A minor naming issue that does not affect the paper's technical validity. The paper describes the specific terms it includes.
- "No evaluation at practically relevant resolutions": Partially scope-creepy. The paper is a proof-of-concept at stated resolutions. The SOTA overclaim concern already captures the issue indirectly.
- Missing sensitivity analysis for hyperparameters: A generic weakness that would strengthen the paper but is not a core flaw. Moved to Nice-to-Haves.
- Criticism about rotation equivariance offering limited benefits for regional forecasting not being acknowledged: The paper explicitly acknowledges this in the Conclusion (Section 5).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the TFN formulation.** Either provide the correct mathematical description of the rotation-equivariant architecture used (including spatial message passing, spherical-harmonic filters, or Clebsch-Gordan tensor products if actually implemented), or rename the operation to something accurate (e.g., "bilinear feature interaction") and do not claim rotation equivariance based on it.
2. **Derive the 78.92% and 38.12% figures.** Show exactly which variables, lead times, and metric these numbers come from, with a clear formula traceable to specific table entries.
3. **Tone down SOTA claims** to match the actual comparison scope, or include comparisons to modern neural weather models (even at a discussion level).
4. **Report parameter counts** for all models to substantiate the "comparable parameters" claim.
5. **Discuss the mixed physics-awareness results honestly**, including where PA-TFNP underperforms TFNP and ClimaX.
6. **Add an empirical rotation-equivariance test** (e.g., apply a known rotation to input, pass both original and rotated through the model, verify output consistency).

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>