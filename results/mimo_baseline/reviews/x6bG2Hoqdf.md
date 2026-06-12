## Summary

This paper introduces CALM, a framework for automatic heuristic design (AHD) that co-evolves an LLM alongside the heuristic search process by fine-tuning the LLM via GRPO (a score-based RL algorithm) using rewards derived from heuristic quality. CALM combines "verbal gradients" (evolutionary prompt operators including fine-granularity mutation, diversity-aware crossover, and a collapse mechanism for escaping local optima) with "numerical gradients" (RL-based adaptation of the LLM). Experiments across four optimization tasks show that a compact, quantized 7B model fine-tuned with this approach outperforms or matches baselines built on substantially more powerful API-based models.

## Strengths

- **Novel and well-motivated co-evolution paradigm.** The core insight—that LLM-based AHD methods waste a natural learning signal by keeping the LLM frozen—is clearly articulated and the RL-based co-evolution solution is technically sound. The distinction between "verbal gradients" (prompt manipulation) and "numerical gradients" (parameter updates) is a useful conceptual framing.

- **Substantial empirical gains with practical deployment.** CALM running on a single 24GB GPU with INT4-quantized Qwen2.5-7B-Instruct outperforms GPT-4o-mini-based baselines on OBP (0.71% vs 0.82% avg gap), CVRP (3.83% vs 5.44% gap at N=50), and OP (15.43% vs 16.13% at N=100; 12.58% vs 15.10% at N=200). The training curves in Figure 2 clearly show the GRPO-adapted model converging to and surpassing API-based approaches over the course of training.

- **Comprehensive ablation studies.** Table 4 systematically isolates contributions of GRPO (largest single impact), collapse mechanism, each evolutionary operator, and the reward design. The ablations on reward function alternatives and collapse hyperparameters provide meaningful design insights. Removing GRPO causes the largest performance drop across nearly all settings, directly validating the central thesis.

- **Well-designed operator suite.** The fine-granularity injection and replacement operators are motivated by a clear reasoning about token-level credit assignment in GRPO, and the diversity-aware crossover provides a principled mechanism to balance exploitation and exploration. The collapse mechanism addresses a genuine concern about premature convergence in evolutionary LLM-based methods, with a theoretical analysis of expected collapse timing.

## Weaknesses

### Fatal
None.

### Major

- **Marginal gains on TSP with inconsistency across scales.** On the in-domain TSP-50 task, CALM (GRPO) scores 10.04% gap vs MCTS-AHD's 9.69% gap—both are GPT-4o-mini baselines that outperform CALM. At N=100, MCTS-AHD (11.79%) still edges out CALM (11.58%) by a small margin. CALM only clearly wins at N=200 (13.41% vs 13.71%). Given that TSP is a canonical benchmark for AHD, this pattern raises questions about whether the method's advantages are task-dependent rather than general. The paper could benefit from deeper analysis of why GRPO helps more on CVRP/OP than on TSP (e.g., is it related to the ACO framework structure, problem dimensionality, or the nature of the heuristic space?).

- **Fairness of computational budget comparison.** CALM uses a fixed budget of 2,000 LLM queries across tasks, while baselines use 1,000 heuristic evaluations (which the authors argue translates to ~4,000+ queries). However, the RL fine-tuning process itself involves generating G responses per prompt for GRPO updates, which adds significant wall-clock computation beyond the raw query count. The paper reports running time in Appendix I but does not provide a head-to-head wall-clock comparison with baselines in the main text. Since the claim of "running entirely on a local computer" is a selling point, a more transparent accounting of total computational cost (including RL training overhead) would strengthen the argument.

### Minor

- **Ablations cover only two tasks (OBP and OP).** The ablation studies in Table 4 only report results on OBP and OP. Including TSP and CVRP would provide stronger evidence that design choices generalize across problem types, especially given the TSP variance noted above.

- **No analysis of RL training stability or sample efficiency.** GRPO requires generating multiple responses per prompt (G samples), and the paper does not discuss how sensitive the method is to the choice of G, potential training instabilities, or how quickly the model converges. A brief analysis of training dynamics beyond the aggregate curves in Figure 2 would be informative.

- **Quantization effects not fully isolated.** The paper uses INT4-quantized Qwen2.5-7B-Instruct throughout and compares against FP-quality GPT-4o-mini. While the authors acknowledge the accuracy gap from quantization, they do not provide experiments with FP16 Qwen2.5-7B-Instruct to isolate how much performance is lost to quantization versus gained from GRPO fine-tuning. This would help readers understand the true potential of the approach.

### Trivial

None.

## Nice-to-Haves

- A visualization or analysis of how the fine-tuned LLM's output distribution changes over training (e.g., do generated heuristics become structurally more similar to high-performing ones?).
- Discussion of failure cases: are there problem instances or settings where CALM's co-evolution approach fails to help or even hurts?
- Comparison with other RL algorithms for LLM fine-tuning (e.g., PPO) to contextualize the choice of GRPO.

## Novel Insights

The paper's most novel insight is that the iterative heuristic evaluation process in LLM-based AHD generates a rich stream of prompt-response-reward data that can be directly exploited for RL-based LLM adaptation, creating a positive feedback loop between the search process and the generator. This reframes AHD from a pure optimization problem (where the LLM is a fixed tool) to a joint optimization problem (where the LLM itself improves). The fine-granularity mutation operators, designed to improve token-level credit assignment under GRPO, represent a thoughtful bridge between prompt engineering and RL training—a connection that is non-obvious and potentially applicable to other RL-for-code-generation settings.

## Suggestions

- Add a direct wall-clock time comparison table for all methods on at least one representative task to substantiate the efficiency claims.
- Provide an ablation on the number of GRPO response groups (G) to help practitioners understand the compute-performance tradeoff.
- Analyze why the TSP results are less decisive than CVRP/OP—this could reveal important insights about when co-evolution helps most.

## Score and Decision

The paper presents a well-motivated and technically sound contribution that advances the state of LLM-based automatic heuristic design. The co-evolution idea is natural yet non-trivial, the empirical results are strong across multiple tasks, the ablation studies are thorough, and the practical advantage of running on a single consumer GPU is compelling. The gains on TSP are less decisive, and the computational cost analysis could be more transparent, but these do not undermine the core contribution. The paper provides clear value to the ICLR community working at the intersection of LLMs and optimization.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>