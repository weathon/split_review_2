Now I have enough calibration data. Let me finalize the review.

## Summary

This paper proposes a pipeline for enhancing 3T BOLD fMRI to approximate 7T quality for visual retinotopic decoding. The method maps 3D cortical surfaces to 2D parametric brain disks via conformal mapping, then applies a Schrödinger Bridge diffusion model (BDSB) trained on unpaired 3T/7T data to enhance the 3T signals. The paper evaluates on synthetic (down-sampled 7T + Gaussian noise), cross-dataset real (3T NOD → 7T NSD without ground truth), and limited paired real (TDM, 2 subjects) settings.

## Strengths

- **The conformal mapping + disk parameterization (Section 2.2) is a technically well-motivated contribution.** It preserves cortical topology across subjects and datasets while enabling standard 2D image translation architectures. The ablation study (Table 3) credibly shows conformal mapping outperforms harmonic mapping (R² 22.02 vs 16.97) and direct slicing (6.10), and the BD-SSIM regularization term provides meaningful gains in pRF decoding accuracy (R² from 22.02 to 24.00). This is the paper's strongest concrete contribution. (weight: +3.84)

- **The problem is genuinely important and well-scoped.** The scarcity of 7T fMRI relative to 3T is a real bottleneck for high-resolution retinotopic mapping, and existing medical image enhancement work has focused overwhelmingly on structural modalities rather than functional fMRI. (weight: +1.22)

- **The inclusion of both signal-level metrics (SSIM, PSNR, FID) and a downstream task metric (pRF R²) is the right evaluation strategy.** Pure image similarity can be gamed, and requiring improved pRF decoding adds a functional validation check. The scatter plots (Figure 7) showing R² consistency and receptive center stability are informative. (weight: +3.13)

- **The experimental design is thoughtfully structured given the fundamental data constraint.** The paper honestly acknowledges that large-scale paired 3T/7T fMRI with identical stimuli does not exist publicly, and designs three complementary experiments to triangulate evidence (Section 2.1, Discussion). (weight: +1.31)

## Weaknesses

### Major

- **The cross-dataset real experiment lacks meaningful ground truth, making its metrics ambiguous for the central claim.** (Section 2.1, Table 2 cross-dataset rows) The paper evaluates using (a) FID between enhanced NOD data and 7T NSD training data from different subjects who viewed different stimuli — distribution mismatch from subject, stimulus, and dataset differences is conflated with enhancement quality — and (b) pRF R² on enhanced data, which measures how well the pRF model fits the enhanced signals, not whether the signals are accurate. Higher R² can reflect added structured content rather than genuine signal recovery toward 7T quality. The paper transparently notes the lack of ground truth, but the abstract's claim that the method "makes 3T data comparable to 7T quality" is not supported for real 3T data by this experiment. (weight: -6.35)

- **The synthetic experiment uses an unrealistic degradation model that does not meaningfully approximate real 3T/7T differences.** (Section 2.1 "Synthetic Data", Table 2 synthetic rows) The paper generates "3T-like" data by down-sampling 7T NSD from 164k fsaverage to 32k fsLR and adding per-vertex Gaussian noise. This captures none of the actual physical differences between 3T and 7T BOLD fMRI: different T2* decay rates, BOLD contrast-to-noise ratios, physiological noise characteristics (thermal vs. physiological noise scale differently with field strength), pulse sequence parameters, B0 inhomogeneity, and spatial specificity of the BOLD response. Reversing a known down-sampling + Gaussian noise degradation is substantially easier than actual 3T-to-7T enhancement. The paper acknowledges this in the Discussion ("such synthetic 3T-like data cannot fully capture scanner hardware...") but still uses synthetic results throughout to support claims of "7T comparable quality." (weight: -5.25)

- **The claim that the method "improves SNR" (abstract) is not directly verified by any explicit SNR or CNR metric.** PSNR requires ground truth and is only available in the synthetic/TDM settings (not for real cross-dataset data). No direct SNR estimate is reported for the cross-dataset experiment, which is the primary real-use scenario. (weight: -4.72)

### Minor

- **No statistical uncertainty is reported anywhere.** (Tables 2, 3) All results are single numbers with no variance estimates, error bars, or confidence intervals. This is significant because the synthetic and cross-dataset experiments each use only 2 test subjects, and the TDM experiment uses 2 subjects with a train/test split across 6 runs. Some differences are small enough that variance could change rankings (e.g., TDM SSIM: Proposed 0.718 vs OTT-GAN 0.727). (weight: -2.78)

- **Several baselines produce worse pRF R² than the raw (unprocessed) LQ input.** (Table 2 synthetic row) SCR-Net (13.54), fast-DDPM (15.53), Cycle-GAN (17.22), and OTE-GAN (16.89) all fall below raw LQ (18.30). The paper does not discuss why four out of five baselines degrade performance below doing nothing. (weight: -3.43)

- **The cross-dataset R² (25.91) is notably higher than the synthetic experiment's ground truth R² (24.00).** (Table 2) Since the cross-dataset task uses real 3T data while the synthetic task uses down-sampled 7T with known ground truth, one would expect lower performance on the harder real task. This discrepancy suggests that pRF R² in the cross-dataset setting may be inflated by added structure rather than reflecting genuine signal recovery toward 7T quality. (weight: -0.92)

- **The TDM experiment (the only paired ground-truth setting on real data) shows mixed results.** The proposed method does not win on SSIM (0.718 vs OTT-GAN 0.727), uses only 2 subjects, and employs non-standard eccentricity stimuli (not pRF). This limits the confirmatory weight of the TDM results. (weight: -0.34)

### Trivial

None.

## Nice-to-Haves

- Provide per-subject breakdowns or bootstrapped confidence intervals for all metrics to address the small test-set sizes.
- Consider anchoring cross-dataset pRF maps against retinotopic atlas templates (e.g., Benson et al. 2014, Wang et al. 2015) for a ground-truth-free functional validation.
- Test whether enhanced 3T data improves stimulus decoding accuracy (e.g., classification or reconstruction), providing an objective downstream task that does not depend on pRF model assumptions.
- Report an explicit SNR/CNR estimate from the real data experiments.

## Removed Points

The following points from the harsh critic input were removed after verification:

- Concern that "baselines were not properly tuned for this application" and "whether baselines were adapted to work with brain disks" — REMOVED. The paper states (line 160) "We adopt five 2D translation models to our pipeline as baselines," indicating baselines were integrated into the same pipeline. The claim that they may have been unfairly disadvantaged is speculative.
- Concern about "no analysis of failure cases" — REMOVED. The paper discusses inert vertices (Figure 5b, line 178): "for inert vertices, where the signal remains relatively constant, the alignment is weaker."
- Concern about "ROI boundaries not corresponding precisely to functionally defined retinotopic areas" — REMOVED. The paper uses standard FreeSurfer anatomical labels; requiring functionally-defined ROIs for validation is scope creep.
- Concern about "TDM stimuli being fundamentally different from pRF stimuli" — REMOVED. The paper explicitly notes this limitation and only reports similarity metrics (not pRF) for TDM.
- Concern about "no variance or uncertainty quantification" — kept as Minor but downsized since the paper does use scatter plots to show per-vertex variability (Figure 7).
- Concern about "stimulus comparability between NSD and NOD" — partially addressed by the paper noting both include pRF-fLOC stimuli.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. The most impactful improvement would be adding a validation strategy for the cross-dataset experiment that does not require paired ground truth — for instance, comparing pRF maps from enhanced 3T data against a standard retinotopic atlas, or measuring split-half reliability of pRF estimates.
2. Report explicit uncertainty estimates (per-subject breakdowns or confidence intervals) for all metrics.
3. Either moderate the central claim ("comparable to 7T quality") or provide substantially stronger evidence for it on real data.

## Score and Decision

**Calibration anchors used:**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| fMRI-PTE (BZkKMQ25Z7) | 4.00 | R1 | Yes | Similar fMRI domain; had heavier innovation criticisms but broader experiments; our paper has stronger methodological contribution but sharper evaluation gap |
| Brain fMRI alignment (GYAvwLviup) | 4.25 | R1 | Yes | Similar cross-subject fMRI; had limited subjects and missing comparisons; our paper has similar evaluation strength |
| Rethinking Brain-to-Image (UUNTAwJIIn) | 4.00 | R2 | Yes | Similar fMRI decoding domain; had heavy scientific grounding criticisms (-9.55); our paper's evaluation gap is comparable |
| Bi-DPM (GqsepTIXWy) | 5.00 | R2 | Yes | Medical image translation; had one very heavy weakness (-12.45) but very strong positive items; our paper has more consistent moderate weaknesses |
| Efficient Multi-Subject (z2QdVmhtAP) | 3.00 | R1 | Yes | Lower-scoring fMRI paper with missing details (-7.76) and limited innovation (-8.78); our paper has stronger methodological substance |
| MRI SR Cerebellum (exei8zvY13) | 2.00 | R1 | Yes | Scored low due to "no technical contribution" (-9.14) and "out-of-the-box" (-10.40); our paper has more genuine contribution |

**Round 1 bracket:** 3.5–5.0

**Weighted-item comparison placing the final score:** The paper's two heaviest weaknesses (cross-dataset lack of ground truth at -6.35, synthetic unrealistic at -5.25) are structural — they concern whether the core claim can be evaluated at all from the presented evidence. These are more central to the paper's thesis than the relatively fixable presentation issues that weighed down fMRI-PTE (4.00). However, the paper's positive-weighted items (conformal mapping +3.84, dual metrics +3.13) are genuinely stronger contributions than those of the lowest-scoring anchors (e.g., MRI SR cerebellum at 2.00 which had near-zero positive weights). The net balance positions this paper below 5.0 (the Bi-DPM anchor, which had one super-heavy weakness but stronger empirical results) and above 4.0 (the fMRI-PTE anchor, which had weaker methodological contributions). The key observation placing it at 4.5 specifically: the evaluation gap directly undermines the paper's headline claim, but the pipeline itself (conformal mapping + BD-SSIM regularization) is a technically sound and potentially useful contribution that could be validated with further work.

**Score:** 4.5
**Decision:** Reject

**Reasoning for borderline-reject decision:** The paper addresses an important problem and proposes a technically sensible pipeline. However, the evaluation does not convincingly support the central claim that 3T data can be enhanced to "7T quality" on real data. The synthetic experiment uses an unrealistic degradation model, the cross-dataset experiment lacks ground truth and its metrics are ambiguous, and the TDM experiment shows mixed results on 2 subjects. The gap between what is claimed (abstract, introduction) and what is demonstrated is too large for acceptance at a top-tier venue in its current form.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>