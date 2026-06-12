## Summary

This paper addresses the problem of making chain-of-thought (CoT) reasoning more *monitorable*, focusing on faithfulness (whether the CoT honestly reflects the factors influencing the answer) and conciseness (whether the CoT is short enough to be effectively monitored). The authors show that naive reinforcement learning fails because monitorability signals are sparse under the initial policy, leading to vanishing gradients. They propose a prior-guided distillation framework: use an instruct model to transform raw CoTs into monitorable versions, filter for correctness and monitorability, then supervised fine-tune the base model on these traces. Experiments on MMLU-Pro, GSM8K, and MATH500 with a 1.5B model show improvements in faithfulness (from ~15% to ~25%) and conciseness (e.g., from ~12% to ~97% under a length threshold) while maintaining task accuracy.

## Strengths

- **Clear problem formulation and analysis.** The paper formalizes CoT monitorability as a constrained optimization problem and provides a clean mathematical explanation of why naive RL fails due to sparse gradients (Eq. 4–5). This analysis is insightful and well-motivated.
- **Simple and practical method.** The proposed prior-guided transformation + SFT pipeline is straightforward to implement and leverages existing instruct models, making it accessible.
- **Empirical improvements on both dimensions.** The method yields non-trivial gains in faithfulness (10 percentage points absolute) and dramatic gains in conciseness (e.g., 96.6% of outputs under 950 tokens vs. 11.6% for the base model) with minimal accuracy degradation.

## Weaknesses

### Major

- **Limited evaluation scope and baselines.** Experiments are conducted only on a single small base model (DeepSeek R1 Qwen-1.5B). No comparisons are made to other methods for improving faithfulness or conciseness, such as RL with process rewards, reward shaping, or alternative distillation approaches. The baselines (naive RL, direct/indirect prompting) are weak and do not represent the state of the art.
- **Faithfulness evaluation is fragile.** The faithfulness metric relies on an LLM-as-a-judge to detect hint verbalization, which may inherit subjectivity and bias from the judge model. No human evaluation or multi-judge validation is provided. The absolute faithfulness after training is still only 25%, which is low and raises questions about practical utility.
- **Conciseness results lack clear accuracy reporting.** The paper claims accuracy is maintained (e.g., "~90% relative accuracy") but does not present the actual accuracy numbers for the conciseness experiments in a clear table or figure. The bar charts in Figure 5 show only conciseness percentages, not accuracy. This omission makes it difficult to assess the trade-off.
- **No ablation studies.** The method has several components (prior model choice, filtering criteria, likelihood-based selection). None are ablated. For example, what happens if we train on all prior-generated traces without filtering? How sensitive is performance to the choice of prior model? Without such analysis, the contribution of each design choice is unclear.
- **The "principled" claim is overstated.** The constrained optimization formulation (Eq. 1) is not directly optimized; the actual algorithm is a heuristic distillation pipeline. The Lagrangian analysis is used only to motivate the sparsity problem, not to derive the method. This disconnect weakens the paper's theoretical contribution.

### Minor

- **Arbitrary conciseness thresholds.** The thresholds (125 tokens for GSM8K, 950 for MATH500) are chosen without justification. The results are highly dependent on these thresholds.
- **Small training set.** Only 3,200 examples are used for training. The paper does not study how dataset size affects performance.
- **No statistical significance or variance reported.** All results appear to be single-run point estimates, making it impossible to assess reliability.

## Nice-to-Haves

- Human evaluation of faithfulness to validate the LLM-as-a-judge approach.
- Experiments on larger models (e.g., 7B or 70B) to test scalability.
- Comparison to RL with a dense reward (e.g., process reward model) or to direct prompting baselines that ask the model to be concise/faithful.
- Ablation of the filtering step and the likelihood-based selection in Algorithm 1.

## Novel Insights

The key insight—that monitorable traces are reward-compatible but rarely sampled, so external transformation can provide dense supervision—is useful but not entirely novel. Similar ideas appear in distillation and data augmentation literature. The paper's main contribution is applying this insight to the specific problem of CoT monitorability and providing a clean failure analysis of naive RL.

## Suggestions

1. Include a table with exact accuracy numbers for all conciseness experiments (both base and trained models on GSM8K and MATH500).
2. Add an ablation that trains without the filtering step (i.e., use all prior-generated traces) to isolate the effect of filtering.
3. Compare against a simple baseline that prompts the base model to "think concisely" or "be faithful" without any training.
4. Report standard deviations or confidence intervals for all metrics.

## Score and Decision

**Score:** 4.0

**Decision:** Reject

The paper addresses an important problem and provides a clean analysis of why naive RL fails. However, the evaluation is too limited: only one small model, weak baselines, no ablations, and incomplete reporting of accuracy for the conciseness experiments. The absolute faithfulness improvement is modest (25% after training), and the method's reliance on a strong prior model is not critically examined. While the idea has merit, the current evidence is insufficient to support acceptance at a top venue like ICLR.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>