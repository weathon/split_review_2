## Summary

This paper proposes CARL (Constraint-aware Reward Relabeling), a simple wrapper approach for offline safe reinforcement learning (OSRL) that reformulates the problem as an unconstrained optimization by enforcing state-action-wise safety constraints. The method iteratively alternates between cost evaluation via offline policy evaluation and policy optimization on reward-relabeled data, where state-action pairs predicted to exceed the cost budget receive a maximally negative reward. CARL requires no additional hyperparameters beyond the base offline RL algorithm and demonstrates strong safety and reward performance on DSRL benchmark tasks under tight cost budgets.

## Strengths

- **Simplicity and modularity**: CARL is notably minimalist—it wraps around existing offline RL algorithms (e.g., TD3-BC, IQL) without modifying their loss functions or introducing extra tunable hyperparameters. This makes it highly practical and easy to adopt.
- **Theoretical motivation for state-action-wise constraints**: The paper provides a clean theoretical justification (Theorem 1) showing that enforcing pointwise safety constraints via reward relabeling is equivalent to solving an unconstrained optimization problem, eliminating the need for Lagrangian multiplier tuning.
- **Comprehensive empirical evaluation**: Experiments span 19 tasks from DSRL (Bullet and Safety-Gym) under strict cost budgets (κ=5 or 10), with comparisons against 7 state-of-the-art baselines. CARL is the only method that satisfies safety constraints across all Bullet tasks and achieves competitive or best reward among safe methods.

## Weaknesses

### Fatal
None.

### Major
- **Limited theoretical grounding for the practical algorithm**: Theorem 1 shows equivalence under the idealized setting where Qc^π is known exactly. However, the actual algorithm uses learned (estimated) cost Q-functions updated via batch OPE with M=K=1. The convergence or stability of this practical variant is not analyzed, and the paper explicitly acknowledges this as an open problem. The oscillatory behavior shown in Figure 1 when using large M,K further highlights that the theoretical result does not directly guarantee the practical algorithm's behavior.
- **Inconsistent safety on Safety-Gym tasks**: While CARL achieves perfect safety on Bullet tasks, it violates safety constraints on 3 out of 11 Safety-Gym tasks (CarCircle1, CarCircle2, CarGoal2). Given that the paper emphasizes "small cost budgets" as a key challenge, this inconsistency across a significant fraction of safety tasks is a concern. The authors do not provide sufficient analysis of why safety fails on these specific tasks.
- **Missing ablation on the choice of penalty magnitude**: The paper uses R_max (the max single-step reward from the dataset) as the penalty in the main results, noting that V_max is used in a separate ablation (Table 5, appendix). Since the penalty magnitude directly affects how strongly unsafe actions are discouraged, the sensitivity to this choice is underexplored. This is particularly important because the penalty is a design decision, yet the paper claims "no additional tunable hyperparameters."

### Minor
- **Limited comparison with Lagrangian variants**: While the paper mentions evaluating Lagrangian variants in Table 5 (appendix), the main results omit these comparisons. Given that Lagrangian methods are the most common baseline in safe RL, a direct comparison in the main tables would strengthen the paper's claims about the advantage of avoiding Lagrangian tuning.
- **Oscillatory behavior analysis is incomplete**: Figure 1 demonstrates oscillation when M,K are large, but the paper does not quantitatively analyze why M=K=1 resolves this. A more rigorous diagnostic (e.g., tracking Qc^π estimates over time) would strengthen the claim.

### Trivial
- The evaluation protocol uses normalized cost computed as C_norm = C_pi / kappa, which makes costs >1 unsafe. This is clear but differs slightly from some prior works that use different normalization; the paper correctly specifies this.

## Nice-to-Haves

- An analysis of failure cases on Safety-Gym tasks (CarCircle1, CarCircle2, CarGoal2) would be valuable—e.g., whether the cost Q-function estimation is poor on these tasks, or whether the dataset lacks sufficient coverage of safe state-action pairs.
- A theoretical or empirical study of how the choice of penalty (R_max vs. V_max) interacts with task properties (e.g., reward scale, cost sparsity) would strengthen the paper's practical guidance.

## Novel Insights

The key insight is that enforcing state-action-wise safety constraints via reward relabeling transforms the offline safe RL problem into an unconstrained optimization that can leverage existing offline RL algorithms without Lagrangian multipliers. While reward shaping for safety is known, the specific formulation of pointwise cost-to-go constraints with a binary relabeling rule, combined with the observation that small M=K=1 updates stabilize training, is a practical and effective recipe. The paper also provides compelling evidence that CARL can learn safe policies even when the training dataset contains only unsafe trajectories—a challenging and practically relevant scenario.

## Suggestions

- Provide an analysis of why CARL fails on 3 of 11 Safety-Gym tasks. If possible, suggest conditions under which the method is likely to succeed or fail.
- Include a sensitivity study for the penalty magnitude (R_max vs. V_max vs. other values) across multiple tasks in the main paper, not just the appendix, to clarify whether this choice is indeed not a hyperparameter.

## Score and Decision

The paper presents a clean, simple, and effective approach that addresses a practically important problem (offline safe RL under tight cost budgets). The modular design and strong empirical results on most tasks make a solid contribution. However, the lack of theoretical guarantees for the practical algorithm and the inconsistent safety on some Safety-Gym tasks prevent it from being a breakthrough. The contribution is solid but not exceptional; it represents incremental but meaningful progress within a well-studied area.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>