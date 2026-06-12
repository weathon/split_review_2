## Summary

This paper explores Long-Form Spatio-Temporal Video Grounding (LF-STVG), extending the standard STVG setting from ~20-second clips to 1–5 minute videos. The authors propose ART-STVG, an autoregressive transformer that processes frames sequentially with spatial/temporal memory banks and a cascaded decoder design. They extend the HCSTVG-v2 validation set to create five LF-STVG benchmarks (1–5 minutes) and demonstrate that ART-STVG substantially and consistently outperforms existing non-autoregressive methods, with relative gains growing as video length increases (e.g., 15.0 vs. 7.7–8.1 m.tIoU at 5 minutes).

## Strengths

1. **Well-motivated problem framing with concrete evidence of a real gap.** The paper correctly identifies that existing STVG benchmarks cap out at under one minute, while real-world applications involve much longer videos. The quantitative demonstration that TubeDETR collapses from 32.5 to 7.8 m.tIoU as the video extends from 1 to 5 minutes (Tab. 1) concretely motivates the need for LF-STVG research.

2. **Consistent and large relative improvements across all settings.** ART-STVG outperforms every existing method on all five LF-STVG benchmarks and all metrics. At 3 minutes it achieves 23.0 vs. 13.6–14.2 m.tIoU, and at 5 minutes 15.0 vs. 7.7–8.1 — roughly double the best competitor. The performance gap grows monotonically with video length, which is a clean and non-trivial result that cannot be dismissed as noise.

3. **Well-structured ablations that validate individual components.** The temporal memory selection ablation (Tab. 2) is especially informative: using all memories *hurts* (16.7→9.6 m.tIoU), while selective memory recovers and improves beyond the no-memory baseline (9.6→23.0). The cascaded vs. parallel decoder ablation (Tab. 4) and the spatial memory selection ablation (Tab. 3) are similarly clean and convincing.

## Weaknesses

### Fatal
None.

### Major
- **The evaluation protocol tests short-to-long generalization, not matched-length capability.** All methods (including ART-STVG) are trained exclusively on the HCSTVG-v2 training set (average length 20 seconds) and evaluated on 1–5 minute videos (lines 206–207). While this is a meaningful generalization test, it does not demonstrate that ART-STVG learns from or handles long-form videos when trained on similar-length data. Tab. 6 provides partial mitigation by training on 40-second videos, but even this is much shorter than the 3-minute test set. The conclusion's claim that ART-STVG "can handle long-term videos effectively" (line 333) overstates what the current evidence supports — the evidence shows a clear *generalization advantage*, not necessarily a *long-form learning capability*. The authors should either provide matched-length training experiments (e.g., training on 1–2 minute videos and testing on comparable lengths) or recalibrate their claims accordingly. This is the paper's most significant gap.

### Minor
- **Low absolute performance is not discussed.** On LF-STVG-5min, ART-STVG achieves only 15.0 m.tIoU and 10.0 m.vIoU; at 4 and 5 minutes, vIoU@0.7 is around 5%. While relative comparisons are favorable, the paper does not acknowledge or contextualize what these low absolute numbers mean for practical LF-STVG. A discussion of whether the bottleneck is the evaluation metric, annotation quality, task difficulty, or model capability would strengthen the paper.

- **Dataset extension documentation is underspecified.** The LF-STVG benchmarks extend only the HCSTVG-v2 validation set (2,000 pairs) to 1–5 minutes. The paper states that extensions are "based on original YouTube videos, not concatenated clips" and are "manually reviewed" (line 200), but it does not specify: (a) the manual review protocol, (b) whether queries were checked for validity in the longer videos (a query written for a 20-second clip may not uniquely describe an event in a 5-minute video), (c) whether new spatial/temporal annotations were created or original labels were projected, or (d) inter-annotator agreement if new annotations were created. Since the benchmarks are a key contribution, these details are needed for reproducibility and quality assessment.

- **Memory bank growth is unbounded.** The memory bank update rule "simply adds the query as a new memory, without removing any existing memories" (line 148). For 5-minute videos at 3.2 FPS (~960 frames), the memory bank grows without bound. The selection mechanism (top-*N_s* for spatial, event-closest for temporal) limits retrieval cost but not storage. No maximum size or forgetting mechanism is specified.

- **Loss function details deferred to supplementary.** Section 3.5 defers the loss description entirely to the supplementary material. While space-constrained, stating which losses are used (e.g., L1 + GIoU for boxes, BCE for start/end probabilities) in the main text is standard and expected.

### Trivial
- The motion backbone (VidSwin) is kept frozen during training (line 194). This is a consequential design choice that is not ablated.
- No GPU memory measurements are reported to substantiate the claimed computational bottleneck of existing methods on long videos (lines 30–31).

## Nice-to-Haves
- Training on matched-length videos (even 1–2 minutes) would substantially strengthen the paper's core claims.
- Extending VidSTG to LF-STVG, if source videos are available, would broaden the benchmark's coverage.

## Removed Points

These points are flagged to be removed, treat them with caution.

- **"Baseline is underspecified and appears unfairly weak"** — REMOVED. The baseline (autoregressive without memory) underperforms existing methods on *short* videos (1 min: 30.1 vs. 32.5–38.4), which is expected: processing one frame at a time without history is inherently disadvantaged compared to seeing the full clip at once. On *longer* videos (3–5 min), the baseline actually outperforms existing methods (16.7 vs. 13.6–14.2), showing the autoregressive paradigm itself helps for long videos. The baseline serves its intended ablation purpose; its weakness relative to batch methods on short videos does not inflate ART-STVG's contribution.

- **"Processing all frames in one time is imprecise"** — REMOVED. The paper's description is standard for the field. Existing STVG methods (DETR-based) do process the entire video's feature sequence in one forward pass during inference.

- **"No results on VidSTG"** — REMOVED. The paper explicitly explains (line 200) that HCSTVG-v2 is the only dataset providing available source videos for extension, making this a dataset constraint, not an oversight.

- **"Autoregressive design forces fixed frame rate"** — REMOVED. All compared methods use a fixed frame rate; this is a design choice, not a specific weakness of this paper.

- **"No error bars reported"** — REMOVED. Single-run evaluation without error bars is standard practice in the STVG literature.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Provide at least one matched-length training experiment (e.g., train on 1-minute or 2-minute videos and test at the same length). This would directly address the paper's most significant weakness.
2. Expand the dataset documentation: describe the manual review protocol, explain how query validity was checked for longer videos, report whether new annotations were created, and provide frame-level target-presence statistics.
3. Add a brief discussion of the low absolute performance numbers and what they imply for the LF-STVG task.
4. State the loss functions (L1 + GIoU for boxes, BCE for start/end probabilities) in the main text.
5. Specify a practical maximum memory bank size or a forgetting mechanism for arbitrary-length videos.

**Calibration Anchors (retrieved across all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `u1cQYxRI1H.md` (Diffusion illumination) | 0.50 | R1 strong-reject | Irrelevant topic; very weak paper |
| `gwZ90hFSL2.md` (Humanoid robots NLP) | 1.00 | R1 strong-reject | Irrelevant topic; very weak paper |
| `YGWxpOI6Y0.md` (VideoGPT+) | 3.40 | R1 reject | Video understanding with temporal limitations; less well-motivated than our paper |
| `ICR3swcnaa.md` (STD-Former) | 3.00 | R1 reject | Action recognition paper with weaker experiments than our paper |
| `xYzOkOGD96.md` (Grounded Video Caption) | 3.83 | R1 borderline-reject | Introduces new task+benchmark+model like our paper, but criticized for overclaiming novelty and incomplete baselines |
| `YCwN7wQA6W.md` (Grounded-VideoLLM) | 4.25 | R1 borderline-reject | Video-LLM temporal grounding; criticized for limited novelty, while ART-STVG has cleaner novelty |
| `tEei1bolt3.md` (Motion-Grounded Video Reasoning) | 5.00 | R1 borderline-reject | Motion grounding task with dataset; comparable structure to our paper |
| `IryGDUHxDE.md` (Unsupervised action recognition) | 5.25 | R1 borderline-reject | Autoregressive video model; reasonable contribution with limitations |
| `14fFV0chUS.md` (TRACE) | 6.75 | R1 borderline-accept | Stronger paper — VTG with causal event modeling; cleaner evaluation and no training-test mismatch issue |
| `a1P5kh2oo8.md` (Vinoground) | 5.75 | R1 borderline-accept | Temporal reasoning benchmark; solid contribution |
| `QETk0lBdVf.md` (Long Context Transfer) | 5.80 | R1 borderline-accept | Long video LMM; comparable scope but stronger experiments |
| `9Cu8MRmhq2.md` (Multi-granularity Correspondence) | 8.00 | R1 accept | Top-tier paper on long video-language learning; stronger evaluation than our paper |

**Round 1 bracket:** 4.5 – 6.5 (based on comparison with Grounded Video Captioning at 3.83 with a similar new-task+dataset+model structure but cleaner novelty, and TRACE at 6.75 which has no training-test mismatch issue).

**Final narrowing:** The paper's main gap (no matched-length training experiments) prevents it from reaching the 6+ borderline-accept range where papers like TRACE (6.75) sit with cleaner evaluations. However, the paper's contribution (new problem formulation, benchmark, and a method with convincing relative gains and ablations) places it clearly above the 3–4 reject range of Grounded Video Captioning (3.83) and Grounded-VideoLLM (4.25), which have more significant novelty concerns. The appropriate score is **5.5**.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>