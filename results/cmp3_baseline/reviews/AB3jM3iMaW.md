## Summary
This paper presents **ReaL-TG**, a reinforcement learning (RL) framework that fine-tunes LLMs (using GRPO with an F1-based reward) to perform explainable link forecasting on real-world temporal graphs with anonymized node IDs. The authors also introduce a new evaluation protocol that combines a penalized MRR (pMRR) for prediction accuracy with an LLM-as-a-Judge system that assesses faithfulness, logical consistency, and answer-explanation alignment of reasoning traces. The fine-tuned 4B model (ReaL-TG-4B) outperforms much larger frontier models (e.g., Llama 3.3 70B, GPT-5 mini) on both seen and unseen graphs, and human evaluation confirms high reasoning quality.

## Strengths
1. **Novel framework.** This is the first work to apply RL-based fine-tuning of LLMs specifically for link forecasting on real-world temporal graphs, demonstrating that an outcome-based reward (F1) can guide an LLM to self-explore effective reasoning strategies without explicit process supervision.
2. **Comprehensive evaluation protocol.** The paper goes beyond simple ranking metrics by proposing pMRR to penalize over-generation, and introduces a systematic LLM-as-a-Judge evaluation of reasoning quality (faithfulness, logical consistency, answer-explanation alignment). This is a valuable contribution for the community studying LLM-based graph reasoning.
3. **Strong empirical results.** ReaL-TG-4B consistently outperforms much larger models (including GPT-5 mini and Llama 3.3 70B) on ranking metrics across six datasets, and shows substantial improvements over its base model Qwen3-4B. The framework also enables zero-shot transfer to unseen graphs without retraining.
4. **Rigorous validation.** The authors validate their LLM-as-a-Judge system with human evaluation, showing high agreement and high judgment quality. The human evaluation of ReaL-TG-4B’s reasoning traces also confirms the effectiveness of the fine-tuning approach.

## Weaknesses
### Fatal
None.

### Major
None.

### Minor
1. **Training data size and filtering.** The training set consists of only 1,000 queries (with additional filtering to ensure context graphs contain all ground-truth answers and are not too large). This filtering may introduce a selection bias, as queries with answers outside the selected subgraph or with very large context graphs are excluded. While understandable for computational reasons, the impact on generalization to more diverse or denser graphs is not thoroughly discussed.
2. **T-CGS hyperparameter sensitivity.** The Temporal Context Graph Selection relies on hyperparameters α, β, and the number of selected nodes (set to 100). The paper provides values but no ablation study on how different choices affect downstream performance. Sensitivity to these parameters could affect reproducibility in other settings.
3. **Reasoning quality still behind larger models.** Despite strong ranking performance, ReaL-TG-4B still lags behind Llama 3.3 70B in logical consistency and answer-explanation alignment (Table 3). The attribution to base model size is plausible, but the paper does not explore whether further RL training or different reward designs could bridge this gap.

### Trivial
- Some figures (e.g., Figure 2) contain redundant text descriptions that could be simplified.
- The paper uses “Real-TG” and “ReaL-TG” interchangeably; consistency would help.

## Nice-to-Haves
- An ablation study on the T-CGS hyperparameters (α, β, number of selected nodes) would strengthen the understanding of the algorithm’s robustness.
- Exploring the effect of different reward functions (e.g., MRR-based reward instead of F1) could provide insight into the trade-offs between ranking accuracy and explanation quality.
- Applying the framework to a larger base model (e.g., Qwen3-8B) would be a natural next step and could further validate the approach.

## Novel Insights
Beyond the paper’s own contributions, this work shows that outcome-based RL with a simple F1 reward can effectively teach an LLM to reason about temporal graph structure without any process-level supervision or graph-specific architectural modifications. The success on unseen graphs suggests that the LLM learns transferable reasoning strategies (e.g., focusing on recent, multiple-hop interactions) rather than memorizing patterns from training graphs. The paper also demonstrates that pMRR is a more informative metric than standard MRR when evaluating LLM-based link forecasting, because it captures the risk of over-generation inherent in generative models.

## Suggestions
- Provide an ablation study on the T-CGS parameters (α, β, number of selected nodes) to help practitioners adapt the method to different temporal graphs.
- Discuss the limitations of the filtering step in training data collection more explicitly, and consider evaluating on unfiltered queries to measure the framework’s robustness to missing context or very large histories.
- Consider reporting confidence intervals or variance across random seeds for the main results to strengthen reproducibility claims.

## Score and Decision
MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>