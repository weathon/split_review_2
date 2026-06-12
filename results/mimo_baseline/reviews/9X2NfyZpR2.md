## Summary

This paper introduces TbLTA, presented as the first weakly-supervised framework for dense long-term action anticipation (LTA) trained exclusively from video transcripts—ordered action lists without temporal boundaries. The method combines a transformer encoder, a temporal alignment module for pseudo-label generation, cross-modal attention between video and transcript embeddings, and an anticipation decoder with CRF refinement, supervised through alignment, segmentation (CTC), and anticipation losses. Experiments on Breakfast, 50Salads, and EGTEA demonstrate competitive results with fully-supervised methods, particularly strong performance on the Breakfast dataset.

## Strengths

- **Genuine novelty in problem formulation.** The paper correctly identifies that all prior dense LTA methods rely on frame-level annotations, and weakly-supervised LTA is essentially unexplored. Using transcripts alone is a practical and meaningful relaxation of the supervision requirement. The only prior weak-supervision work for LTA (Zhang et al., 2021) still requires temporally localized annotations for the observed segment.

- **Well-designed multi-component architecture with complementary losses.** The combination of ATBA-based pseudo-labels, CTC loss for transcript consistency, cross-modal attention with local masking, CRF for sequence coherence, and an affinity-based duration loss is well-motivated. The ablation study (Tables 3-4) demonstrates that each component contributes meaningfully: removing CTC costs ~0.6-0.8 points, removing cross-attention costs ~1.3-5.7 points, removing CRF costs ~4.1-5.3 points at longer horizons, and removing duration loss costs ~0.2-3.3 points.

- **Strong empirical results on Breakfast.** At Obs 30%, TbLTA achieves 40.28/35.76/31.67/28.79 MoC across horizons, surpassing the best supervised method ActFusion (35.79/31.76/29.64/28.78). This is a remarkable result for a weakly-supervised method and validates the hypothesis that transcript-level procedural structure can substitute for dense frame annotations in structured activity domains.

- **Comprehensive evaluation across three benchmarks and multiple observation/horizon settings**, following established protocols. The inclusion of stochastic predictions provides additional insight into the model's ability to capture uncertainty.

## Weaknesses

### Fatal
None.

### Major

- **The gap on 50Salads is substantial and insufficiently explained.** TbLTA achieves 20.92 avg MoC vs 28.39 for ActFusion—a 7.5-point gap, and at the 50% horizon the gap widens to 7-10 points. The paper briefly attributes this to "denser action distributions and frequent transitions" but does not provide systematic analysis (e.g., pseudo-label quality metrics on each dataset, alignment accuracy, or error breakdowns). For a method that claims to offer "a very robust alternative" to full supervision, understanding when and why it underperforms is essential.

- **Pseudo-label quality is not measured or discussed.** The entire framework depends on ATBA-generated pseudo-labels serving as frame-level supervision for both TAS and LTA heads. Yet the paper reports no metrics on pseudo-label accuracy (e.g., frame-level accuracy of pseudo-labels vs. ground truth, boundary localization error). This makes it impossible to assess whether the approach's limitations stem from poor alignment, noisy pseudo-labels, or downstream model capacity. Given that pseudo-labels functionally create dense supervision, their quality is central to evaluating the "weak supervision" claim.

- **Stochastic Top1 comparison is misleading in context.** The Top1 stochastic results (28.51 on 50Salads, 37.15 on Breakfast) are presented alongside deterministic baselines, and while they are visually separated, the paper's abstract and conclusion cite the approach as "competitive with, and occasionally superior to, fully supervised approaches" without clarifying that the strongest numbers come from a fundamentally different evaluation protocol. Selecting the best of multiple stochastic samples is not comparable to deterministic single-pass evaluation. This claim needs to be qualified more explicitly.

### Minor

- **The comparison with WS-DA (Zhang et al., 2021) is incomplete.** Only a single number per dataset is shown (Obs 30%, 10% horizon), with no other observation/horizon settings. A more thorough comparison with the only prior weakly-supervised LTA method would strengthen the contribution claims.

- **No comparison with weakly-supervised TAS methods adapted for LTA.** Several recent weakly-supervised TAS methods (Xu & Zheng, 2024, which provides ATBA itself) could serve as natural baselines when extended to anticipation. The paper does not discuss why simply combining a weakly-supervised TAS model with an anticipation head would or would not work.

- **Tables 3 and 4 appear to contain identical data** despite being labeled as ablations on "TAS module" and "LTA module" respectively. If this is not a parser artifact, it raises questions about whether separate TAS and LTA ablation results were actually obtained.

- **The EGTEA results (Table 2) show a significant overall gap** (65.37 vs 76.80 mAP). While competitive on rare classes, this is acknowledged only briefly.

### Trivial
- The claim "first stochastic variant" of CRF for LTA (in related work) would benefit from a citation or more explicit positioning relative to diffusion-based stochastic methods.

## Nice-to-Haves

- Report pseudo-label quality metrics (frame-level accuracy, edit score) across datasets to diagnose where the supervision signal breaks down.
- Include a table or figure showing how pseudo-label quality evolves across the progressive training stages.
- Provide failure case analysis on 50Salads to understand when the transcript-only signal is insufficient.
- Discuss computational cost of annotation: quantify the actual cost savings of transcript collection vs. frame-level annotation in practice.

## Novel Insights

The paper's central insight—that transcripts encode sufficient procedural structure to supervise dense frame-level anticipation without boundary annotations—is genuinely valuable and supported by the Breakfast results. The finding that a weakly-supervised method can outperform fully-supervised ones on structured procedural datasets suggests that for activities with strong sequential regularity, the marginal information in precise temporal boundaries may be less important than the semantic ordering. However, the 50Salads results suggest this insight has boundary conditions: when activities are shorter, transitions are more frequent, and temporal regularity is weaker, frame-level supervision becomes more important. The cross-modal attention mechanism with transcript-derived local masking is an interesting design choice that moves beyond using transcripts merely as ordering constraints.

## Suggestions

- Add pseudo-label quality evaluation to the main results, showing alignment accuracy at each training stage and per-dataset. This would substantially strengthen the paper by explaining both successes and failures.
- Qualify the "competitive with fully-supervised" claim by separating deterministic and stochastic results clearly in the abstract and conclusion.
- Investigate and report the 50Salads gap more thoroughly: Is it pseudo-label quality, model capacity, or inherent dataset difficulty? A simple experiment varying pseudo-label noise could help.
- Provide a fairer comparison with WS-DA across all evaluation settings.

## Score and Decision

The paper presents a genuinely novel problem formulation (transcript-only dense LTA) with a well-architected solution and strong results on the Breakfast benchmark. However, the significant performance gap on 50Salads, the absence of pseudo-label quality analysis, and the misleading presentation of stochastic results as competitive with supervised methods temper enthusiasm. The contribution is meaningful but the evidence is not fully convincing that transcript-based supervision is a robust general alternative to full supervision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>