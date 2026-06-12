## Summary

This paper studies language model pre-training under a data-constrained regime with no compute constraints, motivated by the observation that compute grows much faster than web text. The authors show that standard approaches of increasing epoch count and parameter count overfit, and propose a regularized recipe with much higher weight decay (30× larger than standard) that achieves monotonic loss improvement following a power law in parameter count. They further demonstrate that ensembling independently trained models achieves a significantly lower loss asymptote than parameter scaling alone, and that composing both approaches yields a 5.17× data efficiency improvement at 200M tokens. The paper also shows that distillation can compress these gains into smaller models, and that validation loss improvements translate to downstream benchmarks.

## Strengths

- **Novel framing and evaluation metric**: The paper introduces the concept of evaluating scaling recipes by their asymptote (limit as parameters → ∞) rather than performance at fixed compute budgets, which is well-motivated for the data-constrained, compute-unlimited regime they study. This is a genuinely useful conceptual contribution.

- **Clear empirical findings with practical implications**: The discovery that optimal weight decay is 30× larger than standard practice (0.1) for over-parameterized models is a concrete, actionable finding. The demonstration that ensembling smaller models outperforms scaling a single large model under infinite compute is non-trivial and well-supported.

- **Thorough experimental design**: The paper systematically builds from standard recipe → regularized recipe → ensembling → joint scaling, with careful hyperparameter tuning at each step. The use of coordinate descent for hyperparameter optimization and the fitting of power laws with asymptotes is methodologically sound.

- **Generalization checks**: The paper validates that findings hold across multiple token counts (200M to 1.6B), that distillation preserves most gains, and that validation loss improvements translate to downstream benchmarks (PIQA, SciQ, ARC Easy). The decision to evaluate downstream benchmarks only at the end of the project is a good guard against cherry-picking.

## Weaknesses

### Major

- **Scale limitations**: All experiments are conducted at very small scales (200M-1.6B tokens, models up to 1.4B parameters). While the authors acknowledge this and attempt to extrapolate via data scaling laws, the core claims about "infinite compute" regimes are based on extrapolations from tiny models. The finding that optimal weight decay is 30× larger may not hold at scales where models are trained on trillions of tokens, and the ensembling benefits may diminish at larger scales where individual models are more capable.

- **Data scaling law extrapolation is speculative**: The data scaling laws in Section 5 are fit from only 4 token counts (200M, 400M, 800M, 1.6B) and extrapolate to much larger scales. The claim that "data efficiency wins will not disappear across all data scales" relies on the assumption that the asymptotes and exponents of different recipes are equal, which is not convincingly established with so few data points. The confidence intervals on these extrapolations are not provided.

- **Ensemble scaling comparison is not compute-matched**: The paper compares ensembling K models of size N to a single model of size NK in terms of "total parameter count," but this is not a fair comparison for inference cost. Ensembling K models requires K× the inference FLOPs, which is a significant practical limitation. The paper acknowledges this but does not adequately address whether the ensembling benefits persist when controlling for inference compute rather than total parameters.

### Minor

- **Limited downstream evaluation**: Only three benchmarks (PIQA, SciQ, ARC Easy) are used, all of which are relatively simple multiple-choice tasks. The claim that "improvements on validation loss translate to improvements on downstream benchmarks" would be stronger with a broader evaluation including generation tasks or more challenging benchmarks.

- **Hyperparameter tuning details are in appendix**: The coordinate descent algorithm for hyperparameter tuning is described in Appendix C.1, but the paper would benefit from a brief summary of the procedure in the main text, as the tuning methodology is central to the results.

- **The self-distillation result is interesting but underexplored**: The finding that self-distillation (teacher and student of same size) outperforms the teacher is notable, but the paper does not provide sufficient analysis of why this works or under what conditions it might fail (e.g., at larger scales or with more training).

### Trivial

- The paper uses "PDCMLoss" in Figure 8 which appears to be a typo for "DCLM loss."

## Nice-to-Haves

- A comparison to compute-matched baselines for ensembling (e.g., training a single model for K× more steps vs. training K ensemble members) would strengthen the practical relevance.
- Ablation studies on the effect of different regularization techniques (e.g., dropout, label smoothing) beyond weight decay would be informative.
- Analysis of whether the optimal weight decay depends on the parameter-to-token ratio in a systematic way would help practitioners apply these findings at different scales.

## Novel Insights

Beyond the paper's own contributions, the most novel insight is that the optimal regularization strength for data-constrained pre-training is dramatically higher than standard practice, and that this simple change transforms the scaling behavior from non-monotonic (overfitting) to monotonic power-law improvement. This suggests that many existing "scaling law" results may be artifacts of suboptimal regularization rather than fundamental limits. The finding that ensembling smaller models can outperform scaling a single large model under the asymptote metric is also a non-trivial challenge to the prevailing wisdom that "bigger is always better" in the compute-unlimited regime.

## Suggestions

- Add confidence intervals or error bars to the data scaling law extrapolations in Section 5 to better communicate uncertainty.
- Include a compute-matched comparison for ensembles (e.g., train a single model for K× more steps vs. K ensemble members) to clarify the practical trade-offs.
- Provide a brief summary of the coordinate descent hyperparameter tuning procedure in the main text for clarity.

## Score and Decision

The paper makes a clear, well-motivated contribution to an important and timely problem (data-constrained pre-training). The findings are novel, empirically sound within the studied scale, and have practical implications. The main limitations are the small experimental scale and the speculative nature of the data scaling law extrapolations, but these are acknowledged by the authors and do not invalidate the core contributions. The paper is well-written and the experimental design is thoughtful.

Score: 8

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>