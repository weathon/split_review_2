Now I have all the information I need. Let me compile the final consolidated review.

**Final bracket:** The paper sits between γ-MoD (6.67, accept) and SparseVLM (5.20, reject) / eRAM-V (5.00, reject). Compared to γ-MoD: this paper tackles a harder problem (dual-task unified transformers vs. single-task MLLMs) with stronger diagnostic analysis, but its experimental validation is weaker (no variance, Emu3 on a re-implementation). The comparison is favorable to this paper on novelty and analysis but unfavorable on experimental rigor. γ-MoD's strongest weakness was significance questions (-6.80 weight), while this paper's strongest weakness is -3.91 (Emu3 re-implementation). This paper sits in the 5.5–6.5 range.

---

## Summary

This paper studies efficient training for unified multimodal transformers (handling both generation and understanding). Through empirical analysis across four models, it finds that token redundancy is task-dependent and layer-dependent. Based on these findings, it proposes UniMoD, which uses task-specific routers with per-task pruning ratios to prune tokens selectively. Applied to Show-o (1.4B) and Emu3 (8.5B), UniMoD reduces training FLOPs by ~15% and ~40% respectively while maintaining broadly comparable performance.

## Strengths

- **Analysis-first approach is genuinely informative (Sections 3.2–3.4).** The paper's strongest contribution is its diagnostic work: attention weight analysis across Show-o, JanusFlow, Emu3, and Lumina-mgpt (Figure 2), ARank-based redundancy analysis across layers (Figure 3), and competitive token-pruning experiments (Figure 4). These provide concrete evidence that token redundancy is both task-dependent and layer-dependent, and this analysis would serve as a useful reference for future work regardless of the proposed method.

- **The core idea is clean and well-motivated.** The observation that a single router either prunes too aggressively (harming one task) or too conservatively (wasting FLOPs) is intuitive and empirically supported. The method architecture — task-specific routers with per-task pruning ratios derived from ARank — directly addresses the diagnosed problem. The design is simple enough to be practical while solving the right problem.

- **Coverage of two fundamentally different unified architectures.** Applying UniMoD to Show-o (diffusion for generation, autoregressive for understanding) and Emu3 (fully autoregressive) demonstrates generality beyond a single modeling paradigm. This is a meaningful distinction the authors correctly emphasize.

- **The ablation study (Table 5) confirms the full system outperforms simpler variants.** The catastrophic GenEval drop from 0.61 (UniMoD) to 0.15 (Basic MoD) convincingly shows that naive MoD application damages generation quality, justifying the need for task-aware design.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **No variance estimates reported for any benchmark.** Every result in Tables 3, 4, and 5 is a point estimate with no standard deviation, confidence interval, or number of runs. Given that many deltas are within 1–2 points (GQA 56.3→54.5, VQAv2 68.3→66.2, MMMU 25.8→25.7), it is impossible to distinguish signal from noise. This is a particular concern because the paper's central claim is that UniMoD "maintains or improves performance" — without variance, this claim is not empirically supported for small-magnitude differences.

- **The framing "maintaining or improving performance" is selectively optimistic.** For Show-o (Table 3), 3 of 8 metrics drop: GQA (−1.8), VQAv2 (−2.1), and GenEval (−0.01). While 5 metrics improve or stay essentially flat, the drops on GQA and VQAv2 are notable. The paper should acknowledge these trade-offs explicitly rather than treating all metrics as uniformly maintained. A more precise framing would strengthen the paper.

- **Emu3 results are from an unverified re-implementation.** The paper transparently states (line 242) that Emu3 uses "alternative training datasets, as the official code and data are not publicly available." The 40% FLOPs reduction is a valid computational measurement, and the within-paper comparison (re-implementation baseline vs. UniMoD on the same re-implementation) is internally consistent. However, the baseline quality is unverified, which weakens the external significance of the Emu3 results. The headline "40% FLOPs reduction" would be substantially stronger if validated against the original published Emu3.

- **Ablation does not fully isolate the contribution of each design choice.** The ablation tests "w/o task-aware router" (single router, ARank-selected layers) and "w/o layer switch module" (separate routers, interleaved layers), but neither tests "separate routers at ARank-selected layers with equal capacities" to isolate whether the benefit comes from task-specific routing or from the per-task capacity tuning. Additionally, Basic MoD (40.8 TFLOPs) uses fewer FLOPs than UniMoD (43.3 TFLOPs), making the comparison asymmetric — a same-FLOPs comparison would be cleaner.

- **Layer Switch Module is underspecified.** The paper states "select the half of layers with the lowest [ARank] values for each task" but does not explain how conflicts are resolved when a layer has low ARank for one task but high ARank for the other. The decision rule for assigning a layer as T2I MoD, MMU MoD, or Shared MoD is not stated, which hurts reproducibility.

### Trivial
None.

## Nice-to-Haves

- Report inference-time FLOPs/latency in addition to training FLOPs, since inference is also computationally expensive for these models.
- Add a clearer scope statement: the method is evaluated during fine-tuning, not pre-training. Extending to pre-training would be a natural next step.
- Specify the layer conflict resolution rule in the Layer Switch Module description.

## Removed Points

These points are flagged to be removed; treat them with caution:

- *"Emu3 comparison is invalid"* (Harsh Critic Critical Issue 1) → Downgraded to Minor. The comparison is internally consistent (both baseline and UniMoD use the same re-implementation on the same data); the 40% FLOPs savings is a computational measurement unaffected by baseline quality. The paper transparently discloses the data mismatch.

- *"MoMa should be compared against"* → MoMa applies to Chameleon, a different model architecture; the paper correctly notes it lacks generation and most understanding benchmarks, making direct comparison infeasible.

- *"8B model results / Pareto frontier deferred to appendix"* → The parser strips appendix sections from all papers; these exist in the original submission.

- *"Table 1 GQA=0.0 not adequately explained"* → The paper discusses this finding (Observation 2: early layers are more critical). It is presented as an empirical finding, not an unexplained anomaly.

- *"Figure 4 confounds task importance with router preferences"* → Speculative interpretation. The experiment's framing is clearly stated.

- *"Memory savings are modest"* / *"Training cost metric vague"* → Factual observations about specific numbers, not methodological weaknesses.

- *"Table 3 formatting"* → Pure style nitpick.

- *"Method applied only during fine-tuning"* → The model weights assigned this a positive weight (+2.06), indicating it is not a genuine weakness. Efficiency methods applied during fine-tuning are standard practice.

## Novel Insights

The reviews converge on two real insights the paper should address: (1) the lack of variance reporting makes the "maintaining performance" claim unverifiable for small-magnitude differences, and (2) the Emu3 re-implementation, while transparently disclosed, weakens the headline efficiency result. Neither insight fundamentally undermines the paper's core contribution — the diagnostic analysis and task-aware pruning idea are solid — but both identify concrete ways the experimental presentation could be more rigorous.

## Suggestions

1. Report all benchmark results with standard deviations across multiple runs (at least 3 seeds). Without variance, the central claim of "maintaining performance" cannot be evaluated for small deltas.
2. Frame the Show-o results more precisely: e.g., "achieves comparable or better performance on 5 of 8 metrics while saving 15% FLOPs, with minor degradation on GQA (−1.8) and VQAv2 (−2.1)."
3. Add a scope statement clarifying that results are demonstrated during fine-tuning; pre-training extension is future work.
4. Specify the conflict resolution rule in the Layer Switch Module for reproducibility.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>