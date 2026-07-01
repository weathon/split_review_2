Now I have thoroughly read the paper and cross-checked every claim. Let me write the final consolidated review.

---

## Summary

This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), extending the conventional STVG task from short clips (~20–35 seconds) to minute-long videos. The authors propose ART-STVG, an autoregressive transformer that processes video frames sequentially with spatial and temporal memory banks and selection mechanisms, avoiding the GPU memory bottleneck of existing methods that must process all frames simultaneously. On newly extended LF-STVG benchmarks (1-to-5-minute videos derived from HCSTVG-v2), ART-STVG consistently outperforms prior STVG methods and remains competitive on short-form benchmarks.

## Strengths

1. **Well-motivated and timely problem formulation.** The paper correctly identifies that existing STVG research operates on videos under one minute (average 20–35 seconds on standard benchmarks), while real applications involve minutes or hours of footage. The gap is genuine and clearly articulated in §1.

2. **Autoregressive design is the right architectural choice for the stated problem.** Processing all frames simultaneously is impractical for long videos due to GPU memory constraints. The sequential, streaming-style design (§3.2) directly addresses this computational bottleneck and naturally generalizes to arbitrary-length videos during inference. This is a principled design decision rather than an ad-hoc adaptation.

3. **Consistent and widening performance gap.** In Table 1, ART-STVG's improvement over baselines grows with video length: +0.7/0.9% (m.tIoU/m.vIoU) at 1 min, +9.1/6.8% at 3 min, and +7.3/5.5% at 5 min. This trend is consistent with the paper's thesis that autoregressive processing becomes increasingly advantageous as videos lengthen.

4. **Competitive short-form performance.** ART-STVG achieves 59.2 m.tIoU and 39.2 m.vIoU on the original HCSTVG-v2 (Table 7), close to the current state-of-the-art TA-STVG (60.4/40.2) and ahead of most prior methods. This demonstrates that the autoregressive design does not sacrifice short-video capability — a non-trivial result that supports the method's generality.

5. **Informative ablations across design dimensions.** Tables 2–5 systematically ablate temporal memory selection, spatial memory selection, the cascaded decoder design, and the number of selected spatial memories. The ablations cleanly isolate the contribution of each component and support the design choices.

## Weaknesses

### Fatal
None.

### Major

1. **Baseline evaluation on long videos is underspecified — a critical reproducibility gap.**  
   The paper's central empirical claim (Table 1) is that ART-STVG outperforms existing DETR-based STVG methods (TubeDETR, STCAT, CG-STVG, TA-STVG) on 1-to-5-minute videos. These baselines are designed to process all frames simultaneously. At the paper's stated 3.2 FPS sampling rate, a 5-minute video yields ~960 frames. Processing 960 frames through a transformer in a single forward pass is not feasible on standard hardware. The paper never describes how the baselines were run: Were frames subsampled? Was a sliding window used? Were memory optimizations (gradient checkpointing, etc.) employed? All methods were trained on 20-second HCSTVG-v2 and tested on long videos without fine-tuning (§4.1), but the *inference* protocol for baselines is omitted entirely. This does not necessarily mean the comparison is unfair, but it prevents verification and raises legitimate questions about whether the baselines were operating under equal frame budgets.

2. **Only one dataset is extended for LF-STVG evaluation.**  
   The paper extends only HCSTVG-v2 because "it is the only dataset which provides available source videos" (§4, line 196–200). While the stated reason is understandable, the entire empirical case for LF-STVG rests on a single source dataset. Evaluating on additional datasets (or even synthetic extensions) would substantially strengthen the generality of the findings. The paper should more prominently acknowledge this as a limitation.

### Minor

3. **Temporal memory fragility suggests a deeper architectural issue.**  
   The temporal memory ablation (Table 2) shows that adding *all* unselected temporal memories *hurts* performance dramatically — m.tIoU drops from 16.7% (no temporal memory) to 9.6% (all memories, no selection), a 43% relative decline. The paper attributes this to "irrelevant information" from other events. However, the attention mechanism in the temporal decoder should, in principle, be able to downweight irrelevant memories. That adding information actively *destroys* performance points to a design fragility: the cross-attention mechanism lacks a built-in way to ignore irrelevant content when selection is disabled. This is not fatal (the selection mechanism works), but it suggests the architecture's robustness depends heavily on the selection pre-filter, and the paper does not offer a mechanistic explanation (e.g., attention weight distributions for the "all memories" case vs. the selected case).

4. **Low absolute performance on long videos is not sufficiently contextualized.**  
   ART-STVG achieves 15.0% m.tIoU and 10.0% m.vIoU on 5-minute videos. While relative improvements over near-random baselines (7.7–8.1% m.tIoU) are meaningful for a new task, the paper would benefit from a discussion of where the performance ceiling lies. Is the task intrinsically hard due to the evaluation protocol? Does the training-inference length mismatch (64 frames during training vs. up to 960 frames during inference, §4 Implementation) create a distribution shift that caps performance? Would training on longer videos (as Table 6 hints) substantially close the gap? The paper should ground what 15% m.tIoU means for practical deployment.

### Trivial

5. **The memory bank grows unboundedly.** The paper states memories are added "without removing any existing memories" (§3.3, line 148). While the selection mechanism limits the *used* memories to top-32 (spatial) or nearest-event (temporal), the raw bank grows linearly with video length. The impact on runtime and memory for very long (e.g., hour-long) videos is not analyzed.

6. **The motion feature is not strictly per-frame.** The paper notes that "when applying VidSwin to extract motion features, previous frames are also used as input" (§3.1, line 78). This means the motion stream has a local temporal receptive field, which is not fully aligned with the "streaming" framing. The effective temporal window should be stated, and the impact on the autoregressive claim should be briefly discussed.

## Nice-to-Haves

- **Report results over multiple seeds (≥3).** All reported numbers are point estimates. Given the potential variance from training (especially with the limited HCSTVG-v2 training set), variance estimates would increase confidence in the comparisons.
- **Provide an attention-weight analysis for the temporal memory ablation.** Showing attention distributions for the "all memories" vs. "selected memories" cases in the temporal decoder would clarify whether the attention mechanism genuinely fails to downweight irrelevant memories, strengthening the paper's central claim about the necessity of selection.
- **Analyze memory bank growth as a function of video length.** A simple plot of bank size vs. video length, along with associated compute costs, would bolster the scalability claims.

## Removed Points

These points from the input review were removed under the filtering rules:

1. **"Loss function deferred to supplementary material"** — The parser strips appendices; this content exists in the original submission. Removed per the rule against penalizing stripped appendix content.
2. **"Baseline architecture described in supplementary material"** — Same reason as above.
3. **Speculative claims about baseline unfairness** (e.g., "if baselines were forced to use fewer frames… the comparison is not informative") — The core observation (missing inference protocol) is kept as a Major weakness; hypothetical scenarios about what *might* have happened are removed per the rule against weaknesses that depend on information not present in the paper.
4. **General concern about "vIoU@0.5 is 11.4% and vIoU@0.7 is 4.7%… these numbers mean even the best method barely localizes"** — This phrasing attempts to paint low numbers as a fatal problem while simultaneously acknowledging they don't invalidate the contribution. Rolled into the Minor weakness about contextualization (item 4 above).
5. **"The gap between baseline (30.1) and ART-STVG (39.1) is 9.0 m.tIoU, while the gap between ART-STVG and TA-STVG is only 0.7… memory mechanisms contribute the vast majority of the improvement"** — This is a factual observation but not a weakness; it simply describes what the ablation already shows. Removed as it does not identify a problem.
6. **"Table 6 relative advantage shrinks… not discussed"** — This is an observation that could be discussed more, but it's not a weakness. The absolute improvement still favors ART-STVG. Removed.

## Novel Insights

None beyond the paper's own contributions. The reviews largely agree with the paper's framing and do not surface a counter-narrative or alternative explanation that casts the work in a different light. The main novel observation from the review process is the underspecified baseline inference protocol, which is a transparency gap rather than an interpretative insight.

## Suggestions

1. **Add a dedicated subsection describing the baseline inference protocol.** For each baseline method, report: (a) the frame count used for each video length, (b) any subsampling or windowing strategy, (c) GPU model and memory consumption, and (d) runtime. If all baselines used the same number of frames as ART-STVG (i.e., all frames at 3.2 FPS), describe how this was achieved. If subsampling was necessary, report the ratio and justify its fairness.

2. **Add an attention-weight analysis for the temporal memory ablation** to show why the cross-attention cannot ignore irrelevant memories on its own, and how selection remedies this.

3. **Discuss the training-inference length mismatch explicitly** as a limitation and characterize what performance might be achievable with longer training videos.

4. **Make the memory bank size analysis and the VidSwin temporal receptive window size explicit** in the main paper.

## Score and Decision

This paper tackles a genuine and underexplored problem with a well-motivated, principled approach. The experimental results show a consistent and widening advantage over baselines, the ablations are informative, and the method remains competitive on short-form benchmarks. The main concern is a significant transparency gap in how baselines were evaluated on long videos, which must be addressed. The remaining issues (temporal memory fragility, limited dataset scope, low absolute performance) are not fatal and are typical for a first paper on a new task formulation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>