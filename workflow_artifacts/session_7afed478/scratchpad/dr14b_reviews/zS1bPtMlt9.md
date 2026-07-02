### Summary

This paper introduces REPL, a novel framework for enhancing pseudo-label quality in semi-supervised LiDAR semantic segmentation. The key innovation lies in identifying and correcting potential errors in pseudo-labels through masked reconstruction and a dedicated training strategy. The authors provide a theoretical analysis demonstrating the conditions under which pseudo-label refinement is beneficial and empirically validate these conditions on two benchmark datasets: nuScenes-lidarseg and SemanticKITTI. The results show that REPL significantly improves pseudo-label quality and achieves state-of-the-art performance in LiDAR semantic segmentation tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper presents a novel approach to pseudo-label refinement in semi-supervised learning, specifically tailored for LiDAR semantic segmentation. The integration of masked reconstruction with a teacher-student network is a creative solution to the problem of noisy pseudo-labels.
2. The theoretical analysis provided is rigorous and supports the empirical findings. The authors demonstrate that the conditions for the effectiveness of pseudo-label refinement are mild and easily met in practice.
3. The empirical evaluation is extensive, covering two major benchmarks in the field. The results show consistent improvements over existing methods, particularly in scenarios with limited labeled data.
4. The ablation studies are thorough and provide insights into the contribution of each component of the framework. The analysis of the error candidate mask quality and the impact of random masking are particularly noteworthy.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed method. For instance, the performance of REPL might be sensitive to the choice of hyperparameters, such as the confidence percentile (κ) used for identifying unreliable voxels. A more thorough sensitivity analysis would strengthen the paper.
2. While the paper demonstrates strong performance on nuScenes-lidarseg and SemanticKITTI, it would be valuable to see how REPL performs on other datasets or in different settings, such as with different LiDAR sensors or in more complex environments. This would help to establish the generalizability of the approach.
3. The computational cost of the proposed method is not thoroughly discussed. While the paper mentions the additional overhead of the refiner, a more detailed analysis of the computational complexity and memory requirements would be beneficial, especially for practical applications.

### Suggestions

The paper would benefit from a more in-depth analysis of the hyperparameter sensitivity, particularly regarding the confidence percentile (κ). While the paper mentions this parameter, a more detailed exploration of its impact on performance across different datasets and scenarios is needed. For example, the authors could investigate how the optimal value of κ varies with the amount of labeled data or the complexity of the scene. A sensitivity analysis could involve systematically varying κ and observing the resulting changes in segmentation accuracy, perhaps visualized through plots showing performance curves. This would provide a clearer understanding of the robustness of the method and offer practical guidance for users on how to select appropriate values for their specific applications. Furthermore, it would be beneficial to explore adaptive strategies for setting κ, rather than relying on a fixed value, which could potentially improve the method's performance across diverse conditions.

To further strengthen the paper, the authors should consider evaluating the proposed method on a wider range of datasets and scenarios. While nuScenes-lidarseg and SemanticKITTI are standard benchmarks, they may not fully represent the diversity of real-world LiDAR data. Testing on datasets with different sensor characteristics, such as varying point densities or noise levels, would provide a more comprehensive assessment of the method's generalizability. Additionally, evaluating the method in more complex environments, such as those with heavy occlusions or dynamic objects, would be valuable. This could involve using datasets that include more challenging scenarios or creating synthetic datasets that simulate these conditions. Such evaluations would help to identify potential limitations of the method and provide insights into its applicability in different real-world settings. It would also be beneficial to compare the performance of REPL with other state-of-the-art semi-supervised methods on these additional datasets to further demonstrate its effectiveness.

Finally, a more detailed analysis of the computational cost of the proposed method is needed. While the paper mentions the additional overhead of the refiner, a more thorough analysis of the computational complexity and memory requirements would be beneficial. This should include a breakdown of the time and memory costs associated with each component of the framework, such as the teacher network, student network, and refiner. The authors should also compare the computational cost of REPL with other state-of-the-art semi-supervised methods. This analysis should be performed on a standard hardware setup and should include metrics such as training time, inference time, and memory usage. This would provide a clearer understanding of the practical implications of using the proposed method and help users to make informed decisions about its applicability in resource-constrained environments.

### Questions

1. Could the authors provide more details on the sensitivity of the method to the choice of hyperparameters, particularly the confidence percentile (κ)? How does the performance vary with different values of κ?
2. How does the method perform on datasets other than nuScenes-lidarseg and SemanticKITTI? Are there any plans to evaluate the approach on more diverse or challenging datasets?
3. Can the authors provide a more detailed analysis of the computational cost of the proposed method, including training time, inference time, and memory usage? How does it compare to other state-of-the-art methods?

### Rating

6

### Confidence

4

**********