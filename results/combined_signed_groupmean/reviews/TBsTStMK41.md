Now I have a clear picture from calibration. Let me compile the final review.

## Summary

This paper formalizes the desk-rejection problem under per-author submission limits at AI conferences as a maximum desk-acceptance integer program (IP), proposes a practical two-stage algorithm (LP relaxation + greedy rounding), and evaluates it on 11 years of ICLR submission data. The method consistently reduces desk-rejections compared to existing policies, preserving up to 19.23% more papers while satisfying author-level submission limits.

## Strengths

- **Clean formalization.** The maximum desk-acceptance IP (Definition 4.1) is a natural and precise mathematical reframing that correctly identifies the inadequacy of current feasible-solution-only formulations (Definition 3.1). This gives the community a clear optimization target for a practical problem.

- **Substantial real-data evaluation.** The paper crawls 11 years of ICLR data via OpenReview (Table 2), producing a dataset spanning 161–38,495 authors and 67–11,672 papers, evaluating over b ∈ {4,5,…,25} across all years. The scale (up to 61,992 nonzeros in the authorship matrix for 2025) makes the runtime claim (≤53.64 seconds) meaningful.

- **Consistent empirical improvement.** Table 3 shows the proposed method outperforms both baselines across nearly all years and b values where desk-rejection occurs. Improvement reaches 19.23% (ICLR 2024, b=22) and is consistently 5–15% for moderate b in recent years. For 2024 and 2025, improvement appears at every b value.

## Weaknesses

### Major

- **No comparison to the true IP optimum or LP upper bound.** The paper claims to "maximize" desk acceptance but evaluates only against two existing policies (ALLREJECT, FORWARDREJECT). The maximum desk-acceptance IP (Definition 4.1) has m ∼ 10^4 binary variables and n ∼ 10^4 constraints — a packing problem with 0-1 coefficients well within reach of standard solvers (PuLP supports integer programming). Without comparing the heuristic solution to the IP optimum, the reader cannot tell whether the method achieves 50% of the possible improvement or 99%. The LP relaxation value provides an immediate upper bound on the IP optimum but is never reported. This gap between the "maximizing" framing and the actual evaluation scope is the paper's most significant limitation.

### Minor

- **LP relaxation constraint discrepancy.** Definition 4.3 reads `Ax ≤ b − 1_n` while the original IP (Definition 4.1) correctly has `Ax ≤ b · 1_n`. If the vector expression is literal, each author's constraint is tightened by 1, which could systematically reduce the LP-selected set. The authors must confirm that the implementation used `b · 1_n` (the correct relaxation of the IP) and not `b−1`.

- **Tension between random initialization and claimed determinism.** Algorithm 4 (OPTREJECT) includes "Randomly initialize x₀" (line 275), but Section 5.1 states "The experiments are deterministic and contain no randomness." If the LP solver is deterministic regardless of initialization, this should be clarified. If initialization matters, the claimed determinism is incorrect.

- **Rounding algorithm design choices unjustified.** Algorithm 3 (MAXROUNDING) selects the fractional variable with the largest value without motivation or ablation against alternatives (e.g., fewest co-authors first, most-constrained author first). Theorem 4.6 only proves feasibility, providing no objective-value analysis relative to the LP or IP optimum.

### Trivial

None.

## Nice-to-Haves

- Report absolute savings (papers rescued) alongside relative percentages in Table 3, since the "19.23% improvement" at ICLR 2024 (b=22) corresponds to saving 5 papers out of 7,404. The relative figure sounds dramatic but the absolute impact is modest in that specific cell.
- Compare against a randomized rounding baseline with a multiplicative guarantee.

## Removed Points

These points from the harsh critic input are removed with justification:

- *"The algorithm does not maximize desk-acceptance — it is a heuristic with no optimality or approximation guarantee. This invalidates the paper's central claim."* → The paper's central claim is demonstrably that it *improves over existing policies* (stated in abstract and contributions). The "maximizing" language refers to the IP formulation's objective, not a claim of guaranteed optimality. Repackaged as the concrete Major weakness about missing optimality comparison.
- *Calling FORWARDREJECT a "naive strawman"* → FORWARDREJECT is the actual policy used by conferences (reject by submission ID order). It is a legitimate baseline.
- *"No randomized rounding"* → The introduction mentions randomized rounding as motivation; the actual method uses deterministic greedy rounding. This is a permissible design choice, not a flaw.
- *"Missing fairness analysis"* → Out of scope for a desk-rejection algorithm paper. The ethics statement adequately covers the welfare dimension.
- *"Code/data not released"* → Standard for double-blind review.
- *"Missing related works"* → Cannot verify without external sources; all cited references are assumed to exist per instructions.
- *Typographical/formatting criticisms* → Parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviews converge on a single structural concern: the paper would significantly benefit from comparing its heuristic against the true IP optimum or even the LP upper bound, which would either justify the "maximizing" language or honestly bound the suboptimality. This gap is the primary factor separating the paper's current framing from its demonstrated evidence.

## Suggestions

1. **Solve the IP to optimality** (or to a known gap) using PuLP's integer programming capability and report the gap between the heuristic and the optimum across all years and b values. This single addition would either justify the "maximizing" framing or honestly scope the contribution.
2. **Report the LP relaxation value** alongside the rounded solution to provide an immediate, cheap-to-compute optimality gap.
3. **Clarify the `b − 1_n` vs `b · 1_n` discrepancy** in Definition 4.3 and confirm what was actually implemented.
4. **Resolve the random-initialization vs. determinism contradiction** in Sections 4 and 5.
5. **Add absolute savings** (papers rescued) alongside relative percentages in Table 3.

## Score and Decision

**Round 1 bracket:** After searching calibration anchors across score bands, the paper most closely aligns with applied OR papers scoring 4.5–6.0. The strongest topical match is Light-MILPopt (5.00), which shares a similar pattern: a practical optimization framework evaluated on real data, with a major missing comparison as the primary weakness but clear empirical improvements. The current paper has higher-magnitude strengths (formalization impact=+10.00, real-data evaluation impact=+9.89, consistent improvement impact=+10.00) than Light-MILPopt's strongest items, and its minor weaknesses have much smaller impact (-0.17, -0.00, -1.45) than Light-MILPopt's presentation issues (-10.00). The defining commonality is the single -10.00 weakness (missing IP optimum comparison for this paper; missing comparison with prior work for Light-MILPopt).

**Round 2 narrowing:** Comparing against Light-MILPopt (accepted, 5.00) and the crew pairing paper (rejected, 4.25), this paper surpasses both in evaluation thoroughness (11 years of ICLR data vs. 4 benchmark datasets in Light-MILPopt, 1 instance in crew pairing). However, it trails in methodological sophistication — the proposed approach is a straightforward LP + greedy rounding with no learning component, whereas Light-MILPopt combines GNNs, graph partitioning, and iterative refinement. The paper's contribution is genuinely practical and well-executed within its scope, supporting a score above Light-MILPopt's 5.00.

**Final placement:** The paper sits at **5.5** — the clean formalization and strong real-data evaluation push it above 5.00 anchors, while the missing optimality analysis and minor inconsistencies prevent it from reaching the 6.0+ range. The paper has a solid applied contribution that, with the suggested additions, could become a significantly stronger submission.

**Calibration anchors consulted:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/C9pndmSjg6.md` (3.00, R1) — portfolio optimization MIQP; weaker methodology, no runtime reporting. Our paper is stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/yQuF0jslCc.md` (4.50, R1) — online knapsack with predictions; strong theory but synthetic experiments only. Our paper has real data but weaker theory.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rHbxQebhDd.md` (4.25, R2) — crew pairing optimization; evaluated on single instance. Our paper's evaluation is more thorough.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/scdGzuwC9u.md` (6.00, R1/R2) — MILP reoptimization; more sophisticated methodology but ultimately rejected on novelty concerns.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2oWRumm67L.md` (5.00, R1/R2) — Light-MILPopt; accepted, shares similar profile (practical OR + real data + missing comparison weakness). Closest anchor.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5t57omGVMw.md` (8.00, R1) — learning to relax linear systems; strong theory with proofs. Our paper is substantially weaker theoretically.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NdcQQ82mfy.md` (5.67, R2) — imitation learning for branching; accepted, stronger technical contribution.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ghk8lnOYRq.md` (5.00, R2) — hyperplane clustering; pure optimization theory, less directly comparable.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>