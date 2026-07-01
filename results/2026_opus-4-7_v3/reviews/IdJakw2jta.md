Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me begin calibration. Round 1 — Bracketing:Let me read the most relevant anchors to calibrate:Now I have sufficient calibration data. Let me finalize the review.

**Round 1 Bracket:**

Comparing against the anchors:
- The paper is clearly better than score-3 papers (LVM-NET, Spatio-temporal Diffusion Transformer) which have weak novelty and limited evaluation
- It's comparable to score 4.5–5 papers (Adaptive Memory Mechanism at 4.60, Motion-Grounded Video Reasoning at 5.00) — similar "new problem + method" setup with comparable evaluation concerns
- It falls short of TRACE (6.75, Accepted) which has stronger experimental evidence and broader evaluation
- Far from the score-8 papers which have comprehensive, well-validated contributions

**Initial bracket: 4.5 – 6.0**

The two major weaknesses (benchmark conflation, structural comparison advantage) are real but the paper has genuine merit (novel problem, strong ablations, effective memory selection). The question is whether the contributions are sufficient despite the evaluation limitations. Let me write the final review.

---

## Summary
This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG) as a new problem setting and proposes ART-STVG, an autoregressive transformer with spatial and temporal memory banks and selective memory strategies. The authors extend HCSTVG-v2 validation videos to their original YouTube source videos (1–5 minutes) to create five benchmark splits, and demonstrate large improvements over existing STVG methods. The core idea — sequential frame-by-frame processing with event-aware memory selection — is architecturally well-matched to the long-form challenge.

## Strengths
- **Temporal memory selection is strongly validated.** Tab. 2 shows that using all temporal memories actually *hurts* performance (m.tIoU drops from 16.7% to 9.6%), while selective temporal memory using TextTiling-inspired event boundary detection raises it to 23.0% — a 13.4-point swing. This is a convincing and insightful result demonstrating that naive memory augmentation is counterproductive for long videos and that event-aware selection is critical.

- **Systematic ablation study isolates individual contributions.** Tables 2–5 ablate temporal memory selection, spatial memory selection, cascaded vs. parallel decoder design, and spatial memory size $N_s$, all on the same LF-STVG-3min split. Each component shows meaningful gains (e.g., cascaded vs. parallel decoder: +1.5% m.tIoU, +2.8% vIoU@0.3 in Tab. 4).

- **Benchmark uses original source videos.** The extension methodology uses original YouTube videos rather than clip concatenation (Sec. 4, "Datasets"), preserving natural video structure and avoiding artificial distribution shifts.

- **Performance gap widens with video length.** Fig. 2 and Tab. 1 show ART-STVG's advantage over competitors grows monotonically with video duration (e.g., from +0.7% m.tIoU at 1-min to +7.3% at 5-min vs. TA-STVG), demonstrating the method scales better to the long-form regime.

## Weaknesses

### Fatal
None

### Major
- **Benchmark design conflates temporal and spatial evaluation.** The LF-STVG benchmarks extend ~20-second HCSTVG-v2 clips to 1–5 minute source videos, but the annotations — the same ~20-second temporal window and per-frame bounding boxes — remain unchanged. The spatial grounding difficulty is identical to short-form STVG by construction; only the temporal search space grows. The paper reports m.vIoU and vIoU metrics that conflate temporal and spatial performance without disaggregation. The paper does separately report m.tIoU (temporal-only), but does not report spatial grounding accuracy conditioned on correct temporal localization. This means the reader cannot determine whether ART-STVG's improvements come from better temporal retrieval, better spatial grounding, or both — though the benchmark design strongly suggests the former dominates. This limits the evidential value of the evaluation for understanding *why* the method works.

- **Structural comparison advantage from length extrapolation robustness.** All methods are trained on 20-second clips and tested on 1–5 minute videos (Sec. 4.1). ART-STVG's frame-by-frame autoregressive design is inherently robust to this train-test length mismatch, while baseline methods (TubeDETR, STCAT, CG-STVG, TA-STVG) process entire videos simultaneously and face severe length extrapolation at test time. Tab. 6 partially addresses this by training all methods on 40-second videos, and ART-STVG still wins handily (m.tIoU 28.3 vs. ~20-21 for competitors on 3-min videos). However, 40 seconds is still far from 3 minutes. No length-adaptive inference strategy (e.g., sliding window, temporal sub-sampling) is provided for baselines to separate ART-STVG's architectural robustness from its methodological contributions (memory selection, cascaded decoder).

### Minor
- **Missing computational analysis despite efficiency claims.** The introduction argues existing methods face "computational bottlenecks" for long videos (Sec. 1) and that ART-STVG "resolv[es] the computational bottleneck." However, no runtime, GPU memory usage, or FLOPs comparisons are provided anywhere in the paper. This is a stated motivation that lacks empirical support.

- **"One frame at a time" framing is slightly misleading.** Sec. 3.1 acknowledges "when applying VidSwin to extract motion features, previous frames are also used as input," meaning the model processes a local temporal window for motion features, not truly a single frame. The abstract ("processes its frames sequentially") and Fig. 1 ("processing one frame at a time") oversimplify this.

- **Base autoregressive architecture is substantially weaker on short-form STVG.** Tab. 7 shows the baseline (ART-STVG without memory) achieves only 46.2% m.tIoU on HCSTVG-v2, far below all competitors (53.9%–60.4%). The memory modules recover most of this gap (to 59.2%), but this reveals the autoregressive architecture alone is less suited to short-form STVG. The paper does not discuss this trade-off or analyze why.

### Trivial
None

## Nice-to-Haves
- Report spatial grounding accuracy conditioned on oracle temporal segments to disaggregate temporal vs. spatial contributions.
- Provide at least one length-adapted baseline (e.g., sliding-window inference for TA-STVG) to better separate architectural advantage from methodological contribution.
- Failure case analysis on 4–5 minute videos to diagnose whether errors are dominated by temporal localization failures, spatial localization on correct frames, or compounding autoregressive drift.
- Computational cost analysis (GPU memory, inference time vs. video length) to substantiate the efficiency claims.
- Discussion of the autoregressive architecture's weakness on short-form STVG (Tab. 7 baseline at 46.2%) and what this implies about the design trade-off.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Loss function deferred to supplementary material"** — Removed per policy: supplementary/appendix content is stripped by the parser; the original submission contains this.
- **"Dataset construction lacks detail (quality criteria, exclusion rates, inter-annotator agreement)"** — Removed: reproducibility nitpick about dataset curation implementation details.
- **"No comparison against video-LLM baselines (MA-LMM, VideoLLaMA)"** — Removed: these are different task paradigms (video QA, captioning) and cannot be directly applied to STVG bounding-box prediction without significant adaptation.
- **"No statistical significance or variance across runs"** — Removed: single-run evaluation is standard practice in this field's benchmarks.
- **"Edge cases in temporal memory selection (gradual transitions, noisy early training)"** — Removed: speculative concern without concrete evidence from the paper.
- **"Abstract mentions hours-long videos but evaluates only up to 5 minutes"** — Removed: the abstract says "several minutes or even hours" when describing real-world videos as motivation; the evaluation addresses the "several minutes" part. This is standard motivational framing.
- **"Spatial memory selection mechanism is under-analyzed"** — Removed: Tab. 3 demonstrates it works empirically; deeper analysis would be nice but is not a weakness.

## Novel Insights
The finding that naive temporal memory augmentation is counterproductive for long-form video grounding (m.tIoU drops from 16.7% to 9.6% when using all temporal memories, Tab. 2) while event-boundary-aware selection dramatically improves it (to 23.0%) is a genuinely useful insight for the broader long-form video understanding community. This suggests that memory-augmented architectures for long videos require careful curation of what information to retain, and that TextTiling-style event segmentation provides an effective selection criterion. The cascaded spatial-to-temporal decoder design (Tab. 4) also offers a modest but consistent insight that fine-grained spatial target information can assist temporal boundary prediction.

## Suggestions
- Report temporal localization accuracy (tIoU distribution) and spatial grounding conditioned on oracle temporal segments separately. This single experiment would resolve the most significant evaluation ambiguity.
- Implement sliding-window inference for at least one strong baseline (e.g., TA-STVG) to provide a fairer long-form comparison. Even a simple approach of running the baseline on overlapping windows and merging predictions would be informative.
- Add a computational cost table (GPU memory, wall-clock time) for ART-STVG vs. baselines at each video length. This would substantiate the efficiency claims and demonstrate practical benefits.
- Discuss the short-form performance trade-off explicitly: the autoregressive design trades short-form optimality for long-form scalability, and this should be acknowledged as a limitation.

## Score and Decision

**Calibration Anchors (all rounds):**

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| LVM-NET | bEvI30Hb2W | 3.00 | 1 | Similar topic (long-form video + memory), but much weaker evaluation and novelty; reviewed paper is clearly better |
| Spatio-temporal Diffusion Transformer | ICR3swcnaa | 3.00 | 1 | Related topic, rejected for weak novelty; reviewed paper has stronger problem formulation |
| Anomalous Action Recognition | MSxCBXD5C8 | 3.00 | 1 | Related spatiotemporal work, limited scope; reviewed paper is substantially better |
| Grounded Video Caption Generation | xYzOkOGD96 | 3.83 | 1 | New task + dataset paper, criticized for overclaiming novelty; reviewed paper has better experimental support |
| Video Q-Former | R6sIi9Kbxv | 4.00 | 1 | Related multimodal video model, rejected for limited comparison and unclear generalization |
| Grounded-VideoLLM | YCwN7wQA6W | 4.25 | 1 | Temporal grounding, rejected with mixed reviews; similar evaluation concerns |
| Adaptive Memory Mechanism | 1DEHVMDBaO | 4.60 | 1 | Very similar topic (memory for long-form video ViT), rejected for marginal improvements and missing ablations; reviewed paper has much better ablations but similar evaluation concerns |
| Motion-Grounded Video Reasoning | tEei1bolt3 | 5.00 | 1 | New task + new benchmark + model, rejected; similar paper type with comparable concerns about evaluation metrics |
| TemporalBench | Wto5U7q6I2 | 4.20 | 1 | Benchmark paper for temporal understanding, rejected for evaluation concerns |
| Vinoground | a1P5kh2oo8 | 5.75 | 1 | Temporal reasoning benchmark, rejected; stronger evaluation design |
| ResidualViT | QWDFOOoV3U | 5.75 | 1 | Efficient video grounding, borderline; somewhat stronger experimental design |
| Long Context Transfer | QETk0lBdVf | 5.80 | 1 | Long context for video LMMs, borderline reject; more comprehensive evaluation |
| UniSDNet | UX9lljSZqX | 6.25 | 1 | Video grounding, borderline; stronger experimental comparisons |
| TRACE | 14fFV0chUS | 6.75 | 1 | Temporal grounding via causal event modeling, accepted; significantly stronger experimental evidence and broader benchmarks |
| Multi-granularity Correspondence | 9Cu8MRmhq2 | 8.00 | 1 | Long-term video, accepted; much stronger comprehensive evaluation |
| ARVideo | hWlCc7Iksi | 3.40 | 1 | Autoregressive video pretraining, rejected for limited novelty |

**Round 1 bracket: 4.5 – 6.0**

**Narrowing to final score:** The paper sits clearly above the score-3 reject-range papers and the score-4 papers (Adaptive Memory Mechanism, Video Q-Former) — it has better ablations, a clearer problem formulation, and a more novel contribution. However, the two major weaknesses (benchmark conflation, structural comparison advantage) are substantive and prevent it from reaching the borderline accept level occupied by papers like TRACE (6.75) or UniSDNet (6.25), which have more comprehensive and fair evaluations. The paper is most comparable to Motion-Grounded Video Reasoning (5.00) and the 5.5-range papers — it introduces a genuine new problem with a reasonable method but has evaluation gaps that limit the strength of its claims.

The paper's contribution is real: it identifies an important gap (STVG methods fail on long videos), proposes a well-motivated architecture, and validates its components through strong ablations. The memory selection finding is genuinely insightful. But the evaluation does not fully separate the method's contributions from its architectural advantages, and the benchmark design limits what can be concluded about spatial grounding. These are addressable issues, and the paper would benefit significantly from a resubmission with disaggregated evaluation and fairer baselines.

**Final Score: 5.0** — The paper makes a genuine contribution to an underexplored problem with a well-motivated method and strong ablations, but the evaluation design has significant gaps (benchmark conflation, structurally unfair comparison) that prevent the claims from being fully supported. It falls between borderline reject and borderline accept.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>