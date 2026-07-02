## Summary

This paper studies language model pre-training under a data-constrained regime with unlimited compute. The authors show that standard recipes of epoching and parameter scaling overfit, and propose a regularized recipe with much higher weight decay (30× larger than standard) that achieves monotonic power-law scaling in parameter count. They further demonstrate that ensembling independently trained models achieves a lower loss asymptote than scaling a single model, and that composing both approaches yields a 5.17× data efficiency improvement at 200M tokens. The paper also shows that distillation can compress these gains into smaller models and that validation loss improvements translate to downstream benchmarks.

## Strengths

- **Novel framing and evaluation metric**: The paper introduces the concept of evaluating scaling recipes by their loss asymptote (as N → ∞) rather than at fixed compute budgets, which is a principled way to compare algorithms under the data-constrained, compute-unlimited regime. This is a genuinely new perspective on scaling law evaluation.

- **Clear and well-motivated problem**: The paper identifies a timely and important problem—the growing gap between compute growth and web text growth—and formulates it cleanly as a data-constrained, compute-unlimited pre-training problem. The motivation is compelling and well-articulated.

- **Comprehensive empirical study**: The paper conducts extensive experiments across multiple dimensions (regularization, ensembling, distillation, data scaling) with careful hyperparameter tuning. The experiments are well-designed and the results are presented clearly with power-law fits.

- **Practical findings with actionable insights**: The discovery that optimal weight decay is 30× larger than standard practice is a simple, actionable finding. The distillation results showing that gains can be compressed into smaller models are practically valuable.

- **Strong generalization checks**: The paper validates that validation loss improvements translate to downstream benchmarks, and that findings hold across multiple token budgets. The use of held-out benchmarks selected after the project is a strong test of generalization.

## Weaknesses

### Fatal
None.

### Major
- **Scale limitations**: All experiments are conducted at very small scales (200M tokens, models up to 1.4B parameters). While the paper acknowledges this and attempts to extrapolate to higher token counts, the extrapolations are based on only 4 data points (200M, 400M, 800M, 1.6B tokens) and models up to 1.4B parameters. It is unclear whether the findings—particularly the 30× larger weight decay and the superiority of ensembling over parameter scaling—hold at the scales where data constraints become practically relevant (e.g., trillions of tokens). The paper's central claim about a "compute-rich future" is about scales many orders of magnitude larger than what is tested.

- **Limited downstream evaluation**: The paper evaluates on only three small benchmarks (PIQA, SciQ, ARC Easy) that are appropriate for the model scale but provide limited evidence of generalization. More diverse evaluations (e.g., reasoning, coding, or multilingual tasks) would strengthen the claim that validation loss improvements translate to meaningful capabilities.

- **Ensemble scaling comparison is not compute-matched**: The paper compares ensembling K models of size N to a single model of size NK in terms of total parameters, but this is not a fair comparison in terms of training compute. Training K models of size N requires K× the compute of training one model of size N, while training one model of size NK requires more compute than training one model of size N but less than K× (since training compute scales super-linearly with parameters). The paper acknowledges this implicitly but does not fully address whether the ensembling advantage holds under a compute-matched comparison.

- **Hyperparameter tuning methodology is somewhat ad-hoc**: The coordinate descent approach for hyperparameter tuning is described at a high level, and the heuristic for joint scaling (2× epochs, 0.5× weight decay) is not rigorously justified. The paper would benefit from a more systematic tuning procedure or ablation studies showing sensitivity to these choices.

### Minor

- **Limited analysis of why ensembling outperforms parameter scaling**: The paper cites Allen-Zhu and Li (2023) for a theoretical explanation but does not provide empirical evidence (e.g., feature visualization, diversity analysis) to support the "multi-view" explanation in this specific setting.

- **The data efficiency metric is defined relative to the standard recipe baseline**: The 5.17× improvement is relative to a baseline that may not be optimally tuned. While the paper tunes the baseline reasonably, the absolute improvement might be smaller against a more carefully tuned standard recipe.

- **The paper does not study the effect of different data distributions or data quality**: All experiments use DCLM data. It is unclear whether the findings generalize to other data sources or data quality levels.

### Trivial
- The paper uses "PDCMLoss" in Figure 8 which appears to be a typo for "DCLM loss".

## Nice-to-Haves
- An ablation study showing the sensitivity of the results to the coordinate descent hyperparameter tuning procedure would strengthen the paper.
- Analysis of ensemble diversity (e.g., agreement rates, feature visualization) would provide empirical support for the "multi-view" explanation.
- Experiments with different model architectures (e.g., different width/depth ratios) would test the generality of the findings.
- A discussion of the computational cost of the hyperparameter tuning itself would help contextualize the practical feasibility of the approach.

## Novel Insights

The paper's most novel insight is the proposal to evaluate scaling recipes by their loss asymptote (as N → ∞) rather than at fixed compute budgets, which is a principled way to compare algorithms under data-constrained, compute-unlimited conditions. The finding that ensembling independently trained models achieves a lower asymptote than scaling a single model—and that the two compose—is a non-trivial empirical discovery. The observation that optimal weight decay is 30× larger than standard practice for over-parameterized models is a simple but impactful practical insight. The success of self-distillation (matching the regularized asymptote without increasing parameter count) is surprising given recent concerns about model collapse from training on synthetic data.

## Suggestions

- **Scale up experiments**: Even modestly scaling to 1-2B tokens and 7B parameter models would significantly strengthen the paper's claims about the persistence of the observed effects at larger scales. The current experiments are at scales where data constraints are not practically relevant.

- **Add compute-matched comparisons**: Provide a clearer comparison between ensembling and parameter scaling under matched training compute budgets, not just matched total parameter count. This would address a key ambiguity in the paper's central comparison.

- **Expand downstream evaluation**: Include more diverse benchmarks (e.g., HellaSwag, WinoGrande, MMLU subsets) to strengthen the claim that validation loss improvements generalize to meaningful capabilities.

- **Provide more systematic hyperparameter tuning details**: Include ablation studies showing the sensitivity of results to the coordinate descent procedure and the heuristic for joint scaling hyperparameters.

- **Add ensemble diversity analysis**: Measure and report ensemble diversity metrics (e.g., prediction disagreement, feature similarity) to empirically support the theoretical explanation for why ensembling outperforms parameter scaling.

## Score and Decision

The paper addresses a timely and important problem with a novel framing, comprehensive experiments, and actionable findings. The core contributions—the asymptote-based evaluation metric, the discovery of optimal weight decay 30× larger than standard, and the demonstration that ensembling outperforms parameter scaling under data constraints—are significant and well-supported by the experiments. The paper is clearly written and the experiments are carefully designed.

However, the major weakness is the scale of the experiments. All results are at 200M-1.6B tokens with models up to 1.4B parameters, which is far from the regime where data constraints become practically relevant (trillions of tokens). While the paper attempts to extrapolate, the extrapolations are based on limited data points and small scales. This limits confidence in whether the findings will hold at the scales that matter for the "compute-rich future" the paper motivates. Additionally, the downstream evaluation is limited to three small benchmarks.

Despite these limitations, the paper's contributions are significant: a novel evaluation framework (asymptote-based), a simple and actionable finding (30× larger weight decay), and a clear demonstration that ensembling and distillation can provide substantial data efficiency gains. The experiments are carefully conducted and the results are internally consistent. The paper is likely to influence how the community thinks about data-constrained pre-training.

**Score: 8** — This is a strong paper with a novel contribution, careful experiments, and actionable findings. The scale limitations prevent a higher score, but the paper is clearly above the acceptance threshold.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>