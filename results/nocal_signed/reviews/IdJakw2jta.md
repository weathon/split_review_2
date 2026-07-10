## Summary

This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), extending the standard STVG task from ~20-second clips to 1–5 minute videos. The authors propose ART-STVG, an autoregressive transformer that processes frames sequentially with spatial and temporal memory banks that use selection mechanisms to retain relevant context. A cascaded spatial→temporal decoder design is also introduced. The paper extends the HCSTVG-v2 validation set to create LF-STVG benchmarks at five lengths (1–5 minutes). ART-STVG substantially outperforms existing methods on LF-STVG while remaining competitive on short-form STVG.

## Strengths

- **Well-motivated problem and first formalization of LF-STVG.** The paper correctly identifies that existing STVG benchmarks (20–35 seconds) are far shorter than real-world videos, and it is the first to formally define and tackle the long-form variant. (Section 1)

- **Principled autoregressive design with effective memory mechanisms.** Processing frames sequentially is a natural fit for long videos, avoiding the GPU-memory bottleneck of all-at-once methods. The spatial and temporal memory banks with selection mechanisms cleanly retain relevant context, and the cascaded spatial→temporal decoder is a non-trivial architectural contribution (+1.5% m.tIoU over a parallel design, Tab. 4).

- **Valuable dataset extension.** The LF-STVG-1min through LF-STVG-5min benchmarks are built from original YouTube videos (not concatenated clips), filling a genuine evaluation gap and enabling future work. (Section 4)

- **Informative ablation studies.** Tab. 2 cleanly demonstrates that using all temporal memories *hurts* performance (16.7→9.6 m.tIoU) while selective recovery surpasses the baseline (23.0), validating the core claim about non-trivial memory selection. Tabs. 3–5 similarly isolate each component's contribution.

## Weaknesses

### Major

- **Baseline inference protocol on long videos is not specified.** The paper's central evaluation (Tab. 1) compares ART-STVG against TubeDETR, STCAT, CG-STVG, and TA-STVG on 1–5 minute videos. These methods process all frames simultaneously and are designed for ~20-second clips. How they were adapted to handle ~960 frames (5 min at 3.2 FPS) — via frame subsampling, sliding windows, or some other strategy — is not described. The growing advantage of ART-STVG as videos lengthen (+0.7% m.tIoU on 1-min to +7.3% on 5-min over TA-STVG) is consistent with the hypothesis that existing methods degrade because they cannot process the full video, not necessarily because ART-STVG has better per-frame localization. While the 40-second training experiment (Tab. 6) provides converging evidence, the omission makes the main comparison less interpretable than it should be.

### Minor

- **Low absolute performance not discussed.** On 5-minute videos, even ART-STVG achieves only 15.0% m.tIoU, and baselines are at 7.7–8.1%. The paper focuses on *relative* improvements but does not discuss what this means for task feasibility, provide an oracle baseline (e.g., training on full-length videos), or include an error analysis. The 40-second training experiment (Tab. 6) partially addresses this but stops short.

- **Train-test memory bank size gap not discussed.** ART-STVG is trained with memory banks of at most 64 entries (N\_f=64 frames) but tested with banks accumulating up to ~960 entries (5-minute video). While the selection mechanism picks top N\_s=32, the selection pool grows 15× beyond the training distribution. The paper does not discuss whether this distribution shift might affect memory selection quality.

### Trivial

- **No variance estimates or significance tests.** Given the 2,000-sample validation set, some reported differences (e.g., 38.4 vs. 39.1 m.tIoU on LF-STVG-1min) may not be statistically significant.

## Nice-to-Haves

- Training ART-STVG on longer videos (e.g., 1–2 minute clips) to more directly validate the claim that it is specifically designed for and benefits from longer training.
- Reporting the fraction of test videos with any correct localization (vIoU>0 or tIoU>0) to help interpret the low absolute numbers.
- Adding a sliding-window adaptation for baseline methods to produce a more controlled comparison.

## Removed Points

Points from the input review that were filtered out with justifications:

1. **Feature fusion nitpick (Section 3.1):** The critic questioned why cross-attention wasn't used instead of concatenation+self-attention. This is a standard approach in prior STVG work; removed as a trivial design-choice nitpick.
2. **SF-STVG results behind TA-STVG:** The paper acknowledges being "competitive" on short-form STVG (59.2 vs 60.4 m.tIoU). Since the paper's focus is long-form STVG, being marginally behind SOTA on short-form is not a weakness — removed as scope-creep.
3. **Baseline having same autoregressive architecture:** The critic flags that the "Baseline" row shares ART-STVG's autoregressive design. This is by design — it is an ablation isolating the memory contribution. Removed as a misunderstanding of the experimental design.
4. Various speculative concerns subsumed by the documented major weakness about the unspecified inference protocol.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Specify how each baseline method was adapted for long-video inference (frame sampling rate, any subsampling or windowing strategy) to make Tab. 1 fully interpretable.
- Add a discussion of the train-test memory bank size gap and why the selection mechanism is expected to generalize (or acknowledge the limitation).
- Consider including variance estimates for the main results.

## Score and Decision

The paper tackles an important and underexplored problem with a well-motivated architecture, strong ablations, and a useful dataset extension. The one significant gap — the unspecified baseline inference protocol — is addressable and does not invalidate the core architectural or dataset contributions. The strengths decisively outweigh the weaknesses.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>