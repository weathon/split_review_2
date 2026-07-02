## Summary
This paper introduces Agentic Reinforced Policy Optimization (ARPO), a reinforcement learning algorithm tailored for training LLMs that interact with external tools over multiple turns. ARPO is motivated by the observation that token-level entropy spikes after tool-call steps, suggesting high uncertainty. It incorporates an entropy-based adaptive rollout mechanism that branches partial reasoning paths at high-entropy tool-use steps, combined with advantage attribution estimation that differentiates shared and divergent token segments. Experiments on 13 reasoning benchmarks (math, knowledge-intensive, and deep search) show ARPO consistently outperforms trajectory-level RL baselines (GRPO, DAPO, REINFORCE++) while using roughly half the tool-call budget.

## Strengths
- **Novel and well-motivated mechanism:** The observation that entropy increases sharply after tool-call steps is clearly demonstrated and provides a strong motivation for step-level exploration rather than trajectory-level rollouts.
- **Extensive empirical validation:** The paper evaluates on 13 diverse benchmarks covering mathematical reasoning, knowledge-intensive QA, and complex deep search tasks, with consistent improvements over multiple trajectory-level RL baselines on two backbone model families (Qwen2.5-7B, Llama3.1-8B, Qwen3-8B/14B).
- **Tool-call efficiency:** ARPO achieves better or comparable performance with approximately half the tool-call budget during training compared to GRPO (Figure 7a), which is practically important for real-world deployment costs.
- **Clear ablation on advantage estimation:** The comparison between hard and soft advantage settings (Figure 5) shows soft advantage yields more stable training, justifying the design choice.

## Weaknesses
### Major
- **Advantage Attribution Estimation lacks novelty:** The "soft advantage estimation" is essentially the standard GRPO loss. The paper acknowledges this but still presents it as a contribution. The only novel aspect is applying GRPO to the branched rollout structure, but the claim of "proposing advantage attribution estimation" inflates the contribution.
- **Sensitivity to hyperparameters is not studied:** The entropy-based branching depends on parameters α, β, and threshold τ (Equation 2). No ablation or sensitivity analysis is provided, making it unclear how robust ARPO is to these choices across different tasks or models.
- **Theoretical foundation is thin:** The Generalized Policy Gradient Theorem (Equation 6) simply reformulates the standard policy gradient at the macro-action (segment) level. This is a known extension (e.g., hierarchical RL, options) and does not provide new theoretical insight specific to ARPO.
- **Limited RL baselines for deep search:** In the deep search experiments (Table 2), the only RL-based competitor is GRPO. Stronger agentic RL baselines or more recent methods (e.g., Tool-Star which is cited in the paper) are not compared, weakening the claim of superiority in that setting.

### Minor
- **Sample size for deep search RL training:** The paper uses only 1k RL training samples for deep search tasks. While this demonstrates sample efficiency, the choice is not justified and raises questions about whether the performance holds under larger training budgets typical for RLVR.
- **Pass@K analysis is only for ARPO:** The scaling analysis (Figure 6) shows Pass@3/Pass@5 for ARPO, but no corresponding results for GRPO or other baselines, so it is unclear whether the diversity gain is unique to ARPO.

### Trivial
- None.

## Nice-to-Haves
- Ablation study on the branching threshold τ and the coefficients α, β to show robustness.
- Comparison with additional agentic RL baselines on deep search (e.g., Tool-Star) and on math/knowledge tasks.
- Pass@K comparisons between ARPO and GRPO to support the diversity claim more directly.
- Study on the effect of the number of initial global samples N vs. partial budget M−N.

## Novel Insights
Beyond the paper's own contributions, the core insight that *token-level entropy in LLMs rises sharply after tool feedback, and that this uncertainty can be exploited for guided step-level exploration*, is a genuinely useful observation for designing future agentic RL algorithms. It reframes tool-call steps as natural branching points where exploration is most valuable, rather than treating the entire trajectory as a monolithic sequence.

## Suggestions
1. Provide an ablation study on the key hyperparameters (α, β, τ) to demonstrate robustness across tasks.
2. Include Pass@K results for baseline RL methods to directly compare sampling diversity.
3. Consider comparing against a broader set of agentic RL methods, especially for deep search, to strengthen the empirical claims.

## Score and Decision
Score: 6.0  
Decision: Accept

**Rationale:** The paper presents a well-motivated and empirically validated improvement over trajectory-level RL for tool-use agents. The entropy-based adaptive rollout is a simple but effective idea, and the experiments across 13 benchmarks show consistent gains with better tool-use efficiency. However, the advantage attribution component adds limited novelty, and missing hyperparameter sensitivity analysis and additional baselines temper the overall contribution. Nonetheless, the work provides clear value to the ICLR community and is likely to be useful for practitioners training LLM agents.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>