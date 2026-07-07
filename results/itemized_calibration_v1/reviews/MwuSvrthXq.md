Now let me write the final consolidated review.

## Summary
This paper proposes WeCAN, an end-to-end RL framework for heterogeneous DAG scheduling with task-pool compatibility coefficients. The key innovations are: (1) a weighted cross-attention (WeCA) layer that places compatibility coefficients as a multiplicative bias outside softmax, preserving fine-grained compatibility information across pools; (2) a longest directed distance GNN for capturing dependency structure; (3) a theoretical analysis of the optimality gap in list scheduling with a skip-action mechanism that closes this gap in the single-pass setting. Experiments on TPC-H and Computation Graphs datasets show WeCAN achieves 7.7–9.5% improvement over neural baselines while running in sub-second to few-second times.

## Strengths
- **Well-motivated weighted cross-attention (WeCA) design.** The WeCA layer (Sec 3.1) places compatibility coefficients outside softmax normalization, which solves a genuine limitation: inside-softmax placement loses information about a task's overall compatibility profile. The concrete counterexample (two tasks with identical attributes but different compatibility profiles) convincingly motivates this design choice.
- **Non-trivial theoretical analysis of the optimality gap (Section 4).** The framing of scheduling in terms of spaces A and B with generation maps, plus Theorem 2 characterizing when list scheduling fails to achieve optimality, provides a clean foundation for the skip-action mechanism. The construction via skip actions to achieve surjectivity is a genuine theoretical contribution beyond the engineering of the architecture.
- **Strong empirical results with careful ablation.** WeCAN achieves up to 18.1% improvement over heuristics and 7.7–9.5% over neural baselines. Standard deviations are small relative to improvements (e.g., ±10–118 on makespans in the thousands). The ablation study (Table 3) systematically tests WeCA placement variants, inside-vs-outside softmax, and GNN variants, all controlled for layer count and hidden dimensions, convincingly showing all components contribute.
- **Practical computational efficiency.** WeCAN-Greedy runs in 0.15–1.72 seconds on TPC-H problems (Table 1), comparable to heuristic runtimes and dramatically faster than PPO-BiHyb (20–179 seconds), making it viable for time-sensitive scheduling applications.

## Weaknesses

### Fatal
None.

### Major
- **PRO-BALM appears in a key experimental result (Figure 3) but is never defined, cited, or introduced in the paper.** The heavy-task ablation (Figure 3) is central to validating the skip-action mechanism. PRO-BALM is the second-best method in this experiment (4.7% and 4.5% improvement over HEFT), yet the baselines section (Sec 5.1) only lists PPO-BiHyb and One-Shot as RL baselines. PRO-BALM is never introduced in the text — it appears only in the figure's alt-text and data table (lines 299, 301–302). This undermines the interpretability and credibility of the heavy-task experiment, which is the primary evidence for the skip-action benefit.

### Minor
- **Figure 3 has ambiguous labeling.** Two bars are both labeled "WeCAN-S(256)" — one showing 8.3%/8.9% improvement (presumably the full skip-action variant) and one showing -2.3%/0.0% (presumably the non-skipping variant). The text distinguishes a "non-skipping variant" (line 310), but the figure itself is confusing at a glance. The green bar should have a distinct label such as "WeCAN-S(256) w/o skip."
- **Several heterogeneous-specific methods discussed in related work are not compared against experimentally.** The paper (lines 36–48) discusses Zhou et al. (2022), Zhadan et al. (2023), Wang et al. (2025), and Grinsztajn et al. (2021) as approaches specifically designed for heterogeneous environments — the exact setting the paper targets. Yet none appear in the baselines (Sec 5.1), which only include two RL methods: PPO-BiHyb (2021, a general bi-level scheduler) and One-Shot (2023, described as not handling compatibility coefficients well). While the results against included baselines are strong, the omission of these directly relevant heterogeneous methods tempers the "outperforming state-of-the-art" claim.
- **The environment generalization experiment (Figure 2) lacks concrete ranges in the main text.** The paper reports improvements of 20.4%, 6.7%, 14.3%, and 19.3% under "more pool," "more pool type," "more task," and "more task type" fluctuations, but does not specify the training environment parameters or the range of variation for each fluctuation type (e.g., from how many pools to how many). The paper references Appendix F, but the main text should at minimum characterize the difficulty of the generalization task.
- **The skip action scoring function is presented without comparison against alternatives.** The formula $u_{\pi_{skip}} = u_a(1 - \frac{k}{2n})^{u_b} + u_c$ uses a specific decay term described as preventing the skip action from being "overly prioritized," but no analysis or ablation compares this formulation against simpler alternatives (e.g., a fixed learned penalty, linear decay). Given that the theoretical claims about closing the optimality gap depend on this mechanism performing well in practice, some empirical justification for the chosen functional form would strengthen the paper.

### Trivial
None.

## Nice-to-Haves
- An explicit comparison on standard (non-heavy-task) benchmarks of WeCAN with and without the skip action would quantify how much of the improvement is attributable to the skip mechanism vs. the WeCA architecture itself.

## Removed Points
- **Non-autoregressive decoder assumption not validated:** The critic claimed this is not validated, but the paper explicitly states "comparison with auto-regressive one in Appendix B" (line 137). Since the appendix is stripped by the parser, this criticism is removed per hard rules.
- **Large-scale results "only referenced":** The critic claimed large-scale results are only in Appendix F, but Table 1 already shows TPC-H-100 results (918 tasks on average), partially covering this claim.
- **Training details underspecified (optimizer, batch size, etc.):** The paper references Appendices D, E, H for experimental details. Per hard rules, criticisms about content likely addressed in the appendix (which is stripped by the parser) are removed.
- **Generic speculation about confounders/metrics:** The critic raised speculative concerns about whether the skip design's claims hold; these are not anchored to specific errors in the paper as written.
- **Pure reproducibility nitpicks:** The critic's request for disclosed hyperparameters, while helpful, falls under the hard-rule exclusion for reproducibility details impractical to include in a submission.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Define PRO-BALM** in the baselines section and properly distinguish the two WeCAN-S(256) bars in Figure 3 (e.g., relabel as "WeCAN-S(256) w/ skip" and "WeCAN-S(256) w/o skip").
2. **Add comparisons** against at least one or two of the heterogeneous-specific methods discussed in related work (Zhou et al. 2022, Zhadan et al. 2023, or Wang et al. 2025), or clearly scope the claim to the compared methods.
3. **Include concrete ranges** for the environment generalization experiment (training vs. test environment parameters) in the main text, not only in Appendix F.
4. **Add a brief ablation or discussion** justifying the skip score functional form against simpler alternatives.

## Score and Decision

**Calibration Anchors.** The following anchors were retrieved from the human-review corpus:

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| FJSP RL (generate+improve) | 10eQ4Cfh8p.md | 3.00 | R1 | Yes | Lower quality: missing ablations, no std devs, poor writing. Our paper has careful ablations, std devs, and is clearly written — substantially stronger. |
| Pipeline Parallelism DRL | b9aCXHhdbv.md | 4.50 | R1 | Yes | Missing formal analysis (weight -4) and incomplete experiments. Our paper has Section 4's theoretical analysis and more complete experiments — stronger. |
| Massively Parallel RL for CO | CJEBFNBLhO.md | 4.25 | R2 | No | Engineering-focused infrastructure paper; different contribution type. Our paper has stronger methodological novelty. |
| Multi-task Neural Solver | Dgc5RWZwTR.md | 4.75 | R2 | No | Training paradigm paper; less directly comparable. Our paper has stronger architectural novelty. |
| **Boosting NCO for Large-Scale VRPs** | **TbTJJNjumY.md** | **6.25** | R1,R2 | **Yes** | **Most comparable: lightweight cross-attention for CO, strong results, missing some baselines (weight -2). Our paper adds theoretical analysis but has a more concrete evaluation gap (PRO-BALM undefined). Slightly below this anchor.** |
| **Learning to solve CCBPP** | **6hvtSLkKeZ.md** | **6.40** | R1,R2 | **Yes** | **Comparable: first method for a new problem variant, comprehensive experiments, but insufficient baselines (weight -3). Our paper has stronger theory but weaker evaluation presentation. Comparable quality.** |
| Multi-Task Learning for Routing | DKfcxPxunu.md | 5.75 | R1,R2 | No | Cross-problem generalization for VRPs. Similar in having both architectural novelty and some evaluation gaps. Comparable. |
| ROS for Max-k-Cut | CpiJWKFdHN.md | 5.67 | R2 | No | GNN-based framework for CO with theoretical analysis. Slightly below our paper in empirical scope. |
| Neural Solver Selection | CFLEIeX7iK.md | 5.75 | R1 | No | Meta-level framework for solver selection; different contribution type. |

**Round 1 Bracket:** After comparing weighted items from the most relevant anchors, the narrowest plausible range is **5.5–6.5**. The paper's core contributions (WeCA, theoretical analysis) are stronger than the 4.0–5.0 anchors, but the PRO-BALM presentation error prevents it from reaching the 6.5–7.0 level of the strongest CO papers.

**Final Score: 6.0.** The paper presents a genuinely novel architecture (WeCA) and non-trivial theoretical analysis — contributions that are well-ablated and clearly communicated. The empirical results against included baselines are strong and consistent. However, the presence of an undefined method (PRO-BALM) in a key experimental figure is a concrete presentation error that must be fixed, and the omission of heterogeneous-specific baselines discussed in the paper's own related work tempers the strength of the performance claims. These issues are addressable (not fatal) but prevent a higher score.

**Decision: Borderline Accept.** The paper should be accepted contingent on addressing the PRO-BALM issue and ideally adding heterogeneous-specific comparisons.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>