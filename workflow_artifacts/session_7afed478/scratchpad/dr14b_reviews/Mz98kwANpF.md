### Summary

This paper introduces Align-LoRA, a method for parameter-efficient fine-tuning (PEFT) of large language models (LLMs) in multi-task learning (MTL) scenarios. The authors begin by challenging the widely-adopted assumption that architectural isolation of task-specific features is essential for effective multi-task adaptation, arguing that learning task-shared representations can be a more effective approach. They observe that a simplified multi-head LoRA variant (M-LoRA) with high inter-head similarity outperforms complex multi-component architectures. Building on this insight, they propose increasing the rank of a standard single-head LoRA as a means to achieve competitive performance.  Align-LoRA is introduced as a method to explicitly align task representations within the shared adapter space by incorporating an auxiliary loss function based on Kullback-Leibler (KL) Divergence. This approach encourages task-shared representations without adding parameters or inference overhead.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

- The paper is well-organized, with clear explanations of the different LoRA architectures and their respective trade-offs. 
- The authors provide a comprehensive empirical evaluation of their proposed method, demonstrating its effectiveness across a range of tasks and model sizes. The experimental results are presented clearly, making it easy to understand the performance gains achieved by Align-LoRA compared to baseline methods.
- The authors provide a comprehensive theoretical analysis of their method, deriving a generalization bound for multi-task learning scenarios. This theoretical analysis provides valuable insights into why Align-LoRA is effective and how it can help to improve generalization performance.

### Weaknesses

#### Some Related Works


#### comment

 - The paper could benefit from a more detailed discussion of the limitations of the proposed method and potential directions for future research. For example, it would be interesting to explore how Align-LoRA performs on more diverse and complex task benchmarks, as well as how it could be extended to other parameter-efficient fine-tuning techniques beyond LoRA.
- The paper could also benefit from a more thorough analysis of the computational cost of Align-LoRA compared to other multi-component architectures. While the authors mention that Align-LoRA does not introduce additional inference overhead, it would be helpful to provide a more detailed comparison of training time and memory requirements.

### Suggestions

The authors should delve deeper into the limitations of Align-LoRA, particularly regarding its performance on highly diverse task sets. While the current experiments demonstrate effectiveness on a range of tasks, it is crucial to understand the boundaries of the method. For instance, how does Align-LoRA perform when tasks have minimal semantic overlap or when the task complexity varies significantly? Exploring these scenarios would provide a more comprehensive understanding of the method's applicability. Furthermore, the authors should investigate the sensitivity of Align-LoRA to the choice of the auxiliary loss function. While KL divergence is a reasonable choice, it would be beneficial to explore other options, such as Maximum Mean Discrepancy (MMD) or contrastive losses, and analyze their impact on the alignment of task representations. This analysis could reveal whether the specific choice of the auxiliary loss is critical to the method's success or if other options could provide similar or even better performance.

In addition to the theoretical analysis, a more detailed empirical investigation of the computational cost of Align-LoRA is needed. While the authors mention the absence of additional inference overhead, a thorough comparison of training time and memory requirements against other multi-component architectures is essential. This comparison should include not only the total training time but also the time required for hyperparameter tuning and the memory footprint during training. It would also be beneficial to analyze the scalability of Align-LoRA with respect to the number of tasks and the size of the model. This analysis would provide valuable insights into the practical applicability of the method in resource-constrained environments. Furthermore, the authors should explore the potential for optimizing the training process of Align-LoRA, such as using techniques like gradient checkpointing or mixed-precision training, to reduce the computational burden.

Finally, the authors should consider exploring the integration of Align-LoRA with other parameter-efficient fine-tuning techniques beyond LoRA, such as adapter layers or prefix tuning. This exploration could lead to hybrid approaches that combine the strengths of different methods and potentially achieve even better performance. For example, it would be interesting to investigate whether applying Align-LoRA to the weights of adapter layers or prefix tuning can further improve multi-task learning performance. Additionally, the authors should analyze the impact of the rank parameter on the performance of Align-LoRA. While the paper mentions increasing the rank of a standard single-head LoRA, a more detailed analysis of how the rank affects the alignment of task representations and the overall performance is needed. This analysis could provide guidance on how to choose the optimal rank for different tasks and model sizes.

### Questions

- How does the performance of Align-LoRA vary with the number of tasks? Is there a threshold beyond which the benefits of Align-LoRA start to diminish?
- The paper focuses on the application of Align-LoRA to LoRA. How well does the approach generalize to other parameter-efficient fine-tuning techniques beyond LoRA?

### Rating

6

### Confidence

4

**********