## Summary

This paper introduces a shape-adaptive guidance signal (WGDT) for interactive cortical sulcal labeling on spherical surface representations. The key idea is to encode user clicks by solving the eikonal equation with a speed function derived from cortical mean curvature, so that the signal propagates faster along sulcal valleys and slower along gyral ridges. Experiments on 72 HCP subjects with 17 sulci in the lateral prefrontal cortex demonstrate that even a single click with WGDT outperforms fully automatic methods and equidistance-based encoding schemes, particularly for small and variable sulci.

## Strengths

- **Novel and well-motivated encoding scheme.** The use of the eikonal equation with a curvature-based speed function to produce shape-adaptive guidance signals is a genuine contribution. The idea that wavefront propagation should follow cortical folding patterns (faster along sulci, slower along gyri) is intuitive and well-justified by the anatomy. This addresses a real gap: no prior work has explored geometry-aware guidance signals for interactive segmentation on cortical surfaces.

- **Comprehensive and rigorous experimental evaluation.** The paper performs 5-fold cross-validation on 72 subjects across 17 sulci, compares three guidance signal types (ADT, Disk, WGDT) with multiple hyperparameter settings, includes three recent automatic baselines retrained on the same data for fair comparison, applies FDR-corrected paired t-tests, and provides both quantitative (Dice scores per sulcus) and qualitative (surface visualizations) results. The runtime analysis confirming sub-second inference (<0.5s per click) further supports practical applicability.

- **Clear practical impact for neuroscience.** The paper convincingly demonstrates that small and shallow sulci—which are increasingly recognized as relevant to higher-order cognitive functions—remain poorly labeled by automatic methods. The interactive framework with WGDT substantially reduces the annotation burden (1–3 clicks vs. full manual correction), which has direct value for scaling neuroimaging studies.

## Weaknesses

### Fatal
None.

### Major

- **Per-sulcus model training limits scalability.** The paper trains 17 separate binary models, one per sulcus. While this is acknowledged and justified by morphological heterogeneity, it raises concerns about computational cost at training time and practical deployment complexity. The paper would benefit from discussing how this scales to full cortical surfaces with hundreds of sulci, or whether a multi-class or shared-parameter approach could be explored.

- **Simulated clicks only, no real user study.** All evaluations use simulated clicks with a specific sampling strategy (center of largest mislabeled component with weighted randomization). While this is standard practice, the paper does not validate that the click simulation strategy faithfully represents real annotator behavior. A small real-user pilot study, even informal, would substantially strengthen the practical claims.

- **Limited geographic scope.** Evaluation is restricted to the left hemisphere LPFC. While the authors acknowledge this, the paper's claim of generalizability would be significantly strengthened by at least preliminary results on another cortical region with different sulcal characteristics.

### Minor

- **Hyperparameter sensitivity not fully characterized.** The paper notes that k and σ require manual tuning and that large k values can limit the benefit of additional clicks. A more systematic analysis (e.g., sensitivity curves or ablation tables) would help practitioners select appropriate values and understand the robustness of the method.

- **No comparison with interactive baselines from adjacent domains.** While no interactive sulcal labeling methods exist, interactive segmentation methods on 3D meshes (e.g., graph cuts with user seeds, or recent learning-based 3D interactive methods) could serve as informative baselines to contextualize the contribution.

- **Single initial click placement strategy.** The 10 initial clicks are selected to maximize distance from label boundaries and mutual separation, which may not reflect realistic user behavior. Sensitivity to click placement (e.g., near boundaries, in ambiguous regions) would be informative.

### Trivial
None.

## Nice-to-Haves

- A discussion or experiment showing how automatic predictions could serve as initialization for the interactive model, reducing the number of required clicks further.
- Visualization of the eikonal wavefront propagation on the sphere to better illustrate how the curvature-based speed function shapes the signal in practice.
- Analysis of failure cases where WGDT still underperforms, to identify remaining challenges.

## Novel Insights

The paper's central insight—that encoding user interactions via curvature-aware geodesic propagation on the sphere produces more effective guidance signals than equidistance-based approaches—is genuinely novel. The observation that this advantage is most pronounced for small and variable sulci (where the initial click's spatial prior is most critical) is well-supported by the data and has practical implications for interactive annotation workflows in neuroimaging. Beyond this core contribution, the paper also demonstrates the viability of spherical CNN-based interactive segmentation more broadly, which could inspire similar approaches in other surface-based domains.

## Suggestions

- Consider adding a multi-sulcus or shared-backbone variant to address the scalability concern of per-sulcus models.
- Include a small real-user validation (even 2–3 raters on a subset of subjects) to bridge the gap between simulated and real interaction.
- Add a hyperparameter sensitivity analysis (e.g., a table or plot of Dice vs. k and σ) to guide practitioners.
- Explore using automatic predictions as the initial "current prediction" to reduce required clicks to zero for well-identified sulci.

## Score and Decision

The paper presents a novel, well-motivated method with solid experimental validation for a specialized but important application. The curvature-aware eikonal encoding is a genuine technical contribution, and the results convincingly demonstrate its advantages for small, variable sulci. The limitations (per-sulcus models, simulated clicks, single-region evaluation) are acknowledged but do not invalidate the core claims. The paper would benefit from broader evaluation and scalability analysis, but the contribution is clear and practically valuable.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept