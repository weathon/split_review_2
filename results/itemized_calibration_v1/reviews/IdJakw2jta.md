## Summary

This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), extending the task from ~20-second clips to 1–5 minute videos. The authors propose ART-STVG, an autoregressive transformer that processes frames sequentially (rather than all-at-once like prior DETR-style methods) with spatial and temporal memory banks that use selective retrieval. ART-STVG also employs a cascaded spatio-temporal decoder (spatial output → RoI pooling → temporal decoder) instead of parallel spatial+temporal heads. On extended LF-STVG benchmarks derived from HCSTVG-v2, ART-STVG substantially outperforms prior methods, with gains widening on longer videos.

## Strengths

1. **Well-motivated new task (Section 1).** The observation that existing STVG benchmarks cap at ~20–35 seconds while real applications require minutes of coverage is genuine. The paper correctly identifies that all-at-once processing faces both GPU-memory bottlenecks and contextual reasoning challenges on longer videos. The problem framing itself is a clear contribution.

2. **Principled autoregressive architecture (Sections 3.2–3.4).** Treating video as a streaming input and processing frames one at a time is the natural response to the fixed-frame-budget limitation. The memory banks with selection strategies—top-*N* text-similarity for spatial (Sec. 3.3) and TextTiling-style event-boundary detection for temporal (Sec. 3.4)—are reasonable mechanisms for retaining long-range context without diluting attention with irrelevant frames.

3. **Strong empirical results on LF-STVG (Table 1).** Improvements grow consistently with video length. On LF-STVG-5min, ART-STVG achieves 15.0 m.tIoU vs. 8.1 for the best prior method (CG-STVG)—nearly 2×. On LF-STVG-3min: 23.0 vs. 14.2. The trend (wider gap on longer videos) aligns with the paper's thesis and is the strongest evidence in the paper.

4. **Cascaded spatio-temporal decoder (Section 3.2, validated in Table 4).** Connecting spatial decoder output (ROI-pooled target features) to the temporal decoder, instead of parallel spatial+temporal heads, is a simple but sensible architectural contribution that yields 1.5% m.tIoU improvement.

## Weaknesses

### Major

1. **How prior methods handle videos longer than their frame budget is not specified (Section 4.1).** Current STVG methods (TubeDETR, STCAT, CG-STVG, TA-STVG) process a fixed number of frames simultaneously (typically 64–128). At 3.2 FPS, a 1-minute video has ~192 frames and a 5-minute video ~960 frames—far beyond what these models can ingest in one forward pass. The paper states only: "all methods including ART-STVG are trained exclusively on the HCSTVG-v2 training set" (line 206). It does *not* specify: (a) how prior methods were adapted at test time for longer videos (frame subsampling? windowed processing with prediction merging?), (b) whether released code was modified, or (c) what frame counts or window sizes were used. The paper's central claim (that autoregressive processing is superior for long videos) depends on this comparison. If prior methods had to discard most frames while ART-STVG processes all frames sequentially, the comparison would be systematically biased in ART-STVG's favor.

### Minor

2. **Dataset extension annotation protocol is underspecified (Section 4, Dataset paragraph).** The paper extends HCSTVG-v2's validation set from 20-second clips to 1–5 minutes by retrieving original YouTube videos. However, it does not clarify how ground-truth annotations (bounding boxes per frame + temporal event boundaries) cover the extended portions. The text says: "we manually review the extended videos to ensure their quality" (line 201). This does not specify whether the original 20-second annotations were simply carried forward (evaluating whether the model locates the known event within a longer video) or whether new annotations were added for the extended portions. Either approach is defensible, but the missing detail makes the evaluation protocol unclear.

3. **Inconsistency between Table 1 baseline and Table 3 ablation row ❶.** On LF-STVG-3min, the "Baseline (ours)" in Table 1(c) achieves 16.7 m.tIoU and is described as "without memory and memory selection modules" (line 208). Table 3 row ❶ (spatial decoder ablation, also dash-marked for memory/selection) achieves 21.3 m.tIoU. The 4.6-point gap likely arises because the Table 1 baseline removes *both* spatial and temporal memory while Table 3 only removes spatial memory (retaining temporal memory), but the paper never clarifies this. The mismatch undermines confidence unless resolved.

4. **Handling of frames without the target is not discussed (Section 3.2).** The spatial decoder predicts a box *bᵢ* for every frame (line 108), and the temporal decoder produces start/end probabilities *hᵢ* for every frame (line 124). In STVG, the target is present only during a contiguous temporal segment. The paper does not explain: (a) whether the model predicts "no object" for non-event frames, (b) how loss is computed for such frames, or (c) how m.vIoU evaluation handles frames outside the target interval.

5. **Missing ablation that isolates the autoregressive design (Section 4.2).** The paper's core claim is that sequential processing is crucial for LF-STVG. However, the "Baseline" in Table 1 removes both memory banks *and* the cascaded design simultaneously—it does not isolate the autoregressive property. An ablation comparing ART-STVG against a variant that keeps memory banks and cascade but processes frames in parallel (to the extent GPU memory allows) would directly test whether sequential processing itself drives the gains, rather than the added components.

### Trivial

None.

## Nice-to-Haves

- **Computational cost comparison.** The paper motivates autoregressive processing partly on computational grounds (GPU-memory bottleneck) but provides no quantitative comparison of peak GPU memory, FLOPs, or inference time per video-second against prior methods across different video lengths. Adding this would strengthen the motivation.
- **Memory bank capacity discussion.** The spatial memory bank grows without bound (line 148: "without removing any existing memories"). For hour-long videos (a stated motivation), an eviction or summarization policy would be needed. A brief limitation discussion would be helpful.

## Removed Points

These points were flagged but are removed after cross-checking; treat them with caution:

- **"Critical Issue 4: Temporal inference procedure unspecified"** — REMOVED. The loss function and inference details are deferred to supplementary material (line 190, 329). The parser strips these sections from all papers per standard processing; they exist in the original submission.
- **"Potential circularity in temporal memory selection"** — REMOVED. The temporal memory selection uses adjacent-frame feature similarity (content-based segmentation) to identify event boundaries as a *pre-processing step* for context selection. The temporal decoder then predicts per-frame start/end probabilities for the *target event*. These serve different roles and are not circular.
- **"Statistical significance / confidence intervals"** — REMOVED. Single-run evaluation without confidence intervals is standard practice in this benchmarking setting. Not a specific flaw of this paper.
- **Section-by-section observations about related work being "adequate" or the encoder being "sound but not novel"** — REMOVED as generic observations, not specific weaknesses.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Specify the test-time protocol for prior methods on long videos: frame sampling rate, windowing strategy, and prediction merging approach. If subsampling was used, discuss how this affects the comparison.
2. Clarify the annotation/evaluation protocol for the extended LF-STVG datasets: what ground-truth covers which portions, and how metrics are computed for frames outside the original 20-second event interval.
3. Resolve the Table 1 vs. Table 3 baseline discrepancy by explaining which memory components each configuration includes.
4. Discuss how frames without the target object/event are handled in spatial prediction, loss computation, and evaluation (this may already be in the supplementary).
5. If feasible, add an ablation comparing autoregressive vs. non-autoregressive processing with matched memory/cascade components.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>