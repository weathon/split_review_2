Now I have good calibration anchors. Let me synthesize and write the final review.

**Calibration summary:**

| Anchor | Avg Score | Topic | Comparison |
|--------|-----------|-------|------------|
| Adaptive Memory (1DEHVMDBaO) | 4.60 | Long-form video + memory | Similar topic. The current paper has larger relative improvements, clearer ablations, and a new task formulation — stronger in these respects. But the training/evaluation confound is a weakness this anchor doesn't have. My paper sits above this anchor. |
| SAM2Long (Ze49bGd4ON) | 5.25 | Long video + memory selection | Different task (VOS vs. STVG). SAM2Long's improvements are cleaner (training-free, apples-to-apples vs SAM2). My paper's evaluation confound makes it weaker on rigor. I place mine slightly below this anchor. |
| Motion-Grounded (tEei1bolt3) | 5.00 | New spatio-temporal grounding task | Most structurally similar: new task formulation + dataset + baseline. That paper's dataset is more thorough. Mine has weaker evaluation. Comparable at ~5.0. |
| ResidualViT (QWDFOOoV3U) | 5.75 | Temporal video grounding + efficiency | Higher efficiency contribution but limited to zero-shot setting. My paper has a different contribution profile. Not directly comparable. |

**Bracket from Round 1:** The paper sits between 4.60 (Adaptive Memory) and 5.25 (SAM2Long), with the closest structural match being Motion-Grounded (5.00).

**Weighted-item comparison:** My draft's strongest positive items (relative improvements trend at 9.58, memory selection ablation at 8.40) compare well against the anchors' top strengths. However, my paper's `-0.85` weakness (training regime mismatch) is a heavier drag than any single weakness in the Motion-Grounded anchor (where even the -5.62 novelty concern is offset by very high-strength weights like 12.09). The SAM2Long anchor's lowest-weight weakness (-4.40) is similarly serious but its top strength (8.69+9.14) is also stronger. This places the paper in the 4.5–5.5 band, with a final score of 5.0 being the most defensible — above the Adaptive Memory paper (4.60) due to clearer contributions and stronger trend evidence, but below SAM2Long (5.25) and comparable to Motion-Grounded (5.00) due to the evaluation confound.

Now let me assemble the final review.

**Regarding Issue 1 (training regime mismatch):** I need to verify one more time. The paper says "all methods including ART-STVG are trained exclusively on the HCSTVG-v2 training set (average video length 20 seconds) for fair comparison" (line 206). Then Tab. 6 shows training on 40-second videos. Let me verify the 40-second vs 3min mismatch. 40s to 3min... 40s is 0.67 min, so 3min/0.67min ≈ 4.5×. The critic said "40s → 3min is still a 4.5× length mismatch." Let me recalculate: 3 minutes = 180 seconds. 40 seconds → 180 seconds = 4.5×. Yes, the critic is correct.

Wait, but all methods including existing ones are also trained on 40s in Tab. 6. So the comparison is fair within Tab. 6 — they all get the same extended training. And ART-STVG still outperforms. But the existing methods in Tab. 1 (trained on 20s, tested on 1-5min) is the unfair comparison. The paper says this is "for fair comparison" which is misleading — it IS uniform, but it disadvantages methods never designed for such extrapolation.

Let me also verify: does the baseline (ours) consistently outperform existing methods on 3min+? Tab. 1(c): Baseline=16.7 vs best existing=14.2 (CG-STVG). Tab. 1(d): Baseline=9.9 vs best existing=10.6 (CG-STVG). Actually on 4min, CG-STVG (10.6) beats the baseline (9.9). Tab. 1(e): Baseline=9.2 vs best existing=8.1 (CG-STVG). So the baseline beats existing methods on 3min and 5min but not 4min. The critic said "3min+ videos (e.g., 16.7% m.tIoU vs. 13.6–14.2% for existing methods on LF-STVG-3min)" — this is accurate for 3min. For 4min, the baseline is slightly behind. Let me verify: Tab 1(d): TubeDETR=9.6, STCAT=10.4, CG-STVG=10.6, TA-STVG=10.1, Baseline=9.9. So Baseline is slightly lower than STCAT and CG-STVG. The critic's claim that "Baseline (ours) — which is an autoregressive model without memory — also consistently outperforms existing methods on 3min+ videos" is therefore not entirely accurate for 4min. It outperforms on 3min and 5min but not 4min. This is a small inaccuracy in the critic's claim. But the broader point stands: the baseline performs competitively with or better than existing methods despite being simpler.

Let me adjust: I'll say "substantially outperforms on 3min and 5min" rather than "consistently outperforms on 3min+."

OK, I'm ready to write the final review.## Summary

This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), a new setting where the model must localize a target in both space and time from videos spanning 1–5 minutes (versus the standard <1 minute). The authors propose ART-STVG, an autoregressive transformer that processes frames sequentially rather than all at once, with spatial and temporal memory banks and selection strategies. They extend the HCSTVG-v2 validation set to 1–5 minutes to create LF-STVG benchmarks and show large relative improvements over existing methods (e.g., +7.3% m.tIoU on 5-minute videos vs. TA-STVG).

## Strengths

- **The problem formulation is timely and well-motivated.** The paper correctly identifies that current STVG research is confined to videos under a minute, while real applications (surveillance, retrieval) involve multi-minute or hour-long videos. Section 1 articulates this gap clearly and makes a compelling case for LF-STVG as a distinct problem. **[weight=7.60]**

- **The autoregressive/sequential processing design is well-motivated for the long-video setting.** The insight that processing all frames at once is infeasible for long videos — due to both GPU memory and the difficulty of modeling long-range dependencies in a single forward pass — is sound. Treating video as streaming input (Figure 1(b)) is a natural architectural fit for long-form video grounding. **[weight=6.95]**

- **Relative improvements over existing methods are large and the trend is convincing.** In Table 1, the performance gap between ART-STVG and prior methods widens as video length increases (e.g., +0.7%/0.9% on 1min vs. +7.3%/5.5% on 5min relative to TA-STVG). This monotonic trend is the paper's strongest evidence that the approach is on the right track for long-form video. **[weight=9.58]**

- **The memory selection strategies are clearly described and individually ablated.** The paper explains why naive memory accumulation fails (Tables 2–3) and demonstrates that using all temporal memories actually *hurts* performance (Table 2: 16.7% m.tIoU → 9.6% with all memories), showing that selection is essential, not cosmetic. The recovery to 23.0% via selection validates the design. **[weight=8.40]**

## Weaknesses

### Fatal
None.

### Major

1. **The evaluation protocol conflates method advantage with training regime mismatch.** All methods in Table 1 are trained on 20-second clips from HCSTVG-v2 and tested on 1–5 minute videos. The paper states this is for "fair comparison" (line 206), but it systematically disadvantages methods that were designed and tuned for short videos — their architectures may have hard frame limits and have never been trained to handle longer temporal spans. Critically, the Baseline (ours) — an autoregressive model *without* memory — also substantially outperforms existing methods on 3min and 5min videos (e.g., 16.7 vs. 13.6–14.2 m.tIoU on LF-STVG-3min). This means a meaningful portion of the gain comes from the sequential processing paradigm itself, not from the memory banks and cascaded design that constitute the paper's claimed novel contributions. Table 6 (training on 40-second videos) partially addresses this, but 40s → 3min is still a 4.5× length mismatch. Without showing that existing methods fail due to architectural constraints (e.g., maximum frame limits, OOM errors) rather than training mismatch, it is unclear whether ART-STVG is genuinely better at long-form grounding or benefits from a training setup the competitors were not designed for. **[weight=-0.85]**

2. **Absolute performance is very low and the framing overstates the results.** ART-STVG achieves 23.0% m.tIoU on 3-minute videos and 15.0% on 5-minute videos. On LF-STVG-5min, vIoU@0.5 is 11.4% and vIoU@0.7 is 4.7% — the model localizes the target correctly (at IoU>0.5) in only ~1 in 9 video-queries on 5-minute videos. The paper describes these results as "excellent performance" (contribution ♢) without adequately discussing why performance is so low: whether the task is inherently extremely difficult, whether the extended annotations are reliable (no inter-annotator agreement is reported), or whether the 20-second training set simply cannot teach useful long-form structure. An honest discussion of these absolute numbers would help the reader calibrate expectations. **[weight=1.16]**

3. **The memory banks grow unboundedly with no analysis of capacity or computational cost.** The paper states: "we update the memory bank by simply adding the query as a new memory, without removing any existing memories" (line 148). For a 5-minute video at 3.2 FPS, the spatial and temporal memory banks would each accumulate ~960 frames × K partitions worth of features. There is no discussion of maximum capacity, how the selection cost (computing similarities against all stored memories) scales with video length, whether inference time grows linearly, or how the banks would be bounded for hour-long videos. Since the paper's central claim is handling long videos, this is a significant omission. **[weight=3.74]**

### Minor

4. **The cascaded design improvement is marginal relative to its billing.** Table 4 shows cascaded vs. parallel decoders: 23.0% vs. 21.5% m.tIoU (+1.5%). This is presented as a major contribution (contribution ♡ in the abstract), but the improvement is modest. Moreover, the cascaded design creates a hard dependency where temporal localization depends on spatial localization; if the spatial prediction is wrong (m.vIoU ~15%), the error propagates. The paper does not analyze this error propagation or justify why +1.5% is worth the architectural commitment. **[weight=-0.14]**

5. **No computational cost analysis despite this being a stated motivation.** The paper motivates the approach by claiming existing methods face "computational bottlenecks" (Section 1) but never reports runtime, GPU memory, or FLOPs for any method at any video length. The claim that ART-STVG resolves computational bottlenecks is therefore unsubstantiated. **[weight=1.33]**

6. **The value of K (number of decoder blocks) is never specified.** K is used throughout Sections 3.2–3.4 to define the decoder architecture but its numerical value is never stated. Similarly, the memory bank partition size per block is not given. **[weight=3.98]**

7. **Ablations are conducted only on LF-STVG-3min (Tables 2–5).** The effectiveness of memory selection might differ at different video lengths (e.g., selection could be more important at 5min than at 1min). This should at least be discussed. **[weight=6.12]**

### Trivial

8. **No dataset statistics for the LF-STVG extensions.** The number of videos in each variant (1min–5min), the distribution of target event lengths within the longer videos, and whether target annotations appear in the extended portion of the video or only in the original 20-second window are not reported. This limits reproducibility. **[weight=3.35]**

## Nice-to-Haves

- Disentangle the advantage of the autoregressive paradigm from the specific memory/cascaded contributions by training competitors on videos matching the test length (at minimum 1–2 minutes), or equivalently adapting ART-STVG's autoregressive baseline to subsampled frames so existing methods' all-at-once paradigm can process the same frame count.
- Provide runtime, GPU memory, and FLOPs scaling with video length to substantiate the computational efficiency claim.
- Add dataset statistics for the LF-STVG extensions and inter-annotator agreement for the manual review.
- Discuss and ideally bound the memory bank's growth (e.g., max-capacity with eviction policy) and analyze how the selection cost scales.
- Analyze error propagation in the cascaded design: does the model fail primarily on spatial, temporal, or both?

## Removed Points

These points from the input review were removed with justifications:
- **Temporal memory design fragility**: The critic argued that adding all memories reduces performance (Tab. 2: 16.7% → 9.6%), suggesting fragile cross-attention. However, the paper explicitly presents this finding to *motivate* why memory selection is needed — the recovery to 23.0% validates the approach. This is not a weakness.
- **VidSwin overstating "one frame at a time"**: The critic noted that VidSwin uses previous frames for motion features, contradicting the "one frame at a time" framing. This is a minor framing imprecision that does not affect the substance of the contribution. Removed as a nitpick.
- **Loss function in supplementary**: Standard practice at this venue. Removed.
- **Existing methods show extremely low performance on 4min/5min (Tab. 1)**: This is a descriptive observation of the status quo, not a weakness of the paper. Removed.
- **No variance/statistical significance**: Single-run evaluation on these benchmarks is the norm in this community. Removed as not standard practice.

## Novel Insights

The most noteworthy observation from combining the reviews is that the paper's baseline (autoregressive without memory) already outperforms existing short-form methods on 3min+ videos. This suggests the sequential processing paradigm — rather than the specific memory selection or cascaded design — may be the primary driver of improvement, a confound the current experimental design cannot disentangle. The paper would be significantly strengthened by an experiment that isolates this effect (e.g., training existing methods on longer videos, or subsampling frames for ART-STVG's baseline to match competitors' frame counts).

## Suggestions

1. Retrain existing methods on videos matching the test length (at minimum 1–2 minutes) to disentangle paradigm advantage from training mismatch.
2. Report runtime/memory scaling curves for all methods across video lengths.
3. Provide dataset statistics for each LF-STVG variant (video count, event duration distribution) and inter-annotator agreement for the manual extension review.
4. Bound the memory bank (e.g., FIFO with max capacity) and analyze selection cost scaling.
5. Add error analysis: does the model fail on spatial, temporal, or both? Where does the cascaded dependency propagate errors?

## Score and Decision

**Round 1 bracket:** 4.5–5.5 (above Adaptive Memory at 4.60, below SAM2Long at 5.25, comparable to Motion-Grounded at 5.00).

**Narrowing:** The paper's strongest weighted items (relative improvements at 9.58, memory selection ablation at 8.40) are genuinely positive, but the training regime mismatch (weight -0.85) is a significant drag that no anchor in the 5+ range shares to this degree. SAM2Long's weaknesses (-4.40 for limited insights) are offset by higher-weight strengths (9.14, 8.69), while this paper's strengths are lighter. The Motion-Grounded anchor (5.00) provides the closest structural match — new task formulation + baseline + dataset — and the papers are of comparable quality. I place this paper at **5.0**.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>