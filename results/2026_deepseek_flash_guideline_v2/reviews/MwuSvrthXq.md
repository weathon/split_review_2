Now I'll write the final consolidated review.

## Summary

The paper proposes WeCAN, an end-to-end RL framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. Two main contributions: (1) a weighted cross-attention (WeCA) layer that integrates compatibility coefficients outside the softmax normalization, enabling the network to handle variable numbers of pools and task types; (2) a skip-action mechanism that, in a single-pass setting, provably restores surjectivity of the generation map (Theorem 1), closing an optimality gap inherent in list-scheduling-based methods. Experiments on TPC-H and Computation Graphs benchmarks show 14–18% improvement over heuristics and 7–14% over neural baselines, with single-pass inference times competitive with heuristics.

## Strengths

1. **Weighted Cross-Attention with outside-softmax compatibility weighting (Section 3.1).** The WeCA layer places compatibility coefficients as a diagonal weighting matrix outside the softmax normalization (`diag{K_acc(...)} V^c`). The ablation study (Table 3) validates this design: WeCA-outside+LDDGNN achieves 14.0% improvement over Tetris on TPC-H-30, while WeCA-inside+LDDGNN achieves only 10.5%, and removing WeCA layers entirely collapses performance to 0.5%. This directly addresses the limitation in prior work (lines 40–48) that fixed-size or averaged compatibility representations lose fine-grained information.

2. **Skip-action mechanism with formal guarantees (Section 3.2, Theorem 1).** The paper designs a single-pass skip score computed once from initial network embeddings (`u_a(1 − k/(2n))^{u_b} + u_c` ), avoiding multi-round processing required by prior skip-action approaches (Mao et al., 2016). Theorem 1 proves that (iii) without skip actions the scheduler provably cannot reach optimal solutions for some problems, and (iv) with skip actions there exist scores enabling greedy optimal selection. Empirical validation (Figure 3) shows WeCAN with skip achieves +8.3% improvement over HEFT on heavy-task instances, while the non-skip variant achieves −2.3%.

3. **Formal characterization of list scheduling's optimality gap (Section 4).** The paper traces list scheduling's inability to guarantee optimality to the fact that `TS_list` is neither the identity nor surjective (line 198), causing it to shrink its image away from optimal solutions. Theorem 2 establishes that a generation map satisfying Assumption 1 (injectivity and objective improvement) suffices to include optimal solutions. This goes beyond prior empirical observations by pinning the gap to a specific structural property of the generation map.

4. **Single-pass runtime competitive with heuristics (Table 1).** WeCAN-Greedy runs in 0.15s on TPC-H-30, comparable to HEFT (0.18s) and Tetris (0.21s), while the only prior single-pass neural method (One-Shot) produces worse schedules, and multi-round PPO-BiHyb takes 20.48s. This concretely demonstrates the efficiency claim.

5. **Robustness to environment fluctuations (Figure 2).** WeCAN maintains strong performance under unseen variations in pool count, pool types, task count, and task types — all without retraining. Under "more pool type" variation, WeCAN achieves 6.7% improvement over heuristics vs. One-Shot's 0.9%; under "more task type," 19.3% vs. 10.2%. These gaps directly support the claim that the weighted cross-attention mechanism preserves adaptability across varying heterogeneous configurations.

## Weaknesses

### Major

- **The One-Shot baseline comparison is not on equal footing.** The paper's related work (lines 27–34) states that One-Shot "does not consider compatibility coefficients or pool allocation." Despite this, One-Shot is used as a primary neural baseline without stating whether it was adapted in any way for the heterogeneous setting. The claimed 7.7% improvement over the "best neural baseline" is partly driven by this asymmetry (One-Shot-S(256): 20399 on TPC-H-30 vs. PPO-BiHyb: 21941 — One-Shot is already much better, likely because it uses 256 samples while PPO-BiHyb uses beam search of a different size). *However*, this weakness is substantially mitigated: WeCAN also outperforms PPO-BiHyb (which *is* designed for heterogeneous settings) by 7–14% across all datasets, so the core result does not depend on the One-Shot comparison. The paper should transparently acknowledge this and either adapt One-Shot or qualify the comparison.

### Minor

- **The skip-action mechanism's empirical validation is narrower than its theoretical treatment.** Theorem 1 makes strong claims about closing the optimality gap, but is supported only by a single ablation: 1% heavy tasks on TPC-H-30 and TPC-H-50 (Figure 3). While the results are clear (WeCAN with skip +8.3% vs. non-skip −2.3%), the evaluation would benefit from (a) verifying against known optimal solutions on small synthetic instances (e.g., via MILP), (b) reporting how often skip actions are selected during inference, and (c) testing across a wider range of task characteristics.

- **Limited pool variation in main experiments.** All main results (Tables 1, 2) use exactly 3 pools. While Figure 2 tests generalization to different pool counts, the core performance evaluation would be more convincing with experiments at 5, 10, or more pools, given that pool-count adaptability is explicitly claimed as an advantage.

- **Ablation study uses only 10 test problems (Table 3).** While the results are consistent and the ablation is well-designed, the small test set limits statistical confidence, especially for high-variance variants (e.g., WeCA-decoder-inside+LDDGNN with SD 195–72 on small makespans).

### Trivial

None.

## Nice-to-Haves
- Report the frequency of skip actions selected during inference (fraction of steps where skip is taken, distribution across instances).
- Add statistical significance tests (e.g., paired tests) for the main results across instances.
- Include a brief limitations paragraph discussing when WeCAN might underperform (e.g., very large graphs, extreme heterogeneity).
- Clarify how the resource demand vector p(v) and capacity vector λ(c) interact with compatibility coefficients in the experiments — these are introduced in the formulation but not discussed further.

## Removed Points

The following points from the Harsh Critic were removed after verification against the paper:

1. **"Inside vs. outside placement argument is not sound as stated."** — Removed because the specific counter-argument is incorrect. The paper's example (line 125) states "two pools with **identical capacity**." With identical pool features (same k, same V), the inside placement yields the same weighted value for both tasks (V for the task compatible with one pool, 0.5V+0.5V=V for the task compatible with both). The paper's specific claim is mathematically correct. The broader point about the motivation being example-specific rather than a general proof is reasonable but is covered by the Nice-to-Haves above. The Harsh Critic's counterargument assumed pools must differ in value representations, which contradicts the explicit scenario in the paper.

2. **"Suspiciously low variance."** — Removed. The table header states "standard deviation among random seed," meaning variation of the final metric across different training seeds. With 256 samples per evaluation and REINFORCE with baseline, low cross-seed variance is expected and not suspicious. One-Shot similarly shows low variance (SD 108–181). This is a misunderstanding of the experimental setup.

3. **Generic criticisms about missing training details in main text** — Removed per hard rules. The paper defers architecture details, hyperparameters, and training specifics to appendices. The parser strips these sections from all papers; they exist in the original submission.

4. **Complaints about missing error bars on heuristic baselines** — Removed. Heuristics (SFT, MOPNR, CP, HEFT, Tetris) are deterministic algorithms; variance is inapplicable.

5. **Strength Finder's outputs** — All five strengths were specific, concrete, and evidence-backed. None were generic or superficial. All kept.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
1. **Clarify the One-Shot comparison.** State whether One-Shot was adapted for heterogeneous settings. If not, explicitly note this limitation and center the narrative on the PPO-BiHyb and heuristic comparisons, which are already strong.
2. **Directly verify the skip-action optimality claim.** Add a small-instance experiment (6–20 tasks, solvable via MILP) showing that the skip-enabled policy assigns positive probability to and can greedily select optimal solutions that list scheduling misses.
3. **Report skip-action statistics.** Show the fraction of steps where the skip action is selected and its correlation with makespan improvement.
4. **Expand pool-count experiments.** Add results with 5, 10, or 20 pools to substantiate the claimed scalability.

## Score and Decision

### Calibration

The calibration retrieval tool encountered a persistent data availability issue (the index references files that do not exist on disk across multiple retries with different queries and batch sizes). I therefore proceed without retrieved anchors. Instead, I calibrate against the ICLR scale directly using the paper's content.

### Assessment

This paper makes two clear, well-supported technical contributions (WeCA layer, skip-action mechanism) accompanied by non-trivial theoretical analysis (Theorem 1, Theorem 2, Assumption 1). The empirical evaluation is strong: 14–18% improvement over strong heuristics (HEFT, Tetris) and 7–14% over a heterogeneous-aware neural baseline (PPO-BiHyb), with single-pass inference times matching heuristics. The main weakness — the asymmetric One-Shot comparison — is real but does not threaten the core claims, since the PPO-BiHyb comparison alone establishes substantial gains. The skip-action validation, though narrower than the theory, clearly demonstrates the mechanism's practical value. The paper is a solid contribution to the scheduling literature, with architecture, theory, and experiments that advance the state of the art in heterogeneous DAG scheduling.

**Score: 7.0** — solid accept. Clear contributions, thorough theoretical grounding, strong empirical results, and addressable weaknesses.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>