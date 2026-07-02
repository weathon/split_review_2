### Summary

This paper introduces a novel tokenization method for robot action sequences, FASTerVQ, which addresses the trade-off between reconstruction fidelity and inference efficiency in autoregressive vision-language-action (VLA) models. FASTerVQ encodes action chunks as single-channel images, capturing global spatio-temporal dependencies while maintaining a high compression ratio. Building upon this, FASTerVLA employs block-wise autoregressive decoding and a lightweight action expert, achieving faster inference and improved task performance. Extensive experiments demonstrate that FASTerVQ achieves superior reconstruction quality, high token utilization, and strong generalization across different tasks and robot embodiments. Furthermore, FASTerVLA surpasses previous state-of-the-art models in both inference speed and task performance.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces FASTer, a novel framework that combines a learnable action tokenizer (FASTerVQ) and an autoregressive VLA model (FASTerVLA) to improve efficiency and performance in robotic manipulation tasks. The approach of encoding action chunks as single-channel images to capture spatio-temporal dependencies is innovative.
2. The paper is well-structured and clearly written. The authors effectively communicate complex ideas and provide detailed explanations of the methodology.
3. The paper addresses a critical challenge in autoregressive VLA models-the trade-off between reconstruction fidelity and inference efficiency. The proposed solution has practical implications for real-world robotic applications.

### Weaknesses

#### Some Related Works


#### comment

1. While the paper demonstrates strong results, it would be beneficial to analyze the limitations of the proposed method and potential failure cases. For example, how does the model perform in highly dynamic environments or with unexpected obstacles? Are there specific types of tasks or environments where FASTerVQ and FASTerVLA struggle? Understanding these limitations would provide a more complete picture of the method's applicability and robustness.
2. The paper could benefit from a more detailed comparison with existing action tokenization methods and autoregressive VLA models. While the authors mention that existing tokenization methods fail to comprehensively satisfy the four key requirements, a more thorough analysis and comparison would strengthen the paper's claims. For example, a quantitative comparison with other tokenization methods on the same datasets and tasks would provide a clearer picture of the advantages of FASTerVQ. Similarly, a more detailed comparison with other autoregressive VLA models, highlighting the specific improvements brought by FASTerVLA, would be valuable.
3. The paper introduces several new metrics, such as Valid Reconstruction Rate (VRR), but it would be helpful to provide more context and justification for these metrics. How do these metrics relate to existing evaluation metrics in the field? Why are they particularly suitable for evaluating action tokenization methods? A more detailed explanation of the metrics and their significance would enhance the paper's clarity and impact.

### Suggestions

To further strengthen the paper, the authors should consider a more in-depth analysis of the failure modes of FASTerVQ and FASTerVLA. Specifically, it would be beneficial to investigate the model's performance in scenarios with significant deviations from the training data, such as novel object configurations, unexpected environmental changes, or interactions with dynamic obstacles. For instance, how does the model handle situations where the robot's gripper encounters unexpected resistance or slippage? A detailed analysis of these edge cases would provide a more comprehensive understanding of the model's robustness and limitations. Furthermore, exploring the sensitivity of the model to variations in the training data, such as different action sequences or environmental conditions, would also be valuable. This could involve experiments with augmented datasets or adversarial examples to identify potential weaknesses in the model's generalization capabilities. Such analysis would not only highlight the current limitations but also guide future research directions for improving the model's robustness and adaptability.

In addition to a more detailed comparison with existing methods, the authors should also consider a more thorough analysis of the computational complexity and resource requirements of FASTerVQ and FASTerVLA. This could involve a breakdown of the computational cost of each component of the model, such as the tokenizer, the autoregressive decoder, and the action expert. Comparing these costs with those of existing methods would provide a clearer picture of the trade-offs between performance and efficiency. Furthermore, it would be beneficial to investigate the scalability of the model to larger and more complex tasks. For example, how does the model's performance and computational cost scale with the length of the action sequence or the number of degrees of freedom in the robot? This analysis would help to identify potential bottlenecks and guide future efforts to optimize the model for real-world applications. The authors could also explore techniques such as model pruning or quantization to reduce the computational footprint of the model without significantly sacrificing performance.

Finally, the authors should provide a more detailed explanation of the design choices behind the proposed metrics, particularly the Valid Reconstruction Rate (VRR). While the paper introduces this metric, it would be helpful to provide a more thorough justification for its use and its relationship to existing evaluation metrics. For example, how does VRR relate to metrics such as reconstruction error or perceptual quality? Why is VRR particularly suitable for evaluating action tokenization methods? A more detailed discussion of these points would enhance the paper's clarity and impact. Furthermore, the authors could consider including additional metrics to provide a more comprehensive evaluation of the model's performance. For example, metrics such as the diversity of generated actions or the consistency of the model's predictions could provide valuable insights into the model's behavior. The authors should also discuss the limitations of the proposed metrics and potential avenues for future research in this area.

### Questions

1. Could you provide more details on the computational resources required for training and inference? This information would be valuable for researchers looking to implement and build upon your work.
2. How does the proposed method handle noisy or incomplete sensory information? Robotic systems often encounter such data in real-world settings, and understanding how FASTerVQ and FASTerVLA perform under these conditions would be valuable.
3. The paper focuses on specific robotic manipulation tasks. How well do you expect the proposed method to generalize to other types of robotic tasks, such as navigation or exploration? Are there any modifications or adaptations that would be needed to apply FASTerVQ and FASTerVLA to these different domains?

### Rating

6

### Confidence

3

**********