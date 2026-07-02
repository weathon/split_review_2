### Summary

This paper proposes a novel approach to merging large language models (LLMs) in latent space, addressing limitations in existing weight-space merging techniques. The key contributions include:

1. **Latent Space Encoding**: A transformer-based variational autoencoder (VAE) is used to encode model weights into a smooth, lower-dimensional latent space, enabling cross-architecture merging.
2. **Two-Stage Compression Curriculum**: A two-stage training process for the VAE is introduced to handle the computational demands of encoding large models and improve generalization to unseen weights.
3. **Dimensionality-Matching Projection**: A projection technique is developed to align latent spaces of models with different architectures, facilitating interpolation between them.
4. **Empirical Validation**: The paper demonstrates that latent-space interpolation outperforms weight-space averaging, especially for heterogeneous merges, across various benchmarks and model architectures.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. **Architecture-Agnostic Merging**: The latent space approach enables merging models with different architectures, overcoming a significant limitation of existing weight-space methods.
2. **Robustness to Heterogeneity**: The use of optimal transport (OT) for latent alignment ensures stable and effective merging even between models from different families.
3. **Comprehensive Evaluation**: The paper includes extensive experiments on various tasks and model architectures, demonstrating consistent performance gains over baselines.
4. **Theoretical Justification**: Provides a detailed analysis of LLM weight distributions and the theoretical basis for using VAEs in latent space merging.

### Weaknesses

#### Some Related Works


#### comment

1. **Computational Overhead**: The two-stage VAE training and latent encoding/decoding process introduce additional computational costs compared to simpler weight-space methods. The paper does not provide a detailed breakdown of the computational resources required for each stage of the VAE training, such as the time and memory consumption for the initial deterministic autoencoder training and the subsequent fine-tuning with the KL term. This makes it difficult to assess the practical scalability of the approach, especially for very large models. Furthermore, the paper lacks a comparison of the computational cost of their method against other merging techniques, such as Task Arithmetic, in terms of actual runtime and GPU memory usage.
2. **Sensitivity to Hyperparameters**: The method's performance is sensitive to the choice of VAE architecture and compression ratio. The paper does not provide a comprehensive sensitivity analysis of the VAE architecture, such as the number of layers, the dimensionality of the latent space, and the size of the hidden layers, on the final merging performance. This lack of analysis makes it challenging to determine the optimal VAE configuration for different model sizes and architectures. The paper also does not explore the impact of different compression ratios on the quality of the latent space and the resulting merged model performance.
3. **Limited Analysis of Merging Strategies**: The paper primarily focuses on linear interpolation in latent space, with limited exploration of more complex merging strategies. The paper does not investigate the impact of different interpolation methods, such as non-linear interpolation techniques or weighted averaging based on model performance. This lack of exploration limits the understanding of the full potential of latent space merging and may overlook more effective merging strategies.

### Suggestions

The paper would benefit from a more detailed analysis of the computational overhead associated with the proposed latent space merging method. Specifically, the authors should provide a breakdown of the computational resources required for each stage of the VAE training, including the time and memory consumption for the initial deterministic autoencoder training and the subsequent fine-tuning with the KL term. This analysis should also include a comparison of the computational cost of their method against other merging techniques, such as Task Arithmetic, in terms of actual runtime and GPU memory usage. Furthermore, the authors should explore techniques to reduce the computational cost of the VAE training, such as using more efficient VAE architectures or employing techniques like knowledge distillation to transfer the learned latent space to a smaller model. This would make the method more practical for large-scale applications and allow for a more fair comparison with other merging techniques.

To address the sensitivity to hyperparameters, the authors should conduct a more comprehensive sensitivity analysis of the VAE architecture on the final merging performance. This analysis should include a systematic exploration of the impact of different VAE architectures, such as the number of layers, the dimensionality of the latent space, and the size of the hidden layers, on the quality of the latent space and the resulting merged model performance. The authors should also investigate the impact of different compression ratios on the quality of the latent space and the resulting merged model performance. This analysis should provide guidelines for selecting the optimal VAE configuration for different model sizes and architectures. Additionally, the authors should explore techniques to make the method less sensitive to hyperparameter choices, such as using adaptive learning rate schedules or employing regularization techniques.

Finally, the paper should explore more complex merging strategies beyond linear interpolation in latent space. This could include investigating non-linear interpolation techniques, such as spherical interpolation or other non-linear transformations, and weighted averaging based on model performance or other criteria. The authors should also explore the impact of different interpolation methods on the final merged model performance. This exploration would provide a more comprehensive understanding of the full potential of latent space merging and may uncover more effective merging strategies. The authors should also investigate the impact of different merging strategies on the robustness of the merged model to different tasks and datasets.

### Questions

1. **Computational Cost Analysis**: Could you provide a more detailed breakdown of the computational resources required for VAE training and latent encoding/decoding, especially for larger models? How does this compare to the computational cost of other merging techniques like Task Arithmetic?
2. **Sensitivity to VAE Architecture**: How sensitive is the method's performance to the choice of VAE architecture and compression ratio? Have you explored different VAE designs or compression strategies?
3. **Impact of Merging Coefficient (λ)**: How does the choice of merging coefficient (λ) impact the performance of the merged model? Are there any guidelines for selecting an optimal λ for different tasks or model architectures?
4. **Comparison with Other Representation Merging Methods**: How does your method compare to other representation merging techniques, such as activation-informed merging methods, in terms of performance and computational efficiency?

### Rating

6

### Confidence

3

**********