## Summary
# Final Review Report

## Summary

This paper addresses the challenging problem of interactive cortical sulcal labeling, focusing on small and shallow sulci in the lateral prefrontal cortex (LPFC) that exhibit high anatomical variability. The authors propose a shape-adaptive guidance signal called Weighted Geodesic Distance Transform (WGDT) that encodes user clicks by solving the eikonal equation with a mean-curvature-dependent speed function on the spherical domain. This curvature-aware propagation enables faster signal spread along sulcal valleys and slower spread across gyri, producing anatomically coherent guidance. The framework is built on SPHARM-Net, a spherical CNN backbone, and supports iterative refinement through multiple simulated user clicks. Evaluated on 72 HCP subjects with 17 manually defined LPFC sulci, the WGDT signal with a single click outperforms both fully automatic baselines (Lyu et al., 2021; Lee et al., 2025a,b) and equidistance-based guidance signals (ADT, binary Disk), achieving statistically significant improvements on all 9 small and variable sulci. The method achieves sub-500ms per click, suggesting practical usability. The core idea—embedding cortical folding geometry into interactive guidance signals via the eikonal equation—is well-motivated and technically sound. However, several limitations warrant attention: the per-sulcus separate-model design does not scale to whole-cortex labeling, the main accuracy results lack variance reporting, the automatic baselines are confined to the same spherical CNN lineage, and the mathematical presentation of the eikonal formulation contains an inconsistency (anisotropic-appearing equation presented as isotropic). Additionally, external literature verification was unavailable in this run, so novelty and positioning conclusions are deferred to manual verification.

## Strengths
1. **Well-motivated technical contribution**: The core idea—using the eikonal equation with a curvature-dependent speed function to produce anatomically adaptive guidance signals—is conceptually clean and directly addresses a genuine limitation of existing interactive segmentation methods for cortical surfaces. The connection between sulcal geometry (mean curvature) and wavefront propagation speed is principled and physically intuitive.

2. **Strong empirical evidence on the target task**: The experimental results convincingly demonstrate that WGDT with a single click outperforms equidistance-based signals (ADT, Disk) on all 9 small and variable sulci, with statistical significance (adjusted p < 0.05). The improvement pattern is consistent across multiple k values, and qualitative visualizations (Figure 6) show clear differences in sulcal coverage. The comparison against automatic baselines further validates the practical utility of even minimal user interaction.

3. **Iterative refinement integration**: The method supports multi-click iterative refinement with a well-designed click simulation strategy (largest-mislabeled-component targeting with distance-weighted center sampling). The iterative click loss formulation with increasing weights for later steps is a sensible adaptation that encourages the model to improve with each successive click.

4. **Computational efficiency**: The runtime analysis (Table 2) shows that a full interaction cycle (signal encoding + re-tessellation + forward pass) takes under 500ms, supporting real-time interactive use. This is an important practical consideration that strengthens the deployment potential.

5. **Honest limitations discussion**: The authors openly acknowledge the per-sulcus model design's scalability limitation, the need for hyperparameter tuning (k, σ), and the dependence on accurate surface reconstruction. This transparency improves the scientific credibility of the presentation.

6. **Good use of spherical domain**: Leveraging the genus-zero topology of cortical surfaces for spherical mapping is appropriate and avoids the occlusion problems inherent in 2D projection-based approaches. The compatibility with spherical CNNs is a natural fit.

## Weaknesses
### W1. Missing variance reporting in main accuracy results (Major)
The central experimental results (Section 4.1, Figures 4 and 5) report Dice scores without standard deviations, confidence intervals, or fold-level ranges. While paired t-tests with FDR correction provide some statistical validation, the absence of error bars makes it impossible for readers to assess the stability and reliability of the reported improvements. The runtime analysis (Table 2) does include ±std, demonstrating that the authors can compute variance when they choose to. **Impact**: Readers cannot judge whether the WGDT gains over ADT/Disk are robust across subjects and cross-validation folds. **Fix**: Report mean Dice ± std over cross-validation folds and subjects, and add error bars to Figures 4 and 5. Include a supplementary table with per-fold performance ranges.

### W2. Per-sulcus separate-model design limits scalability (Major)
The method trains 17 independent binary segmentation models—one per sulcus (Section 2.1). This design does not scale to whole-cortex parcellation (typically 30+ regions) without prohibitive model proliferation, training data requirements, and inference cost. The authors cite common practice in medical imaging, but the cited references typically train 1-3 models for specific organs, not 17+ for a single cortical region. **Impact**: The claim of practical utility for reducing manual labeling effort is bounded by the per-sulcus design. Scaling to full cortex would require a fundamentally different multi-class or parameter-sharing approach. **Fix**: Either (a) demonstrate a path to unified multi-sulcus modeling (e.g., shared encoder with per-sulcus heads), or (b) explicitly bound the contribution to the 17-sulcus LPFC setting and discuss scaling challenges concretely in limitations.

### W3. Eikonal formulation inconsistency: anisotropic equation vs isotropic claim (Major)
Equation (3) presents the eikonal equation in a general anisotropic form where the speed function F depends on both position x and the gradient direction ∇u/||∇u||. However, the text states "F is considered an isotropic function known as the eikonal equation. This equation describes wavefront propagation with a constant speed in all directions." If F depends only on x (as in Eq 4, where F = exp(kH(x))), the direction argument should be removed from Eq (3). **Impact**: The inconsistency could confuse readers familiar with eikonal PDEs. While the implementation (fast marching with isotropic speed) is likely correct, the mathematical presentation is imprecise. **Fix**: Rewrite Eq (3) in isotropic form: ||∇u_c(x)|| F(x) = 1, removing the direction dependence from F.

### W4. Non-standard cross-entropy notation in Eq (6) (Major)
Equation (6) writes L_label^i = - Σ_{n∈{0,1}} log(p_n, z_n). The notation "log(p_n, z_n)" with two arguments is mathematically ambiguous. Standard binary cross-entropy is -Σ z_n log(p_n) = -[z_1 log(p_1) + (1-z_1) log(1-p_1)]. Additionally, the probability p is not explicitly defined as the softmax of F's ℝ² output, though this can be inferred. **Impact**: This formulation is not reproducible as written. **Fix**: Replace with explicit standard cross-entropy: L_label^i = - Σ_n z_n log(p_n) where p_n = softmax(F(x))_n.

### W5. Same-lineage automatic baselines (Moderate)
The three automatic baselines (Lyu et al., 2021; Lee et al., 2025a,b) all come from closely related research groups and use the same spherical CNN paradigm. While retraining ensures within-family fairness, the absence of out-of-family baselines (graph-based, transformer-based, or traditional mesh segmentation methods) limits the generalizability of the superiority claim. **Impact**: A reader may question whether WGDT's advantage is specific to the spherical CNN family rather than reflecting a general advantage of the interactive curvature-aware approach. **Fix**: Add at least one non-spherical-CNN baseline or explicitly discuss why such comparisons are infeasible, while bounding the claim scope.

### W6. Abstract lacks compact structure and contains informal phrasing (Minor)
The abstract is a single dense paragraph mixing motivation, gap, method, technical detail, and results. The phrase "Thanks to the use of spherical mapping" is informal for a scientific abstract. **Impact**: Reduced readability and signal-to-noise ratio. **Fix**: Restructure into a 5-sentence compact arc (problem → gap → method → result → implication) as detailed in the Page 1 - Abstract annotation.

### W7. Introduction opening is overly generic (Minor)
The first paragraph starts with "Image segmentation is one of the fundamental tasks in computer vision" which is too broad for the specific neuroimaging focus. The transition from generic computer vision to cortical sulcal labeling is compressed. **Impact**: Missed opportunity to immediately establish scientific stakes. **Fix**: Open with a domain-specific problem statement as provided in the Page 1 - Introduction annotation.

### W8. Conclusion future work is overly optimistic (Minor)
The final paragraph introduces multiple extension directions without acknowledging concrete technical challenges (e.g., learning-based speed optimization requires differentiable eikonal solvers). **Impact**: Slightly reduces the rigor of an otherwise well-structured conclusion. **Fix**: Qualify each direction with specific challenges as suggested in the Page 1 - Conclusion annotation.

### Novelty and Positioning (Deferred — External Literature Verification Unavailable)
External paper search was not available in this run (missing API token). Therefore, novelty/comparison conclusions regarding the claimed "first" use of curvature-aware guidance signals for interactive cortical labeling are deferred to manual verification. The authors claim "To the best of our knowledge, no prior studies have investigated interactive geometric segmentation methods that explicitly incorporate surface geometry to generate structure-aware guidance signals." This claim appears appropriately scoped but cannot be independently verified in this review. **Action**: Authors should provide a brief literature survey confirming that no prior work combines (a) interactive click-based segmentation on the sphere, (b) eikonal-equation guidance encoding, and (c) curvature-based speed functions for cortical surface labeling.

## Score
**Final Score: 6/10**

**Rationale**: This score reflects a balanced assessment of the paper's strengths and weaknesses:

- **Research value**: The paper addresses a genuine and important problem (interactive cortical sulcal labeling) with a well-motivated technical idea. The curvature-aware guidance signal via the eikonal equation is a principled contribution that could influence future interactive segmentation work on surfaces. (+)
- **Novelty**: The core idea of embedding folding geometry into click-encoding via the eikonal equation appears novel within the specific context of interactive cortical surface segmentation. However, independent literature verification was unavailable, so this assessment is provisional. The per-sulcus modeling strategy is not novel. (neutral)
- **Validity/Soundness**: The experimental design has strengths (5-fold CV, FDR-corrected statistics, multiple click simulations) but is weakened by missing variance reporting in main accuracy results, the same-lineage baseline concern, and the mathematical inconsistency in Eq (3). The formula error in Eq (6) (non-standard cross-entropy notation) is a reproducibility issue. (−)
- **Scalability/Practical impact**: The sub-500ms runtime is encouraging, but the 17-model-per-dataset design is a fundamental scalability barrier that limits practical deployment to whole-cortex labeling. (−)
- **Presentation**: The paper is generally well-structured and clearly written. The introduction would benefit from tighter narrative focus, and the abstract could be more compact. The honest limitations discussion is commendable. (neutral)

**Key risks that prevent a higher score**:
1. Missing variance reporting (W1) — undermines confidence in the claimed improvements.
2. Per-sulcus model proliferation (W2) — limits practical scalability claims.
3. Non-standard/mathematically inconsistent equations (W3, W4) — reproducibility concern.
4. Same-lineage baselines (W5) — weakens the evidence breadth.

**Lower bound (5/10)**: If the formula errors are not corrected and variance remains unreported, the paper's reproducibility and reliability would be substantially reduced.

**Upper bound (7/10)**: If the authors add variance reporting, correct the formulas, add one out-of-family baseline, and provide a clear pathway to multi-sulcus modeling, the paper could reach a solid acceptance-level contribution.