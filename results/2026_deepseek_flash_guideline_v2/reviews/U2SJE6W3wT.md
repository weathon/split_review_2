Now let me produce the final consolidated review.

## Summary

This paper proposes AdcVSR, a compressed one-step diffusion model for real-world video super-resolution (Real-VSR). It combines two key ideas: (1) a "2D + 1D" architecture using a pruned 2D SD backbone augmented with lightweight 1D temporal convolutions, enabling massive compression while maintaining temporal modeling; and (2) a dual-head, dual-discriminator adversarial distillation scheme that disentangles detail and consistency objectives. Distilled from the DOVE teacher, AdcVSR achieves **95% parameter reduction** (10.55B → 0.57B) and **8× speedup** (4.42s → 0.55s for 25-frame 512² video), while maintaining competitive quality and achieving state-of-the-art temporal consistency (e.g., E_warp* 1.67 vs. DOVE's 2.22 on UDM10).

## Strengths

1. **Massive compression with improved temporal consistency over the teacher.** Table 1 and Figure 4 show AdcVSR not only reduces parameters by 95% and achieves 8× speedup over DOVE (10.55B, 4.42s), but also achieves strictly better flow warping error (E_warp* 1.67 vs. 2.22 on UDM10, 6.74 vs. 8.41 on VideoLQ). This directly validates the claim that 3D attentions contain redundancy for Real-VSR and that the "2D + 1D" design suffices.

2. **Dual-head discriminator ablation cleanly isolates the benefit of disentangling detail from consistency.** Table 3 compares three configurations on YouHQ40: single-head dual-domain achieves CLIP-IQA 0.6745 but poor E_warp* 6.32; dual-head single-domain improves E_warp* to 3.59 but drops CLIP-IQA; the proposed dual-head dual-domain achieves the best of both (0.6861 CLIP-IQA, 2.22 E_warp*), directly validating contribution (3).

3. **Careful training-data curation for disentangled supervision.** Section 3.3 defines five curated data types with head-specific labels (`y_d, y_c ∈ {-1, 0, 1}`) that independently vary detail and consistency. Real images supply positive detail supervision; real videos supply positive consistency supervision; shuffled videos and cropped images supply negative signals. This deliberate construction goes well beyond standard GAN discriminators and prior ADC work.

4. **Comprehensive evaluation spanning six datasets and eight metrics.** Table 1 reports results on synthetic (UDM10, SPMCS, YouHQ40) and real-world (RealVSR, MVSR4x, VideoLQ) benchmarks, covering fidelity (PSNR, SSIM), perceptual quality (LPIPS, DISTS), no-reference quality (MANIQA, CLIPIQA, MUSIQ), and temporal consistency (E_warp*, DOVER), with 11 comparison methods.

## Weaknesses

### Fatal

None.

### Major

- **Ablation studies are thin on metric coverage, making it harder to fully validate individual contributions.** Each ablation table reports only 2–3 metrics on a single dataset, and the metric sets vary across tables. Table 2 (network design, UDM10) reports only DISTS and E_warp* — no PSNR, SSIM, LPIPS, or any no-reference metric. This makes it difficult to verify whether the "2D + 1D" design genuinely recovers per-frame perceptual quality or merely improves temporal consistency. Table 3 (discriminator design, YouHQ40) reports only CLIP-IQA and E_warp*. A consistent metric suite across ablations (e.g., adding LPIPS, PSNR, or a no-reference metric to every table) would substantially strengthen confidence that the reported improvements are robust.

### Minor

- **No error bars or variance statistics.** Given the well-known instability of adversarial training (the paper uses two discriminators, multiple loss terms, and a two-stage training protocol), reporting single-run results without standard deviations or confidence intervals weakens the quantitative evidence.
- **No discussion of limitations or failure cases.** The paper ends without examining conditions where the method might underperform (e.g., complex motion, severe occlusions, out-of-distribution degradations, very long videos beyond 25 frames).
- **The detail head's positive supervision comes exclusively from images, never from real videos.** As the paper acknowledges (Section 3.3), real video frames are labeled "unlabeled" (y_d=0) for the detail head, and only image-derived data provides positive detail supervision. This means AdcVSR's notion of "good details" is image-quality-based, which may not fully capture what makes video frames look natural in motion. The paper does not discuss this potential limitation or its implications.
- **Limited analysis of the 1D temporal convolution design choices.** The paper specifies kernel size 3 and the insertion strategy, but there is no ablation studying how performance varies with kernel size, number of 1D layers stacked per block, or whether stacking more layers provides diminishing returns.

### Trivial

None.

## Nice-to-Haves

- Adding LPIPS, PSNR, and at least one no-reference metric to Tables 2 and 3 would make the ablation evidence substantially stronger.
- An ablation varying the channel-pruning ratios (currently fixed at 25% UNet, 50% VAE decoder, inherited from AdcSR) could test whether the 1D convs compensate for more aggressive compression.
- A single pooled ablation table with a shared metric set across all design choices would allow direct comparison of marginal contributions.

## Removed Points

The following points from the reviews were removed as per the filtering rules; they are noted here for transparency:

1. **"Efficiency comparisons against multi-step methods are presented to inflate the perceived advantage"** — REMOVED. The numbers (121×, 59×, 175×) are factually correct (verified against Table 1) and the paper also separately and explicitly reports the 8× speedup over DOVE. Presenting both comparisons is standard and informative, not misleading. This is a framing preference, not a weakness.

2. **"AdeVSR typo in Figure 3 caption and Section 4.2"** — REMOVED per hard rule on typos/formatting artifacts.

3. **"Missing appendix content"** — REMOVED per hard rule; the parser strips appendix sections from all papers; the original submission contains them.

4. **"Pruning ratios not motivated"** — REMOVED. The paper states the ratios are inherited from AdcSR (Chen et al., 2025a); additional ablation would be a nice-to-have but is not a required justification.

5. **"The '2D+1D' design details are incomplete"** — REMOVED. The paper specifies kernel size 3, same channel number as the preceding UNet block (Section 4.1), and insertion of residual blocks after each UNet block. This is sufficient for the claimed level of architectural description.

6. **"No temporal kernel size ablation"** — MOVED to Minor/Major weakness (merged with point 4 in Minor above) rather than a separate criticism.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Expand the ablation studies** with a consistent metric suite (at minimum add LPIPS and PSNR to Tables 2 and 3) and ideally report results on a second dataset to assess robustness.
2. **Add a brief limitations paragraph** discussing potential failure modes: complex motion, severe occlusions, long-range temporal coherence beyond 25 frames, and out-of-distribution degradations.
3. **Report variance statistics** (standard deviations or confidence intervals across multiple runs or seeds) for at least the main results in Table 1, given the use of adversarial training.
4. **Discuss the image-only detail supervision** more explicitly — acknowledge the potential bias and explain why this design is still sufficient for video-level detail quality.

## Score and Decision

Based on the calibration search (which was unfortunately unavailable due to a tool error — the calibration corpus had missing files), I evaluated the paper against my knowledge of ICLR standards. The paper makes a clear, well-motivated contribution: a principled architecture + distillation scheme that compresses a 10.55B-parameter video diffusion model to 0.57B with 8× speedup and superior temporal coherence. The strengths are concrete and evidenced (Tables 1, 3; Figures 3, 4). The main weakness — thin ablation metric coverage — is real but does not threaten the core claims; it would reduce confidence in a border case but the main result table (Table 1) is comprehensive with 8 metrics across 6 datasets. The missing limitations and error bars are common omissions that do not invalidate the contribution. I calibrate this to a **borderline accept**, slightly above the midpoint of the scale because the efficiency–quality trade-off is genuinely impressive and the dual-head discriminator design is well-validated.

**Score: 6.5**  
**Decision: Accept**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>