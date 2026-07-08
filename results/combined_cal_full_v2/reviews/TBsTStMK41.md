Now I have everything I need. Let me compose the final consolidated review.

**Calibration Report:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Portfolio Optimization | C9pndmSjg6.md | 3.00 | R1 | Yes | Weaker than our paper — has fundamental methodology errors, no runtime reporting |
| Light-MILPopt | 2oWRumm67L.md | 5.00 | R1 | Yes | Comparable — similar strength weights but our weaknesses are less severe |
| Reoptimization Framework | scdGzuwC9u.md | 6.00 | R1 | Yes | Stronger — deeper technical contribution, more comprehensive evaluation |
| Neur2RO | T5Xb0iGCCv.md | 6.67 | R1 | Yes | Stronger — theory + experiments, more sophisticated method |
| Edge Matters | 9p2YMVs1Tl.md | 4.00 | R2 | No | Weaker — less practical impact, method not clearly differentiated |
| OptiBench | KD9F5Ap878.md | 5.00 | R2 | Yes | Comparable — similar strength weights, more severe weaknesses (-6.87 vs our -0.42) |
| k-Hyperplane | ghk8lnOYRq.md | 5.00 | R2 | Yes | Comparable — similar quality, different domain |

**Bracket (R1):** Between 3.0 and 6.0.
**Narrowing (R2):** Our strengths (7.89–10.55) are comparable to 5.0-level anchors; our most negative weakness weight (-0.42) is far milder than typical 3.0-level papers (which have -3.38 to -4.64). This places the paper cleanly around 5.0.

**Final score: 5.0** — Borderline. Genuine contribution held back by addressable technical gaps.

---

## Summary

This paper addresses a real operational problem facing AI conferences: per-author submission limits that cause desk-rejections in arbitrary submission-ID order. The authors formalize the "maximum desk-acceptance problem" as an integer linear program (Definition 4.1), propose an LP relaxation + greedy rounding algorithm, and evaluate on 11 years of ICLR data, showing consistent improvement over current policies (up to 19.23% fewer desk-rejections) with practical runtime (<54 seconds).

## Strengths

- **Timely, well-motivated problem.** Per-author submission limits are now enforced at CVPR, ICCV, KDD, AAAI, IJCAI, WSDM, and ICDE, with ICLR submissions reaching 11,672 in 2025. The paper formalizes an operational challenge that directly affects thousands of authors (Section 1, Figure 1).

- **Clean problem formalization.** Definition 4.1 formulates the maximum desk-acceptance problem as an integer linear program — maximizing the number of desk-accepted papers subject to per-author submission caps. This is, to the reviewer's knowledge, the first explicit mathematical treatment of this specific operational constraint.

- **Consistent empirical improvement over deployed baselines.** Table 3 shows that the proposed method desk-rejects fewer papers than both ALLREJECT and FORWARDREJECT in every setting where desk-rejection is needed, across all 8 reported years of ICLR data. Improvement reaches 19.23% in the best case (ICLR 2024, b=22).

- **Practical efficiency.** All results are computed within at most 53.64 seconds using a standard LP solver on commodity hardware (2 vCPUs, 13GB RAM), demonstrating deployability at scale.

## Weaknesses

### Fatal

None.

### Major

1. **The LP in Definition 4.3 uses `Ax ≤ b - 1_n` instead of `Ax ≤ b·1_n` from the IP (Definition 4.1), without explanation.** The IP (line 204) has constraint `Ax ≤ b·1_n`. The so-called "LP relaxation" (line 221) replaces this with `Ax ≤ b - 1_n`, making the RHS smaller by 1 for every author. This is not a standard relaxation — a relaxation should have a feasible set that *contains* the original's. Since `b - 1_n` is tighter than `b·1_n`, the LP's optimal value is a *lower bound* on the IP optimum, not an upper bound. The paper never justifies this choice. If the b-1 constraint is intentional (e.g., to guarantee feasibility after rounding), this needs explicit motivation and analysis of its effect on solution quality. As written, this is a structural gap: we cannot determine whether the method's results understate or overstate the potential improvement relative to a correct LP relaxation.

2. **No comparison against the exact IP optimum.** The paper compares only against ALLREJECT and FORWARDREJECT — two simple baselines that process papers in submission-ID order. Without an optimality gap — either a theoretical approximation ratio or an empirical comparison against the IP optimum (solvable via branch-and-bound for smaller instances like ICLR 2018 with 935 papers) — we cannot assess how close the LP+rounding approach comes to the optimal solution. The 19.23% figure measures improvement over naive baselines, not distance from optimal. This is the single most important missing experiment.

### Minor

3. **"Randomized rounding" claim does not match the algorithm.** The introduction (line 45) states the algorithm uses "randomized rounding," but Algorithm 3 (MAXROUNDING) is fully deterministic — it picks the largest fractional value, rounds to 1, and zeros out conflicting papers. The experiments section (line 374) correctly states "The experiments are deterministic and contain no randomness." This mismatch should be corrected.

4. **Baselines are weak for establishing the method's broader value.** FORWARDREJECT and ALLREJECT are the actual policies used by conferences, so the comparison is valid for the paper's stated claim of outperforming current policy. However, the paper would be stronger by also comparing against a simple sorted-greedy baseline (e.g., sort papers by decreasing number of co-authors before running the forward algorithm). This would isolate whether the LP formulation, rather than any intelligent ordering, drives the improvement.

### Trivial

None.

## Nice-to-Haves

- Compare against the IP optimum on small instances (e.g., ICLR 2018) via branch-and-bound to establish an optimality gap.
- Add a simple sorted-greedy baseline (e.g., sort papers by decreasing number of co-authors) to demonstrate the specific value of the LP formulation.
- Analyze which papers get preserved (e.g., do early-career researchers benefit disproportionately, as the ethics statement suggests?).
- Discuss the trade-off between fewer desk-rejections and the resulting increase in reviewer burden.
- Ablate different rounding strategies (e.g., random order, fewest co-authors first) to show robustness of the chosen greedy rounding.

## Removed Points

These points are flagged to be removed, treat them with caution:

- Criticism about code/data "will be made publicly available upon paper acceptance" reducing verifiability — removed per hard rule against questioning release status.
- Criticism about missing related work — removed per hard rule (cannot confirm external context).
- Criticism about Remark 4.4's runtime complexity bound "adding little" — removed as subjective judgment, not a weakness.
- Strength about "addressing an important problem" — removed per filtering instruction (generic/superficial).
- Various section-by-section notes that are presentation nits or restate issues already covered.

## Novel Insights

None beyond the paper's own contributions. The review confirms that the problem formalization is the paper's main contribution; the technical weaknesses (unexplained b-1 constraint, missing optimality gap) are genuine but not fatal — they reduce the strength of the contribution rather than invalidating it.

## Suggestions

1. **Clarify the b-1 constraint.** Either justify why `b-1` is used as the RHS in the LP (e.g., as a deliberate slack for the rounding algorithm to ensure feasibility) or correct it to `b` and reassess the results. This is the most important technical fix.

2. **Compute an optimality gap.** Solve the IP exactly via branch-and-bound for the smallest instance (ICLR 2018, 935 papers) and report how far the LP+rounding solution is from optimal. Even a partial comparison would substantially strengthen the paper's evidence.

3. **Correct the "randomized rounding" language** in the introduction to match the deterministic algorithm.

4. **Add a sorted-greedy baseline** to help isolate whether the LP formulation or simply using any intelligent ordering drives the gains.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>