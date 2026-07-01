## Summary
The paper proposes a data-driven method for NP-hard combinatorial optimization by parameterizing the update step of a dynamical Ising machine with a small MLP and training it via zeroth-order evolutionary optimization. The approach, called NPIM (neural network parameterized Ising machine), combines ideas from algorithm unrolling, physics-inspired Ising machines, and learning-to-optimize. Empirical results on Max-Cut, Maximum Independent Set, and Max-Clique benchmarks show competitive or state-of-the-art performance compared to both neural CO methods and classical Ising machine algorithms.

## Strengths
- **Novel combination of paradigms**: The paper is the first to apply algorithm unrolling to the NP-hard Max-Cut/Ising problem, merging ideas from dynamical Ising machines and neural CO. The specific architectural design (odd function, no bias, temporal basis functions) is well-motivated.
- **Effective training strategy**: The use of zeroth-order evolutionary optimization to circumvent vanishing/exploding gradients and noisy credit assignment in Ising machine trajectories is a practical and clever solution. The paper demonstrates that this training works even with simple MLPs.
- **Competitive empirical results**: The method achieves the best solution quality among neural CO methods on 4 out of 5 benchmarks (Table 1) and outperforms state-of-the-art Ising machines (CAC, CFC, dSBM) on most G-set Max-Cut instance types (Table 2). The analysis of learned dynamics (momentum emergence) provides useful insight.
- **Clear framework and thorough related work**: The paper carefully positions itself within the CO, Ising machine, learning-to-optimize, and zeroth-order optimization literature.

## Weaknesses
### Fatal
None.

### Major
- **Unfair comparison protocol for neural CO benchmarks**: For the results in Table 1, dNPIM uses “top 30” (30 parallel trajectories with best selected), while baselines (DiffUCO, SDDS) appear to report results from single runs or different sampling budgets. This difference could artificially inflate dNPIM’s solution quality without a commensurate increase in time (the paper notes time is larger for some instances). A controlled comparison (e.g., same number of function evaluations) is needed to support the claimed superiority.
- **Poor performance on planar G-set instances**: dNPIM’s TTS on “N=800, P, +” (planar, positive weights) is 4.42e+07, which is 24× worse than CAC (1.81e+06) and the worst among all algorithms evaluated. The paper dismisses this as a known difficulty, but it represents a significant failure mode that undermines the claim of “competitive performance on almost all problem instances.”
- **Limited out-of-distribution generalization and reliance on per-distribution training**: The method requires fine-tuning on the target distribution, and performance degrades significantly when the test distribution differs from the training distribution (Figure 3a,d). This limits practical applicability and makes the method less general than claimed. The paper acknowledges this but does not provide a solution.
- **Scalability constraints of zeroth-order training**: The training overhead grows with parameter count (Figure 4 in appendix), inherently limiting the model capacity. While the paper discusses this, it does not demonstrate that the approach can scale to solve larger or more complex problems beyond the relatively small instances tested (N ≤ 800).

### Minor
- **Loose connection to algorithm unrolling**: The paper frames the method as algorithm unrolling, but unlike classic examples (LISTA) where a fixed iterative algorithm is “unrolled” with learnable parameters, here a full neural network defines the dynamics from scratch. The connection is valid but less strong than suggested.
- **Qualitative analysis of learned dynamics**: The momentum analysis (Section 4.1) is based on a single-layer network with M=1 and is primarily illustrative. The paper does not provide rigorous evidence that the learned dynamics are meaningfully better than handcrafted Ising machines beyond raw performance metrics.

### Trivial
None.

## Nice-to-Haves
- A controlled ablation comparing dNPIM and baselines under equal computational budget (same number of trajectories, same evaluation protocol) would greatly strengthen the empirical claims.
- Additional analysis on why dNPIM fails on planar graphs and whether architecture modifications (e.g., graph-aware inputs) could resolve this would increase the paper’s impact.
- A discussion of how the method could be extended to other CO problems (e.g., TSP, SAT) with concrete steps would improve future-work guidance.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
- Conduct a controlled evaluation on the neural CO benchmarks where all methods use the same number of forward passes and the same selection strategy (single run or best-of-N).
- Include results on planar G-set instances with dNPIM after additional fine-tuning or architectural changes, or clearly qualify the claim of “competitive performance” to exclude the planar case.
- Report the variance of TTS across instances more prominently and discuss whether the method is consistently superior or only on a subset.

## Score and Decision
Score: 6. The paper presents a novel and promising synthesis of ideas, with competitive results on several benchmarks. However, the major weaknesses—particularly the unfair comparison protocol and the poor performance on planar graphs—prevent it from being a clear accept. The paper is technically sound and offers value to the community, but the empirical claims need stronger support.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>