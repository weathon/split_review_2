Now let me write the final consolidated review.

## Summary
The paper proposes a shape-adaptive guidance signal (WGDT) for interactive cortical sulcal labeling. By solving the eikonal equation on the spherical surface with a mean-curvature-based speed function, the signal propagates faster along sulcal valleys and slower across gyral ridges, capturing fine-grained anatomical structure. Experiments on 72 HCP subjects with 17 LPFC sulci show that WGDT significantly outperforms equidistance-based encoding schemes (ADT, Disk) on small, variable sulci with a single click, while maintaining practical runtime under 0.5 seconds.

## Strengths
- **Principled and novel technical contribution.** The curvature-aware geodesic distance on the sphere is a clean, physically motivated approach. It exploits the specific geometry of cortical surfaces — propagating faster along sulcal valleys (H ≥ 0) and slower across gyral ridges (H < 0) — in a way that equidistance-based ADT and Disk signals cannot.
- **Statistically rigorous evaluation.** The paper uses 5-fold cross-validation, 10 initial click locations per subject-sulcus combination averaged into a single performance value, paired t-tests with FDR correction across 17 sulci, and reports adjusted p-values. This is more careful than many interactive segmentation papers.
- **Consistent advantage on the hardest cases.** WGDT shows significant improvement (adjusted p < 0.05) with a single click on all 9 small and variable sulci — precisely the cases that motivate the work — while large sulci show comparable performance across methods. The narrowing gap with more clicks is correctly interpreted as an efficiency result.
- **Practical runtime.** At under 0.5 seconds per click (including signal encoding, re-tessellation, and forward pass) on meshes with 100k–170k vertices, the framework supports real-time interactive refinement.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **Untested claim of backbone complementarity (Section 2.5).** The paper states that SPHARM-Net's isotropic filters limit expressive power and that WGDT "addresses this limitation by complementing the extracted features." This specific claim is never experimentally validated — no ablation varies the backbone or the signal independently. While the core comparison (WGDT vs. ADT/Disk with the same backbone) is unaffected, the assertion about why WGDT helps would be stronger if tested.
- **No human-in-the-loop validation.** The evaluation relies entirely on simulated clicks that match the training distribution (always targeting the largest mislabeled component and sampling near its center). While simulated-click evaluation is standard practice in interactive segmentation, the practical claims about "reducing human effort" would be strengthened by a small human annotation study or a robustness analysis with alternative click simulation strategies (e.g., clicking near boundaries, targeting smaller components). The paper does not explicitly acknowledge this limitation.
- **Standard deviations for Dice scores not reported in main text.** Results are shown visually in Figures 4 and 5 with statistical significance, but no summary table of means and variance appears in the main paper. Table 2 provides runtime mean±std, but no analogous table exists for the primary performance metric. Given the modest sample (72 subjects, ~14 per fold), knowing the spread is important for assessing consistency.
- **Automatic baseline comparison is predictably favorable.** The comparison showing WGDT outperforming Lyu et al. and Lee et al. methods (Section 4.2) is expected because the interactive method receives privileged click information. The paper is transparent about this (no interactive baselines exist) but presents it as a headline result, which risks overclaiming. The meaningful comparison that isolates the curvature-aware contribution is WGDT vs. ADT/Disk under identical conditions, which is cleanly executed.
- **Hyperparameter sensitivity acknowledged but unexplored.** The method's performance depends on k (curvature modulation) and σ (propagation cutoff), yet the paper states selecting appropriate values "is therefore necessary to balance coverage and precision, which we leave for future work." A sensitivity analysis showing performance as a function of these parameters would strengthen the contribution.
- **Speed function behavior near zero-curvature regions not discussed.** The eikonal equation with isotropic exponential speed may produce ambiguous front propagation where mean curvature is near zero (flat regions or saddle points), potentially causing the guidance signal to leak outside the intended sulcus. This methodological gap merits discussion.

### Trivial
None.

## Nice-to-Haves
- A small human annotation study (even 1–2 raters on a subset of sulci) would directly validate the practical claims.
- An ablation replacing SPHARM-Net with a graph CNN on the sphere would clarify whether WGDT's benefit is backbone-independent.
- Adding a summary table of Dice means and standard deviations across methods and clicks in the main text.

## Removed Points
These points from the input review are removed:
- **Criticism about the "no prior studies" claim being too strong**: Removed because the paper qualifies the claim with "to the best of our knowledge" and specifies *surface geometry*, distinguishing it from 2D/3D grid methods. The criticism misreads the scope.
- **`log(p_n, z_n)` formatting issue**: The reviewer notes this is a PDF parser artifact, not a paper flaw. Removed per formatting-nitpick rule.
- **Missing appendix content concerns**: Appendix A.3 and A.5 are parser-stripped; concerns about their content are removed per hard rules.
- **Generic scope-creep points** (e.g., "could extend to other cortical regions"): The paper explicitly discusses generalization as future work.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add a summary table of mean Dice scores with standard deviations across methods and click iterations in the main text.
2. Perform a backbone ablation (e.g., replacing SPHARM-Net with a graph CNN on the sphere) to test the complementarity claim.
3. Include a sensitivity analysis of k and σ (even on a subset of sulci) to help readers understand how these choices affect performance.
4. Acknowledge the simulated-click limitation explicitly in the Discussion and, if feasible, conduct a robustness test with alternative click simulation strategies.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>