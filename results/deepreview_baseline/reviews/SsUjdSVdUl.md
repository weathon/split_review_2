## Summary
The paper proposes Critique-RL, a two-stage reinforcement learning approach for training critiquing language models without requiring stronger supervisors. In Stage I, the critic's discriminability (ability to correctly judge response correctness) is optimized using direct rule-based reward signals. In Stage II, the critic's helpfulness (ability to provide useful feedback for refinement) is optimized while maintaining discriminability via regularization. Experiments across mathematical reasoning tasks with Qwen2.5-3B/7B show consistent improvements over SFT, STaR, Retroformer, and CTRL baselines in terms of final accuracy and discrimination.

## Strengths
- **Clear problem motivation and insightful analysis**: The paper identifies and empirically demonstrates that optimizing critics using only indirect reward signals (e.g., refinement correctness) leads to either overly conservative or overly aggressive behavior, with poor discriminability as the root cause. Figure 3 compellingly shows this training collapse.
- **Well-designed two-stage method**: The decoupling of discriminability (Stage I) and helpfulness (Stage II) is conceptually clean and directly addresses the identified failure modes. The regularization in Stage II (KL with Stage-I model + discrimination reward) is a principled way to prevent forgetting.
- **Thorough and convincing experiments**: The paper evaluates on multiple models (3B, 7B), multiple in-domain reasoning tasks (MATH, GSM8K, AQuA), and out-of-domain tasks (SVAMP, TheoremQA). Ablation studies in Table 3 cleanly validate the necessity of each stage and the discrimination-preserving components. Iterative training results show further gains (Table 2).
- **Demonstrates compute-efficiency**: The scaling analysis (Figure 1) shows that Critique-RL's response-critique-refinement sampling is more efficient than naive parallel sampling, a practically important result.

## Weaknesses
### Major
- **Unclear RL algorithm control in baselines**: The paper states that Critique-RL uses RLOO as its base algorithm, while Retroformer and CTRL originally used PPO and GRPO respectively. It is not specified whether the baselines were re-implemented with RLOO or kept as originally proposed. If different RL algorithms were used, the performance gains attributed to the two-stage method could be partially confounded by the choice of RL algorithm. This should be explicitly addressed or controlled.

### Minor
- **Reliance on oracle verifier during training**: While the paper claims "without stronger labeling," it still requires the ground-truth correctness signal (\(r_{\text{oracle}}\)) to compute \(r_{\text{dis}}\) in Stage I and \(r_{\text{refine}}\) in Stage II. For tasks where a rule-based verifier is unavailable (e.g., open-ended generation), the method would need a learned reward model, which is acknowledged only briefly in Appendix G. The framing in the abstract and introduction could be sharper about this limitation.
- **Modest gains on some benchmarks**: On AQuA with the 7B model, the improvement over CTRL is only 0.79 points (65.75 vs 64.96), and over Retroformer is 2.36 points. While the overall trend is positive, the benefit on harder multiple-choice reasoning appears smaller.
- **Hyperparameter sensitivity not deeply explored**: The KL coefficients \(\beta, \beta_1, \beta_2\) and the number of training steps are set to fixed values. No sensitivity analysis is provided to show how robust the method is to these choices.

### Trivial
- None.

## Nice-to-Haves
- A controlled experiment where all RL baselines use the same RL algorithm (e.g., RLOO) to isolate the effect of the two-stage reward design.
- Analysis of computational cost (training time, number of RL steps) for Critique-RL vs. baselines.
- Ablation of the optimism/aggressiveness patterns using per-step reward breakdown (e.g., whether Stage II reduces \(\Delta^{c \to i}\) and increases \(\Delta^{i \to c}\) simultaneously).

## Novel Insights
The key insight beyond the paper's own contributions is that discriminability (judging response correctness) and helpfulness (providing constructive feedback) are not automatically aligned under standard RL with outcome-based rewards for the critic. Discriminability requires explicit direct reward signals, and without it, the critic's behavior degrades into conservative (avoiding changes) or aggressive (over-changing) modes. This suggests that for any training of auxiliary critic or verifier models, explicitly maintaining or optimizing the correctness of the critic's judgment is a critical inductive bias.

## Suggestions
- Add a controlled experiment where Retroformer and CTRL baselines are also implemented with RLOO (or Critique-RL is implemented with PPO/GRPO) to demonstrate that the two-stage method itself, not the RL algorithm, drives improvement.
- Clarify in the main text the distinction between "no stronger supervisor" (no human-written critique annotations) and the requirement of a task-specific correctness oracle at training time. This limitation should be discussed more upfront.
- Include a sensitivity analysis for the KL coefficients \(\beta, \beta_1, \beta_2\) to guide practitioners on robustness.

## Score and Decision
**Score**: 8.0  
**Decision**: Accept

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>