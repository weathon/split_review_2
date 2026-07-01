## Summary

This paper proposes CARL (Constraint-aware Reward Relabeling), a simple wrapper for offline safe RL. CARL alternates between (1) updating a cost critic via off-policy evaluation and (2) updating the policy with relabeled rewards that assign a large penalty to state-action pairs whose estimated cost-to-go exceeds a threshold κ. The approach is motivated by a theoretical equivalence (Theorem 1) between a state-action-wise constrained CMDP and an unconstrained reward-relabeled problem at optimality. Empirically, CARL achieves strong safety-reward trade-offs on DSRL benchmarks, especially on Bullet tasks, and can learn safe policies even when trained exclusively on unsafe data.

## Strengths

1. **Clean theoretical anchor (Section 4, Theorem 1).** The equivalence between the state-action-wise constrained problem (Eq. 2) and the unconstrained reward-relabeled problem (Eq. 3) is proven compactly and correctly. This provides a genuine conceptual justification for the relabeling idea, distinguishing it from ad-hoc penalty tuning.

2. **Truly simple method with strong backbone generality.** CARL adds almost no machinery beyond the base offline RL algorithm: one cost critic, one relabeling step, and one policy update per batch (M=K=1). Table 2 shows it works comparably with both TD3-BC and IQL, two very different offline RL algorithms, confirming the wrapper claim.

3. **Best safety consistency on Bullet tasks (Table 1, κ=5).** CARL is the only method that satisfies the cost constraint on all 8 Bullet tasks. No other baseline (CAPS, CCAC, FISOR, CPQ, CDT, etc.) achieves this. On DroneRun specifically (C_norm=0.30), only CARL and CDT succeed while most baselines produce costs 2–15× the threshold.

4. **Impressive unsafe-data ablation (Figure 3).** Training CARL on *only* unsafe trajectories and still producing safe, reward-competitive behavior is the most striking result. On AntCircle, BallCircle, and AntVelocity, CARL generates trajectories entirely below the cost limit while maintaining high reward. This strongly suggests the relabeling mechanism genuinely reshapes the optimization landscape rather than just filtering data.

## Weaknesses

### Fatal
None.

### Major

1. **Theory-algorithm gap is insufficiently acknowledged in the paper's framing.** Theorem 1 establishes an equivalence between formulations (2) and (3) *at optimality* — it says an optimal solution to one is an optimal solution to the other. It does not address the iterative procedure with function approximation, simultaneous Q_c learning, and single-gradient-step updates (M=K=1). The gap is significant:

   - Theorem 1 assumes you know Q_c^π and uses V_max = R_max/(1-γ) as the penalty. The actual experiments use R_max (a much smaller, dataset-derived value), as stated on line 193. An ablation with V_max is deferred to the appendix.
   - The iterative sketch (Eq. 4) resembles policy iteration, but CARL is not policy iteration — each "iteration" is one minibatch gradient step, and the cost critic is updated incrementally.
   
   The paper is transparent about this on line 166 ("Formally analyzing whether K=M=1 converges... is an open problem"). However, the abstract and introduction present Theorem 1 as the theoretical foundation without caveating the disconnect between the theorem's assumptions (exact Q_c^π, V_max penalty, policy iteration-like convergence) and the actual algorithm (joint learning, R_max penalty, batch-gradient updates). This could mislead readers about how theoretically grounded the algorithm is. The authors should mark this boundary explicitly: Theorem 1 justifies the *formulation* (Eq. 3), not the *algorithm* (Algorithm 1 with M=K=1 and R_max penalty).

### Minor

2. **"Reliably enforces safety constraints" is qualified by mixed Safety Gym results.** The abstract claims CARL "reliably enforces safety constraints under small cost budgets" (line 9). On Bullet tasks this holds. But on Safety Gym tasks (κ=10), CARL is unsafe on 3 of 11 tasks: CarCircle1 (C_norm=4.15±8.93), CarCircle2 (C_norm=1.57±1.38), and CarGoal2 (C_norm=1.77±0.51). The variance on CarCircle1 is enormous (8.93), meaning some seeds produce catastrophically unsafe behavior. The paper accurately reports this in Table 1, but the headline claim in the abstract and introduction is broader than "safe on 8/11 harder tasks." The authors should qualify the "reliably" claim with the Safety Gym failure rate or provide analysis of why CARL fails there.

3. **"No additional hyperparameters" claim is slightly overstated.** The paper states that CARL "doesn't introduce any additional tunable hyperparameters" (lines 9, 23, 160, 171). In practice:
   - **M and K are design choices.** Fixing M=K=1 is defended (line 164: "we have not found values that consistently outperform CARL"), but this is still a choice that could matter in other settings.
   - **The penalty magnitude is a choice.** The main results use R_max rather than V_max from the theory. Table 5 (appendix) compares the two, but the choice is not derived from theory and could affect results.
   
   The authors should soften this to "does not introduce task-specific hyperparameters beyond the fixed choice M=K=1 and a dataset-derived penalty magnitude."

4. **Missing analysis of Safety Gym failures.** CARL is unsafe on 3/11 Safety Gym tasks but the paper offers no analysis of why. Is the cost critic inaccurate on those tasks? Do the datasets lack low-cost state coverage? Is R_max insufficient? Is the pointwise constraint too strict for those MDPs? A method paper reporting state-of-the-art results should include failure analysis to help future work understand limitations and avoid treating all failures as tuning issues.

5. **Statistical significance is weak on high-variance tasks.** Results are averaged over only 3 seeds (line 185). Several Safety Gym tasks show very large standard deviations (CarCircle1: 8.93 on a mean of 4.15; PointCircle2: 1.46 on a mean of 0.91). With 3 seeds, the reported means may not be stable. Additional seeds or bootstrapped confidence intervals would strengthen the evaluation, especially for tasks where safety status is marginal.

### Trivial
None.

## Nice-to-Haves

- A brief analysis of cost critic accuracy (e.g., correlation between Q_c and Monte Carlo returns on a held-out set) would strengthen the evaluation, since the relabeling depends entirely on Q_c being correct.
- A wall-clock time or gradient-step comparison with baselines would contextualize the "minimalist wrapper" claim.
- Ablating M and K on 2–3 tasks in the main text (rather than only the oscillation example in Figure 1) would strengthen the "no hyperparameter" argument.
- Reporting whether baselines' published hyperparameters were tuned for the specific κ=5/10 values used here would address potential fairness concerns.

## Removed Points

These points from the input review were removed with justification:

- **"Choice of OPE algorithm introduces hyperparameters."** The critic argued that FQE has its own hyperparameters (learning rate, architecture, etc.), making CARL not hyperparameter-free. This is technically true but applies to nearly any method that introduces a neural network — it is a generic criticism that does not single out CARL. The paper's claim is about *additional task-specific* tuning, and FQE hyperparameters follow standard defaults. This point is too generic to retain as a specific weakness.

- **"FISOR comparison nuance."** The critic suggested CARL and FISOR optimize different points on the Pareto frontier (CARL trades safety for reward, FISOR minimizes cost). The paper already acknowledges this (line 257: "FISOR is trained solely to minimize cost and does not adapt to different cost limits"). This is adequately addressed.

- **"Ablation of penalty magnitude in main text."** The critic requested this as a missing analysis. While a reasonable suggestion, it is a nice-to-have improvement, not a weakness — the ablation exists in the appendix (Table 5).

## Novel Insights

The most interesting finding from the review process is that CARL's strength is its simplicity, but its theoretical foundation (Theorem 1) and its practical instantiation (M=K=1, R_max penalty) are connected by an acknowledged but unbridged gap. The paper would benefit from explicitly separating "what the theory guarantees" from "what the algorithm does" rather than presenting both under the same theoretical umbrella. Additionally, the unsafe-data ablation (Figure 3) is the single most compelling piece of evidence for CARL's effectiveness — it is arguably more informative than the aggregate Table 1 results — and future work building on CARL should prioritize understanding *why* relabeling succeeds where hard filtering fails.

## Suggestions

1. Add a paragraph explicitly delineating the gap between Theorem 1 (optimality of formulation, assumes exact Q_c^π and V_max) and Algorithm 1 (batch-gradient updates, joint learning, R_max penalty).
2. Add a brief failure analysis for the three Safety Gym tasks where CARL is unsafe — even a paragraph of speculation would help readers understand the method's scope.
3. Qualify the abstract's "reliably enforces" claim to acknowledge the Safety Gym failure rate.
4. Soften the "no additional hyperparameters" claim as suggested above.

## Score and Decision

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>