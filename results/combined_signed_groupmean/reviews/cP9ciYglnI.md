## Summary

This paper proposes a shape-adaptive guidance signal (Weighted Geodesic Distance Transform, WGDT) for interactive cortical sulcal labeling on spherical surface representations. The core idea is to solve the eikonal equation on the unit sphere with a curvature-dependent propagation speed (Eq. 4: \(F = e^{kH}\)), so the signal travels faster along sulcal valleys and slower along gyri. This curvature-aware signal is fed into a spherical CNN (SPHARM-Net) alongside geometric features to iteratively refine sulcal labels from user clicks. Evaluated on 72 HCP subjects with 17 LPFC sulci, WGDT with a single click outperforms isotropic baselines (ADT, Disk) on small/variable sulci with statistical significance, and achieves <0.5s runtime per click.

## Strengths

- **The curvature-aware propagation mechanism is elegant and well-motivated.** Encoding user clicks via an eikonal equation whose speed depends on mean curvature (Eq. 4) is a physically natural design for sulcal following. Figure 3 provides direct visual evidence: WGDT concentrates along sulcal valleys while ADT and Disk spill over into gyri. **[impact: +9.56]**

- **Rigorous statistical evaluation.** Paired t-tests with FDR correction (q=0.05) across 17 sulci, 10 initializations per subject averaged, and 5-fold cross-validation is substantially more careful than most medical imaging segmentation papers. The separate analysis of 8 large/consistent vs. 9 small/variable sulci is honest and informative. **[impact: +10.00]** / **[impact: +8.74]**

- **Practical runtime.** Table 2 reports <0.5 seconds per click (including WGDT encoding, tessellation, and forward pass), demonstrating real-time feasibility for an interactive tool. **[impact: +6.39]**

- **Well-motivated problem.** The paper correctly identifies that small/shallow sulci are poorly handled by automatic methods (Figure 1), and makes a compelling case for spherical mapping to avoid occlusion of buried brain structures like the Sylvian fissure. **[impact: +2.12]**

## Weaknesses

### Fatal
None.

### Major

1. **The WGDT signal and SPHARM-Net backbone are confounded.** Section 2.5 explicitly states that SPHARM-Net "has limited expressive power due to the isotropic weighting of its convolutional filters" and that "the proposed guidance signal addresses this limitation by complementing the extracted features." This means the evaluation measures WGDT + SPHARM-Net against ADT/Disk + SPHARM-Net, without isolating whether WGDT's benefit is backbone-independent. If evaluated with a more expressive spherical CNN (e.g., DeepSphere, S2CNN), the margin might shrink. An ablation with at least one additional backbone is needed to establish that WGDT's advantages generalize beyond compensating for SPHARM-Net's expressivity deficit. **[impact: −9.29]**

2. **No table of numerical results and an unsupported empirical claim.** The paper relies entirely on figures (Figures 4, 5) and p-values for quantitative results. With 17 sulci × 5 encoding schemes × 3 click counts = 255 data points, a summary table with mean Dice and standard deviations is necessary for readers to assess effect sizes. Additionally, the claim "By 2 or 3 clicks, the variable sulci reach near-perfect accuracy" (line 198) is unquantified — the paper never defines what Dice threshold constitutes "near-perfect." **[impact: −9.68 / −9.72]**

### Minor

3. **Simulated clicks favor centered positions.** The click simulation (Section 2.2) places initial clicks near the center of the largest connected component. For WGDT, whose propagation is anisotropic and follows sulcal valleys, a centered starting point is a near-ideal condition. While the paper introduces modest variation via weighted random sampling and averages over 10 runs, a sensitivity analysis with systematically off-center clicks would strengthen real-world applicability claims. **[impact: −0.02]**

4. **No robustness test for curvature noise.** Mean curvature \(H\) (used in Eq. 4) can be noisy on real cortical surfaces due to reconstruction artifacts. The paper acknowledges this in the limitations but does not test how WGDT degrades with noisy curvature (e.g., via synthetic noise injection). **[impact: −0.00]**

5. **No variance reporting across initialization seeds.** The paper averages across 10 runs per subject but does not report standard deviations. A statement of variance across runs would clarify whether WGDT's advantage is stable. **[impact: −0.00]**

### Trivial
None.

## Nice-to-Haves

- A comparison against a competitive interactive method adapted from mesh/point-cloud segmentation (the paper explains why SAM-based projection approaches are non-trivial to adapt, which is reasonable, but a best-effort adaptation would further strengthen the evaluation).
- Joint modeling of morphologically similar sulci to improve generalization.
- An analysis of how hyperparameters \(k\) and \(\sigma\) interact.

## Removed Points

These points from the input reviews were evaluated and removed:

1. *"The σ value for ADT/Disk is not matched to the WGDT σ"* — **Removed (factually incorrect).** The paper states ADT and Disk use σ ∈ [π/32, 3π/64, π/16], which includes π/32 — the same value used by WGDT. The σ values do overlap.

2. *"No comparison against competitive interactive segmentation methods (Kontogianni et al., Lang et al., SAM)"* — **Removed.** The paper explicitly explains why adapting these methods is non-trivial: "projecting the 3D mesh onto a 2D plane... often results in the occlusion of deeply buried brain structures." Demanding adaptation of fundamentally planar methods for a spherical-domain task is scope creep.

3. *"Training one model per sulcus limits scalability"* — **Removed.** This is a practical design choice the paper justifies, noting it is consistent with common practice in medical interactive segmentation.

4. *"No comparison against a learned guidance signal"* — **Removed.** Beyond the paper's stated scope; listed as future work.

5. *"Novelty claim in line 47 is too broad"* — **Removed.** The claim is precise enough given the specific combination: curvature-aware propagation on the sphere as an interactive guidance signal for cortical sulci.

## Novel Insights

The reviews surface a genuine confound that the paper partially acknowledges but does not experimentally address: the WGDT signal's benefit and SPHARM-Net's limited expressivity are coupled in the evaluation design. This is a useful insight for the authors, as a backbone ablation would cleanly separate the signal's contribution from backbone compensation. The other major weakness — absence of a numerical results table — is a presentation gap that obscures effect sizes and makes the unquantified "near-perfect" claim unverifiable.

## Suggestions

1. **Add a backbone ablation:** Evaluate WGDT vs. ADT/Disk with at least one more expressive spherical backbone (e.g., DeepSphere, S2CNN) to demonstrate that WGDT's benefit is backbone-independent.
2. **Include a summary table** of mean Dice ± std for all 17 sulci × encoding schemes × click counts.
3. **Add a click-position sensitivity analysis** showing WGDT's performance with off-center clicks.
4. **Quantify the "near-perfect" claim** with specific Dice thresholds or ranges.
5. **Report variance across the 10 initialization seeds** to show result stability.

## Score and Decision

**Calibration anchors consulted across rounds:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `u1cQYxRI1H.md` | 10.00 | R1 | No | Not topically relevant (illumination harmonization) |
| `gwZ90hFSL2.md` | 1.00 | R1 | No | Not topically relevant (cross-lingual robotics) |
| `5lUdTogEL3.md` | 1.00 | R1 | No | Not topically relevant (person re-id) |
| `Gvg3nXZvyg.md` (IntRaBench) | 3.00 | R1 | Yes | Benchmark paper with limited novelty; our paper has a genuinely novel technical contribution |
| `8zCB9rTnmE.md` (TPP) | 4.75 | R1 | Yes | Missing strong baselines (−9.74) and unclear innovation (−10.00); our paper has a cleaner contribution |
| `Cf0K6jgzZt.md` (G2Sphere) | 5.33 | R2 | Yes | Spherical signal domain similar; weaknesses include "limited novelty" (−10.00) — more foundational than our paper's issues |
| `NhLBhx5BVY.md` (Neuron seg) | 5.33 | R2 | Yes | Limited novelty (−10.00); our paper's idea is more domain-grounded |
| `8ZLzw5pIrc.md` (OIS) | 6.00 | R1 | Yes | SOTA results but technical novelty questioned (−9.79, −9.89); our paper has cleaner novelty but weaker evaluation |
| `Pm1NXHgzyf.md` (SegLLM) | 6.00 | R1 | Yes | Strong experimental validation with thorough ablations (+10.00); our paper's evaluation is less thorough |

**Round 1 bracket:** [4.0, 6.5]
**Narrowing (Round 2):** The paper is stronger than G2Sphere (5.33) due to a more genuinely novel mechanism but weaker than OIS/SegLLM (6.00) in evaluation thoroughness.
**Final placement:** The two dominant weaknesses — backbone confound (−9.29) and missing numerical results (−9.68, −9.72) — are significant but fixable. The core technical contribution is clean and well-motivated. Placing above G2Sphere (5.33) and below OIS (6.00): **5.5**.

<score>5.5</score>
<decision>Borderline (leaning accept with revisions)</decision>