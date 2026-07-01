## Summary

This paper studies the problem of desk-rejection policies at AI conferences that enforce per-author submission limits. The authors formalize the current practice as an optimization problem, propose a linear programming relaxation with a rounding scheme to maximize the number of papers that proceed to review while respecting author limits, and evaluate their method on 11 years of ICLR submission data. The method reduces unnecessary desk-rejections by up to 19.23% compared to current policies, with all computations completing within 54 seconds.

## Strengths

- **Timely and practically relevant problem**: The paper addresses a genuine and growing challenge in AI conferences—the surge in submissions and the need for desk-rejection policies. The motivation is clear and well-justified with real-world examples (CVPR, KDD, etc.).
- **Clean formalization**: The paper provides a rigorous mathematical formulation of the submission-limit problem (Definition 3.1) and the maximum desk-acceptance problem (Definition 4.1), which is a useful contribution in itself. The connection to integer programming and multi-dimensional knapsack is appropriate.
- **Strong empirical results**: The method consistently outperforms baselines across all years and submission limits where desk-rejections are needed, with improvements reaching 19.23%. The trend of larger improvements for larger conferences (ICLR 2024, 2025) is compelling and suggests practical value as submission volumes grow.
- **Efficiency**: The algorithm runs in under 54 seconds on all datasets, making it practical for real conference operations.

## Weaknesses

### Major

- **The problem is trivially solvable to optimality for the given data scale**: The maximum desk-acceptance problem (Definition 4.1) is a binary integer linear program with a totally unimodular constraint matrix. The constraint matrix \(A\) is a 0-1 matrix where each column (paper) has a small number of 1s (authors). This is a **packing problem** on a bipartite incidence matrix. For the scale of ICLR data (\(m \sim 10^4\), \(n \sim 10^4\), \(\text{nnz}(A) \sim 10^5\)), this can be solved **exactly** to optimality using standard integer programming solvers (e.g., Gurobi, CPLEX) in seconds or minutes, without any need for LP relaxation and rounding. The paper's claim that the problem "cannot be solved efficiently in general" (Section 4.2) is technically true for worst-case instances, but for the specific data at hand, exact optimal solutions are easily obtainable. The authors do not report whether they attempted to solve the integer program directly, nor do they compare the quality of their rounded solution to the true optimal solution. This is a critical omission: the paper's core algorithmic contribution (LP relaxation + rounding) may be unnecessary, and the reported "improvements" may be suboptimal compared to what an exact solver would achieve.

- **The baselines are weak and the comparison is incomplete**: The paper compares against ALLREJECT (Algorithm 1) and FORWARDREJECT (Algorithm 2). However, FORWARDREJECT is essentially a greedy algorithm that processes papers in submission order. A more natural and stronger baseline would be a **greedy algorithm that sorts papers by some criterion** (e.g., number of authors, or total "load" on constrained authors) and accepts papers greedily. Even a simple greedy that processes papers in random order would likely outperform FORWARDREJECT. The paper does not explore any such baselines, making the claimed improvements less impressive.

- **No comparison to the optimal solution**: As noted above, the paper does not report the optimal value of the integer program (Definition 4.1) for any dataset. Without this, it is impossible to know how close the proposed method is to the true optimum. The "relative improvement" metric is only relative to the baselines, not to the best possible outcome. This is a significant gap in the evaluation.

- **The rounding algorithm (Algorithm 3) is ad-hoc and lacks theoretical guarantees**: The rounding algorithm is a simple heuristic: it rounds the largest fractional value to 1, then rejects papers from the same author to maintain feasibility. There is no guarantee that this rounding preserves any approximation factor relative to the LP optimum. The paper does not provide any theoretical analysis of the rounding quality (e.g., approximation ratio). Given that the LP relaxation itself can be solved exactly, a more principled approach would be to use randomized rounding with Chernoff bounds, or to simply solve the integer program directly.

### Minor

- **The paper overclaims novelty**: The formulation as an integer program is straightforward and has been studied in other contexts (e.g., multi-dimensional knapsack, bipartite matching with capacity constraints). The paper's claim of being "one of the first formal formulations and optimization-based analyses" (Section 2) is somewhat overstated, as the problem is a standard resource allocation problem.
- **The running time analysis is superficial**: The paper reports that all results are computed within 53.64 seconds but does not provide a breakdown of time spent on LP solving vs. rounding, nor does it discuss scaling behavior for larger conferences (e.g., if submissions reach 50,000 or 100,000).
- **The paper does not discuss fairness or strategic behavior**: The current policy (reject by submission ID) is arbitrary but arguably fair in a procedural sense. The proposed optimization could be gamed by authors (e.g., creating more co-authors to increase paper count). The paper does not address these practical concerns.

### Trivial

- The paper uses "desk-acceptance" as a term, which is non-standard and slightly confusing. "Desk-accept" is not a common term in peer review.

## Nice-to-Haves

- Compare the proposed method to the exact optimal solution (solved via a commercial IP solver) to quantify the suboptimality gap.
- Explore a simple greedy baseline that sorts papers by some heuristic (e.g., number of constrained authors) to see if it matches or exceeds the LP-based approach.
- Provide a theoretical analysis of the rounding algorithm's approximation guarantee.
- Discuss potential fairness concerns and whether the optimization could be gamed.

## Novel Insights

None beyond the paper's own contributions. The paper's main insight—that the desk-rejection problem can be formulated as an integer program and solved approximately—is a useful application of known techniques to a practical problem, but it does not introduce fundamentally new algorithmic or theoretical ideas.

## Suggestions

1. **Solve the integer program exactly** using a standard solver (e.g., Gurobi, CPLEX) and report the optimal number of desk-accepted papers for each dataset and submission limit. Compare the proposed method's performance to this optimal value. If the gap is small (e.g., <1%), the rounding approach is validated. If the gap is large, the paper's claims are weakened.
2. **Add a stronger baseline**: Implement a greedy algorithm that sorts papers by the number of constrained authors (or by total "load") and accepts papers greedily. This is a natural and simple baseline that may perform competitively.
3. **Report the LP optimal value** (fractional) alongside the rounded integer value to show the quality of the rounding.
4. **Discuss the practical implications** of the optimization: Would conferences actually adopt such a policy? What are the fairness and transparency concerns? How would authors react if their paper is desk-rejected because another author's paper was prioritized?

## Score and Decision

The paper addresses a real and important problem, and the empirical results show clear improvement over current practice. However, the core algorithmic contribution (LP relaxation + rounding) is likely unnecessary for the problem scale, and the evaluation is incomplete because it does not compare to the true optimal solution or to stronger baselines. The paper would be significantly strengthened by addressing these issues. In its current form, the contribution is more of a well-executed case study than a novel methodological advance.

**Score**: 4

**Decision**: Reject

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>