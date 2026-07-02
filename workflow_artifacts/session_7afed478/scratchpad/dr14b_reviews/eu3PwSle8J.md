### Summary

This paper proposes a novel approach to enhance the robustness of LLMs against prompt injection attacks by introducing Augmented Intermediate Representations (AIR). The key idea is to inject instruction hierarchy (IH) signals recurrently across all layers of the LLM, rather than solely at the input level. The authors demonstrate that this approach significantly improves robustness against gradient-based attacks while maintaining model utility.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper identifies a critical limitation in existing prompt injection defense mechanisms and proposes a novel solution that addresses this limitation effectively.
2. The proposed method is simple yet effective, adding minimal overhead to the model.
3. The paper provides a comprehensive evaluation of the proposed method across multiple models, training setups, and evaluation datasets, demonstrating its effectiveness and generalizability.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed analysis of the computational overhead introduced by AIR, particularly in terms of training time and memory usage. While the authors mention that the overhead is minimal, a quantitative analysis would be beneficial to understand the practical implications of this approach. Specifically, the paper should include a breakdown of the increased parameter count, FLOPs, and memory consumption during both training and inference, compared to baseline models without AIR. This analysis should also consider the scaling of these overheads with model size and the number of layers.
2. The evaluation primarily focuses on gradient-based attacks. It would be valuable to see how AIR performs against other types of prompt injection attacks, such as those based on adversarial examples or semantic manipulations. The paper should include evaluations against a broader range of attack strategies, including those that do not rely on gradient information, to provide a more comprehensive assessment of the method's robustness. For example, evaluations against attacks that use synonym substitution or paraphrasing to bypass the instruction hierarchy could be included.
3. The paper does not provide a detailed analysis of the trade-offs between robustness and model utility. While the authors claim that AIR does not significantly degrade model utility, a more rigorous analysis of the impact on various downstream tasks would be beneficial. This analysis should include a quantitative evaluation of the performance on a diverse set of tasks, such as question answering, text summarization, and code generation, to understand the potential impact of AIR on model accuracy and generation quality.

### Suggestions

To address the lack of detailed computational overhead analysis, the authors should include a comprehensive breakdown of the increased parameter count, FLOPs, and memory consumption during both training and inference. This analysis should be presented in a table format, comparing the baseline models with the AIR-enhanced models across different model sizes and layer configurations. The authors should also discuss the scaling behavior of these overheads, providing insights into how the computational cost of AIR changes with increasing model size and complexity. Furthermore, it would be beneficial to include a discussion of the potential impact of these overheads on training time and inference latency, especially for large-scale models. This detailed analysis will allow readers to better understand the practical implications of using AIR in real-world applications.

To broaden the evaluation of AIR, the authors should include experiments against a wider range of prompt injection attacks, particularly those that do not rely on gradient information. This could include attacks based on adversarial examples, semantic manipulations, or synonym substitution. For example, the authors could evaluate the robustness of AIR against attacks that use paraphrasing or synonym replacement to bypass the instruction hierarchy. Additionally, the authors should consider evaluating the method against attacks that target specific vulnerabilities of the instruction hierarchy, such as attacks that attempt to manipulate the hierarchy itself. This more comprehensive evaluation will provide a more robust assessment of the method's effectiveness and its limitations. The results should be presented in a clear and concise manner, allowing readers to compare the performance of AIR against different attack strategies.

To provide a more rigorous analysis of the trade-offs between robustness and model utility, the authors should conduct a quantitative evaluation of the impact of AIR on various downstream tasks. This evaluation should include a diverse set of tasks, such as question answering, text summarization, code generation, and other relevant tasks. The authors should report the performance of the AIR-enhanced models on these tasks, comparing them to the baseline models without AIR. This analysis should also include a discussion of the potential impact of AIR on model accuracy, generation quality, and other relevant metrics. The authors should also discuss the potential limitations of AIR in specific application scenarios and provide guidance on how to mitigate these limitations. This detailed analysis will allow readers to better understand the practical implications of using AIR in real-world applications.

### Questions

1. Could the authors provide more details on the computational overhead introduced by AIR, particularly in terms of training time and memory usage?
2. How does AIR perform against other types of prompt injection attacks, such as those based on adversarial examples or semantic manipulations?
3. What is the impact of AIR on model utility across various downstream tasks, and are there any specific scenarios where AIR might degrade performance?

### Rating

6

### Confidence

4

**********