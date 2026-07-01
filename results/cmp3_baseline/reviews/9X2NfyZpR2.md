## Summary

The paper proposes TbLTA, the first framework for dense long-term action anticipation (LTA) trained exclusively from video transcripts—ordered action lists without temporal boundaries or durations. The model uses a temporal alignment module to generate pseudo-labels, cross-modal attention to couple video features with transcript semantics, and a combination of CTC, CRF, and duration losses to supervise both segmentation and anticipation without frame-level annotations. Experiments on Breakfast, 50Salads, and EGTEA show that transcript-only supervision yields results competitive with fully supervised methods on some benchmarks, particularly Breakfast, establishing a novel weakly-supervised paradigm for LTA.

## Strengths

1. **Novel and important problem formulation**: The paper addresses a genuine limitation of existing LTA work—the reliance on expensive frame-level annotations—by demonstrating that transcripts alone can provide sufficient supervision. This opens a more scalable path for real-world LTA applications where dense labels are impractical.

2. **Comprehensive and well-designed methodology**: The architecture integrates multiple complementary components (temporal alignment for pseudo-label generation, cross-modal attention for feature grounding, CTC for sequence-level alignment, CRF for temporal coherence, and a self-supervised duration module) that are each motivated and ablated. The progressive training scheme (pre-training → alignment → end-to-end) is a practical solution to the cold-start problem of pseudo-labeling.

3. **Strong empirical results on Breakfast**: The deterministic model outperforms all fully supervised baselines (including ActFusion, FUTR, and Cycle Cons.) at 30% observation across all horizons, and is competitive at 20% observation. This is a genuinely surprising result given the complete absence of frame-level labels, and it convincingly demonstrates that transcripts capture enough procedural structure for anticipation.

4. **Thorough ablation studies**: The ablations in Tables 3 and 4 systematically isolate the contribution of each loss component and architectural choice across two datasets, providing clear evidence for the value of CTC, cross-modal attention, CRF, and duration losses. The degradation patterns are consistent and interpretable.

5. **Clear writing and reproducible framing**: The problem definition, training/inference pipeline, and evaluation protocols are clearly stated. The paper establishes the first transcript-only baselines on three standard benchmarks, which will be valuable for future work in this direction.

## Weaknesses

### Fatal
None.

### Major

1. **Performance gap on 50Salads is substantial**: While the paper highlights competitive results, the deterministic TbLTA on 50Salads lags behind fully supervised ActFusion by 7.5 points on average (20.92 vs. 28.39), with gaps as large as 15 points at short horizons (e.g., Obs 30%, horizon 10%: 27.67 vs. 42.80). The claim "occasionally superior to fully supervised approaches" is only true on Breakfast at 30% observation and is not representative of overall performance. The paper should be more measured in articulating where and why transcript supervision works well versus where it struggles.

2. **Misleading presentation of stochastic results**: The paper reports "Ours (TbLTA)* - Top1" which achieves 28.51 on 50Salads—comparable to ActFusion's 28.39. However, this is a stochastic (Top-1 from multiple samples) rather than deterministic result, and it is compared against fully supervised deterministic methods. The paper does not clearly separate these evaluation protocols, and the "Top1" stochastic protocol is not standard for the deterministic baselines. The averaging in Table 1 (mixing deterministic, stochastic mean, and stochastic top-1 in the same column) is confusing and inflates the perceived competitiveness.

3. **Limited comparison to existing weakly-supervised LTA work**: The only prior weakly-supervised LTA method (Zhang et al., 2021, WS-DA) is cited but only a single number is reported for each dataset (e.g., 21.30 on 50Salads, 15.65 on Breakfast). No direct comparison under the same evaluation protocol (observation percentage, horizon) is provided. Since WS-DA uses a different supervision level (weak labels for the next action rather than full transcripts), the paper should at minimum discuss why direct comparisons are difficult and provide whatever comparable numbers are available.

4. **EGTEA evaluation is limited**: Only two supervised baselines are compared, both from 2019 and 2022. The paper reports 65.37 mAP (All) vs. Anticipatr's 76.80—an 11-point gap. The claim that transcript supervision "can mitigate data imbalance" is supported only by the Rare class result (60.11 vs. 55.10 for Anticipatr, 59.70 for Timeception), but without statistical significance or more baselines, this is weak evidence. The different metric (mAP vs. MoC) also makes cross-dataset synthesis difficult.

### Minor

1. **Reliance on existing alignment module**: The temporal alignment module is adopted from ATBA (Xu & Zheng, 2024). While the paper integrates it into a novel LTA context, the core alignment method is not novel. The paper would benefit from clarifying which components are novel contributions versus adaptations of prior work.

2. **Annotation cost not quantified**: The paper motivates transcript supervision as "significantly cheaper" but provides no estimate of annotation time, cost, or labor reduction compared to dense frame-level labeling. A quantitative comparison would strengthen the practical motivation substantially.

3. **No failure case analysis**: The qualitative results show two successful examples, but the paper does not analyze cases where the model fails (e.g., on 50Salads where performance is weaker). Understanding failure modes would help contextualize the method's limitations.

### Trivial

None.

## Nice-to-Haves

- A cost-benefit analysis (annotation time/cost for transcripts vs. dense labels) would substantially strengthen the practical motivation.
- Multi-sample stochastic results on EGTEA to see if the rare-class advantage persists.
- Results with vision-language model features (e.g., CLIP, ViCLIP) instead of I3D, to test whether stronger visual features further close the gap with supervised methods.
- A discussion of how the number of action classes or video length correlates with performance degradation under transcript supervision.

## Novel Insights

The central insight—that the narrative temporal structure of transcripts, combined with weak alignment signals (CTC, CRF, pseudo-labels), can substitute for dense frame-level supervision in LTA—is genuinely novel and practically important. More subtly, the paper shows that transcript-based supervision can sometimes *exceed* fully supervised performance on datasets with strong procedural regularities (Breakfast at 30% observation). This suggests that transcripts act as a structured prior that regularizes the model toward the correct action ordering, while frame-level labels may overfit to spurious visual correlates. The ablation study further reveals that the cross-modal attention mechanism is the single most important component on Breakfast (5.7 point drop when removed), indicating that grounding visual features with language semantics is especially valuable when temporal annotations are absent. The observation that the duration loss provides modest but consistent gains despite being trained without ground truth durations is also insightful for future work on self-supervised temporal modeling.

## Suggestions

1. Restructure Table 1 to clearly separate deterministic and stochastic evaluation protocols, and add a note clarifying which methods are fairly comparable under each protocol. The current mixing of protocols in one table is misleading.

2. Add a more complete comparison to Zhang et al. (2021) by re-implementing or citing their results under the same observation/horizon conditions. If this is not possible, add a paragraph explicitly discussing the differences in supervision and why direct comparison is difficult.

3. Tone down the claim about being "occasionally superior" to fully supervised methods, and instead frame the contribution more precisely: transcript supervision is highly effective on procedurally regular datasets (Breakfast) while showing a clearer gap on datasets with denser transitions and less regularity (50Salads, EGTEA).

4. Quantify the annotation cost savings (e.g., "transcripts require approximately X minutes per video vs. Y minutes for dense labels") to substantiate the scalability motivation.

## Score and Decision

The paper tackles an important and underexplored problem—reducing annotation cost for LTA—and proposes a well-engineered solution with clear components and thorough ablations. The results on Breakfast are genuinely impressive and establish a new weakly-supervised baseline. However, the performance gap on 50Salads and EGTEA is substantial, the presentation of stochastic results is misleading, and the comparison to the only prior weakly-supervised LTA work is insufficient. The core contribution (first transcript-only LTA framework) is solid and the methodology is sound, but the empirical claims are somewhat overstated relative to the full set of results.

Score: 6 — borderline accept. The paper has clear value for the community and the approach is novel, but the empirical evidence is uneven and the presentation of results needs more careful framing.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>