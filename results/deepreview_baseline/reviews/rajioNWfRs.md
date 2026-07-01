## Summary
This paper introduces TNT, a two-stage training paradigm for deep memory modules (such as Titans and TTT) that decouples training efficiency from inference performance. Stage 1 uses a hierarchical memory architecture with a global module for long-range context and parallel local modules with periodic state resets to enable massive context parallelism. Stage 2 is a brief fine-tuning phase that adapts local memory modules to smaller chunk sizes for optimal inference. The authors demonstrate up to 17× training speedup on Titans models while simultaneously improving model accuracy.

## Strengths
- **Addresses a genuine and important bottleneck**: The paper correctly identifies that deep memory modules (non-linear RNNs with test-time memorization) suffer from prohibitively slow training due to poor hardware utilization, and this is a critical barrier preventing these architectures from competing with Transformers. The problem is well-motivated and practically significant.
- **Novel technical contribution with clear reasoning**: The periodic state reset mechanism for local memories is a clever and principled way to break sequential dependencies in non-linear RNNs, enabling context parallelism. The Q-K projection to resolve the compression-retrieval domain mismatch is also well-motivated and elegantly implemented with a running sum.
- **Strong empirical results**: The 17× speedup over the most accurate baseline configuration while simultaneously improving perplexity is impressive. The ablation study cleanly validates each design choice (hierarchical memory, Q-K projection, Stage 2 fine-tuning), and the linear scaling with sequence length is clearly demonstrated.

## Weaknesses

### Fatal
None.

### Major
- **The paper overclaims relative to Transformers while the comparison is incomplete**: The paper states TNT achieves "up to 17× faster than the most accurate baseline configuration" and that TNT "outperforms even the highly optimized FlashAttention kernel." However, Table 1 shows that Transformers with FlashAttention (w/ gating) are still 20.22× faster than the Titans baseline (C=8), while TNT's best speedup is 17.37×. The claim about beating FlashAttention in Figure 4 is only for a specific configuration (C_L=128) and the paper does not report perplexity for that configuration—the best perplexity models use smaller chunk sizes. The paper should be more precise about which specific comparison is being made.
- **The 150M parameter scale is too small to be conclusive**: All experiments are at 150M parameters. At this scale, many architectural differences are less pronounced, and the practical bottlenecks of deep memory modules may manifest differently at larger scales (e.g., 1B+ parameters). The paper claims to "remove a critical scalability barrier" but only demonstrates scaling at a single, small model size. The authors should acknowledge this limitation more explicitly and ideally provide at least one experiment at a larger scale.
- **Stage 2 fine-tuning gains are marginal**: The improvement from Stage 1 (best PPL 23.13) to Stage 2 (best PPL 23.09) is only 0.04 perplexity points. While the paper claims this is "computationally inexpensive," the practical significance of this improvement is questionable. The authors should either provide stronger evidence that Stage 2 is meaningful (e.g., showing it enables chunk size 1 inference which is critical for autoregressive decoding) or temper their claims about its importance.

### Minor
- **The paper does not compare against the most recent deep memory modules**: The paper focuses on Titans and TTT but does not compare against Atlas (Behrouz et al., 2025a) which is cited in the introduction. Given that Atlas is a contemporary deep memory module, its absence from the experimental comparison is noticeable.
- **The Q-K projection analysis could be deeper**: The paper motivates Q-K projection as solving a domain mismatch but does not provide empirical analysis of the key vs. query distributions to demonstrate the mismatch exists. A simple visualization or quantitative measure would strengthen this claim.

### Trivial
- The paper uses "TNT" as an abbreviation but the expansion is given in a footnote rather than the main text.

## Nice-to-Haves
- A comparison against Mamba or other state-space models would help contextualize TNT's performance within the broader efficient sequence modeling landscape.
- Analysis of how the local window size S_L affects the trade-off between parallelism and context retention would be useful for practitioners.
- A discussion of how TNT handles the "memory staleness" issue—since local memories are reset, information from earlier in the sequence is lost unless captured by the global memory.

## Novel Insights
The key insight is that the chunk size conflict in deep memory modules can be resolved by recognizing that different components of the model should operate at different granularities during different training stages. The periodic state reset for local memories is a surprisingly simple yet effective mechanism to enable context parallelism for non-linear RNNs—a problem that has been considered largely unsolved outside of linear RNNs. The Q-K projection insight—that the compression and retrieval stages operate on different input domains (keys vs. queries)—is a subtle but important observation that likely applies to many memory-augmented architectures beyond those studied here.

## Suggestions
- Add at least one experiment at a larger scale (e.g., 350M or 1B parameters) to demonstrate that the speedup and quality improvements hold at practical model sizes.
- Clarify the comparison with FlashAttention: report both speed and perplexity for the same configuration to give a fair comparison.
- Provide a more detailed analysis of Stage 2 fine-tuning, including how many steps are needed and whether the gains are statistically significant.

## Score and Decision
The paper addresses a genuine and important problem with a novel, well-motivated solution. The empirical results are strong and the ablation study is clean. However, the limited scale (150M parameters) and the marginal gains from Stage 2 fine-tuning prevent this from being a definitive contribution. The paper is a solid contribution that advances the state of the art in training deep memory modules, but it does not yet fully deliver on its promise of removing the scalability barrier at practical model sizes.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>