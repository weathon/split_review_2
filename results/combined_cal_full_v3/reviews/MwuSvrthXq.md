Now I have all the information needed. Let me produce the final consolidated review.

---

## Summary

This paper proposes WeCAN, an end-to-end reinforcement learning framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. The key innovations are: (1) a Weighted Cross-Attention (WeCA) layer that places compatibility coefficients outside softmax normalization to produce distinguishable embeddings for tasks with different compatibility profiles; (2) a theoretical analysis of the optimality gap in list-scheduling-based methods, with a skip-action mechanism that provably closes this gap under single-pass inference; and (3) an LDDGNN (longest directed distance GNN) for capturing task dependencies. Empirical results on TPC-H and Computation Graphs datasets show consistent improvements over heuristics and homogeneous-designed neural baselines.

## Strengths

- **Well-motivated architectural innovation in the WeCA layer (Section 3.1).** Placing compatibility coefficients outside the softmax normalization is theoretically grounded and practically consequential. The paper provides a clear scenario where two tasks with identical attributes but different compatibility profiles would be indistinguishable under "inside" placement but distinct under "outside" placement. The ablation (Table 3) confirms this: WeCA-inside+LDDGNN underperforms WeCA+LDDGNN by ~4% relative makespan on TPC-H-30 (20729 vs. 19908).

- **Theoretical analysis of the list-scheduling optimality gap with a constructive fix (Sections 4.1–4.2, Theorem 1).** The paper formalizes the reduced space B, proves that TS_list is neither injective nor surjective, and constructs a skip-action mechanism that provably closes this gap. The analysis identifies which cases (heavy tasks with extreme resource demands and running times) are most affected, and the skip-score function is thoughtfully designed to concentrate poor solutions in high-u_a, high-u_c regions to reduce training variance.

- **Clean empirical gains on two diverse datasets (Tables 1 and 2).** WeCAN-S(256) improves over the best heuristic by 14.0–18.1% on TPC-H and 13.4% on Computation Graphs, and over the best neural baseline (One-Shot-S(256)) by 7.0–7.7% and 9.5% respectively. Standard deviations where reported are small relative to the improvements (e.g., ±10 vs. mean 18964 on TPC-H-30).

- **Thorough ablation study (Table 3).** The ablation systematically tests six architectural variants (WeCA-inside, WeCA-decoder-only, WeCA-decoder-inside, WeCA-final-only, GAT-forward, GAT-bidirectional), confirming that both the WeCA design and LDDGNN contribute meaningfully.

- **Generalization experiments (Figure 2).** WeCAN maintains robust performance under varying environment fluctuations (pool number, pool type, task number, task type), significantly outperforming One-Shot in several settings (e.g., 6.7% improvement vs. 0.9% for One-Shot under more pool types).

## Weaknesses

### Fatal
None.

### Major

- **Missing comparisons against heterogeneous scheduling baselines.** The paper's core framing is about *heterogeneous* DAG scheduling with compatibility coefficients. Yet both neural baselines (PPO-BiHyb, One-Shot) were designed for *homogeneous* settings — the paper itself acknowledges this (lines 29–30, 44–45). Meanwhile, the related work section (lines 36–48) cites at least six methods explicitly designed for heterogeneous scheduling (Wu et al. 2018, Ni et al. 2020, Grinsztajn et al. 2021/READYS, Zhou et al. 2022, Zhadan et al. 2023, Wang et al. 2025), but none appear in the experiments. This undermines the headline claim of "outperforming state-of-the-art methods across diverse datasets" (abstract). Without comparisons against methods that also target heterogeneous environments, it is unclear whether WeCAN's improvements stem from its architectural innovations or from the fact that any RL-based method would outperform homogeneous-designed baselines on heterogeneous problems. (Note: HEFT is a heterogeneous *heuristic*, so the gap is specifically in neural heterogeneous baselines.)

### Minor

- **Missing standard deviations for greedy-mode results.** In Tables 1 and 2, WeCAN-Greedy shows makespan values without ± uncertainties, while WeCAN-S(64) and WeCAN-S(256) include them. Since the greedy mode best showcases the claimed single-pass speed advantage, standard deviations are needed to assess statistical reliability.

- **No comparison with One-Shot-Greedy.** The paper references "One-Shot-greedy" at line 260 but provides no corresponding table entries. Since One-Shot is the closest neural baseline (also single-pass, list-scheduling-based), comparing One-Shot-Greedy vs. WeCAN-Greedy would be the cleanest test of the single-pass architecture claim.

- **Randomly generated compatibility coefficients on TPC-H.** The compatibility coefficients are described as "random" (line 216). Since these coefficients are the central challenge the method is designed to address, the use of randomly generated (rather than real-world-measured) values should be acknowledged as a limitation.

- **Skip-action usage frequency not reported.** How often the trained model chooses to skip vs. schedule a task is not quantified. While the heavy-task experiment (Figure 3) validates the skip mechanism, its contribution in standard settings remains unclear.

### Trivial
None.

## Nice-to-Haves

- Testing with more than three pools in the main results (beyond the generalization experiment in Figure 2) would further demonstrate the architecture's adaptability claim.
- Reporting results at higher heavy-task proportions in the main text (beyond 1%) would strengthen the empirical validation of the skip-action analysis.

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **"Non-autoregressive decoder is unablated / insufficiently scrutinized"** — The paper states "comparison with auto-regressive one in Appendix B" (line 137), so this analysis exists in the original submission. Removed per hard rules about missing appendix content.
2. **"WeCAN-S(256) runtime is slower than One-Shot-S(256), undermining efficiency claims"** — The paper accurately describes the runtime as "comparable" (2.43s vs. 2.26s on TPC-H-30). The single-pass speed advantage is clearly articulated for the greedy mode. The claim is not undermined.
3. **"Only three pools in main experiments"** — The paper tests generalization across varying pool counts in Figure 2, partially addressing this concern.
4. **"1% heavy tasks is a modest perturbation"** — The paper states further rates are in Appendix C.
5. **"Skip-score formula rationale unexplained"** — The paper provides the design rationale (concentrating poor solutions in high-u_a, high-u_c regions to reduce variance).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add comparisons against at least 2–3 heterogeneous scheduling baselines** (e.g., READYS (Grinsztajn et al. 2021), Zhou et al. 2022) to directly validate the paper's claims in its stated setting. This is the highest-leverage improvement.
2. **Report standard deviations for greedy-mode results** and include a One-Shot-Greedy column for a cleaner single-pass comparison.
3. **Report skip-action usage frequency** during trained inference to quantify the mechanism's empirical contribution.
4. **Acknowledge the synthetic nature of the compatibility coefficients** as a limitation.

## Score and Decision

**Score justification (calibration):** I retrieved 27 calibration anchors across two rounds. The most directly comparable are the FJSP-RL paper (avg 3.00, rejected for missing baselines and poor presentation), the NAR-GNN paper (avg 5.33, rejected for baseline-weakening issues, weakness favorability -2.71), the VRP cross-attention paper (avg 6.25, accepted despite a -2.63 missing-baseline weakness because core contributions were validated at 100K-node scale), and the quantum scheduling paper (avg 5.00, rejected with a -2.51 missing-comparison weakness and strongly divergent reviews). Our paper's strengths are high (favorability 9.01–10.64) and the theoretical contributions (WeCA placement, optimality gap analysis, skip-action mechanism) are genuine. However, the major weakness (missing heterogeneous baselines, favorability -2.10) is central to the paper's framing — the paper claims superiority in heterogeneous scheduling but does not compare against methods designed for that setting. The evaluation scope (up to 918 tasks, 3 pools) is also more limited than the VRP paper that was accepted despite similar baseline gaps. On balance, the paper sits between the NAR-GNN (5.33, rejected) and quantum scheduling (5.00, rejected) anchors, making 5.0 the appropriate score.

**Round-1 bracket:** 4.0–6.0. **Round-2 narrowing:** After comparing itemized favorability against anchors, the paper's missing-baseline weakness is too central to the heterogeneous scheduling claim to score above 5.5.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>