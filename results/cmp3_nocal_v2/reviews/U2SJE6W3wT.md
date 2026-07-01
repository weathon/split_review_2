Now let me compile the final review.

## Summary

This paper proposes AdcVSR, a compressed one-step diffusion model for real-world video super-resolution that distills a large 3D DiT teacher (DOVE) into a pruned 2D SD backbone augmented with lightweight 1D temporal convolutions. A dual-head, dual-discriminator adversarial distillation scheme is introduced to disentangle and jointly optimize detail richness and temporal consistency. The resulting model achieves a 95% parameter reduction and 8× speedup over its teacher DOVE while maintaining competitive video quality and delivering the best temporal consistency (E_warp*) across both synthetic and real-world benchmarks.

## Strengths

1. **Well-motivated architectural insight (Section 3.2, Table 2).** The paper argues that heavy 3D spatio-temporal attentions introduce redundancy for Real-VSR because the LR input already provides structural layout and temporal continuity. The proposed "2D+1D" design follows from this insight: Table 2 shows it closes the DISTS gap to a pruned 3D model (0.2112 vs. 0.2098) while using 94% fewer parameters (0.55B vs. 8.36B) — a genuine engineering achievement.

2. **Dual-head discriminator design (Section 3.3, Table 3).** Decoupling detail and consistency assessment into separate heads with curated data types (real videos, shuffled videos, static images, random crops) is a principled response to the known detail-consistency conflict. Table 3 shows clear benefit: dual-head dual-domain (CLIP-IQA 0.6861, E_warp* 2.22) substantially outperforms both single-head dual-domain (0.6745, 6.32) and dual-head single-domain (0.6421, 3.59).

3. **Strong temporal consistency.** AdcVSR achieves the best E_warp* on both UDM10 (1.67) and VideoLQ (6.74), substantially outperforming its teacher DOVE (2.22 and 8.41). This is the clearest empirical signal that the temporal modeling and dual-head training work as intended.

4. **Impressive practical compression.** The paper demonstrates a 95% parameter reduction and 8× speedup over DOVE while maintaining competitive quality across a broad suite of metrics, placing AdcVSR among the fastest and lightest methods in the comparison set (0.57B params, 0.55s for 25 frames at 512×512).

## Weaknesses

### Fatal
None.

### Major

1. **Numerical error in acceleration claim (Section 4.2, line 189).** The paper states: "Against one-step diffusion-based Real-VSR models SeedVR2 and DLoRAL, it achieves... accelerations of 110× and 308×, respectively." From Table 1, DLoRAL inference time is 6.36s and AdcVSR is 0.55s. The correct acceleration factor is 6.36/0.55 ≈ **12×**, not 308× — an overstatement by a factor of ~26. The SeedVR2 claim (60.61/0.55 ≈ 110×) and all other acceleration claims in the same paragraph check out correctly, so this appears to be an isolated arithmetic error rather than a systemic issue. Nevertheless, a numerical error this large in a headline quantitative claim erodes confidence and must be corrected before the numbers can be taken at face value.

2. **Insufficiently controlled network design ablation (Table 2, Section 4.3).** Table 2 compares "3D (A Pruned DOVE)," "2D (AdcSR)," and "2D+1D (Ours)." The 2D baseline is described as "a 2D SD backbone (AdcSR)" but AdcSR is a pretrained Real-ISR model — it was trained on images with a different teacher (PiSA-SR), not fine-tuned with DOVE distillation or the dual-head adversarial scheme on video data. The ablation therefore conflates **architecture difference** (2D vs. 2D+1D) with **training procedure difference** (Real-ISR training vs. Real-VSR distillation from DOVE). We cannot cleanly attribute the gap between "2D" and "2D+1D" to the 1D convolutions alone. A controlled ablation would fine-tune the 2D backbone (no 1D convs) using the identical DOVE distillation + dual-head adversarial training on the same video data. The conclusions are directionally plausible, but the evidence is weaker than claimed.

### Minor

1. **No variance or uncertainty quantification.** All results in Tables 1–4 are reported as point estimates without standard deviations, confidence intervals, or any indication of run-to-run variability. Given that comparisons are sometimes close (e.g., AdcVSR CLIPIQA 0.6818 vs. AdcSR 0.6693 on UDM10), it is impossible to assess whether reported differences are meaningful or within the noise of training seeds or test sampling. Reporting single-run results is common in this field, but the paper would be strengthened by acknowledging this limitation.

2. **Detail-head training asymmetry not discussed.** In the labeling scheme (Section 3.3, Eq. 5), real video details are "unlabeled" (y_d=0), meaning the detail head receives positive signal only from static images (which are temporally trivial) and random crops (which are inherently temporally inconsistent). The detail head never learns what "good detail" looks like in a video with natural motion. The paper states this design choice (line 124) but does not discuss whether it could bias the notion of "detail" toward static-image characteristics. This is a plausible limitation worth acknowledging.

### Trivial
- The model name is inconsistently rendered as "AdeVSR" (lines 179, 181, 185, 189, 191, 193, 195) vs. "AdcVSR" everywhere else.

## Nice-to-Haves
- A controlled ablation where the 2D backbone (AdcSR architecture without 1D convs) is fine-tuned with the same DOVE distillation + dual-head training pipeline would cleanly isolate the contribution of the 1D convolutions.
- The paper could briefly discuss failure cases: conditions where AdcVSR may underperform (e.g., severe motion, extreme degradations, very long videos where kernel-size-3 1D convolutions may not capture long-range dependencies).
- A brief justification of why DOVE (a one-step model) was chosen as teacher over multi-step diffusion models (e.g., 64-step SeedVR) would be informative, beyond the empirical result in Table 4.

## Removed Points
- **Criticism about DOVE "over-smoothed" claim conflicting with PSNR/LPIPS**: The reviewer argued that DOVE's best PSNR and LPIPS are "not indicative of over-smoothing." This is factually incorrect — over-smoothed outputs frequently score well on PSNR and LPIPS (which favor smooth, artifact-free reconstructions). Removed as factually wrong.
- **Criticism about missing citations for the claim that "existing learning approaches... are ineffective under aggressive pruning"**: The paper does provide citations (Sun et al., 2024, 2025; Xu et al., 2025; Liu et al., 2025; Chen et al., 2025a) immediately after the claim. The criticism was inaccurate. Removed.
- **Criticism about evaluation leaning on Real-ISR baselines outside their designed use case**: The paper explicitly acknowledges these are image methods applied frame-by-frame (line 173-174) and uses their poor temporal consistency precisely to motivate the need for temporal modeling. This is a valid comparison, not a flaw. The "rhetorical tension" observation is interesting but does not constitute a weakness. Removed.
- **Miscellaneous minor criticisms about missing appendix content, formatting, and scope-creep requests**: Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
1. Correct the DLoRAL acceleration factor from 308× to the correct value (~12×) in Section 4.2.
2. Add a controlled ablation that fine-tunes the 2D backbone (AdcSR architecture, no 1D convs) with the identical DOVE distillation + dual-head adversarial training pipeline, and report whether the gap with AdcVSR remains.
3. Resolve the "AdeVSR" / "AdcVSR" naming inconsistency.
4. Add a brief limitations paragraph to the conclusion.
5. Consider reporting at least one representative result with variance across 2–3 seeds to help readers gauge metric stability.

## Score and Decision

**MY FINAL SCORE: <score>6.5</score>**
**MY FINAL DECISION: <decision>Accept</decision>**