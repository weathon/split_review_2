Now I have all the information I need. Let me produce the final consolidated review.

## Summary

ARSS proposes the first decoder-only autoregressive framework for novel view synthesis (NVS) from a single image with camera control. The pipeline combines a video tokenizer (VidTok with FSQ), a camera autoencoder that compresses Plücker raymaps into latent tokens providing 3D positional guidance, and a causal transformer trained with a spatial-shuffle / temporal-preserve token ordering. Evaluated on RealEstate10K, ACID, and DL3DV against 5 baselines (SEVA, LVSM, MotionCtrl, ViewCrafter, RayZer) plus qualitative comparison with Genwarp.

## Strengths

- **First decoder-only AR formulation for NVS with camera control.** Prior AR visual generation methods (LlamaGen, VAR, Random-Shuffle) focus on single-image generation, while diffusion-based NVS methods generate all views jointly. ARSS is the first to formulate multi-view synthesis as next-token prediction conditioned on camera trajectories (lines 86–87, 281). This is a genuinely novel framing.

- **Hybrid token-order permutation validated via controlled ablation.** The paper proposes permuting only spatial token order while keeping temporal order fixed (Section 3.2.3). Table 2 provides a clean comparison: "ours" achieves PSNR 19.22 vs. raster 16.29 and full-perm 18.76, and LPIPS 0.294 vs. raster 0.402 and full-perm 0.315 — evidence that the specific permutation strategy is effective.

- **Camera autoencoder with explicit geometric losses.** The camera encoder is trained with four geometric constraints (Eq. 5): L2 reconstruction on ray direction and momentum, unit-norm regularization, and orthogonality regularization. This provides principled 3D positional information at each token position, going beyond the class-label or text conditioning used in prior AR image generation.

- **Error accumulation analysis demonstrates robustness along long trajectories.** Figure 6 reports per-frame PSNR/SSIM/LPIPS from frame 0 to 16. ARSS maintains the highest or near-highest values with flatter degradation slopes than all baselines, providing direct evidence that the autoregressive design does not suffer from uncontrolled drift over multi-frame sequences.

- **Video tokenizer ablation shows temporal-consistency gains.** Table 3 compares VidTok with FSQ against per-frame VQ: FVD improves from 137.68 to 52.56 (~62% relative improvement), validating the claim that per-frame VQ tokenization fails to preserve temporal consistency for NVS.

- **Zero-shot generalization to out-of-distribution inputs.** ARSS achieves the best PSNR (16.70) and LPIPS (0.347) on DL3DV among all methods (Table 1), and shows qualitative results on AI-generated cartoonish/oil-paint images (Figure 5), supporting the generalizability claim.

## Weaknesses

### Major
None.

### Minor

- **Inconsistent percentage claims in §4.2 that do not match Table 1.** The text states "+22% FID" when comparing against SEVA, but this value does not match any comparison in Table 1 (RealEstate10K: +1.3%; ACID: +44%). The other cited percentages (+1.1% PSNR, -21% LPIPS, -6.6% SSIM) are also rough approximations that differ from exact calculations computed from the table. While these do not affect the table data themselves, they erode confidence in the precision of the paper's claims and should be corrected.

- **Genwarp included in qualitative but not quantitative comparisons without explanation.** Genwarp (Seo et al., 2024) is listed among baselines in §4.1, appears in qualitative comparisons (Figures 3, 4), and is discussed in the quantitative results text as "underperform[ing] across metrics" (line 231). Yet Genwarp has no column in Table 1 and no footnote explaining its absence. The reader cannot assess whether Genwarp would have been competitive on the reported metrics. The paper should either include Genwarp numbers or state why they are unavailable.

- **Ablation numbers do not reconcile with main results, and the evaluation setup is unspecified.** The ablation tables (Tables 2 and 3) report "ours" at PSNR=19.22, SSIM=0.565, LPIPS=0.294, FID=60.11, while the main table (Table 1, RealEstate10K column) reports the full method at PSNR=19.02, SSIM=0.624, LPIPS=0.269, FID=47.60. These are substantially different (FID differs by ~23%). The paper does not specify what dataset, split, or configuration the ablation uses, making the quantitative ablations uninterpretable as controlled evidence for the design choices.

- **Equation (7) is missing the target argument in the cross-entropy loss.** The loss is written as `CE(f_θ([S, [x_{21}^{P_2(1)}, …, x_{ln}^{P_l(n)}]]))` with only one argument. Compare with Eq. (3), which correctly shows both the predictions and the target token sequence. This is a substantive error in the mathematical specification of the training objective.

- **Abstract vs. introduction inconsistency in the strength of claims.** The abstract (line 9) states ARSS achieves results "overall comparable to state-of-the-art," while the introduction (line 88) claims it "out-performs current state-of-the-art methods." Table 1 supports the more cautious "comparable" framing (ARSS leads on some metrics/datasets but trails on SSIM and FID vs. SEVA on RealEstate10K). The paper should adopt a consistent characterization.

### Trivial

- **Figure 6 caption refers to "L2SM"** (line 235), which is not a method described in the paper — likely a typo for "LVSM."

## Nice-to-Haves

- Report variance estimates (standard deviations or confidence intervals) for the quantitative results, particularly for metrics where gaps between methods are small (e.g., ARSS vs. SEVA on RealEstate10K PSNR: 19.02 vs 18.73).
- Provide runtime or inference speed comparison. The paper mentions "parallel decoding" as an advantage (line 177) but provides no speed measurements.
- Clarify whether the camera autoencoder is trained jointly with the autoregressive transformer or frozen during main training, and specify the loss weighting values (λ₁–λ₄) in Eq. (5).
- Discuss systematic failure cases beyond the tokenizer-quality limitation acknowledged in Section 5.

## Removed Points

These points were raised by the reviewers but are removed from the main evaluation for the reasons stated:

- **"purpose to reorder" typo** — Removed per formatting/typo rule (parser artifact).
- **Criticism about missing appendix content** — Removed per instruction: the parser strips those sections; they exist in the original submission.
- **Criticism about missing related works** — Removed per instruction: cannot confirm existence of uncited works.
- **Generic criticism that "without images it's impossible to verify qualitative claims"** — Removed as it applies to any paper with figures.
- **Criticism about camera autoencoder latent dimension and codebook details** — Moved to Nice-to-Haves; these are clarifications, not weaknesses.
- **Generic criticism about absence of variance estimates as a major flaw** — Demoted to Nice-to-Have; single-run evaluation is the norm in this subfield.
- **Strength Finder's generic/delusional/sycophantic claimed strengths** (e.g., "addressed an important problem") — Removed; only concrete, evidence-grounded strengths are retained.

## Novel Insights

The most substantive findings from the review synthesis are: (1) the numerical inconsistency in the FID percentage claim in §4.2, which is verifiably wrong; (2) the unexplained gap between ablation and main-table numbers, which prevents the ablations from serving as clean evidence; and (3) the omission of Genwarp from quantitative comparisons without justification. None of these is fatal — the core novelty and main results remain intact — but they collectively indicate that the paper's experimental presentation needs significant cleanup before the claims can be taken at face value. The paper's genuine strength is its novel causal framing for NVS, and the evidence of superiority on long-horizon error accumulation (Figure 6) is a compelling advantage that the diffusion baselines cannot match by design.

## Suggestions

1. **Correct the "+22% FID" claim in §4.2** to match the actual numbers in Table 1, or clarify which dataset/split the percentages refer to.
2. **Add a footnote in Table 1 explaining why Genwarp is excluded** from quantitative comparison, or include its numbers if available.
3. **State which dataset and configuration the ablation experiments (Tables 2, 3) use** and reconcile the numerical differences with the main results.
4. **Fix Equation (7)** to include the target token sequence as the second argument to the cross-entropy loss.
5. **Harmonize the abstract and introduction claims** to consistently reflect the paper's actual empirical standing (leads on some metrics, trails on others).

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>