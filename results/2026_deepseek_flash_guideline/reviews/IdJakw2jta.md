Here is the final consolidated review:

## Summary

This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), extending the task from ~20-second clips to 1–5 minute videos. It proposes ART-STVG, an autoregressive transformer that processes frames sequentially with two memory banks (spatial and temporal) using selection strategies to retain only relevant context, plus a cascaded spatio-temporal decoder. On extended HCSTVG-v2 datasets, ART-STVG substantially outperforms existing methods (e.g., +7.3% m.tIoU over TA-STVG on 5-min videos) while remaining competitive on short-form STVG (59.2 vs. 60.4 m.tIoU).

## Strengths

1. **Clear empirical demonstration with scaling evidence**: Table 1 shows ART-STVG outperforming all baselines across five video lengths (1–5 min), with the gap growing monotonically (TA-STVG advantage from +0.7% to +9.1% m.tIoU). This directly supports the core claim that the approach is better suited to long videos. Meanwhile, existing methods collapse on 5-min videos (TA-STVG vIoU@0.5 = 0.3%) while ART-STVG maintains 11.4%.

2. **Ablation isolating a non-obvious failure mode**: Table 2 shows that using *all* temporal memories degrades m.tIoU from 16.7% to 9.6% compared to no memory — a counterintuitive finding — and the memory selection mechanism specifically addresses this (recovering to 23.0%). This provides strong causal evidence for the selection contribution.

3. **Cascaded design ablation shows genuine complementarity**: Table 4, holding everything else fixed, shows the cascaded decoder outperforming a parallel variant (23.0 vs. 21.5 m.tIoU, +1.5%), supporting the claim that spatial-to-temporal information flow provides measurable gains beyond added capacity.

4. **Competitive on short-form while excelling on long-form**: Table 7 shows ART-STVG achieves 59.2 m.tIoU on SF-STVG (vs. TA-STVG's 60.4, just 1.2% behind), ruling out the hypothesis that the method trades short-video for long-video performance.

5. **Well-motivated, independently ablated memory strategies**: The spatial (top-Nₛ by text similarity) and temporal (event-boundary detection via cosine similarity) selection mechanisms are grounded in different failure modes and ablated separately (Tabs. 2, 3), verifying independent contributions.

## Weaknesses

### Fatal
None.

### Major

1. **Underspecified baseline evaluation protocol for long videos**: The paper states that existing STVG methods "process all frames at once" and identifies this as a GPU-memory bottleneck for long videos (lines 28–30). Yet it reports results for these methods on 1–5 minute videos (192–960 frames at 3.2 FPS) without specifying how they were adapted. Were frames subsampled? Were videos processed in chunks? The paper states all methods are "trained exclusively on the HCSTVG-v2 training set" and uses "provided source codes for fair comparison" (Tab. 6 caption), but does not describe the inference protocol. Without this information, the comparison is harder to interpret: ART-STVG's autoregressive design naturally sees all frames, but the baselines may have had to drop frames to fit in GPU memory. This does not invalidate the results — the baselines' vIoU@0.5 scores on 5-min videos are near 0%, suggesting genuine inability to handle long videos regardless of adaptation — but it is a significant reporting gap that the authors should address.

### Minor

1. **Dataset annotation details for extended videos**: The paper extends HCSTVG-v2 validation videos from 20 seconds to 1–5 minutes and states "we manually review the extended videos to ensure their quality" (line 200). However, it does not specify whether new ground-truth annotations (bounding boxes, temporal boundaries) exist for the extended portions or only for the original 20-second segment. Clarifying this would help the reader understand what the metrics measure.

2. **Unbounded memory bank growth**: The spatial memory bank is updated "by simply adding the query as a new memory, without removing any existing memories" (line 148). For a 5-minute video at 3.2 FPS with K decoder blocks, this produces O(K×960) stored entries. While the selection mechanisms limit what is actually *used*, the stored bank grows without bound. The paper does not discuss whether this becomes a bottleneck for even longer videos.

3. **Temporal memory selection threshold unspecified**: The temporal selection identifies event boundaries at "points with lower similarities" (line 176), but no threshold or criterion for "lower similarity" is specified. This makes the method partially irreproducible without access to the code.

4. **Training/evaluation distribution shift**: ART-STVG is trained on N_f=64 frames (~20 seconds) but evaluated on up to 960 frames (5 minutes). This 15× distribution shift is not discussed. The ablation in Table 6 (training on 40-second videos) partially addresses this but only for the 3-minute evaluation setting.

### Trivial
None.

## Nice-to-Haves
- Reporting inference speed, GPU memory usage, and FLOPs for all methods would better support the computational-efficiency motivation in the introduction.
- Releasing the extended dataset annotations would benefit the community.
- Testing with training on even longer videos (e.g., 1-minute) could further validate whether the advantage is architectural or a training-length artifact.

## Removed Points
These points from the reviews were removed with brief justification:

1. **"Autoregressive baseline undermines the design choice"** — REMOVED (misread). The baseline (no memory) performing worse is evidence that memory is needed, not a flaw in the design. The paper transparently reports the short-video gap (59.2 vs. 60.4).
2. **"Temporal memory ablation (all memories worse) should be acknowledged as a limitation"** — REMOVED (already addressed). The paper explicitly explains this finding and uses it as motivation for the selection mechanism.
3. **"Low absolute scores make comparisons unreliable"** — REMOVED (not a valid weakness). The task is inherently difficult; low absolute values do not invalidate relative comparisons between methods facing the same difficulty.
4. **"The cascaded design is not novel"** — REMOVED (subjective opinion without evidence; Table 4 provides ablation evidence for its effectiveness).
5. **Formatting/style/appendix nitpicks** — REMOVED per instructions (parser artifacts and scope).

## Novel Insights
None beyond the paper's own contributions. The reviews validate the paper's claims with evidence from the tables and identify genuine exposition gaps, but do not produce new observations about the work.

## Suggestions
1. In a rebuttal or revision, specify exactly how each baseline method was adapted for 1–5 minute videos: frame subsampling rate, chunking strategy, GPU memory optimizations, or any other modifications. This single clarification would resolve the most consequential ambiguity in the paper.
2. Clarify whether the extended HCSTVG-v2 validation set includes full-coverage annotations for the 1–5 minute clips, and describe what the evaluation metrics capture.
3. Add a brief discussion of memory bank growth and any practical limits on video length.
4. Specify the threshold or criterion for detecting event boundaries in temporal memory selection.

---

**Calibration anchors used:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| LVM-NET: Efficient Long-Form Video Reasoning (bEvI30Hb2W) | 3.00 | R1 | Lower quality — non-competitive performance, weaker novelty, single dataset. Our paper is clearly stronger. |
| Spatio-temporal Diffusion Transformer for Action Recognition (ICR3swcnaa) | 3.00 | R1 | Different task, lower quality. |
| Unsupervised open-vocabulary action recognition with autoregressive model (IryGDUHxDE) | 5.25 | R1 | Different task (action recognition), comparable quality. |
| Motion-Grounded Video Reasoning (tEei1bolt3) | 5.00 | R1 | Related task (spatiotemporal grounding with reasoning). |
| Unified Static and Dynamic: Temporal Filtering Network (UX9lljSZqX) | 6.25 | R1 | Video grounding paper with redundancy concerns in ablations. Rejected despite SOTA. Our paper has cleaner ablations. |
| TRACE: Temporal Grounding Video LLM (14fFV0chUS) | 6.75 | R1 | Accepted. Similar quality — both define new approaches to video grounding tasks with strong experiments. |
| Long Context Transfer from Language to Vision (QETk0lBdVf) | 5.80 | R2 | Long-form video understanding. Rejected with mixed reviews (5, 6, 8, 5, 5). Comparable quality. |
| ARLON: Autoregressive for Long Video Generation (8pusxkLEQO) | 6.25 | R2 | Accepted. Long video generation with autoregressive models. Different task, similar quality. |
| Video Active Perception (KtqZrNjvjd) | 5.80 | R2 | Rejected. Long-form video QA. Comparable scope, slightly lower quality. |

**Initial bracket**: 5.5–7.0 (after Round 1 comparison with LVM-NET, UniSDNet, TRACE)

**Narrowing (Round 2)**: Compared with Long Context Transfer (5.80, reject), ARLON (6.25, accept), Video Active Perception (5.80, reject). The paper is on par with or slightly stronger than the ~5.8-level papers but has a more significant reporting gap than TRACE (6.75). The core contributions are solid, and the missing details are addressable in revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>