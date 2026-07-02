### Summary

The authors propose a new method for training LLMs on reasoning tasks using RL. Their method, GHPO, builds on the GRPO algorithm by introducing a mechanism to detect when a problem is too difficult for the model, and then providing a hint by incorporating a ground truth solution trace into the prompt. This allows the model to learn from problems that would otherwise yield no reward signal. GHPO dynamically adjusts the level of guidance based on the model's performance, ensuring that the model is always challenged but not overwhelmed. The authors demonstrate that GHPO outperforms GRPO and other baselines on several challenging math benchmarks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

* The paper is well-written and clearly explains the proposed method and its motivation.
* The authors provide a thorough analysis of the training dynamics, comparing GHPO to GRPO across several metrics.
* The experimental results are compelling, showing consistent improvements over baselines across different model families and benchmarks.
* The method is relatively simple to implement and does not require significant computational overhead compared to GRPO.

### Weaknesses

#### Some Related Works


#### comment

 * The method relies on the availability of ground truth solution traces, which may not be available for all tasks. This limits the applicability of the method to domains where such traces can be easily obtained or generated.
* The paper does not provide a detailed analysis of the sensitivity of the method to the hyperparameters, such as the hint ratio and the threshold for detecting difficult problems. It is unclear how these parameters should be tuned for different tasks and models, and whether the optimal values are consistent across different settings.
* The paper does not provide a detailed analysis of the computational cost of the method compared to GRPO. While the authors claim that the overhead is minimal, a more rigorous analysis of the training time and memory requirements would be beneficial, especially when scaling to larger models and datasets. The lack of a detailed breakdown of the computational cost makes it difficult to assess the practical feasibility of the method.

### Suggestions

The authors should investigate the impact of using noisy or incomplete ground truth traces, as this would more closely reflect real-world scenarios where perfect solutions are not always available. It would be beneficial to explore how the performance of GHPO degrades as the quality of the hints decreases, and to identify the types of errors that are most detrimental to the learning process. This analysis could include experiments with automatically generated hints, which would further broaden the applicability of the method. Furthermore, the authors should provide a more detailed analysis of the sensitivity of the method to the hint ratio and the threshold for detecting difficult problems. This analysis should include a systematic exploration of the parameter space, and should identify the optimal values for different tasks and models. The authors should also investigate whether the optimal values are consistent across different settings, and if not, what factors influence the choice of parameters. This analysis should include a discussion of the trade-offs between different parameter values, and should provide practical guidance for tuning the method for new tasks.

To address the lack of computational cost analysis, the authors should provide a detailed breakdown of the training time and memory requirements of GHPO compared to GRPO. This analysis should include a comparison of the number of forward and backward passes, the memory footprint of the model and the data, and the overall training time. The authors should also investigate the scalability of the method to larger models and datasets, and should identify any potential bottlenecks. This analysis should be conducted on a range of hardware configurations, and should provide practical guidance for deploying the method in different environments. The authors should also consider the impact of the hint generation process on the overall computational cost, and should explore ways to optimize this process.

Finally, the authors should explore alternative methods for providing guidance to the model, such as using a smaller, more capable model to generate hints. This approach could potentially reduce the reliance on ground truth traces, and could also provide a more flexible way to adapt the method to different tasks. The authors should also investigate the possibility of using a curriculum learning approach, where the model is initially trained on easier problems with more guidance, and then gradually transitioned to more difficult problems with less guidance. This approach could potentially improve the stability and efficiency of the training process, and could also lead to better generalization performance.

### Questions

* How sensitive is the method to the choice of the hint ratio and the threshold for detecting difficult problems? Is there a principled way to determine these parameters, or do they need to be tuned for each task?
* How does the method perform when the ground truth traces are noisy or incomplete? Have you considered using automatically generated hints instead of ground truth traces?
* Can you provide a more detailed analysis of the computational cost of the method compared to GRPO? How does the training time and memory usage scale with the size of the model and the dataset?

### Rating

6

### Confidence

3

**********