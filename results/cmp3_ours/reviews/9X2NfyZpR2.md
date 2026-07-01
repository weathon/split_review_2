## Summary

This paper introduces TbLTA, the first framework for dense long-term action anticipation (LTA) trained exclusively from video transcripts (ordered action lists without timing or duration information), eliminating the need for frame-level annotations. The method combines a weakly-supervised temporal alignment module (adapted from ATBA) to generate pseudo-labels, cross-modal attention between video features and transcript embeddings, and an encoder-decoder architecture with CTC, CRF, and duration losses. Experiments on Breakfast, 50Salads, and EGTEA establish the first transcript-only LTA baselines and show competitive performance with supervised methods on Breakfast.

## Strengths

1. **Well-motivated and clearly scoped problem.** The paper correctly identifies that LTA has been tackled exclusively with dense frame-level annotations while TAS has already moved toward weak supervision, and that transcripts (ordered action lists without timestamps) are a natural fit for LTA's focus on procedural logic (Section 1, lines 13–17). This framing is specific, defensible, and makes clear why the paper is worth reading.

2. **Cross-modal attention with local masking (Section 3.1, Eq. 1–2) is a clean design choice.** Using predicted pseudo-labels to construct a binary mask that restricts each action text embedding to its temporal neighborhood, then injecting grounded features via a gated residual connection, is a sensible way to avoid the "global average of unrelated text" problem. The ablation (Table 4) confirms this component consistently matters — performance drops by ~5.7 points on Breakfast and ~1.3 points on 50Salads when removed, among the largest ablation effects in the paper.

3. **Establishes usable baselines on three benchmarks.** Reporting results on Breakfast, 50Salads, and EGTEA across multiple observation/horizon splits (Table 1, Table 2) provides a starting point for future work on weakly-supervised LTA. This is a genuine service to the community, even if absolute numbers are below supervised methods on most settings.

## Weaknesses

### Major

1. **The comparison to WS-DA — the only existing weakly-supervised LTA baseline — is too thin to support the headline claim.** WS-DA (Zhang et al., 2021) is reported at a single evaluation point per dataset: Obs 30% on Breakfast (15.65) and Obs 30% on 50Salads (21.30). No other observation/horizon combinations are provided (Table 1). The paper claims TbLTA "consistently surpasses" WS-DA (Section 4.2), but this cannot be fully assessed with one data point per dataset. Since WS-DA uses *more* supervision (some frame-level labels) — as the paper itself notes in the Table 1 footnote — a thorough multi-horizon comparison would substantially strengthen the central thesis.

2. **The "competitive with fully supervised methods" narrative overstates what the evidence supports.** The claim broadly holds for Breakfast (TbLTA deterministic avg 29.03 vs ActFusion 28.45) but not for 50Salads, where TbLTA (avg 20.92) trails ActFusion (28.39) by 7.5 points (Table 1), or EGTEA, where TbLTA (65.37 mAP) trails Anticipatr (76.80) by 11.4 points on the All category (Table 2). The paper acknowledges these gaps in passing ("Performance on 50Salads paints a complementary picture", "supervised models retain a clear edge overall on EGTEA") but the overall narrative weights the Breakfast result more heavily than the full evidence warrants.

### Minor

1. **Missing "upper bound" ablation.** The paper does not train TbLTA with ground-truth frame-level labels replacing the pseudo-labels (while keeping everything else identical). This single experiment would directly quantify the performance gap caused by weak supervision vs. the architecture itself, and would be the most informative ablation for understanding where the method's limitations come from.

2. **CRF ablation shows inconsistent effects.** On Breakfast at Obs 20%, β=10%, removing the CRF *improves* accuracy (39.7 vs 37.2, Table 4). While the paper notes this ("short-term accuracy remains similar, even slightly higher on BF"), there is no exploration of why a designed component sometimes hurts. This weakens confidence in the design's necessity.

3. **EGTEA evaluation is restricted to verb-only mAP** on a verb-noun dataset. The paper states it follows the protocol of Nagarajan et al. (2020), but verb-only evaluation may inflate numbers relative to full verb-noun evaluation. This choice should be justified or accompanied by full evaluation results.

4. **No systematic error analysis.** The paper acknowledges duration prediction is challenging (Section 4.4, Conclusion) but does not analyze failure modes: does the model confuse action order, collapse durations to the mean, or fail more on rare actions? Understanding failure modes would strengthen the contribution and guide future work.

5. **The "first" claim in the Introduction could be more precise.** The paper claims "the first weakly-supervised approach for LTA." Kim et al. (2024) explored language-based anticipation without explicit time annotations using a VLM with in-context learning (Section 2). The distinction (training an encoder-decoder from scratch with dense frame-level predictions vs. prompting a VLM) is reasonable but should be stated explicitly upfront rather than left for the Related Work section.

### Trivial

- Table 4 content is duplicated across two identical tables in the paper text (parser artifact).
- Only two qualitative examples are shown in the main paper (Figure 3); more are deferred to supplementary.

## Nice-to-Haves

- An ablation replacing ATBA-style pseudo-labels with simpler alternatives (e.g., CTC-only alignment, or Viterbi decoding) would clarify whether the ATBA module specifically drives performance or whether simpler alignment would suffice.
- Reporting loss weights (γ₁, γ₂, γ₃) and key training hyperparameters in the main paper — the current version defers these to supplementary material extracted by the parser.
- Reporting standard deviations or confidence intervals would help assess whether observed differences between methods or ablation conditions are meaningful, though this is not standard practice in the published baselines either.

## Removed Points

These points were removed from the input review with justification:

- **"Loss weights not reported in main paper"** — REMOVED per hard rule: the parser strips appendix/supplementary material from all papers; these details exist in the original submission.
- **"Stochastic results inflate apparent performance"** — REMOVED: the paper clearly separates deterministic (bold) and stochastic (gray) results in Table 1 with an explicit footnote, and the narrative discusses them in separate sentences. No conflation exists.
- **"Global guidance loop unclear"** — REMOVED: Section 3.1 clearly explains that pseudo-labels are used to construct the binary mask M for cross-attention ("Given encoder features and pseudo-labels, we construct a binary local mask..."). The mechanism is adequately described.
- **"Missing related works"** — REMOVED per hard rule about not commenting on missing related works without external verification.
- **"ATBA adoption limits novelty"** — WEAKENED to a nice-to-have suggestion (ablation against simpler alternatives). The paper clearly attributes ATBA to Xu & Zheng (2024) and describes its adaptation to LTA (partitioning transcript into observed/future sub-transcripts), which is a legitimate contribution.
- **"Reproducibility concerns about hyperparameters"** — REMOVED per hard rule about not penalizing deferred implementation details.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add an "upper bound" ablation**: train TbLTA with ground-truth frame-level labels replacing pseudo-labels to quantify the supervision gap.
2. **Expand the WS-DA comparison** across multiple horizons, even via re-implementation, to substantiate the "consistently surpasses" claim.
3. **Calibrate the narrative claims** ("competitive with supervised methods") to precisely match which datasets and settings support them, distinguishing Breakfast from 50Salads and EGTEA.
4. **Analyze the CRF inconsistency**: understand why removing the CRF sometimes improves short-horizon accuracy on Breakfast.
5. **Include loss weights and key training hyperparameters** in the main paper.

## Score and Decision

**Calibration anchors** (retrieved from deepreview_13k_calibration):

| Paper | Avg Score | Decision | Comparison to TbLTA |
|-------|-----------|----------|---------------------|
| Actions-to-Action (dl34rOnbqJ) | 4.40 | Reject | Weaker contribution — main design component showed minimal ablation improvement. TbLTA has clearer contribution and stronger ablations |
| Boundary Denoising (bLpUtGyf9g) | 5.75 | Accept | Comparable strength — both have real contributions but notable evaluation gaps. TbLTA has clearer methodology |
| AntGPT (Bb21JPnhhr) | 6.25 | Accept | Stronger evaluation and SOTA results, but also uses more supervision. TbLTA tackles a harder (weakly-supervised) setting |
| Action Seq. Aug. (f3CdjpPkSq) | 6.50 | Accept | More thorough experimental validation across multiple baselines. TbLTA experiments are less comprehensive |

**Bracket**: Initial bracket 4.5–6.0. After comparing with anchors, TbLTA clearly exceeds the weak-reject band (<4.5) but falls below the strongest accepted papers (>6.0) due to incomplete WS-DA comparison, overclaimed narrative, and missing upper-bound ablation.

TbLTA introduces a genuinely novel problem formulation (first transcript-only LTA) with a sensible, modular architecture and reasonable experiments across three benchmarks. However, the evaluation has two significant gaps — the WS-DA comparison rests on a single data point per dataset, and the headline claim of being "competitive with supervised methods" only reliably holds for Breakfast — that limit the strength of the contribution as currently presented. These are addressable with additional experiments and more careful claim calibration.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>