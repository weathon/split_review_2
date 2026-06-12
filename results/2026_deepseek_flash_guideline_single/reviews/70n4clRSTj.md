## Summary

SpookyBench is a synthetic benchmark that encodes information (text, object silhouettes, dynamic scenes) purely through opposing-motion noise patterns—individual frames contain no spatial signal and appear as random noise. Humans achieve ~98% accuracy on the benchmark, while all 15 tested state-of-the-art video-language models (including GPT-4o, Gemini, Qwen, InternVL families—spanning 2B to 78B+ parameters) score 0% under all conditions. Control experiments (frame-rate variation, fine-tuning on the task) confirm the failure is not attributable to temporal sampling artifacts or simple distribution shift.

## Strengths

1. **Genuinely novel benchmark design.** The core idea—encoding information exclusively through opposing motion of noise patterns so individual frames contain no usable spatial signal (Section 3, Algorithms 1 and 2)—closes a loophole in existing temporal benchmarks where spatial shortcuts are available. This is a legitimate, clearly motivated contribution.

2. **Broad model coverage with a striking result.** The evaluation spans 15 models including closed-source systems (GPT-4o, Gemini 1.5 Pro, Gemini 2.0 Flash), multiple scales, and diverse architectural families (LLaVA, Qwen, InternVL, InternVideo). The consistent 0% result across this diverse set is genuinely informative and more impactful than testing only 2–3 models.

3. **Useful control experiments.** The fine-tuning experiment (Section 4.4)—training InternVL2.5-8B and Qwen2-VL-7B on 400 SpookyBench videos for 10 epochs with continued 0% accuracy—is a strong sanity check ruling out distribution shift as the explanation. The frame-rate ablation (Section 4.3) also usefully shows that temporal sampling frequency alone does not explain the gap.

## Weaknesses

### Major

**1. The SNR threshold analysis (Section 3.3.2) is poorly specified and inconsistent with the main results.** The text states: "The words exhibited negligible detection (~0%) below 2.5dB SNR, but jumped to 85.7% accuracy above this threshold" and "Prompts performed best (40% accuracy), with Chain-of-Thought reasoning improving general identification tasks." It is never specified whether these figures refer to humans or models. If models, the 85.7% and 40% figures directly contradict Table 1 (all models 0% across all conditions). If humans, they are inconsistent with Table 3 (human accuracy 98.9% for Text). Furthermore, the table accompanying Figure 4 shows accuracy jumping to 1.00 (100%) above the threshold, not 85.7%. This section conflates different experiments or detector conditions without adequate explanation and must be clarified to avoid undermining the paper's credibility.

### Minor

**2. The paper lacks basic mechanistic analysis that would validate the 0% result beyond reporting it.** The paper does not show any representative model outputs across models or categories (e.g., do models say "I see noise," hallucinate specific content, or refuse to answer?), does not report how many frames each of the 15 models actually processes, and does not examine whether any temporal signal is detectable in intermediate features. Even a small table of sample responses across model families would significantly strengthen the contribution by ruling out trivial explanations (format mismatch, refusal to answer, overly strict matching).

**3. Details of the acceptable-label sets for Object Images and Dynamic Scenes are not reported.** The paper gives one example and states these sets exist, but does not report the average size, semantic diversity, or construction process of the label sets per video (Section 4.1). Without this information, it is difficult to assess how strict the evaluation is and whether the 0% result could be partially an artifact of narrow label coverage.

**4. The fine-tuning experiment is a reasonable sanity check but is over-interpreted.** The paper says the result "indicates a fundamental architectural inability" (Section 4.4), but training on only 400 videos for 10 epochs on an off-the-shelf pipeline cannot demonstrate architectural impossibility—it mainly shows that quick fine-tuning on a small dataset does not teach motion perception. The paper should acknowledge this limitation.

**5. The paper's diagnostic framing slightly overstates what the evidence distinguishes.** The paper interprets the 0% result as revealing a "fundamental architectural inability" to process temporal information, but all 15 tested models share the same architectural paradigm (sparse frame-sampling + per-frame ViT encoding + temporal aggregation). The result shows that *this specific paradigm* cannot recover motion-defined patterns. The paper's own Figure 1 acknowledges the frame-sampling bottleneck as the culprit, making the stronger "fundamental" framing somewhat inconsistent with its own analysis. Scoping the claims more precisely to the current VLM paradigm would better align the evidence with the conclusions.

### Trivial

None.

## Nice-to-Haves

- Report per-model frame sampling rates and how frames are selected (uniform, keyframe-based, etc.), since the number of frames processed varies dramatically across models.
- Show a small table of representative model outputs across model families and categories.
- Provide average size and diversity metrics for the acceptable-label sets.
- Clarify whether evaluation uses exact string matching or containment/equivalence checking.

## Removed Points

- **Critic's Issue 1 (Structural — the benchmark tests frame-sampling, not "time blindness"):** Partially addressed by the paper (Figure 1 acknowledges the frame-sampling bottleneck; claims are scoped to current VLMs). The demand to test non-VLM video backbones (I3D, SlowFast, TimeSformer) is outside the paper's stated scope (it is about *video-language models*). However, the milder concern about overclaiming is retained as Minor weakness #5.
- **Critic's observation that negative SNR values make 0% less surprising:** This is a descriptive observation about the data, not a weakness of the paper.
- **Critic's request to quantify spatial shortcuts in existing benchmarks:** A nice-to-have that does not constitute a weakness of the current paper.
- **Pure section-by-section descriptive notes with no critical content:** Removed as non-substantive.
- **Formatting/style nitpicks and grammar/typo concerns:** Removed per filtering rules (parser artifacts, not author errors).

## Novel Insights

None beyond the paper's own contributions. The harsh critic's main insight—that the paper's "fundamental time blindness" framing overstates what the evidence supports—is well-taken and has been incorporated as a Minor weakness, but the reviewer did not surface a genuinely novel observation about the problem or methodology that the authors themselves had missed.

## Suggestions

1. **Clarify Section 3.3.2**: Specify whether the accuracy figures (85.7%, 40%) refer to human participants, model outputs, or a separate automatic detection system; reconcile with the table showing 100% accuracy above threshold.
2. **Add representative model outputs**: A single table showing what GPT-4o, Gemini, Qwen, and InternVL models actually output for a few sample videos across categories would validate that the 0% is not an evaluation artifact.
3. **Report per-model frame counts**: For the 15 evaluated models, report the number of frames sampled and the sampling strategy.
4. **Report acceptable-label set statistics**: Average size and semantic coverage of label sets per video.
5. **Scope the diagnostic claims** to "current VLM architectures (sparse frame-sampling + per-frame ViT encoding)" rather than asserting a "fundamental" architectural limitation without testing alternative video processing paradigms.

## Score and Decision

**Round 1 Bracket**: 5.5–6.5 (based on comparison with similar temporal/benchmark papers: ViLMA at 6.0, TVBench at 6.75, Vinoground at 5.75, VideoNIAH at 5.75).

**Final calibration**: The paper sits between ViLMA (6.0, accepted) and TVBench (6.75, accepted). Its benchmark concept is more novel than both, but its presentation clarity (especially the confusing SNR threshold section) is below TVBench's standard. The core empirical contribution—a cleverly designed benchmark that cleanly isolates temporal reasoning and produces a striking 0%-vs-98% gap—is solid and will be useful to the community. The main weaknesses are addressable through clarifying revisions and are not fatal to the contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>