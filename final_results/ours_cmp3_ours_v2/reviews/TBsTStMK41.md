Here is my final consolidated review.

## Summary

This paper studies the problem of desk-rejection policies at large AI conferences that enforce per-author submission limits. Current practice (reject excess papers by submission-ID order) is wasteful. The authors formalize the optimal desk-rejection problem as an integer program (maximizing papers forwarded to review subject to per-author limits), propose a two-stage method (LP relaxation + deterministic rounding), and evaluate on 11 years of ICLR data (2013–2025). The method consistently reduces desk-rejections compared to greedy baselines, with relative improvements up to 19.23%, and runs in under 54 seconds on all instances.

## Strengths

1. **Well-motivated, timely problem.** The growth of AI conference submissions (ICLR: 67→11,672) and resulting per-author submission limits create a genuine administrative burden. The paper correctly identifies that current ID-order policies are unnecessarily wasteful — a real operational problem affecting thousands of authors annually.

2. **Clean problem formulation.** Definition 4.1 (maximum desk-acceptance submission limit problem) is a simple, natural IP. The objective (maximize papers forwarded) and constraints (per-author limits) directly capture the relevant trade-off. This formalization is itself a useful contribution that clarifies what a "better" desk-rejection policy looks like.

3. **Thorough data collection and consistent empirical improvement.** The authors crawled 11 years of ICLR submission data from OpenReview. Across 8 years of data (2018–2025) and b=4 to b=25, the proposed method never desk-rejects *more* papers than either baseline, and frequently rejects fewer. The improvements are modest but consistent, suggesting real slack in current greedy policies.

4. **Practical efficiency.** All results are computed within at most 53.64 seconds using standard LP solvers, making the approach feasible for real conference operations.

## Weaknesses

### Fatal
None.

### Major

1. **The LP "relaxation" uses b−1 instead of b without justification, making it a restriction.** The original IP (Definition 4.1) has constraint `Ax ≤ b·𝟙_n`. The LP in Definition 4.3 uses `Ax ≤ (b−1)·𝟙_n`. This tightens each author's limit by 1, producing a feasible region that is a *subset* of the original IP's feasible region (after integrality relaxation). The LP therefore gives a *lower bound* on the IP optimum, not an upper bound — it is not a relaxation in the standard sense. The paper never justifies this choice, never compares against the untightened LP (with b), and never analyzes how much performance is lost by this tightening. If the standard LP (with b) were used, a simple LP solver might produce better solutions without any rounding, but this is never tested. This is a significant methodological gap that undermines the technical framing of the contribution.

2. **The rounding algorithm (Algorithm 3, line 14) is underspecified.** The key step states: "Find the set S_i ⊆ (S ∩ T_i) such that ∑_{j∈S_i} x̃_j ≥ (1 − x_l)" and claims O(k₁) time. The paper does not specify *how* this set is found — whether by greedy selection (largest fractional values first), exhaustive search, or some other procedure. Different selection strategies could affect solution quality, and no analysis of the rounding procedure's properties is provided. As written, this step is not reproducible.

### Minor

3. **No comparison against the standard LP relaxation (with b) as an optimality upper bound.** With b−1 in the LP, the method's true distance from optimality is unknown. Solving the standard LP (with b) would provide a valid upper bound on the IP optimum and let readers assess how much room for improvement remains. The paper evaluates only against greedy baselines, which is insufficient to quantify absolute optimality.

4. **"Randomized rounding" claim does not match the deterministic algorithm.** The introduction (line 45) states the method uses "randomized rounding," but Algorithm 3 is entirely deterministic. This is a minor inconsistency in presentation.

5. **No approximation guarantee for the rounding algorithm.** The paper proves correctness (feasibility) but provides no approximation ratio, optimality gap, or quality analysis. For a paper whose claimed contribution is an optimization-based method, some discussion of solution quality relative to optimal would strengthen the work.

6. **Relative improvements can be more informative with absolute numbers.** The headline "19.23%" (ICLR 2024, b=22) corresponds to an absolute reduction of 5 desk-rejected papers (26→21). While the relative percentage is correct, reporting only the relative figure can inflate perceived practical impact in cases where the baseline rejection count is small. Reporting both would give a more complete picture.

### Trivial

7. **Author-level fairness is not analyzed.** The paper advocates for "author welfare" but never examines which authors benefit or lose — e.g., whether the optimization systematically favors authors with more co-authors or concentrates rejections on a small subset. This analysis would strengthen the ethics claims.

## Nice-to-Haves

- Sensitivity analysis of the FORWARDREJECT baseline to submission-ID order (tie-breaking).
- Discussion of generalization to other conferences with different authorship norms (e.g., high-energy physics vs. ML).

## Removed Points

These points are flagged to be removed. Treat them with caution.

- **Critical Issue 1 (Structural): "The problem is a maximum bipartite b-matching, solvable optimally as a linear program — the LP relaxation + rounding is unnecessary."** REMOVED because it is factually incorrect. The constraint matrix A (n×m) is the *biadjacency* matrix of the authors-papers bipartite graph, *not* the node-edge incidence matrix. A column of A can have many 1's (multiple co-authors per paper), meaning the matrix is NOT necessarily totally unimodular. A concrete counterexample: for 3 authors and 3 papers with authorship pattern [[1,1,0],[1,0,1],[0,1,1]], the 3×3 submatrix has determinant −2, violating TU. The problem is therefore *not* equivalent to a standard bipartite b-matching, and the LP relaxation does not guarantee integer solutions. The paper's claims about computational hardness and the need for rounding are valid.

- **Corresponding "Strengthening" suggestions that rely on the TU claim.** REMOVED because they are based on a misunderstanding. The suggestion "Drop the b−1 tightening — the standard LP (with b) gives a global optimum and no rounding is needed" is wrong because A is not TU.

- **Criticism that the 19.23% number is "misleading."** MODIFIED to Minor weakness #6 — the point about reporting absolute numbers alongside relative percentages is valid as a presentation suggestion, but the harsh critic's framing ("the absolute impact is tiny") is subjective and too strong.

- **"No comparison to the optimal solution" as a structural/fatal issue.** MODIFIED to Minor weakness #3 — computing the true optimal solution is NP-hard (multidimensional knapsack variant), so requiring optimal comparison is too strong. However, comparing against the standard LP (with b) as an upper bound is feasible and useful.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Replace b−1 with b in the LP, or justify the tightening rigorously.** The simplest fix is to use `Ax ≤ b·𝟙_n` as the LP constraint. This would make the LP a true relaxation (providing an upper bound) and eliminate the need to justify the ad-hoc −1 shift. If there is a principled reason for b−1 (e.g., related to the rounding step's correctness), it must be stated explicitly.

2. **Specify the rounding selection step.** Describe how S_i is constructed in Algorithm 3 (e.g., greedy selection of papers with largest fractional values). Analyze whether different selection strategies affect solution quality.

3. **Report the standard LP (with b) as an optimality upper bound** in the experiments to show how close the method is to optimal, even if the final deployed method uses the b−1 LP.

4. **Align the abstract's "randomized rounding" claim with the deterministic algorithm used.** Either change the abstract to say "deterministic rounding" or make the algorithm actually randomized and analyze the expected performance.

5. **Report absolute reductions alongside relative percentages** in Table 3 for clarity.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| bEgDEyy2Yk.md | 1.00 | R1 (strong reject) | Implementation paper with no novel contribution — far weaker than this paper |
| nSDOkm0SKo.md | 1.00 | R1 (strong reject) | Hypothetical scenario analysis with weak methodology — far weaker |
| l5ouuojPGe.md | 3.00 | R1 (reject) | Thresholding strategies paper — similar level of "practical problem + simple method" but less data |
| BjZP3fTlVg.md | 3.00 | R1 (reject) | LLM deployment with risk control — solid empirical work but limited novelty |
| nTZOIlf8YH.md | 2.33 | R1 (reject) | Multi-objective decision pipeline — weak experiments, limited novelty |
| ghk8lnOYRq.md | 5.00 | R1 (borderline) | Hyperplane clustering with IP — solid technical contribution but limited to simulated data |
| IwmyQUPIP0.md | 4.75 | R1 (borderline) | Peaceman-Rachford for LP — theoretical but limited practical scope |
| uZVDJfV2Ex.md | 3.67 | R1 (reject) | Graph-based global optimization — significant reproducibility and scalability concerns |
| W2dR6rypBQ.md | 6.75 | R1 (accept) | Explainable OR with LLMs — strong framework but limited baselines |
| scdGzuwC9u.md | 6.00 | R1 (borderline accept) | MILP reoptimization — solid but limited convergence guarantees |
| rHbxQebhDd.md | 4.25 | R2 (narrow) | Crew pairing optimization — mixed reviews, practical problem |
| 9p2YMVs1Tl.md | 4.00 | R2 (narrow) | MILP predict-and-search — mixed reviews, limited novelty |
| KD9F5Ap878.md | 5.00 | R2 (narrow) | Optimization benchmark for LLMs — solid benchmark but execution concerns |
| 2FAPahXyVh.md | 4.75 | R2 (narrow) | LLM agent for optimization — mixed reviews |
| o0oroLuPLZ.md | 4.60 | R2 (narrow) | Decision-focused learning for LPs — mixed reviews |

**Round 1 Bracket:** 3.5 – 5.5  
**Round 2 Narrowing:** The paper's strengths (real problem, clean formulation, real data, consistent results) place it above the 3–4 range. However, the significant methodological gap (unexplained b−1 tightening) and underspecified algorithm prevent it from reaching the 5.5–6.5 range. It sits near the upper end of the 4–5 band, comparable to papers like KD9F5Ap878 (5.00) and rHbxQebhDd (4.25) — which have real contributions but notable methodological or presentation issues.

**Final Score:** 4.5 / 10  
**Decision:** Reject

The paper addresses a timely, practical problem and provides a clean formalization and thorough real-world data evaluation. However, the unexplained b−1 tightening in the LP (making it a restriction, not a relaxation) and the underspecified rounding step are significant methodological gaps that need to be resolved before the paper's technical contribution can be properly assessed. With revisions addressing these issues (particularly dropping or justifying the b−1 shift, specifying the rounding algorithm, and comparing against the standard LP as an upper bound), the paper could be substantially strengthened.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>