### Summary

This paper introduces TWINFLOW, a novel framework for achieving one-step generation in large-scale generative models without the need for auxiliary networks or pre-trained teacher models. By extending the time interval and introducing twin trajectories, TWINFLOW enables efficient and high-quality generation, demonstrating strong performance on benchmarks like GenEval and DPG-Bench, especially with the Qwen-Image-20B model.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel approach to achieving one-step generation in large-scale generative models, which is a significant advancement in the field.
2. The proposed method is well-motivated and grounded in theoretical analysis, providing a solid foundation for the approach.
3. The experimental results are comprehensive and demonstrate the effectiveness of TWINFLOW across various benchmarks and model sizes.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed method, particularly in scenarios where the assumptions made by the twin-trajectory concept may not hold. Specifically, the assumption that the noise distribution is symmetric and centered around zero may not always be valid in practice, and the impact of deviations from this assumption on the performance of TWINFLOW should be explored. Furthermore, the paper does not address the potential for mode collapse or reduced diversity in the generated samples, which is a common issue in one-step generative models.
2. While the paper provides a comparison with existing methods, a more in-depth analysis of the computational cost and efficiency of TWINFLOW compared to other one-step generation techniques would be valuable. The paper should include a breakdown of the computational resources required for training and inference, including memory usage and FLOPs, and compare these metrics with other state-of-the-art one-step methods. This would provide a more complete picture of the practical trade-offs associated with TWINFLOW.
3. The paper could explore the potential for extending the twin-trajectory concept to other types of generative models beyond flow-based models, such as GANs or VAEs. The current formulation of TWINFLOW is tightly coupled with the flow-matching framework, and it is unclear how the twin-trajectory concept could be adapted to other generative frameworks. A discussion of the challenges and potential solutions for extending TWINFLOW to other model architectures would be beneficial.

### Suggestions

To address the limitations regarding the assumptions of the twin-trajectory concept, the authors should conduct experiments with different noise distributions that deviate from the standard Gaussian, such as non-symmetric or heavy-tailed distributions. This would provide a more robust evaluation of the method's performance under various conditions. Additionally, the authors should investigate the diversity of the generated samples using metrics such as Fréchet Inception Distance (FID) and Kernel Inception Distance (KID), and compare these results with those of multi-step methods. This would help to quantify the potential trade-off between generation speed and sample diversity. Furthermore, the authors could explore techniques to mitigate mode collapse, such as incorporating regularization terms or using more sophisticated sampling strategies.

To provide a more comprehensive analysis of the computational cost, the authors should include a detailed breakdown of the memory usage and FLOPs required for both training and inference. This should include a comparison with other one-step generation methods, such as consistency models and distillation techniques. The authors should also investigate the scalability of TWINFLOW to larger models and datasets, and discuss the potential bottlenecks that may arise. This would provide a more practical understanding of the method's efficiency and its suitability for real-world applications. Furthermore, the authors should explore techniques to optimize the implementation of TWINFLOW, such as using mixed-precision training or model compression methods.

Finally, to broaden the applicability of the twin-trajectory concept, the authors should explore potential extensions to other generative models, such as GANs and VAEs. For GANs, the authors could investigate how the twin-trajectory concept could be incorporated into the discriminator or generator networks. For VAEs, the authors could explore how the twin-trajectory concept could be used to improve the quality of the generated samples. The authors should also discuss the challenges and potential solutions for adapting the twin-trajectory concept to these different model architectures. This would demonstrate the versatility of the proposed method and its potential for broader impact.

### Questions

1. How does the performance of TWINFLOW compare to other one-step generation methods in terms of computational cost and efficiency?
2. Can the twin-trajectory concept be extended to other types of generative models beyond flow-based models?
3. What are the potential limitations of the twin-trajectory concept, and how might these limitations be addressed in future work?

### Rating

6

### Confidence

3

**********