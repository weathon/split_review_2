Now let me finalize the consolidated review.

## Summary

This paper formalizes desk-rejection under author-level submission limits as an integer program (maximum desk-acceptance problem), proposes a two-stage algorithm that solves an LP relaxation followed by a deterministic rounding procedure, and evaluates it on 11 years (2013–2025) of ICLR submission data. The method consistently reduces desk rejections compared to current ID-order policies, with absolute savings of up to 316 papers (10.59% relative improvement over the strongest baseline at low limits) and up to 19.23% relative improvement at high limits.

## Strengths

- **Well-motivated and timely problem.** The paper correctly identifies that current desk-rejection policies (reject by submission ID order) are needlessly wasteful. Several major AI conferences have adopted per-author submission limits in 2024–2025, and the question of how to enforce them while minimizing rejections is a real operational concern. The introduction and Section 2 make this case clearly.

- **Clean formalization of existing policies.** Algorithms 1 (ALLREJECT) and 2 (FORWARDREJECT) are clearly specified with correctness propositions (3.5 and 3.6). Having these baselines in precise algorithmic form is a useful contribution.

- **Substantial data collection effort.** Crawling 11 years of ICLR data from OpenReview and constructing the author–paper authorship matrix (Table 2) is a non-trivial undertaking that grounds the evaluation in real conference data.

- **Consistent empirical results across a decade.** Across all years and all b values where desk-rejection occurs, the proposed method either beats or matches both baselines (Table 3). This consistency is the paper's strongest empirical asset.

## Weaknesses

### Major

- **The LP relaxation uses a stricter constraint than the integer program without explanation.** Definition 4.1 (IP) has constraint `Ax ≤ b·1_n`, while Definition 4.3 (LP relaxation) has constraint `Ax ≤ b − 1_n`, which is strictly tighter (b−1 per author instead of b). A standard LP relaxation relaxes integrality while keeping the same constraints; the change in RHS is never explained or justified. The rounding algorithm (Algorithm 3) maintains feasibility against b directly (Theorem 4.6), suggesting the tighter constraint unnecessarily restricts the LP's solution space and may produce worse results. This is a technical flaw in the method's definition.

- **No comparison against the optimal integer solution or LP upper bound gap.** The paper argues the problem is "inherently related to the multi-dimensional knapsack problem [and] cannot be solved efficiently in general" (Section 4.2), but never tries to solve the IP directly for the ICLR instances. The constraint matrix A is extremely sparse (nnz(A) ≈ 3–5× m, ASPA ≈ 3, Table 2), so the IP may well be solvable to optimality by standard solvers for instances up to ~10,000 variables. The paper should either (a) solve the IP directly and report the gap, or (b) report the LP upper bound (with the correct constraint) and show how far the rounded solution is from it. Without this, readers cannot assess whether the LP+rounding approach is a useful approximation or unnecessarily complex for a potentially tractable problem.

### Minor

- **Headline "19.23% improvement" is a relative percentage on a very small absolute number and lacks context.** At ICLR 2024, b=22, FORWARDREJECT rejects 26 papers and the proposed method rejects 21 — a saving of 5 papers out of 7404 (0.07% of submissions). The relative percentage is inflated by the tiny denominator (26). The far larger absolute savings occur at low b values (e.g., b=4 for ICLR 2025: 2984→2668, saving 316 papers, 10.59% relative). The paper leads with the 19.23% figure in the abstract, introduction, and contributions without contextualizing the absolute scale. Absolute numbers are visible in Table 3, but the framing should prominently include absolutes.

- **Inconsistent description of randomness/randomized rounding.** The introduction describes the algorithm as using "linear programming relaxation and randomized rounding" (line 45). Algorithm 4 includes "Randomly initialize x₀" (line 275). Yet Algorithm 3 (the rounding procedure) is entirely deterministic (it processes fractional entries in decreasing order with no randomness), and Section 5.1 states "experiments are deterministic and contain no randomness" (line 374). The random initialization is never explained or justified, and standard LP solvers do not require it. These statements are contradictory.

- **Unsubstantiated hardness claim and no approximation guarantees.** The paper claims to "establish the computational hardness of the problem" (line 45), but Section 4.2 merely states a connection to multi-dimensional knapsack without a formal reduction or proof. No approximation ratio is provided for the LP+rounding algorithm. The empirical contribution is valid without this theoretical framing, but the paper oversells the theoretical component.

- **Evaluation on a single conference's data.** The paper acknowledges ICLR is the only venue with public submission records. While honestly stated, different conferences may have different co-authorship patterns, and it is unclear how well the results generalize.

### Trivial

None.

## Nice-to-Haves

- Practical deployment considerations (enforcing limits at submission time vs. post-hoc, potential for gaming, transparency trade-offs) are outside the paper's scope but would strengthen the practical narrative.
- Comparing the LP objective value against the rounded solution value would help measure rounding quality.
- A brief discussion of fairness across authors (does the algorithm systematically favor certain author types?) would be a useful addition.

## Removed Points

These points from the input review were removed after verification:

1. **Criticism about code/data not being available for review.** The paper states code/data will be released upon acceptance — standard practice. Removed per policy.
2. **Criticism about missing appendix content (hardness proof, etc.).** Appendix content is stripped by the parser; the original submission contains it. Removed per policy.
3. **Criticism about "transformative social impact" being overstated.** A stylistic nitpick. Removed.
4. **Criticism about no sensitivity analysis on b.** The paper tests b from 4 to 25 for all years — a broad sensitivity analysis. The criticism is factually incorrect. Removed.
5. **Deployment constraint criticisms** (enforcing at submission time, authors gaming, transparency). These address considerations outside the paper's stated scope. Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Fix the LP relaxation constraint in Definition 4.3 to match the IP constraint (`Ax ≤ b·1_n` with x ∈ [0,1]^m). If the b−1 constraint is intentional as a safety margin, state and justify it explicitly.
- Solve the IP directly with a standard IP solver for the ICLR instances and report the optimality gap. This would either validate the LP+rounding approach or show that the IP is tractable.
- Report absolute reductions alongside relative percentages in the abstract and headline claims.
- Resolve the inconsistency between "randomized rounding" / "Randomly initialize x₀" and the claim that experiments are deterministic with no randomness.
- Tone down or substantiate the "computational hardness" claim.

## Score and Decision

This paper addresses a real and timely problem, formalizes it cleanly, and presents consistent empirical improvements over current practice across a decade of real data. However, two substantive issues — the unexplained tightening of the LP constraint (b to b−1) and the lack of any comparison against the optimal IP solution — prevent full confidence in the technical contribution as presented. Both issues are fixable and do not necessarily invalidate the empirical findings, but they require author attention.

<score>6</score>
<decision>Accept</decision>