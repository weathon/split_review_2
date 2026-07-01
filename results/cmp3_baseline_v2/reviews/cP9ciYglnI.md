## Summary
This paper proposes a shape-adaptive guidance signal for interactive cortical sulcal labeling. The method solves the eikonal equation on the sphere with a mean-curvature-based speed function, so that user clicks propagate faster along sulcal valleys and slower across gyri. The resulting weighted geodesic distance transform (WGDT) is fed together with geometric features into a spherical CNN (SPHARM-Net) to refine segmentations iteratively with minimal user clicks. Experiments on 72 HCP subjects with 17 LPFC sulci show that a single WGDT click significantly outperforms fully automatic baselines and equidistance-based encoding schemes (ADT, Disk), especially on small, variable sulci.

## Strengths
- **Well-motivated problem and design.** Small/shallow sulci have high anatomical variability and are poorly handled by automatic methods; existing interactive techniques rely on 2D projections that lose buried structure. The use of spherical mapping avoids these projection issues, and the curvature-aware eikonal propagation is a principled way to encode user intent along cortical folds.
- **Clear and thorough experimental comparison.** The paper compares WGDT against two equidistance-based signals (ADT, Disk) across multiple radii, and against three recent automatic baselines re-trained on the same data. ROI-wise results with FDR correction show that WGDT achieves statistically significant gains on all 9 small/variable sulci with just one click, and the gap holds up to three clicks.
- **Practical efficiency and iterative design.** The runtime is under 0.5 seconds per click, supporting real-time use. The iterative click simulation (sampling the largest mislabeled component with boundary-aware perturbation) is reasonable and mirrors real correction behavior.
- **Good ablation and analysis.** Figures 4 and 6 clearly illustrate why equidistance signals spill over into adjacent regions while WGDT stays localized along folds. The discussion of hyperparameter trade-offs (k, σ) is honest and provides guidance for future work.

## Weaknesses
### Fatal
None.

### Major
- **Limited generalization scope.** Evaluation is restricted to 72 participants, left hemisphere only, and a single region (LPFC, 17 sulci). While the motivation about shallow sulci is compelling, the paper does not demonstrate performance on other cortical regions (e.g., medial temporal, occipital) or on the right hemisphere. The claim that the method works for “cortical sulcal labeling” in general is not fully supported.
- **No comparison to any interactive baseline.** The authors state that no interactive methods exist for sulcal labeling, but they could have adapted a generic interactive method to meshes (e.g., graph cuts with geodesic distance, or back-projecting SAM predictions to the surface after 2D rendering). At minimum, a simple geodesic distance transform (without curvature weighting) on the original mesh should have been included as a baseline to isolate the benefit of the curvature-aware speed.
- **Per-sulcus modeling limits scalability to full cortex.** Training a separate model for each of 17 sulci is manageable for LPFC, but scaling to 100+ sulci would be impractical. The paper acknowledges this only briefly and does not discuss shared representations or multi-task alternatives.

### Minor
- **Hyperparameter sensitivity is underexplored.** Only three values of k (6,8,10) and one σ (π/32) are tested for WGDT. The paper notes that larger k can reduce the benefit of additional clicks, but the optimal choice likely depends on sulcus size and curvature distribution. A more systematic sweep or a data-driven tuning strategy would strengthen the claim.
- **Statistical test details are sparse.** The paired t-test and FDR correction are mentioned, but no effect sizes or confidence intervals are reported. Appendix tables would help interpret the magnitude of improvement, especially for large sulci where differences are small.
- **The simulation of user clicks may not fully capture real human behavior.** The simulated click picks the largest mislabeled component and selects a near-center point with moderate variation. Human annotators may click less optimally (e.g., on boundaries, or on multiple regions in one click). While a reasonable approximation, this introduces a risk of overestimating real-world performance.

### Trivial
None.

## Nice-to-Haves
- Inclusion of a geodesic distance transform without curvature weighting (i.e., constant speed on the sphere) as an additional baseline to isolate the effect of the curvature term.
- A small experiment on right-hemisphere or on a different cortical region (e.g., occipital pole) to test generalization.
- Reporting Dice curves for each sulcus as a function of the number of clicks (not just up to 3) to show the plateau behavior.

## Novel Insights
None beyond the paper's own contributions. The core insight is that encoding user clicks with a curvature-modulated eikonal equation on the sphere yields guidance signals that align with cortical folds, improving interactive sulcal labeling efficiency. This is a well-engineered adaptation of classical geodetic concepts to a specific neuroimaging problem.

## Suggestions
- **For camera-ready:** Add a baseline that uses a standard geodesic distance transform (constant speed) on the sphere to isolate the benefit of the curvature term. Report Dice for each sulcus in a table with standard deviations and effect sizes.
- **For future work:** Investigate a single multi-sulcus model (e.g., with per-sulcus output heads or conditional labeling) to improve scalability, and explore learning the propagation speed from data rather than hand-tuning k.

## Score and Decision
**Score:** 8

**Decision:** Accept

**Rationale:** The paper addresses an important, under-studied problem (interactive labeling of shallow cortical sulci) with a technically sound and novel encoding mechanism. The experiments are carefully executed, comparisons are fair, and the results clearly demonstrate advantages over both automatic methods and simpler interaction encoding. The main limitations (single region, per-sulcus modeling, lack of interactive baselines) are acknowledged and do not invalidate the core contribution. For ICLR, the work provides a clear methodological advance in geometric deep learning for non-Euclidean interactive segmentation, and it is likely to have practical impact in neuroscience.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>