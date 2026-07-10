Now let me compile the final review.

## Summary

This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), extending STVG from videos of ~20–35 seconds to 1–5 minutes. To handle longer videos, the authors propose ART-STVG, an autoregressive transformer that processes frames sequentially with spatial and temporal memory banks augmented by selection strategies. A cascaded decoder design uses spatial predictions to inform temporal grounding. The method is evaluated on five extended benchmarks (LF-STVG-1min through 5min) derived from HCSTVG-v2, outperforming existing STVG methods, and remains competitive on short-form STVG.

## Strengths

- **The problem formulation is genuinely novel and well-motivated (§1).** Existing STVG benchmarks max out at ~35 seconds, while real-world applications demand minutes-to-hours. Formalizing LF-STVG as a distinct evaluation regime is a timely contribution.

- **The autoregressive, frame-by-frame design follows naturally from the problem definition (Figure 1, §3.2).** Processing one frame at a time with memory avoids the GPU memory wall that blocks methods attending to all frames simultaneously — the right design choice for the stated problem.

- **The cascaded spatial→temporal decoder (§3.2) is architecturally clean.** Using the predicted spatial box to crop motion features via RoI pooling before temporal decoding makes temporal grounding conditional on spatial grounding. The ablation in Table 4 confirms it improves over a parallel design (+1.5 m.tIoU).

- **Memory selection strategies are simple, well-motivated, and properly ablated (Tables 2, 3).** The temporal selection (event-boundary detection via adjacent-memory similarity) delivers particularly striking gains: +13.4 m.tIoU from "all memories" to selected memories.

- **Results on the long-form benchmarks show a consistent and widening gap as video length increases (Table 1, Figure 2).** The relative improvement over the best baseline (TA-STVG) grows from ~0.7% m.tIoU at 1 minute to ~7.3% at 5 minutes, consistent with the claim that ART-STVG handles longer videos better.

## Weaknesses

### Major

- **The evaluation protocol for baseline methods on long videos is critically underspecified (Table 1, §4.1).** The paper trains all methods on 20-second videos (64 frames) but evaluates on 1–5 minute videos (192–960 frames). The baselines (TubeDETR, STCAT, CG-STVG, TA-STVG) use DETR-style architectures that attend to all input frames jointly. The paper never describes how these baselines were run on the long videos — whether frames were subsampled to maintain a fixed input length, processed in chunks with aggregation, or given all frames (which would likely cause OOM for the 5-minute case). This makes the central comparison in Table 1 uninterpretable as a fair test: if baselines saw far fewer frames than ART-STVG, the growing gap with video length would be explained by frame coverage rather than architectural advantage. This must be clarified before the paper's main empirical claim can be properly assessed.

### Minor

- **Overstated framing relative to absolute scores.** The paper characterizes results as achieving "excellent performance" (Contributions, line 48), but the absolute numbers are low: 15.0% m.tIoU and 10.0% m.vIoU on 5-minute videos. While outperforming baselines is meaningful and relative gains are substantial (nearly doubling the best baseline at 5 minutes), the practical applicability claimed in the introduction (video retrieval, surveillance) is not supported by these absolute scores. Calibrating the language to the results would strengthen the paper.

- **No computational analysis despite computational motivation (§1, lines 30–31).** The paper motivates ART-STVG partly on computational grounds ("computational bottlenecks because of high GPU memory requirements") but never reports runtime, peak GPU memory, or FLOPs for any method. For a paper whose core architectural argument is about scalability, this is a measurable omission.

- **The spatial memory bank grows without bound (§3.3, line 148).** The update rule adds the query as a new memory "without removing any existing memories." The paper does not discuss memory capacity limits, saturation effects, or a forgetting mechanism. While the selection mechanism limits what is retrieved at inference, the bank itself continues to accumulate over very long videos.

- **Unexplained asymmetry between spatial and temporal memory gains.** Ablations show temporal memory selection provides +13.4 m.tIoU (Table 2, rows ❷→❸) while spatial memory selection provides only +0.9 m.tIoU (Table 3, rows ❷→❸). This asymmetry is not discussed; it could indicate that spatial grounding benefits less from long-range context or that the spatial selection mechanism is weaker.

- **Single-domain evaluation.** Long-form evaluation is conducted only on HCSTVG-v2 (multi-person scenes from movies/TV). The paper acknowledges the availability limitation (§4, lines 196–200) but claims applicability to surveillance and egocentric domains without evidence.

## Nice-to-Haves

- A controlled experiment isolating video length from frame count: evaluate ART-STVG and a representative baseline on 1-minute videos while controlling the number of frames each sees (e.g., both see 64 uniformly sampled frames). This would distinguish architectural advantage from frame-coverage advantage.
- Discussion of the spatial/temporal memory gain asymmetry.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. "Baseline architecture is underspecified and the gap is suspiciously large" — Removed: the paper describes the baseline as "similar to ART-STVG but without memory" in the main text and defers details to supplementary material (which the parser strips). The 13-point gap on short-form STVG is explained by the presence/absence of full memory modules and is not inherently suspicious.
2. "Loss function deferred to supplementary material" — Removed per hard rule: parser strips supplementary sections.
3. "VidSwin not fully autoregressive" — The paper acknowledges this (§3.1, line 78: "previous frames are also used as input"). It is a known design detail.
4. "No failure mode analysis / qualitative examples" — Generic expectation not standard for this setting; the paper does provide attention visualizations (Figures 5, 6).
5. "Single-run results / no variance reported" — Common practice in this benchmark setting; not a distinguishing weakness.
6. "Claim that existing methods cannot be adapted is stated without evidence" — The paper's claim is about the architectural limitation of processing all frames at once, which is supported by the OMM argument. Chunking/scaling counterarguments are speculative.
7. "Table 2 shows all-memories hurt performance" — Already discussed in the paper.

## Novel Insights

None beyond the paper's own contributions. The key synthesis from the review is that the paper's central empirical claim (ART-STVG outperforms baselines increasingly with video length) cannot be fully evaluated without knowing the baseline inference protocol, and this issue should dominate the discussion.

## Suggestions

1. **Disclose the exact evaluation protocol for each baseline on long videos:** how many frames were input, any subsampling/chunking strategy used, and peak GPU memory required. This is the single highest-leverage improvement.
2. Add a controlled experiment isolating video length from frame count.
3. Report runtime and GPU memory for all methods.
4. Tone down "excellent performance" language or contextualize with explicit discussion of benchmark difficulty.

---

**MY FINAL SCORE: <score>6</score>**
**MY FINAL DECISION: <decision>Borderline Accept</decision>**