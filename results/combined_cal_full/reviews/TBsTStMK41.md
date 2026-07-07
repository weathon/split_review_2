Now let me write the final consolidated review.

## Summary

This paper formalizes the problem of desk-rejecting papers at AI conferences under per-author submission limits as an integer programming problem (maximize the number of desk-accepted papers while respecting author caps). The authors propose a two-stage approach: solve an LP relaxation, then round the fractional solution to a feasible integer solution via a deterministic greedy rounding algorithm. Experiments on 11 years of ICLR data (2013–2025) show that this method reduces desk-rejections by up to 19.23% compared to current ID-order baselines (ALLREJECT, FORWARDREJECT). The work addresses a timely operational problem and offers a clean formalization.

## Strengths

1. **Well-motivated practical problem.** Table 1 documents real per-author submission limits at 7 major conferences (CVPR, ICCV, AAAI, etc.), and Figure 1 shows the 11-year ICLR submission explosion. The gap between current ID-order rejection and a principled optimization approach is clear.

2. **Comprehensive real-world evaluation.** The experiments use 11 years of ICLR data (2013–2025, excluding 2015–2016), crawled via the OpenReview API. Dataset statistics are detailed in Table 2. This gives the empirical findings substantive coverage.

3. **Consistent and concrete improvements.** The method beats both baselines across many years and b values. For ICLR 2024 at b=22, it desk-rejects 21 papers vs 26 for FORWARDREJECT and 30 for ALLREJECT — a 19.23% relative improvement. Improvements are present across multiple settings, not a single cherry-picked result.

4. **Clean formalization of existing policies.** The paper provides clear pseudocode for ALLREJECT and FORWARDREJECT, giving a precise mathematical description to what previously existed only as informal conference guidelines.

5. **Practical efficiency.** All results are computed within 53.64 seconds using a general-purpose LP solver (PuLP), confirming feasibility for real conference operation.

## Weaknesses

### Major

1. **The LP relaxation (Definition 4.3) uses an unexplained stricter constraint.** The integer program (Definition 4.1) has the constraint `Ax ≤ b·1_n` (each author may submit at most b papers). The LP (Definition 4.3) uses `Ax ≤ b - 1_n` (each author at most b-1 papers) instead of the standard relaxation `Ax ≤ b·1_n`, `x ∈ [0,1]^m`. This is strictly tighter than the original IP constraint, not a relaxation. The paper labels it a "relaxation" but offers no justification for the RHS change. While the method still produces feasible integer solutions beating the baselines, the relationship between the LP and the original problem is unclear, and the formulation could be unnecessarily conservative. This is a significant technical gap in the paper's core methodological contribution.

2. **No comparison to the optimal integer solution.** The paper compares only against the heuristic baselines ALLREJECT and FORWARDREJECT. For small years (e.g., ICLR 2013: 67 papers, 161 authors; ICLR 2014: 69 papers), the exact IP could be solved with a commercial solver to establish the optimality gap. Without this, the "up to 19.23%" improvement is relative only to simple baselines, and the distance from the true optimum is unknown. This weakens the central empirical claim.

### Minor

3. **Contradiction between claimed determinism and Algorithm 4.** Section 5.1 states "The experiments are deterministic and contain no randomness," yet Algorithm 4 begins with "Randomly initialize x₀" (line 2). While LP solvers like CBC (used by PuLP) are typically deterministic and converge to the same optimum regardless of initialization, this textual contradiction undermines the reproducibility claims. The paper should clarify how this randomness was handled.

4. **The introduction mentions "randomized rounding" but the rounding is deterministic.** Algorithm 3 (MAXROUNDING) is a deterministic greedy procedure that processes fractional variables in decreasing order. The term "randomized rounding" in the introduction (line 45) is misleading.

5. **Algorithm 3 has an underspecified step.** Line 14 says "Find the set S_i ⊆ (S ∩ T_i) such that Σⱼ∈Sᵢ x̃ⱼ ≥ (1 - xₗ)" without specifying how this set is found (e.g., greedy selection of largest fractional values, subset-sum approximation, or some other method). This is a reproducibility gap.

6. **No bound on solution quality.** The rounding algorithm's correctness guarantee (Theorem 4.6) only ensures feasibility, not any approximation factor relative to the IP optimum. The paper relates the problem to multi-dimensional knapsack (NP-hard) but provides no integrality gap analysis or approximation guarantee. While the paper's primary claim is empirical, the lack of any theoretical quality bound limits the contribution.

### Trivial

None.

## Nice-to-Haves

- Compute the optimal IP solution for small years (2013–2018) using a commercial solver and report the gap. This would substantially strengthen the evaluation.
- Consider a simple greedy baseline that sorts papers by author count (or some other criterion) for comparison, though FORWARDREJECT already serves as a natural greedy.

## Removed Points

These points appeared in the input reviews but are removed or excluded from the main weakness list for the following reasons:

- "Computational hardness claim not executed in main text": REMOVED — formal hardness proofs may exist in the appendix (stripped by the parser).
- "Headline 19.23% is cherry-picked": REMOVED — the paper accurately uses "up to"; improvements are consistent across b values for recent years.
- "No discussion of fairness": REMOVED — the Ethics Statement touches on early-career researcher impacts; comprehensive fairness analysis is beyond the paper's stated scope.
- "No comparison to simple greedy alternative": REMOVED — FORWARDREJECT is itself a greedy (by ID order); additional greedy variants would not substantively change the evaluation picture.
- "Runtime comparison to baselines is unfair": REMOVED — the runtime (≤53.64s) is acceptable for the application; comparing to millisecond baselines is not meaningful.
- "Missing related works": REMOVED — not verifiable without external sources.
- "Missing appendix content": REMOVED — the parser strips appendices; they exist in the original submission.
- "Typographical/presentation nitpicks": REMOVED — these are parser artifacts.

## Novel Insights

None beyond the paper's own contributions. The reviews surface specific technical issues (the b-1 LP constraint, lack of optimality gap, determinism contradiction) and evaluation gaps, but do not add new analytical insights beyond what the paper presents.

## Suggestions

1. **Fix the LP formulation.** Either (a) use `Ax ≤ b·1_n` in the LP (the standard relaxation) and justify why the relaxation is valid, or (b) if `b-1` is intentional, explain it as a deliberate safety margin with a clear rationale (e.g., to ensure rounding feasibility). Rerun experiments if the change affects results.
2. **Compute the optimal IP gap.** Solve the exact IP for small years (2013–2018) with a commercial solver (or branch-and-bound from the LP) and report the optimality gap.
3. **Clarify the randomness in Algorithm 4.** Either remove the random initialization (if it has no effect) or explain how it was controlled, and report statistics if randomness matters.
4. **Specify the set-selection method in Algorithm 3 line 14.** Provide the concrete procedure (e.g., "greedily take papers with largest fractional values until the sum reaches 1−xₗ").

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| bEgDEyy2Yk.md | 1.00 | R1 | No | Code implementation paper with no novelty — far weaker |
| nSDOkm0SKo.md | 1.00 | R1 | No | Unsubstantiated financial modeling — far weaker |
| C9pndmSjg6.md | 3.00 | R1 | Yes | Hybrid relaxation for MIQP; similar optimization framing but more severe flaws (no runtime, flawed comparison) |
| yYylDyLnzt.md | 3.00 | R1 | No | RL+Dantzig-Wolfe for 3D bin packing |
| o0oroLuPLZ.md | 4.60 | R1 | Yes | Decision-focused learning; stronger theoretical grounding and comparable evaluation depth |
| 9p2YMVs1Tl.md | 4.00 | R1 | Yes | ML for MILP; heavier experimental evaluation but concerns about incremental contribution |
| ghk8lnOYRq.md | 5.00 | R1 | Yes | Multi-norm formulations for k-hyperplane clustering; stronger theory |
| joMMM9eadc.md | 6.25 | R1 | No | Diffusion for IP feasible solutions; stronger methodology |
| 5t57omGVMw.md | 8.00 | R1 | No | Learning solver parameters; strong theory and experiments — far stronger |

**Bracket determination (Round 1):** The paper sits between 3.0 and 5.0. It is clearly stronger than C9pndmSjg6 (3.00), which had more fundamental issues (misunderstanding of Lagrangian relaxation, no runtime, flawed comparisons). It is weaker than ghk8lnOYRq (5.00), which provides strong theoretical foundations and rigorous experiments. It is comparable to 9p2YMVs1Tl (4.00) and o0oroLuPLZ (4.60), though with a different weakness profile: this paper has a more original problem formalization but a more significant technical flaw (the b-1 LP constraint).

**Final score: 4.0.** This reflects the paper's strengths (timely problem, clean formalization, solid empirical improvements over baselines) weighed against the two major weaknesses: (a) the unexplained deviation in the LP formulation's constraint, which affects the paper's technical core, and (b) the absence of any comparison to the true optimal solution, which leaves the optimality gap unknown. With revisions addressing these two issues, the paper could be substantially strengthened.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>