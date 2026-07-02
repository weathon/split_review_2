### Summary

This paper addresses a gap in neural combinatorial optimization (NCO) by tackling the challenge of handling asymmetric distance matrices in vehicle routing problems (VRPs). Traditional NCO models assume symmetric distances, limiting their real-world applicability where routing is affected by factors like one-way streets and traffic. The authors propose RADAR, a framework that enhances neural VRP solvers with asymmetry-aware embeddings. RADAR uses Singular Value Decomposition (SVD) to initialize embeddings that capture static asymmetry and Sinkhorn normalization to model dynamic asymmetry in attention mechanisms. Extensive experiments show that RADAR outperforms existing methods on both synthetic and real-world benchmarks, demonstrating robust generalization and superior performance in asymmetric VRPs.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-organized and easy to follow. The authors clearly articulate the problem of handling asymmetric distance matrices in VRPs and provide a comprehensive overview of related work, which helps contextualize their contributions.

2. The proposed RADAR framework is innovative in its use of SVD for initialization and Sinkhorn normalization for attention mechanisms. These techniques are well-justified and effectively address the challenges of modeling both static and dynamic asymmetries.

3. The empirical evaluation is thorough, with experiments on synthetic and real-world datasets demonstrating the effectiveness of RADAR across various VRP variants. The results show consistent improvements over baselines, highlighting the practical significance of the approach.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion of the limitations of the proposed approach, particularly in scenarios where the asymmetry is not well-captured by the SVD initialization or where Sinkhorn normalization may not be sufficient to model dynamic asymmetries. For instance, the reliance on SVD might struggle with distance matrices that have a low-rank structure or where the asymmetry is highly localized and not globally consistent. Similarly, the Sinkhorn normalization, while effective for balancing attention, might not fully capture complex, non-linear interactions that arise in highly asymmetric routing scenarios. A more thorough analysis of these failure modes would be valuable.

2. While the paper focuses on asymmetric VRPs, a more detailed analysis of the computational overhead introduced by the SVD and Sinkhorn normalization would be useful. Specifically, the paper lacks a detailed breakdown of the time complexity of these operations, especially in relation to the size of the input distance matrix. It would be beneficial to understand how the computational cost scales with the number of nodes and edges, and whether the proposed method remains practical for large-scale instances. A comparison of the runtime with and without these components would also be insightful.

3. The paper could explore the sensitivity of the model to hyperparameters, such as the number of singular values used in the SVD initialization and the parameters of the Sinkhorn normalization. Providing guidelines or a sensitivity analysis for these choices would enhance the reproducibility and practical applicability of the proposed method. For example, how does the performance vary with different numbers of singular values, and what is the impact of the regularization parameter in the Sinkhorn normalization? A more detailed exploration of these aspects would be beneficial.

### Suggestions

To strengthen the paper, the authors should delve deeper into the limitations of their approach, particularly concerning the SVD initialization and Sinkhorn normalization. The current discussion is somewhat superficial, and a more rigorous analysis is needed. For example, the authors could explore scenarios where the distance matrix has a low-rank structure, which might not be well-represented by a truncated SVD. They could also investigate cases where the asymmetry is highly localized, such as in urban areas with many one-way streets, and analyze how well the global SVD captures these local variations. Furthermore, the authors should consider the impact of noise in the distance matrix on the SVD initialization and how this might affect the overall performance. A more detailed analysis of these failure modes would provide a more complete picture of the method's applicability and limitations.

In addition, the authors should provide a more detailed analysis of the computational overhead introduced by the SVD and Sinkhorn normalization. The current discussion lacks a thorough breakdown of the time complexity of these operations, especially in relation to the size of the input distance matrix. It would be beneficial to understand how the computational cost scales with the number of nodes and edges, and whether the proposed method remains practical for large-scale instances. A comparison of the runtime with and without these components would also be insightful. The authors could also explore alternative methods for approximating the SVD or Sinkhorn normalization to reduce the computational burden, such as using randomized SVD techniques or iterative methods for Sinkhorn normalization. This would make the method more practical for real-world applications.

Finally, the authors should conduct a more thorough sensitivity analysis of the model's hyperparameters. Specifically, they should explore how the performance varies with different numbers of singular values used in the SVD initialization and the regularization parameter in the Sinkhorn normalization. Providing guidelines or a sensitivity analysis for these choices would enhance the reproducibility and practical applicability of the proposed method. For example, the authors could perform a grid search over a range of hyperparameter values and report the performance metrics for each combination. This would provide valuable insights into the robustness of the method and help practitioners choose appropriate hyperparameter values for their specific applications. Furthermore, the authors should investigate the impact of different initialization strategies and normalization techniques on the model's performance and provide a rationale for their choices.

### Questions

1. How does the model handle cases where the asymmetry in the distance matrix is not consistent or has discontinuities? Is there a sensitivity analysis on the impact of such irregular asymmetries?

2. Can the authors provide more insights into the choice of hyperparameters for the SVD and Sinkhorn normalization? How sensitive is the model's performance to these choices?

3. The paper mentions that RADAR outperforms baselines on real-world datasets. Could the authors elaborate on the characteristics of these datasets and how they reflect real-world routing challenges?

4. How does the model perform when the input distance matrix is noisy or contains errors? Is there any robustness analysis to assess the model's performance under such conditions?

### Rating

6

### Confidence

4

**********