### Summary

This paper introduces GoalRank, a generator-only ranking framework that challenges the traditional Generator-Evaluator paradigm in recommender systems. The authors provide theoretical proof that a sufficiently large generator-only model can achieve a strictly smaller approximation error compared to any finite Generator-Evaluator model. They also derive an upper bound for the one-stage optimization objective, enabling the use of a reward model trained on real user feedback to construct a practical surrogate for the optimal policy. Extensive offline experiments on public benchmarks and large-scale online A/B tests demonstrate that GoalRank consistently outperforms state-of-the-art methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. Theoretical Foundation: The paper provides a rigorous theoretical analysis, proving that a generator-only model can outperform the Generator-Evaluator paradigm in terms of approximation error and demonstrating a scaling law.

2. Practical Training Framework: The group-relative optimization principle offers a practical approach to training large generator-only models, making the theoretical advantages applicable in real-world scenarios.

3. Comprehensive Validation: The effectiveness of GoalRank is validated through extensive offline experiments on public benchmarks and large-scale online A/B tests, showing substantial improvements over strong baselines.

4. Clear Writing: The paper is well-organized and clearly written, making complex theoretical concepts accessible to readers.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not discuss the computational complexity of GoalRank compared to the Generator-Evaluator paradigm. The authors should provide a detailed analysis of the time and space complexity of GoalRank, especially as the model scales up. This analysis should include a breakdown of the computational costs associated with both training and inference, and should consider the impact of different model sizes and hardware configurations. Furthermore, the authors should discuss the practical implications of these complexities, such as the feasibility of deploying GoalRank in resource-constrained environments.

2. The paper does not discuss the potential limitations of GoalRank in adapting to diverse and changing business objectives. The authors should discuss how GoalRank can be adapted to different ranking objectives and how quickly it can converge to a new optimal policy when business goals change. This discussion should include an analysis of the sensitivity of the model to changes in the reward function and the potential need for retraining or fine-tuning when objectives shift. The authors should also consider the impact of these adaptations on the model's overall performance and stability.

### Suggestions

The authors should provide a more detailed analysis of the computational complexity of GoalRank, including a breakdown of the time and space requirements for both training and inference. This analysis should consider the impact of different model sizes, hardware configurations, and optimization techniques. Specifically, the authors should compare the computational cost of GoalRank with that of traditional Generator-Evaluator models, providing a clear understanding of the trade-offs involved. Furthermore, the authors should discuss the practical implications of these complexities, such as the feasibility of deploying GoalRank in resource-constrained environments. This discussion should include an analysis of the potential bottlenecks and strategies for optimizing the computational efficiency of the proposed framework. For example, the authors could explore techniques such as model compression, quantization, or distributed training to mitigate the computational burden.

To address the limitations in adapting to diverse and changing business objectives, the authors should investigate methods for incorporating contextual information into the GoalRank framework. This could involve developing mechanisms for dynamically adjusting the reward function based on the specific business objectives or user context. The authors should also explore techniques for fine-tuning the model on new objectives without requiring complete retraining. This could involve techniques such as transfer learning or meta-learning, which allow the model to quickly adapt to new tasks. Furthermore, the authors should provide a detailed analysis of the sensitivity of the model to changes in the reward function, including an evaluation of the convergence rate and the impact on overall performance. This analysis should consider the potential for instability or performance degradation when adapting to rapidly changing objectives.

Finally, the authors should consider the practical implications of deploying GoalRank in real-world scenarios, including the need for robust monitoring and evaluation systems. This should include a discussion of the potential for bias in the reward model and strategies for mitigating this bias. The authors should also consider the ethical implications of using a large ranking model, including the potential for unintended consequences or negative impacts on user experience. This discussion should include an analysis of the potential for manipulation or misuse of the model and strategies for ensuring responsible deployment.

### Questions

Please see Weaknesses

### Rating

6

### Confidence

3

**********