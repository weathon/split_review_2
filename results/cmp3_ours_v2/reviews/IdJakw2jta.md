Here is the final consolidated review:

## Summary

This paper proposes ART-STVG, an autoregressive transformer for Long-Form Spatio-Temporal Video Grounding (LF-STVG). Unlike prior methods that process all frames at once, ART-STVG processes frames sequentially using spatial and temporal memory banks with selective retrieval and a cascaded decoder design. The authors extend HCSTVG-v2 validation videos from 20 seconds to 1–5 minutes to create LF-STVG benchmarks. ART-STVG substantially outperforms prior methods on these benchmarks when all methods are trained on 20-second clips, and shows competitive results on short-form STVG.

## Strengths

1. **Well-motivated and timely problem.** Existing STVG benchmarks max out at 20–35 seconds. The paper correctly identifies this gap with real-world applications and is the first to explicitly name and target minute-scale LF-STVG. The framing is clear and the motivation is compelling.

2. **Sensible architectural design for the task.** The autoregressive streaming approach (processing one frame at a time) naturally avoids the GPU memory bottleneck of batch-processing long sequences and permits arbitrary-length inputs at inference. The dual memory banks with selective retrieval (text-guided top-k for spatial, event-boundary detection for temporal) are principled and well-motivated mechanisms for retaining long-range context in a streaming setting.

3. **Strong and monotonic relative improvements.** In Table 1, ART-STVG consistently outperforms all baselines across all five video lengths, with the gap widening as videos grow longer. On LF-STVG-5min, ART-STVG achieves 15.0 m.tIoU vs. the best baseline at 8.1 (85% relative improvement). On LF-STVG-3min, it achieves 23.0 vs. 14.2 (62% relative). This monotonic trend is the pattern one would expect from a method genuinely better suited for this setting.

4. **Clean, informative ablation studies.** Tables 2–6 cleanly isolate each component's contribution: selective temporal memory yields a 13.4% m.tIoU gain (Table 2), selective spatial memory adds 0.9% (Table 3), and the cascaded decoder design adds 1.5% over parallel (Table 4). Table 6 (training on 40-second videos) provides important evidence that ART-STVG's advantage persists when training length is increased.

5. **Dataset extension is a concrete community contribution.** Extending HCSTVG-v2 validation from 20 seconds to 1–5 minutes using original YouTube source material (not concatenated clips) fills a genuine evaluation gap and will likely be used by subsequent work.

## Weaknesses

### Major

1. **Evaluation primarily tests generalization under distribution shift, not LF-STVG capability per se.** All models are trained exclusively on 20-second clips and evaluated on 1–5 minute videos (line 206). This answers "how well does a model trained on 20s clips generalize to longer videos?" — not "how well does each model perform at LF-STVG when trained on comparable-length videos?" The very low absolute scores (m.tIoU of 15% on 5-minute videos) confirm all methods operate far outside their training distribution. The baselines' low scores are expected and may not reflect their ceiling with appropriate training. Table 6 provides a partial remedy by training on 40-second videos, but 40s is still far from 3–5 minutes. The headline claim — that ART-STVG is "superior for LF-STVG" — would be substantially stronger if supported by an evaluation where models are trained on videos of length comparable to the test set.

2. **Computational efficiency claims are unsubstantiated.** The paper motivates the autoregressive design by stating it "resolves the computational bottleneck" and avoids "high GPU memory requirements" (lines 30–32), yet reports zero computational metrics — no GPU memory usage, parameters, FLOPs, inference time, or throughput. The reader cannot evaluate whether ART-STVG is genuinely more efficient for long videos or whether sequential processing introduces latency overhead. Given that this is one of the paper's two stated motivations, this omission is significant.

### Minor

3. **No variance or statistical significance reported.** None of the tables report standard deviations or confidence intervals. While the main comparisons show large gaps (mitigating this concern), the ablation studies include small differences (e.g., 0.9% m.tIoU gain in Table 3 for spatial memory selection) that cannot be assessed without error bars.

4. **Single dataset.** Evaluation is limited to HCSTVG-v2, which the paper acknowledges (lines 196–200) is the only dataset with available source videos. The generality to other domains, annotation styles, or video types (e.g., egocentric, surveillance) is unknown.

5. **Unbounded memory growth and capacity not discussed.** Line 148 states memories are added "without removing any existing memories." For a 5-minute video at 3.2 FPS with K=6 decoder blocks, this accumulates ~5,760 features. The paper does not discuss whether this causes memory issues, performance saturation, or forgetting at very long lengths.

6. **Annotation details for extended videos are unclear.** The paper states videos were "manually reviewed" (line 200), but it is not specified whether ground-truth annotations (spatial boxes, temporal boundaries) were fully re-annotated for the extended portions or extrapolated from the original 20-second annotations.

### Trivial

7. The loss function is deferred to supplementary material (line 190). Standard practice is to include the optimization objective in the main paper.

## Nice-to-Haves

- Train all methods on videos of comparable length to the evaluation (e.g., extend training to ≥1 minute clips) to directly test whether ART-STVG's design is genuinely better for LF-STVG, rather than just more robust to distribution shift.
- Report GPU memory usage and inference time scaling with video length, to substantiate the claimed computational advantage.
- Analyze whether ART-STVG's gains come more from spatial or temporal localization improvements as video length increases (the m.vIoU gap grows from 0.9% at 1min to 5.5% at 5min, suggesting both benefit).
- Clarify the annotation protocol for the extended validation set.

## Removed Points

These points were considered and removed from the main review:

- **Criticism that the training set "could have been extended as easily as the validation set":** Removed — the training set has 10,131 samples vs. 2,000 validation samples; re-annotation at scale is substantially more work.
- **Requests for details deferred to supplementary material:** Removed — the parser strips appendix sections; these exist in the original submission and are not missing by author choice.
- **Criticism that "processing all frames at once" precludes long videos due to GPU memory:** Weakened to "unsubstantiated" rather than "untrue" — this is a known limitation of full-sequence transformers for long videos, but measurements would still strengthen the claim.
- **Various section-by-section formatting and presentation nitpicks:** Removed as noise that does not affect core claims.
- **Speculative concern about feature fusion token count (Eq. 1):** Removed — the spatial resolution H×W is not explicitly stated, making the exact token count calculation speculative.

## Novel Insights

Beyond the paper's own contributions, the joint analysis of the harsh critic and strengths suggests that the paper's clean ablation structure (Tables 2–6) is the most robust part of the experimental section. The ablation showing that using *all* temporal memories actually hurts performance (9.6% vs. 16.7% without any memory) is a particularly informative finding — it demonstrates that naive memory accumulation is harmful for long-video grounding, and that selective retrieval is not merely an efficiency trick but a correctness requirement. This observation could inform the design of other long-video models beyond STVG.

## Suggestions

1. The highest-leverage improvement is to extend the *training* set to videos of length comparable to the test set (e.g., train on 1–3 minute clips) and rerun the main comparison. This would directly address the central evaluation concern and significantly strengthen the paper's claims.
2. Add a table reporting GPU memory usage at different video lengths (e.g., 1, 3, 5 minutes) and per-frame / total inference time for ART-STVG and the leading baseline.
3. Include standard deviations for the ablation studies (Tables 2–6) to help readers assess the reliability of small improvements.
4. Clarify whether the extended validation set annotations were re-annotated for the longer portions or extrapolated.
5. Discuss the memory bank capacity: at what video length does the unbounded accumulation become a bottleneck?

## Score and Decision

**Bracket analysis (Round 1):** I compared the paper against five score bands using calibration retrieval. The most relevant anchors were:
- **LVM-NET (avg 3.00)**: Long-form video reasoning with memory. Weaker relative gains, single dataset, similar scope. ART-STVG has stronger ablations and larger relative improvements, placing it above this.
- **Grounded-VideoLLM (avg 4.25)**: Temporal grounding in Video-LLMs. Mixed reviews (6,3,5,3). Comparable contribution depth but different framing. ART-STVG's novelty is clearer (first to tackle LF-STVG) though its evaluation has a more significant gap.
- **Streaming Video Understanding / StreamChat (avg 5.80)**: Memory-augmented streaming video with new benchmark. Mostly positive (8,6,6,6,3). ART-STVG's scope (task definition + architecture + benchmark extension) is comparable, but StreamChat had stronger empirical support for its efficiency claims.
- **Multi-granularity Correspondence from Long-term Noisy Videos (avg 8.00)**: All reviewers gave 8. Extensive evaluation across multiple tasks. Clearly stronger paper.

The initial bracket was **[4.5, 6.5]**.

**Narrowing:** ART-STVG's two major weaknesses (training/evaluation mismatch, missing efficiency metrics) are real and prevent it from being a strong accept, but its contributions (new task, sensible architecture, strong ablations, dataset extension) are genuine and the weaknesses are fixable. The paper is clearly stronger than LVM-NET-type papers (3.0) and comparable to mid-range papers (4–6). The relative improvements are large and the ablations are clean.

**Final score: 5.5** — a borderline accept. The paper addresses a genuine gap with a sensible method and provides reasonably strong evidence within its chosen experimental design, but the central evaluation concern and missing efficiency metrics prevent full confidence in the headline claims.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>