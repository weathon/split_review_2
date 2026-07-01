## Summary

The paper introduces SpookyBench, a benchmark where information (text, object shapes, scene depth) is encoded purely in temporal sequences of noise-like frames. Humans achieve 98% accuracy, while all 22 Video-VLM variants (2B–78B, including GPT-4o and Gemini) score 0% across prompting strategies and frame rates. The authors argue this reveals a fundamental "time blindness" in current architectures that over-rely on spatial features.

## Strengths

- **Clean, creative benchmark design that cleanly isolates temporal reasoning.** The opposing-noise-movement (Algorithm 1) and threshold-based depth animation (Algorithm 2) ensure individual frames are indistinguishable from random noise (Basic SNR −39 to −49 dB in Table 2), forcing reliance on motion cues. This design is genuinely novel compared to existing temporal benchmarks.

- **Comprehensive evaluation across 22 model variants** (Table 1), spanning 2B to 78B parameters, multiple architectural families (LLaVA, Qwen, InternVL, InternVideo, GPT-4o, Gemini), and both direct-prompt and chain-of-thought conditions.

- **Genuinely striking finding:** 0% accuracy across ALL models under ALL tested conditions (direct prompt, CoT, various frame rates, even after fine-tuning on the task itself), against a 98% human baseline. This is more dramatic than the partial failures reported in comparable temporal benchmarks.

## Weaknesses

### Fatal
None.

### Major

- **Missing critical control: ordered vs. temporally-scrambled frames.** The paper does not include the experiment that would distinguish frame-level encoding failure from temporal-integration failure. If models also score 0% when the same noise frames are presented in scrambled temporal order, the failure is at the frame-encoding stage (the ViT cannot process binary noise, which is OOD for ImageNet-pretrained encoders). If they perform better on ordered than scrambled sequences, temporal processing would be implicated. Without this control, the paper's central "time blindness" claim conflates two distinct failure modes: (a) the visual encoder cannot extract features from noise-domain frames, and (b) temporal integration mechanisms cannot extract patterns from motion. The benchmark is consistent with both explanations, and the paper does not provide evidence ruling out (a).

- **The fine-tuning experiment (Section 4.4) does not adequately rule out frame-level domain mismatch.** The paper fine-tunes InternVL2.5-8B and Qwen2-VL-7B on 400 SpookyBench videos for 10 epochs and reports persistent 0% accuracy, concluding the failure is "not attributable to domain mismatch." However, typical fine-tuning pipelines (e.g., LoRA via LlamaFactory) update only the language model head or connector, leaving the ViT-based visual encoder frozen. If the encoder produces near-random features from −40 dB noise frames (binary 0/255 values that nothing in ImageNet or LAION training data resembles), no amount of fine-tuning on the LM side can recover meaningful representations. The paper should specify which parameters were updated; if the encoder was frozen, this experiment only confirms that a frozen encoder on OOD inputs yields 0%, not that temporal processing is architecturally impossible.

### Minor

- **Confusing and potentially inconsistent SNR definitions.** Table 2 reports Basic SNR of −39 to −49 dB (measuring motion-boundary-energy to static-frame-variance ratio). Section 3.3.2 / Figure 4 then reports a "binary SNR threshold" at ~2.5 dB where text detection jumps from 0% to 85.7%. These appear to be different SNR metrics (the Figure 4 SNR range of −20 to +10 dB does not overlap with Table 2's −39 to −49 dB range), but the paper does not explain how they differ, what SNR definition Figure 4 uses, or how the threshold analysis relates to the main benchmark. This creates confusion about whether the benchmark operates far below a known detection threshold.

- **The "time blindness" framing partially overclaims the evidence.** The experiments convincingly show that current Video-VLMs fail catastrophically on SpookyBench, but they do not fully disentangle whether the bottleneck is at the frame-encoding stage (ViT cannot process noise frames) or the temporal-integration stage (temporal modules cannot extract patterns from motion). The conclusion should more carefully distinguish these possibilities. A model could have perfectly functional temporal processing that never gets any signal because the encoder gates it out.

- **Human evaluation uses only 6 participants.** While the results are consistent across annotators (Table 3: 94.3–98.9% accuracy, low variance), a larger and more diverse participant pool would strengthen the human baseline claim. Comparable benchmarks (e.g., Vinoground, TVBench) typically use crowdsourced annotation with larger pools.

### Trivial
None.

## Nice-to-Haves

- Add a higher-SNR variant of SpookyBench where individual frames contain faint but recognizable content (above the ~2.5 dB threshold from Figure 4), testing whether temporal integration works when the encoder has a usable signal from individual frames.
- Add a static-frame sanity check: present single frames to VLMs and ask "what do you see?" — this would clarify whether the encoder is producing random outputs or hallucinating content.
- Report results for fine-tuning that explicitly updates the visual encoder (or uses adapter modules on the encoder), to more directly test whether the failure is due to domain mismatch at the encoder level.

## Removed Points

- **"The 0% accuracy is almost certainly explained by frame-level OOD failure, not temporal blindness — and this invalidates the central claim."** Overstated: the Basic SNR metric measures motion-boundary-energy vs. static variance, not traditional pixel-level signal-vs-noise. The paper is aware the frames are noise-like and designs them that way intentionally. However, the underlying need for a control experiment (ordered vs. scrambled) is retained as a Major weakness above.

- **"The human comparison is apples-to-oranges."** This largely restates the paper's own thesis (humans have motion-processing circuitry that ViTs lack; Section 2.2 discusses neuroscience insights). The gap the paper documents IS the contribution, not a flaw in the analysis.

- **"The SNR threshold analysis directly undermines the paper's interpretation."** Reframed as the SNR-definition confusion (kept as Minor). The threshold analysis is a separate experiment on a different SNR metric; it does not contradict the main results.

- Criticisms about missing specification for non-video models (number of frames, resolution, arrangement) — these details are in the appendix, which was stripped by the PDF parser. Excluded per policy.

- Criticisms about garbled text or formatting artifacts in Table 5 — excluded per policy as parser issues, not author errors.

## Novel Insights

None beyond the paper's own contributions. The main critical insight — that the ordered-vs.-scrambled control is needed to distinguish frame-level from temporal-level failure — is a standard experimental-design consideration that is valid but not novel.

## Suggestions

1. **Add the ordered vs. scrambled frame control experiment.** This single experiment would determine whether the failure is at the frame-encoding stage or the temporal-integration stage, and would directly strengthen or temper the "time blindness" claim.
2. **Specify which parameters were updated in the fine-tuning experiment.** If the visual encoder was frozen, repeat with full fine-tuning or encoder adaptation to properly test whether the failure is due to domain mismatch.
3. **Clarify the relationship between the SNR metric in Table 2 and the one used in Figure 4.** If they differ, rename them and explain how the threshold analysis relates to the main benchmark's SNR values.
4. **Qualify the "time blindness" claim** in the conclusion to acknowledge that the failure locus (frame encoding vs. temporal integration) remains unresolved by the current experiments, and that the benchmark tests a compound failure that likely involves both stages.

## Calibration Anchors

**Round 1 bracket:** 4.5–6.5, based on comparison with topically similar temporal-reasoning benchmarks.

**Full anchor list:**
- **TVBench** (6.75, Accept, Round 1): Stronger validation with three quantitative principles; less novel benchmark design. This paper's novelty is higher but validation is weaker.
- **Vinoground** (5.75, Reject, Round 1): Similar temporal-failure finding, rejected primarily for limited novelty. SpookyBench has stronger novelty but weaker validation (missing control experiment).
- **ViLMA** (6.00, Accept, Round 1): Well-validated counterfactual benchmark. SpookyBench has more novel design but less rigorous validation.
- **TemporalBench** (4.20, Reject, Round 1): Weaker novelty and data quality concerns. SpookyBench is clearly stronger.
- **Revealing the Illusion** (5.25, Reject, Round 1): About shortcuts in VideoQA. Different framing but similar finding (models not doing what they claim).
- **Motion-Grounded Video Reasoning** (5.00, Reject, Round 2): Motion understanding benchmark, less directly comparable.
- **TC-Bench** (4.75, Reject, Round 2): Video generation compositionality, less directly comparable.
- **Five-in-One Video Annotations** (5.00, Reject, Round 2): Video description benchmark, less directly comparable.

**Narrowing:** SpookyBench's noise-frame design is more creative than Vinoground's, but the missing control experiment is a more significant gap than Vinoground had. The paper sits between Vinoground (5.75, Reject) and ViLMA (6.00, Accept) — closer to Vinoground due to the validation gap.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>