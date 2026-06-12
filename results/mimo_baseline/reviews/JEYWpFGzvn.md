## Summary
This paper introduces INFOTOK, an information-theoretic framework for adaptive video tokenization that allocates variable numbers of tokens based on per-video information complexity. The authors prove that fixed-rate and data-agnostic adaptive tokenizers are theoretically suboptimal, propose an ELBO-based router to determine token lengths, and develop a transformer-based adaptive compressor, demonstrating ~50% token savings without quality loss and 2.3× compression improvement over the prior adaptive method ElasticTok.

## Strengths
- **Rigorous theoretical grounding**: The paper provides meaningful proofs showing that fixed-rate tokenizers are inherently suboptimal (Theorem 2.1), that uniform routers can be arbitrarily biased (Theorem 2.2), and that the ELBO-based router achieves near-optimal compression (Theorem 3.1). These results are non-trivial and provide a principled foundation for adaptive tokenization that goes beyond heuristic motivation.
- **Modular and practical design**: INFOTOK is built on top of existing fixed-length tokenizers (Cosmos), requiring only an additional router and adaptive compressor. The ELBO-based router needs only one extra decoder pass, making it 11× more efficient than ElasticTok's binary search approach. The Flex variant ensembles multiple compression rates into a single model, adding practical flexibility.
- **Thorough ablation studies**: Table 2 demonstrates that the ELBO-based router performs nearly identically to an exhaustive "optimal" search strategy, validating the theoretical claims empirically. Table 3 shows the adaptive mechanism generalizes across architectures (Cosmos and ViT backbones) and that the ELBO-based compressor outperforms naive masking strategies (right-to-left, jump).
- **Comprehensive benchmarking**: The paper compares against three fixed-length baselines and one adaptive baseline across two datasets with four quality metrics, showing consistent improvements. The visualizations in Figures 2 and 3 effectively illustrate how INFOTOK allocates more tokens to complex content.

## Weaknesses
### Fatal
None.

### Major
- **No downstream task evaluation**: The entire evaluation is limited to reconstruction quality (PSNR, SSIM, LPIPS, FVD). The paper's introduction motivates the work with "unified multi-modal models" and "video-understanding or generation tasks," yet no downstream experiments are conducted. The claim of "saving 20% tokens without influence on performance" is only validated for reconstruction, not for the tasks that actually consume these tokens. This is a significant gap given that the paper positions itself as enabling efficient long-video processing for foundation models.
- **Narrow adaptive baseline comparison**: ElasticTok is the sole adaptive baseline. Recent methods like FlexTok, ALIT, CAT, and One-D-Piece are discussed in related work but not empirically compared. This limits the strength of "state-of-the-art" claims, particularly since FlexTok uses a diffusion decoder which may handle low-token-count regimes differently.

### Minor
- **ELBO-log-likelihood gap not empirically validated**: The router's quality depends on ELBO being a tight proxy for log-likelihood. While theoretically motivated, the paper does not measure the actual correlation between ELBO values and reconstruction difficulty, or quantify the ELBO-log-likelihood gap in practice.
- **Coarse grid for "Optimal" search in Table 2**: The optimal strategy searches over BPP₁₆ ∈ {1/16, 6/16, ..., 1}, a relatively coarse grid. A finer grid might reveal larger gaps between the ELBO-based router and the true optimum.
- **Sensitivity of Flex hyperparameters**: INFO_TOK-Flex uses B = {0.25N_max, 0.5N_max, 0.75N_max, N_max} without exploring sensitivity to the number or spacing of compression rates.

### Trivial
None.

## Nice-to-Haves
- A downstream video generation or understanding experiment, even at small scale, would substantially strengthen the paper's impact claims.
- Correlation analysis between ELBO values and per-video reconstruction error to empirically validate the router's proxy quality.

## Novel Insights
The key novel insight is that data-agnostic adaptive routers (e.g., uniform random masking as in ElasticTok) are not merely suboptimal in a mild sense but can be *arbitrarily* suboptimal relative to information-theoretic bounds (Theorem 2.2). This is a strong negative result that motivates the need for content-aware routing. The paper then constructively shows that ELBO—a quantity already available in VAE-style tokenizers—serves as a near-optimal proxy for determining per-video token allocation, bridging information theory and practical deep learning tokenization in a clean way.

## Suggestions
- Add at least one downstream task experiment (e.g., video generation with a autoregressive model consuming INFOTOK tokens) to validate that reconstruction-level improvements translate to task-level improvements.
- Compare against FlexTok or other recent adaptive image/video tokenizers to broaden the empirical comparison.
- Report the Pearson/Spearman correlation between per-video ELBO values and reconstruction error to empirically validate the router.

## Score and Decision
The paper makes a genuine theoretical contribution by proving the suboptimality of existing approaches and providing a principled alternative, backed by solid reconstruction-level experiments and thorough ablations. However, the absence of downstream task evaluation and the narrow adaptive baseline comparison are notable limitations that prevent a stronger recommendation. The work is well-executed within its stated scope but the practical impact for the broader community remains uncertain without evidence that adaptive tokens improve the tasks that consume them.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept