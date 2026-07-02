### Summary

This paper proposes a method to share noisy transformer embeddings while preserving privacy and maintaining utility. The approach, called Nonparametric Variational Differential Privacy (NVDP), integrates a Nonparametric Variational Information Bottleneck (NVIB) layer into the transformer architecture. This layer injects noise into the embeddings to obscure sensitive information, with privacy protection measured using Rényi divergence and Bayesian Differential Privacy (BDP). Experiments on the GLUE benchmark demonstrate a trade-off between privacy and accuracy, showing that the model can maintain high utility with strong privacy guarantees at lower noise levels.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The paper is well-written and easy to follow.
2. The paper provides a comprehensive introduction to the background, including Differential Privacy, Rényi Differential Privacy (RDP), Bayesian Differential Privacy (BDP), and Nonparametric Variational Information Bottleneck (NVIB).
3. The paper presents a clear and detailed description of the proposed method, including the NVDP architecture, the role of the NVIB layer, and the process of generating noisy embeddings.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational complexity of the proposed method. Specifically, the paper lacks an analysis of the time and space complexity of the NVIB layer and how it scales with the input sequence length and the number of attention heads. This makes it difficult to assess the practicality of the method for large-scale applications, especially when considering the overhead of noise injection and sampling from the learned distribution.
2. The paper does not provide a detailed analysis of the sensitivity of the proposed method to hyperparameters. While the paper mentions the existence of hyperparameters, it does not provide a systematic study of how these parameters affect the privacy-utility trade-off. For example, the paper does not analyze how the learning rate, the noise scale, and the regularization parameters of the NVIB layer impact the final performance and privacy guarantees. This lack of analysis makes it challenging to tune the method for different datasets and tasks.
3. The paper does not provide a detailed analysis of the robustness of the proposed method to adversarial attacks. The paper only focuses on the privacy aspect measured by Rényi divergence and BDP, but it does not analyze how the noisy embeddings affect the model's robustness to adversarial perturbations. It is unclear whether the added noise makes the model more or less susceptible to adversarial attacks, which is a critical consideration for real-world applications.

### Suggestions

To address the lack of computational complexity analysis, the authors should provide a detailed breakdown of the time and space complexity of the NVIB layer, including the forward and backward passes. This analysis should consider the impact of the input sequence length, the number of attention heads, and the dimensionality of the embeddings. Furthermore, the authors should provide empirical results on the training and inference time of the proposed method on different datasets and hardware configurations. This would provide a more comprehensive understanding of the practical implications of the proposed method and allow for a more informed comparison with existing approaches. The analysis should also include a discussion of the trade-offs between privacy, utility, and computational cost, which is crucial for real-world applications.

To address the lack of hyperparameter sensitivity analysis, the authors should conduct a systematic study of how the hyperparameters of the NVIB layer affect the privacy-utility trade-off. This study should include a range of values for the learning rate, the noise scale, and the regularization parameters. The authors should also provide visualizations of the privacy-utility trade-off curves for different hyperparameter settings. This would allow practitioners to tune the method for their specific needs and provide a better understanding of the method's behavior. Furthermore, the authors should discuss the optimal strategy for selecting hyperparameters, such as using a validation set or cross-validation. This would make the method more accessible and easier to use in practice.

To address the lack of robustness analysis, the authors should evaluate the performance of the proposed method under adversarial attacks. This evaluation should include a range of adversarial attack methods, such as gradient-based attacks and perturbation-based attacks. The authors should also compare the robustness of the proposed method with existing approaches. This would provide a more comprehensive understanding of the method's strengths and weaknesses and allow for a more informed comparison with existing approaches. The authors should also discuss the potential limitations of the proposed method in terms of robustness and suggest future research directions to address these limitations.

### Questions

Please refer to the weaknesses part.

### Rating

5

### Confidence

3

**********