Now I have enough to draft the review. Let me compile it.Based on my calibration, the most topically similar anchors are:
- bEvI30Hb2W (LVM-NET): avg 3.0 — rejected; long-form video reasoning with memory on single dataset, unclear comparisons
- YCwN7wQA6W (Grounded-VideoLLM): avg 4.25 — rejected; temporal grounding with single dataset/domain limitations  
- tEei1bolt3 (Motion-Grounded Video Reasoning): avg 5.0 — rejected; introduces new spatiotemporal grounding task with dataset
- 14fFV0chUS (TRACE): avg 6.75 — accepted; video LLM temporal grounding with event modeling, solid methodology

**Round-1 bracket: 4.5 – 6.5**

This paper is stronger than the score-3 LVM-NET (better ablations, bigger margins, introduces problem definition rather than just a method) and comparable to or stronger than the score-5 motion grounding paper. It has the major methodological gap (baseline inference protocol) that weaker papers lack, but is not as methodologically complete as TRACE (6.75). The large ablation-supported gains and clear problem motivation push it above the 4-5 range. I'll anchor at **5.5**.

---

## Summary
ART-STVG introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG) as a new evaluation setting and proposes an autoregressive transformer framework with selective spatial/temporal memory banks and a cascaded decoder design. The authors extend the HCSTVG-v2 validation set to 1–5 minute videos for benchmarking, and ART-STVG achieves large performance margins over non-autoregressive baselines on all five lengths while remaining competitive on short-form STVG.

## Strengths
- **Concrete problem motivation**: Figure 2 and Table 1 show a striking collapse of existing methods from ~25% m.vIoU at 1 min to ~4-5% at 5 min, quantitatively establishing the gap that motivates the work.
- **Principled and well-ablated temporal memory selection**: The TextTiling-inspired event-boundary detection using cosine similarity between adjacent memories is elegant. Table 2 reveals a counterintuitive but coherent result: using *all* temporal memories hurts performance (9.6% m.tIoU) versus no memory (16.7%), while selective memory reaches 23.0%—a 13.4% gain that clearly validates the mechanism.
- **Adequate ablation coverage**: Tables 2–5 isolate temporal memory selection, spatial memory selection, cascaded vs. parallel decoder design, and memory bank size, providing a thorough breakdown of each component's contribution.
- **Competitive short-form performance**: ART-STVG achieves 59.2/39.2 m.tIoU/m.vIoU on SF-STVG HCSTVG-v2 (Table 7), only 1.2/1.0 points behind SOTA TA-STVG, demonstrating the autoregressive approach does not severely sacrifice short-form capability once memory is incorporated.

## Weaknesses

### Fatal
None.

### Major
- **Baseline inference protocol for long videos is unspecified — the central comparison is difficult to interpret.** Section 4.1 states only that "all methods including ART-STVG are trained exclusively on the HCSTVG-v2 training set for fair comparison," but is silent on how non-autoregressive baselines (TubeDETR, STCAT, CG-STVG, TA-STVG) handle inference on 1–5 minute videos. At 3.2 FPS over 5 minutes, a video has ~960 frames; these methods process all frames simultaneously and were designed for 64-frame inputs. If baselines are forced to subsample to their native frame budget (~64 frames over 5 minutes ≈ 1 frame per ~5 seconds), they operate at ~16× lower temporal resolution than ART-STVG's sequential per-frame processing. The performance gap in Table 1 would then partly reflect input temporal density rather than architectural design. Partial evidence that architecture matters independently: the autoregressive Baseline (no memory) outperforms TA-STVG at 5 min (9.2 vs. 7.7 m.tIoU, Table 1e), but the confound remains unresolved. This is the single most important missing specification.

- **Single-dataset, single-domain evaluation.** As acknowledged in Sec. 4 ("the reason for choosing HCSTVG-v2 only for extension is that it is the only dataset which provides available source videos"), all five LF-STVG benchmarks are validation-set extensions of one dataset covering one domain (multi-person human-centric surveillance). There is no held-out test set and no second domain. The claim of general LF-STVG capability is therefore unsupported by the evidence, which is restricted to slices of a single source.

### Minor
- **Temporal prediction aggregation not described.** Eq. 7 outputs per-frame start/end probabilities $h_i^s$, $h_i^e$ for each frame $i$. The main paper does not describe how these per-frame outputs across the full video are combined into a final temporal interval for computing m.tIoU. Since the aggregation strategy (argmax, window-based, etc.) directly affects the primary metric, it should be stated in the main text.

- **Spatial memory selection is functionally static.** Spatial memories are ranked by cosine similarity to the textual feature $\tilde{f}_i^t$ (Sec. 3.3), which is fixed throughout the video. This means the same top-$N_s$ memories are selected for every frame, regardless of temporal position—making selection query-driven but not temporally adaptive. The stated motivation ("memories at different moments are not always relevant") implies time-varying relevance, which the mechanism does not achieve for spatial memory. The modest ablation gain (+0.9% m.tIoU, Table 3 vs. Table 2's +13.4%) is consistent with this limitation but goes unacknowledged.

- **Table 6 (40-second training) only evaluates LF-STVG-3min.** Showing results across all five video lengths would clarify whether training on longer videos improves performance uniformly or is concentrated near the training distribution length (40s → closer to 1 min than to 5 min).

### Trivial
None.

## Nice-to-Haves
- A controlled experiment equalizing frame budget across methods (e.g., all methods given 64 frames, either uniformly subsampled or via a sliding window with aggregation) would directly address the temporal-density confound and make the architectural contribution interpretable.
- A failure-mode analysis for temporal memory selection (when does event boundary detection fail, and how often does that cascade to final localization error?) would increase the contribution's actionability given that temporal memory selection is the highest-leverage component.
- Table 6 could be extended to all five video lengths for a cleaner characterization of training-length effects.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **SF-STVG Baseline gap framed as unacknowledged architectural cost**: The reviewer noted that the Baseline (46.2% m.tIoU) is 13+ points below prior methods on SF-STVG. However, ART-STVG with memory reaches 59.2%, which is genuinely competitive. The paper's claim of "competitive results" refers to the full model, which is accurate. This is a minor completeness-of-discussion observation, not a substantive weakness; removed.

## Novel Insights
The most genuinely novel and counterintuitive finding is that naive all-temporal-memory *hurts* performance relative to no memory at all (9.6% vs. 16.7% m.tIoU, Table 2). This is not merely a confirmation that selective memory helps — it demonstrates that unfiltered historical context actively degrades localization in long-form video, likely because cross-attention over many irrelevant temporal events dilutes the signal. This result has broader implications for streaming video understanding architectures: memory bank design must incorporate active selection to be beneficial, and simply growing the memory window can be counterproductive.

## Suggestions
- In Sec. 4.1 or the implementation section, explicitly state the frame-sampling protocol for each baseline at inference time (e.g., "baselines subsample to 64 frames uniformly" or "baselines use sliding-window inference"). This is the most critical clarification needed.
- Add a brief paragraph in Sec. 3.2 or 3.5 describing how per-frame start/end probabilities are combined into a final temporal interval for m.tIoU computation.
- Discuss the static nature of spatial memory selection and why text-similarity-based ranking still provides benefit (e.g., focusing on target-relevant frames globally).
- If computationally feasible, add a simple sliding-window variant of TA-STVG as a controlled baseline to isolate architectural contribution from temporal density.

## Score and Decision

**Anchor papers:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| bEvI30Hb2W | 3.0 | 1 | LVM-NET: long-form video with memory networks, single dataset, weaker ablations — rejected; ART-STVG has stronger ablations and clearer contributions |
| ICR3swcnaa | 3.0 | 1 | Spatio-temporal diffusion for action recognition — different task, much weaker contribution |
| YCwN7wQA6W | 4.25 | 1 | Grounded-VideoLLM: temporal grounding in video LLMs, single domain, rejected; similar evaluation limitations |
| tEei1bolt3 | 5.0 | 1 | Motion-grounded video reasoning: introduces new grounding task+dataset; rejected; similar scope |
| 14fFV0chUS | 6.75 | 1 | TRACE: temporal grounding via causal event modeling, accepted; stronger methodology (multi-dataset, clearer comparisons) |
| QWDFOOoV3U | 5.75 | 1 | ResidualViT for temporal video grounding; borderline reject; stronger evaluation design |
| OxKi02I29I | 5.67 | 1 | Long video understanding with MLMs; accepted; simpler contribution but cleaner evaluation |
| 9Cu8MRmhq2 | 8.0 | 1 | Multi-granularity correspondence in long videos; accepted; stronger methodology, multi-dataset |

**Round 1 bracket: 4.5 – 6.0**

The paper sits above the score-3 rejected papers (better ablations, genuine new benchmark, large gains) but below TRACE (6.75, which has cleaner multi-dataset evaluation and clearer comparison protocols). The two major weaknesses — unspecified baseline inference protocol and single-domain evaluation — meaningfully reduce confidence in the central empirical claims, but the ablation design (especially Table 2's striking result) and the large performance margins across five video lengths provide real evidence. The competition at borderline accept (5.5–6) is tight; the missing baseline protocol is the key differentiator that keeps this from a clear accept.

**Final score: 5.0**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>