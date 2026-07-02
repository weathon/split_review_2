### Summary

The paper introduces a reinforcement learning framework, WeCAN, for scheduling directed acyclic graphs (DAGs) in heterogeneous environments. It leverages a weighted cross-attention layer to capture environment information and a longest directed distance graph neural network to adapt to varying task dependencies. The paper also proposes a skip-action mechanism to close the optimality gap inherent in list-scheduling-based methods. The approach is evaluated on TPC-H and Computation Graphs datasets, demonstrating improved performance and computational efficiency compared to state-of-the-art methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel end-to-end reinforcement learning framework for heterogeneous DAG scheduling, addressing the challenges of adaptability and rapid schedule generation in diverse environments.
2. The introduction of the weighted cross-attention layer and the skip-action mechanism are innovative contributions that enhance the framework's ability to utilize environment information and improve scheduling performance.
3. The paper provides a thorough analysis of the optimality gap in list-scheduling-based methods and demonstrates the effectiveness of the proposed skip-action mechanism in closing this gap.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion on the limitations of the proposed approach, particularly in scenarios with highly dynamic environments or real-time constraints. Specifically, the paper does not address how the model would adapt to changes in task dependencies or resource availability during execution, which is a critical aspect of real-world scheduling problems. The current evaluation focuses on static environments, and it's unclear how the model's performance would degrade under dynamic conditions.
2. The complexity analysis of the WeCAN framework is somewhat lacking. A more rigorous analysis of the time and space complexity would be beneficial. The paper should provide a detailed breakdown of the computational cost associated with each component of the framework, including the weighted cross-attention layer and the skip-action mechanism. This analysis should consider the impact of the number of tasks, resources, and dependencies on the overall complexity.
3. The paper does not provide a detailed comparison with other learning-based scheduling methods, particularly those that also use reinforcement learning or graph neural networks. The paper should include a more comprehensive comparison with state-of-the-art learning-based scheduling algorithms, highlighting the specific advantages and disadvantages of the proposed approach. This comparison should include a discussion of the trade-offs between solution quality, computational efficiency, and adaptability.

### Suggestions

The paper should include a more thorough discussion of the limitations of the WeCAN framework, particularly in scenarios with highly dynamic environments or real-time constraints. The current evaluation focuses on static environments, and it's unclear how the model's performance would degrade under dynamic conditions. The authors should consider adding experiments that simulate changes in task dependencies or resource availability during execution. This could involve introducing random task failures, resource additions or removals, or changes in task priorities. The paper should also discuss the potential overhead associated with retraining or adapting the model in such scenarios. Furthermore, the authors should explore the use of techniques such as online learning or transfer learning to improve the adaptability of the framework to dynamic environments. A detailed analysis of the model's sensitivity to changes in the environment would also be beneficial, including how the model's performance varies with different levels of dynamism.

Regarding the complexity analysis, the paper should provide a more detailed breakdown of the time and space complexity of the WeCAN framework. The analysis should consider the impact of the number of tasks, resources, and dependencies on the overall complexity. Specifically, the paper should analyze the computational cost associated with each component of the framework, including the weighted cross-attention layer and the skip-action mechanism. The analysis should also consider the memory requirements of the model, including the storage of the DAG and the learned parameters. A comparison of the time complexity of WeCAN with other state-of-the-art scheduling algorithms would also be beneficial. This analysis should be presented in a clear and concise manner, using standard complexity notation. The authors should also discuss the practical implications of the complexity analysis, including the scalability of the framework to large-scale problems.

The paper should include a more detailed comparison with other learning-based scheduling methods, particularly those that also use reinforcement learning or graph neural networks. The comparison should include a discussion of the trade-offs between solution quality, computational efficiency, and adaptability. The authors should consider comparing their approach with other state-of-the-art learning-based scheduling algorithms, such as those based on policy gradient methods or Q-learning. The comparison should also include a discussion of the specific advantages and disadvantages of the proposed approach, highlighting the scenarios where WeCAN is expected to perform well and where it may struggle. The authors should also discuss the limitations of existing methods and how WeCAN addresses these limitations. This comparison should be presented in a clear and concise manner, using tables or figures to summarize the results.

### Questions

1. How does the WeCAN framework handle scenarios where task dependencies or resource availabilities change dynamically?
2. Can the authors provide a more detailed analysis of the time and space complexity of the WeCAN framework?
3. How does WeCAN compare to other learning-based scheduling methods in terms of solution quality and computational efficiency?

### Rating

6

### Confidence

3

**********