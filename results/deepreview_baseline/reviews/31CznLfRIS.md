## Summary

This paper introduces VideoJudge, a bootstrapping framework for training MLLM-based evaluators specialized for video understanding tasks. The approach uses an iterative generator-evaluator pipeline that synthesizes training data with quality control, creating over 100,000 training examples without human annotation, and fine-tunes judge models that can generate both ratings and instance-specific rubrics at test time. The trained 3B and 7B VideoJudge models match or outperform much larger baselines (up to 10× larger) across multiple meta-evaluation benchmarks, demonstrating that bootstrapped supervision can enable smaller models to achieve competitive judgment reliability.

## Strengths

- **Novel and practical framework**: The bootstrapping methodology that generates training data through a generator-evaluator pipeline with iterative refinement is a clever approach to addressing the scarcity of human-annotated evaluation data for video understanding. This is a genuine methodological contribution that could extend beyond video.

- **Strong empirical results**: VideoJudge-3B and VideoJudge-7B consistently match or outperform much larger models (Qwen2.5-VL-32B/72B) across multiple benchmarks, including pointwise (Table 1), pairwise (Table 3), and rubric generation (Table 2). For instance, VideoJudge-7B achieves 98.6 accuracy on VJ pairwise compared to 93.2 for Qwen2.5-VL-72B.

- **Comprehensive evaluation suite**: The paper evaluates on multiple meta-evaluation benchmarks (VideoJudgeLLaVA, VideoJudgeVCG, VATEX, LongVideoBench, VideoAutoArena) and includes human evaluation, providing thorough validation. The analysis of temperature robustness and frame count effects adds practical value.

- **Rubric generation capability**: Training models to generate instance-specific rubrics at test time is a valuable contribution that improves interpretability. VideoJudgeR-3B produces rubrics preferred over those from GPT-4o-mini (53.4% win rate) and Qwen-72B (63.9%) in human evaluation.

## Weaknesses

### Major

- **Closed-loop evaluation concern**: The training data and a portion of the meta-evaluation benchmarks (VideoJudgeLLaVA-MetaEval and VideoJudgeVCG-MetaEval) are both constructed using the same generator-evaluator pipeline. While the authors acknowledge this limitation and evaluate on independent benchmarks (VATEX, LongVideoBench, VideoAutoArena), the strongest results in Table 1 (Spearman 0.82 for VideoJudge-3B on VideoJudgeLLaVA) are on benchmarks constructed through the same pipeline. The performance gap between VideoJudge-3B and stronger baselines narrows considerably on independent benchmarks (e.g., VATEX PSUP: 0.61 vs 0.73 for Qwen2.5-VL-32B).

- **Limited novelty relative to existing self-play/self-refinement methods**: Bootstrapping from a generator-evaluator loop bears strong resemblance to established techniques in LLM self-improvement (self-verification, constitutional AI, SPIN, self-rewarding). The paper claims "the first bootstrapped framework for training scalable MLLM-based evaluators" but does not thoroughly differentiate from prior work like Lee et al. (2024a) which already explored fine-tuning open-weight MLLMs as judges. The methodological novelty is incremental rather than foundational.

- **Data quality concerns from the bootstrapping process**: The human evaluation reveals that even after bootstrapping, generator-evaluator disagreements are most frequent around ratings 2 and 3, and only 94.8% annotator agreement on these pairs. The error analysis shows severe overestimation bias: 81.3% of rating-4 responses are incorrectly rated as 5, and only 36.9% of rating-3 responses get the correct score. These calibration issues suggest the bootstrapped data has systematic quality problems that the pipeline does not fully resolve.

- **Inconsistent baseline comparisons**: The paper excludes several models (VideoLLaMA3-7B, VideoChat-Flash, Keye-VL, SmolVLM2) because they "failed to follow instructions or produce valid scores." This selective exclusion could favor the proposed method. Additionally, the baselines do not include other fine-tuned judge models (e.g., Lee et al. 2024a style models) which would be a more direct comparison.

### Minor

- **Computational cost of the bootstrapping pipeline is unclear**: The pipeline requires a generator model, an evaluator model, and multiple refinement iterations for each of 25K seed examples to create 20,765 video-instruction pairs. The total compute cost is not reported, making it difficult to assess the efficiency claims.

- **The ablation study on feedback is incomplete**: While Table 3 shows w/ FB vs w/o FB results, the paper does not ablate the refinement iterations themselves (e.g., how many iterations are needed, whether more iterations improve quality). The acceptance criterion threshold α is also not analyzed.

## Nice-to-Haves

- The paper would benefit from a more thorough comparison with existing fine-tuned judge models in the vision-language domain, not just zero-shot baselines.
- Analysis of failure cases where VideoJudge performs worse than baselines (beyond the overestimation bias already reported) would help characterize limitations.
- Discussion of the computational cost of the full bootstrapping pipeline vs. the cost of human annotation would strengthen the scalability argument.

## Novel Insights

The most interesting finding is that instance-specific rubric generation enables a compact 3B model to produce rubrics preferred over those from GPT-4o-mini and Qwen-72B, while simultaneously improving evaluation performance. This suggests that training for structured evaluation criteria (rubric generation + reasoning + scoring) provides a stronger learning signal than training for scoring alone, even with limited data (10% of the pointwise data). The finding that LLM judges without video input perform worse than MLLM judges provides empirical evidence that video information is necessary for accurate video understanding evaluation, which has practical implications for benchmark design.

## Suggestions

1. Conduct a proper human evaluation on the final benchmark responses (not just the bootstrapped training data) to validate that VideoJudge's ratings align with human judgments on independently collected video-instruction pairs, rather than relying primarily on pipeline-constructed meta-evaluation sets.

2. Compare against other fine-tuned MLLM judge models under comparable settings, such as models trained using the approach from Lee et al. (2024a) or Chen et al. (2024b), to establish the relative advantage of the bootstrapping pipeline over simpler fine-tuning approaches.

3. Report the number of refinement iterations required and analyze whether the acceptance criterion α (currently unspecified) affects downstream performance, as this would inform practical application of the method.

## Score and Decision

The paper makes a solid contribution with a practical bootstrapping framework for training video evaluators, strong empirical results demonstrating that small models can match much larger ones, and a useful rubric generation capability. However, the closed-loop evaluation design, the limited novelty relative to existing self-improvement methods, and the significant calibration issues in the bootstrapped data temper the contribution. The paper is above the acceptance threshold for ICLR but does not reach the level of a strong accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>