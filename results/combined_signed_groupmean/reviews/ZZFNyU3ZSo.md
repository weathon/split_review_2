I have enough information to finalize. Let me write the complete review.

## Summary

This paper introduces UniMoD, a task-aware token pruning method for unified multimodal transformers. Through empirical analysis of attention weights, layer importance (ARank), and task interactions in models like Show-o and Emu3, the authors find that token redundancy varies significantly across tasks and layers. Building on these insights, they propose using separate per-task routers with task-specific capacities instead of a single shared router. UniMoD reduces training FLOPs by ~15% on Show-o (1.4B) and ~40% on Emu3 (8.5B) while maintaining or improving performance on several understanding and generation benchmarks.

## Strengths

- **The empirical analysis in Sections 3.2–3.4 is genuinely informative.** Figure 2 (attention weight patterns across tasks/modalities), Figure 3 (ARank across layers for four unified transformers), and the competitive token-pruning experiment (Figure 4) provide concrete evidence that token redundancy is task-dependent and layer-dependent in unified transformers. This analysis is the strongest part of the paper and is independently useful regardless of the method.

- **The core design insight is clear and well-motivated.** The idea that a single shared router cannot serve both generation and understanding tasks optimally, and that separate per-task routers are needed, follows naturally from the empirical analysis. The method (transforming dense layers into T2I MoD, MMU MoD, and Shared MoD blocks) is simple to implement on top of existing models. The paper provides a clear pipeline in Figure 5.

- **The FLOPs reductions are non-trivial.** 15% for Show-o (1.4B parameters) and 40% for Emu3 (8.5B parameters) while maintaining or improving performance on several benchmarks is a practically meaningful result. The method also shows improved efficiency at larger scales (20% FLOPs reduction on 8B models, noted in Section 5.2).

## Weaknesses

### Major

- **Incomplete controlled comparison for the core claim.** The paper's central thesis is that separate task-aware routers outperform a single shared router. However, in Table 5, the key variant "w/o task-aware router" (single router, selected layers) runs at **40.8 TFLOPs** while UniMoD runs at **43.3 TFLOPs** — a FLOPs mismatch. This makes it impossible to fully attribute the GenEval gap (0.50 vs. 0.61) to the router design rather than the ~6% compute difference. The ablation "w/o layer switch module" at 43.3 TFLOPs (equal to UniMoD) does provide a controlled comparison showing the layer switch module matters, but the core claim about separate routers is not isolated at equal FLOPs. The paper states "maintains the same pruning rate" (Section 5.3), but FLOPs differ because architectural choices affect compute, and the confound should be explicitly analyzed.

- **Emu3 results are based on an uncalibrated reimplementation.** The paper states: *"Our full Emu3 results differ from the original paper because we use alternative training datasets, as the official code and data are not publicly available."* The paper does not report whether this reimplementation reproduces the original Emu3's published benchmark numbers. The Emu3 baseline in Table 3 achieves MME=881.3 and GQA=46.0 — are these numbers consistent with the original published Emu3? Without this calibration, the reader cannot tell whether UniMoD's claimed 40% FLOPs reduction on Emu3 is a genuine advance or an artifact of the reimplementation being suboptimally trained (making it easier to match with pruning). The comparison is internally valid (UniMoD vs. the paper's own Emu3 baseline), but its external significance is unclear.

### Minor

- **No statistical significance or variance reporting.** Every result in Tables 1–5 is a single point estimate. Given that several differences are small (GenEval 0.62 vs. 0.61, DSG 72.2 vs. 73.6) and that the pruned model sometimes scores *higher* than the full model (MME 1056.0 vs. 1093.7), there is no way to assess whether these reflect real improvements or noise. Variance across runs is essential for a paper that claims pruning can improve performance.

- **Internal baseline inconsistency.** Table 2 reports "Show-o*" (joint training) with MME=1032.0, GQA=52.5, POPE=77.9, GenEval=0.63, while Table 3 reports the full Show-o baseline with MME=1056.0, GQA=56.3, POPE=79.8, GenEval=0.62. Both are described as the full model with both tasks, yet the numbers differ substantially (e.g., GQA differs by 3.8 points). The paper does not explain this discrepancy, which erodes confidence in the measurement consistency.

- **Gap between method description and implementation.** Section 4.1 describes an ARank-based procedure to select the half of layers with lowest ARank values and estimate pruning ratios from normalized ARank scores. Yet Section 5.1 says for Show-o *"we transform the last 12 layers into MoD layers"* and for Emu3 *"80% token pruning in the last 16 layers."* The paper does not verify that the last 12/16 layers correspond to those with lowest ARank, nor does it report which layers ARank actually selected. The connection between the principled ARank analysis and the final implementation choices is not explicit, making it harder to assess whether the ARank analysis drives the design or merely justifies it post-hoc.

- **Underspecified capacity scheduling.** Section 5.1 states: *"For the Multi-Modal Understanding (MMU) task, we scale the capacity from 1 down to 0.2."* It is unclear whether this is a linear schedule over layers, over training steps, or something else. For T2I: *"we prune 20% of the tokens in the later layers"* — which specific layers is not defined. These details are needed for reproducibility.

### Trivial

None.

## Nice-to-Haves

- A Pareto frontier analysis showing the FLOPs-performance tradeoff for single-router MoD vs. UniMoD at multiple operating points would significantly strengthen the paper's main claim.
- Calibrating the Emu3 reimplementation against the original published results (or clearly quantifying the gap) would make the strongest quantitative claim more credible.
- Reporting results with at least 3 random seeds and including standard deviations would address the variance concern.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Task interaction analysis undermines motivation"** (from Harsh Critic). REMOVED. The paper's motivation for separate routers comes from different token redundancy patterns across tasks (Observations 3–4 in Section 3.3) and the competitive pruning experiment (Figure 4, Observation 5), not from task interference. Table 2 shows tasks do not negatively interfere, which actually supports the feasibility of joint training with separate routers. This criticism misunderstands the paper's logical chain.

- **"MoMa comparison framing"** (from Harsh Critic). REMOVED. The paper accurately describes MoMa's scope and correctly identifies that MoMa's MoD application is a "simplistic combination" without task-specific design for unified transformers.

- **"Only GQA is tested for layer importance"** (from Harsh Critic). REMOVED. The paper explicitly scopes this experiment (Table 1) as a simple probe during inference; it does not claim comprehensive analysis.

- **"Training cost mixed units"** (from Harsh Critic). REMOVED. This is a minor presentation nitpick that does not affect the paper's core claims.

- **"Missing baselines in appendix"** (from Harsh Critic). REMOVED. The appendix was stripped by the parser; the reviewer acknowledged this limitation.

- **"Baselines are too weak"** (overall framing from Harsh Critic). PARTIALLY REMOVED for severity overstatement. The paper includes Interleaved Layer Skipping and Early Exit as straightforward naive baselines. The real comparison is in the ablation study (Table 5). The retained weakness is the controlled-comparison issue (now listed under Major).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run a controlled comparison between single-router MoD and UniMoD at the **same FLOPs budget** (e.g., match compute by adjusting pruning ratios), or provide an explicit analysis of how the FLOPs difference affects the performance gap.
2. Calibrate the Emu3 reimplementation by comparing it against published Emu3 numbers on shared benchmarks, or clearly state the gap and why it does not affect conclusions.
3. Report main results with at least 3 seeds and include standard deviations.
4. Reconcile the ARank-based layer selection with the implemented "last 12/16 layers" by reporting the ARank values for each layer and showing they coincide.
5. Explain why the Show-o baseline differs between Table 2 (Show-o*) and Table 3 (full Show-o).
6. Clarify the capacity scheduling for Show-o (e.g., linear schedule over layers or over steps) and which specific layers are pruned for the T2I task.

---

**Calibration Anchor Summary**

| Anchor Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| `/home/.../q44uq3tc2D.md` (γ-MoD) | 6.67 | R1 | Yes | Most directly relevant anchor. Uses same ARank+MoD paradigm but for understanding-only MLLMs. Similar weakness magnitudes but more complete evaluation (3 model families). Paper under review tackles harder problem (unified gen+und) with weaker eval. |
| `/home/.../5ncdKonxd4.md` (PyramidDrop) | 3.00 | R1 | Yes | Progressive token pruning for LVLMs. Lower score due to limited novelty and insufficient baselines. Paper under review has clearer novelty. |
| `/home/.../jIAKjjEmWi.md` (A-MoD) | 4.00 | R1 | Yes | Attention-based MoD routing. Stronger on novelty but weaker on results relevance to this paper's setting. |
| `/home/.../1xG3MN1RRW.md` (SparseVLM) | 5.20 | R2 | Yes | Training-free token pruning for VLMs. Had more numerous and severe weaknesses (performance drops, missing comparisons). Paper under review has cleaner methodology but similar evaluation gaps. |
| `/home/.../UQJ7CDW8nb.md` (LLaVA-Mini) | 6.50 | R2 | Yes | Extreme token compression (1 vision token). Strong empirical validation across 18 benchmarks. Lower direct relevance but serves as upper-anchor for efficiency papers. |

**Round 1 bracket**: 4.0–6.5 (based on comparison with PyramidDrop at 3.00 as lower bound and γ-MoD at 6.67 as upper bound).

**Narrowing**: The paper sits below γ-MoD (6.67) because its evaluation has two notable gaps (controlled comparison, Emu3 calibration) that γ-MoD's evaluation did not have. It sits above SparseVLM (5.20) because its strengths are higher-impact (all >+9.7 vs. SparseVLM's mixed impacts) and its weaknesses are more focused and addressable. The strongest impact items in the paper's draft (+9.96 empirical analysis, +9.79 design insight, +9.99 FLOPs savings) are comparable to the strongest items in γ-MoD (+9.95 experiments, +9.78 novelty of MoD for MLLMs). The negative items (−9.98, −9.96) are comparable in magnitude to γ-MoD's most impactful negatives (−10.00 methodological ambiguity, −8.77 significance concern). The paper under review has fewer total weaknesses but they are more concentrated on the evaluation, whereas γ-MoD had broader methodological concerns.

**Final placement**: 5.5 — between γ-MoD (6.67) and SparseVLM (5.20), reflecting a paper with genuine contributions and strong empirical motivation but evaluation gaps that prevent a stronger acceptance.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>