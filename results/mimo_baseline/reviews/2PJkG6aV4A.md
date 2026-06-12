## Summary

This paper proposes a guardrail-agnostic method for evaluating societal bias in large vision-language models (LVLMs). The key observation is that existing bias benchmarks use attribute-inferring prompts (e.g., "Is this person a CEO or a secretary?") that trigger refusals in models with strong safety guardrails, making evaluations unreliable. The proposed solution uses person-irrelevant prompts (e.g., "Write a fictional story") while attaching demographic images only as provisional user context, achieving zero refusals across all 20 evaluated models. The evaluation reveals that all models exhibit gender and racial bias, with proprietary models generally showing lower bias than open-source ones.

## Strengths

- **Timely and well-motivated problem**: The paper clearly identifies a real and growing practical issue — that safety guardrails in modern LVLMs render existing bias benchmarks unreliable. Table 1 provides compelling evidence with refusal rates up to 100% on popular benchmarks, making the problem concrete and urgent.

- **Comprehensive evaluation scope**: The paper evaluates 20 recent LVLMs (16 open-source, 4 proprietary) across three distinct tasks and two bias axes (gender and race), providing a thorough empirical landscape. The diversity of tasks (story generation, term explanation, exam-style QA) captures different manifestations of bias, and the weak cross-task correlations (Observation 2.3) meaningfully demonstrate that bias is not monolithic.

- **Clean experimental design**: The method achieves zero refusals across all models (Table 1), directly solving the stated problem. The careful control of confounding variables (e.g., aligning non-target demographic distributions) and the validation of the LLM assistant's judgments against human annotators (Appendix D) strengthen the experimental rigor.

- **Insightful analysis**: The finding that gender and racial biases are strongly correlated within tasks (r = 0.49–0.93) is a useful observation for debiasing efforts. The analysis showing that model size and performance do not reliably predict bias (Observation 2.5) challenges simplistic assumptions about scaling.

## Weaknesses

### Fatal
None.

### Major

- **Validity of the core measurement construct**: The paper's Hypothesis 1 states that an unbiased model's outputs for person-irrelevant tasks should be statistically independent of user demographics. However, the paper does not deeply engage with the question of whether all observed demographic-conditioned differences constitute harmful "societal bias." A model might reasonably adjust communication style based on perceived user context (e.g., cultural references, reading level assumptions) in ways that reflect demographic sensitivity rather than harmful stereotyping. The story generation task most clearly reveals stereotyping (occupation associations), but the term explanation and exam-style QA tasks measure differences whose harmfulness is less self-evident. The paper would benefit from a more nuanced discussion of what constitutes bias versus legitimate adaptation in this setting.

- **LLM-as-judge introduces a second model's biases**: For story generation and term explanation, the paper relies on Qwen3-32B to extract character attributes and judge explanation difficulty. This means the bias measurement is partially a function of the judge model's own biases and capabilities. While Appendix D validates alignment with human judges, this is a significant methodological dependency that could systematically skew results. For instance, if the judge model has its own demographic biases in attribute extraction or difficulty assessment, these would propagate into the reported bias scores.

- **Speculative causal claims in the discussion**: Section 5 argues that "continuous monitoring and iterative refinement" may explain why proprietary models show lower bias. This is presented as a key insight but is largely speculative — there are many confounding differences between proprietary and open-source models (training data scale, RLHF procedures, data curation, etc.). The paper acknowledges this but still frames the monitoring hypothesis prominently, which overstates the evidence.

### Minor

- **Limited demographic axes**: The evaluation focuses on binary gender and seven race categories from FairFace. While the paper acknowledges this limitation, the binary gender framing and discrete racial categories may miss important intersectional effects and non-binary identities. The paper could at least discuss how the framework extends to more nuanced demographic representations.

- **Single prompt per task type**: Story generation uses a single fixed prompt, which limits the generalizability of findings for that task. Different prompt wordings could elicit different bias patterns. The term explanation and exam-style QA tasks use larger prompt sets, providing more robust estimates.

- **The exam-style QA task measures accuracy differences, not bias in the traditional sense**: If a model performs differently on MMLU questions when conditioned on different user photos, this could reflect many factors beyond societal bias (e.g., the model's uncertainty calibration being affected by visual context). The connection to harmful stereotyping is less direct than for the other tasks.

### Trivial
None.

## Nice-to-Haves

- A comparison of bias scores from the proposed method against some external criterion of "known bias" (e.g., from human annotations of what constitutes stereotypical content) would strengthen the validity argument.
- Analysis of whether the LLM judge's own demographic biases systematically affect the extracted attribute distributions would address the methodological concern about the judge model.
- An ablation studying the effect of the textual prefix ("I've attached my photo") versus just the image alone would clarify how much the framing matters.

## Novel Insights

The paper's most genuinely novel insight is methodological: by decoupling the evaluation task from the depicted person and using images only as user context, one can bypass safety guardrails that block traditional attribute-inferring prompts. This is a practical contribution that will likely influence how bias evaluations are conducted going forward, especially as guardrails become more prevalent across both proprietary and open-source models. The empirical finding that bias is task-specific and does not transfer across tasks (weak cross-task correlations) is also a valuable observation that challenges the notion of bias as a single model property.

## Suggestions

- Strengthen the validity argument by discussing in more detail what types of demographic-conditioned differences constitute harmful bias versus reasonable adaptation, possibly with concrete examples distinguishing the two.
- Consider using multiple independent LLM judges or a human-in-the-loop validation for the story generation and term explanation tasks to reduce dependence on a single judge model.
- Add a brief analysis of intersectional effects (e.g., gender × race) to demonstrate the framework's extensibility beyond single-axis analysis.

## Score and Decision

The paper addresses a real and timely problem with a creative solution, provides comprehensive empirical evaluation across 20 models, and offers useful insights about the nature of bias in LVLMs. The core methodological contribution (guardrail-agnostic evaluation) is practically valuable. However, the validity of the measurement construct — whether all observed differences truly represent harmful societal bias — is not sufficiently addressed, and the reliance on an LLM judge introduces a significant methodological dependency. These issues prevent a strong accept but the paper is above the acceptance threshold.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>