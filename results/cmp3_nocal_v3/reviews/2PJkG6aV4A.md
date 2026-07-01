## Summary

This paper identifies a critical blind spot in existing LVLM bias benchmarks: high refusal rates (49–100%) for guardrailed proprietary models like GPT-5 and Claude 3.7 Sonnet, and increasingly for recent open-source models. The authors propose a clean technical solution: replace attribute-inferring prompts with person-irrelevant prompts (e.g., "Write a fictional story about an imaginary person") while attaching the image only as user context rather than the object of inquiry. This method achieves zero refusals across all 20 evaluated models. The experimental scope is substantial, covering story generation, term explanation, and exam-style QA across 16 open-source and 4 proprietary LVLMs, revealing systematic demographic conditioning even in safety-aligned models.

## Strengths

- **A genuine problem, convincingly demonstrated.** Table 1 provides striking evidence: refusal rates of 49–100% on proprietary models and 35–94% on recent open-source models for standard benchmarks (SBBench, ModScan, VLA-gender, Pairs). This empirically grounds the paper's motivation and shows that the issue is not hypothetical.

- **The core technical idea is effective and clean.** Decoupling the evaluation task from the depicted person — replacing attribute-inferring prompts with person-irrelevant prompts and using images only as user context — is a simple yet clever solution. The zero-refusal result across all 20 models (Table 1) is unambiguous and demonstrates that the method achieves its stated objective.

- **Substantial empirical scope.** Evaluating 20 recent LVLMs (16 open-source from 7B–38B, 4 proprietary) across three diverse tasks provides a broad descriptive picture. The inclusion of model families at multiple scales enables cross-model comparisons that strengthen the paper's findings.

- **Concrete qualitative examples strengthen the quantitative results.** Figure 2 shows generated stories and explanations that clearly illustrate the kind of stereotyping the method surfaces (e.g., mechanic for male users vs. nurse for female users; more technical NLP explanations for White users).

## Weaknesses

### Fatal
None.

### Major

- **The asymmetric Pearson correlations in Figure 3 are mathematically impossible and suggest an analysis error.** For standard Pearson correlation r, r(X,Y) must equal r(Y,X). Yet the paper reports striking asymmetries in the gender-bias task correlations: Exam QA → Term Exp. (r = 0.08) vs. Term Exp. → Exam QA (r = 0.93), and Story Gen. → Exam QA (r = −0.11) vs. Exam QA → Story Gen. (r = 0.11). The 0.08 vs. 0.93 discrepancy in particular cannot arise from standard Pearson r of the same two variables. The authors must clarify whether these are Pearson correlations, some other directional measure, or whether there is a labeling/calculation error. This casts doubt on Observation 2.3 (task correlations) and Observation 2.4 (gender–race correlations), though the paper's core empirical findings (Tables 1 and 2) are independent of this analysis.

### Minor

- **No statistical inference or uncertainty quantification is reported anywhere.** TVD scores (Table 2) and Pearson correlations (Figs. 3, 4) are presented as point estimates without confidence intervals, p-values, or bootstrapped uncertainty. For small scores like GPT-5's exam-style gender bias (0.50 on a 0–100 scale) or racial bias (0.36), the reader cannot determine whether these are meaningfully different from zero or within the range of random variation for the given sample sizes (e.g., 100 questions per domain). A permutation test or bootstrap-based confidence intervals would substantially strengthen the evidential value of the results.

- **The exam-style QA task is underspecified.** The exact prompt format joining the user image with the MMLU question is not provided in the main text (full details are relegated to the stripped appendix). This is important because presenting an irrelevant face image during a math exam question creates an unnatural multimodal interaction — accuracy differences across demographics could reflect differential model confusion or attention effects rather than reasoning bias. No control condition (same questions without any image) is included to establish a baseline. The paper should clarify the prompt format and ideally include a no-image ablation.

- **The LLM-as-judge pipeline introduces an unexamined potential confound.** Story generation and term explanation use Qwen3-32B to extract character attributes and judge technicality. As the critic rightly notes, Qwen3-32B is itself an LLM with its own demographic conditioning — its judgments could systematically favor certain demographic associations, conflating the target model's bias with the judge's bias. The paper claims (line 143) that "Appendix D further confirms that its judgments align well with human judges," but this validation cannot be evaluated in the current form. Even with human alignment, agreement on *which* explanation is more technical does not guarantee the judge is unbiased in detecting demographic-based differences.

- **The Section 5 discussion attributing lower proprietary bias to "continuous monitoring and iterative refinement" is unsupported speculation.** The paper presents no direct evidence for this claim — no ablation studies, no cross-version comparisons of the same model, no model developer interviews. This section is presented as analysis but the claims go well beyond what the paper's data can support. The section should be more explicitly labeled as hypothesis generation.

### Trivial

- **Table 2's formatting legend is contradictory.** It states: "Best/second-best are shown in **bold/underline**, and worst/second-worst in **bold/underline**" — identical formatting for both poles, making it ambiguous which entries are best and which are worst.

## Nice-to-Haves

- **Add a no-image control for exam-style QA.** Running the same MMLU questions without any image would establish whether accuracy is artifactually reduced by the irrelevant face image, isolating the effect of demographic conditioning from general model confusion.
- **Report bootstrapped confidence intervals or permutation test results** for TVD scores, particularly for the small exam-style QA scores where random variation could be a concern.
- **Validate the LLM judge's demographic neutrality** by stratifying its agreement with human judges across different output types (e.g., stories about different demographic groups).
- **Clarify the directional asymmetry in Figure 3** — if these are not standard Pearson correlations, the metric should be explicitly defined and justified. If they are Pearson r, this needs correction.

## Removed Points

These points from the input review were removed after verification against the paper:

1. **The "societal bias" vs. "demographic conditioning" framing critique (the critic's Critical Issue #1).** The critic argues that Hypothesis 1 (unbiased models should show demographic independence) is unjustified and that models could be "personalizing" rather than "stereotyping." This critique is not well-grounded: the paper's tasks are explicitly person-irrelevant (write about an *imaginary* person, explain a technical term, answer a math question). In these settings, user demographics should not affect outputs. The paper's operationalization follows standard fairness criteria (demographic parity) widely accepted in the literature. The observation that models write "mechanic" for male users and "nurse" for female users for an *imaginary* character is straightforwardly stereotyping, not benign personalization. This weakness was removed as a strawman.

2. **Insufficient evidence for reduced contextual confounds re: Section 2.** The critic claims the paper provides no evidence that its method reduces spurious image cues relative to captioning prompts. However, the paper's logic is sound: when the model is not asked to describe the image, background cues are less salient. The paper controls for this by balancing non-target demographics across groups. No dedicated experiment is required to validate this straightforward design choice.

3. **Term explanation assuming "more technical is better."** The critic misreads the task: the paper measures *uniformity* of technicality across groups, not that "more technical" is better. The fairness criterion is identical treatment.

4. **Section-by-section notes about abstract reliability claims and formatting nits** were either duplicative of preserved weaknesses or removed as parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the Figure 3 correlations.** This is the most pressing issue. Specify whether these are Pearson correlations or a different metric, and if Pearson, correct the asymmetry or explain the methodology that produces it. If the asymmetry is a labeling error, the corrected figure should be provided.

2. **Add a statistical-inference appendix.** Even a simple bootstrap analysis (resample images with replacement, recompute TVD, report 95% CI) would substantially strengthen the paper's evidential claims, especially for the small exam-style QA scores.

3. **Specify the exact exam-style QA prompt format** in the main text, and add a brief note on whether the model processes the face image equivalently across all inputs (or whether some models may attend differently to the image vs. text).

4. **In Section 5, explicitly label the continuous-monitoring discussion as speculative/hypothesis-generating** and add a sentence noting that the paper's data do not directly test this claim.

5. **Fix Table 2's legend** to clearly distinguish formatting for best vs. worst entries.

## Score and Decision

The paper makes a genuine technical contribution — a guardrail-agnostic method for evaluating demographic conditioning in LVLMs that demonstrably solves the refusal problem. The empirical scope is substantial, and the core findings are interesting and well-supported by Table 1 and Table 2. However, the unexplained asymmetric correlations in Figure 3 raise a significant concern about the paper's correlation analyses, and the absence of statistical inference weakens confidence in small effect sizes. These issues are addressable and do not undermine the paper's primary empirical contributions (the zero-refusal demonstration and the task-level bias measurements), but they must be resolved before the paper can be accepted.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>