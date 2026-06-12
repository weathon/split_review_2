## Summary

This paper proposes a data-driven approach to combinatorial optimization by learning the parameters of an iterative dynamical system (Ising machine) for solving the NP-hard Max-Cut/Ising problem. The authors parameterize the update step of an Ising machine with a small MLP, use zeroth-order evolutionary optimization for training, and demonstrate competitive performance against both neural CO methods and classical Ising machine algorithms on standard benchmarks including G-set instances and MIS/Max-Cut problems.

## Strengths

- **Novel combination of techniques**: The paper successfully bridges algorithm unrolling, dynamical Ising machines, and zeroth-order optimization in a way that is genuinely novel for the NP-hard combinatorial optimization setting. This cross-pollination of ideas from different subfields is creative and well-motivated.

- **Competitive empirical results**: The method achieves state-of-the-art or competitive performance across multiple benchmarks. On G-set instances (Table 2), dNPIM outperforms CAC, CFC, and dSBM on 4 out of 5 instance types. On neural CO benchmarks (Table 1), dNPIM achieves the best solution quality on 4 out of 5 problem categories compared to DiffUCO and SDDS.

- **Clear analysis of learned dynamics**: Section 4 provides insightful analysis, particularly the demonstration of emergent momentum in single-layer networks (Figure 2) and the comparison between continuous (cNPIM) and discrete (dNPIM) coupling variants. The discussion of overfitting differences between cNPIM and dNPIM (Section 4.5) is thoughtful and reveals meaningful algorithmic insights.

- **Well-motivated training approach**: The authors provide a clear rationale for using zeroth-order optimization instead of backpropagation or policy gradients, citing vanishing/exploding gradients and reward attribution problems in long trajectories. This methodological choice is justified both conceptually and with reference to appendix results.

## Weaknesses

### Major

- **Limited architectural exploration and scalability concerns**: The paper uses only a two-layer MLP with tanh activations and a specific Fourier basis for temporal modulation. While the authors claim simplicity as a virtue, the method's ability to scale to more complex problems or larger parameter counts is questionable. The zeroth-order optimization method's overhead with increasing parameters (acknowledged in Section 6) is a genuine limitation that could prevent the method from learning more sophisticated dynamics needed for harder problem classes.

- **Incomplete comparison with neural CO baselines**: Table 1 compares against results from Sanokowski et al. (2025), but the paper does not include comparisons with other important neural CO methods for Max-Cut such as GNN-based approaches (Schuetz et al., 2022), G-flow nets (Zhang et al., 2023), or other diffusion-based methods. The comparison is limited to a single recent paper's results, which weakens the claim of "state-of-the-art" performance in neural CO.

- **Training distribution dependence and generalization**: The method requires fine-tuning on problem-specific distributions (Section 4.4), and performance degrades significantly when the test distribution differs from training. The bootstrapping procedure (training on easier instances first) is necessary but adds complexity. The paper does not provide clear guidelines on how to select training distributions or how much fine-tuning data is needed for new problem types.

### Minor

- **Time-to-solution metric limitations**: The TTS metric in Table 2 is reported in "number of iterations" rather than wall-clock time, which makes direct comparison with practical implementations difficult. While the authors argue the matrix-vector product is the bottleneck, this ignores implementation-specific optimizations that could favor one algorithm over another.

- **Limited analysis of failure cases**: The paper notes that dNPIM struggles on unweighted planar G-set instances (Table 2) but does not provide analysis of why this occurs or what architectural changes might help. Understanding failure modes would strengthen the paper's contribution.

### Trivial

- The paper uses "state-of-the-art" somewhat loosely given the limited comparison set and the fact that some baselines (e.g., Gurobi with long runtimes) still achieve better solution quality on some instances.

## Nice-to-Haves

- An ablation study showing the contribution of each component (temporal basis, hidden layers, noise injection) to overall performance would strengthen the architectural understanding.
- A discussion of how the method might be extended to constrained optimization problems beyond quadratic binary optimization (e.g., TSP with permutation constraints) would increase the paper's impact.
- Wall-clock time comparisons on the G-set benchmarks would make the results more practically relevant.

## Novel Insights

The paper's key insight is that the dynamics of Ising machines can be effectively learned from data using a surprisingly simple parameterization (small MLP with temporal modulation) and zeroth-order optimization. The emergence of momentum-like behavior from pure reward maximization (Figure 2) provides a concrete example of how learned optimization dynamics can rediscover and potentially improve upon hand-designed heuristics. The contrast between continuous and discrete coupling variants (cNPIM vs. dNPIM) reveals an interesting trade-off between average-case performance and robustness on hard instances, suggesting that the choice of relaxation matters significantly for learned optimizers in discrete settings.

## Suggestions

- Expand the neural CO baseline comparisons to include more methods (GNN-based, GFlowNets, other diffusion approaches) to substantiate the "state-of-the-art" claim.
- Provide wall-clock time comparisons for the G-set benchmarks in addition to iteration-based TTS.
- Include an analysis of how the method performs on instances with different structural properties (e.g., sparsity, community structure) to better characterize when the learned dynamics are effective.

## Score and Decision

The paper presents a novel and well-executed approach that combines ideas from algorithm unrolling, Ising machines, and zeroth-order optimization. The empirical results are competitive across multiple benchmarks, and the analysis of learned dynamics provides meaningful insights. However, the limited comparison with neural CO baselines and the scalability concerns with the zeroth-order optimization method prevent this from being a strong accept. The paper makes a solid contribution to the field and deserves acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>