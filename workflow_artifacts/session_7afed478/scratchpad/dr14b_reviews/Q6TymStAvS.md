### Summary

This paper proposes a novel method for learning the ground states of quantum many-body systems by leveraging geometric considerations in the flow matching framework. The authors introduce two approaches: a Riemannian-based method that incorporates the geometry of the Bloch sphere and an anisotropic probability path-based method that respects the asymmetric structure of shadows. The method is evaluated on the transverse-field Ising model and the Heisenberg model, demonstrating improved accuracy in predicting observables compared to existing methods.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and clearly explains the motivation behind incorporating geometric considerations into the flow matching framework.

2. The proposed method is novel and addresses a significant challenge in learning quantum many-body systems.

3. The experimental results demonstrate the effectiveness of the proposed method in predicting observables for both the transverse-field Ising model and the Heisenberg model.

### Weaknesses

#### Some Related Works


#### comment

1. The paper lacks a detailed discussion of the computational complexity of the proposed method, especially in comparison to existing approaches. It would be beneficial to provide a more thorough analysis of the computational cost associated with the Riemannian-based and anisotropic probability path-based methods, including the number of parameters, training time, and inference time. A comparison with the computational cost of methods like Diff-LM, which is mentioned as a baseline, would be particularly valuable. Furthermore, the analysis should consider the scaling of computational cost with system size, which is crucial for assessing the method's applicability to larger quantum systems.

2. The paper could benefit from a more in-depth analysis of the limitations of the proposed method. For example, it would be helpful to discuss the potential challenges in applying the method to more complex quantum systems or to systems with different types of interactions. Specifically, the paper should address how the geometric considerations might break down or become less effective in systems with long-range interactions or strong correlations. Additionally, a discussion on the sensitivity of the method to the choice of geometric parameters or the initialization of the flow matching process would be beneficial.

### Suggestions

To address the lack of computational complexity analysis, the authors should include a detailed breakdown of the computational cost for both the Riemannian-based and anisotropic probability path-based methods. This should include the number of parameters in the model, the time required for training, and the time required for inference. The analysis should also consider the scaling of these costs with respect to the system size, such as the number of qubits. A comparison with the computational cost of existing methods, such as Diff-LM, should be provided, highlighting the trade-offs between accuracy and computational efficiency. This comparison should not only focus on the overall time but also on the memory requirements and the parallelizability of the different methods. Furthermore, the authors should discuss the potential bottlenecks in their method and how these might be addressed in future work. For example, if the computation of the geodesic paths on the Bloch sphere is a bottleneck, the authors should discuss potential approximations or optimizations that could be used to reduce the computational cost.

To improve the analysis of the method's limitations, the authors should discuss the potential challenges in applying the method to more complex quantum systems. This should include a discussion of how the geometric considerations might break down or become less effective in systems with long-range interactions, strong correlations, or different types of symmetries. For example, the authors could discuss how the choice of the Riemannian metric on the Bloch sphere might affect the performance of the method in different systems. Additionally, the authors should analyze the sensitivity of the method to the choice of geometric parameters, such as the curvature of the manifold, and the initialization of the flow matching process. This analysis should include a discussion of how these parameters can be tuned to optimize the performance of the method and how the method might fail if these parameters are not chosen appropriately. The authors should also consider the potential for the method to be extended to mixed quantum states, which would be a significant step forward in the field.

Finally, the authors should provide a more detailed discussion of the experimental setup, including the specific choices of hyperparameters and the details of the training process. This should include a discussion of how the hyperparameters were chosen and how they affect the performance of the method. The authors should also provide a more detailed analysis of the experimental results, including a discussion of the statistical significance of the results and the potential sources of error. This would help to ensure that the results are reproducible and that the conclusions drawn from the experiments are well-supported by the data.

### Questions

1. Could the authors provide a more detailed analysis of the computational complexity of the proposed method compared to existing approaches?

2. How does the proposed method perform on larger quantum systems or systems with different types of interactions?

### Rating

6

### Confidence

3

**********