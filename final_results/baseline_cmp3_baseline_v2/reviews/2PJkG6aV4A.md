## Summary

This paper proposes a guardrail-agnostic method for evaluating societal bias in large vision-language models (LVLMs). Instead of using attribute-inferring prompts that trigger refusals in safety-guarded models, the authors replace them with person-irrelevant prompts (e.g., “Write a fictional story”) and treat images as provisional user context. Applied across three tasks—story generation, term explanation, and exam-style QA—the method achieves zero refusals on 20 recent LVLMs. The experiments reveal that all models exhibit gender and racial bias, proprietary models show lower bias than open-source ones, and bias is not reliably explained by model size or performance.

## Strengths

- **Well-motivated problem**: The paper identifies a genuine and timely limitation of existing bias benchmarks—the rising refusal rates caused by safety guardrails—and demonstrates this empirically on four popular benchmarks (Table 1).
- **Simple and clever idea**: Decoupling the task from the depicted person by using person-irrelevant prompts while attaching images as user context is a neat workaround that elegantly avoids refusals. The approach is conceptually clear and easy to implement.
- **Extensive experiments**: The evaluation spans 20 recent LVLMs (16 open-source, 4 proprietary) across three different tasks, providing a broad picture of societal bias in current models. The analysis of correlations between tasks and with model size/performance is informative.
- **Practical implications**: The discussion on continuous monitoring and iterative refinement as a possible factor for bias reduction is actionable and relevant for model deployment.

## Weaknesses

### Fatal
None.

### Major

- **Questionable core assumption**: The paper assumes that an unbiased model should produce outputs statistically independent of user demographics. However, differences could arise from benign personalization (the model tailoring the output to the inferred user identity) rather than harmful societal bias. The paper does not distinguish between these interpretations, which threatens the validity of the proposed metric as a measure of *societal bias* specifically.
- **Confounding due to image-based demographic inference**: The method relies on the model’s own (potentially biased) recognition of race, gender, and other attributes from images. The model’s internal representation of these demographics may introduce confounds that affect outputs, yet the paper does not control for or analyze this effect (e.g., by using text-described demographics or anonymized controls).
- **Construct validity of the comparison to prior benchmarks**: The paper shows that prior benchmarks have high refusal rates and claims they are “unreliable.” However, the prior benchmarks were designed to measure bias in *attribute inference*, whereas the proposed method measures bias in *person-irrelevant tasks*. These are different constructs; avoiding refusals does not automatically make the new method a better measure of the same societal bias. The paper does not demonstrate that the observed disparities correspond to the same harmful stereotypes that prior benchmarks target.

### Minor

- **“Zero refusals” claim is overscoped**: The claim of zero refusals is based on sampled prompts (300 per benchmark) for three tasks. It may not hold for all possible prompts, especially edge cases that models might deem sensitive even if person-irrelevant (e.g., prompts involving violence or certain socio-political terms).
- **Correlation reporting inconsistency**: The correlation values in Figure 3 and its caption appear inconsistent (e.g., dotted line vs. solid line descriptions) and the numbers in the text do not clearly match the figure. This makes the analysis hard to verify.
- **The role of safety-aware training**: The paper dismisses safety-aware training as insufficient because Gemma3 (which has safety measures) still shows high bias, but this is a single data point. The conclusion that continuous monitoring is the key factor is speculative and not directly supported by the experiments.

### Trivial
- Some figure captions are duplicated (e.g., Figure 1 caption appears twice in the PDF extraction).

## Nice-to-Haves

- A controlled experiment where demographic information is provided as text (e.g., “I am a 30-year-old male”) instead of images, to isolate the effect of visual demographic inference from the image-based bias measurement.
- A human evaluation study to verify that the output differences observed (e.g., *mechanic* vs. *nurse*) are perceived as harmful stereotypes by human judges, rather than benign adaptations.
- An ablation where the model is asked to ignore the user photo, to test whether the bias persists even when the model is instructed to disregard the image.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Address the core assumption head-on: discuss whether output independence from user demographics is the correct fairness criterion, and provide evidence or a clear argument for why the observed disparities reflect harmful societal bias rather than benign personalization. Consider adding a control task where the model is explicitly told the user’s demographics and asked to produce a response that is *not* personalized, to see if bias persists.
- To strengthen construct validity, compare the proposed method’s bias scores with those from prior benchmarks on models that *do* answer both types of prompts (e.g., some open-source models with lower refusal rates) and check if the rankings agree.
- Clarify the correlation analysis in Figure 3 and ensure the numbers in the text and caption are consistent and properly explained.
- Provide a more nuanced discussion of why continuous monitoring might reduce bias, perhaps with references to specific deployment examples or evidence from other domains.

## Score and Decision

The paper presents a creative and practical solution to a real problem, and the experiments are thorough. However, the core conceptual issue—whether the method measures societal bias or something else (e.g., personalization)—is a major weakness that undermines the paper’s contribution. The claim of guardrail-agnostic bias evaluation relies on an assumption that is not adequately defended. Therefore, the paper currently does not convincingly meet the bar for acceptance.

**Score**: 4  
**Decision**: Reject  

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>