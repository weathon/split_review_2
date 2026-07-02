## Summary

This paper proposes a shape-adaptive guidance signal (WGDT) for interactive cortical sulcal labeling on spherical surfaces. The method solves the eikonal equation with a curvature-dependent speed function on the sphere to encode user clicks, allowing faster propagation along sulcal folds (mean curvature H ≥ 0) and slower over gyral regions (H < 0). On 72 HCP subjects with 17 LPFC sulci, WGDT significantly outperforms equidistance-based encoding schemes (ADT, Disk) on all 9 small/variable sulci with a single click, and runs in under 0.5s per click. The paper also shows that one click with WGDT beats fully automatic methods.

## Strengths

- **Novel and principled technical contribution.** Using the eikonal equation with curvature-dependent speed (Eqs. 3–5) to make guidance signals shape-adaptive on the cortical sphere is a clean, well-motivated idea that is clearly tied to the anatomy of interest (faster along sulci, slower on gyri). This is the first paper to introduce shape-adaptive guidance signals for interactive segmentation on cortical surfaces.

- **Rigorous and appropriately scoped evaluation.** The 5-fold cross-validation over 72 subjects, 10 initial clicks averaged per subject, per-sulcus statistical testing with FDR correction (q=0.05), and hyperparameter sweeps (k ∈ {6,8,10} for WGDT, multiple σ for ADT/Disk) reflect careful experimental design that is standard for the neuroimaging community.

- **Consistent and statistically significant results.** WGDT shows significant improvement (adjusted p < 0.05) over ADT and Disk on all 9 small/variable sulci, with the largest gap at the first click. Qualitative examples (Figure 6) support the quantitative pattern: WGDT identifies the full extent of shallow sulci that ADT/Disk under-segment.

- **Practical efficiency.** Runtime analysis (Table 2) demonstrates under 0.5s per click, which supports real-time interactive use.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Simulated clicks limit generalizability to real annotators.** The click simulation (Section 2.2) always targets the largest mislabeled component with distance-weighted sampling near its center. Real annotators may click on boundaries, target small residual errors, or vary their strategy across subjects and sessions. While this simulation is carefully designed and standard for interactive segmentation research, the paper's practical claims about "reducing human effort" refer to an idealized annotator, not a real one. A small user study (even 2–3 raters on a subset) would substantially strengthen the practical claims.

- **No ablation of the ICL loss weighting scheme.** The iterative click loss (Eq. 7) uses β_i ∈ [1/6, 1/3, 1/2] with increasing weight on later clicks. This scheme is inherited from prior work (Sun et al., 2024) and is not validated in this setting. An ablation comparing this weighting against uniform weighting would confirm whether the component contributes meaningfully.

- **No analysis of failure cases or conditions where WGDT underperforms.** The paper reports average performance but does not examine subjects or sulci where WGDT performs poorly. Understanding when the curvature signal fails—e.g., due to noise in curvature estimation, extremely thin sulci, or adjacent sulci with similar curvature profiles—would strengthen the contribution and guide future improvements.

- **"Near-perfect accuracy" lacks a quantitative threshold in the main text.** Section 4.2 states "By 2 or 3 clicks, the variable sulci reach near-perfect accuracy" without specifying the Dice threshold. The appendix likely contains the actual numbers, but the main text should include them directly.

- **The automatic-method comparison is over-emphasized in the framing.** The abstract and Section 4.2 lead with the result that one click beats fully automatic methods. While factually correct, this comparison is unsurprising—any interactive method with a click in the target region should outperform automatic methods that have no subject-specific input. The paper's real contribution is the WGDT encoding versus ADT/Disk, which is well-evaluated but somewhat buried. The framing should foreground the guidance signal comparison as the primary result.

### Trivial
None.

## Nice-to-Haves
- A small user study (2–3 raters on a subset of subjects) would transform the paper from a simulation study to a practical demonstration.
- Ablation of the ICL loss weighting scheme.
- Analysis of failure cases and conditions where curvature-based propagation is unreliable.
- A sensitivity analysis exploring the clamping range [0.05, 10] for propagation speed.

## Removed Points
These points are flagged to be removed, treat them with caution.

1. **Missing uniform-speed geodesic distance baseline (Critical Issue #1 from Harsh Critic).** The critic claims that ADT confounds geodesic distance and curvature weighting, and that a uniform-speed (F=1) geodesic distance transform is the missing intermediate baseline. **This is factually incorrect.** ADT (Eq. 1) computes `arccos(x·c)` which IS the geodesic (great-circle) distance on the unit sphere. Therefore ADT already serves as the uniform-speed geodesic distance baseline on the sphere, and the WGDT vs. ADT comparison directly isolates the effect of curvature weighting. The paper's central claim is properly supported by its existing comparison.

2. **ADT/Disk σ values not tested at larger values (Section-by-Section Notes).** The critic claims the paper "does not test larger σ values for ADT/Disk that might cover more of the sulcus." **This is factually incorrect.** The paper tests σ ∈ [π/32, 3π/64, π/16] for ADT/Disk, with π/16 being twice the WGDT σ of π/32. Larger values were tested and ADT/Disk still underperformed.

3. **Sensitivity to clamping range [0.05, 10] not explored.** This is a generic hyperparameter sensitivity request that could apply to any numerical method, not a specific weakness of this paper.

4. **17 separate models as a practical limitation.** The paper transparently acknowledges the per-sulcus design (Section 2.1), explains the rationale (distinct morphological characteristics per sulcus), and discusses joint modeling as future work (Section 5). This is a standard design choice in medical image interactive segmentation, not a flaw.

5. **Missing related work.** Removed per policy (cannot be verified without external sources).

## Novel Insights

None beyond the paper's own contributions. The reviews identified no synthesis that the paper does not already claim or imply.

## Suggestions

1. Add the actual Dice score ranges for the "near-perfect accuracy" claim in Section 4.2.
2. Consider an ablation experiment comparing the proposed β_i weighting against uniform weighting for the ICL loss.
3. Include a brief discussion (or appendix section) of failure cases—subjects or sulci where WGDT underperformed and why.
4. Reframe the abstract and introduction to foreground the guidance signal comparison (WGDT vs. ADT/Disk) as the primary contribution, with the automatic-method comparison presented as supporting context.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>