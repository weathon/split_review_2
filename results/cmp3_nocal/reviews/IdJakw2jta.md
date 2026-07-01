Now I'll produce the final consolidated review.

## Summary

This paper defines and addresses Long-Form Spatio-Temporal Video Grounding (LF-STVG), where videos span minutes rather than tens of seconds. The authors propose ART-STVG, an autoregressive transformer that processes frames sequentially with spatial and temporal memory banks and novel memory-selection strategies. They extend the HCSTVG-v2 validation set from ~20 seconds to 1–5 minutes and show that ART-STVG outperforms existing STVG methods on these long-video benchmarks while remaining competitive on short-video benchmarks.

## Strengths

- **Well-motivated problem framing.** Section 1 clearly documents the gap between existing benchmarks (HCSTVG-v2 at ~20s, VidSTG at ~35s) and real-world scenarios, giving the community a concrete label ("LF-STVG") for an underexplored regime.

- **Autoregressive design is architecturally sensible for long videos.** Processing frames one at a time (Fig. 1b) avoids the GPU memory bottleneck that would arise from feeding all frames of a 5-minute video through a single forward pass of a transformer encoder. The paper correctly identifies this advantage.

- **Memory selection ablations are convincing and non-obvious.** Table 2 shows that using *all* temporal memories drops m.tIoU from 16.7% to 9.6%, while the proposed selection strategy recovers it to 23.0%. This is a non-trivial finding — irrelevant historical information actively harms grounding, and the selection mechanism is essential, not a minor refinement.

## Weaknesses

### Fatal

None.

### Major

- **Dataset extension protocol is critically underspecified (lines 196–200).** The paper extends the HCSTVG-v2 validation set from ~20s to 1–5 minutes but does **not** state what ground-truth annotations exist for the extended portions. The original dataset provides spatial bounding boxes and temporal segments for a single ~20s target event per video-query pair. The evaluation uses m.vIoU, vIoU@R, and m.tIoU on the 5-minute videos, but the reader cannot determine: (a) whether the ground-truth temporal segment is still the original ~20s interval within the longer video, (b) whether spatial bounding boxes exist for all frames or only within that interval, and (c) how frames outside the ground-truth temporal tube are scored (ignored? treated as false positives?). The statement "manually review the extended videos to ensure their quality" is ambiguous about what was reviewed. This is the foundation of every quantitative claim in the paper, yet the evaluation protocol is not reproducible from the description given.

- **Comparison protocol for baselines on long videos is not fully explained (lines 206–207, Table 1).** All methods (including baselines TubeDETR, STCAT, CG-STVG, TA-STVG) are trained on 20-second videos (64 frames at 3.2 FPS) but tested on videos up to 5 minutes (~960 frames). The baselines are DETR-like architectures designed to process *all frames at once* via joint self-attention. The paper does **not** specify how these baselines handle 960-frame videos during inference — do they subsample frames? Use a sliding window? The answer directly affects whether the comparison reflects an architectural limitation of the baselines (as claimed) or simply an unstated implementation choice. While Table 6 partially addresses this by training on 40-second videos, the main comparison (Table 1) remains ambiguous. The paper should either explain the baseline evaluation protocol or explicitly discuss this as a confound.

### Minor

- **Loss function is deferred entirely to supplementary material (line 190).** The sentence "Due to limited space, please see our loss function in supplementary material" omits a central component of the method description. A one-paragraph summary of the loss (combination of L1/GIoU for boxes, focal/cross-entropy for classification, temporal boundary losses) belongs in the main paper.

- **Memory capacity and forgetting are not discussed (line 148).** The spatial memory bank is updated by *adding* the spatial query without removing any existing memories. For a 5-minute video at 3.2 FPS with K decoder blocks, this accumulates ~960×K memory entries. The paper never discusses memory capacity limits, computational cost of the selection step over a growing bank, or whether old memories are eventually discarded — especially relevant since Table 2 shows that accumulating *all* temporal memories hurts performance.

- **No measures of uncertainty or variance reported.** No error bars, confidence intervals, or standard deviations are reported for any result. Given that some ablations report modest gains (0.8–0.9% m.tIoU in Table 3, 1.5% in Table 4), it is unclear whether these differences are statistically significant.

### Trivial

None.

## Nice-to-Haves

- The paper would benefit from training all methods on videos of the same length as evaluation (or at least a length closer to 5 minutes). If GPU memory prevents existing methods from doing so, this should be discussed transparently as a genuine limitation of those architectures.
- Clarify the baseline architecture (used in "Baseline (ours)" rows) in the main text rather than deferring to supplementary material.

## Removed Points

These points surfaced in the input review but are excluded from the main weaknesses for the stated reasons:

- *"Related work is superficial"* — subjective judgment; the paper does engage with relevant literature.
- *"Section 3.1 does not report sequence length"* — minor implementation detail, not a substantive weakness.
- *"Table 1 baseline description deferred to supplementary"* — standard practice in conference papers.
- *"Table 1(c)–(e) baselines at floor-level"* — observation about results, not a weakness of the paper; if anything it validates the problem.
- *"Table 6 only trains on 40s"* — acknowledged in "Nice-to-Haves" above; the paper does provide this experiment.
- *"Strengthening the Paper on Its Own Terms" suggestions* — these are constructive suggestions, not weaknesses to weigh against acceptance.

## Novel Insights

None beyond the paper's own contributions. The review panel identified the evaluation underspecification as the central concern, but this is a documentation gap rather than a novel analytical insight.

## Suggestions

1. **Clarify the dataset extension protocol explicitly.** State: (a) whether ground-truth annotations are the original ~20s segment or newly created for the full 1–5 min video; (b) whether spatial bounding boxes exist for all frames or only within the ground-truth temporal tube; (c) how evaluation metrics handle frames outside the ground-truth temporal segment.
2. **Explain how baselines process 960-frame videos during evaluation.** State the frame-sampling strategy, subsampling rate, or any architectural adaptation used for baselines on long videos.
3. **Include a one-paragraph summary of the loss function in Section 3.5.**
4. **Add a discussion of memory bank capacity** — how it scales with video length, and whether the selection mechanism implicitly bounds the effective memory.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>