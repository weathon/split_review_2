The calibration database is unavailable, so I'll proceed with my calibrated judgment. Let me finalize the review.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
// List only reasonable points. Rank by severity.
// Not every paper has weaknesses at every tier. Leave a tier empty (or write "None") if nothing qualifies.

### Fatal
// Errors that invalidate the paper's core claims or results.
// Examples: fundamentally flawed methodology, unsupported central claim, incorrect proofs, data fabrication concerns.
// Most papers have none. Leave empty if none apply.

### Major
// Issues that a reviewer would weigh against acceptance, and that the authors should fully resolve in a rebuttal.
// Examples: missing critical baseline, overclaimed scope unsupported by experiments, significant methodological gap.
// Not every paper has major weaknesses. Do not invent them to fill this section.

- weakness 1 — why it matters
- weakness 2 — why it matters

### Minor
// Issues worth the authors' attention but unlikely to change an accept/reject decision.
// Examples: addressable in rebuttal, limited scope of one experiment, unclear phrasing of a claim, missing ablation that would strengthen but not invalidate.

- weakness 1 — why it matters

### Trivial
// Small issues the authors should fix but that carry no weight in evaluation.
// Examples: typos, minor notation inconsistencies, suboptimal figure choices, small presentation issues.

- weakness 1

## Nice-to-Haves
- suggestion that would improve but is not a core flaw

## Removed Points
Include something like this "These points are flagged to be removed, treat them with caution"
Weaknesses that are removed keep the details of the S/W just in case they are useful 

## Novel Insights
One paragraph synthesizing genuinely novel observations.
If no genuinely novel insight emerges from the reviews beyond the paper's own contributions, write
"None beyond the paper's own contributions."

## Suggestions
- specific actionable suggestion

Here is my final consolidated review.

---

## Summary

This paper addresses a practical and growing problem: existing LVLM societal bias benchmarks use attribute-inferring prompts ("Is this person a CEO or a secretary?") that trigger safety-guardrail refusals in modern models, especially proprietary ones like GPT-5 and Claude. The authors propose a clever solution — replace attribute-inferring prompts with person-irrelevant prompts ("Write a fictional story about an imaginary person") while attaching face images as user context rather than task subject — achieving zero refusals across all tested models. The method is instantiated across three diverse tasks (story generation, term explanation, exam-style QA) and evaluated on 20 recent LVLMs. Key findings include that all models exhibit bias, proprietary models show lower but non-zero bias, bias does not generalize across tasks, and model size/performance do not reliably explain bias.

## Strengths

1. **Clear empirical demonstration of the refusal gap (Table 1):** The paper systematically measures refusal rates of six LVLMs on four existing benchmarks, finding rates of 49–100% for proprietary models and high rates even for recent open-source models. The proposed method achieves exactly 0% refusals across all models. This paired comparison is the central quantitative evidence that prior benchmarks are unreliable for guardrailed models and that the proposed solution solves the stated problem.

2. **Controlled demographic balancing (Section 4.1):** When evaluating bias along one axis (e.g., gender), non-target demographic distributions (race, age) are explicitly matched across comparison groups. This addresses a known confound in captioning-style alternatives and makes the bias measurements cleaner than those from prior approaches.

3. **Weak cross-task bias correlations (Figure 3, Observation 2.3):** Task-wise correlations range from −0.11 to 0.21, empirically demonstrating that bias is not a monolithic property — a model with low bias on story generation can have high bias on exam-style QA. This finding validates the multi-task design and goes beyond what single-task benchmarks provide.

4. **Large-scale evaluation across 20 LVLMs (Table 2):** The paper evaluates 16 open-source models (7B–38B across 6 families) and 4 proprietary models, consistently finding non-zero bias across the board. The systematic comparison (proprietary vs. open-source, across tasks and demographics) provides a useful empirical landscape that prior work could not produce for guardrailed models.

5. **Qualitative examples concretely illustrating the phenomenon (Figure 2):** Generated outputs (e.g., GPT-4o producing *mechanic* for male users vs. *nurse* for female users; Claude 3.7 giving more technical NLP explanations for White users than for Southeast Asian users) bridge the quantitative TVD scores to tangible, recognizable stereotype behavior — this is a simple but effective communication of the finding.

## Weaknesses

### Fatal
None.

### Major

1. **No uncertainty quantification for the headline bias scores (Table 2).** All TVD scores are reported as point estimates without confidence intervals, error bars, or significance tests. The paper makes comparative claims — "proprietary models show lower bias" (average 18.99 vs. 29.29 for story generation gender), and individual model comparisons (GPT-5 at 14.53 vs. Claude 3.5 at 14.33) — without any variance estimates. With 500 images per group for story generation and 100 per group for the other tasks, bootstrapped confidence intervals or at minimum standard errors should be reported. This is especially important because the TVD scores span a wide range (0.5–48) and differences between adjacent models are often 1–3 points, making it unclear which comparisons are reliable.

### Minor

1. **Construct framing could be more precise.** The paper presents itself as measuring "societal bias" in the same sense as prior work, but the method measures a distinct phenomenon: whether models adjust their outputs based on a user's profile picture in tasks that have nothing to do with the person depicted. Prior benchmarks measured whether models stereotype the *person in the image*. These are related but different constructs — a model could stereotype people in images without treating users differently based on their profile pictures, and vice versa. The paper acknowledges this implicitly in Figure 1 (framing it as user-context bias) but does not discuss the implications or clarify the relationship. This does not invalidate the method — user-facing differential treatment is a real and important form of bias — but the framing overclaims alignment with the specific construct that prior work studied.

2. **No validation of bias scores against prior benchmarks.** The paper compares refusal rates with prior benchmarks (Table 1) but never compares the *bias scores themselves* against scores from prior methods on models where both work (e.g., LLaVA-1.6 has 0% refusal on VLA-gender). Such a comparison would provide evidence about construct alignment and help calibrate what the proposed method's scores mean relative to the established literature.

3. **Low-performing models trivially achieve low bias on exam-style QA.** The paper honestly excludes LLaVA-1.6 variants from exam-style QA due to "near-random accuracies that lead to misleadingly low bias scores." This reveals a genuine limitation: floor effects compress all groups to similar accuracies, producing TVD ≈ 0 regardless of the model's true bias. The task cannot meaningfully measure bias in models at or near chance performance. The paper acknowledges this but does not discuss solutions (e.g., conditional analysis on correctly-answered questions).

4. **Limited evidence for the contextual-confounds claim.** The paper asserts that treating images as user context (rather than the subject of the prompt) "reduces the impact of spurious image contexts." However, no experiment or analysis is provided to verify this reduction. Since images still contain non-person cues that could correlate with demographics, this claim would benefit from empirical support.

5. **LLM judge (Qwen3-32B) for term explanation could embed its own biases.** The paper uses an LLM to judge which explanations are "more technical." This judge could itself have demographic biases. The paper claims alignment with human judges (Appendix D, stripped by the parser), but agreement rates and details about the diversity of human judges are not in the main paper.

### Trivial
None.

## Nice-to-Haves
- Adding bootstrapped confidence intervals to all TVD scores in Table 2.
- Validating the method by comparing bias scores against prior benchmarks on models where both methods work.
- Adding a conditional analysis or calibration-based correction for the exam-style QA task to handle floor effects.
- Discussing the user-facing vs. person-depicted construct distinction more explicitly in the paper.

## Removed Points
These points are flagged to be removed; treat them with caution if you encounter them elsewhere.

1. **Personalization vs. bias (Hypothesis 1 conflates bias with personalization):** The harsh critic argued that some demographic disparities could be benign personalization (e.g., making stories relatable) rather than harmful bias. **Reason for removal:** The tasks are explicitly person-irrelevant, so any demographic conditioning is definitionally problematic. The examples shown (mechanic/nurse stereotypes) are clearly harmful stereotyping. In the context of societal bias evaluation, differential treatment by demographics in task-irrelevant settings is precisely what constitutes bias.

2. **TVD computation for exam-style QA not clearly specified:** The harsh critic argued the TVD application to exam-style QA was vague. **Reason for removal:** The paper explicitly references Appendix A for the TVD definition and the full formula. The appendix was stripped by the parser, so this is not a valid criticism of the submission as originally written.

3. **Image quality and presentation effects:** Speculative concern about whether models respond to image quality or lighting rather than demographics. **Reason for removal:** No evidence supports this concern; FairFace is a standardized dataset with controlled images.

4. **Cost and reproducibility concerns about proprietary models (API costs, versioning).** **Reason for removal:** These are practical logistics questions, not methodological weaknesses, and are not expected in a conference submission.

5. **Figure 3 asymmetric correlation values:** The harsh critic flagged asymmetric values in the figure description (e.g., 0.49 vs. 0.60 for the same pair). **Reason for removal:** The paper's textual claim is that task-wise correlations are weak (−0.11 to 0.21), which is consistent. The figure description details appear affected by parser artifacts.

6. **Generic strengths from the Strength Finder** (e.g., "addresses an important problem," "the paper is well-written"): **Reason for removal:** These are superficial and not specific to the paper's concrete contributions.

## Novel Insights

None beyond the paper's own contributions. The key novel findings — that cross-task bias correlations are weak, that continuous monitoring may be more important than one-time safety alignment, and that all tested models exhibit non-zero bias even with guardrails — are already clearly presented in the paper.

## Suggestions

1. **Add bootstrapped confidence intervals to Table 2.** This is the single most important technical addition. With 500/100 samples per group, bootstrapping is straightforward and would substantially strengthen the reliability of all comparative claims.

2. **Sharpen the construct framing.** Explicitly position the method as measuring *user-facing differential treatment* or *user-context bias* and discuss how this relates to (but is distinct from) person-depicted stereotyping. A brief paragraph in Sections 1 and 5 would suffice.

3. **Validate against prior benchmarks.** On models where prior benchmarks have low refusal rates (e.g., LLaVA-1.6 on VLA-gender), compute bias scores using both the proposed method and the prior method, and report the correlation. This would provide strong evidence about what the proposed scores capture.

4. **Include LLM judge validation details in the main paper.** Report the human agreement rate, sample size, and human judge demographics for the term explanation evaluation in the main paper rather than relegating to the appendix.

## Score and Decision

Since the calibration database was unavailable, I calibrated based on my understanding of ICLR standards. The paper makes a genuine contribution: it identifies a real and growing problem (guardrail refusals invalidating existing bias benchmarks), proposes a novel and clever solution, and provides comprehensive empirical evidence. The core result (zero refusals, Table 1) is unambiguous and well-documented. The weaknesses are all addressable — the most significant is the lack of uncertainty quantification, but this does not invalidate the main findings (the zero-refusal result needs no CIs, and the overall trends in bias scores are clear). The paper is clearly a solid accept: above borderline but not flawless.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>