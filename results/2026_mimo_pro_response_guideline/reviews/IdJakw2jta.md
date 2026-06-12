Now I have sufficient calibration data. Let me compile the final review.

## Summary
This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG) — localizing a target object described by a text query in videos of 1–5 minutes — and proposes ART-STVG, an autoregressive transformer that processes frames sequentially with spatial and temporal memory banks. Memory selection strategies filter relevant memories, and a cascaded decoder feeds spatial localization results into the temporal decoder. The authors extend the HCSTVG-v2 validation set to longer videos and demonstrate substantial gains over existing STVG methods, with the advantage growing as video length increases.

## Strengths
- **Quantitative validation of the problem gap (Table 1)**: Existing methods degrade catastrophically on long videos — TA-STVG's m.vIoU@0.5 drops from 12.1 (1min) to 0.0 (4min, 5min) while ART-STVG maintains 17.6, 13.2, 9.5, 5.2, and 4.7. This directly validates the motivation that short-form approaches are inadequate for long-form video grounding.

- **Non-obvious finding that naïve memory is harmful (Table 2)**: Adding temporal memory *without* selection reduces m.tIoU from 16.7% to 9.6%, while selection boosts it to 23.0% — a 13.4% swing. This empirically demonstrates that "more context is better" fails for long-form video grounding, where irrelevant events dominate the memory bank, and clearly justifies the memory selection design.

- **Training-data-length control (Table 6)**: Competing methods are retrained on 40-second videos to control for the confound that ART-STVG may simply be more architecturally suitable for longer sequences. ART-STVG still achieves 28.3 vs ~20-21 m.tIoU, ruling out this confound.

- **Thorough ablations**: Tables 2–6 systematically isolate temporal memory selection, spatial memory selection, cascaded vs. parallel decoder design, the number of selected spatial memories N_s, and training video length — each evaluated consistently on LF-STVG-3min. This is more comprehensive than most comparable papers in the calibration set.

- **Competitive short-form results (Table 7)**: ART-STVG achieves 59.2 m.tIoU on standard HCSTVG-v2, close to TA-STVG (60.4), demonstrating the approach does not sacrifice short-form performance. The memory-free baseline gets only 46.2, confirming memory banks are essential rather than the autoregressive framing alone.

- **Fair evaluation protocol**: All methods trained exclusively on the same 20-second HCSTVG-v2 training set; extended benchmarks use original YouTube source videos (not concatenated clips) with manual quality review.

## Weaknesses

### Fatal
None

### Major
- **Temporal inference protocol undescribed**: The temporal head produces per-frame start/end probabilities h_i ∈ ℝ² (Equation 7), but evaluation uses video-level m.tIoU requiring global start/end frames. The paper never describes how per-frame probabilities are aggregated into video-level temporal boundaries — whether by thresholding, argmax, or another mechanism. Figure 6 shows start/end probability curves suggesting some aggregation exists, but the procedure is not documented. This is central to reproducibility and affects whether the evaluation supports the claimed gains.

- **Evaluation rests on a single author-constructed benchmark family**: The LF-STVG evaluation extends only the HCSTVG-v2 validation set. While the authors explain HCSTVG-v2 is the only dataset with available source videos, and they created 5 length variants, the benchmark construction protocol lacks detail — how clips were selected, how temporal ground-truth boundaries were annotated for extended portions, and inter-annotator agreement are not described. This limits confidence in the generalizability of the results.

### Minor
- **No computational cost analysis for memory scaling**: Training uses N_f = 64 frames (~20s at 3.2 FPS). Inference on LF-STVG-5min involves ~960 frames. Memory banks accumulate entries from every processed frame across all K decoder blocks without pruning. The paper does not report memory bank size at inference, inference time as a function of video length, or whether memory selection becomes a bottleneck. For a paper whose primary contribution is handling long videos, this is a notable omission.

- **Training-test scale gap for temporal memory selection**: Temporal memory selection — the most distinctive component, responsible for the largest gains (Table 2: 16.7→23.0 m.tIoU) — is trained on ~64-frame sequences but evaluated on up to ~960-frame sequences (a 15× gap). Whether the TextTiling-inspired boundary detection generalizes at this scale is not analyzed.

### Trivial
None

## Nice-to-Haves
- GPU memory measurements showing existing methods fail on long videos would empirically support the computational bottleneck claim made in the introduction.
- Analysis of how temporal boundary detection quality changes with video length would strengthen confidence in the memory selection mechanism.
- At least a summary equation for the loss function in the main text (currently entirely deferred to supplementary).

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Notation confusion in Eq. 1, 5**: The harsh critic flagged that Eq. 1 uses the same notation for appearance and motion features, and Eq. 5 uses the same symbol for both input and output of RoI pooling. These are likely parser artifacts where different symbols/diacritics were lost during PDF extraction. Removed per formatting artifact rules.
- **"Baseline performs poorly on short-form"**: The harsh critic noted the baseline (without memory) gets 46.2 vs 59.2 on short-form, suggesting autoregressive framing alone is harmful. This is not a weakness — it is an observation the paper already demonstrates through its ablations to show memory matters.

## Novel Insights
The paper's most novel empirical finding is that naïvely accumulating all temporal memories is *worse* than having no temporal memory at all (Table 2: 9.6% vs 16.7% m.tIoU). This non-obviously validates that "more context is better" fails for long-form video grounding — a finding with implications beyond this specific task for any memory-augmented architecture processing long sequences with multiple events.

## Suggestions
- Add a clear description of how per-frame temporal predictions h_i^s, h_i^e are aggregated into video-level temporal boundaries for evaluation. This is essential for reproducibility.
- Add a table or figure reporting inference time, GPU memory usage, and memory bank size as a function of video length (1–5 minutes).
- Provide more detail on the benchmark extension protocol: clip selection criteria, temporal ground-truth annotation process, and whether the query target appears throughout the extended video.

## Calibration Anchors

| Anchor Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| ARVideo (hWlCc7Iksi) | 3.40 | 1 | Weaker contribution and experimental validation than our paper |
| Grounded-VideoLLM (YCwN7wQA6W) | 4.25 | 2 | Narrower evaluation and less comprehensive ablations than our paper |
| AMM (1DEHVMDBaO) | 4.60 | 1 | Marginal improvements and limited experiments; our paper has much stronger results |
| Motion-Grounded (tEei1bolt3) | 5.00 | 1 | New task + dataset but novelty concerns; our paper has stronger experimental validation |
| CoSPaL (yHj6EunfVQ) | 5.50 | 2 | Same domain (STVG) but weaker ablations and tracker/encoder fairness concerns |
| ResidualViT (QWDFOOoV3U) | 5.75 | 2 | Missing inference details and limited scope; our paper is more comprehensive |
| StreamChat (JbPb6RieNC) | 5.80 | 2 | Training-free streaming video framework; comparable quality but different focus |
| CG-Bench (le4IoZZHy1) | 6.20 | 2 | Benchmark paper; different contribution type |
| ARLON (8pusxkLEQO) | 6.25 | 1 | Comparable novelty, weaker ablations, accepted; our paper slightly stronger |
| TRACE (14fFV0chUS) | 6.75 | 1 | Comparable novelty with broader benchmark coverage; our paper slightly below |
| Autoregressive Transformers (wkbx7BRAsM) | 7.00 | 1 | Stronger novelty in different domain |

**Round 1 bracket**: 5.5–7.0. Our paper is clearly above the 4.5–5.0 range (AMM, Motion-Grounded) due to much stronger experimental validation, comparable to ARLON (6.25) but with better ablations, and slightly below TRACE (6.75) due to narrower benchmark coverage and the missing inference protocol. **Final score**: 6.5.

## Score and Decision
The paper makes a genuine contribution by defining a practically relevant problem (LF-STVG) and proposing a method with clear, well-ablated improvements that grow with video length. The main concerns — missing inference protocol, single benchmark family, no computational cost analysis — are addressable omissions rather than fundamental methodology flaws. The experimental evidence, while built on one benchmark, is thorough and honestly presented. This warrants a score of 6.5, placing it above accepted papers with weaker experimental support (ARLON, CoSPaL) but below papers with more complete evaluation (TRACE).

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>