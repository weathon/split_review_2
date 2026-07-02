### Summary

This paper proposes a unified Dimension Domain Co-Decomposition (3D) framework that integrates dimension decomposition with a Mixture-of-Experts (MoE) based domain decomposition for solving partial differential equations (PDEs) with physics-informed neural networks (PINNs). The proposed method achieves three key innovations: (i) an interpretable dimension decomposition strategy, (ii) a novel metric called Variable Interpretability (VI) that quantifies the alignment between the learned latent representations of each input dimension and their corresponding exact solution components, and (iii) an MoE-driven domain decomposition architecture that automatically partitions the solution space without requiring predefined regions or interface conditions.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed method is well-motivated and achieves improved computational efficiency and solution accuracy across a range of high-dimensional PDE benchmarks.
2. The proposed method is interpretable and scalable, making it a promising approach for solving complex PDEs.
3. The paper is well-written and easy to follow.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method is only evaluated on a limited number of PDE benchmarks. It would be beneficial to see how the method performs on a wider range of problems, including those with more complex geometries and boundary conditions. The current benchmarks, while demonstrating the core concepts, do not fully explore the method's robustness in more realistic scenarios.
2. The paper does not provide a detailed analysis of the computational cost of the proposed method compared to existing approaches. This makes it difficult to assess the practical applicability of the method in real-world scenarios. A more thorough breakdown of the computational resources required, such as memory usage and training time, is needed to understand the method's efficiency.
3. The paper does not discuss the limitations of the proposed method in detail. For example, it is unclear how the method would perform on problems with highly non-smooth solutions or solutions with multiple scales. The sensitivity of the method to hyperparameter choices, particularly those related to the MoE architecture and the dimension decomposition, should also be addressed.
4. The proposed method relies on the availability of reference solutions for computing the Variable Interpretability (VI) metric. This may not always be the case in practice, especially when dealing with complex problems where analytical solutions are not available. The reliance on a reference solution limits the applicability of the VI metric in purely data-driven settings.

### Suggestions

To strengthen the evaluation of the proposed method, it is crucial to expand the range of PDE benchmarks considered. This should include problems with more complex geometries, such as those involving irregular domains or curved boundaries, and problems with more challenging boundary conditions, such as time-dependent or non-homogeneous conditions. Furthermore, the method should be tested on PDEs with varying degrees of nonlinearity and stiffness to assess its robustness and generalizability. For example, the method could be applied to problems arising in fluid dynamics, such as the Navier-Stokes equations, or in heat transfer, such as the heat equation with variable thermal conductivity. These additional benchmarks would provide a more comprehensive understanding of the method's capabilities and limitations.

A detailed analysis of the computational cost is essential for assessing the practical applicability of the proposed method. This analysis should include a breakdown of the computational resources required, such as memory usage, training time, and inference time, as a function of the problem size and complexity. A comparison with existing methods, such as standard PINNs and other domain decomposition techniques, should be provided to demonstrate the efficiency of the proposed approach. This comparison should consider both the absolute computational cost and the scaling behavior with respect to the problem dimension and the number of training data points. Furthermore, the analysis should investigate the impact of different hyperparameter choices on the computational cost, such as the number of experts in the MoE architecture and the rank of the dimension decomposition.

The limitations of the proposed method should be discussed in more detail, including its performance on problems with highly non-smooth solutions, solutions with multiple scales, and its sensitivity to hyperparameter choices. The method's behavior in the presence of discontinuities or sharp gradients should be investigated, and strategies for improving its performance in such cases should be explored. For example, adaptive mesh refinement or specialized activation functions could be considered. The sensitivity of the method to hyperparameter choices, particularly those related to the MoE architecture and the dimension decomposition, should also be addressed. A systematic study of the impact of different hyperparameter values on the solution accuracy and computational cost should be performed to provide guidance on how to choose appropriate values for different problems.

### Questions

1. How does the proposed method perform on problems with highly non-smooth solutions or solutions with multiple scales?
2. How sensitive is the proposed method to the choice of hyperparameters, such as the number of experts in the MoE architecture and the rank of the dimension decomposition?
3. How does the proposed method compare to other state-of-the-art methods for solving PDEs with PINNs in terms of computational cost and solution accuracy?

### Rating

6

### Confidence

3

**********