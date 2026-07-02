### Summary

This paper proposes an intrinsic reward method for improving autoregressive T2I models. The authors find that minimizing self-certainty, rather than maximizing it, improves image generation. This finding contrasts with previous work in text generation, where maximizing self-certainty has been beneficial. The proposed method, IRIS, uses negative self-certainty as a reward signal in a reinforcement learning framework, achieving competitive performance with methods that rely on external rewards.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel approach by applying self-certainty to autoregressive T2I models, demonstrating that minimizing self-certainty improves image generation. This finding contrasts with previous work in text generation and offers valuable insights for multimodal models.

2. IRIS is the first framework to use only intrinsic rewards for improving T2I models, reducing reliance on costly and subjective human preference data or domain-specific automated rewards.

3. The authors provide empirical evidence showing that IRIS matches or outperforms external reward-based methods on several benchmarks, including GenEval, T2I-CompBench, and WISE.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a theoretical explanation for why minimizing self-certainty improves image generation. The authors suggest that it may encourage the model to explore more diverse and less certain outputs, leading to richer and more varied images. However, further theoretical analysis is needed to understand the underlying mechanisms driving this improvement. Specifically, the paper lacks a rigorous analysis of the relationship between the model's confidence distribution and the resulting image diversity. It is unclear why a flatter confidence distribution across tokens necessarily leads to more diverse or higher-quality images. The authors should explore potential alternative explanations, such as the possibility that minimizing self-certainty inadvertently regularizes the model, preventing it from converging to a narrow, overfitted solution space.

2. The experiments are conducted on a specific autoregressive T2I model (Janus-Pro), and it is unclear how well the findings generalize to other T2I models or architectures. Additional experiments on different types of models would strengthen the claims. For example, the authors should investigate whether the observed phenomenon holds for models with different architectural designs, such as those based on diffusion processes or transformer decoders. Furthermore, the paper should explore the sensitivity of the results to different model sizes and training datasets. It is possible that the observed effect is specific to the Janus-Pro model's particular training regime or dataset biases.

3. The paper primarily focuses on objective-based evaluation. Including human preference studies would provide more direct evidence of the visual quality improvements and user preferences for images generated with IRIS. The current evaluation relies on automated metrics that may not fully capture the nuances of human perception of image quality. It is essential to conduct human evaluations to assess whether the changes in self-certainty and objective metrics translate to perceptually better images. This should include a diverse set of human raters and a well-defined evaluation protocol to ensure the reliability of the results.

### Suggestions

To address the lack of theoretical understanding, the authors should delve deeper into the mathematical properties of the self-certainty measure and its impact on the model's output distribution. A more rigorous analysis could involve examining the entropy of the model's predicted token distributions and how this entropy changes during training with the proposed intrinsic reward. It would be beneficial to explore the connection between the self-certainty reward and the model's exploration-exploitation trade-off. Specifically, the authors should investigate whether minimizing self-certainty encourages the model to explore a wider range of image features and styles, or if it simply leads to more noisy or less coherent outputs. Furthermore, the authors should consider analyzing the gradient of the self-certainty loss with respect to the model's parameters to understand how this loss function affects the learning dynamics. This analysis could provide insights into why minimizing self-certainty leads to improved image generation quality, rather than simply reducing model confidence.

To strengthen the generalizability of the findings, the authors should conduct experiments on a wider range of T2I models, including those with different architectures and training procedures. This should include models based on diffusion processes, transformer decoders, and other common architectures. The authors should also investigate the sensitivity of the results to different model sizes and training datasets. It would be beneficial to explore whether the observed phenomenon is consistent across different model scales and datasets, or if it is specific to the Janus-Pro model and its training regime. Furthermore, the authors should consider analyzing the impact of different hyperparameter settings on the performance of the proposed method. This would help to determine the robustness of the method and its applicability to different scenarios. The authors should also investigate the computational cost of the proposed method and compare it to other reward-based methods.

Finally, the authors should conduct human preference studies to evaluate the perceptual quality of the images generated with IRIS. This should involve a diverse set of human raters and a well-defined evaluation protocol. The authors should compare the images generated with IRIS to those generated with other methods, including baseline models and models trained with external rewards. The human evaluation should focus on various aspects of image quality, such as visual appeal, diversity, and alignment with the input text prompt. The authors should also consider using pairwise comparisons to assess user preferences. The results of the human evaluation should be compared to the objective metrics to determine whether there is a correlation between the two. This would provide a more comprehensive understanding of the effectiveness of the proposed method.

### Questions

1. Could the authors provide a theoretical explanation for why minimizing self-certainty improves image generation in T2I models?

2. How sensitive is the method to the choice of hyperparameters, such as the learning rate and the weight of the intrinsic reward?

3. Could the authors provide human preference studies to compare the visual quality of images generated with and without IRIS?

### Rating

6

### Confidence

3

**********