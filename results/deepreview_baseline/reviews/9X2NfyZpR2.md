## Summary

The paper proposes TbLTA, the first fully weakly-supervised framework for dense long-term action anticipation (LTA) from video. During training, only video transcripts—ordered action lists without timing or duration—are used, eliminating the need for costly frame-level annotations. The architecture combines a transformer encoder, a weakly-supervised temporal alignment module (ATBA) to generate pseudo-labels, cross-modal attention to ground video features with transcript embeddings, and an anticipation decoder with CRF-based sequence modeling. Experiments on Breakfast, 50Salads, and EGTEA show that transcript-only supervision yields results competitive with fully supervised methods, establishing a new weakly-supervised baseline for LTA.

## Strengths

- **Problem relevance and novelty**: The paper addresses a genuine scalability bottleneck in LTA—dense frame-level annotation—and introduces the first framework that operates solely on video transcripts. This is a meaningful step toward more practical, language-informed anticipation models.
- **Strong empirical results**: On Breakfast, the deterministic TbLTA matches or exceeds recent fully supervised methods (e.g., ActFusion, FUTR) at several observation/prediction splits, and the stochastic variant achieves even higher top-1 accuracy, demonstrating that transcript supervision can be surprisingly effective.
- **Thorough ablation study**: Each component (CTC loss, cross-attention, CRF, duration loss) is systematically ablated on two datasets, clearly showing their individual contributions and justifying the design choices.
- **Clear exposition**: The problem setting, architectural details, and loss formulations are well described. Figures 1 and 2 effectively communicate the training/inference pipelines.

## Weaknesses

### Fatal
None.

### Major

- **Limited comparative baselines**: The weakly-supervised comparison is restricted to WS-DA (Zhang et al., 2021), which is semi-weakly supervised and uses frame labels for the observed portion. A proper fully weakly-supervised baseline is missing, making it difficult to isolate the advantage of TbLTA. Comparisons to other weakly-supervised methods for temporal action segmentation (e.g., CTD, ASR) that could be adapted to LTA are absent, weakening the claim of “first baseline.”
- **Incomplete reporting of stochastic protocol**: The stochastic results (Mean and Top1) are reported only in Tables 1 and 3, but the specific sampling procedure, number of samples, and how “Mean” vs. “Top1” are computed are not explained in the main text or the supplementary material (which is stripped). This leaves a significant ambiguity about what the numbers represent and how they should be interpreted relative to deterministic methods.
- **Selective success on datasets**: While TbLTA excels on Breakfast, its performance on 50Salads is substantially below strong supervised methods (e.g., ActFusion: 28.39 vs. TbLTA deterministic: 20.92). On EGTEA, it lags behind supervised methods on the “All” and “Freq” categories. The narrative emphasizes competitiveness but downplays these gaps. A more candid discussion of when and why transcript supervision fails would strengthen the paper.

### Minor

- **Overclaim on “superior” performance**: The abstract and conclusion state “competitive with, and in some settings superior to, fully supervised methods.” The “superior” claim rests mainly on Breakfast at 30% observation, where TbLTA outperforms ActFusion. However, this is only one of many splits, and on 50Salads TbLTA is clearly inferior. The claim should be qualified more precisely.
- **Dependence on prior modules**: The temporal alignment module (ATBA) and the CRF formulation are directly adopted from previous work (Xu & Zheng, 2024; Maté & Dimecicoli, 2024). While the combination is novel, the paper would benefit from clarifying which parts are novel contributions versus integration of existing methods.

### Trivial

- Figure 3 is somewhat low-resolution and the legend is difficult to read; a higher-quality rendering would improve readability.
- The caption of Table 1 uses “*” for stochastic protocol but does not define “grey” highlighting consistently in the text.

## Nice-to-Haves

- Provide confidence intervals or error bars for the main results to quantify variability across splits.
- Include an ablation that removes the transcript entirely (random transcript?) to measure the lower bound of transcript usefulness.
- Compare against a simple baseline that uses only the CTC loss without the ATBA-based pseudo-labeling to isolate the contribution of the alignment module.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Add a proper fully weakly-supervised baseline by training a recent TAS method (e.g., ASR or CTD) to produce frame predictions and then applying a simple anticipation rule (e.g., repeating the last predicted observed action). This would contextualize TbLTA’s advantage.
- Clarify the stochastic inference protocol: specify the number of stochastic samples, how “Mean” and “Top1” are aggregated, and whether the same seed or multiple runs are used.
- Frame the results more honestly: emphasize that TbLTA is the first transcript-only LTA method and that it approaches supervised performance on certain benchmarks, while acknowledging where it still falls short.

## Score and Decision

**Score**: 6  
**Decision**: Accept  

MY FINAL SCORE: 6<score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>