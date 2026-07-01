## Summary

The paper addresses a critical blind spot in existing societal bias benchmarks for large vision-language models (LVLMs): strong safety guardrails cause models to refuse attribute-inferring prompts (e.g., “Is this person a CEO or a secretary?”), making evaluation unreliable. The authors propose a guardrail-agnostic evaluation method that replaces such prompts with person-irrelevant tasks (story generation, term explanation, exam-style QA) and treats images as provisional user information rather than the subject of the prompt. This design achieves zero refusals across both open-source and proprietary models. Evaluating 20 recent LVLMs, they find all models exhibit gender and racial bias—though proprietary models tend to be less biased—and show that bias does not reliably correlate with model performance or size.

## Strengths

- **Timely and practical problem identification.** The paper clearly demonstrates that existing bias benchmarks fail on safety-guarded models (Table 1 shows refusal rates up to 100% for Claude and over 90% for several open-source models). This is a genuine and growing issue as guardrails become ubiquitous.
- **Elegant and effective methodological shift.** By decoupling the evaluation task from the depicted person and using images only as user context, the method avoids triggering guardrails while still measuring how demographic cues influence outputs. The three task instantiations (story generation, term explanation, exam-style QA) span a useful range of open-endedness.
- **Comprehensive evaluation.** 20 models (16 open-source, 4 proprietary) are tested across gender and race axes. The experiments include refusal rate comparisons, detailed bias scores, qualitative examples, and correlation analyses. The results consistently show that proprietary models are less biased but still far from fair.
- **Thoughtful discussion of bias sources.** The paper goes beyond simply reporting numbers to hypothesize that continuous monitoring and iterative refinement (rather than one-time safety alignment) may be key drivers of bias reduction, contrasting proprietary and open-source development cycles.
- **Strong empirical evidence for the method’s necessity and validity.** Zero refusals are achieved across all models and tasks, and the extracted bias patterns (e.g., mechanic vs. nurse for gender, lawyer vs. community health worker for race) align with known stereotypes, supporting the ecological validity of the approach.

## Weaknesses

### Fatal
None.

### Major
- **Potential confound: models may simply ignore the image in more constrained tasks.** In exam-style QA (multiple-choice), models might skip processing the attached user photo altogether, artificially lowering the measured bias. The paper notes that exam-style QA shows the lowest bias scores, but this could partly reflect task design rather than true fairness. The dependence of the evaluation on the model’s propensity to attend to the image is not explicitly controlled or measured.

- **Reliance on an LLM assistant for attribute extraction and technicality judgment.** The method uses Qwen3-32B to extract character attributes from stories and to judge which explanation is more technical. While the appendix reportedly validates alignment with human judges, the main text lacks details on this validation (inter-annotator agreement, potential biases in the LLM judge). If the judge itself has systematic preferences, the bias scores could be confounded.

### Minor
- **The claim that “bias in one task does not generalize to others” is supported by weak correlations (r between -0.11 and 0.21).** However, the sample size is only 20 models, so these correlations have wide confidence intervals. The statement is plausible but not strongly established given the limited statistical power.
- **The discussion of continuous monitoring as a driving factor for lower bias in proprietary models is speculative.** The paper acknowledges this and frames it as a hypothesis, but it could be strengthened by more concrete evidence (e.g., release dates, documented updates). This does not detract from the main contribution.

### Trivial
- Figure 3 (correlation diagram) is somewhat hard to parse with many numbers; a simpler table might have been clearer. This is a minor presentation issue.

## Nice-to-Haves

- Include an ablation study where the image is not provided at all, to quantify how much the image itself (vs. the prompt alone) contributes to the bias measured.
- Provide confidence intervals or statistical significance tests for the bias scores and refusal rates.
- Extend the analysis to other demographic axes (e.g., age, intersectional groups) to demonstrate generality.

## Novel Insights

None beyond the paper’s own contributions. The core insight—that guardrails make direct bias evaluation impossible and that a context-shifting approach avoids refusals—is the main novelty. The finding that bias is not monolithic across tasks or correlated with model size/performance is a useful empirical observation, but it has been noted in related work on LLM bias. The hypothesis that continuous monitoring rather than one-time alignment reduces bias is interesting but not yet substantiated.

## Suggestions

- **Control for image attention.** In exam-style QA, explicitly check whether the model’s output changes when the image is replaced with a blank/dummy image, to verify that the model actually uses the user demographic information. This would strengthen the validity of the low bias scores in that task.
- **Validate the LLM judge more transparently in the main text.** Report a brief summary of human agreement rates for attribute extraction and technicality judgment, or show that the judge’s own biases are small relative to the measured effect sizes.
- **Report refusal rates per task individually** (story generation, term explanation, exam-style QA) rather than only an aggregate “Ours” column to confirm that zero refusals hold across all three.

## Score and Decision

The paper makes a clear, original, and practically important contribution. The core problem is well-motivated, the proposed solution is effective and simple to adopt, and the evaluation is thorough across many models. The weaknesses (potential confound in exam-style QA, reliance on LLM judge) are manageable and do not invalidate the main claims. The paper is well-written and will be of high value to the community.

MY FINAL SCORE: <score>8.5</score>
MY FINAL DECISION: <decision>Accept</decision>