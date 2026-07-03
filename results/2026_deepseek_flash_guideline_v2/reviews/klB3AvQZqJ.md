## Summary

This paper proposes CARL (Constraint-Aware Reward Relabeling), a minimalist wrapper for offline safe reinforcement learning. CARL alternates between estimating a cost Q-function via off-policy evaluation and relabeling rewards with a large negative penalty for state-action pairs whose estimated cost-to-go exceeds the budget κ. The method wraps around any batch-update offline RL algorithm (demonstrated with TD3-BC and IQL), requires no Lagrangian multiplier tuning, and introduces no tunable hyperparameters beyond the backbone's own. Empirical evaluation across 19 DSRL benchmark tasks shows CARL achieves the most consistent safety across tasks among existing methods, including learning safe policies from entirely unsafe data.

## Strengths

1. **Consistent safety across a large benchmark.** Table 1 shows CARL is the *only* method that satisfies the cost constraint on all 8 Bullet Gym tasks (κ=5) and is safe on 8/11 Safety Gym tasks (κ=10). No baseline—including FISOR, CCAC, CAPS, or CDT—achieves comparable breadth of constraint satisfaction.

2. **Zero-additional-hyperparameter design with stability diagnosis.** The paper identifies an oscillation failure mode (Figure 1, Section 5.1) when cost Q-function and policy updates are too aggressive. Setting M=K=1 (one OPE + one OPO step per batch) eliminates this instability and introduces no tunable hyperparameters. The paper honestly acknowledges convergence analysis remains an open problem.

3. **Backbone-agnostic generalization.** Table 2 confirms CARL works comparably with both TD3-BC and IQL, which use fundamentally different update mechanisms (actor-critic with BC regularization vs. advantage-weighted regression). This supports the claim that the relabeling mechanism is algorithm-agnostic.

4. **Recovery from purely unsafe data.** Figures 3 demonstrate that CARL trained exclusively on trajectories exceeding the cost limit learns safe policies with strong reward (e.g., AntVelocity reaches ~3000 reward while staying within budget). This ablation isolates the effect of reward relabeling and is arguably the paper's strongest empirical finding.

5. **Scalable safety under relaxed budgets.** Figure 2 shows that on CarCircle2—where all baselines are unsafe at κ=10—CARL becomes safe and achieves higher rewards as the budget increases to 40 or 80, demonstrating it exploits larger budgets rather than collapsing to a fixed conservative solution.

## Weaknesses

### Fatal
None.

### Major

1. **The proof of Theorem 1 contains a logical gap.** The proof attempts to show that any solution to the unconstrained problem (3) must satisfy the pointwise safety constraints of problem (2). It assumes that \(\tilde{\pi}^*\) (a solution to (2)) has positive value under the relabeled reward \(r_{\pi^*}\) because \(\tilde{\pi}^*\) is safe. However, \(r_{\pi^*}\) penalizes actions based on \(Q_c^{\pi^*}\) (the cost Q-function under \(\pi^*\)), not \(Q_c^{\tilde{\pi}^*}\). Safety of \(\tilde{\pi}^*\) under (2) guarantees \(Q_c^{\tilde{\pi}^*}(s, \tilde{\pi}^*(s)) \leq \kappa\) for all \(s\), but does **not** guarantee \(Q_c^{\pi^*}(s, \tilde{\pi}^*(s)) \leq \kappa\), which is what would be needed for \(\tilde{\pi}^*\) to avoid penalties under \(r_{\pi^*}\). The theorem may still be true, but the proof as presented is incomplete. This weakens the claimed theoretical justification for the unconstrained formulation. (Lines 93–95)

### Minor

2. **Failure cases on 3 Safety Gym tasks are unanalyzed.** CARL is unsafe on CarCircle1 (C_norm=4.15), CarCircle2 (C_norm=1.57), and CarGoal2 (C_norm=1.77). The paper notes "8 out of 11" but provides no analysis of what distinguishes these tasks. For a safety paper, understanding whether these failures stem from function approximation errors, dataset coverage issues, or fundamental limitations of the pointwise formulation is important for users deciding when to apply CARL. (Lines 225–232)

3. **Empirical framing overstates the reward-safety balance.** The paper claims CARL "strikes a strong balance between reward maximization and constraint satisfaction." While CARL achieves the most consistent safety, on several tasks other safe methods achieve substantially higher reward (e.g., DroneRun: CDT reward 0.58 vs CARL 0.36; AntRun: FISOR reward 0.43 vs CARL 0.36; PointGoal1: BC-Safe reward 0.22 vs CARL 0.06; SwimmerVelo: BC-Safe reward 0.46 vs CARL 0.21). The paper would benefit from a more precise characterization—CARL is the safest method, but at the cost of being conservative on some tasks.

4. **Problem (2) may not have a solution in practice.** Theorem 1 requires "Assume there exists a solution to Problem (2)," but the pointwise constraint \(Q_c^\pi(s, \pi(s)) \leq \kappa\) for all states simultaneously is strong and may not be satisfiable in many MDPs. The paper does not discuss when this assumption is violated or what happens empirically in such cases. (Lines 81, 91)

5. **Ablation on (K,M) values is limited.** The paper states "we have not found values that consistently outperform CARL across benchmarks" but does not report what values were tried or show results. Reporting performance for a few configurations (e.g., (K,M) ∈ {(1,1), (5,5), (10,10)}) would substantiate the claim. (Line 164)

### Trivial
None.

## Nice-to-Haves
- The gap between the discounted-cost formulation in problem (1) and the undiscounted cumulative-cost evaluation metric could be acknowledged, though this is common in the OSRL literature.

## Removed Points
These points are flagged to be removed; treat them with caution.

- **Criticism about "V_max inequality in proof not justified":** The critic claimed the inequality "< 0" was unjustified. In fact, with \(V_{\max} = R_{\max}/(1-\gamma)\), we have \(-V_{\max} + \sum_{t=1}^\infty \gamma^t R_{\max} = -R_{\max} < 0\), so the inequality holds straightforwardly. **Removed as factually incorrect criticism.**

- **Criticism about "no additional tunable hyperparameters" being overstated:** The critic claimed the penalty magnitude (R_max vs V_max) is a tunable hyperparameter. However, R_max is deterministically derived from the data, not tuned across values, and the paper includes an ablation (Table 5, appendix) comparing the two choices. **Removed as it misreads the claim.**

- **Weakness about CarGoal2 as a case where CARL is safe but conservative:** The critic included CarGoal2 (reward 0.13) in the list of tasks "where CARL is safe" with low reward. In fact, CARL is unsafe on CarGoal2 (C_norm=1.77 > 1). This is a factual error. **Removed as factually incorrect.**

- **Strength about "Theorem 1 proving formal equivalence":** Given the proof gap identified above, claiming this as a confirmed strength is premature. The formulation remains well-motivated algorithmically, but the theorem should not be presented as established. **Downgraded from strength.**

- **Strength about "safe across all Bullet tasks, safe on 8/11 Safety Gym tasks":** Though factually correct, the critic's point about reward conservatism on some tasks tempers this. The strength is kept as "consistent safety across a large benchmark" above, which is accurate.

## Novel Insights

None beyond the paper's own contributions. The key insight—that reward relabeling with a large data-derived penalty based on estimated cost-to-go can serve as a hyperparameter-free wrapper for offline safe RL—is clearly stated in the paper.

## Suggestions

1. **Fix or remove the flawed proof of Theorem 1.** If the theorem is true, provide a correct proof. If the proof cannot be fixed, state the result as a conjecture with intuitive justification. A wrong theorem is worse than no theorem.

2. **Analyze the 3 Safety Gym failure cases** (CarCircle1, CarCircle2, CarGoal2). Understanding whether failures stem from function approximation error in the cost Q-estimate, dataset composition, or fundamental limitations of the pointwise formulation would provide actionable guidance for practitioners.

3. **Report ablation results for different (K,M) values** to substantiate the claim that M=K=1 is consistently the best choice.

4. **Temper the empirical framing** to more accurately reflect the reward-safety trade-off: CARL achieves the most consistent safety across tasks, but on several tasks it is more conservative than the best safe alternative.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>