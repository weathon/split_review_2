### Summary

This paper introduces a novel approach for detecting AI-generated images by incorporating structural semantic features. The method uses cuboidal partitioning to recursively divide images into sub-regions, capturing hierarchical structural information that is often overlooked by existing detectors. By integrating these structural features with the AIDE model, the authors achieve state-of-the-art performance on the GenImage benchmark and demonstrate strong generalization across multiple datasets, including AIGCDetect and Chameleon. The paper highlights the importance of structural semantics in AI-generated content (AIGC) detection and provides a comprehensive evaluation of the proposed method's effectiveness.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel approach by incorporating structural semantic features into AIGC detection, which is an unexplored area that significantly enhances detection capabilities. This approach provides a fresh perspective and adds a new dimension to the field of AIGC detection.

2. The method is rigorously tested across multiple benchmarks, including GenImage, AIGCDetect, and Chameleon, demonstrating its robustness and generalization capabilities. The consistent superior performance across these datasets highlights the method's effectiveness and reliability.

3. The paper is well-organized and clearly written, making the technical details and novel contributions accessible to readers. The structured presentation helps in understanding the complex methodologies and experimental results.

4. By addressing the limitations of existing AIGC detection methods, this work has significant implications for the field of digital media forensics. It offers a powerful new tool for detecting AI-generated content, which is crucial in the fight against misinformation and for copyright protection.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion on the computational complexity and efficiency of the proposed method. While the method shows strong performance, the practical implications of its computational demands, especially when dealing with high-resolution images or large datasets, are not fully explored. A more thorough analysis of the time and space complexity, including a breakdown of the computational cost associated with the cuboidal partitioning and feature extraction, would be valuable.

2. While the paper demonstrates strong performance on the tested datasets, it would be valuable to explore the method's robustness against various image transformations and compression techniques. The current evaluation lacks a systematic analysis of how common image manipulations, such as JPEG compression at different quality levels, rotation by various angles, and resampling with different interpolation methods, affect the detection accuracy. Understanding these limitations is crucial for practical deployment, as real-world images often undergo such transformations.

3. The paper could provide more insights into the choice of parameters for the cuboidal partitioning and how they affect the detection performance. A sensitivity analysis of parameters such as the number of partitions, the size of the cuboids, and the criteria for recursive division is needed. This would help in understanding the trade-offs between detection accuracy and computational cost, and provide guidance on how to optimize these parameters for different types of images and applications.

### Suggestions

To address the computational complexity concerns, the authors should include a detailed analysis of the time and space complexity of their method. This analysis should consider the impact of image size and the number of partitions on the overall computational cost. Specifically, they should provide a breakdown of the time spent on each step of the process, such as the cuboidal partitioning, feature extraction, and classification. Furthermore, they should explore potential optimizations to reduce the computational overhead, such as using more efficient data structures or parallel processing techniques. This would help in assessing the scalability of the method for real-world applications and provide practical guidance for its implementation. For example, the authors could investigate the use of hierarchical data structures to store the partitioned image regions, which could reduce memory usage and improve access times. Additionally, they could explore the use of GPU acceleration for the feature extraction process, which could significantly speed up the computation.

To enhance the robustness analysis, the authors should conduct a systematic evaluation of their method's performance under various image transformations and compression techniques. This should include a range of common manipulations, such as JPEG compression at different quality levels, rotation by various angles, resampling with different interpolation methods, and adding noise. The results should be presented in a clear and concise manner, allowing for a thorough understanding of how these transformations affect the detection accuracy. This analysis would provide valuable insights into the limitations of the method and help in developing strategies to improve its robustness for practical deployment. For instance, the authors could investigate the use of data augmentation techniques during training to improve the model's generalization capabilities. They could also explore the use of adversarial training methods to make the model more robust to specific types of image manipulations. Furthermore, the authors should consider evaluating the method's performance on images with different resolutions and aspect ratios to ensure its applicability to a wide range of real-world scenarios.

To provide more insights into the parameter selection, the authors should conduct a sensitivity analysis of the cuboidal partitioning parameters. This analysis should explore the impact of different parameter values on the detection performance and computational cost. Specifically, they should investigate the effect of varying the number of partitions, the size of the cuboids, and the criteria for recursive division. The results should be presented in a way that allows for a clear understanding of the trade-offs between detection accuracy and computational cost. Based on this analysis, the authors should provide recommendations on how to choose the optimal parameter values for different types of images and applications. This would make the method more practical and easier to use for a wider range of scenarios. For example, the authors could provide a set of guidelines for selecting the optimal number of partitions based on the image resolution and the desired level of detail. They could also investigate the use of adaptive partitioning strategies that automatically adjust the number of partitions based on the image content.

### Questions

1. Could the authors provide more details on the computational complexity and efficiency of the proposed method? How does it scale with larger datasets or higher-resolution images?

2. How robust is the proposed method to common image transformations and compression techniques? Are there any specific scenarios where the method might fail or underperform?

3. Can the authors provide more insights into the choice of parameters for the cuboidal partitioning? How sensitive is the detection performance to these parameters, and are there guidelines for selecting optimal values?

### Rating

8

### Confidence

4

**********