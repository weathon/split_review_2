## Summary

This paper proposes WeCAN, an end-to-end RL framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. The key technical contributions are: (1) a weighted cross-attention (WeCA) mechanism that places compatibility coefficients outside the softmax normalization to preserve distinguishability between tasks with identical attributes but different compatibility profiles; (2) a longest-directed-distance GNN (LDDGNN) for encoding task dependencies; and (3) a skip-action mechanism in the single-pass setting that addresses the optimality gap inherent in list-scheduling-based methods. Empirical evaluation on TPC-H and Computation Graphs datasets shows makespan improvements of up to 18.1% over heuristics and 9.5% over the best neural baseline.

## Strengths

1. **Weighted cross-attention is well-motivated and non-trivial.** The placement of compatibility coefficients outside softmax (Eq. 2, Section 3.1) is accompanied by a clear argument: inside-softmax placement normalizes away differences between tasks with identical attributes but different compatibility profiles, while the outside placement preserves these distinctions. This design is purpose-built for heterogeneous scheduling and is not a standard attention variant.

2. **Theoretical analysis of skip actions is substantive.** The paper identifies and formally characterizes the optimality gap in list-scheduling-based methods (Theorem 1, Assumption 1, Theorem 2). The skip-action design with the formula $u_a(1 - k/2n)^{u_b} + u_c$ is a practical mechanism that Theorem 1(iv) shows can theoretically enable optimal solutions via greedy selection in a single network pass — addressing a genuine limitation of existing neural schedulers.

3. **Empirical results are strong across diverse settings.** WeCAN-S(256) achieves 18.1% improvement over best heuristics and 7.7% over the best neural baseline on TPC-H; on Computation Graphs the corresponding numbers are 13.4% and 9.5%. Improvements are consistent across three dataset sizes (TPC-H-30/50/100) and three graph types (Erdős-Rényi, Layer, SBM). Greedy inference (0.15–1.72s) is competitive with heuristics and orders of magnitude faster than multi-round PPO-BiHyb.

4. **Generalization experiments (Figure 2) validate size-agnostic claims.** Training on a fixed environment and testing under varied pool counts, pool features, task counts, and task types shows WeCAN maintaining advantages over One-Shot (e.g., 20.4% vs. 9.2% improvement for more pools), directly supporting the claim that WeCA's architecture delivers on its promise of adaptability.

5. **Ablation study (Table 3) is informative and honestly presented.** Six architectural variants are compared. The degradation of "WeCA-final-only + LDDGNN" to near-heuristic levels (0.5% improvement on TPC-H-30) convincingly shows that WeCA's iterative information flow throughout the network is essential, not just its one-time application.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Skip action not ablated on standard benchmarks.** The skip mechanism is evaluated only on a synthetically modified heavy-task variant (Figure 3: randomly replacing 1% of tasks with heavy tasks). The paper never compares WeCAN-with-skip against WeCAN-without-skip on the standard TPC-H and Computation Graphs datasets where the headline results are reported (Tables 1, 2). The paper's own theoretical analysis (Section 4) positions the skip action as a primary contribution (contribution 3 in the introduction), yet its contribution to the main empirical improvements (7.7–9.5% over neural baselines) is untested — these gains could be entirely from the WeCA architecture and training improvements. This is an easily fixable gap but a genuine one.

2. **Ambiguity about the One-Shot baseline's handling of compatibility.** The paper describes One-Shot in two different ways: first stating it "does not consider compatibility coefficients or pool allocation" (line 29–30), then grouping it among methods that "handle compatibility coefficients using representations like one-hot embedding of task types or fixed-dimensional vectors" (line 43–44). The paper does not describe how One-Shot was specifically configured for this heterogeneous setting — whether it was used as originally published or augmented. This ambiguity makes it harder to interpret the reported 7.7–9.5% improvements over One-Shot, though it does not invalidate the comparison.

3. **Test set sizes and statistical variance not clearly reported.** Greedy results are reported as single-point numbers with no variance. The standard deviations for sampling results are labeled "standard deviation among random seed" (Table 1 caption), which could refer to multiple training runs rather than test-instance variance. The ablation study mentions "10 test problems" — if the main results also use a similarly small test set, the reported advantages could be within noise. Without explicit test set sizes, the confidence intervals around the improvements are uninterpretable.

4. **Unsubstantiated claim about clustering poor solutions.** Section 4 states that the skip-action design "clusters most poor solutions in the high-$u_a$, high-$u_c$ region" and that "this concentration makes such regions easier to handle during training and reduces variance." No empirical evidence is provided — no analysis of learned skip parameters, distribution of poor solutions, or training variance is shown. This claim is presented as a factual benefit without support.

5. **Training conditions for generalization experiments unspecified.** Figure 2 tests under "fixed training conditions" but does not specify what those conditions were (pool count, task count, or environment configuration used for training). Without this information, the generalization results cannot be fully interpreted.

### Trivial
None.

## Nice-to-Haves
- The skip score formula $u_a(1 - k/2n)^{u_b} + u_c$ is presented without derivation or ablation. An ablation varying the functional form (different decay schedules, learned thresholds) would strengthen the paper.
- A direct experiment isolating *why* the outside-softmax placement helps (e.g., measuring embedding distinguishability) would deepen the analysis, though the ablation study already confirms it performs better.
- Reporting variance for greedy results (e.g., across random seeds or test instances) would improve completeness.

## Removed Points
- **Criticism about training details being underspecified (hyperparameters, network depth, optimizer, batch size, GPU, etc.):** REMOVED. The paper states "further experimental details provided in Appendices D, E, and H." The parser strips appendix content; the original submission contains these details.
- **"LDDNN" vs "LDDGNN" inconsistency in figure caption:** REMOVED. This is a parser artifact (the figure caption is OCR'd from an image).
- **Criticism that One-Shot comparison is structurally unfair:** PARTIALLY RETAINED and softened. The paper itself creates ambiguity by describing One-Shot in two different ways. I kept a clarified version as Minor weakness #2 about clarity rather than fairness.
- **Theoretical analysis (Theorem 1) only provides existence result:** REMOVED. The paper acknowledges this implicitly, and Theorem 1(iv) is clearly stated as an existence result. This is a correct characterization, not a weakness.

## Novel Insights
The paper's key insight — that the optimality gap in list-scheduling-based neural schedulers arises because the list-scheduling map is not surjective onto the optimal schedule, and that skip actions in a single-pass setting can restore surjectivity without multi-round computation — is well-identified and cleanly formalized. The reviewer's most useful observation is that this secondary contribution (skip actions) is only validated on a synthetic heavy-task variant, while its contribution to the headline numbers on standard benchmarks remains unknown. This does not undermine the primary contribution (WeCA architecture) but is an easily fixable empirical gap that should be addressed.

## Suggestions
1. **Add a skip-action ablation on standard benchmarks.** Train WeCAN without skip actions and compare makespan on the standard TPC-H and Computation Graphs datasets. This directly quantifies the skip action's contribution to the headline results and would significantly strengthen the paper.
2. **Clarify One-Shot adaptation.** State explicitly whether One-Shot was modified for the heterogeneous setting and, if so, how. If it was used as published, explain what mechanism (if any) One-Shot uses to handle compatibility coefficients.
3. **Report test set sizes** for all experiments and add confidence intervals or variance for greedy results.
4. **Provide empirical support** for the claim about clustering poor solutions in the high-$u_a$, high-$u_c$ region (e.g., visualization of learned skip parameters).
5. **Specify the training environment configuration** used for the generalization experiments in Figure 2.

## Score and Decision

**Calibration anchors used (all from `deepreview_13k_calibration`):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `10eQ4Cfh8p.md` (FJSP RL) | 3.0 | Bracket | Significantly weaker — missing baselines, no std dev, poor writing |
| `b9aCXHhdbv.md` (Pipeline Parallelism DRL) | 4.5 | Bracket | Weaker evaluation, less clear novelty, comparable idea quality |
| `8WtBrv2k2b.md` (Quantum Resource Scheduling) | 5.0 | Bracket | Mixed reviews (3,3,6,8), significant clarity concerns, comparable empirical scope |
| `CJEBFNBLhO.md` (Massively Parallel CO) | 4.25 | Bracket | Engineering contribution with limited novelty; our paper has clearer novelty |
| `jBYQAtzp5Z.md` (Competitive Fair Scheduling) | 6.8 | Bracket | Stronger theoretical rigor, comparable evaluation; our paper has more novel architecture |
| `Cs6MrbFuMq.md` (HexGen-2) | 6.0 | Bracket | Comparable quality — solid system contribution with some clarity gaps |

**Round 1 bracket:** 5.5–6.5. The paper is clearly above the 3–5 range (which contain papers with missing baselines, no std dev, poor novelty) but below the 7+ range (papers with comprehensive theory and near-flawless evaluation). The core contributions are genuine and well-evaluated, but the missing skip ablation on standard benchmarks and clarity issues prevent a higher score.

**Final score:** 6.0 — Borderline Accept. The weaknesses are all addressable and do not invalidate the core claims. If the authors add the skip-action ablation and clarify the One-Shot comparison, the paper would be a solid addition to the literature.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>