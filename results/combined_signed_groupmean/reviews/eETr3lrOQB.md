Here is the final consolidated review.

---

## Summary

VQ-Transplant proposes a two-stage framework for swapping Vector Quantization (VQ) modules in pretrained visual tokenizers without costly end-to-end retraining: (1) substitute the VQ module while freezing the encoder-decoder, then (2) perform lightweight decoder adaptation (5 epochs). A secondary contribution, MMD-VQ, uses maximum mean discrepancy for distributional alignment in the codebook. Evaluated on ImageNet-1k and three additional datasets across 5 VQ algorithms, the framework achieves reconstruction quality competitive with or surpassing the original VAR tokenizer at a fraction of the training cost (44 vs 960 GPU-hours).

## Strengths

- **Well-motivated practical problem (Section 1).** Training discrete tokenizers from scratch is computationally prohibitive for resource-constrained researchers; decoupling VQ module development from full tokenizer training addresses a real bottleneck.
- **Clean, intuitive two-stage design (Section 4.1).** Stage I freezes the encoder-decoder and trains only the new VQ module; Stage II freezes the encoder+VQ and fine-tunes only the decoder for 5 epochs. The 44 GPU-hour cost (2×A100, 22h) versus VAR's 960 GPU-hours (16×A100, 60h) is a genuine reduction.
- **Comprehensive evaluation across 5 VQ algorithms (Tables 3, 7)** in both multi-scale and fixed-scale configurations with multiple codebook sizes. This provides a solid empirical basis for the finding that distribution-aligned VQ methods benefit most from the transplant framework.
- **Ablation on adaptation epochs (Table 4, Figure 3)** showing consistent r-FID improvement from 1 to 20 epochs, cleanly demonstrating that decoder adaptation is the mechanism driving performance recovery.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **MMD-VQ overclaimed as a contribution (Section 4.2).** The paper presents MMD-VQ as a novel method with claimed advantages over Wasserstein VQ (e.g., non-Gaussian robustness), but the empirical evidence does not support this. Results are mixed: on ImageNet the differences are marginal (K=4096 multi-scale: MMD 0.91 vs Wasserstein 0.93 r-FID); on FFHQ (Table 8, K=32768, Adaptation) Wasserstein wins decisively (1.21 vs MMD 1.37); on Churches (Table 10) Wasserstein also wins (1.79 vs MMD 1.87). The claim about nonparametric distribution alignment is not tested with known non-Gaussian data. This is a weakness primarily of the *secondary* contribution; the primary contribution (VQ-Transplant framework) is unaffected.

- **No downstream generation experiments.** The paper motivates discrete tokenizers for "visual generation" (Section 1) and builds on the VAR architecture designed for autoregressive image generation, yet evaluation is limited entirely to reconstruction metrics (r-FID, PSNR, SSIM, LPIPS). Without generation experiments (e.g., FID of autoregressively sampled images), the claim that VQ-Transplant "democratizes quantization research" for generative modeling is partially unsupported.

- **Introductory comparison uses mismatched codebook sizes (Section 1, page 1).** The headline comparison of "0.81 rFID" (MMD VAR, K=8192) vs "0.92 rFID" (Vanilla VAR, K=4096) uses different codebook sizes without acknowledging this. At equal K=4096, MMD VAR achieves 0.91 vs VAR's 0.92 — near-parity, not the superiority implied by the headline 0.81 figure.

- **"Record r-FID" claim overstated (Section 5.3).** The claim that Wasserstein VQ achieves a "record r-FID of 1.21" on FFHQ compares against baselines trained entirely from scratch (RQVAE, VQGAN, etc.), while Wasserstein VQ benefits from the pretrained VAR encoder-decoder backbone. This is not an apples-to-apples comparison.

### Trivial
None.

## Nice-to-Haves

- Provide variance or multiple-seed reporting for reconstruction metrics, given that adversarial training (used in Stage II) can be unstable.
- Ablate the benefit of Stage I (VQ-only training) alone for each VQ method, to isolate whether the MMD loss specifically makes decoder adaptation easier.

## Removed Points

These points from the input review were removed after verification:

- **Efficiency framing / 21.8× speedup claim** — REMOVED. The comparison between VQ-Transplant (44 GPU-hours) and full VAR training (960 GPU-hours) is technically correct and relevant: if you want a better VQ module, you can either train a full tokenizer from scratch or use VQ-Transplant with an existing pretrained model. The Table 6 comparison against 5-7 epoch from-scratch training actually understates VQ-Transplant's advantage (since the paper itself states hundreds of epochs are needed for convergence).
- **95% reduction claim not derived** — REMOVED. (960−44)/960 = 95.4%, directly derivable from Table 1 numbers.
- **Equation (3) missing commitment loss** — REMOVED. Reviewer acknowledges the encoder is frozen, so the commitment loss is unnecessary. Not a substantive issue.
- **τ-FID vs r-FID typo** — REMOVED. Minor formatting/notation inconsistency with no impact on results.
- **Wasserstein VQ Gaussian assumption claim unsupported** — REMOVED. This is a standard known theoretical property of Wasserstein-2 distance, not an empirical claim requiring new evidence in this paper.
- **LDM tokenizer discussion deferred to Appendix D** — REMOVED. The appendix was stripped by the parser; it exists in the original submission per the rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a downstream generation experiment** — train a VAR transformer on tokens from the transplanted VQ module and report generation FID. This would directly validate the paper's framing of supporting generative modeling.
2. **Acknowledge the codebook size difference** when comparing r-FID across configurations in the introduction.
3. **Reframe the "record r-FID" claim** on FFHQ to clarify that the comparison is against baselines trained from scratch while the proposed method leverages a pretrained backbone.
4. **Temper the claims about MMD-VQ's superiority** over Wasserstein VQ, or provide experiments directly testing the non-Gaussian robustness claim (e.g., on data with known multimodal distributions).

---

### Calibration Notes

**Round 1 (bracketing, 5.5–7.5):** The paper sits above flawed visual tokenization papers (score ~2.5) and below exceptionally strong VQ methodology papers (score ~8.0).

**Closest anchors (itemized):**
- **BSQ-ViT** (score 5.75, Accept): Visual tokenization paper with a novel quantization method. VQ-Transplant has a cleaner primary contribution (framework, not just another VQ method) and fewer high-impact weaknesses, placing it slightly above.
- **LaVIT / Dynamic Discrete Visual Tokenization** (score 6.25, Accept): Strong vision-language pretraining with visual tokenization. VQ-Transplant is more focused and better controlled in evaluation but lacks the breadth of downstream tasks.
- **BPE Image Tokenizer** (score 6.00, Accept): Applies BPE to image tokenization. VQ-Transplant has substantially stronger evaluation and less controversial claims, placing them comparably.

**Impact-score comparison:** VQ-Transplant's strongest items — comprehensive evaluation (+9.27) and epoch ablation (+9.88) — match or exceed the top items of its closest anchors. Its strongest weakness (MMD-VQ overclaim, -9.97) is high-magnitude but targets only the secondary contribution; the primary framework contribution is not undermined. This pattern (one salient weakness about an ancillary claim, strong primary evidence) is characteristic of papers scoring ~6.0 in the calibration set.

**Final score placement:** The paper's core contribution (VQ-Transplant) is solid and well-supported. The weaknesses concern framing and a secondary contribution, not the main method. This places the paper at the borderline-accept level.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>