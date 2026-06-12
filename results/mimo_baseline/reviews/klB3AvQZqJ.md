## Summary

The paper proposes CARL (Constraint-aware Reward Relabeling), a minimalist wrapper for offline safe reinforcement learning that reformulates the constrained optimization as an unconstrained problem via state-action-wise constraints. At each training step, CARL estimates cost-to-go using off-policy evaluation and relabels rewards for state-action pairs exceeding the cost budget with a large negative penalty, then passes the relabeled data to any standard offline RL algorithm. Experiments on 19 DSRL benchmark tasks under tight cost budgets demonstrate that CARL achieves consistent constraint satisfaction while maintaining competitive rewards.

## Strengths

- **Simplicity and modularity.** CARL is an elegantly simple wrapper that requires no architectural modifications to the backbone offline RL algorithm and introduces no task-specific hyperparameters beyond the cost budget κ. This is a genuine practical advantage over Lagrangian-based methods that require tuning multipliers. The method works with both TD3-BC and IQL (Table 2), demonstrating backbone-agnostic design.

- **Strong empirical results under tight cost budgets.** CARL is the only method that satisfies cost constraints across all Bullet tasks (Table 1) and achieves safety on 8/11 SafetyGym tasks, outperforming FISOR, CAPS, CCAC, and others in the challenging κ=5/10 regime. Importantly, safety is not achieved at the expense of reward—CARL consistently ranks among the top methods for reward while remaining safe.

- **Interesting ablation on unsafe-only training.** The experiment training CARL exclusively on unsafe trajectories (Figure 3) convincingly demonstrates that reward relabeling can transform unsafe data into safe policy behavior, providing insight into the mechanism's effectiveness beyond simply filtering safe data.

## Weaknesses

### Fatal
None.

### Major

- **Limited theoretical depth.** Theorem 1 establishes equivalence between the pointwise-constrained formulation and the unconstrained reward relabeling formulation, but the proof is a straightforward contradiction argument. The convergence properties of the iterative procedure with M=K=1 and function approximation are left as an open problem (acknowledged in Section 5.2). While empirical stability is demonstrated, a deeper theoretical understanding—e.g., under what conditions on the MDP class, dataset coverage, or function approximation class convergence holds—would significantly strengthen the contribution.

- **Inconsistent safety on SafetyGym tasks.** CARL fails to satisfy constraints on 3/11 SafetyGym tasks (CarCircle1: 4.15±8.93, CarCircle2: 1.57±1.38, CarGoal2: 1.77±0.51). The CarCircle1 result has extremely high variance, suggesting the method can be unstable on certain task/dataset combinations. While 8/11 is still better than baselines, this inconsistency somewhat undermines the claim of reliable safety enforcement and should be analyzed more carefully—what distinguishes the failing tasks from the succeeding ones?

- **The "no additional hyperparameters" claim deserves scrutiny.** The penalty magnitude used in reward relabeling (R_max from the data vs. V_max = R_max/(1-γ)) is effectively a design choice with significant impact. Table 5 (appendix) compares these, but the main paper uses R_max without deep justification. Additionally, M and K are technically hyperparameters, even if M=K=1 works well empirically. The claim should be stated more carefully.

### Minor

- **High variance in several results.** Beyond CarCircle1, several CARL results show notable variance (e.g., DroneRun cost 0.30±0.52, PointCircle2 cost 0.91±1.46). Reporting additional statistics (e.g., median, interquartile range, success rate across seeds) would provide a clearer picture of reliability.

- **The oscillation analysis (Figure 1) is illustrative but limited.** The oscillation is shown only for one task (AntRun) with one backbone (TD3-BC). A brief analysis across multiple tasks/backbones would better justify the M=K=1 design choice and clarify whether oscillation is a general phenomenon or task-specific.

- **Missing analysis of Q_c estimation quality.** CARL's performance fundamentally depends on accurate cost-to-go estimation. The paper does not analyze how Q_c estimation errors propagate through reward relabeling, or what happens when the off-policy evaluation (FQE) produces poor cost estimates—a likely scenario in data-sparse regions relevant to safety.

### Trivial
None.

## Nice-to-Haves

- An analysis of how the number of training iterations affects the trade-off between reward and constraint satisfaction would be informative for practitioners.
- A comparison of wall-clock training time between CARL and Lagrangian methods would strengthen the practical simplicity argument.
- Visualizations of which state-action regions are relabeled across training iterations would provide insight into how CARL navigates the safety-reward trade-off.

## Novel Insights

The key novel insight is that state-action-wise safety constraints can be converted into an unconstrained optimization via conditional reward relabeling, and that performing this relabeling at the mini-batch level (M=K=1) with gradual updates avoids the oscillation instability that arises from decoupled cost evaluation and policy optimization steps. This insight—that the granularity of batch updates acts as a natural stabilizer connecting cost estimation and policy improvement—is practically useful and goes beyond simply applying penalty-based methods. The demonstration that training on purely unsafe data can yield safe policies through relabeling is also a noteworthy empirical finding.

## Suggestions

- Provide a more detailed analysis of failure cases on SafetyGym tasks to understand when and why CARL's cost-to-go estimation leads to insufficient penalty.
- Include a sensitivity analysis of the penalty magnitude choice (R_max vs. V_max vs. other options) in the main paper, not just the appendix.
- Consider adding a simple convergence diagnostic (e.g., monitoring the fraction of relabeled transitions over training) to help practitioners assess whether training has stabilized.

## Score and Decision

The paper presents a clean, practical contribution to offline safe RL with strong empirical results. The simplicity of the approach is a genuine strength, and the results under tight cost budgets address a real gap. However, the theoretical contribution is limited (straightforward theorem, no convergence analysis), safety consistency across all benchmark tasks is not fully achieved, and some claims about hyperparameter freedom are overstated. The work is solid but falls short of exceptional.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept