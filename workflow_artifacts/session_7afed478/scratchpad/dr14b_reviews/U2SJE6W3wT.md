### Summary

This paper proposes an improved Adversarial Diffusion Compression (ADC) method for real-world video super-resolution (Real-VSR). The authors distill a large diffusion Transformer (DiT) teacher DOVE into a pruned 2D Stable Diffusion (SD)-based AdcSR backbone, augmented with lightweight 1D temporal convolutions. A dual-head adversarial distillation scheme is introduced to balance the optimization of details and temporal consistency. Experiments demonstrate that the resulting compressed AdcVSR model reduces complexity by 95% in parameters and achieves an 8× acceleration over its DiT teacher DOVE, while maintaining competitive video quality and efficiency.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed Adversarial Diffusion Compression (ADC) method is novel and effective. The authors propose a new adversarial distillation scheme that decouples the discriminations of details and consistency into two heads sharing a common network backbone, applied in both VAE decoder’s feature space and the pixel space. This design enables balanced optimization, avoiding collapse into either over-smoothed outputs (loss of spatial details) or flickering (loss of temporal consistency).
2. The authors demonstrate that a 2D image diffusion backbone augmented with lightweight 1D temporal convolutions can effectively learn Real-VSR mapping from 3D diffusion Transformer (DiT) teacher. This is a significant contribution as it shows that a more efficient 2D architecture can achieve comparable performance to a larger 3D architecture.
3. The proposed method achieves significant efficiency gains while maintaining competitive video quality. The AdcVSR model reduces parameters by 95% and achieves an 8× acceleration over its teacher DOVE, making it more suitable for real-world applications.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed analysis of the computational cost of the proposed method. While the authors claim that their method is more efficient, they do not provide a breakdown of the computational cost of each component of the model, such as the 2D backbone, the 1D temporal convolutions, and the dual-head adversarial distillation scheme. This makes it difficult to understand the trade-offs between performance and efficiency. Specifically, the FLOPs and memory access patterns for each component should be analyzed to provide a more complete picture of the computational overhead.
2. The paper does not provide a comparison of the proposed method with other state-of-the-art video super-resolution methods in terms of computational cost. While the authors compare their method with other methods in terms of performance, they do not provide a comparison of the computational cost of their method with other methods. This makes it difficult to assess the practical applicability of the proposed method. A comparison of FLOPs, inference time, and memory usage with other methods would be beneficial.
3. The paper does not provide a detailed analysis of the impact of the different components of the proposed method on the overall performance. While the authors provide an ablation study of the dual-head adversarial distillation scheme, they do not provide a detailed analysis of the impact of the 2D backbone and the 1D temporal convolutions on the overall performance. This makes it difficult to understand the contribution of each component to the overall performance. For example, the impact of different kernel sizes and numbers of channels in the 1D temporal convolutions should be analyzed.
4. The paper does not provide a detailed analysis of the limitations of the proposed method. While the authors mention that their method is more efficient, they do not discuss the limitations of their method in terms of performance, computational cost, or generalization ability. For example, the authors should discuss the performance of their method on different types of videos, such as videos with fast motion or complex scenes, and the computational cost of their method on different hardware platforms.

### Suggestions

The paper would benefit from a more thorough analysis of the computational cost associated with the proposed Adversarial Diffusion Compression (ADC) method. While the authors claim efficiency gains, a detailed breakdown of FLOPs, memory access patterns, and inference time for each component (2D backbone, 1D temporal convolutions, and dual-head adversarial distillation) is crucial. This analysis should include a comparison with other state-of-the-art video super-resolution methods, providing a clear understanding of the trade-offs between performance and computational resources. Furthermore, the authors should explore the impact of different architectural choices within their model, such as varying the kernel sizes and number of channels in the 1D temporal convolutional layers, and analyze how these choices affect both performance and computational cost. This would provide a more complete picture of the model's behavior and allow for a more informed assessment of its practical applicability.

To strengthen the paper, the authors should conduct a more comprehensive ablation study that isolates the impact of each component on the overall performance. Specifically, the contribution of the 2D backbone and the 1D temporal convolutions should be analyzed in detail. This could involve ablating each component individually and in combination, and evaluating the resulting performance on a range of video datasets. The analysis should not only focus on quantitative metrics but also include qualitative assessments of the generated video frames, highlighting the strengths and weaknesses of each configuration. This would provide a more nuanced understanding of the model's behavior and allow for a more informed assessment of its practical applicability. Additionally, the authors should explore the sensitivity of the model to different hyperparameter settings, such as the learning rate, batch size, and number of training epochs, and provide guidelines for selecting appropriate values for different datasets and hardware platforms.

Finally, the paper should include a more detailed discussion of the limitations of the proposed method. This should include an analysis of the model's performance on different types of videos, such as those with fast motion, complex scenes, or significant occlusions. The authors should also discuss the computational cost of their method on different hardware platforms, including both GPUs and CPUs, and provide guidelines for selecting appropriate hardware for different use cases. Furthermore, the authors should discuss the potential for further improvements to their method, such as exploring different architectures for the 2D backbone or the 1D temporal convolutions, or incorporating additional regularization techniques. This would provide a more complete picture of the model's capabilities and limitations and guide future research in this area.

### Questions

1. Can you provide a detailed analysis of the computational cost of the proposed method, including the FLOPs and memory access patterns for each component of the model?
2. Can you provide a comparison of the proposed method with other state-of-the-art video super-resolution methods in terms of computational cost, including FLOPs, inference time, and memory usage?
3. Can you provide a detailed analysis of the impact of the different components of the proposed method on the overall performance, including the 2D backbone and the 1D temporal convolutions?
4. Can you provide a detailed analysis of the limitations of the proposed method, including its performance on different types of videos and its computational cost on different hardware platforms?

### Rating

6

### Confidence

3

**********