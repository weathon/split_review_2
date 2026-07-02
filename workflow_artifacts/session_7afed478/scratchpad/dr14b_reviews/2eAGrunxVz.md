### Summary

This paper introduces Spherical Watermark, a novel framework for lossless watermarking in diffusion models that eliminates the need for encryption. The key innovation is a spherical mapping module that transforms binary watermarks into Gaussian noise, making the watermarked images indistinguishable from unwatermarked ones while ensuring robust extraction. The method is shown to outperform existing watermarking approaches in terms of undetectability, traceability, and computational efficiency.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. **Lossless Embedding**: The spherical mapping module ensures that the watermarked noise distribution is statistically indistinguishable from standard Gaussian noise, preserving the original image quality.
2. **Encryption-Free**: The method eliminates the need for per-image key storage, simplifying deployment and reducing overhead.
3. **Robustness**: The framework demonstrates strong resilience against various post-processing and adversarial attacks, outperforming existing lossy and lossless watermarking schemes.

### Weaknesses

#### Some Related Works


#### comment

1. **Theoretical Justification**: The paper provides a theoretical analysis of the spherical mapping module, but the assumptions and limitations of this analysis could be more thoroughly discussed. Specifically, the analysis should delve deeper into the conditions under which the spherical mapping truly preserves the Gaussian distribution, especially considering the finite precision of practical implementations. The impact of the dimensionality of the latent space on the effectiveness of the spherical mapping also warrants further investigation. It is not clear if the theoretical guarantees hold across different latent space sizes and structures.

2. **Scalability**: While the method is efficient, the scalability to very large models or datasets is not explicitly addressed. The paper lacks a detailed analysis of how the computational cost and memory requirements scale with increasing model size and the number of watermarked images. This is particularly important for practical applications where models and datasets can be extremely large. The paper should also discuss the potential bottlenecks in the proposed pipeline when applied to large-scale scenarios.

3. **Generalization**: The experiments are primarily conducted on Stable Diffusion models. It would be beneficial to see how the method generalizes to other types of diffusion models or generative architectures. The paper should explore the applicability of the spherical mapping module to different latent space structures and noise distributions used in other diffusion models. It is not clear if the method can be easily adapted to models with different noise scheduling or sampling techniques.

### Suggestions

To strengthen the theoretical justification, the authors should provide a more detailed analysis of the spherical mapping module's behavior under various conditions. This should include a discussion of the impact of finite precision arithmetic on the Gaussian distribution of the watermarked noise. Specifically, the analysis should quantify the deviation from the ideal Gaussian distribution due to the discretization of the latent space and the finite bit-depth of the noise values. Furthermore, the authors should investigate the relationship between the dimensionality of the latent space and the effectiveness of the spherical mapping. It would be beneficial to provide a theoretical bound on the distortion introduced by the spherical mapping as a function of the latent space dimensionality. This would help to understand the limitations of the method and identify the scenarios where it is most effective. The authors should also explore the sensitivity of the method to different noise distributions and provide a theoretical analysis of its robustness to deviations from the standard Gaussian distribution.

To address the scalability concerns, the authors should conduct a more thorough analysis of the computational cost and memory requirements of the proposed method. This should include a breakdown of the time and memory consumption for each step of the watermarking pipeline, including the spherical mapping, embedding, and extraction processes. The analysis should consider the impact of model size, dataset size, and watermark length on the overall performance. The authors should also investigate the potential bottlenecks in the pipeline and propose strategies to optimize the performance for large-scale applications. This could involve exploring parallel processing techniques or using more efficient data structures. Furthermore, the authors should provide empirical results demonstrating the scalability of the method on large models and datasets, including a comparison with existing watermarking techniques.

To improve the generalization of the method, the authors should conduct experiments on a wider range of diffusion models and generative architectures. This should include models with different latent space structures, noise distributions, and sampling techniques. The authors should also investigate the impact of different noise schedules on the performance of the watermarking method. It would be beneficial to explore the applicability of the spherical mapping module to other types of generative models, such as GANs or VAEs. The authors should also discuss the potential challenges in adapting the method to different architectures and provide guidelines for selecting the appropriate parameters for each model. This would help to establish the broader applicability of the proposed method and identify its limitations.

### Questions

1. **Computational Complexity**: How does the computational complexity of the spherical mapping module compare to traditional encryption-based methods, especially for high-dimensional latent spaces?
2. **Adversarial Robustness**: What are the limitations of the method against more sophisticated adversarial attacks that specifically target the spherical mapping or the Gaussian noise distribution?

### Rating

6

### Confidence

3

**********