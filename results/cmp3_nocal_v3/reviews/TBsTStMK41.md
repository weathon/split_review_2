## Summary

This paper formalizes the per-author submission-limit desk-rejection policies used at top AI conferences as an optimization problem (maximum desk-acceptance), proposes an LP relaxation + greedy rounding algorithm to minimize desk-rejections while respecting author caps, and evaluates on 11 years of ICLR data. The method consistently reduces desk-rejections relative to current ID-order policies, but the absolute improvements are modest and the technical approach is straightforward.

## Strengths

- **First formal treatment of an under-studied administrative problem.** Section 3 provides a clean mathematical formalization (Definitions 3.1, 4.1) of what was previously an opaque rule-based policy. The maximum desk-acceptance framing is a sensible reframing, and this appears to be the first work to treat it formally.

- **Non-trivial data collection.** The authors crawled 11 years of ICLR data (2013–2025) via the OpenReview API, yielding informative statistics (Table 2) that document the rapid growth of the conference. This dataset is a concrete asset.

- **Consistent empirical wins.** In every instance where the baselines desk-reject any papers at all, the proposed method rejects fewer (Table 3). There is no counterexample in the data. The algorithm is also fast—sub-minute for all ICLR years.

## Weaknesses

### Fatal
None.

### Major

- **Rhetoric significantly overstates the practical impact.** The headline "up to 19.23% reduction" is a *relative* improvement over a baseline that itself rejects very few papers at that limit. In absolute terms, for the headline case (ICLR 2024, b=22), the method saves **5 papers out of 7,404**—i.e., 0.07% of all submissions. The paper calls this "dramatic" and claims it "demonstrates the effectiveness of our proposed method in saving thousands of authors from having their papers desk-rejected" (line 384). The largest absolute savings in Table 3 is ICLR 2025 at b=4: 316 fewer papers desk-rejected (2.7 percentage points)—meaningful, but not "thousands of authors." The paper's own data shows the existing policies are already quite close to optimal; the marginal improvement, while consistent, is small. The abstract, introduction, and conclusion should be recalibrated to honestly characterize the modest scale.

- **No optimality analysis or comparison against the optimal solution.** The paper acknowledges the problem is NP-hard (multi-dimensional knapsack, line 213) but provides no approximation guarantee for the LP relaxation + rounding. Theorem 4.6 only proves the rounded solution is *feasible*, not that it is *any good* relative to the optimum. The paper could solve the exact IP for small years (ICLR 2013: 67 papers, 2014: 69 papers) to measure the optimality gap, or compare the LP upper bound against the rounded solution for larger years. Without *any* estimate of how far the solution is from optimal, the empirical results are uninformative beyond showing that the method beats two hand-coded heuristics. This is the most consequential missing piece in the evaluation.

- **The LP relaxation contains an unexplained constraint change.** Definition 4.1 (the IP) has constraint $Ax \leq b \cdot \mathbf{1}_n$, while Definition 4.3 (the "LP relaxation") has constraint $Ax \leq b - \mathbf{1}_n$—each author's constraint is tightened by 1 relative to the IP. This is *not* a standard relaxation (which would keep the same constraints and only relax the domain). No explanation is given for this change (lines 213–221). If intentional (e.g., to guarantee feasibility after rounding), it needs justification and analysis. If a typesetting error, it must be corrected. Either way, the formal foundation of the method is unclear at a critical juncture.

### Minor

- **"Randomized rounding" is a mischaracterization.** The introduction (line 45) claims the algorithm uses "randomized rounding," but Algorithm 3 (MAXROUNDING) is entirely deterministic—it picks the largest fractional value greedily and rounds up. The only stochastic element in Algorithm 4 is "Randomly initialize $x_0$" (line 275), which is irrelevant for a convex LP solver. The paper itself confirms "the experiments are deterministic and contain no randomness" (line 374). The terminology should be corrected.

- **No fairness or distributional analysis.** The Ethics Statement (Section 7) expresses concern for early-career researchers who may be disproportionately affected by desk-rejections. Yet there is zero analysis of whether the method's savings are distributed equitably—e.g., do saved papers concentrate among a few prolific authors, or spread across many? This is a natural analysis to include given the paper's own stated ethical motivation.

- **No ablation study.** The method has two components (LP + rounding). There is no separation of how much each component contributes (e.g., how does greedy rounding compare to simple threshold rounding or randomized rounding on the same LP solution?).

### Trivial
None.

## Nice-to-Haves
- For small years, solving the exact IP with a standard solver would definitively measure optimality and strengthen the empirical claims considerably.
- A discussion of strategic gameability (e.g., authors adding co-authors to game LP-based policies) would be relevant for real-world deployment.
- Additional synthetic baselines (e.g., priority heuristics) would further validate the approach.

## Removed Points
These points are flagged to be removed; treat them with caution.

- **"Baselines are weak (missing priority heuristic, per-author proportional allocation)":** The paper compares against the *actual policies used by conferences*, which is the most relevant comparison. Suggestions for additional synthetic baselines are nice-to-haves, not weaknesses. The absence of an optimal solution comparison is already covered in Major Weakness #2.
- **"Cherry-picking b values and years in the main table":** The paper explicitly states it selected representative values due to space and that full results are in Appendix E (line 380). This is standard practice and adequately disclosed.
- **"Discussion of communication/transparency":** Reasonable but outside the paper's stated scope as a technical formulation.
- **"Randomly initialize $x_0$ criticism":** Trivial detail that does not affect the paper's validity.

## Novel Insights
The harsh critic's central insight—that the paper's own numbers reveal existing policies are already quite close to optimal, and the paper's rhetoric systematically inflates the magnitude of the contribution—is a genuinely novel observation that goes beyond what the paper itself acknowledges. The critic correctly identifies that the paper's main value is in the problem framing and formalization, not in the technical method, and that adding an optimality comparison would either strengthen the paper significantly (if the gap is small) or reveal limitations (if the gap is large). This tension between the paper's formal contribution and its empirical claims is not addressed in the paper itself.

## Suggestions
1. Rewrite the abstract, introduction, and conclusion to honestly characterize the improvement scale (small but consistent). Remove "dramatic" and "saving thousands of authors."
2. Solve the exact IP for small years (2013, 2014, 2017) using a standard IP solver and report the gap. For larger years, compare the LP upper bound against the rounded solution.
3. Clarify the $b$ vs. $b-1$ discrepancy in Definition 4.3—either justify the tightened constraint as intentional or correct it to the standard relaxation $Ax \leq b \cdot \mathbf{1}_n$.
4. Add at least a basic fairness analysis (e.g., distribution of saved papers across authors) to support the ethics claims.
5. Correct "randomized rounding" to "deterministic greedy rounding."
6. Add an ablation comparing the LP solution quality against the rounded solution to isolate the contribution of each component.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>