## Summary

The paper identifies a genuine methodological crisis: existing societal bias benchmarks for LVLMs use attribute-inferring prompts that are increasingly refused by safety-guarded models (Table 1 shows Claude 3.7 Sonnet refuses 100% of SBBench prompts). The proposed solution is elegant: decouple the evaluation task from the depicted person by using person-irrelevant prompts (e.g., "Write a fictional story") while treating the image only as user context. This achieves zero refusals across all 20 tested models. The framework is instantiated across three tasks and applied to 20 recent LVLMs, revealing that all models exhibit bias (e.g., male users → *mechanic*, female users → *nurse*), though proprietary models show lower bias than open-source ones.

## Strengths

1. **A well-diagnosed, consequential problem with clear evidence.** Table 1 is not hypothetical: Claude 3.7 Sonnet refuses 100% of SBBench prompts and 98% of ModScan and VLA-gender prompts. Even open-source models like Qwen2.5-VL-32B show 90%+ refusal rates on several benchmarks. This concretely demonstrates that attribute-inference-based benchmarks are becoming unreliable as guardrails strengthen — a real methodological crisis the paper identifies and quantifies.

2. **An effective solution to the stated problem.** The core idea — switching from attribute-inferring prompts to person-irrelevant prompts and re-framing the image as user context — is simple, well-motivated, and validated to achieve zero refusals across all 20 models. This is a clean, transferable design pattern.

3. **Broad and systematic evaluation.** Evaluating 20 models (16 open-source, 4 proprietary) across three tasks gives the empirical findings genuine breadth. The explicit control for confounding demographics (aligning race/age distributions when measuring gender bias, Sec. 4.1) is methodologically responsible.

4. **Informative cross-task analysis.** The finding that bias scores correlate weakly across tasks (r = −0.11 to 0.21) is non-obvious and practically important: it shows that a single bias test is insufficient and that different tasks probe different mechanisms.

## Weaknesses

### Fatal

None.

### Major

None. The core methodological contribution is sound and the qualitative findings are consistent with stereotyping. The weaknesses below affect confidence in some comparative and quantitative claims but do not invalidate the paper's central contribution.

### Minor

1. **No uncertainty quantification for any reported score.** All bias scores in Table 2, all correlation coefficients in Figs. 3–4, and all comparative claims (e.g., "proprietary models show lower bias") are reported as point estimates with no confidence intervals, standard errors, or significance tests. The TVD scores themselves have sampling uncertainty from (a) the finite set of images per group (500 for story generation, 100 for term explanation), (b) the finite set of prompts, and (c) the LLM-based attribute extraction pipeline. Without any measure of variance, the reader cannot assess whether the differences the paper discusses — e.g., GPT-5's gender bias of 14.53 vs. Claude 3.5 Sonnet's 14.33 in story generation — are meaningful or within noise. The correlation analyses (n=20 models) similarly lack any indication of statistical reliability. This weakens confidence in comparative claims but does not threaten the method's validity.

2. **LLM evaluator confound is insufficiently characterized in the main text.** For story generation and term explanation, the paper relies on Qwen3-32B to extract character attributes and judge explanation difficulty. The main text states only that "Appendix D confirms that its judgments align well with human judges" (line 143). Without details in the main body — sample size, agreement metric, whether judges were shown user demographics — the risk that the evaluator LLM's own biases systematically amplify or attenuate measured bias cannot be assessed from the paper as presented. The appendix (stripped in extraction) may address this fully, but the main text should include key figures.

3. **No specification of sampling/generation parameters.** The paper does not state whether model responses were sampled with temperature > 0 or generated greedily, nor whether multiple runs were averaged. For open-ended generation tasks (story generation, term explanation), this is a critical methodological detail affecting both reproducibility and the variability of results. The only mention of randomness is for sampling prompts from prior benchmarks.

4. **Construct validity nuance unaddressed for story generation.** The paper defines bias as "statistical disparity in outputs across user demographics" (Hypothesis 1). For story generation, a model could produce outputs correlated with user demographics as an attempt at *personalization* or *user modeling* (creating relatable characters) rather than reflecting harmful stereotyping. The paper's qualitative findings (men→*mechanic*, women→*nurse*, Black users→*community health worker*, White users→*lawyer*) are consistent with stereotyping rather than benign identity-matching, which partially resolves this. However, the paper does not explicitly acknowledge this distinction or argue why the observed patterns go beyond personalization. For term explanation and exam-style QA, the case is much stronger — there is no plausible personalization justification for differential explanation depth or QA accuracy.

5. **No discussion of vision-encoder-specific biases.** The paper uses face-centric images from FairFace. Known issues with vision encoders (e.g., less accurate feature extraction for darker skin tones, differential processing across demographic groups) could introduce measurement error in the bias scores. This is a relevant methodological caveat that the paper does not discuss.

### Trivial

- The conclusion (Sec. 6) states that "continuous monitoring and iterative refinement... may play a key role in reducing bias" more assertively than the evidence supports. The discussion section (Sec. 5) appropriately frames this as "a plausible explanation," so this is a minor framing issue in the conclusion only.

## Nice-to-Haves

- **Bootstrap confidence intervals or standard errors** for the bias scores in Table 2 would immediately strengthen the comparative claims and allow readers to assess which model differences are reliable.
- **Ablation of the LLM evaluator** (e.g., running attribute extraction with GPT-4o or Claude on a subset and comparing resulting bias scores) would directly address the evaluator-confound concern.
- **Explicit discussion of the personalization-vs-stereotyping distinction** for story generation would strengthen the paper's construct validity argument.

## Removed Points

- **Background confounds concern** (the paper already acknowledges "reducing the impact of spurious image contexts" in line 97 — this is not a gap).
- **Experimental capacity / computational cost observation** — not a substantive weakness; the scale is appropriate for the claims made.
- **"Three tasks probe different mechanisms"** — this is a feature of the design, not a weakness.
- **Table 2 scale interpretation** — The 0–100 scale is clearly stated ("multiplied by 100 (0 = no bias, 100 = maximum bias)") in the table caption — this is sufficient.
- **Observation 2.2 causal claim** — the paper says "reflects," not "is caused by." The language is appropriately correlational.
- **Missing related works** — cannot be verified without external sources.

## Novel Insights

The most novel methodological insight from the review process is that the personalization-vs-stereotyping ambiguity in story generation is partially resolvable through the pattern of results themselves. The fact that the observed occupational disparities map onto real-world stereotypes (mechanic/nurse, lawyer/community health worker) rather than simple demographic mirroring (e.g., Latina user → Latina protagonist) constitutes a form of construct validity evidence that the paper could make more explicit. Beyond this, the reviews reinforce rather than add to the paper's own contributions.

## Suggestions

1. Add bootstrapped 95% confidence intervals to all bias scores in Table 2 and to the correlation values in Figs. 3–4.
2. Report the sampling/generation parameters (temperature, top-p, number of runs) used for all model queries.
3. Either move key details of the human agreement study (sample size, agreement metric, inter-rater reliability) into the main text, or run a robustness check with a second evaluator LLM.
4. Add a brief acknowledgment in Sec. 3.1 that statistical disparity in story generation could in principle reflect benign personalization, and argue why the specific observed pattern (occupational stereotypes) goes beyond what personalization would predict.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>