## Summary

This paper proposes a pipeline to enhance 3T BOLD fMRI signals toward 7T quality by: (1) conformally mapping 3D cortical surfaces to a shared 2D parametric "brain disk" domain for cross-subject/cross-dataset alignment, and (2) applying an unpaired Schrödinger Bridge diffusion model (BDSB) to translate the low-quality disks toward the high-quality distribution. The method is evaluated on synthetic data (down-sampled 7T→3T), cross-dataset real data (3T NOD → 7T NSD), and a small paired 3T/7T dataset (TDM), with downstream pRF retinotopic decoding as the target application.

## Strengths

1. **Conformal mapping is a principled and highly effective solution to cross-subject/cross-dataset alignment.** The ablation in Table 3 is compelling: conformal mapping (R²=22.02) massively outperforms direct slicing (R²=6.1) and harmonic mapping (R²=16.97). This component is a genuine contribution that could serve as a preprocessing standard for multi-dataset cortical fMRI analysis.

2. **Evaluating on downstream pRF decoding is the right target.** Rather than only reporting image-quality metrics, the paper measures whether enhanced data yields better retinotopic maps — the metric that matters for the claimed application. The temporal stability analysis (Fig. 7b) and R² scatter plots (Fig. 7a) are well-designed diagnostics.

3. **The paper candidly acknowledges its data limitations.** The "Lack of Paired Data" and "Synthetic Data" sections in the Conclusion are honest about the constraints: synthetic degradation is not a perfect proxy, and TDM is far too small. This transparency is commendable.

## Weaknesses

### Fatal
None.

### Major

1. **The synthetic experiment — which carries the strongest quantitative results — does not test the claimed problem.** The synthetic LQ data is created by down-sampling 7T NSD from 164k fsaverage to 32k fsLR and adding Gaussian noise (Section 2.1). This models spatial resolution loss and additive noise, but does *not* model the actual differences between 3T and 7T fMRI: different scanner hardware, pulse sequences, physiological noise profiles, susceptibility artifacts, B0 inhomogeneity, or subject populations. A model trained on this degradation solves a super-resolution + denoising problem on 7T data, not a cross-scanner translation problem. The quantitative headline results (SSIM=0.855, PSNR=25.05, FID=42.88, R²=24.00 in Table 2) are all from this setting. The paper acknowledges this limitation in the Conclusion but the abstract and introduction still claim the method "achieves signal quality and downstream performance comparable to native 7T scans" — a claim that the synthetic experiment does not support.

2. **The cross-dataset real experiment lacks ground-truth validation.** In this setting, the model enhances real 3T NOD data toward the 7T NSD distribution, but no ground-truth 7T scan exists for the NOD test subjects. The two metrics used have known limitations:
   - **FID** measures distributional similarity between enhanced NOD disks and NSD disks. Since NOD and NSD are different datasets (different subjects, stimuli, acquisition protocols), a low FID could simply reflect that the model produces "7T-looking" disks regardless of whether the actual fMRI signals are more accurate.
   - **R²** is a goodness-of-fit measure for the pRF model, not an accuracy measure. If the enhancement smooths signals or removes noise, R² will mechanically increase — the pRF model will fit cleaner data better — *even if the resulting pRF parameters (center, size) are less accurate than those from the original 3T data*. The paper reports R²=25.91 for enhanced vs 20.26 for raw LQ, but without ground-truth pRF parameters (from a 7T scan of the same subjects), this increase alone is insufficient evidence of better decoding.

3. **The TDM validation is too thin to support strong conclusions.** The only paired 3T/7T data consists of 2 subjects, 1 session each, with eccentricity-based stimuli (no pRF evaluation possible). On this tiny dataset (3 test runs per subject), the proposed method does not achieve the best SSIM (0.718 vs 0.727 for OTT-GAN, Table 2). No confidence intervals, error bars, or statistical tests are reported anywhere in the paper. With this sample size, variance is almost certainly substantial and the reported metric differences may not be meaningful.

4. **Claims of "comparable to 7T quality" are overstated relative to the evidence.** The abstract states the method makes 3T data "comparable to 7T quality," and the conclusion says it "achieves signal quality and downstream performance comparable to native 7T scans." This claim is not supported by the evidence: (a) the synthetic experiment compares enhanced *down-sampled 7T* to original 7T, not real 3T to 7T; (b) the cross-dataset real experiment has no ground-truth 7T for the same subjects; and (c) the TDM experiment, the only direct 3T/7T comparison, shows the method does not even beat OTT-GAN on SSIM. The claims should be scaled back to match what the experiments actually demonstrate.

### Minor

1. **The ablation interpretation is selective.** Table 3 shows that adding PatchNCE regularization alone *worsens* both FID (34.23→42.64) and R² (22.02→21.88) compared to the conformal-mapped BDSB without regs. The paper claims "PatchNCE loss provides modest gains" — this is misleading for FID and R² (it improves SSIM and PSNR but degrades the two more important metrics). The full model (both regs) improves R² by ~2 points over conformal mapping alone but at a substantial FID cost (34.23→42.88). This trade-off is not discussed. The paper would benefit from a more balanced analysis of what the regularizations actually contribute.

2. **The temporal stability analysis (Fig. 7b) only examines the top-40 vertices by R².** These are the easiest cases — vertices with the strongest stimulus-locked response. Showing results for average or low-R² vertices would be more informative about the method's robustness.

3. **No statistical uncertainty is reported anywhere in the paper.** No error bars, confidence intervals, or standard deviations on any metric. For the synthetic experiment this is less critical, but for TDM (2 subjects) and cross-dataset experiments, variance could be large and single-point comparisons are unreliable.

### Trivial
None.

## Nice-to-Haves
- Compare against a simple non-learned baseline: conformal mapping + bicubic interpolation/Gaussian filtering on the disk, to isolate what the learning component actually adds.
- Add a sanity check: apply the trained model to NSD 7T data and check whether the "enhanced" output stays close to the original 7T. If the model distorts 7T data, that would suggest it is not learning a principled mapping.
- Report metrics on lower-R² vertices in the temporal stability analysis.

## Removed Points
These points are flagged to be removed, treat them with caution:
1. **"fast-DDPM not evaluated on TDM"** — Factually incorrect. Table 2 shows fast-DDPM *is* evaluated on TDM Real (SSIM=0.511, PSNR=14.06, FID=96.91). The "No pair data" entry applies only to the cross-dataset experiment where fast-DDPM cannot be used because it requires paired data that doesn't exist across datasets.
2. **"First approach claim should be checked against existing work"** — The claim is specifically about "unpaired learning across public datasets" for fMRI SNR/retinotopic improvement. Per the rules, I cannot verify the existence/non-existence of other methods without external sources; the claim is narrow enough to be plausible.
3. **"Missing related works on fMRI enhancement"** — Per the rules, I should not mention missing related works as I cannot verify them externally.
4. **"The BDSB-specific contribution is marginal" framing** — On re-examination, the base BDSB model (SB + adversarial loss on conformal disks, no regs) achieves R²=22.02 vs harmonic=16.97, a 5-point gain. The BDSB method's contribution is distinct from the conformal mapping preprocessing. The marginal component is the *regularizations*, not the BDSB model itself. This nuance was lost in the reviewer's framing.
5. **"PatchNCE hurts both metrics"** — Slight inaccuracy. PatchNCE alone improves SSIM (0.849→0.858) and PSNR (24.26→24.88) while worsening FID (34.23→42.64) and R² (22.02→21.88). It helps 2 of 4 metrics. The corrected observation is maintained in Minor Weakness #1.

## Novel Insights

None beyond the paper's own contributions. The key insight not fully exploited by the authors is that the conformal mapping component may be the pipeline's most impactful element, and a simpler non-learned enhancement on conformally aligned disks could serve as a stronger baseline against which to measure the BDSB model's added value.

## Suggestions

1. **Scale back the claims.** Replace "comparable to 7T quality" with more measured statements like "consistently improves 3T fMRI quality as measured by [specific metrics]" that accurately reflect the experimental evidence.
2. **Add a non-learned baseline** — conformal mapping + conventional interpolation/denoising — to the ablation in Table 3, to isolate what the learning-based BDSB component contributes beyond the mapping and basic signal processing.
3. **Add error bars or confidence intervals** for the TDM experiment and cross-dataset experiments where test sizes are small. At minimum, report standard deviations across test subjects or runs.
4. **Discuss the FID/R² trade-off in the ablation** (conformal alone: best FID at 34.23 vs full model: best R² at 24.00 but FID degrades to 42.88). Explain why this trade-off is acceptable for the target application.
5. **Expand the temporal stability analysis** to include mid-range and low-R² vertices, not just the top 40.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>