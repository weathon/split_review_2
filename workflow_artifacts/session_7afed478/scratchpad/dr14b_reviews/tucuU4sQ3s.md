### Summary

This paper introduces a novel memory-free continual learning method called Null Space Adaptation for Continual Learning (NuSA-CL), designed for vision-language models like CLIP. The method addresses the challenge of catastrophic forgetting by identifying and leveraging the null space of the model’s parameters to apply task-specific updates. This approach allows new knowledge to be integrated without interfering with previously learned tasks, thus preserving the model’s zero-shot capabilities. NuSA-CL operates without external memory or replay buffers, making it highly efficient in terms of memory and computationally lightweight. The authors provide theoretical bounds to support their approach, showing that updates within the null space minimize interference in parameter space. Experimental results demonstrate that NuSA-CL achieves competitive performance on continual learning benchmarks, outperforming other storage-free methods and rivaling even storage-based approaches in some metrics.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. NuSA-CL leverages the null space of the model’s parameters to apply task-specific updates, which is a novel approach in continual learning. This strategy allows the model to adapt to new tasks while preserving previously learned knowledge without the need for external memory or replay buffers.
2. The method is backed by theoretical analysis, including bounds on parameter interference, which adds robustness to the proposed approach.
3. NuSA-CL is highly efficient in terms of memory usage, as it does not require storing past data or expanding model parameters. This makes it suitable for deployment in resource-constrained environments.
4. The paper is well-written and clearly explains the methodology, theoretical foundations, and experimental results.

### Weaknesses

#### Some Related Works


#### comment

1. The persistent null-space constraint, while effective in preventing forgetting, may limit the model’s ability to fully adapt to tasks that require significant deviations from previously learned knowledge. This constraint could hinder the model’s performance in scenarios where new tasks demand substantial changes to the model’s parameter space, potentially leading to suboptimal results compared to more flexible adaptation methods.
2. The effectiveness of NuSA-CL depends on the accurate identification of the null space, which might be challenging in highly dynamic or complex task sequences. The method relies on a singular value decomposition (SVD) to approximate the null space, and the accuracy of this approximation can be affected by the condition number of the weight matrix. In scenarios with rapidly changing task distributions, the identified null space might not accurately represent the true subspace where updates can be made without interfering with prior knowledge, potentially leading to performance degradation.
3. While the paper provides a theoretical bound on interference, it remains unclear how well these bounds translate to practical scenarios, especially with highly correlated task sequences. The theoretical bounds are derived under certain assumptions, and it is not clear how these assumptions hold in real-world scenarios, particularly when tasks are highly correlated. The paper lacks a detailed analysis of the correlation between tasks and its impact on the performance of NuSA-CL, making it difficult to assess the practical applicability of the theoretical bounds.

### Suggestions

To address the potential limitations of the persistent null-space constraint, future work could explore adaptive constraint mechanisms that allow for controlled deviations from the null space when necessary. This could involve dynamically adjusting the constraint based on the characteristics of the new task or the degree of similarity to previously learned tasks. For example, a metric could be introduced to quantify the required deviation from the null space, and the constraint could be relaxed accordingly. This would allow the model to adapt more effectively to tasks that require significant changes while still maintaining stability for tasks that are closely related to previous ones. Furthermore, exploring different methods for identifying the null space, such as using more robust SVD techniques or alternative matrix decomposition methods, could improve the accuracy of null space identification, especially in highly dynamic or complex task sequences. This could involve investigating the use of randomized SVD or other approximation techniques that are less sensitive to the condition number of the weight matrix. Additionally, a more detailed analysis of the impact of task correlation on the performance of NuSA-CL is needed. This could involve conducting experiments with different levels of task correlation and analyzing how the performance of the method varies. This analysis could help to identify the limitations of the method and guide the development of more robust approaches.

To further investigate the practical implications of the theoretical bounds, it would be beneficial to conduct experiments that specifically target scenarios where the bounds are expected to be tight or loose. This could involve designing task sequences with varying degrees of correlation and analyzing the performance of NuSA-CL in these scenarios. Additionally, it would be useful to compare the performance of NuSA-CL with other continual learning methods that do not rely on null space constraints, such as methods based on regularization or replay buffers. This would provide a more comprehensive understanding of the strengths and weaknesses of the proposed approach. Furthermore, the paper could benefit from a more detailed discussion of the computational cost of the SVD operation, especially for large models. While the authors mention that the SVD is performed on smaller matrices, a more detailed analysis of the time and memory requirements would be helpful. This analysis should also consider the impact of the rank parameter on the computational cost and the performance of the method. It would be useful to provide guidelines for selecting the rank parameter based on the specific application and the available computational resources.

Finally, the paper could be strengthened by including a more detailed analysis of the limitations of NuSA-CL. This could involve discussing the scenarios where the method is expected to perform poorly and identifying potential avenues for future research. For example, the paper could discuss the limitations of the method in scenarios where the task sequence is very long or where the tasks are highly diverse. This would provide a more balanced view of the proposed approach and help to guide future research in this area. Additionally, it would be beneficial to explore the sensitivity of the method to different hyperparameter settings, such as the learning rate and the batch size. This would help to ensure that the method is robust and reliable in different settings.

### Questions

1. How does NuSA-CL perform in highly dynamic environments where the task distribution changes rapidly or where tasks are highly correlated? Is there a risk of the null space becoming saturated or ineffective in such scenarios?
2. What are the limitations of the persistent null-space constraint in scenarios where new tasks require significant deviations from previously learned knowledge? How does this constraint affect the model’s plasticity in such cases?
3. How sensitive is NuSA-CL to the choice of the rank parameter for the low-rank updates? Is there a principled way to select this parameter, or does it require extensive tuning for different task sequences?
4. The paper mentions that the SVD is performed on smaller matrices within the model. However, for very large models, even this operation could become computationally intensive. How does the method scale with increasing model size, and what are the potential bottlenecks?

### Rating

6

### Confidence

3

**********