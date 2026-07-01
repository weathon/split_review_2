##Summary

This paper introduces InfoTok, a principled adaptive video tokenization framework grounded in Shannon’s information theory. It proves that existing fixed-rate and data-agnostic adaptive tokenizers are suboptimal in expected token length, and proposes an ELBO-based router to dynamically determine token counts per video, combined with a transformer-based adaptive compressor. Empirical results on video reconstruction benchmarks show that InfoTok saves up to 20% tokens without quality loss and achieves 2.3× better compression than prior adaptive methods, while requiring only a single extra decoder pass (vs. 11 for ElasticTok).

## Strengths

- **Strong theoretical foundation.** The paper rigorously proves (Theorem 2.2) that uniform-length routers are biased and can lead to arbitrarily suboptimal expected token lengths, and shows (Theorem 3.1) that the proposed ELBO-based router achieves near-optimal compression under mild conditions. This provides a principled justification for adaptive tokenization that goes beyond heuristic masking.
- **Clear and well-motivated framework.** The adaptive tokenization framework is modular (router + compressor) and can be built on top of any existing fixed-length tokenizer (here Cosmos-DV). The design choices (ELBO as proxy for log-likelihood, likelihood-based token selection) are directly tied to the theoretical analysis.
- **Strong empirical results.** InfoTok consistently outperforms ElasticTok across multiple compression rates on both TokenBench and DAVIS, with substantial gains in PSNR, LPIPS, and FVD (e.g., FVD reduced by 40–60% at the same BPP). The ablation studies confirm that both the ELBO-based router and the likelihood-based compressor are crucial, and that the method generalizes across architectures.
- **Inference efficiency.** Unlike ElasticTok’s binary search (11 additional forward passes), InfoTok requires only one extra decoder pass to compute the ELBO, making it significantly more practical for real-world use.

## Weaknesses

### Fatal
None.

### Major
- **Theoretical assumptions may not fully hold in practice.** The optimality guarantee (Theorem 3.1) assumes the tokenizer minimizes the reconstruction loss and that the ELBO is a tight lower bound on the log-likelihood. In practice, the ELBO gap may be non-negligible, and the loss minimization may not be exact. While the paper acknowledges this, the practical gap between theory and implementation is not quantified.
- **Comparison with ElasticTok may be confounded by different base tokenizers.** InfoTok is built on Cosmos-DV, while ElasticTok uses its own architecture. Although the paper matches compression rates, differences in base tokenizer quality could partly explain the performance gap. The ablation in Table 3 (right) partially addresses this by swapping adaptive mechanisms on the same backbone, but the main comparison (Table 1, Figure 4) uses different base models.

### Minor
- **No evaluation on downstream tasks.** The paper focuses on reconstruction metrics as a proxy for representational quality. While this is a reasonable first step, the ultimate value of adaptive tokenization lies in downstream applications (e.g., video generation, understanding). The paper acknowledges this as a limitation but does not provide even small-scale downstream experiments.
- **Extra computational overhead.** The ELBO-based router requires an additional decoder pass. While much cheaper than ElasticTok’s search, this overhead is not negligible for very large models. The paper suggests lighter-weight routers as future work but does not explore them here.

### Trivial
- The notation for BPP (bits per 16 pixels) is non-standard and could be clarified earlier in the paper.

## Nice-to-Haves

- Explore a lightweight router that estimates information complexity directly from encoder latents, avoiding the extra decoder pass.
- Evaluate InfoTok on a downstream task such as video generation (e.g., using the tokens as input to a GPT-like model) to demonstrate practical benefits beyond reconstruction.
- Provide a more detailed analysis of the ELBO gap and its impact on the optimality bound in practice.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that adaptive tokenization should be driven by the *information content* of each video, not by heuristic masking or uniform random selection. By connecting token length to the negative log-likelihood (via ELBO), the paper shows that the optimal allocation is essentially a rate-distortion problem where each token should carry a similar amount of information. This perspective unifies compression theory with modern VAE-based tokenizers and provides a principled alternative to the ad-hoc approaches in prior work.

## Suggestions

- To strengthen the comparison with ElasticTok, consider fine-tuning ElasticTok on the same Cosmos-DV backbone (if feasible) or at least reporting results with both methods using the same base tokenizer.
- Include a small-scale downstream experiment (e.g., video classification with frozen tokens) to demonstrate that the compressed tokens retain semantic information.
- Discuss the sensitivity of the ELBO-based router to the quality of the fixed-length tokenizer and whether the method degrades when the base tokenizer is weaker.

## Score and Decision

**Score:** 8  
**Decision:** Accept  

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>