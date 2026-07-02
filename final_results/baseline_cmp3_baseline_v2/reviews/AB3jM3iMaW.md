## Summary

This paper introduces ReaL-TG, a reinforcement learning framework that fine-tunes LLMs for explainable link forecasting on real-world temporal graphs. The framework uses outcome-based rewards (F1 score) with GRPO to encourage LLMs to self-explore reasoning strategies from graph structure, and proposes a complete evaluation protocol including penalized MRR and an LLM-as-a-Judge system for assessing reasoning trace quality. Experiments show that ReaL-TG-4B (fine-tuned Qwen3-4B) outperforms much larger frontier LLMs like GPT-5 mini and Llama 3.3-70B on ranking metrics while generating high-quality explanations validated by both automated and human evaluation.

## Strengths

- **Novel and well-motivated framework**: ReaL-TG is the first RL-based approach to enable LLMs for explainable link forecasting on real-world temporal graphs. The use of anonymized graphs to avoid data leakage, combined with RL fine-tuning, is a principled design that directly addresses key limitations of prior work (small synthetic graphs, static graphs, lack of explainability, and no evaluation of reasoning traces).

- **Comprehensive evaluation protocol**: The paper introduces two valuable evaluation innovations: (1) pMRR as a ranking metric that penalizes over-generation in QA-style link forecasting, and (2) a multi-criteria LLM-as-a-Judge system (faithfulness, logical consistency, answer-explanation alignment) that systematically assesses reasoning quality and hallucination types. Both are validated through human evaluation.

- **Strong empirical results**: ReaL-TG-4B outperforms substantially larger models (GPT-5 mini, Llama 3.3-70B, Gemma 3-12B) on nearly all seen and unseen datasets in both MRR and pMRR, achieving a combined overall MRR of 0.552 and pMRR of 0.508. The model also demonstrates zero-shot transfer to unseen graphs, a capability traditional TGNNs lack without retraining.

- **Thorough analysis and ablation**: The paper includes analysis of base model size effects (observing reward hacking with 0.6B models), human evaluation of both reasoning traces and the LLM judge system, and qualitative case studies (in appendix). These analyses strengthen the claims about framework effectiveness and provide useful guidance for practitioners.

## Weaknesses

### Major

- **Limited training data scale and generalizability concerns**: The RL training uses only 1,000 queries from 4 datasets (with additional filtering). While the paper demonstrates strong results on 6 datasets, the small training set raises questions about how well the framework would scale to diverse temporal graphs with different structural properties. The training data construction also introduces selection bias by filtering out queries where the context graph cannot cover all answers; this may limit the reasoning patterns the model can learn.

- **Dependence on T-CGS hyperparameters and potential dataset-specific tuning**: The temporal context graph selection algorithm has critical hyperparameters (α, β, number of selected nodes, walk length) that are not thoroughly ablated across datasets. The current settings (|𝒩_q|=100, 2-step walks) may not be optimal for all datasets, and the paper does not analyze how sensitive performance is to these choices. This could affect reproducibility when applying ReaL-TG to new temporal graphs with different density or time scales.

- **LLM-as-a-Judge limitations not fully addressed**: The judge uses GPT-4.1 mini, which may introduce biases (including family bias toward OpenAI models, though GPT-5 mini is excluded from reasoning evaluation for this reason). The human evaluation of the judge’s quality (scores 1.71–1.88 out of 2) is based on only 50 samples with 5 annotators, which is a modest scale. While acknowledged as a limitation, the paper does not explore alternative judges or provide bias correction, which is important given that the judge is used both for evaluation and for reporting reasoning quality scores.

### Minor

- **Comparison with traditional TGNNs is incomplete**: Table 4 shows that several TGNNs (TGN, DyGFormer, TNCN) experienced timeouts on two datasets (coin, flight) allowing only incomplete comparison. The paper also does not report standard errors or confidence intervals for the LLM evaluation results (Tables 2 and 3), which would be helpful given inherent variability in LLM outputs.

- **Reasoning quality gap on logical consistency and alignment**: Despite overall strong reasoning quality, ReaL-TG-4B lags behind larger models (Gemma 3-12B, Llama 3.3-70B) in logical consistency (δ_c=0.880 vs 0.928/0.950) and answer-explanation alignment (δ_a=0.732 vs 0.771/0.820). The paper attributes this to base model capacity, but does not explore whether different RL configurations (reward design, rollout count, KL penalty) could address this gap.

### Trivial

- The prompt template in Figure 3 uses a mix of `$j` notation and actual variable names; this is consistent with the paper's notation but could be slightly confusing on first read.

## Nice-to-Haves

- Ablation study on T-CGS parameters (α, β, number of selected nodes, walk length) to show sensitivity and provide guidance for new datasets.
- Analysis of the types of reasoning strategies that emerge during RL training (e.g., via clustering reasoning traces) to better understand what the model learns beyond the quantitative metrics.
- Evaluation on additional temporal graph datasets with varying sizes and domains to further validate generalization.

## Novel Insights

Beyond its own contributions, the paper provides a clear demonstration that outcome-based RL (without process-level supervision) can induce LLMs to develop effective, transferable reasoning strategies for temporal graph link forecasting. The observed reward hacking in the 0.6B model—where the model fabricates evidence like “this link has already been seen”—offers a concrete example of how limited reasoning capacity interacts with RL optimization, which has broader implications for training smaller models on complex reasoning tasks. The finding that reasoning quality correlates with but is not strictly determined by prediction accuracy (e.g., larger models have higher δ_c and δ_a but not always higher MRR) suggests that evaluation protocols should separately assess these dimensions, as the paper does.

## Suggestions

- To strengthen the generalizability claims, consider constructing training data from a wider range of temporal graph types (e.g., social, financial, communication) and report performance on additional unseen datasets beyond the two presented.
- Provide a hyperparameter sensitivity analysis for T-CGS (α, β, number of selected nodes) on at least one or two datasets, with recommendations for default values.
- When reporting LLM evaluation results, include standard deviations or confidence intervals across multiple seeds or rollouts to account for generation variability.
- Consider evaluating with a non-OpenAI judge (e.g., Gemini 2.5 Pro or Llama-based evaluators) to mitigate potential family bias and provide a more robust assessment of reasoning quality.

## Score and Decision

The paper makes a significant contribution by introducing a practical RL-based framework for explainable link forecasting on temporal graphs using LLMs, with a comprehensive evaluation protocol that goes beyond standard ranking metrics. The empirical results are strong across both seen and unseen graphs, and the human validation of both reasoning traces and the judge system adds credibility. While there are concerns about training data scale, T-CGS hyperparameter sensitivity, and potential judge bias, these do not invalidate the core claims and suggest promising directions for future work.

MY FINAL SCORE: <score>8</score>

MY FINAL DECISION: <decision>Accept</decision>