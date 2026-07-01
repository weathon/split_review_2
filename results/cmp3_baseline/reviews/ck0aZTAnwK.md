## Summary

This paper studies language model pre-training under a fixed data budget with no compute constraint, motivated by the observation that compute grows faster than web text. The authors show that standard data-constrained recipes (epoching and parameter scaling) overfit, and propose a regularized recipe with much higher weight decay (30x larger than standard) that yields monotonic power-law scaling in parameter count. They further show that ensembling independently trained models achieves a lower loss asymptote than scaling parameter count alone, and that combining both (joint scaling) gives the best data efficiency. Their interventions achieve up to 5.17x data efficiency gains at 200M tokens, and these gains persist when extrapolated to higher token budgets. Distillation can compress most of the ensemble benefit into smaller models, and improvements on validation loss transfer to downstream benchmarks.

## Strengths

- **Novel framing and evaluation metric**: The paper identifies an important and timely problem (pre-training when compute exceeds data) and proposes evaluating recipes via the asymptote of their scaling law rather than performance at a fixed compute budget, which is conceptually appropriate for the infinite-compute setting.
- **Clear empirical contribution**: The finding that optimal weight decay is 30x larger than standard practice under data constraints is a non-obvious and practically actionable insight. The systematic hyperparameter tuning and demonstration of monotonic scaling are thorough.
- **Comprehensive recipe comparison**: The paper systematically compares parameter scaling, ensemble scaling, and their combination, building scaling laws in each case and quantifying data efficiency relative to a standard baseline. The distillation experiments further show practical utility.
- **Downstream validation**: The authors confirm that validation loss improvements translate to real benchmark gains (9% average improvement), strengthening the relevance of the main results.

## Weaknesses

### Fatal
None.

### Major
1. **Limited experimental scale**: The experiments use at most 1.6B tokens and 1.4B parameters. While the paper acknowledges this and extrapolates via data scaling laws, the core claims about "infinite compute" and the persistence of data efficiency gains at much larger scales rest on extrapolation from relatively small-scale runs. It remains uncertain whether the same phenomena and exponents hold at e.g. 100B tokens or 10B+ parameter models.

2. **Baseline may understate standard practice**: The "standard recipe" baseline tunes epochs and learning rate but does not tune weight decay. Many practitioners do tune regularization, so the gap between the standard and regularized recipes may be smaller against a stronger baseline that also tunes weight decay. The paper argues this represents common practice (weight decay 0.1 from Brown et al. 2020), which is fair, but the strength of the claimed improvement depends on this comparison.

3. **Downstream evaluation is narrow**: Only three small benchmarks (PIQA, SciQ, ARC Easy) are used. While these are appropriate for the model scale, the paper's claims about generalization to downstream tasks would be strengthened by a broader evaluation or a discussion of which capabilities these benchmarks cover.

### Minor
- The coordinate descent hyperparameter tuning procedure is described at a high level; more details on the search space and convergence would be helpful (likely deferred to appendix, but the main text could summarize key choices).
- The exponent of ~1.0 in the parameter scaling law is much larger than typical Chinchilla exponents (~0.34); the paper attributes this to better data leverage, but further intuition or analysis of why regularization changes the exponent so dramatically would strengthen the contribution.

### Trivial
None.

## Nice-to-Haves

- Experiments at a larger token count (e.g., 6.4B or 12.8B) to directly validate the extrapolation of data scaling laws, even if with fewer parameter counts.
- A comparison against a recent data-constrained approach such as synthetic data generation or diffusion language models, to contextualize the magnitude of improvement.
- Analysis of ensemble member diversity (e.g., agreement, feature overlap) to support the "multi-view" explanation.

## Novel Insights

The paper's key insight is that under data-constrained pre-training with unlimited compute, the optimal strategy is not simply to scale model size arbitrarily, but to scale ensemble size, because ensembling independently trained models achieves a lower loss asymptote than a single model of equivalent total parameter count. This reverses the typical Chinchilla intuition that a single large model is compute-optimal. The finding that optimal weight decay grows with model size (reaching 30x standard values) is also surprising and practically valuable.

## Suggestions

- To strengthen the empirical claims, include at least one additional data scale (e.g., 3.2B tokens) to validate the extrapolation of data scaling laws, even if with fewer model sizes or ensemble members.
- Consider comparing the regularized recipe against a baseline that also tunes weight decay to isolate the contribution of aggressive regularization from the contribution of joint hyperparameter tuning.
- Expand the downstream evaluation to include additional benchmarks (e.g., WinoGrande, HellaSwag) or provide a more detailed analysis of why the chosen benchmarks are representative.

## Score and Decision

The paper is a solid, well-executed contribution to a timely problem. It provides novel insights, clear methodology, and convincing evidence within its experimental scope. The major weakness is the limited scale, which tempers confidence in extrapolation to the large-scale setting that motivates the paper. Nonetheless, the results are valuable and likely to influence future pre-training practice.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>