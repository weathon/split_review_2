### Summary

This paper presents a novel approach to co-designing morphology and control in soft robotics by leveraging Graph Neural Networks (GNNs) and Deep Reinforcement Learning (DRL). The authors propose a Graph Attention Network (GAT)-based policy framework that models robots as graphs, enabling adaptive control strategies that can respond to morphological changes. The method is evaluated on a benchmark platform, demonstrating superior performance in terms of final fitness and adaptability compared to traditional MLP-only approaches.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel and effective approach to co-designing morphology and control in soft robotics, addressing a significant challenge in the field.
2. The use of GATs for policy representation is well-justified and provides a robust solution to the problem of controller inheritance across morphological changes.
3. The empirical validation on a benchmark platform provides strong evidence of the method's effectiveness, showing higher final rewards and improved robustness to morphology changes compared to baselines.
4. The paper is well-structured and clearly written, making it accessible to a broad audience.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed approach, particularly in terms of scalability to more complex morphologies and environments.
2. While the empirical results are promising, the paper lacks a thorough analysis of the computational cost associated with the GAT-based approach compared to MLP-based methods. This is important for practical applications where computational resources may be limited.
3. The paper does not provide a detailed comparison with other state-of-the-art methods in the field, which would help to contextualize the contributions of this work.

### Suggestions

The paper should include a more in-depth analysis of the computational demands of the GAT-based approach, specifically detailing the time complexity of the message-passing operations and the overall training time. A comparison of the number of parameters and FLOPs (floating-point operations) between the GAT and MLP approaches would be beneficial. This analysis should also consider the impact of graph size (number of nodes and edges) on computational cost, as this directly relates to the complexity of the robot morphology. Furthermore, the authors should discuss the practical implications of these computational costs, such as the feasibility of deploying the proposed method on resource-constrained platforms or in real-time applications. This would provide a more complete picture of the method's applicability and limitations.

To better contextualize the contributions of this work, the authors should include a more detailed comparison with other state-of-the-art methods in the field of co-designing morphology and control. This comparison should not only focus on the final performance metrics but also consider the underlying assumptions, design choices, and limitations of each approach. For example, the authors could compare their method to other GNN-based approaches, as well as methods that use different types of neural networks or optimization techniques. This comparison should also discuss the specific tasks and environments used in each study, as this can significantly impact the performance of different methods. A table summarizing the key features and performance of each method would be a useful addition to the paper.

Finally, the paper should address the limitations of the proposed approach in terms of scalability to more complex morphologies and environments. The authors should discuss the challenges of applying their method to robots with a large number of degrees of freedom or to environments with complex dynamics. They should also consider the potential for using hierarchical GNNs or other techniques to address these scalability issues. Furthermore, the authors should discuss the limitations of the current benchmark platform and suggest potential future directions for evaluating the proposed method in more realistic scenarios. This would provide a more comprehensive understanding of the method's strengths and weaknesses and guide future research in this area.

### Questions

1. How does the computational cost of the GAT-based approach compare to the MLP-based methods, particularly in terms of training time and inference speed?
2. Can the proposed method be extended to handle more complex morphologies or environments, and what are the potential challenges in doing so?
3. How does the proposed method compare to other state-of-the-art approaches in the field of co-designing morphology and control, and what are the key differences and advantages?

### Rating

6

### Confidence

3

**********