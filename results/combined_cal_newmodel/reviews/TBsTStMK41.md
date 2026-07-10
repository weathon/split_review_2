Now I have enough calibration data. Let me compile the final review with my comparative analysis.

**Round 1 bracket**: Based on the calibration, papers at 1.0-3.0 are clearly worse (trivial or broken contributions), papers at 3.0-5.0 have optimization methodology but weaker applications, papers at 5.75-6.80 (the MILP reoptimization and scheduling-with-predictions papers) are the closest to our paper in character. Our paper sits in the 5.5-6.5 range — it has a cleaner practical motivation and simpler, more verifiable empirical results than the MILP reoptimization papers, but the unexplained LP constraint change and presentation issues prevent it from reaching the 6.5+ tier.

**Narrowing**: Comparing against the 6.00 MILP reoptimization anchor and the 6.25 IP diffusion anchor: our paper's strengths have higher favorability (10.49-13.28 vs 9.44-12.89) and our weaknesses have higher (less damaging) favorability (0.24-1.72 vs the 6.25 paper's weaknesses going down to -2.86). The 6.25 paper was rejected despite its score because it had a fatal comparison gap; our paper has no such fatal flaw. This places our paper at **6.0**.

Here is the final review:

## Summary

This paper addresses a practical problem: major AI conferences enforce per-author submission limits by desk-rejecting excess papers in simple submission-ID order, discarding papers arbitrarily. The authors formalize the desk-rejection problem as a maximum-coverage integer program (maximize accepted papers subject to per-author limits), relax it to an LP, and round the fractional solution to a feasible integer solution. Using 11 years of ICLR data (2013–2025), they show consistent improvements over current policies, saving up to 10–13% more papers at practically relevant limits and up to 19% in specific cases.

## Strengths
- **A genuinely practical problem, well-motivated.** The paper addresses a real policy gap that affects thousands of submissions annually. Section 1 and Table 1 document the prevalence of this policy convincingly (e.g., CVPR 2025 uses limit 25, KDD 2025 uses limit 7, etc.).
- **Clean, appropriate formalization.** The maximum-coverage IP (Definition 4.1: maximize 1_m^T x subject to Ax ≤ b·1_n, x ∈ {0,1}^m) is the right abstraction for "accept as many papers as possible while respecting per-author limits."
- **Empirical evaluation on real historical data.** Using 11 years of ICLR data (2013–2025) crawled from OpenReview grounds the results in realistic submission patterns. Table 2 shows the authorship matrix statistics, and the evaluation covers a wide range of submission limits b ∈ {4,5,…,25}.
- **Consistent empirical improvement.** Across all years and all limits where desk rejection is non-trivial, the proposed method rejects fewer papers than both baselines. Table 3 shows the improvements are modest in absolute terms but consistent — no case where it does worse than the baselines.

## Weaknesses

### Major
- **The LP relaxation changes the constraint RHS without justification.** Definition 4.3 changes the constraint from `Ax ≤ b·1_n` (Definition 4.1) to `Ax ≤ b - 1_n` — tightening each author's bound by 1 — without any explanation. The paper states only "we relax the domain of x to [0,1]^m" (line 213), which is incomplete: it also changes the constraints, making the feasible region a strict subset of what a standard LP relaxation would define. This tightened bound clearly creates slack for the rounding algorithm (Algorithm 3), but the paper never acknowledges the change, explains why a margin of 1 is both necessary and sufficient, or proves its interaction with the rounding guarantee in the main text. A reader cannot verify the algorithm's correctness from the main text alone. (The proof is in the stripped Appendix B, but the design choice itself needs justification in the main text.)

### Minor
- **Contradictory claims about randomness.** Algorithm 4 (line 275) says "Randomly initialize x_0," and the introduction mentions "randomized rounding" (line 46). However, Section 5.1 (line 374) states "The experiments are deterministic and contain no randomness." The rounding algorithm (Algorithm 3) is also purely deterministic (greedy arg-max selection, then zeroing out). These are contradictory. If the LP solver finds the global optimum regardless of initialization (LP is convex), the paper should state this; otherwise, variance reporting is needed.
- **Headline number is not representative.** The abstract emblazons "up to 19% unnecessary desk-rejections" / "19.23% more papers" (line 49), which comes from ICLR 2024 at b=22, where the absolute difference is only 5 papers (26 vs. 21). The percentage is inflated by a small denominator. At more practically relevant limits (b=4,7,10) the improvements are 10–13% — still meaningful, but the headline figure is not typical.
- **The "computational hardness" claim is unsubstantiated.** The introduction says "we establish the computational hardness of the problem" (line 45), but the main text only states it is "inherently related to the multi-dimensional knapsack problem" (line 213) without a formal NP-hardness statement or proof sketch. For a highlighted contribution, this is insufficient.

### Trivial
- **Imprecise "equivalence" wording.** The paper states the reverse greedy algorithm (Algorithm 5, in appendix) is equivalent to the forward version (Algorithm 2) "due to its equivalence" (line 153). They process papers in opposite orders and may produce different desk-rejection sets, so they are not equivalent in output.

## Nice-to-Haves
- **Measure the gap to the true IP optimum.** On smaller instances (ICLR 2013–2017, n ≤ 1474, m ≤ 490), an IP solver could find the true optimum. Showing the LP+rounding solution is within a few percent of optimal would substantially strengthen the claim of near-optimality.
- **Quantify the reviewer workload trade-off.** Since the algorithm accepts more papers, reviewer workload is higher. A simple table showing additional papers entering review per year per b would clarify the practical implications.

## Removed Points
- Criticism about code/data not released at review time — paper states it will be released upon acceptance; rule says not to question cited availability.
- Baseline comparison against true IP optimum — moved to nice-to-have; the chosen baselines (actual conference policies) are appropriate scope.
- 53.64 seconds runtime characterization as "not remarkable" — subjective opinion, not a weakness.
- Table 3 readability nitpick — formatting concern.
- "Safe author" preprocessing speedup analysis — implementation detail, not a core weakness.
- Sensitivity to submission order — the paper's method is order-independent, which is an advantage the paper could emphasize more (nice-to-have).
- Approximation guarantee — the paper does not claim one; acceptable for a practical heuristic.

## Novel Insights
None beyond the paper's own contributions. The reviews confirm the paper's practical value and identify genuine expository gaps, but do not uncover findings the authors missed.

## Suggestions
1. **Explain the `b-1` constraint change in Definition 4.3** with a clear justification of why the margin of 1 is both needed for the rounding guarantee and sufficient for feasibility.
2. **Resolve the randomness contradiction** — either remove "Randomly initialize" from Algorithm 4 (if deterministic) or report variance.
3. **Add a formal NP-hardness statement** in Section 4.1 to substantiate the computational-hardness claim.
4. **Tone down or contextualize the 19.23% headline** — report it alongside the more representative 10–13% improvements.

## Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jBYQAtzp5Z.md (Competitive Fair Scheduling) | 6.80 | 1 | Yes | Stronger theory and presentation; weaker practical connection |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/scdGzuwC9u.md (MILP Reoptimization) | 6.00 | 1,2 | Yes | More complex method but with more damaging weaknesses (error propagation, no convergence guarantees); our paper has comparable strengths but less severe weaknesses |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bLhqPxRy3G.md (LP via diagonal networks) | 5.75 | 1 | Yes | Theory paper with limited real-world experiments; our paper is stronger empirically |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/joMMM9eadc.md (Feasible Solutions via Diffusion) | 6.25 | 2 | Yes | Complex ML approach with high feasible ratio but fundamental gap (no comparison to optimal); our weaknesses are less severe |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8eNLKk5by4.md (Constrained MDPs) | 6.00 | 1 | No | Theoretical CMDP paper; different domain |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/McfYbKnpT8.md (L2P-MIP) | 6.50 | 2 | No | Stronger optimization contribution; our paper has clearer practical motivation |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FPfCUJTsCn.md (Differentiable ILP) | 7.20 | 2 | No | Significantly stronger theoretical contribution with unsupervised learning for ILP; our paper is simpler and more applied |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/psDvcWtFdE.md (DIG-MILP) | 3.00 | 1 | No | MILP data generation; different type of contribution, lower impact |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/o0oroLuPLZ.md (SP-R-IP) | 4.60 | 1 | No | Decision-focused learning for LP; narrower contribution |

**Score placement rationale**: The round-1 bracket was 5.5–6.5. Round 2 narrowed by comparing itemized favorability: our paper's strengths (10.49–13.28) match or exceed the 6.00 MILR reopt paper (10.31–12.60) and the 6.25 diffusion paper (9.44–12.89). More importantly, our paper lacks the sub-zero weaknesses (-2.86, -0.70) that pulled down both those papers — our lowest favorability weakness is -0.90 (Trivial) and the next is 0.24 (Minor). The main drag is the unexplained b-1 constraint (favorability 1.02), which is a significant presentation gap but fixable. This places the paper at **6.0** — a borderline-accept paper whose real contribution is undermined by an expository gap that the authors can plausibly address.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>