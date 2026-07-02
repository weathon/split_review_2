## Summary

This paper introduces InfoTok, a principled adaptive video tokenization framework grounded in Shannon information theory. It proves that existing fixed-rate and data-agnostic adaptive tokenizers are suboptimal, and proposes an ELBO-based router to dynamically determine token length per video, combined with a transformer-based adaptive compressor. Experiments show that InfoTok saves up to 20% tokens without quality loss and achieves 2.3× compression gains over prior adaptive methods like ElasticTok, while requiring only a single additional decoder pass instead of costly search.

## Strengths

- **Strong theoretical foundation**: The paper provides rigorous proofs (Theorems 2.2 and 3.1) showing why fixed-length and uniformly-trained adaptive tokenizers are suboptimal, and why the proposed ELBO-based router can achieve near-optimal compression. This information-theoretic framing is a principled advance over heuristic approaches.
- **Clear and well-motivated framework**: The adaptive tokenization framework (router + compressor) is cleanly separated, built on top of existing fixed-length tokenizers, and the design choices (ELBO-based length selection, likelihood-based token masking) are directly motivated by the theory.
- **Compelling empirical results**: InfoTok consistently outperforms ElasticTok across multiple compression rates and datasets (TokenBench, DAVIS), with FVD reductions of 40–60% and PSNR gains of 1–2 dB at the same BPP. The method also matches or exceeds fixed-length Cosmos-DV while using 20% fewer tokens.
- **Inference efficiency**: Unlike ElasticTok which requires 11× additional forward passes for binary search, InfoTok needs only one extra decoder pass, making it substantially more practical.
- **Thorough ablation studies**: The paper validates the ELBO-based router against an optimal search strategy (Table 2), compares different compressor designs (Table 3 left), and shows the adaptive mechanism generalizes across architectures (Table 3 right).

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- The theoretical guarantee in Theorem 3.1 provides an upper bound on expected token length that depends on the gap between β and the true entropy. While the bound is informative, the claim of “near-optimality” relies on the ELBO being a tight approximation and β being chosen appropriately. The paper does not provide a lower bound or quantify the approximation gap, so the theoretical optimality is somewhat qualified.
- The method requires an additional decoder pass to compute the ELBO for each video. Although this is far cheaper than ElasticTok’s search, it still adds overhead. The paper acknowledges this and suggests future work on lighter-weight routers, but the current overhead is a practical consideration.
- The evaluation is limited to reconstruction metrics (PSNR, SSIM, LPIPS, FVD) and does not include downstream tasks such as video generation or understanding. The authors explicitly state this is beyond scope due to resource constraints, which is understandable, but it leaves open the question of whether the adaptive tokens are equally effective for generative modeling.

### Trivial
- The paper uses “BPP_16” (bits per 16 pixels) as the compression metric, which is non-standard and slightly harder to interpret than standard BPP. The conversion is explained, but it adds a minor cognitive load.

## Nice-to-Haves
- A lightweight router that estimates complexity directly from encoder latents (without a full decoder pass) would further improve efficiency.
- Extending the evaluation to video generation (e.g., training a small autoregressive model on InfoTok tokens) would strengthen the case for downstream utility.
- A discussion of how the binary mask overhead (≈5%) could be reduced or amortized would be useful.

## Novel Insights

The key insight is that optimal token allocation should be proportional to the negative log-likelihood of the data, and that the ELBO from a fixed-length tokenizer provides a tractable surrogate for this quantity. This connects adaptive tokenization directly to Shannon’s source coding theorem, moving beyond heuristic masking strategies. The paper also demonstrates that a simple likelihood-based token selection (masking low-ELBO tokens) is more effective than spatial or random masking, which aligns with the information-theoretic principle.

## Suggestions
- Consider reporting standard BPP (bits per pixel) alongside BPP_16 for easier comparison with future work.
- Provide a more detailed analysis of the approximation gap between ELBO and true log-likelihood in the context of Theorem 3.1, perhaps with empirical measurements on the datasets used.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>