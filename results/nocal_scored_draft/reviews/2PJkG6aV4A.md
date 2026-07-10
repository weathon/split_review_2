## Summary

This paper proposes a "guardrail-agnostic" method for evaluating societal bias in LVLMs. Rather than using attribute-inferring prompts that safety guardrails often refuse (the standard approach), the method uses person-irrelevant tasks (story generation, term explanation, exam-style QA) where images are treated as user context rather than the subject of the prompt. This design achieves zero refusals across all 20 evaluated models. The paper reports that all models exhibit demographic conditional dependence, with proprietary models showing lower bias scores than open-source ones.

---

## Strengths

- **Identifies a genuine and growing problem quantitatively.** The high refusal rates on attribute-inferring prompts (Tab. 1 shows Claude 3.7 Sonnet refusing 100% of SBBench prompts, 98% of ModScan, 98% of VLA-gender, 81% of Pairs) make existing bias benchmarks unreliable for guardrailed LVLMs, and this trend is accelerating. The paper documents this problem clearly with concrete numbers.

- **Core idea is creative and well-motivated.** Decoupling the evaluation task from the depicted person by switching from "infer this person's attributes" to person-irrelevant tasks with images as user context is a genuinely clever way to sidestep refusal behavior. The method achieves zero refusals (Tab. 1), which is a clean, nontrivial result.

- **Broad model coverage.** Evaluating 20 LVLMs (16 open-source, 4 proprietary) across three diverse tasks provides a comprehensive picture of bias in current models. The scale of the evaluation is substantial relative to prior work.

- **Interesting empirical findings.** The paper documents that proprietary models consistently show lower bias scores than open-source models, and reports weak cross-task correlations (Observation 2.3), suggesting bias is not a monolithic property — a useful result for the community.

---

## Weaknesses

### Fatal

None.

### Major

- **The TVD metric conflates demographic sensitivity with harmful stereotyping.** Hypothesis 1 (line 111) states that an unbiased model's outputs should be statistically independent of user demographics, and the paper labels any deviation as "societal bias" (lines 56–57). However, TVD measures *any* distributional difference across demographic groups without distinguishing between genuinely harmful stereotyping (e.g., always portraying women as nurses, men as mechanics) and patterns that could be non-stereotypical demographic sensitivity. The paper provides qualitative examples showing actual stereotypical associations (Fig. 2), which is helpful, but the quantitative metric itself aggregates both. As a result, the headline claim that the method measures "societal bias" is broader than the evidence supports. This is the paper's most significant limitation and should be addressed by either (a) analyzing the direction/specificity of the associations that drive the TVD score, or (b) reframing the contribution as measuring *demographic sensitivity* rather than *societal bias*.

### Minor

- **No uncertainty quantification.** Bias scores in Tab. 2 are reported to two decimal places without confidence intervals, standard errors, or statistical tests. Without these, it is impossible to determine which model differences are meaningful vs. noise. Bootstrapped CIs would be straightforward to compute from the 500-story-per-group setup.

- **The use of an LLM (Qwen3-32B) as a judge** for attribute extraction and technicality judgment introduces a potential confound. Even though the paper claims human-judgment alignment (Appendix D), the LLM's own demographic biases could be projected onto the bias measurements. More transparent validation (e.g., multiple LLM judges, inter-annotator agreement on a random subset) would strengthen confidence.

- **The method could be validated against existing bias benchmarks** on models where those benchmarks still work (e.g., LLaVA-1.6-34B has only 10% refusal on Pairs). Showing correlation with prior established measures would build confidence that the approach measures a related construct rather than an entirely different one.

### Trivial

- The paper focuses on aggregate TVD scores but does not systematically analyze which specific stereotypical associations drive the bias (e.g., which occupations are over/under-represented per group). The qualitative examples (Fig. 2) are illustrative, but a systematic breakdown would allow readers to distinguish the specific stereotypes being reinforced.

---

## Nice-to-Haves

- Distinguish demographic sensitivity from harmful stereotyping by including a directional analysis alongside TVD.
- Validate against prior methods on models where existing benchmarks still work.
- Provide systematic breakdowns of which specific attributes drive the bias scores.

---

## Removed Points

- **Discussion about continuous monitoring being speculative:** Removed. The paper uses appropriately hedged language ("a plausible explanation," "may play a key role," "can be a critical factor") and clearly presents this as a hypothesis, not a verified finding. The reviewer's characterization as a strong causal claim misreads the text.
- **Exam-style QA validity as a separate issue:** Merged into the demographic-sensitivity-vs-societal-bias concern (Major weakness #1).
- **Missing appendix / human-validation concern:** Removed per hard rules — the parser strips appendices; the original submission includes Appendix D with the claimed validation.
- **Abstract overstatement:** Removed as generic and not anchored to a specific claim in the paper.
- **Section 2 contextual confound point:** The paper acknowledges this limitation and claims to "reduce" (not eliminate) contextual confounds (line 97). The criticism does not go beyond what the paper already addresses.
- **Cherry-picked examples:** The paper uses examples purely for illustration; the quantitative evidence comes from TVD scores across 500 samples. This is standard practice.
- **Pure formatting/style nitpicks:** Removed per hard rules.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. Add bootstrapped confidence intervals to all bias scores in Tab. 2.
2. Supplement TVD with a directional analysis (which specific occupations/attributes are over/under-represented per group) to distinguish harmful stereotyping from benign demographic sensitivity.
3. Validate against existing bias metrics on models with low refusal rates (e.g., LLaVA-1.6-34B on Pairs).
4. Use multiple LLM judges or provide inter-annotator agreement statistics to strengthen LLM-as-judge robustness.
5. Consider reframing the contribution as measuring *demographic conditional dependence* for person-irrelevant tasks, with societal-bias interpretations supported by directional analysis of the specific associations.

---

## Score and Decision

The paper identifies a real problem and proposes a creative, effective solution (zero refusals is a clean result). The evaluation is broad and the empirical findings are informative. The main concern — that TVD measures demographic sensitivity rather than specifically harmful stereotyping — is significant but not fatal: the paper's qualitative examples show that the detected patterns are indeed stereotypical, and the core methodological contribution (eliciting demographic-dependent behavior without guardrail interference) stands independently. The issue is addressable with reframing and additional analysis.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>