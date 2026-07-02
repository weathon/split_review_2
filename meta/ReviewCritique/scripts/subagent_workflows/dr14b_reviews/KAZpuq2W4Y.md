### Summary

The paper introduces a novel method for whole-slide image (WSI) classification using multi-instance learning (MIL). The authors propose incorporating second-order statistical moments, specifically covariance matrices, into the MIL framework to capture the variability and inter-feature relationships among patches within a WSI. They also introduce an adaptive clustering approach using DBSCAN to group similar patches, allowing for variable-resolution processing that emphasizes rare pathological regions. The method, evaluated on two real-world WSI datasets, demonstrates improved performance over existing MIL baselines.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

1. The paper is well-organized and clearly written, making it easy to follow the proposed methodology and experimental results.

2. The authors provide a comprehensive ablation study that effectively demonstrates the contributions of each component of the HOMIL framework.

### Weaknesses

#### Some Related Works


#### comment

1. The novelty of the paper is limited. The proposed method appears to be a combination of existing approaches, and the authors do not sufficiently demonstrate how their method differs significantly from previous work.

2. The authors should provide a more detailed analysis of the computational complexity of their method compared to existing approaches, particularly concerning the calculation of second-order moments and the adaptive clustering process.

3. The authors should provide a more detailed analysis of the sensitivity of the method to the choice of hyperparameters, such as the epsilon parameter in DBSCAN and the number of clusters.

### Suggestions

The authors should more clearly articulate the novelty of their approach by explicitly contrasting it with existing methods, particularly those that also utilize covariance matrices or adaptive clustering techniques. A detailed comparison, highlighting the specific differences in how these components are integrated and utilized within the proposed framework, is needed. For instance, if other methods use covariance matrices, the authors should explain how their method's use of these matrices differs, such as in the way they are computed, aggregated, or used in the final classification. Similarly, if other methods employ adaptive clustering, the authors should clarify how their approach to clustering is unique, perhaps by focusing on the specific parameters or the way clustering is integrated into the overall MIL framework. This would help to establish the unique contribution of their work beyond a simple combination of existing techniques.

To address the computational complexity concerns, the authors should provide a more rigorous analysis, including a breakdown of the time complexity for each step of their method. This should include the feature extraction, covariance calculation, clustering, and classification stages. The analysis should not only consider the asymptotic complexity but also provide empirical evidence of the actual runtime on different datasets and with varying input sizes. Furthermore, the authors should compare the computational cost of their method with that of the baseline methods, providing a clear understanding of the trade-offs between performance and computational resources. This analysis should also consider the impact of different hardware configurations on the runtime, which would be beneficial for reproducibility and practical application of the method. A table summarizing the computational cost of each step for all methods would be beneficial.

Finally, a more thorough investigation of the hyperparameter sensitivity is needed. The authors should provide a detailed analysis of how the choice of epsilon in DBSCAN affects the clustering results and the final classification performance. This should include a range of epsilon values and a discussion of how the clustering behavior changes with different values. Similarly, the authors should analyze the impact of the number of clusters on the performance, even if the method is designed to automatically determine the number of clusters. It is important to understand how the method behaves under different clustering scenarios and how sensitive the final results are to the initial clustering parameters. This analysis should include visualizations of the clustering results for different parameter values to provide a more intuitive understanding of the method's behavior.

### Questions

1. How does the proposed method perform on other types of medical images or non-medical images? Can the method be generalized to other domains?

2. The authors should provide a more detailed analysis of the computational complexity of their method compared to existing approaches, particularly concerning the calculation of second-order moments and the adaptive clustering process.

3. The authors should provide a more detailed analysis of the sensitivity of the method to the choice of hyperparameters, such as the epsilon parameter in DBSCAN and the number of clusters.

### Rating

5

### Confidence

3

**********