## Summary

This paper formalizes the desk-rejection problem at AI conferences—where papers by authors exceeding per-author submission limits are rejected—as an integer programming optimization problem. The authors propose a linear programming relaxation with a rounding scheme to maximize the number of papers preserved (desk-accepted) while respecting submission limits, and evaluate on 11 years of ICLR data, demonstrating up to 19.23% fewer desk-rejections compared to naive sequential policies.

## Strengths

- **Novel and timely problem formulation.** The paper is among the first to formalize the submission-limit desk-rejection policy as an optimization problem (Definition 4.1). With major venues (CVPR, AAAI, KDD, etc.) now enforcing per-author limits and rejecting papers by submission ID, this formalization is directly relevant to how conferences operate. The connection to social welfare and author equity is well-motivated.

- **Practical algorithm with strong empirical validation.** The proposed method (LP relaxation + rounding) runs in under 54 seconds on all ICLR datasets (up to ~12K papers, ~38K authors) using a standard PuLP solver, making it immediately deployable. The evaluation spans 11 years of data across 8 different submission limits (b=4 to b=25), providing thorough evidence of consistent improvement over baselines.

- **Clear presentation and honest scope.** The paper is well-organized with formal definitions, algorithms with pseudocode, correct propositions, and a reproducibility statement. The authors correctly acknowledge that their baselines are the only known desk-rejection policies and that their code/data will be released upon acceptance.

## Weaknesses

### Fatal
None.

### Major

- **Unexplained use of $b-1$ in the LP relaxation (Definition 4.3).** The original IP (Definition 4.1) has constraint $Ax \leq b \cdot \mathbf{1}_n$, but the LP relaxation in Definition 4.3 uses $Ax \leq (b-1) \cdot \mathbf{1}_n$. This is not a standard relaxation—it is a strictly tighter constraint that yields a worse (lower) objective bound. The authors do not discuss or justify this choice anywhere. Since the rounding algorithm (Algorithm 3, lines 12-18) already explicitly handles overflow when rounding papers from fractional to 1, the tighter constraint appears redundant for correctness while degrading solution quality. This likely causes the method to preserve fewer papers than it could, and the paper would benefit from either (a) using the standard relaxation with $b$, or (b) providing a clear justification and experimental comparison.

- **Somewhat misleading headline improvement metric.** The headline "up to 19.23%" improvement is relative to the number of desk-rejected papers, not total submissions. For the cited case (ICLR 2024, b=22), the method goes from 26 to 21 rejections out of 7404 total papers—a difference of 5 papers (0.07% of submissions). Even for the largest absolute savings (ICLR 2025, b=4), the method saves 316 papers out of 11,672 (2.7%). The relative improvement over desk-rejections is real but the practical magnitude of impact is more modest than the framing suggests. The paper should present both relative and absolute improvement figures.

### Minor

- **Limited comparison with alternative optimization approaches.** The only baselines are naive sequential policies (Algorithms 1 and 2). Comparing with a simple greedy heuristic (e.g., iteratively accepting the paper that violates the fewest constraints) or the direct LP relaxation with $b$ would better characterize the contribution of each component.

- **No discussion of incentive compatibility.** If authors know the optimized desk-rejection policy, strategic behavior could change (e.g., submitting more papers expecting the optimization to save them). While this is a secondary concern, it would strengthen the paper to at least acknowledge this consideration.

### Trivial
None.

## Nice-to-Haves
- A comparison of the LP with $b$ vs. $b-1$ to quantify the cost of the conservative relaxation.
- Analysis of which papers get saved by the optimization (e.g., are they from early-career researchers as the ethics statement suggests?).
- Discussion of how this interacts with reviewer assignment—preserving more papers increases review load.

## Novel Insights

The core insight—that desk-rejection by submission ID order is suboptimal and can be significantly improved via combinatorial optimization—is genuinely useful. The observation that this problem maps naturally to a multi-dimensional knapsack problem, while not technically surprising, provides a clean bridge between optimization theory and conference administration. The empirical finding that improvement scales with conference size (the method helps more as submissions grow) is practically important for the rapidly expanding AI conference landscape.

## Suggestions
- Replace the $b-1$ LP relaxation with the natural $Ax \leq b\mathbf{1}$ relaxation and verify that the rounding algorithm still produces correct results (which it should, given the explicit overflow handling).
- Report absolute numbers of papers saved alongside percentage improvements relative to desk-rejections.
- Consider a simple greedy baseline for comparison to isolate the value of the LP relaxation specifically.

## Score and Decision

The paper identifies a novel and practical problem with real-world relevance to conference management. The formulation is clean and the solution works. However, the technical approach (LP relaxation + greedy rounding) is standard optimization, the relaxation choice ($b-1$) appears suboptimal and unexplained, and the practical impact—while real—is more modest than the framing implies. This is a borderline contribution that provides genuine value but could be strengthened with better methodological justification.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Accept