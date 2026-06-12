## Summary

This paper identifies a critical blind spot in existing LVLM bias benchmarks: safety guardrails cause high refusal rates on attribute-inferring prompts (e.g., “Is this person a CEO or a secretary?”), making evaluations unreliable for proprietary and increasingly for open-source models. The authors propose a guardrail-agnostic evaluation method that uses _person-irrelevant prompts_ (e.g., “Write a fictional story”) and treats the image only as user context, thereby avoiding refusals while still detecting output disparities across demographic groups. The method is instantiated across three tasks (story generation, term explanation, exam-style QA) and applied to 20 recent LVLMs, revealing that all models exhibit gender and racial bias, though proprietary models show lower bias than open-source ones.

## Strengths

- **Important and timely problem**: High refusal rates on existing bias benchmarks (Tab. 1, e.g., Claude 3.7 Sonnet refuses 81–100% of prompts) are a real and growing obstacle. The paper correctly identifies this blind spot and proposes a practical solution.
- **Clever and principled method**: Decoupling the task from the depicted person by using person-irrelevant prompts and treating images as user context is a simple yet effective idea. It elegantly bypasses guardrails while still measuring undesirable demographic conditioning.
- **Comprehensive evaluation**: 20 models (open-source 7B–38B and proprietary) are evaluated on three diverse tasks with controlled demographic distributions, yielding a rich set of observations (e.g., proprietary models are less biased but still biased, bias correlations across tasks are weak, gender and racial biases are correlated).
- **Clear and actionable recommendations**: The discussion distinguishes between one-time safety alignment and continuous monitoring, and the framework is positioned as a tool for both pre-deployment testing and post-deployment auditing.

## Weaknesses

### Fatal
None.

### Major
1. **Potential confound from non-demographic image cues**: Even with person-irrelevant tasks, images may contain background, lighting, or expression cues that correlate with demographics. For exam-style QA, such cues could affect model performance independent of user identity, introducing a confound. The paper claims this issue is “reduced” but does not control for it (e.g., by using synthetic/anonymized avatars or cropping to faces only). This weakens the claim of fair comparison across groups.
2. **Reliance on an LLM assistant for attribute extraction and technicality judgment**: In story generation and term explanation, the LLM assistant (Qwen3-32B) is used to extract occupations/personalities or judge which explanation is more technical. Any bias or inaccuracy in the assistant (especially if it shares training data or biases with the target LVLMs) would propagate into the bias scores. The validation in Appendix D is not described in the main paper and may be insufficient.

### Minor
1. **No statistical tests or confidence intervals**: Bias scores in Tab. 2 are reported as point estimates without error bars. With finite sample sizes (e.g., 500 stories per demographic group), some variation is expected, and it is unclear whether differences between models are statistically significant. This is important for ranking models reliably.
2. **Unclear boundary between bias and legitimate personalization**: The assumption that any demographic-dependent output variation in person-irrelevant tasks is undesirable bias may be too strong. For example, adjusting explanation difficulty based on perceived user background could be beneficial personalization. The paper does not discuss this nuance, though the observed stereotypical patterns (e.g., male→mechanic, female→nurse) are clearly harmful.
3. **Speculative discussion on continuous monitoring**: The claim that “continuous monitoring and iterative refinement is a critical factor” for lower bias in proprietary models is plausible but not directly supported by evidence. Many confounds (training data, architecture, compute) differ between proprietary and open-source models, so the attribution to monitoring alone is weak.
4. **Ignoring intersectional demographics**: Only binary gender and seven race categories are analyzed separately. Intersectional combinations (e.g., Black women) are not explored, limiting comprehensiveness.

### Trivial
None.

## Nice-to-Haves

- Validate the LLM assistant’s judgments with human evaluation across demographic groups to rule out assistant bias.
- Use face-only or synthetic avatars to control for background confounds.
- Report confidence intervals (e.g., bootstrap) for bias scores.
- Explore intersectional bias (e.g., gender × race) to reveal compound disparities.

## Novel Insights

Beyond the paper’s own contributions, the finding that bias across tasks (story generation, term explanation, exam-style QA) is only weakly correlated (r ≈ –0.11 to 0.21) is genuinely insightful: it demonstrates that societal bias is **not a monolithic property of a model** but manifests differently depending on the task context. This has practical implications—evaluators must use diverse tasks rather than a single benchmark to capture the full bias profile. The strong correlation between gender and racial bias within the same task (r up to 0.93) further suggests that biases along different demographic axes share common underlying mechanisms, pointing toward integrated rather than separate debiasing strategies.

## Suggestions

1. Provide bootstrap confidence intervals or standard errors for the bias scores in Tab. 2 to enable principled model comparisons.
2. Discuss or experimentally control for the influence of non-demographic image content (e.g., by using only face-cropped images or adding a controlled baseline with neutral avatars).
3. Present a more thorough validation of the LLM assistant used for attribute extraction and judgment, including agreement with human raters across different demographic groups.
4. Explicitly address the boundary between undesirable bias and potentially acceptable personalization, and motivate why the observed disparities (especially the stereotypical patterns) are harmful.

## Score and Decision

The paper addresses a timely and important problem with a clever, practical solution, and provides a comprehensive evaluation across many models and tasks. The weaknesses (confound from image backgrounds, reliance on an LLM judge, lack of error bars) are significant but not fatal; they can be addressed with additional controls or discussion. The contribution is solid and the findings are valuable for the community.

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>