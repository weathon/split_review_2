### Summary

This paper studies the dynamic regret of online inventory optimization (OIO) problem. The authors propose an algorithm with a dynamic regret bound that matches the known lower bound up to logarithmic factors. The key idea is to connect OIO with smoothed online convex optimization (SOCO) through a two-stage projection. The algorithm uses a base learner for SOCO and a doubling trick to handle the unknown maximum sell-out period $L_{max}$.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper proposes the first algorithm with a dynamic regret bound for the OIO problem, which matches the lower bound up to logarithmic factors. The result improves upon existing static regret bounds.
2. The algorithm uses a simple two-stage projection strategy, which is easy to implement.
3. The paper provides a lower bound for OIO, which helps to understand the fundamental limit of the problem.

### Weaknesses

#### Some Related Works


#### comment

1. The algorithm assumes that the subgradient is observable, which may not hold in practice. Specifically, the requirement to observe the full subgradient, rather than just its action, limits the applicability of the proposed method in scenarios where only partial or noisy gradient information is available. This assumption is particularly restrictive in complex systems where the underlying cost functions are not easily differentiable or where the subgradient is computed through approximations.
2. The paper does not provide empirical evaluation of the algorithm. The lack of empirical validation makes it difficult to assess the practical performance of the proposed algorithm. It is unclear how the algorithm would perform in real-world scenarios with noisy data, non-convex cost functions, or other practical challenges. The absence of numerical results also makes it hard to compare the proposed algorithm with existing heuristics or other online learning methods.
3. The paper only considers a single-item inventory system with a capacity limit. The analysis and algorithm are limited to a single-item setting, which may not be representative of more complex multi-item inventory systems. The extension to multi-item systems, even with a simplified linear cost structure, is not trivial and requires further investigation. The current scope limits the practical relevance of the results to a narrow class of inventory problems.

### Suggestions

The paper makes a significant theoretical contribution by providing a dynamic regret bound for the online inventory optimization problem. However, the practical applicability of the proposed algorithm is limited by the assumption of observable subgradients. To address this, future work could explore methods for handling noisy or partial gradient information. For instance, techniques from stochastic optimization or online learning with bandit feedback could be adapted to the OIO setting. Specifically, the algorithm could be modified to use an estimate of the subgradient based on limited observations, and the regret analysis could be adjusted to account for the estimation error. This would make the algorithm more robust to real-world scenarios where the true subgradient is not directly available. Furthermore, exploring the use of variance reduction techniques could also be beneficial in reducing the impact of noisy gradient estimates.

Another important direction for future research is to conduct a thorough empirical evaluation of the proposed algorithm. This would involve implementing the algorithm in a simulated environment and testing its performance under various conditions, such as different demand patterns, cost functions, and noise levels. The simulation should also compare the proposed algorithm with existing heuristics and other online learning methods to assess its relative performance. The empirical evaluation should also investigate the sensitivity of the algorithm to its parameters, such as the learning rate and the doubling trick parameter. This would provide valuable insights into the practical tuning of the algorithm and its robustness to different settings. Furthermore, it would be beneficial to explore the performance of the algorithm in real-world case studies, where the data is more complex and noisy.

Finally, the paper should be extended to consider more complex inventory systems, such as multi-item systems with correlated demands or lead times. The current analysis and algorithm are limited to a single-item setting, which may not be representative of many real-world inventory problems. Extending the algorithm to multi-item systems would require addressing challenges such as the curse of dimensionality and the need for more sophisticated coordination mechanisms. One possible approach is to explore the use of decomposition methods, where the multi-item problem is broken down into a set of single-item subproblems. Another approach is to use techniques from multi-armed bandits or reinforcement learning to learn the optimal inventory policy in a multi-item setting. This would significantly broaden the scope and practical relevance of the proposed algorithm.

### Questions

1. Can the algorithm be extended to handle multi-item inventory systems with correlated demands or lead times?
2. How does the algorithm perform in practice compared to existing heuristics or other online learning methods?
3. Can the algorithm be extended to handle non-convex cost functions or non-stationary environments?

### Rating

6

### Confidence

3

**********