## Summary

The paper addresses the practical problem of desk-rejection policies at AI conferences that enforce per-author submission limits. It formalizes the problem as an integer linear program that maximizes the number of papers proceeding to review while respecting per-author caps, proposes an LP-relaxation plus rounding algorithm, and evaluates on 11 years of ICLR data, reporting up to 19.23% fewer desk rejections compared to current policies. The work targets an important and timely operational issue for the community.

## Strengths

- The problem is highly relevant and timely: many top AI conferences have recently adopted per-author submission limits, and the paper articulates the negative consequences for authors (especially early-career researchers) clearly.
- Empirical evaluation uses real ICLR data over 11 years, demonstrating substantial improvements over the naive baselines currently used in practice.
- The overall structure of the paper is clear, and the pseudocode makes the algorithms easy to follow.

## Weaknesses

### Fatal

1. **The LP relaxation (Definition 4.3) is incorrect and invalidates the claimed optimality.** The integer program (Definition 4.1) has constraint \(Ax \le b\mathbf{1}_n\). The LP relaxation should be the same constraint with \(x\in[0,1]^m\). Instead, the paper uses \(Ax \le b\mathbf{1}_n - \mathbf{1}_n\) (i.e., \(b-1\) per author). This is not a relaxation of the original problem — it is a *strict tightening*. Consequently, the LP optimum can be *strictly less* than the true integer optimum, and the algorithm does not solve the intended “maximum desk-acceptance” problem. The paper never justifies this change, and it directly undermines the core claim of the method. A correct LP relaxation must keep the original right-hand side \(b\mathbf{1}_n\).

### Major

1. **No theoretical quality guarantee.** The rounding algorithm (Algorithm 3) is only shown to produce a feasible integer solution (Theorem 4.6). No approximation ratio, optimality gap, or any other guarantee is provided. Without such an analysis, it is unclear whether the algorithm actually achieves near-optimal welfare or simply beats the trivial baselines.

2. **The rounding step is underspecified and potentially inefficient.** Line 14 of Algorithm 3 says “Find the set \(S_i \subseteq (S \cap T_i)\) such that \(\sum_{j\in S_i} \tilde{x}_j \ge (1 - x_l)\).” How to find such a set efficiently (claimed \(O(k_1)\) time) is not explained. This is essentially a subset-sum-like selection problem; without further structure it may require a greedy heuristic or increase the computational cost significantly.

3. **Weak baselines and limited evaluation.** Only two baselines are compared: ALLREJECT and FORWARDREJECT (the latter being order-dependent). A stronger baseline would be the optimal integer solution (e.g., via an ILP solver for small instances) to show how far the method is from the true optimum. Additionally, because FORWARDREJECT depends on submission order, the paper should examine the effect of different orders (e.g., random or reverse) rather than assuming the official order is the strongest competitor.

### Minor

- The definition \(k_1, k_2\) is used only for runtime analysis, but the actual experiments do not measure or report these quantities.
- The paper claims “All experiments are deterministic and contain no randomness” – but the LPSOLVER might use randomness internally (e.g., initialization), and the algorithm description says “Randomly initialize \(x_0\)” (line 2 of Algorithm 4), which introduces variance. The authors should clarify or fix this.

## Nice-to-Haves

- Compare against the true LP relaxation (with constraint \(Ax \le b\mathbf{1}_n\)) to quantify the effect of the tightening.
- Provide approximation guarantees or prove that the rounding algorithm is a \((1+\epsilon)\)-approximation under certain conditions.
- Consider a more realistic experimental setup that includes the actual review-acceptance stage to show the downstream impact of fewer desk rejections.

## Novel Insights

None beyond the paper’s own contributions: the problem framing and the (flawed) LP formulation are straightforward applications of integer programming; the rounding scheme is ad-hoc. The empirical results show that current policies can be improved, but the methodological novelty is limited and the fatal error prevents the core claim from being supported.

## Suggestions

1. **Correct the LP relaxation** to use \(Ax \le b\mathbf{1}_n\) (without the \(-1\) shift). Re-run all experiments to see if the improvements hold.
2. **Provide a clear analysis** of the rounding step’s correctness and approximation factor, including how \(S_i\) is constructed efficiently.
3. **Add an optimal baseline** for small datasets (e.g., via ILP solver) to validate the algorithm’s performance relative to the true optimum.
4. **Discuss the impact of paper ordering** on the FORWARDREJECT baseline and consider reporting results with random order perturbations.

## Score and Decision

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>