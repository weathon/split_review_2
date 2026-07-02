## Summary

This paper proposes **VQ-Transplant**, a two-stage framework that replaces the native VQ module in a pre-trained visual tokenizer (e.g., VAR) with an arbitrary new VQ module while keeping the encoder and decoder frozen, then performs a lightweight decoder adaptation (5 epochs on ImageNet-1k) to realign the decoder’s priors. The paper also introduces **MMD-VQ**, a quantization method that uses Maximum Mean Discrepancy to align feature and codebook distributions. Empirically, VQ-Transplant + MMD-VAR achieves 0.81 r-FID on ImageNet-1k (vs. original VAR’s 0.92) with a 21.8× GPU-hour speedup, and generalizes well to FFHQ, CelebA-HQ, and LSUN-Churches.

## Strengths

- **Well-motivated problem and practical contribution.** Training VQ tokenizers from scratch is computationally prohibitive for many groups. The idea of decoupling VQ module development from full encoder-decoder retraining is clearly useful and timely.
- **Clean, simple framework.** The two-stage design (VQ substitution + decoder adaptation) is intuitive and easy to adopt. The paper validates it with five different VQ methods in both fixed-scale and multi-scale settings, demonstrating general applicability.
- **Thorough empirical evaluation.** Experiments cover multiple VQ algorithms, codebook sizes, and three unseen datasets (FFHQ, CelebA-HQ, LSUN-Churches). Ablation on adaptation epochs (Table 4, Figure 3) and comparison with from-scratch training (Table 6) strengthen the conclusions.
- **Strong gains in efficiency and quality.** VQ-Transplant + MMD-VAR exceeds the original VAR tokenizer’s r-FID (0.81 vs. 0.92) while requiring only 44 A100-GPU-hours on ImageNet-1k, compared to 960 GPU-hours for VAR training.

## Weaknesses

### Major

1. **MMD-VQ is an incremental contribution over Wasserstein VQ.** The paper claims MMD-VQ is superior because it avoids Gaussian assumptions, yet the empirical gap between MMD-VQ and Wasserstein VQ is very small (e.g., 0.81 vs. 0.83 r-FID in Table 3, 0.86 vs. 0.92 in Table 7). The advantage is marginal and not clearly statistically significant. The novelty of MMD-VQ as a “secondary contribution” is limited.

2. **Efficiency claims are not fully contextualized.** The decoder adaptation stage still uses adversarial training (DINO-S discriminator, DiffAug, consistency regularization, etc.). While 5 epochs is lightweight compared to full 60-hour VAR training, the paper does not separately report the cost of the VQ substitution stage versus the adaptation stage. Moreover, the speedup in Table 1 mixes different GPU counts and datasets (e.g., VAR uses 16 A100 on OpenImages, VQ-Transplant uses 2 A100 on ImageNet-1k), making direct comparison less transparent than a pure GPU-hour comparison.

### Minor

3. **Discriminator description is confusing.** The paper states “identical frozen DINO-S discriminator” but then discusses “improving discriminator training” with DiffAug and consistency regularization. It is unclear whether the discriminator is trained from scratch or fine-tuned, and whether the DINO-S backbone is frozen or learnable. This should be clarified.

4. **No discussion of limitations.** The paper does not acknowledge potential failure cases (e.g., when the pre-trained encoder-decoder is weak, when the new VQ module produces a radically different latent space, or when adversarial adaptation is unstable). Addressing these would strengthen the work.

### Trivial

5. Some figure captions are overly verbose with repeated captions from the main text (e.g., Figures 1, 2, 4-6), but these are likely parser artifacts.

## Nice-to-Haves

- An ablation study isolating the contribution of each loss term in the decoder adaptation (e.g., L₂ only, perceptual only, GAN only) would help understand what drives the improvement.
- A comparison with other parameter-efficient fine-tuning approaches (e.g., LoRA on the decoder) could further highlight the efficiency of VQ-Transplant.
- Reporting confidence intervals or standard deviations on r-FID would improve statistical reliability.

## Novel Insights

None beyond the paper’s own contributions—the key insight that a pre-trained tokenizer’s encoder-decoder can be reused with a different VQ module after lightweight adaptation is practically valuable but not theoretically surprising.

## Suggestions

- Clarify the discriminator training setup in Section 4.1 (Stage II).
- Add a limitations paragraph to the conclusion discussing cases where VQ-Transplant may underperform.
- Provide a breakdown of training time for the VQ substitution stage versus the decoder adaptation stage.

## Score and Decision

**Score:** 7.0  
**Decision:** Accept

VQ-Transplant is a well-executed framework with clear practical value. It addresses a real bottleneck in VQ research, is supported by extensive experiments, and achieves strong reconstruction quality with substantial computational savings. The secondary contribution (MMD-VQ) is incremental, but the primary contribution is solid and the evaluation is thorough. Minor clarity issues and a lack of limitation discussion do not detract from the overall contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>