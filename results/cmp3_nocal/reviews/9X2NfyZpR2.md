Here is my final consolidated review:

## Summary

This paper introduces TbLTA, the first framework for dense long-term action anticipation (LTA) that uses only video transcripts (ordered action lists without timing/duration) as supervision, eliminating the need for expensive frame-level annotations. The model combines a temporal alignment module (ATBA) to generate pseudo-labels, cross-modal attention to ground video features with transcript semantics, and an encoder-decoder architecture trained with CTC and CRF losses. Experiments on Breakfast, 50Salads, and EGTEA establish a transcript-only baseline, with the strongest results on Breakfast where the deterministic model is competitive with fully supervised methods.

## Strengths

1. **Well-motivated problem framing and timely contribution.** The paper clearly articulates why transcripts are a natural supervisory signal for LTA: they capture procedural action logic while being substantially cheaper than dense frame labels (Section 1). Establishing the first transcript-only baseline on three standard benchmarks is a genuine service to the community, and the paper correctly identifies this as a previously unexplored setting.

2. **Non-trivial results on Breakfast.** The deterministic TbLTA model achieves 29.03 MoC average on Breakfast, outperforming the fully supervised ActFusion (28.45). At 30% observation / 10% horizon, TbLTA reaches 40.28 versus ActFusion's 35.79 (Table 1). This is a meaningful result that demonstrates transcript-based supervision can capture procedural structure that dense labels may not provide.

3. **Principled combination of established techniques for a new setting.** The architecture integrates ATBA alignment, CTC-based transcript supervision, cross-modal attention with local masking, and CRF-based temporal coherence — each component is adapted to work under transcript-only supervision. While the components are individually known, their composition for this task is non-obvious, and the ablation study (Table 4) provides evidence that each contributes to overall performance.

## Weaknesses

### Fatal

None.

### Major

1. **Ablation study uses the stochastic Top-1 protocol, conflating architectural value with oracle selection.** Section 4.3 states ablations use the "Top-1 MoC metric." The values in Table 4 (e.g., TbLTA averages 28.5 on 50Salads, 37.2 on Breakfast) match the *stochastic* Top-1 row from Table 1 (28.51 and 37.15), not the *deterministic* row (20.92 and 29.03). The stochastic protocol generates multiple futures and selects the best one — an oracle upper bound that does not reflect deployed inference. Ablating architectural components against this inflated baseline does not reveal whether those components matter for the deterministic model that would actually be used. The paper should report ablation results for the deterministic variant, which is the primary contribution. This directly affects whether the evidence supports the paper's architectural claims.

2. **The central claim of being "competitive with fully supervised methods" holds on only one of three datasets, but this qualification is not reflected in the abstract or conclusion.** The deterministic model is genuinely competitive on Breakfast (29.03 vs. ActFusion's 28.45, Table 1). However, on 50Salads the gap is large (TbLTA 20.92 vs. ActFusion 28.39), and on EGTEA the gap is also large (TbLTA 65.37 mAP vs. Anticipatr 76.80, Table 2). The conclusion (line 291) states the model "achieves results that are competitive with, and in certain settings even superior to, fully supervised methods" without explicitly noting that this characterization primarily applies to Breakfast. The paper's own discussion at line 227 acknowledges the 50Salads gap, but this is not calibrated into the high-level claims.

### Minor

3. **Limited analysis of the prior weakly-supervised baseline.** WS-DA (Zhang et al., 2021) is the only weakly-supervised comparator, reported at a single data point (Obs 30%) with dashes for all other columns (Table 1). While the paper correctly notes WS-DA uses more supervision, no analysis is offered for why its performance is lower or how the two formulations differ. This limits the informativeness of the comparison.

4. **Soft-to-binary conversion in cross-modal attention is not discussed.** The ATBA module generates "soft per-frame pseudo-labels that preserve boundary uncertainty" (line 126), which the paper argues is "crucial" for long-horizon anticipation. Yet the cross-modal attention layer (line 130) converts these to a "binary local mask M," discarding the uncertainty information. This tension is not addressed in the paper.

5. **No analysis of pseudo-label quality.** The entire method depends on ATBA-generated pseudo-labels, but the paper never reports how accurate these alignments are (e.g., frame-wise accuracy on the observed portion against ground truth). Without this, it is unclear whether downstream components are learning from reliable targets or propagating alignment errors.

### Trivial

6. **Abstract slightly overstates the gap in prior LTA supervision.** The abstract claims LTA has been tackled "exclusively in a fully supervised manner" (line 9), but the paper itself cites Zhang et al. (2021) as a prior weakly-supervised attempt. The Introduction (line 15) correctly qualifies this, so the inconsistency is limited to the abstract.

## Nice-to-Haves

- A simple baseline using ATBA alignment alone (aligning the transcript to the observed portion and outputting the remaining transcript actions as the anticipation) would help isolate whether the learned encoder-decoder adds value beyond the alignment module.
- Reporting error bars or confidence intervals would be valuable, especially for the ablation study where some differences (e.g., 0.6 points for CTC on 50Salads) may be within noise given the small dataset sizes.
- A discussion of *when* transcript-only supervision works vs. fails, grounded in measurable properties (e.g., alignment accuracy as a function of video length or action density), would convert the descriptive observation about Breakfast vs. 50Salads into actionable insight.

## Removed Points

- **Missing Table 3 (IAS results):** The reviewer flagged that Table 3 (mentioned at line 235) is missing from the parsed paper. The parser strips appendix/supplementary sections from all papers. This content exists in the original submission and is therefore not a valid weakness.
- **Novelty concern ("method's novelty is primarily in task formulation, not technique"):** This is a subjective assessment of contribution style rather than a concrete weakness. Many good papers productively combine existing components for a new task. The paper appropriately cites its inspirations. The reviewer acknowledges this is "not a fatal issue." Removed because it conflates adopted components (which the paper transparently cites) with lack of contribution.
- **I3D features being "dated":** The claim that using I3D features is a weakness because "many recent LTA papers use video-language features" is speculative — the reviewer provides no evidence that this choice materially affects the method's validity or the paper's conclusions. I3D remains standard in the action understanding literature.
- **Qualitative results showing "only two examples":** The paper states "More qualitative results are provided in the supp. mat." (line 287), which the parser strips. This is not a weakness.
- **Inference cost / sampling strategy for stochastic variant:** The paper states details are "in the supp. mat." (line 223). The appendix is stripped by the parser. Not a valid weakness.
- **ATBA-only baseline suggestion framed as a weakness:** The reviewer presents this as a missing baseline, but the paper's contribution is the full architecture operating under transcript-only supervision, not the alignment module. This is more appropriately a nice-to-have suggestion.

## Novel Insights

The key insight that emerges from combining the reviews is that the paper's evidence is stronger than its claims in some ways and weaker in others. On the positive side, the deterministic model's 29.03 MoC on Breakfast genuinely outperforming the fully supervised ActFusion (28.45) is a non-trivial finding that suggests transcript-based supervision captures procedural structure that dense labels may not provide. On the negative side, the ablation study's reliance on the stochastic Top-1 protocol creates a disconnect: the paper's architectural analysis is validated against an oracle metric while the paper's main claims are about the deterministic model. This tension — between the evaluation protocol used for analysis and the protocol used for claims — is the single most important issue the authors should address, as it prevents readers from having full confidence in either the architectural design choices or the comparative claims.

## Suggestions

The single highest-leverage improvement is to **re-run the ablation study using the deterministic protocol** (not stochastic Top-1). This alone would determine whether the architectural components (CRF, cross-attention, duration loss) are as important as claimed for the model that would actually be deployed. Second, **recalibrate the claims in the abstract and conclusion** to reflect that the "competitive with fully supervised" characterization primarily applies to Breakfast, while noting the method's strengths on other datasets (e.g., competitive on rare classes in EGTEA). Third, **report pseudo-label alignment accuracy** on the observed portion to contextualize the method's ceiling and identify failure modes.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>