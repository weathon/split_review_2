## Summary

This paper proposes WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. The method uses a weighted cross-attention encoder to capture environment information while maintaining adaptability across varying numbers of pools and task types, and a longest-directed-distance GNN for dependency embedding. It achieves single-pass network inference with a generation map that includes a novel skip-action mechanism, theoretically closing the optimality gap inherent in list-scheduling-based methods. Experiments on TPC-H and Computation Graphs datasets show significant improvements over heuristics and state-of-the-art neural schedulers, with inference speeds comparable to heuristics.

## Strengths

- **Novel architecture for heterogeneous scheduling**: The weighted cross-attention (WeCA) layer is a principled design that integrates compatibility coefficients as multiplicative biases outside softmax, preserving adaptability to varying numbers of pools and task types while capturing fine-grained task-pool interactions. This is a clear improvement over fixed-size embedding approaches in prior work.
- **Theoretical analysis of optimality gap and skip action**: The paper formally analyzes why list-scheduling maps cannot represent optimal solutions and proves (Theorem 1) that their single-pass framework with skip action can embed all feasible orders including optimal ones. This provides a solid theoretical foundation for the skip mechanism, which is often heuristically motivated in the literature.
- **Strong empirical performance**: WeCAN consistently outperforms strong baselines (HEFT, Tetris, PPO-BiHyb, One-Shot) on two diverse datasets. Improvements over the best neural baseline reach 7.7% (TPC-H) and 9.5% (Computation Graphs). The greedy variant also achieves runtime comparable to heuristics, demonstrating practical efficiency.
- **Thorough ablation studies**: The ablations systematically validate each component—WeCA placement (outside vs. inside softmax), LDDGNN vs. GAT variants, and the skip-action mechanism on heavy-task datasets. Results confirm the contribution of each design choice.
- **Generalization to varying environments**: Figure 2 shows that WeCAN trained on a fixed environment generalizes well to changes in pool count, pool type, task count, and task type, outperforming One-Shot by a large margin.

## Weaknesses

### Fatal
None.

### Major
- **Skip score formula is heuristic**: The skip score is defined as \( u_a(1 - \frac{k}{2n})^{u_b} + u_c \). While the paper shows that there *exist* scores that enable optimal solutions (Theorem 1(iv)), the specific parametric form with exponential decay is empirically motivated rather than derived. The choice of the decay rate and the clipping of \(k/2n\) are not justified beyond preventing endless idling. It would strengthen the paper to compare with simpler alternatives (e.g., constant skip score with static penalty).
- **Lack of ablation on skip action for regular datasets**: The skip action is evaluated only on heavy-task variants of TPC-H (Figure 3). It is unclear whether including the skip action negatively affects performance on normal datasets where list scheduling may already be near-optimal. The paper should show results with and without skip on the standard TPC-H and Computation Graphs benchmarks to confirm no degradation.

### Minor
- **Terminology "end-to-end" overclaimed**: The network produces scores, but the schedule is constructed via a generation map (list-scheduling with skip). This is common in neural scheduling, but the term "end-to-end" could be misconstrued as direct mapping from problem instance to schedule. Clarification would help.
- **Baseline comparison details**: One-Shot (Jeon et al., 2023) also uses a single-pass network but generates priorities via Gumbel-TopK. The paper does not discuss how the generation maps differ beyond skip actions, making it harder to attribute improvements solely to the architecture. A more detailed comparison of the action spaces and maps would be beneficial.

### Trivial
- Some notation inconsistencies: \(\rho(v)\) is used for both resource demand and task attributes across different sections.
- Figure 1 contains duplicated captions due to extraction artifacts.

## Nice-to-Haves

- Empirical analysis of training variance with and without skip actions, to support the claim that skip clusters poor solutions in high-\(u_a\), high-\(u_c\) regions.
- Additional experiments on larger-scale problems (more than 1000 tasks) or with more than 3 pools to further demonstrate scalability.
- Comparison with a version that uses an auto-regressive decoder to isolate the benefit of single-pass efficiency.

## Novel Insights

Beyond the paper's own contributions, the insight that list scheduling’s optimality gap arises from the non-surjectivity of the \(TS_{list}\) map and that a single well-designed skip action can restore surjectivity without multi-round computation is valuable. The design of placing compatibility coefficients outside the softmax to preserve task-level differentiation in embeddings is a subtle but important architectural choice that could inspire similar approaches in other heterogeneous assignment problems.

## Suggestions

- Compare skip and no-skip variants on the standard (non-heavy) benchmarks to rule out any negative side effects.
- Provide a more detailed justification for the exponential decay form of the skip score, or include an ablation comparing different functional forms.
- Discuss the computational overhead of the skip action in the generation map relative to standard list scheduling, especially in terms of the number of additional iterations.

## Score and Decision

**Score**: 8  
**Decision**: Accept  

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>