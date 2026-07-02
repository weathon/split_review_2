### Summary

The paper introduces a framework called HARA (Hybrid Arithmetic-ReLU Networks Approximation) that aims to optimize the deployment of Transformer models on resource-constrained edge devices. The key innovation is replacing computationally intensive non-linear operators (like GELU, Softmax, and LayerNorm) with a unified architecture based on simple arithmetic operations and a shallow ReLU network. This approach significantly reduces hardware complexity and power consumption while maintaining model performance. The framework uses dynamic programming for optimized parameter initialization, ensuring high-fidelity approximation of non-linear functions. Experiments across various models (BERT, Swin, LLaMA, Stable Diffusion) show that HARA achieves over 60% reduction in silicon area for non-linear processing with minimal impact on accuracy (<0.1% change) and is compatible with 8-bit quantization.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel approach to hardware-efficient non-linearity in Transformers by introducing a unified framework (HARA) that replaces diverse non-linear operators with a single, canonical architecture based on simple arithmetic primitives and a shallow ReLU network. This unified approach addresses the issue of hardware bloat associated with function-specific approximations.

2. The Optimized Parameter Initialization pipeline, which employs dynamic programming to derive near-optimal parameters for the ReLU approximator, is a key technical innovation. This systematic approach ensures high-fidelity approximation and robustness, overcoming the limitations of heuristic methods.

3. The paper provides strong empirical validation across four modern architectures (BERT, Swin, LLaMA, and Stable Diffusion), demonstrating that the proposed method maintains model performance with negligible accuracy impact while achieving significant hardware savings. The compatibility with 8-bit quantization further enhances its practicality for edge deployment.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's discussion on the limitations of the proposed framework is somewhat limited. While it mentions that the hardware benefits are based on synthesis estimations rather than a full physical implementation, it would be beneficial to have a more detailed discussion on the potential challenges and limitations that might arise during actual hardware deployment. For instance, the synthesis estimations might not fully capture the complexities of on-chip variations, power gating effects, or the impact of different process nodes on the performance of the unified ReLU network. A more thorough analysis of these factors would provide a more realistic assessment of the framework's practical applicability.

2. The paper could benefit from a more in-depth analysis of the trade-offs between the depth and width of the ReLU network used in the approximation. While the paper mentions using a shallow ReLU network, it does not provide a detailed exploration of how different network configurations impact both the approximation accuracy and the hardware complexity. For example, how does increasing the number of layers or the number of neurons per layer affect the accuracy of the approximation, and what are the corresponding changes in silicon area and power consumption? A more granular analysis of these trade-offs would provide valuable insights for practitioners.

3. While the paper demonstrates the effectiveness of HARA across several modern architectures, it would be valuable to include a more detailed analysis of the framework's performance on a wider range of edge devices with varying resource constraints. The current evaluation focuses on general hardware savings, but a more specific analysis of how HARA performs on different types of edge devices (e.g., mobile phones, embedded systems, IoT devices) with different memory and computational capabilities would be beneficial. This would help to better understand the practical applicability of the framework in real-world scenarios.

### Suggestions

To strengthen the paper, the authors should include a more detailed discussion on the potential challenges and limitations of the HARA framework during actual hardware deployment. This should go beyond the current mention of synthesis estimations and delve into specific issues such as on-chip variations, power gating effects, and the impact of different process nodes. For example, the authors could discuss how variations in transistor threshold voltages might affect the accuracy of the ReLU approximations and how these variations could be mitigated through design techniques. Furthermore, a more detailed analysis of the power consumption characteristics of the unified ReLU network, including dynamic and static power consumption, would be valuable. This would provide a more comprehensive understanding of the framework's practical applicability and limitations in real-world hardware implementations.

Additionally, the paper should include a more in-depth analysis of the trade-offs between the depth and width of the ReLU network used in the approximation. This analysis should explore how different network configurations impact both the approximation accuracy and the hardware complexity. For example, the authors could present a series of experiments where they vary the number of layers and the number of neurons per layer and then measure the resulting approximation accuracy and hardware resource usage. This would provide valuable insights into the optimal network configuration for different applications and resource constraints. The analysis should also consider the impact of different activation functions within the ReLU network, as this could also affect both accuracy and hardware complexity. A detailed exploration of these trade-offs would allow practitioners to make informed decisions when applying the HARA framework.

Finally, the authors should expand their evaluation to include a more diverse range of edge devices with varying resource constraints. This would involve testing the HARA framework on different types of edge devices, such as mobile phones, embedded systems, and IoT devices, and analyzing its performance in terms of both accuracy and hardware resource usage. The evaluation should also consider the impact of different memory and computational capabilities on the framework's performance. For example, the authors could investigate how the framework performs on devices with limited memory or slow processing units. This would provide a more comprehensive understanding of the framework's practical applicability and limitations in real-world scenarios and help to identify potential bottlenecks and areas for improvement.

### Questions

1. Could the authors elaborate on the potential challenges and limitations of the HARA framework during actual hardware deployment, beyond the synthesis estimations mentioned in the paper?

2. How does the performance of HARA vary across different types of edge devices with varying resource constraints? Are there specific device characteristics that could significantly impact the effectiveness of the proposed framework?

3. What are the potential trade-offs between the depth and width of the ReLU network used in the approximation, and how do these trade-offs affect both the approximation accuracy and the hardware complexity?

### Rating

6

### Confidence

3

**********