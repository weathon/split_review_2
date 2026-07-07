Now I have everything I need. Let me produce the final consolidated review.

---

## Summary

This paper introduces ART-STVG, an autoregressive transformer for spatio-temporal video grounding (STVG) in long-form videos (1–5 minutes), addressing the limitation that existing STVG methods process all frames simultaneously and cannot scale to longer videos. The model processes frames sequentially with memory-augmented spatial and temporal decoders that employ selective memory mechanisms (text-guided for spatial, TextTiling-inspired boundary detection for temporal) and a cascaded decoder design. The authors extend the HCSTVG-v2 validation set to create LF-STVG-1min through 5min benchmarks. ART-STVG substantially outperforms prior methods on these benchmarks while remaining competitive on short-form STVG.

## Strengths

- **Problem framing is well-motivated (Sec. 1).** Existing STVG benchmarks top out at ~35 seconds, and the paper correctly identifies that current methods processing all frames simultaneously face fundamental scaling issues — both computational (GPU memory) and informational (excessive irrelevant content) — as video length grows. The need for a new paradigm is clearly argued.

- **The temporal memory selection mechanism is empirically crucial and well-demonstrated (Tab. 2).** Using all temporal memories hurts performance (16.7→9.6 m.tIoU) while the proposed TextTiling-inspired selection recovers and surpasses it (9.6→23.0) — a 13.4-point gain that strongly validates the design and shows that naive memory accumulation is harmful in long videos.

- **ART-STVG achieves significant and widening margins over existing methods on LF-STVG (Tab. 1).** The gap grows from ~1–7 points on 1-minute videos to ~7–8 points on 5-minute videos, consistent with the claim that the autoregressive design is better suited to longer videos. The method also shows competitive performance on short-form STVG (Tab. 7: 59.2 m.tIoU vs. 60.4 for the SOTA TA-STVG).

- **The cascaded spatio-temporal decoder is ablated and delivers consistent improvements (Tab. 4: +1.5 m.tIoU, +1.4 m.vIoU over parallel design),** showing a clear benefit from using fine-grained spatial target information to assist temporal localization.

- **Multiple ablation studies (Tabs. 2–6) systematically isolate the contributions** of temporal memory selection, spatial memory selection, decoder design, the number of selected memories, and training video length, providing a thorough understanding of what drives performance.

## Weaknesses

### Major

- **The paper never specifies how existing STVG methods (TubeDETR, STCAT, CG-STVG, TA-STVG) were adapted for inference on 1–5 minute videos.** These methods process all frames simultaneously and were designed for ~20-second videos (~64 frames at 3.2 FPS). A 5-minute video at the same FPS contains ~960 frames — no existing STVG method can process this in a single forward pass on a single GPU. The paper states only that "all methods including ART-STVG are trained exclusively on the HCSTVG-v2 training set" (Sec. 4.1) but says nothing about the inference protocol. Whether baselines were subsampled, chunked into windows with aggregated predictions, or otherwise adapted fundamentally affects the comparison. Without this information, the reader cannot assess whether the reported improvements reflect genuine architectural superiority or an artifact of how the baselines were (or were not) able to operate at these video lengths. **This must be clarified for the experimental results to be properly interpretable.**

- **The temporal grounding procedure is incompletely specified.** Sec. 3.2 describes that the temporal head outputs per-frame start probabilities h_i^s and end probabilities h_i^e (h_i ∈ ℝ²), but never specifies how these per-frame predictions are converted to a single video-level time interval [t̂_start, t̂_end] for computing tIoU. Standard approaches (thresholding, argmax over start/end pairs, or some aggregation) are not discussed. The metrics section (Sec. 4) defers to prior work for metric definitions, but the conversion from per-frame outputs to a video-level interval is a method-specific design choice, not a metric definition. This gap matters because m.tIoU depends critically on where the temporal boundaries are placed, and the method description is incomplete without this information.

### Minor

- **The evaluation is confined to a single source dataset (HCSTVG-v2).** While the paper explains that HCSTVG-v2 is "the only dataset which provides available source videos" (Sec. 4), all five LF-STVG benchmarks derive from the same 2,000 validation samples from one domain (complex multi-person scenes). Cross-dataset evaluation (e.g., extending another benchmark or collecting new long-form annotations) would substantially strengthen the contribution, though the practical constraint is acknowledged.

- **The spatial memory selection yields only marginal improvements.** Tab. 3 shows that using all spatial memories gives +0.8 m.tIoU over no spatial memory, and the selection strategy adds only +0.9 more (22.1→23.0). The paper treats both selection strategies as a single contribution, but the spatial selection component is empirically weak compared to the temporal selection (13.4-point gain). The spatial memory selection's contribution would benefit from a more measured characterization.

- **The baseline (ART-STVG without memory or selection) already outperforms existing SOTA on LF-STVG-3min (16.7 vs. 14.2 m.tIoU) and LF-STVG-5min (9.2 vs. 8.1 m.tIoU)** — Tab. 1. This suggests that a substantial portion of the improvement comes from the autoregressive paradigm itself rather than the memory mechanisms. The paper reports this but does not discuss its implications for what the core contribution is. It also somewhat undercuts the narrative that existing methods "fail" on long videos in absolute terms, since even the baseline autoregressive model helps.

- **The memory bank grows without removal** ("without removing any existing memories," Sec. 3.3). For a 5-minute video at 3.2 FPS with K=6 decoder blocks, the spatial memory bank could reach 960×6 = 5,760 entries. The paper does not discuss whether this causes computational or attention saturation issues in practice, nor how the selection mechanism's computational cost scales with bank size.

### Trivial

None.

## Nice-to-Haves

- An analysis of failure modes (e.g., does temporal grounding fail because event boundaries are misidentified, or because spatial localization loses the target mid-video?) would deepen the contribution and point to improvement directions.
- Reporting inference time and GPU memory usage would strengthen the computational motivation, since efficiency is part of the paper's argument for the autoregressive design.
- A few qualitative prediction examples (beyond attention maps) would help readers interpret what a 23% m.tIoU score means in practice.

## Removed Points

These points are flagged to be removed; treat them with caution:
- **Missing loss function specification** — The paper defers to supplementary material (Sec. 3.5). The parser strips supplementary sections from all papers; this content exists in the original submission.
- **Missing inference time / GPU memory reporting** — A valid nice-to-have but not a core weakness.
- **VidSwin temporal window concern** — Very minor implementation detail that does not affect the paper's claims.
- **Absolute claims in abstract should be "tempered"** — Not a substantive criticism; claims are appropriate for the results shown.
- **Training-on-short-clips concern** — The paper frames this as testing generalization and provides a separate experiment with longer training (Tab. 6). This is a methodological choice, not a weakness.
- **Lack of qualitative prediction examples** — Nice-to-have, not a weakness.
- **Strengthening suggestions about failure mode analysis** — Already captured as a nice-to-have.

## Novel Insights

Beyond the paper's own contributions, the most interesting observation from the cross-review is that the baseline (autoregressive architecture without any memory mechanisms) itself substantially outperforms existing SOTA on longer videos (e.g., 16.7 vs. 14.2 on 3min). This suggests that the paradigm shift from parallel to autoregressive processing accounts for a significant portion of the gains, independent of the memory innovations. The paper's own ablation isolates the memory contribution at roughly +6–7 points on 3-minute videos, but the baseline's lead over prior art (~2.5 points) indicates that the processing paradigm itself is a meaningful design choice for long-form video. This nuance could be more explicitly discussed to sharpen the paper's technical contribution.

## Suggestions

1. **Disclose the baseline inference protocol in full.** Explain exactly how each prior method was run on 1–5 minute videos — how many frames were fed, whether subsampling/chunking/aggregation was used, and what GPU hardware was employed. This is the single most important clarification.
2. **Specify how per-frame start/end probabilities are converted to a video-level temporal interval.** This is a straightforward addition (thresholding, argmax, or learned prediction) but essential for reproducibility.
3. **Add a brief discussion of the baseline's strong performance without memory** — acknowledging that the autoregressive paradigm itself contributes meaningfully to long-video grounding would make the contribution framing more precise.
4. **Include a runtime/memory comparison** showing that ART-STVG's sequential processing is practically feasible on the long videos it targets.

## Score and Decision

**Calibration anchors used:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bEvI30Hb2W.md` (LVM-NET, avg 3.00, Round 1, itemized): Long-form video reasoning with memory. Compared to our paper: weaker empirical results, novelty concerns, and limited benchmarks. Our paper is stronger across all dimensions.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1DEHVMDBaO.md` (Adaptive Memory Mechanism, avg 4.60, Round 1, itemized): Long-form video with memory bank. Compared to our paper: marginal improvements over baselines, limited benchmarks, weaker novelty. Our paper has larger gains and better ablations.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Ze49bGd4ON.md` (SAM2Long, avg 5.25, Round 1, itemized): Long video segmentation with memory tree. Compared to our paper: heuristic engineering concerns, incomplete ablation. Our paper has more complete ablations and clearer innovation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/yHj6EunfVQ.md` (CoSPaL WSTVG, avg 5.50, Round 2, itemized): Weakly supervised STVG. Compared to our paper: comparable empirical strength but our paper has clearer technical novelty and more thorough ablations.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/14fFV0chUS.md` (TRACE, avg 6.75, Round 1/2, itemized): Video temporal grounding with LLMs. Compared to our paper: more polished presentation and multiple benchmarks, but addresses a different (temporal-only) sub-problem and uses LLMs. Our paper has stronger direct empirical margins but more missing-detail issues.

**Weighted-item comparison:** Our draft's strongest positive items (temporal memory selection +5.15, significant margins +4.82, cascaded design +4.54) outweigh those of the 3.0–5.25 anchors, whose heaviest weaknesses include very negative items (-7.08, -9.40, -10.68). Our two major weaknesses (-3.88, -3.06) are substantial but are about missing details rather than invalid claims. The Adaptive Memory anchor (4.60) had far more negative weight density. The 5.50 WSTVG anchor had comparable positive weights but also heavy negative weights from novelty concerns. Our paper's positive-to-negative weight ratio supports a score between 5.5 and 6.5.

**Final bracket:** 5.5–6.5 → narrowed to **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>