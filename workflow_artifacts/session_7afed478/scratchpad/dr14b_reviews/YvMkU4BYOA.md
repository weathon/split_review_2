### Summary

This paper proposes a new score-based method for causal discovery in discrete data. The method, called XBIC, enhances the Bayesian Information Criterion (BIC) by incorporating edge-specific Shapley evidence. The authors evaluate XBIC on ten benchmark discrete Bayesian networks and seven sample-size regimes, showing that it outperforms existing methods in terms of oriented-edge F1 score and structural Hamming distance.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper proposes a novel score-based causal discovery method, called XBIC, that incorporates edge-specific Shapley evidence into the Bayesian Information Criterion (BIC). This is a creative combination of ideas from causal discovery and explainable AI.

2. The paper provides a thorough evaluation of XBIC on ten benchmark discrete Bayesian networks and seven sample-size regimes. The experimental results show that XBIC outperforms existing methods in terms of oriented-edge F1 score and structural Hamming distance.

3. The paper is well-written and easy to follow. The authors provide clear explanations of the proposed method and the experimental setup.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method has a high computational cost due to the need to train per-node classifiers and compute Shapley values. This may limit its applicability to large-scale problems. The computational bottleneck arises from the need to train a separate classifier for each node, which can be time-consuming, especially with high-dimensional data. Furthermore, computing Shapley values for each edge adds another layer of computational overhead, making the method potentially impractical for very large graphs.

2. The paper does not provide a theoretical analysis of the proposed method. It is unclear whether the method is consistent, and if so, under what conditions. The lack of theoretical guarantees makes it difficult to assess the reliability of the method. Specifically, it is unclear whether the proposed method will converge to the true causal graph as the sample size increases, and what assumptions are needed for this convergence to hold. Without such analysis, it is hard to determine the conditions under which the method can be expected to perform well.

### Suggestions

The authors should provide a more detailed analysis of the computational complexity of the proposed method. This should include a breakdown of the time complexity for each step, such as training the per-node classifiers and computing the Shapley values. It would be beneficial to provide a theoretical analysis of the computational cost, perhaps in terms of the number of variables, the size of the graph, and the sample size. Furthermore, the authors should explore potential strategies for reducing the computational cost, such as using more efficient algorithms for training the classifiers or approximating the Shapley values. For example, instead of training a separate classifier for each node, one could explore methods that share information across nodes, or use ensemble methods to reduce the variance of the estimates. Additionally, the authors could investigate techniques for approximating the Shapley values, such as using sampling methods or closed-form approximations, which could significantly reduce the computational burden. A thorough analysis of the computational cost is crucial for assessing the practical applicability of the proposed method.

To address the lack of theoretical analysis, the authors should investigate the conditions under which the proposed method is consistent. This would involve proving that the method converges to the true causal graph as the sample size increases. The authors should clearly state the assumptions under which this convergence holds, and discuss the limitations of the method when these assumptions are violated. For example, it would be important to analyze the impact of model misspecification on the consistency of the method. If the true data-generating process does not belong to the class of models considered by the method, it is unclear whether the method will still be able to recover the true causal graph. The authors should also investigate the robustness of the method to different types of noise and outliers. A theoretical analysis would provide a more solid foundation for the proposed method and increase its credibility. The authors should also consider providing a discussion on the identifiability of the causal structure under the assumptions of their method.

Finally, the authors should provide more details on the practical implementation of the method. This should include a discussion of the hyperparameter settings, and how these settings affect the performance of the method. The authors should also provide guidelines for choosing the appropriate base learner for the per-node classifiers. It would be helpful to include a sensitivity analysis of the method to different choices of hyperparameters and base learners. Furthermore, the authors should discuss the limitations of the method and suggest potential directions for future research. This would help the readers to better understand the strengths and weaknesses of the method, and to identify areas where further improvements are needed. For example, the authors could discuss the potential for extending the method to handle continuous variables or mixed data types.

### Questions

1. Can you provide a theoretical analysis of the proposed method? Specifically, what are the conditions under which the method is consistent?

2. How does the proposed method perform on large-scale problems with hundreds or thousands of variables? What are the computational costs of the method in these settings?

3. How does the choice of the base learner for the per-node classifiers affect the performance of the method? Are there any guidelines for choosing the appropriate base learner?

### Rating

6

### Confidence

4

**********