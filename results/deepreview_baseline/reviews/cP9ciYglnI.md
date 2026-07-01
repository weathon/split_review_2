## Summary

This paper introduces a shape-adaptive guidance signal for interactive cortical sulcal labeling on the lateral prefrontal cortex. The method encodes user clicks by solving the eikonal equation with a curvature-based speed function on the spherical mapping of cortical surfaces, enabling the guidance signal to propagate faster along sulcal valleys and slower along gyri. Experimental results on 72 HCP subjects with 17 sulci demonstrate that the proposed weighted geodesic distance transform (WGDT) signal outperforms equidistance-based encoding schemes (ADT and Disk) and fully automatic baselines, achieving improved labeling accuracy with as few as one to three user clicks.

## Strengths

- **Novel and well-motivated approach**: The paper identifies a genuine limitation in existing interactive segmentation methods for cortical surfaces—namely, that equidistance-based guidance signals ignore underlying anatomy—and proposes a principled solution using the eikonal equation with curvature-aware propagation. This is a creative adaptation of classical PDE methods to a modern deep learning pipeline.

- **Strong empirical validation**: The experiments are thorough, covering 17 sulci (8 large/consistent and 9 small/variable) across 72 subjects with 5-fold cross-validation. The WGDT signal consistently outperforms ADT and Disk signals on all 9 small/variable sulci with statistical significance (adjusted p < 0.05), and outperforms three fully automatic baselines with a single click. The runtime analysis (under 0.5 seconds per click) demonstrates practical feasibility.

- **Clear and appropriate methodology**: The use of spherical mapping to avoid occlusion issues inherent in 2D projection methods is well-justified for cortical surface data. The iterative click simulation strategy with spatial variability is sensible and mimics real annotator behavior. The per-sulcus modeling approach is appropriate given the distinct morphological characteristics of LPFC sulci.

## Weaknesses

### Fatal
None.

### Major
- **Limited evaluation scope**: The method is evaluated only on the lateral prefrontal cortex (LPFC) with 17 sulci. While the authors acknowledge this limitation, the paper would be significantly strengthened by demonstrating generalization to other cortical regions (e.g., medial surface, temporal lobe) or to full cortical parcellation. The claim that the method is "for interactive cortical sulcal labeling" is broader than what is actually validated.

- **No comparison to existing interactive segmentation methods**: The paper compares only to fully automatic baselines, stating "no interactive methods are available for sulcal labeling." However, general-purpose interactive segmentation methods for 3D meshes (e.g., Kontogianni et al., 2023; Lang et al., 2024) could potentially be adapted to this domain. Even if direct adaptation is non-trivial, a discussion of why these methods are unsuitable or a simple baseline using SAM on 2D projections would strengthen the claims.

- **Hyperparameter sensitivity is underexplored**: The WGDT signal has two hyperparameters (k and σ) that require manual tuning. The paper reports results for k ∈ [6,8,10] and σ = π/32, but does not systematically analyze how performance varies with these parameters across different sulci. The observation that "a large k can limit the benefit of additional clicks" suggests that parameter selection is non-trivial and may need to be sulcus-specific.

### Minor
- **The iterative click simulation strategy**, while reasonable, assumes the user always clicks near the center of the largest mislabeled region. Real annotators may click on boundaries, extremities, or multiple regions in sequence. The impact of this assumption on real-world performance is unclear.

- **The masking strategy** (keeping only faces with curv ≥ 0) to address re-tessellation artifacts is somewhat ad-hoc and could potentially discard valid sulcal regions if the curvature threshold is not perfectly calibrated.

### Trivial
- The paper uses "sulcal" and "sulci" terminology consistently, but "sulcal labeling" is occasionally used where "sulcus labeling" might be more standard.

## Nice-to-Haves

- An ablation study isolating the contribution of the curvature-based speed function from the eikonal equation framework itself (e.g., comparing WGDT with a geodesic distance transform using constant speed) would clarify which component drives the improvement.
- A user study with human annotators (even a small one) would provide stronger evidence of practical utility than simulated clicks.
- Visualizing the propagation speed function F on the sphere for different k values would help readers understand the behavior of the WGDT signal.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Extend evaluation to at least one additional cortical region (e.g., medial prefrontal cortex or temporal lobe) to demonstrate generalization beyond LPFC.
- Include a comparison or at least a discussion of why general-purpose interactive 3D segmentation methods (e.g., SAM-based approaches on mesh projections) are not suitable for this task.
- Provide a sensitivity analysis for the k and σ hyperparameters across different sulci, and consider proposing a data-driven method for selecting these parameters.

## Score and Decision

The paper presents a novel, well-motivated, and empirically validated method for interactive cortical sulcal labeling. The core idea of using curvature-aware eikonal propagation to encode user clicks is creative and effective, particularly for small and variable sulci where automatic methods struggle. The experimental design is sound, and the results are convincing within the evaluated domain. However, the limited scope of evaluation (LPFC only) and the lack of comparison to any interactive baseline prevent the paper from being a strong accept. The contribution is solid but incremental—it addresses a specific neuroimaging problem with a clever adaptation of existing techniques rather than introducing a fundamentally new paradigm.

**Score**: 6.0

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>