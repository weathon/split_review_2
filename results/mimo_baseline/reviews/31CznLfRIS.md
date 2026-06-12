## Summary

This paper introduces VideoJudge, a framework that bootstraps training data for MLLM-based evaluators of video understanding tasks through an iterative generator-evaluator pipeline. The approach synthesizes over 100K rated response examples without human annotation, then fine-tunes 3B and 7B Qwen2.5-VL models to serve as pointwise and pairwise judges, also enabling instance-specific rubric generation at inference time. Across multiple meta-evaluation benchmarks, the trained models match or outperform much larger baselines (up to 72B parameters).

## Strengths

- **Important and underexplored problem**: The paper addresses a genuine gap — applying MLLM-as-a-judge to video understanding, where temporal complexity makes evaluation particularly challenging. The lack of human-annotated evaluation resources for video is a real bottleneck.

- **Comprehensive experimental evaluation**: The paper evaluates across four pointwise benchmarks (VideoJudgeLLaVA, VideoJudgeVCG, VATEX, LongVideoBench) and three pairwise benchmarks, against a wide range of baselines from 0.6B to 72B parameters, including both unimodal (Qwen3 with/without thinking mode) and video-language models. This breadth provides useful comparative insights.

- **Practical contribution — rubric generation**: The VideoJudgeR-3B model that generates instance-specific rubrics is an interesting technical contribution. The human evaluation showing it produces rubrics preferred over Qwen-72B (63.9% win rate) and even GPT-4o-mini (53.4%) suggests genuine quality improvements from this approach.

- **Useful ancillary findings**: The paper provides valuable empirical observations: (1) MLLM judges outperform LLM judges on video tasks, (2) chain-of-thought reasoning does not improve judging performance, (3) the model is robust to decoding temperature variation, and (4) the analysis of optimal `maxframes` for training vs. inference provides practical guidance.

- **Resource release**: The paper commits to releasing trained models, bootstrapped datasets, and meta-evaluation benchmarks, which would benefit the community.

## Weaknesses

### Fatal

None.

### Major

- **Closed-loop evaluation risk**: The paper acknowledges (§7) that both training data and several meta-evaluation benchmarks are constructed through the same generator-evaluator pipeline. This creates a fundamental circularity concern: the model is trained on bootstrapped data, then evaluated on benchmarks also bootstrapped with the same pipeline (threshold 0). The paper partially mitigates this by also testing on VATEX (human-annotated) and VideoAutoArena (human preferences), but the strong results on self-constructed benchmarks (e.g., 98.6% on VideoJudge-pairwise) cannot be taken at face value as evidence of quality. The paper would be substantially stronger if more evaluation relied on independently sourced human annotations.

- **Severe overestimation bias**: The error analysis reveals alarming calibration failures: 46.6% of rating-3 responses are incorrectly inflated to 5, and 81.3% of rating-4 responses are incorrectly rated as 5. This means the model essentially collapses the top of the rating scale. This is a significant limitation that undermines the reliability of pointwise scoring, yet it is buried in §6.2 and not adequately discussed in the paper's framing of its contributions. For any downstream application relying on calibrated scores, this would be problematic.

- **Questionable claims of "matching or surpassing" larger models**: On the independent human-annotated benchmarks, the results are more mixed than the abstract suggests. On VideoAutoArena (pairwise, the most independent benchmark), VideoJudge-3B scores 71.76 vs. Qwen2.5-VL-72B's 89.80 — a significant gap. On VATEX, VideoJudge-7B achieves a PSUP of 0.66, while Qwen2.5-VL-32B achieves 0.73. The strong results appear concentrated on bootstrapped benchmarks where the model may benefit from pipeline-specific artifacts. The paper's claims would benefit from more honest framing of where the approach succeeds and where it falls short.

### Minor

- **Limited training analysis**: Training for only 2 epochs on ~103K examples is a rather narrow training regime. No analysis of training curves, overfitting behavior, or sensitivity to data size is provided. Given the bootstrapped nature of the data, understanding how much training data is needed and when diminishing returns occur would be valuable.

- **BERTScore/BLEU as data quality proxies**: The monotonic degradation in Figure 2 is used to validate bootstrapped data quality, but these metrics measure surface-level similarity to the gold response rather than actual quality differences. A response rated 1 could still have high BERTScore with the gold if it contains similar vocabulary but wrong content. VQAScore is mentioned in the appendix but not given equal prominence.

### Trivial

None beyond parser artifacts.

## Nice-to-Haves

- A qualitative analysis comparing VideoJudge's evaluation explanations against human reasoning would strengthen the interpretability claims.
- Evaluation on additional independent benchmarks or a newly collected human-annotated dataset would substantially strengthen the paper.
- Analysis of which video understanding tasks (captioning, QA, temporal reasoning) benefit most or least from the approach.

## Novel Insights

The finding that rubric-guided training dramatically improves robustness to decoding temperature (Figure 4) is a genuinely useful practical observation — the base model's Spearman correlation drops from 0.56 to 0.42 with increasing temperature, while VideoJudge remains stable or improves. This suggests that structured evaluation criteria can serve as an implicit regularizer against stochastic decoding noise, an insight that extends beyond video judging to any setting where evaluator consistency matters. Additionally, the demonstration that instance-specific rubric generation can nearly close the gap between 3B and 72B models is noteworthy and suggests that explicit evaluation criteria matter more than raw model capacity for this task.

## Suggestions

- Re-run evaluations separating bootstrapped benchmarks from independent human-annotated ones, and adjust the claims accordingly. Results on VATEX and VideoAutoArena should be given more prominence.
- Address the overestimation bias more thoroughly — consider techniques like temperature scaling, class-balanced sampling during training, or explicit calibration losses to mitigate this issue.
- Provide confidence intervals or statistical significance tests for the reported results, particularly for pairwise accuracy where the differences are sometimes small.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>