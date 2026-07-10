Now let me write the final consolidated review.

## Summary

This paper addresses interactive cortical sulcal labeling by introducing a shape-adaptive guidance signal — the Weighted Geodesic Distance Transform (WGDT) — that encodes user clicks on the sphere using the eikonal equation with a curvature-dependent speed function. The signal propagates faster along sulcal valleys and slower across gyri, providing structure-aware spatial cues to a spherical CNN. Evaluated on 72 HCP subjects with 17 lateral prefrontal sulci, WGDT significantly outperforms isotropic encoding schemes (ADT and Disk) on all 9 small/variable sulci with a single click.

## Strengths

- **A well-motivated, principled contribution (Section 2.3.3).** The core idea — encoding user clicks via the eikonal equation with a curvature-dependent speed function — is conceptually clean and technically sound. The problem it addresses (small, shallow sulci that are anatomically variable) is real, and the formulation (Equations 3–5) is precise and directly follows from the stated motivation.

- **Statistically rigorous evaluation (Section 3.3).** The use of 5-fold cross-validation, 10 initial click locations per subject averaged into a single score, paired *t*-tests, and FDR correction across 17 sulci (*q*=0.05) is thorough and above the bar for this type of work. Multiple *k* and *σ* values tested (Section 3.2) demonstrate results are not cherry-picked from a single configuration.

- **Clean ablation inherent in the comparison against ADT.** On a unit sphere, angular distance *is* geodesic distance, so ADT (Equation 1) is exactly the unweighted geodesic distance transform. The WGDT-vs-ADT comparison directly isolates the effect of adding curvature-awareness to the propagation without confounds from different coordinate spaces or distance metrics.

- **Honest limitations section (Section 5).** The paper explicitly acknowledges limited generalization to other cortical regions, hyperparameter tuning burden, and potential unreliability under pathological anatomy — reflecting genuine boundaries of the work rather than perfunctory caveats.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Framing over-emphasizes the automatic-baseline comparison (Section 4.2, Figure 5).** The paper prominently features the result that one click outperforms fully automatic methods (abstract, Figure 5, Section 4.2). This comparison is inherently expected — an interactive method receiving a spatial prior identifying the target sulcus should naturally outperform methods with no such prior — and it does not test the paper's core contribution (curvature-aware encoding). The real contribution is tested in Section 4.1 (WGDT vs ADT/Disk). The paper would be more honestly scoped if the automatic comparison were presented as a sanity check/context rather than a headline result, and the narrative were more tightly focused on the WGDT-vs-ADT comparison that isolates what the method contributes.

- **No discussion of real-annotator variability from simulated clicks (Section 2.2).** The evaluation uses simulated clicks that sample from the center of the largest mislabeled component with softmax-weighted spatial variability. While this is standard practice, the paper does not discuss how real annotator behavior (e.g., clicking near boundaries, variable accuracy, multi-region clicks) could produce a wider performance distribution. A sentence acknowledging this and noting that a user study is future work would address this gap.

- **Single backbone architecture creates a confound (Section 2.5).** The paper uses only SPHARM-Net and acknowledges its isotropic-weighting limitation, noting that WGDT "addresses this limitation." This creates a plausible confound: WGDT's benefit may be especially large because the backbone's filters are isotropic, and the advantage might shrink with a more expressive spherical CNN. Testing at least one alternative backbone would demonstrate that the guidance signal itself — not the backbone's specific weakness — drives the improvement.

- **Asymmetric comparison with automatic baselines (Section 2.1 vs 4.2).** The interactive method trains 17 separate binary models (one per sulcus), while the automatic baselines handle all 17 sulci jointly via multi-class classification. This structural asymmetry could inflate the apparent advantage over automatic methods. The paper should at minimum acknowledge this and discuss whether it could affect the comparison.

### Trivial

- **The click simulation's greedy "largest mislabeled component" strategy (Section 2.2) is not analyzed.** How often does the first click target a large, easy-to-fix region vs. a small, hard-to-find region? This affects how interpretable the "1 click" results are in terms of practical effort.

## Nice-to-Haves

- Add an ablation that varies the speed function itself (e.g., sulcal depth instead of mean curvature) to confirm that mean curvature specifically is the right geometric prior.
- Joint modeling of morphologically similar sulci, as mentioned in Section 5, could reduce hyperparameter tuning and improve generalization.

## Removed Points

These points are flagged to be removed from the final review; treat them with caution.

- **σ is set differently for WGDT vs ADT/Disk:** REMOVED. The paper tests ADT/Disk at σ ∈ [π/32, 3π/64, π/16], including the same σ = π/32 used for WGDT. ADT/Disk are tested at *more* σ values than WGDT, so any asymmetry favors the baselines, not the proposed method. The criticism is factually incorrect.
- **Missing error bars in figures:** REMOVED. The paper describes 10-run averaging and reports statistical testing (paired t-tests, FDR correction), indicating variance information is both collected and used. Whether error bars appear in the actual figures cannot be judged from parsed text descriptions alone, and the statistical testing already accounts for variance.
- **Claim about prior work being too narrow:** REMOVED. The reviewer acknowledges this claim is "narrow enough to be defensible," so it is not actually a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Re-frame Section 4.2:** Shift the automatic-baseline comparison to a secondary/sanity-check position; focus the narrative on the WGDT-vs-ADT comparison in Section 4.1, which is the experiment that tests the paper's core contribution.
2. **Add a sentence in Section 5** explicitly acknowledging that simulated clicks may not fully capture real-world annotator variability, with a note that a user study is future work.
3. **Consider testing at least one alternative backbone** (e.g., a graph-based spherical CNN or a different harmonic-bandwidth configuration) to demonstrate that the WGDT signal's benefit is not specific to SPHARM-Net's isotropic-weighting limitation.
4. **Acknowledge the structural asymmetry** between per-sulcus binary models (interactive) and joint multi-class models (automatic baselines) in Section 4.2, and discuss whether it could affect the comparison.

## Score and Decision

The paper makes a clear, principled contribution (curvature-aware guidance signal via the eikonal equation), backed by statistically rigorous evaluation that cleanly isolates the effect of the proposed mechanism. The weaknesses are all addressable framing, scope, and discussion gaps — none threaten the core claims. The central result (WGDT significantly outperforms isotropic encoding on small/variable sulci) is convincingly demonstrated.

MY FINAL SCORE: 8.0

MY FINAL DECISION: Accept