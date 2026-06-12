## Summary
This paper addresses the problem of making Chain-of-Thought (CoT) reasoning traces more monitorable by improving two properties: faithfulness (the CoT honestly reflects what influenced the answer) and conciseness (the CoT is short enough to be practically monitored). The authors formulate this as a constrained optimization problem, demonstrate that naive RL fine-tuning fails due to vanishing gradients from sparse monitorability signals, and propose a prior-guided distillation pipeline where a stronger instruct model transforms base model CoTs into monitorable versions, which are then used for supervised fine-tuning.

## Strengths
- **Well-motivated problem formulation.** The constrained optimization framing of Eq. 1 is clean and principled, and the analysis of why naive RL fails (Eq. 4-5, showing that f(z) ≈ 0 under π₀ causes gradient collapse in L₁) provides genuine insight into the optimization landscape. This is a useful theoretical contribution that explains a practical failure mode.
- **Strong proof-of-concept validation.** Figure 3 convincingly demonstrates that the base model *can* produce correct answers when conditioned on monitorable traces (85% faithfulness, 96.6% conciseness), establishing that the bottleneck is sampling probability rather than inherent capability. This is a well-designed diagnostic experiment.
- **Substantial conciseness gains.** The conciseness results are impressive: on MATH500, the fraction of responses under 950 tokens jumps from 11.6% to 96.6%, and on GSM8K from 24.1% to 80%, with the entire length distribution shifting left (Figure 6). This demonstrates that much verbose CoT reasoning is genuinely redundant.
- **Comparison against prompting baselines.** Figure 4 shows that direct and indirect prompting fail to improve faithfulness, strengthening the case that training-based intervention is necessary.

## Weaknesses
### Fatal
None.

### Major
- **Large gap between proof-of-concept and trained model.** The prior-guided transformation achieves 85% faithfulness and 96.6% conciseness (Figure 3), but the actual SFT-trained model achieves only 25% faithfulness and 80% conciseness on GSM8K. This 60-point gap in faithfulness suggests the distillation process loses substantial quality, and the paper does not analyze or address this discrepancy. This undermines confidence that the method is working as intended.
- **Very limited experimental scope.** All experiments use a single base model (DeepSeek R1 Qwen-1.5B) and a single prior model (Qwen 2.5-7B Instruct). The 1.5B parameter scale is quite small, and it is unclear whether the findings (especially the sparsity of f(z) and the effectiveness of distillation) transfer to larger, more capable reasoning models where the problem may manifest differently.
- **No comparison against alternative training methods.** The paper compares against naive RL and prompting but does not compare against other plausible approaches such as process reward models, reward shaping with intermediate step feedback, rejection sampling, or other distillation baselines. This makes it difficult to assess whether the prior-guided approach is the right solution or simply *a* solution.
- **Narrow faithfulness evaluation.** Faithfulness is measured solely through hint-verbalization on MMLU-Pro with injected hints. This is a specific and somewhat artificial setup. The paper does not evaluate faithfulness in other contexts (e.g., does the model verbalize when it uses world knowledge shortcuts, or when it makes implicit assumptions?), limiting the generalizability of the faithfulness claims.

### Minor
- **Accuracy drops are under-discussed.** The paper claims accuracy is "essentially unchanged" but the conciseness results show ~10% relative accuracy drops (e.g., 83.6% → ~75% on MATH500 based on "approximately 90% relative accuracy"). For a method that explicitly constrains against accuracy degradation (Eq. 1), this deserves more careful analysis.
- **The mathematical analysis, while correct, is relatively straightforward.** The observation that f(z) ≈ 0 leads to vanishing gradients is a standard exploration-exploitation issue. The paper could strengthen this by connecting to the broader literature on sparse-reward RL and exploration strategies.
- **LLM-as-judge for faithfulness.** The paper acknowledges this limitation but the lack of inter-annotator agreement or human validation data makes the faithfulness numbers hard to trust at face value.

### Trivial
- Some figure/table duplication (Figure 1 caption appears twice, Figure 3 data appears in both chart and table form).

## Nice-to-Haves
- Experiments on larger models (7B, 14B) to assess scalability
- Analysis of *why* the distillation gap (85% → 25% faithfulness) is so large — is it a capacity issue, a data quality issue, or an SFT optimization issue?
- Evaluation of faithfulness beyond hint injection (e.g., on tasks where the model might use heuristics or shortcuts)
- Comparison with process reward model approaches or rejection sampling as alternative baselines

## Novel Insights
The paper's most novel insight is the diagnostic analysis showing that the base model *can* produce correct answers under monitorable traces but simply doesn't generate them (Figure 3), combined with the gradient analysis explaining why standard RL cannot fix this. This reframes the problem from "models can't reason monitorably" to "models rarely sample monitorable reasoning," which is a useful conceptual distinction that could guide future work on CoT quality.

## Suggestions
- Investigate and address the large distillation gap between the proof-of-concept and trained model results — this is the most important open question from the paper.
- Expand experiments to at least one additional base model at a larger scale to establish generalizability.
- Add at least one alternative training baseline (e.g., rejection sampling with the same prior, or a process reward model) to contextualize the approach.
- Provide a more honest accounting of accuracy changes, including per-benchmark breakdowns rather than aggregate "approximately 90% relative accuracy."

## Score and Decision
The paper tackles an important and timely problem with a principled formulation and a reasonable approach. The conciseness results are strong, and the analysis of why naive RL fails is a useful contribution. However, the large gap between the proof-of-concept and actual trained model results, the very limited experimental scope (single small model), and the lack of comparison against alternative training methods weaken the paper's claims. The faithfulness improvements, while statistically meaningful, are modest in absolute terms (15% → 25%). This is a solid exploratory paper that opens interesting directions but needs broader validation to be fully convincing.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: Reject