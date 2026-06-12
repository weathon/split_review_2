## Summary

This paper introduces **SpookyBench**, a synthetic benchmark designed to evaluate purely temporal reasoning in video-language models (VLMs) by encoding visual content (text, objects, dynamic scenes) exclusively via motion patterns within noise—individual frames appear as noise, and information is only accessible through temporal changes. Humans achieve 98% accuracy on this benchmark, while 26 state-of-the-art VLMs (including GPT-4o, Gemini, Qwen, InternVL, and many others) achieve **0% accuracy** across all prompting strategies, frame rates, and even after fine-tuning on the task. The paper argues this reveals a fundamental "time-blindness" in current architectures that over-rely on spatial features and lack dedicated temporal pattern recognition mechanisms.

## Strengths

- **Novel and well-motivated benchmark design.** SpookyBench cleanly isolates temporal reasoning from spatial cues, addressing a real blind spot in existing benchmarks that often allow spatial shortcuts. The motion-based encoding (opposing noise motion, threshold-based animation) is elegant and grounded in perceptual principles.
- **Extremely thorough empirical evaluation.** The paper tests 26 models spanning scales (2B–78B), architectures (LLaVA, Qwen, InternVL, InternVideo), and both open-source/closed-source systems, with consistent 0% accuracy across direct prompts, chain-of-thought prompts, varying frame rates (1–30 FPS), and after fine-tuning. The failure is robust.
- **Key positive control: fine-tuning still yields 0%.** The fact that InternVL2.5-8B and Qwen2-VL-7B remain at 0% after 10 epochs of training on SpookyBench strongly suggests a fundamental architectural limitation rather than a distribution shift or insufficient exposure.
- **Clear human baseline with high accuracy (98%).** The human evaluation, though small (N=6), convincingly shows the task is perceptually easy for humans, emphasizing the gap.
- **Signal-to-noise analysis provides quantitative insight.** The SNR metrics (coherence, motion contrast, etc.) characterize why models might fail (e.g., negative motion contrast), though a direct correlation with model failure is not fully explored.

## Weaknesses

### Fatal
None.

### Major
1. **Limited human evaluation scale.** Only 6 participants participated. While the results are striking, a larger participant pool (e.g., 20–50) would strengthen the human baseline claim, especially for the perceptual rating and frame-rate experiments (only 3 participants for the frame-rate study). The 0% model results are so stark that this does not invalidate the paper, but it is a concern for reproducibility.
2. **No exploration of why fine-tuning fails.** The paper reports that fine-tuning yielded 0% accuracy but does not analyze training dynamics (e.g., loss curves, per-category accuracy during training, or whether the models learned any motion-based features at all). Without such analysis, it remains possible that the fine-tuning setup (10 epochs, 400 videos) was insufficient or that the optimization was poor. The authors should provide at least a loss curve or show that the model did not overfit the training set to rule out basic training issues.
3. **The benchmark is entirely synthetic; real-world relevance is argued but not demonstrated.** The paper references biological signaling and covert communication, but does not provide any experiments showing that the same temporal processing deficit would manifest in more naturalistic videos where spatial cues are partially available but unreliable (e.g., low-light conditions, blur, occlusion). Connecting SpookyBench performance to realistic temporal understanding tasks would strengthen the claim that this is a fundamental limitation.

### Minor
1. **The claim of "time blindness" is somewhat overstated.** The models fail on a very specific motion-in-noise pattern recognition task. There exist temporal reasoning tasks (e.g., counting actions, ordering events, detecting speed changes) where current VLMs show non-trivial performance. The paper acknowledges this by citing existing benchmarks, but the title and framing suggest a more universal temporal blindness, which may oversimplify.
2. **The baseline analysis could be enriched.** The paper does not compare against simple non-learned temporal processing methods (e.g., optical flow + motion energy detector) to confirm that the temporal information is indeed extractable by algorithms other than humans. While not required, this would strengthen the claim that VLMs are unusually deficient.

### Trivial
- The table in Section 3.3.1 formatting is slightly garbled (e.g., " $-2.20$  and  $-3.18$  dB" appears inconsistent with Table 2). This is minor and likely a parser artifact.

## Nice-to-Haves
- Provide learning curves from the fine-tuning experiment (loss, training accuracy) to show that the models indeed converged to zero.
- Include a simple baseline method (e.g., frame differencing + classification) to quantify how much temporal information is theoretically available.
- Expand the human evaluation to a larger pool (e.g., via Mechanical Turk) to confirm the 98% result.
- Show that models also fail on more naturalistic videos where spatial cues are degraded but not absent (e.g., temporal noise on real videos).

## Novel Insights

None beyond the paper's own contributions. The paper's main insight—that current VLMs are completely blind to purely temporal pattern information despite its trivial perceptibility to humans—is well supported and important.

## Suggestions

1. Provide a more detailed analysis of the fine-tuning failure: show loss curves, training set accuracy (to confirm overfitting or lack thereof), and perhaps fine-tune with a larger dataset or longer training to rule out insufficient resources.
2. Consider adding a small experiment with a traditional computer vision baseline (e.g., optical flow + SVM) to quantify the temporal signal and show that algorithms can solve the task—this would sharpen the critique of VLMs.
3. Broaden the human participant pool (e.g., via a crowdsourcing platform) for a more statistically robust human baseline, especially for the frame-rate experiment.

## Score and Decision

The paper makes a clear, novel, and well-supported contribution: it constructs the first benchmark that isolates pure temporal reasoning in videos, demonstrates a catastrophic and consistent failure across all current VLMs, and provides strong evidence (fine-tuning failure) that this is an architectural limitation rather than a data or optimization issue. The weaknesses (small human study, limited analysis of fine-tuning) are non-fatal and can be addressed in revision. The paper is valuable to the community and likely to stimulate new research on temporal processing in multimodal models.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>