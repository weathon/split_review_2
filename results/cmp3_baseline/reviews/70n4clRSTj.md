## Summary

The paper introduces **SpookyBench**, a synthetic benchmark designed to isolate **purely temporal** understanding in video-language models by encoding information (text, object silhouettes, dynamic scenes) exclusively through motion patterns over noise-like frames where individual frames contain no spatial content.  The authors demonstrate that human participants achieve 98% accuracy on this benchmark, while 27 state-of-the-art open-source and closed-source Video-VLMs—including those with explicit temporal modules (TimeChat, Qwen-VL, GPT-4o, etc.)—all achieve **0% accuracy**, even after fine-tuning on the benchmark itself.  The study argues that current architectures are fundamentally "time-blind" because they prioritize frame-level spatial features over temporal dynamics.

## Strengths

- **Novel and well-motivated diagnostic benchmark.**  While existing benchmarks test temporal reasoning alongside spatial cues (e.g., TemporalBench, TVBench), SpookyBench is the first to **eliminate all spatial information**, forcing models to rely solely on temporal changes. This clean isolation is a genuine contribution.
- **Comprehensive evaluation.**  The paper tests 24 open-source and 3 closed-source models spanning a wide range of architectures, parameter scales (2B–78B), and training strategies (generalist, video-specific, temporal-focused).  The uniform zero accuracy across all models is striking and reveals a clear, consistent limitation.
- **Human baseline confirms task solvability.**  With 98% human accuracy (6 participants, three task categories), the benchmark is clearly not impossible; the failure is on the machine side.
- **Fine-tuning experiment strengthens the architectural argument.**  Finetuning InternVL2.5-8B and Qwen2-VL-7B on 400 SpookyBench videos for 10 epochs still yields 0% test accuracy, suggesting the limitation is architectural, not a simple distribution-shift or data-availability issue.

## Weaknesses

### Fatal
None.

### Major
1. **Lack of qualitative analysis of model outputs.** The paper reports only binary accuracy (0%).  It is crucial to understand *what* models actually output: do they produce noise-like tokens, generic phrases ("a scene"), empty responses, or confessions of uncertainty?  Without seeing model outputs, it is impossible to distinguish between a genuine temporal-processing failure and an inability to process the unusual input format (e.g., the ViT encoder might simply fail on noise-like frames, leading to degenerate next-token predictions).  Providing even a handful of example responses would greatly strengthen the claim.
2. **Fine-tuning experiment is under-reported.** The paper states that models were trained on 400 videos for 10 epochs using LlamaFactory, but reports no training accuracy, loss curves, or learning dynamics.  It is possible that the models never successfully fitted the training set (e.g., due to learning rate issues, collapse, or an uncanny loss landscape resulting from the noise inputs).  Without evidence that the models actually learned the training distribution, the fine-tuning result cannot be interpreted as proof of architectural limitation.
3. **Evaluation protocol requires more detail.**  For the *Images* and *Dynamic Scenes* categories, the paper uses a flexible set of acceptable labels, but it does not explain how these sets were constructed, how many labels are per video, or whether they were validated by multiple humans.  Also, the exact prompts used for each model are referenced only to an appendix that is not provided in the extracted text, making it impossible for reviewers to assess prompt quality.

### Minor
- **Human evaluation uses only 6 participants.** While the gap is so large that 6 participants are sufficient to establish the basic finding, a larger N would improve statistical robustness, especially for per-category performance.
- **SNR analysis (Section 3.3.1) feels tangential.** The detailed SNR metrics (Basic, Perceptual, Temporal Coherence, Motion Contrast) are presented with equations but are not convincingly connected to the models' failures.  The "binary threshold effect" analysis (Figure 4) is based on text detection and does not directly explain VLM behavior.  This section adds complexity without clear benefit.
- **Standard deviations reported as ±0.0 for all model scores.** This is unlikely; there may be variation across runs or individual videos, and the paper should report how the 0% was computed (e.g., mean over multiple seeds, exact match on the entire set, etc.).

### Trivial
- None of substance.

## Nice-to-Haves

- Include a small qualitative table of model outputs (e.g., two examples per category) to illustrate failure modes.
- Provide training curves for fine-tuning experiments, including training accuracy and loss.
- Conduct a control experiment where static noise frames (no motion) are presented alongside the animated versions to confirm that failure is motion-specific and not just due to the noise texture.
- Expand human evaluation to 20+ participants for better statistical power.

## Novel Insights

Beyond the paper’s own contributions, the fact that explicit temporal-encoding models (TimeChat, Momentor) also achieve 0% accuracy suggests that current temporal modules are merely spatial-feature aggregators that operate over frame-level tokens, not genuine temporal-pattern recognizers.  The fine-tuning results further imply that gradient-based training on this synthetic temporal task is insufficient to overcome the inductive bias of ViT-based encoders, which are inherently spatial.  This points toward the need for architectures with dedicated recurrent or dynamic mechanisms—perhaps drawing on neural circuit models of time perception—rather than transformer layers that treat time as a sequence dimension.

## Suggestions

1. **Provide a qualitative breakdown of model outputs** for a small set of SpookyBench videos.  Show whether models produce irrelevant tokens, repeat training-set labels, or fail to generate any meaningful response.
2. **Report training accuracy and loss curves** for the fine-tuning experiment.  If training accuracy remained at 0%, this would be a stronger indicator of an architectural bottleneck; if training accuracy was high but test accuracy was 0%, overfitting should be discussed.
3. **Clarify evaluation protocol for Image and Dynamic Scene categories:** list the acceptable label sets for a few example videos, and show that these sets are indeed correct and sufficient.
4. **Include the exact prompts used** (either in the main text or a supplemental document that is available to reviewers).

## Score and Decision

**Score:** 6  
**Decision:** Accept

The paper presents a novel, well-motivated diagnostic benchmark and a stark empirical finding that is likely to have significant impact on the community.  The weaknesses listed are major but addressable; they do not invalidate the core contribution.  With the requested qualitative and training-detail additions, the paper would be a strong accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>