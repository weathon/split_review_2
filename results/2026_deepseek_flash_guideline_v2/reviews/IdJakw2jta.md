Now let me produce the final consolidated review.

---

## Summary

This paper explores Long-Form Spatio-Temporal Video Grounding (LF-STVG), a new task setting where the goal is to localize a target in 1–5 minute videos given a text query. Current STVG methods process all frames at once (batch-style), which does not scale to long videos. The authors propose ART-STVG, an autoregressive transformer that processes frames one at a time, uses selective spatial and temporal memory banks to store relevant historical context, and employs a cascaded spatio-temporal decoder that leverages spatial grounding to assist temporal grounding. On extended HCSTVG-v2 benchmarks of 1–5 minutes, ART-STVG outperforms all prior methods by increasing margins as video length grows, while remaining competitive on short-form STVG.

## Strengths

1. **Growing advantage with video length directly validates the central thesis.** Table 1 shows ART-STVG's performance advantage over all prior methods grows monotonically from ~1 point at 1 minute to ~7 points at 5 minutes (m.tIoU). This pattern — not just the absolute numbers — is evidence that autoregressive streaming addresses a scalability failure of batch-processing methods.

2. **Memory selection is ablated as the critical component.** Table 2 shows a non-obvious result: using *all* temporal memories (9.6% m.tIoU) is worse than no temporal memory at all (16.7%), while the proposed memory selection achieves 23.0% — a 13.4-point gain. Table 3 shows a similar (though less dramatic) pattern for spatial memory. This is specific evidence that the selection mechanism is not a minor refinement but the enabler of useful memory.

3. **Cascaded decoder design is validated.** Table 4 directly compares parallel vs. cascaded architectures, with cascaded achieving 23.0% vs. 21.5% m.tIoU, supporting the claim that fine-grained spatial features from RoI pooling help temporal localization in long videos.

4. **Competitive on short-form STVG despite architectural shift.** Table 7 shows ART-STVG achieves 59.2/39.2 m.tIoU/m.vIoU on HCSTVG-v2, outperforming most prior methods and trailing TA-STVG by only 1.2/1.0 points. This demonstrates the autoregressive design does not sacrifice short-video performance — a non-trivial property given the different demands of the two settings.

5. **Training with longer videos further amplifies advantage.** Table 6 shows that when all methods are retrained on 40-second videos, ART-STVG reaches 28.3% m.tIoU while the next best (STCAT) reaches only 21.0%.

## Weaknesses

### Fatal
None.

### Major

- **Inference protocol for baseline methods is not specified.** The paper does not describe how non-autoregressive methods (TubeDETR, STCAT, CG-STVG, TA-STVG) — which process all frames simultaneously with full self-attention — were adapted to run on 1–5 minute videos (192–960 frames at 3.2 FPS), which are 3–15× longer than their 64-frame training clips. These methods have no built-in mechanism for variable-length streaming. Without specifying whether frames were subsampled, a sliding window was used, or full-resolution frames were packed into GPU memory, the reported performance gaps (e.g., ART-STVG 23.0 vs. TA-STVG 13.9 on LF-STVG-3min) cannot be fully interpreted as grounding capability differences rather than artifacts of ad-hoc inference adaptation. Reproducibility requires this information. *This is the most significant weakness in the paper.*

### Minor

- **The memory-free baseline already outperforms existing methods, conflating two sources of gain.** On LF-STVG-3min, the baseline (ART-STVG without any memory modules) achieves 16.7 m.tIoU while the best existing method (TA-STVG) achieves 13.9. Since the baseline already has the autoregressive frame-by-frame design, this shows that the architecture alone — before any memory contribution — is sufficient to beat existing approaches. The paper's headline comparisons (ART-STVG vs. prior methods) package autoregressive design gains and memory gains together, and this is not acknowledged or disentangled in the narrative.

- **Spatial memory selection uses a frame-independent criterion.** The selection computes similarity between each spatial memory and the *textual feature*, which is static across all frames. This means the same memories are prioritized regardless of the current frame's temporal context — a tension with the stated motivation ("memories at different moments are not always relevant for target localization in current frame"). A frame-dependent or query-conditioned selection would better align with the claimed goal.

- **Unbounded memory growth without analysis.** The memory bank "update[s] by simply adding the query as a new memory, without removing any existing memories" (line 148). For a 5-minute video at 3.2 FPS with K=6 decoder blocks, this accumulates ~5,760 entries. The paper does not discuss whether inference time, memory usage, or feature staleness become practical concerns as the bank grows.

- **Unselected temporal memory degrades performance without deeper analysis.** Table 2 shows that adding *all* temporal memories drops m.tIoU from 16.7% to 9.6% — a 7.1-point *decrease*. The paper attributes this to "irrelevant information from multiple events" but offers no diagnostic analysis (e.g., attention weight distributions, feature-space visualization, or control experiments isolating the cause). Understanding this degradation would strengthen the core claim about memory selection being essential.

- **Single dataset and limited annotation clarity.** Evaluation is limited to HCSTVG-v2 (multi-person interactions) because it is the only dataset with available source videos. The paper states that extensions are "based on original YouTube videos, not concatenated clips" and were "manually reviewed," but does not clarify how ground-truth annotations were defined for video portions beyond the original 20-second clips — i.e., whether the target event may appear only in the original window or anywhere in the extended video.

### Trivial

None.

## Nice-to-Haves

- Runtime and peak-memory analysis comparing ART-STVG to baselines as memory banks grow.
- Qualitative examples (predicted vs. ground-truth tubes) on long videos to help interpret the modest absolute numbers.
- A control experiment where existing methods receive the same number of input frames as ART-STVG (e.g., by subsampling the long video to a fixed length).

## Removed Points

*The following were raised in the reviews but are removed from the main assessment for the stated reasons:*

- **"Training-test domain shift undermines the comparison"** — Removed because all methods (ART-STVG and baselines) face the identical domain shift (trained on 20s clips, tested on 1–5min videos). The comparison is a level playing field; ART-STVG's advantage reflects genuine capability differences.
- **"Low absolute numbers" (e.g., 4.7% vIoU@0.7)** — Removed. LF-STVG is a new, harder task setting. Relative comparisons are the appropriate benchmark; absolute numbers being modest is expected for pioneering work on an out-of-distribution extension.
- **"Tab. 6 gap is smaller than Tab. 1c"** — Removed. Tab. 6 still shows ART-STVG substantially winning (28.3 vs. ~20.8). This trend is consistent with the paper's claims and is not a weakness.
- **Formatting/style/reproducibility nitpicks** — Removed per instructions (parser artifacts, missing appendix content, etc.).

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis surfaces two observations worth noting: (1) the autoregressive architecture itself (without memory) accounts for a substantial part of the improvement over prior methods, which the paper could acknowledge more explicitly; (2) the text-similarity-based spatial memory selection is frame-independent by construction, which conflicts with the stated motivation of frame-adaptive selection. These are not novel discoveries but useful framing notes.

## Suggestions

1. **Clarify the baseline inference protocol.** For each prior method, state how many frames were fed at once, whether sliding windows or subsampling was used, GPU memory usage, and whether any modifications to the original code were needed to handle longer inputs.
2. **Disentangle sources of improvement.** Add a decomposition showing: (a) baseline (autoregressive without memory) vs. prior methods, (b) baseline + spatial memory only, (c) baseline + temporal memory only, (d) full ART-STVG. This would clarify what each component contributes.
3. **Diagnose the "all memories" failure.** Analyze why temporal memory without selection hurts (e.g., attention weight analysis, feature similarity visualization) to strengthen the motivation for memory selection.
4. **Address spatial memory selection.** Either justify why a frame-independent text-similarity criterion is sufficient, or adopt a frame-dependent selection mechanism.
5. **Discuss memory growth.** Report runtime and memory usage as a function of video length, and consider a capacity limit or eviction policy.
6. **Clarify annotation protocol.** Describe how ground-truth was defined for the extended video portions.

## Score and Decision

### Round 1 — Bracketing

I attempted calibration retrieval across six score bands but the calibration database returned file-not-found errors for all queries. (The tool attempted to access files in `/home/wg25r/split_review_opus_repro/results/2026_deepseek_flash_guideline/snapshot/datasets/deepreview_13k_calibration/` that do not exist.) Consequently, I cannot report anchor papers or compare against retrieved reviews. The score below is based on the paper's content and the submitted reviews alone.

### Final Score Reasoning

The paper makes a genuine contribution: it identifies a real limitation of current STVG benchmarks and methods, proposes a well-motivated architectural response (autoregressive streaming + selective memory + cascaded decoder), and demonstrates across five video lengths that the approach yields growing improvements. The ablations (Tables 2–5) are thorough and support the claimed benefits of each component.

The main weaknesses are: (1) The inference protocol for baselines is not reported, creating a transparency gap — the paper must state how non-autoregressive methods were adapted to long videos. (2) Several minor design issues (frame-independent memory selection, unbounded memory growth, undiagnosed "all memories" degradation) merit attention but do not invalidate the core contribution. (3) Evaluation is limited to one dataset, though this is an acknowledged constraint due to source video availability.

The paper is **not** fatally flawed — the missing inference details are a reporting gap, not evidence of a rigged comparison, and the internal ablations provide supporting evidence for the method's effectiveness independent of the baseline comparisons. However, the transparency issue prevents full confidence in the headline numbers, keeping the paper in the borderline range.

**Score: 6.0** — Borderline accept. The contribution is real and the architecture is sound, but the evaluation reporting gap must be addressed before the results can be fully trusted.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>