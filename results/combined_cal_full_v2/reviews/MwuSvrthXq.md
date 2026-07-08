## Summary

This paper proposes WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. The key contributions are: (1) a weighted cross-attention (WeCA) mechanism that places compatibility coefficients outside the softmax to preserve distinguishability of tasks with different compatibility profiles; (2) a theoretical analysis of the optimality gap in list scheduling, showing it is not surjective onto the optimal solution, and a method to enable skip actions in the single-pass setting that closes this gap; (3) strong empirical results on TPC-H query DAGs and ML compiler computation graphs, outperforming state-of-the-art methods including One-Shot and PPO-BiHyb while maintaining competitive runtime.

## Strengths

- **Novel and well-motivated architectural contribution.** The weighted cross-attention (WeCA) mechanism (Section 3.1) places compatibility coefficients outside the softmax normalization, motivated by a concrete failure mode: identical tasks with different compatibility profiles receive indistinguishable embeddings under the inside-softmax variant. The ablation study (Table 3) confirms this empirically — the outside variant achieves 14.0% improvement over Tetris on TPC-H-30 vs. 10.5% for the inside variant. Weight: 11.10.

- **Genuinely novel theoretical analysis of the optimality gap.** Section 4 formalizes the reduced space B_f, proves that list scheduling's generation map S_list is not surjective onto the optimal solution, and constructs a map with skip actions that *is* surjective (Theorem 1(ii)–(iii)). The parametric skip score design that avoids both endless idling and repeated network inference is a clever engineering solution to a real tension. Weight: 9.32.

- **Strong and consistent empirical results.** On TPC-H-30, WeCAN-Greedy (19578) outperforms One-Shot-S(256) (20399) while being 15× faster. On Computation Graphs, WeCAN-Greedy matches or beats all heuristic baselines and is orders of magnitude faster than PPO-BiHyb. Improvement is consistent across all six dataset×graph-type combinations. Weight: 10.31.

- **Generalization experiments directly validate the core claim.** Training on a fixed environment and testing under varying pool counts, pool types, task counts, and task types (Figure 2) is the right protocol. The margin over One-Shot widens under environment shifts (e.g., 20.4% vs. 9.2% under "more pool"), strengthening the case that WeCA captures heterogeneous environment structure. Weight: 10.49.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The "PRO-BALM" baseline in the heavy-tasks ablation (Figure 3) is never defined.** The paper's baselines section (Section 5.1) lists SFT, MOPNR, CP, HEFT, Tetris, PPO-BiHyb, and One-Shot. "PRO-BALM" appears only in the heavy-tasks ablation table with numerical results (4.7% and 4.5% improvement over HEFT) but receives no definition or citation anywhere in the paper. This renders those specific comparisons uninterpretable. The core comparisons (WeCAN vs. non-skip variants) still stand, so this is a reporting gap rather than a fatal flaw. Weight: 0.96.

- **The main experimental tables (Tables 1 and 2) do not specify the number of test instances or random seeds.** Table 1 caption says "standard deviation among random seed" but no N is given. The ablation study explicitly states "10 test problems" (Section 5.3). Without N for the main results, readers cannot assess statistical reliability, particularly for small margins such as WeCAN-S(256) 32814 vs. WeCAN-S(64) 32912 on TPC-H-50 (a ~0.3% difference with overlapping standard deviations). Weight: 3.28.

- **The claim about clustering of poor solutions via the skip score form is asserted without evidence.** Section 4.2 states that the parametric skip score "clusters most poor solutions in the high-u_a, high-u_c region" and that "this concentration makes such regions easier to handle during training and reduces variance." No analysis or experiment supports this claim — no scatter plots, ablations, or variance statistics are provided. The skip action clearly works empirically (heavy-tasks ablation shows clear benefit), but this specific narrative is unsupported. Weight: 0.93.

### Trivial
None.

## Nice-to-Haves

- **Non-autoregressive decoder discussion.** The paper uses a non-autoregressive decoder (action scores depend only on initial state s_1), which trades flexibility for speed. The paper mentions this briefly and references Appendix B for comparison with autoregressive variants, but a short discussion in the main text about when this design choice could hurt performance would improve transparency.

## Removed Points

These points from the input review are removed with justification:
- **LDDNN vs LDDGNN naming in figure caption** — parser artifact from garbled figure extraction; not a paper flaw.
- **Duplicated column header "WeCAN-S(256)" in heavy-tasks table** — parser artifact from table extraction; original submission likely differentiates the two variants.
- **Non-autoregressive decoder limitation as a weakness** — the paper explicitly states this design choice for scalability and references the appendix; the reviewer's request for more main-text discussion is a nice-to-have, not a weakness.
- **Missing test instances/seeds as a "methodological gap" (original severity)** — downgraded to Minor; the results are consistent across datasets so the core findings are unlikely to be invalidated, but the reporting is incomplete.
- **"Could the metric be measuring a proxy" type speculation** — removed as generic hypothetical; no concrete anchor in the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Define or remove the PRO-BALM baseline from the heavy-tasks ablation.
2. State the number of test instances and random seeds in Tables 1 and 2, and include statistical significance tests for the main comparisons.
3. Provide empirical evidence for the clustering claim (e.g., a scatter plot of (u_a, u_c) values color-coded by makespan), or soften the language to reflect that it is a plausible intuition rather than a demonstrated property.
4. Briefly note in the main text when the non-autoregressive decoder's fixed (pre-computed) action scores could limit performance.

## Score and Decision

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| Uj0h13lVrR.md | 1.00 | R1 | No | GFlowNets — very different topic, low quality |
| bEgDEyy2Yk.md | 1.00 | R1 | No | Minimax path problem — unrelated |
| nSDOkm0SKo.md | 1.00 | R1 | No | Financial news — unrelated |
| bntJK4NyIW.md | 2.00 | R1 | No | Decentralized training — different problem |
| ArJikvI6xo.md | 3.40 | R1 | No | Federated learning — different problem |
| 10eQ4Cfh8p.md | 3.00 | R1 | No | FJSP optimization — similar scheduling but weaker eval |
| b9aCXHhdbv.md | 4.50 | R1 | Yes | Pipeline parallelism DRL — weaker strengths, heavier weaknesses |
| 8WtBrv2k2b.md | 5.00 | R1 | Yes | Quantum resource scheduling — divided opinions, unclear MDP |
| 76NYyOrnfk.md | 5.67 | R2 | No | FlashAttention — unrelated |
| DKfcxPxunu.md | 5.75 | R2 | No | Multi-task VRP — routing, different scheduling domain |
| Cs6MrbFuMq.md | 6.00 | R1/R2 | No | LLM inference scheduling — systems paper, different contribution type |
| iEHYbGbZ4D.md | 6.33 | R2 | No | Spiking GNN — unrelated |
| yEox25xAED.md | 6.60 | R2 | No | Grammar RL — unrelated |
| jBYQAtzp5Z.md | 6.80 | R1/R2 | Yes | Scheduling with predictions — theoretical, heavier weaknesses |
| skGSOcrIj7.md | 6.80 | R2 | No | DAG representation learning — not scheduling |
| hB2hXtxIPH.md | 7.00 | R1 | Yes | MARL heterogeneous tasks — novelty concerns, heavier weaknesses |
| jsWCmrsHHs.md | 7.50 | R2 | Yes | DRL for JSSP — strengths avg 9.8, weaknesses avg 3.1 |
| 7BLXhmWvwF.md | 8.00 | R1 | No | Robotics RL — unrelated domain |
| 9pW2J49flQ.md | 8.00 | R1 | No | LTL RL — unrelated |
| JDud6zbpFv.md | 8.00 | R1 | No | Quality-Diversity — unrelated |

**Round 1 bracket:** 6.5–8.0 (determined by comparing my draft's weight profile against the 4.50–7.00 anchors).

**Round 2 narrowing:** The most topically similar anchor (jsWCmrsHHs, DRL for JSSP, 7.50) has strength weights averaging ~9.8 and weakness weights averaging ~3.1. My paper has slightly higher strength weights (avg ~10.3) and substantially lower weakness weights (avg ~1.7). The 7.50 anchor's weaknesses include structural concerns (reliance on handcrafted neighborhood, presentation clarity issues), while my weaknesses are reporting gaps (undefined baseline, missing test counts, unsupported clustering claim) — all easily addressable. However, the PRO-BALM gap and missing test counts are genuine flaws that prevent a higher score. **Final score placed at 7.0**, reflecting a strong paper with clear contributions and minor but real reporting gaps.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>