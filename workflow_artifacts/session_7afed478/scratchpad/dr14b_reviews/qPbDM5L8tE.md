### Summary

This paper introduces CoRAL, a modular framework for robotic manipulation that integrates vision and language models with motion planning and reactive control. The framework is designed to handle complex, contact-rich tasks without relying on extensive teleoperated datasets. The system uses a vision module for environmental parameter initialization and object pose tracking, while an LLM generates initial contact strategies and cost function estimations. A memory unit is also included to leverage past experiences for generalizing and reusing manipulation strategies. The paper presents experiments on challenging tasks to demonstrate the framework's robustness and effectiveness.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-organized and clearly written.
- The framework shows strong performance on contact-rich tasks, outperforming state-of-the-art baselines.
- The ablation studies effectively demonstrate the importance of each component in the proposed architecture.

### Weaknesses

#### Some Related Works


#### comment

 - The paper does not address how the system handles situations where the VLM provides incorrect physical parameters or the LLM generates infeasible strategies. More discussion on error handling and recovery mechanisms would be beneficial.
- The paper lacks a detailed analysis of the computational efficiency of the proposed framework. A breakdown of the runtime for each component and the overall system would be helpful. Additionally, the paper does not discuss the scalability of the approach to more complex tasks or environments. It is unclear how the system would perform with a larger number of objects or more intricate manipulation sequences.
- The paper does not discuss the sensitivity of the system to the choice of hyperparameters, such as the feedback gain matrix K_f in the reactive control loop. A more detailed analysis of how these parameters affect the system's performance and robustness would be valuable.

### Suggestions

The paper should include a more thorough discussion of the system's robustness to errors in the Vision-Language Model (VLM) and Large Language Model (LLM) outputs. Specifically, it would be beneficial to explore scenarios where the VLM provides inaccurate physical parameters, such as incorrect mass or friction coefficients, and how these errors propagate through the system. Similarly, the paper should analyze cases where the LLM generates infeasible or suboptimal contact strategies, and how the system detects and recovers from such situations. This could involve implementing mechanisms for detecting inconsistencies between the predicted and actual behavior of objects during manipulation, and triggering replanning or adaptation strategies when such inconsistencies are detected. For example, if the robot is pushing an object and it moves less than predicted, the system should be able to recognize this discrepancy and adjust its model or strategy accordingly. The paper should also discuss the limitations of the current error handling mechanisms and suggest potential improvements for future work.

To address the lack of computational analysis, the paper should provide a detailed breakdown of the runtime for each component of the framework, including the VLM, LLM, motion planner, and reactive controller. This analysis should include the average time taken for each component to execute, as well as the variance in execution time across different trials. The paper should also discuss the overall system latency and how it affects the real-time performance of the system. Furthermore, the paper should explore the scalability of the approach by evaluating its performance on more complex tasks with a larger number of objects and more intricate manipulation sequences. This could involve testing the system on tasks that require multi-step planning and coordination, and analyzing how the performance degrades as the complexity of the task increases. The paper should also discuss the computational resources required to run the system, such as the memory and processing power, and how these requirements scale with the complexity of the task.

Finally, the paper should include a sensitivity analysis of the system's performance to the choice of hyperparameters, particularly the feedback gain matrix K_f in the reactive control loop. This analysis should explore how different values of K_f affect the system's stability, responsiveness, and robustness to disturbances. The paper should also discuss how the optimal value of K_f may vary depending on the specific task and environment, and provide guidelines for selecting appropriate values. Additionally, the paper should investigate the sensitivity of the system to other hyperparameters, such as the parameters of the MPPI controller, and discuss how these parameters affect the overall performance and robustness of the system. This analysis should provide a more complete understanding of the system's behavior and help guide the selection of appropriate parameters for different applications.

### Questions

- How does the system handle situations where the VLM provides incorrect physical parameters or the LLM generates infeasible strategies? Are there any error handling or recovery mechanisms in place?
- What is the computational efficiency of the proposed framework? How does the runtime break down across different components? How does the approach scale to more complex tasks or environments?
- How sensitive is the system to the choice of hyperparameters, such as the feedback gain matrix K_f in the reactive control loop?

### Rating

6

### Confidence

4

**********