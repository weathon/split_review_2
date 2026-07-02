### Summary

This paper proposes a method called LoLoRA, which aims to reduce the memory usage of LoRA by eliminating the need to store activations for the backward pass. The key idea is to update the matrix A in LoRA using gradient-free updates during the forward pass, based on the layer's input. This allows the model to adapt to input distribution shifts without storing activations for backpropagation. The authors provide theoretical analysis showing that the optimal initialization for matrix A should approximate the maximum eigenspace transformation. They also propose a hybrid method that combines local unsupervised updates of matrix A with gradient-based updates of matrix B. Experimental results on various tasks demonstrate that LoLoRA achieves comparable performance to standard LoRA while reducing memory usage.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach to fine-tuning large language models (LLMs) that reduces memory usage without significant performance degradation. The use of gradient-free updates for the A matrix in LoRA is a creative solution to the memory bottleneck.
2. The authors provide a strong theoretical foundation for their method, including proofs for the optimal initialization of the A matrix. This adds credibility to the proposed approach.
3. The experimental results are comprehensive, covering various tasks and models. The paper demonstrates that LoLoRA achieves comparable performance to LoRA while reducing memory usage, which is a significant practical contribution.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's main contribution is the introduction of gradient-free updates for the A matrix, which is a relatively minor modification to the existing LoRA-FA method. While the theoretical analysis is valuable, the practical impact of the proposed method might be limited.
2. The paper does not provide a detailed analysis of the computational overhead introduced by the gradient-free updates. It would be helpful to understand how the computational cost of these updates compares to the memory savings achieved.
3. The paper could benefit from a more thorough comparison with other memory-efficient fine-tuning methods beyond LoRA and LoRA-FA. This would help to better contextualize the contribution of LoLoRA within the broader landscape of parameter-efficient fine-tuning techniques.

### Suggestions

The authors should provide a more detailed analysis of the computational overhead introduced by the gradient-free updates to the A matrix. Specifically, they should quantify the time spent on the local updates of A relative to the overall training time, and compare this to the time spent on updating B. It would be beneficial to see a breakdown of the computational cost for different components of the method, such as the local updates of A, the gradient descent on B, and any other overhead. This analysis should be performed across different model sizes and hardware configurations to understand the scalability of the approach. Furthermore, the authors should investigate the impact of different choices for the local update rule on both the computational cost and the performance of the method. For example, they could explore different approximations for the eigenvectors of the input covariance matrix, or alternative methods for updating A based on the layer's input. This would provide a more comprehensive understanding of the trade-offs involved in using gradient-free updates for A.

To better contextualize the contribution of LoLoRA, the authors should include a more comprehensive comparison with other memory-efficient fine-tuning methods. This comparison should go beyond just LoRA and LoRA-FA and include methods such as adapter layers, prefix tuning, and other low-rank adaptation techniques. The comparison should not only focus on memory usage but also on other relevant metrics such as training time, inference time, and performance on various downstream tasks. It would be helpful to see a table summarizing the performance of different methods across these metrics. The authors should also discuss the limitations of their method compared to other approaches, and identify the specific scenarios where LoLoRA is most effective. This would help to better understand the trade-offs involved in using LoLoRA compared to other memory-efficient fine-tuning methods.

Finally, the authors should provide more details on the implementation of their method, including the specific choices for the local update rule, the optimization algorithm used for updating B, and any other relevant implementation details. This would help to ensure the reproducibility of their results and allow other researchers to build upon their work. The authors should also discuss the sensitivity of their method to different hyperparameters, such as the learning rate, the batch size, and the rank of the low-rank matrices. It would be helpful to see a sensitivity analysis of these hyperparameters and provide guidance on how to choose appropriate values for different tasks and models. This would make the method more practical and easier to use for other researchers.

### Questions

1. How does the computational cost of the gradient-free updates compare to the memory savings achieved? Is there a trade-off between computational efficiency and memory efficiency?
2. How sensitive is the performance of LoLoRA to the choice of the local update rule for the A matrix? Are there specific scenarios where the proposed update rule might not be optimal?

### Rating

6

### Confidence

3

**********