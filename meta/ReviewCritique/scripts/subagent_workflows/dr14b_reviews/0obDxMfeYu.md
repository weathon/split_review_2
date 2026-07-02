### Summary

This paper presents a method for identifying outliers in unlabeled data using the median operation. The authors claim that the median provides a stable estimate of the central tendency, as an OOD detection mechanism, due to its robustness against noise and outliers. The paper also includes a theoretical analysis and empirical results to support the proposed method.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

The paper provides a theoretical analysis of the proposed method, which adds to the credibility of the approach.

### Weaknesses

#### Some Related Works


#### comment

 - The paper could benefit from a more thorough comparison with existing methods. While the authors mention that their method is more flexible than some existing approaches, they do not provide a detailed comparison of the performance of their method with these approaches on various datasets. Specifically, the paper lacks a comparison with methods that also leverage unlabeled data for OOD detection, making it difficult to assess the true novelty and performance gains of the proposed approach. A more comprehensive evaluation should include a variety of datasets with different characteristics and OOD scenarios, and should also consider the computational cost and sensitivity to hyperparameter settings of the proposed method compared to existing techniques.
- The paper could benefit from a more detailed discussion of the limitations of the proposed method. For example, how does the method perform when the outliers are not well-separated from the in-distribution data? Are there any specific types of outliers that the method is not able to identify? The paper should also discuss the potential impact of the choice of the median operation on the performance of the method, and whether other robust statistical measures could be more appropriate in certain situations. Furthermore, the paper should address the potential sensitivity of the method to the quality and quantity of the unlabeled data used for outlier detection.

### Suggestions

The paper should include a more comprehensive experimental evaluation that compares the proposed method with a wider range of existing OOD detection techniques, particularly those that also utilize unlabeled data. This comparison should not only focus on performance metrics such as FPR95 and AUROC, but also on computational efficiency and robustness to different hyperparameter settings. The evaluation should include datasets with varying degrees of out-of-distribution shift and different types of outliers, such as those that are close to the in-distribution data or those that form complex patterns. Furthermore, the paper should provide a detailed analysis of the performance of the proposed method under different conditions, such as varying amounts of unlabeled data and different levels of noise in the data. This would help to better understand the strengths and weaknesses of the method and its applicability to different real-world scenarios.

The paper should also include a more in-depth discussion of the limitations of the proposed method. This discussion should address the sensitivity of the method to the quality and quantity of the unlabeled data, as well as the potential impact of the choice of the median operation on the performance of the method. The authors should explore whether other robust statistical measures, such as the trimmed mean or M-estimators, could be more appropriate in certain situations. Additionally, the paper should discuss the potential challenges of applying the method to high-dimensional data and the computational cost associated with calculating the median in such cases. The authors should also consider the potential for adversarial attacks that could exploit the reliance on the median operation for outlier detection.

Finally, the paper should provide more practical guidance on how to apply the proposed method in real-world scenarios. This should include recommendations on how to select the appropriate parameters for the method, how to preprocess the data, and how to interpret the results. The authors should also discuss the potential challenges of deploying the method in resource-constrained environments and provide suggestions on how to address these challenges. The paper should also include a discussion of the potential ethical implications of using the proposed method for outlier detection, particularly in sensitive applications such as healthcare or finance.

### Questions

- The paper mentions that the median provides a stable estimate of the central tendency, as an OOD detection mechanism, due to its robustness against noise and outliers. Can you provide more details on how the median operation helps in identifying outliers in the data? How does it compare to other methods for outlier detection?
- The paper mentions that the proposed method is more flexible than some existing approaches. Can you provide more details on the specific assumptions that the proposed method does not make, and how this makes it more flexible?

### Rating

3

### Confidence

3

**********