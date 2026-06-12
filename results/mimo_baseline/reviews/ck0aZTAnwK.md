## Summary

This paper investigates pre-training under fixed data with unlimited compute, showing that standard approaches of increasing epochs and parameters lead to overfitting. The authors demonstrate that aggressively increasing weight decay (30× standard practice) enables monotone power-law scaling in parameter count, propose evaluating scaling recipes by the asymptote of their power laws, and show that ensembling independently trained models achieves a lower asymptote than parameter scaling alone. Their best combined recipe achieves 5.17× data efficiency over the baseline, and distillation can compress most of this benefit into smaller models.

## Strengths

- **Novel and well-motivated research question.** The paper clearly identifies the growing compute-to-data gap and frames a concrete, important question: how to pre-train under fixed data and no compute constraints. The asymptote-based evaluation framework is a genuinely useful conceptual contribution for reasoning about scaling in this regime.

- **Strong empirical methodology with careful hyperparameter tuning.** The paper performs extensive joint tuning of weight decay, learning rate, and epoch count using coordinate descent across four parameter counts (150M–1.4B). The finding that optimal weight decay is 30× larger than standard practice (0.1) is concrete, actionable, and well-supported by the data in Figure 3.

- **Comprehensive experimental narrative.** The paper systematically builds from standard recipes (Section 2) → regularized recipes (Section 3) → ensembling (Section 4) → data scaling (Section 5) → distillation (Section 6) → downstream benchmarks (Section 7), with each section building on the previous. The 5.17× data efficiency claim is well-documented through the multi-step asymptote estimation procedure.

- **Practical distillation results.** The demonstration that an 8-ensemble of 300M models can be distilled into a single 300M student retaining 83% of the ensemble benefit (Figure 8) is practically valuable and addresses the obvious concern about inference cost. The self-distillation result is surprising and interesting.

- **Downstream benchmark validation.** The 9% improvement on PIQA, SciQ, and ARC Easy confirms that validation loss improvements transfer to downstream tasks, and the authors note these benchmarks were only evaluated after recipe selection, making this a genuine test of generalization.

## Weaknesses

### Fatal

None.

### Major

- **Small experimental scale limits confidence in extrapolation.** The primary experiments use 200M tokens with models up to 1.4B parameters. While the paper extends to 1.6B tokens in Section 5, the data scaling laws are fit on only four token counts and the authors acknowledge they are "expected to be noisy." The claim that "data efficiency improvements will persist at higher token counts" (Section 5.3) rests on extrapolation from these noisy laws with similar exponents (0.23–0.24) and asymptotes (1.89–1.96). At modern pre-training scales (trillions of tokens, hundreds of billions of parameters), the relative benefit of these techniques is genuinely uncertain.

- **No compute efficiency analysis for ensembling.** The paper compares recipes by total parameter count (NK for ensembles), but does not analyze total training FLOPs. Training K independent models requires K× the training compute of a single model. A fairer comparison would be: given a fixed compute budget, is it better to train one large model or an ensemble of smaller models? The paper's framing of "infinite compute" sidesteps this, but the practical value of the approach depends on whether the compute overhead is justified.

- **Power law fits on limited data points.** The regularized recipe power law (Figure 3) is fit on only four parameter counts. The ensemble scaling law (Figure 4) is also fit on four points. The joint scaling recipe (Figure 5) involves nested power law fits on similarly sparse data. While the fits appear reasonable, the confidence intervals on the asymptotes are not systematically reported (only briefly mentioned in Appendix I.1 with ±0.02 variation across seeds).

### Minor

- **The "infinite compute" framing is somewhat misleading.** The paper's regime is better described as "fixed data, flexible compute" rather than truly infinite compute. The ensemble approach requires K×N parameters at inference time, and even with distillation, the training compute for the best recipe is substantial. A clearer framing of the practical compute costs would strengthen the paper.

- **Hyperparameter tuning cost is not discussed.** The regularized recipe requires jointly tuning weight decay, learning rate, and epoch count at each parameter count. The paper does not discuss the computational cost of this search or whether the optimal hyperparameters follow predictable patterns that could reduce tuning overhead.

- **Limited model scale diversity.** All experiments use a single architecture family. It would be valuable to know whether the 30× weight decay finding and the relative ranking of recipes hold for different architectures (e.g., different depths, widths, or attention mechanisms).

### Trivial

None.

## Nice-to-Haves

- A comparison of total training FLOPs across recipes, not just parameter counts, to help practitioners understand the compute tradeoffs.
- Analysis of whether optimal weight decay follows a predictable function of the parameter-to-data ratio, which would reduce tuning costs.
- Experiments at slightly larger scales (e.g., 1B+ tokens, 7B+ parameters) to increase confidence in the extrapolation.

## Novel Insights

The paper's most novel insight is the proposal to evaluate scaling recipes by the asymptote of their power law rather than performance at a fixed compute budget. This reframes the question from "what is the best model I can train with X FLOPs?" to "what is the best model I can possibly train with this data?" The finding that ensembling achieves a lower asymptote than parameter scaling (3.34 vs 3.43) is theoretically interesting and aligns with the "multi-view" theory of Allen-Zhu and Li (2023). The practical insight that aggressive regularization (30× standard weight decay) is necessary for monotone scaling in over-parameterized, data-constrained regimes is a valuable correction to current practice.

## Suggestions

- Add a compute efficiency analysis comparing total training FLOPs across all recipes, including the cost of hyperparameter search.
- Investigate whether the optimal weight decay follows a predictable function of the parameter-to-data ratio (e.g., linear or polynomial), which would make the regularized recipe more practical.
- Provide confidence intervals on all asymptote estimates, not just the 200M token case.
- Consider experiments at one or two larger scales to strengthen the extrapolation claims.

## Score and Decision

The paper presents a clear, well-motivated research question with a systematic experimental approach. The core findings—aggressive regularization for data-constrained scaling, asymptote-based evaluation, and ensembling outperforming parameter scaling—are novel and well-supported at the experimental scale used. The main limitation is the small scale of experiments (200M tokens, 1.4B parameters), which limits confidence in the extrapolation to practical settings. The lack of compute efficiency analysis for ensembling is a notable gap. However, the conceptual contributions (asymptote framework, the regularization finding) are valuable regardless of scale, and the distillation results show practical applicability. The paper would benefit from larger-scale validation but the current evidence is sufficient to warrant interest from the community.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept