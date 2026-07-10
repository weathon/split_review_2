Now I have sufficient calibration data. Let me synthesize the final review.

Based on my calibration analysis:

**Round 1 bracket identification:** The paper's contributions (new task formulation + autoregressive method + extended benchmark + thorough ablations) place it clearly above rejected papers with fundamental task-validity concerns (Motion-Grounded at 5.00) and comparable to accepted papers with solid but not flawless methods (ARLON at 6.25, TRACE at 6.75). The two Major documentation gaps (annotation protocol, prior-methods inference) prevent it from reaching the 7+ range but don't undermine the core contribution.

**Round 2 narrowing:** Comparing item-level favorability ratings:
- My lowest weakness (1.65 for annotation clarity) is less extreme than ARLON's (-0.00) or TRACE's (-1.97), but having two Major-level documentation gaps is more concerning than TRACE's all-minor weaknesses.
- My strengths (9.80, 9.37, 7.79) are competitive with ARLON's (9.31, 9.26, 9.15) and TRACE's (9.09, 8.77).
- This places the paper between ARLON (6.25) and slightly below TRACE (6.75), given the evaluation gaps are more central.

**Final score: 6.0** — a borderline accept reflecting genuine contributions that need evaluation clarification.

---

## Summary
This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), a new problem formulation for localizing targets in videos spanning 1-5+ minutes (vs. the current <1 minute standard). The authors propose ART-STVG, an autoregressive transformer that processes frames sequentially with spatial and temporal memory banks with selective memory retrieval, plus a cascaded spatio-temporal decoder design. They extend the HCSTVG-v2 validation set to create LF-STVG benchmarks at 1-5 minute lengths. ART-STVG consistently outperforms prior methods across all lengths, with a widening gap as videos grow longer, and shows competitive results on short-form STVG.

## Strengths
- **A genuinely underexplored problem.** The paper correctly identifies that existing STVG research is confined to videos under a minute, while real applications (surveillance, retrieval) involve much longer videos. Formulating LF-STVG as a distinct problem is a meaningful step. (Section 1, paragraphs 1-2) [favorability=5.74]
- **The autoregressive frame-by-frame processing is well-motivated for the long-video setting.** Unlike prior methods that attend to all frames simultaneously (incurring quadratic memory cost w.r.t. frame count), ART-STVG processes one frame at a time, making it architecturally suited to videos of arbitrary length. (Figure 1, Section 3.2) [favorability=7.79]
- **Consistent and widening performance advantage over prior methods.** ART-STVG outperforms all prior methods on all five video lengths (1-5 min). The gap grows with video length — from ~0.7% m.tIoU at 1 min to ~7.3% at 5 min — which is precisely what an LF-STVG method should demonstrate. (Table 1, Section 4.1) [favorability=9.37]
- **Ablation evidence for the memory selection is compelling.** Tables 2-3 demonstrate that (a) using all temporal memories hurts performance compared to no memory (m.tIoU drops from 16.7 to 9.6), and (b) memory selection recovers and exceeds the no-memory baseline (23.0). This shows the selection strategy is not merely helpful but necessary — a non-trivial finding. (Section 4.2, Tables 2-3) [favorability=9.80]

## Weaknesses

### Fatal
None.

### Major
1. **Ground-truth annotations for the extended dataset are not described, undermining the evaluation.** The paper creates LF-STVG benchmarks by extending HCSTVG-v2 validation videos from 20 seconds to 1-5 minutes using "original YouTube videos" (line 200). However, it never explains how ground-truth spatio-temporal annotations exist for the extended portions. The original HCSTVG-v2 provides annotations only within its 20-second clips. The closest statement is "we manually review the extended videos to ensure their quality" (line 200), which refers to video quality, not annotation validity. If the annotations are inherited from the original 20-second clip with the rest treated as distractor content (a plausible and common setup), this should be stated explicitly. Without this clarification, the reported metrics cannot be properly interpreted. [favorability=1.65]

2. **How prior methods were adapted to process 1-5 minute videos is not explained, raising fairness questions.** The paper motivates its autoregressive design by arguing that prior methods "process all the video frames in one time" and face "computational bottlenecks because of high GPU memory requirements" (lines 30-31). At 3.2 FPS, a 5-minute video yields ~960 frames, and processing all frames simultaneously with ResNet-101 features would exceed typical GPU memory. Yet Table 1 reports results for TubeDETR, STCAT, CG-STVG, and TA-STVG on all five video lengths. The paper states all methods are "trained exclusively on the HCSTVG-v2 training set" (line 206) but never describes the inference procedure for longer videos. If prior methods were run under degraded settings (e.g., lower frame rate, truncated context) to fit in memory, the comparison is not like-for-like. If they were run at full resolution and frame rate, the GPU memory argument motivating ART-STVG is weakened. [favorability=2.13]

### Minor
3. **The contribution of the autoregressive design itself is not adequately disentangled from the memory components.** The baseline (autoregressive without memory) achieves results competitive with or exceeding prior methods on several longer video lengths (e.g., 16.7 vs 13.9 m.tIoU at 3min; 9.2 vs 7.7 at 5min — though at 4min CG-STVG scores 10.6 vs baseline 9.9). This suggests the autoregressive processing paradigm itself may be a major driver of gains for long videos, yet the paper's narrative focuses primarily on the memory and cascaded design components. While the ablation does compare ART-STVG against the baseline (showing memory helps), there is no discussion of the fact that the baseline architecture alone can already challenge prior methods on longer videos. Cleaner attribution of which gains come from the autoregressive paradigm vs. the memory components would strengthen the paper. [favorability=3.72]

4. **The cascaded vs. parallel decoder ablation (Table 4) is underspecified.** The paper reports that cascaded decoding outperforms parallel decoding by 1.5% m.tIoU, describing the parallel variant as "parallelizing spatial and temporal localization as done in existing approaches" (line 94). However, it is unclear whether "parallel" means (a) two independent decoders with separate queries, (b) the temporal decoder using the same visual features without RoI crops, or (c) some other configuration. The ablation design is not described clearly enough to assess whether the comparison isolates the cascaded connection or confounds it with other architectural changes. [favorability=4.76]

### Trivial
5. **The memory bank grows unboundedly.** The spatial memory bank is updated by "simply adding the query as a new memory, without removing any existing memories" (line 148). Over a 5-minute video at 3.2 FPS this means ~960 entries per decoder layer partition. While the selection mechanism limits attention cost (top N_s=32), the bank itself continues to grow linearly with video length. For hour-long videos (which the paper mentions as motivation), this would become problematic. The paper does not discuss this limitation. [favorability=2.83]

## Nice-to-Haves
- Provide a comparison that isolates the effect of the autoregressive architecture from the memory components (e.g., adapting a prior method to autoregressive processing vs. the full ART-STVG).
- Include a discussion of memory bank growth for very long videos as a practical limitation.

## Removed Points
These points are flagged to be removed; treat them with caution:
- **Loss function in supplementary:** The critic noted the loss function is relegated to supplementary (line 190). Per review rules, weaknesses about content deferred to the supplementary material (which the parser strips) should not be counted against the paper. This is standard practice.
- **Baseline "outperforms all prior methods at 3min+":** The critic claimed the autoregressive baseline "outperforms all prior methods at 3min+". This is factually incorrect at 4min, where the baseline (9.9 m.tIoU) is worse than CG-STVG (10.6) and TA-STVG (10.1). The corrected, more nuanced version is retained as Minor weakness #3.

## Novel Insights
None beyond the paper's own contributions. The review surfaces the observation that the autoregressive architecture itself (even without memory) is competitive with prior methods on longer videos — a point the paper does not discuss — but this stems directly from the paper's own reported numbers.

## Suggestions
1. **Clarify the dataset annotation protocol explicitly.** State whether the extended video portions have ground-truth annotations, and if so, how they were obtained. If the annotations are inherited from the original 20-second clips with the rest treated as distractor content, state this clearly in the main paper.
2. **Describe the inference protocol for prior methods on long videos:** frame sampling rate, whether the entire video was processed at once or in chunks, GPU hardware used, and any memory-saving techniques applied.
3. **Add a brief discussion** comparing the autoregressive baseline against prior methods to clarify what portion of the gains comes from the autoregressive paradigm vs. the memory components.
4. **Clarify the exact implementation** of the "parallel" decoder in the Table 4 ablation.

## Score and Decision

**Anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| tEei1bolt3 (Motion-Grounded) | 5.00 | R1 | Yes | Task+benchmark paper with fundamental task-validity concerns (-5.62 favorability) making it weaker than this paper |
| 14fFV0chUS (TRACE) | 6.75 | R1 | Yes | Video temporal grounding with minor documentation gaps; this paper has more substantial evaluation gaps |
| wkbx7BRAsM (ARVideo Imitator) | 7.00 | R1 | Yes | Strong autoregressive paper with novelty concerns (-3.61); this paper has clearer novelty but larger evaluation gaps |
| 8pusxkLEQO (ARLON) | 6.25 | R2 | Yes | Long video generation with performance concerns; comparable methodology quality but different domain |
| vlg5WRKHxh (F3Set) | 7.00 | R2 | Yes | Benchmark+method with very low favorability items (-2.60, -1.42) but still accepted; shows score variability |
| a1P5kh2oo8 (Vinoground) | 5.75 | R2 | No | Pure benchmark paper, less relevant |
| QETk0lBdVf (Long Context Transfer) | 5.80 | R2 | No | LMM long video, less relevant methodologically |

**Score rationale:** The paper's strengths (high favorability: 9.80, 9.37, 7.79) are comparable to accepted papers at 6.25-6.75, and the contribution (new problem formulation + well-designed method + thorough ablations) is genuine. However, the two Major evaluation documentation gaps — the annotation protocol for the extended dataset and the inference setup for prior methods — are significant enough to prevent the paper from reaching the 7+ range. These are fixable gaps rather than fundamental flaws. The paper sits between ARLON (6.25) and TRACE (6.75), closer to ARLON due to the centrality of the evaluation concerns.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>