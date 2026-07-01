Now let me write the final consolidated review.

## Summary

VideoJudge proposes a bootstrapping pipeline that generates training data for MLLM-based video evaluators by having a generator produce responses at quality levels 1–5, validating them with an evaluator model, and iteratively refining mismatches. Fine-tuned 3B and 7B judge models (based on Qwen2.5-VL) are evaluated on both pointwise and pairwise video understanding meta-evaluation benchmarks, including two new bootstrapped benchmarks and two existing human-annotated ones. The paper demonstrates that small specialized judges can approach the performance of much larger (32B–72B) general-purpose MLLMs.

## Strengths

1. **The bootstrapping pipeline is a practical and creative solution to data scarcity.** Generating candidate responses at different quality levels, validating them with an evaluator, and refining mismatches is a sensible way to create fine-grained training data without expensive human annotation. The iterative refinement loop addresses the key weakness of purely synthetic data. This idea has potential impact beyond video understanding.

2. **The empirical scope is substantial.** The paper trains and evaluates models at two sizes (3B, 7B), tests both pointwise and pairwise settings, includes rubric generation, studies temperature robustness, frame count sensitivity, and provides error analysis. The breadth of experiments is a genuine strength.

3. **The efficiency result is notable.** Demonstrating that a fine-tuned 3B model can approach the performance of 32B–72B models on several metrics is practically significant for deployment. The pairwise results (e.g., VideoJudge-3B achieving 94.0 on the in-distribution VideoJudge pairwise benchmark) are particularly compelling evidence that the bootstrapping data provides effective supervision.

## Weaknesses

### Fatal

None.

### Major

1. **The strongest quantitative claims rely partly on meta-evaluation benchmarks whose labels come from the same pipeline that produced the training data.** The paper's two main pointwise benchmarks, VideoJudgeLLaVA-MetaEval and VideoJudgeVCG-MetaEval, are constructed by the bootstrapping pipeline with threshold 0 (Section 4.2). The ground-truth ratings in these benchmarks are pipeline labels, not human judgments. When VideoJudge performs well on these benchmarks, it partially reflects that the model has learned to reproduce the preferences of the same generator-evaluator pipeline that produced both its training and evaluation data. The paper acknowledges this "closed-loop" concern in Section 7, but the headline claim that VideoJudge "matches or surpasses much larger models" is substantiated primarily on these two benchmarks. On the two independent human-annotated benchmarks (VateX-Eval, LongVideoBench), the advantage is mixed — for instance, VideoJudge-7B has higher RMSE than Qwen2.5-VL-72B on VateX (1.46 vs. 1.40) and lower PSUP on LongVideoBench (0.66 vs. 0.71). The paper's central claim is not invalidated, but it is overstated relative to the evidence from human-annotated evaluation.

2. **The systematic overestimation bias significantly undermines practical utility as a judge.** Error analysis (Section 6.2) reveals that VideoJudge overestimates scores by ≥2 points in 14.8% of cases but underestimates by the same margin in only 1.5%. Only 36.9% of rating-3 responses receive the correct score, with 46.6% inflated to a perfect 5, and 81.3% of rating-4 responses are incorrectly rated as 5. This means the model has poor discriminative ability in the range that matters most for practical evaluation — distinguishing good responses from excellent ones. The paper acknowledges this as future work but it is a first-order limitation for a paper proposing a judge model. Readers considering using VideoJudge for actual evaluation need to understand that it will systematically inflate scores in the 3–5 range.

### Minor

3. **No uncertainty quantification for comparative results.** All tables (1, 2, 3) report single numbers without standard deviations, confidence intervals, or mention of number of runs. The paper makes comparative claims about small performance differences (e.g., Spearman 0.82 vs. 0.80, RMSE 1.33 vs. 1.40) between VideoJudge models and much larger baselines. Without variance estimates, it is impossible to determine whether these differences are meaningful or within the noise of a single run. This is a significant evidential gap for a paper whose central argument is a comparative one.

4. **The LLM-as-Judge evaluation for rubrics is weakened by circularity.** VideoJudgeR-3B's rubric quality is evaluated using GPT-4o-mini as the judge, yielding a 92.7% win rate against GPT-4o-mini itself (Section 6.1). Using the same model family as both judge and opponent is logically circular and inflates the result. The human evaluation (300 rubric pairs), which shows more modest win rates (53.4% vs. GPT-4o-mini), is more credible, but the paper's presentation emphasizes the 92.7% figure more strongly.

5. **The specific generator (G) and evaluator (E) models used in the bootstrapping pipeline are not stated in the main text.** Section 3.1 refers to "strong vision-language models (§A.2)" but never specifies which models serve as G and E in the main body. The quality and bias of the entire bootstrapping pipeline depend on the capabilities of G and E; the reader cannot fully assess the pipeline's strengths or limitations without this information. (Details presumably exist in the appendix, which was stripped from the submission file available for review.)

### Trivial

None.

## Nice-to-Haves

- A version of Table 1 that visually separates bootstrapped benchmarks from human-annotated ones would help readers assess the evidence more clearly.
- Post-hoc calibration or an analysis of why rating-3 and rating-4 responses are so frequently inflated would strengthen the paper's practical contribution.
- Reporting the failure rates of models excluded from baselines (e.g., VideoLLaMA3-7B, VideoChat-Flash) would provide useful transparency about the difficulty of the task.

## Removed Points

These points from the input review are removed with justification:

- **"The problem is real and well-motivated"** — Generic strength about importance of the problem; removed per filtering rules.
- **"Table 1 is dense and somewhat hard to parse"** — Pure formatting/style nitpick; removed.
- **"BLEU scores of 3.0–11.0 are already very low"** — The paper also reports BERTScore (91.1–86.9), which shows clearer degradation; the BLEU observation does not undercut the data quality validation.
- **"Human evaluation only covers 2 vs. 3 rating region"** — The paper explicitly states this was targeting the hardest cases; this is reasonable methodology, not a weakness.
- **"The paper should report failure rates of excluded models"** — Nice-to-have detail, not a substantive weakness.
- **"The paper does not mention how many runs were averaged"** — Merged into Weakness 3 above (no uncertainty quantification).

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface an unexpected interpretation or synthesis that changes how the paper's contribution should be understood.

## Suggestions

1. Restructure the results presentation to clearly separate results on bootstrapped vs. human-annotated benchmarks, and temper the headline claim to state that VideoJudge is competitive with much larger models on a mix of benchmarks, with strongest gains on pipeline-constructed evaluations.
2. Add variance estimates (e.g., at least 3 runs with standard deviations) for the key comparative results, or clearly state that single runs are reported and acknowledge the limitation.
3. Address the overestimation bias with either post-hoc calibration or a more detailed analysis of its root cause, rather than deferring entirely to future work.
4. State in the main text which specific models serve as G and E in the bootstrapping pipeline, since the entire method's quality depends on this choice.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>