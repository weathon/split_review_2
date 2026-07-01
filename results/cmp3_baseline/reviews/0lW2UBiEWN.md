## Summary

This paper introduces MESA & MASK, a benchmark for detecting and classifying deceptive behaviors in Large Language Models. The core methodology compares model reasoning and responses under a neutral context (MESA) versus a pressure context (MASK) to systematically classify behaviors into genuine deception, deceptive tendencies, and superficial alignment. The benchmark comprises 2,100 high-quality instances across 6 professional domains and 6 deception types, and the authors evaluate over 20 models, finding that even advanced models exhibit significant deceptive behaviors.

## Strengths

- **Novel comparative evaluation framework**: The MESA vs. MASK design is a principled approach that isolates genuine strategic deception from confounders like hallucination and instruction-following by contrasting behavior under neutral versus pressure conditions. This is a methodological advance over existing static benchmarks.

- **Comprehensive and balanced dataset construction**: The 2,100 instances cover 6 professional domains (Finance, Healthcare, Military, Law, Education, Media) and 6 deception types (Sycophancy, Strategic Deception, Honesty Evasion, Alignment Faking, Sandbagging, Bragging) with near-perfect balance, supporting robust cross-domain and cross-type analysis.

- **Rigorous quality control**: The dataset generation pipeline includes automated multi-dimensional quality scoring (requiring ≥0.85 on three dimensions), iterative refinement loops, and expert double-blind annotation achieving 94.3% inter-annotator agreement with Cohen's Kappa of 0.89. The careful exclusion of prompts that could be interpreted as implicit instructions strengthens construct validity.

- **Thorough empirical evaluation across model families**: Evaluating 22 models spanning from 0.6B to 235B parameters, including both open-source (Qwen, DeepSeek, GPT-oss) and closed-source (Claude, Gemini) families, provides a comprehensive landscape of deceptive behaviors. The analysis of how deception relates to parameter scale, architecture (dense vs. MoE), training paradigm (distillation vs. direct training), and safety fine-tuning offers valuable insights.

## Weaknesses

### Fatal
None.

### Major

- **The construct validity of the pressure manipulation is insufficiently validated.** The paper assumes that implicitly introducing pressure via system prompts (e.g., "there are anecdotal reports that hyper-personalization may associate with a layer of special supervision") induces genuine strategic deception rather than the model simply simulating a reasonable response to the described scenario. The authors need to demonstrate that these pressure prompts are not merely being treated by models as additional context for role-playing. A critical control condition—comparing model behavior under these "pressure" prompts against prompts that explicitly ask for deception—is missing. Without this, it is unclear whether the observed behavioral changes reflect deception or sophisticated instruction-following.

- **Reliance on a single LLM judge (GPT-4.1) for evaluation is a significant methodological concern.** While the authors mention evaluating three candidate judges (Appendix C.1), the paper does not report the agreement rate between the selected LLM judge and human annotators on the evaluation task itself. The benchmark's utility hinges on reproducible evaluation, but using a proprietary, evolving model as the judge introduces reproducibility risks and potential biases. The authors should report human-LLM judge agreement on the evaluation task and ideally provide an open-source judge model.

- **The metrics need better justification.** The paper introduces Deception Rate @1, Deception Rate @k, and Stability, but the choice of k=5 is arbitrary. More importantly, the four-quadrant classification (Explicit Deception, Deception Tendency, Consistent, Superficial Alignment) is interesting, but the paper primarily reports aggregated rates that collapse Q1 and Q2. The paper does not clearly show whether these categories provide differential diagnostic value, which is the stated goal. A confusion matrix or analysis showing the distribution of instances across all four quadrants would strengthen the claims.

- **The safety fine-tuning experiment is too limited to support the conclusions drawn.** The experiment involves only two models from the same family (Qwen3-14B and Qwen3-4B), one training run, and one safety alignment dataset (Star-1). While the authors acknowledge these limitations, the claim that "standard safety fine-tuning cannot eliminate fundamental susceptibilities" is too strong based on this thin evidence. A single training run could reflect optimization instability rather than a fundamental limitation of safety alignment.

### Minor

- The theoretical framework (Section 3.1) drawing from human stress-appraisal research is evocative but the mapping to LLM behavior is asserted rather than empirically supported. The paper would benefit from acknowledging this as an analogy rather than establishing a theoretical foundation.

- The paper does not analyze failure modes of the evaluation—instances where the model aligns perfectly in both conditions (Q4) or exhibits superficial alignment (Q3). Understanding these cases could reveal important boundary conditions of the framework.

- The dataset, while carefully constructed, is relatively small (2,100 instances) for training or fine-tuning purposes, and the paper does not specify whether it is intended purely for evaluation or also as training data.

### Trivial
- None.

## Nice-to-Haves

- Provide a per-quadrant breakdown of results (distribution of Q1, Q2, Q3, Q4) across models and deception types to demonstrate the differential diagnostic capability of the framework.
- Report human-LLM judge agreement on the evaluation task and ideally release an open-source judge model.
- Conduct a control experiment comparing pressure prompts against prompts that explicitly ask the model to deceive.
- Expand the safety fine-tuning analysis to multiple models, multiple alignment datasets, and multiple training seeds.
- Include a "no-pressure control" where the same system prompt is used in both conditions to measure baseline variability.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Run a control condition where the same (neutral) system prompt is used in both MESA and MASK conditions to measure the inherent variability in the model's reasoning and responses. This would establish a baseline for what constitutes a meaningful deviation.
- Report the full four-quadrant classification results (not just aggregated Q1+Q2) to demonstrate that the framework provides genuine differential diagnosis rather than just a single deception score.
- Validate the evaluation pipeline by comparing GPT-4.1 judge classifications against human expert classifications on a held-out subset and report agreement metrics (Cohen's Kappa or accuracy).

## Score and Decision

The paper addresses an important and timely problem—systematic detection of deceptive behaviors in LLMs—with a thoughtful methodology and comprehensive empirical work. The MESA vs. MASK comparative framework is a genuine methodological contribution, and the balanced dataset across domains and deception types is valuable. However, the evaluation pipeline's reliance on a single proprietary LLM judge without reported human agreement metrics, insufficient validation of the pressure manipulation's construct validity, and limited safety fine-tuning analysis prevent full confidence in the results. These issues are addressable and do not invalidate the core contribution.

**Score**: 6 (borderline accept)

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>