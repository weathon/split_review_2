### Summary

This paper presents a method for evaluating societal bias in large vision-language models (LVLMs) by using person-irrelevant prompts and treating images as user context rather than direct subjects of inference. The authors demonstrate that their approach avoids the high refusal rates seen in existing benchmarks, enabling reliable bias measurement across 20 recent LVLMs, including both open-source and proprietary models. The study finds that all models exhibit societal bias, with proprietary models showing less bias than open-source ones. The authors suggest that continuous model monitoring and improvement may play a key role in reducing bias.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper addresses a critical issue in the evaluation of large vision-language models (LVLMs) by proposing a guardrail-agnostic framework that overcomes the limitations of existing benchmarks. The shift from attribute-infering prompts to person-irrelevant prompts and the use of images as user context rather than direct subjects of inference is a significant innovation that enables reliable bias measurement even in models with strong safety guardrails. This approach is both novel and practical, providing a way to evaluate societal bias without triggering refusals.
2. The paper presents a comprehensive evaluation of 20 recent LVLMs, including both open-source and proprietary models, demonstrating the effectiveness of the proposed method in measuring societal bias across different model architectures and training paradigms. The use of diverse tasks such as story generation, term explanation, and exam-style QA provides a robust assessment of bias in various contexts. The authors also employ rigorous statistical methods to quantify bias, ensuring the validity of their findings.
3. The paper is well-structured and clearly written, making it accessible to a broad audience. The authors provide detailed explanations of their methodology, including the rationale behind their choices and the steps involved in the evaluation process. The use of figures and tables effectively illustrates key concepts and results, enhancing the clarity and impact of the paper.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's focus on gender and racial biases, while important, does not fully capture the complexity of societal bias. Other forms of bias, such as those related to age, socioeconomic status, or physical ability, are not addressed. This limitation could be mitigated by expanding the scope of the evaluation to include a broader range of demographic attributes. The current evaluation, while comprehensive in terms of models and tasks, is narrow in the types of biases it considers. For instance, the impact of ageism or ableism in these models remains unexplored, potentially overlooking significant sources of societal bias. The study should consider how the proposed framework could be extended to capture these additional dimensions of bias, which are crucial for a holistic understanding of the problem.
2. The paper does not provide a detailed analysis of the potential sources of bias in the evaluated models. While the authors observe that proprietary models tend to exhibit less bias, they do not fully explore the underlying reasons for this difference. A deeper investigation into the training data, model architecture, and safety alignment techniques used in these models could provide valuable insights into the mechanisms of bias and how to mitigate it. The paper lacks a thorough examination of the training data used for these models, which is a critical factor in understanding the origins of bias. Furthermore, the specific architectural choices and safety alignment techniques employed by proprietary models, which may contribute to their lower bias scores, are not analyzed in detail. A more granular analysis of these factors is needed to draw meaningful conclusions about the sources of bias.

### Suggestions

To address the limited scope of bias evaluation, the authors should consider expanding their framework to include a more diverse set of demographic attributes. This could involve incorporating datasets that contain images with annotations for age, socioeconomic status, and physical ability, among others. The evaluation should also include tasks that are specifically designed to elicit these types of biases. For example, the story generation task could be modified to assess whether the model generates different narratives based on the perceived age or socioeconomic status of the person in the image. Furthermore, the term explanation task could be adapted to examine if the model provides different levels of technical detail based on these attributes. By broadening the range of biases considered, the study would provide a more comprehensive assessment of societal bias in LVLMs. This would also require a careful consideration of how to define and measure bias for these additional attributes, which may require the development of new metrics and evaluation protocols.

To better understand the sources of bias, the authors should conduct a more detailed analysis of the training data used for the evaluated models. This could involve examining the demographic distribution of the training data and identifying potential biases in the representation of different groups. The authors should also investigate the specific architectural choices and safety alignment techniques used by proprietary models, which may contribute to their lower bias scores. This could involve analyzing the impact of different training objectives, regularization techniques, and data augmentation strategies on the model's bias. Furthermore, the authors should explore the use of interpretability techniques to identify the specific features or patterns in the input data that contribute to biased outputs. By combining these approaches, the authors could gain a deeper understanding of the mechanisms of bias and develop more effective mitigation strategies. This analysis should also consider the potential for bias to emerge during the model's deployment, not just during training.

Finally, the authors should consider the ethical implications of their findings and discuss the potential for their work to be used to improve the fairness of LVLMs. This could involve exploring the use of their framework to develop bias mitigation techniques and evaluating the effectiveness of these techniques in reducing societal bias. The authors should also discuss the limitations of their approach and acknowledge that bias is a complex issue that cannot be fully addressed by a single study. By engaging with these ethical considerations, the authors can ensure that their work contributes to the development of more responsible and equitable AI systems.

### Questions

1. How does the proposed guardrail-agnostic framework handle cases where the image context is ambiguous or contains multiple individuals? Is there a risk that the model's responses could be influenced by factors other than the intended demographic attribute?
2. The paper observes that proprietary models exhibit less societal bias than open-source models. What specific factors contribute to this difference? Is it primarily due to differences in training data, model architecture, or safety alignment techniques?
3. How does the proposed method perform when applied to models with different types of safety guardrails? Are there any specific types of guardrails that are more likely to interfere with the evaluation process?
4. The paper focuses on gender and racial biases. How well does the proposed framework generalize to other forms of societal bias, such as ageism, ableism, or socioeconomic bias? What modifications would be needed to adapt the framework to these other forms of bias?
5. The paper uses a fixed set of person-irrelevant prompts for evaluation. How sensitive are the results to the choice of prompts? Would different prompts lead to significantly different bias scores?
6. The paper does not provide a detailed analysis of the computational resources required to implement the proposed framework. What are the main computational bottlenecks, and how can they be addressed to make the framework more accessible to researchers with limited resources?

### Rating

6

### Confidence

4

**********