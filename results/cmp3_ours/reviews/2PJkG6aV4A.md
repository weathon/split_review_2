## Summary

This paper proposes a new method for evaluating societal bias in LVLMs that sidesteps safety guardrails. Instead of asking models to infer attributes of depicted persons (which triggers refusals in guardrailed models), the method uses person-irrelevant prompts (e.g., "Write a fictional story") while providing the image as user context. Across 20 models (16 open-source, 4 proprietary), 3 tasks (story generation, term explanation, exam-style QA), and 2 bias axes (gender, race), the method achieves zero refusals where prior benchmarks fail (Table 1: Claude 3.7 Sonnet refuses 81–100% of prior-benchmark prompts). The evaluation reveals that all models exhibit gender and racial biases in person-irrelevant tasks — e.g., stories for male users feature mechanics, those for female users feature nurses.

## Strengths

1. **The refusal problem is convincingly documented.** Table 1 is the paper's strongest empirical contribution, showing starkly that prior bias benchmarks (SBBench, ModScan, VLA-gender, Pairs) are essentially non-functional for guardrailed models. This finding is important and well-motivates the need for alternative approaches.

2. **The core idea is clever and practical.** Decoupling the evaluation task from the depicted person — using person-irrelevant prompts with the image as "user context" — is a simple and elegant way to avoid triggering safety guardrails while still measuring whether demographic information influences model outputs. The method's simplicity is a virtue for adoption.

3. **Comprehensive empirical scope.** Evaluating 20 models across 3 tasks and 2 bias axes represents substantial effort. The finding that bias is not monolithic (weak task-to-task correlations, Observation 2.3) is non-trivial and has practical implications for how bias should be measured.

4. **Zero refusal rates are convincingly demonstrated.** The claim is tested against the same models that refuse prior benchmarks, and the result is clean (Table 1: 0% for all models on the proposed method).

## Weaknesses

### Fatal
None.

### Major

None.

### Minor

1. **No statistical uncertainty or significance testing.** Bias scores are reported as point estimates without confidence intervals, standard errors, or significance tests (Table 2). This is consequential because many scores are small (e.g., exam-style QA ranges from 0.36 to 3.44 on a 0–100 scale) and could be within noise range. Claims like "proprietary models show lower bias" (Observation 2.1) rely on comparisons where the paper provides no way to assess whether observed differences are meaningful (e.g., GPT-5's exam-style QA gender score of 0.50 vs. InternVL3-38B's 0.88). Adding bootstrap confidence intervals would substantially strengthen the comparative claims.

2. **No control condition to establish the source of the bias signal.** The method's logic assumes that when a model receives an image + "I've attached my photo," it processes demographic cues and uses them to modulate outputs. However, there is no control condition (e.g., the same prompt with no image, or with an unrelated image like a landscape) to establish a baseline TVD. Without this, it is difficult to fully disentangle whether the measured TVD reflects genuine demographic bias vs. inherent output stochasticity. That said, the qualitative examples in Figure 2 (mechanic vs. nurse for male vs. female users; middle-class vs. poor for White vs. Black users) provide strong evidence the signal is real and stereotype-consistent, so this is a nice-to-have improvement rather than a fatal gap.

3. **Construct validity and framing could be sharper.** The paper presents itself as addressing limitations of prior benchmarks (line 97: "Our method addresses both limitations") without clearly acknowledging that it measures a complementary form of bias rather than a direct replacement. Prior benchmarks ask: "When shown an image of a person, does the model stereotype that person?" The proposed method asks: "When told a user's demographics via their photo, does the model's output on a person-irrelevant task differ across demographics?" These are related but different constructs. A model biased in visual recognition could score well here by ignoring user information, and vice versa. The paper would benefit from explicitly positioning the method as measuring *user-conditional output bias* — a form of bias that prior methods cannot measure due to refusals — rather than as a general-purpose replacement.

4. **LLM-as-judge validation is deferred to the appendix.** For story generation (attribute extraction) and term explanation (which explanation is "more technical"), the pipeline uses Qwen3-32B as a judge. The paper states that its judgments "align well with human judges" (line 143) but defers all numbers to Appendix D (stripped by the parser but present in the original submission). Given that the judge's own demographic biases could confound the measurements, this validation is critical enough to warrant main-text presentation (e.g., agreement statistics or accuracy vs. human judges).

5. **Proprietary vs. open-source comparison averages over unequal group sizes.** Observation 2.1 compares the average bias of 4 proprietary models against 16 open-source models. The claim ("proprietary models show lower bias") is reasonable as a general trend, but presenting raw averages without acknowledging this imbalance or providing per-model detail is somewhat misleading.

6. **Unequal sample sizes across tasks complicate cross-task comparisons.** Story generation uses 500 images per group, while term explanation and exam-style QA use 100. The statistical power to detect bias varies accordingly, making cross-task comparisons of bias magnitude (Observation 2.2: "Bias increases as tasks become more open-ended") potentially confounded by sample size differences alongside the genuine task effects.

7. **The false-negative case is not discussed in the main text.** A model could be genuinely biased in its visual recognition of people but produce output independent of user demographics simply by ignoring the image entirely. Such a model would score as "unbiased" under this method. The paper mentions this only via a footnote reference to Appendix H. A brief acknowledgment in the main text would strengthen the paper's intellectual honesty.

### Trivial
None.

## Nice-to-Haves

- Adding a no-image or unrelated-image control condition to establish a baseline TVD and strengthen causal claims.
- Adding bootstrap confidence intervals to each bias score in Table 2.
- Presenting LLM-judge human agreement statistics in the main text.
- Reframing the contribution as a complementary approach measuring user-conditional bias rather than a direct replacement for prior benchmarks.
- Discussing the false-negative limitation explicitly in the main text.

## Removed Points

These points from the input review were removed or demoted after verification against the paper:

1. **"Construct validity is a structural/fatal issue"** — The harsh critic argued the method measures a fundamentally different phenomenon and oversells itself as a replacement. After verification: the paper's framing could indeed be sharper, but "guardrail-agnostic societal bias evaluation" accurately describes what the method does (it works despite guardrails), and measuring user-conditional output bias is a legitimate form of societal bias evaluation. This is a minor framing concern, not a structural flaw. Demoted to Minor (#3 above).

2. **"No evidence that bias signals actually come from the image" as a major evidential gap** — The paper's qualitative examples (Figure 2 showing mechanic vs. nurse, middle-class vs. poor, etc.) provide strong evidence that the signal is real and stereotype-consistent. A no-image control would strengthen the paper but is not required to support the core claim. Demoted from Major to Minor (#2 above).

3. **"FairFace background context confounds" criticism** — The paper explicitly addresses this concern (line 95–97), noting that its design (person-irrelevant prompts with images as user context) reduces the impact of spurious image contexts compared to captioning-style prompts. The criticism ignores the paper's stated design rationale. Removed.

4. **"Term explanation ambiguity (audience calibration vs. harmful stereotyping)"** — The reviewer acknowledges this is "noted but not deeply explored." This is a nuanced philosophical distinction that doesn't threaten the core contribution. Removed.

## Novel Insights

The harsh critic raises a useful distinction that the paper itself does not fully articulate: the method measures bias in *user-conditional personalization* (does the model treat users differently based on perceived demographics?) rather than bias in *visual person recognition* (does the model stereotype people in images?). This distinction provides a clearer lens for understanding the method's scope and limitations. Additionally, the lack of statistical uncertainty reporting is correctly identified as a meaningful gap for a paper making comparative claims.

## Suggestions

1. Add bootstrap confidence intervals to each bias score in Table 2 to support comparative claims.
2. Add a no-image control condition to establish a baseline TVD.
3. Present LLM-judge human agreement statistics in the main text.
4. Sharpen the framing: present the method as measuring user-conditional output bias that prior methods cannot assess due to refusals, rather than as a direct replacement.
5. Discuss the false-negative limitation (biased models that ignore the image) explicitly in the main text.
6. Acknowledge the unequal group sizes when comparing proprietary vs. open-source averages and the unequal sample sizes across tasks.

## Score and Decision

**Calibration Anchors (retrieved from human-review corpus):**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| xx05gm7oQw (Debias your VLM with Counterfactuals) | 5.0 | Bracketing | Similar topic (VLM bias); rejected due to limited scope (gender only). Our paper has broader evaluation. |
| J6nKxekCCo (Intersectional Stereotypes in LLMs) | 3.0 | Bracketing | Bias evaluation but LLM-only; rejected with methodological concerns. Our paper is stronger. |
| kIboeK0Wzs (T2IEthics) | 4.4 | Bracketing | Ethics benchmark; rejected due to limited novelty. Our paper has a more novel contribution. |
| Xbl6t6zxZs (See It from My Perspective) | 6.0 | Bracketing + Narrowing | Cultural bias in VLMs; accepted. Cleaner experiments, similar scope. Our paper slightly weaker on experimental rigor. |
| 45rvZkJbuX (Cross-Modal Safety Mechanism Transfer) | 6.5 | Bracketing | Safety in VLMs; accepted with thorough analysis. Our paper is comparable in scope but has more methodological loose ends. |
| wvFnqVVUhN (Failures to Find Transferable Image Jailbreaks) | 6.25 | Bracketing | VLM safety/robustness; accepted. Extensive experiments, clear claims. Our paper has a similar level of contribution. |
| liuqDwmbQJ (ViLMA Benchmark) | 6.0 | Narrowing | VLM benchmark; accepted. Clean, well-scoped contribution. |
| kZEXgtMNNo (LLMs as Automated Aligners) | 6.0 | Narrowing | VLM alignment benchmark; accepted (8,5,5). |

**Round 1 Bracket:** 5.5–6.5.

This paper is clearly above the reject-level bias papers (3.0–5.0) — the core idea is genuinely novel, the empirical scope is substantial, and no fatal methodological flaws exist. It sits below the strongest VLM papers (8.0+) due to several minor but accumulative methodological gaps (no uncertainty estimates, no control condition, framing imprecision). Among the 6.0-range anchors, the paper is most comparable to "See It from My Perspective" and "ViLMA" in terms of contribution level, though those papers have cleaner empirical presentations.

**Final Score:** 6.0 — borderline accept. The paper makes a solid contribution (identifying the refusal problem, proposing a clever workaround, conducting broad evaluation) but would benefit from addressing the methodological gaps listed above.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>