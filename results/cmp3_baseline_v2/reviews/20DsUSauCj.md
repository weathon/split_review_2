## Summary

This paper introduces *persona vectors*—linear directions in LLM activation space corresponding to personality traits—extracted via an automated pipeline from natural-language trait descriptions. The authors demonstrate four applications: monitoring persona shifts at deployment time and during finetuning, mitigating unwanted traits after finetuning via inference-time steering, preventing drift during finetuning through a novel *preventative steering* method, and screening training data before finetuning to flag samples likely to induce undesirable traits. Experiments across two 7-8B open-source models and three negative traits (evil, sycophancy, hallucination) show strong correlations between activation shifts and behavioral changes, and preventative steering better preserves general capabilities than inference-time interventions.

## Strengths

- **Automated pipeline to persona vectors.** The method requires only a natural-language trait description and a frontier LLM, producing contrastive prompts, evaluation questions, and a rubric automatically. This makes the approach easily extensible to new traits without manual curation.
- **Multiple validated applications.** The paper goes well beyond monitoring and inference-time steering (which are already known) by introducing preventative steering during finetuning and pre-finetuning data screening. Both are novel and practically significant contributions.
- **Preventative steering is convincingly superior.** The case study on fact-acquisition (Section 5.2) is particularly strong: preventative steering suppresses hallucination while largely preserving MMLU and new-fact accuracy, whereas inference-time steering degrades both. This demonstrates real practical value.
- **Strong empirical evidence.** Correlations between finetuning shift along persona vectors and behavioral trait expression are high (r = 0.76–0.97). The projection difference on training data predicts post-finetuning trait expression with equally high correlations (r = 0.88–0.95). The experiments are thorough, covering two models and multiple datasets including emergent-misalignment-like ones.
- **Data screening is a forward-looking contribution.** The ability to predict problematic persona shifts *before training* using only pre-finetuning data analysis could be very impactful for safety, and the projection difference metric is well-motivated.

## Weaknesses

### Major

1. **Reliance on LLM-based evaluations throughout.** The persona vector extraction, trait expression scoring, and many of the validation steps depend on LLM judges (Claude 3.7 Sonnet for generation, GPT-4.1-mini for scoring). While the authors validate agreement with human evaluators (Appendix D), this creates a potential circularity: the same type of model used to extract vectors also evaluates them. The cross-trait and cross-model consistency mitigates this concern somewhat, but the paper would be stronger with more diverse evaluation approaches (e.g., established behavioral benchmarks, human studies beyond correlation checks).

2. **Limited model scale and scope.** All experiments are on two 7-8B open-source chat models. It is unclear whether the findings generalize to larger models (e.g., 70B, 400B) or to proprietary models with different architectures (e.g., mixture-of-experts). Given that persona shifts are known to differ with scale, the claims should be caveated more strongly.

3. **Data screening is correlational, not causal.** The paper shows that the projection difference on training data correlates strongly with post-finetuning trait expression. However, it does *not* demonstrate an end-to-end experiment where filtering data based on this metric actually leads to a safer model. The sample-level separation (Figure 8) is promising but does not show that removing flagged samples improves outcomes. This is a gap between the strong claim in the title (“flagging”) and the evidence provided.

### Minor

- The paper does not explore whether persona vectors transfer across models or need to be re-extracted per model. Given the method is automated, this is not a fatal flaw, but it limits scalability.
- The preventative steering coefficient requires tuning; it is unclear how to set it without access to the target trait evaluation (which may not be available in practice).
- Some of the high cross-trait correlations (e.g., evil and sycophancy shifting together) are acknowledged but not deeply explained. The explanation in Appendix I.2 (correlated underlying vectors and data correlations) is plausible but speculative.

### Trivial

- The list of references in the main text terminates abruptly (“Rest of paper (reference and Appendix) is removed”). This is a parser artifact and not a flaw of the paper.

## Nice-to-Haves

- An end-to-end data filtering experiment: take a real-world dataset, rank samples by projection difference, train models on filtered vs. unfiltered data, and compare trait expression scores and capabilities. This would greatly strengthen the claim about pre-finetuning screening.
- Demonstration on a larger model (e.g., 70B) to test scalability.
- Ablation study on the quality of the LLM-generated artifacts: how sensitive are the persona vectors to the specific frontier LLM used for generating prompts and rubrics?
- Comparison with a wider range of alternative training interventions beyond CAFT and regularization.

## Novel Insights

The paper’s most striking insight is that *training-time steering toward* an undesirable direction can be more effective than *inference-time steering away* from it, because it counters the finetuning objective’s push directly. This inverts the typical intuition about steering direction and is supported by clear empirical evidence. A second valuable insight is that the *difference* in persona vector projection between training responses and the model’s natural responses (rather than the raw projection) is the better predictor of finetuning-induced shifts—this makes intuitive sense because the model only needs to shift when the training data differs from its default behavior.

## Suggestions

1. Add an end-to-end experiment where training data is filtered based on projection difference and the resulting model’s trait expression and capabilities are measured. This would complete the “flagging” application.
2. Discuss the potential for circularity in relying on LLM judges throughout the pipeline and how the validation (human agreement, cross-trait checks) addresses this. Consider adding a short human evaluation on a subset of the main steering experiments.
3. Include a sensitivity analysis for the steering coefficient in preventative steering—how does performance degrade if the coefficient is misspecified by a factor of 2?
4. Clarify in the abstract and introduction that the method has been validated only on 7-8B models, and note that scaling behavior is an open question.

## Score and Decision

**Score:** 7.0  
**Decision:** Accept  

This is a well-executed paper with a clear contribution. The automated pipeline, the demonstration of multiple applications, and the novel preventative steering method all represent solid additions to the literature on representation engineering and AI safety. The major weaknesses (reliance on LLM judges, limited model scale, lack of end-to-end data filtering validation) are real but do not invalidate the paper’s core claims; they primarily point to directions for future work. The paper is clearly written and will be of interest to both researchers and practitioners working on controlling and monitoring LLM behavior.

MY FINAL SCORE: 7.0</score>
MY FINAL DECISION: Accept</decision>