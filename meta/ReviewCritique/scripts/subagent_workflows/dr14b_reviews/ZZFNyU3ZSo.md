### Summary

This paper introduces UniMoD, a task-aware token pruning method for unified multimodal transformers. The authors first analyze the behavior of unified transformers by examining attention weight patterns, evaluating layer importance and token redundancy, and analyzing task interactions. They find that token redundancy varies significantly across different tasks and layers. Based on these findings, UniMoD employs separate routers for each task to determine which tokens should be pruned. The method is applied to Show-o and Emu3, reducing training FLOPs by approximately 15% in Show-o and 40% in Emu3, while maintaining or improving performance on several benchmarks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper provides a thorough empirical analysis of unified multimodal transformers, examining attention weights, layer importance, and task interactions. This analysis provides valuable insights into the behavior of these models and motivates the design of UniMoD.
2. The proposed UniMoD method is novel and effective in reducing computational cost while maintaining or improving performance. The task-aware token pruning approach addresses the unique challenges of unified transformers and demonstrates significant efficiency gains.
3. The paper is well-written and clearly explains the methodology and experimental results. The figures and tables are informative and help to illustrate the key findings.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed discussion of the limitations of the UniMoD method. For example, it does not address scenarios where the task-specific routers might fail to accurately identify redundant tokens, potentially leading to performance degradation. Additionally, the paper does not explore the sensitivity of the method to hyperparameter settings, such as the pruning ratio for each task. A more thorough analysis of these limitations would provide a more balanced view of the method's applicability and robustness.
2. The paper primarily focuses on two specific models, Show-o and Emu3, which may limit the generalizability of the findings. While these models are representative of unified multimodal transformers, the paper does not provide sufficient evidence to demonstrate that the proposed method would be equally effective on other architectures. The analysis should include a wider range of models with varying layer depths, attention mechanisms, and pre-training datasets to ensure the robustness of the proposed approach.
3. The paper does not provide a comprehensive comparison with other state-of-the-art token pruning methods. While the authors demonstrate improvements over baseline methods, a more detailed comparison with existing techniques, such as those based on magnitude pruning or gradient-based pruning, would help to contextualize the performance of UniMoD. This comparison should include not only performance metrics but also computational cost and memory usage.

### Suggestions

To strengthen the paper, the authors should conduct a more rigorous analysis of the limitations of UniMoD. This should include a detailed investigation into the scenarios where the task-specific routers might fail to accurately identify redundant tokens, potentially leading to performance degradation. For instance, the authors could explore the impact of aggressive pruning on tasks with inherently less redundancy, and how the method adapts to varying levels of task complexity. Furthermore, the analysis should include a discussion on the computational overhead introduced by the task-specific routers and how this overhead scales with the number of tasks. It would be beneficial to include experiments that systematically vary the pruning ratio for each task and analyze the resulting performance trade-offs. This would provide a more comprehensive understanding of the method's sensitivity to hyperparameter settings and its robustness under different conditions. The authors should also consider including a discussion on the potential for catastrophic forgetting when pruning tokens in a multi-task setting, and how UniMoD mitigates this issue.

To address the limited generalizability of the findings, the authors should expand their experiments to include a wider range of unified multimodal transformer models. This should include models with varying layer depths, attention mechanisms, and pre-training datasets. It is also important to consider models that use different tokenization strategies or have different ratios of generative to understanding components, as these factors could significantly impact the effectiveness of task-aware pruning. The authors should also investigate how the performance of UniMoD varies with different model sizes and training data volumes. This would provide a more comprehensive understanding of the method's applicability across different scenarios. Additionally, the authors should explore the potential for transferring the learned pruning strategies from one model to another, which could reduce the need for extensive retraining when applying UniMoD to new architectures.

Finally, the authors should provide a more comprehensive comparison with other state-of-the-art token pruning methods. This comparison should include not only performance metrics but also computational cost and memory usage. The authors should analyze the trade-offs between different pruning methods and discuss the specific scenarios where UniMoD offers the most significant advantages. For example, the authors could compare UniMoD with magnitude-based pruning, gradient-based pruning, and other dynamic pruning techniques. This would help to contextualize the performance of UniMoD and highlight its unique contributions. The authors should also consider including a discussion on the potential for combining UniMoD with other pruning techniques to achieve even greater efficiency gains. This would provide a more complete picture of the method's capabilities and limitations.

### Questions

1. How does UniMoD perform on models with significantly different architectures or pre-training datasets? Are there specific architectural features that make a model more or less amenable to task-aware pruning?
2. What is the computational overhead introduced by the task-specific routers in UniMoD? How does this overhead scale with the number of tasks and the size of the model?
3. How sensitive is UniMoD to the choice of hyperparameters, such as the pruning ratio for each task? Are there guidelines for selecting these parameters to optimize performance across different tasks and models?
4. Can the insights gained from the analysis of attention weights and ARank values be used to further refine the pruning strategy in UniMoD? For example, could these insights lead to more adaptive or dynamic pruning methods?
5. How does UniMoD compare to other state-of-the-art token pruning methods in terms of both performance and computational efficiency? Are there specific scenarios where UniMoD significantly outperforms existing techniques?

### Rating

6

### Confidence

4

**********