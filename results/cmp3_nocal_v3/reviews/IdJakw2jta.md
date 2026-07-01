Now I have all the evidence I need. Here is the final consolidated review.

---

## Summary

This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), a new problem setting targeting videos that span minutes rather than seconds. To address it, the authors propose ART-STVG, an autoregressive transformer that processes frames sequentially with two memory banks (spatial and temporal) equipped with selective retrieval strategies, plus a cascaded decoder that uses spatial outputs to guide temporal localization. On five extended benchmarks (1–5 min), ART-STVG consistently outperforms existing methods, with the performance gap growing on longer videos.

## Strengths

1. **Problem framing is genuinely motivated and timely.** The paper identifies a real and well-defined gap: existing STVG research operates on videos <1 minute, while real applications routinely involve minutes or hours (Section 1). This gap is quantified (HCSTVG-v2 averages 20s, VidSTG averages 35s), and the argument that processing all frames at once does not scale to long videos is supported both conceptually and via the GPU memory bottleneck noted in Section 1.

2. **The autoregressive design follows naturally from the problem analysis.** Treating the video as a streaming input (Section 3.2) sidesteps the quadratic memory scaling that would afflict DETR-style approaches on long videos. This architectural choice is a coherent consequence of the task definition rather than an arbitrary addition.

3. **Memory selection strategies are well-motivated and convincingly ablated.** The paper correctly identifies that not all historical frames are equally relevant (Sections 3.3–3.4). The ablation in Table 2 is particularly compelling: adding all temporal memories *hurts* performance (16.7→9.6 m.tIoU), while selective retrieval sharply recovers and exceeds it (9.6→23.0), cleanly isolating the selection mechanism as essential.

4. **Results are consistently positive across all five long-form benchmarks.** ART-STVG outperforms all baselines at every video length (Table 1), and the gap grows with video duration — exactly the trend expected from a method designed for long-form video. On LF-STVG-5min, ART-STVG's m.tIoU (15.0) is nearly double that of the best existing method (8.1).

5. **The cascaded decoder design is ablated cleanly.** Table 4 shows a 1.5% m.tIoU gain from cascaded over parallel, with a consistent direction across metrics. The motivation (spatial cues aiding temporal localization in long, complex videos) is sensible and the evidence supports it.

## Weaknesses

### Fatal
None.

### Major

1. **Missing inference protocol for baselines on long videos threatens the main comparison.** The paper does not describe how existing STVG methods (designed and trained for 64-frame clips) were adapted to process 1–5 minute videos at inference time. Several plausible setups exist (aggressive subsampling to 64 frames, sliding-window aggregation, lower frame rate), with very different implications. If baselines were forced to discard ~89% of frames while ART-STVG processes all frames, the comparison conflates architectural advantage with an asymmetric information advantage. The paper states only that "all methods are trained on the HCSTVG-v2 training set" (Section 4.1) — this concerns training, not inference. The silence on inference protocol is the most significant gap in the experimental section and directly affects the central claims of Table 1.

### Minor

2. **Training/evaluation domain gap is acknowledged but underexplored.** All methods in Table 1 are trained on 20-second clips and evaluated on 1–5 minute videos, testing domain generalization rather than in-distribution performance. Table 6 (training on 40-second videos) partially addresses this and shows ART-STVG still leads. However, 40 seconds remains far from 5 minutes, and the paper does not discuss whether the trend would extrapolate if all methods were trained on full-length videos.

3. **LF-STVG benchmark construction is insufficiently documented.** The paper states benchmarks were "extended to 1 to 5 minutes" and "manually reviewed" (Section 4), but omits: (a) the exact number of videos per benchmark length, (b) how the original 20-second ground-truth annotations were mapped onto the longer videos, (c) what constitutes ground truth for portions outside the original annotation window, and (d) the number of annotators and quality criteria. Since these benchmarks are the sole evaluation platform for the paper's central claims, fuller documentation is needed for reproducibility and validity assessment.

4. **GPU memory — a key motivation — is never measured.** The paper repeatedly motivates the autoregressive approach via the "high GPU memory requirements" of processing all frames at once (Section 1). Yet the experiments never report GPU memory usage or compare it across methods. This rhetorical claim appears in the motivation but is never verified empirically.

5. **Temporal memory selection threshold is not specified.** The method detects event boundaries where adjacent-frame similarities are "lower" (Section 3.4), but does not specify whether a fixed threshold, relative threshold, or local-minima detection scheme is used. This detail is needed for reproducibility.

6. **Memory bank capacity and eviction are not discussed.** The spatial memory grows unboundedly: "adding the query as a new memory, without removing any existing memories" (Section 3.3). For a 5-minute video with K=6 decoder blocks, this accumulates ~5,760 memories. The paper does not address whether this causes retrieval degradation or memory overhead, or whether an eviction policy is needed for hour-scale videos.

## Nice-to-Haves

- **Discuss absolute performance in context.** On LF-STVG-5min, even ART-STVG achieves only 15.0 m.tIoU. Adding a brief discussion of what these absolute numbers mean for practical applicability would strengthen the paper, especially given the "real-world applications" framing in Section 1.
- **Report variance or statistical significance.** Single-run reporting is the norm in this field, but given the low absolute numbers, confidence intervals or significance tests would add confidence.
- **Clarify why the spatial query is re-initialized to zeros each frame** rather than carried forward (Section 3.3). The paper could explain how the memory bank alone suffices for temporal context.

## Removed Points

These points were flagged in the input review but removed after cross-checking against the paper or per review guidelines:

- **Loss function deferred to supplementary** and **baseline architecture in supplementary**: Removed per the guideline that the parser strips appendix content from all papers; these exist in the original submission.
- **Spatial query re-initialized to zeros as a flaw**: Removed — this is an intentional design choice; the autoregressive context is conveyed through the memory bank rather than a carried-forward query, which is a valid architectural decision.
- **"No variance reporting" as a weakness**: Downgraded to Nice-to-Have — single-run reporting is standard practice in STVG publications.
- **"Absolute performance very low" as a weakness**: Moved to Nice-to-Have — the paper's contribution is solving a new harder problem and demonstrating relative gains; low absolute numbers reflect task difficulty, not a methodological flaw. The reviewer's valid point about contextualizing numbers is kept as a suggestion.
- **"Equation (1) token count ~5200" concern**: Removed — the paper's self-attention encoder handles this implicitly; the reviewer's speculation about computational cost is not a verified problem.
- **Pure formatting/style nitpicks and speculation about "not yet released" models**: Removed per guidelines.

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis surfaces the severity of the inference-protocol gap and the benchmark documentation deficit, but does not reveal a structural flaw with the method that the paper itself fails to recognize.

## Suggestions

1. **Clarify the baseline inference protocol.** Describe in one paragraph how each existing method was adapted to process 1–5 minute videos at test time — frame sampling rate, any architectural modifications, any post-processing for aggregation. If sliding windows were used, specify window size, stride, and how window-level predictions were fused.
2. **Report GPU memory usage** for ART-STVG vs. baselines on videos of varying lengths to directly support the computational-bottleneck motivation.
3. **Provide fuller LF-STVG benchmark documentation** — number of videos per length, annotation adaptation procedure, annotator count, and quality criteria.
4. **Specify the event-boundary detection criterion** for temporal memory selection.
5. **Discuss the unbounded memory growth** and whether any practical eviction or capacity limit is needed for hour-scale videos.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>