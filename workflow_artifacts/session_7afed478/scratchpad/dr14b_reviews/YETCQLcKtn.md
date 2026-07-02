### Summary

The paper introduces PolicyFlow, an on-policy reinforcement learning algorithm that integrates continuous normalizing flows with Proximal Policy Optimization (PPO) to handle complex action distributions without requiring costly likelihood evaluations. PolicyFlow approximates importance ratios using velocity field variations along simple interpolation paths, avoiding path-wise backpropagation. Additionally, the authors propose a Brownian Regularizer to prevent mode collapse and encourage exploration, inspired by Brownian motion. Experiments on MultiGoal, PointMaze, IsaacLab, and MuJoCo Playground demonstrate that PolicyFlow outperforms PPO with Gaussian policies and flow-based baselines FPO and DPPO, particularly in capturing rich multimodal action distributions.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed method is sound and achieves strong experimental results.
3. The authors conducted comprehensive experiments, and the ablation studies effectively demonstrate the contributions of the proposed components.

### Weaknesses

#### Some Related Works

[1] Policy Gradient Methods for Reinforcement Learning with Function Approximation

#### comment

1. The proposed algorithm is only compared with PPO using Gaussian policies and flow-based baselines FPO and DPPO. It would be beneficial to compare it with other advanced policy gradient methods that can handle multimodal action distributions, such as [1] and its subsequent work. Additionally, it would be valuable to include comparisons with other policy parameterizations, like Gaussian mixtures.

2. The paper lacks a theoretical analysis of how the approximation error in the importance ratio affects the algorithm's convergence properties. It is also unclear if the approximation error is bounded or how it scales with training, and how this impacts the algorithm's performance and stability over time.

### Suggestions

The paper would benefit from a more thorough comparison against a wider range of policy gradient methods, especially those designed to handle multimodal action distributions. While the current comparisons to PPO with Gaussian policies, FPO, and DPPO are useful, they do not fully establish the superiority of PolicyFlow against all relevant alternatives. Specifically, methods that explicitly model multimodal distributions, such as those using Gaussian mixtures or other parametric approaches, should be included in the experimental evaluation. This would provide a more complete picture of PolicyFlow's strengths and weaknesses relative to the state-of-the-art. Furthermore, the experimental section should include a more detailed analysis of the performance of PolicyFlow across different levels of multimodality in the action space. This could be achieved by varying the number of modes in the reward function or by using environments with inherently more complex action requirements. Such an analysis would help to better understand the conditions under which PolicyFlow excels and where it might fall short.

In addition to the empirical comparisons, a more rigorous theoretical analysis of the importance ratio approximation is needed. The paper should provide a formal analysis of the approximation error, including whether it is bounded and how it scales with training. This analysis should also explore the impact of this error on the convergence properties of the algorithm. For instance, it would be valuable to investigate if the approximation error introduces any bias in the policy update and how this bias affects the stability and performance of the algorithm over time. Furthermore, the paper should discuss the potential for error accumulation during training and how this might impact the final policy. A theoretical bound on the approximation error would be beneficial, along with a discussion of the practical implications of this bound. This would provide a more solid foundation for the proposed method and increase its credibility.

Finally, the paper should provide more details on the practical aspects of implementing PolicyFlow. This includes a discussion of the hyperparameter sensitivity of the algorithm, especially those related to the Brownian regularizer and the interpolation path. It would also be helpful to provide guidelines on how to choose the appropriate network architecture for the velocity field and how to ensure the stability of the ODE solver. Furthermore, the paper should discuss the computational cost of PolicyFlow compared to other methods, including the time required for training and sampling. This would help practitioners to better understand the trade-offs involved in using PolicyFlow and to make informed decisions about its applicability to their specific problems.

### Questions

1. In the experiments, do the baselines use the Brownian regularizer? If not, it would be helpful to include baselines with the Brownian regularizer enabled to provide a fairer comparison.

2. How does the proposed Brownian regularizer compare to other regularization techniques, such as uniform noise injection? It would be valuable to see an experimental comparison to understand the relative strengths and weaknesses of each approach.

3. What is the computational complexity of PolicyFlow compared to other methods? Specifically, how does the training time and memory usage of PolicyFlow compare to PPO with Gaussian policies and the flow-based baselines?

### Rating

6

### Confidence

3

**********