Now let me check a few more specific details in the paper to verify claims about the "randomized rounding" language and the LP constraint formulation.Now let me produce the draft review and submit it for calibration.Now let me do calibration. Round 1 — Bracketing across score bands:Let me read a few key anchors to compare:Now let me look at one more anchor in the 3-5 range that's more similar to this paper's nature:Now I have sufficient calibration data. Let me form my initial bracket and write the final review.

**Initial bracket: 3.0 – 4.5**

Reasoning:
- The paper is clearly better than the strong-reject (1.0) papers which are fundamentally broken or trivial
- It shares the core weakness of C9pndmSjg6 (3.0) — applying standard optimization to a practical problem without algorithmic novelty — but is better motivated and more relevant to the community
- It falls well short of scdGzuwC9u (6.0) which introduces genuinely novel ML-based components (GNN + Thompson Sampling)
- The paper's contribution is primarily in problem identification, not algorithmic innovation, and the missing IP baseline leaves a critical gap

The paper sits between a clear reject (3.0) and borderline reject (4.0). The practical relevance to the community and clean execution push it above 3.0, but the lack of technical novelty and missing obvious baseline keep it below 4.0. **Final estimate: 3.5.**

---

## Summary
This paper formalizes the desk-rejection problem at AI conferences with per-author submission limits as a binary integer program (maximize accepted papers subject to per-author constraints), proposes an LP relaxation with deterministic greedy rounding, and evaluates on 11 years of ICLR submission data showing 10–19% improvements over naive baseline policies.

## Strengths
- **Clear problem identification with practical relevance**: The paper identifies a concrete inefficiency in current desk-rejection policies and provides a rigorous mathematical formulation (Definition 4.1). The survey of submission-limit policies across conferences (Table 1) is a useful reference for the community.
- **Comprehensive empirical coverage**: Experiments span 11 years of ICLR data (2013–2025) across submission limits b=4 to 25. For large-scale recent years (ICLR 2024–2025), improvements of 10–13% are consistently achieved across most realistic b values (Table 3).
- **Clear presentation and reproducibility**: Pseudocode for all algorithms (Algorithms 1–4) is provided, the dataset construction methodology is explicit, and the deterministic execution ensures reproducibility.

## Weaknesses

### Fatal
None

### Major
- **Missing direct IP solution baseline**: The paper motivates LP relaxation by citing NP-hardness of multi-dimensional knapsack in general (Section 4.2), but the specific problem instances are small and very sparse (nnz ≈ 62K for the largest instance, ICLR 2025 with m=11,672 papers and n=38,495 authors; Table 2). The authors use PuLP (Section 5.1, line 366) which bundles the CBC solver capable of solving binary IPs. Modern solvers routinely handle problems of this size in seconds. Without solving the IP directly or reporting the LP upper bound, we cannot assess how close the rounded solution is to optimal. The paper claims to "minimize" unnecessary desk rejections, but only demonstrates improvement over naive baselines — the gap to true optimality is unknown.

- **Limited technical novelty for a top venue**: The paper itself acknowledges (Section 4.2): "The maximum desk-acceptance submission limit problem is a standard integer programming problem, inherently related to the multi-dimensional knapsack problem." LP relaxation + greedy rounding is the textbook first approach to such problems. Despite this, the paper frames the contribution as "novel re-formulation" (Introduction, line 45) and "pioneering study" (Conclusion). The value rests entirely on problem identification and practical demonstration rather than algorithmic innovation, which is thin for ICLR's standards.

### Minor
- **Terminology inconsistency ("randomized rounding")**: The introduction (line 45) describes the method as using "randomized rounding," but Section 5.1 (line 374) explicitly states "experiments are deterministic and contain no randomness." Algorithm 3 (MAXROUNDING) is entirely deterministic — it greedily picks the highest-fractional variable. Only Algorithm 4 line 2 randomly initializes the LP solver's starting point, which is not "randomized rounding" in the established technical sense.

- **LP constraint tightening not explained**: Definition 4.3 uses constraint Ax ≤ (b−1)·𝟏_n (tightened by 1 per author) vs. the original IP's Ax ≤ b·𝟏_n (Definition 4.1). This slack presumably ensures feasibility after rounding, but the paper never discusses why this tightening is necessary or quantifies its impact on solution quality. It means the LP upper bound is strictly lower than the true IP optimum, potentially leaving papers on the table.

- **Simulated evaluation on non-representative venue**: ICLR has never enforced submission limits, so the claimed "19% reduction in unnecessary desk-rejections" never actually occurred. The paper acknowledges using "simulation experiments" (Section 5.1) but the title and abstract frame results as addressing real desk-rejections. Collaboration structures at venues that actually use limits (CVPR, KDD, AAAI) may differ from ICLR's.

- **Headline figure from small-base configuration**: The 19.23% improvement (ICLR 2024, b=22) comes from saving 5 papers out of 26 baseline rejections. For realistic large-scale scenarios the consistent improvement is 10–13%, which is meaningful but less dramatic than the title suggests.

### Trivial
- "Pioneering study" language in the conclusion overstates novelty given the standard nature of the technical approach.

## Nice-to-Haves
- Solve the IP directly and report the optimality gap — this would either validate the LP+rounding approach (strengthening the paper significantly) or reveal room for improvement
- Analyze which papers/authors benefit from the optimization to empirically support the Ethics Statement's claim about early-career researchers
- Test on synthetic authorship graphs mimicking collaboration structures of venues that actually use submission limits
- Consider the constraint tightening in Definition 4.3 as a tunable parameter and study its effect

## Removed Points
*These points are flagged to be removed, treat them with caution:*
- **Fairness concern** (that maximizing total acceptance may systematically favor prolific senior authors): The paper's Ethics Statement (lines 398–401) addresses this, claiming the method helps early-career researchers. While empirical validation would strengthen this claim, the concern is speculative without evidence, and the paper explicitly scopes its objective to total welfare maximization.
- **Demand for confidence intervals/variance**: The algorithm is deterministic (acknowledged in line 374), so single-run reporting is appropriate.
- **Transferability to other venues**: While noted as a limitation, this is scope-creep — the paper uses the only publicly available data and acknowledges the simulation nature.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Run the IP to optimality using CBC/Gurobi on the ICLR instances and report the gap between LP+rounding and exact solutions. This is likely trivial to implement and would dramatically strengthen (or appropriately qualify) the paper's claims.
- Clarify the constraint tightening in Definition 4.3 with explicit discussion of why b−1 is used and what it costs in solution quality.
- Fix the "randomized rounding" terminology throughout to "deterministic greedy rounding."
- Report absolute numbers of papers saved alongside percentages — "saving 5 out of 26 papers" vs. "saving 316 out of 2984 papers" (ICLR 2025, b=4) conveys very different practical significance.
- Consider reframing the paper's contribution as problem identification + practical demonstration rather than algorithmic novelty.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Clothing-Irrelevant Lifelong ReID | 5lUdTogEL3 | 1.0 | R1 | Fundamentally flawed; paper under review is far better executed |
| All Pairs Minimax Path Implementation | bEgDEyy2Yk | 1.0 | R1 | Pure implementation paper with no novelty; paper under review has more substance |
| Financial Markets Neural Network | nSDOkm0SKo | 1.0 | R1 | Hypothetical scenario with no rigor; paper under review is much stronger |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.0 | R1 | Fundamentally flawed methodology; not comparable |
| Portfolio Optimization Hybrid Relaxation | C9pndmSjg6 | 3.0 | R1 | **Most comparable** — standard optimization (LP relaxation + heuristics) applied to a practical problem without ML. Paper under review is better motivated and more relevant to the community, but shares the same fundamental weakness of limited technical novelty |
| Dantzig-Wolfe + DRL | yYylDyLnzt | 3.0 | R1 | Combines standard decomposition with RL; has slightly more ML novelty than paper under review but worse presentation |
| Adaptive Proximal Gradient P+O | cya3eEczAx | 1.67 | R1 | Poorly executed optimizer paper; paper under review is clearly better |
| Provably Safe RL Bender's | RAdBtquPiI | 3.4 | R1 | Novel combination of Bender's decomposition with RL; more technical novelty than paper under review |
| MILP Reoptimization | scdGzuwC9u | 6.0 | R1 | Introduces novel GNN + Thompson Sampling framework; significantly more technical novelty |
| IP Feasible Solutions via Diffusion | joMMM9eadc | 6.25 | R1 | Novel ML approach (contrastive learning + diffusion) for IP; far more innovative |
| L2P-MIP Presolving | McfYbKnpT8 | 6.5 | R1 | ML-driven MILP presolving; genuinely novel contribution |
| BTBS-LNS | siHHqDDzvS | 6.25 | R1 | Novel learning-based neighborhood search; significantly more technical depth |
| Learning to Relax | 5t57omGVMw | 8.0 | R1 | Strong theoretical contribution with practical validation; far above paper under review |

**Round 1 bracket: 3.0 – 4.5**

The paper sits squarely between the 3.0 portfolio optimization paper (standard optimization without ML, limited novelty, but paper under review is better motivated/presented) and the 6.0+ papers which all introduce genuinely novel algorithmic components. The paper's practical relevance to the ML community and clean execution lift it slightly above pure 3.0, but the entirely standard technique and missing obvious baseline prevent it from reaching borderline-reject territory at 4.0+.

**Final score: 3.5** — The paper identifies a relevant practical problem and provides a clean formulation and working solution, but the technical contribution is a textbook application of LP relaxation + greedy rounding to a problem that could likely be solved exactly at this scale. The missing IP baseline is particularly damaging: it leaves open whether the method is 1% or 50% from optimal, undermining the paper's central claim. For a venue that values technical innovation, this contribution does not clear the bar.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>