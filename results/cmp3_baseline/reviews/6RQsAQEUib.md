## Summary

The paper proposes Guided Hybrid Policy Optimization (GHPO), a reinforcement learning framework for LLM reasoning that addresses reward sparsity caused by capacity-difficulty mismatch. GHPO dynamically detects whether a problem is too difficult for the current policy (based on all group responses being zero-reward) and, if so, adaptively refines the prompt by appending a partial ground-truth solution trace. This hybrid approach switches between standard on-policy RL and guided imitation learning, aiming to provide valid learning signals on hard problems while preserving exploration on easier ones. Experiments on six math benchmarks using Qwen2.5-7B models show average gains of ~5% over GRPO and curriculum learning baselines.

## Strengths

- **Identifies a critical practical problem.** The capacity-difficulty mismatch leading to reward sparsity is a genuine bottleneck in RLVR training, especially for smaller models, and the paper clearly motivates the issue.
- **Simple and intuitive method.** The idea of using on-the-fly difficulty detection based on group reward sparsity and injecting partial ground-truth traces is straightforward, easy to implement, and well-grounded in the intuition that more guidance is needed when the model cannot solve a problem at all.
- **Reasonable ablation analysis.** The comparison with a fixed-hint curriculum learning baseline (GRPO-CL-H0.5) demonstrates that adaptive guidance (GHPO) is better than static hint quotas, supporting the core claim about dynamic refinement.
- **Training dynamics analysis.** Figure 4 provides useful insight into how GHPO differs from GRPO in terms of accuracy reward, response length, and gradient norm, lending support to the claimed stability benefits.
- **Generalization to a stronger base model.** The experiments with Qwen2.5-Math-7B show consistent improvement over GRPO on that backbone, which strengthens the applicability claim.

## Weaknesses

### Major

1. **Insufficient baseline comparisons.** The paper compares only with GRPO and curriculum-learning variants of GRPO. Several recent competitive RLVR methods (DAPO, Dr. GRPO, LUFFY, VAPO) are discussed in the related work but are not evaluated. Without such comparisons, the claim of “state-of-the-art” or “consistently outperforming strong on-policy reinforcement learning” is not substantiated. DAPO, for example, also addresses reward sparsity via dynamic sampling; it should be included.

2. **No statistical significance or multi-run results.** All tables present single accuracy numbers without error bars, standard deviations, or any indication of multiple runs. Given the inherent variance in RL training, single runs are insufficient to support the claimed improvements. This is a major reproducibility and reliability concern.

3. **Narrow evaluation scope.** Experiments are limited to mathematics benchmarks and only one model family (Qwen2.5). The paper claims general applicability, but no evidence is provided for other reasoning domains (e.g., programming, science QA) or other model families (e.g., Llama, Mistral). The method’s reliance on ground-truth solution traces further limits domains where such traces are available.

4. **Performance is not uniformly positive.** On the Mixed dataset (Table 2), GHPO performs *worse* than GRPO on OlympiadBench (0.389 vs. 0.396) and ties with GRPO-CL-H0.5 on that benchmark. The paper does not discuss these cases or examine why certain benchmarks degrade. The overall average gain is driven by a few benchmarks (e.g., GPQA-Diamond), not consistent across all tasks.

### Minor

- **Difficulty detection is coarse.** The criterion (all G responses zero-reward) may miss “borderline” problems where only a very small fraction of responses are correct. These problems still provide very sparse signal and may benefit from guidance, but are not captured.
- **Cold-start strategy hyperparameter.** N=20 steps is chosen without sensitivity analysis. The method’s sensitivity to this value is not explored.
- **Hint adaptation details are deferred to appendix.** The multi-stage guidance strategy is only sketched in the main text; full details and the design rationale appear in the appendix (not fully visible here). A reviewer cannot evaluate this aspect fully without the appendix.

## Nice-to-Haves

- Include comparisons with at least one additional recent method (e.g., DAPO, Dr. GRPO) to calibrate the improvements.
- Perform multiple random seeds and report mean ± std or at least significance tests.
- Evaluate on a non-mathematical reasoning benchmark (e.g., coding, science) to broaden the scope.
- Provide an analysis of cases where GHPO degrades performance and why, to understand limitations.
- Ablate the hint ratio adaptation mechanism (e.g., compare with fixed ratios and no adaptation) to isolate its benefit.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Strengthen the experimental section by adding runs with multiple seeds and reporting variance. This is essential for confidence in the results.
- Include at least one strong recent baseline (e.g., DAPO) in the comparison. Without it, the paper cannot support claims of state-of-the-art performance.
- Discuss the benchmark-specific performance variations (e.g., OlympiadBench) honestly; this would improve trust in the analysis.
- Clarify the applicability boundaries: domains where ground-truth solution traces are not available or where the zero-reward condition is rare.

## Score and Decision

Score: 4  
Decision: Reject  

The paper addresses a meaningful problem and proposes a simple, sensible solution. However, the experimental validation has significant gaps: lack of comparison to recent competitive methods, absence of error bars or multiple runs, limited domain scope, and mixed individual benchmark results. These weaknesses prevent the paper from providing convincing evidence of its claimed effectiveness. The core idea has merit, but the empirical support is insufficient for acceptance at ICLR.

MY FINAL SCORE: 4</score>
MY FINAL DECISION: Reject</decision>