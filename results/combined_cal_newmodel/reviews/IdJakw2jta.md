Now I have sufficient calibration data. Let me write the final review.

Based on my analysis:

**Round 1 bracket:** [4.5, 5.5] — The paper is structurally similar to papers scoring 4.5 (LVBench) and 5.75 (ResidualViT). It has stronger contributions than LVBench (method + task, not just benchmark) but comparable dataset documentation issues. Compared to ResidualViT (5.75), it has less thorough evaluation documentation.

**Round 2 narrowing:** Comparing against Motion-Grounded Video Reasoning (5.00) — both introduce new tasks + datasets + methods and have similar underspecification issues. The current paper has stronger empirical breadth (5 benchmarks vs 1) but comparable evaluation documentation gaps.

Let me finalize the review.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
// List only reasonable points. Rank by severity.

### Fatal
None

### Major
- ...

### Minor
- ...

### Trivial
None

## Nice-to-Haves
- ...

## Removed Points
...

## Novel Insights
...

## Suggestions
...

## Score and Decision

Let me write the full review now.

For the favorability comparison - my strongest strength (Memory selection strategies, 11.52) is comparable to the strongest strengths of calibration anchors. My weakest weakness (Cascaded design marginal, -2.13) is worse than most anchor weaknesses (typically -1 to -3 range for the worst ones).

Comparing to Motion-Grounded (5.00):
- My strengths: 7.54 to 11.52
- My weaknesses: -2.13 to 0.56

Motion-Grounded strengths: 10.17 to 13.28
Motion-Grounded weaknesses: -2.57 to 5.55

The current paper's strengths are slightly weaker than Motion-Grounded's best (11.52 vs 13.28), and the weaknesses are comparable (-2.13 vs -2.57).

I'll place the final score at 5.0.

Let me write the review.## Summary

This paper proposes Long-Form Spatio-Temporal Video Grounding (LF-STVG), extending STVG from ~20-second clips to 1-5 minute videos. To address the GPU memory bottleneck that arises when processing thousands of frames simultaneously, the authors introduce ART-STVG, an autoregressive transformer that processes frames one at a time with spatial and temporal memory banks and selective memory retrieval mechanisms. On extended HCSTVG-v2 benchmarks spanning 1–5 minutes, ART-STVG consistently outperforms existing non-autoregressive methods (TubeDETR, STCAT, CG-STVG, TA-STVG) by wide margins, with the gap growing as video length increases.

## Strengths

- **Problem framing is genuine and timely.** The paper correctly identifies that existing STVG benchmarks (HCSTVG-v2 at ~20s, VidSTG at ~35s) are far shorter than real-world videos and proposes LF-STVG as a natural problem extension. This is a real gap and the paper is the first to explicitly formulate it (Sec. 1, lines 15-16).

- **Core architectural choice is well-motivated.** Processing frames autoregressively (one at a time, with memory) instead of all-at-once is a sensible response to the GPU memory bottleneck that would arise from processing thousands of frames simultaneously. This design choice follows directly from the problem constraints (Sec. 1, lines 30-32, Fig. 1).

- **Memory selection strategies are domain-appropriate and empirically validated.** The spatial memory selection (top-k by text similarity) and temporal memory selection (adjacent-frame similarity for event boundary detection) are simple, interpretable, and directly target the stated challenge of irrelevant information in long videos. Ablations (Tab. 2, Tab. 3) show meaningful gains over both no-memory and all-memory baselines (e.g., selective temporal memory improves m.tIoU from 9.6% to 23.0% on 3-min videos).

- **Tab. 6 (training on 40-second videos) provides a partial robustness check.** All methods improve with longer training, and ART-STVG still leads (28.3 vs. 20.8–21.0 m.tIoU), showing the result is not solely an artifact of training-length mismatch.

- **Competitive short-form STVG results (Tab. 7)** demonstrate the method does not sacrifice short-video capability to achieve long-video gains, falling only ~1% behind the SOTA TA-STVG.

## Weaknesses

### Fatal
None.

### Major

- **Baseline inference protocol on long videos is critically underspecified.** The paper states (§4) that all methods are trained on 20-second videos and evaluated on 1–5 minute videos, but never describes how non-autoregressive baselines (TubeDETR, STCAT, CG-STVG, TA-STVG) were adapted for inference on videos 3–15× longer than their training data. At 3.2 FPS, a 5-minute video produces 960 frames, which no practical GPU can process at once for these models. The paper does not specify whether frames were subsampled, videos were chunked into segments, or a sliding window was used. Tab. 6 (training on 40s) partially addresses this but still evaluates on 3-minute videos (4.5× training length) without describing the baseline inference strategy. Without this information, it is difficult to determine whether ART-STVG's advantage reflects genuine architectural superiority or merely the baselines being evaluated under conditions they were never designed for.

- **Dataset extension methodology is critically underspecified.** The paper extends HCSTVG-v2 validation videos from 20 seconds to 1–5 minutes using "original YouTube videos" and reports only that "we manually review the extended videos to ensure their quality" (lines 196-200). No annotation process is described: were the original 20-second ground-truth annotations kept with the extended portions treated as distractor content, or were new annotations created for the full video? No annotation agreement or quality metrics are reported. The extended benchmark is also limited to 2,000 validation samples. Without clarity on how ground-truth spatio-temporal tubes were produced, the benchmark's validity as an evaluation tool is uncertain.

### Minor

- **Low absolute performance is not adequately discussed.** On LF-STVG-5min, ART-STVG achieves m.tIoU = 15.0%, m.vIoU = 10.0%; on LF-STVG-3min, m.tIoU = 23.0%, m.vIoU = 15.3%. While baselines are even lower, the paper does not address whether these numbers indicate the difficulty of LF-STVG as an open problem or what they imply about practical deployment. An honest discussion of the gap between current results and real-world requirements would strengthen the paper.

- **The cascaded vs. parallel decoder improvement is modest** (1.5% m.tIoU, 1.4% m.vIoU in Tab. 4), yet is presented as a core contribution. The "parallel" design comparison also may not fully capture what existing methods actually do, reducing the informativeness of this ablation.

- **Memory bank grows without bound.** The paper states (line 148) that memories are added without removal. For a 5-minute video at 3.2 FPS with K decoder blocks, the bank could hold ~5,760 entries. No discussion of computational cost, forgetting, or pruning is provided.

- **Handling of frames where the target is absent is not discussed.** The spatial decoder predicts a box for every frame — whether this is realistic and how these frames are treated in the loss and evaluation is not addressed.

- **The number of decoder blocks K is used as a structural parameter throughout (§3.3, §3.4) but its numerical value is never specified** in the main paper, which is needed for reproducibility.

### Trivial
None.

## Nice-to-Haves

- Describe how non-autoregressive baselines are adapted for long-video inference (sliding window, chunking, frame sampling) and hold that strategy constant across methods.
- Clarify the dataset construction process: specify whether annotations were re-created or retained from the original 20-second window, and report annotation agreement statistics.
- Add a brief discussion acknowledging the gap between current absolute performance and practical deployment requirements for LF-STVG.

## Removed Points

The following criticisms from the input review are removed per policy:
- **Loss function deferred to supplementary** (removed: appendix content stripped by parser; exists in original submission).
- **Baseline architecture details in supplementary** (removed: same reason).
- **Additional results in supplementary** (removed: same reason).
- **"Option (a) makes task easier" framing** (removed: partially mischaracterizes the task — the model does not know the original 20-second window, so extended distractor content makes the problem harder, not easier. The core underspecification concern is retained in the Major weakness above.)

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Disclose the exact inference protocol used for each baseline on long videos (how many frames were fed per forward pass, sampling strategy, any chunking).
- Document the dataset extension process in detail, including annotation decisions and agreement metrics.
- Add a brief limitations section discussing the gap between current absolute performance and practical deployment.
- Specify the numerical value of K (decoder blocks) and discuss memory bank growth management (pruning, forgetting, or computational cost analysis).
- Clarify how frames without the target object are handled during training and inference.

## Score and Decision

**Calibration anchors used across rounds:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/bEvI30Hb2W.md` (LVM-NET) | 3.00 | R1 | Yes | Both address long-form video with memory, but LVM-NET underperforms baselines while ART-STVG outperforms them; current paper is above 3.0 |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/uHgVrGF2Wn.md` (LVBench) | 4.50 | R1 | Yes | Both have underspecified dataset annotation processes; LVBench is purely a benchmark while current paper adds method + task |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4j9plQoOH1.md` (LongViTU) | 4.75 | R2 | No | Both extend video understanding to longer videos with dataset contributions |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tEei1bolt3.md` (Motion-Grounded) | 5.00 | R2 | Yes | Both introduce new task + dataset + method with similar annotation underspecification; current paper has broader evaluation (5 benchmarks vs 1) |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QWDFOOoV3U.md` (ResidualViT) | 5.75 | R2 | Yes | Both address video grounding with efficiency-motivated architecture; current paper has comparable strengths but more severe evaluation documentation gaps |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wkbx7BRAsM.md` (Autoregressive Transformers) | 7.00 | R1 | Yes | Both use autoregressive transformers for video, but the calibration paper has cleaner evaluation and stronger presentation |

**Round 1 bracket:** [4.5, 5.5]. The paper shares key structural features with Motion-Grounded (5.00) — new task, new dataset, new method, comparable underspecification issues — and sits above LVBench (4.50) because it contributes a method + task formulation, not just a benchmark.

**Favorability comparison:** The paper's strongest items (memory ablation favorability 11.52, Tab. 6 robustness 10.40) are competitive with Motion-Grounded's best (12.64), but its most negative weakness (cascaded design at -2.13) is slightly more negative than Motion-Grounded's worst (-2.57). The two Major weaknesses (baseline inference at 0.56, dataset extension at -0.36) are moderately negative — they signal real documentation gaps but not fatal structural flaws.

**Final score:** 5.0. The paper has genuine contributions (new problem formulation, well-motivated architecture, consistent empirical gains across 5 benchmarks) but the evaluation has significant documentation gaps that prevent proper assessment of the central claim. Both Major weaknesses are addressable in revision.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>