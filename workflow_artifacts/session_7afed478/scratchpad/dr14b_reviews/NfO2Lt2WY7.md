### Summary

This paper investigates the necessity of complicated loss functions for enhancing reasoning capabilities in large language models (LLMs). The authors focus on Group Relative Policy Optimization (GRPO), a post-training technique that has shown promise in improving reasoning and mathematical abilities. Through a systematic analysis of GRPO, they identify two key findings: (1) incorporating negative feedback is essential—training solely on actions above a baseline limits learning; and (2) PPO-style constraints, such as policy ratio clipping, are not required to improve mathematical reasoning or performance. Building on these insights, they propose REINFORCE with Group Relative Advantage (RGR), a simplified variant that retains group-relative advantage estimation but removes PPO-style clipping and policy ratio terms. Experiments across standard mathematical benchmarks indicate that RGR has the potential to achieve stronger performance than GRPO. The results suggest that simpler REINFORCE-based approaches can effectively enhance reasoning in LLMs, offering a more transparent and efficient alternative to GRPO.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a systematic analysis of the GRPO loss function, breaking down its components and evaluating their individual contributions. This approach offers valuable insights into the design of reinforcement learning algorithms for reasoning tasks.
2. The proposed RGR method is a practical simplification of GRPO, demonstrating that complex components like PPO-style clipping may not be essential for achieving strong reasoning performance. This simplification could lead to more efficient and transparent training processes.
3. The experiments are conducted across a range of mathematical benchmarks, including multilingual datasets, which strengthens the generalizability of the findings. The results suggest that RGR is a competitive alternative to GRPO, with potential advantages in terms of simplicity and performance.

### Weaknesses

#### Some Related Works


#### comment

1. While the paper focuses on mathematical reasoning, it would be beneficial to explore the effectiveness of RGR in other reasoning domains, such as commonsense reasoning or logical inference. This would provide a more comprehensive understanding of the method's applicability and limitations.
2. The paper could benefit from a more detailed analysis of the training dynamics, such as convergence rates and sensitivity to hyperparameters. Understanding these aspects would help in optimizing the training process and ensuring the robustness of the method.
3. The paper could provide more insights into the computational efficiency of RGR compared to GRPO. This would be valuable for practitioners considering the trade-offs between performance and computational resources.

### Suggestions

To strengthen the paper, the authors should consider expanding their evaluation to include a more diverse set of reasoning tasks beyond mathematical problems. Specifically, incorporating benchmarks from commonsense reasoning, such as those found in the SocialIQA or HellaSwag datasets, would provide a more comprehensive assessment of RGR's capabilities. Additionally, including logical inference tasks, such as those from the LogicQA dataset, would further demonstrate the method's generalizability. This would involve adapting the current training framework to handle different input formats and evaluation metrics, but it would significantly enhance the paper's impact and relevance. Furthermore, the authors should investigate the performance of RGR on tasks that require multi-step reasoning, as this would provide a more realistic evaluation of its reasoning capabilities. This could involve using datasets that require a series of logical deductions or inferences to arrive at a solution, which would be a more challenging test of the method's reasoning abilities.

In addition to expanding the evaluation, the authors should conduct a more detailed analysis of the training dynamics of RGR. This should include a systematic study of how different hyperparameters, such as the learning rate, batch size, and the number of training steps, affect the performance of the method. The authors should also investigate the convergence behavior of RGR, including the number of training steps required to reach a stable solution and the sensitivity of the method to different initialization conditions. This analysis should include visualizations of the training curves and a discussion of the factors that influence the convergence rate. Furthermore, the authors should explore the use of techniques such as early stopping or learning rate scheduling to improve the training process and ensure the robustness of the method. This would provide valuable insights into the practical aspects of using RGR and help practitioners optimize its performance.

Finally, the authors should provide a more detailed analysis of the computational efficiency of RGR compared to GRPO. This should include a quantitative comparison of the training time, memory usage, and the number of parameters required by each method. The authors should also discuss the trade-offs between performance and computational resources, and provide guidance on how to choose the most appropriate method for a given task and resource constraint. This analysis should include a discussion of the hardware requirements for training RGR and GRPO, and the potential for parallelization. Furthermore, the authors should investigate the scalability of RGR to larger models and datasets, and discuss the potential for further optimization of the method. This would provide valuable insights for practitioners and help them make informed decisions about the practical applicability of RGR.

### Questions

See Weaknesses.

### Rating

6

### Confidence

4

**********