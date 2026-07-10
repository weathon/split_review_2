Now let me write the final consolidated review.

## Summary

This paper studies desk-rejection policies at AI conferences that enforce per-author submission limits. It formalizes the problem of minimizing desk rejections while satisfying author-level limits as an integer program (the maximum desk-acceptance problem), proposes an LP relaxation plus rounding algorithm, and evaluates it on 11 years of ICLR submission data (2013–2025). The method consistently outperforms the greedy policies currently used at conferences, reducing desk rejections by up to 19.23% relative to the strongest baseline.

## Strengths

- **Well-motivated, practical problem.** The paper identifies a genuine issue: current desk-rejection policies at major AI conferences (CVPR, KDD, AAAI, etc.) reject papers purely by submission ID order when authors exceed limits, potentially discarding valuable work. The motivation is clearly presented (Section 1, Figure 1) and grounded in real conference policies (Table 1).

- **Useful dataset contribution.** The authors collected, cleaned, and documented 11 years of ICLR submission data from OpenReview (Table 2), covering 2013–2025 with detailed author-paper affiliation statistics. This dataset has independent value for studying conference submission patterns and can support future work on peer-review policy design.

## Weaknesses

### Major

- **Unexplained constraint discrepancy between the IP and its LP relaxation.** Definition 4.1 (the IP) uses the constraint `Ax ≤ b·1_n`, meaning each author can have at most *b* papers. Definition 4.3 (the LP relaxation) uses `Ax ≤ b − 1_n`, meaning each author can have at most *b*−1 papers (fractionally). This is a stricter constraint, and the paper provides no explanation for the difference. If it is a typo (should be `b·1_n`), it undermines the technical rigor. If it is intentional (e.g., to create rounding slack), the design rationale and its impact on solution quality must be analyzed. Either way, this is a significant omission that the authors must address.

- **No theoretical guarantee of solution quality.** Theorem 4.6 only proves feasibility (constraint satisfaction) of the rounding output. There is no approximation ratio, optimality gap, or any bound on how far the output is from the optimal solution. The paper presents the method as "maximizing" desk acceptance but provides no analysis showing that it does so effectively. This is especially problematic because the LP already uses a stricter constraint (`b−1`) than the original problem (`b`), which could systematically discard solvable papers.

### Minor

- **Contradiction between random initialization and claimed determinism.** Algorithm 4 (line 2) says "Randomly initialize x₀", but the experimental section (line 374) states "The experiments are deterministic and contain no randomness, so we report single results without variances or p-values." These statements conflict. The authors should clarify whether the initialization is actually random (in which case variance should be reported across multiple runs) or deterministic (in which case the algorithm pseudocode is misleading).

## Nice-to-Haves

- For small instances (e.g., ICLR 2013–2017 with ≤500 papers), compute the exact optimal solution using a standard IP solver and compare the LP+rounding output against it, to establish an empirical optimality gap.
- Release the code and processed dataset to facilitate reproducibility and follow-up work (the paper states code/data will be released upon acceptance).

## Removed Points

These points were raised in the input but removed after verification against the paper:

- **REMOVED (factually incorrect):** "The optimization problem is solvable exactly in polynomial time via max flow / bipartite b-matching." The reviewer's proposed flow network (source→author→paper→sink) models a different problem where each selected paper counts toward only *one* author's quota. The actual constraint `Ax ≤ b·1_n` requires each selected paper to count toward *all* its authors' quotas simultaneously. When *b*=1, the problem reduces to maximum set packing (papers must have disjoint author sets), which is NP-hard. The reviewer's claim that this is a simple max-flow problem is incorrect.

- **REMOVED (incorrect):** "The method is both slower and weaker than a standard exact solution." This follows from the erroneous claim above. Since no fast exact algorithm for the actual problem is known, the LP+rounding approach is a reasonable heuristic.

- **REMOVED (incorrect):** "Baselines are straw men." The baselines (ALLREJECT and FORWARDREJECT) are explicitly modeled on the actual policies used by conferences such as CVPR 2025, as cited in the paper. FORWARDREJECT is presented as a "more careful implementation" of current practice, which is a legitimate baseline.

- **REMOVED (unreasonable framing):** The criticism that the 19.23% improvement for ICLR 2024 at *b*=22 represents only 5 papers. This cherry-picks one cell; many entries show substantial absolute improvements (e.g., ICLR 2025 at *b*=4: 316 fewer desk-rejected papers; ICLR 2024 at *b*=7: 83 fewer). Relative improvement is a standard metric.

- **REMOVED (speculative about missing appendix):** Criticisms about missing proofs or hardness analysis that may reside in the appendix (stripped by the parser).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the constraint discrepancy** between Definition 4.1 (`b·1_n`) and Definition 4.3 (`b−1_n`). If intentional, explain the design rationale and analyze the resulting optimality gap. If a typo, correct it.
2. **Reconcile the random initialization** in Algorithm 4 with the determinism claim, or run multiple trials with variance reporting.
3. **For small instances**, compute the exact IP optimum to establish how close the LP+rounding approach gets to the optimal solution.
4. **Provide an approximation analysis** or at minimum an empirical gap analysis between the LP upper bound and the integer solution found.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>