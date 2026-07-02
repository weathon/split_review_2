### Summary

This paper proposes a new method to learn task-conditioned policies from offline reward-free data. The core of the method is a latent-predictive representation, which is obtained by minimizing a TD-style objective. Policies are then learned by planning in the learned latent space. The method is evaluated on various offline reward-free benchmarks.

### Soundness

3

### Presentation

2

### Contribution

2

### Strengths

1. The proposed method is well-motivated and the presentation is clear.
2. The method is supported by some theoretical analysis.
3. The empirical performance of the proposed method is good.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is rather complex, involving learning of four components. In contrast, some existing methods (e.g., Laplacian, HILP, and PSM) only need to learn a task encoder. This complexity may hinder the scalability of the method. Specifically, the method requires training separate state and task encoders, two sets of predictors, and a policy, each with their own hyperparameters and optimization challenges. The interplay between these components is not fully clear, and the potential for instability or cascading errors during training is a concern. Furthermore, the computational cost of training these multiple components simultaneously could be a significant barrier to wider adoption.
2. The method requires parameterizing policies in the latent space, which introduces an extra dimension of hyperparameters (e.g., the latent dimension). This dependency on a latent space introduces a bottleneck, potentially limiting the expressiveness of the policy. The choice of latent dimension is critical and requires careful tuning, adding to the overall complexity of the method. Furthermore, the mapping from the observation space to the latent space may not be optimal for all tasks, and the policy's performance is highly dependent on the quality of this learned representation.
3. The method only works for task-conditioned policies, which limits its scope. The reliance on a task encoder restricts the method's applicability to scenarios where a clear task definition is available. This limits the method's ability to handle more general RL problems where the goal is to learn a single policy that can perform well across a range of tasks without explicit task conditioning. The method's performance in more open-ended or dynamic environments remains unclear.

### Suggestions

The paper should provide a more detailed analysis of the interplay between the different components of the method, particularly the state and task encoders, and the two sets of predictors. It would be beneficial to include ablation studies that systematically evaluate the impact of each component on the overall performance. For example, the authors could investigate the effect of removing one of the predictors or using a shared encoder for both state and task representations. This would help to understand the necessity of each component and identify potential areas for simplification. Furthermore, the authors should provide more guidance on how to choose the hyperparameters for each component, as the current approach relies on a grid search which is computationally expensive and may not be feasible for all practitioners. A more principled approach to hyperparameter selection would greatly enhance the practical value of the method.

To address the limitations of the latent space policy parameterization, the authors should explore alternative approaches that do not rely on a latent space bottleneck. For example, they could investigate the use of implicit policies or other techniques that allow for a more direct mapping from observations to actions. This would help to mitigate the risk of information loss during the encoding process and potentially improve the method's performance on more complex tasks. Additionally, the authors should provide a more thorough analysis of the impact of the latent dimension on the method's performance, including a sensitivity analysis that explores a wider range of latent dimensions. This would help to identify the optimal latent dimension for different tasks and provide a better understanding of the trade-offs involved in choosing this hyperparameter.

Finally, the authors should discuss the limitations of the method in more detail, particularly its restriction to task-conditioned policies. They should explore potential avenues for extending the method to more general RL settings, such as by incorporating techniques for learning unified policies or by developing methods for adapting the task-conditioned policy to new tasks. This would help to broaden the applicability of the method and make it more relevant to a wider range of RL problems. Furthermore, the authors should provide a more detailed comparison to existing methods that can handle unified policies, such as PSM, and discuss the trade-offs between the proposed method and these alternatives. This would help to clarify the method's strengths and weaknesses and provide a more complete picture of its contribution to the field.

### Questions

1. The method is evaluated on various benchmarks, but the applicability of the proposed method is unclear. Can this method be applied to more general RL settings? For example, can it be used to train a unified policy?
2. The method is evaluated on the antmaze-me task, which is known to be difficult for unsupervised RL methods. Can the authors provide some insights on the limitations of the proposed method on this task?

### Rating

6

### Confidence

3

**********