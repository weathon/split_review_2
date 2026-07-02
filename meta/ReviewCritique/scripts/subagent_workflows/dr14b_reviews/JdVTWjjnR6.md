### Summary

This paper proposes a Hippocampal-Thalamic inspired dual-stream Network (HiTNet) for multimodal sentiment analysis under missing data. The Hippocampal-inspired intra-modal enhancement stream employs semantic memory modules with dynamic retrieval and sparse activation networks to mine modality-specific information and reconstruct missing features. Thalamic-inspired inter-modal regulation stream implements confidence perception and adaptive cross-modal completion modules to dynamically integrate high-quality cross-modal information while suppressing redundant interference. Comprehensive experiments on MOSI, MOSEI, and SIMS demonstrate that HiTNet achieves superior performance with 1.5%–2.0% average accuracy improvements over state-of-the-art methods across all missing rates and maintains 72.20% accuracy under extreme 90% missing conditions on MOSEI, validating the effectiveness of brain function-inspired design for robust multimodal sentiment analysis even under extreme missing data scenarios.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-organized and clearly written, making it easy to follow the proposed methodology and experimental results.
2. The authors provide a comprehensive review of related work, which helps to contextualize their contributions within the existing literature.
3. The experimental setup is thorough, with detailed descriptions of datasets, evaluation metrics, and baseline comparisons. The results are presented clearly, and the analysis is insightful.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from more detailed explanations of certain technical choices, such as the specific configurations of the semantic memory module and the sparse activation network. For instance, the paper does not specify the dimensionality of the memory vectors or the retrieval mechanism used in the semantic memory module. Similarly, the sparse activation network's architecture, including the number of layers and activation functions, is not clearly defined. This lack of detail makes it difficult to reproduce the results and understand the impact of these components on the overall performance.
2. While the authors claim that their method is robust to missing data, the paper does not provide a detailed analysis of how the performance degrades with increasing missing rates. It would be beneficial to see a more granular breakdown of performance across different missing data scenarios, including specific missing rates for each modality. For example, the paper should show how the model performs when only the visual modality is missing, or when all modalities are missing at different rates. This would provide a more comprehensive understanding of the model's robustness.

### Suggestions

To enhance the paper, the authors should provide a more detailed explanation of the semantic memory module and the sparse activation network. Specifically, they should clarify the dimensionality of the memory vectors, the retrieval mechanism (e.g., cosine similarity, dot product), and the specific activation functions used in the sparse activation network. Furthermore, the paper should include a sensitivity analysis of these components, showing how different configurations affect the overall performance. For example, the authors could vary the size of the memory module or the sparsity level in the activation network and report the corresponding changes in accuracy. This would provide a deeper understanding of the model's behavior and allow for better reproducibility.

Additionally, the authors should provide a more detailed analysis of the model's performance under different missing data scenarios. Instead of just reporting the average performance across all missing rates, the paper should include a breakdown of performance at specific missing rates for each modality. For example, the authors could show how the model performs when the visual modality is missing at 10%, 20%, 30%, etc., and similarly for the audio and text modalities. This would provide a more granular understanding of the model's robustness and allow for a more thorough comparison with other methods. The authors should also analyze the performance degradation patterns as the missing rate increases, which could reveal potential weaknesses in the model's design.

Finally, the authors should consider including a visualization of the learned semantic memory representations. This could provide insights into how the model is capturing modality-specific information and how it is using this information to reconstruct missing features. For example, the authors could use t-SNE or PCA to project the high-dimensional memory vectors into a 2D space and visualize the clusters of similar features. This would not only enhance the interpretability of the model but also provide a more compelling argument for the effectiveness of the proposed approach.

### Questions

1. Can the authors provide more details on the computational complexity of HiTNet compared to other methods? How does the model scale with larger datasets or more complex multimodal inputs?
2. The paper focuses on sentiment analysis. How well does the proposed method generalize to other multimodal tasks, such as emotion recognition or multimodal question answering?

### Rating

6

### Confidence

3

**********