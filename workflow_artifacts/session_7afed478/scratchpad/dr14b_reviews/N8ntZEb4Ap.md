### Summary

This paper proposes AutoNFS, a neural network-based approach for automatic feature selection. It combines a masking network with Gumbel-Sigmoid sampling and a predictive model to evaluate feature relevance. The model is trained end-to-end using a differentiable loss, automatically determining the minimal set of features needed for a downstream task. AutoNFS achieves a nearly constant computational overhead, regardless of input dimensionality, making it scalable to large data spaces. The authors evaluate AutoNFS on classification and regression benchmarks, as well as real-world metagenomic datasets, showing that it consistently outperforms existing methods while selecting fewer features.

### Soundness

3

### Presentation

3

### Contribution

2

### Strengths

1. The proposed AutoNFS is a novel neural network for end-to-end feature selection, leveraging Gumbel-Sigmoid relaxation and a regularization term that penalizes the number of selected features.
2. The paper is well-written and easy to follow.
3. The authors provide a comprehensive evaluation of AutoNFS on various datasets, demonstrating its effectiveness and scalability.

### Weaknesses

#### Some Related Works


#### comment

1. The novelty of the proposed method is limited. The proposed method is a combination of existing methods.
2. The proposed method is not compared with existing methods on a wide range of datasets.

### Suggestions

The paper's primary weakness lies in its limited novelty. While the combination of a masking network with Gumbel-Sigmoid sampling and a task network is functional, it doesn't introduce a fundamentally new approach to feature selection. The core idea of using a differentiable mask for feature selection has been explored in various contexts, and the specific implementation here, while effective, doesn't represent a significant leap forward. To strengthen the contribution, the authors should explore more innovative masking mechanisms or demonstrate how their specific combination of existing techniques leads to unique advantages not achievable with other methods. For example, they could investigate adaptive masking strategies that dynamically adjust based on the task or dataset characteristics, or explore the use of more sophisticated regularization techniques beyond a simple penalty on the number of selected features. Furthermore, a more detailed analysis of the method's sensitivity to hyperparameter settings, particularly the temperature parameter in the Gumbel-Sigmoid, would be beneficial.

To address the lack of comprehensive evaluation, the authors should expand their experimental setup to include a wider range of datasets with varying characteristics. The current evaluation, while demonstrating the method's effectiveness on corrupted features and metagenomic data, does not provide a complete picture of its general applicability. Specifically, the inclusion of datasets with different feature dimensionalities, class imbalances, and noise levels would be crucial to assess the robustness of the proposed method. Furthermore, the comparison with existing methods should be more extensive, including a wider range of feature selection techniques, such as those based on information theory or spectral methods. This would provide a more comprehensive understanding of the method's strengths and weaknesses relative to the state-of-the-art. The authors should also consider reporting the computational cost of their method compared to other approaches, as this is an important factor in practical applications.

Finally, the paper would benefit from a more in-depth analysis of the selected features. While the authors demonstrate that their method selects fewer features, they do not provide much insight into the characteristics of these features or their importance for the task at hand. A more detailed analysis of the selected features, such as their distribution, correlation with the target variable, or their biological relevance in the metagenomic datasets, would provide a deeper understanding of the method's behavior and its potential for practical applications. This analysis could also help to identify potential biases or limitations of the method. For example, it would be interesting to see if the method tends to select features that are highly correlated with each other, or if it is able to identify features that are truly informative for the task.

### Questions

1. How does the proposed method compare to existing feature selection methods in terms of computational efficiency and scalability?
2. Can the authors provide more insights into the interpretability of the selected features and how they relate to the downstream tasks?

### Rating

6

### Confidence

3

**********