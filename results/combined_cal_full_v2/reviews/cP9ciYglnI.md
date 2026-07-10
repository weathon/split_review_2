## Summary

This paper introduces a shape-adaptive guidance signal (WGDT) for interactive cortical sulcal labeling on spherical surfaces. The key idea is to encode user clicks by solving the eikonal equation with a curvature-dependent speed function on the sphere, so the guidance signal propagates faster along sulcal valleys and slower across gyral ridges — adapting to cortical morphology rather than using equidistance-based signals. Evaluated on 72 HCP subjects with 17 LPFC sulci, the WGDT signal significantly outperforms angular-distance-transform (ADT) and binary-disk signals on all 9 small/variable sulci with a single click (adjusted p < 0.05), and the full pipeline runs in under 0.5 seconds per click.

## Strengths

- **Domain-motivated and genuinely novel guidance signal (WGDT, Section 2.3.3).** Encoding user clicks by solving the eikonal equation with a curvature-dependent speed function — so the signal propagates faster along sulcal valleys (H ≥ 0) and slower across gyral ridges (H < 0) — directly addresses the limitation of equidistance-based signals that ignore cortical morphology. This is a signal designed from first principles for the specific geometry of cortical sulci. **[weight=7.89]**

- **Clean ablation of the guidance signal itself (Section 4.1).** The comparison against ADT and Disk signals holds the backbone, the interactive loop, the click simulation, and the per-sulcus binary task formulation constant. The only variable is the guidance signal. Under this controlled comparison, WGDT significantly outperforms both equidistance baselines on all 9 small/variable sulci with a single click (adjusted p < 0.05, FDR-corrected). **[weight=9.12]**

- **Appropriate use of spherical mapping.** The paper correctly identifies that projecting cortical surfaces onto 2D planes (as done by SAM-based approaches) occludes deeply buried structures like the Sylvian fissure. Spherical mapping preserves full topology and is naturally compatible with spherical CNNs. **[weight=8.13]**

- **Statistical rigor above the typical standard for medical image segmentation papers.** The evaluation uses 5-fold cross-validation, FDR correction across 17 sulci (q = 0.05), paired t-tests, and 10 initial click seeds per subject averaged into a single performance value. **[weight=9.38]**

- **Practical runtime (Table 2).** Total time per click < 0.5 seconds (175 ms for signal encoding + 208 ms for re-tessellation + 28 ms forward pass) on meshes with 100k–170k vertices, fast enough for real-time interactive use. **[weight=9.51]**

## Weaknesses

### Fatal
None.

### Major

- **The automatic baseline comparison (Section 4.2, Figures 5–6) conflates task formulation with interactivity.** The proposed method trains a separate binary classifier per sulcus (17 models), while the automatic baselines (Lyu et al. 2021, Lee et al. 2025a,b) are multi-class models that must simultaneously distinguish all 17 sulci from each other and from background. A per-sulcus binary classifier is strictly easier — it only needs to separate one class from everything else, with no risk of confusing one sulcus for another. The paper claims "WGDT significantly outperforms the baselines with a single click in all small sulci" and frames this as interactive labeling beating automatic methods. But the observed gains could be partially attributable to the easier per-sulcus binary formulation rather than to interactivity or the WGDT signal. The required control — training the same SPHARM-Net backbone as a per-sulcus binary classifier without any user clicks — is absent. **This does not invalidate the WGDT contribution** (the Section 4.1 comparison against ADT/Disk is clean and unaffected), but the headline claim is overstated. The paper states "By retraining all baselines, we ensure a fair comparison" — retraining ensures the same data and features, but not the same task difficulty. **[weight=3.19]**

### Minor

- **No real user validation (Sections 2.2, 3.3, 4).** All user interactions are simulated by an algorithm that clicks near the center of the largest mislabeled connected component. The paper states the simulation "mimics a trained rater" but provides no evidence for this claim. Real annotators may click inconsistently, near boundaries, in suboptimal locations, or on adjacent structures, and may deviate from the "largest mislabeled component first" strategy. Without a user study or at minimum a sensitivity analysis with noisy/off-center click locations, the reported Dice scores may overstate real-world performance under imperfect user input. **[weight=1.35]**

- **Limited generalization evidence.** The dataset consists of 72 healthy subjects (22–36 years) from HCP, left hemisphere LPFC only. With 5-fold cross-validation, the effective training set is ~57 subjects per fold. No results on the right hemisphere (sulcal asymmetry is well-documented), other cortical regions, or clinical/aging populations. The paper acknowledges these scope limitations (Section 5), which is good practice, but they bound the contribution substantially. **[weight=-0.03]**

### Trivial
None.

## Nice-to-Haves

1. **Per-sulcus automatic (no-click) ablation of SPHARM-Net.** Training the same backbone on the same per-sulcus binary task without any guidance signal would isolate how much of the gain comes from interactivity itself versus the per-sulcus specialization versus the WGDT-specific encoding. This would also provide a fairer reference point for the automatic baseline comparison.
2. **Click location robustness analysis.** Adding a sensitivity analysis where click locations are perturbed by angular offsets (e.g., ±5°, ±10°) would strengthen claims about real-world applicability without requiring a full user study.
3. **Clarify "current prediction" input initialization** (Figure 2, Section 2.1) — the paper mentions this as an optional input but does not specify how the model handles step 0 when no prior prediction exists.
4. **Clarify curvature mapping** — the paper uses mean curvature H from the white-matter surface as a spherical function H: S² → R (Section 2.3.3). It should state explicitly that these values are mapped vertex-wise to the sphere, since curvature is not a conformal invariant under spherical mapping.

## Removed Points

- **Loss notation concern (Equation 6):** The reviewer flagged `log(p_n, z_n)` as unusual notation. This is a PDF-extraction artifact; the original paper likely uses standard cross-entropy notation. Removed per hard rules on formatting artifacts.
- **Missing quantitative tables in the main paper:** The reviewer wanted Dice tables in the main paper rather than the appendix. Since the appendix is stripped by the parser and the rule states to assume appendix content exists, this criticism is removed.
- **Hyperparameter asymmetry (σ for WGDT vs ADT/Disk):** The paper explicitly states that σ was tuned for each method (Section 3.2). Using different optimal σ values for different signal types is standard and reasonable. Not a weakness.
- **"Current prediction" initialization and curvature mapping:** These are technical questions, not weaknesses — moved to Nice-to-Haves.
- **Missing related works, learning curve experiments, scope-expansion suggestions:** Either not verifiable without external sources, outside the paper's stated scope, or demanding practices not standard in the field.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a clear confound in the automatic baseline comparison that the paper does not address, but this is a methodological limitation rather than a novel analytical insight.

## Suggestions

1. Add the per-sulcus automatic (no-click) ablation of SPHARM-Net to isolate the additive value of interactivity from the per-sulcus formulation advantage. This would both strengthen the core claim and provide a fairer reference point for the automatic baseline comparison.
2. Reframe the headline claims about outperforming automatic methods to transparently acknowledge the task-formulation difference, or add the missing control experiment.
3. Add a sensitivity analysis with noisy/off-center click locations to demonstrate robustness to imperfect user input.
4. Clarify the initialization of the "current prediction" input channel at step 0.

---

**Calibration Summary:**

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| IntRaBench (Gvg3nXZvyg) | 3.00 | R1 | Yes | Benchmark paper with limited novelty; my paper is clearly stronger |
| P2SAM (czvVNVLr7R) | 4.75 | R1 | Yes | Mixed reviews, unclear contribution; my paper has cleaner experiments |
| InstanceSegSupervoxel (NhLBhx5BVY) | 5.33 | R2 | Yes | Comparable quality profile: novel loss with missing ablation concerns |
| AGILE3D (9cQtXpRshE) | 5.50 | R2 | Yes | Interactive 3D segmentation; has user study my paper lacks but my core experiment is cleaner |
| DiffeomorphicMesh (gxhRR8vUQb) | 7.00 | R1/R2 | Yes | Stronger paper with theoretical depth; sets upper bound |

**Round-1 bracket:** Between P2SAM (4.75) and DiffeomorphicMesh (7.00). **Narrowing:** My paper's weighted profile (strengths 7.89–9.51, main weakness 3.19) is stronger than InstanceSegSupervoxel (5.33) and comparable to AGILE3D (5.50). The DiffeomorphicMesh paper's theoretical contribution solidly exceeds my paper's, capping the score at 6.0–6.5. The task-formulation confound is the primary moderating factor — without it, the paper would sit closer to 6.5.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>