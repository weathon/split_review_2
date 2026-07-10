## Summary

This paper introduces Long-Form STVG (LF-STVG), a task formulation for spatio-temporal grounding in videos ranging from 1–5 minutes (up from the current 20–35 second benchmarks). The authors propose ART-STVG, an autoregressive transformer that processes frames one at a time with spatial and temporal memory banks plus a cascaded decoder design. On extended HCSTVG-v2 validation sets, ART-STVG substantially outperforms existing STVG methods (23.0 vs. 13.9 m.tIoU on 3-min videos). On short-form STVG, it remains competitive with state-of-the-art.

## Strengths

- **The problem framing fills a genuine gap.** Existing STVG benchmarks are capped at ~20–35 seconds (HCSTVG-v2, VidSTG), while real-world applications require minutes or hours. Defining LF-STVG as a distinct task is a useful contribution that the community would benefit from.

- **The autoregressive architecture is a natural fit for the streaming/long-video regime.** Processing one frame at a time avoids the O(T²) memory scaling of full-frame-pairwise attention used by existing methods, which would be intractable on 3–5 minute videos. This architectural choice is conceptually clean for the stated problem.

- **Results on extended benchmarks show a clear and growing gap.** ART-STVG degrades far more gracefully than existing methods as video length increases. On LF-STVG-3min (Tab. 1c) ART-STVG achieves m.tIoU=23.0% vs. TA-STVG's 13.9%; on LF-STVG-5min (Tab. 1e) 15.0% vs. 7.7%. The gap grows monotonically with length, which is the trend one would hope for from an autoregressive approach on this task.

- **Tab. 6 partially mitigates fairness concerns.** When all methods (including baselines) are trained on 40-second videos instead of 20-second videos, ART-STVG still substantially outperforms (28.3 vs. 20.7 m.tIoU on LF-STVG-3min), showing the advantage is not purely an artifact of training-length mismatch.

## Weaknesses

### Major

- **The main comparison in Tab. 1 conflates architectural advantage with baseline inability to process longer inputs.** The paper states (line 206) that all baselines are "trained exclusively on the HCSTVG-v2 training set (average video length 20 seconds) for fair comparison." But TubeDETR, STCAT, CG-STVG, and TA-STVG encode all frames simultaneously with full spatio-temporal attention — architectures that fundamentally cannot process 3–5 minute videos at inference. Testing these models on inputs 3–15× longer than their design target is not "fair comparison" but structurally unfavorable to the baselines. Tab. 6 (training on 40-second videos) partially addresses this concern but only evaluates on 3-minute videos; we do not know how the gap changes on 4-minute and 5-minute videos when baselines are trained on longer inputs. The dramatic win in Tab. 1 is driven in unknown proportion by ART-STVG's genuine advantage vs. the baselines' inability to process these inputs at all.

- **The temporal memory ablation reveals a concerning design fragility.** In Tab. 2, using temporal memory *without* selection collapses m.tIoU from 16.7% (no memory) to 9.6% (all past memories, no selection) — a **42% relative drop**. The paper's explanation ("irrelevant information") does not account for why adding *all* past information actively hurts more than having no history at all. A well-conditioned decoder should at worst dilute the signal modestly. The fact that the selection heuristic is doing essential filtering (from 9.6 → 23.0, a 140% gain) suggests the temporal decoder's cross-attention over unselected memory is poorly conditioned. This contrasts with the spatial memory (Tab. 3), where adding all memories improves rather than hurts (21.3 → 22.1), confirming the temporal decoder has a specific fragility.

- **Several critical baselines and analyses are missing.** (a) There is no sliding-window adaptation of existing STVG methods (e.g., running them on 20-second chunks with prediction aggregation), which would directly test whether the autoregressive sequential design is genuinely superior to applying existing methods locally. (b) Despite motivating the method with "computational bottlenecks" from "high GPU memory requirements" (Sec. 1, line 30), the paper provides no GPU memory usage, inference time, or FLOPs comparison as video length scales. (c) No variance or confidence intervals are reported for any result (Tabs. 1–7 all show single numbers), making it hard to assess whether performance gaps are meaningful given the modest absolute scores (15–39% m.tIoU).

### Minor

- **Unbounded memory bank growth is not discussed.** Line 148 states memories are added "without removing any existing memories." For a 5-minute video at 3.2 FPS (~960 frames) with K decoder blocks, the bank grows to K×960 query features that must be attended over during selection. The paper does not discuss whether this becomes a bottleneck at even longer lengths (30+ minutes) or whether an eviction mechanism would be needed.

- **The cascaded vs. parallel improvement is modest.** The gain is 1.5% m.tIoU (Tab. 4: 21.5 → 23.0). The paper attributes this to spatial information "assisting" temporal localization, but the cascaded temporal decoder also receives an additional ROI-pooled feature (more parameters/computation). A controlled ablation would strengthen this claim.

- **No human performance or oracle upper bound is provided.** With low absolute scores (23.0% m.tIoU on 3-min, 15.0% on 5-min), it is unclear whether the task is inherently difficult or the method has substantial room for improvement. Reporting human performance would contextualize these numbers.

### Trivial

- **Notation confusion in Eq. 1.** The symbol $\tilde{f}_i^t$ is used to denote both the concatenated multimodal input (Eq. 1) and the textual component after deconcatenation (line 90), which is confusing on first reading.

## Nice-to-Haves

- A sliding-window baseline (existing STVG methods on 20-second chunks with NMS/averaging aggregation) would directly test the claim that autoregressive design is superior.
- A compute/memory scaling plot (GPU memory, inference time vs. video length) would validate the claimed computational motivation in Sec. 1.
- Variance reporting (standard deviations across runs) would help assess whether performance gaps are reliable given the modest absolute scores.
- An investigation into why temporal memory without selection causes a 42% collapse (Tab. 2) and whether architectural changes (gating, learned attention bias) could make the decoder more robust.

## Removed Points

- "5 minutes is not long-form by most standards" — removed as scope creep; the paper defines LF-STVG as minutes-long vs. the existing 20–35 second benchmarks, which is a reasonable scope.
- "Loss function in supplementary" — removed per rule that parser strips appendix sections.
- "Only validation set extension" — removed because this is standard practice when test set annotations are not public, and the paper follows prior work (Yang et al., 2022; Lin et al., 2023b; Gu et al., 2024).
- "The 'first' claim being narrow" — removed; the paper says "to our best knowledge," which is appropriate for a newly defined task scope.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add sliding-window baselines** (existing STVG methods on 20-second chunks with aggregation) and report 4-min/5-min results under the 40-second training setup from Tab. 6.
2. **Provide a compute/memory scaling analysis** (GPU memory, inference time vs. video length) to validate the claimed computational motivation.
3. **Investigate the temporal memory fragility** in Tab. 2 — the 42% relative collapse when unselected memory is added suggests the cross-attention mechanism in the temporal decoder needs architectural attention (gating, learned attention bias, or a different conditioning approach).
4. **Report variance** across multiple runs for key results.

---

**Anchor papers retrieved across rounds:**

| Path | Avg Human Score | Round | Itemized | Comparison |
|------|:---------------:|:-----:|:--------:|-----------|
| `14fFV0chUS.md` (TRACE) | 6.75 | 1 | Yes | Stronger empirical validation; clear performance on standard benchmarks; higher score. |
| `hWlCc7Iksi.md` (ARVideo) | 3.40 | 1 | Yes | Weaker contribution (incremental over VideoMAE); less clear problem motivation. |
| `nAVejJURqZ.md` (TimeSuite) | 5.80 | 1 | Yes | More polished evaluation and comprehensive experiments; accepted despite moderate novelty. |
| `YCwN7wQA6W.md` (Grounded-VideoLLM) | 4.25 | 2 | Yes | Similar profile — sensible architecture but evaluation/novelty concerns led to rejection. |
| `WSze9IIN3d.md` (PA-VDM) | 4.00 | 2 | Yes | Similar quality — interesting idea with missing baselines and evaluation gaps; rejected. |
| `tEei1bolt3.md` (Motion-Grounded) | 5.00 | 1/2 | No | New task + dataset paper; stronger benchmark contribution. |
| `xYzOkOGD96.md` (GROC) | 3.83 | 1/2 | No | New task + automatic annotation method; similar evaluation concerns. |
| `wkbx7BRAsM.md` (Autoregressive Video Imitators) | 7.00 | 1 | No | Strong zero-shot results with comprehensive evaluation. |
| `8pusxkLEQO.md` (ARLON) | 6.25 | 1 | No | Long video generation with diffusion; well-evaluated. |
| `QETk0lBdVf.md` (Long Context Transfer) | 5.80 | 1 | No | Clever approach with thorough ablation. |
| `IryGDUHxDE.md` (Unsupervised AR Action Rec.) | 5.25 | 1 | No | New paradigm for action recognition; mixed reviews. |

**Round-1 bracket:** 3.5–5.5. **Narrowing:** Comparing against Grounded-VideoLLM (4.25, Reject) and PA-VDM (4.00, Reject) — the reviewed paper has a stronger problem motivation than either but similar-magnitude evaluation weaknesses. The decisive items are the unfair-comparison weakness (−9.94) and temporal-memory fragility (−9.43), which together are severe enough to place the paper below the acceptance threshold but not so severe as to be irredeemable.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>