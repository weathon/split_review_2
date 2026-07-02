### Summary

This paper proposes a novel transformer architecture, ELMUR, designed to address long-horizon, partially observable decision-making tasks in reinforcement learning. ELMUR introduces structured external memory at each layer, bidirectional token-memory cross-attention, and an LRU-based update mechanism, significantly extending memory retention beyond the typical attention window. The architecture is evaluated across diverse environments, including synthetic T-Maze tasks, robotic manipulation challenges (MIKASA-Robo), and the POPGym benchmark, demonstrating robust performance improvements over existing methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

* The paper is well-written and easy to follow.
* The proposed architecture is novel, with a clear and well-justified design.
* The evaluation is comprehensive, covering a diverse set of tasks and demonstrating strong performance.

### Weaknesses

#### Some Related Works


#### comment

 * The evaluation is conducted on a limited set of environments, which may not fully capture the generalizability of the approach. While the paper includes diverse tasks, expanding the evaluation to a broader range of environments, particularly those with more complex state spaces or higher-dimensional action spaces, would strengthen the claims of robustness. For example, testing on environments with continuous control, stochastic dynamics, or partial observability beyond the current set would be beneficial.
* The paper lacks an in-depth analysis of failure cases. Understanding the limitations of the approach is crucial for practical applications. The paper should include a more detailed analysis of scenarios where ELMUR fails or underperforms, including a discussion of the underlying reasons for these failures. This could involve examining specific task characteristics or memory configurations that lead to poor performance.
* The architecture introduces additional complexity, which may pose challenges for real-world deployment. The paper should provide a more detailed analysis of the computational overhead introduced by the external memory and LRU mechanism, including memory usage, training time, and inference latency. A comparison with simpler architectures would help to quantify the trade-off between performance gains and computational costs.

### Suggestions

To address the limitations in the evaluation, the authors should consider expanding their experiments to include a wider variety of environments that present different challenges. Specifically, incorporating tasks with continuous action spaces, such as those found in robotics or control systems, would provide a more comprehensive assessment of the method's capabilities. Furthermore, environments with stochastic transitions and partial observability, beyond the current set, would be valuable in testing the robustness of the memory mechanism. For example, the authors could explore environments with noisy sensors or unpredictable dynamics. This would help to demonstrate the generalizability of ELMUR across a broader range of real-world scenarios. Additionally, the authors should consider evaluating the method's performance under different memory configurations, such as varying the size of the external memory or the frequency of LRU updates, to understand how these parameters affect performance and computational cost.

To improve the analysis of failure cases, the authors should conduct a more detailed investigation into the specific scenarios where ELMUR underperforms. This could involve analyzing the memory content at different time steps to understand how the memory is being used and whether it is capturing the relevant information. The authors should also examine the attention patterns to see if the model is focusing on the correct parts of the memory. Furthermore, it would be beneficial to analyze the gradients during training to identify potential issues with the learning process. A detailed analysis of the failure cases should include a discussion of the underlying reasons for these failures, such as limitations in the memory capacity, the update mechanism, or the attention mechanism. This analysis should also consider the impact of different task characteristics on the performance of ELMUR. For example, the authors could investigate whether the method struggles with tasks that require long-term planning or those that involve complex state transitions.

Finally, to address the concerns about computational overhead, the authors should provide a more detailed analysis of the computational cost of ELMUR compared to simpler architectures. This analysis should include a breakdown of the memory usage, training time, and inference latency for different task configurations. The authors should also investigate techniques to optimize the implementation of ELMUR, such as using more efficient data structures or parallelizing the computations. A comparison with simpler architectures, such as standard transformers or recurrent neural networks, would help to quantify the trade-off between performance gains and computational costs. The authors should also consider the impact of different memory configurations on the computational cost, such as varying the size of the external memory or the frequency of LRU updates. This analysis should provide practical guidance for deploying ELMUR in resource-constrained environments.

### Questions

* Could the authors provide more details on the computational overhead introduced by the external memory and LRU mechanism? How does this compare to simpler architectures?
* How does the performance of ELMUR scale with the complexity of the environment? Are there specific types of tasks where the method struggles?
* What are the primary failure modes of ELMUR? Understanding these limitations would provide valuable insights for future improvements.

### Rating

6

### Confidence

3

**********