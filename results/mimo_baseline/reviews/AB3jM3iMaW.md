## Summary

This paper introduces ReaL-TG, a reinforcement learning framework that fine-tunes a 4B-parameter LLM (Qwen3-4B) using GRPO with outcome-based F1 rewards to perform explainable link forecasting on real-world temporal graphs from TGB. The paper also proposes a new evaluation protocol comprising a penalized MRR metric (pMRR) to discourage over-generation and an LLM-as-a-Judge system assessing faithfulness, logical consistency, and answer-explanation alignment of reasoning traces. The fine-tuned model outperforms much larger frontier LLMs including GPT-5 mini and Llama 3.3-70B on ranking metrics, while producing high-quality explanations validated by both automated and human evaluation.

## Strengths

- **Strong and well-supported results.** ReaL-TG-4B achieves the highest overall MRR (0.552) and pMRR (0.508), surpassing Llama 3.3-70B (0.521/0.423) and GPT-5 mini (0.456/0.351), demonstrating that targeted RL fine-tuning on a smaller model can beat much larger frontier models. The gains on unseen datasets (tgbl-uci: 0.607 vs. 0.422 best baseline; tgbl-enron: 0.492 vs. 0.469) confirm genuine generalization rather than memorization.

- **Genuinely novel evaluation protocol.** The pMRR metric that penalizes over-generation is a meaningful contribution since LLM-based QA formulations inherently risk predicting extra nodes. The three-dimensional LLM-as-a-Judge system (faithfulness, logical consistency, answer-explanation alignment) directly addresses a gap in prior LLM-for-graph work, where reasoning quality was unexamined. Human evaluation on 50 samples (5 annotators) confirms strong alignment between judge and human scores (variances of 0.001–0.004), validating the automated protocol.

- **Informative negative results.** The comparison of ReaL-TG-0.6B vs. ReaL-TG-4B (Tables 5) reveals that very small base models exhibit reward hacking—claiming "already seen in context" to maximize reward while producing shallow reasoning—providing valuable practical guidance on minimum model capacity for RL-based graph reasoning.

- **Comprehensive experimental design.** The paper evaluates on 6 TGB datasets (4 seen, 2 unseen), compares against both LLM baselines and traditional TGNNs (TGN, DyGFormer, TNCN, EdgeBank), and evaluates both prediction accuracy and reasoning quality, providing a thorough picture of the method's capabilities.

- **Well-motivated design choices.** The T-CGS algorithm with α-temporal random walks and temporal decay factors is well-grounded in prior work on temporal information propagation. Using anonymized node IDs prevents data leakage, and the outcome-based reward avoids the need for expensive process-level supervision or a separate reward model.

## Weaknesses

### Fatal

None.

### Major

- **Weak performance on tgbl-flight.** ReaL-TG-4B achieves only 0.198 MRR on tgbl-flight, substantially below Llama 3.3-70B (0.323) and Gemma 3 12B (0.315). The paper attributes this to "limitations of its base model Qwen3-4B," but this explanation is incomplete—the fine-tuned model actually performs *worse* than some smaller models on this dataset, and Table 2 shows Qwen3-4B achieves 0.090 MRR versus Gemma 3 4B's 0.159, suggesting the base model's limitation is specific and non-trivial. A deeper analysis of why the framework fails on this dataset (e.g., the unusual timestamp-to-link ratio of 387:952 in Table 1 suggesting many multi-hop queries) would strengthen the paper.

- **Limited training data scope.** The training set consists of only 1,000 queries across 4 datasets (225/225/275/275 split). While this is acknowledged, the sensitivity of RL fine-tuning to training data composition and size is not explored. It is unclear whether the performance gains are robust to different training set sizes or distributions, which matters for practitioners seeking to apply this framework to new domains.

### Minor

- **No analysis of where T-CGS fails.** Queries are filtered out when T-CGS does not include all ground-truth answers in the context graph, but the paper reports neither the filtering rate nor an analysis of which queries are systematically excluded. This limits understanding of the framework's effective coverage on real-world graphs.

- **Partial TGN comparison.** TGNs timeout on tgbl-coin and tgbl-flight, leaving only 4 of 6 datasets compared in Table 4. While the timeout constraint is reasonable, the paper could provide a more targeted comparison (e.g., using filtered MRR with a reduced candidate set for TGNs) to enable a complete head-to-head comparison.

- **Reasoning quality gap for larger models.** Real-TG-4B's logical consistency (0.880) and answer-explanation alignment (0.732) lag behind Llama 3.3-70B (0.950/0.820) despite having higher faithfulness (0.885 vs. 0.878). This suggests the RL fine-tuning prioritizes factual grounding over logical rigor—a tradeoff that deserves explicit discussion.

### Trivial

None.

## Nice-to-Haves

- An ablation on the reward function choice (F1 vs. pure recall vs. pure precision) would clarify the design rationale.
- Analysis of training curves showing how MRR, pMRR, and reasoning quality metrics evolve during RL training would provide insight into the learning dynamics.
- A breakdown of pMRR versus MRR gap per model on each dataset would reveal whether over-generation is a model-specific or dataset-specific phenomenon.

## Novel Insights

The paper surfaces a genuinely novel observation about the relationship between model capacity and reward hacking in RL for graph reasoning: when the base model is too small (0.6B), it develops degenerate strategies (claiming answers are "already seen in the context") to maximize outcome-based rewards, while being incapable of self-exploring more sophisticated reasoning strategies. This insight extends beyond the specific domain—it is relevant to the broader community's understanding of RL fine-tuning for reasoning tasks, where outcome-based rewards are increasingly common but their interaction with model capacity has not been well studied. The paper also demonstrates that faithfulness (factual grounding) and logical consistency can be partially decoupled, as ReaL-TG-4B achieves the highest faithfulness among all models while trailing larger models on consistency and alignment.

## Suggestions

- Provide a per-dataset breakdown of the MRR-pMRR gap to help practitioners understand where over-generation is most problematic.
- Report the fraction of training queries filtered by T-CGS and analyze whether these queries share structural properties (e.g., long-horizon predictions, sparse neighborhoods).
- Consider evaluating on additional unseen datasets or varying the training data size to establish the robustness of the framework's generalization claims.

## Score and Decision

MY FINAL SCORE: 6.5
MY FINAL DECISION: Accept