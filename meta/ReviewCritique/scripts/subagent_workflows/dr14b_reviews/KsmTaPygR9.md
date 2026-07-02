### Summary

This paper introduces MANAGERBENCH, a benchmark designed to evaluate the safety-pragmatism trade-off in LLMs when making decisions in managerial scenarios. The benchmark includes realistic scenarios where LLMs must choose between a pragmatic but potentially harmful action and a safe but less effective one. The authors evaluate several state-of-the-art LLMs and find that most models struggle to balance safety and pragmatism. The paper also explores the fragility of safety alignment under goal-oriented prompts and the sensitivity of models to the severity of harm and the magnitude of operational benefits.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper addresses a critical and timely issue in the field of LLMs, which is the alignment of safety and pragmatism in decision-making. The introduction of MANAGERBENCH is a valuable contribution that can help researchers and practitioners better understand the limitations of current LLMs in this area.
2. The experimental design is well-thought-out, with a clear methodology for constructing the benchmark and evaluating the models. The use of human validation to ensure the realism and harmfulness of the scenarios adds credibility to the benchmark.
3. The paper provides a comprehensive evaluation of several state-of-the-art LLMs, revealing interesting patterns and insights into their behavior. The analysis of the fragility of safety alignment and the sensitivity to harm and benefit is particularly insightful.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the benchmark and potential biases in the scenarios. For example, the cultural and ethical background of the human annotators could influence their perception of harm and realism. The paper should include a more thorough analysis of how the annotators' demographics and backgrounds might have shaped the benchmark's design and the resulting evaluation of LLMs. This is crucial for understanding the generalizability of the findings.
2. The paper could explore the impact of different prompting strategies on model performance. For example, how do models perform when given more context or different instructions? The current evaluation seems to rely on a single prompting strategy, which may not fully capture the capabilities of the models. Exploring a range of prompts, including those that explicitly emphasize safety or pragmatism, could reveal more nuanced behaviors and provide a more comprehensive assessment of the models' alignment.
3. The paper could benefit from a more in-depth analysis of the relationship between model size and performance on the benchmark. Are larger models consistently better at balancing safety and pragmatism, or are there other factors at play? The paper should investigate whether the observed performance differences are solely due to model size or if other factors, such as training data or architecture, play a more significant role. This analysis could provide valuable insights into the design of future LLMs.

### Suggestions

To address the limitations regarding potential biases in the benchmark, the authors should conduct a more detailed analysis of the human annotators' backgrounds and their potential influence on the scenarios. This could involve collecting demographic information about the annotators and performing statistical analyses to identify any correlations between annotator characteristics and the perceived harm or realism of the scenarios. Furthermore, the authors could explore methods for mitigating these biases, such as using a more diverse pool of annotators or employing techniques to adjust for systematic differences in their ratings. This would enhance the robustness and generalizability of the benchmark and provide a more accurate assessment of LLM performance across different contexts. The authors should also consider including scenarios that are specifically designed to test for cultural biases, allowing for a more granular analysis of how different cultural backgrounds might affect the perception of harm and safety.

To explore the impact of different prompting strategies, the authors should conduct a systematic evaluation of various prompt formulations. This could include prompts that explicitly emphasize safety or pragmatism, as well as prompts that provide additional context or instructions. The authors could also explore the use of chain-of-thought prompting to encourage more nuanced reasoning and decision-making. By comparing the performance of models across these different prompting conditions, the authors could gain a more comprehensive understanding of the models' capabilities and limitations. This analysis should also investigate whether certain prompting strategies are more effective for specific types of scenarios or models. The results of this analysis could provide valuable guidance for developing more effective prompting techniques for LLMs in safety-critical applications.

Finally, to better understand the relationship between model size and performance, the authors should conduct a more detailed analysis of the performance of models across different scales. This could involve evaluating a wider range of models with varying sizes and architectures, as well as analyzing the performance of models with different training data. The authors should also investigate whether the observed performance differences are correlated with specific model characteristics, such as the number of parameters or the type of training data. This analysis could provide valuable insights into the design of future LLMs and help identify the key factors that contribute to effective safety-pragmatism trade-offs. The authors should also consider exploring the use of techniques such as knowledge distillation to transfer the capabilities of larger models to smaller models, potentially improving the performance of smaller models without sacrificing efficiency.

### Questions

1. How do the authors ensure the realism and harmfulness of the scenarios in the benchmark? What methods are used to validate these properties?
2. The paper mentions that the benchmark is designed to be difficult for current models. How do the authors measure the difficulty of the benchmark, and what evidence do they have to support this claim?
3. How do the authors address the potential biases in the scenarios, such as cultural or ethical biases?
4. The paper explores the impact of different prompting strategies on model performance. What are the implications of these findings for the development of more robust and reliable LLMs?
5. The paper analyzes the relationship between model size and performance on the benchmark. What are the implications of these findings for the design of future LLMs?

### Rating

6

### Confidence

4

**********