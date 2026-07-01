Here is the final consolidated review:

## Summary

This paper formulates conference desk-rejection under per-author submission limits as an integer program that maximizes the number of papers forwarded to review. The authors propose solving via LP relaxation followed by a deterministic rounding scheme, and evaluate on 11 years of ICLR data. The method consistently reduces desk-rejections relative to current ID-order-based policies (up to 19.23% relative improvement), and all results are computed in under 54 seconds.

## Strengths

- **Well-motivated real problem.** The growth in AI submissions (ICLR: 67 → 11,672) and the widespread adoption of per-author submission limits by conferences such as CVPR, AAAI, KDD, and IJCAI (Table 1) make this a timely and practically relevant question.
- **Evaluation on 11 years of real ICLR data.** The paper crawls actual submission records from OpenReview across 2013–2025 (Table 2), covering a wide range of scales (67 to 11,672 submissions), and evaluates across many values of the submission limit b. This is a solid empirical basis that goes well beyond a single-year snapshot.
- **Consistent improvements over the current policy.** For low-to-moderate b values (4–13) on the larger datasets (ICLR 2023–2025), the method reduces desk-rejections by 5–13% relative to FORWARDREJECT, the stronger baseline. Table 3 transparently reports results across 11 datasets × 8 b-values, showing widespread improvements.
- **Efficient in practice.** All results are computed within 53.64 seconds using a standard LP solver (PuLP) on modest hardware, demonstrating practical deployability.

## Weaknesses

### Fatal
None.

### Major

- **The LP relaxation uses a different constraint set than the IP—without explanation or justification.** The IP (Definition 4.1) constrains `Ax ≤ b·1_n`, while the LP (Definition 4.3) replaces the RHS with `b − 1_n`, tightening every author's budget by 1. This is *not* the standard LP relaxation (which would keep the same RHS and relax only the domain `{0,1} → [0,1]`). The paper never acknowledges, justifies, or analyzes this change. As a result:
  - The LP provides no upper bound on the optimal value of the original IP (it solves a stricter problem).
  - The algorithm has no approximation guarantee relative to the true optimum.
  - The paper repeatedly claims to "maximize" desk-acceptance (abstract, line 48, Section 6), but the method is effectively an uncharacterized heuristic.  
  Even if the tightening is intentional (e.g., to absorb rounding-induced increases in the LHS), the paper must state this, explain why `1` is the right margin, and ideally bound the resulting suboptimality.

- **Baselines do not rule out much simpler heuristics.** The method is compared only against ALLREJECT and FORWARDREJECT (which processes papers in arbitrary submission-ID order). A natural and stronger baseline—a greedy algorithm that sorts papers by number of co-authors (fewest first) and accepts them greedily—is absent. Since the LP method takes up to 53 seconds while a greedy heuristic would be essentially instantaneous, the paper does not establish that the LP+rounding machinery adds value over a well-chosen ordering policy. Without this comparison, the reader cannot tell whether the improvement stems from the optimization framework or simply from replacing the current arbitrary ordering with a reasonable one.

### Minor

- **Misleading "randomized rounding" terminology.** The introduction (line 45) promises "randomized rounding," but Algorithm 3 (MAXROUNDING) is purely deterministic (it picks the argmax fractional value). The only randomness is in the LP solver initialization (Algorithm 4, line 275). "Randomized rounding" carries a specific technical meaning in approximation algorithms (Raghavan & Thompson); using it here sets false expectations about the nature of the contribution.
- **Contradiction about randomness.** Algorithm 4 specifies "Randomly initialize x_0" (line 275), while the experiments section states "The experiments are deterministic and contain no randomness" (line 374). If the solver output is invariant to initialization or the seed is fixed, this should be clarified.
- **Headline number lacks absolute context.** The 19.23% improvement in the abstract corresponds to b=22 on ICLR 2024, where the absolute numbers are 26 vs. 21 desk-rejections—a reduction of 5 papers out of 7,404. While factually correct, leading with this number without the absolute denominator inflates the perceived impact. The more practically relevant low-b settings (where hundreds of papers are saved) show smaller relative improvements (e.g., 10.59% at b=4 for ICLR 2025 saves 316 papers).
- **Practical runtime analysis is disconnected from the theoretical one.** Remark 4.4 cites the O*(m^2.37 log(m/δ)) complexity of stochastic central path methods, but the actual implementation uses PuLP (a simplex/interior-point solver on ∼10^4-scale instances). The theoretical runtime is irrelevant to the deployment scenario.

### Trivial
- The preprocessing simplification described in Section 5 ("removing safe authors") is not reflected in Algorithm 4's pseudocode, creating a minor mismatch between description and implementation.

## Nice-to-Haves
- Compare against simple greedy heuristics (sort papers by author count, accept greedily; random ordering with multiple trials) to isolate whether the LP machinery itself drives the improvement.
- For small instances where the IP can be solved optimally via a MIP solver, report the optimality gap of the LP+rounding heuristic.
- If the b−1 tightening is intentional, explain the rationale and provide an approximation ratio relative to the original IP.

## Removed Points
These are not included in the main weaknesses because they either reflect misreadings or are excluded by policy:
- Criticism of Remark 4.2 (welfare claim about the IP without a solution method): the remark is about the IP formulation itself (optimization vs. feasibility), which is a valid conceptual claim regardless of solver.
- Criticism that the forward/reverse algorithm "equivalence" is unclear: the context ("provably correct in producing feasible solutions") makes clear this refers to feasibility equivalence, not output identity.
- Complaint about "only ICLR data": the paper transparently acknowledges that data from other conferences is not publicly available.
- Concern about code/data not being released: the paper states it will be released upon acceptance; policy prohibits questioning existence/release status of cited resources.
- Several section-by-section granular notes that duplicate the weaknesses above or are too minor to warrant inclusion (e.g., runtime analysis irrelevance is already softened and folded into Minor).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Correct the LP relaxation to use the same RHS as the IP (`b·1_n`), or explicitly justify the `b−1` tightening and provide an approximation analysis.
2. Add comparisons against simple greedy baselines to establish that the LP+rounding approach adds value beyond well-chosen ordering heuristics.
3. Fix the "randomized rounding" terminology and resolve the contradiction between random initialization and claimed determinism.
4. Contextualize the 19.23% headline number with absolute counts in the abstract.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>