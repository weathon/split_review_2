## Summary

INFOToK proposes an adaptive discrete video tokenizer grounded in information theory. It replaces fixed-rate compression with dynamic token allocation: an ELBO-based router estimates per-video complexity and determines token length, and a transformer-based compressor condenses embeddings accordingly. The method is modular (built on Cosmos-DV) and empirically shows 1.2–2.3× compression gains over fixed-length and existing adaptive (ElasticTok) tokenizers at similar reconstruction quality, with inference overhead only one extra decoder pass.

## Strengths

- **Principled theoretical foundation.** The paper uses Shannon’s source coding theorem to prove that fixed-length and data-agnostic adaptive tokenizers are suboptimal (Theorem 2.2), and shows that an ELBO-based router can achieve near-optimal token allocation (Theorem 3.1). This formalizes an intuition that was previously only heuristic.
- **Novel, efficient router design.** The ELBO-based router avoids the expensive binary search of prior adaptive methods (e.g., ElasticTok’s 11 NFEs) by requiring only a single extra decoder pass, while still yielding close-to-optimal allocation (Table 2).
- **Strong empirical results.** At matched compression levels (0.81 and 0.56 BPP₁₆), INFOToK substantially outperforms ElasticTok on all four metrics (PSNR, SSIM, LPIPS, FVD) on both TokenBench and DAVIS, with FVD reductions of 40–60%. When compared to the fixed-compression Cosmos-DV, INFOToK saves roughly 20% of tokens without quality loss.
- **Clean modularity.** The framework is designed to be retrofitted on top of existing fixed-length tokenizers (e.g., Cosmos-DV), making it readily compatible with future advances in base tokenizers.
- **Thorough ablation study.** The paper ablates the router (ELBO vs. optimal search), the compressor (right-to-left, jump, and ELBO-based masking), and the adaptive mechanism across two architectures (Cosmos and ViT), consistently showing the advantage of the proposed design.

## Weaknesses

### Fatal
None.

### Major
- **Limited adaptive baseline comparison.** The only adaptive video tokenizer compared is ElasticTok. Several other adaptive representation methods (ALIT, One-D-Piece, FlexTok) are discussed in related work but are not adapted or evaluated in the video setting. Without a broader comparison, the “state-of-the-art” claim is not fully supported. The paper should at least discuss how these methods would compare or provide a small-scale adaptation.
- **Overstated token savings claim.** The abstract and introduction claim “saving 50% tokens without loss of quality.” From Table 1, INFOToK at 0.81 BPP₁₆ achieves similar quality to Cosmos-DV (1.00 BPP₁₆), which is a 19% token reduction (1 – 0.81/1.00 = 19%). A 50% saving would require 0.50 BPP₁₆ at equal quality, which is not demonstrated. The 50% figure appears to be a cherry-picked example from a later paragraph, but the paper should state clear, consistent numbers.

### Minor
- **Theoretical–practical gap.** Theorem 3.1 guarantees near-optimality only if the tokenizer minimizes the reconstruction loss globally and if the ELBO approximates the log-likelihood well. The paper does not verify how tight the ELBO approximation is for the Cosmos tokenizer or how far the actual trained model is from the global optimum.
- **Inference overhead justification.** The extra decoder pass for ELBO computation is modest (1 NFE vs. ElasticTok’s 11), but the paper does not report wall-clock timing. Stating that “one additional decoder pass” is the cost is clear, but a brief latency table would strengthen the efficiency claim.
- **Evaluation scope.** Reconstruction metrics are a proper proxy, but the paper does not test on downstream tasks (generation, understanding). The authors acknowledge this as a limitation, which is acceptable, but it limits immediate impact.

### Trivial
None.

## Nice-to-Haves

- Adapting and evaluating ALIT, One-D-Piece, or FlexTok on video would greatly strengthen the SOTA claim.
- Reporting wall-clock inference time (e.g., ms/video) for INFOToK vs. ElasticTok.
- Analyzing how the ELBO approximation error affects token allocation in practice (e.g., correlation between ELBO and the optimal length from exhaustive search).

## Novel Insights

The key insight is linking adaptive token length to the negative log-likelihood of the video, which information theory dictates is the ideal. The paper then operationalizes this via the ELBO, a quantity already available from VAE-style tokenizer training, and shows that a deterministic router based on normalized ELBO suffices to achieve near-optimal expected token length. This elegantly bypasses the need for any search or reinforcement learning, making the approach both principled and practical. The proof that a uniformly trained router (as in ElasticTok) produces arbitrarily suboptimal expected length is also a valuable clarification for the field.

## Suggestions

- Provide a more precise description of the claimed token savings. Replace “saving 50% tokens” with the exact numbers from Table 1 (e.g., “19% token reduction at equal PSNR/SSIM”) and clearly state the compression ratios where larger savings are observed (e.g., 2.3× over ElasticTok in Figure 4).
- Extend the adaptive baseline comparison by at least applying ALIT to video and reporting results on the same benchmarks, or justify why such a comparison is not feasible in a reproducible manner.
- Report wall-clock inference time in milliseconds for the full pipeline (encoder→router→compressor→quantizer→decompressor→decoder) to complement the NFE ratio.

## Score and Decision

Score: 6

Decision: Borderline Accept

**MY FINAL SCORE:** <score>6</score>  
**MY FINAL DECISION:** <decision>Accept</decision>