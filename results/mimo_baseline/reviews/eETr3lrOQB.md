## Summary

The paper proposes VQ-Transplant, a two-stage framework for plug-and-play replacement of vector quantization modules in pre-trained visual tokenizers (e.g., VAR) without end-to-end retraining. The first stage substitutes the native VQ module while freezing the encoder-decoder, and the second stage performs lightweight decoder adaptation (5 epochs on ImageNet-1k) to align the decoder's learned priors with the new quantization space. The authors additionally introduce MMD-VQ, which uses maximum mean discrepancy for codebook-feature distribution matching, and demonstrate that the combined approach achieves near-SOTA reconstruction fidelity (0.81 r-FID on ImageNet-1k) while reducing training cost by ~95%.

## Strengths

- **Practical and well-motivated framework**: The core problem—prohibitive computational cost of training VQ modules with adversarial training—is real and affects many researchers. The two-stage transplant+adaptation pipeline is clean, principled, and directly addresses this bottleneck. Training on 2×A100 for 22 hours versus 16×A100 for 60 hours (VAR) or 32×A100 for 40 hours (ImageFolder) is a compelling efficiency gain.

- **Comprehensive VQ algorithm comparison**: The paper systematically evaluates five VQ algorithms (Vanilla, EMA, Online, Wasserstein, MMD) across both multi-scale and fixed-scale configurations (Tables 3, 7), providing a clear empirical picture of which VQ methods are most compatible with transplantation. The consistent finding that distribution-aligned methods (Wasserstein, MMD) produce lower quantization error and higher codebook utilization is well-supported.

- **Rigorous cross-dataset evaluation**: Testing on CelebA-HQ, FFHQ, and LSUN-Churches (Tables 8-10) demonstrates generalization beyond ImageNet-1k. The FFHQ results (1.21 r-FID with Wasserstein VQ) convincingly outperform prior baselines.

- **Thorough ablation studies**: The paper includes adaptation epoch analysis (Tables 4-5), from-scratch training comparisons (Table 6), and joint optimization experiments (Appendix), providing good evidence for design choices.

## Weaknesses

### Fatal
None.

### Major

- **No downstream generation evaluation**: The paper evaluates only reconstruction quality (r-FID, PSNR, LPIPS, etc.) but never tests whether transplanted VQ modules maintain or improve downstream generative performance. Since the stated goal is to improve visual tokenizers for generative models, and the entire motivation centers on improving generation-relevant discrete representations, this omission is significant. A VQ module could have excellent reconstruction fidelity but produce discrete codes that a downstream autoregressive model handles poorly, and this gap is never examined.

- **Claimed cost reduction is overstated via misleading comparison**: The "21.8× faster" claim in Table 1 compares VQ-Transplant on ImageNet-1k (2×A100, 22 hours) against VAR trained on OpenImages (16×A100, 60 hours). These are different datasets with different scales and different training procedures. The paper does not disentangle whether the cost reduction comes from the transplant framework itself or from training on a smaller dataset. A fairer comparison would train MMD-VAR from scratch on ImageNet-1k with the same hardware and report the actual speedup attributable to transplantation.

- **Limited tokenizer generalizability**: All main experiments use only the VAR tokenizer. The brief mention of LDM-16 in Appendix D (Table 16) reportedly shows lower adaptability, which the paper acknowledges but does not deeply analyze. Given the claim of a general "plug-and-play framework for pre-trained visual tokenizers," demonstrating applicability across at least one more family of tokenizers (e.g., LlamaGen, FLUX tokenizer) in the main text would substantially strengthen the contribution.

### Minor

- **Downweighting the MMD-VQ contribution**: The paper lists MMD-VQ as a secondary contribution, and while it performs well, the improvement over Wasserstein VQ is marginal (0.81 vs 0.83 r-FID for K=8192). The MMD-VQ results for K=4096 show nearly identical r-FID to Wasserstein VAR after adaptation (0.91 vs 0.93). The nonparametric advantage of MMD over Wasserstein's Gaussian assumption is theoretically motivated but not empirically validated against cases where features are explicitly non-Gaussian.

- **No analysis of codebook structure post-transplant**: The paper reports utilization rates but does not analyze whether the transplanted codebooks exhibit qualitatively different structures (e.g., different code diversity, semantic coverage) compared to the original VAR codebook. This would provide deeper insight into what the transplant preserves and what it changes.

### Trivial
None.

## Nice-to-Haves

- A downstream text-to-image generation comparison using the transplanted tokenizer versus the original would dramatically strengthen the paper's core claims.
- Applying VQ-Transplant to at least one additional tokenizer architecture (beyond VAR) in the main experiments.
- A fairness-controlled cost comparison isolating the transplantation efficiency from dataset/hardware differences.

## Novel Insights

The key genuinely novel insight is that VQ module substitution followed by lightweight decoder adaptation is a viable alternative to full tokenizer retraining, and that the compatibility of different VQ algorithms in this transplantation setting correlates with their distribution-alignment properties. The finding that distribution-aligned VQ methods (Wasserstein, MMD) consistently outperform conventional methods (Vanilla, EMA, Online) in the transplant setting—measured by both quantization error and final reconstruction quality—provides a useful practical guideline for the community. However, the insight that decoupling components and fine-tuning selective parts can be efficient is not entirely new in transfer learning.

## Suggestions

- Add a downstream generation evaluation section comparing generation quality (FID on class-conditional generation) using the transplanted tokenizer versus the original VAR tokenizer. This is critical for validating the paper's core premise.
- Include a controlled cost experiment: train MMD-VAR from scratch on the same ImageNet-1k dataset with 2×A100 and measure the actual speedup from transplantation alone, disentangling it from dataset/hardware differences.
- Add at least one experiment transplanting VQ modules into a different tokenizer family to demonstrate the claimed generality.

## Score and Decision

The paper presents a well-executed practical contribution with genuine efficiency gains and thorough experimentation. However, the absence of downstream generation evaluation—arguably the most important validation for a visual tokenizer improvement paper—and the misleading cost comparison weaken the claims considerably. The limited tokenizer generalizability further constrains the contribution's significance. While the idea is sound and the experiments are extensive, the paper does not yet convincingly demonstrate the full value proposition in the most important use case.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject