## Summary

The paper introduces VideoJudge, a bootstrapping framework for training MLLM-based evaluators specialized for video understanding. The core innovation is an iterative generator-evaluator pipeline that synthesizes high-quality training data without human annotation, enabling smaller models (3B and 7B) to match or outperform much larger models (up to 72B) on evaluation tasks. Additionally, the paper demonstrates training judge models to generate instance-specific rubrics at test time, improving interpretability and reliability.

## Strengths

- **Well-motivated problem and practical methodology**: The paper addresses the critical need for scalable, reliable evaluation of video understanding models. The bootstrapping approach that leverages a generator-evaluator pipeline to create training data without human annotation is clever and potentially impactful, especially given the scarcity of human preference data for video tasks.

- **Comprehensive evaluation across multiple benchmarks**: The paper evaluates on four pointwise benchmarks (including two constructed benchmarks and two independent benchmarks: VATEX, LongVideoBench) and three pairwise benchmarks (VideoAutoArena, VideoJudge-Pairwise, VideoJudge-Pairwise-H). The inclusion of both constructed and independent benchmarks strengthens the validity of the results.

- **Strong empirical results**: VideoJudge-7B consistently outperforms or matches much larger baselines (Qwen2.5-VL-32B/72B) across multiple benchmarks. For example, on LongVideoBench, VideoJudge-7B achieves Δ(C-D) of 1.16 vs. 1.08 for Qwen2.5-VL-32B and 1.06 for Qwen2.5-VL-72B. Similarly, on pairwise evaluation, VideoJudge-7B achieves 98.6% accuracy on the VideoJudge benchmark.

- **Rubric generation as a novel capability**: Training the judge model to generate instance-specific rubrics at test time is a valuable contribution. The analysis showing VideoJudgeR-3B produces rubrics preferred by both human annotators and LLM judges is compelling and opens up directions for more interpretable evaluation.

- **Thorough analysis of design choices**: The paper studies the effect of number of frames, decoding temperature, and compares with/without feedback. The finding that training benefits from up to 240 frames while evaluation saturates at ~120 frames provides practical guidance. The robustness of VideoJudge to temperature variation is also a useful insight.

## Weaknesses

### Fatal
None.

### Major
- **Systematic calibration issues and overestimation bias**: The error analysis reveals that the judge model overestimates scores by ≥2 points in 14.8% of cases while underestimating by the same margin in only 1.5%. Furthermore, only 36.9% of rating-3 responses are correctly scored, with 46.6% inflated to 5, and 81.3% of rating-4 responses incorrectly rated as 5. This represents a significant flaw for a model intended for fine-grained evaluation, as it cannot reliably distinguish between moderate and high-quality responses. The paper acknowledges this but does not provide a sufficient solution.

- **Potential closed-loop evaluation**: The training data and two of the four pointwise meta-evaluation benchmarks (VideoJudgeLLaVA-MetaEval and VideoJudgeVCG-MetaEval) are constructed using the same generator-evaluator pipeline. While the paper evaluates on independent benchmarks (VATEX, LongVideoBench, VideoAutoArena) and acknowledges this limitation, the majority of the pointwise evaluation data comes from the pipeline. This could overestimate performance due to distributional alignment with the training process.

### Minor
- **Human evaluation scope is limited**: The human evaluation for pairwise data validation is restricted to 250 examples from the 2-vs-3 rating range only. While agreement is high, broader validation across the full rating spectrum would provide stronger evidence of data quality. The rubric quality human evaluation also uses only 300 pairs per model.

- **Exclusion of several strong baselines**: Several recent video understanding models (VideoLLaMA3-7B, VideoChat-Flash, Keye-VL, SmolVLM2) were excluded because they "failed to follow instructions or produce valid scores." This could introduce selection bias, and a more systematic analysis of why these models failed would be helpful for understanding the difficulty of the evaluation task.

- **Mixed results on some benchmarks**: VideoJudge-3B underperforms the Qwen2.5-VL-3B baseline on VideoJudgeVCG (RMSE 1.59 vs. 1.58, MAE 1.06 vs. 1.12, S 0.59 vs. 0.51, P 0.63 vs. 0.52—actually looking more carefully, VideoJudge-3B has higher RMSE but slightly better correlation). The improvement is not uniform across all settings, which weakens the claim of consistent superiority.

### Trivial
None.

## Nice-to-Haves

- The computational cost of the bootstrapping pipeline (number of generator/evaluator passes, cost of generating dense video descriptions) could be reported to help practitioners assess the practical trade-offs.
- An ablation study varying the quality of the generator model used in bootstrapping would help understand how sensitive the results are to the generator's capability.

## Novel Insights

Beyond the paper's core contributions, the finding that long chain-of-thought reasoning does not improve evaluation performance for video tasks (and that unimodal LLM judges perform strictly worse than MLLM judges) provides a useful empirical observation. This suggests that video understanding evaluation fundamentally requires access to visual inputs rather than textual descriptions, even when detailed descriptions are available. The temperature robustness analysis also offers a practical insight: trained judge models can maintain reliability under stochastic decoding, which is important for real-world deployments where deterministic decoding is not always desirable.

## Suggestions

- The calibration issues and overestimation bias should be addressed more directly, perhaps by incorporating harder negatives or preference-optimization techniques during training, or by designing a calibration-aware loss function.
- The meta-evaluation benchmarks constructed from the pipeline could be more clearly separated from the training distribution, or the paper could rely more heavily on the independent benchmarks for the main claims.

## Score and Decision

Score: 7.0  
Decision: Accept

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>