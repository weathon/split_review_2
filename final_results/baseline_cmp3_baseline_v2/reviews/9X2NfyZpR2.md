##Summary

This paper introduces TbLTA, the first weakly-supervised framework for dense long-term action anticipation (LTA) that relies solely on video transcripts (ordered action lists without timing or duration) during training, eliminating the need for expensive frame-level annotations. The model uses a temporal alignment module to generate pseudo-labels, cross-modal attention to ground video features with transcript semantics, and a combination of CTC, CRF, and duration losses to supervise both segmentation and anticipation. Experiments on Breakfast, 50Salads, and EGTEA show that transcript-only supervision yields results competitive with fully supervised methods, establishing a new and more scalable paradigm for LTA.

## Strengths

- **Novel problem formulation.** The paper is the first to tackle dense LTA using only transcript-level supervision, which is significantly cheaper to obtain than frame-level annotations. This opens a practical and scalable direction for the field.
- **Well-motivated and principled architecture.** The design choices—temporal alignment for pseudo-labels, cross-modal attention for feature enrichment, and a multi-loss objective (CTC, CRF, duration)—are clearly motivated by the challenges of weak supervision and long-horizon forecasting. Each component is ablated and shown to contribute.
- **Competitive empirical results.** On Breakfast, TbLTA outperforms all fully supervised methods at 30% observation and matches or exceeds them at other settings. On 50Salads and EGTEA, the stochastic variant achieves strong results, and the method consistently beats the only prior (semi-)weakly-supervised baseline (Zhang et al., 2021).
- **Thorough evaluation.** Experiments cover three diverse benchmarks (Breakfast, 50Salads, EGTEA) with multiple observation/prediction splits, both deterministic and stochastic protocols, and ablation studies that isolate the effect of each loss and module.

## Weaknesses

### Fatal
None.

### Major
- **Performance gap on 50Salads (deterministic).** The deterministic TbLTA lags behind fully supervised methods by a large margin (e.g., 20.92 vs. 28.39 average MoC). While the stochastic variant closes the gap, the paper’s claim of being “competitive with fully supervised methods” is only partially supported. The authors acknowledge this but do not provide a deeper analysis or mitigation.
- **Limited novelty beyond combination of existing components.** The temporal alignment module (ATBA) and the CTC loss are directly adopted from prior weakly-supervised TAS work. The CRF and duration loss are also known techniques. The main novelty is the adaptation of these ideas to LTA and the cross-modal attention design. The paper would benefit from a clearer delineation of which parts are novel versus inherited, and a more detailed discussion of the unique challenges of applying these to LTA.

### Minor
- **Incomplete ablation for CTC loss.** The text states that removing CTC degrades performance, but no table or quantitative results are provided for this ablation in the visible content. The reader cannot verify the magnitude of the effect.
- **Stochastic protocol not fully explained.** The paper mentions reporting stochastic results following Abu Farha & Gall (2019) but does not describe how multiple futures are sampled or how Top-1 is selected. The supplementary material is not available for review.
- **EGTEA evaluation uses a different metric (mAP for verb prediction) than the other datasets (MoC), making cross-dataset comparison less direct.** The comparison to supervised methods on EGTEA is also limited to only two baselines.

### Trivial
- The paper uses “TbLTA” and “TBLTA” inconsistently in the text and figures (e.g., Figure 1 caption uses “TBLTA” while the abstract uses “TbLTA”). This is a minor formatting issue.

## Nice-to-Haves

- An analysis of where the deterministic model fails on 50Salads (e.g., which action classes or temporal horizons are most affected) would help understand the limitations of transcript-only supervision for longer, denser videos.
- A study of the sensitivity to the number of pseudo-label refinement steps or the progressive training schedule would strengthen the empirical grounding.
- Comparison to a simple baseline that uses transcripts as a sequence-level ordering constraint without pseudo-labels (e.g., only CTC) would isolate the benefit of the alignment module.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Clarify the novelty contribution by explicitly stating which components are inherited from prior work (ATBA, CTC) and which are newly introduced for LTA (cross-modal attention with local masking, CRF on decoder outputs, self-supervised duration loss).
- Provide the CTC ablation results in a table to match the other ablations.
- Include a brief description of the stochastic inference protocol (e.g., how multiple samples are generated and how Top-1 is selected) in the main paper, since the supplementary is not available.
- Discuss why the deterministic model underperforms on 50Salads and whether the gap can be reduced by better pseudo-label quality or longer training.

## Score and Decision

**Score:** 6.5  
**Decision:** Accept  

The paper makes a clear and valuable contribution by demonstrating that dense long-term action anticipation is feasible with only transcript-level supervision, which is a significant step toward scalable and practical video understanding. The method is sound, the experiments are thorough, and the results are competitive. The weaknesses—primarily the performance gap on one dataset and the reliance on existing components—do not invalidate the core contribution but suggest that further work is needed to close the gap with fully supervised methods. Overall, the paper merits acceptance as it opens a new research direction and provides a strong baseline for future work.

MY FINAL SCORE: <score>6.5</score>  
MY FINAL DECISION: <decision>Accept</decision>