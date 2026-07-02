### Summary

This paper proposes a novel framework for continual spatio-temporal forecasting, called STBP, which combines a general spatio-temporal backbone with a scalable contextual pattern bank. The backbone is designed to handle distributional drift and model spatio-temporal correlations, while the contextual pattern bank is used to mitigate catastrophic forgetting and adapt to new scenarios. The proposed method is evaluated on three real-world datasets, and the results show that it outperforms state-of-the-art baselines in terms of forecasting accuracy and scalability.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed STBP framework is a novel approach to continual spatio-temporal forecasting that combines a general spatio-temporal backbone with a scalable contextual pattern bank.
2. The proposed method is evaluated on three real-world datasets, and the results show that it outperforms state-of-the-art baselines in terms of forecasting accuracy and scalability.
3. The paper is well-written and easy to follow, with clear explanations of the proposed method and experimental results.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed STBP framework is a novel approach to continual spatio-temporal forecasting that combines a general spatio-temporal backbone with a scalable contextual pattern bank.
2. The proposed method is evaluated on three real-world datasets, and the results show that it outperforms state-of-the-art baselines in terms of forecasting accuracy and scalability.
3. The paper is well-written and easy to follow, with clear explanations of the proposed method and experimental results.

1. The proposed STBP framework is a novel approach to continual spatio-temporal forecasting that combines a general spatio-temporal backbone with a scalable contextual pattern bank.
2. The proposed method is evaluated on three real-world datasets, and the results show that it outperforms state-of-the-art baselines in terms of forecasting accuracy and scalability.
3. The paper is well-written and easy to follow, with clear explanations of the proposed method and experimental results.

### Suggestions

The paper introduces a novel framework for continual spatio-temporal forecasting, which is a valuable contribution. However, the evaluation could be strengthened by including a more diverse set of datasets, particularly those with more complex spatial dependencies and temporal dynamics. The current datasets, while real-world, might not fully capture the challenges of highly dynamic or irregular spatio-temporal patterns. For example, datasets with more frequent missing data or abrupt changes in the underlying patterns could provide a more rigorous test of the proposed method's robustness and adaptability. Furthermore, the paper could benefit from a more detailed analysis of the computational cost associated with the proposed method, especially in comparison to the baselines. While the paper mentions scalability, a more quantitative analysis of the time and memory requirements would be beneficial for practical applications. This analysis should include a breakdown of the computational cost of each component of the STBP framework, such as the spatio-temporal backbone and the contextual pattern bank, to better understand the trade-offs between accuracy and efficiency.

Additionally, the paper could explore the sensitivity of the proposed method to different hyperparameter settings. The performance of the STBP framework might be highly dependent on the choice of hyperparameters, and a thorough sensitivity analysis would be valuable for practitioners. This analysis should include a discussion of the optimal range of hyperparameters for different datasets and scenarios. Furthermore, the paper could provide more insights into the interpretability of the learned patterns. While the contextual pattern bank is designed to mitigate catastrophic forgetting, it is not clear how these patterns are related to the underlying spatio-temporal dynamics. A visualization or analysis of the learned patterns could provide a better understanding of the model's behavior and its ability to capture meaningful information. This could involve techniques such as attention visualization or feature importance analysis.

Finally, the paper could benefit from a more detailed discussion of the limitations of the proposed method. While the paper demonstrates the effectiveness of STBP on several datasets, it is important to acknowledge the scenarios where the method might not perform well. For example, the paper could discuss the potential challenges of applying STBP to very large-scale datasets or datasets with highly non-stationary patterns. A discussion of these limitations would provide a more balanced view of the proposed method and guide future research directions. Furthermore, the paper could explore the potential for extending the proposed framework to other types of spatio-temporal data, such as those with non-Euclidean spatial structures or those with multi-resolution temporal scales. This would broaden the applicability of the proposed method and highlight its potential for future research.

### Questions

1. How does the proposed STBP framework compare to other state-of-the-art methods in terms of computational complexity and memory requirements?
2. How does the proposed STBP framework handle missing data or noisy data in the input time series?
3. How does the proposed STBP framework perform on datasets with more complex spatial dependencies or temporal dynamics?

### Rating

6

### Confidence

3

**********