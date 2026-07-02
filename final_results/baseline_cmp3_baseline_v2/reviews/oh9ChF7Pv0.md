## Summary

This paper introduces EGG-SR, a unified framework that integrates symbolic equivalence into symbolic regression via equality graphs (e-graphs). The framework augments three modern SR paradigms—Monte Carlo Tree Search (MCTS), Deep Reinforcement Learning (DRL), and Large Language Models (LLMs)—by using e-graphs to compactly represent equivalent expressions, enabling redundant subtree pruning in MCTS, reward aggregation in DRL, and enriched feedback in LLMs. The authors provide theoretical regret and variance guarantees and demonstrate consistent empirical improvements across multiple benchmarks.

## Strengths

- **Novel unified framework**: EGG-SR is the first work to systematically integrate symbolic equivalence via e-graphs into a broad class of modern SR algorithms, covering MCTS, DRL, and LLMs. This unification is valuable given the fragmented nature of current SR methods.
- **Theoretical contributions**: The paper proves that EGG-MCTS achieves a tighter regret bound (smaller effective branching factor) and that EGG-DRL yields an unbiased gradient estimator with strictly lower variance. These results provide principled justification for the approach.
- **Strong empirical validation**: Experiments across multiple benchmarks (trigonometric datasets, scientific cases) show consistent improvements over baselines in terms of lower NMSE, increased search tree size, and reduced variance. The comparison covers three different SR families with multiple backbone architectures.
- **Time/space efficiency analysis**: The paper convincingly demonstrates that the EGG module introduces negligible computational overhead and large memory savings compared to explicit storage, supporting practical applicability.

## Weaknesses

### Major
No major weaknesses.

### Minor

- The set of rewrite rules is manually specified and limited to common trigonometric/logarithmic identities. The paper does not discuss how to automatically expand or learn new rewrite rules, which limits generality for scientific domains with more specialized equivalences.
- The LLM experiments are smaller in scope compared to the MCTS and DRL experiments (four benchmark problems). While the results are positive, the integration with LLMs is less thoroughly validated, and the feedback mechanism is described at a high level.
- The theoretical analysis (Theorems 3.1 and 3.2) relies on certain assumptions (e.g., Markov decision process structure for MCTS, reward equivalence across equivalent sequences) that may not hold exactly in all practical settings. The proof sketches are provided, but full proofs are relegated to the appendix without detailed verification.

### Trivial
None.

## Nice-to-Haves

- Explore automatic discovery of rewrite rules from data or from mathematical knowledge bases to broaden applicability.
- Investigate inference-time use of e-graphs for MCTS and DRL (the paper focuses on training-time integration).
- Apply the framework to larger-scale scientific discovery problems (e.g., Feynman equations) with more comprehensive evaluation.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that modeling symbolic equivalence explicitly—rather than relying solely on implicit representation learning—can substantially reduce the effective search space and stabilize training in sequential generation tasks for symbolic expressions. This suggests that many existing SR methods underperform simply because they waste capacity on equivalent variants, and a lightweight equivalence-aware mechanism can remedy this without architectural changes. The theoretical variance reduction result is particularly interesting as it connects equivalence grouping to existing variance reduction techniques in reinforcement learning.

## Suggestions

1. Clarify the exact set of rewrite rules used in each experiment and provide a rationale for their selection. This would help reproducibility and assessment of domain coverage.
2. Discuss limitations more explicitly: e-graph saturation time for very deep expressions, potential failure modes when rewrite rules are incomplete, and computational cost scaling with the number of rewrite rules.
3. For the LLM experiments, include an ablation showing the impact of the number of equivalent expressions generated for the feedback prompt, and report wall-clock time overhead.

## Score and Decision

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>