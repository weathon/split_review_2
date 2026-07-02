### Summary

The paper introduces Direct Optimal Action Learning (DOAL), a framework for policy extraction in offline reinforcement learning that avoids the computational complexity of backpropagating through iterative sampling chains. DOAL achieves this by directly learning an optimized action based on Q-values and a behavior cloning loss. The paper also introduces a Batch-Normalizing Optimizer, which simplifies hyperparameter tuning by establishing a trust region for action shifts. DOAL is tested with various policies and Q-value functions, showing improvements over baseline models in the OGBench tasks.

### Soundness

3

### Presentation

2

### Contribution

3

### Strengths

1. DOAL provides a computationally efficient solution for policy extraction without backpropagating through iterative sampling chains.
2. The Batch-Normalizing Optimizer simplifies hyperparameter tuning, making the framework more accessible and practical.
3. DOAL demonstrates improvements over baseline models in the OGBench tasks.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed analysis of DOAL's performance on Adroit tasks, especially given the varying quality of datasets (expert, human, cloned). While the paper mentions that improvements can be achieved with regularized Q-learning, a more in-depth analysis of DOAL's performance across different dataset qualities is needed to fully understand its robustness and generalizability. Specifically, the paper should investigate how the performance of DOAL varies when trained on expert data versus cloned data, and whether the regularization of the Q-function is sufficient to mitigate the issues arising from noisy or suboptimal data. It is crucial to understand if the method is sensitive to the quality of the data, and if so, what are the limitations.
2. The paper could benefit from a more thorough discussion on the limitations of DOAL, particularly in scenarios where the Q-value function may not be reliable. The current discussion does not delve into the specific scenarios where the Q-function might fail, such as in environments with sparse rewards or highly stochastic transitions. Furthermore, the paper should explore the potential impact of approximation errors in the Q-function on the performance of DOAL, and how these errors might propagate through the policy extraction process. A more detailed analysis of these limitations would provide a more balanced view of the method's applicability.
3. While the paper mentions that DOAL can be integrated with any Q-value-based offline RL method, more empirical evidence demonstrating its compatibility and performance enhancements across a wider range of methods would strengthen this claim. The paper should include experiments with a diverse set of offline RL algorithms, not just IQL, to demonstrate the general applicability of DOAL. For example, it would be beneficial to see how DOAL performs when combined with constraint-based methods like CQL or with model-based approaches. This would provide a more comprehensive understanding of the method's strengths and weaknesses.
4. The paper could provide more insights into the choice of the trust region hyperparameter δ and its impact on the performance of DOAL. The paper should include a more detailed analysis of how the choice of δ affects the stability and performance of the algorithm. It is not clear how to choose the optimal value of δ, and the paper should provide guidelines for selecting this hyperparameter. Furthermore, the paper should investigate the sensitivity of the method to different values of δ, and whether there are any specific ranges that work well across different environments.

### Suggestions

To address the lack of detailed analysis on Adroit tasks, the authors should include a more comprehensive evaluation of DOAL's performance across the different dataset qualities (expert, human, and cloned). This should involve a breakdown of the results for each dataset type, along with a discussion of the observed trends. Specifically, the authors should investigate whether the performance of DOAL is significantly different when trained on expert data versus cloned data, and if so, what are the underlying reasons for these differences. This analysis should also include a comparison of DOAL with other offline RL methods, such as CQL, to understand how DOAL performs relative to these methods under different data conditions. Furthermore, the authors should explore the impact of regularized Q-learning on the performance of DOAL, and whether this regularization is sufficient to mitigate the issues arising from noisy or suboptimal data. This would provide a more complete understanding of the robustness and generalizability of DOAL.

To address the limitations of DOAL, the authors should include a more detailed discussion of the scenarios where the Q-value function might not be reliable, and how this might affect the performance of DOAL. This discussion should include specific examples of environments where the Q-function might fail, such as those with sparse rewards or highly stochastic transitions. The authors should also explore the potential impact of approximation errors in the Q-function on the performance of DOAL, and how these errors might propagate through the policy extraction process. Furthermore, the authors should investigate whether there are any techniques that can be used to mitigate the impact of these errors, such as using ensemble methods or incorporating uncertainty estimates into the Q-function. This would provide a more balanced view of the method's applicability and limitations.

To strengthen the claim that DOAL can be integrated with any Q-value-based offline RL method, the authors should include more empirical evidence demonstrating its compatibility and performance enhancements across a wider range of methods. This should involve experiments with a diverse set of offline RL algorithms, not just IQL, to demonstrate the general applicability of DOAL. For example, it would be beneficial to see how DOAL performs when combined with constraint-based methods like CQL or with model-based approaches. The authors should also investigate the impact of different hyperparameter settings on the performance of DOAL when combined with these different methods. This would provide a more comprehensive understanding of the method's strengths and weaknesses, and would help to establish its general applicability.

### Questions

Please refer to the weakness.

### Rating

6

### Confidence

3

**********