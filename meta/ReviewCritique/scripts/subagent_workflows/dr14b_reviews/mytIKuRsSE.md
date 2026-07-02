### Summary

This paper addresses the problem of Dual-level Noisy Correspondence (DNC) in Multi-Modal Entity Alignment (MMEA), where noise exists both in intra-entity (entity-attribute) and inter-graph (entity-entity and attribute-attribute) correspondences. The authors propose a novel framework, RULE (dually Robust Learning), to mitigate the negative impact of DNC. RULE estimates the reliability of correspondences using a two-fold principle of uncertainty and consensus, and incorporates a correspondence reasoning module to enhance test-time robustness. Extensive experiments on five benchmarks demonstrate the effectiveness of RULE against seven state-of-the-art methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel and practical problem in MMEA, termed Dual-level Noisy Correspondence (DNC), which is often overlooked in existing methods.
2. The proposed method, RULE, is technically sound and well-designed to address the DNC problem. The two-fold principle of uncertainty and consensus for reliability estimation is innovative and effective.
3. The correspondence reasoning module enhances test-time robustness, which is a significant contribution.
4. The experimental results are comprehensive and demonstrate the superiority of RULE over existing methods.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could provide more details on the implementation of the correspondence reasoning module, particularly how it leverages the Chain-of-Thought (CoT) approach to guide the MLLM. The current description lacks specifics on how the intermediate reasoning steps are generated and integrated into the final similarity score. It is unclear how the MLLM is prompted to perform reasoning and how the outputs of the MLLM are processed to obtain the reliability weights.
2. The paper could benefit from a more detailed analysis of the performance of the proposed method under different levels of noise. While the paper mentions the Dual-level Noisy Correspondence (DNC) problem, it does not provide a systematic evaluation of how the method's performance degrades as the noise level increases. It would be beneficial to see a more granular analysis of the impact of varying degrees of noise on the alignment accuracy.
3. The paper could discuss the limitations of the proposed method and potential directions for future research. For example, the paper does not address the computational complexity of the proposed method, especially when dealing with large-scale knowledge graphs. Furthermore, the paper does not discuss the sensitivity of the method to the choice of hyperparameters, which could be a significant factor in its practical application.

### Suggestions

To enhance the clarity and reproducibility of the correspondence reasoning module, the authors should provide a more detailed explanation of how the Chain-of-Thought (CoT) approach is implemented. Specifically, they should elaborate on the prompt engineering used to guide the MLLM, including the specific instructions and examples provided to the model. It would be beneficial to include a step-by-step example of how the MLLM generates intermediate reasoning steps and how these steps are used to calculate the reliability weights. Furthermore, the authors should clarify how the outputs of the MLLM are processed to obtain the final similarity scores. This could involve explaining the specific mathematical operations or algorithms used to integrate the MLLM's outputs into the overall framework. Providing pseudocode or a detailed algorithm description would significantly improve the understanding and reproducibility of this module.

To address the lack of detailed analysis on the impact of noise, the authors should conduct a more systematic evaluation of the proposed method under different levels of noise. This could involve creating datasets with varying degrees of noise, such as by randomly corrupting a certain percentage of entity-attribute and entity-entity correspondences. The authors should then evaluate the performance of the proposed method on these datasets and present the results in a clear and concise manner, such as through graphs or tables. This analysis should not only focus on the overall alignment accuracy but also on the performance of the correspondence reasoning module under different noise levels. It would be particularly insightful to examine how the reliability weights assigned by the module change as the noise level increases. This would provide a better understanding of the robustness of the proposed method to noisy data.

Finally, the authors should discuss the limitations of the proposed method in more detail. This should include an analysis of the computational complexity of the method, particularly when dealing with large-scale knowledge graphs. The authors should also discuss the sensitivity of the method to the choice of hyperparameters and provide guidelines for selecting appropriate values. Furthermore, the authors should explore potential directions for future research, such as extending the method to handle more complex types of noise or incorporating additional modalities. Addressing these limitations and suggesting future research directions would strengthen the paper and provide a more comprehensive understanding of the proposed method.

### Questions

1. How does the proposed method handle cases where the noise level is very high, and what are the limitations in such scenarios?
2. Can the proposed method be extended to handle other types of noise or other types of knowledge graphs?
3. How does the performance of the proposed method compare to other methods when dealing with very large-scale knowledge graphs?

### Rating

6

### Confidence

3

**********