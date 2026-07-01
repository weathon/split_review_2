## Summary

This paper proposes Guided Hybrid Policy Optimization (GHPO), a reinforcement learning framework for fine-tuning LLMs on reasoning tasks. GHPO addresses the reward sparsity problem caused by a mismatch between task difficulty and model capability by dynamically detecting when a model fails on a problem (all sampled responses are incorrect) and adaptively injecting partial ground-truth solution traces into the prompt to guide learning. The framework switches between standard on-policy RL for manageable problems and guided imitation learning for difficult ones, achieving approximately 5% average improvement across six math benchmarks compared to GRPO baselines.

## Strengths

- **Well-motivated problem identification**: The paper clearly identifies and empirically validates (52% failure rate on NuminaMath-1.5) the capacity-difficulty mismatch and resulting reward sparsity as a critical bottleneck in RLVR training, particularly for smaller models.
- **Practical and computationally efficient solution**: Unlike methods requiring auxiliary LLMs or value models, GHPO leverages the existing reward signal (group reward analysis) for difficulty detection and uses readily available ground-truth solution traces, making it lightweight and easy to implement.
- **Consistent empirical gains**: The method shows improvements across multiple benchmarks (Math-500, AMC23, GPQA-Diamond, Minerva Math, OlympiadBench) and generalizes to a stronger base model (Qwen2.5-Math-7B), with the largest gains on the hardest problems (e.g., AIME24: 0.122→0.163, GPQA-Diamond: 0.308→0.394).
- **Informative training dynamics analysis**: Figure 4 provides valuable insight into why GHPO works—showing higher accuracy rewards, longer reasoning chains, and critically, smaller and more stable gradient norms compared to GRPO, indicating smoother optimization.

## Weaknesses

### Major

- **Insufficient comparison with state-of-the-art methods**: The paper compares GHPO primarily against vanilla GRPO and a simple curriculum learning baseline. It does not compare against DAPO (Yu et al., 2025), which is explicitly cited as addressing the same reward sparsity issue through dynamic sampling, nor against LUFFY (Yan et al., 2025), which also balances imitation and exploration. Without these comparisons, it is unclear whether GHPO offers advantages over existing approaches that tackle the same problem.
- **Limited evaluation scope**: All experiments are conducted on 7B-parameter models from a single model family (Qwen2.5). The paper claims GHPO is particularly beneficial for "compact, on-device models," yet provides no experiments on smaller models (e.g., 1.5B, 3B) where the capacity-difficulty mismatch would be even more severe. Additionally, only math reasoning is evaluated; the method's generality to other domains (e.g., code generation, scientific reasoning) is unsubstantiated.
- **Missing ablation studies on key design choices**: The adaptive multi-stage guidance (hint ratio ω) is described as important but receives no ablation. How sensitive is performance to the hint ratio schedule? What happens with a fixed ω=0.3 vs. ω=0.7? The cold-start strategy (N=20 steps) also lacks ablation—is this critical, or would the method work without it? The paper claims the difficulty detection is "automated" but the hint ratio adjustment itself appears to require manual scheduling.

### Minor

- **Assumption 1 is not formally proven**: The assumption that using ground-truth traces for failing problems improves OOD generalization is stated as an assumption and "demonstrated through comprehensive experiment," but the experiment only shows in-distribution performance gains. The OOD generalization claim is not directly tested.
- **Theoretical contribution is limited**: The paper is primarily an empirical engineering contribution. The core idea (using partial solutions as guidance when the model fails) is intuitive and has been explored in prior work on curriculum learning and imitation learning for RL. The novelty lies in the specific integration with GRPO and the automated difficulty detection, which is a reasonable but incremental contribution.
- **Training cost analysis is missing**: The paper claims GHPO is "efficient" but does not report training time, FLOPs, or GPU hours compared to GRPO. Since GHPO requires generating hints (even if pre-computed) and potentially longer responses, a cost-benefit analysis would strengthen the efficiency claims.

### Trivial

- The paper uses "GHPO-CL-H(0.5)" in Table 2 but the main text refers to "Qwen2.5-7B-GHPO-CL-H0.5"—minor naming inconsistency.
- Figure 2 is difficult to parse; the flow from "Sparse Rewards" to "Hint Extraction" to "New Query" is not clearly explained in the caption.

## Nice-to-Haves

- Evaluate on smaller models (1.5B, 3B) to validate the claim that GHPO is especially beneficial for capacity-constrained models.
- Compare against DAPO and LUFFY to establish relative performance against existing methods targeting the same problem.
- Add an ablation study on the hint ratio ω schedule and the cold-start step count N.
- Report training wall-clock time and GPU hours to substantiate efficiency claims.
- Test on non-math reasoning tasks (e.g., code generation, scientific QA) to demonstrate generality.

## Novel Insights

None beyond the paper's own contributions. The key insight—that adaptive guidance based on online difficulty detection can mitigate reward sparsity in RLVR—is a practical engineering contribution rather than a fundamentally new theoretical insight. The observation that gradient norms are smaller and more stable under GHPO (Figure 4d) is a nice empirical finding that could inform future work on training stability.

## Suggestions

- Add comparisons with DAPO and LUFFY, as these are the most directly related methods addressing the same reward sparsity problem.
- Include experiments on at least one smaller model (e.g., Qwen2.5-1.5B) to validate the claim about on-device models.
- Provide an ablation study varying the hint ratio ω (e.g., fixed 0.3, 0.5, 0.7 vs. adaptive) to justify the multi-stage guidance design.
- Report training time and computational cost to support efficiency claims.

## Score and Decision

The paper addresses a real and important problem (reward sparsity in RLVR), proposes a practical and well-motivated solution, and provides solid empirical evidence of improvement over vanilla GRPO. However, the lack of comparison with state-of-the-art methods (DAPO, LUFFY), limited evaluation scope (only 7B models, only math), and missing ablations on key design choices prevent a stronger recommendation. The contribution is solid but incremental.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>