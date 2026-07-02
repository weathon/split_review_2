## Summary
# Final Review Report

## Summary

This paper introduces SpookyBench, a synthetic benchmark designed to evaluate pure temporal understanding in Video-VLMs by encoding content (text, object images, dynamic scenes) exclusively in the motion of noise patterns across frames, where individual frames contain no discriminative spatial information. The key experimental finding is dramatic: while human participants achieve 98%+ accuracy on SpookyBench tasks, all 15+ evaluated Video-VLMs—spanning 2B to 78B parameters, open-source and commercial—score exactly 0% accuracy under both direct and chain-of-thought prompting, even after task-specific finetuning on 400 training videos. The paper argues this reveals a fundamental "time blindness" in current architectures that rely on spatial-first feature extraction and lack dedicated mechanisms for temporal pattern recognition. The benchmark is well-motivated and the 0% model accuracy result is striking, but several methodological limitations (small human sample, limited Dynamic Scenes category, missing experimental details, unclear SNR analysis, constrained response format) weaken the strength of the conclusions. The paper is best positioned as a diagnostic benchmark contribution that highlights an important blind spot, though the claim of "fundamental architectural failure" requires stronger evidence than currently provided.

## Strengths
**1. Well-motivated and important research question.** The paper identifies a genuine blind spot in current Video-VLMs: their reliance on spatial features for temporal reasoning. While existing benchmarks (TemporalBench, TVBench, VidHalluc) test temporal understanding, they still allow spatial shortcuts. SpookyBench's design—using motion patterns in structured-noise frames—cleanly eliminates spatial cues, providing the first benchmark that isolates pure temporal pattern recognition. This is a conceptually clean and valuable contribution to the evaluation ecosystem.

**2. Comprehensive model evaluation.** The paper evaluates an impressive 25+ model variants across 4 major families (LLaVA, InternVL, Qwen, and closed-source models), spanning 2B to 78B parameters, including both open-source and commercial systems. The consistent 0% result across this diverse set convincingly demonstrates that the failure is not specific to a particular architecture, scale, or training methodology.

**3. Strong human baseline with controlled methodology.** The human evaluation uses exact-match criteria and perceptibility ratings, with consistent results across 6 annotators (98.9% ± 0.7 for Text, 98.2% ± 1.1 for Images, 94.3% ± 3.1 for Dynamic Scenes). The perceptibility ratings (4.8/5 for Text) confirm that stimuli are clearly perceivable to humans, strengthening the argument that the failure is in machine vision rather than in the stimulus design.

**4. Informative temporal SNR analysis.** The four SNR metrics (Basic, Perceptual, Temporal Coherence, Motion Contrast) provide a rigorous framework for quantifying why these stimuli are challenging for computational models. The finding that Temporal Coherence is high for Dynamic Scenes (21.91 dB) while Motion Contrast is negative (-3.18 dB) offers specific guidance for which temporal properties future models should target.

**5. Finetuning experiment addresses domain-mismatch concern.** By showing that models finetuned on 400 SpookyBench videos still score 0%, the paper provides evidence that the failure is not merely due to distribution shift but reflects a deeper architectural limitation. This is a useful control experiment that strengthens the core claim.

**6. High dataset quality and transparency.** The dataset generation is deterministic, well-documented with clear algorithms (Algorithms 1 and 2), and uses reproducible specifications (960×540 resolution, 7.11s average duration, per-category frame statistics). The commitment to releasing the generation code will facilitate reproducibility and extension.

## Weaknesses
### W1. Headline 0% accuracy claim is not properly scoped (Major)
**Evidence:** Page 1 - Abstract, "state-of-the-art VLMs achieve 0% accuracy"; Page 6 - Section 4.1, "All prompts instruct models to respond with only 1-5 words identifying the content" and for non-video-native models, "We input sequences of multiple video frames simultaneously."
**Impact:** The 0% claim is the paper's central result and will be widely cited, but it is tested under two important constraints that the abstract and conclusion do not disclose: (1) a 1-5 word response limit, which may prevent models from expressing partial understanding through longer descriptions, and (2) frame-stacking for models that lack native video processing, which may degrade temporal perception. Without clear scope boundaries, readers may over-interpret the result as proving VLMs have zero temporal understanding in any setting.
**Fix:** Qualify the claim in the abstract and conclusion as "under a constrained 1-5 word response protocol with frame-based input." Also report what models actually output (even incorrect responses) to enable analysis of whether they detect *some* structure.

### W2. Critical experimental details missing (Major)
**Evidence:** Page 6 - Section 4.1, the frame sampling strategy for non-video-native models is unspecified ("We input sequences of multiple video frames simultaneously" with no number of frames, sampling method, or arrangement). Page 7 - Section 4.4, finetuning experiment lacks training split, loss function, learning rate, batch size, frozen layers, optimizer, and validation curves.
**Impact:** Reproducibility is compromised. Without knowing framerate/sampling details, other researchers cannot replicate the model evaluation protocol. The finetuning experiment—which is used to argue for "fundamental architectural inability"—is missing critical design parameters that could affect whether 0% accuracy reflects poor training configuration rather than inherent limitation.
**Fix:** (a) Specify exact frame count, sampling method, and arrangement for non-video-native models. (b) Provide a full training configuration table (LR, batch size, optimizer, epochs, scheduler, frozen components, train/val/test split) and report validation accuracy trajectory.

### W3. Text duplication and structural errors (Major)
**Evidence:** Page 8 - Section 5, the paragraph describing model failure modes ("Across all models tested, we observed attempts to extract information from individual frames...") appears twice verbatim, with Table 5 inserted between the two occurrences.
**Impact:** This is a clear copy-paste error that signals hasty preparation. For a submission claiming to be under double-blind review, such errors reduce reviewer confidence in the manuscript's overall carefulness. While not affecting scientific validity, it suggests insufficient proofreading.
**Fix:** Remove the duplicated paragraph (lines 202-203). Restructure Section 5 as: Results summary → Table 5 → Architectural Implications.

### W4. Small sample in Dynamic Scenes category (Major)
**Evidence:** Page 4 - Section 3.3, "Dynamic Scenes (12.6%, 57 videos)." Page 5 - Section 3.3.1, Dynamic Scenes have high variance in Motion Contrast (SD = 10.17 dB).
**Impact:** With only 57 videos in the most complex and naturalistic category (depth-map-based dynamic scenes), the statistical power to detect non-zero model performance is limited. The 95% binomial confidence interval for 0/57 extends to approximately 6.4%, meaning the true accuracy could be as high as ~6% without being detected. This category is also the most relevant for claims about real-world temporal understanding.
**Fix:** Report exact binomial confidence intervals for all accuracy estimates. Expand the Dynamic Scenes category or clearly acknowledge the limited statistical power as a limitation.

### W5. Human evaluation with only 6 participants (Minor)
**Evidence:** Page 7 - Section 4.2, "We recruited a total of six human participants for this study."
**Impact:** While the results are consistent across the 6 annotators, the sample is small and likely homogeneous (all from the authors' institution). For a benchmark that positions human performance as the gold standard (98% vs 0%), the human baseline should ideally be established with a larger, more diverse sample. The small N also precludes analysis of individual differences in temporal perception.
**Fix:** Add a limitation paragraph acknowledging the small sample size. Report per-participant demographics. Consider a larger online study (N ≥ 30) to strengthen the human baseline.

### W6. SNR analysis is confusing and internally inconsistent (Major)
**Evidence:** Page 5 - Section 3.3.2, "The words exhibited negligible detection (~0%) below 2.5dB SNR, but jumped to 85.7% accuracy above this threshold" and "Prompts performed best (40% accuracy)." The source of these accuracy numbers is unclear (human? model? algorithmic detector?). The text mentions "Chain-of-Thought reasoning improving general identification tasks" but Table 1 shows all models at 0% regardless of prompting. The figure data shows a step from 0.00 to 1.00 at 3 dB, conflicting with the text's "85.7%."
**Impact:** The SNR analysis is potentially the paper's most insightful section for understanding *why* models fail, but the unclear narrative—switching between detection phenomena, prompting strategies, and medical analogies—makes it hard to extract the scientific contribution. The apparent contradiction between the 85.7% accuracy and Figure 4's step function (0→1 at 3 dB) undermines confidence.
**Fix:** Clearly separate the SNR analysis into two parts: (a) metric definitions and video-level SNR statistics (clear), and (b) the relationship between SNR and detectability—explicitly stating whether the accuracy values in (b) come from humans, models, or an algorithmic motion-detection pipeline. Revise Figure 4's data to match the text.

### W7. Response format constraint may mask partial understanding (Minor)
**Evidence:** Page 6 - Section 4.1, "All prompts instruct models to respond with only 1-5 words identifying the content."
**Impact:** The 1-5 word constraint is a strong limitation. A model that partially perceives a pattern (e.g., detecting "there is moving text" but misreading it) would score 0% under exact match. Reporting what models actually output (even wrong answers) would provide valuable diagnostic information about what temporal features models can detect versus what they can decode. The paper currently provides no failure-mode analysis—only the 0% aggregate.
**Fix:** Add a qualitative analysis of model outputs: categorize errors (e.g., "perceives motion but no content" vs "hallucinates content" vs "random guess"). This would strengthen the paper's diagnostic value.

### W8. Overclaim in Conclusion about conventional benchmarks (Minor)
**Evidence:** Page 8 - Conclusion, "The benchmark effectively exposes the time blindness of current architectures that remain hidden in conventional evaluation settings where spatial features can provide shortcuts."
**Impact:** This claim suggests that SpookyBench reveals a failure mode that conventional benchmarks miss entirely. However, the paper does not compare model performance on SpookyBench to performance on conventional temporal benchmarks, so this conclusion is not directly supported by the data. It may be true, but it requires explicit comparison.
**Fix:** Either (a) add a comparative analysis showing that models perform well on conventional temporal benchmarks while failing SpookyBench, or (b) soften the claim to "SpookyBench exposes a previously unmeasured dimension of temporal understanding."

### W9. Title could be more informative (Minor)
**Evidence:** The title "Time Blindness: Why Video-Language Models Can't See What Humans Can" is catchy but does not convey that the paper's primary contribution is a benchmark.
**Impact:** Readers may expect an architectural solution or mechanistic explanation, neither of which the paper provides. A more descriptive title would better set expectations.
**Fix:** Consider "SpookyBench: A Benchmark Revealing Pure-Temporal-Understanding Blindness in Video-Language Models" or similar.

### W10. Neuroscience section is disconnected from the paper's contribution (Minor)
**Evidence:** Page 3 - Section 2.2, "Neuroscience research offers critical insights..." but no neuroscience insight is operationalized or tested.
**Impact:** The neuroscience section suggests the paper will draw design principles from biology, but SpookyBench does not test or derive any specific neuroscience-inspired hypothesis. The section remains decorative rather than functional.
**Fix:** Either (a) connect each cited neuroscience finding to a testable prediction about model behavior on SpookyBench, or (b) reposition as broader motivation and explicitly state that the benchmark is designed to test whether current architectures possess any form of these biological temporal-processing capabilities.

### W11. No novelty verification via external literature (Deferred - Retrieval Disabled)
Due to API limitations (Retrieval-Disabled Mode), external paper search could not be performed. The novelty assessment of SpookyBench relative to existing temporal reasoning benchmarks (TemporalBench, TVBench, VidHalluc, SVBench, VideoVista) is based solely on the paper's own descriptions and should be verified manually. Key questions for manual verification: (1) Are there existing benchmarks that also eliminate spatial cues for temporal evaluation? (2) Is the fine-tuning failure result consistent with known results from similar diagnostic benchmarks? (3) Are there relevant neuroscience-inspired video architectures that should have been compared or discussed?

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a well-motivated and important research question—whether Video-VLMs can understand purely temporal patterns without spatial cues—and the core experimental finding (universal 0% accuracy across 25+ models) is striking and likely reproducible. The SpookyBench benchmark is conceptually clean and fills a genuine gap in the evaluation ecosystem. However, the paper's impact is significantly weakened by several issues that prevent it from being a definitive reference:

- The headline 0% claim is not properly scoped to acknowledge the constrained 1-5 word response format and frame-stacking for non-video-native models, which could affect reader interpretation.
- Critical experimental details (frame sampling strategy, finetuning configuration) are missing, compromising reproducibility and the strength of the architectural-failure argument.
- A text duplication error in Section 5 indicates insufficient proofreading.
- The SNR threshold analysis (Section 3.3.2) is confusing and internally inconsistent, undermining one of the paper's most insightful contributions.
- The Dynamic Scenes category (57 videos) has limited statistical power.

These weaknesses are fixable with additional details, clearer writing, and more careful framing. The core contribution—a benchmark exposing pure-temporal-understanding failures—is valuable and should be published after addressing these concerns. The score reflects a borderline acceptance at a major venue (e.g., NeurIPS, CVPR) contingent on addressing the major weaknesses, particularly W1-W4 and W6.