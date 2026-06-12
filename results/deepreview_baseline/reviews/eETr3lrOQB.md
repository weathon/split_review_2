## Summary

The paper proposes VQ-Transplant, a framework that allows plug-and-play replacement of the vector quantization (VQ) module in pre-trained discrete visual tokenizers (e.g., VAR) without costly end-to-end retraining. The approach first substitutes the native VQ module with a new one while freezing the encoder and decoder, then performs lightweight decoder adaptation (5 epochs on ImageNet-1k) to remedy distribution mismatch. The paper also introduces MMD-VQ, a nonparametric quantization method that uses maximum mean discrepancy to align feature and codebook distributions. Experiments show that VQ-Transplant achieves reconstruction fidelity close to or exceeding the original tokenizer (e.g., 0.81 r-FID vs. 0.92 for VAR) while reducing training cost by ~95%.

## Strengths
- **Practical, resource-efficient contribution**: The core idea of decoupling VQ module development from full tokenizer training directly addresses a genuine bottleneck in discrete visual tokenization research. The reported 21.8× speedup and 95% cost reduction are significant for the community.
- **Thorough empirical evaluation**: The paper tests five different VQ algorithms (vanilla, EMA, Online, Wasserstein, MMD) under both multi-scale and fixed-scale configurations, on ImageNet-1k and three cross-domain datasets (FFHQ, CelebA-HQ, LSUN-Churches). Ablation on adaptation epochs and comparison with from-scratch training strengthen the claims.
- **Clear two-stage pipeline**: The VQ module substitution and decoder adaptation stages are well motivated, and the paper convincingly demonstrates the existence of decoder-quantization mismatch (lower quantization error but worse r-FID after substitution) and its resolution via lightweight adaptation.
- **State-of-the-art reconstruction quality**: VQ-Transplant with MMD-VQ achieves the best r-FID among all compared methods on ImageNet-1k (0.74 after 20 epochs adaptation) and sets a new state-of-the-art on FFHQ (r-FID 1.21).
- **Open source and reproducibility**: Code and models are released, which is valuable for the community.

## Weaknesses

### Fatal
None.

### Major
1. **Overclaimed “plug-and-play”**: The framework still requires decoder adaptation (training with adversarial loss for 5 epochs on a large dataset), which is lightweight but not truly plug-and-play in the sense of zero retraining. The term may mislead readers expecting direct substitution without any training.
2. **Unfair comparison in Table 6**: VQ-Transplant (22 hours, adapted on a strong pretrained model) is compared to from-scratch MMD VAR training for only 5-7 epochs (25-35 hours). The paper acknowledges that tokenizers need hundreds of epochs to converge, so the from-scratch baseline is not representative of a fully trained model. A fair comparison would require training from scratch to convergence, even if that is computationally infeasible for the authors. The current comparison inflates the relative advantage of VQ-Transplant.

### Minor
1. **Clarity of cross-dataset evaluation**: Section 5.3 claims to test cross-dataset generalization, but it is ambiguous whether the decoder adaptation (Stage II) is performed on the target domain (FFHQ/CelebA/Churches) or if the model adapted on ImageNet-1k is directly applied zero-shot. The large improvement from Substitution to Adaptation in Tables 8–10 strongly suggests domain-specific fine-tuning, which would make the title “Cross-Dataset Generalization” somewhat misleading. The paper should explicitly state the adaptation protocol for each dataset.
2. **MMD-VQ novelty is incremental**: Applying MMD for distribution alignment between features and codebook is a straightforward extension of Wasserstein VQ (Fang et al., 2025) without the Gaussian assumption. The paper correctly cites the motivation but the technical contribution of MMD-VQ is limited. The framework (VQ-Transplant) is the primary contribution.

### Trivial
- In Table 7 and later tables, the r-FID column is sometimes labeled with a tau symbol (τ-FID) due to parser artifact; this does not affect understanding.

## Nice-to-Haves
- Ablation on the impact of different kernel choices for MMD (e.g., single Gaussian vs. multi-Gaussian) would strengthen the analysis.
- Discussion on how to select a good “new” VQ module for a given pretrained tokenizer (beyond empirical trial) could be useful.

## Novel Insights
None beyond the paper's own contributions. The insight that a pretrained decoder can be quickly adapted to a new quantization space by only fine-tuning the decoder is practically valuable but empirically established rather than theoretically derived.

## Suggestions
- Clarify the cross-dataset adaptation protocol: specify whether decoder adaptation is performed on each target dataset or zero-shot.
- Rephrase “plug-and-play” to something like “lightweight integration” to avoid overclaiming.
- In Table 6, add a note that from-scratch training would require much longer training to reach comparable quality, explaining why the 5-epoch baseline is not competitive.

## Score and Decision
The paper presents a clear and practical framework that addresses a real bottleneck in VQ research. The experiments are extensive and largely support the claims, despite the minor issues noted. The contribution is solid but not groundbreaking; it is likely to have immediate impact for resource-constrained researchers. I recommend acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>