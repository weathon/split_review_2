## Summary

The paper proposes a curvature-aware geodesic distance transform (WGDT) as a guidance signal for interactive cortical sulcal labeling on spherical surface representations. User clicks are encoded by solving the eikonal equation with a mean-curvature-dependent speed function, so the signal propagates faster along sulcal valleys than across gyri. The method is evaluated on 72 HCP subjects with 17 LPFC sulci using SPHARM-Net as the backbone, outperforming equidistance-based encoding schemes (ADT, Disk) on small and variable sulci.

## Strengths

1. **Well-motivated problem with a sensible technical approach.** Small/variable sulci genuinely challenge automatic methods (Figure 1), and existing interactive frameworks rely on 2D projections that occlude buried cortical structures (Section 1). Spherical mapping avoids this occlusion, and using the eikonal equation with curvature-dependent speed (Equations 3–4) to propagate click influence along sulcal valleys is a natural and principled adaptation of geodesic distance transforms to cortical anatomy.

2. **The core experiment (WGDT vs. ADT vs. Disk) is the right test and yields clean results.** Figure 4 and Section 4.1 show that WGDT yields statistically significant improvements (adjusted p<0.05) specifically on the 9 small/variable sulci, while all three methods perform comparably on large/consistent sulci. This pattern validates the paper's motivation with internal coherence. Qualitative results (Figure 6) further support the claim.

3. **Carefully designed click simulation protocol.** Section 2.2 describes an iterative refinement procedure that identifies the largest mislabeled connected component, filters boundary-adjacent points, and samples near the region center with weighted random sampling. This addresses realistic failure modes and is described in sufficient detail to be reproducible.

4. **Practical runtime.** Table 2 reports ~411 ms per click (~28 ms forward pass), indicating interactive-feasible latency.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **17 separate per-sulcus models are a practical limitation that is under-discussed.** Section 2.1 (line 59) states that a separate SPHARM-Net model is trained for each of the 17 sulci, justified by distinct morphological characteristics. This design choice means full cortical coverage would require 50+ models, and the paper does not analyze scalability, annotation cost, or the feasibility of multi-task/multi-class alternatives. This limits practical deployment.

2. **The comparison to automatic baselines (Section 4.2, Figure 5) is framed as validating the WGDT encoding but is not a controlled test of it.** The paper shows that WGDT with 1 click outperforms three automatic baselines. However, any interactive method with a click-based spatial prior would likely outperform automatic methods under these conditions. The paper does not report ADT/Disk against automatic baselines, so the reader cannot determine whether WGDT's advantage over automatic methods is due to the encoding scheme or simply due to the presence of a click. This does not undermine the main validation (Section 4.1 against ADT/Disk), but the abstract's phrasing — "even a single click using the proposed encoding scheme outperforms fully automatic methods and equidistance schemes" — conflates two different types of evidence.

3. **The backbone choice (SPHARM-Net) creates an unablated confound for the WGDT advantage.** The paper explicitly states (line 131) that SPHARM-Net has "limited expressive power due to the isotropic weighting of its convolutional filters" and that WGDT "addresses this limitation." This means the reported WGDT advantage is conditional on a deliberately weak backbone. Without an ablation with a more expressive backbone (e.g., a graph CNN), it is unclear whether WGDT's advantage would persist or would be diminished.

4. **Key quantitative results are in the appendix (stripped from the submission reader).** Mean Dice scores and standard deviations for the main comparisons are not in the main text. Error bars in Figures 4–5 are not explicitly defined in the captions (standard deviation? standard error? confidence interval?). Without effect sizes and variability, the practical significance of the reported statistical improvements is difficult to assess.

5. **Several methodological details are underspecified.** (a) The mean curvature H in Equation 4 is defined as a spherical function H: S²→ℝ (line 107), but how curvature computed on the original cortical surface is transferred to the spherical domain is not described. Since spherical mapping introduces metric distortion, the distinction matters for reproducibility. (b) The ADT/Disk σ values (Section 3.2, line 153) are not stated to have been optimized on a validation set — only WGDT's σ is described as optimized. (c) The re-tessellation to 40,962 vertices from 100k–170k (Section 3.3) is a significant resolution reduction whose impact on fine-grained sulcal labeling is not discussed.

6. **Runtime is only measured on the largest sulcus (central sulcus).** For smaller sulci the WGDT encoding may be faster, but this is not reported. The 175 ms for WGDT signal encoding may accumulate across multiple clicks.

### Trivial

None.

## Nice-to-Haves

- **Ablate the backbone.** Run WGDT vs. ADT/Disk with at least one alternative backbone (e.g., a graph CNN) to test whether the advantage generalizes beyond SPHARM-Net's limited expressivity.
- **Report ADT/Disk against automatic baselines** to disentangle the effect of having a click from the effect of the specific encoding scheme.
- **Quantify practical benefit** (e.g., number of clicks saved to reach a target Dice threshold of 0.90 on small sulci).
- **Discuss generalizability** to other spherical-topology surfaces or to full cortical coverage.

## Removed Points

These points from the input review were removed with justification:

1. **Spherical mapping claim is "misleading"** (from Critical Issue 3). The abstract states the approach "preserves structural information without the need for sacrificing anatomical details." In the neuroimaging context, FreeSurfer's spherical mapping is invertible and preserves topological relationships; the key advantage is avoiding occlusion (correctly stated later in Section 1). The phrasing is standard for this domain, not materially misleading. **Removed as a field-specific framing disagreement, not a substantive flaw.**

2. **Equation 6 notation concern** (log(p_n, z_n) not being standard cross-entropy). This is likely a PDF extraction artifact — the original submission almost certainly uses standard cross-entropy notation. **Removed as a parser artifact.**

3. **"Small dataset" criticism.** 72 subjects with 5-fold CV is modest but standard for manually annotated neuroimaging datasets, where each sulcus requires expert labeling. **Removed as a domain-inappropriate standard.**

4. **Missing discussion of limitations.** The discussion (lines 225–229) does mention generalization to other regions and hyperparameter tuning. The other omissions (17-model scalability, backbone reliance, dataset size) are reasonable future work directions, not critical omissions. **Demoted to the minor point about the 17-model design being under-discussed.**

5. **Criticism that automatic baseline comparison is fatal/evidential.** The paper's primary validation of WGDT is Section 4.1 (against ADT/Disk). The automatic baseline comparison is secondary context. The issue is presentation/framing, not a flaw in the core result. **Demoted to Minor.**

## Novel Insights

None beyond the paper's own contributions. The reviews surface no observation about the method, evaluation, or framing that would fundamentally change the interpretation of the paper's empirical claims.

## Suggestions

1. Move mean Dice scores and standard deviations (or confidence intervals) from the appendix into the main text, and explicitly define error bars in all figure captions.
2. Discuss the scalability of the per-sulcus modeling approach and whether multi-task learning is feasible.
3. Clarify how mean curvature is transferred from the original surface to the sphere (Section 2.3.3).
4. Rephrase the abstract to distinguish the evidence for the encoding scheme (WGDT vs. ADT/Disk in Section 4.1) from the evidence that interactive labeling beats automatic methods (Section 4.2), which is a different claim.

## Score and Decision

**Calibration anchors considered:**
- INTRABENCH (3.00, reject): interactive segmentation benchmark; less technical contribution than the current paper — current paper is stronger.
- Annotation by Clicks (4.50, reject): point-supervised medical segmentation; comparable domain specificity — current paper has better experimental design but similar narrowness.
- Cortical Surface Reconstruction (3.67, reject): cortical surface paper with unclear methodology — current paper is more clearly executed.
- fMRI Functional Connectivity (5.25, reject): neuroimaging paper rejected for limited novelty — comparable scenario.
- Order-aware Interactive Segmentation (6.00, accept): general interactive segmentation with SOTA on standard benchmarks — broader scope and stronger contribution than the current paper.
- Diffeomorphic Mesh Deformation (7.00, accept): strong theoretical contribution (sliced Wasserstein distance) with thorough evaluation — substantially stronger.

**Bracket**: 4.0–5.5. The paper is technically sound and well-executed for its domain, but the contribution is narrow and incremental for a general ML audience. The core technical novelty (curvature-dependent geodesic distance transform on a sphere) is a straightforward adaptation of well-established techniques, the evaluation is on a single small dataset (72 subjects, one hemisphere), and the paper does not demonstrate generalizability beyond the specific neuroimaging application. The calibration papers in the 4–5.5 range with similar characteristics (domain specificity, modest technical novelty, well-executed but narrow evaluation) tended to be rejected.

Score: 4.5 — borderline reject. The paper would be a stronger fit at a specialist venue (e.g., MICCAI, NeuroImage) where its careful domain-specific engineering contributions would be more appropriately valued. For ICLR, the contribution is too narrow and the technical novelty too incremental.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>