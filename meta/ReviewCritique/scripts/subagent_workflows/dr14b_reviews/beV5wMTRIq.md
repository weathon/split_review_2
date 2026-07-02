### Summary

This paper presents a novel framework, Physics-Aware Tensor Field Neural PDE (PA-TFNP), designed for climate and weather prediction. PA-TFNP integrates rotation-equivariant tensor-field neural operators with a numerically rigorous gradient operator based on spherical transforms and physically consistent boundary treatment. The framework also incorporates diffusion terms derived from atmospheric primitive equations, enhancing its physical fidelity. The proposed model outperforms existing benchmarks, such as ClimODE, by a significant margin in global and regional weather prediction tasks.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel approach by combining tensor-field neural networks with physical principles, which is a significant advancement in the field of climate and weather prediction.
2. The authors provide a comprehensive evaluation of the PA-TFNP framework, demonstrating its superior performance across various climate and weather prediction tasks.
3. The paper is well-structured and clearly articulates the methodology, experiments, and results.

### Weaknesses

#### Some Related Works


#### comment

1. The paper could benefit from a more detailed discussion on the limitations of the proposed framework, particularly in terms of computational complexity and scalability. While the authors mention the computational efficiency of their model, a more rigorous analysis of the computational cost, including FLOPs and memory requirements, would be beneficial. Specifically, it would be useful to see a breakdown of the computational cost associated with each component of the PA-TFNP framework, such as the tensor-field neural operators and the spherical gradient operator. This would allow for a more informed comparison with existing numerical weather prediction models, which often have well-characterized computational profiles. Furthermore, the paper should discuss how the computational cost scales with increasing spatial resolution and the number of atmospheric variables being predicted. This is crucial for assessing the practical applicability of the method to high-resolution, large-scale climate simulations.

2. The paper primarily focuses on the application of PA-TFNP to weather and climate prediction. It would be interesting to explore the potential of this framework in other scientific computing domains. The current evaluation is limited to atmospheric variables, and it is unclear how well the framework would generalize to other physical systems governed by different PDEs. For example, it would be valuable to see experiments on fluid dynamics problems, such as incompressible flow or Navier-Stokes equations, or even on problems from other domains like heat transfer or electromagnetism. This would demonstrate the versatility of the proposed framework and its potential impact beyond climate modeling.

### Suggestions

To address the limitations regarding computational complexity, the authors should provide a more detailed analysis of the computational cost of their PA-TFNP framework. This should include a breakdown of the FLOPs and memory requirements for each component of the model, such as the tensor-field neural operators, the spherical gradient operator, and the diffusion dynamics. Furthermore, the authors should investigate how the computational cost scales with increasing spatial resolution and the number of atmospheric variables. This analysis should be presented in a tabular format, allowing for a direct comparison with existing numerical weather prediction models. For example, the authors could compare the computational cost of their model with that of a standard finite-difference or spectral method for solving the same set of equations. This would provide a more concrete understanding of the computational trade-offs associated with the proposed approach. Additionally, the authors should discuss the potential for optimizing the implementation of their framework to further reduce the computational cost, such as through the use of specialized hardware or parallel computing techniques.

To broaden the applicability of the PA-TFNP framework, the authors should explore its performance on a wider range of scientific computing problems. This could include experiments on fluid dynamics problems, such as simulating incompressible flow or solving the Navier-Stokes equations. The authors could also consider applying their framework to other physical systems governed by different PDEs, such as heat transfer or electromagnetism. This would demonstrate the versatility of the proposed approach and its potential impact beyond climate modeling. For each new application, the authors should provide a detailed description of the problem setup, the specific PDEs being solved, and the evaluation metrics used to assess the performance of the model. This would allow for a more comprehensive understanding of the strengths and limitations of the PA-TFNP framework in different scientific domains. Furthermore, the authors should discuss any modifications or adaptations that may be necessary to apply the framework to different types of PDEs or boundary conditions.

Finally, the authors should consider providing a more detailed discussion of the limitations of their approach. This should include a discussion of the assumptions made in the model, the potential for error accumulation over long prediction horizons, and the sensitivity of the model to different initial conditions. The authors should also discuss the potential for incorporating additional physical constraints or regularization techniques to improve the robustness and accuracy of the model. This would provide a more balanced and nuanced perspective on the capabilities and limitations of the PA-TFNP framework, and would help guide future research in this area.

### Questions

1. Can the authors provide more insights into the computational complexity of the PA-TFNP framework compared to traditional numerical weather prediction models?
2. How does the proposed framework handle uncertainty quantification in weather and climate predictions?
3. Are there any plans to extend the PA-TFNP framework to other scientific computing domains beyond weather and climate prediction?

### Rating

6

### Confidence

3

**********