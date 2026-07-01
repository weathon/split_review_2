Now let me produce the final review.

## Summary

The paper proposes WeCAN, an end-to-end RL framework for heterogeneous DAG scheduling with task-pool compatibility. Its main contributions are: (1) a weighted cross-attention (WeCA) mechanism that encodes compatibility coefficients between tasks and resource pools while remaining adaptable to varying problem sizes; (2) a longest-directed-distance GNN (LDDGNN) for dependency encoding; (3) a theoretical analysis of the optimality gap in list scheduling, with a skip-action mechanism designed to close this gap in a single-pass setting; and (4) empirical results on TPC-H and Computation Graphs benchmarks showing 13-14% improvement over heuristics and 7-9.5% over the best neural baseline.

## Strengths

1. **The WeCA mechanism is architecturally well-motivated.** Section 3.1 provides a clear rationale for placing the compatibility coefficient outside (multiplying after) softmax rather than inside it, with a concrete example showing how the naive inside placement would fail to distinguish tasks with identical attributes but different compatibility profiles. This is a genuine architectural insight.

2. **The theoretical analysis of the list scheduling optimality gap (Section 4) is a substantive contribution.** The paper identifies that TS_list is neither the identity nor surjective, meaning list scheduling collapses multiple schedule orders to the same feasible schedule and can exclude the optimal solution. Framing this in terms of spaces A and B and maps T and S is clean and provides principled grounding for the skip-action mechanism.

3. **Empirical results are strong and consistent across two datasets.** On TPC-H (Table 1), WeCAN-S(256) achieves ~13-14% improvement over the best heuristic and ~7-8% over One-Shot. On Computation Graphs (Table 2), improvements are 9-11% over HEFT and 9-10% over One-Shot across three graph families (Erdős-Rényi, Layer Graphs, Stochastic Block Models). Results hold across problem sizes (30 to 100 nodes).

4. **The ablation study (Table 3) is informative and well-designed.** Testing six architectural variants — including the inside version of WeCA, decoder-only WeCA, and GAT replacements for LDDGNN — clearly demonstrates that each component contributes. Skipping WeCA layers entirely drops improvement from 14.0% to 0.5% on TPC-H-30, providing a strong sanity check that the main claimed innovation is doing real work.

## Weaknesses

### Fatal

None.

### Major

1. **Missing heterogeneous-specific neural baselines weaken the "state-of-the-art" claim.** The paper cites Zhou et al. (2022), Zhadan et al. (2023), and Wang et al. (2025) in lines 36-48 as methods specifically designed for *heterogeneous* DAG scheduling, but none is included as a baseline. The only neural baselines are PPO-BiHyb (a bi-level method, not designed for heterogeneous compatibility) and One-Shot (Jeon et al., 2023) — which the paper itself criticizes (lines 28-31) for not considering compatibility coefficients or pool allocation. While the paper sketches reasons for exclusion (lines 39-48: averaging compatibility coefficients, fixed-size embeddings), the claim of "outperforming state-of-the-art methods" (abstract, line 9; line 69) is not properly supported without comparing against at least one heterogeneous-specific neural scheduler. The improvement over heuristics (13-14%) is meaningful on its own, but the neural-comparison claim as presented is inflated by the baseline choice.

2. **Skip-action ablation is only conducted on artificially modified data, not on the standard benchmarks.** The skip action is presented as a central contribution (contributions 3 and 4; Theorem 1; Section 4). However, its empirical evaluation (Figure 3) is confined to a modified version of TPC-H where 1% of tasks are replaced with artificially "heavy" tasks. There is no ablation showing what WeCAN achieves *without* skip on the standard TPC-H or Computation Graphs benchmarks (Tables 1, 2). The reader cannot tell whether the 14% improvement over heuristics comes from the WeCA architecture, the skip action, or both. Given that skip is one of four claimed contributions, this is a significant evidential gap.

### Minor

3. **Theorem 1's guarantee is representational, not a learning result.** Theorem 1(iv) states "there exist scores enabling an optimal solution" — this is an existence/expressiveness result. The REINFORCE training procedure has no convergence guarantee to this regime. The paper's phrasing in line 210 ("our design ensures that TS is a surjection, enabling the generation of the optimal schedule") could be read as claiming the learned policy actually finds optimal solutions. The theorem statement itself is precise, but the surrounding language should more carefully separate representational capacity from learned performance.

4. **The "processing time close to heuristics" claim only holds for the greedy variant.** The abstract and introduction (line 55) claim single-pass inference yields processing time close to heuristics. On TPC-H-30, WeCAN-Greedy (0.15s) is indeed comparable to HEFT (0.18s). But WeCAN-S(256) (2.43s) is ~13× slower than HEFT. The claim should be qualified to apply specifically to the greedy (single-pass) mode.

5. **The adaptability experiments (Figure 2) lack training-environment details in the main text.** The paper reports WeCAN achieving 20.4% (more pool) and 19.3% (more task type) improvement vs. One-Shot's 9.2% and 10.2%, but does not specify the training conditions (number of pools, task types, etc.) in the main body. The appendix was stripped from the submission bundle, so these details are not verifiable from the main text.

6. **The REINFORCE baseline is underspecified.** Line 186 states the baseline is "taken as average rewards" without clarifying whether this is a batch average, an exponential moving average, or a learned baseline.

7. **Several design choices are heuristic and presented without derivation.** The skip score formula $u_a(1 - k/2n)^{u_b} + u_c$ (line 145) and the claim that LDDGNN captures "undirected dependency structure" in a DAG (line 133) lack justification.

### Trivial

8. Standard deviations are reported for One-Shot and WeCAN sampling methods but not for heuristic baselines or WeCAN-Greedy in Tables 1-2. While greedy methods have zero within-seed variance, reporting across-instance variance would allow significance assessment.

## Nice-to-Haves

- **Comparison to MILP optimal solutions on small instances.** The paper frames the problem as an MILP and provides theoretical analysis of optimality gaps but never compares WeCAN's solutions to the MILP optimum on tractably small instances (e.g., 10-20 tasks). This would calibrate the practical significance of the theoretical guarantees.
- **A skip-action ablation on the standard TPC-H benchmarks** (not just the heavy-task modification) would fully disentangle the contributions of WeCA and skip. If the paper's theory correctly predicts skip matters most with heavy tasks, running this ablation and confirming that finding would strengthen the narrative.

## Removed Points

- **LDDGNN/LDDNN naming inconsistency (LSTM label in Figure 1 caption).** The figure caption text extracted from the PDF says "LDDNN (Long Short-Term Memory Network)" while the text correctly describes "LDDGNN (Longest Directed Distance based Graph Neural Network)." This is almost certainly a parser artifact from OCR of the embedded figure image, not an author error. Removed per the hard rule on formatting/parser artifacts.
- **"No comparison to optimal MILP solutions"** was moved from weaknesses to Nice-to-Haves because it is a strengthener that does not threaten any core claim of the paper.
- Several generic or speculative concerns from the source review (e.g., "could the metric be measuring a proxy?", "may be in the appendix") were removed because they lack concrete anchoring in the paper text.
- Criticisms about missing appendix/proof content were removed since the parser strips those sections from all papers.

## Novel Insights

None beyond the paper's own contributions. The reviews identify genuine gaps in the evidence (missing heterogeneous baselines, skip-ablation scope) but do not uncover novel interpretations of the paper's results or methodology.

## Suggestions

1. **Add at least one heterogeneous-specific neural baseline** from the papers cited in lines 36-48 (Zhou et al., 2022; Zhadan et al., 2023; Wang et al., 2025). If adaptation of these methods is non-trivial, explain why clearly rather than leaving the omission implicit.
2. **Run WeCAN without the skip action on the standard benchmarks** (TPC-H and Computation Graphs) and report the results alongside the full model. If skip contributes little on standard data, that is useful information for readers and consistent with the paper's own theory; if it contributes substantially, that strengthens contributions 3 and 4.
3. **Qualify the "close to heuristics" runtime claim** to specify it applies to the greedy (single-pass) mode, not the sampling mode.
4. **Specify the REINFORCE baseline details** (what "average rewards" means — batch average, EMA, etc.) and add a sentence summarizing the training environment conditions used for Figure 2.
5. **More carefully separate representational guarantees from learned guarantees** in the discussion of Theorem 1.

## Score and Decision

This paper has genuine strengths: a well-motivated architectural contribution (WeCA), a principled theoretical analysis of list scheduling optimality gaps, and strong empirical results across two datasets. The weaknesses are real but addressable: the "state-of-the-art" claim is not fully supported due to missing heterogeneous-specific baselines, and the skip-action contribution is not properly ablated on standard benchmarks. Neither flaw invalidates the core method or its demonstrated improvement over heuristics. With revisions, this would be a strong paper.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>