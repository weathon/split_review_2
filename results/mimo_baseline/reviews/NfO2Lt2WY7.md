## Summary

This paper systematically ablates the components of Group Relative Policy Optimization (GRPO) to determine which are essential for teaching LLMs to reason mathematically. Through controlled experiments on small Qwen2.5 and Llama3.2 models (0.5B–1.5B), the authors identify that negative feedback via negative advantages is essential, advantage estimation is critical for stability, and PPO-style clipping is unnecessary. They propose RGR (REINFORCE with Group Relative Advantage), a simplified GRPO variant that retains group-relative advantages but removes policy ratio clipping and PPO-style constraints.

## Strengths

- **Clear and well-motivated research question.** The paper directly addresses a practical concern shared by many practitioners: whether GRPO's complexity (clipping, policy ratios, KL regularization, group-relative advantages) is fully justified. This is timely given the explosion of GRPO variants and the importance of reasoning post-training.

- **Well-designed ablation study.** The paper isolates individual GRPO components (negative feedback, PPO-style clipping, advantage estimation) in a principled manner, testing each removal independently. The ablation of positive-only advantages cleanly demonstrates that negative feedback is essential—a finding with practical implications for RAFT-like methods that inherently discard negative signal.

- **Comprehensive evaluation across languages and domains.** The paper evaluates on nine benchmarks spanning English math, Chinese math, and STEM domains, with three model families, providing a reasonably diverse assessment.

- **Clear finding on training collapse.** Figure 1 convincingly shows that removing negative feedback (positive-only GRPO) or removing advantage estimation (direct REINFORCE) leads to training collapse with response length dropping to near-zero, illustrating the phenomenon of reward hacking through trivial outputs.

## Weaknesses

### Fatal

None.

### Major

- **Experiments limited to very small models (0.5B–1.5B).** This is the most significant limitation. GRPO's primary use cases involve models at 7B+ scale (e.g., DeepSeek-R1 uses 671B). The authors acknowledge this limitation in the conclusion but do not address it in the claims. The PPO-style clipping constraints may serve a fundamentally different role at larger scales where policy drift is more severe, and conclusions drawn at 0.5B–1.5B may not transfer.

- **Performance margins of RGR over GRPO are marginal and inconsistent across model families.** On the primary Math-English benchmarks, the average differences are 0.9 points for Qwen-0.5B (26.5 vs 25.6) and 1.0 point for Qwen-1.5B (38.3 vs 37.3), while for Llama3.2-1B they are essentially identical (20.2 vs 20.1). On Chinese Math and STEM benchmarks, Llama3.2-1B consistently shows GRPO outperforming RGR (30.1 vs 26.6 on Chinese Math; 24.9 vs 22.5 on STEM). This inconsistency undermines the central claim that clipping is universally unnecessary.

- **No error bars or multi-seed evaluations.** All reported numbers come from single runs. Given the small margins of improvement (often <1 point), it is impossible to determine whether differences are statistically meaningful or within random variation. For a paper whose core contribution is a comparison of methods, this is a significant gap.

- **Very limited training data and compute.** Training uses only 1,800 GSM8K instances for ~70 steps. While this enables controlled comparison, it severely limits the generalizability of conclusions. The paper does not investigate whether longer training, curriculum effects, or training on harder problems changes the relative ordering of methods.

### Minor

- **"17 out of 27 comparisons" framing is misleading.** The paper claims RGR surpasses GRPO in 17/27 individual comparisons, but this count includes many benchmark-model pairs where the difference is within noise (e.g., GSM8K Llama3.2: 43.3 vs 43.0). A more honest presentation would emphasize the aggregate trends rather than cherry-picking per-cell wins.

- **Missing hyperparameter sensitivity analysis.** The paper does not analyze sensitivity to the KL coefficient β, learning rate, group size G, or LoRA rank—all of which could interact with the choice of clipping. A brief sensitivity analysis would strengthen the claim that RGR is robust.

- **The GRPO loss formulation (Eq. 1) appears to have a subtle issue.** The PPO-style clipping is applied to the policy ratio $r_{i,t}$ multiplied by advantage $\hat{A}_{i,t}$, but the standard GRPO formulation clips the ratio alone before multiplying by advantage. If the authors are faithfully reproducing GRPO, this should be clarified; if they are using a non-standard formulation, it could affect the comparison.

### Trivial

None.

## Nice-to-Haves

- Experiments at 7B scale, even if limited to a single model, would dramatically strengthen the paper's relevance to the community.
- Analysis of reasoning chain quality (e.g., length, logical coherence) beyond just correctness scores would provide deeper insight into *how* simplification affects reasoning behavior.
- A theoretical argument for why clipping is unnecessary from strong initializations (building on the Ahmadian et al. 2024 insight) would complement the empirical analysis.

## Novel Insights

The paper's most genuinely novel insight is the demonstration that positive-only advantages (ignoring negative feedback) cause training collapse through a reward-hacking mechanism where models converge to trivially short responses. This is a clean, well-supported finding with practical implications: methods like RAFT that inherently discard negative signal are fundamentally limited in the RL-for-reasoning setting. The finding that this collapse manifests as response length truncation—rather than, say, mode collapse on specific tokens—provides a useful diagnostic signal for practitioners.

## Suggestions

- Add multi-seed experiments (at least 3 seeds) with error bars for the primary benchmark comparisons. This is essential given the small margins.
- If larger-scale experiments are not feasible, add a careful discussion of why results at 0.5B–1.5B may or may not transfer to the scales where GRPO is most commonly used.
- Clarify the exact GRPO formulation used and verify it matches the original DeepSeek-Math paper, as the clipping interaction with advantage is non-obvious.
- Consider adding a sensitivity analysis over the KL coefficient β, which is a key hyperparameter that interacts with the clipping constraint.

## Score and Decision

The paper tackles a relevant question and provides a clean ablation framework. The negative feedback finding is valuable. However, the evidence for the central claim—that clipping is unnecessary—is undermined by marginal and inconsistent improvements across model families, experiments limited to very small models (0.5B–1.5B), and the absence of error bars. The improvements on Qwen models are modest (~1 point average), and GRPO consistently outperforms RGR on Llama3.2-1B, contradicting the universal claim. For a paper proposing simplification as its main contribution, the evidence needs to be more robust.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>