### Summary

This paper proposes two techniques, TALF and SALF, to improve tree-based speculative decoding. TALF is a training objective that aligns the draft model's predictions with the target model across all branches of the tree, while SALF is a dynamic tree construction algorithm that balances computational cost against draft quality for maximum performance. The authors demonstrate that these techniques deliver significant speedups over state-of-the-art methods without altering the draft model architecture.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper identifies an important problem in existing tree-based speculative decoding methods, namely the misalignment between training and inference due to the use of token sequences rather than trees as references. The proposed TALF objective addresses this issue by aligning the draft model's predictions with the target model across all branches of the tree, leading to improved performance.

2. The authors provide a thorough analysis of the training-inference mismatch problem and present empirical evidence to support their claims. The experiments on various benchmarks demonstrate the effectiveness of TALF and SALF, achieving consistent speedups over existing methods. The ablation studies further provide insights into the individual benefits of each technique.

### Weaknesses

#### Some Related Works


#### comment

1. The paper primarily focuses on the performance improvements achieved by TALF and SALF but does not extensively discuss any potential limitations or trade-offs. A more balanced discussion of the proposed methods, including potential drawbacks, would be beneficial. For instance, the computational overhead of TALF during training is not thoroughly explored, and it is unclear how this might impact its practical applicability. Furthermore, the paper lacks a detailed analysis of the memory footprint of the proposed methods, which is a crucial factor when dealing with large language models.

2. The paper could benefit from a more detailed comparison of TALF and SALF with other existing or potential approaches to address the identified training-inference mismatch problem. This would provide a clearer understanding of the advantages and disadvantages of the proposed methods compared to alternative solutions. For example, a comparison with methods that use different draft model architectures or those that employ alternative training strategies would be valuable. The current comparison is limited to EAGLE-2 and HASS, which may not fully capture the landscape of speculative decoding techniques.

3. The paper's writing style could be improved in certain sections. For instance, the introduction could be more concise and focused on the key contributions of the paper. Additionally, some sections, such as the description of the SALF algorithm, could be written in a more clear and accessible manner. The description of the SALF algorithm lacks sufficient detail, making it difficult to fully grasp the nuances of the dynamic tree construction process. A more step-by-step explanation with clear examples would be beneficial.

### Suggestions

To address the lack of discussion regarding the computational overhead of TALF, the authors should include a detailed analysis of the training time and resource consumption of their method compared to existing approaches. This analysis should include a breakdown of the time spent on different parts of the training process, such as the tree construction and the loss calculation. Furthermore, the authors should investigate the scalability of TALF with respect to the size of the target model and the draft model. This would provide a more complete picture of the practical implications of using TALF in real-world scenarios. Additionally, the authors should explore the memory footprint of TALF and SALF, providing a detailed analysis of the memory requirements during both training and inference. This analysis should consider the memory usage of the draft model, the target model, and any additional data structures used by the proposed methods. This is particularly important when dealing with large language models, where memory constraints can be a significant limiting factor.

To enhance the comparison with other approaches, the authors should include a more comprehensive evaluation of TALF and SALF against a wider range of speculative decoding techniques. This evaluation should include methods that use different draft model architectures, such as smaller, distilled models or models with different training objectives. Furthermore, the authors should compare their methods to techniques that employ alternative training strategies, such as reinforcement learning or adversarial training. This would provide a more complete understanding of the strengths and weaknesses of TALF and SALF compared to other state-of-the-art methods. The authors should also consider including a discussion of the potential limitations of their approach, such as the sensitivity to hyperparameter settings or the performance degradation under certain conditions. This would provide a more balanced and nuanced view of the proposed methods.

To improve the clarity of the paper, the authors should revise the introduction to be more concise and focused on the key contributions of the paper. The introduction should clearly state the problem being addressed, the proposed solution, and the main results. Additionally, the authors should provide a more detailed and accessible explanation of the SALF algorithm. This explanation should include a step-by-step description of the algorithm, along with clear examples that illustrate how the algorithm works in practice. The authors should also consider using visual aids, such as diagrams or flowcharts, to help readers understand the dynamic tree construction process. Furthermore, the authors should ensure that the writing style is consistent throughout the paper, with clear and concise language that is easy to understand.

### Questions

1. How sensitive are the performance improvements achieved by TALF and SALF to the choice of hyperparameters, such as the SALF threshold? Are there any guidelines for selecting appropriate hyperparameter values for different tasks or models?

2. Can the proposed techniques be applied to other speculative decoding methods or draft model architectures? How would the performance compare in such cases?

### Rating

6

### Confidence

4

**********