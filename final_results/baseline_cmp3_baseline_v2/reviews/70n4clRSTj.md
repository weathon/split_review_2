## Summary

This paper introduces **SpookyBench**, a synthetic benchmark designed to isolate pure temporal understanding in video-language models. Videos encode information (text, object silhouettes, depth-map-based scenes) exclusively through motion patterns in noise-like frames, eliminating spatial cues. Human participants achieve 98% accuracy, while 15 state-of-the-art VLMs (including GPT-4o, Gemini, Qwen, InternVL) score 0% across all prompting strategies, frame rates, and even after fine-tuning on the benchmark. The paper argues this reveals a fundamental "time-blindness" in current architectures that rely on spatial-first processing.

## Strengths

- **Novel and well-motivated benchmark design.** SpookyBench cleanly isolates temporal pattern recognition by removing spatial shortcuts, addressing a known gap in existing temporal reasoning benchmarks that inadvertently allow spatial cues.
- **Comprehensive and consistent evaluation.** The paper tests 15 open-source and 3 closed-source models across scales (2B–78B), two prompting strategies, and multiple frame rates. The 0% accuracy is remarkably consistent, making the failure mode unambiguous.
- **Human baseline and frame-rate analysis.** Human evaluation with 6 participants shows 98% accuracy, and the frame-rate experiment (1–30 FPS) confirms that the VLM failure is not due to temporal sampling rate.
- **Fine-tuning experiment strengthens the architectural claim.** Two models fine-tuned on 400 SpookyBench videos for 10 epochs still achieve 0% on the test set, suggesting the limitation is not merely distribution shift but a fundamental architectural inability.
- **Clear presentation and useful analysis.** The SNR metrics and the binary threshold effect for text detection provide insight into why the task is hard for models but easy for humans.

## Weaknesses

### Major

- **Limited scope of the benchmark.** SpookyBench tests a very specific form of temporal understanding: decoding information from motion-defined patterns in binary noise. While interesting, this is far from the full range of temporal reasoning needed in real-world video understanding (e.g., event causality, long-term dependencies, action prediction). The paper's claim that models are "time-blind" for video understanding in general is an overgeneralization from this narrow task.
- **Small human evaluation sample.** Only 6 participants were used. While the results are consistent, a larger and more diverse sample would strengthen the human baseline. The paper does not discuss whether participants were familiar with the task or had prior exposure to similar stimuli.
- **No comparison to non-VLM baselines.** The paper only tests VLMs. It would be informative to evaluate simple motion-based classifiers (e.g., optical flow + SVM) or models that explicitly process temporal patterns (e.g., video action recognition models without language). This would help determine whether the failure is specific to VLMs or a broader limitation of current video understanding architectures.

### Minor

- **Fine-tuning experiment may be insufficient.** Training on only 400 videos for 10 epochs is a limited exploration. The paper claims this proves architectural limitation, but it is possible that more data, longer training, or different fine-tuning strategies (e.g., full model fine-tuning vs. LoRA) could yield non-zero accuracy. The paper should discuss this caveat.
- **The binary SNR threshold effect is only analyzed for text.** It is unclear whether similar thresholds exist for images and dynamic scenes. The paper could provide analogous analysis for those categories.
- **Dataset size is small (451 videos).** While the generator can produce more, the current evaluation is limited. The paper should report variance across different random seeds or generation parameters to show robustness.

### Trivial

- The paper states "all models achieved 0% accuracy across all frame rates" but Table 5 only shows four models. The claim would be stronger if all models were tested at multiple frame rates.

## Nice-to-Haves

- Include a simple non-VLM baseline (e.g., optical flow + classifier) to contextualize the VLM failure.
- Provide a larger human evaluation (e.g., 20+ participants) and report inter-annotator agreement.
- Analyze whether models can learn the task with more extensive fine-tuning (e.g., 1000+ videos, 50 epochs).
- Show the binary SNR threshold analysis for image and dynamic scene categories.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add a non-VLM baseline (e.g., a model that computes optical flow and classifies motion patterns) to show whether the failure is specific to VLMs or a general limitation of current video understanding.
- Expand the human evaluation to at least 20 participants and report inter-annotator agreement.
- Conduct a more extensive fine-tuning study (more data, longer training, different learning rates) to better support the claim of architectural limitation.
- Provide SNR threshold analysis for all three categories, not just text.

## Score and Decision

The paper presents a novel, well-executed benchmark that convincingly exposes a failure mode of current VLMs. The main limitation is the narrow scope of the temporal understanding tested, which tempers the generality of the "time-blindness" claim. The human evaluation is small but consistent. Overall, the contribution is valuable and likely to stimulate research, but the benchmark's synthetic nature and limited scope prevent it from being a definitive test of general temporal understanding. I recommend borderline accept.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>