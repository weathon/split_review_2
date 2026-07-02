### Summary

The paper presents a method for 3D style transfer using a transformer-based architecture. The method takes multiple views of a scene and a style reference image as input, and outputs a stylized 3D Gaussian representation of the scene. The key contributions of the paper are the use of a shared backbone with two pathways for geometry and style, the introduction of a voxel-level 3D style loss, and the development of a single-forward-pass pipeline for 3D style transfer.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to 3D style transfer using a transformer-based architecture. The use of a shared backbone with two pathways for geometry and style is a creative solution to the problem of disentangling geometry and style in 3D scenes.

2. The paper is well-written and easy to follow. The authors provide a clear explanation of the proposed method, including the architecture, training strategy, and style losses. The paper also includes a thorough ablation study that analyzes the impact of different design choices.

3. The proposed method is evaluated on multiple datasets and compared with state-of-the-art methods. The results show that the proposed method achieves high-quality stylization with strong cross-view consistency.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could provide more details on the computational resources required for training and inference. This would help readers understand the practical limitations of the proposed method.

2. The paper could discuss the potential impact of the proposed method on different applications, such as virtual reality or augmented reality.

3. The paper could provide more details on the limitations of the proposed method and potential directions for future work.

### Suggestions

The paper would benefit from a more thorough discussion of the computational demands of the proposed method. Specifically, the authors should provide a detailed breakdown of the training time, including the number of GPUs used, the batch size, and the time per epoch. Furthermore, the inference time should be analyzed in terms of the number of views processed and the time taken to generate the stylized 3D Gaussian representation. This analysis should also include the memory footprint of the model, which is crucial for practical deployment. A comparison with existing methods in terms of computational cost would also be valuable to understand the trade-offs of the proposed approach. This would allow readers to better assess the feasibility of using the method in resource-constrained environments.

Expanding on the potential applications of the proposed method would also strengthen the paper. While the paper mentions the possibility of using the method for virtual reality or augmented reality, it lacks specific details on how the method could be integrated into these applications. For example, the authors could discuss how the method could be used to create stylized 3D environments for VR experiences or how it could be used to augment real-world scenes with artistic styles in AR applications. A discussion of the challenges and opportunities associated with these applications would be beneficial. This would help readers understand the practical implications of the proposed method and its potential impact on different fields.

Finally, the paper should provide a more in-depth discussion of the limitations of the proposed method and potential avenues for future research. For example, the authors could discuss the limitations of the method in handling complex scenes with occlusions or self-intersections. They could also discuss the challenges of extending the method to handle dynamic scenes or scenes with varying lighting conditions. Furthermore, the authors could explore potential directions for future work, such as improving the quality of the stylized output, reducing the computational cost of the method, or extending the method to handle different types of input data. This would provide a more complete picture of the proposed method and its potential for future development.

### Questions

1. Can the authors provide more details on the computational resources required for training and inference?

2. Can the authors discuss the potential impact of the proposed method on different applications, such as virtual reality or augmented reality?

3. Can the authors provide more details on the limitations of the proposed method and potential directions for future work?

### Rating

6

### Confidence

3

**********