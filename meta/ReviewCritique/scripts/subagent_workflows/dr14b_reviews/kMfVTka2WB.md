### Summary

This paper proposes a covariance-adjusted support vector classification algorithm in non-Euclidean spaces. The authors argue that traditional SVM classification, which relies on the max-margin principle and Karush Kuhn Tucker (KKT) boundary conditions, is only valid in Euclidean spaces. They propose a methodology that incorporates data covariance into the optimization problem using the transformation matrix obtained from Cholesky Decomposition of class covariance matrices. The resulting classifier separates the margin space in a ratio proportional to class population covariance. The authors also propose an iterative algorithm to estimate the population covariance-adjusted SVM classifier from sample covariance matrices. The effectiveness of this approach is demonstrated through experiments on multiple datasets, showing improved accuracy, precision, F1 scores, and ROC performance compared to traditional SVM kernels and whitening algorithms.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

The paper presents a novel approach to support vector classification in non-Euclidean spaces by incorporating data covariance into the optimization problem. The proposed algorithm iteratively estimates the population covariance-adjusted SVM classifier from sample covariance matrices. The experimental results demonstrate improved performance compared to traditional SVM kernels and whitening algorithms on multiple datasets.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a clear and concise contribution summary. While the introduction provides context and motivation, it does not explicitly outline the specific contributions of the proposed method. A dedicated section or paragraph summarizing the key contributions would enhance the paper's clarity and impact.
2. The experimental section lacks crucial details regarding the datasets used. The authors should provide information about the number of samples, dimensionality, and class distributions for each dataset. Additionally, the specific evaluation metrics used should be explicitly stated and justified. The absence of these details makes it difficult to assess the validity and generalizability of the experimental results.
3. The paper does not include a thorough discussion of the limitations of the proposed method. It is important to acknowledge potential drawbacks, such as sensitivity to parameter settings, computational complexity, or performance degradation under specific data conditions. Addressing these limitations would provide a more balanced and realistic assessment of the method's applicability.
4. The experimental results are presented without any measure of variability or uncertainty. The authors should report the standard deviation of the performance metrics across multiple runs or cross-validation folds. This is essential to assess the statistical significance of the observed improvements and to determine whether the proposed method consistently outperforms the baselines.
5. The paper lacks a dedicated discussion section that interprets the experimental results in the context of the proposed method's theoretical properties. The authors should discuss the reasons behind the observed performance improvements and relate them to the specific characteristics of the datasets. This would provide a deeper understanding of the method's strengths and weaknesses and guide future research directions.
6. The paper does not include a comparison with other state-of-the-art methods for support vector classification in non-Euclidean spaces. The authors should consider comparing their method with relevant techniques, such as kernel methods or manifold learning approaches, to demonstrate its superiority or unique advantages. This would provide a more comprehensive evaluation of the proposed method's performance and its position within the existing literature.

### Suggestions

The paper needs a more rigorous experimental evaluation to support its claims. Specifically, the authors should provide detailed information about the datasets used, including the number of samples, dimensionality, class distributions, and any preprocessing steps applied. This information is crucial for assessing the validity and generalizability of the results. Furthermore, the authors should explicitly state the evaluation metrics used and justify their choice. For example, if accuracy is used, they should discuss its suitability for potentially imbalanced datasets and consider reporting other metrics like precision, recall, and F1-score. The experimental results should also include measures of variability, such as standard deviations or confidence intervals, to assess the statistical significance of the observed improvements. This could be achieved by performing multiple runs with different random initializations or using cross-validation techniques. Without these details, it is difficult to ascertain the robustness and reliability of the proposed method.

To enhance the paper's impact, the authors should include a more in-depth discussion of the proposed method's theoretical properties and how they relate to the experimental results. For instance, they should discuss why incorporating covariance information leads to improved performance and under what conditions this approach is most effective. This discussion should be grounded in the mathematical formulation of the method and should provide insights into its behavior on different types of datasets. Furthermore, the authors should compare their method with other state-of-the-art techniques for support vector classification in non-Euclidean spaces. This could include kernel methods, manifold learning approaches, or other techniques that explicitly handle non-Euclidean data. A thorough comparison would help to position the proposed method within the existing literature and highlight its unique advantages and limitations. The authors should also discuss the computational complexity of their method and compare it to other approaches. This is important for assessing the practical applicability of the method, especially for large-scale datasets.

Finally, the paper should include a dedicated section discussing the limitations of the proposed method. This should include a discussion of potential drawbacks, such as sensitivity to parameter settings, computational complexity, or performance degradation under specific data conditions. For example, the authors should discuss how the choice of covariance estimation method affects the performance of the classifier and whether the method is robust to noisy or outliers. Addressing these limitations would provide a more balanced and realistic assessment of the method's applicability and guide future research directions. The authors should also consider providing a more detailed analysis of the convergence properties of the iterative algorithm used to estimate the covariance-adjusted SVM classifier. This would help to establish the stability and reliability of the method.

### Questions

1. Could you provide a more detailed explanation of the theoretical underpinnings of your proposed method? Specifically, how does incorporating covariance information into the optimization problem affect the decision boundary and margin in non-Euclidean spaces?
2. How does your method handle high-dimensional data? Does the performance degrade as the dimensionality increases, and if so, what are the potential solutions to mitigate this issue?
3. Could you elaborate on the choice of Cholesky Decomposition for obtaining the transformation matrix? Are there alternative decomposition methods that could be used, and what are the advantages or disadvantages of each?
4. How sensitive is your method to the choice of parameters, such as the regularization parameter and kernel parameters? Have you performed any sensitivity analysis to assess the robustness of your method to parameter variations?
5. Could you provide a more detailed comparison of your method with other state-of-the-art approaches for support vector classification in non-Euclidean spaces? What are the key differences, and in what scenarios does your method outperform or underperform these alternatives?
6. How does your method handle imbalanced datasets? Are there any modifications or techniques that you have employed to address this issue, and how do they affect the performance of your classifier?

### Rating

3

### Confidence

4

**********