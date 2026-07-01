## Summary

This paper proposes WeCAN, an end-to-end RL framework for heterogeneous DAG scheduling with task-resource compatibility. Key contributions include: (1) a weighted cross-attention (WeCA) mechanism that places compatibility coefficients outside softmax to preserve magnitude information across resource pools; (2) a longest directed distance GNN (LDDGNN) for encoding task dependencies; (3) a skip-action mechanism adapted to single-pass inference to close the optimality gap of list scheduling; and (4) theoretical analysis of the list-scheduling optimality gap and conditions for surjectivity. Experiments on TPC-H and Computation Graphs benchmarks show 7.7–9.5% improvements over the best neural baseline and 13–18% over heuristics.

## Strengths

- **Weighted cross-attention is a well-motivated architectural contribution.** Placing compatibility coefficients outside softmax (Eq. 2, Section 3.1) preserves overall compatibility magnitude across pools, unlike "inside" placement or averaging approaches in prior work. The illustrative example with two tasks of identical attributes but different compatibility profiles convincingly demonstrates the limitation of inside placement. This is a genuinely novel architectural innovation for the heterogeneous scheduling setting.

- **Strong empirical gains on realistic benchmarks.** On TPC-H (industry-standard decision-support benchmark), WeCAN-S(256) achieves 18.1% improvement over the best heuristic and 7.7% over the best neural baseline. On Computation Graphs, improvements are 13.4% over HEFT and 9.5% over One-Shot. The greedy mode achieves runtimes comparable to heuristic methods (0.15–1.72s), which is the advertised use case.

- **Skip-action adaptation to single-pass inference is non-trivial.** Deriving skip coefficients u_a, u_b, u_c from pooled embeddings in a single pass and using the formula u_a(1 − k/(2n))^{u_b} + u_c to produce a monotonic decaying score avoids the multi-round processing required by prior skip-action methods (Mao et al., 2016). Theorem 1's proof that the resulting generation map is a surjection (can reach the optimal solution) is a meaningful theoretical contribution.

- **Theoretical analysis of the list-scheduling optimality gap (Section 4)** provides a clean framework (original space A, reduced space B, maps T and S) for reasoning about when and why skip actions are needed, with concrete connection to "heavy tasks" (high resource demand, long duration).

## Weaknesses

### Major

- **One-Shot baseline adaptation is not transparent.** The paper acknowledges that One-Shot "does not consider compatibility coefficients or pool allocation" (Section 1), as it was designed for homogeneous settings. Yet One-Shot is used as a neural baseline in the main results, and improvements of 7.7–9.5% over it are cited as headline claims. The paper never explains how One-Shot was adapted to handle pool allocation and compatibility coefficients in the heterogeneous setting — whether via a heuristic pool-selection rule, fixed assignment, or some other mechanism. Without this clarification, it is unclear whether the comparison is fair or whether One-Shot is disadvantaged by the setting. The core empirical contributions (gains over heuristics) are substantial regardless, but the neural-baseline comparison claims need proper qualification.

### Minor

- **Statistical reporting is incomplete.** (a) Greedy results (WeCAN-Greedy) in Tables 1 and 2 have no variance estimates at all, even though greedy is presented as the primary use case. (b) The reported standard deviations for sampling methods are "among random seed" (Table 1 caption), i.e., across network initialization seeds rather than across test instances — the variability that matters most to practitioners. (c) The number of test instances for the main results (Tables 1, 2) is not stated; the ablation section states 10 problems. These issues weaken the apparent precision of the reported improvements but do not invalidate the core conclusions.

- **Skip-action formula is under-justified.** The specific functional form u_a(1 − k/(2n))^{u_b} + u_c is motivated informally ("prevents the skip action from overly prioritized"). The paper does not discuss why this form was chosen over alternatives (e.g., exponential decay), nor does it analyze training dynamics for u_b (the exponent). The claim that "our design clusters most poor solutions in the high-u_a, high-u_c region" (Section 4.2) is stated without supporting evidence or visualization. These are not fatal — the mechanism works empirically — but the design choices are less grounded than the paper suggests.

- **Heavy-task ablation conflates attention placement and skip action.** The heavy-task experiment (Figure 3) compares WeCAN-S(256) against WeCAN-inside-S(256), but WeCAN-inside changes both the attention placement (inside vs. outside softmax) and presumably removes skip actions. This conflates two factors. A cleaner ablation would compare the full method with vs. without skip actions while keeping the attention mechanism fixed.

### Trivial

None.

## Nice-to-Haves

- The paper could analyze why LDDGNN outperforms GAT variants (Table 3) — e.g., through attention pattern visualization or analysis of long-range dependency capture. Currently the superiority is empirical but not explained.
- Generalization experiments (Figure 2) test one factor at a time (pool count, pool type, task count, task type). Testing simultaneous variation or cross-dataset generalization would strengthen the claims of robustness.
- A proper "skip vs. no-skip" ablation keeping the architecture fixed (as noted under Minor weaknesses) would strengthen the skip-action analysis.

## Removed Points

- **PRO-BALM baseline undefined in Figure 3:** The figure description shows "PRO-BALM" as one entry alongside two WeCAN-S(256) entries with different colors, strongly suggesting parser-level text garbling. The hard rule about formatting artifacts applies; this cannot be confirmed as an author omission.
- **Non-autoregressive decoder limitation not acknowledged:** The paper explicitly states "(comparison with auto-regressive one in Appendix B)" — the appendix is stripped by the parser, but the paper does acknowledge this trade-off.
- **Training details absent from main text:** These are in the appendices (stripped by parser); the rule about missing appendix criticisms applies.
- **F(t,v) vs F(t,c) notational inconsistency:** Parser-level formatting artifact.
- **One-Shot runtime comparison as "apples-to-oranges":** The paper transparently reports runtimes for all methods; the PPO-BiHyb runtime difference is evident from the tables and is an acknowledged property of the baseline, not a weakness.
- **Criticism about LDDGNN not being empirically motivated:** The paper does show empirical comparison (Table 3: GAT variants vs LDDGNN). Requesting deeper analysis of why LDD works better is scope expansion, not a flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Clarify how One-Shot was adapted to the heterogeneous setting. If extended with a pool-selection rule, describe it; if not, acknowledge the limitation and qualify the neural-baseline improvement claims.
- Report instance-level variance (or at minimum specify the number of test instances) for all main-table results, including greedy mode.
- Add a clean ablation: WeCAN with skip vs. WeCAN without skip (same architecture, skip action disabled during inference).
- Provide evidence or analysis for the claim that poor solutions cluster in the high-u_a, high-u_c region.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>