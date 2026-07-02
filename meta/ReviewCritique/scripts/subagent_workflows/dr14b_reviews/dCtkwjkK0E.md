### Summary

The paper presents a study on active learning for flow matching models, a type of generative model that has shown great promise in various applications. The authors analyze the generalization error of flow matching models using a piecewise-linear neural network framework. They propose two query strategies: one aimed at enhancing model diversity and the other at improving model accuracy. They also introduce a hybrid strategy that combines the two. The paper evaluates the proposed strategies on multiple datasets and shows that they outperform standard active learning methods designed for discriminative models.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel application of active learning to flow matching models, which is a unique and valuable contribution to the field.
2. The authors provide a thorough theoretical analysis, using a piecewise-linear neural network framework to explain how data points influence model diversity and accuracy, which strengthens the credibility of the proposed methods.
3. The proposed query strategies are shown to outperform traditional active learning methods, offering a practical solution for improving both diversity and accuracy in model training.

### Weaknesses

#### Some Related Works


#### comment

1. The paper assumes that flow matching models can be effectively represented as piecewise-linear neural networks, which may not hold in all practical scenarios. This assumption is critical to the theoretical framework, and its potential violation could significantly impact the validity of the proposed query strategies. Specifically, the flow matching model's reliance on complex, non-linear transformations might not be adequately captured by a piecewise-linear approximation, especially when the underlying data distribution is highly complex or when the model depth is significant. This could lead to a mismatch between the theoretical analysis and the actual model behavior.
2. The approach may face scalability challenges when applied to very large datasets, as the query strategies involve complex calculations that could be computationally intensive. The computational burden arises from the need to evaluate the diversity and accuracy metrics for each potential query point, which could become prohibitive for high-dimensional data or large unlabeled pools. The paper does not provide a detailed analysis of the computational complexity of the proposed methods, making it difficult to assess their practicality for large-scale applications.
3. The effectiveness of the diversity-based query strategy relies on the quality of the RBF network used for label prediction, which could introduce variability in performance. The RBF network's ability to accurately predict labels for unlabeled data points is crucial for the diversity strategy to work effectively. If the RBF network is not well-tuned or if the data has complex non-linear relationships, the label predictions could be inaccurate, leading to suboptimal query point selection and potentially degrading the overall performance of the active learning framework.

### Suggestions

The paper's core contribution lies in its novel application of active learning to flow matching models, which is a significant step given the high cost of labeling data in this domain. However, the theoretical framework relies on the assumption that flow matching models can be effectively represented as piecewise-linear neural networks. While this assumption simplifies the analysis, it may not hold in all practical scenarios, particularly when dealing with complex data distributions or deep models. To address this, the authors should provide a more detailed analysis of the limitations of this assumption and explore potential alternatives or extensions that could accommodate more complex model behaviors. For example, they could investigate the impact of approximation errors on the performance of the proposed query strategies or consider using more sophisticated function approximation techniques that can capture non-linearities more accurately. Furthermore, it would be beneficial to include experiments that explicitly test the validity of the piecewise-linear assumption under different conditions, such as varying model depth and data complexity.

Another area that requires further attention is the computational scalability of the proposed query strategies. The paper mentions that the strategies involve complex calculations, but it does not provide a detailed analysis of their computational complexity. This is a critical issue, as the proposed methods may not be practical for very large datasets or high-dimensional data. To address this, the authors should provide a thorough analysis of the computational complexity of their methods and explore potential techniques for improving their scalability. For example, they could investigate the use of approximation algorithms or parallel computing techniques to reduce the computational burden. Additionally, it would be helpful to include experiments that evaluate the performance of the proposed methods on large-scale datasets and compare their computational efficiency with existing active learning methods. This would provide a more comprehensive understanding of the practical limitations of the proposed approach.

Finally, the paper's diversity-based query strategy relies on the quality of the RBF network used for label prediction. The performance of this strategy is highly dependent on the accuracy of the RBF network's predictions, and any inaccuracies could lead to suboptimal query point selection. To address this, the authors should provide a more detailed analysis of the sensitivity of their method to the choice of RBF network parameters and explore alternative methods for label prediction. For example, they could investigate the use of other types of neural networks or kernel methods for label prediction. Additionally, it would be helpful to include experiments that explicitly test the impact of RBF network accuracy on the performance of the diversity-based query strategy. This would provide a more robust evaluation of the proposed method and help to identify potential limitations.

### Questions

1. How robust is the piecewise-linear approximation for flow matching models across different datasets and conditions?
2. Can the authors provide more insights into the computational efficiency of the proposed query strategies when applied to large-scale datasets?
3. How sensitive is the diversity-based query strategy to the choice of RBF network parameters, and could other methods for label prediction be equally effective?

### Rating

6

### Confidence

3

**********