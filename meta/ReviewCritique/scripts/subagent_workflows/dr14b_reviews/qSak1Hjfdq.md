### Summary

This paper proposes a novel approach to address the challenge of deploying vision-and-language navigation (VLN) agents across diverse scenes and environments. The authors formalize this challenge as the all-day multi-scenes lifelong VLN (AML-VLN) problem, highlighting the issue of catastrophic forgetting when fine-tuning on specific scenarios. To overcome this, they introduce Tucker Adaptation (TuKA), which represents multi-hierarchical navigation knowledge as a high-order tensor using Tucker decomposition. This allows for the decoupling of shared subspaces and scenario-specific experts. Additionally, they present a decoupled knowledge incremental learning strategy to consolidate shared subspaces while constraining specific experts to mitigate catastrophic forgetting. The paper also introduces AllDayWalker, a VLN agent that continually learns across multiple navigation scenarios, achieving all-day multi-scenes navigation. Extensive experiments demonstrate that AllDayWalker outperforms state-of-the-art baselines, showcasing the effectiveness of the proposed approach. The paper contributes a new problem formulation, a novel parameter-efficient adaptation method, a lifelong VLN agent, and an extended benchmark for evaluation.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to tackling the challenge of deploying VLN agents in diverse scenes and environments by formalizing the problem as AML-VLN. This problem formulation is well-motivated and addresses a critical issue in the field.
2. The proposed Tucker Adaptation (TuKA) method is a significant technical innovation. Using Tucker decomposition to represent multi-hierarchical knowledge in a high-order tensor is a creative solution that allows for the decoupling of shared and specific knowledge, which is a significant advancement over existing methods.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed comparison with existing methods, particularly in terms of computational efficiency and scalability. While the authors mention parameter efficiency, a more rigorous analysis of the computational overhead introduced by TuKA would be valuable. Specifically, the paper lacks a detailed breakdown of the FLOPs required for both training and inference, making it difficult to assess the practical applicability of the method, especially in resource-constrained environments. Furthermore, a comparison of training time per epoch and inference latency against baseline methods would provide a more comprehensive understanding of the computational trade-offs.
2. The generalization experiments are limited to only six unseen tasks. Expanding the evaluation to a larger and more diverse set of unseen tasks would provide a more robust assessment of the method's generalization capabilities. The current evaluation does not fully explore the boundaries of the method's applicability, and it is unclear how performance would degrade under more challenging or novel scenarios. The selection criteria for these six tasks are also not clearly defined, making it difficult to assess the representativeness of the evaluation set.
3. The paper could provide more insights into the limitations of the proposed approach and potential avenues for future research. For instance, the paper does not discuss the potential failure modes of the method or the scenarios where it might struggle. A more thorough discussion of these limitations would provide a more balanced view of the method's capabilities and guide future research directions.

### Suggestions

To address the lack of detailed computational analysis, the authors should include a comprehensive breakdown of the computational costs associated with TuKA. This should include a comparison of FLOPs for both training and inference, as well as a detailed analysis of memory usage. Furthermore, the authors should provide a comparison of training time per epoch and inference latency against baseline methods, such as standard fine-tuning and other parameter-efficient adaptation techniques. This analysis should be conducted on a consistent hardware setup to ensure a fair comparison. It would also be beneficial to explore the scalability of the method by evaluating its performance with varying numbers of navigation scenarios and environments. This would provide a better understanding of how the computational cost scales with the complexity of the problem.

To strengthen the generalization analysis, the authors should significantly expand the evaluation to include a larger and more diverse set of unseen tasks. This could involve incorporating tasks from different datasets or creating novel scenarios that are significantly different from the training environments. The selection criteria for these tasks should be clearly defined and justified. Furthermore, the authors should analyze the performance of the method across different types of scenarios to identify any potential biases or limitations. It would also be valuable to investigate the sensitivity of the method to variations in the environment, such as changes in lighting conditions, object arrangements, or the presence of obstacles. This would provide a more comprehensive understanding of the method's robustness and generalization capabilities.

Finally, the authors should provide a more thorough discussion of the limitations of the proposed approach. This should include an analysis of the potential failure modes of the method and the scenarios where it might struggle. For example, the authors could investigate the impact of extreme environmental conditions, such as very low light or heavy occlusions, on the performance of the method. Furthermore, the authors should discuss the potential for catastrophic forgetting in scenarios that are significantly different from the training environments. This discussion should also include potential avenues for future research, such as exploring alternative tensor decomposition techniques, incorporating meta-learning strategies, or developing more robust methods for handling catastrophic forgetting. This would provide a more balanced view of the method's capabilities and guide future research directions.

### Questions

1. How does the computational cost of TuKA compare to existing methods, especially in terms of training time and inference latency? Could the authors provide a detailed analysis of the computational overhead introduced by the proposed method?
2. What are the potential limitations or failure cases of the proposed approach? Are there specific scenarios or conditions where TuKA might struggle to perform effectively?
3. How does the performance of AllDayWalker scale with the number of navigation scenarios and environments? Is there a point at which the performance starts to degrade significantly as more scenarios are added?

### Rating

6

### Confidence

4

**********