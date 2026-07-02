### Summary

This paper presents SigMap, a multimodal foundation model for wireless localization that addresses the challenge of achieving precise localization across diverse environments. The model introduces two key innovations: a cycle-adaptive masking strategy that adjusts masking patterns based on channel periodicity to learn robust wireless representations, and a "map-as-prompt" framework that integrates 3D geographic information for effective cross-scenario adaptation. Extensive experiments demonstrate that SigMap achieves state-of-the-art performance across multiple localization tasks, showing strong zero-shot generalization in unseen environments and significantly outperforming both supervised and self-supervised baselines.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The paper proposes a cycle-adaptive masking strategy that dynamically adjusts masking patterns based on channel periodicity characteristics to learn robust wireless representations. This approach disrupts periodic shortcuts, forcing the model to learn globally meaningful signal representations.
2. The paper introduces a novel "map-as-prompt" framework that integrates 3D geographic information through lightweight soft prompts. This allows for effective cross-scenario adaptation by incorporating environmental constraints during fine-tuning, enhancing accuracy in complex multipath scenarios.
3. The model demonstrates strong zero-shot generalization capabilities, performing well in unseen environments and base station configurations with minimal labeled data.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's evaluation is primarily based on simulated datasets, which may not fully capture the complexities of real-world environments. The use of ray-tracing simulations, while useful, does not account for all the nuances of real-world signal propagation, such as unpredictable multipath effects, non-line-of-sight conditions, and environmental dynamics. This raises concerns about the practical applicability of the proposed method in real-world scenarios where the signal characteristics can be significantly different from the simulated conditions.
2. While the paper compares against several baselines, it could benefit from a more comprehensive comparison with other state-of-the-art foundation models in wireless localization. The current comparison lacks a detailed analysis against models that specifically address similar challenges in wireless signal processing and localization, making it difficult to ascertain the true novelty and performance gains of the proposed approach. A more thorough comparison should include models that utilize different architectural designs and training strategies.
3. The paper could provide more details on the computational complexity and real-time performance of the proposed model. The description of the model's architecture and training process lacks a detailed analysis of the computational resources required, such as memory usage, processing time, and energy consumption. This is crucial for assessing the feasibility of deploying the model in resource-constrained environments or for real-time applications. The paper should also discuss the scalability of the model with respect to the size of the input data and the number of parameters.

### Suggestions

To address the limitations of relying solely on simulated data, the authors should conduct experiments using real-world datasets to validate the performance of SigMap in practical scenarios. This would involve collecting channel state information (CSI) data from diverse environments, including indoor and outdoor settings with varying levels of multipath interference and non-line-of-sight conditions. The evaluation should also include a detailed analysis of the model's robustness to noise and interference, which are common in real-world wireless environments. Furthermore, the authors should explore techniques for domain adaptation to bridge the gap between simulated and real-world data, such as using adversarial training or transfer learning methods. This would help to ensure that the model generalizes well to unseen environments and is not overfitting to the specific characteristics of the simulated data. The inclusion of real-world experiments would significantly strengthen the paper's claims and demonstrate the practical applicability of the proposed method.

To provide a more comprehensive comparison with state-of-the-art methods, the authors should include a wider range of baselines that represent different approaches to wireless localization. This should include models that utilize different architectural designs, such as convolutional neural networks, recurrent neural networks, and graph neural networks, as well as models that employ different training strategies, such as supervised, unsupervised, and semi-supervised learning. The comparison should also include a detailed analysis of the strengths and weaknesses of each baseline, highlighting the specific scenarios where the proposed method outperforms or underperforms the existing approaches. Furthermore, the authors should provide a quantitative analysis of the computational complexity and memory requirements of each baseline, allowing for a more comprehensive assessment of the trade-offs between performance and resource consumption. This would provide a more complete picture of the proposed method's performance relative to the state-of-the-art and help to identify areas for further improvement.

To address the lack of details on computational complexity and real-time performance, the authors should provide a detailed analysis of the model's resource requirements, including memory usage, processing time, and energy consumption. This should include a breakdown of the computational cost of each component of the model, such as the transformer layers, the masking strategy, and the map-as-prompt framework. The authors should also discuss the scalability of the model with respect to the size of the input data and the number of parameters, as well as the potential for optimizing the model for deployment on resource-constrained devices. Furthermore, the authors should provide an analysis of the model's real-time performance, including the time required to process a single sample and the latency introduced by the model. This would help to assess the feasibility of deploying the model in real-time applications and identify potential bottlenecks that need to be addressed.

### Questions

1. How does the cycle-adaptive masking strategy compare to other advanced masking techniques in terms of computational efficiency and performance? Could the authors provide more details on the trade-offs involved in using this approach?
2. The paper demonstrates strong zero-shot generalization, but how does the model perform with limited fine-tuning in new environments? Are there specific conditions or environments where the model's performance degrades significantly?
3. The integration of 3D geographic information is a key aspect of the proposed method. How sensitive is the model's performance to the accuracy and resolution of the 3D maps used? Are there any specific requirements or limitations regarding the quality of the map data?
4. Could the authors provide more details on the computational complexity and real-time performance of the proposed model? How does it compare to existing methods in terms of resource requirements and latency?
5. The paper focuses on wireless localization. Are there other potential applications for the proposed cycle-adaptive masking and map-as-prompt techniques in different areas of wireless communication or signal processing?

### Rating

5

### Confidence

4

**********