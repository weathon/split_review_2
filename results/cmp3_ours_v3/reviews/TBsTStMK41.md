Now I have a thorough understanding of the calibration landscape. Let me write the final review.

**Bracket analysis:**
- Round 1 bracket: Score 2.5–4.5
- The portfolio optimization paper (score 3.00, C9pndmSjg6) is most comparable in terms of methodological scope (pure optimization, no ML). The MILP+ML paper (score 4.00, 9p2YMVs1Tl) uses ML and still scored 4.00. The paper under review has the advantage of addressing a timely problem directly relevant to the ICLR community, and the clean formalization + real-data evaluation are genuine strengths. However, the structural LP issue (b-1), weak baselines, and lack of any learning component keep it below the acceptance threshold. Score 3.0 (Reject) captures that the paper has real merits but is not ready for acceptance at ICLR.

Here is the final consolidated review:

---

## Summary

This paper studies the problem of desk-rejecting papers under per-author submission limits, a policy recently adopted by several AI conferences. It formalizes the problem as an integer program (maximizing the number of papers desk-accepted under author-level caps), proposes a two-stage LP-relaxation-and-rounding algorithm, and evaluates it on 11 years of ICLR submission data (2013–2025). The method consistently outperforms the two baseline policies (ALLREJECT and FORWARDREJECT) used by conferences, with up to 19.23% fewer desk-rejections at negligible computational cost (≤ 53.64 seconds).

## Strengths

1. **Timely and well-motivated problem.** The submission-limit desk-rejection policy is a recent phenomenon (adopted by many conferences starting 2023–2025), and this paper provides the first formal treatment. The motivation is grounded in real submission-growth data (Figure 1: ICLR submissions grew from ~1,400 in 2019 to ~11,700 in 2025).

2. **Clean formalization of the problem and existing policies.** Section 3 precisely defines the submission-limit problem (Definition 3.1) and provides algorithmically precise descriptions of the actual policies used by conferences (Algorithms 1 and 2). This formalization is a useful standalone contribution.

3. **Meaningful empirical results on real-world data.** Table 3 shows consistent improvements over both baselines across years and submission limits. The gains on recent large-scale data are materially significant (e.g., 116 papers saved at *b*=10 for ICLR 2025; up to 19.23% at *b*=22 for ICLR 2024). Evaluation spans 11 years of actual ICLR author-paper mappings.

4. **Computational efficiency.** All results computed within 53.64 seconds, fast enough for practical conference deployment.

## Weaknesses

### Fatal
None.

### Major

1. **The LP formulation uses a tightened constraint (b‑1) without analyzing the resulting optimality gap.** The IP (Definition 4.1) uses *Ax ≤ b·1ₙ*, while the LP (Definition 4.3, promoted as a "relaxation") uses *Ax ≤ (b‑1)·1ₙ*. The constraint is tightened, not relaxed, so the LP feasible set is not a superset of the IP feasible set. This has a direct, predictable cost: an author who submits exactly *b* papers can have all *b* accepted in the IP optimum, but the LP caps them at *b‑1*, guaranteeing at least one rejection. For authors with many papers (MSPA reaches 42 in ICLR 2025, Table 2), this compounds. Theorem 4.6 only certifies feasibility, not objective quality, and the paper provides **no analysis** of how much optimality is lost by this design choice. Without understanding this gap, the reader cannot determine whether the method is genuinely good or merely better than the obviously wasteful baselines.

2. **The empirical comparison lacks a strong upper bound.** The two baselines are FORWARDREJECT (arbitrary submission-ID order) and ALLREJECT (rejects all exceeding papers at once). Both are trivially suboptimal. The paper does not compare against: (a) solving the ILP to optimality with a commercial solver (Gurobi/CPLEX/SCIP) — the instances have ~10⁴ binary variables and ~3×10⁴ sparse constraints, which may be tractable; or (b) a smarter greedy heuristic (e.g., accept papers in order of fewest authors first). Such comparisons would either confirm near-optimality (strengthening the contribution) or reveal that most gains come from beating a trivially bad policy. The headline "up to 19.23% reduction" is incompletely contextualized against only weak baselines.

### Minor

1. **"Randomized rounding" claim is inaccurate.** The introduction (line 45) describes the method as using "randomized rounding," but Algorithm 3 (MAXROUNDING) is entirely deterministic — it picks `arg max` at each step. Only the LP initialization in Algorithm 4 has a random element. This factual error should be corrected.

2. **The conclusion overstates the contribution.** Describing the work as a "pioneering study" with "direct transformative social impact" (line 392) is disproportionate relative to the scope and technical depth of the contribution.

3. **Only 8 of the 22 *b*-values appear in the main table** (the rest are deferred to the appendix). While space constraints are understandable, this makes the main empirical presentation less complete.

### Trivial
- The small improvements on early ICLR years (e.g., 3.77% at ICLR 2018, *b*=4; 5.13% at ICLR 2019, *b*=7) are reported without any discussion of whether they arise from structural properties of the data or from methodological/numerical variation. A brief comment would be helpful.

## Nice-to-Haves
- Replace the *Ax ≤ b‑1* constraint with *Ax ≤ b* and develop a proper rounding scheme (e.g., dependent rounding) that allows approximation-ratio analysis. This would make the LP a true relaxation.
- Compare against the optimal ILP solution (solved by Gurobi/CPLEX with a reasonable time limit), at least for smaller-to-mid-size ICLR instances. This would establish how far the method is from optimal.
- Compare against a smarter greedy baseline (e.g., papers ordered by increasing number of co-authors) to test whether the LP+rounding adds value beyond a well-designed heuristic.
- Provide a running-time breakdown by year and *b*-value rather than just a single aggregate maximum.

## Removed Points
- **"NP-hardness not formally established in the main text."** The hardness discussion/reduction may be in the appendix (which the parser strips). Per meta-review rules, missing appendix content is not penalized. Removed.
- **"Section 2 (Related Works) is thin."** A generic presentation criticism without a specific anchor. Removed.
- **"Only ICLR data is used."** The paper explicitly acknowledges this limitation (line 313: "ICLR is the only venue with public submission records"). Removed as already addressed.
- **"The specific CVPR footnote verification."** The paper cites a publicly available conference URL. Removed.
- **"Missing max-flow reformulation discussion."** The paper already mentions total unimodularity (line 227) and uses it to motivate the rounding. Removed as the paper already addresses it.

## Novel Insights
The harsh critic's core observation — that the LP uses *Ax ≤ b‑1* instead of *Ax ≤ b* — is a genuinely insightful technical point. Standard LP relaxation would relax both the domain *and* keep the original constraint. The paper's choice to tighten the constraint (b‑1) while relaxing the domain means the feasible set is not a proper relaxation, and the unanalyzed optimality gap directly affects how the results should be interpreted. This is a specific, verifiable structural concern that goes beyond generic critique. The suggestion to compare against the optimal ILP solution is also well-targeted: for instances of this size with sparse constraint matrices, commercial solvers may well find the true optimum, cleanly revealing the method's real quality.

## Suggestions
1. **Address the LP constraint issue.** Either replace *Ax ≤ b‑1* with *Ax ≤ b* and design a rounding scheme that preserves feasibility (e.g., dependent rounding), or provide an analysis of the optimality loss introduced by the tightening. An approximation-ratio guarantee would significantly strengthen the paper.
2. **Add an ILP-optimum comparison.** Solve the ILP with a commercial solver (even with a time limit) for the smaller-to-mid-size ICLR instances to establish how far the LP+rounding solution is from optimal.
3. **Add a smarter greedy baseline.** Compare against heuristics such as papers ordered by increasing number of authors or by increasing sum of remaining author capacity.
4. **Correct the "randomized rounding" description** in the introduction to match the deterministic Algorithm 3.
5. **Provide running-time breakdowns** by year and *b*-value, and briefly discuss the cases where improvements are small.

## Score and Decision
**Calibration anchors:** The retrieval searched the 13k-paper review corpus for similar optimization/OR papers across score bands.

| Anchor Path | Avg Score | Round | Comparison |
|---|---|---|---|
| C9pndmSjg6 (Portfolio Optimization, MIQP) | 3.00 | R1 | Pure optimization without ML; reviewers cited lack of ICLR relevance and no time reporting. The current paper has stronger real-world grounding and cleaner experiments. |
| 9p2YMVs1Tl (MILP with GNN) | 4.00 | R2 | Uses ML (GNN) but criticized as incremental; scored 4.00 (reject). Current paper has no ML component. |
| 2oWRumm67L (Light-MILPopt) | 5.00 | R2 | Uses ML (GNN) for MILP solving; accepted with score 5.00. Current paper has a simpler method without ML. |
| joMMM9eadc (IP Feasible via Diffusion) | 6.25 | R2 | Uses diffusion models; scored 6.25 (reject). Much more technically sophisticated. |
| scdGzuwC9u (MILP Reoptimization) | 6.00 | R2 | Uses GNN; scored 6.00 (reject). More sophisticated methodology. |

**Round 1 bracket:** 2.5–4.5. The paper's real-data evaluation and timely problem prevent it from being a strong reject (score 1), but the structural LP issue, weak baselines, and lack of any learning component keep it clearly below the acceptance threshold. Score 3.0 is the appropriate calibrated point — it communicates "has real merits but significant issues prevent acceptance at ICLR."

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>