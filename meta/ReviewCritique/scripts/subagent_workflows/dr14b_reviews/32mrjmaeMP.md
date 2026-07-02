### Summary

The paper proposes a novel method for task arithmetic without requiring access to task-specific data. The authors achieve this by formulating the problem as a curvature matrix approximation, specifically using the Kronecker-Factored Approximate Curvature (KFAC) approach. This allows for effective task vector composition and negation while maintaining performance and mitigating cross-task interference.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The use of KFAC for dataless task arithmetic is innovative and addresses key limitations in existing methods, such as data dependency and computational complexity.
2. The paper provides comprehensive experiments across multiple benchmarks, demonstrating that TAK outperforms state-of-the-art methods in both task addition and negation.
3. The method’s robustness to task vector rescaling and its ability to maintain performance across different task combinations enhance its appeal for practical applications.

### Weaknesses

#### Some Related Works


#### comment

1. The method’s reliance on linearization may limit its effectiveness in highly non-linear models or tasks. The approximation of the loss landscape using a linearized version of the network may not accurately capture the true curvature, especially when the task-specific updates are large enough to move the parameters significantly away from the pre-trained point. This could lead to suboptimal task vectors and reduced performance in scenarios where non-linearities play a crucial role.
2. The approach may involve complex implementation steps, particularly in aggregating per-task curvature factors. While the paper describes the aggregation process, the practical details of efficiently computing and storing the KFAC approximations, especially for large models, could pose challenges. The process of inverting or decomposing the Kronecker factors for each task and then merging them might introduce computational bottlenecks and require careful memory management.
3. The paper does not fully explore the potential trade-offs in terms of computational efficiency for very large models or tasks with high dimensionality. Although the authors mention that the method scales linearly with the number of parameters, the actual computational cost of calculating and applying the KFAC approximations, which involves matrix operations on the layer-wise curvature matrices, could still be substantial for very large models. Furthermore, the memory footprint of storing the KFAC factors for multiple tasks could become a limiting factor.

### Suggestions

The paper introduces an interesting approach to task arithmetic using KFAC, but there are several areas where further investigation and clarification would strengthen the work. First, while the authors acknowledge the reliance on linearization, a more thorough analysis of its limitations is needed. Specifically, the paper should include experiments that quantify the performance degradation as the magnitude of task-specific updates increases, moving further away from the linear regime. This could involve measuring the curvature of the loss landscape along the task update directions and comparing it to the linear approximation. Additionally, exploring alternative curvature approximations that better capture non-linearities, such as higher-order Taylor expansions or methods based on empirical gradients, could be beneficial. This would help to understand the trade-offs between computational cost and accuracy of the curvature approximation.

Second, the paper should provide more details on the practical implementation of the KFAC aggregation. While the authors mention that the method scales linearly with the number of parameters, the constant factor associated with the matrix operations could be significant for large models. A detailed breakdown of the computational cost of each step, including the calculation of the Jacobian and Hessian approximations, the Kronecker factorization, and the merging of per-task factors, would be valuable. Furthermore, the paper should discuss the memory requirements for storing the KFAC factors, especially when dealing with multiple tasks. Exploring techniques for reducing the memory footprint, such as low-rank approximations or compression methods, would be beneficial. The authors could also consider providing a reference implementation to facilitate the adoption of their method by the community.

Finally, the paper should include a more comprehensive analysis of the computational efficiency of the method, particularly for very large models and high-dimensional tasks. This should include a comparison of the training time and memory usage of the proposed method with existing task arithmetic techniques. The authors should also investigate the impact of the number of tasks on the computational cost and memory requirements. It would be useful to see how the method scales with an increasing number of tasks and whether there are any practical limitations in terms of the number of tasks that can be handled. This analysis should be performed on a range of model sizes and task complexities to provide a more complete picture of the method's applicability.

### Questions

1. How does the method perform when applied to highly non-linear tasks or models? Are there specific domains where the linearization assumption may not hold?
2. Can the authors provide more details on the computational overhead introduced by KFAC regularization, particularly for very large models or datasets?
3. How does the method handle scenarios with a large number of tasks? Is there a point at which the complexity or memory requirements become prohibitive?

### Rating

6

### Confidence

3

**********