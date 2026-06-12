## Summary

This paper investigates how architectural choices—specifically hidden size, mlp-to-attention ratio, and grouped-query attention (GQA)—affect the trade-off between inference efficiency and accuracy in decoder-only LLMs. The authors propose a conditional scaling law that augments the Chinchilla framework with architectural parameters, enabling prediction of how architectural variants affect training loss. They validate their framework by training over 200 models from 80M to 3B parameters and demonstrate that optimized architectures (Surefire models) achieve up to 2.1% higher accuracy and 42% greater inference throughput compared to LLaMA-3.2 baselines under identical training budgets.

## Strengths

- **Pragmatic and well-motivated problem formulation.** The paper addresses a genuinely important gap: existing scaling laws focus almost exclusively on training compute, yet inference cost dominates deployment. The authors clearly motivate why prior approaches (Sardana et al. 2023, Bian et al. 2025) are insufficient, and their design choice to fix the number of layers while varying hidden size and mlp-to-attention ratio is well-justified by the observation that open-weight models with similar parameter counts use markedly different architectures.

- **Comprehensive empirical validation.** The paper trains over 200 models spanning multiple scales (80M to 3B) and token budgets (8B to 100B), systematically varying architectural factors. The three-task progressive evaluation (fit on smaller, evaluate on larger) provides convincing evidence that the conditional scaling law generalizes. The low MSE (0.0001–0.0002) and high Spearman correlations (0.745–0.891) across scales are impressive.

- **Clean, interpretable methodology.** The two-step conditional approach (Chinchilla reference loss + multiplicative/additive calibration for architectural factors) is simple, transparent, and avoids overfitting. The U-shaped relationships in Figures 4 and 5 are physically plausible and well-documented. The search framework (Algorithm 1) is practical and directly actionable for practitioners.

- **Practical impact demonstrated.** The resulting Surefire models outperform LLaMA-3.2 baselines on both accuracy (up to 2.1% gain) and inference throughput (up to 42% gain) under identical training budgets. The ablation of fitting data strategy (Figure 8) provides useful practical guidance: fitting within one-third of the target scale is sufficient.

## Weaknesses

### Fatal
None.

### Major

- **Limited scope of architectural factors.** The paper fixes the number of layers and only varies hidden size, mlp-to-attention ratio, and GQA. While the authors justify fixing layers, this is a significant limitation because layer count strongly influences both accuracy and inference latency. The claim that "aspect ratio alone fails to capture the full range of factors that influence inference efficiency" (page 2) is valid, but the paper does not adequately address the interaction between layer count and the studied factors. A practitioner reading this paper cannot determine the optimal number of layers for a given parameter budget, which is arguably the most important architectural decision.

- **GQA analysis is incomplete.** The paper acknowledges that GQA does not exhibit a consistent continuous relationship with loss (Appendix I) and resorts to a local search with early stopping. However, the ablation of GQA on inference efficiency (Figure 11, Appendix F) is not shown in the main paper, and the reader cannot assess the magnitude of GQA's impact. More importantly, the paper does not study whether the optimal GQA value interacts with hidden size or mlp-to-attention ratio—the three factors are treated as separable, but there is no empirical evidence supporting this separability assumption for GQA.

- **Downstream evaluation is limited.** The nine benchmarks used (ARC-Easy/Challenge, LAMBADA, HellaSwag, OpenBookQA, PIQA, SciQ, Winogrande, CoQA) are relatively simple and mostly single-answer or multiple-choice tasks. The paper does not evaluate on more challenging benchmarks such as MMLU, GSM8K, HumanEval, or reasoning-based tasks that are more discriminative at the 1B–3B scale. The reported accuracy gains (0.6–2.1%) may not reflect meaningful improvements on harder tasks. Additionally, the paper does not report standard deviations or statistical significance for the downstream results.

- **The claim of "42% higher inference throughput" is not consistently contextualized.** Table 6 (Appendix F) shows that the throughput gain varies significantly by batch size, hardware, and serving framework. At batch size 16, Surefire-1B achieves ~22% improvement over LLaMA-3.2-1B on A100, while at batch size 128, the improvement reaches ~38–42%. The paper should clearly state which configuration yields the 42% figure and whether this represents the maximum or typical gain.

### Minor

- **The training token budget (100B for 1B and 3B models) is relatively small** compared to typical pretraining (e.g., LLaMA-3.2-3B was trained on significantly more tokens). The authors use 100×N tokens, which is 5× Chinchilla optimal. While this ensures convergence for the purpose of fitting scaling laws, it is unclear whether the optimal architectures under this budget generalize to the massively over-trained regime (e.g., 2T+ tokens) typical of production models.

- **The multiplicative and additive calibration forms assume separability** of hidden size and mlp-to-attention ratio effects on loss. The paper briefly notes that joint non-separable formulations do not improve performance (Appendix J), but this negative result is not shown in the main paper. Given that the paper's core contribution is a conditional scaling law, the separability assumption deserves more thorough empirical validation.

- **The paper does not compare to other architecture search methods** for LLMs, such as neural architecture search (NAS) or evolutionary methods. While the conditional scaling law approach is more efficient, the paper could benefit from a brief discussion of how it relates to these alternatives.

### Trivial

- The legend in Figure 2 caption is repeated verbatim below the figure.
- The paper refers to "Table 6" in the main text but Table 6 is in Appendix F; the reader is left searching.
- The abstract states "80M to 3B parameters and 8B to 100B training tokens" but the 3B models are trained on 100B tokens, which is 33×N, not 100×N as stated in the training setup section for smaller models.

## Nice-to-Haves

- Apply the framework to 7B-scale models and evaluate on more challenging benchmarks (MMLU, GSM8K, etc.) to strengthen claims about real-world impact.
- Study the interaction between layer count and the other architectural factors, perhaps by jointly optimizing layer count alongside hidden size and mlp-to-attention ratio.
- Provide analytical expressions for inference throughput as a function of architecture, enabling fully analytical Pareto optimization without requiring enumeration over feasible configurations.

## Novel Insights

The paper's most genuinely novel insight is that the optimal mlp-to-attention ratio for LLMs is not universally low (as recent trends toward allocating fewer parameters to attention might suggest), but instead exhibits a U-shaped relationship with a clear interior optimum around r=1–1.2 for models up to 3B parameters. This contradicts the design choices of several prominent open-weight models (e.g., LLaMA-3.2-1B has r=4.8), suggesting that many current architectures are suboptimal for the inference-accuracy trade-off. The finding that fitting data from models approximately one-third the target scale yields better predictions than fitting from much smaller models is also practically valuable.

## Suggestions

- **Clarify the scope of the contribution.** The paper should explicitly state that the framework is designed for a fixed layer count and that the optimal architectures identified may not be optimal if layer count is also allowed to vary. Add a discussion of when fixing layers is reasonable (e.g., within a model family with a fixed depth) and when it is not.
- **Report downstream results with error bars** (e.g., standard deviation over 3–5 runs) and include results on harder benchmarks (e.g., MMLU 0-shot/5-shot) to strengthen the claim that architectural optimization improves meaningful performance.
- **Provide a sensitivity analysis** of the optimal architecture to the training token budget. If the optimal hidden size and mlp-to-attention ratio shift significantly when trained on 200B or 500B tokens, the practical value of the framework is limited.
- **Show the GQA inference efficiency ablation** (Figure 11 in Appendix F) in the main paper, as it is referenced multiple times in the core methodology.
- **Clarify the 42% throughput claim:** specify exact batch size, hardware, serving framework, and token generation length for this maximum figure. Report the range of gains across configurations.

## Score and Decision

The paper addresses a timely and important problem with a well-executed methodology. The empirical validation is thorough, the conditional scaling law is clean and interpretable, and the practical results (accuracy gains + throughput improvements) are compelling. The main weaknesses are the limited scope of architectural factors (fixed layers, limited GQA analysis) and the relatively lightweight downstream evaluation. However, within its stated scope, the paper makes a solid contribution that is likely to be practically useful for the LLM deployment community.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>