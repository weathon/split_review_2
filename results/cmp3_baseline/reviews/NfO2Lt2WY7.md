## Summary

This paper systematically decomposes the GRPO loss function used for post-training LLMs on reasoning tasks. Through controlled ablations on small models (0.5B–1.5B), the authors find that (1) negative feedback is essential for stable learning, (2) group-relative advantage estimation is crucial, and (3) PPO-style clipping and policy ratio terms are unnecessary. They propose RGR (REINFORCE with Group Relative Advantage), a simplified variant that removes clipping while retaining group-relative advantages, and show that it often matches or exceeds GRPO on mathematical reasoning benchmarks.

## Strengths

- **Clear and well-motivated research question**: The paper asks whether GRPO’s complexity is truly necessary, which is timely given the widespread adoption of GRPO and its many variants. The systematic ablation approach is appropriate and well-executed.
- **Empirically supported key findings**: The experiments convincingly demonstrate that positive-only training (GRPO-pos, RAFT) leads to collapse or stagnation, and that removing advantage estimation (plain REINFORCE) destabilizes learning even in larger models. These results are consistent across three model families and multiple benchmarks.
- **Simple and practical contribution**: RGR is straightforward to implement and removes the clipping hyperparameter, making it more transparent and easier to tune. The paper provides a clear recipe for practitioners who want a simpler alternative to GRPO.
- **Good coverage of benchmarks**: The evaluation spans English math, Chinese math, and STEM benchmarks, showing generalization beyond the training distribution (GSM8K).

## Weaknesses

### Fatal
None.

### Major
- **Lack of statistical rigor**: All experiments appear to be run with a single seed. RL training is notoriously noisy, and without multiple seeds or confidence intervals, the reported performance differences (e.g., RGR vs. GRPO) cannot be assessed for significance. This is a critical omission for a paper making comparative claims.
- **Limited model scale**: Experiments are restricted to models ≤1.5B parameters. GRPO’s main successes (e.g., DeepSeek-R1) are at much larger scales (7B+). It is unclear whether the findings—especially that PPO clipping is unnecessary—hold for larger models where policy updates may be more aggressive. The paper acknowledges this as future work, but it limits the strength of the conclusions.
- **Training only on GSM8K**: All models are trained exclusively on a subset of GSM8K. While the benchmarks are diverse, the training data is narrow. It is unknown whether the conclusions generalize to other reasoning domains (e.g., coding, science) or to training on multiple datasets.
- **Inconsistent naming**: The paper introduces “RGR A” in Section 3.2 but then uses “RGR” in tables and later text. It is unclear whether RGR A and RGR are the same method. The final conclusion refers to “RGRA” (a typo). This confusion undermines clarity.

### Minor
- **Missing hyperparameter details**: The paper does not report the KL penalty coefficient β, the clipping coefficient ε (for GRPO), or the learning rate schedule. These are important for reproducibility, especially since the paper claims clipping is unnecessary—the specific hyperparameter choices could affect the comparison.
- **No comparison with other GRPO variants**: The paper mentions DAPO, CPPO, S-GRPO, etc. in related work but does not compare RGR against any of them. Including at least one recent variant (e.g., DAPO, which also modifies clipping) would strengthen the positioning.
- **Figure 1 is hard to read**: The six subplots are small, and the line styles are difficult to distinguish (especially GRPO vs. RGRa). A zoomed or higher-resolution figure would help.

### Trivial
- The abstract says “RGR has the potential to achieve stronger performance” but the results show it often does; the hedging is unnecessary.
- The paper uses “RGRA” in the conclusion but “RGR” elsewhere.

## Nice-to-Haves
- Run experiments with at least 3 random seeds and report mean ± std.
- Extend experiments to a 7B model (e.g., Qwen2.5-7B) to test scalability of the findings.
- Include a comparison with DAPO or another recent GRPO variant that also modifies clipping.
- Provide the exact hyperparameters (β, ε, learning rate, batch size) in the main text or a table.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that the success of GRPO-style training for reasoning may be driven more by the group-relative advantage baseline (which provides a natural, reward-normalized signal) than by the PPO clipping mechanism. This suggests that the RL challenges that motivated PPO (e.g., large policy updates from scratch) are less relevant when starting from a strong pretrained policy, and that simpler policy-gradient methods can suffice. The finding that negative feedback is essential also reinforces the importance of learning from both successes and failures, which is often overlooked in rejection-sampling approaches.

## Suggestions
- Run all experiments with at least 3 seeds and report error bars or confidence intervals.
- Clarify the naming: use “RGR” consistently throughout, and explicitly state that RGR = RGR A.
- Add a table of hyperparameters (β, ε, learning rate, batch size, number of steps) for all methods.
- Include a brief experiment on a larger model (e.g., 7B) to demonstrate scalability, even if only on a subset of benchmarks.
- Compare RGR with at least one recent GRPO variant (e.g., DAPO) to contextualize the improvement.

## Score and Decision

**Score**: 5.0  
**Decision**: Borderline Accept

The paper addresses an important question with a clean ablation study and produces a simpler, effective method. However, the lack of statistical rigor and the restriction to small models prevent the conclusions from being fully convincing. With additional seeds and larger-scale validation, this work could be a strong contribution. In its current form, it is borderline but has clear value for the community.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>