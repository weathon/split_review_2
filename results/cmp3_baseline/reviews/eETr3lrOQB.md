## Summary

This paper proposes VQ-Transplant, a framework that enables plug-and-play replacement of Vector Quantization (VQ) modules within pre-trained visual tokenizers (e.g., VAR) without costly end-to-end retraining. The method freezes the encoder and decoder, substitutes the native VQ module with a new one, and then performs a lightweight decoder adaptation (5 epochs on ImageNet-1k) to resolve distributional mismatch. The authors also introduce MMD-VQ, a quantization method using Maximum Mean Discrepancy for distributional alignment, and demonstrate that VQ-Transplant achieves near state-of-the-art reconstruction fidelity while reducing training cost by 95%.

## Strengths

- **Significant practical contribution**: The core idea of decoupling VQ module development from full tokenizer training is well-motivated and addresses a real bottleneck in the field. The 21.8x speedup over training VAR from scratch, while matching or exceeding its reconstruction performance, is a compelling result that could meaningfully democratize VQ research for resource-constrained groups.
- **Thorough empirical evaluation**: The paper evaluates five different VQ algorithms (Vanilla, EMA, Online, Wasserstein, MMD) under both multi-scale and fixed-scale configurations, across multiple datasets (ImageNet-1k, FFHQ, CelebA-HQ, LSUN-Churches), and provides extensive metrics (r-FID, PSNR, SSIM, LPIPS, r-IS, quantization error, codebook utilization). The ablation on adaptation epochs (5 vs 10 vs 15 vs 20) and the comparison against from-scratch training are informative.
- **Clear and well-structured presentation**: The problem statement, proposed method (two-stage framework), and experimental design are clearly articulated. Figure 1 effectively communicates the pipeline. The paper is easy to follow.

## Weaknesses

### Fatal
None.

### Major
- **The MMD-VQ contribution is incremental and insufficiently motivated**: MMD-VQ is presented as a secondary contribution, but its novelty over Wasserstein VQ (Fang et al., 2025) is thin. The paper claims MMD-VQ avoids Gaussian assumptions, yet the empirical results show MMD-VQ and Wasserstein VQ perform nearly identically across almost all metrics and settings (e.g., Table 3: MMD VAR 0.91 r-FID vs Wasserstein VAR 0.93 r-FID; Table 7: MMD VQ 1.05 r-FID vs Wasserstein VQ 1.04 r-FID). The paper does not provide any analysis of cases where feature distributions are demonstrably non-Gaussian, nor does it show that MMD-VQ's non-parametric nature yields a practical advantage. The theoretical motivation (Appendix B) is not backed by empirical evidence of a regime where Wasserstein VQ fails and MMD-VQ succeeds.
- **The decoder adaptation stage is essentially fine-tuning the decoder with the original training objective**: The decoder adaptation loss (Equation 4) is the same composite loss (L2 + perceptual + GAN) used in the original VAR training. The only difference is that the encoder and VQ module are frozen. This is a standard fine-tuning procedure, not a novel algorithmic contribution. The paper's framing of this as a key methodological innovation is somewhat overstated. The main novelty remains the observation that one can freeze the encoder and replace the VQ module, which is a practical insight rather than a deep technical advance.
- **Limited analysis of failure modes and limitations**: The paper does not discuss scenarios where VQ-Transplant might fail or underperform. For example, what happens if the new VQ module produces a latent space that is fundamentally incompatible with the frozen encoder's feature distribution (not just the decoder's priors)? The paper only evaluates on the VAR tokenizer; it is unclear how well the framework generalizes to other tokenizer architectures (e.g., VQGAN with different encoder/decoder designs). The LDM-16 experiment (Table 16, Appendix D) is mentioned but not discussed in the main text, and the paper notes "lower adaptability" without analysis.

### Minor
- **The paper claims "state-of-the-art" reconstruction fidelity but the improvements over the original VAR tokenizer are modest**: MMD VAR achieves 0.81 r-FID vs VAR's 0.92 r-FID. While this is an improvement, the paper's framing as "industry-level" and "state-of-the-art" is somewhat hyperbolic given the small absolute gain and the fact that the comparison is against the same architecture with a different VQ module.
- **The cross-dataset results (Tables 8-10) lack baselines trained from scratch on those datasets**: The paper compares against full-training baselines (RQVAE, VQGAN, etc.) that were trained on those specific datasets. However, VQ-Transplant leverages a tokenizer pre-trained on OpenImages/ImageNet. A fairer comparison would include the original VAR tokenizer evaluated zero-shot on these datasets, to isolate the benefit of the VQ transplant from the benefit of the pre-trained encoder-decoder.

### Trivial
- The paper uses "r-FID" and "r-IS" as metrics, but the "r" prefix (reconstruction) is non-standard and could be confused with "FID" and "IS" used for generation quality. The paper should clarify this early on.
- Table 7 has a typo: "$\tau$-FID" and "$\tau$-IS" instead of "r-FID" and "r-IS".

## Nice-to-Haves
- An analysis of the computational cost breakdown (encoder forward pass, VQ module, decoder adaptation) would help practitioners understand where the savings come from.
- A discussion of whether the decoder adaptation could be done with even fewer epochs (e.g., 1-2 epochs) or with a smaller subset of data.
- An experiment showing that VQ-Transplant works with a different base tokenizer (e.g., VQGAN trained on a different dataset) would strengthen the claim of generality.

## Novel Insights

None beyond the paper's own contributions. The core insight—that one can freeze the encoder-decoder of a pre-trained tokenizer and only retrain the VQ module plus a lightweight decoder adaptation—is a practical observation that is well-demonstrated but not surprising in retrospect. The paper does not reveal any deeper theoretical understanding of why this works or when it might fail.

## Suggestions

1. **Strengthen the MMD-VQ contribution**: Either provide a clear empirical setting where MMD-VQ outperforms Wasserstein VQ (e.g., on data with known non-Gaussian feature distributions), or reframe MMD-VQ as a simple variant of Wasserstein VQ rather than a separate contribution. The current presentation overclaims its novelty.
2. **Add a zero-shot baseline for cross-dataset experiments**: Report the performance of the original VAR tokenizer (without any adaptation) on FFHQ, CelebA-HQ, and LSUN-Churches. This would help the reader understand how much of the cross-dataset performance is due to the VQ transplant vs. the pre-trained encoder-decoder.
3. **Discuss limitations more explicitly**: Add a paragraph in the conclusion or a separate limitations section that addresses when VQ-Transplant might not work (e.g., if the new VQ module's latent space is too different from the original, or if the encoder is not sufficiently expressive).
4. **Clarify the novelty of decoder adaptation**: Acknowledge that the decoder adaptation is essentially fine-tuning with the original objective, and frame the contribution as the *discovery* that this lightweight fine-tuning suffices after VQ module replacement, rather than as a novel algorithm.

## Score and Decision

The paper presents a practically useful framework that addresses a real computational bottleneck in VQ research. The empirical evaluation is thorough and the results are convincing. However, the paper's novelty is moderate: the core idea is a simple observation (freeze encoder-decoder, replace VQ module, fine-tune decoder), and the secondary contribution (MMD-VQ) is incremental over existing work. The paper is well-executed and clearly written, but it does not introduce deep new insights or methods. It is a solid empirical contribution that will be useful to the community, but it is not at the level of a top-tier breakthrough.

Score: 6 (borderline accept)

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>