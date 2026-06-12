## Summary

This paper proposes Neural Predictor-Corrector (NPC), a reinforcement learning framework that unifies diverse homotopy-based problems (robust optimization, global optimization, polynomial root-finding, and sampling) under a common predictor-corrector (PC) structure, and replaces hand-crafted heuristics for step-size scheduling and corrector termination with learned neural policies. Trained amortized across problem instances via PPO, NPC demonstrates significant efficiency improvements (70-80% fewer iterations) across all four problem domains while maintaining comparable accuracy and generalizing to unseen instances without per-instance fine-tuning.

## Strengths

- **Genuine unification perspective.** The paper convincingly demonstrates that four independently developed homotopy-based solvers share a common PC structure, formalized in Section 3. This cross-domain synthesis is intellectually valuable and, to my knowledge, has not been systematically articulated before. The unified MDP formulation (Section 4.1, Algorithm 1) translates this insight into a concrete, general framework.

- **Consistent speedups across all four domains.** NPC achieves 70-80% fewer iterations and 80-90% less runtime on GNC point cloud registration (Table 1), ~85% fewer iterations on polynomial root-finding (Table 4), and ~75% fewer iterations on ALD sampling (Table 5), all while maintaining accuracy comparable to classical methods. The breadth of evaluation across fundamentally different problem types strengthens the claim that the approach is general rather than domain-specific.

- **Amortized training with demonstrated cross-instance generalization.** Training on a single instance/distribution (e.g., Aquarius for point cloud registration, Ackley with randomized parameters for GH) and deploying on unseen instances is a strong design choice. Tables 1-5 consistently show that the amortized policy transfers effectively, avoiding per-instance fine-tuning overhead at inference time.

- **Informative ablation and trade-off analysis.** Table 6 provides a clean ablation showing that each state component contributes meaningfully, with corrector statistics being most informative. Figure 4's efficiency-precision trade-off visualization compellingly shows that NPC operates below the classical Pareto frontier.

## Weaknesses

### Fatal
None.

### Major

- **Accuracy trade-offs are under-discussed.** In several cases, NPC achieves slightly worse accuracy than classical methods: on the GNC dragon sequence (Table 1), both rotation and translation errors are marginally worse; on ALD's 40-mode GMM (Table 5), W2 increases from 11.57 to 11.91. While these differences may be small, the paper does not discuss whether the speedup-accuracy trade-off is Pareto-optimal or whether users can control precision via reward scaling. This is especially important because the reward function's accuracy-efficiency balance depends on hand-tuned coefficients λ1 and λ2, whose sensitivity is not analyzed.

- **Training computational cost is never reported.** The paper emphasizes amortized training as a key advantage ("one-time offline training"), yet never discloses how long RL training takes or how many environment interactions are required. For practitioners evaluating whether to adopt NPC, this is essential information. If training requires millions of episodes across thousands of instances, the amortization benefit may be limited to frequently-recurring problem classes.

- **All experiments are on small-scale problems.** The GH experiments use 2D functions, the HC benchmarks are modest polynomial systems (katsura10, cyclic7), and the ALD distributions are low-dimensional (funnel in d=10). It is unclear whether NPC scales to high-dimensional optimization (e.g., d=100+), large polynomial systems, or high-dimensional sampling where the PC trajectory becomes far more complex. The small MLP architecture (16 hidden units) suggests the approach may struggle with more complex state-action mappings at scale.

### Minor

- **No confidence intervals or statistical tests.** All results report averages over 50 trials but provide no standard deviations or confidence intervals. Given that some differences are small (e.g., W2 of 11.57 vs. 11.91), it is unclear whether improvements are statistically significant.

- **Task-specific state representation undermines "unified" framing.** While the paper claims a unified framework, the RL state and reward definitions require problem-specific adaptations: convergence velocity uses objective value for optimization but KSD for sampling; corrector termination uses tolerance in some tasks and iteration count in others. A more honest framing would acknowledge that while the PC structure is unified, the RL instantiation still requires per-domain engineering.

- **Comparison fairness issues.** Simulator HC is implemented in C++ while NPC is in Python (Table 4), and iDEM runs on a more powerful GPU (Table 5). While the paper notes these discrepancies, the bolded "best" results in tables implicitly suggest NPC is faster, which may not hold under equivalent implementations.

- **The RL contribution relative to simple adaptive heuristics is unclear.** The paper does not compare against simpler adaptive baselines (e.g., line-search-inspired step adaptation, or PID-controlled step sizes), which could capture some of the benefits with much less complexity. The ablation in Table 6 shows that removing state components causes conservatism, but this doesn't establish that RL is necessary versus simpler adaptive rules that also use these signals.

## Nice-to-Haves

- Report training wall-clock time and sample complexity for each domain, so practitioners can assess amortization feasibility.
- Include a comparison against simple adaptive baselines (e.g., doubling/halving step sizes based on convergence velocity) to isolate the value of RL versus basic adaptivity.
- Experiment with at least one higher-dimensional problem per domain to assess scalability.
- Provide standard deviations or confidence intervals for all reported metrics.

## Novel Insights

The paper's most genuinely novel insight is the systematic identification of the predictor-corrector structure as a common thread across four independently-developed homotopy-based solvers, and the subsequent realization that this structure can be cast as a sequential decision-making problem amenable to RL. While each individual connection (e.g., RL for optimization, learning-based improvements to homotopy) has prior art, the synthesis—particularly the amortized training regime that produces a single policy transferable across instances within a problem class—goes beyond the paper's own explicit contributions and suggests a broader research direction: treating algorithmic hyperparameter selection as an RL problem at the level of algorithm structure rather than individual parameters.

## Suggestions

- Add a table or paragraph reporting NPC training times (total wall-clock hours and number of training instances) for each domain to complete the efficiency picture.
- Include at least one adaptive heuristic baseline (e.g., an adaptive step-size controller using convergence velocity) in the GH or ALD experiments to disentangle the value of RL from simple adaptivity.
- Discuss the sensitivity of results to the reward coefficients λ1, λ2—perhaps via a small hyperparameter sweep—to strengthen the claim that NPC is robust.

## Score and Decision

The paper presents a genuinely novel unification of homotopy problems and a practical RL-based solver with consistent cross-domain speedups. The experimental breadth across four domains is commendable, and the amortized generalization results are convincing. However, the accuracy trade-offs are under-discussed, training costs are undisclosed, all experiments are small-scale, and the absence of simple adaptive baselines makes it hard to isolate RL's contribution. These are meaningful but not fatal concerns that would benefit from author clarification.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept