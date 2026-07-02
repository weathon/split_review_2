### Summary

This paper proposes a novel approach to learning state representations in Markov Decision Processes (MDPs) by estimating the Minimum Action Distance (MAD) between states. The authors introduce two algorithms, MADDist and TDMadDist, which learn state embeddings and quasimetric distance functions using only state trajectories, without requiring rewards or actions. The framework is evaluated on a diverse set of environments, including those with stochastic dynamics and noisy observations, demonstrating superior performance over existing methods in capturing environment structure and supporting downstream tasks like goal-conditioned reinforcement learning. The paper also introduces a novel quasimetric distance function that is computationally efficient and outperforms more elaborate quasimetrics in the existing literature.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach for learning state representations based on the Minimum Action Distance (MAD), a metric that captures the shortest path between states in terms of actions. This approach is innovative and addresses a fundamental challenge in reinforcement learning.
2. The authors propose two algorithms, MADDist and TDMADDist, that learn state embeddings and quasimetric distance functions using only state trajectories. This is a significant advancement, as it eliminates the need for rewards or actions, making the framework applicable in a wider range of scenarios.
3. The framework is evaluated on a diverse set of environments, including those with stochastic dynamics, noisy observations, and both discrete and continuous state spaces. This comprehensive evaluation demonstrates the robustness and generalizability of the proposed approach.
4. The empirical results show that the proposed methods outperform existing state representation techniques in terms of MAD approximation accuracy and performance on downstream tasks, such as goal-conditioned reinforcement learning.
5. The paper is well-written and clearly structured, making it accessible to readers with a background in reinforcement learning. The authors provide a thorough explanation of the theoretical foundations, algorithmic details, and experimental results.

### Weaknesses

#### Some Related Works


#### comment

1. The paper does not provide a detailed analysis of the computational complexity of the proposed algorithms, particularly in large-scale environments. This makes it difficult to assess the practical scalability of the approach. Specifically, the paper lacks a discussion on how the computational cost scales with the size of the state space, the length of trajectories, and the dimensionality of the learned embeddings. A more rigorous analysis, including Big-O notation, would be beneficial.
2. The framework's performance in environments with highly stochastic transitions or sparse rewards is not thoroughly explored. While the paper mentions stochastic environments, it does not provide specific experiments or analysis on how the method performs under varying degrees of stochasticity. Furthermore, the absence of experiments in sparse reward settings is a significant gap, as many real-world problems fall into this category.
3. The paper lacks a comprehensive discussion on the sensitivity of the proposed methods to hyperparameters, such as the choice of quasimetric or the size of the latent dimension. This makes it challenging to reproduce the results or apply the framework in new environments. For example, the paper does not provide guidance on how to select the appropriate quasimetric for a given environment, nor does it analyze the impact of different latent space dimensions on the quality of the learned representations.
4. The paper does not include a thorough comparison with other state-of-the-art representation learning methods, particularly those that do not rely on MAD. This makes it difficult to assess the relative strengths and weaknesses of the proposed approach. A more comprehensive comparison, including methods based on contrastive learning or autoencoders, would provide a better understanding of the proposed method's place in the broader landscape of representation learning.

### Suggestions

To address the lack of computational complexity analysis, the authors should include a detailed discussion of how the runtime and memory usage of their algorithms scale with key parameters such as the size of the state space, the length of trajectories, and the dimensionality of the learned embeddings. This analysis should include Big-O notation and, if possible, empirical measurements on different environments. Furthermore, the authors should provide practical guidelines for selecting appropriate hyperparameter values, such as the size of the latent dimension, based on the characteristics of the environment. This could involve a sensitivity analysis that shows how the performance of the algorithm varies with different hyperparameter settings. Such an analysis would greatly enhance the practical applicability of the proposed methods.

To improve the evaluation of the framework in challenging environments, the authors should conduct experiments in environments with varying degrees of stochasticity and sparse rewards. This could involve using benchmark environments specifically designed for these scenarios. The authors should also analyze how the performance of their methods degrades as the stochasticity or sparsity increases. Furthermore, the paper should include a more detailed discussion of the limitations of the proposed approach in these settings and suggest potential avenues for future research. This would provide a more complete picture of the strengths and weaknesses of the proposed methods.

Finally, the authors should include a more comprehensive comparison with other state-of-the-art representation learning methods, particularly those that do not rely on MAD. This comparison should include both quantitative and qualitative analysis, highlighting the relative strengths and weaknesses of the proposed approach. The authors should also discuss the potential benefits and drawbacks of using MAD as a metric for representation learning, compared to other metrics such as those used in contrastive learning or autoencoders. This would provide a better understanding of the proposed method's place in the broader landscape of representation learning and help readers assess its suitability for different applications.

### Questions

1. How does the computational complexity of the proposed algorithms scale with the size of the state space and the length of trajectories? Are there any practical limitations in applying these methods to very large environments?
2. How sensitive are the proposed methods to the choice of quasimetric and the size of the latent dimension? Are there any guidelines for selecting these hyperparameters in new environments?
3. How does the performance of the proposed methods degrade in environments with highly stochastic transitions or sparse rewards? Are there any potential solutions to address these challenges?
4. How does the proposed approach compare to other state-of-the-art representation learning methods, particularly those that do not rely on MAD? Are there any scenarios where these alternative methods might be more suitable?

### Rating

6

### Confidence

4

**********