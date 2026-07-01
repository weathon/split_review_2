## Summary

This paper proposes BDSB, a framework that enhances 3T BOLD fMRI signals to approximate 7T quality for retinotopic decoding. The key ideas are (1) conformal mapping of 3D cortical surfaces onto a shared 2D parametric disk domain to align cross-subject data, and (2) an unpaired Schrödinger Bridge diffusion model (BDSB) with PatchNCE and BD-SSIM regularization to translate 3T brain disks toward the 7T distribution. The method is evaluated on three settings—synthetic (down-sampled 7T), cross-dataset real (3T NOD → 7T NSD), and paired real (TDM 3T/7T)—showing improvements in SSIM, PSNR, FID, and downstream pRF R².

## Strengths

1. **Principled cross-subject alignment via conformal mapping.** Projecting 3T and 7T cortical surfaces from different subjects into a shared 2D parametric disk (Section 2.2) is a geometrically sound way to make unpaired translation tractable. This is the paper's most distinctive methodological contribution and is clearly described.

2. **Thoughtful multi-setting evaluation strategy.** The three experimental designs (synthetic with ground truth, cross-dataset real for generalization, TDM paired real for limited validation) are well-motivated given the scarcity of paired 3T/7T fMRI data (Section 2.1, Table 1). The honest discussion of data limitations in Section 4 is a strength.

## Weaknesses

### Fatal
None.

### Major

1. **No 7T baseline metrics are reported, making the core claim untestable.** The abstract and conclusion state that enhanced 3T data is "comparable to 7T quality," but Table 2 never reports the actual 7T ground-truth values for any metric—including the average pRF R² on the synthetic experiment where original 7T data exists for the test subjects. The synthetic experiment (down-sampled NSD) has the original 7T data as ground truth, so the original 7T R² is computable. Without this reference, there is no way to judge how close an enhanced R² of 24.00 is to native 7T quality. Fig. 7(a) shows R² scatter plots with ground truth R² on the x-axis, but a summary statistic in Table 2 is needed to support the headline claim.

2. **The only real paired-data experiment (TDM) does not show consistent superiority.** Table 2 shows that on TDM—the most realistic evaluation setting, with the same subjects scanned at both field strengths—OTT-GAN achieves higher SSIM (0.727 vs. 0.718) and the proposed method's PSNR lead is negligible (19.24 vs. 19.18). The only clear win is on FID (62.09 vs. 84.45). Combined with the fact that TDM has only 2 subjects with a single session each, this weakens the evidence that the method reliably outperforms baselines on real paired data.

### Minor

3. **The R² improvement mechanism is not fully disentangled from potential variance inflation.** The pRF R² is defined as R² = 1 − SSE/SST (Section 2.4). If the enhancement model increases the variance of the BOLD signal (SST) without reducing prediction error (SSE), R² could mechanically rise. The paper provides some mitigating evidence—Fig. 5 shows enhanced BOLD signals aligning with ground-truth 7T, and Fig. 7(b) shows temporal stability across random stimulus intervals—but never decomposes R² into its SSE and SST components. A direct analysis would cleanly address this concern.

4. **Ablation study reveals an undiscussed trade-off.** Table 3 shows that the unregularized conformal mapping model achieves FID = 34.23, while adding PatchNCE and BD-SSIM regularization degrades FID to 42.88 (worse) while improving R² from 22.02 to 24.00. The paper focuses on the R² improvement without discussing why FID worsens. This is not necessarily a flaw (R² may be the more important metric for downstream decoding), but the trade-off should be acknowledged and analyzed.

5. **BD-SSIM is never formally defined.** Section 2.3 introduces "brain disk structural similarity measure (BD-SSIM)" as one of two regularization terms, but the paper does not specify whether this is standard SSIM applied to brain disk images, a modified version, or a new metric. The loss function in Eq. 5 references `λ_Reg_bdl` without definition.

6. **FID's suitability for fMRI brain disks is not motivated.** FID relies on Inception features trained on ImageNet. Brain disk images of fMRI activation patterns are semantically and structurally unlike natural images. The paper uses FID without justifying its applicability to this domain or considering alternative distributional metrics better suited for fMRI feature spaces.

### Trivial
None.

## Nice-to-Haves

- A direct comparison of enhanced R² against the native 7T R² on the synthetic experiment (single summary statistic in Table 2).
- An SSE vs. SST decomposition to confirm that R² gains come from reduced prediction error rather than variance inflation.
- Clarification of whether BD-SSIM is standard SSIM or a custom variant.

## Removed Points

These points were raised in the input review but are removed with justification:

- **"Slice" baseline inconsistency in Table 3**: The reviewer assumed "Slice" should match Table 2's raw LQ values. The paper explains that "Slice" is direct slicing without conformal mapping, which introduces geometric distortions—a different mapping strategy, not the same data. The reviewer's confusion is understandable given the table labeling could be clearer, but the paper does explain this distinction (Section 3, Ablation Study paragraph).

- **Cross-dataset real experiment lacks subject-level ground truth**: The paper explicitly acknowledges this limitation ("Since we do not have ground truth 7T fMRI for NOD subjects, we can only evaluate the results by the overall Fréchet inception distance (FID) and the downstream pRF decoding performance"—Section 2.1). The paper is transparent about this known data constraint.

- **Statistical significance not reported**: Point estimates without confidence intervals are standard practice in large-scale fMRI benchmark evaluations where single-run evaluation is the norm. This is not a weakness specific to this paper.

- **Missing related works**: Cannot be verified without external sources.

- **"First approach" claim is narrow**: This is a contribution claim, not an evidential weakness. Whether the reader finds it compelling is a matter of opinion.

## Novel Insights

The main insight from the reviewer analysis that goes beyond the paper's own claims is the tension in the ablation study: the unregularized Schrödinger Bridge achieves substantially better FID (34.23) than the full regularized model (42.88), yet the paper's narrative emphasizes only the R² improvement from regularization. This suggests the regularization operates differently on distributional fidelity vs. downstream task performance—a trade-off the paper should explicitly analyze rather than omit. The FID degradation may be acceptable if pRF decoding is the true objective, but the omission weakens the analytical thoroughness.

## Suggestions

1. Add a column to Table 2 reporting the 7T ground-truth metrics for the synthetic experiment (especially average pRF R²), so the reader can directly see how close the enhanced values come to native 7T.
2. Discuss the FID trade-off revealed in Table 3—even a brief paragraph acknowledging that regularization trades distributional fidelity for downstream task accuracy would improve internal coherence.
3. Provide a definition or citation for BD-SSIM in Section 2.3.
4. Consider computing and reporting SSE/SST components alongside R² to address the variance-inflation concern, or cite evidence that the concern does not apply in this setting (e.g., the temporal stability analysis in Fig. 7b).
5. Temper the claim "comparable to 7T quality" to match the evidence; e.g., "significantly closer to 7T quality than unenhanced 3T data" would be more precise.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Reject</decision>