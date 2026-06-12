## Summary

This paper introduces CaTS-Bench, a large-scale multimodal benchmark for context-aware time series captioning and reasoning. It is built from 11 real-world datasets, providing ~20k samples (16k train, 4k test) that pair numeric time series segments with rich metadata, line-plot images, and reference captions. The captions are primarily generated via a scalable oracle LLM pipeline with extensive quality validation (factual checks, human indistinguishability study, diversity analysis) and are supplemented by a human-revised subset of 579 test captions. Beyond captioning, the benchmark includes 460 multiple-choice Q&A questions across five categories. The authors evaluate a wide range of proprietary and open-source VLMs, finding that finetuning significantly improves open-source models but that VLMs generally fail to effectively leverage the provided visual inputs.

## Strengths

- **Comprehensive, large-scale multimodal benchmark filling a clear gap.** Existing TSC benchmarks (TADACap, TRUCE, TACO) are either domain-specific, pattern-only, or lack visual and metadata modalities. CaTS-Bench combines numeric series, metadata, line plots, and expressive captions at scale across 11 real-world domains, enabling more realistic evaluation of time series understanding.

- **Rigorous quality validation of the semi-synthetic captions.** The authors verify caption quality through multiple complementary studies: manual validation of 72.5% of test captions showing 98.6% factual accuracy, a blind human detectability study yielding near-random accuracy (41.1%), and comprehensive diversity/bias analyses. This goes well beyond typical benchmark construction practices and strengthens confidence in the reference captions.

- **Extensive evaluation across many models and settings.** The paper benchmarks 12+ VLMs (proprietary, pretrained open-source, and finetuned) on both the captioning task and Q&A tasks, with careful macro-averaging, robustness checks (variance across runs, paraphrasing sensitivity), and a human baseline for Q&A. The inclusion of a program-aided model (PAL) provides additional insight.

- **Important finding about VLM under-utilization of visual inputs.** The visual modality ablation and attention analysis convincingly show that current VLMs largely ignore line-plot images during captioning, relying instead on textual priors. This is a valuable, actionable finding for the community.

## Weaknesses

### Fatal
None.

### Major
1. **Human-revised subset is limited in coverage.** Only 579 test captions (from 4 out of 11 domains) are human-revisited. For the remaining 7 domains, evaluation must rely entirely on LLM-generated captions as reference. While validation studies support caption quality, the lack of human revision across all domains limits the gold-standard utility of the benchmark for those domains. This is particularly relevant because the human-revisited subset is presented as a key contribution.

2. **Q&A test suite is small, with very few questions per sub-task.** The entire Q&A set contains only 460 questions, and several sub-tasks have as few as 40 questions (amplitude, peak, mean, variance comparison). This small sample size limits statistical power and makes per-task accuracy estimates unreliable (a difference of 1-2 questions can shift accuracy by 2.5-5%). The filtering procedure (removing questions correctly answered by Qwen 2.5 Omni) may also introduce model-specific bias.

3. **The multimodal claim is somewhat undercut by the finding that visual input is non-essential.** The paper shows that for the captioning task, most models perform equally well or better without the line-plot image. While the authors frame this as a VLM limitation rather than a benchmark limitation, it raises a question: does CaTS-Bench actually require multimodal reasoning for its primary task? The Q&A plot-matching task does require visual grounding, but this is a small component (100 questions out of 460). The captioning task—the core of the benchmark—can be solved without the visual modality, which weakens the "multimodal benchmark" claim somewhat.

### Minor
1. **Numeric Score weights and tolerance are arbitrary.** The choice of λ_A=0.3, λ_R=0.7 and the 5% tolerance are reasonable but not formally justified. Sensitivity analysis to these parameters would strengthen the metric design.

2. **The evaluation prompt format could be a confounding factor.** All models use the same template-based prompt. Prompt sensitivity is a well-known issue in LLM evaluation, but the paper does not test alternative prompt formulations to verify result robustness.

3. **The "first large-scale multimodal" claim should be slightly tempered.** While CaTS-Bench is the first to combine numeric+text+visual at this scale, TACO (Dohi et al., 2025) has much larger temporal coverage and also provides expressive captions, just without visual modalities. The novelty is in the combination, not in each individual aspect.

## Nice-to-Haves
- Expand the human-revised subset to cover all domains for a fully gold-standard evaluation.
- Increase the Q&A test set size, particularly for the comparison sub-tasks, to at least 100 questions each.
- Test prompt robustness by evaluating a subset of models with multiple prompt variants.
- Include an analysis of what specific visual elements (if any) models attend to when they do use visuals, beyond the qualitative attention map analysis.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
- Consider releasing a version of the benchmark where the time series plot is essential for good performance (e.g., by hiding the raw numeric values from the model, forcing it to rely on the visual input for captioning). This would create a more genuinely multimodal test.

## Score and Decision

**Score:** 7  
**Decision:** Accept

This is a well-executed and thorough benchmark paper that makes a significant contribution to a relatively underserved area (time series captioning). The data curation pipeline is carefully designed and validated, the evaluation is comprehensive, and the finding about VLM under-utilization of visual input is valuable for the community. The main limitations—the partial coverage of human-revised captions and the small Q&A set—are non-fatal and can be addressed in future versions. The paper will be a useful resource for researchers working at the intersection of time series analysis and foundation models.

MY FINAL SCORE: 7.0</score>
MY FINAL DECISION: Accept</decision>