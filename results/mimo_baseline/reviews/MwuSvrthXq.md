## Summary
This paper proposes WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. The framework combines a weighted cross-attention (WeCA) layer for encoding compatibility information with a longest-directed-distance GNN for dependency structure, generates solutions via single-pass network inference, and introduces a skip-action mechanism in the list-scheduling generation map to close the inherent optimality gap. Theoretical analysis characterizes this gap, and experiments on TPC-H and Computation Graphs datasets demonstrate state-of-the-art makespan with competitive inference speed.

## Strengths
- **Novel and principled skip-action mechanism**: The paper identifies a genuine theoretical limitation of list-scheduling-based generation maps (they cannot represent all optimal solutions) and proposes a clean solution by enlarging the feasible reduced space with skip actions. Theorem 1 guarantees feasibility within 2n steps, surjectivity onto optimal solutions, and that without skip actions surjectivity fails for some problems. This is a meaningful theoretical contribution.
- **Effective handling of compatibility coefficients via WeCA**: The weighted cross-attention design elegantly integrates K_acc as attention bias outside the softmax, preserving adaptability across varying numbers of pools and task types without fixed-dimensionality constraints. The ablation in Table 3 strongly validates this design—the "inside" placement variant and removing WeCA layers both degrade performance significantly (e.g., from 14.0% to 10.5% improvement on TPC-H-30).
- **Strong empirical results with practical efficiency**: WeCAN-greedy achieves up to 18.1% makespan improvement over the best heuristic on TPC-H while running at comparable speed (e.g., 0.15s vs 0.18s for HEFT on TPC-H-30). The generalization experiments in Figure 2 demonstrate robustness across varying pool counts, pool types, task counts, and task types under fixed training conditions.
- **Comprehensive ablation and validation of skip action**: The heavy-task experiments (Figure 3) convincingly demonstrate that list scheduling has a practical optimality gap—HEFT outperforms the best list-scheduling approach (CP)—and that WeCAN's skip action closes this gap, achieving 8.3% and 8.9% improvement on TPC-H-30-heavy and TPC-H-50-heavy respectively.

## Weaknesses
### Fatal
None.

### Major
- **Non-autoregressive decoder limits expressiveness**: The decoder computes all action probabilities from the initial state alone ($p_\theta(\pi_l | s_1)$), meaning the policy cannot adapt its scores as the schedule unfolds. While the paper mentions a comparison in Appendix B, this is a fundamental architectural limitation for sequential decision-making problems. For complex scheduling scenarios with many interacting constraints, the inability to condition on the evolving state could limit solution quality, especially compared to autoregressive alternatives that can adapt during construction.
- **Skip action formula is somewhat ad-hoc**: The specific form $u_{\pi_{skip}} = u_a(1 - \frac{k}{2n})^{u_b} + u_c$ is designed to prevent endless idling while maintaining single-pass efficiency, but the functional form lacks deep justification. The decay term $(1 - \frac{k}{2n})$ and the exponents $u_b$ are motivated intuitively, but alternative formulations could achieve similar goals. The paper does not compare against other skip-action designs, making it unclear whether this specific form is optimal or merely adequate.

### Minor
- **Baseline coverage**: The comparison includes two RL baselines (PPO-BiHyb, One-Shot) but does not compare against more recent heterogeneous RL scheduling methods like SpotDAG (Lin et al., 2024), which is cited in the introduction. This would strengthen the empirical claims.
- **REINFORCE variance**: Using vanilla REINFORCE with average-reward baseline is a simple choice. For a paper that emphasizes practical efficiency, the training convergence behavior and comparison with lower-variance alternatives (e.g., PPO, critic-based baselines) would strengthen the work, particularly for large-scale instances.
- **Limited scale diversity**: While the computation graphs have 500 tasks and TPC-H goes up to ~1000 tasks, real-world data center scheduling often involves much larger DAGs. The paper claims scalability but does not test beyond 1000 nodes in the main results.

### Trivial
None.

## Nice-to-Haves
- A visualization or analysis of the learned skip-action behavior (e.g., how often skip is chosen, when it tends to occur during scheduling) would provide insight into how the mechanism works in practice.
- Analysis of how the non-autoregressive assumption impacts performance as problem scale increases, potentially with an adaptive variant.
- Comparison with MILP solvers on small instances to understand the optimality gap relative to exact solutions.

## Novel Insights
The identification and formal characterization of the optimality gap in list-scheduling-based generation maps is a genuinely useful theoretical contribution. The paper shows that list scheduling maps multiple reduced-space points to the same schedule, creating a many-to-one mapping that excludes optimal solutions for certain problem instances. The construction of a surjection via skip actions that clusters poor solutions in identifiable regions of the parameter space (high-$u_a$, high-$u_c$) is a clever design that simultaneously enables optimality and aids training. This analysis applies beyond the specific WeCAN framework and could guide future neural scheduler designs.

## Suggestions
- Compare with more recent heterogeneous RL scheduling baselines (e.g., SpotDAG) and potentially with MILP solvers on small instances for reference.
- Provide training convergence curves and analysis of REINFORCE variance versus alternatives.
- Investigate adaptive or learned skip-action formulations and compare with the proposed fixed-formula approach.
- Extend experiments to larger scales (2000+ tasks) to better validate scalability claims.

## Score and Decision
The paper makes a solid contribution to an important practical problem area. The WeCA architecture is well-designed and validated, the theoretical analysis of list-scheduling's optimality gap is a genuine contribution, and the skip-action mechanism is both novel and effective. The experiments are comprehensive with strong results and good ablations. The non-autoregressive decoder and ad-hoc skip formula are limitations but do not invalidate the contributions. This paper sits in the range of a good, incremental contribution that advances the field.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>