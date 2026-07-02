### Summary

This paper studies whether sparse autoencoders (SAEs) can distinguish trained transformers from random ones. The authors find that SAEs trained on randomly initialized transformers can produce auto-interpretability scores and reconstruction metrics that are similar to those from trained models. They also find that the latents of SAEs trained on trained transformers tend to be more complex and abstract, especially in later layers. The authors suggest that high auto-interpretability scores alone do not guarantee that an SAE has identified complex, learned computations, and that more rigorous methods are needed to distinguish between artifacts and genuinely learned computations.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The paper studies an important problem in the field of mechanistic interpretability.
3. The paper provides a comprehensive analysis of the performance of SAEs on trained and randomized transformers, using a variety of metrics and model sizes.
4. The paper provides a novel insight into the limitations of SAEs in distinguishing trained and randomized transformers, and suggests that more rigorous methods are needed to validate interpretability techniques.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a clear explanation of why the SAEs are able to produce similar scores for trained and randomized transformers. It is unclear what specific properties of the SAEs or the transformer architectures lead to this behavior. For instance, are the SAEs simply learning to reconstruct the input activations regardless of their origin, or are they capturing some underlying structure that is shared between trained and randomized models? The paper should delve deeper into the mechanisms behind this phenomenon.
2. The paper does not provide a clear recommendation for how to validate interpretability techniques. While the authors suggest that more rigorous methods are needed, they do not offer concrete steps or methodologies for achieving this. What specific types of analyses or experiments should researchers conduct to ensure that their interpretability techniques are actually capturing meaningful computations, rather than just artifacts of the model or training process? The paper needs to provide more actionable guidance.

### Suggestions

The paper should investigate the specific properties of the sparse autoencoders (SAEs) that lead to similar performance on trained and randomized transformers. One approach would be to analyze the learned latent representations in more detail. For example, the authors could examine the distribution of activation patterns in the latent space for both trained and randomized models. Are there distinct clusters or patterns that differentiate the two? If not, what does this suggest about the SAE's ability to capture meaningful features? Furthermore, the authors could explore the sensitivity of the SAE's performance to different hyperparameters, such as the sparsity level or the dimensionality of the latent space. This could reveal whether the observed similarities are robust or dependent on specific configurations. It would also be beneficial to analyze the reconstruction errors in more detail. Are there specific types of activations that are more difficult to reconstruct, and do these errors differ between trained and randomized models? Such analysis could provide insights into the limitations of SAEs for interpretability.

To address the lack of clear recommendations for validating interpretability techniques, the paper should propose a set of criteria or guidelines that researchers can use to assess the validity of their methods. One potential approach is to develop a suite of benchmark tasks or datasets that are specifically designed to test the ability of interpretability techniques to capture meaningful computations. These benchmarks could include tasks that require specific types of reasoning or knowledge, and the performance of interpretability techniques could be evaluated based on their ability to identify the relevant computations. Another approach would be to develop quantitative metrics that measure the degree to which an interpretability technique captures the underlying structure of the model. For example, one could measure the correlation between the latent representations of the SAE and the activations of specific layers in the transformer. The paper should also discuss the limitations of current interpretability techniques and suggest directions for future research.

Finally, the paper should explore alternative interpretability techniques that may be more robust to the limitations of SAEs. For example, the authors could investigate the use of attention mechanisms or gradient-based methods to identify the most important features or computations in the transformer. These methods may be less sensitive to the specific architecture of the model and more capable of capturing meaningful computations. The paper should also discuss the potential for combining different interpretability techniques to obtain a more comprehensive understanding of the model. By exploring a wider range of techniques, the paper could provide a more complete picture of the challenges and opportunities in the field of mechanistic interpretability.

### Questions

1. What are the implications of the findings for the field of mechanistic interpretability?
2. How can interpretability techniques be validated to ensure that they are capturing meaningful computations, rather than just artifacts of the model or training process?

### Rating

6

### Confidence

3

**********