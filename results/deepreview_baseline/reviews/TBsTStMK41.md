## Summary

This paper studies the problem of desk-rejection policies at AI conferences that enforce per-author submission limits. The authors formalize the current rule as an optimization problem (maximum desk-acceptance under author-level capacity constraints), relax it to a linear program, design a rounding algorithm to recover integer decisions, and evaluate the method on 11 years of real ICLR submission data. They report relative reductions in desk-rejections of up to 19.23% compared with the greedy policies currently used by venues such as CVPR and KDD.

## Strengths

* The paper identifies a real, practically important problem: current submission-limit desk-rejection policies (reject by submission ID order) are needlessly wasteful, and the paper demonstrates with real data that meaningful improvements are possible.
* The empirical evaluation covers 11 years of ICLR data with realistic submission limits, showing consistent improvements. The absolute number of additional papers saved per year is non-trivial, especially for recent large conferences (e.g., 198 fewer rejections for ICLR 2025 at b=7).
* The problem formulation is clean and the solution is simple enough that a conference could actually adopt it—the LP solver + rounding runs within a minute, which is fast enough for real-world use.

## Weaknesses

### Fatal

None.

### Major

* **The "pioneering" claim is overstated, and the technical contribution is thin.** The problem is a standard integer linear program (max Σ x_j s.t. A x ≤ b·1, x∈{0,1}^m) and the proposed method—LP relaxation + greedy rounding—is the most straightforward approach one would try. No complexity analysis, no approximation guarantee, no comparison with the true optimal integer solution (which could be obtained via branch-and-bound for many of these instance sizes). The paper essentially applies an off-the-shelf technique to a new application; the novelty lies in the application domain, not in the method itself.

* **Missing comparison with the true optimal solution.** The paper claims to "maximize desk-acceptance" and "minimize unnecessary desk-rejections," yet never establishes how close the LP+rounding solution is to the integer optimum. For small instances (ICLR 2013: 67 papers, 161 authors) the IP could be solved exactly with a modern solver. Even for larger instances, the LP upper bound is readily available, and the gap between the rounded solution and the LP optimum could be reported. Without this, the reader cannot assess whether the improvement over baselines is due to the LP+rounding being near-optimal or merely better than very weak greedy baselines.

* **The baselines are limited in scope.** FORWARDREJECT (Algorithm 2) processes papers in submission-ID order and accepts if capacity remains. The paper evaluates only this single order. Greedy algorithms with different orders (e.g., process papers with the most co-authors first, or process papers from the most prolific authors last) could perform differently. Since the proposed method is being compared in a controlled experiment, the paper should either justify why submission-ID order is the correct "state-of-the-art" baseline or compare against multiple plausible orderings to demonstrate that the LP+rounding consistently beats any greedy ordering, not just the specific one currently used.

* **No theoretical foundation for the rounding algorithm.** Algorithm 3 (MAXROUNDING) is described and its correctness (feasibility) is proved, but there is no analysis of its effect on solution quality. Since the overall algorithm is presented as a method to *minimize* rejections, the lack of any approximation guarantee or bound on the rounding-induced loss is a significant gap. The rounding is essentially a heuristic.

* **Scope/appropriateness for ICLR.** The paper is about conference organization policy and applies standard operations-research techniques. It does not contribute new knowledge to machine learning theory, algorithms, or applications. While ICLR has published meta-science papers before, this paper's contribution is primarily an empirical study of an optimization heuristic applied to desk-rejection data. The value to the ML community is indirect.

### Minor

* The paper reports "up to 19.23% relative improvement" but the absolute number of saved papers in that case (ICLR 2024, b=22) is 5 papers out of 7404 submissions—a <0.1% absolute improvement. The headline number, while technically correct, gives a misleading impression of practical impact without the absolute scale.

### Trivial

None.

## Nice-to-Haves

* A complexity proof (showing the problem is NP-hard via a reduction from maximum set packing with b=1) would strengthen the motivation for using LP relaxation and justify why a purely combinatorial algorithm is unlikely to exist.
* Comparing against a greedy baseline that removes papers from the most-overloaded author first (instead of submission-ID order) would test whether the LP+rounding method provides meaningful benefits over the best simple heuristic, not just the current policy.
* Reporting the integrality gap (LP optimum vs. best integer solution found within a time budget) would give the reader a sense of how close the LP+rounding solution is to optimal.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

Provide the gap between the LP upper bound and the rounded solution for all datasets and b values. If the gap is consistently small, it would substantially increase confidence in the method. Also, run small instances (ICLR 2013–2017) through an IP solver to confirm that the LP+rounding solution matches the global optimum.

## Score and Decision

The paper addresses a real problem with a clean formulation and solid empirical evaluation, but the technical contribution is limited to applying a standard LP relaxation + rounding approach without any theoretical analysis of solution quality. The missing comparison with the true optimal solution and the limited baselines weaken the claim that the method actually "minimizes" rejections. The paper is more suitable for an applied venue or a workshop focused on peer review infrastructure than for ICLR.

**Score: 4**

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>