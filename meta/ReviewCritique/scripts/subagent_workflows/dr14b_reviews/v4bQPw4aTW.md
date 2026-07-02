### Summary

The paper proposes a prompt-adaptive approach to Best-of-N alignment, which allocates inference-time compute more efficiently by estimating reward distributions for each prompt and adaptively allocating resources. The method is evaluated on multiple LM-RM pairs and datasets, demonstrating improved performance over uniform allocation strategies while maintaining low latency. The authors also introduce new evaluation metrics to assess the effectiveness of their adaptive approach.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow, with clear explanations of the proposed method and experimental setup.
2. The authors provide a comprehensive evaluation of their method across multiple LM-RM pairs and datasets, demonstrating its effectiveness and robustness.
3. The proposed method is simple and practical, requiring minimal hyperparameter tuning and no auxiliary training.
4. The authors introduce new evaluation metrics that provide a more nuanced assessment of the method's performance.
5. The paper includes a thorough discussion of the limitations of the proposed method and potential directions for future research.

### Weaknesses

#### Some Related Works


#### comment

1. The method assumes that the reward distributions are smooth and easy to learn, which may not hold for all LM-RM pairs or reward models. Specifically, the assumption of smoothness is not rigorously justified, and the paper lacks a discussion on how the method would perform with highly multimodal or discontinuous reward landscapes. The reliance on kernel density estimation (KDE) further exacerbates this issue, as KDE can struggle with complex distributions, potentially leading to inaccurate reward estimates and suboptimal allocation of the sampling budget.
2. The two-stage approach may not be optimal for all scenarios, and more sophisticated adaptive allocation strategies could potentially yield better results. The current approach uses a fixed exploration budget and then a greedy allocation based on the estimated reward distribution. This lacks the flexibility of more dynamic methods that could adjust the exploration and exploitation phases based on the observed reward variance or other criteria. For example, a Bayesian optimization approach could potentially adapt the exploration budget based on the uncertainty in the reward estimates, leading to more efficient resource allocation.
3. The paper does not provide a detailed analysis of the computational overhead of the proposed method compared to simpler alternatives. While the authors mention that the method is efficient, a quantitative comparison of the runtime and memory usage with uniform BoN sampling is missing. This makes it difficult to assess the practical trade-offs between the improved performance and the increased computational cost. A breakdown of the time spent on each stage of the algorithm (exploration, estimation, allocation) would be beneficial.
4. The paper does not explore the sensitivity of the method to the choice of hyperparameters, such as the exploration budget and the bandwidth parameter for the KDE. The performance of KDE is highly dependent on the bandwidth parameter, and the paper does not provide any guidance on how to choose this parameter. Similarly, the exploration budget is fixed, and the paper does not analyze how the performance varies with different exploration budgets. This lack of sensitivity analysis makes it difficult to assess the robustness of the method.

### Suggestions

The paper would benefit from a more thorough investigation into the assumptions underlying the proposed method. Specifically, the assumption of smooth reward distributions should be rigorously justified, and the paper should explore how the method performs with more complex reward landscapes. The authors could consider using alternative reward estimation techniques that are less sensitive to the smoothness assumption, such as Gaussian process regression or other non-parametric methods. Additionally, the paper should include a discussion on the limitations of the method when applied to highly multimodal or discontinuous reward functions. It would also be beneficial to provide a theoretical analysis of the convergence properties of the proposed method, particularly in relation to the choice of exploration budget and the bandwidth parameter for the KDE. This would provide a more solid foundation for the method and help to identify the conditions under which it is expected to perform well.

To improve the adaptive allocation strategy, the authors could explore more sophisticated methods that dynamically adjust the exploration and exploitation phases based on the observed reward variance or other criteria. For example, a Bayesian optimization approach could be used to adapt the exploration budget based on the uncertainty in the reward estimates. This would allow the method to focus more resources on prompts where the reward distribution is poorly understood, potentially leading to better overall performance. The authors could also consider using a multi-armed bandit approach to dynamically allocate the sampling budget, which would allow the method to adapt to the varying difficulty of different prompts. This would require a more complex implementation, but it could potentially lead to significant improvements in performance. The paper should also include a comparison of the proposed method with other adaptive sampling techniques, such as importance sampling or adaptive rejection sampling, to better understand its strengths and weaknesses.

Finally, the paper should include a more detailed analysis of the computational overhead of the proposed method. This should include a quantitative comparison of the runtime and memory usage with uniform BoN sampling, as well as a breakdown of the time spent on each stage of the algorithm. The authors should also explore the sensitivity of the method to the choice of hyperparameters, such as the exploration budget and the bandwidth parameter for the KDE. This could involve conducting a grid search over a range of hyperparameter values and reporting the performance of the method for each combination. This would provide a more complete picture of the method's performance and help to identify the optimal hyperparameter settings for different scenarios. The paper should also include a discussion on the practical implications of the computational overhead, particularly in resource-constrained environments.

### Questions

1. How does the method perform when the reward distributions are highly non-stationary or multimodal?
2. Can the authors provide a more detailed analysis of the computational overhead of the proposed method compared to simpler alternatives?
3. How sensitive is the method to the choice of hyperparameters, such as the exploration budget and the bandwidth parameter for the KDE?
4. How does the method perform when prompts arrive sequentially rather than in batches?
5. How does the method perform when the reward distributions are highly non-stationary?

### Rating

6

### Confidence

4

**********