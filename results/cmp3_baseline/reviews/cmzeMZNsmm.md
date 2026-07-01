## Summary

This paper presents the first systematic study of prompt optimization applied to Large Reasoning Models (LRMs), using event extraction as a case study. Through a Monte Carlo Tree Search framework, the authors compare LRMs (DeepSeek-R1, o1) and LLMs (GPT-4o, GPT-4.5) as both task models and prompt optimizers, finding that LRMs benefit more from prompt optimization and are themselves more effective optimizers that produce higher-quality prompts with faster convergence. The findings are extended to symbolic reasoning and biomedical NER tasks.

## Strengths

- **First systematic investigation of prompt optimization for LRMs.** The paper fills a timely gap by examining whether the advanced reasoning capabilities of models like DeepSeek-R1 and o1 eliminate the need for prompt engineering. This is a practically relevant and well-motivated research question.
- **Comprehensive experimental design.** The study varies both the task model and optimizer model across multiple settings (low-resource and medium-scale training, shallow and full MCTS depth), and tests generalization to two additional tasks. The inclusion of both LRMs and LLMs enables clear comparative analysis.
- **Detailed qualitative and quantitative analysis of optimized prompts.** The paper goes beyond aggregate scores to examine prompt content (Table 2), convergence behavior (Figure 4), survival rates (Figure 5a), and prompt length vs. performance (Figure 5b). The error analysis (Figure 5c) provides actionable insights about which mistakes different optimizers reduce.
- **Clear, well-formulated research questions** that guide the experiments and help the reader digest the large set of results.

## Weaknesses

### Major

1. **Low absolute performance raises questions about practical significance.** Even after optimization, the best AC F1 score on ACE05 is ~44% (DeepSeek-R1, dev set). The zero-shot baselines are extremely low (13–16%). Without comparison to even simple supervised baselines or few-shot in-context learning with strong prompts, it is unclear whether the observed improvements represent meaningful progress or merely moving from very poor to still poor performance. The paper would be much stronger with a reference point.

2. **Quantization of DeepSeek-R1 to 2.5 bits is a serious confound.** The authors acknowledge this limitation but rely on a blog post (UnSloth) to claim “minimal degradation in reasoning tasks.” This is not a peer-reviewed benchmark, and quantization can unpredictably affect structured outputs like event extraction. The fairness of comparing quantized DeepSeek-R1 against full-precision GPT-4o/o1 is questionable, and it undermines claims about LRMs outperforming LLMs.

3. **Downsampled event set (10 of 33 types) and small training sets limit task representativeness.** The paper acknowledges this as a compromise due to prompt length constraints. However, it severely restricts the scope of the “event extraction” case study. The complexity of full ACE05 with 33 event types may yield different conclusions, especially regarding the scalability of prompt optimization and the handling of long contexts.

4. **No comparison to alternative prompt optimization methods.** The paper uses a single MCTS framework derived from PromptAgent. It does not compare to other established methods such as APE, OPRO, PromptBreeder, or simple iterative refinement. Without this, it is difficult to determine whether the observed patterns are specific to the chosen framework or general.

### Minor

- The paper mentions that “batch prompting” yields performance gains over single-question prompting but does not ablate this effect separately from optimization. This could be a confounding factor.
- The survival plot (Figure 5a) is based on a relatively small set of prompts from MCTS trajectories; the statistical reliability of the curves is not discussed.
- The error analysis (Figure 5c) provides only qualitative pie charts without quantitative counts or statistical tests across models.

### Trivial

- None notable.

## Nice-to-Haves

- A comparison to fully supervised fine-tuned models or few-shot in-context learning (e.g., selecting the best few-shot examples via optimization) would greatly help contextualize the absolute performance levels.
- An ablation experiment testing the quantized DeepSeek-R1 against a non-quantized version on a small subset, or against a smaller non-quantized LRM, would address the quantization concern.
- Testing on the full 33-event ACE05 set (even with a modified prompt strategy) would strengthen generalizability claims.

## Novel Insights

The paper demonstrates that LRMs are not immune to prompt optimization; they actually benefit more than LLMs from structured feedback and iterative refinement. More importantly, when used as optimizers, LRMs produce prompts that emphasize actionable extraction rules and exception handling rather than generic formatting instructions, and they show faster convergence and lower variance. This suggests that the reasoning capabilities of LRMs make them particularly well-suited for generating precise, informative task descriptions. However, the practical impact is tempered by the fact that even these optimized prompts yield low absolute performance on the event extraction task.

## Suggestions

- Add a baseline comparison: report performance of a standard fine-tuned model on the same downsampled event set (e.g., a BERT-based EE model) and a few-shot prompt without optimization. This will clarify whether prompt optimization for LRMs is a practical approach or merely a marginal improvement over a weak baseline.
- Validate the quantization assumption by running an experiment on a non-quantized DeepSeek-R1 (or a smaller non-quantized LRM) on a subset of the data. If that is not possible, soften the claims about LRM superiority and discuss how quantization might bias results.
- Show that the findings hold for more than two additional tasks by including at least one more diverse task (e.g., a classification task with clear schema) to strengthen the “generalization” claim.

## Score and Decision

Score: 4.5

Decision: Reject

The paper addresses a timely research question and provides a systematic, well-structured study. However, the combination of low absolute performance, a confounded quantization setup, a limited event set, and lack of comparisons to other optimization methods or baselines prevents the results from being sufficiently robust or impactful to warrant acceptance. The contributions are valuable as a first exploration but require stronger experimental validation and broader scope to meet the bar for ICLR.

MY FINAL SCORE: 4.5
MY FINAL DECISION: Reject