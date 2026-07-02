## Summary

The paper introduces Dynamic Nested Depth (DND), a post-training method that improves LLM performance by selectively reprocessing "critical" tokens through an additional pass of the same transformer layer. A router identifies tokens requiring deeper processing, and their hidden states are refined via a nested pass and fused with the original outputs. The method includes specialized training losses for router discriminability and a dynamic threshold control scheme for stable token selection. Experiments on dense (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and MoE (Qwen3-30B-A3B) models show consistent gains (0.87%–2.61% average improvement) across diverse benchmarks with modest compute overhead (~7–8% throughput reduction).

## Strengths

- **Novel and well-motivated approach**: The idea of dynamically routing only difficult tokens for extra depth in latent space is a natural extension of token pruning and test-time scaling insights. The paper clearly motivates why token-choice routing and nested reprocessing are beneficial.
- **Effective training strategy**: The combination of router controlling loss (score dispersion + distribution preservation) and threshold control (buffer proportional + EMA synchronization) is carefully designed to address the instability of token-choice routing. Ablations confirm each component contributes meaningfully.
- **Strong empirical validation across architectures**: DND is evaluated on three small dense models and a 30B MoE model, covering 17 diverse benchmarks. The consistent improvements—especially on reasoning-heavy tasks (BBH, GPQA, coding)—demonstrate practical utility.
- **Comprehensive analysis**: The paper includes token selection analysis (entropy correlation), threshold dynamics visualization, and layer-wise selection patterns, providing insight into why and how DND works.

## Weaknesses

### Major

- **Lack of statistical significance / error bars**: Results are reported as single numbers without confidence intervals or standard deviations. Given the modest average gains (0.87%–2.61%), it is unclear whether differences are significant beyond random variation. This is important for empirical claims in a top venue.
- **Insufficient baseline comparisons**: The only direct comparison is to ITT (on Qwen3-1.7B), which shows DND is much better. However, MOR is discussed as the most related work, but no adaptation of MOR to the post-training setting is attempted or compared. While MOR requires pretraining from scratch, a reasonable baseline could be a simpler post-training approach (e.g., just adding a fixed-depth loop for all tokens, or a random router). The paper would benefit from such baselines to isolate the benefit of dynamic selection.

### Minor

- **Limited analysis of compute-accuracy trade-off**: The FLOPs and throughput numbers are provided, but there is no systematic study varying the target selection ratio (ablation only on Qwen3-1.7B shows 10% vs 20% vs 30%). A Pareto curve showing performance vs. compute for different selection ratios across models would strengthen the claims of efficiency.
- **Learnable fusion parameter β not analyzed**: The fusion uses a learnable β, but its final learned value and sensitivity are not reported. It would be informative to know if β converges to a consistent range across layers / models.
- **Post-training data dependence**: The method requires SFT on 1–2M synthetic instances. The paper does not discuss how sensitive results are to the quality or composition of this training data, nor whether the gains persist with smaller amounts of data.

### Trivial

- The paper claims "negligible parameter increase (<0.1M)" but does not break down the source of these parameters (router + β).

## Nice-to-Haves

- Add error bars (e.g., bootstrap confidence intervals) to main results.
- Compare against a simple baseline: fixed-depth loop for all tokens (e.g., repeating the layer for all tokens once) to isolate the benefit of *selective* reprocessing.
- Show a compute vs. accuracy Pareto curve for different target selection ratios.
- Analyze sensitivity to training data size and quality.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Report confidence intervals or standard deviations for the average scores in Tables 1 and 2.
- Include a baseline where all tokens undergo one extra pass (non-selective) to demonstrate that the benefit comes from dynamic selection, not just extra computation.
- Provide the learned β values and discuss whether they vary meaningfully across layers or tasks.

## Score and Decision

**Score**: 6 (borderline accept)

**Decision**: Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>