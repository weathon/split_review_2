## Summary

This paper proposes CARL (Constraint-aware Reward Relabeling), a simple wrapper for offline safe RL that alternates between estimating a cost Q-function via off-policy evaluation and relabeling rewards with a large negative penalty for state-action pairs whose estimated cost-to-go exceeds a threshold κ. The core idea is to reformulate the expected-value CMDP constraint into pointwise state-action constraints, which naturally yields an unconstrained reward-relabeling problem (Theorem 1). Empirical results on 19 DSRL tasks show CARL achieves the best safety-reward trade-off, particularly under tight cost budgets, and works across multiple backbone algorithms.

## Strengths

1. **Clean, well-motivated core idea.** The reformulation from expected-value constraints (Eq. 1) to pointwise state-action constraints (Eq. 2), and the resulting unconstrained problem (Eq. 3), is principled. Theorem 1 correctly establishes that solving Eq. 3 is equivalent to solving Eq. 2 when the true cost function is known. This provides genuine theoretical grounding for the relabeling form.

2. **No Lagrange multiplier tuning.** Prior OSRL methods (CoptiDICE, CPQ, Lagrangian variants) require tuning a Lagrange multiplier schedule, which is brittle under tight cost budgets. CARL sidesteps this entirely by fixing M=K=1 and using a dataset-derived penalty. This is a clear practical advantage.

3. **Strong and multi-faceted empirical results.** CARL is the only method safe on all 8 Bullet tasks and safe on 8/11 SafetyGym tasks (Table 1). The unsafe-data ablation (Figure 3) is a genuinely informative stress test — showing CARL can produce safe policies even when trained exclusively on unsafe trajectories is non-trivial and distinguishes the method from simple filtering. The backbone generality test (Table 2, TD3-BC vs. IQL) further supports the wrapper claim.

4. **Well-articulated instability diagnosis and fix.** Section 5 clearly identifies the oscillation failure mode when M,K are large (Figure 1), explains why it occurs, and proposes the specific M=K=1 fix. This is good engineering reasoning.

## Weaknesses

### Fatal
None.

### Major

1. **Penalty magnitude used in main results differs from what the theory prescribes, and this discrepancy is under-discussed.** Theorem 1 and Eq. 3 specify the penalty as `V_max = R_max/(1-γ)`. Line 193 states (in a single sentence): "For the main results, we set the penalty using R_max = max_{(s,a,r)} r from the offline data instead of V_max." For γ=0.99, V_max is ≈100× R_max, so the penalty used is orders of magnitude smaller than what the theory calls for. If the penalty is too small, the proof of Theorem 1 breaks — an unsafe state-action pair may still yield positive total return if future rewards are high enough. The paper mentions an ablation with V_max (Table 5—stripped appendix), so the authors are aware of the issue, but the choice of R_max for the main results with only a brief passing mention leaves the theory-practice connection unclear. This should be discussed openly in the main paper, not relegated to a table reference and a single sentence.

### Minor

1. **Theory–algorithm gap is acknowledged but understated.** Theorem 1 characterizes equivalence for a fixed policy π, whereas CARL iteratively updates π and re-estimates Q_c^π, creating a moving-target optimization. The paper honestly notes this as an open problem (line 166), but the surrounding presentation (Section 4, the iterative sketch in Eq. 4) gives the impression the theorem provides stronger algorithmic justification than it does. The paper would be clearer if it more sharply distinguished the theorem's role (justifying the relabeling form) from the iterative algorithm (motivated by analogy to policy iteration, without convergence guarantees).

2. **No analysis of OPE quality.** CARL's safety hinges entirely on whether Q_c^π(s,a) ≤ κ is correctly estimated. If the cost critic (trained via FQE) systematically underestimates costs—a real risk under distribution shift—the relabeling will fail to penalize unsafe actions. The paper provides no oracle-cost comparison, no analysis of how OPE errors correlate with safety violations, and no ablation where the cost critic is replaced with ground-truth costs. The SafetyGym results (8/11 safe) suggest OPE errors may contribute to failures on the remaining 3 tasks, but no analysis of why those specific tasks fail is given.

3. **High cost variance on at least one SafetyGym task.** On CarCircle1 (κ=10), CARL's cost is 4.15 ± 8.93. A single standard deviation above the mean (13.08) exceeds the safety threshold. When the standard deviation of cost is larger than the mean and a one-σ interval covers the unsafe region, the "safe" label based on mean cost alone is not very informative. A per-episode safety rate or a statistical test would improve reliability of the reported results.

### Trivial

- None.

## Nice-to-Haves

- **Run CARL with the theory-prescribed V_max penalty on a subset of tasks** and report whether it hurts reward or remains safe. If V_max causes performance collapse, that is informative; if it works, use it for main results. Either way, this choice should be front-and-center.
- **Provide an oracle-cost sanity check** on simpler environments where the true cost-to-go can be computed, to measure how much OPE error affects relabeling decisions.
- **Report the fraction of evaluation episodes that were safe** (not just mean cost) for tasks with high cost variance.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"No additional hyperparameters" claim is misleading (Critical Issue 3):** The reviewer argued that penalty magnitude, OPE algorithm, backbone, and M/K values are degrees of freedom. The paper's claim is defensible in a narrow sense (no new tunable scalar parameters beyond the backbone), and the penalty-magnitude concern is already covered in Weakness 1 above. Removed to avoid duplication and because it overstates the issue.

- **PointCircle2 variance example:** The reviewer claimed standard deviation crosses the safety threshold for PointCircle2 (cost 0.91±1.46, κ=10). This is factually wrong: 0.91+1.46=2.37, well below κ=10. Removed.

- **Section-by-section notes about missing Lagrangian baseline, "inherits" claim, and "embarrassingly simple" phrasing:** These are observations or stylistic preferences, not substantive weaknesses. Removed.

- **Generic / area-of-concern sweep comments** about confounders, metric proxies, etc. that lacked concrete anchors in the paper text. Removed.

## Novel Insights

None beyond the paper's own contributions. The review confirms the paper's framing: CARL is a simple, empirically effective wrapper whose main vulnerability is the discrepancy between the theory (which calls for V_max penalty) and the practice (which uses R_max). The unsafe-data ablation is the most distinctive empirical finding.

## Suggestions

- Move the V_max vs. R_max discussion from a single sentence in Section 6.2 to a dedicated paragraph (or a new subsection) in the main paper. Clearly explain why R_max was chosen, report whether V_max works (even briefly, beyond an appendix pointer), and state what this means for the theory-practice connection.
- Add a brief OPE quality diagnostic on 1–2 simple tasks: compare the learned Q_c with a Monte-Carlo estimate from rollouts, or flag state-action pairs where the cost critic's uncertainty is high.
- For tasks where cost variance is comparable to or exceeds the threshold (CarCircle1 is the clearest case), report the fraction of evaluation episodes that were actually safe.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>