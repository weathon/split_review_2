### Summary

This paper introduces Continuous Online Action Detection (COAD) for egocentric videos, enabling real-time action recognition and adaptation from streaming data. The authors propose a novel benchmark, Ego-OAD, and demonstrate improved accuracy and generalization in personalized AI systems.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel task formulation, Continuous Online Action Detection (COAD), which addresses the limitations of traditional Online Action Detection (OAD) models. COAD allows models to learn and adapt continuously from streaming videos in real time, without storing data or requiring multiple training passes. This approach is particularly well-suited for dynamic, resource-constrained environments like wearable devices.

2. The paper introduces Ego-OAD, a large-scale benchmark dataset for egocentric online action detection. This dataset provides a diverse and realistic testbed for evaluating COAD models in first-person settings, contributing valuable resources to the field of egocentric vision.

3. The paper is well-structured and clearly explains the concepts and methodologies.

4. The experimental results demonstrate the effectiveness of the proposed COAD approach, showing improvements in both adaptation to users' environments and generalization to new scenarios.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed analysis of the computational efficiency of the COAD approach, especially for real-time applications on resource-constrained devices. Specifically, the paper lacks a discussion on the memory footprint of the model during continuous learning, which is crucial for deployment on wearable devices with limited RAM. Furthermore, the paper does not provide a breakdown of the inference latency, which is a critical factor for real-time performance. A more thorough analysis of the computational cost per frame or per action segment would be beneficial.

2. The paper primarily focuses on egocentric videos. It would be valuable to discuss the potential and challenges of applying the COAD approach to other types of video data or domains. For instance, the paper could explore the performance of COAD in exocentric videos, where the camera is not worn by a person, or in videos with different characteristics, such as those with lower frame rates or different types of motion. Additionally, the paper could discuss the potential impact of different camera viewpoints and motion patterns on the performance of the COAD model.

3. While the paper shows promising results, further investigation into the model's robustness to various real-world challenges, such as occlusions, varying lighting conditions, and complex backgrounds, would strengthen the findings. The paper could include experiments that specifically evaluate the performance of COAD under these challenging conditions. For example, the paper could analyze how the model's performance degrades when there are partial occlusions of the hands or the object being manipulated, or when the lighting conditions change abruptly. Furthermore, the paper could explore the impact of complex backgrounds with clutter and dynamic elements on the accuracy of the action detection.

### Suggestions

To address the lack of detailed computational analysis, the authors should include a comprehensive breakdown of the computational costs associated with the COAD model. This should include a detailed analysis of the FLOPs, memory footprint, and latency of each component of the model, such as the feature extraction, temporal processing, and adaptation modules. Furthermore, the authors should provide a clear comparison of the computational overhead of COAD compared to traditional offline training methods. This comparison should include metrics such as training time, inference time, and memory usage. The authors could also explore techniques for optimizing the computational efficiency of the COAD model, such as model compression, quantization, or pruning. This would make the approach more practical for real-time applications on resource-constrained devices. Additionally, the authors should provide a discussion of the trade-offs between accuracy and computational efficiency, which would be valuable for practitioners who want to deploy the COAD model in real-world applications.

To broaden the scope of the paper, the authors should explore the potential and challenges of applying the COAD approach to other types of video data or domains. This could include experiments on exocentric videos, where the camera is not worn by a person, or in videos with different characteristics, such as those with lower frame rates or different types of motion. The authors should also discuss the potential impact of different camera viewpoints and motion patterns on the performance of the COAD model. This discussion should include an analysis of the strengths and weaknesses of the COAD approach in different scenarios, and should provide guidance for practitioners who want to apply the approach to new domains. Furthermore, the authors could explore the use of domain adaptation techniques to improve the performance of COAD in different domains. This could involve techniques such as fine-tuning the model on a small amount of data from the target domain or using adversarial training to learn domain-invariant features.

To further investigate the robustness of the COAD model, the authors should include experiments that specifically evaluate the performance of COAD under various real-world challenges, such as occlusions, varying lighting conditions, and complex backgrounds. This could include experiments with synthetic occlusions, where parts of the hands or objects are intentionally hidden, or with videos that have different lighting conditions or complex backgrounds. The authors should also analyze how the model's performance degrades under these challenging conditions and discuss potential strategies for improving the robustness of the model. This could include the use of data augmentation techniques, robust feature extraction methods, or adversarial training. The authors should also provide a quantitative analysis of the impact of these challenges on the accuracy of the action detection, and should discuss the limitations of the COAD model in these scenarios.

### Questions

Please see the weaknesses.

### Rating

6

### Confidence

3

**********