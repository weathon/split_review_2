## Summary

This paper presents the first systematic study of prompt optimization for Large Reasoning Models (LRMs), using end-to-end event extraction (EE) as a case study. The authors compare two LRMs (DeepSeek-R1, OpenAI o1) and two general-purpose LLMs (GPT-4o, GPT-4.5) as both task models and prompt optimizers within a Monte Carlo Tree Search framework. They find that LRMs benefit more from prompt optimization than LLMs, serve as more effective optimizers, produce higher-quality and more concise prompts, converge faster, and generalize to other tasks (Geometric Shapes, NCBI Disease NER).

## Strengths

- **First systematic investigation of prompt optimization for LRMs.** The paper addresses a timely and practically important question—whether the strong reasoning capabilities of LRMs eliminate the need for prompt engineering—and provides clear, evidence-based answers. This fills a genuine gap in the literature.
- **Comprehensive and well-designed experimental setup.** The authors evaluate four models in both roles (task model and optimizer) across low-resource and medium-resource settings, at shallow and full MCTS depths, and report results on development and test sets. The cross-model optimization grid (each task model paired with each optimizer) is thorough and revealing.
- **Rich qualitative and quantitative analysis.** Beyond raw scores, the paper provides an error categorization (Fig. 5c), survival analysis of prompt quality (Fig. 5a), prompt length analysis (Fig. 5b), and concrete examples of optimized prompts (Table 2). These analyses give real insight into *why* LRM-optimized prompts are more effective.
- **Generalization to diverse tasks.** The inclusion of symbolic reasoning and biomedical NER shows that the findings are not an artifact of the event extraction task, strengthening the paper’s broader claim about LRMs and prompt optimization.
- **Clear, actionable insights.** The five research questions are answered with explicit insights, and the conclusions are well supported by the data.

## Weaknesses

### Fatal
None.

### Major
1. **Downsampled event types limit ecological validity.** The experiments use only 10 out of 33 ACE05 event types due to prompt length constraints. The paper acknowledges this as a limitation but does not discuss whether the conclusions would hold for the full set. Since event extraction is the primary case study, this reduces confidence in the paper’s central claim that “LRMs benefit substantially from prompt optimization” for EE as actually practiced. A sensitivity analysis or even a small-scale verification on the full set would substantially strengthen the work.
2. **Quantization of DeepSeek-R1 introduces an uncontrolled confound.** The authors deployed DeepSeek-R1 locally at 2.5-bit quantization using the UnSloth framework. While they cite evidence that reasoning tasks degrade minimally, the comparison with o1 and GPT-4.5 (both presumably run at full precision) is not apples-to-apples. Any performance advantage or disadvantage of DeepSeek-R1 could be partially explained by quantization. The paper should either benchmark the quantized version against a full-precision run on a smaller set, or explicitly discuss the potential impact.

### Minor
1. **Diminishing returns of full MCTS are not deeply analyzed.** The paper notes that depth-5 gains are incremental over depth-1 (Insight 2), but does not explore *why*. Understanding when deeper search is warranted (e.g., based on task complexity, data size, or model properties) would strengthen the practical contribution. As it stands, the results suggest depth-1 might suffice, which undercuts some of the motivation for the full MCTS framework.
2. **Absolute AC F1 scores are low across all settings.** Even after optimization, the best AC F1 on the test set is 43.75 (DeepSeek-R1). This is likely due to the difficulty of the task and the zero-shot setup, but it raises the question of whether the prompt optimization gains are practically significant. The paper should contextualize these numbers against supervised state-of-the-art performance or human performance to calibrate the reader’s expectations.

### Trivial
None.

## Nice-to-Haves
- A cost analysis (token usage, API calls, wall time) comparing LRM vs LLM optimizers, since LRMs are computationally expensive but the paper shows they converge faster.
- An ablation controlling for the effect of batch prompting, since the authors note it improved performance compared to single-query inference.
- Experiments on the full 33-event ACE05 set, possibly using a truncation strategy or longer-context models, to confirm that prompt length remains the only obstacle.

## Novel Insights

Beyond the paper’s own contributions, the most striking observation is the qualitative difference in how LRMs and LLMs rewrite prompts: LRMs (especially DeepSeek-R1) generate highly specific, rule-based instructions with concrete span normalization rules and exception handling, while LLMs tend to focus on output format and generic task descriptions. This suggests that the *nature* of optimization credit in LRMs comes from distilling implicit annotation heuristics into explicit extraction rules, rather than from better formatting or exemplar selection. The survival analysis further shows that LRM optimizers not only produce higher peak performance but also a greater density of usable prompts, indicating that their search in prompt space is more targeted and less noisy.

## Suggestions
- Quantify the impact of quantization by running DeepSeek-R1 at a higher precision (e.g., 4-bit or 8-bit) on the ACE_low setting and reporting whether the ranking of optimizers changes.
- Conduct a small experiment on the full 33-event ACE05 set with a length-aware prompt selection strategy (e.g., only optimizing event types that appear in the error batch) to test whether the 10-event results generalize.
- Include a discussion of the computational cost of the different optimizers, such as average optimization time per MCTS node, to help practitioners choose between an LRM and an LLM optimizer.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>