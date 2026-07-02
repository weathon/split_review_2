### Summary

This paper proposes a new relative error-based evaluation framework for heterogeneous treatment effect (HTE) estimators. The key idea is to relax the requirement for consistent outcome regression models, which is a limitation of existing methods. The authors derive key conditions for robust relative error estimation and introduce novel loss functions and a neural network architecture to estimate nuisance parameters. The proposed method is validated through extensive experiments, demonstrating its effectiveness in evaluating HTE estimators and improving HTE estimation.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel relative error-based evaluation framework for HTE estimators, addressing a key limitation of existing methods by relaxing the requirement for consistent outcome regression models.
2. The authors provide a rigorous theoretical analysis, deriving key conditions for robust relative error estimation and demonstrating the asymptotic properties of their proposed estimator.
3. The paper is well-organized and clearly written, with detailed explanations of the methodology, theoretical results, and experimental setup.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the practical implications of the proposed evaluation framework, particularly in real-world applications where treatment effect heterogeneity is critical. Specifically, the paper lacks a discussion on how the proposed framework would handle scenarios with high-dimensional covariates or complex treatment assignment mechanisms, which are common in real-world datasets. The current evaluation focuses on relatively simple synthetic datasets, and it is unclear how the method would perform when faced with the challenges of real-world data, such as non-linear relationships and interactions between covariates.
2. The paper's reliance on a correctly specified propensity score model, while less restrictive than requiring a fully consistent outcome model, still poses a potential limitation. The paper does not adequately address the sensitivity of the proposed method to misspecification of the propensity score model. While the authors mention that the impact of propensity score misspecification is less significant, they do not provide a rigorous analysis of how different types of misspecification (e.g., omitted variables, incorrect functional form) would affect the relative error estimation. Furthermore, the paper does not explore methods to mitigate the impact of propensity score misspecification, such as using robust propensity score estimation techniques.

### Suggestions

To enhance the practical relevance of the proposed evaluation framework, the authors should include a more detailed discussion of its application in real-world scenarios. This should include an analysis of how the method would handle high-dimensional covariates, complex treatment assignment mechanisms, and non-linear relationships between covariates and outcomes. The authors could consider including experiments on more complex synthetic datasets that mimic real-world data characteristics, or even explore the use of real-world datasets with known treatment effect heterogeneity. This would provide a more comprehensive understanding of the method's strengths and limitations in practical settings. Furthermore, the authors should discuss the computational cost of their method in high-dimensional settings and provide guidance on how to optimize the implementation for large datasets.

To address the reliance on a correctly specified propensity score model, the authors should conduct a more thorough sensitivity analysis of the proposed method to different types of propensity score misspecification. This should include an investigation of the impact of omitted variables, incorrect functional forms, and incorrect distributional assumptions. The authors could also explore methods to mitigate the impact of propensity score misspecification, such as using robust propensity score estimation techniques or incorporating sensitivity analysis into the evaluation framework. This would provide a more complete picture of the method's robustness and reliability in real-world settings where the propensity score model is likely to be misspecified to some degree. The authors should also discuss the trade-offs between the robustness of their method and the potential for bias introduced by propensity score misspecification.

Finally, the authors should provide more guidance on how to choose the hyperparameters of their method, particularly the regularization parameters. The paper currently lacks a detailed discussion of how these parameters affect the performance of the method, and it is unclear how practitioners should select appropriate values for their specific applications. The authors could consider including a sensitivity analysis of the hyperparameters and providing recommendations based on the characteristics of the data and the research question. This would make the method more accessible and practical for researchers and practitioners who are not experts in machine learning.

### Questions

1. How sensitive is the proposed relative error estimator to the correct specification of the propensity score model? Are there scenarios where even small deviations in propensity score estimation could significantly impact the robustness of the relative error?
2. How does the proposed method handle cases where the outcome models for the treated and control groups exhibit significant distributional differences? Are there specific conditions under which the method performs optimally or suboptimally?
3. Can the authors provide more details on the computational complexity of the proposed method, especially in comparison to existing approaches? How does the method scale with increasing sample size and number of candidate estimators?
4. Are there any practical guidelines or heuristics for selecting the hyperparameters of the proposed method, particularly the regularization parameters? How sensitive is the performance to the choice of these parameters?

### Rating

6

### Confidence

3

**********