## Summary

This paper proposes WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. The key innovation is a weighted cross-attention layer that integrates compatibility information while remaining adaptable to varying numbers of pools and task types. The paper also analyzes the optimality gap of list-scheduling-based methods and introduces a skip action mechanism in the single-pass setting to close this gap, supported by theoretical and empirical evidence. Experiments on TPC-H and Computation Graphs datasets demonstrate improved makespan over heuristic and neural baselines with competitive inference speed.

## Strengths

- **Novel architecture for heterogeneous scheduling**: The weighted cross-attention (WeCA) layer elegantly incorporates compatibility coefficients as attention biases, enabling the framework to adapt to arbitrary numbers of pools and task types without fixed-dimensional embeddings. This is a principled design choice that addresses a real limitation of prior work.
- **Theoretical analysis of skip action**: The paper provides a formal analysis of the optimality gap in list scheduling, establishes criteria for generation maps to achieve optimality, and shows how the proposed skip action mechanism yields a surjection that can represent optimal solutions. This theoretical grounding strengthens the method beyond purely empirical contributions.
- **Strong empirical results**: WeCAN consistently outperforms both heuristic baselines (e.g., CP, HEFT, Tetris) and neural baselines (PPO-BiHyb, One-Shot) across TPC-H and Computation Graphs datasets, often by substantial margins. Single-pass greedy inference achieves speeds comparable to heuristics while delivering significantly better makespan.
- **Ablation studies validate design**: Systematic ablation of WeCA placement, inside/outside placement, and GNN variants confirms that each component contributes meaningfully. The skip action ablation on heavy-task datasets demonstrates the practical impact of closing the optimality gap.

## Weaknesses

### Major

1. **Limited evaluation of scalability and generalization**: The experiments are conducted on instances up to 1000 tasks. While the architecture is designed to scale, the paper does not provide results on significantly larger problems (e.g., 5000+ tasks) or detailed runtime scaling analysis. The generalization experiments (Figure 2) only evaluate on TPC-H-30 variants with changes to one factor at a time; testing on entirely different problem distributions would strengthen the adaptability claim.

2. **Skip action formulation appears heuristic**: The skip score formula \(u_a(1 - \frac{k}{2n})^{u_b} + u_c\) is introduced without clear motivation beyond preventing endless idling. The paper does not analyze alternative formulations or provide guidance on why this specific parametric form is appropriate. This feels like a design choice that could significantly affect performance and whose robustness deserves more scrutiny.

### Minor

1. **Baseline recency**: The neural baselines (PPO-BiHyb 2021, One-Shot 2023) are reasonable but the field moves quickly; recent works from 2024-2025 on heterogeneous scheduling are not compared. While the paper mentions several recent references in the introduction, it does not include them as direct baselines. This slightly weakens the "state-of-the-art" claim.

2. **Training details are sparse**: The paper describes the REINFORCE objective and mentions a baseline, but does not report training time, number of gradient steps, reward curves, or hyperparameter sensitivity. This makes it harder to assess practical training cost and reproducibility.

3. **Heavy-task experiments**: The modification of TPC-H datasets by replacing 1% of tasks with "heavy tasks" is artificial. While it serves to illustrate the skip-action benefit, it is unclear how representative this is of real workloads. A more natural benchmark or analysis of where heavy tasks occur in practice would strengthen this experiment.

### Trivial

- No significant trivial issues.

## Nice-to-Haves

- A more detailed analysis of when skip actions are taken during scheduling (e.g., histogram of skip frequency) would help interpret the learned policy.
- An extension to multi-objective scheduling (e.g., makespan vs. energy or fairness) could broaden applicability.
- Providing open-source code and trained models would significantly enhance reproducibility and community adoption.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Include experiments on larger instances (e.g., 5000 tasks) with runtime breakdown to demonstrate scalability more concretely.
- Provide an ablation where the skip action is replaced by a simple learned threshold or removed entirely, to directly quantify the benefit of the parametric formula.
- Report training time and convergence behavior to help practitioners assess computational cost.

## Score and Decision

This paper makes a well-motivated technical contribution with both theoretical analysis and strong empirical validation. The weighted cross-attention design is a clean solution to the heterogeneous scheduling problem, and the skip-action analysis offers insight into a known limitation of list-scheduling approaches. The weaknesses are not fatal and can be addressed with additional experiments in a revision. The paper meets the ICLR bar for acceptance.

MY FINAL SCORE: 8.0

MY FINAL DECISION: Accept