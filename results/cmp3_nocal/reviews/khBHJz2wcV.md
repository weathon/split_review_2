## Summary

This paper proposes a framework for fine-tuning flow-matching generative models to enforce parameter-dependent PDE constraints and jointly infer latent physical parameters. The key idea is to augment the generative state with a latent parameter α, evolve both jointly via an adjoint-matching stochastic control formulation, and use a scaled memoryless noise schedule for stability. The method is evaluated on four PDE families (Darcy flow, linear elasticity, Helmholtz, Stokes) plus a natural-image recoloring task.

## Strengths

1. **Joint evolution of state and latent parameters (Section 3.2) is a genuine technical contribution.** Extending the generative flow to simultaneously traverse both x and α via a surrogate base flow defined through the inverse predictor φ is a principled solution to parameter-dependent constraint enforcement without requiring paired training data. The Stokes results (Figure 5) provide credible evidence that the joint formulation adds value beyond φ alone: the joint model reaches MMD_α ≈ 0.07–0.13 while ablations remain at 0.22–0.28.

2. **Scaled memoryless noise schedule (Section 3.3, κ parameter).** The paper shows that a family of schedules σ²(t) = (1−κ)·2η_t remains theoretically consistent with the memoryless property — not just the single canonical schedule. This gives practitioners a stabilization knob for mitigating blow-ups near t→0 while retaining theoretical guarantees, which prior work treated as having a unique schedule.

3. **Computational efficiency is demonstrated concretely.** Fine-tuning on noisy Darcy requires only 20 gradient steps and "under 15 minutes on a single NVIDIA L40S" (Section 4.1), after which inference proceeds at base-model cost. This is a meaningful practical advantage over training-time approaches (Bastek et al., 2024; Baldan et al., 2025).

## Weaknesses

### Fatal
None.

### Major

1. **Inverse problem claims are not validated at the per-sample level.** The abstract claims "accurate recovery of latent coefficients" and the introduction claims "addressing ill-posed inverse problems." However, the only parameter-related evaluation metric is MMD_α — a distribution-level similarity measure between the set of inferred parameters and a reference dataset D_ref (Section 4, Comparisons). MMD_α measures whether the *distribution* of predicted parameters matches the reference, not whether any individual parameter prediction is correct. A model could produce parameter estimates that have the right distributional statistics (roughness, scale, range) but are uncorrelated with the true parameters per sample, and still achieve low MMD_α. The qualitative α maps in Figure 2 are described as "cleaner" but, as the paper itself acknowledges, cleaner ≠ more accurate. To support the inverse problem claims, the paper would need per-sample metrics such as relative L2 error or correlation between α̂ and α_true on a held-out set where ground-truth parameters are known (the synthetic data setup already supports this). This is a gap between the claims made and the evidence provided.

2. **Diversity-preservation claim is overstated.** The abstract says the method promotes physical consistency "without distorting the underlying learned distribution," and the conclusion claims samples "adhere to complex constraints without significantly affecting the sample diversity." Yet Figure 3a directly shows that increasing λ reduces the PDE residual *and simultaneously* reduces SSIM-based diversity from ~0.98 (base) to ~0.84 (strongest constraint) — a ~14% reduction on a bounded metric. This is a systematic trade-off, not an absence of distortion. The paper honestly shows this trade-off in the ablation but then contradicts it in the abstract and conclusion. The contribution should be framed as enabling *controllable navigation* of this trade-off (via λ, λ_f), which is a legitimate and useful capability.

### Minor

3. **Baseline coverage is limited relative to the literature positioning.** The paper discusses inference-time constraint enforcement approaches in Section 2 (Huang et al., 2024; Christopher et al., 2024; Utkarsh et al., 2025) but does not compare against any of them experimentally. The experimental comparisons are to PBFM (a training-time method), ECI (Cheng et al., 2024, appearing only in the linear elasticity table with residual 1,013 suggesting possible misconfiguration), and two self-ablations (Base AM, Base AM+φ). Adding at least one representative inference-time baseline on the simplest PDE task (Darcy) would substantially strengthen the paper's positioning.

4. **The primary evaluation metric (R_weak) is also the reward being optimized, creating a mild circularity concern.** While R_strong is reported as a secondary metric and MMD provides orthogonal information, the main evidence for physical consistency is reduction of the same quantity minimized during fine-tuning. R_weak improvements are larger than R_strong improvements in some cases (e.g., Helmholtz from Table 2: R_weak drops ~3.5× for the full AM model vs. R_strong drops ~2.2×), which is consistent with the method specializing to the particular set of test functions ψ used. Validation against an independent metric such as pointwise solution error would strengthen the conclusions.

5. **Natural image experiment (Section 4.6) is purely qualitative.** Three cherry-picked samples are shown comparing "Vanilla Adjoint Matching" against the joint model, with no quantitative metrics (FID, CLIP score, or comparable measure). The connection to physics is analogical (α is a polynomial color transform, not physically meaningful). This experiment does not provide rigorous support for the "cross-domain utility" claim.

6. **Dependence of the surrogate base flow on φ accuracy is not analyzed.** The surrogate base flow v_{t,α}^{base}(α_t) = (φ(x̂₁) − α_t)/(1-t) (Section 3.2) depends critically on the quality of the inverse predictor φ. If φ is inaccurate (likely early in fine-tuning or when the base model produces noisy samples), the surrogate flow provides a noisy training signal. The paper does not study this dependency empirically or theoretically.

### Trivial

7. MMD_x and MMD_α are reported as point estimates without variance, making it difficult to assess significance. Given that MMD estimates can have high variance with 256 samples, this should be addressed.

8. The Helmholtz table (Table 2) reports each method with two rows (selected for lowest R_weak and lowest MMD_x respectively), making the table harder to parse than a single operating point or a Pareto figure would be.

## Nice-to-Haves
- Including the total cost comparison (base model pre-training + fine-tuning) vs. training-time approaches would give a more complete efficiency picture.
- The guidance mechanism toward sparse observations (Section 4.2) is deferred entirely to Appendix E.4; a brief sketch in the main text would improve readability.

## Removed Points
The following points from the input review were removed with justification:
- **Code URL is empty:** Removed — this is a double-blind submission placeholder.
- **φ training details insufficient:** Removed — the approach (minimizing R_weak(x, φ(x)) w.r.t. φ) is standard; the concern reflected a misunderstanding of physics-informed learning.
- **Stokes base FM omitted from figure:** Removed — the paper explicitly reports its R_weak (=305) in the text; omission for visual clarity is acceptable.
- **Generic speculation about confounders not anchored to specific paper content:** Removed per filtering guidelines.

## Novel Insights
None beyond the paper's own contributions. The reviews converge on a clear pattern: the paper makes claims ("accurate recovery", "without distorting") that exceed the current evidence, but the underlying method is genuinely novel, principled, and computationally efficient. The gap is between rhetoric and evidence, not between method and performance.

## Suggestions
1. **Validate inverse problem inference at the per-sample level.** On a task where ground-truth α is known (e.g., Darcy with synthetic α from the same GP), report per-sample parameter error (relative L2 or correlation) alongside MMD_α. This directly addresses the most significant weakness.
2. **Adjust the diversity claim.** Qualify "without distorting" / "without significantly affecting" and instead frame the contribution as enabling controllable navigation of the constraint-diversity trade-off shown in Figure 3a.
3. **Add at least one inference-time baseline** (e.g., Huang et al.'s guidance approach) on the Darcy task to strengthen the literature positioning relative to work discussed in Section 2.
4. **Add quantitative metrics to the natural image experiment** (FID or PickScore) to support the cross-domain utility claim, or remove the experiment.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>