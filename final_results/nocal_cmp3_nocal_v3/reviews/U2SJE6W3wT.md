## Summary

This paper proposes AdcVSR, an improved adversarial diffusion compression (ADC) method for real-world video super-resolution (Real-VSR). The method distills a large 3D DiT-based one-step diffusion model (DOVE) into a compact student network built from a pruned 2D SD backbone augmented with lightweight 1D temporal convolutions, achieving 95% parameter reduction and 8× speedup. The core technical novelty is a dual-head, dual-discriminator adversarial distillation scheme that assigns separate "detail" and "consistency" heads in both pixel and feature domains, with a curriculum-inspired labeling strategy using five curated data types. Experiments across 6 datasets and 10 baselines show competitive video quality with substantially lower computational cost.

## Strengths

- **Dual-head discriminator design is well-motivated and empirically validated.** The idea of splitting the GAN discriminator into separate detail and consistency heads — addressing the known optimization conflict between these objectives — is cleanly motivated. The ablation in Table 3 is convincing: single-head degrades warping error from 2.22 to 6.32, and single-domain degrades CLIP-IQA from 0.6861 to 0.6421, confirming both heads and both domains contribute non-redundantly.

- **Compression results are practically meaningful.** The 95% parameter reduction (10.55B → 0.57B) and 8× speedup over the teacher DOVE, while maintaining competitive quality on most metrics, is a genuine engineering achievement. The student (0.57B) is comparable to or smaller than most one-step Real-ISR models yet handles video with temporal consistency.

- **Thorough evaluation scope.** The paper compares against 10 baselines (spanning non-generative, multi-step diffusion, one-step VSR, and one-step ISR methods) on 6 datasets (3 synthetic, 3 real-world) using 9 metrics including temporal-specific ones (E_warp*, DOVER). This is more comprehensive than typical 3–4 baseline comparisons in compressed diffusion work.

## Weaknesses

### Fatal

None.

### Major

- **Generator adversarial loss for the dual-head discriminators is underspecified.** The paper's headline contribution is that dual-head discriminators provide separate detail and consistency signals to the generator. However, Eqs. 2–3 define the generator loss as a single `Softplus(−𝒟(·))` term per discriminator, treating each discriminator output as a scalar. Yet Eq. 4 defines each discriminator as producing **two** head outputs (`[𝒟(s)]_d` and `[𝒟(s)]_c`). How these two head outputs are combined, summed, or separately used in the generator's adversarial loss is never stated. This is not a minor detail — the whole point of the dual-head design is that the generator receives *separate* gradients for detail and consistency, but the current formulation is ambiguous about whether and how this happens. The authors must clarify whether the generator receives two separate Softplus terms (one per head), a summed/averaged scalar, or some other aggregation.

### Minor

- **No variance or statistical significance reported.** All quantitative results in Tables 1–4 are single numbers without standard deviations or confidence intervals. Several comparisons involve small margins (e.g., SSIM difference of 0.0108 between AdcVSR and DOVE on UDM10; LPIPS difference of 0.0417). While single-run evaluation is common practice for large-scale diffusion model benchmarks, reporting variance across runs or seeds would strengthen confidence that observed rankings are stable, especially for the "top three in most cases" claim.

- **Disentanglement claim would benefit from direct analysis.** The paper asserts that the two heads provide "separate weight gradients" and "disentangled signals" for detail and consistency (Sec. 3.3), but provides no analysis of whether the heads actually specialize. The ablation in Table 3 shows the full method works better than ablations — good evidence for the combined design — but does not demonstrate that the two heads learn distinct feature representations. Simple diagnostics (e.g., correlation between head outputs on spatially vs. temporally corrupted inputs, or head-specific attention visualizations) would substantiate the disentanglement claim beyond architectural plausibility.

- **The detail head's positive supervision comes exclusively from static images, not real videos.** By design (Eq. 5), the detail head receives "real" labels only from repeated single images and random image sequences (data types 4–5), while real video details are left unlabeled. The paper acknowledges this design choice but does not discuss whether image-level detail assessment transfers to video frames that may contain realistic motion blur, compression artifacts, or other video-specific degradations.

- **Ablation in Table 4 confounds multiple variables.** Comparing "No Adversarial Loss" and "No Teacher (HR GT Only)" against teacher-guided variants changes both the supervision target (teacher vs. GT) and the presence of adversarial learning simultaneously, making it difficult to attribute the performance differences to one factor.

### Trivial

None.

## Nice-to-Haves

- **Comparably-sized 3D baseline.** Table 2 compares the 2D+1D student (0.55B) against a pruned 3D DiT with 8.36B parameters. A more aggressively pruned 3D model at ~0.5B parameters would strengthen the architecture claim by controlling for model size, though the current comparison already validates the main efficiency argument.

- **Head-specific analysis.** Adding head output correlation analysis or response to controlled spatial vs. temporal corruptions would strengthen the disentanglement claim beyond what current ablations provide.

## Removed Points

- *"No experiment tests direct application of ADC to Real-VSR"* — REMOVED. Table 1 includes AdcSR (the direct ADC baseline) applied frame-by-frame, and its poor E_warp* (6.19 on UDM10) directly supports the paper's claim.
- *"Where in UNet the 1D convolutions are inserted"* — REMOVED. The paper states "after each UNet block" (Sec. 3.2), which is sufficient architectural detail.
- *"Speedup numbers against multi-step methods are less informative"* — REMOVED. The paper emphasizes the 8× over DOVE (one-step teacher) in the abstract/conclusion and reports multi-step comparisons as additional context; there is no misrepresentation.
- *"Code/model release plan"* — REMOVED per hard rules prohibiting criticism of existence/availability of cited resources. This is a standard reproducibility request but cannot be treated as a weakness about the paper's technical content.
- *"Inference time on H20 GPUs"* — REMOVED. All methods are compared under the same hardware, so the relative comparisons are internally valid.

## Novel Insights

The most interesting observation from the reviewer is that the dual-head discriminator's detail head receives positive supervision exclusively from static images, never from real videos. This creates a potential domain mismatch — the detail head learns to recognize high-quality *image* details rather than *video* details (which may include motion blur, rolling shutter artifacts, etc.). This observation is specific and actionable, and exploring this mismatch could either reveal a limitation or provide insight into why image-derived detail priors transfer to video. None of the other novel insights in the review go beyond the paper's own contributions.

## Suggestions

1. **Clarify the generator's adversarial loss formulation.** Specify whether the generator receives two separate Softplus terms (one per head, summed) or a single combined scalar. If separate terms are used, show the modified equations explicitly.
2. **Add variance information** (at least for the main results in Table 1), or acknowledge the absence as a limitation.
3. **Include a simple diagnostic** showing that the two discriminator heads respond differently to spatial vs. temporal corruptions (e.g., compute head output correlation on a test set with controlled artifacts).
4. **Discuss the detail-static-images vs. video-domain limitation** explicitly in the paper.
5. **Restructure Table 4** to avoid confounding teacher choice with presence/absence of adversarial loss.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>